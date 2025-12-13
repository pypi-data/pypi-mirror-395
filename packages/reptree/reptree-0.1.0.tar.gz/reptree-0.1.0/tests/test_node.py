"""
Tests for TreeNode data structure

Test Coverage:
- Node creation and properties
- Tree traversal methods
- Depth calculation
- Leaf counting
- Prediction methods (single and batch)
- Parent-child relationships
"""

import numpy as np
import pytest

from src.REPTree.node import TreeNode


class TestTreeNode:
    """Tests for TreeNode class"""

    def test_node_creation_default(self):
        """Test creating node with default parameters"""
        node = TreeNode()

        assert node.node_id is not None
        assert node.parent is None
        assert node.feature_index is None
        assert node.threshold is None
        assert node.value is None
        assert node.samples == 0
        assert node.impurity == 0.0
        assert node.left is None
        assert node.right is None

    def test_node_creation_with_params(self):
        """Test creating node with specific parameters"""
        node = TreeNode(
            node_id=5,
            feature_index=2,
            threshold=3.5,
            value={0: 0.3, 1: 0.7},
            samples=100,
            impurity=0.42,
        )

        assert node.node_id == 5
        assert node.feature_index == 2
        assert node.threshold == 3.5
        assert node.value == {0: 0.3, 1: 0.7}
        assert node.samples == 100
        assert node.impurity == 0.42

    def test_is_leaf_true(self):
        """Test is_leaf returns True for leaf nodes"""
        node = TreeNode(value=1.5)
        assert node.is_leaf() is True

    def test_is_leaf_false(self):
        """Test is_leaf returns False for internal nodes"""
        node = TreeNode(feature_index=0, threshold=2.0)
        node.left = TreeNode(value=0)
        node.right = TreeNode(value=1)

        assert node.is_leaf() is False

    def test_parent_child_relationship(self):
        """Test that parent-child relationships are maintained"""
        parent = TreeNode(feature_index=0, threshold=5.0)
        left_child = TreeNode(value=0)
        right_child = TreeNode(value=1)

        parent.left = left_child
        parent.right = right_child

        assert left_child.parent is parent
        assert right_child.parent is parent

    def test_get_depth_leaf(self):
        """Test get_depth for leaf node returns 0"""
        node = TreeNode(value=1)
        assert node.get_depth() == 0

    def test_get_depth_simple_tree(self):
        """Test get_depth for simple two-level tree"""
        root = TreeNode(feature_index=0, threshold=5.0)
        root.left = TreeNode(value=0)
        root.right = TreeNode(value=1)

        assert root.get_depth() == 1

    def test_get_depth_unbalanced_tree(self):
        """Test get_depth for unbalanced tree"""
        root = TreeNode(feature_index=0, threshold=5.0)
        root.left = TreeNode(feature_index=1, threshold=3.0)
        root.left.left = TreeNode(value=0)
        root.left.right = TreeNode(value=1)
        root.right = TreeNode(value=2)

        assert root.get_depth() == 2

    def test_count_nodes_single(self):
        """Test count_nodes for single node"""
        node = TreeNode(value=1)
        assert node.count_nodes() == 1

    def test_count_nodes_tree(self):
        """Test count_nodes for tree with multiple nodes"""
        root = TreeNode(feature_index=0, threshold=5.0)
        root.left = TreeNode(feature_index=1, threshold=3.0)
        root.left.left = TreeNode(value=0)
        root.left.right = TreeNode(value=1)
        root.right = TreeNode(value=2)

        assert root.count_nodes() == 5

    def test_count_leaves_single(self):
        """Test count_leaves for single leaf"""
        node = TreeNode(value=1)
        assert node.count_leaves() == 1

    def test_count_leaves_tree(self):
        """Test count_leaves for tree"""
        root = TreeNode(feature_index=0, threshold=5.0)
        root.left = TreeNode(feature_index=1, threshold=3.0)
        root.left.left = TreeNode(value=0)
        root.left.right = TreeNode(value=1)
        root.right = TreeNode(value=2)

        assert root.count_leaves() == 3

    def test_predict_sample_leaf(self):
        """Test predict_sample for leaf node"""
        node = TreeNode(value=42)
        x = np.array([1, 2, 3])

        prediction = node.predict_sample(x)
        assert prediction == 42

    def test_predict_sample_simple_tree(self):
        """Test predict_sample for simple tree"""
        root = TreeNode(feature_index=0, threshold=5.0)
        root.left = TreeNode(value="left")
        root.right = TreeNode(value="right")

        x_left = np.array([3.0, 1.0])
        x_right = np.array([7.0, 1.0])

        assert root.predict_sample(x_left) == "left"
        assert root.predict_sample(x_right) == "right"

    def test_predict_sample_with_nan(self):
        """Test predict_sample handles NaN values"""
        root = TreeNode(feature_index=0, threshold=5.0, samples=100)
        root.left = TreeNode(value="left", samples=60)
        root.right = TreeNode(value="right", samples=40)

        x_nan = np.array([np.nan, 1.0])

        # Should route to larger child (left has more samples)
        prediction = root.predict_sample(x_nan)
        assert prediction == "left"

    def test_predict_batch(self):
        """Test predict_batch for multiple samples"""
        root = TreeNode(feature_index=0, threshold=5.0)
        root.left = TreeNode(value=0)
        root.right = TreeNode(value=1)

        X = np.array([[3.0, 1.0], [7.0, 2.0], [4.0, 3.0], [8.0, 4.0]])

        predictions = root.predict_batch(X)

        assert predictions.shape == (4,)
        assert predictions[0] == 0  # 3 <= 5
        assert predictions[1] == 1  # 7 > 5
        assert predictions[2] == 0  # 4 <= 5
        assert predictions[3] == 1  # 8 > 5

    def test_predict_batch_with_nan(self):
        """Test predict_batch handles NaN values"""
        root = TreeNode(feature_index=0, threshold=5.0, samples=100)
        root.left = TreeNode(value=0, samples=60)
        root.right = TreeNode(value=1, samples=40)

        X = np.array([[3.0, 1.0], [np.nan, 2.0], [7.0, 3.0]])

        predictions = root.predict_batch(X)

        assert predictions.shape == (3,)
        assert predictions[0] == 0
        assert predictions[1] == 0  # NaN routes to left (larger child)
        assert predictions[2] == 1

    def test_convert_to_leaf(self):
        """Test convert_to_leaf removes children"""
        root = TreeNode(feature_index=0, threshold=5.0)
        root.left = TreeNode(value=0)
        root.right = TreeNode(value=1)

        root.convert_to_leaf(value=42)

        assert root.is_leaf()
        assert root.value == 42
        assert root.left is None
        assert root.right is None
        assert root.feature_index is None
        assert root.threshold is None

    def test_get_path_from_root_single_node(self):
        """Test get_path_from_root for single node"""
        node = TreeNode()
        path = node.get_path_from_root()

        assert len(path) == 1
        assert path[0] is node

    def test_get_path_from_root_tree(self):
        """Test get_path_from_root for node in tree"""
        root = TreeNode(node_id=0)
        child = TreeNode(node_id=1)
        grandchild = TreeNode(node_id=2)

        root.left = child
        child.left = grandchild

        path = grandchild.get_path_from_root()

        assert len(path) == 3
        assert path[0] is root
        assert path[1] is child
        assert path[2] is grandchild

    def test_reset_id_counter(self):
        """Test reset_id_counter resets node IDs"""
        TreeNode.reset_id_counter()

        node1 = TreeNode()
        node2 = TreeNode()

        assert node1.node_id == 0
        assert node2.node_id == 1

        TreeNode.reset_id_counter()
        node3 = TreeNode()
        assert node3.node_id == 0

    def test_node_id_auto_increment(self):
        """Test that node IDs auto-increment"""
        TreeNode.reset_id_counter()

        nodes = [TreeNode() for _ in range(5)]

        for i, node in enumerate(nodes):
            assert node.node_id == i

    def test_classification_prediction(self):
        """Test prediction with classification probabilities"""
        root = TreeNode(feature_index=0, threshold=5.0)
        root.left = TreeNode(value={0: 0.8, 1: 0.2})
        root.right = TreeNode(value={0: 0.1, 1: 0.9})

        x_left = np.array([3.0])
        x_right = np.array([7.0])

        pred_left = root.predict_sample(x_left)
        pred_right = root.predict_sample(x_right)

        assert isinstance(pred_left, dict)
        assert isinstance(pred_right, dict)
        assert pred_left == {0: 0.8, 1: 0.2}
        assert pred_right == {0: 0.1, 1: 0.9}

    def test_deep_tree(self):
        """Test with a deeper tree structure"""
        # Build a tree of depth 4
        root = TreeNode(feature_index=0, threshold=10.0)
        root.left = TreeNode(feature_index=1, threshold=5.0)
        root.right = TreeNode(feature_index=1, threshold=15.0)

        root.left.left = TreeNode(feature_index=2, threshold=2.0)
        root.left.right = TreeNode(value=1)

        root.right.left = TreeNode(value=2)
        root.right.right = TreeNode(value=3)

        root.left.left.left = TreeNode(value=0)
        root.left.left.right = TreeNode(value=0.5)

        assert root.get_depth() == 3
        assert root.count_nodes() == 9
        assert root.count_leaves() == 5

    def test_slots_memory_efficiency(self):
        """Test that __slots__ is properly defined"""
        node = TreeNode()

        # Should not be able to add arbitrary attributes
        with pytest.raises(AttributeError):
            node.arbitrary_attribute = "test"
