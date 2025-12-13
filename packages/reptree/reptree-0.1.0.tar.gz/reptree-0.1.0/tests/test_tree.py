"""
Tests for REPTreeClassifier and REPTreeRegressor

Test Coverage:
- Tree construction and fitting
- Prediction accuracy
- Parameter validation
- Edge cases (empty data, single class, etc.)
- Pruning functionality
- Model persistence (save/load)
"""

import os
import tempfile

import numpy as np
import pytest
from sklearn.datasets import load_iris, make_regression

from src.REPTree import REPTreeClassifier, REPTreeRegressor
from src.REPTree.utils import train_test_split


class TestREPTreeClassifier:
    """Comprehensive tests for REPTreeClassifier"""

    def test_initialization_default_params(self):
        """Test classifier initialization with default parameters"""
        clf = REPTreeClassifier()
        assert clf.criterion == "gini"
        assert clf.max_depth is None
        assert clf.min_samples_split == 2
        assert clf.min_samples_leaf == 1
        assert clf.pruning is None
        assert clf.tree_ is None

    def test_initialization_custom_params(self):
        """Test classifier initialization with custom parameters"""
        clf = REPTreeClassifier(
            criterion="entropy",
            max_depth=5,
            min_samples_split=10,
            min_samples_leaf=5,
            max_features="sqrt",
            pruning="rep",
            random_state=42,
        )
        assert clf.criterion == "entropy"
        assert clf.max_depth == 5
        assert clf.min_samples_split == 10
        assert clf.min_samples_leaf == 5
        assert clf.max_features == "sqrt"
        assert clf.pruning == "rep"
        assert clf.random_state == 42

    def test_invalid_criterion(self):
        """Test that invalid criterion raises ValueError"""
        with pytest.raises(ValueError, match="criterion must be"):
            REPTreeClassifier(criterion="invalid")

    def test_invalid_max_depth(self):
        """Test that invalid max_depth raises ValueError"""
        with pytest.raises(ValueError, match="max_depth must be"):
            REPTreeClassifier(max_depth=0)
        with pytest.raises(ValueError, match="max_depth must be"):
            REPTreeClassifier(max_depth=-1)

    def test_invalid_min_samples_split(self):
        """Test that invalid min_samples_split raises ValueError"""
        with pytest.raises(ValueError, match="min_samples_split must be"):
            REPTreeClassifier(min_samples_split=1)
        with pytest.raises(ValueError, match="min_samples_split must be"):
            REPTreeClassifier(min_samples_split=0)

    def test_invalid_min_samples_leaf(self):
        """Test that invalid min_samples_leaf raises ValueError"""
        with pytest.raises(ValueError, match="min_samples_leaf must be"):
            REPTreeClassifier(min_samples_leaf=0)
        with pytest.raises(ValueError, match="min_samples_leaf must be"):
            REPTreeClassifier(min_samples_leaf=-1)

    def test_fit_simple_data(self, simple_classification_data):
        """Test fitting on simple binary classification data"""
        X, y = simple_classification_data
        clf = REPTreeClassifier(random_state=42)
        clf.fit(X, y)

        assert clf.tree_ is not None
        assert clf.n_features_ == X.shape[1]
        assert clf.n_classes_ == 2
        assert len(clf.classes_) == 2

    def test_fit_iris_dataset(self, iris_dataset):
        """Test fitting on iris dataset (multiclass)"""
        X, y = iris_dataset
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        clf = REPTreeClassifier(random_state=42)
        clf.fit(X_train, y_train)

        assert clf.tree_ is not None
        assert clf.n_features_ == X_train.shape[1]
        assert clf.n_classes_ == 3
        assert clf.feature_importances_ is not None
        assert clf.feature_importances_.shape == (X_train.shape[1],)

    def test_fit_with_pruning_no_validation_data(self, iris_dataset):
        """Test that pruning without validation data triggers auto-split"""
        X, y = iris_dataset
        clf = REPTreeClassifier(pruning="rep", random_state=42)

        with pytest.warns(UserWarning, match="validation data not provided"):
            clf.fit(X, y)

        assert clf.tree_ is not None

    def test_fit_with_pruning_with_validation_data(self, iris_dataset):
        """Test fitting with explicit validation data for pruning"""
        X, y = iris_dataset
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)
        X_train, X_val, y_train, y_val = train_test_split(
            X_train, y_train, test_size=0.25, random_state=42
        )

        clf = REPTreeClassifier(pruning="rep", random_state=42)
        clf.fit(X_train, y_train, X_val=X_val, y_val=y_val)

        assert clf.tree_ is not None

    def test_predict(self, iris_dataset):
        """Test prediction functionality"""
        X, y = iris_dataset
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        clf = REPTreeClassifier(random_state=42)
        clf.fit(X_train, y_train)

        predictions = clf.predict(X_test)

        assert predictions.shape == y_test.shape
        assert all(pred in clf.classes_ for pred in predictions)
        assert predictions.dtype in [np.int64, np.int32]

    def test_predict_proba(self, iris_dataset):
        """Test probability prediction"""
        X, y = iris_dataset
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        clf = REPTreeClassifier(random_state=42)
        clf.fit(X_train, y_train)

        probas = clf.predict_proba(X_test)

        assert probas.shape == (X_test.shape[0], clf.n_classes_)
        assert np.allclose(probas.sum(axis=1), 1.0)
        assert np.all(probas >= 0) and np.all(probas <= 1)

    def test_score(self, iris_dataset):
        """Test scoring (accuracy) functionality"""
        X, y = iris_dataset
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        clf = REPTreeClassifier(random_state=42)
        clf.fit(X_train, y_train)

        score = clf.score(X_test, y_test)

        assert 0 <= score <= 1
        assert isinstance(score, float)

    def test_get_depth(self, iris_dataset):
        """Test getting tree depth"""
        X, y = iris_dataset

        clf = REPTreeClassifier(max_depth=3, random_state=42)
        clf.fit(X, y)

        depth = clf.get_depth()
        assert depth <= 3
        assert depth >= 0

    def test_get_n_leaves(self, iris_dataset):
        """Test getting number of leaves"""
        X, y = iris_dataset

        clf = REPTreeClassifier(random_state=42)
        clf.fit(X, y)

        n_leaves = clf.get_n_leaves()
        assert n_leaves >= 1
        assert isinstance(n_leaves, int)

    def test_feature_importances(self, iris_dataset):
        """Test feature importance calculation"""
        X, y = iris_dataset

        clf = REPTreeClassifier(random_state=42)
        clf.fit(X, y)

        importances = clf.feature_importances_

        assert importances.shape == (X.shape[1],)
        assert np.all(importances >= 0)
        # Should sum to 1 or be all zeros
        assert np.isclose(importances.sum(), 1.0) or np.isclose(importances.sum(), 0.0)

    def test_max_features_sqrt(self, iris_dataset):
        """Test max_features='sqrt' parameter"""
        X, y = iris_dataset

        clf = REPTreeClassifier(max_features="sqrt", random_state=42)
        clf.fit(X, y)

        predictions = clf.predict(X)
        assert predictions.shape == y.shape

    def test_max_features_log2(self, iris_dataset):
        """Test max_features='log2' parameter"""
        X, y = iris_dataset

        clf = REPTreeClassifier(max_features="log2", random_state=42)
        clf.fit(X, y)

        predictions = clf.predict(X)
        assert predictions.shape == y.shape

    def test_max_features_int(self, iris_dataset):
        """Test max_features as integer"""
        X, y = iris_dataset

        clf = REPTreeClassifier(max_features=2, random_state=42)
        clf.fit(X, y)

        predictions = clf.predict(X)
        assert predictions.shape == y.shape

    def test_max_features_float(self, iris_dataset):
        """Test max_features as float (fraction)"""
        X, y = iris_dataset

        clf = REPTreeClassifier(max_features=0.5, random_state=42)
        clf.fit(X, y)

        predictions = clf.predict(X)
        assert predictions.shape == y.shape

    def test_entropy_criterion(self, iris_dataset):
        """Test classifier with entropy criterion"""
        X, y = iris_dataset
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        clf = REPTreeClassifier(criterion="entropy", random_state=42)
        clf.fit(X_train, y_train)

        score = clf.score(X_test, y_test)
        assert 0 <= score <= 1

    def test_get_params(self):
        """Test get_params method"""
        clf = REPTreeClassifier(max_depth=5, criterion="entropy")
        params = clf.get_params()

        assert params["max_depth"] == 5
        assert params["criterion"] == "entropy"
        assert "min_samples_split" in params
        assert "min_samples_leaf" in params

    def test_set_params(self):
        """Test set_params method"""
        clf = REPTreeClassifier()
        clf.set_params(max_depth=10, criterion="entropy")

        assert clf.max_depth == 10
        assert clf.criterion == "entropy"

    def test_set_params_invalid(self):
        """Test set_params with invalid parameter raises error"""
        clf = REPTreeClassifier()

        with pytest.raises(ValueError, match="Invalid parameter"):
            clf.set_params(invalid_param=10)

    def test_predict_unfitted(self):
        """Test that predicting with unfitted model raises error"""
        clf = REPTreeClassifier()
        X_test = np.array([[1, 2, 3, 4]])

        with pytest.raises(ValueError, match="not fitted"):
            clf.predict(X_test)

    def test_predict_wrong_n_features(self, iris_dataset):
        """Test that predicting with wrong number of features raises error"""
        X, y = iris_dataset

        clf = REPTreeClassifier(random_state=42)
        clf.fit(X, y)

        X_wrong = np.array([[1, 2]])  # Wrong number of features

        with pytest.raises(ValueError, match="features"):
            clf.predict(X_wrong)

    def test_fit_with_nan_values(self, data_with_nan):
        """Test fitting with NaN values (should handle gracefully)"""
        X, y = data_with_nan

        clf = REPTreeClassifier(random_state=42)
        clf.fit(X, y)

        assert clf.tree_ is not None
        predictions = clf.predict(X)
        assert predictions.shape == y.shape

    def test_save_load(self, iris_dataset):
        """Test model saving and loading"""
        X, y = iris_dataset
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        clf = REPTreeClassifier(random_state=42)
        clf.fit(X_train, y_train)

        # Save model
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pkl") as tmp:
            tmp_path = tmp.name

        try:
            clf.save(tmp_path)

            # Load model
            clf_loaded = REPTreeClassifier.load(tmp_path)

            # Compare predictions
            pred_original = clf.predict(X_test)
            pred_loaded = clf_loaded.predict(X_test)

            np.testing.assert_array_equal(pred_original, pred_loaded)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_single_class_data(self):
        """Test behavior with single-class data"""
        X = np.array([[1, 2], [3, 4], [5, 6]])
        y = np.array([0, 0, 0])  # All same class

        clf = REPTreeClassifier(random_state=42)
        clf.fit(X, y)

        predictions = clf.predict(X)
        assert np.all(predictions == 0)

    def test_binary_classification(self, simple_classification_data):
        """Test binary classification specifically"""
        X, y = simple_classification_data

        clf = REPTreeClassifier(random_state=42)
        clf.fit(X, y)

        assert clf.n_classes_ == 2
        predictions = clf.predict(X)
        accuracy = np.mean(predictions == y)
        assert accuracy >= 0.5  # Should do better than random


class TestREPTreeRegressor:
    """Comprehensive tests for REPTreeRegressor"""

    def test_initialization_default_params(self):
        """Test regressor initialization with default parameters"""
        reg = REPTreeRegressor()
        assert reg.criterion == "variance"
        assert reg.max_depth is None
        assert reg.min_samples_split == 2
        assert reg.min_samples_leaf == 1
        assert reg.pruning is None
        assert reg.tree_ is None

    def test_initialization_custom_params(self):
        """Test regressor initialization with custom parameters"""
        reg = REPTreeRegressor(
            criterion="mae",
            max_depth=5,
            min_samples_split=10,
            min_samples_leaf=5,
            pruning="rep",
            random_state=42,
        )
        assert reg.criterion == "mae"
        assert reg.max_depth == 5
        assert reg.min_samples_split == 10
        assert reg.min_samples_leaf == 5
        assert reg.pruning == "rep"
        assert reg.random_state == 42

    def test_invalid_criterion(self):
        """Test that invalid criterion raises ValueError"""
        with pytest.raises(ValueError, match="criterion must be"):
            REPTreeRegressor(criterion="invalid")

    def test_fit_simple_data(self, simple_regression_data):
        """Test fitting on simple regression data"""
        X, y = simple_regression_data
        reg = REPTreeRegressor(random_state=42)
        reg.fit(X, y)

        assert reg.tree_ is not None
        assert reg.n_features_ == X.shape[1]

    def test_fit_regression_dataset(self, regression_data):
        """Test fitting on generated regression dataset"""
        X, y = regression_data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        reg = REPTreeRegressor(random_state=42)
        reg.fit(X_train, y_train)

        assert reg.tree_ is not None
        assert reg.n_features_ == X_train.shape[1]
        assert reg.feature_importances_ is not None

    def test_fit_with_pruning(self, regression_data):
        """Test fitting with REP pruning"""
        X, y = regression_data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)
        X_train, X_val, y_train, y_val = train_test_split(
            X_train, y_train, test_size=0.25, random_state=42
        )

        reg = REPTreeRegressor(pruning="rep", random_state=42)
        reg.fit(X_train, y_train, X_val=X_val, y_val=y_val)

        assert reg.tree_ is not None

    def test_predict(self, regression_data):
        """Test prediction functionality"""
        X, y = regression_data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        reg = REPTreeRegressor(random_state=42)
        reg.fit(X_train, y_train)

        predictions = reg.predict(X_test)

        assert predictions.shape == y_test.shape
        assert predictions.dtype == np.float64

    def test_score(self, regression_data):
        """Test scoring (R²) functionality"""
        X, y = regression_data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        reg = REPTreeRegressor(random_state=42)
        reg.fit(X_train, y_train)

        score = reg.score(X_test, y_test)

        # R² can be negative for very bad models
        assert score <= 1.0
        assert isinstance(score, float)

    def test_mae_criterion(self, regression_data):
        """Test regressor with MAE criterion"""
        X, y = regression_data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        reg = REPTreeRegressor(criterion="mae", random_state=42)
        reg.fit(X_train, y_train)

        predictions = reg.predict(X_test)
        assert predictions.shape == y_test.shape

    def test_max_depth_constraint(self, regression_data):
        """Test that max_depth constraint is respected"""
        X, y = regression_data

        reg = REPTreeRegressor(max_depth=3, random_state=42)
        reg.fit(X, y)

        depth = reg.get_depth()
        assert depth <= 3

    def test_feature_importances(self, regression_data):
        """Test feature importance calculation"""
        X, y = regression_data

        reg = REPTreeRegressor(random_state=42)
        reg.fit(X, y)

        importances = reg.feature_importances_

        assert importances.shape == (X.shape[1],)
        assert np.all(importances >= 0)

    def test_predict_unfitted(self):
        """Test that predicting with unfitted model raises error"""
        reg = REPTreeRegressor()
        X_test = np.array([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]])

        with pytest.raises(ValueError, match="not fitted"):
            reg.predict(X_test)

    def test_save_load(self, regression_data):
        """Test model saving and loading"""
        X, y = regression_data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        reg = REPTreeRegressor(random_state=42)
        reg.fit(X_train, y_train)

        # Save model
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pkl") as tmp:
            tmp_path = tmp.name

        try:
            reg.save(tmp_path)

            # Load model
            reg_loaded = REPTreeRegressor.load(tmp_path)

            # Compare predictions
            pred_original = reg.predict(X_test)
            pred_loaded = reg_loaded.predict(X_test)

            np.testing.assert_array_almost_equal(pred_original, pred_loaded)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_constant_target(self):
        """Test behavior with constant target values"""
        X = np.array([[1], [2], [3], [4]])
        y = np.array([5.0, 5.0, 5.0, 5.0])  # All same value

        reg = REPTreeRegressor(random_state=42)
        reg.fit(X, y)

        predictions = reg.predict(X)
        assert np.allclose(predictions, 5.0)
