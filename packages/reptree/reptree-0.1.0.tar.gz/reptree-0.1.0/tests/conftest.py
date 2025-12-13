"""
Pytest configuration and shared fixtures
"""

import numpy as np
import pytest
from sklearn.datasets import load_iris, make_classification, make_regression


@pytest.fixture
def simple_classification_data():
    """Generate simple binary classification dataset"""
    np.random.seed(42)
    X = np.array([[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7]])
    y = np.array([0, 0, 0, 1, 1, 1])
    return X, y


@pytest.fixture
def simple_regression_data():
    """Generate simple regression dataset"""
    np.random.seed(42)
    X = np.array([[1], [2], [3], [4], [5], [6]])
    y = np.array([2.1, 4.0, 6.2, 7.9, 10.1, 12.0])
    return X, y


@pytest.fixture
def iris_dataset():
    """Load iris dataset"""
    iris = load_iris()
    return iris.data, iris.target


@pytest.fixture
def multiclass_data():
    """Generate multiclass classification dataset"""
    X, y = make_classification(
        n_samples=200,
        n_features=10,
        n_informative=8,
        n_redundant=2,
        n_classes=3,
        n_clusters_per_class=1,
        random_state=42,
    )
    return X, y


@pytest.fixture
def regression_data():
    """Generate regression dataset"""
    X, y = make_regression(n_samples=200, n_features=10, noise=0.1, random_state=42)
    return X, y


@pytest.fixture
def data_with_nan():
    """Generate dataset with missing values"""
    np.random.seed(42)
    X = np.array([[1.0, 2.0], [2.0, np.nan], [np.nan, 4.0], [4.0, 5.0], [5.0, 6.0]])
    y = np.array([0, 0, 1, 1, 1])
    return X, y


@pytest.fixture
def tiny_tree_data():
    """Generate minimal dataset for tree construction"""
    X = np.array([[1], [2], [3], [4]])
    y = np.array([0, 0, 1, 1])
    return X, y
