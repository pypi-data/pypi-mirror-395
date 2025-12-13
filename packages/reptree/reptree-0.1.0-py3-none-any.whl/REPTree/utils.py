"""
Validation and helper functions.
"""

from typing import Optional, Tuple
import numpy as np

from .node import TreeNode


def check_array(
    X: np.ndarray,
    ensure_2d: bool = True,
    allow_nan: bool = True,
    dtype: Optional[type] = None
) -> np.ndarray:
    """
    Validate and convert input array.
    
    Parameters
    ----------
    X : np.ndarray
        Input array to validate.
    ensure_2d : bool, default=True
        Whether to ensure array is 2D.
    allow_nan : bool, default=True
        Whether to allow NaN values.
    dtype : type, optional
        Required data type.
    
    Returns
    -------
    np.ndarray
        Validated array.
    
    Raises
    ------
    ValueError
        If array has invalid shape or contains invalid values.
    """
    if not isinstance(X, np.ndarray):
        X = np.array(X)
    
    if ensure_2d and X.ndim == 1:
        X = X.reshape(-1, 1)
    
    if ensure_2d and X.ndim != 2:
        raise ValueError(f"Expected 2D array, got shape {X.shape}")
    
    # Only check for NaN/inf if array is numeric
    if X.dtype != object:
        if not allow_nan and np.any(np.isnan(X)):
            raise ValueError("Input contains NaN values")
        
        if np.any(np.isinf(X)):
            raise ValueError("Input contains infinite values")
    
    if dtype is not None and X.dtype != dtype:
        try:
            X = X.astype(dtype)
        except (ValueError, TypeError):
            # If conversion fails, continue with original dtype
            pass
    
    return np.ascontiguousarray(X)


def check_X_y(
    X: np.ndarray,
    y: np.ndarray,
    allow_nan: bool = True
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Validate feature-target pairs.
    
    Parameters
    ----------
    X : np.ndarray
        Feature matrix.
    y : np.ndarray
        Target vector.
    allow_nan : bool, default=True
        Whether to allow NaN values in X.
    
    Returns
    -------
    X : np.ndarray
        Validated feature matrix.
    y : np.ndarray
        Validated target vector.
    
    Raises
    ------
    ValueError
        If shapes don't match or arrays contain invalid values.
    """
    X = check_array(X, ensure_2d=True, allow_nan=allow_nan)
    
    if not isinstance(y, np.ndarray):
        y = np.array(y)
    
    if y.ndim != 1:
        if y.ndim == 2 and y.shape[1] == 1:
            y = y.ravel()
        else:
            raise ValueError(f"Expected 1D target array, got shape {y.shape}")
    
    if X.shape[0] != y.shape[0]:
        raise ValueError(
            f"X and y have inconsistent numbers of samples: {X.shape[0]} != {y.shape[0]}"
        )
    
    # Only check for NaN/inf if y is numeric
    if y.dtype != object:
        if np.any(np.isnan(y)):
            raise ValueError("Target array contains NaN values")
        
        if np.any(np.isinf(y)):
            raise ValueError("Target array contains infinite values")
    
    return X, y


def check_is_fitted(estimator) -> None:
    """
    Verify that estimator is fitted.
    
    Parameters
    ----------
    estimator : object
        Estimator instance to check.
    
    Raises
    ------
    ValueError
        If estimator is not fitted.
    """
    if not hasattr(estimator, 'tree_') or estimator.tree_ is None:
        raise ValueError(
            f"This {type(estimator).__name__} instance is not fitted yet. "
            "Call 'fit' with appropriate arguments before using this estimator."
        )


def train_test_split(
    X: np.ndarray,
    y: np.ndarray,
    test_size: float = 0.3,
    random_state: Optional[int] = None
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Split arrays into random train and test subsets.
    
    Parameters
    ----------
    X : np.ndarray
        Feature matrix.
    y : np.ndarray
        Target vector.
    test_size : float, default=0.3
        Proportion of dataset to include in test split.
    random_state : int, optional
        Random seed for reproducibility.
    
    Returns
    -------
    X_train : np.ndarray
        Training features.
    X_test : np.ndarray
        Test features.
    y_train : np.ndarray
        Training targets.
    y_test : np.ndarray
        Test targets.
    
    Examples
    --------
    >>> X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
    >>> y = np.array([0, 1, 0, 1])
    >>> X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)
    """
    if not 0 < test_size < 1:
        raise ValueError(f"test_size must be between 0 and 1, got {test_size}")
    
    n_samples = X.shape[0]
    n_test = int(n_samples * test_size)
    
    rng = np.random.RandomState(random_state)
    indices = rng.permutation(n_samples)
    
    test_idx = indices[:n_test]
    train_idx = indices[n_test:]
    
    return X[train_idx], X[test_idx], y[train_idx], y[test_idx]


def get_feature_importance(tree: TreeNode, n_features: int) -> np.ndarray:
    """
    Calculate feature importance from impurity decreases.
    
    Feature importance is calculated as the total reduction in impurity
    brought by each feature across all splits.
    
    Parameters
    ----------
    tree : TreeNode
        Root node of fitted tree.
    n_features : int
        Total number of features.
    
    Returns
    -------
    np.ndarray
        Feature importances (normalized to sum to 1.0).
    
    Examples
    --------
    >>> importances = get_feature_importance(tree, n_features=4)
    >>> most_important = np.argmax(importances)
    """
    importances = np.zeros(n_features)
    
    def traverse(node: TreeNode):
        """Recursively accumulate importance."""
        if node.is_leaf():
            return
        
        # Calculate impurity decrease
        if node.left and node.right:
            n_node = node.samples
            n_left = node.left.samples
            n_right = node.right.samples
            
            impurity_decrease = (
                node.impurity -
                (n_left / n_node) * node.left.impurity -
                (n_right / n_node) * node.right.impurity
            )
            
            # Weight by number of samples
            importances[node.feature_index] += n_node * impurity_decrease
        
        # Recurse
        if node.left:
            traverse(node.left)
        if node.right:
            traverse(node.right)
    
    traverse(tree)
    
    # Normalize
    total = np.sum(importances)
    if total > 0:
        importances /= total
    
    return importances


def export_text(
    tree: TreeNode,
    feature_names: Optional[list] = None,
    max_depth: Optional[int] = None,
    decimals: int = 2
) -> str:
    """
    Generate ASCII representation of tree.
    
    Parameters
    ----------
    tree : TreeNode
        Root node of tree.
    feature_names : list, optional
        Names of features.
    max_depth : int, optional
        Maximum depth to display.
    decimals : int, default=2
        Number of decimal places for thresholds.
    
    Returns
    -------
    str
        ASCII tree representation.
    """
    lines = []
    
    def recurse(node: TreeNode, depth: int = 0, prefix: str = ""):
        """Recursively build tree string."""
        if max_depth is not None and depth > max_depth:
            lines.append(f"{prefix}...")
            return
        
        indent = "  " * depth
        
        if node.is_leaf():
            lines.append(f"{indent}{prefix}Leaf: value={node.value}, samples={node.samples}")
        else:
            feat_name = f"X[{node.feature_index}]"
            if feature_names:
                feat_name = feature_names[node.feature_index]
            
            threshold_str = f"{node.threshold:.{decimals}f}"
            lines.append(
                f"{indent}{prefix}{feat_name} <= {threshold_str} "
                f"(samples={node.samples}, impurity={node.impurity:.{decimals}f})"
            )
            
            if node.left:
                recurse(node.left, depth + 1, "├─ ")
            if node.right:
                recurse(node.right, depth + 1, "└─ ")
    
    recurse(tree)
    return "\n".join(lines)


def export_dict(tree: TreeNode) -> dict:
    """
    Convert tree to nested dictionary (JSON-serializable).
    
    Parameters
    ----------
    tree : TreeNode
        Root node of tree.
    
    Returns
    -------
    dict
        Nested dictionary representation of tree.
    """
    def recurse(node: TreeNode) -> dict:
        """Recursively convert to dict."""
        result = {
            'node_id': node.node_id,
            'samples': node.samples,
            'impurity': float(node.impurity),
        }
        
        if node.is_leaf():
            result['leaf'] = True
            result['value'] = node.value if not isinstance(node.value, dict) else dict(node.value)
        else:
            result['leaf'] = False
            result['feature_index'] = node.feature_index
            result['threshold'] = float(node.threshold)
            result['left'] = recurse(node.left) if node.left else None
            result['right'] = recurse(node.right) if node.right else None
        
        return result
    
    return recurse(tree)


def plot_tree_stats(tree: TreeNode) -> str:
    """
    Generate summary statistics for tree.
    
    Parameters
    ----------
    tree : TreeNode
        Root node of tree.
    
    Returns
    -------
    str
        Formatted statistics string.
    """
    stats = {
        'Total Nodes': tree.count_nodes(),
        'Leaf Nodes': tree.count_leaves(),
        'Internal Nodes': tree.count_nodes() - tree.count_leaves(),
        'Max Depth': tree.get_depth(),
    }
    
    lines = ["Tree Statistics:", "=" * 40]
    for key, value in stats.items():
        lines.append(f"{key:20s}: {value}")
    
    return "\n".join(lines)