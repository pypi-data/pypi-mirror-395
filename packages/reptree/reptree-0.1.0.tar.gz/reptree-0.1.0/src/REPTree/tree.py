"""
Main REPTree classifier and regressor implementations.
"""

import logging
import pickle
import warnings
from typing import Dict, Literal, Optional, Union

import numpy as np

from .node import TreeNode
from .pruning.rep import ReducedErrorPruner
from .splitter import OptimizedSplitter
from .utils import check_array, check_is_fitted, check_X_y, get_feature_importance, train_test_split

logger = logging.getLogger(__name__)


class BaseREPTree:
    """
    Base class for REPTree estimators.

    Parameters
    ----------
    criterion : str
        Impurity criterion.
    max_depth : int, optional
        Maximum tree depth (None = unlimited).
    min_samples_split : int, default=2
        Minimum samples required to split a node.
    min_samples_leaf : int, default=1
        Minimum samples required in a leaf.
    min_impurity_decrease : float, default=0.0
        Minimum impurity decrease required to split.
    max_features : int, float, str, optional
        Number of features to consider for each split:
        - int: exact number
        - float: fraction of features
        - 'sqrt': sqrt(n_features)
        - 'log2': log2(n_features)
        - None: all features
    max_leaf_nodes : int, optional
        Maximum number of leaf nodes (None = unlimited).
    pruning : {'rep', None}, default=None
        Pruning strategy to apply.
    random_state : int, optional
        Random seed for reproducibility.
    """

    def __init__(
        self,
        criterion: str,
        max_depth: Optional[int] = None,
        min_samples_split: int = 2,
        min_samples_leaf: int = 1,
        min_impurity_decrease: float = 0.0,
        max_features: Optional[Union[int, float, str]] = None,
        max_leaf_nodes: Optional[int] = None,
        pruning: Optional[Literal["rep"]] = None,
        random_state: Optional[int] = None,
    ):
        self.criterion = criterion
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.min_impurity_decrease = min_impurity_decrease
        self.max_features = max_features
        self.max_leaf_nodes = max_leaf_nodes
        self.pruning = pruning
        self.random_state = random_state

        # Validate parameters
        self._validate_parameters()

        # Will be set during fit
        self.tree_: Optional[TreeNode] = None
        self.n_features_: Optional[int] = None
        self.feature_importances_: Optional[np.ndarray] = None

    def _validate_parameters(self) -> None:
        """Validate hyperparameters."""
        if self.max_depth is not None and self.max_depth < 1:
            raise ValueError(f"max_depth must be >= 1, got {self.max_depth}")

        if self.min_samples_split < 2:
            raise ValueError(f"min_samples_split must be >= 2, got {self.min_samples_split}")

        if self.min_samples_leaf < 1:
            raise ValueError(f"min_samples_leaf must be >= 1, got {self.min_samples_leaf}")

        if self.min_impurity_decrease < 0:
            raise ValueError(
                f"min_impurity_decrease must be >= 0, got {self.min_impurity_decrease}"
            )

        if self.max_leaf_nodes is not None and self.max_leaf_nodes < 2:
            raise ValueError(f"max_leaf_nodes must be >= 2, got {self.max_leaf_nodes}")

        if self.pruning is not None and self.pruning not in ["rep"]:
            raise ValueError(f"pruning must be 'rep' or None, got {self.pruning}")

    def _get_max_features(self, n_features: int) -> int:
        """
        Calculate actual number of features to consider at each split.

        Parameters
        ----------
        n_features : int
            Total number of features.

        Returns
        -------
        int
            Number of features to consider.
        """
        if self.max_features is None:
            return n_features
        elif self.max_features == "sqrt":
            return max(1, int(np.sqrt(n_features)))
        elif self.max_features == "log2":
            return max(1, int(np.log2(n_features)))
        elif isinstance(self.max_features, int):
            return min(self.max_features, n_features)
        elif isinstance(self.max_features, float):
            return max(1, int(self.max_features * n_features))
        else:
            raise ValueError(f"Invalid max_features: {self.max_features}")

    def _build_tree(
        self,
        X: np.ndarray,
        y: np.ndarray,
        depth: int = 0,
        sample_weight: Optional[np.ndarray] = None,
        splitter: Optional[OptimizedSplitter] = None,
        task_type: str = "classification",
    ) -> TreeNode:
        """
        Recursively build decision tree.

        Parameters
        ----------
        X : np.ndarray
            Feature matrix.
        y : np.ndarray
            Target values.
        depth : int
            Current depth in tree.
        sample_weight : np.ndarray, optional
            Sample weights.
        splitter : OptimizedSplitter
            Splitter instance.
        task_type : str
            'classification' or 'regression'.

        Returns
        -------
        TreeNode
            Root of constructed subtree.
        """
        n_samples, n_features = X.shape

        # Compute node value and impurity
        node_value = splitter.compute_leaf_value(y, sample_weight, task_type)
        node_impurity = splitter.compute_impurity(y, sample_weight)

        # Create node
        node = TreeNode(value=node_value, samples=n_samples, impurity=node_impurity)

        # Check stopping criteria
        if (
            depth == self.max_depth
            or n_samples < self.min_samples_split
            or n_samples < 2 * self.min_samples_leaf
            or node_impurity == 0.0
        ):
            return node

        # Check max_leaf_nodes constraint (approximate via depth)
        if self.max_leaf_nodes is not None:
            estimated_leaves = 2 ** (depth + 1)
            if estimated_leaves >= self.max_leaf_nodes:
                return node

        # Select features to consider
        max_features = self._get_max_features(n_features)
        if max_features < n_features:
            rng = np.random.RandomState(self.random_state)
            feature_indices = rng.choice(n_features, max_features, replace=False)
        else:
            feature_indices = None

        # Find best split
        best_feature, best_threshold, best_gain = splitter.find_best_split(
            X, y, sample_weight, feature_indices
        )

        if best_feature is None:
            # No valid split found
            return node

        # Split data
        feature_vals = X[:, best_feature]

        # Handle missing values: assign to larger child
        non_missing = ~np.isnan(feature_vals)
        left_mask_non_missing = non_missing & (feature_vals <= best_threshold)
        right_mask_non_missing = non_missing & (feature_vals > best_threshold)

        # Tentatively assign missing to left to determine sizes
        left_mask = left_mask_non_missing.copy()
        right_mask = right_mask_non_missing.copy()
        missing_mask = ~non_missing

        if np.any(missing_mask):
            n_left = np.sum(left_mask_non_missing)
            n_right = np.sum(right_mask_non_missing)

            if n_left >= n_right:
                left_mask = left_mask | missing_mask
            else:
                right_mask = right_mask | missing_mask

        # Ensure minimum samples in leaves
        if np.sum(left_mask) < self.min_samples_leaf or np.sum(right_mask) < self.min_samples_leaf:
            return node

        # Set split information
        node.feature_index = best_feature
        node.threshold = best_threshold

        # Build children
        node.left = self._build_tree(
            X[left_mask],
            y[left_mask],
            depth + 1,
            sample_weight[left_mask] if sample_weight is not None else None,
            splitter,
            task_type,
        )
        node.right = self._build_tree(
            X[right_mask],
            y[right_mask],
            depth + 1,
            sample_weight[right_mask] if sample_weight is not None else None,
            splitter,
            task_type,
        )

        return node

    def _compute_feature_importances(self) -> None:
        """Calculate feature importances from tree."""
        if self.tree_ is None:
            self.feature_importances_ = None
        else:
            self.feature_importances_ = get_feature_importance(self.tree_, self.n_features_)

    def get_depth(self) -> int:
        """
        Get maximum depth of tree.

        Returns
        -------
        int
            Maximum depth.

        Raises
        ------
        ValueError
            If model is not fitted.
        """
        check_is_fitted(self)
        return self.tree_.get_depth()

    def get_n_leaves(self) -> int:
        """
        Get number of leaves in tree.

        Returns
        -------
        int
            Number of leaf nodes.

        Raises
        ------
        ValueError
            If model is not fitted.
        """
        check_is_fitted(self)
        return self.tree_.count_leaves()

    def get_params(self) -> Dict:
        """
        Get parameters for this estimator.

        Returns
        -------
        dict
            Parameter names mapped to their values.
        """
        return {
            "criterion": self.criterion,
            "max_depth": self.max_depth,
            "min_samples_split": self.min_samples_split,
            "min_samples_leaf": self.min_samples_leaf,
            "min_impurity_decrease": self.min_impurity_decrease,
            "max_features": self.max_features,
            "max_leaf_nodes": self.max_leaf_nodes,
            "pruning": self.pruning,
            "random_state": self.random_state,
        }

    def set_params(self, **params):
        """
        Set parameters for this estimator.

        Parameters
        ----------
        **params : dict
            Estimator parameters.

        Returns
        -------
        self
            Estimator instance.
        """
        for key, value in params.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"Invalid parameter {key}")

        self._validate_parameters()
        return self

    def save(self, filepath: str) -> None:
        """
        Save model to file using pickle.

        Parameters
        ----------
        filepath : str
            Path to save model.
        """
        check_is_fitted(self)
        with open(filepath, "wb") as f:
            pickle.dump(self, f)
        logger.info(f"Model saved to {filepath}")

    @classmethod
    def load(cls, filepath: str):
        """
        Load model from file.

        Parameters
        ----------
        filepath : str
            Path to load model from.

        Returns
        -------
        estimator
            Loaded model instance.
        """
        with open(filepath, "rb") as f:
            model = pickle.load(f)

        if not isinstance(model, cls):
            raise TypeError(f"Loaded object is not a {cls.__name__}")

        logger.info(f"Model loaded from {filepath}")
        return model


class REPTreeClassifier(BaseREPTree):
    """
    Decision tree classifier with Reduced Error Pruning.

    Parameters
    ----------
    criterion : {'gini', 'entropy'}, default='gini'
        Function to measure split quality.
    max_depth : int, optional
        Maximum depth of tree (None = unlimited).
    min_samples_split : int, default=2
        Minimum samples required to split internal node.
    min_samples_leaf : int, default=1
        Minimum samples required in a leaf node.
    min_impurity_decrease : float, default=0.0
        Minimum impurity decrease required for split.
    max_features : int, float, str, optional
        Number of features to consider at each split.
    max_leaf_nodes : int, optional
        Maximum number of leaf nodes.
    class_weight : dict, optional
        Weights associated with classes (not yet implemented).
    pruning : {'rep', None}, default=None
        Pruning strategy.
    random_state : int, optional
        Random seed.

    Attributes
    ----------
    classes_ : np.ndarray
        Unique class labels.
    n_classes_ : int
        Number of classes.
    tree_ : TreeNode
        Root node of fitted tree.
    n_features_ : int
        Number of features seen during fit.
    feature_importances_ : np.ndarray
        Feature importances.

    Examples
    --------
    >>> from reptree import REPTreeClassifier
    >>> X = [[0, 0], [1, 1]]
    >>> y = [0, 1]
    >>> clf = REPTreeClassifier(max_depth=1)
    >>> clf.fit(X, y)
    >>> clf.predict([[0.5, 0.5]])
    array([0])
    """

    def __init__(
        self,
        criterion: Literal["gini", "entropy"] = "gini",
        max_depth: Optional[int] = None,
        min_samples_split: int = 2,
        min_samples_leaf: int = 1,
        min_impurity_decrease: float = 0.0,
        max_features: Optional[Union[int, float, str]] = None,
        max_leaf_nodes: Optional[int] = None,
        class_weight: Optional[Dict] = None,
        pruning: Optional[Literal["rep"]] = None,
        random_state: Optional[int] = None,
    ):
        if criterion not in ["gini", "entropy"]:
            raise ValueError(f"criterion must be 'gini' or 'entropy', got {criterion}")

        super().__init__(
            criterion=criterion,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            min_impurity_decrease=min_impurity_decrease,
            max_features=max_features,
            max_leaf_nodes=max_leaf_nodes,
            pruning=pruning,
            random_state=random_state,
        )

        self.class_weight = class_weight

        # Will be set during fit
        self.classes_: Optional[np.ndarray] = None
        self.n_classes_: Optional[int] = None

    def fit(
        self,
        X: np.ndarray,
        y: np.ndarray,
        sample_weight: Optional[np.ndarray] = None,
        X_val: Optional[np.ndarray] = None,
        y_val: Optional[np.ndarray] = None,
    ):
        """
        Build decision tree classifier.

        Parameters
        ----------
        X : np.ndarray
            Training data of shape (n_samples, n_features).
        y : np.ndarray
            Target values of shape (n_samples,).
        sample_weight : np.ndarray, optional
            Sample weights.
        X_val : np.ndarray, optional
            Validation data for pruning.
        y_val : np.ndarray, optional
            Validation targets for pruning.

        Returns
        -------
        self
            Fitted estimator.

        Raises
        ------
        ValueError
            If pruning is enabled but validation data is not provided.
        """
        # Reset node ID counter for reproducibility
        TreeNode.reset_id_counter()

        # Validate input
        X, y = check_X_y(X, y, allow_nan=True)

        # Store classes
        self.classes_ = np.unique(y)
        self.n_classes_ = len(self.classes_)
        self.n_features_ = X.shape[1]

        # Map labels to integers
        label_map = {label: i for i, label in enumerate(self.classes_)}
        y_encoded = np.array([label_map[label] for label in y])

        # Handle pruning validation data requirement
        if self.pruning == "rep":
            if X_val is None or y_val is None:
                warnings.warn(
                    "REP pruning enabled but validation data not provided. "
                    "Automatically splitting 20% of training data for validation.",
                    UserWarning,
                )
                X, X_val, y_encoded, y_val_raw = train_test_split(
                    X, y_encoded, test_size=0.2, random_state=self.random_state
                )
                y_val = np.array([label_map[label] for label in y_val_raw])
            else:
                X_val, y_val = check_X_y(X_val, y_val, allow_nan=True)
                y_val = np.array([label_map[label] for label in y_val])

        # Create splitter
        splitter = OptimizedSplitter(
            criterion=self.criterion,
            min_samples_split=self.min_samples_split,
            min_samples_leaf=self.min_samples_leaf,
            min_impurity_decrease=self.min_impurity_decrease,
            random_state=self.random_state,
        )

        # Build tree
        logger.info("Building decision tree...")
        self.tree_ = self._build_tree(
            X,
            y_encoded,
            depth=0,
            sample_weight=sample_weight,
            splitter=splitter,
            task_type="classification",
        )

        logger.info(f"Tree built: {self.tree_.count_nodes()} nodes, depth {self.tree_.get_depth()}")

        # Apply pruning
        if self.pruning == "rep":
            logger.info("Applying REP pruning...")
            pruner = ReducedErrorPruner(task_type="classification")
            self.tree_ = pruner.prune(self.tree_, X_val, y_val)
            logger.info(
                f"Pruning complete: {pruner.pruned_nodes_} nodes removed, "
                f"{self.tree_.count_nodes()} nodes remaining"
            )

        # Compute feature importances
        self._compute_feature_importances()

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict class labels for samples.

        Parameters
        ----------
        X : np.ndarray
            Samples of shape (n_samples, n_features).

        Returns
        -------
        np.ndarray
            Predicted class labels.
        """
        check_is_fitted(self)
        X = check_array(X, ensure_2d=True, allow_nan=True)

        if X.shape[1] != self.n_features_:
            raise ValueError(
                f"X has {X.shape[1]} features, but model was trained with {self.n_features_}"
            )

        # Get predictions (probability dictionaries)
        probs = self.tree_.predict_batch(X)

        # Extract most likely class
        predictions = np.array(
            [
                max(prob.items(), key=lambda x: x[1])[0] if isinstance(prob, dict) else prob
                for prob in probs
            ]
        )

        # Map back to original labels
        return self.classes_[predictions.astype(int)]

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Predict class probabilities for samples.

        Parameters
        ----------
        X : np.ndarray
            Samples of shape (n_samples, n_features).

        Returns
        -------
        np.ndarray
            Class probabilities of shape (n_samples, n_classes).
        """
        check_is_fitted(self)
        X = check_array(X, ensure_2d=True, allow_nan=True)

        if X.shape[1] != self.n_features_:
            raise ValueError(
                f"X has {X.shape[1]} features, but model was trained with {self.n_features_}"
            )

        # Get predictions (probability dictionaries)
        probs_list = self.tree_.predict_batch(X)

        # Convert to array
        n_samples = X.shape[0]
        proba = np.zeros((n_samples, self.n_classes_))

        for i, prob_dict in enumerate(probs_list):
            if isinstance(prob_dict, dict):
                for cls, prob in prob_dict.items():
                    proba[i, cls] = prob
            else:
                # Single class prediction
                proba[i, int(prob_dict)] = 1.0

        return proba

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """
        Return accuracy score on given test data.

        Parameters
        ----------
        X : np.ndarray
            Test samples.
        y : np.ndarray
            True labels.

        Returns
        -------
        float
            Accuracy score.
        """
        from .metrics import accuracy_score

        y_pred = self.predict(X)
        return accuracy_score(y, y_pred)


class REPTreeRegressor(BaseREPTree):
    """
    Decision tree regressor with Reduced Error Pruning.

    Parameters
    ----------
    criterion : {'variance', 'mae'}, default='variance'
        Function to measure split quality.
    max_depth : int, optional
        Maximum depth of tree (None = unlimited).
    min_samples_split : int, default=2
        Minimum samples required to split internal node.
    min_samples_leaf : int, default=1
        Minimum samples required in a leaf node.
    min_impurity_decrease : float, default=0.0
        Minimum impurity decrease required for split.
    max_features : int, float, str, optional
        Number of features to consider at each split.
    max_leaf_nodes : int, optional
        Maximum number of leaf nodes.
    pruning : {'rep', None}, default=None
        Pruning strategy.
    random_state : int, optional
        Random seed.

    Attributes
    ----------
    tree_ : TreeNode
        Root node of fitted tree.
    n_features_ : int
        Number of features seen during fit.
    feature_importances_ : np.ndarray
        Feature importances.

    Examples
    --------
    >>> from reptree import REPTreeRegressor
    >>> X = [[0, 0], [1, 1]]
    >>> y = [0.5, 1.5]
    >>> reg = REPTreeRegressor(max_depth=1)
    >>> reg.fit(X, y)
    >>> reg.predict([[0.5, 0.5]])
    array([0.5])
    """

    def __init__(
        self,
        criterion: Literal["variance", "mae"] = "variance",
        max_depth: Optional[int] = None,
        min_samples_split: int = 2,
        min_samples_leaf: int = 1,
        min_impurity_decrease: float = 0.0,
        max_features: Optional[Union[int, float, str]] = None,
        max_leaf_nodes: Optional[int] = None,
        pruning: Optional[Literal["rep"]] = None,
        random_state: Optional[int] = None,
    ):
        if criterion not in ["variance", "mae"]:
            raise ValueError(f"criterion must be 'variance' or 'mae', got {criterion}")

        super().__init__(
            criterion=criterion,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            min_impurity_decrease=min_impurity_decrease,
            max_features=max_features,
            max_leaf_nodes=max_leaf_nodes,
            pruning=pruning,
            random_state=random_state,
        )

    def fit(
        self,
        X: np.ndarray,
        y: np.ndarray,
        sample_weight: Optional[np.ndarray] = None,
        X_val: Optional[np.ndarray] = None,
        y_val: Optional[np.ndarray] = None,
    ):
        """
        Build decision tree regressor.

        Parameters
        ----------
        X : np.ndarray
            Training data of shape (n_samples, n_features).
        y : np.ndarray
            Target values of shape (n_samples,).
        sample_weight : np.ndarray, optional
            Sample weights.
        X_val : np.ndarray, optional
            Validation data for pruning.
        y_val : np.ndarray, optional
            Validation targets for pruning.

        Returns
        -------
        self
            Fitted estimator.
        """
        # Reset node ID counter
        TreeNode.reset_id_counter()

        # Validate input
        X, y = check_X_y(X, y, allow_nan=True)
        self.n_features_ = X.shape[1]

        # Handle pruning validation data
        if self.pruning == "rep":
            if X_val is None or y_val is None:
                warnings.warn(
                    "REP pruning enabled but validation data not provided. "
                    "Automatically splitting 20% of training data for validation.",
                    UserWarning,
                )
                X, X_val, y, y_val = train_test_split(
                    X, y, test_size=0.2, random_state=self.random_state
                )
            else:
                X_val, y_val = check_X_y(X_val, y_val, allow_nan=True)

        # Create splitter
        splitter = OptimizedSplitter(
            criterion=self.criterion,
            min_samples_split=self.min_samples_split,
            min_samples_leaf=self.min_samples_leaf,
            min_impurity_decrease=self.min_impurity_decrease,
            random_state=self.random_state,
        )

        # Build tree
        logger.info("Building decision tree...")
        self.tree_ = self._build_tree(
            X, y, depth=0, sample_weight=sample_weight, splitter=splitter, task_type="regression"
        )

        logger.info(f"Tree built: {self.tree_.count_nodes()} nodes, depth {self.tree_.get_depth()}")

        # Apply pruning
        if self.pruning == "rep":
            logger.info("Applying REP pruning...")
            pruner = ReducedErrorPruner(task_type="regression")
            self.tree_ = pruner.prune(self.tree_, X_val, y_val)
            logger.info(
                f"Pruning complete: {pruner.pruned_nodes_} nodes removed, "
                f"{self.tree_.count_nodes()} nodes remaining"
            )

        # Compute feature importances
        self._compute_feature_importances()

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict target values for samples.

        Parameters
        ----------
        X : np.ndarray
            Samples of shape (n_samples, n_features).

        Returns
        -------
        np.ndarray
            Predicted values.
        """
        check_is_fitted(self)
        X = check_array(X, ensure_2d=True, allow_nan=True)

        if X.shape[1] != self.n_features_:
            raise ValueError(
                f"X has {X.shape[1]} features, but model was trained with {self.n_features_}"
            )

        predictions = self.tree_.predict_batch(X)
        return predictions.astype(float)

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """
        Return R² score on given test data.

        Parameters
        ----------
        X : np.ndarray
            Test samples.
        y : np.ndarray
            True values.

        Returns
        -------
        float
            R² score.
        """
        from .metrics import r2_score

        y_pred = self.predict(X)
        return r2_score(y, y_pred)
