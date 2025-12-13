"""
Example 01: Basic Classification with REPTree

Demonstrates:
- Loading and preparing iris dataset
- Training classifier without pruning
- Training with REP pruning
- Comparing accuracy and tree size
"""
import argparse
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
    
import numpy as np
from sklearn.datasets import load_iris

from src.REPTree import REPTreeClassifier
from src.REPTree.utils import export_text, plot_tree_stats, train_test_split


def main():
    print("=" * 70)
    print("REPTree Classification Example - Iris Dataset")
    print("=" * 70)

    # Load iris dataset
    print("\n1. Loading iris dataset...")
    iris = load_iris()
    X, y = iris.data, iris.target
    feature_names = iris.feature_names
    print(f"   Dataset shape: {X.shape}")
    print(f"   Classes: {iris.target_names}")

    # Split into train, validation, and test sets
    print("\n2. Splitting data (60% train, 20% validation, 20% test)...")
    X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=0.25, random_state=42  # 0.25 of 80% = 20%
    )

    print(f"   Train samples: {X_train.shape[0]}")
    print(f"   Validation samples: {X_val.shape[0]}")
    print(f"   Test samples: {X_test.shape[0]}")

    # Train classifier without pruning
    print("\n3. Training REPTreeClassifier WITHOUT pruning...")
    clf_no_prune = REPTreeClassifier(
        criterion="gini", max_depth=None, min_samples_split=2, min_samples_leaf=1, random_state=42
    )
    clf_no_prune.fit(X_train, y_train)

    # Evaluate
    train_acc_no_prune = clf_no_prune.score(X_train, y_train)
    val_acc_no_prune = clf_no_prune.score(X_val, y_val)
    test_acc_no_prune = clf_no_prune.score(X_test, y_test)

    print("\n   Without Pruning Results:")
    print(f"   Train accuracy: {train_acc_no_prune:.4f}")
    print(f"   Validation accuracy: {val_acc_no_prune:.4f}")
    print(f"   Test accuracy: {test_acc_no_prune:.4f}")
    print(f"   Tree depth: {clf_no_prune.get_depth()}")
    print(f"   Number of nodes: {clf_no_prune.tree_.count_nodes()}")
    print(f"   Number of leaves: {clf_no_prune.get_n_leaves()}")

    # Train classifier with REP pruning
    print("\n4. Training REPTreeClassifier WITH REP pruning...")
    clf_with_prune = REPTreeClassifier(
        criterion="gini",
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        pruning="rep",
        random_state=42,
    )
    clf_with_prune.fit(X_train, y_train, X_val=X_val, y_val=y_val)

    # Evaluate
    train_acc_prune = clf_with_prune.score(X_train, y_train)
    val_acc_prune = clf_with_prune.score(X_val, y_val)
    test_acc_prune = clf_with_prune.score(X_test, y_test)

    print("\n   With REP Pruning Results:")
    print(f"   Train accuracy: {train_acc_prune:.4f}")
    print(f"   Validation accuracy: {val_acc_prune:.4f}")
    print(f"   Test accuracy: {test_acc_prune:.4f}")
    print(f"   Tree depth: {clf_with_prune.get_depth()}")
    print(f"   Number of nodes: {clf_with_prune.tree_.count_nodes()}")
    print(f"   Number of leaves: {clf_with_prune.get_n_leaves()}")

    # Comparison
    print("\n5. Comparison:")
    print(f"   {'Metric':<25} {'No Pruning':<15} {'With Pruning':<15} {'Change':<15}")
    print("   " + "-" * 70)

    node_reduction = clf_no_prune.tree_.count_nodes() - clf_with_prune.tree_.count_nodes()
    node_reduction_pct = (node_reduction / clf_no_prune.tree_.count_nodes()) * 100

    test_acc_change = test_acc_prune - test_acc_no_prune

    print(
        f"   {'Test Accuracy':<25} {test_acc_no_prune:<15.4f} {test_acc_prune:<15.4f} {test_acc_change:+.4f}"
    )
    print(
        f"   {'Tree Depth':<25} {clf_no_prune.get_depth():<15} {clf_with_prune.get_depth():<15} {clf_with_prune.get_depth() - clf_no_prune.get_depth():+}"
    )
    print(
        f"   {'Number of Nodes':<25} {clf_no_prune.tree_.count_nodes():<15} {clf_with_prune.tree_.count_nodes():<15} {-node_reduction:+}"
    )
    print(f"   {'Node Reduction %':<25} {'':<15} {'':<15} {node_reduction_pct:.1f}%")

    # Feature importance
    print("\n6. Feature Importances (with pruning):")
    importances = clf_with_prune.feature_importances_
    for i, (name, imp) in enumerate(zip(feature_names, importances)):
        print(f"   {name:<30}: {imp:.4f}")

    # Make predictions
    print("\n7. Sample Predictions:")

    sample_indices = np.random.choice(len(X_test), size=3, replace=False)

    for idx in sample_indices:
        sample = X_test[idx : idx + 1]
        true_label = iris.target_names[y_test[idx]]
        pred_label = iris.target_names[clf_with_prune.predict(sample)[0]]
        proba = clf_with_prune.predict_proba(sample)[0]

    print(f"   Sample {idx}:")
    print(f"      True: {true_label}, Predicted: {pred_label}")
    print(f"      Probabilities: {dict(zip(iris.target_names, proba))}")

    # Display tree structure (first few levels)
    print("\n8. Tree Structure (with pruning, max depth=3):")
    tree_text = export_text(clf_with_prune.tree_, feature_names=list(feature_names), max_depth=3)
    print(tree_text)

    print("\n" + "=" * 70)
    print("Example complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
