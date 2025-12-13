"""
Tests for OptimizedSplitter

Test Coverage:
- Split finding algorithms
- Impurity calculations
- Threshold selection
- Feature subsampling
- Handling missing values in splits
- Edge cases
"""

import numpy as np
import pytest

from src.REPTree.splitter import OptimizedSplitter


class TestOptimizedSplitter:
    """Tests for OptimizedSplitter class"""

    def test_initialization_gini(self):
        """Test splitter initialization with Gini criterion"""
        splitter = OptimizedSplitter(criterion="gini", random_state=42)

        assert splitter.criterion == "gini"
        assert splitter.min_samples_split == 2
        assert splitter.min_samples_leaf == 1
        assert splitter.min_impurity_decrease == 0.0

    def test_initialization_entropy(self):
        """Test splitter initialization with entropy criterion"""
        splitter = OptimizedSplitter(criterion="entropy", random_state=42)
        assert splitter.criterion == "entropy"

    def test_initialization_variance(self):
        """Test splitter initialization with variance criterion"""
        splitter = OptimizedSplitter(criterion="variance", random_state=42)
        assert splitter.criterion == "variance"

    def test_initialization_mae(self):
        """Test splitter initialization with MAE criterion"""
        splitter = OptimizedSplitter(criterion="mae", random_state=42)
        assert splitter.criterion == "mae"

    def test_find_best_split_simple(self):
        """Test finding best split on simple data"""
        X = np.array([[1], [2], [3], [4]])
        y = np.array([0, 0, 1, 1])

        splitter = OptimizedSplitter(criterion="gini", random_state=42)
        feature_idx, threshold, gain = splitter.find_best_split(X, y)

        assert feature_idx is not None
        assert threshold is not None
        assert gain > 0

    def test_find_best_split_perfect_separation(self):
        """Test finding split that perfectly separates classes"""
        X = np.array([[1], [2], [10], [11]])
        y = np.array([0, 0, 1, 1])

        splitter = OptimizedSplitter(criterion="gini", random_state=42)
        feature_idx, threshold, gain = splitter.find_best_split(X, y)

        # Should find a threshold between 2 and 10
        assert 2 < threshold < 10
        assert gain > 0

    def test_find_best_split_multifeature(self):
        """Test finding best split with multiple features"""
        X = np.array([[1, 10], [2, 11], [10, 1], [11, 2]])
        y = np.array([0, 0, 1, 1])

        splitter = OptimizedSplitter(criterion="gini", random_state=42)
        feature_idx, threshold, gain = splitter.find_best_split(X, y)

        assert feature_idx in [0, 1]
        assert gain > 0

    def test_find_best_split_no_split(self):
        """Test when no valid split is possible"""
        X = np.array([[1], [1], [1], [1]])  # All same feature value
        y = np.array([0, 0, 1, 1])

        splitter = OptimizedSplitter(criterion="gini", random_state=42)
        feature_idx, threshold, gain = splitter.find_best_split(X, y)

        # Should return None when no split is possible
        assert feature_idx is None
        assert threshold is None
        assert gain == 0.0

    def test_find_best_split_min_samples_split(self):
        """Test that min_samples_split is respected"""
        X = np.array([[1], [2]])
        y = np.array([0, 1])

        splitter = OptimizedSplitter(criterion="gini", min_samples_split=10, random_state=42)
        feature_idx, threshold, gain = splitter.find_best_split(X, y)

        assert feature_idx is None  # Too few samples to split

    def test_find_best_split_min_samples_leaf(self):
        """Test that min_samples_leaf is respected"""
        X = np.array([[1], [2], [3], [4]])
        y = np.array([0, 0, 1, 1])

        splitter = OptimizedSplitter(
            criterion="gini",
            min_samples_leaf=3,  # Each child must have at least 3 samples
            random_state=42,
        )
        feature_idx, threshold, gain = splitter.find_best_split(X, y)

        # With 4 samples total and min_leaf=3, no valid split
        assert feature_idx is None

    def test_find_best_split_min_impurity_decrease(self):
        """Test that min_impurity_decrease is respected"""
        X = np.array([[1], [2], [3], [4]])
        y = np.array([0, 0, 0, 1])  # Minimal improvement possible

        splitter = OptimizedSplitter(
            criterion="gini", min_impurity_decrease=0.5, random_state=42  # Very high threshold
        )
        feature_idx, threshold, gain = splitter.find_best_split(X, y)

        # Gain might not meet threshold
        if gain < 0.5:
            assert feature_idx is None

    def test_find_best_split_with_feature_subset(self):
        """Test finding split with feature subset"""
        X = np.array([[1, 10, 100], [2, 11, 101], [10, 1, 100], [11, 2, 101]])
        y = np.array([0, 0, 1, 1])

        splitter = OptimizedSplitter(criterion="gini", random_state=42)
        feature_indices = np.array([0, 1])  # Only consider first two features

        feature_idx, threshold, gain = splitter.find_best_split(
            X, y, feature_indices=feature_indices
        )

        # Should only select from features 0 or 1
        assert feature_idx in [0, 1] or feature_idx is None

    def test_find_best_split_with_nan(self):
        """Test finding split with missing values"""
        X = np.array([[1], [2], [np.nan], [10], [11]])
        y = np.array([0, 0, 0, 1, 1])

        splitter = OptimizedSplitter(criterion="gini", random_state=42)
        feature_idx, threshold, gain = splitter.find_best_split(X, y)

        # Should handle NaN gracefully
        assert feature_idx is not None or (feature_idx is None and gain == 0.0)

    def test_compute_leaf_value_classification(self):
        """Test computing leaf value for classification"""
        y = np.array([0, 0, 1, 1, 1])

        splitter = OptimizedSplitter(criterion="gini", random_state=42)
        value = splitter.compute_leaf_value(y, task_type="classification")

        assert isinstance(value, dict)
        assert 0 in value and 1 in value
        assert value[1] > value[0]  # More 1s than 0s

    def test_compute_leaf_value_regression_mean(self):
        """Test computing leaf value for regression (mean)"""
        y = np.array([1.0, 2.0, 3.0, 4.0])

        splitter = OptimizedSplitter(criterion="variance", random_state=42)
        value = splitter.compute_leaf_value(y, task_type="regression")

        assert np.isclose(value, 2.5)  # Mean

    def test_compute_leaf_value_regression_median(self):
        """Test computing leaf value for regression (median with MAE)"""
        y = np.array([1.0, 2.0, 3.0, 4.0])

        splitter = OptimizedSplitter(criterion="mae", random_state=42)
        value = splitter.compute_leaf_value(y, task_type="regression")

        assert np.isclose(value, 2.5)  # Median

    def test_compute_impurity_gini(self):
        """Test computing Gini impurity"""
        y = np.array([0, 0, 1, 1])

        splitter = OptimizedSplitter(criterion="gini", random_state=42)
        impurity = splitter.compute_impurity(y)

        expected = 0.5
        assert np.isclose(impurity, expected)

    def test_compute_impurity_entropy(self):
        """Test computing entropy"""
        y = np.array([0, 0, 1, 1])

        splitter = OptimizedSplitter(criterion="entropy", random_state=42)
        impurity = splitter.compute_impurity(y)

        expected = 1.0
        assert np.isclose(impurity, expected)

    def test_compute_impurity_variance(self):
        """Test computing variance"""
        y = np.array([1.0, 2.0, 3.0, 4.0])

        splitter = OptimizedSplitter(criterion="variance", random_state=42)
        impurity = splitter.compute_impurity(y)

        expected = np.var(y)
        assert np.isclose(impurity, expected)

    def test_compute_impurity_mae(self):
        """Test computing MAE impurity"""
        y = np.array([1.0, 2.0, 3.0, 4.0])

        splitter = OptimizedSplitter(criterion="mae", random_state=42)
        impurity = splitter.compute_impurity(y)

        assert impurity > 0

    def test_get_candidate_thresholds_few_unique(self):
        """Test threshold selection with few unique values"""
        unique_vals = np.array([1.0, 2.0, 3.0])

        splitter = OptimizedSplitter(criterion="gini", random_state=42)
        thresholds = splitter._get_candidate_thresholds(unique_vals)

        # Should use midpoints
        expected = np.array([1.5, 2.5])
        np.testing.assert_array_almost_equal(thresholds, expected)

    def test_get_candidate_thresholds_many_unique(self):
        """Test threshold selection with many unique values"""
        unique_vals = np.arange(100)

        splitter = OptimizedSplitter(criterion="gini", random_state=42)
        thresholds = splitter._get_candidate_thresholds(unique_vals)

        # Should use percentile-based binning
        assert len(thresholds) <= splitter.MAX_UNIQUE_VALUES

    def test_regression_split(self):
        """Test finding split for regression task"""
        X = np.array([[1], [2], [3], [4], [5], [6]])
        y = np.array([1.0, 2.0, 3.0, 10.0, 11.0, 12.0])

        splitter = OptimizedSplitter(criterion="variance", random_state=42)
        feature_idx, threshold, gain = splitter.find_best_split(X, y)

        # Should find a threshold that separates low and high values
        assert feature_idx is not None
        assert gain > 0
        assert 3 < threshold < 4  # Should split between 3 and 10

    def test_all_same_class(self):
        """Test splitting when all samples have same class"""
        X = np.array([[1], [2], [3], [4]])
        y = np.array([0, 0, 0, 0])

        splitter = OptimizedSplitter(criterion="gini", random_state=42)
        feature_idx, threshold, gain = splitter.find_best_split(X, y)

        # No gain possible with pure node
        assert gain == 0.0

    def test_binary_features(self):
        """Test splitting on binary features"""
        X = np.array([[0], [0], [1], [1]])
        y = np.array([0, 0, 1, 1])

        splitter = OptimizedSplitter(criterion="gini", random_state=42)
        feature_idx, threshold, gain = splitter.find_best_split(X, y)

        assert feature_idx is not None
        assert 0 < threshold < 1
        assert gain > 0

    def test_evaluate_split_with_missing(self):
        """Test split evaluation with missing values"""
        feature_vals = np.array([1.0, 2.0, np.nan, 10.0, 11.0])
        y = np.array([0, 0, 0, 1, 1])
        threshold = 5.0

        splitter = OptimizedSplitter(criterion="gini", random_state=42)
        gain = splitter._evaluate_split(feature_vals, y, threshold)

        # Should handle NaN by routing to larger child
        assert gain >= 0
