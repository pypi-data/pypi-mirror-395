"""
Optimized split-finding logic for decision trees.
"""

from abc import ABC, abstractmethod
from typing import Literal, Optional, Tuple

import numpy as np

from .metrics import entropy, gini_impurity, information_gain, mae_impurity, variance


class BaseSplitter(ABC):
    """
    Abstract base class for split finders.

    Parameters
    ----------
    criterion : str
        Impurity criterion ('gini', 'entropy', 'variance', 'mae').
    min_samples_split : int
        Minimum samples required to split.
    min_samples_leaf : int
        Minimum samples required in a leaf.
    min_impurity_decrease : float
        Minimum gain required to split.
    random_state : int, optional
        Random seed for reproducibility.
    """

    def __init__(
        self,
        criterion: str,
        min_samples_split: int = 2,
        min_samples_leaf: int = 1,
        min_impurity_decrease: float = 0.0,
        random_state: Optional[int] = None,
    ):
        self.criterion = criterion
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.min_impurity_decrease = min_impurity_decrease
        self.random_state = random_state
        self.rng = np.random.RandomState(random_state)

    @abstractmethod
    def find_best_split(
        self,
        X: np.ndarray,
        y: np.ndarray,
        sample_weight: Optional[np.ndarray] = None,
        feature_indices: Optional[np.ndarray] = None,
    ) -> Tuple[Optional[int], Optional[float], float]:
        """
        Find the best split for the given data.

        Parameters
        ----------
        X : np.ndarray
            Feature matrix of shape (n_samples, n_features).
        y : np.ndarray
            Target values of shape (n_samples,).
        sample_weight : np.ndarray, optional
            Sample weights.
        feature_indices : np.ndarray, optional
            Indices of features to consider. If None, consider all features.

        Returns
        -------
        feature_idx : int or None
            Index of best feature to split on, or None if no valid split.
        threshold : float or None
            Best threshold value, or None if no valid split.
        gain : float
            Information gain from the split (0.0 if no valid split).
        """
        pass


class OptimizedSplitter(BaseSplitter):
    """
    Optimized splitter with vectorized operations and adaptive binning.

    Uses percentile-based binning when unique values exceed threshold,
    and leverages NumPy for efficient gain calculations.
    """

    MAX_UNIQUE_VALUES = 32

    def find_best_split(
        self,
        X: np.ndarray,
        y: np.ndarray,
        sample_weight: Optional[np.ndarray] = None,
        feature_indices: Optional[np.ndarray] = None,
    ) -> Tuple[Optional[int], Optional[float], float]:
        """Find the best split using vectorized operations."""
        n_samples, n_features = X.shape

        # Check stopping criteria
        if n_samples < self.min_samples_split:
            return None, None, 0.0

        # Determine features to consider
        if feature_indices is None:
            feature_indices = np.arange(n_features)

        best_feature = None
        best_threshold = None
        best_gain = 0.0

        # Try each feature
        for feat_idx in feature_indices:
            feature_vals = X[:, feat_idx]

            # Skip if all values are the same or all missing
            if np.all(np.isnan(feature_vals)):
                continue

            unique_vals = np.unique(feature_vals[~np.isnan(feature_vals)])
            if len(unique_vals) <= 1:
                continue

            # Get candidate thresholds
            thresholds = self._get_candidate_thresholds(unique_vals)

            # Evaluate each threshold
            for threshold in thresholds:
                gain = self._evaluate_split(feature_vals, y, threshold, sample_weight)

                if gain > best_gain:
                    best_gain = gain
                    best_feature = feat_idx
                    best_threshold = threshold

        # Check if gain meets minimum requirement
        if best_gain < self.min_impurity_decrease:
            return None, None, 0.0

        return best_feature, best_threshold, best_gain

    def _get_candidate_thresholds(self, unique_vals: np.ndarray) -> np.ndarray:
        """
        Get candidate split thresholds using adaptive binning.

        Parameters
        ----------
        unique_vals : np.ndarray
            Sorted unique feature values.

        Returns
        -------
        np.ndarray
            Candidate threshold values.
        """
        n_unique = len(unique_vals)

        if n_unique <= self.MAX_UNIQUE_VALUES:
            # Use midpoints between consecutive values
            if n_unique == 1:
                return unique_vals
            return (unique_vals[:-1] + unique_vals[1:]) / 2.0
        else:
            # Use percentile-based binning
            percentiles = np.linspace(0, 100, self.MAX_UNIQUE_VALUES + 1)[1:-1]
            return np.percentile(unique_vals, percentiles)

    def _evaluate_split(
        self,
        feature_vals: np.ndarray,
        y: np.ndarray,
        threshold: float,
        sample_weight: Optional[np.ndarray] = None,
    ) -> float:
        """
        Evaluate information gain for a split.

        Parameters
        ----------
        feature_vals : np.ndarray
            Feature values for splitting.
        y : np.ndarray
            Target values.
        threshold : float
            Split threshold.
        sample_weight : np.ndarray, optional
            Sample weights.

        Returns
        -------
        float
            Information gain (0.0 if split is invalid).
        """
        # Handle missing values: assign to larger child
        non_missing = ~np.isnan(feature_vals)

        # Create initial split masks
        left_mask = non_missing & (feature_vals <= threshold)
        right_mask = non_missing & (feature_vals > threshold)

        n_left = np.sum(left_mask)
        n_right = np.sum(right_mask)

        # Check minimum samples in leaves
        if n_left < self.min_samples_leaf or n_right < self.min_samples_leaf:
            return 0.0

        # Assign missing values to larger child
        missing_mask = ~non_missing
        if np.any(missing_mask):
            if n_left >= n_right:
                left_mask = left_mask | missing_mask
            else:
                right_mask = right_mask | missing_mask

        # Calculate information gain
        y_left = y[left_mask]
        y_right = y[right_mask]

        if len(y_left) == 0 or len(y_right) == 0:
            return 0.0

        return information_gain(y, y_left, y_right, self.criterion)

    def compute_leaf_value(
        self,
        y: np.ndarray,
        sample_weight: Optional[np.ndarray] = None,
        task_type: str = "classification",
    ) -> any:
        """
        Compute the prediction value for a leaf node.

        Parameters
        ----------
        y : np.ndarray
            Target values at the leaf.
        sample_weight : np.ndarray, optional
            Sample weights.
        task_type : str
            'classification' or 'regression'.

        Returns
        -------
        any
            Prediction value (class probabilities or regression value).
        """
        if len(y) == 0:
            return None

        if task_type == "classification":
            # Return class probabilities
            classes, counts = np.unique(y, return_counts=True)
            if sample_weight is not None:
                # Weighted counts
                weighted_counts = np.zeros(len(classes))
                for i, cls in enumerate(classes):
                    weighted_counts[i] = np.sum(sample_weight[y == cls])
                probs = weighted_counts / np.sum(weighted_counts)
            else:
                probs = counts / len(y)

            # Return as dict mapping class to probability
            return dict(zip(classes.astype(int), probs))

        else:  # regression
            if self.criterion == "mae":
                # Use median for MAE
                return np.median(y)
            else:
                # Use mean for variance/MSE
                if sample_weight is not None:
                    return np.average(y, weights=sample_weight)
                return np.mean(y)

    def compute_impurity(self, y: np.ndarray, sample_weight: Optional[np.ndarray] = None) -> float:
        """
        Compute impurity for the given targets.

        Parameters
        ----------
        y : np.ndarray
            Target values.
        sample_weight : np.ndarray, optional
            Sample weights (not currently used).

        Returns
        -------
        float
            Impurity value.
        """
        if len(y) == 0:
            return 0.0

        if self.criterion == "gini":
            return gini_impurity(y)
        elif self.criterion == "entropy":
            return entropy(y)
        elif self.criterion == "variance":
            return variance(y)
        elif self.criterion == "mae":
            return mae_impurity(y)
        else:
            raise ValueError(f"Unknown criterion: {self.criterion}")
