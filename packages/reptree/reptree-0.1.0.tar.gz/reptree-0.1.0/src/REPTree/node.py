"""
Tree node data structure for REPTree.
"""

from typing import Any, List, Optional

import numpy as np


class TreeNode:
    """
    Node in a decision tree.

    Uses __slots__ for memory efficiency and maintains bidirectional
    parent-child relationships for bottom-up pruning.

    Parameters
    ----------
    node_id : int
        Unique identifier for this node.
    parent : TreeNode, optional
        Parent node reference.
    feature_index : int, optional
        Feature index used for splitting (None for leaf nodes).
    threshold : float, optional
        Threshold value for splitting.
    value : Any
        Prediction value (class probabilities or regression value).
    samples : int
        Number of training samples at this node.
    impurity : float
        Impurity measure at this node.

    Attributes
    ----------
    left : TreeNode
        Left child node.
    right : TreeNode
        Right child node.
    """

    __slots__ = (
        "node_id",
        "parent",
        "feature_index",
        "threshold",
        "_left",
        "_right",
        "value",
        "samples",
        "impurity",
    )

    _id_counter = 0

    def __init__(
        self,
        node_id: Optional[int] = None,
        parent: Optional["TreeNode"] = None,
        feature_index: Optional[int] = None,
        threshold: Optional[float] = None,
        value: Any = None,
        samples: int = 0,
        impurity: float = 0.0,
    ):
        if node_id is None:
            self.node_id = TreeNode._id_counter
            TreeNode._id_counter += 1
        else:
            self.node_id = node_id

        self.parent = parent
        self.feature_index = feature_index
        self.threshold = threshold
        self._left: Optional[TreeNode] = None
        self._right: Optional[TreeNode] = None
        self.value = value
        self.samples = samples
        self.impurity = impurity

    @property
    def left(self) -> Optional["TreeNode"]:
        """Get left child node."""
        return self._left

    @left.setter
    def left(self, node: Optional["TreeNode"]) -> None:
        """Set left child and update its parent pointer."""
        self._left = node
        if node is not None:
            node.parent = self

    @property
    def right(self) -> Optional["TreeNode"]:
        """Get right child node."""
        return self._right

    @right.setter
    def right(self, node: Optional["TreeNode"]) -> None:
        """Set right child and update its parent pointer."""
        self._right = node
        if node is not None:
            node.parent = self

    def is_leaf(self) -> bool:
        """
        Check if this node is a leaf.

        Returns
        -------
        bool
            True if node has no children.
        """
        return self._left is None and self._right is None

    def get_depth(self) -> int:
        """
        Calculate maximum depth of subtree rooted at this node.

        Returns
        -------
        int
            Depth of subtree (0 for leaf nodes).
        """
        if self.is_leaf():
            return 0

        left_depth = self._left.get_depth() if self._left else 0
        right_depth = self._right.get_depth() if self._right else 0

        return 1 + max(left_depth, right_depth)

    def count_nodes(self) -> int:
        """
        Count total nodes in subtree.

        Returns
        -------
        int
            Total number of nodes including this one.
        """
        count = 1
        if self._left:
            count += self._left.count_nodes()
        if self._right:
            count += self._right.count_nodes()
        return count

    def count_leaves(self) -> int:
        """
        Count leaf nodes in subtree.

        Returns
        -------
        int
            Number of leaf nodes.
        """
        if self.is_leaf():
            return 1

        count = 0
        if self._left:
            count += self._left.count_leaves()
        if self._right:
            count += self._right.count_leaves()
        return count

    def predict_sample(self, x: np.ndarray) -> Any:
        """
        Predict single sample by traversing tree.

        Parameters
        ----------
        x : np.ndarray
            Feature vector of shape (n_features,).

        Returns
        -------
        Any
            Prediction value at leaf node.
        """
        if self.is_leaf():
            return self.value

        feature_val = x[self.feature_index]

        # Handle missing values: route to child with more samples
        if np.isnan(feature_val):
            if self._left and self._right:
                if self._left.samples >= self._right.samples:
                    return self._left.predict_sample(x)
                else:
                    return self._right.predict_sample(x)
            elif self._left:
                return self._left.predict_sample(x)
            elif self._right:
                return self._right.predict_sample(x)
            else:
                return self.value

        # Normal traversal
        if feature_val <= self.threshold:
            return self._left.predict_sample(x) if self._left else self.value
        else:
            return self._right.predict_sample(x) if self._right else self.value

    def predict_batch(self, X: np.ndarray) -> np.ndarray:
        """
        Predict multiple samples using vectorized operations where possible.

        Parameters
        ----------
        X : np.ndarray
            Feature matrix of shape (n_samples, n_features).

        Returns
        -------
        np.ndarray
            Predictions for all samples.
        """
        n_samples = X.shape[0]
        predictions = np.empty(n_samples, dtype=object)

        # For leaf nodes, return same value for all samples
        if self.is_leaf():
            predictions[:] = self.value
            return predictions

        # Vectorized split
        feature_vals = X[:, self.feature_index]

        # Handle missing values
        missing_mask = np.isnan(feature_vals)
        if np.any(missing_mask):
            # Route missing to larger child
            if self._left and self._right:
                larger_child = (
                    self._left if self._left.samples >= self._right.samples else self._right
                )
                predictions[missing_mask] = larger_child.predict_batch(X[missing_mask])
            elif self._left:
                predictions[missing_mask] = self._left.predict_batch(X[missing_mask])
            elif self._right:
                predictions[missing_mask] = self._right.predict_batch(X[missing_mask])
            else:
                predictions[missing_mask] = self.value

        # Route non-missing values
        non_missing = ~missing_mask
        if np.any(non_missing):
            left_mask = non_missing & (feature_vals <= self.threshold)
            right_mask = non_missing & (feature_vals > self.threshold)

            if np.any(left_mask) and self._left:
                predictions[left_mask] = self._left.predict_batch(X[left_mask])
            elif np.any(left_mask):
                predictions[left_mask] = self.value

            if np.any(right_mask) and self._right:
                predictions[right_mask] = self._right.predict_batch(X[right_mask])
            elif np.any(right_mask):
                predictions[right_mask] = self.value

        return predictions

    def convert_to_leaf(self, value: Any) -> None:
        """
        Convert internal node to leaf by removing children.

        Parameters
        ----------
        value : Any
            New prediction value for this leaf.
        """
        self._left = None
        self._right = None
        self.feature_index = None
        self.threshold = None
        self.value = value

    def get_path_from_root(self) -> List["TreeNode"]:
        """
        Get path from root to this node.

        Returns
        -------
        List[TreeNode]
            List of nodes from root to this node (inclusive).
        """
        path = []
        current = self
        while current is not None:
            path.append(current)
            current = current.parent
        return list(reversed(path))

    @classmethod
    def reset_id_counter(cls) -> None:
        """Reset the node ID counter (useful for testing)."""
        cls._id_counter = 0
