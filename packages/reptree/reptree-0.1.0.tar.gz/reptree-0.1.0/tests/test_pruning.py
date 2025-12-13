"""
Tests for Reduced Error Pruning (REP)

Test Coverage:
- REP algorithm correctness
- Pruning on various tree structures
- Comparison of pruned vs. unpruned performance
- Edge cases (empty validation set, single node, etc.)
"""

import numpy as np
import pytest

from src.REPTree import REPTreeClassifier, REPTreeRegressor
from src.REPTree.node import TreeNode
from src.REPTree.pruning.rep import ReducedErrorPruner
from src.REPTree.utils import train_test_split


class TestReducedErrorPruner:
    """Tests for ReducedErrorPruner class"""

    def test_initialization_classification(self):
        """Test pruner initialization for classification"""
        pruner = ReducedErrorPruner(task_type="classification")

        assert pruner.task_type == "classification"
        assert pruner.pruned_nodes_ == 0

    def test_initialization_regression(self):
        """Test pruner initialization for regression"""
        pruner = ReducedErrorPruner(task_type="regression")

        assert pruner.task_type == "regression"
        assert pruner.pruned_nodes_ == 0

    def test_prune_simple_tree(self):
        """Test pruning a simple tree"""
        # Build a simple tree
        root = TreeNode(feature_index=0, threshold=5.0, samples=100)
        root.left = TreeNode(value={0: 0.9, 1: 0.1}, samples=50)
        root.right = TreeNode(value={0: 0.1, 1: 0.9}, samples=50)

        # Validation data
        X_val = np.array([[3], [4], [7], [8]])
        y_val = np.array([0, 0, 1, 1])

        pruner = ReducedErrorPruner(task_type="classification")
        pruned_tree = pruner.prune(root, X_val, y_val)

        assert pruned_tree is not None

    def test_prune_with_empty_validation_raises_error(self):
        """Test that empty validation set raises error"""
        root = TreeNode(value=1)
        X_val = np.array([]).reshape(0, 1)
        y_val = np.array([])

        pruner = ReducedErrorPruner(task_type="classification")

        with pytest.raises(ValueError, match="Validation set is empty"):
            pruner.prune(root, X_val, y_val)

    def test_prune_leaf_node(self):
        """Test pruning a single leaf node (should do nothing)"""
        root = TreeNode(value=1, samples=10)

        X_val = np.array([[1], [2], [3]])
        y_val = np.array([1, 1, 1])

        pruner = ReducedErrorPruner(task_type="classification")
        pruned_tree = pruner.prune(root, X_val, y_val)

        assert pruned_tree.is_leaf()
        assert pruner.pruned_nodes_ == 0

    def test_prune_improves_generalization(self):
        """Test that pruning can improve validation performance"""
        from sklearn.datasets import make_classification

        X, y = make_classification(
            n_samples=200, n_features=10, n_informative=5, n_redundant=5, random_state=42
        )

        X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.4, random_state=42)
        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp, test_size=0.5, random_state=42
        )

        # Train without pruning
        clf_no_prune = REPTreeClassifier(random_state=42)
        clf_no_prune.fit(X_train, y_train)
        nodes_before = clf_no_prune.tree_.count_nodes()

        # Train with pruning
        clf_with_prune = REPTreeClassifier(pruning="rep", random_state=42)
        clf_with_prune.fit(X_train, y_train, X_val=X_val, y_val=y_val)
        nodes_after = clf_with_prune.tree_.count_nodes()

        # Pruned tree should have fewer or equal nodes
        assert nodes_after <= nodes_before

    def test_prune_classification_tree(self):
        """Test pruning on classification tree"""
        from sklearn.datasets import load_iris

        iris = load_iris()
        X, y = iris.data, iris.target

        X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.4, random_state=42)
        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp, test_size=0.5, random_state=42
        )

        # Build overfitted tree
        clf = REPTreeClassifier(max_depth=None, random_state=42)
        clf.fit(X_train, y_train)

        original_nodes = clf.tree_.count_nodes()

        # Prune
        pruner = ReducedErrorPruner(task_type="classification")
        pruned_tree = pruner.prune(clf.tree_, X_val, y_val)

        pruned_nodes = pruned_tree.count_nodes()

        assert pruned_nodes <= original_nodes
        assert pruner.pruned_nodes_ >= 0

    def test_prune_regression_tree(self):
        """Test pruning on regression tree"""
        from sklearn.datasets import make_regression

        X, y = make_regression(n_samples=200, n_features=10, random_state=42)

        X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.4, random_state=42)
        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp, test_size=0.5, random_state=42
        )

        # Build tree
        reg = REPTreeRegressor(max_depth=None, random_state=42)
        reg.fit(X_train, y_train)

        original_nodes = reg.tree_.count_nodes()

        # Prune
        pruner = ReducedErrorPruner(task_type="regression")
        pruned_tree = pruner.prune(reg.tree_, X_val, y_val)

        pruned_nodes = pruned_tree.count_nodes()

        assert pruned_nodes <= original_nodes

    def test_route_samples(self):
        """Test sample routing through tree"""
        # Build simple tree
        root = TreeNode(feature_index=0, threshold=5.0, samples=4)
        root.left = TreeNode(value=0, samples=2)
        root.right = TreeNode(value=1, samples=2)

        X = np.array([[3], [4], [7], [8]])

        pruner = ReducedErrorPruner(task_type="classification")
        node_samples = pruner._route_samples(root, X)

        # Check that all nodes received some samples
        assert root.node_id in node_samples
        assert root.left.node_id in node_samples
        assert root.right.node_id in node_samples

        # Check routing is correct
        root_mask = node_samples[root.node_id]
        assert np.sum(root_mask) == 4  # All samples reach root

        left_mask = node_samples[root.left.node_id]
        assert np.sum(left_mask) == 2  # 3, 4 <= 5

        right_mask = node_samples[root.right.node_id]
        assert np.sum(right_mask) == 2  # 7, 8 > 5

    def test_get_majority_prediction_classification(self):
        """Test getting majority prediction for classification"""
        node = TreeNode(value={0: 0.3, 1: 0.7})

        pruner = ReducedErrorPruner(task_type="classification")
        prediction = pruner._get_majority_prediction(node)

        assert prediction == 1  # Class with highest probability

    def test_get_majority_prediction_regression(self):
        """Test getting prediction for regression"""
        node = TreeNode(value=42.5)

        pruner = ReducedErrorPruner(task_type="regression")
        prediction = pruner._get_majority_prediction(node)

        assert prediction == 42.5

    def test_compute_error_classification(self):
        """Test error computation for classification"""
        y_true = np.array([0, 0, 1, 1])
        y_pred = np.array([0, 1, 1, 1])  # 75% accuracy

        pruner = ReducedErrorPruner(task_type="classification")
        error = pruner._compute_error(y_true, y_pred)

        assert np.isclose(error, 0.25)  # 1 - 0.75

    def test_compute_error_regression(self):
        """Test error computation for regression"""
        y_true = np.array([1.0, 2.0, 3.0, 4.0])
        y_pred = np.array([1.5, 2.5, 3.5, 4.5])

        pruner = ReducedErrorPruner(task_type="regression")
        error = pruner._compute_error(y_true, y_pred)

        expected_mse = 0.25
        assert np.isclose(error, expected_mse)

    def test_pruning_reduces_overfitting(self):
        """Test that pruning reduces overfitting"""
        from sklearn.datasets import make_classification

        X, y = make_classification(
            n_samples=300, n_features=20, n_informative=10, n_redundant=10, random_state=42
        )

        X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.5, random_state=42)
        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp, test_size=0.5, random_state=42
        )

        # Train deep tree (likely overfitted)
        clf = REPTreeClassifier(max_depth=20, min_samples_leaf=1, random_state=42)
        clf.fit(X_train, y_train)

        train_score_before = clf.score(X_train, y_train)
        val_score_before = clf.score(X_val, y_val)

        # Prune
        pruner = ReducedErrorPruner(task_type="classification")
        clf.tree_ = pruner.prune(clf.tree_, X_val, y_val)

        train_score_after = clf.score(X_train, y_train)
        val_score_after = clf.score(X_val, y_val)

        # After pruning, validation score should not decrease significantly
        # (and might even improve in some cases)
        assert val_score_after >= val_score_before - 0.05

    def test_pruning_with_missing_values(self):
        """Test pruning with missing values in validation set"""
        X_train = np.array([[1, 2], [2, 3], [3, 4], [4, 5]])
        y_train = np.array([0, 0, 1, 1])

        X_val = np.array([[1.5, np.nan], [3.5, 4.5]])
        y_val = np.array([0, 1])

        clf = REPTreeClassifier(pruning="rep", random_state=42)
        clf.fit(X_train, y_train, X_val=X_val, y_val=y_val)

        # Should handle NaN gracefully
        assert clf.tree_ is not None

    def test_pruned_nodes_count(self):
        """Test that pruned_nodes_ attribute is correctly updated"""
        from sklearn.datasets import load_iris

        iris = load_iris()
        X, y = iris.data, iris.target

        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.3, random_state=42)

        clf = REPTreeClassifier(random_state=42)
        clf.fit(X_train, y_train)

        nodes_before = clf.tree_.count_nodes()

        pruner = ReducedErrorPruner(task_type="classification")
        clf.tree_ = pruner.prune(clf.tree_, X_val, y_val)

        nodes_after = clf.tree_.count_nodes()

        # pruned_nodes_ should equal difference in node count
        assert pruner.pruned_nodes_ == (nodes_before - nodes_after)
