"""
Impurity and evaluation metrics for decision trees.
"""

from typing import Literal

import numpy as np


def gini_impurity(y: np.ndarray) -> float:
    """
    Calculate Gini impurity for classification.

    Gini impurity = 1 - sum(p_i^2) where p_i is the proportion of class i.

    Parameters
    ----------
    y : np.ndarray
        Class labels.

    Returns
    -------
    float
        Gini impurity in [0, 1-1/n_classes].

    Examples
    --------
    >>> y = np.array([0, 0, 1, 1])
    >>> gini_impurity(y)
    0.5
    """
    if len(y) == 0:
        return 0.0

    _, counts = np.unique(y, return_counts=True)
    proportions = counts / len(y)
    return 1.0 - np.sum(proportions**2)


def entropy(y: np.ndarray) -> float:
    """
    Calculate entropy for classification.

    Entropy = -sum(p_i * log2(p_i)) where p_i is the proportion of class i.

    Parameters
    ----------
    y : np.ndarray
        Class labels.

    Returns
    -------
    float
        Entropy value >= 0.

    Examples
    --------
    >>> y = np.array([0, 0, 1, 1])
    >>> entropy(y)
    1.0
    """
    if len(y) == 0:
        return 0.0

    _, counts = np.unique(y, return_counts=True)
    proportions = counts / len(y)

    # Avoid log(0)
    proportions = proportions[proportions > 0]
    return -np.sum(proportions * np.log2(proportions))


def variance(y: np.ndarray) -> float:
    """
    Calculate variance for regression.

    Parameters
    ----------
    y : np.ndarray
        Target values.

    Returns
    -------
    float
        Variance of y.

    Examples
    --------
    >>> y = np.array([1.0, 2.0, 3.0, 4.0])
    >>> variance(y)
    1.25
    """
    if len(y) == 0:
        return 0.0
    return np.var(y)


def mae_impurity(y: np.ndarray) -> float:
    """
    Calculate Mean Absolute Error from median for regression.

    MAE impurity = mean(|y_i - median(y)|)

    Parameters
    ----------
    y : np.ndarray
        Target values.

    Returns
    -------
    float
        Mean absolute error from median.

    Examples
    --------
    >>> y = np.array([1.0, 2.0, 3.0, 4.0])
    >>> mae_impurity(y)
    1.0
    """
    if len(y) == 0:
        return 0.0
    median = np.median(y)
    return np.mean(np.abs(y - median))


def information_gain(
    y_parent: np.ndarray,
    y_left: np.ndarray,
    y_right: np.ndarray,
    criterion: Literal["gini", "entropy", "variance", "mae"] = "gini",
) -> float:
    """
    Calculate information gain from a split.

    Gain = impurity(parent) - (n_left/n * impurity(left) + n_right/n * impurity(right))

    Parameters
    ----------
    y_parent : np.ndarray
        Parent node labels/values.
    y_left : np.ndarray
        Left child labels/values.
    y_right : np.ndarray
        Right child labels/values.
    criterion : {'gini', 'entropy', 'variance', 'mae'}
        Impurity measure to use.

    Returns
    -------
    float
        Information gain from the split.

    Examples
    --------
    >>> y_parent = np.array([0, 0, 1, 1])
    >>> y_left = np.array([0, 0])
    >>> y_right = np.array([1, 1])
    >>> information_gain(y_parent, y_left, y_right, 'gini')
    0.5
    """
    if len(y_parent) == 0:
        return 0.0

    if len(y_left) == 0 or len(y_right) == 0:
        return 0.0

    # Select impurity function
    if criterion == "gini":
        impurity_fn = gini_impurity
    elif criterion == "entropy":
        impurity_fn = entropy
    elif criterion == "variance":
        impurity_fn = variance
    elif criterion == "mae":
        impurity_fn = mae_impurity
    else:
        raise ValueError(f"Unknown criterion: {criterion}")

    # Calculate weighted impurity
    n_parent = len(y_parent)
    n_left = len(y_left)
    n_right = len(y_right)

    parent_impurity = impurity_fn(y_parent)
    weighted_child_impurity = (n_left / n_parent) * impurity_fn(y_left) + (
        n_right / n_parent
    ) * impurity_fn(y_right)

    return parent_impurity - weighted_child_impurity


def accuracy_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Calculate classification accuracy.

    Parameters
    ----------
    y_true : np.ndarray
        True labels.
    y_pred : np.ndarray
        Predicted labels.

    Returns
    -------
    float
        Accuracy in [0, 1].
    """
    if len(y_true) == 0:
        return 0.0
    return np.mean(y_true == y_pred)


def mean_squared_error(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Calculate mean squared error.

    Parameters
    ----------
    y_true : np.ndarray
        True values.
    y_pred : np.ndarray
        Predicted values.

    Returns
    -------
    float
        Mean squared error.
    """
    if len(y_true) == 0:
        return 0.0
    return np.mean((y_true - y_pred) ** 2)


def mean_absolute_error(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Calculate mean absolute error.

    Parameters
    ----------
    y_true : np.ndarray
        True values.
    y_pred : np.ndarray
        Predicted values.

    Returns
    -------
    float
        Mean absolute error.
    """
    if len(y_true) == 0:
        return 0.0
    return np.mean(np.abs(y_true - y_pred))


def r2_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Calculate R² (coefficient of determination).

    R² = 1 - (SS_res / SS_tot)

    Parameters
    ----------
    y_true : np.ndarray
        True values.
    y_pred : np.ndarray
        Predicted values.

    Returns
    -------
    float
        R² score. Best value is 1.0, can be negative.
    """
    if len(y_true) == 0:
        return 0.0

    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)

    if ss_tot == 0:
        return 0.0 if ss_res == 0 else -np.inf

    return 1.0 - (ss_res / ss_tot)


def confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray, n_classes: int) -> np.ndarray:
    """
    Compute confusion matrix.

    Parameters
    ----------
    y_true : np.ndarray
        True labels (must be in range [0, n_classes)).
    y_pred : np.ndarray
        Predicted labels (must be in range [0, n_classes)).
    n_classes : int
        Number of classes.

    Returns
    -------
    np.ndarray
        Confusion matrix of shape (n_classes, n_classes).
        Element [i, j] is count of samples with true label i and predicted label j.
    """
    cm = np.zeros((n_classes, n_classes), dtype=np.int64)

    for true_label, pred_label in zip(y_true, y_pred):
        if 0 <= true_label < n_classes and 0 <= pred_label < n_classes:
            cm[int(true_label), int(pred_label)] += 1

    return cm
