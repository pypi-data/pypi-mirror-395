"""
Example 03: Pruning Demonstration

Demonstrates:
- Building a full tree
- Exporting tree structure before pruning
- Applying REP pruning
- Comparing tree structures
- Showing pruning statistics
"""
import argparse
import os
import sys
from pathlib import Path
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from sklearn.datasets import make_classification

from src.REPTree import REPTreeClassifier
from src.REPTree.pruning.rep import ReducedErrorPruner
from src.REPTree.utils import export_dict, export_text, plot_tree_stats, train_test_split


def main():
    print("=" * 70)
    print("REPTree Pruning Demonstration")
    print("=" * 70)

    # Generate synthetic classification data
    print("\n1. Generating synthetic classification data...")
    X, y = make_classification(
        n_samples=300,
        n_features=10,
        n_informative=7,
        n_redundant=2,
        n_clusters_per_class=2,
        flip_y=0.05,
        random_state=42,
    )

    print(f"   Dataset shape: {X.shape}")
    print(f"   Class distribution: {np.bincount(y)}")

    # Split data
    print("\n2. Splitting data...")
    X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=0.25, random_state=42
    )

    print(f"   Train: {X_train.shape[0]}, Validation: {X_val.shape[0]}, Test: {X_test.shape[0]}")

    # Train unpruned tree
    print("\n3. Training UNPRUNED tree (no restrictions)...")
    clf_unpruned = REPTreeClassifier(
        criterion="entropy",
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        pruning=None,
        random_state=42,
    )
    clf_unpruned.fit(X_train, y_train)

    # Get statistics before pruning
    train_acc_before = clf_unpruned.score(X_train, y_train)
    val_acc_before = clf_unpruned.score(X_val, y_val)
    test_acc_before = clf_unpruned.score(X_test, y_test)
    nodes_before = clf_unpruned.tree_.count_nodes()
    leaves_before = clf_unpruned.get_n_leaves()
    depth_before = clf_unpruned.get_depth()

    print(f"\n   Tree before pruning:")
    print(f"   - Nodes: {nodes_before}")
    print(f"   - Leaves: {leaves_before}")
    print(f"   - Depth: {depth_before}")
    print(f"   - Train accuracy: {train_acc_before:.4f}")
    print(f"   - Validation accuracy: {val_acc_before:.4f}")
    print(f"   - Test accuracy: {test_acc_before:.4f}")

    # Export tree structure before pruning
    print("\n4. Tree structure BEFORE pruning (first 4 levels):")
    print("-" * 70)
    feature_names = [f"X{i}" for i in range(X.shape[1])]
    tree_text_before = export_text(clf_unpruned.tree_, feature_names=feature_names, max_depth=4)
    print(tree_text_before)

    # Apply pruning manually
    print("\n5. Applying REP pruning...")
    pruner = ReducedErrorPruner(task_type="classification")

    # Create a copy of the tree for pruning
    clf_pruned = REPTreeClassifier(
        criterion="entropy",
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        pruning="rep",
        random_state=42,
    )
    clf_pruned.fit(X_train, y_train, X_val=X_val, y_val=y_val)

    # Get statistics after pruning
    train_acc_after = clf_pruned.score(X_train, y_train)
    val_acc_after = clf_pruned.score(X_val, y_val)
    test_acc_after = clf_pruned.score(X_test, y_test)
    nodes_after = clf_pruned.tree_.count_nodes()
    leaves_after = clf_pruned.get_n_leaves()
    depth_after = clf_pruned.get_depth()

    print(f"\n   Tree after pruning:")
    print(f"   - Nodes: {nodes_after}")
    print(f"   - Leaves: {leaves_after}")
    print(f"   - Depth: {depth_after}")
    print(f"   - Train accuracy: {train_acc_after:.4f}")
    print(f"   - Validation accuracy: {val_acc_after:.4f}")
    print(f"   - Test accuracy: {test_acc_after:.4f}")

    # Export tree structure after pruning
    print("\n6. Tree structure AFTER pruning (first 4 levels):")
    print("-" * 70)
    tree_text_after = export_text(clf_pruned.tree_, feature_names=feature_names, max_depth=4)
    print(tree_text_after)

    # Pruning statistics
    print("\n7. Pruning Statistics:")
    print("=" * 70)

    nodes_removed = nodes_before - nodes_after
    nodes_removed_pct = (nodes_removed / nodes_before) * 100
    leaves_removed = leaves_before - leaves_after
    depth_reduction = depth_before - depth_after

    print(f"   {'Metric':<30} {'Before':<15} {'After':<15} {'Change':<15}")
    print("   " + "-" * 70)
    print(
        f"   {'Nodes':<30} {nodes_before:<15} {nodes_after:<15} {-nodes_removed} ({-nodes_removed_pct:.1f}%)"
    )
    print(f"   {'Leaves':<30} {leaves_before:<15} {leaves_after:<15} {-leaves_removed}")
    print(f"   {'Depth':<30} {depth_before:<15} {depth_after:<15} {-depth_reduction}")
    print(
        f"   {'Train Accuracy':<30} {train_acc_before:<15.4f} {train_acc_after:<15.4f} {train_acc_after - train_acc_before:+.4f}"
    )
    print(
        f"   {'Validation Accuracy':<30} {val_acc_before:<15.4f} {val_acc_after:<15.4f} {val_acc_after - val_acc_before:+.4f}"
    )
    print(
        f"   {'Test Accuracy':<30} {test_acc_before:<15.4f} {test_acc_after:<15.4f} {test_acc_after - test_acc_before:+.4f}"
    )

    # Complexity vs Performance trade-off
    print("\n8. Complexity vs Performance Trade-off:")
    print("-" * 70)
    complexity_reduction = nodes_removed_pct
    accuracy_change = (test_acc_after - test_acc_before) * 100

    print(f"   Complexity reduction: {complexity_reduction:.1f}%")
    print(f"   Test accuracy change: {accuracy_change:+.2f}%")

    if accuracy_change >= 0:
        print(f"   ✓ Pruning IMPROVED generalization while reducing complexity!")
    elif abs(accuracy_change) < 1:
        print(f"   ✓ Pruning maintained accuracy while significantly reducing complexity!")
    else:
        print(f"   ✗ Pruning reduced accuracy (possible underfitting)")

    # Export as dictionary
    print("\n9. Exporting tree as dictionary (pruned tree)...")
    tree_dict = export_dict(clf_pruned.tree_)
    print(f"   Root node: {tree_dict}")
    print(f"   (Full dictionary structure available for JSON serialization)")

    # Tree statistics summary
    print("\n10. Detailed Statistics:")
    print(plot_tree_stats(clf_unpruned.tree_))
    print("\n   After Pruning:")
    print(plot_tree_stats(clf_pruned.tree_))

    # Effect on different complexity levels
    print("\n11. Testing different min_samples_split values:")
    print("-" * 70)
    min_samples_values = [2, 5, 10, 20]

    for min_samples in min_samples_values:
        clf_test = REPTreeClassifier(
            criterion="entropy", min_samples_split=min_samples, pruning="rep", random_state=42
        )
        clf_test.fit(X_train, y_train, X_val=X_val, y_val=y_val)

        test_acc = clf_test.score(X_test, y_test)
        n_nodes = clf_test.tree_.count_nodes()

        print(
            f"   min_samples_split={min_samples:2d}: "
            f"Nodes={n_nodes:3d}, Test Acc={test_acc:.4f}"
        )

    print("\n" + "=" * 70)
    print("Pruning demonstration complete!")
    print("=" * 70)

    # Key takeaways
    print("\n📊 Key Takeaways:")
    print(f"   1. Pruning reduced tree size by {nodes_removed_pct:.1f}%")
    print(f"   2. Test accuracy changed by {accuracy_change:+.2f}%")
    print(f"   3. Simpler trees are easier to interpret and less prone to overfitting")
    print(f"   4. REP pruning uses validation data to make informed pruning decisions")


if __name__ == "__main__":
    main()
