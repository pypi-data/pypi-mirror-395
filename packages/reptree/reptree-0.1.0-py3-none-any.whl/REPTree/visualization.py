"""
Professional visualization module for REPTree.

This module provides clean, object-oriented visualization capabilities for
decision trees, training metrics, and model evaluation.
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import numpy as np

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure

    VISUALIZATION_AVAILABLE = True
except ImportError:
    VISUALIZATION_AVAILABLE = False
    plt = None
    sns = None
    Figure = None
    Axes = None


class VisualizationError(Exception):
    """Raised when visualization dependencies are not available."""

    pass


def check_visualization_available():
    """Check if visualization dependencies are installed."""
    if not VISUALIZATION_AVAILABLE:
        raise VisualizationError(
            "Visualization dependencies not installed. " "Install with: pip install reptree[viz]"
        )


class TreeVisualizer:
    """
    Visualize decision tree structure and properties.

    Parameters
    ----------
    style : str, default='whitegrid'
        Seaborn style for plots.
    figsize : tuple, default=(10, 6)
        Default figure size for plots.
    dpi : int, default=150
        Resolution for saved figures.

    Examples
    --------
    >>> from reptree import REPTreeClassifier
    >>> from reptree.visualization import TreeVisualizer
    >>> clf = REPTreeClassifier(max_depth=3)
    >>> clf.fit(X_train, y_train)
    >>> viz = TreeVisualizer()
    >>> viz.plot_tree(clf, feature_names=feature_names)
    >>> viz.save_figure('tree_structure.png')
    """

    def __init__(
        self, style: str = "whitegrid", figsize: Tuple[int, int] = (10, 6), dpi: int = 150
    ):
        check_visualization_available()
        self.style = style
        self.figsize = figsize
        self.dpi = dpi
        sns.set_style(style)
        self.current_figure: Optional[Figure] = None

    def plot_tree(
        self,
        model,
        feature_names: Optional[List[str]] = None,
        max_depth: Optional[int] = None,
        show_impurity: bool = True,
        show_samples: bool = True,
    ) -> Figure:
        """
        Plot tree structure with nodes and edges.

        Parameters
        ----------
        model : REPTreeClassifier or REPTreeRegressor
            Fitted tree model.
        feature_names : list, optional
            Names of features for display.
        max_depth : int, optional
            Maximum depth to display (None = all).
        show_impurity : bool, default=True
            Whether to show impurity values.
        show_samples : bool, default=True
            Whether to show sample counts.

        Returns
        -------
        Figure
            Matplotlib figure object.
        """
        tree = model.tree_
        if tree is None:
            raise ValueError("Model must be fitted before plotting")

        pos = self._layout_tree(tree)

        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)

        # Draw edges first
        self._draw_edges(ax, tree, pos)

        # Draw nodes
        self._draw_nodes(ax, tree, pos, feature_names, max_depth, show_impurity, show_samples)

        ax.axis("off")
        ax.set_title("REPTree Structure", fontsize=14, fontweight="bold")
        plt.tight_layout()

        self.current_figure = fig
        return fig

    def plot_feature_importance(
        self, model, feature_names: Optional[List[str]] = None, top_n: Optional[int] = None
    ) -> Figure:
        """
        Plot feature importance as horizontal bar chart.

        Parameters
        ----------
        model : fitted estimator
            Model with feature_importances_ attribute.
        feature_names : list, optional
            Names of features.
        top_n : int, optional
            Show only top N features.

        Returns
        -------
        Figure
            Matplotlib figure object.
        """
        importances = model.feature_importances_
        if importances is None:
            raise ValueError("Model has no feature importances")

        n_features = len(importances)
        if feature_names is None:
            feature_names = [f"Feature {i}" for i in range(n_features)]

        # Sort by importance
        indices = np.argsort(importances)[::-1]

        if top_n is not None:
            indices = indices[:top_n]

        fig, ax = plt.subplots(figsize=(8, max(4, len(indices) * 0.3)), dpi=self.dpi)

        y_pos = np.arange(len(indices))
        ax.barh(y_pos, importances[indices], color="#4C78A8")
        ax.set_yticks(y_pos)
        ax.set_yticklabels([feature_names[i] for i in indices])
        ax.invert_yaxis()
        ax.set_xlabel("Importance", fontsize=11)
        ax.set_title("Feature Importances", fontsize=14, fontweight="bold")
        ax.grid(axis="x", alpha=0.3)

        plt.tight_layout()
        self.current_figure = fig
        return fig

    def _layout_tree(
        self,
        node,
        x: float = 0.0,
        y: float = 0.0,
        x_gap: float = 1.6,
        y_gap: float = 1.5,
        pos: Optional[Dict] = None,
    ) -> Dict:
        """Compute positions for tree nodes using recursive layout."""
        if pos is None:
            pos = {}

        pos[node.node_id] = (x, y)

        if node.left:
            pos = self._layout_tree(node.left, x - x_gap, y - y_gap, x_gap * 0.7, y_gap, pos)
        if node.right:
            pos = self._layout_tree(node.right, x + x_gap, y - y_gap, x_gap * 0.7, y_gap, pos)

        return pos

    def _draw_edges(self, ax: Axes, node, pos: Dict):
        """Draw edges between nodes."""
        if node.left:
            x0, y0 = pos[node.node_id]
            x1, y1 = pos[node.left.node_id]
            ax.plot([x0, x1], [y0, y1], color="#999", lw=1.5, zorder=1)
            self._draw_edges(ax, node.left, pos)

        if node.right:
            x0, y0 = pos[node.node_id]
            x1, y1 = pos[node.right.node_id]
            ax.plot([x0, x1], [y0, y1], color="#999", lw=1.5, zorder=1)
            self._draw_edges(ax, node.right, pos)

    def _draw_nodes(
        self,
        ax: Axes,
        node,
        pos: Dict,
        feature_names: Optional[List[str]],
        max_depth: Optional[int],
        show_impurity: bool,
        show_samples: bool,
        current_depth: int = 0,
    ):
        """Draw nodes with labels."""
        if max_depth is not None and current_depth > max_depth:
            return

        x, y = pos[node.node_id]
        is_leaf = node.is_leaf()

        # Color coding
        color = "#59A14F" if is_leaf else "#4C78A8"

        ax.scatter([x], [y], s=400, color=color, zorder=3, edgecolors="white", linewidths=2)

        # Node label
        label_parts = []

        if not is_leaf and node.feature_index is not None:
            fname = feature_names[node.feature_index] if feature_names else f"X{node.feature_index}"
            label_parts.append(f"{fname} ≤ {node.threshold:.3f}")

        if show_samples:
            label_parts.append(f"n={node.samples}")

        if show_impurity:
            label_parts.append(f"imp={node.impurity:.3f}")

        if is_leaf:
            if isinstance(node.value, dict):
                top_class = max(node.value.items(), key=lambda x: x[1])
                label_parts.append(f"class={top_class[0]}")
            else:
                label_parts.append(f"val={node.value:.3f}")

        label = "\n".join(label_parts)

        ax.text(
            x,
            y,
            label,
            ha="center",
            va="center",
            color="white",
            fontsize=8,
            fontweight="bold",
            zorder=4,
        )

        # Recurse
        if node.left:
            self._draw_nodes(
                ax,
                node.left,
                pos,
                feature_names,
                max_depth,
                show_impurity,
                show_samples,
                current_depth + 1,
            )
        if node.right:
            self._draw_nodes(
                ax,
                node.right,
                pos,
                feature_names,
                max_depth,
                show_impurity,
                show_samples,
                current_depth + 1,
            )

    def save_figure(self, filepath: Union[str, Path], **kwargs):
        """
        Save current figure to file.

        Parameters
        ----------
        filepath : str or Path
            Output file path.
        **kwargs
            Additional arguments passed to savefig.
        """
        if self.current_figure is None:
            raise ValueError("No figure to save. Create a plot first.")

        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        self.current_figure.savefig(filepath, dpi=self.dpi, bbox_inches="tight", **kwargs)

    def close(self):
        """Close current figure."""
        if self.current_figure is not None:
            plt.close(self.current_figure)
            self.current_figure = None


class MetricsVisualizer:
    """
    Visualize training metrics and model performance.

    Parameters
    ----------
    style : str, default='whitegrid'
        Seaborn style.
    figsize : tuple, default=(10, 6)
        Default figure size.
    dpi : int, default=150
        Resolution for figures.
    """

    def __init__(
        self, style: str = "whitegrid", figsize: Tuple[int, int] = (10, 6), dpi: int = 150
    ):
        check_visualization_available()
        self.style = style
        self.figsize = figsize
        self.dpi = dpi
        sns.set_style(style)
        self.current_figure: Optional[Figure] = None

    def plot_confusion_matrix(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        class_names: Optional[List[str]] = None,
        normalize: bool = False,
    ) -> Figure:
        """
        Plot confusion matrix.

        Parameters
        ----------
        y_true : array-like
            True labels.
        y_pred : array-like
            Predicted labels.
        class_names : list, optional
            Class names for labels.
        normalize : bool, default=False
            Whether to normalize by row.

        Returns
        -------
        Figure
            Matplotlib figure.
        """
        from .metrics import confusion_matrix as cm_func

        classes = np.unique(y_true)
        n_classes = len(classes)
        cm = cm_func(y_true, y_pred, n_classes)

        if normalize:
            cm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]

        fig, ax = plt.subplots(figsize=(8, 6), dpi=self.dpi)

        sns.heatmap(
            cm,
            annot=True,
            fmt=".2f" if normalize else "d",
            cmap="Blues",
            ax=ax,
            xticklabels=class_names if class_names else classes,
            yticklabels=class_names if class_names else classes,
        )

        ax.set_xlabel("Predicted", fontsize=11)
        ax.set_ylabel("True", fontsize=11)
        ax.set_title("Confusion Matrix", fontsize=14, fontweight="bold")

        plt.tight_layout()
        self.current_figure = fig
        return fig

    def plot_learning_curve(
        self,
        depths: List[int],
        train_scores: List[float],
        val_scores: List[float],
        metric_name: str = "Accuracy",
    ) -> Figure:
        """
        Plot learning curve showing train vs validation performance.

        Parameters
        ----------
        depths : list
            Tree depths.
        train_scores : list
            Training scores.
        val_scores : list
            Validation scores.
        metric_name : str
            Name of metric for y-axis.

        Returns
        -------
        Figure
            Matplotlib figure.
        """
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)

        ax.plot(depths, train_scores, "o-", label="Training", linewidth=2, markersize=6)
        ax.plot(depths, val_scores, "s-", label="Validation", linewidth=2, markersize=6)

        ax.set_xlabel("Tree Depth", fontsize=11)
        ax.set_ylabel(metric_name, fontsize=11)
        ax.set_title(f"{metric_name} vs Tree Depth", fontsize=14, fontweight="bold")
        ax.legend(loc="best", fontsize=10)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        self.current_figure = fig
        return fig

    def plot_pruning_comparison(
        self, unpruned_nodes: int, pruned_nodes: int, unpruned_acc: float, pruned_acc: float
    ) -> Figure:
        """
        Compare pruned vs unpruned tree.

        Parameters
        ----------
        unpruned_nodes : int
            Node count before pruning.
        pruned_nodes : int
            Node count after pruning.
        unpruned_acc : float
            Accuracy before pruning.
        pruned_acc : float
            Accuracy after pruning.

        Returns
        -------
        Figure
            Matplotlib figure.
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=self.dpi)

        # Node count comparison
        labels = ["Unpruned", "Pruned"]
        nodes = [unpruned_nodes, pruned_nodes]
        colors = ["#4C78A8", "#59A14F"]

        ax1.bar(labels, nodes, color=colors)
        ax1.set_ylabel("Number of Nodes", fontsize=11)
        ax1.set_title("Tree Complexity", fontsize=12, fontweight="bold")
        ax1.grid(axis="y", alpha=0.3)

        # Add percentage reduction
        reduction = ((unpruned_nodes - pruned_nodes) / unpruned_nodes) * 100
        ax1.text(
            0.5,
            max(nodes) * 0.95,
            f"{reduction:.1f}% reduction",
            ha="center",
            fontsize=10,
            fontweight="bold",
        )

        # Accuracy comparison
        accs = [unpruned_acc, pruned_acc]
        ax2.bar(labels, accs, color=colors)
        ax2.set_ylabel("Accuracy", fontsize=11)
        ax2.set_title("Model Performance", fontsize=12, fontweight="bold")
        ax2.set_ylim([min(accs) * 0.95, max(accs) * 1.05])
        ax2.grid(axis="y", alpha=0.3)

        plt.tight_layout()
        self.current_figure = fig
        return fig

    def save_figure(self, filepath: Union[str, Path], **kwargs):
        """Save current figure to file."""
        if self.current_figure is None:
            raise ValueError("No figure to save")

        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        self.current_figure.savefig(filepath, dpi=self.dpi, bbox_inches="tight", **kwargs)

    def close(self):
        """Close current figure."""
        if self.current_figure is not None:
            plt.close(self.current_figure)
            self.current_figure = None
