"""
Example 02: Regression with REPTree

Demonstrates:
- Generating synthetic regression data
- Training regressor with and without pruning
- Evaluating MSE and R² scores
- Visualizing tree structure
"""
import argparse
import os
import sys
from pathlib import Path
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from src.REPTree import REPTreeRegressor
from src.REPTree.metrics import mean_absolute_error, mean_squared_error, r2_score
from src.REPTree.utils import export_text, plot_tree_stats, train_test_split



def generate_synthetic_data(n_samples=500, n_features=5, noise=0.1, random_state=42):
    """Generate synthetic regression data with non-linear relationships."""
    np.random.seed(random_state)

    X = np.random.randn(n_samples, n_features)

    # Create target with non-linear relationships
    y = (
        2 * X[:, 0] ** 2
        + np.sin(3 * X[:, 1])
        + 0.5 * X[:, 2] * X[:, 3]
        + X[:, 4]
        + noise * np.random.randn(n_samples)
    )

    return X, y


def main():
    print("=" * 70)
    print("REPTree Regression Example - Synthetic Data")
    print("=" * 70)

    # Generate synthetic data
    print("\n1. Generating synthetic regression data...")
    X, y = generate_synthetic_data(n_samples=500, n_features=5, noise=0.5, random_state=42)
    print(f"   Dataset shape: {X.shape}")
    print(f"   Target range: [{y.min():.2f}, {y.max():.2f}]")
    print(f"   Target mean: {y.mean():.2f}, std: {y.std():.2f}")

    # Split data
    print("\n2. Splitting data (60% train, 20% validation, 20% test)...")
    X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=0.25, random_state=42
    )

    print(f"   Train samples: {X_train.shape[0]}")
    print(f"   Validation samples: {X_val.shape[0]}")
    print(f"   Test samples: {X_test.shape[0]}")

    # Train regressor without pruning
    print("\n3. Training REPTreeRegressor WITHOUT pruning...")
    reg_no_prune = REPTreeRegressor(
        criterion="variance",
        max_depth=None,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
    )
    reg_no_prune.fit(X_train, y_train)

    # Evaluate
    y_train_pred_no_prune = reg_no_prune.predict(X_train)
    y_val_pred_no_prune = reg_no_prune.predict(X_val)
    y_test_pred_no_prune = reg_no_prune.predict(X_test)

    train_mse_no_prune = mean_squared_error(y_train, y_train_pred_no_prune)
    val_mse_no_prune = mean_squared_error(y_val, y_val_pred_no_prune)
    test_mse_no_prune = mean_squared_error(y_test, y_test_pred_no_prune)

    train_r2_no_prune = r2_score(y_train, y_train_pred_no_prune)
    val_r2_no_prune = r2_score(y_val, y_val_pred_no_prune)
    test_r2_no_prune = r2_score(y_test, y_test_pred_no_prune)

    print("\n   Without Pruning Results:")
    print(f"   Train MSE: {train_mse_no_prune:.4f}, R²: {train_r2_no_prune:.4f}")
    print(f"   Validation MSE: {val_mse_no_prune:.4f}, R²: {val_r2_no_prune:.4f}")
    print(f"   Test MSE: {test_mse_no_prune:.4f}, R²: {test_r2_no_prune:.4f}")
    print(f"   Tree depth: {reg_no_prune.get_depth()}")
    print(f"   Number of nodes: {reg_no_prune.tree_.count_nodes()}")
    print(f"   Number of leaves: {reg_no_prune.get_n_leaves()}")

    # Train regressor with REP pruning
    print("\n4. Training REPTreeRegressor WITH REP pruning...")
    reg_with_prune = REPTreeRegressor(
        criterion="variance",
        max_depth=None,
        min_samples_split=5,
        min_samples_leaf=2,
        pruning="rep",
        random_state=42,
    )
    reg_with_prune.fit(X_train, y_train, X_val=X_val, y_val=y_val)

    # Evaluate
    y_train_pred_prune = reg_with_prune.predict(X_train)
    y_val_pred_prune = reg_with_prune.predict(X_val)
    y_test_pred_prune = reg_with_prune.predict(X_test)

    train_mse_prune = mean_squared_error(y_train, y_train_pred_prune)
    val_mse_prune = mean_squared_error(y_val, y_val_pred_prune)
    test_mse_prune = mean_squared_error(y_test, y_test_pred_prune)

    train_r2_prune = r2_score(y_train, y_train_pred_prune)
    val_r2_prune = r2_score(y_val, y_val_pred_prune)
    test_r2_prune = r2_score(y_test, y_test_pred_prune)

    print("\n   With REP Pruning Results:")
    print(f"   Train MSE: {train_mse_prune:.4f}, R²: {train_r2_prune:.4f}")
    print(f"   Validation MSE: {val_mse_prune:.4f}, R²: {val_r2_prune:.4f}")
    print(f"   Test MSE: {test_mse_prune:.4f}, R²: {test_r2_prune:.4f}")
    print(f"   Tree depth: {reg_with_prune.get_depth()}")
    print(f"   Number of nodes: {reg_with_prune.tree_.count_nodes()}")
    print(f"   Number of leaves: {reg_with_prune.get_n_leaves()}")

    # Comparison
    print("\n5. Comparison:")
    print(f"   {'Metric':<25} {'No Pruning':<15} {'With Pruning':<15} {'Change':<15}")
    print("   " + "-" * 70)

    node_reduction = reg_no_prune.tree_.count_nodes() - reg_with_prune.tree_.count_nodes()
    node_reduction_pct = (node_reduction / reg_no_prune.tree_.count_nodes()) * 100

    mse_change = test_mse_prune - test_mse_no_prune
    r2_change = test_r2_prune - test_r2_no_prune

    print(
        f"   {'Test MSE':<25} {test_mse_no_prune:<15.4f} {test_mse_prune:<15.4f} {mse_change:+.4f}"
    )
    print(f"   {'Test R²':<25} {test_r2_no_prune:<15.4f} {test_r2_prune:<15.4f} {r2_change:+.4f}")
    print(
        f"   {'Tree Depth':<25} {reg_no_prune.get_depth():<15} {reg_with_prune.get_depth():<15} {reg_with_prune.get_depth() - reg_no_prune.get_depth():+}"
    )
    print(
        f"   {'Number of Nodes':<25} {reg_no_prune.tree_.count_nodes():<15} {reg_with_prune.tree_.count_nodes():<15} {-node_reduction:+}"
    )
    print(f"   {'Node Reduction %':<25} {'':<15} {'':<15} {node_reduction_pct:.1f}%")

    # Feature importance
    print("\n6. Feature Importances (with pruning):")
    importances = reg_with_prune.feature_importances_
    feature_names = [f"Feature_{i}" for i in range(X.shape[1])]
    for name, imp in zip(feature_names, importances):
        print(f"   {name:<30}: {imp:.4f}")

    # Prediction examples
    print("\n7. Sample Predictions (with pruning):")
    sample_indices = [0, 25, 50]
    for idx in sample_indices:
        sample = X_test[idx : idx + 1]
        true_val = y_test[idx]
        pred_val = reg_with_prune.predict(sample)[0]
        error = abs(true_val - pred_val)

        print(f"   Sample {idx}: True={true_val:.3f}, Predicted={pred_val:.3f}, Error={error:.3f}")

    # Display tree structure
    print("\n8. Tree Structure (with pruning, max depth=3):")
    tree_text = export_text(
        reg_with_prune.tree_, feature_names=feature_names, max_depth=3, decimals=3
    )
    print(tree_text)

    # MAE criterion comparison
    print("\n9. Testing MAE criterion...")
    reg_mae = REPTreeRegressor(
        criterion="mae",
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        pruning="rep",
        random_state=42,
    )
    reg_mae.fit(X_train, y_train, X_val=X_val, y_val=y_val)

    y_test_pred_mae = reg_mae.predict(X_test)
    test_mse_mae = mean_squared_error(y_test, y_test_pred_mae)
    test_mae_score = mean_absolute_error(y_test, y_test_pred_mae)
    test_r2_mae = r2_score(y_test, y_test_pred_mae)

    print(f"   MAE Criterion Results:")
    print(f"   Test MSE: {test_mse_mae:.4f}")
    print(f"   Test MAE: {test_mae_score:.4f}")
    print(f"   Test R²: {test_r2_mae:.4f}")
    print(f"   Number of nodes: {reg_mae.tree_.count_nodes()}")

    print("\n" + "=" * 70)
    print("Example complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
