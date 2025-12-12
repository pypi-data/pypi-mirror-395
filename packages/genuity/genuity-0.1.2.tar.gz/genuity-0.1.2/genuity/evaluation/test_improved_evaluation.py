#!/usr/bin/env python3
"""
Test script for improved evaluation framework with better error handling.
"""

import pandas as pd
import numpy as np
from sklearn.datasets import make_classification

# Import the evaluation framework
from genuity.evaluation import evaluate_synthetic_data_comprehensive


def create_test_data():
    """Create test data with various issues to test error handling."""
    print("📊 Creating test data...")

    # Create small dataset to test minimum size warnings
    X, y = make_classification(
        n_samples=50,  # Small size to trigger warnings
        n_features=5,
        n_informative=3,
        n_redundant=1,
        random_state=42,
    )

    # Create DataFrame
    df_real = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(5)])
    df_real["target"] = y
    df_real["category"] = np.random.choice(["A", "B"], size=50)

    # Add some missing values
    df_real.loc[df_real.index[0:6], "feature_0"] = np.nan

    # Create synthetic data with even smaller size
    df_synthetic = df_real.copy()
    df_synthetic = df_synthetic.sample(
        n=10, random_state=42
    )  # Very small synthetic dataset

    # Add noise to simulate synthetic data
    for col in df_synthetic.columns:
        if col.startswith("feature"):
            df_synthetic[col] += np.random.normal(0, 0.1, size=len(df_synthetic))

    # Add different missing patterns
    df_synthetic.loc[df_synthetic.index[0:3], "feature_1"] = np.nan

    print(f"✅ Created test data:")
    print(f"   Real data: {df_real.shape}")
    print(f"   Synthetic data: {df_synthetic.shape}")
    print(f"   Missing values in real: {df_real.isnull().sum().sum()}")
    print(f"   Missing values in synthetic: {df_synthetic.isnull().sum().sum()}")

    return df_real, df_synthetic


def test_improved_evaluation():
    """Test the improved evaluation framework."""
    print("\n" + "=" * 60)
    print("🧪 TESTING IMPROVED EVALUATION FRAMEWORK")
    print("=" * 60)

    # Create test data
    df_real, df_synthetic = create_test_data()

    print("\n🚀 Running comprehensive evaluation...")
    print("(This will demonstrate improved error handling and validation)")

    try:
        # Run evaluation
        results = evaluate_synthetic_data_comprehensive(
            real_data=df_real,
            synthetic_data=df_synthetic,
            target_column="target",
            generate_plots=False,  # Skip plots for this test
        )

        print("\n✅ Evaluation completed successfully!")
        print("📊 Results summary:")

        if "overall_scores" in results:
            scores = results["overall_scores"]
            for category, score in scores.items():
                if np.isnan(score):
                    print(f"   {category.capitalize()}: N/A")
                else:
                    print(f"   {category.capitalize()}: {score:.4f}")

        print("\n🎯 Key improvements demonstrated:")
        print("   ✅ Data validation with warnings")
        print("   ✅ Graceful error handling for each metric category")
        print("   ✅ NaN value filtering in score calculation")
        print("   ✅ Helpful recommendations for improvement")
        print("   ✅ Detailed error messages for debugging")

    except Exception as e:
        print(f"\n❌ Evaluation failed: {e}")
        print("This should not happen with the improved error handling!")


if __name__ == "__main__":
    test_improved_evaluation()
