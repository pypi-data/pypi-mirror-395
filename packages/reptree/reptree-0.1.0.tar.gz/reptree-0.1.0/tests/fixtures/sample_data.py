"""
Sample data generators for testing

Provides functions to generate various types of test datasets.
"""

import numpy as np
from sklearn.datasets import make_classification, make_regression


def generate_simple_binary_data(n_samples=100, n_features=2, random_state=42):
    """
    Generate simple linearly separable binary classification data.

    Parameters
    ----------
    n_samples : int
        Number of samples
    n_features : int
        Number of features
    random_state : int
        Random seed

    Returns
    -------
    X : np.ndarray
        Feature matrix
    y : np.ndarray
        Binary labels
    """
    np.random.seed(random_state)
    X, y = make_classification(
        n_samples=n_samples,
        n_features=n_features,
        n_redundant=0,
        n_informative=n_features,
        n_clusters_per_class=1,
        random_state=random_state,
    )
    return X, y


def generate_multiclass_data(n_samples=200, n_features=10, n_classes=3, random_state=42):
    """
    Generate multiclass classification data.

    Parameters
    ----------
    n_samples : int
        Number of samples
    n_features : int
        Number of features
    n_classes : int
        Number of classes
    random_state : int
        Random seed

    Returns
    -------
    X : np.ndarray
        Feature matrix
    y : np.ndarray
        Class labels
    """
    X, y = make_classification(
        n_samples=n_samples,
        n_features=n_features,
        n_informative=max(2, n_features // 2),
        n_redundant=min(2, n_features // 4),
        n_classes=n_classes,
        n_clusters_per_class=1,
        random_state=random_state,
    )
    return X, y


def generate_regression_data(n_samples=200, n_features=10, noise=0.1, random_state=42):
    """
    Generate regression data.

    Parameters
    ----------
    n_samples : int
        Number of samples
    n_features : int
        Number of features
    noise : float
        Standard deviation of Gaussian noise
    random_state : int
        Random seed

    Returns
    -------
    X : np.ndarray
        Feature matrix
    y : np.ndarray
        Continuous target values
    """
    X, y = make_regression(
        n_samples=n_samples, n_features=n_features, noise=noise, random_state=random_state
    )
    return X, y


def generate_data_with_missing(n_samples=100, n_features=5, missing_rate=0.1, random_state=42):
    """
    Generate data with missing values (NaN).

    Parameters
    ----------
    n_samples : int
        Number of samples
    n_features : int
        Number of features
    missing_rate : float
        Proportion of values to set as missing
    random_state : int
        Random seed

    Returns
    -------
    X : np.ndarray
        Feature matrix with NaN values
    y : np.ndarray
        Binary labels
    """
    np.random.seed(random_state)
    X, y = generate_simple_binary_data(n_samples, n_features, random_state)

    # Randomly set some values to NaN
    n_missing = int(n_samples * n_features * missing_rate)
    missing_indices = np.random.choice(n_samples * n_features, n_missing, replace=False)

    X_flat = X.flatten()
    X_flat[missing_indices] = np.nan
    X = X_flat.reshape(n_samples, n_features)

    return X, y


def generate_imbalanced_data(n_samples=200, imbalance_ratio=0.9, n_features=5, random_state=42):
    """
    Generate imbalanced binary classification data.

    Parameters
    ----------
    n_samples : int
        Number of samples
    imbalance_ratio : float
        Proportion of majority class
    n_features : int
        Number of features
    random_state : int
        Random seed

    Returns
    -------
    X : np.ndarray
        Feature matrix
    y : np.ndarray
        Imbalanced binary labels
    """
    X, y = make_classification(
        n_samples=n_samples,
        n_features=n_features,
        n_informative=n_features,
        n_redundant=0,
        n_clusters_per_class=1,
        weights=[imbalance_ratio, 1 - imbalance_ratio],
        random_state=random_state,
    )
    return X, y


def generate_noisy_data(n_samples=200, n_features=10, label_noise=0.1, random_state=42):
    """
    Generate classification data with label noise.

    Parameters
    ----------
    n_samples : int
        Number of samples
    n_features : int
        Number of features
    label_noise : float
        Proportion of labels to flip randomly
    random_state : int
        Random seed

    Returns
    -------
    X : np.ndarray
        Feature matrix
    y : np.ndarray
        Noisy binary labels
    """
    np.random.seed(random_state)
    X, y = generate_simple_binary_data(n_samples, n_features, random_state)

    # Flip some labels
    n_noisy = int(n_samples * label_noise)
    noisy_indices = np.random.choice(n_samples, n_noisy, replace=False)
    y[noisy_indices] = 1 - y[noisy_indices]

    return X, y


def save_sample_csv(filename="test_data.csv", n_samples=100):
    """
    Generate and save sample data as CSV for testing.

    Parameters
    ----------
    filename : str
        Output filename
    n_samples : int
        Number of samples to generate
    """
    import pandas as pd

    X, y = generate_simple_binary_data(n_samples=n_samples)

    df = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(X.shape[1])])
    df["target"] = y

    df.to_csv(filename, index=False)
    print(f"Sample data saved to {filename}")


if __name__ == "__main__":
    # Generate and display sample datasets
    print("Generating sample datasets...\n")

    print("1. Binary Classification Data:")
    X, y = generate_simple_binary_data(n_samples=10)
    print(f"   Shape: X={X.shape}, y={y.shape}")
    print(f"   Classes: {np.unique(y)}\n")

    print("2. Multiclass Classification Data:")
    X, y = generate_multiclass_data(n_samples=10, n_classes=3)
    print(f"   Shape: X={X.shape}, y={y.shape}")
    print(f"   Classes: {np.unique(y)}\n")

    print("3. Regression Data:")
    X, y = generate_regression_data(n_samples=10)
    print(f"   Shape: X={X.shape}, y={y.shape}")
    print(f"   Target range: [{y.min():.2f}, {y.max():.2f}]\n")

    print("4. Data with Missing Values:")
    X, y = generate_data_with_missing(n_samples=10, missing_rate=0.2)
    print(f"   Shape: X={X.shape}, y={y.shape}")
    print(f"   Missing values: {np.isnan(X).sum()}\n")

    print("5. Imbalanced Data:")
    X, y = generate_imbalanced_data(n_samples=100, imbalance_ratio=0.9)
    print(f"   Shape: X={X.shape}, y={y.shape}")
    print(f"   Class distribution: {np.bincount(y)}\n")
