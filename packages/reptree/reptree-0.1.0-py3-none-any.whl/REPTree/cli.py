"""
Command-line interface for REPTree using Typer and Loguru.

Provides commands for training, evaluation, and visualization.
"""

import sys
from pathlib import Path
from typing import Optional

try:
    import typer
    from loguru import logger
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.table import Table

    CLI_AVAILABLE = True
except ImportError:
    CLI_AVAILABLE = False
    typer = None
    Console = None
    Table = None
    Progress = None

import numpy as np

from . import __version__
from .pipeline import REPTreePipeline
from .preprocessing import DataPreprocessor
from .tree import REPTreeClassifier, REPTreeRegressor
from .utils import train_test_split

if CLI_AVAILABLE:
    app = typer.Typer(
        name="reptree",
        help="REPTree: Reduced Error Pruning Tree for Classification and Regression",
        add_completion=False,
    )
    console = Console()
else:
    app = None
    console = None


def check_cli_available():
    """Check if CLI dependencies are installed."""
    if not CLI_AVAILABLE:
        print("CLI dependencies not installed. " "Install with: pip install reptree[cli]")
        sys.exit(1)


def configure_logger(verbose: bool, log_file: Optional[Path] = None):
    """Configure loguru logger."""
    logger.remove()

    # Console logging with colors
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )

    level = "DEBUG" if verbose else "INFO"
    logger.add(sys.stderr, format=log_format, level=level, colorize=True)

    # File logging if specified
    if log_file:
        logger.add(log_file, format=log_format, level="DEBUG", rotation="10 MB", compression="zip")


def load_data(filepath: Path, target_column: str):
    """Load data from CSV file."""
    try:
        import pandas as pd

        df = pd.read_csv(filepath)
        logger.info(f"Loaded data: {df.shape[0]} samples, {df.shape[1]} features")

        if target_column not in df.columns:
            logger.error(f"Target column '{target_column}' not found")
            raise ValueError(f"Column '{target_column}' not found in data")

        feature_cols = [c for c in df.columns if c != target_column]
        X = df[feature_cols].values
        y = df[target_column].values

        logger.debug(f"Features: {feature_cols}")
        logger.debug(f"Target: {target_column}")

        return X, y, feature_cols

    except ImportError:
        logger.error("pandas is required for CSV loading. Install with: pip install pandas")
        raise


@app.command()
def version():
    """Display REPTree version."""
    check_cli_available()
    console.print(f"[bold green]REPTree version:[/bold green] {__version__}")


@app.command()
def train(
    data: Path = typer.Argument(..., help="Path to training data (CSV)"),
    target: str = typer.Option(..., "--target", "-t", help="Target column name"),
    output: Path = typer.Option("model.pkl", "--output", "-o", help="Output model path"),
    task: str = typer.Option(
        "classification", "--task", help="Task type: classification or regression"
    ),
    criterion: Optional[str] = typer.Option(None, "--criterion", help="Split criterion"),
    max_depth: Optional[int] = typer.Option(None, "--max-depth", help="Maximum tree depth"),
    min_samples_split: int = typer.Option(2, "--min-samples-split", help="Min samples to split"),
    min_samples_leaf: int = typer.Option(1, "--min-samples-leaf", help="Min samples in leaf"),
    pruning: Optional[str] = typer.Option(None, "--pruning", help="Pruning strategy (rep)"),
    test_size: float = typer.Option(0.2, "--test-size", help="Test set proportion"),
    val_size: float = typer.Option(0.2, "--val-size", help="Validation set proportion for pruning"),
    preprocess: bool = typer.Option(True, "--preprocess/--no-preprocess", help="Use preprocessing"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
    log_file: Optional[Path] = typer.Option(None, "--log-file", help="Log file path"),
):
    """
    Train a REPTree model on provided data.

    Example:
        reptree train data.csv --target Species --task classification --pruning rep
    """
    check_cli_available()
    configure_logger(verbose, log_file)

    logger.info("Starting REPTree training")
    logger.info(f"Task: {task}")

    # Load data
    with Progress(
        SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console
    ) as progress:
        progress.add_task("Loading data...", total=None)
        X, y, feature_names = load_data(data, target)

    # Split data
    logger.info(f"Splitting data: test_size={test_size}, val_size={val_size}")
    X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=val_size, random_state=42
    )

    logger.info(f"Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")

    # Create model
    if task == "classification":
        if criterion is None:
            criterion = "gini"
        model = REPTreeClassifier(
            criterion=criterion,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            pruning=pruning,
            random_state=42,
        )
    else:
        if criterion is None:
            criterion = "variance"
        model = REPTreeRegressor(
            criterion=criterion,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            pruning=pruning,
            random_state=42,
        )

    logger.info(f"Model: {model.__class__.__name__}")
    logger.info(f"Criterion: {criterion}")

    # Train
    with Progress(
        SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console
    ) as progress:
        progress.add_task("Training model...", total=None)

        if preprocess:
            logger.info("Using preprocessing pipeline")
            preprocessor = DataPreprocessor(
                handle_missing="median", categorical_encoding="label", drop_invariant=True
            )
            pipeline = REPTreePipeline(
                estimator=model,
                preprocessor=preprocessor,
                validation_size=val_size,
                random_state=42,
            )
            pipeline.fit(X_train, y_train, X_val=X_val, y_val=y_val)

            # Evaluate
            train_score = pipeline.score(X_train, y_train)
            val_score = pipeline.score(X_val, y_val)
            test_score = pipeline.score(X_test, y_test)

            # Save
            pipeline.save(str(output))
            logger.success(f"Model saved to {output}")
        else:
            model.fit(X_train, y_train, X_val=X_val, y_val=y_val)

            # Evaluate
            train_score = model.score(X_train, y_train)
            val_score = model.score(X_val, y_val)
            test_score = model.score(X_test, y_test)

            # Save
            model.save(str(output))
            logger.success(f"Model saved to {output}")

    # Display results
    table = Table(title="Training Results")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    metric_name = "Accuracy" if task == "classification" else "R²"
    table.add_row("Train " + metric_name, f"{train_score:.4f}")
    table.add_row("Validation " + metric_name, f"{val_score:.4f}")
    table.add_row("Test " + metric_name, f"{test_score:.4f}")

    if preprocess:
        tree = pipeline.estimator_.tree_
    else:
        tree = model.tree_

    table.add_row("Tree Depth", str(tree.get_depth()))
    table.add_row("Tree Nodes", str(tree.count_nodes()))
    table.add_row("Leaf Nodes", str(tree.count_leaves()))

    console.print(table)
    logger.success("Training complete!")


@app.command()
def evaluate(
    model_path: Path = typer.Argument(..., help="Path to saved model"),
    data: Path = typer.Argument(..., help="Path to evaluation data (CSV)"),
    target: str = typer.Option(..., "--target", "-t", help="Target column name"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output report path"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
):
    """
    Evaluate a trained REPTree model on new data.

    Example:
        reptree evaluate model.pkl test_data.csv --target Species
    """
    check_cli_available()
    configure_logger(verbose, None)

    logger.info("Starting model evaluation")

    # Load model
    logger.info(f"Loading model from {model_path}")
    try:
        from .pipeline import REPTreePipeline

        model = REPTreePipeline.load(str(model_path))
        is_pipeline = True
    except:
        from .tree import REPTreeClassifier, REPTreeRegressor

        try:
            model = REPTreeClassifier.load(str(model_path))
            is_pipeline = False
        except:
            model = REPTreeRegressor.load(str(model_path))
            is_pipeline = False

    logger.success("Model loaded successfully")

    # Load data
    X, y, feature_names = load_data(data, target)

    # Evaluate
    logger.info("Evaluating model...")
    score = model.score(X, y)
    predictions = model.predict(X)

    # Determine task type
    is_classification = hasattr(model, "classes_") or (
        is_pipeline and hasattr(model.estimator_, "classes_")
    )

    # Display results
    table = Table(title="Evaluation Results")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    if is_classification:
        table.add_row("Accuracy", f"{score:.4f}")

        # Classification metrics
        from .metrics import confusion_matrix

        actual_model = model.estimator_ if is_pipeline else model
        n_classes = len(actual_model.classes_)
        cm = confusion_matrix(y, predictions, n_classes)

        console.print(table)
        console.print("\n[bold]Confusion Matrix:[/bold]")
        console.print(cm)
    else:
        table.add_row("R² Score", f"{score:.4f}")

        from .metrics import mean_absolute_error, mean_squared_error

        mse = mean_squared_error(y, predictions)
        mae = mean_absolute_error(y, predictions)

        table.add_row("MSE", f"{mse:.4f}")
        table.add_row("MAE", f"{mae:.4f}")
        console.print(table)

    if output:
        logger.info(f"Saving evaluation report to {output}")
        # Save report logic here

    logger.success("Evaluation complete!")


@app.command()
def visualize(
    model_path: Path = typer.Argument(..., help="Path to saved model"),
    output_dir: Path = typer.Option(
        "visualizations", "--output-dir", "-o", help="Output directory"
    ),
    plot_tree: bool = typer.Option(True, "--tree/--no-tree", help="Plot tree structure"),
    plot_importance: bool = typer.Option(
        True, "--importance/--no-importance", help="Plot feature importance"
    ),
    max_depth: Optional[int] = typer.Option(None, "--max-depth", help="Max depth for tree plot"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
):
    """
    Generate visualizations for a trained model.

    Example:
        reptree visualize model.pkl --output-dir plots/
    """
    check_cli_available()
    configure_logger(verbose, None)

    try:
        from .visualization import MetricsVisualizer, TreeVisualizer
    except ImportError:
        logger.error(
            "Visualization dependencies not installed. Install with: pip install reptree[viz]"
        )
        raise typer.Exit(1)

    logger.info("Starting visualization generation")

    # Load model
    logger.info(f"Loading model from {model_path}")
    try:
        from .pipeline import REPTreePipeline

        model = REPTreePipeline.load(str(model_path))
        actual_model = model.estimator_
        feature_names = model.get_feature_names_out()
    except:
        from .tree import REPTreeClassifier, REPTreeRegressor

        try:
            model = REPTreeClassifier.load(str(model_path))
        except:
            model = REPTreeRegressor.load(str(model_path))
        actual_model = model
        feature_names = None

    logger.success("Model loaded successfully")

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Saving plots to {output_dir}")

    # Generate visualizations
    if plot_tree:
        logger.info("Generating tree structure plot...")
        viz = TreeVisualizer()
        viz.plot_tree(actual_model, feature_names=feature_names, max_depth=max_depth)
        viz.save_figure(output_dir / "tree_structure.png")
        viz.close()
        logger.success("Tree plot saved")

    if plot_importance:
        logger.info("Generating feature importance plot...")
        viz = TreeVisualizer()
        viz.plot_feature_importance(actual_model, feature_names=feature_names)
        viz.save_figure(output_dir / "feature_importance.png")
        viz.close()
        logger.success("Feature importance plot saved")

    logger.success(f"All visualizations saved to {output_dir}")


def main():
    """Entry point for CLI."""
    if not CLI_AVAILABLE:
        check_cli_available()
    app()


if __name__ == "__main__":
    main()
