"""
REPTree: Reduced Error Pruning Tree Implementation

A scikit-learn compatible decision tree implementation with Reduced Error Pruning.
Built from scratch using NumPy for educational and research purposes.

Basic Usage
-----------
Classification:
    >>> from REPTree import REPTreeClassifier
    >>> clf = REPTreeClassifier(max_depth=5, pruning='rep')
    >>> clf.fit(X_train, y_train, X_val=X_val, y_val=y_val)
    >>> predictions = clf.predict(X_test)

Regression:
    >>> from REPTree import REPTreeRegressor
    >>> reg = REPTreeRegressor(criterion='variance', pruning='rep')
    >>> reg.fit(X_train, y_train, X_val=X_val, y_val=y_val)
    >>> predictions = reg.predict(X_test)

With Preprocessing:
    >>> from REPTree import REPTreePipeline, DataPreprocessor
    >>> preprocessor = DataPreprocessor(handle_missing='median')
    >>> pipeline = REPTreePipeline(clf, preprocessor)
    >>> pipeline.fit(X_train, y_train)
    >>> predictions = pipeline.predict(X_test)

Visualization (requires viz extras):
    >>> from REPTree.visualization import TreeVisualizer
    >>> viz = TreeVisualizer()
    >>> viz.plot_tree(clf, feature_names=feature_names)
    >>> viz.save_figure('tree.png')

CLI (requires cli extras):
    $ reptree train data.csv --target Species --pruning rep
    $ reptree evaluate model.pkl test.csv --target Species
    $ reptree visualize model.pkl --output-dir plots/
"""

from ._version import __version__
from .pipeline import REPTreePipeline
from .preprocessing import DataPreprocessor, DataValidator
from .tree import REPTreeClassifier, REPTreeRegressor

__all__ = [
    "__version__",
    "REPTreeClassifier",
    "REPTreeRegressor",
    "DataPreprocessor",
    "DataValidator",
    "REPTreePipeline",
]

# Soft import for visualization
try:
    from .visualization import MetricsVisualizer, TreeVisualizer

    __all__.extend(["TreeVisualizer", "MetricsVisualizer"])
except ImportError:
    pass

# Package metadata
__author__ = "Your Name"
__email__ = "your.email@example.com"
__license__ = "MIT"
__description__ = "A scikit-learn compatible decision tree with Reduced Error Pruning"
__url__ = "https://github.com/yourusername/reptree"
