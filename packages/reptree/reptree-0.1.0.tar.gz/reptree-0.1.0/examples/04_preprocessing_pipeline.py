"""
Example 04: Complete Preprocessing Pipeline

Demonstrates:
- Handling real-world messy data
- Automatic feature type detection
- Missing value imputation
- Categorical encoding
- Outlier detection and handling
- End-to-end pipeline usage
- Saving and loading complete pipelines
- Feature importance with preprocessing
"""
import argparse
import os
import sys
from pathlib import Path
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.REPTree import DataPreprocessor, REPTreeClassifier, REPTreePipeline
from src.REPTree.utils import train_test_split


def create_messy_dataset(n_samples=500, random_state=42):
    """
    Create a synthetic dataset with real-world data quality issues:
    - Missing values
    - Mixed numerical and categorical features
    - Outliers
    - Different scales
    """
    np.random.seed(random_state)

    # Numerical features with different scales
    age = np.random.normal(35, 10, n_samples)
    income = np.random.exponential(50000, n_samples)
    credit_score = np.random.normal(700, 50, n_samples)

    # Categorical features
    education_levels = ["High School", "Bachelor", "Master", "PhD"]
    education = np.random.choice(education_levels, n_samples)

    employment_types = ["Full-time", "Part-time", "Self-employed", "Unemployed"]
    employment = np.random.choice(employment_types, n_samples, p=[0.6, 0.2, 0.15, 0.05])

    # Binary target (e.g., loan approval)
    # Higher income, credit score, and education increase approval probability
    education_score = np.array([education_levels.index(e) for e in education])
    employment_score = np.array(
        [
            3 if e == "Full-time" else 2 if e == "Self-employed" else 1 if e == "Part-time" else 0
            for e in employment
        ]
    )

    probability = 1 / (
        1
        + np.exp(
            -(
                0.00003 * income
                + 0.01 * credit_score
                + 0.3 * education_score
                + 0.2 * employment_score
                + 0.05 * age
                - 10
            )
        )
    )

    y = (np.random.random(n_samples) < probability).astype(int)

    # Combine features
    X = np.column_stack([age, income, credit_score])
    X_cat = np.column_stack([education, employment])
    X_combined = np.column_stack([X, X_cat])

    # Introduce missing values (10-15% missing)
    missing_mask = np.random.random(X_combined.shape) < 0.12
    X_combined = X_combined.astype(object)
    X_combined[missing_mask] = np.nan

    # Introduce outliers in income (5% extreme values)
    outlier_indices = np.random.choice(n_samples, size=int(0.05 * n_samples), replace=False)
    X_combined[outlier_indices, 1] = np.random.uniform(200000, 500000, len(outlier_indices))

    feature_names = ["age", "income", "credit_score", "education", "employment"]

    return X_combined, y, feature_names


def print_data_quality_report(X, feature_names, title="Data Quality Report"):
    """Print statistics about data quality."""
    print(f"\n{title}")
    print("=" * 70)

    for i, name in enumerate(feature_names):
        col = X[:, i]

        # Count missing
        missing_count = np.sum([v is None or (isinstance(v, float) and np.isnan(v)) for v in col])
        missing_pct = (missing_count / len(col)) * 100

        # Get non-missing values
        non_missing = [v for v in col if not (v is None or (isinstance(v, float) and np.isnan(v)))]

        print(f"\n{name}:")
        print(f"  Missing: {missing_count} ({missing_pct:.1f}%)")

        if non_missing:
            # Check if numeric
            try:
                numeric_vals = [float(v) for v in non_missing]
                print(f"  Type: Numerical")
                print(f"  Range: [{min(numeric_vals):.2f}, {max(numeric_vals):.2f}]")
                print(f"  Mean: {np.mean(numeric_vals):.2f}")
                print(f"  Std: {np.std(numeric_vals):.2f}")

                # Check for outliers (IQR method)
                q1, q3 = np.percentile(numeric_vals, [25, 75])
                iqr = q3 - q1
                lower = q1 - 1.5 * iqr
                upper = q3 + 1.5 * iqr
                outliers = sum(1 for v in numeric_vals if v < lower or v > upper)
                if outliers > 0:
                    print(
                        f"  Potential outliers: {outliers} ({outliers/len(numeric_vals)*100:.1f}%)"
                    )
            except (ValueError, TypeError):
                print(f"  Type: Categorical")
                unique_vals = set(non_missing)
                print(f"  Unique values: {len(unique_vals)}")
                print(
                    f"  Categories: {list(unique_vals)[:5]}{'...' if len(unique_vals) > 5 else ''}"
                )


def main():
    print("=" * 70)
    print("REPTree Preprocessing Pipeline Example")
    print("=" * 70)

    # 1. Create messy dataset
    print("\n1. Creating synthetic dataset with data quality issues...")
    X, y, feature_names = create_messy_dataset(n_samples=500, random_state=42)

    print(f"   Dataset shape: {X.shape}")
    print(f"   Target distribution: Class 0: {np.sum(y==0)}, Class 1: {np.sum(y==1)}")

    # Print data quality report
    print_data_quality_report(X, feature_names, "BEFORE Preprocessing")

    # 2. Split data
    print("\n2. Splitting data (60% train, 20% validation, 20% test)...")
    X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=0.25, random_state=42
    )

    print(f"   Train: {X_train.shape[0]}, Validation: {X_val.shape[0]}, Test: {X_test.shape[0]}")

    # 3. Configure preprocessor
    print("\n3. Configuring DataPreprocessor...")
    preprocessor = DataPreprocessor(
        handle_missing="median",  # Use median for numerical, mode for categorical
        categorical_encoding="label",  # Label encoding for tree-based models
        handle_outliers="clip",  # Clip outliers to IQR bounds
        outlier_method="iqr",
        outlier_threshold=1.5,
        scale_features=False,  # No scaling needed for trees
        feature_names=feature_names,
        categorical_features=["education", "employment"],  # Specify categorical features
        drop_invariant=True,
    )

    print("   Configuration:")
    print(f"   - Missing value strategy: {preprocessor.handle_missing}")
    print(f"   - Categorical encoding: {preprocessor.categorical_encoding}")
    print(f"   - Outlier handling: {preprocessor.handle_outliers}")
    print(f"   - Categorical features: {preprocessor.categorical_features}")

    # 4. Fit preprocessor and examine learned parameters
    print("\n4. Fitting preprocessor on training data...")
    preprocessor.fit(X_train, y_train)

    print(f"\n   Learned parameters:")
    print(f"   - Input features: {preprocessor.n_features_in_}")
    print(f"   - Output features: {preprocessor.n_features_out_}")
    print(f"   - Feature types detected: {preprocessor.feature_types_}")

    # Show missing value statistics
    print(f"\n   Missing value imputation values:")
    for feat_idx, fill_val in preprocessor.missing_stats_.items():
        feat_name = feature_names[feat_idx]
        print(f"   - {feat_name}: {fill_val}")

    # Show categorical mappings
    print(f"\n   Categorical encodings:")
    for feat_idx, mapping_info in preprocessor.categorical_mappings_.items():
        feat_name = feature_names[feat_idx]
        if mapping_info["type"] == "label":
            print(f"   - {feat_name}: {mapping_info['mapping']}")

    # Show outlier bounds
    print(f"\n   Outlier bounds (IQR method):")
    for feat_idx, bounds in preprocessor.outlier_bounds_.items():
        feat_name = feature_names[feat_idx]
        print(f"   - {feat_name}: [{bounds['lower']:.2f}, {bounds['upper']:.2f}]")

    # 5. Transform data
    print("\n5. Transforming data...")
    X_train_transformed = preprocessor.transform(X_train)
    X_val_transformed = preprocessor.transform(X_val)
    X_test_transformed = preprocessor.transform(X_test)

    print(f"   Transformed shapes:")
    print(f"   - Train: {X_train_transformed.shape}")
    print(f"   - Validation: {X_val_transformed.shape}")
    print(f"   - Test: {X_test_transformed.shape}")
    print(f"   - No missing values: {not np.any(np.isnan(X_train_transformed))}")
    print(f"   - All finite: {np.all(np.isfinite(X_train_transformed))}")

    # 6. Train model WITHOUT preprocessing
    print("\n6. Training model WITHOUT preprocessing (for comparison)...")
    print("   Note: This will fail or perform poorly due to data quality issues")

    try:
        # Convert to numeric where possible
        X_train_numeric = np.zeros_like(X_train, dtype=float)
        for i in range(X_train.shape[1]):
            try:
                X_train_numeric[:, i] = X_train[:, i].astype(float)
            except (ValueError, TypeError):
                # Categorical - use simple integer encoding
                unique = list(set(X_train[:, i]) - {None, np.nan})
                mapping = {v: i for i, v in enumerate(unique)}
                X_train_numeric[:, i] = [mapping.get(v, -1) for v in X_train[:, i]]

        X_test_numeric = np.zeros_like(X_test, dtype=float)
        for i in range(X_test.shape[1]):
            try:
                X_test_numeric[:, i] = X_test[:, i].astype(float)
            except (ValueError, TypeError):
                unique = list(set(X_train[:, i]) - {None, np.nan})
                mapping = {v: i for i, v in enumerate(unique)}
                X_test_numeric[:, i] = [mapping.get(v, -1) for v in X_test[:, i]]

        clf_no_prep = REPTreeClassifier(max_depth=10, random_state=42)
        clf_no_prep.fit(X_train_numeric, y_train)
        acc_no_prep = clf_no_prep.score(X_test_numeric, y_test)
        print(f"   Test accuracy WITHOUT preprocessing: {acc_no_prep:.4f}")
    except Exception as e:
        print(f"   ✗ Training failed: {str(e)[:50]}...")
        acc_no_prep = 0.0

    # 7. Train model WITH preprocessing
    print("\n7. Training model WITH preprocessing...")

    clf_with_prep = REPTreeClassifier(
        criterion="gini",
        max_depth=15,
        min_samples_split=10,
        min_samples_leaf=5,
        pruning="rep",
        random_state=42,
    )

    # Fit the classifier with the already transformed data
    clf_with_prep.fit(X_train_transformed, y_train, X_val=X_val_transformed, y_val=y_val)

    # Evaluate
    train_acc = clf_with_prep.score(X_train_transformed, y_train)
    val_acc = clf_with_prep.score(X_val_transformed, y_val)
    test_acc = clf_with_prep.score(X_test_transformed, y_test)

    print(f"\n   WITH Preprocessing Results:")
    print(f"   - Train accuracy: {train_acc:.4f}")
    print(f"   - Validation accuracy: {val_acc:.4f}")
    print(f"   - Test accuracy: {test_acc:.4f}")
    print(f"   - Tree depth: {clf_with_prep.get_depth()}")
    print(f"   - Number of nodes: {clf_with_prep.tree_.count_nodes()}")

    # 8. Feature importance
    print("\n8. Feature Importances:")
    importances = clf_with_prep.feature_importances_
    output_features = preprocessor.get_feature_names_out()

    # Sort by importance
    importance_pairs = sorted(zip(output_features, importances), key=lambda x: x[1], reverse=True)

    for name, imp in importance_pairs:
        if imp > 0.01:  # Only show significant features
            print(f"   {name:<20}: {imp:.4f} {'█' * int(imp * 50)}")

    # 9. Comparison
    print("\n9. Comparison:")
    print("=" * 70)
    print(f"   {'Method':<40} {'Test Accuracy':<15}")
    print("   " + "-" * 70)
    print(f"   {'Without Preprocessing':<40} {acc_no_prep:<15.4f}")
    print(f"   {'With Preprocessing':<40} {test_acc:<15.4f}")
    improvement = test_acc - acc_no_prep
    print(f"   {'Improvement':<40} {improvement:+.4f}")

    # 10. Create and save complete pipeline
    print("\n10. Creating complete pipeline for deployment...")

    # Create a pipeline that combines preprocessor and classifier
    deployment_pipeline = REPTreePipeline(
        estimator=clf_with_prep, preprocessor=preprocessor, validation_size=0.2, random_state=42
    )

    # Set the fitted components
    deployment_pipeline.preprocessor_ = preprocessor
    deployment_pipeline.estimator_ = clf_with_prep

    # Save pipeline
    deployment_pipeline.save("reptree_pipeline.pkl")
    print("   ✓ Pipeline saved to 'reptree_pipeline.pkl'")

    # Load and verify
    loaded_pipeline = REPTreePipeline.load("reptree_pipeline.pkl")
    print("   ✓ Pipeline loaded successfully")

    # Verify loaded pipeline works (it will preprocess X_test automatically)
    loaded_predictions = loaded_pipeline.predict(X_test)
    original_predictions = clf_with_prep.predict(X_test_transformed)
    match = np.all(loaded_predictions == original_predictions)
    print(f"   ✓ Predictions match: {match}")

    # 11. Feature info
    print("\n11. Feature Information:")
    feature_info = preprocessor.get_feature_info()
    for feat_name, info in feature_info.items():
        print(f"\n   {feat_name}:")
        print(f"   - Type: {info['type']}")
        if "encoding" in info:
            print(f"   - Encoding: {info['encoding']}")
        if "n_categories" in info:
            print(f"   - Categories: {info['n_categories']}")

    print("\n" + "=" * 70)
    print("Preprocessing pipeline example complete!")
    print("=" * 70)

    # Key takeaways
    print("\n📊 Key Takeaways:")
    print("   1. Preprocessing handles missing values, outliers, and mixed data types")
    print("   2. Pipeline provides seamless integration with tree models")
    print(f"   3. Preprocessing improved accuracy by {improvement:.1%}")
    print("   4. Complete pipeline (preprocessing + model) can be saved/loaded")
    print("   5. Feature importance maps to original feature names")
    print("   6. Automatic feature type detection simplifies workflow")


if __name__ == "__main__":
    main()
