"""
Tests for utility functions

Test Coverage:
- Array validation (check_array, check_X_y, check_is_fitted)
- Train-test split functionality
- Feature importance calculation
- Tree export functions (text, dict)
- Tree statistics
"""

import numpy as np
import pytest

from src.REPTree import REPTreeClassifier
from src.REPTree.node import TreeNode
from src.REPTree.utils import (
    check_array,
    check_is_fitted,
    check_X_y,
    export_dict,
    export_text,
    get_feature_importance,
    plot_tree_stats,
    train_test_split,
)


class TestArrayValidation:
    """Tests for array validation functions"""

    def test_check_array_valid_2d(self):
        """Test check_array with valid 2D array"""
        X = np.array([[1, 2], [3, 4]])
        X_checked = check_array(X)

        np.testing.assert_array_equal(X, X_checked)

    def test_check_array_1d_to_2d(self):
        """Test check_array converts 1D to 2D"""
        X = np.array([1, 2, 3, 4])
        X_checked = check_array(X, ensure_2d=True)

        assert X_checked.shape == (4, 1)

    def test_check_array_list_input(self):
        """Test check_array with list input"""
        X = [[1, 2], [3, 4]]
        X_checked = check_array(X)

        assert isinstance(X_checked, np.ndarray)
        assert X_checked.shape == (2, 2)

    def test_check_array_with_nan_allowed(self):
        """Test check_array allows NaN when specified"""
        X = np.array([[1, np.nan], [3, 4]])
        X_checked = check_array(X, allow_nan=True)

        assert np.isnan(X_checked[0, 1])

    def test_check_array_with_nan_not_allowed(self):
        """Test check_array raises error on NaN when not allowed"""
        X = np.array([[1, np.nan], [3, 4]])

        with pytest.raises(ValueError, match="NaN values"):
            check_array(X, allow_nan=False)

    def test_check_array_with_inf(self):
        """Test check_array raises error on infinite values"""
        X = np.array([[1, np.inf], [3, 4]])

        with pytest.raises(ValueError, match="infinite values"):
            check_array(X)

    def test_check_array_wrong_dimensions(self):
        """Test check_array raises error on wrong dimensions"""
        X = np.array([[[1, 2], [3, 4]]])  # 3D array

        with pytest.raises(ValueError, match="Expected 2D array"):
            check_array(X, ensure_2d=True)

    def test_check_X_y_valid(self):
        """Test check_X_y with valid inputs"""
        X = np.array([[1, 2], [3, 4], [5, 6]])
        y = np.array([0, 1, 0])

        X_checked, y_checked = check_X_y(X, y)

        np.testing.assert_array_equal(X, X_checked)
        np.testing.assert_array_equal(y, y_checked)

    def test_check_X_y_2d_target(self):
        """Test check_X_y converts 2D target to 1D"""
        X = np.array([[1, 2], [3, 4]])
        y = np.array([[0], [1]])  # 2D target

        X_checked, y_checked = check_X_y(X, y)

        assert y_checked.ndim == 1
        assert y_checked.shape == (2,)

    def test_check_X_y_mismatched_samples(self):
        """Test check_X_y raises error on mismatched samples"""
        X = np.array([[1, 2], [3, 4], [5, 6]])
        y = np.array([0, 1])  # Wrong length

        with pytest.raises(ValueError, match="inconsistent numbers of samples"):
            check_X_y(X, y)

    def test_check_X_y_nan_in_target(self):
        """Test check_X_y raises error on NaN in target"""
        X = np.array([[1, 2], [3, 4]])
        y = np.array([0, np.nan])

        with pytest.raises(ValueError, match="NaN values"):
            check_X_y(X, y)

    def test_check_is_fitted_fitted_model(self):
        """Test check_is_fitted passes for fitted model"""
        clf = REPTreeClassifier()
        clf.tree_ = TreeNode()  # Simulate fitted

        # Should not raise
        check_is_fitted(clf)

    def test_check_is_fitted_unfitted_model(self):
        """Test check_is_fitted raises error for unfitted model"""
        clf = REPTreeClassifier()

        with pytest.raises(ValueError, match="not fitted"):
            check_is_fitted(clf)


class TestTrainTestSplit:
    """Tests for train_test_split function"""

    def test_train_test_split_basic(self):
        """Test basic train-test split"""
        X = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]])
        y = np.array([0, 1, 0, 1, 0])

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

        assert X_train.shape[0] + X_test.shape[0] == X.shape[0]
        assert y_train.shape[0] + y_test.shape[0] == y.shape[0]
        assert X_test.shape[0] == 2  # 40% of 5

    def test_train_test_split_reproducible(self):
        """Test that split is reproducible with same random_state"""
        X = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]])
        y = np.array([0, 1, 0, 1, 0])

        X_train1, X_test1, y_train1, y_test1 = train_test_split(
            X, y, test_size=0.4, random_state=42
        )

        X_train2, X_test2, y_train2, y_test2 = train_test_split(
            X, y, test_size=0.4, random_state=42
        )

        np.testing.assert_array_equal(X_train1, X_train2)
        np.testing.assert_array_equal(X_test1, X_test2)

    def test_train_test_split_different_sizes(self):
        """Test different test sizes"""
        X = np.array([[i, i + 1] for i in range(100)])
        y = np.array([i % 2 for i in range(100)])

        for test_size in [0.1, 0.2, 0.3, 0.5]:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=42
            )

            expected_test_size = int(100 * test_size)
            assert X_test.shape[0] == expected_test_size

    def test_train_test_split_invalid_test_size(self):
        """Test that invalid test_size raises error"""
        X = np.array([[1, 2], [3, 4]])
        y = np.array([0, 1])

        with pytest.raises(ValueError, match="test_size must be between"):
            train_test_split(X, y, test_size=1.5)

        with pytest.raises(ValueError, match="test_size must be between"):
            train_test_split(X, y, test_size=0.0)


class TestFeatureImportance:
    """Tests for feature importance calculation"""

    def test_get_feature_importance_simple_tree(self):
        """Test feature importance for simple tree"""
        # Build simple tree using only feature 0
        root = TreeNode(feature_index=0, threshold=5.0, impurity=0.5, samples=100)
        root.left = TreeNode(value=0, impurity=0.0, samples=50)
        root.right = TreeNode(value=1, impurity=0.0, samples=50)

        importances = get_feature_importance(root, n_features=2)

        assert importances.shape == (2,)
        assert importances[0] > 0  # Feature 0 is used
        assert importances[1] == 0  # Feature 1 is not used
        assert np.isclose(importances.sum(), 1.0)

    def test_get_feature_importance_leaf(self):
        """Test feature importance for leaf node"""
        leaf = TreeNode(value=1, samples=10)

        importances = get_feature_importance(leaf, n_features=3)

        assert importances.shape == (3,)
        np.testing.assert_array_equal(importances, np.zeros(3))

    def test_get_feature_importance_multiple_features(self):
        """Test feature importance with multiple features"""
        # Build tree using both features
        root = TreeNode(feature_index=0, threshold=5.0, impurity=0.5, samples=100)
        root.left = TreeNode(feature_index=1, threshold=3.0, impurity=0.3, samples=50)
        root.left.left = TreeNode(value=0, impurity=0.0, samples=25)
        root.left.right = TreeNode(value=1, impurity=0.0, samples=25)
        root.right = TreeNode(value=1, impurity=0.0, samples=50)

        importances = get_feature_importance(root, n_features=2)

        assert importances[0] > 0  # Feature 0 is used
        assert importances[1] > 0  # Feature 1 is used
        assert np.isclose(importances.sum(), 1.0)


class TestTreeExport:
    """Tests for tree export functions"""

    def test_export_text_leaf(self):
        """Test exporting leaf node as text"""
        leaf = TreeNode(value=1, samples=10)

        text = export_text(leaf)

        assert "Leaf" in text
        assert "value=1" in text
        assert "samples=10" in text

    def test_export_text_simple_tree(self):
        """Test exporting simple tree as text"""
        root = TreeNode(feature_index=0, threshold=5.0, impurity=0.5, samples=100)
        root.left = TreeNode(value=0, samples=50)
        root.right = TreeNode(value=1, samples=50)

        text = export_text(root)

        assert "X[0]" in text
        assert "5.00" in text
        assert "Leaf" in text

    def test_export_text_with_feature_names(self):
        """Test exporting tree with feature names"""
        root = TreeNode(feature_index=0, threshold=5.0, samples=100)
        root.left = TreeNode(value=0, samples=50)
        root.right = TreeNode(value=1, samples=50)

        text = export_text(root, feature_names=["age", "income"])

        assert "age" in text
        assert "X[0]" not in text

    def test_export_text_max_depth(self):
        """Test exporting tree with max_depth limit"""
        # Build deeper tree
        root = TreeNode(feature_index=0, threshold=5.0, samples=100)
        root.left = TreeNode(feature_index=1, threshold=3.0, samples=50)
        root.left.left = TreeNode(value=0, samples=25)
        root.left.right = TreeNode(value=1, samples=25)
        root.right = TreeNode(value=1, samples=50)

        text = export_text(root, max_depth=1)

        assert "..." in text  # Should truncate

    def test_export_dict_leaf(self):
        """Test exporting leaf as dictionary"""
        leaf = TreeNode(node_id=5, value=42, samples=10, impurity=0.0)

        tree_dict = export_dict(leaf)

        assert tree_dict["node_id"] == 5
        assert tree_dict["leaf"] is True
        assert tree_dict["value"] == 42
        assert tree_dict["samples"] == 10

    def test_export_dict_tree(self):
        """Test exporting tree as dictionary"""
        root = TreeNode(node_id=0, feature_index=0, threshold=5.0, samples=100)
        root.left = TreeNode(node_id=1, value=0, samples=50)
        root.right = TreeNode(node_id=2, value=1, samples=50)

        tree_dict = export_dict(root)

        assert tree_dict["node_id"] == 0
        assert tree_dict["leaf"] is False
        assert tree_dict["feature_index"] == 0
        assert tree_dict["threshold"] == 5.0
        assert tree_dict["left"]["node_id"] == 1
        assert tree_dict["right"]["node_id"] == 2

    def test_plot_tree_stats(self):
        """Test plotting tree statistics"""
        root = TreeNode(feature_index=0, threshold=5.0, samples=100)
        root.left = TreeNode(feature_index=1, threshold=3.0, samples=50)
        root.left.left = TreeNode(value=0, samples=25)
        root.left.right = TreeNode(value=1, samples=25)
        root.right = TreeNode(value=1, samples=50)

        stats = plot_tree_stats(root)

        assert "Total Nodes" in stats
        assert "Leaf Nodes" in stats
        assert "Max Depth" in stats
        assert "5" in stats  # Total nodes
        assert "3" in stats  # Leaf nodes
        assert "2" in stats  # Max depth


class TestEdgeCases:
    """Tests for edge cases in utility functions"""

    def test_empty_array(self):
        """Test handling empty arrays"""
        X = np.array([]).reshape(0, 2)

        X_checked = check_array(X, ensure_2d=True)
        assert X_checked.shape == (0, 2)

    def test_single_sample(self):
        """Test handling single sample"""
        X = np.array([[1, 2]])
        y = np.array([0])

        X_checked, y_checked = check_X_y(X, y)

        assert X_checked.shape == (1, 2)
        assert y_checked.shape == (1,)

    def test_train_test_split_small_dataset(self):
        """Test train-test split on very small dataset"""
        X = np.array([[1, 2], [3, 4]])
        y = np.array([0, 1])

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

        assert X_train.shape[0] == 1
        assert X_test.shape[0] == 1
