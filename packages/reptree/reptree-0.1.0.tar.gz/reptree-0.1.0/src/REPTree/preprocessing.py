"""
Data preprocessing pipeline for tree models.
"""

import warnings
from typing import Dict, List, Literal, Optional, Tuple, Union

import numpy as np


class DataPreprocessor:
    """
    Complete data preprocessing pipeline for tree models.

    Handles numerical and categorical features, missing values,
    outliers, and feature encoding.

    Parameters
    ----------
    handle_missing : {'mean', 'median', 'mode', 'constant', 'drop'}, default='median'
        Strategy for handling missing values.
    missing_values : any, default=np.nan
        Value to treat as missing.
    fill_value : any, default=0
        Fill value when handle_missing='constant'.
    categorical_encoding : {'label', 'onehot', 'ordinal'}, default='label'
        Encoding strategy for categorical features.
    handle_outliers : {'clip', 'remove', None}, default=None
        Strategy for handling outliers.
    outlier_method : {'iqr', 'zscore'}, default='iqr'
        Method for detecting outliers.
    outlier_threshold : float, optional
        Threshold for outlier detection (IQR: 1.5, Z-score: 3.0).
    scale_features : bool, default=False
        Whether to scale numerical features (usually not needed for trees).
    feature_names : List[str], optional
        Names of features.
    categorical_features : List[int or str], optional
        Indices or names of categorical features.
    drop_invariant : bool, default=True
        Remove features with zero variance.
    """

    def __init__(
        self,
        handle_missing: Literal["mean", "median", "mode", "constant", "drop"] = "median",
        missing_values: any = np.nan,
        fill_value: any = 0,
        categorical_encoding: Literal["label", "onehot", "ordinal"] = "label",
        handle_outliers: Optional[Literal["clip", "remove"]] = None,
        outlier_method: Literal["iqr", "zscore"] = "iqr",
        outlier_threshold: Optional[float] = None,
        scale_features: bool = False,
        feature_names: Optional[List[str]] = None,
        categorical_features: Optional[List[Union[int, str]]] = None,
        drop_invariant: bool = True,
    ):
        self.handle_missing = handle_missing
        self.missing_values = missing_values
        self.fill_value = fill_value
        self.categorical_encoding = categorical_encoding
        self.handle_outliers = handle_outliers
        self.outlier_method = outlier_method
        self.scale_features = scale_features
        self.feature_names = feature_names
        self.categorical_features = categorical_features
        self.drop_invariant = drop_invariant

        # Set default outlier threshold
        if outlier_threshold is None:
            self.outlier_threshold = 1.5 if outlier_method == "iqr" else 3.0
        else:
            self.outlier_threshold = outlier_threshold

        # Will be set during fit
        self.feature_types_: Optional[Dict] = None
        self.missing_stats_: Optional[Dict] = None
        self.categorical_mappings_: Optional[Dict] = None
        self.outlier_bounds_: Optional[Dict] = None
        self.scale_params_: Optional[Dict] = None
        self.n_features_in_: Optional[int] = None
        self.n_features_out_: Optional[int] = None
        self.feature_names_in_: Optional[List[str]] = None
        self.feature_names_out_: Optional[List[str]] = None
        self.invariant_features_: Optional[List[int]] = None

    def fit(self, X: np.ndarray, y: Optional[np.ndarray] = None):
        """
        Learn preprocessing parameters from training data.

        Parameters
        ----------
        X : np.ndarray
            Training data of shape (n_samples, n_features).
        y : np.ndarray, optional
            Target values (not used, for API compatibility).

        Returns
        -------
        self
            Fitted preprocessor.
        """
        if not isinstance(X, np.ndarray):
            X = np.array(X)

        if X.ndim != 2:
            raise ValueError(f"Expected 2D array, got shape {X.shape}")

        n_samples, n_features = X.shape
        self.n_features_in_ = n_features

        # Set feature names
        if self.feature_names is None:
            self.feature_names_in_ = [f"feature_{i}" for i in range(n_features)]
        else:
            if len(self.feature_names) != n_features:
                raise ValueError(
                    f"feature_names has {len(self.feature_names)} elements, "
                    f"but X has {n_features} features"
                )
            self.feature_names_in_ = list(self.feature_names)

        # Infer feature types
        self.feature_types_ = self._infer_feature_types(X)

        # Identify invariant features
        if self.drop_invariant:
            self.invariant_features_ = self._find_invariant_features(X)
            if self.invariant_features_:
                warnings.warn(
                    f"Dropping {len(self.invariant_features_)} invariant features: "
                    f"{[self.feature_names_in_[i] for i in self.invariant_features_]}",
                    UserWarning,
                )
        else:
            self.invariant_features_ = []

        # Compute statistics for each feature
        self.missing_stats_ = {}
        self.categorical_mappings_ = {}
        self.outlier_bounds_ = {}
        self.scale_params_ = {}

        for feat_idx in range(n_features):
            if feat_idx in self.invariant_features_:
                continue

            feature_col = X[:, feat_idx]
            feat_type = self.feature_types_[feat_idx]

            # Handle missing values
            self._fit_missing_values(feat_idx, feature_col, feat_type)

            # Handle categorical encoding
            if feat_type == "categorical":
                self._fit_categorical(feat_idx, feature_col)

            # Handle outliers for numerical features
            if feat_type == "numerical" and self.handle_outliers:
                self._fit_outliers(feat_idx, feature_col)

            # Handle scaling for numerical features
            if feat_type == "numerical" and self.scale_features:
                self._fit_scaling(feat_idx, feature_col)

        # Compute output dimensionality
        self._compute_output_features()

        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        """
        Apply learned transformations to data.

        Parameters
        ----------
        X : np.ndarray
            Data to transform of shape (n_samples, n_features).

        Returns
        -------
        np.ndarray
            Transformed data.
        """
        if self.feature_types_ is None:
            raise ValueError("Preprocessor must be fitted before transform")

        if not isinstance(X, np.ndarray):
            X = np.array(X)

        if X.shape[1] != self.n_features_in_:
            raise ValueError(
                f"X has {X.shape[1]} features, but preprocessor was fitted with {self.n_features_in_}"
            )

        X = X.copy()

        # Remove invariant features
        if self.invariant_features_:
            mask = np.ones(X.shape[1], dtype=bool)
            mask[self.invariant_features_] = False
            X = X[:, mask]

        transformed_features = []

        for feat_idx in range(self.n_features_in_):
            if feat_idx in self.invariant_features_:
                continue

            # Map to new index after removing invariant features
            new_idx = feat_idx - sum(1 for i in self.invariant_features_ if i < feat_idx)
            feature_col = X[:, new_idx : new_idx + 1]

            feat_type = self.feature_types_[feat_idx]

            # Apply transformations in order
            feature_col = self._transform_missing_values(feat_idx, feature_col)

            if feat_type == "categorical":
                feature_col = self._transform_categorical(feat_idx, feature_col)
            elif feat_type == "numerical":
                if self.handle_outliers:
                    feature_col = self._transform_outliers(feat_idx, feature_col)
                if self.scale_features:
                    feature_col = self._transform_scaling(feat_idx, feature_col)

            # Handle one-hot encoding output
            if feature_col.ndim == 1:
                feature_col = feature_col.reshape(-1, 1)

            transformed_features.append(feature_col)

        if not transformed_features:
            raise ValueError("All features were removed during preprocessing")

        result = np.hstack(transformed_features)

        try:
            # Fast path: convert all at once
            result = result.astype(np.float64)
        except (ValueError, TypeError):
            # Safe path: convert column-by-column
            result_float = np.empty(result.shape, dtype=np.float64)
            for i in range(result.shape[1]):
                try:
                    result_float[:, i] = result[:, i].astype(np.float64)
                except (ValueError, TypeError):
                    # Column contains non-numeric data → encode it
                    unique_vals = np.unique(result[:, i])
                    mapping = {val: idx for idx, val in enumerate(unique_vals)}
                    result_float[:, i] = np.array([mapping.get(v, -1) for v in result[:, i]])
            result = result_float

        return result


    def fit_transform(self, X: np.ndarray, y: Optional[np.ndarray] = None) -> np.ndarray:
        """
        Fit and transform data in one step.

        Parameters
        ----------
        X : np.ndarray
            Data to fit and transform.
        y : np.ndarray, optional
            Target values.

        Returns
        -------
        np.ndarray
            Transformed data.
        """
        return self.fit(X, y).transform(X)

    def _infer_feature_types(self, X: np.ndarray) -> Dict[int, str]:
        """
        Automatically detect feature types.

        Parameters
        ----------
        X : np.ndarray
            Input data.

        Returns
        -------
        Dict[int, str]
        Mapping from feature index to type ('numerical' or 'categorical').
        """
        feature_types = {}

        for feat_idx in range(X.shape[1]):
            # Check if explicitly specified as categorical
            is_categorical = False
            if self.categorical_features:
                if isinstance(self.categorical_features[0], int):
                    is_categorical = feat_idx in self.categorical_features
                else:
                    feat_name = self.feature_names_in_[feat_idx]
                    is_categorical = feat_name in self.categorical_features

            if is_categorical:
                feature_types[feat_idx] = "categorical"
                continue

            # Infer from data
            feature_col = X[:, feat_idx]

            # Get non-missing values - properly handle both None and np.nan
            non_missing_mask = ~self._is_missing(feature_col)
            non_missing = feature_col[non_missing_mask]

            if len(non_missing) == 0:
                feature_types[feat_idx] = "numerical"
                continue

            # Check if numeric
            try:
                # Try to convert to float
                numeric_values = non_missing.astype(float)
                is_numeric = True
            except (ValueError, TypeError):
                is_numeric = False

            if is_numeric:
                # For numeric data, use numpy unique safely
                try:
                    unique_values = np.unique(numeric_values)
                    unique_ratio = len(unique_values) / len(numeric_values)

                    # Check for low cardinality (might be categorical)
                    if unique_ratio < 0.05 and len(unique_values) < 10:
                        feature_types[feat_idx] = "categorical"
                    else:
                        feature_types[feat_idx] = "numerical"
                except Exception:
                    # Fallback: treat as numerical
                    feature_types[feat_idx] = "numerical"
            else:
                # For categorical (string) data
                feature_types[feat_idx] = "categorical"

        return feature_types

    def _is_missing(self, values: np.ndarray) -> np.ndarray:
        """Check which values are missing."""
        if self.missing_values is np.nan or self.missing_values is None:
            return np.array([v is None or (isinstance(v, float) and np.isnan(v)) for v in values])
        else:
            return values == self.missing_values

    def _find_invariant_features(self, X: np.ndarray) -> List[int]:
        """Find features with zero variance."""
        invariant = []
        for feat_idx in range(X.shape[1]):
            feature_col = X[:, feat_idx]
            non_missing = feature_col[~self._is_missing(feature_col)]

            if len(non_missing) == 0:
                # All missing - consider invariant
                invariant.append(feat_idx)
                continue

            # Use set() instead of np.unique() to avoid type comparison issues
            try:
                # Try numeric comparison first
                numeric_vals = non_missing.astype(float)
                unique_count = len(np.unique(numeric_vals))
            except (ValueError, TypeError):
                # Fall back to set for non-numeric data
                unique_count = len(set(str(v) for v in non_missing))

            if unique_count == 1:
                invariant.append(feat_idx)

        return invariant

    def _fit_missing_values(self, feat_idx: int, feature_col: np.ndarray, feat_type: str) -> None:
        """Learn statistics for missing value imputation."""
        missing_mask = self._is_missing(feature_col)
        non_missing = feature_col[~missing_mask]

        if len(non_missing) == 0:
            # All values are missing
            if feat_type == "numerical":
                self.missing_stats_[feat_idx] = 0.0
            else:
                self.missing_stats_[feat_idx] = "missing"
            return

        if self.handle_missing == "mean" and feat_type == "numerical":
            self.missing_stats_[feat_idx] = np.mean(non_missing.astype(float))
        elif self.handle_missing == "median" and feat_type == "numerical":
            self.missing_stats_[feat_idx] = np.median(non_missing.astype(float))
        elif self.handle_missing == "mode":
            unique, counts = np.unique(non_missing, return_counts=True)
            self.missing_stats_[feat_idx] = unique[np.argmax(counts)]
        elif self.handle_missing == "constant":
            self.missing_stats_[feat_idx] = self.fill_value
        else:
            self.missing_stats_[feat_idx] = None

    def _transform_missing_values(self, feat_idx: int, feature_col: np.ndarray) -> np.ndarray:
        """Apply missing value imputation."""
        feature_col = feature_col.copy()
        missing_mask = self._is_missing(feature_col.ravel())

        if not np.any(missing_mask):
            return feature_col

        if self.handle_missing == "drop":
            # This should be handled at dataset level, not feature level
            warnings.warn(
                "'drop' strategy for missing values should be applied to entire rows", UserWarning
            )
            return feature_col

        fill_value = self.missing_stats_.get(feat_idx)
        if fill_value is not None:
            feature_col[missing_mask] = fill_value

        return feature_col

    def _fit_categorical(self, feat_idx: int, feature_col: np.ndarray) -> None:
        """Learn categorical encoding mappings."""
        non_missing = feature_col[~self._is_missing(feature_col)]
        unique_values = np.unique(non_missing)

        if self.categorical_encoding == "label":
            # Map each category to an integer
            mapping = {val: i for i, val in enumerate(unique_values)}
            self.categorical_mappings_[feat_idx] = {
                "type": "label",
                "mapping": mapping,
                "unknown_value": len(unique_values),
            }
        elif self.categorical_encoding == "onehot":
            # Store categories for one-hot encoding
            self.categorical_mappings_[feat_idx] = {
                "type": "onehot",
                "categories": unique_values,
                "n_categories": len(unique_values),
            }
        else:  # ordinal
            # Same as label but preserves order if possible
            try:
                sorted_values = sorted(unique_values)
                mapping = {val: i for i, val in enumerate(sorted_values)}
            except TypeError:
                mapping = {val: i for i, val in enumerate(unique_values)}

            self.categorical_mappings_[feat_idx] = {
                "type": "ordinal",
                "mapping": mapping,
                "unknown_value": len(unique_values),
            }

    def _transform_categorical(self, feat_idx: int, feature_col: np.ndarray) -> np.ndarray:
        """Apply categorical encoding."""
        mapping_info = self.categorical_mappings_[feat_idx]
        feature_col = feature_col.ravel()

        if mapping_info["type"] == "onehot":
            categories = mapping_info["categories"]
            n_categories = mapping_info["n_categories"]

            # Create one-hot encoded matrix
            encoded = np.zeros((len(feature_col), n_categories))
            for i, val in enumerate(feature_col):
                if val in categories:
                    idx = np.where(categories == val)[0][0]
                    encoded[i, idx] = 1.0
                # Unknown values remain all zeros

            return encoded
        else:
            # Label or ordinal encoding
            mapping = mapping_info["mapping"]
            unknown_value = mapping_info["unknown_value"]

            encoded = np.array([mapping.get(val, unknown_value) for val in feature_col])

            return encoded.reshape(-1, 1)

    def _fit_outliers(self, feat_idx: int, feature_col: np.ndarray) -> None:
        """Learn outlier bounds."""
        non_missing = feature_col[~self._is_missing(feature_col)].astype(float)

        if len(non_missing) == 0:
            self.outlier_bounds_[feat_idx] = {"lower": -np.inf, "upper": np.inf}
            return

        if self.outlier_method == "iqr":
            q1 = np.percentile(non_missing, 25)
            q3 = np.percentile(non_missing, 75)
            iqr = q3 - q1
            lower_bound = q1 - self.outlier_threshold * iqr
            upper_bound = q3 + self.outlier_threshold * iqr
        else:  # zscore
            mean = np.mean(non_missing)
            std = np.std(non_missing)
            lower_bound = mean - self.outlier_threshold * std
            upper_bound = mean + self.outlier_threshold * std

        self.outlier_bounds_[feat_idx] = {"lower": lower_bound, "upper": upper_bound}

    def _transform_outliers(self, feat_idx: int, feature_col: np.ndarray) -> np.ndarray:
        """Handle outliers."""
        bounds = self.outlier_bounds_[feat_idx]
        feature_col = feature_col.astype(float)

        if self.handle_outliers == "clip":
            return np.clip(feature_col, bounds["lower"], bounds["upper"])
        elif self.handle_outliers == "remove":
            # Mark outliers as NaN (should be filtered at dataset level)
            outlier_mask = (feature_col < bounds["lower"]) | (feature_col > bounds["upper"])
            feature_col[outlier_mask] = np.nan
            return feature_col

        return feature_col

    def _fit_scaling(self, feat_idx: int, feature_col: np.ndarray) -> None:
        """Learn scaling parameters."""
        non_missing = feature_col[~self._is_missing(feature_col)].astype(float)

        if len(non_missing) == 0:
            self.scale_params_[feat_idx] = {"mean": 0.0, "std": 1.0}
            return

        mean = np.mean(non_missing)
        std = np.std(non_missing)

        if std == 0:
            std = 1.0

        self.scale_params_[feat_idx] = {"mean": mean, "std": std}

    def _transform_scaling(self, feat_idx: int, feature_col: np.ndarray) -> np.ndarray:
        """Apply feature scaling (standardization)."""
        params = self.scale_params_[feat_idx]
        feature_col = feature_col.astype(float)
        return (feature_col - params["mean"]) / params["std"]

    def _compute_output_features(self) -> None:
        """Compute output feature names and dimensionality."""
        output_names = []
        n_output = 0

        for feat_idx in range(self.n_features_in_):
            if feat_idx in self.invariant_features_:
                continue

            feat_name = self.feature_names_in_[feat_idx]
            feat_type = self.feature_types_[feat_idx]

            if feat_type == "categorical" and self.categorical_encoding == "onehot":
                # One-hot creates multiple features
                mapping_info = self.categorical_mappings_[feat_idx]
                categories = mapping_info["categories"]
                for cat in categories:
                    output_names.append(f"{feat_name}_{cat}")
                n_output += len(categories)
            else:
                output_names.append(feat_name)
                n_output += 1

        self.feature_names_out_ = output_names
        self.n_features_out_ = n_output

    def get_feature_names_out(self) -> List[str]:
        """
        Get output feature names after transformation.

        Returns
        -------
        List[str]
            Feature names after preprocessing.
        """
        if self.feature_names_out_ is None:
            raise ValueError("Preprocessor must be fitted first")
        return self.feature_names_out_

    def get_feature_info(self) -> Dict:
        """
        Get metadata about features.

        Returns
        -------
        Dict
            Feature information including types, missing counts, etc.
        """
        if self.feature_types_ is None:
            raise ValueError("Preprocessor must be fitted first")

        info = {}
        for feat_idx in range(self.n_features_in_):
            feat_name = self.feature_names_in_[feat_idx]
            info[feat_name] = {
                "index": feat_idx,
                "type": self.feature_types_[feat_idx],
                "is_invariant": feat_idx in self.invariant_features_,
            }

            if feat_idx in self.categorical_mappings_:
                mapping_info = self.categorical_mappings_[feat_idx]
                info[feat_name]["encoding"] = mapping_info["type"]
                if mapping_info["type"] == "onehot":
                    info[feat_name]["n_categories"] = mapping_info["n_categories"]
                else:
                    info[feat_name]["n_categories"] = len(mapping_info["mapping"])

        return info

    def inverse_transform(self, X: np.ndarray) -> np.ndarray:
        """
        Reverse transformations where possible.

        Note: Some transformations (like one-hot encoding) cannot be
        perfectly reversed if information was lost.

        Parameters
        ----------
        X : np.ndarray
            Transformed data.

        Returns
        -------
        np.ndarray
            Approximately original data.
        """
        warnings.warn(
            "inverse_transform may not perfectly recover original data "
            "for irreversible transformations like one-hot encoding",
            UserWarning,
        )

        if self.n_features_out_ != X.shape[1]:
            raise ValueError(
                f"X has {X.shape[1]} features, but preprocessor outputs {self.n_features_out_}"
            )

        # This is a simplified implementation
        # Full inverse transform would require tracking all transformations
        return X


class DataValidator:
    """
    Validate and prepare data for tree models.
    """

    @staticmethod
    def validate_training_data(
        X: np.ndarray, y: np.ndarray, sample_weight: Optional[np.ndarray] = None
    ) -> Tuple[np.ndarray, np.ndarray, Optional[np.ndarray]]:
        """
        Validate training data.

        Parameters
        ----------
        X : np.ndarray
            Feature matrix.
        y : np.ndarray
            Target vector.
        sample_weight : np.ndarray, optional
            Sample weights.

        Returns
        -------
        X : np.ndarray
            Validated features.
        y : np.ndarray
            Validated targets.
        sample_weight : np.ndarray or None
            Validated sample weights.

        Raises
        ------
        ValueError
            If data is invalid.
        """
        if not isinstance(X, np.ndarray):
            X = np.array(X)
        if not isinstance(y, np.ndarray):
            y = np.array(y)

        if X.ndim != 2:
            raise ValueError(f"X must be 2D, got shape {X.shape}")
        if y.ndim != 1:
            if y.ndim == 2 and y.shape[1] == 1:
                y = y.ravel()
            else:
                raise ValueError(f"y must be 1D, got shape {y.shape}")

        if X.shape[0] != y.shape[0]:
            raise ValueError(
                f"X and y have different number of samples: {X.shape[0]} != {y.shape[0]}"
            )

        if np.any(np.isinf(X)):
            raise ValueError("X contains infinite values")
        if np.any(np.isinf(y)):
            raise ValueError("y contains infinite values")

        if sample_weight is not None:
            if not isinstance(sample_weight, np.ndarray):
                sample_weight = np.array(sample_weight)
            if sample_weight.shape[0] != X.shape[0]:
                raise ValueError(
                    f"sample_weight has {sample_weight.shape[0]} samples, "
                    f"but X has {X.shape[0]}"
                )
            if np.any(sample_weight < 0):
                raise ValueError("sample_weight contains negative values")

        # Ensure contiguous arrays for performance
        X = np.ascontiguousarray(X, dtype=np.float64)

        return X, y, sample_weight

    @staticmethod
    def validate_prediction_data(X: np.ndarray, n_features_expected: int) -> np.ndarray:
        """
        Validate prediction data.

        Parameters
        ----------
        X : np.ndarray
            Feature matrix.
        n_features_expected : int
            Expected number of features.

        Returns
        -------
        np.ndarray
            Validated features.

        Raises
        ------
        ValueError
            If data is invalid.
        """
        if not isinstance(X, np.ndarray):
            X = np.array(X)

        if X.ndim != 2:
            raise ValueError(f"X must be 2D, got shape {X.shape}")

        if X.shape[1] != n_features_expected:
            raise ValueError(
                f"X has {X.shape[1]} features, but model expects {n_features_expected}"
            )

        if np.any(np.isinf(X)):
            raise ValueError("X contains infinite values")

        return np.ascontiguousarray(X, dtype=np.float64)
