"""
Reduced Error Pruning (REP) implementation.
"""

from typing import Dict, List, Literal

import numpy as np

from ..metrics import accuracy_score, mean_squared_error
from ..node import TreeNode


class ReducedErrorPruner:
    """
    Implements Reduced Error Pruning for decision trees.

    REP uses a bottom-up approach, replacing subtrees with leaves if
    doing so doesn't decrease validation set performance.

    Parameters
    ----------
    task_type : {'classification', 'regression'}
        Type of prediction task.

    Attributes
    ----------
    pruned_nodes_ : int
        Number of nodes pruned during last pruning operation.
    """

    def __init__(self, task_type: Literal["classification", "regression"] = "classification"):
        self.task_type = task_type
        self.pruned_nodes_ = 0

    def prune(self, root: TreeNode, X_val: np.ndarray, y_val: np.ndarray) -> TreeNode:
        """
        Prune tree using validation set.

        Parameters
        ----------
        root : TreeNode
            Root node of the tree to prune.
        X_val : np.ndarray
            Validation features of shape (n_samples, n_features).
        y_val : np.ndarray
            Validation targets of shape (n_samples,).

        Returns
        -------
        TreeNode
            Root of pruned tree (may be the same object, modified in-place).

        Examples
        --------
        >>> pruner = ReducedErrorPruner(task_type='classification')
        >>> pruned_root = pruner.prune(root, X_val, y_val)
        >>> print(f"Pruned {pruner.pruned_nodes_} nodes")
        """
        if X_val.shape[0] == 0:
            raise ValueError("Validation set is empty")

        self.pruned_nodes_ = 0

        # Route validation samples through tree once
        node_samples = self._route_samples(root, X_val)

        # Prune bottom-up
        self._prune_subtree(root, X_val, y_val, node_samples)

        return root

    def _route_samples(self, root: TreeNode, X: np.ndarray) -> Dict[int, np.ndarray]:
        """
        Route all samples through tree and cache their node indices.

        Parameters
        ----------
        root : TreeNode
            Root of tree.
        X : np.ndarray
            Feature matrix.

        Returns
        -------
        Dict[int, np.ndarray]
            Mapping from node_id to boolean mask of samples reaching that node.
        """
        n_samples = X.shape[0]
        node_samples = {}

        def route_recursive(node: TreeNode, mask: np.ndarray):
            """Recursively route samples."""
            node_samples[node.node_id] = mask.copy()

            if node.is_leaf() or not np.any(mask):
                return

            # Get feature values for samples at this node
            feature_vals = X[mask, node.feature_index]

            # Split based on threshold
            left_condition = feature_vals <= node.threshold
            right_condition = feature_vals > node.threshold

            # Handle missing values (route to larger child)
            missing_mask = np.isnan(feature_vals)
            if np.any(missing_mask):
                if node.left and node.right:
                    if node.left.samples >= node.right.samples:
                        left_condition = left_condition | missing_mask
                    else:
                        right_condition = right_condition | missing_mask
                elif node.left:
                    left_condition = left_condition | missing_mask
                elif node.right:
                    right_condition = right_condition | missing_mask

            # Create new masks for children
            left_mask = np.zeros(n_samples, dtype=bool)
            right_mask = np.zeros(n_samples, dtype=bool)

            left_mask[mask] = left_condition
            right_mask[mask] = right_condition

            # Recurse on children
            if node.left:
                route_recursive(node.left, left_mask)
            if node.right:
                route_recursive(node.right, right_mask)

        initial_mask = np.ones(n_samples, dtype=bool)
        route_recursive(root, initial_mask)

        return node_samples

    def _prune_subtree(
        self,
        node: TreeNode,
        X_val: np.ndarray,
        y_val: np.ndarray,
        node_samples: Dict[int, np.ndarray],
    ) -> None:
        """
        Recursively prune subtree using post-order traversal.

        Parameters
        ----------
        node : TreeNode
            Current node to consider.
        X_val : np.ndarray
            Validation features.
        y_val : np.ndarray
            Validation targets.
        node_samples : Dict[int, np.ndarray]
            Sample routing information.
        """
        if node.is_leaf():
            return

        # Prune children first (post-order)
        if node.left:
            self._prune_subtree(node.left, X_val, y_val, node_samples)
        if node.right:
            self._prune_subtree(node.right, X_val, y_val, node_samples)

        # Consider pruning this node
        if not node.is_leaf():  # Children might have been pruned
            self._consider_pruning(node, y_val, node_samples)

    def _consider_pruning(
        self, node: TreeNode, y_val: np.ndarray, node_samples: Dict[int, np.ndarray]
    ) -> None:
        """
        Decide whether to prune this node.

        Parameters
        ----------
        node : TreeNode
            Node to consider pruning.
        y_val : np.ndarray
            Validation targets.
        node_samples : Dict[int, np.ndarray]
            Sample routing information.
        """
        mask = node_samples.get(node.node_id, np.zeros(len(y_val), dtype=bool))

        if not np.any(mask):
            # No validation samples reach this node
            return

        y_node = y_val[mask]

        # Compute current subtree error
        subtree_preds = self._predict_subtree(node, mask, node_samples, y_val)
        subtree_error = self._compute_error(y_node, subtree_preds[mask])

        # Compute error if converted to leaf
        leaf_pred = self._get_majority_prediction(node)
        leaf_preds = np.full(np.sum(mask), leaf_pred)
        leaf_error = self._compute_error(y_node, leaf_preds)

        # Prune if leaf error is not worse
        if leaf_error <= subtree_error:
            # Count nodes being pruned
            self.pruned_nodes_ += node.count_nodes() - 1

            # Convert to leaf
            node.convert_to_leaf(leaf_pred)

    def _predict_subtree(
        self,
        node: TreeNode,
        mask: np.ndarray,
        node_samples: Dict[int, np.ndarray],
        y_val: np.ndarray,
    ) -> np.ndarray:
        """
        Get predictions from subtree for specified samples.

        Parameters
        ----------
        node : TreeNode
            Root of subtree.
        mask : np.ndarray
            Boolean mask of samples to predict.
        node_samples : Dict[int, np.ndarray]
            Sample routing information.
        y_val : np.ndarray
            All validation targets (for sizing).

        Returns
        -------
        np.ndarray
            Predictions for all samples (only valid for masked samples).
        """
        n_samples = len(y_val)
        predictions = np.empty(
            n_samples, dtype=object if self.task_type == "classification" else float
        )

        def predict_recursive(current_node: TreeNode):
            """Recursively collect predictions."""
            current_mask = node_samples.get(current_node.node_id, np.zeros(n_samples, dtype=bool))

            if not np.any(current_mask):
                return

            if current_node.is_leaf():
                pred = self._get_majority_prediction(current_node)
                predictions[current_mask] = pred
            else:
                if current_node.left:
                    predict_recursive(current_node.left)
                if current_node.right:
                    predict_recursive(current_node.right)

        predict_recursive(node)
        return predictions

    def _get_majority_prediction(self, node: TreeNode):
        """
        Get majority class or mean value from node.

        Parameters
        ----------
        node : TreeNode
            Node to get prediction from.

        Returns
        -------
        int or float
            Prediction value.
        """
        if self.task_type == "classification":
            if isinstance(node.value, dict):
                # Get class with highest probability
                return max(node.value.items(), key=lambda x: x[1])[0]
            return node.value
        else:
            return node.value

    def _compute_error(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Compute prediction error.

        Parameters
        ----------
        y_true : np.ndarray
            True targets.
        y_pred : np.ndarray
            Predicted targets.

        Returns
        -------
        float
            Error metric (lower is better).
        """
        if len(y_true) == 0:
            return 0.0

        if self.task_type == "classification":
            # Use misclassification rate (1 - accuracy)
            return 1.0 - accuracy_score(y_true, y_pred)
        else:
            # Use MSE for regression
            return mean_squared_error(y_true, y_pred)
