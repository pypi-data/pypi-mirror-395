"""
End-to-end pipeline combining preprocessing and model.
"""

import logging
import pickle
from typing import Optional, Union

import numpy as np

from .preprocessing import DataPreprocessor
from .tree import REPTreeClassifier, REPTreeRegressor
from .utils import check_is_fitted, train_test_split

logger = logging.getLogger(__name__)


class REPTreePipeline:
    """
    End-to-end pipeline for preprocessing and tree model.

    Combines data preprocessing with REPTree estimator for seamless
    training and prediction workflow.

    Parameters
    ----------
    estimator : REPTreeClassifier or REPTreeRegressor
        Tree estimator to use.
    preprocessor : DataPreprocessor, optional
        Data preprocessor. If None, creates default preprocessor.
    validation_size : float, default=0.2
        Fraction of data to use for validation if not provided.
    random_state : int, optional
        Random seed for reproducibility.

    Attributes
    ----------
    estimator_ : estimator
        Fitted tree estimator.
    preprocessor_ : DataPreprocessor
        Fitted preprocessor.

    Examples
    --------
    >>> from reptree import REPTreeClassifier, REPTreePipeline
    >>> clf = REPTreeClassifier(pruning='rep')
    >>> pipeline = REPTreePipeline(clf)
    >>> pipeline.fit(X_train, y_train)
    >>> predictions = pipeline.predict(X_test)
    """

    def __init__(
        self,
        estimator: Union[REPTreeClassifier, REPTreeRegressor],
        preprocessor: Optional[DataPreprocessor] = None,
        validation_size: float = 0.2,
        random_state: Optional[int] = None,
    ):
        if not isinstance(estimator, (REPTreeClassifier, REPTreeRegressor)):
            raise TypeError("estimator must be REPTreeClassifier or REPTreeRegressor")

        if not 0 < validation_size < 1:
            raise ValueError(f"validation_size must be between 0 and 1, got {validation_size}")

        self.estimator = estimator
        self.validation_size = validation_size
        self.random_state = random_state

        # Create default preprocessor if not provided
        if preprocessor is None:
            self.preprocessor = DataPreprocessor(
                handle_missing="median", categorical_encoding="label", drop_invariant=True
            )
        else:
            self.preprocessor = preprocessor

        # Will be set during fit
        self.estimator_: Optional[Union[REPTreeClassifier, REPTreeRegressor]] = None
        self.preprocessor_: Optional[DataPreprocessor] = None

    def fit(
        self,
        X: np.ndarray,
        y: np.ndarray,
        sample_weight: Optional[np.ndarray] = None,
        X_val: Optional[np.ndarray] = None,
        y_val: Optional[np.ndarray] = None,
    ):
        """
        Fit preprocessing and estimator.

        Parameters
        ----------
        X : np.ndarray
            Training data of shape (n_samples, n_features).
        y : np.ndarray
            Target values of shape (n_samples,).
        sample_weight : np.ndarray, optional
            Sample weights.
        X_val : np.ndarray, optional
            Validation data for pruning. If None and pruning is enabled,
            automatically created from training data.
        y_val : np.ndarray, optional
            Validation targets.

        Returns
        -------
        self
            Fitted pipeline.
        """
        logger.info("Starting pipeline fit...")

        # Fit preprocessor on training data
        logger.info("Fitting preprocessor...")
        self.preprocessor_ = self.preprocessor.fit(X, y)

        # Transform training data
        logger.info("Transforming training data...")
        X_transformed = self.preprocessor_.transform(X)

        # Handle validation set
        needs_validation = self.estimator.pruning == "rep"

        if needs_validation and X_val is None:
            logger.info(f"Creating validation set ({self.validation_size*100:.0f}% of data)...")
            X_transformed, X_val_transformed, y_train, y_val = train_test_split(
                X_transformed, y, test_size=self.validation_size, random_state=self.random_state
            )
        elif needs_validation and X_val is not None:
            logger.info("Transforming provided validation data...")
            X_val_transformed = self.preprocessor_.transform(X_val)
            y_train = y
        else:
            X_val_transformed = None
            y_val = None
            y_train = y

        # Fit estimator
        logger.info("Fitting tree estimator...")
        self.estimator_ = self.estimator
        self.estimator_.fit(
            X_transformed,
            y_train,
            sample_weight=sample_weight,
            X_val=X_val_transformed,
            y_val=y_val,
        )

        logger.info("Pipeline fit complete!")
        logger.info(f"Tree depth: {self.estimator_.get_depth()}")
        logger.info(f"Number of leaves: {self.estimator_.get_n_leaves()}")

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict using fitted pipeline.

        Parameters
        ----------
        X : np.ndarray
            Samples to predict.

        Returns
        -------
        np.ndarray
            Predictions.
        """
        self._check_is_fitted()

        # Preprocess input
        X_transformed = self.preprocessor_.transform(X)

        # Predict
        return self.estimator_.predict(X_transformed)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Predict class probabilities (classifier only).

        Parameters
        ----------
        X : np.ndarray
            Samples to predict.

        Returns
        -------
        np.ndarray
            Class probabilities.

        Raises
        ------
        AttributeError
            If estimator is not a classifier.
        """
        self._check_is_fitted()

        if not isinstance(self.estimator_, REPTreeClassifier):
            raise AttributeError("predict_proba is only available for classifiers")

        # Preprocess input
        X_transformed = self.preprocessor_.transform(X)

        # Predict probabilities
        return self.estimator_.predict_proba(X_transformed)

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """
        Evaluate model on test data.

        Parameters
        ----------
        X : np.ndarray
            Test samples.
        y : np.ndarray
            True values.

        Returns
        -------
        float
            Accuracy (classifier) or R² (regressor).
        """
        self._check_is_fitted()

        # Preprocess input
        X_transformed = self.preprocessor_.transform(X)

        # Score
        return self.estimator_.score(X_transformed, y)

    def get_feature_names_out(self) -> list:
        """
        Get feature names after preprocessing.

        Returns
        -------
        list
            Output feature names.
        """
        if self.preprocessor_ is None:
            raise ValueError("Pipeline must be fitted first")

        return self.preprocessor_.get_feature_names_out()

    def get_feature_importances(self) -> np.ndarray:
        """
        Get feature importances from tree.

        Returns
        -------
        np.ndarray
            Feature importances.
        """
        self._check_is_fitted()
        return self.estimator_.feature_importances_

    def _check_is_fitted(self) -> None:
        """Check if pipeline is fitted."""
        if self.estimator_ is None or self.preprocessor_ is None:
            raise ValueError("Pipeline is not fitted yet. Call 'fit' before using this method.")
        check_is_fitted(self.estimator_)

    def save(self, filepath: str) -> None:
        """
        Save entire pipeline to file.

        Parameters
        ----------
        filepath : str
            Path to save pipeline.
        """
        self._check_is_fitted()

        with open(filepath, "wb") as f:
            pickle.dump(self, f)

        logger.info(f"Pipeline saved to {filepath}")

    @classmethod
    def load(cls, filepath: str):
        """
        Load pipeline from file.

        Parameters
        ----------
        filepath : str
            Path to load pipeline from.

        Returns
        -------
        REPTreePipeline
            Loaded pipeline.
        """
        with open(filepath, "rb") as f:
            pipeline = pickle.load(f)

        if not isinstance(pipeline, cls):
            raise TypeError(f"Loaded object is not a {cls.__name__}")

        logger.info(f"Pipeline loaded from {filepath}")
        return pipeline

    def get_params(self) -> dict:
        """
        Get parameters for pipeline.

        Returns
        -------
        dict
            Pipeline parameters.
        """
        return {
            "estimator": self.estimator,
            "preprocessor": self.preprocessor,
            "validation_size": self.validation_size,
            "random_state": self.random_state,
        }

    def set_params(self, **params):
        """
        Set parameters for pipeline.

        Parameters
        ----------
        **params : dict
            Pipeline parameters.

        Returns
        -------
        self
            Pipeline instance.
        """
        for key, value in params.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"Invalid parameter {key}")

        return self
