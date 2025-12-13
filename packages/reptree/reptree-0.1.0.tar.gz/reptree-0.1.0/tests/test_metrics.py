"""
Tests for metrics module

Test Coverage:
- All metric calculations (gini, entropy, variance, MAE)
- Information gain computation
- Classification metrics (accuracy, confusion matrix)
- Regression metrics (MSE, MAE, R²)
- Edge cases (empty arrays, perfect predictions, all wrong, etc.)
- Validate against known values
"""

import numpy as np
import pytest

from src.REPTree.metrics import (
    accuracy_score,
    confusion_matrix,
    entropy,
    gini_impurity,
    information_gain,
    mae_impurity,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    variance,
)


class TestImpurityMetrics:
    """Tests for impurity measures"""

    def test_gini_impurity_pure(self):
        """Test Gini impurity for pure node (all same class)"""
        y = np.array([0, 0, 0, 0])
        assert gini_impurity(y) == 0.0

    def test_gini_impurity_balanced(self):
        """Test Gini impurity for balanced binary split"""
        y = np.array([0, 0, 1, 1])
        expected = 1.0 - (0.5**2 + 0.5**2)  # 0.5
        assert np.isclose(gini_impurity(y), expected)

    def test_gini_impurity_imbalanced(self):
        """Test Gini impurity for imbalanced split"""
        y = np.array([0, 0, 0, 1])
        expected = 1.0 - (0.75**2 + 0.25**2)  # 0.375
        assert np.isclose(gini_impurity(y), expected)

    def test_gini_impurity_multiclass(self):
        """Test Gini impurity for multiclass"""
        y = np.array([0, 1, 2, 0, 1, 2])
        expected = 1.0 - 3 * (1 / 3) ** 2  # 0.666...
        assert np.isclose(gini_impurity(y), expected, rtol=1e-5)

    def test_gini_impurity_empty(self):
        """Test Gini impurity for empty array"""
        y = np.array([])
        assert gini_impurity(y) == 0.0

    def test_entropy_pure(self):
        """Test entropy for pure node"""
        y = np.array([1, 1, 1, 1])
        assert entropy(y) == 0.0

    def test_entropy_balanced(self):
        """Test entropy for balanced binary split"""
        y = np.array([0, 0, 1, 1])
        expected = 1.0  # -2 * (0.5 * log2(0.5))
        assert np.isclose(entropy(y), expected)

    def test_entropy_imbalanced(self):
        """Test entropy for imbalanced split"""
        y = np.array([0, 0, 0, 1])
        expected = -(0.75 * np.log2(0.75) + 0.25 * np.log2(0.25))
        assert np.isclose(entropy(y), expected)

    def test_entropy_empty(self):
        """Test entropy for empty array"""
        y = np.array([])
        assert entropy(y) == 0.0

    def test_variance_constant(self):
        """Test variance for constant values"""
        y = np.array([5.0, 5.0, 5.0, 5.0])
        assert variance(y) == 0.0

    def test_variance_known_values(self):
        """Test variance with known values"""
        y = np.array([1.0, 2.0, 3.0, 4.0])
        expected = np.var(y)  # 1.25
        assert np.isclose(variance(y), expected)

    def test_variance_empty(self):
        """Test variance for empty array"""
        y = np.array([])
        assert variance(y) == 0.0

    def test_mae_impurity_constant(self):
        """Test MAE impurity for constant values"""
        y = np.array([5.0, 5.0, 5.0])
        assert mae_impurity(y) == 0.0

    def test_mae_impurity_known_values(self):
        """Test MAE impurity with known values"""
        y = np.array([1.0, 2.0, 3.0, 4.0])
        median = 2.5
        expected = np.mean(np.abs(y - median))  # 1.0
        assert np.isclose(mae_impurity(y), expected)

    def test_mae_impurity_empty(self):
        """Test MAE impurity for empty array"""
        y = np.array([])
        assert mae_impurity(y) == 0.0


class TestInformationGain:
    """Tests for information gain calculation"""

    def test_information_gain_perfect_split_gini(self):
        """Test information gain for perfect split using Gini"""
        y_parent = np.array([0, 0, 1, 1])
        y_left = np.array([0, 0])
        y_right = np.array([1, 1])

        gain = information_gain(y_parent, y_left, y_right, "gini")

        # Parent impurity: 0.5, child impurities: 0.0
        expected = 0.5
        assert np.isclose(gain, expected)

    def test_information_gain_perfect_split_entropy(self):
        """Test information gain for perfect split using entropy"""
        y_parent = np.array([0, 0, 1, 1])
        y_left = np.array([0, 0])
        y_right = np.array([1, 1])

        gain = information_gain(y_parent, y_left, y_right, "entropy")

        # Parent entropy: 1.0, child entropies: 0.0
        expected = 1.0
        assert np.isclose(gain, expected)

    def test_information_gain_no_split(self):
        """Test information gain when split doesn't improve purity"""
        y_parent = np.array([0, 1, 0, 1])
        y_left = np.array([0, 1])
        y_right = np.array([0, 1])

        gain = information_gain(y_parent, y_left, y_right, "gini")

        # Should be 0 or very close (no improvement)
        assert np.isclose(gain, 0.0, atol=1e-10)

    def test_information_gain_variance(self):
        """Test information gain for regression with variance"""
        y_parent = np.array([1.0, 2.0, 9.0, 10.0])
        y_left = np.array([1.0, 2.0])
        y_right = np.array([9.0, 10.0])

        gain = information_gain(y_parent, y_left, y_right, "variance")

        # Should have positive gain
        assert gain > 0

    def test_information_gain_mae(self):
        """Test information gain with MAE criterion"""
        y_parent = np.array([1.0, 2.0, 9.0, 10.0])
        y_left = np.array([1.0, 2.0])
        y_right = np.array([9.0, 10.0])

        gain = information_gain(y_parent, y_left, y_right, "mae")

        assert gain > 0

    def test_information_gain_empty_child(self):
        """Test information gain with empty child"""
        y_parent = np.array([0, 1, 2])
        y_left = np.array([])
        y_right = np.array([0, 1, 2])

        gain = information_gain(y_parent, y_left, y_right, "gini")

        assert gain == 0.0

    def test_information_gain_empty_parent(self):
        """Test information gain with empty parent"""
        y_parent = np.array([])
        y_left = np.array([])
        y_right = np.array([])

        gain = information_gain(y_parent, y_left, y_right, "gini")

        assert gain == 0.0

    def test_information_gain_invalid_criterion(self):
        """Test that invalid criterion raises error"""
        y_parent = np.array([0, 1])
        y_left = np.array([0])
        y_right = np.array([1])

        with pytest.raises(ValueError, match="Unknown criterion"):
            information_gain(y_parent, y_left, y_right, "invalid")


class TestClassificationMetrics:
    """Tests for classification metrics"""

    def test_accuracy_score_perfect(self):
        """Test accuracy with perfect predictions"""
        y_true = np.array([0, 1, 2, 0, 1, 2])
        y_pred = np.array([0, 1, 2, 0, 1, 2])

        assert accuracy_score(y_true, y_pred) == 1.0

    def test_accuracy_score_zero(self):
        """Test accuracy with all wrong predictions"""
        y_true = np.array([0, 0, 0, 0])
        y_pred = np.array([1, 1, 1, 1])

        assert accuracy_score(y_true, y_pred) == 0.0

    def test_accuracy_score_half(self):
        """Test accuracy with 50% correct"""
        y_true = np.array([0, 1, 0, 1])
        y_pred = np.array([0, 1, 1, 0])

        assert accuracy_score(y_true, y_pred) == 0.5

    def test_accuracy_score_empty(self):
        """Test accuracy with empty arrays"""
        y_true = np.array([])
        y_pred = np.array([])

        assert accuracy_score(y_true, y_pred) == 0.0

    def test_confusion_matrix_binary(self):
        """Test confusion matrix for binary classification"""
        y_true = np.array([0, 0, 1, 1])
        y_pred = np.array([0, 1, 0, 1])

        cm = confusion_matrix(y_true, y_pred, n_classes=2)

        expected = np.array(
            [[1, 1], [1, 1]]  # True 0: predicted 0, predicted 1  # True 1: predicted 0, predicted 1
        )

        np.testing.assert_array_equal(cm, expected)

    def test_confusion_matrix_multiclass(self):
        """Test confusion matrix for multiclass"""
        y_true = np.array([0, 1, 2, 0, 1, 2])
        y_pred = np.array([0, 1, 2, 0, 1, 2])  # Perfect predictions

        cm = confusion_matrix(y_true, y_pred, n_classes=3)

        expected = np.array([[2, 0, 0], [0, 2, 0], [0, 0, 2]])

        np.testing.assert_array_equal(cm, expected)

    def test_confusion_matrix_all_same_prediction(self):
        """Test confusion matrix when model predicts only one class"""
        y_true = np.array([0, 1, 2, 0, 1, 2])
        y_pred = np.array([0, 0, 0, 0, 0, 0])

        cm = confusion_matrix(y_true, y_pred, n_classes=3)

        expected = np.array([[2, 0, 0], [2, 0, 0], [2, 0, 0]])

        np.testing.assert_array_equal(cm, expected)


class TestRegressionMetrics:
    """Tests for regression metrics"""

    def test_mean_squared_error_perfect(self):
        """Test MSE with perfect predictions"""
        y_true = np.array([1.0, 2.0, 3.0, 4.0])
        y_pred = np.array([1.0, 2.0, 3.0, 4.0])

        assert mean_squared_error(y_true, y_pred) == 0.0

    def test_mean_squared_error_known_values(self):
        """Test MSE with known values"""
        y_true = np.array([1.0, 2.0, 3.0])
        y_pred = np.array([1.5, 2.5, 3.5])

        expected = np.mean((y_true - y_pred) ** 2)  # 0.25
        assert np.isclose(mean_squared_error(y_true, y_pred), expected)

    def test_mean_squared_error_empty(self):
        """Test MSE with empty arrays"""
        y_true = np.array([])
        y_pred = np.array([])

        assert mean_squared_error(y_true, y_pred) == 0.0

    def test_mean_absolute_error_perfect(self):
        """Test MAE with perfect predictions"""
        y_true = np.array([1.0, 2.0, 3.0, 4.0])
        y_pred = np.array([1.0, 2.0, 3.0, 4.0])

        assert mean_absolute_error(y_true, y_pred) == 0.0

    def test_mean_absolute_error_known_values(self):
        """Test MAE with known values"""
        y_true = np.array([1.0, 2.0, 3.0])
        y_pred = np.array([1.5, 2.5, 3.5])

        expected = 0.5
        assert np.isclose(mean_absolute_error(y_true, y_pred), expected)

    def test_mean_absolute_error_empty(self):
        """Test MAE with empty arrays"""
        y_true = np.array([])
        y_pred = np.array([])

        assert mean_absolute_error(y_true, y_pred) == 0.0

    def test_r2_score_perfect(self):
        """Test R² with perfect predictions"""
        y_true = np.array([1.0, 2.0, 3.0, 4.0])
        y_pred = np.array([1.0, 2.0, 3.0, 4.0])

        assert r2_score(y_true, y_pred) == 1.0

    def test_r2_score_mean_prediction(self):
        """Test R² when predicting mean (should be 0)"""
        y_true = np.array([1.0, 2.0, 3.0, 4.0])
        y_pred = np.array([2.5, 2.5, 2.5, 2.5])  # Mean of y_true

        assert np.isclose(r2_score(y_true, y_pred), 0.0, atol=1e-10)

    def test_r2_score_worse_than_mean(self):
        """Test R² with predictions worse than mean (negative R²)"""
        y_true = np.array([1.0, 2.0, 3.0, 4.0])
        y_pred = np.array([10.0, 10.0, 10.0, 10.0])  # Very bad predictions

        score = r2_score(y_true, y_pred)
        assert score < 0

    def test_r2_score_empty(self):
        """Test R² with empty arrays"""
        y_true = np.array([])
        y_pred = np.array([])

        assert r2_score(y_true, y_pred) == 0.0

    def test_r2_score_constant_true(self):
        """Test R² when true values are constant"""
        y_true = np.array([5.0, 5.0, 5.0, 5.0])
        y_pred = np.array([5.0, 5.0, 5.0, 5.0])

        # When ss_tot is 0 and ss_res is 0, should return 0
        assert r2_score(y_true, y_pred) == 0.0

    def test_r2_score_constant_true_wrong_pred(self):
        """Test R² when true values are constant but predictions are wrong"""
        y_true = np.array([5.0, 5.0, 5.0, 5.0])
        y_pred = np.array([6.0, 6.0, 6.0, 6.0])

        # When ss_tot is 0 but ss_res is not, should return -inf
        assert r2_score(y_true, y_pred) == -np.inf


class TestEdgeCases:
    """Tests for edge cases and boundary conditions"""

    def test_metrics_with_single_element(self):
        """Test metrics with single element arrays"""
        y = np.array([1])

        # Impurity metrics should work
        assert gini_impurity(y) == 0.0
        assert entropy(y) == 0.0
        assert variance(y) == 0.0
        assert mae_impurity(y) == 0.0

    def test_metrics_with_large_arrays(self):
        """Test metrics with large arrays"""
        np.random.seed(42)
        y = np.random.randint(0, 10, size=10000)

        # Should not raise errors
        gini = gini_impurity(y)
        ent = entropy(y)

        assert 0 <= gini <= 1
        assert ent >= 0

    def test_numerical_stability(self):
        """Test numerical stability with extreme values"""
        y_true = np.array([1e10, 2e10, 3e10])
        y_pred = np.array([1e10, 2e10, 3e10])

        # Should handle large numbers
        assert np.isclose(mean_squared_error(y_true, y_pred), 0.0)
        assert np.isclose(r2_score(y_true, y_pred), 1.0)
