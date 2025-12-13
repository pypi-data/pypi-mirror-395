import argparse
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler

# Ensure project root is on sys.path when running this script
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.REPTree.tree import REPTreeClassifier, REPTreeRegressor
from src.REPTree.utils import train_test_split

OUTPUT_DIR = Path(__file__).resolve().parent / ".." / "outputs"
DATA_DIR = Path(__file__).resolve().parent / ".." / "data"

sns.set(style="whitegrid")
plt.rcParams.update({"figure.figsize": (8, 5), "axes.titlesize": 12, "axes.labelsize": 11})


def ensure_output_dir() -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUTPUT_DIR


#  Dataset Visualizations  #


def plot_distributions(df: pd.DataFrame, target: str, title: str, fname: str) -> None:
    out = ensure_output_dir() / fname
    num_cols = [c for c in df.columns if c != target]
    n = len(num_cols)
    cols = 3
    rows = int(np.ceil(n / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 4, rows * 3))
    axes = axes.flatten()
    for i, col in enumerate(num_cols):
        sns.histplot(df[col], kde=True, ax=axes[i], color="#4C78A8")
        axes[i].set_title(f"Distribution: {col}")
    for j in range(i + 1, len(axes)):
        axes[j].axis("off")
    fig.suptitle(title)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    fig.savefig(out, dpi=150)
    plt.close(fig)


def plot_pairplot(df: pd.DataFrame, target: str, fname: str) -> None:
    out = ensure_output_dir() / fname
    g = sns.pairplot(df, hue=target, corner=True, diag_kind="hist")
    g.savefig(out, dpi=150)
    plt.close()


def plot_correlations(df: pd.DataFrame, target: Optional[str], title: str, fname: str) -> None:
    out = ensure_output_dir() / fname
    corr = df.drop(columns=[target]) if target and target in df.columns else df
    corr = corr.corr(numeric_only=True)
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.heatmap(corr, annot=False, cmap="coolwarm", center=0, ax=ax)
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)


#  Tree Visualizations  #


def _layout_tree_positions(root, x=0.0, y=0.0, x_gap=1.6, y_gap=1.5, pos=None):
    if pos is None:
        pos = {}
    pos[root.node_id] = (x, y)
    if root.left:
        pos = _layout_tree_positions(root.left, x - x_gap, y - y_gap, x_gap * 0.75, y_gap, pos)
    if root.right:
        pos = _layout_tree_positions(root.right, x + x_gap, y - y_gap, x_gap * 0.75, y_gap, pos)
    return pos


def plot_tree_structure(
    model: REPTreeClassifier, feature_names: Optional[list], fname: str
) -> None:
    out = ensure_output_dir() / fname
    tree = model.tree_
    if tree is None:
        return
    pos = _layout_tree_positions(tree)
    fig, ax = plt.subplots(figsize=(10, 6))

    # Draw edges
    def draw_edges(node):
        if node.left:
            x0, y0 = pos[node.node_id]
            x1, y1 = pos[node.left.node_id]
            ax.plot([x0, x1], [y0, y1], color="#999", lw=1)
            draw_edges(node.left)
        if node.right:
            x0, y0 = pos[node.node_id]
            x1, y1 = pos[node.right.node_id]
            ax.plot([x0, x1], [y0, y1], color="#999", lw=1)
            draw_edges(node.right)

    draw_edges(tree)

    # Draw nodes
    def draw_nodes(node):
        x, y = pos[node.node_id]
        is_leaf = node.is_leaf()
        color = "#59A14F" if is_leaf else "#4C78A8"
        ax.scatter([x], [y], s=300, color=color, zorder=3)
        label = []
        if not is_leaf:
            fname = (
                feature_names[node.feature_index]
                if feature_names and node.feature_index is not None
                else f"f{node.feature_index}"
            )
            label.append(f"{fname} <= {node.threshold:.3f}")
        if isinstance(node.value, dict):
            # classification prob summary
            top = sorted(node.value.items(), key=lambda kv: kv[1], reverse=True)[:2]
            prob_str = ", ".join([f"{int(k)}:{v:.2f}" for k, v in top])
            label.append(f"p: {prob_str}")
        else:
            label.append(f"val: {node.value}")
        label.append(f"n={node.samples}, imp={node.impurity:.3f}")
        ax.text(x, y, "\n".join(label), ha="center", va="center", color="white", fontsize=8)
        if node.left:
            draw_nodes(node.left)
        if node.right:
            draw_nodes(node.right)

    draw_nodes(tree)
    ax.axis("off")
    ax.set_title("REPTree Structure")
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)


def plot_feature_importance(
    model: REPTreeClassifier, feature_names: Optional[list], fname: str
) -> None:
    out = ensure_output_dir() / fname
    fi = model.feature_importances_
    if fi is None:
        return
    order = np.argsort(fi)[::-1]
    names = [feature_names[i] if feature_names else f"f{i}" for i in order]
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=fi[order], y=names, ax=ax, color="#4C78A8")
    ax.set_title("Feature Importances")
    ax.set_xlabel("Importance")
    ax.set_ylabel("Feature")
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)


#  Decision Boundary (2D via PCA)  #


def plot_decision_boundary_2d(
    model: REPTreeClassifier, X: np.ndarray, y: np.ndarray, fname: str
) -> None:
    out = ensure_output_dir() / fname
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)
    pca = PCA(n_components=2, random_state=model.random_state)
    X2 = pca.fit_transform(Xs)
    # Grid
    x_min, x_max = X2[:, 0].min() - 0.5, X2[:, 0].max() + 0.5
    y_min, y_max = X2[:, 1].min() - 0.5, X2[:, 1].max() + 0.5
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 200), np.linspace(y_min, y_max, 200))
    grid_2d = np.c_[xx.ravel(), yy.ravel()]
    # Inverse project grid back to original feature space
    grid_orig = scaler.inverse_transform(pca.inverse_transform(grid_2d))
    Z = model.predict(grid_orig)
    Z = Z.reshape(xx.shape)
    fig, ax = plt.subplots(figsize=(8, 6))
    cmap = sns.color_palette("pastel")
    ax.contourf(xx, yy, Z, alpha=0.3, levels=np.unique(Z), colors=cmap)
    sns.scatterplot(x=X2[:, 0], y=X2[:, 1], hue=y, ax=ax, palette="dark")
    ax.set_title("Decision Boundary (PCA 2D)")
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)


#  Training Curves  #


def plot_depth_vs_accuracy(X: np.ndarray, y: np.ndarray, fname: str) -> None:
    out = ensure_output_dir() / fname
    depths = list(range(1, 11))
    scores = []
    for d in depths:
        Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=42)
        clf = REPTreeClassifier(max_depth=d, random_state=42)
        clf.fit(Xtr, ytr)
        scores.append(clf.score(Xte, yte))
    fig, ax = plt.subplots()
    sns.lineplot(x=depths, y=scores, marker="o", ax=ax)
    ax.set_xlabel("Max Depth")
    ax.set_ylabel("Accuracy")
    ax.set_title("Depth vs Accuracy")
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)


def plot_leaves_vs_accuracy(X: np.ndarray, y: np.ndarray, fname: str) -> None:
    out = ensure_output_dir() / fname
    leaves = [2, 4, 8, 16, 32]
    scores = []
    for L in leaves:
        Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=42)
        clf = REPTreeClassifier(max_leaf_nodes=L, random_state=42)
        clf.fit(Xtr, ytr)
        scores.append(clf.score(Xte, yte))
    fig, ax = plt.subplots()
    sns.lineplot(x=leaves, y=scores, marker="o", ax=ax)
    ax.set_xlabel("Max Leaf Nodes")
    ax.set_ylabel("Accuracy")
    ax.set_title("Leaf Nodes vs Accuracy")
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)


#  Error Analysis  #


def plot_confusion_and_report(
    model: REPTreeClassifier,
    X: np.ndarray,
    y: np.ndarray,
    fname: str,
    target_names: Optional[list] = None,
) -> None:
    out = ensure_output_dir() / fname
    y_pred = model.predict(X)
    cm = confusion_matrix(y, y_pred)
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
    ax.set_title("Confusion Matrix")
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)
    # Save classification report as text
    report = classification_report(y, y_pred, target_names=target_names)
    (ensure_output_dir() / "classification_report.txt").write_text(report, encoding="utf-8")


#  Pruning Effects  #


def plot_pruning_effects(X: np.ndarray, y: np.ndarray, fname: str) -> None:
    out = ensure_output_dir() / fname
    Xtr, Xval, ytr, yval = train_test_split(X, y, test_size=0.3, random_state=42)
    base = REPTreeClassifier(random_state=42)
    base.fit(Xtr, ytr)
    pruned = REPTreeClassifier(pruning="rep", random_state=42)
    pruned.fit(Xtr, ytr, X_val=Xval, y_val=yval)
    sizes = [base.tree_.count_nodes(), pruned.tree_.count_nodes()]
    accs = [base.score(Xval, yval), pruned.score(Xval, yval)]
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    sns.barplot(x=["Base", "Pruned"], y=sizes, ax=ax[0], color="#4C78A8")
    ax[0].set_title("Tree Size (nodes)")
    sns.barplot(x=["Base", "Pruned"], y=accs, ax=ax[1], color="#59A14F")
    ax[1].set_title("Validation Accuracy")
    for a in ax:
        a.set_ylim(0, max(max(sizes), max(accs)) * 1.1)
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)


#  Advanced Pruning Visualizations  #
def _build_id_map(node) -> Dict[int, object]:
    stack = [node]
    mp: Dict[int, object] = {}
    while stack:
        cur = stack.pop()
        mp[cur.node_id] = cur
        if cur.left:
            stack.append(cur.left)
        if cur.right:
            stack.append(cur.right)
    return mp


def _impurity_delta_for_node(orig_node: object) -> float:
    # For internal nodes: impurity reduction approximated as
    # parent_impurity - weighted_child_impurity
    if orig_node.is_leaf():
        return 0.0
    left = orig_node.left
    right = orig_node.right
    if not left or not right:
        return 0.0
    n = orig_node.samples
    wl = (left.samples / n) if n else 0.0
    wr = (right.samples / n) if n else 0.0
    child_imp = wl * (left.impurity or 0.0) + wr * (right.impurity or 0.0)
    return max(0.0, (orig_node.impurity or 0.0) - child_imp)


def plot_pruning_impurity_deltas(X: np.ndarray, y: np.ndarray, fname_prefix: str) -> None:
    # Train base and pruned models
    Xtr, Xval, ytr, yval = train_test_split(X, y, test_size=0.3, random_state=42)
    base = REPTreeClassifier(random_state=42)
    base.fit(Xtr, ytr)
    pruned = REPTreeClassifier(pruning="rep", random_state=42)
    pruned.fit(Xtr, ytr, X_val=Xval, y_val=yval)
    # Map original nodes by id
    id_map = _build_id_map(base.tree_)
    # For nodes that became leaves in pruned, compute delta
    deltas: List[Tuple[int, float]] = []

    def collect(node):
        if node.is_leaf():
            orig = id_map.get(node.node_id)
            if orig is not None:
                d = _impurity_delta_for_node(orig)
                if d > 0:
                    deltas.append((node.node_id, d))
        else:
            if node.left:
                collect(node.left)
            if node.right:
                collect(node.right)

    collect(pruned.tree_)
    # Sort and plot top deltas
    deltas.sort(key=lambda x: x[1], reverse=True)
    top = deltas[:20] if deltas else []
    fig, ax = plt.subplots(figsize=(8, 4))
    if top:
        ids = [f"id#{i}" for i, _ in top]
        vals = [v for _, v in top]
        sns.barplot(x=vals, y=ids, ax=ax, color="#E45756")
        ax.set_title("Top Pruned Nodes by Impurity Reduction")
        ax.set_xlabel("Impurity Reduction")
        ax.set_ylabel("Node (pruned leaf)")
    else:
        ax.text(0.5, 0.5, "No pruning deltas computed", ha="center")
        ax.axis("off")
    fig.tight_layout()
    fig.savefig(ensure_output_dir() / f"{fname_prefix}_pruning_deltas.png", dpi=150)
    plt.close(fig)

    # Overlay deltas on tree structure (color intensity)
    delta_map = {i: v for i, v in deltas}
    pos = _layout_tree_positions(pruned.tree_)
    fig, ax = plt.subplots(figsize=(10, 6))

    # Draw edges
    def draw_edges(node):
        if node.left:
            x0, y0 = pos[node.node_id]
            x1, y1 = pos[node.left.node_id]
            ax.plot([x0, x1], [y0, y1], color="#999", lw=1)
            draw_edges(node.left)
        if node.right:
            x0, y0 = pos[node.node_id]
            x1, y1 = pos[node.right.node_id]
            ax.plot([x0, x1], [y0, y1], color="#999", lw=1)
            draw_edges(node.right)

    draw_edges(pruned.tree_)
    # Normalize deltas for color scale
    max_delta = max(delta_map.values()) if delta_map else 1.0

    def draw_nodes(node):
        x, y = pos[node.node_id]
        d = delta_map.get(node.node_id, 0.0)
        intensity = d / max_delta if max_delta else 0.0
        color = (1.0, 0.5 * (1 - intensity), 0.5 * (1 - intensity))  # red intensity
        ax.scatter([x], [y], s=300, color=color, zorder=3)
        ax.text(
            x,
            y,
            f"id#{node.node_id}\nΔ={d:.3f}",
            ha="center",
            va="center",
            color="white",
            fontsize=8,
        )
        if node.left:
            draw_nodes(node.left)
        if node.right:
            draw_nodes(node.right)

    draw_nodes(pruned.tree_)
    ax.axis("off")
    ax.set_title("Pruned Tree with Impurity Reduction Intensity")
    fig.tight_layout()
    fig.savefig(ensure_output_dir() / f"{fname_prefix}_pruned_tree_deltas.png", dpi=150)
    plt.close(fig)


#  Regression Diagnostics  #


def plot_regression_diagnostics(X: np.ndarray, y: np.ndarray, fname_prefix: str) -> None:
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=42)
    reg = REPTreeRegressor(random_state=42)
    reg.fit(Xtr, ytr)
    y_pred = reg.predict(Xte)
    # Pred vs True
    fig, ax = plt.subplots()
    ax.scatter(yte, y_pred, color="#4C78A8", alpha=0.7)
    lims = [min(yte.min(), y_pred.min()), max(yte.max(), y_pred.max())]
    ax.plot(lims, lims, "--", color="gray")
    ax.set_xlabel("True")
    ax.set_ylabel("Predicted")
    ax.set_title("Regression: Predicted vs True")
    fig.tight_layout()
    fig.savefig(ensure_output_dir() / f"{fname_prefix}_pred_vs_true.png", dpi=150)
    plt.close(fig)
    # Residuals
    residuals = y_pred - yte
    fig, ax = plt.subplots()
    sns.histplot(residuals, kde=True, ax=ax, color="#59A14F")
    ax.set_title("Residuals Distribution")
    fig.tight_layout()
    fig.savefig(ensure_output_dir() / f"{fname_prefix}_residuals.png", dpi=150)
    plt.close(fig)


#  Data Loaders  #


def load_iris() -> Tuple[pd.DataFrame, np.ndarray, np.ndarray, list]:
    path = DATA_DIR / "classification" / "iris_original.csv"
    df = pd.read_csv(path)
    # Detect target column name
    target = "class" if "class" in df.columns else "species"
    feature_cols = [c for c in df.columns if c != target]
    X = df[feature_cols].values
    y = df[target].values
    return df, X, y, feature_cols


def load_bike_hour() -> Tuple[pd.DataFrame, np.ndarray, np.ndarray, list]:
    path = DATA_DIR / "regression" / "hour.csv"
    df = pd.read_csv(path)
    # Pick a small subset of features for clarity
    target = "cnt"
    feature_cols = [
        "season",
        "mnth",
        "hr",
        "holiday",
        "weekday",
        "workingday",
        "temp",
        "atemp",
        "hum",
        "windspeed",
    ]
    df_small = df[feature_cols + [target]].dropna()
    X = df_small[feature_cols].values
    y = df_small[target].values.astype(float)
    return df_small, X, y, feature_cols


#  Runner  #


def run_iris_visualizations():
    df, X, y, feature_names = load_iris()
    target_col = "class" if "class" in df.columns else "species"
    # Dataset
    plot_distributions(
        df, target=target_col, title="Iris Feature Distributions", fname="iris_distributions.png"
    )
    plot_pairplot(df, target=target_col, fname="iris_pairplot.png")
    plot_correlations(
        df, target=target_col, title="Iris Correlations", fname="iris_correlations.png"
    )
    # Model
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=42)
    # Convert string labels to integer codes for utils.check_X_y compatibility
    labels, y_all_codes = np.unique(y, return_inverse=True)
    y_codes = y_all_codes
    # Align train/test splits with codes
    # Recompute splits using codes to keep consistency
    Xtr, Xte, ytr_codes, yte_codes = train_test_split(X, y_codes, test_size=0.3, random_state=42)
    clf = REPTreeClassifier(max_depth=4, random_state=42)
    clf.fit(Xtr, ytr_codes)
    # Plots
    plot_tree_structure(clf, feature_names, fname="iris_tree_structure.png")
    plot_feature_importance(clf, feature_names, fname="iris_feature_importance.png")
    plot_decision_boundary_2d(clf, X, y, fname="iris_decision_boundary.png")
    # Map predictions back to original labels for confusion matrix/report
    plot_confusion_and_report(
        clf, Xte, yte_codes, fname="iris_confusion.png", target_names=list(labels)
    )
    plot_depth_vs_accuracy(X, y_codes, fname="iris_depth_vs_accuracy.png")
    plot_leaves_vs_accuracy(X, y_codes, fname="iris_leaves_vs_accuracy.png")
    plot_pruning_effects(X, y_codes, fname="iris_pruning_effects.png")
    plot_pruning_impurity_deltas(X, y_codes, fname_prefix="iris")


def run_bike_regression_visualizations():
    df, X, y, feature_names = load_bike_hour()
    plot_correlations(
        df, target=None, title="Bike Hour Correlations", fname="bike_correlations.png"
    )
    plot_regression_diagnostics(X, y, fname_prefix="bike_hour")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="REPTree visualization suite")
    parser.add_argument(
        "--dataset", choices=["iris", "bike", "all"], default="all", help="Select dataset"
    )
    parser.add_argument(
        "--plots",
        nargs="*",
        choices=[
            "dataset",
            "model",
            "boundaries",
            "training",
            "errors",
            "pruning",
            "pruning-advanced",
            "regression",
        ],
        help="Which plots to generate (default: all relevant)",
    )
    args = parser.parse_args()

    ensure_output_dir()
    print(f"Saving figures to: {OUTPUT_DIR}")

    def run_iris_selected():
        df, X, y, feature_names = load_iris()
        target_col = "class" if "class" in df.columns else "species"
        labels, y_codes = np.unique(y, return_inverse=True)
        # Dataset
        if not args.plots or "dataset" in args.plots:
            plot_distributions(
                df,
                target=target_col,
                title="Iris Feature Distributions",
                fname="iris_distributions.png",
            )
            plot_pairplot(df, target=target_col, fname="iris_pairplot.png")
            plot_correlations(
                df, target=target_col, title="Iris Correlations", fname="iris_correlations.png"
            )
        # Model
        Xtr, Xte, ytr_codes, yte_codes = train_test_split(
            X, y_codes, test_size=0.3, random_state=42
        )
        clf = REPTreeClassifier(max_depth=4, random_state=42)
        clf.fit(Xtr, ytr_codes)
        if not args.plots or "model" in args.plots:
            plot_tree_structure(clf, feature_names, fname="iris_tree_structure.png")
            plot_feature_importance(clf, feature_names, fname="iris_feature_importance.png")
        if not args.plots or "boundaries" in args.plots:
            plot_decision_boundary_2d(clf, X, y_codes, fname="iris_decision_boundary.png")
        if not args.plots or "errors" in args.plots:
            plot_confusion_and_report(
                clf, Xte, yte_codes, fname="iris_confusion.png", target_names=list(labels)
            )
        if not args.plots or "training" in args.plots:
            plot_depth_vs_accuracy(X, y_codes, fname="iris_depth_vs_accuracy.png")
            plot_leaves_vs_accuracy(X, y_codes, fname="iris_leaves_vs_accuracy.png")
        if not args.plots or "pruning" in args.plots:
            plot_pruning_effects(X, y_codes, fname="iris_pruning_effects.png")
        if not args.plots or "pruning-advanced" in args.plots:
            plot_pruning_impurity_deltas(X, y_codes, fname_prefix="iris")

    def run_bike_selected():
        df, X, y, feature_names = load_bike_hour()
        if not args.plots or "dataset" in args.plots:
            plot_correlations(
                df, target=None, title="Bike Hour Correlations", fname="bike_correlations.png"
            )
        if not args.plots or "regression" in args.plots:
            plot_regression_diagnostics(X, y, fname_prefix="bike_hour")

    if args.dataset in ("iris", "all"):
        run_iris_selected()
    if args.dataset in ("bike", "all"):
        run_bike_selected()

    print("Done. Figures generated.")
