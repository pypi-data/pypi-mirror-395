#!/usr/bin/env python3
"""
Example Usage of Comprehensive Evaluation Framework

This script demonstrates how to use the evaluation framework
with all 29+ metrics across 5 dimensions.
"""

import pandas as pd
import numpy as np
from sklearn.datasets import make_classification, make_regression
from sklearn.model_selection import train_test_split

# Import the evaluation framework
from genuity.evaluation import (
    evaluate_synthetic_data_comprehensive,
    ComprehensiveSyntheticEvaluator,
    evaluate_similarity_metrics,
    evaluate_utility_metrics,
    evaluate_privacy_metrics,
    evaluate_detectability_metrics,
    evaluate_missingness_metrics,
)


def create_sample_data():
    """Create sample real and synthetic data for demonstration."""
    print("📊 Creating sample data...")

    # Create classification dataset
    X_class, y_class = make_classification(
        n_samples=1000, n_features=10, n_informative=8, n_redundant=2, random_state=42
    )

    # Create regression dataset
    X_reg, y_reg = make_regression(
        n_samples=1000, n_features=8, n_informative=6, random_state=42
    )

    # Combine features
    X_combined = np.hstack([X_class, X_reg])

    # Create DataFrame with mixed data types
    feature_names = [f"feature_{i}" for i in range(X_combined.shape[1])]
    df_real = pd.DataFrame(X_combined, columns=feature_names)

    # Add target column
    df_real["target"] = y_class

    # Add some categorical columns
    df_real["category_1"] = np.random.choice(["A", "B", "C"], size=1000)
    df_real["category_2"] = np.random.choice(["X", "Y", "Z"], size=1000)

    # Add some missing values
    df_real.loc[np.random.choice(df_real.index, size=50), "feature_0"] = np.nan
    df_real.loc[np.random.choice(df_real.index, size=30), "category_1"] = np.nan

    # Create synthetic data (simulate synthetic generation)
    # In practice, this would come from your synthetic data generator
    df_synthetic = df_real.copy()

    # Add some noise to simulate synthetic data
    noise_factor = 0.1
    for col in df_synthetic.columns:
        if col in ["feature_0", "feature_1", "feature_2", "feature_3", "feature_4"]:
            df_synthetic[col] += np.random.normal(
                0, noise_factor, size=len(df_synthetic)
            )

    # Slightly modify categorical distributions
    df_synthetic["category_1"] = np.random.choice(
        ["A", "B", "C"], size=1000, p=[0.35, 0.35, 0.30]
    )
    df_synthetic["category_2"] = np.random.choice(
        ["X", "Y", "Z"], size=1000, p=[0.33, 0.34, 0.33]
    )

    # Add different missing patterns
    df_synthetic.loc[np.random.choice(df_synthetic.index, size=40), "feature_1"] = (
        np.nan
    )
    df_synthetic.loc[np.random.choice(df_synthetic.index, size=35), "category_2"] = (
        np.nan
    )

    print(f"✅ Created sample data:")
    print(f"   Real data shape: {df_real.shape}")
    print(f"   Synthetic data shape: {df_synthetic.shape}")
    print(f"   Features: {list(df_real.columns)}")

    return df_real, df_synthetic


def example_1_basic_evaluation():
    """Example 1: Basic comprehensive evaluation."""
    print("\n" + "=" * 60)
    print("🎯 EXAMPLE 1: Basic Comprehensive Evaluation")
    print("=" * 60)

    # Create sample data
    df_real, df_synthetic = create_sample_data()

    # Run comprehensive evaluation
    results = evaluate_synthetic_data_comprehensive(
        real_data=df_real,
        synthetic_data=df_synthetic,
        target_column="target",
        generate_plots=True,
        save_plots_path="example_evaluation_plots.png",
    )

    # Print results summary
    print("\n📊 EVALUATION RESULTS SUMMARY:")
    print("-" * 40)

    if "overall_scores" in results:
        scores = results["overall_scores"]
        for category, score in scores.items():
            print(f"   {category.capitalize()}: {score:.4f}")

    print(f"\n✅ Evaluation complete! Plots saved to: example_evaluation_plots.png")


def example_2_category_specific_evaluation():
    """Example 2: Category-specific evaluation."""
    print("\n" + "=" * 60)
    print("🎯 EXAMPLE 2: Category-Specific Evaluation")
    print("=" * 60)

    # Create sample data
    df_real, df_synthetic = create_sample_data()

    # Evaluate only similarity metrics
    print("\n📏 Evaluating Similarity Metrics...")
    similarity_results = evaluate_similarity_metrics(df_real, df_synthetic)
    print("   Similarity evaluation complete!")

    # Evaluate only utility metrics
    print("\n🎯 Evaluating Utility Metrics...")
    utility_results = evaluate_utility_metrics(
        df_real, df_synthetic, target_column="target"
    )
    print("   Utility evaluation complete!")

    # Evaluate only privacy metrics
    print("\n🔒 Evaluating Privacy Metrics...")
    privacy_results = evaluate_privacy_metrics(df_real, df_synthetic)
    print("   Privacy evaluation complete!")

    # Evaluate only detectability metrics
    print("\n🔍 Evaluating Detectability Metrics...")
    detectability_results = evaluate_detectability_metrics(df_real, df_synthetic)
    print("   Detectability evaluation complete!")

    # Evaluate only missingness metrics
    print("\n❓ Evaluating Missingness Metrics...")
    missingness_results = evaluate_missingness_metrics(df_real, df_synthetic)
    print("   Missingness evaluation complete!")

    print("\n✅ All category-specific evaluations complete!")


def example_3_advanced_usage():
    """Example 3: Advanced usage with custom configuration."""
    print("\n" + "=" * 60)
    print("🎯 EXAMPLE 3: Advanced Usage with Custom Configuration")
    print("=" * 60)

    # Create sample data
    df_real, df_synthetic = create_sample_data()

    # Create evaluator with custom configuration
    evaluator = ComprehensiveSyntheticEvaluator(
        real_data=df_real,
        synthetic_data=df_synthetic,
        target_column="target",
        categorical_columns=["category_1", "category_2"],
    )

    # Run comprehensive evaluation
    results = evaluator.comprehensive_evaluation()

    # Analyze specific results
    print("\n📊 DETAILED ANALYSIS:")
    print("-" * 30)

    # Similarity analysis
    if "similarity" in results:
        print("\n📏 Similarity Metrics:")
        for category, metrics in results["similarity"].items():
            if isinstance(metrics, dict):
                for metric_name, value in metrics.items():
                    if isinstance(value, dict):
                        # Handle per-column metrics
                        avg_value = np.mean(list(value.values()))
                        print(f"   {category}_{metric_name}: {avg_value:.4f}")
                    elif isinstance(value, (int, float)):
                        print(f"   {category}_{metric_name}: {value:.4f}")

    # Utility analysis
    if "utility" in results:
        print("\n🎯 Utility Metrics:")
        for category, metrics in results["utility"].items():
            if isinstance(metrics, dict):
                for metric_name, value in metrics.items():
                    if isinstance(value, (int, float)):
                        print(f"   {category}_{metric_name}: {value:.4f}")

    # Privacy analysis
    if "privacy" in results:
        print("\n🔒 Privacy Metrics:")
        for category, metrics in results["privacy"].items():
            if isinstance(metrics, dict):
                for metric_name, value in metrics.items():
                    if isinstance(value, (int, float)):
                        print(f"   {category}_{metric_name}: {value:.4f}")

    # Generate custom visualizations
    evaluator.generate_visualizations(save_path="advanced_evaluation_plots.png")
    print(
        f"\n✅ Advanced evaluation complete! Plots saved to: advanced_evaluation_plots.png"
    )


def example_4_privacy_focused_evaluation():
    """Example 4: Privacy-focused evaluation."""
    print("\n" + "=" * 60)
    print("🎯 EXAMPLE 4: Privacy-Focused Evaluation")
    print("=" * 60)

    # Create sample data
    df_real, df_synthetic = create_sample_data()

    # Focus on privacy metrics
    privacy_results = evaluate_privacy_metrics(df_real, df_synthetic)

    print("\n🔒 PRIVACY METRICS ANALYSIS:")
    print("-" * 30)

    if "membership_inference" in privacy_results:
        membership_auc = privacy_results["membership_inference"].get(
            "membership_inference_auc", 0.0
        )
        print(f"   Membership Inference AUC: {membership_auc:.4f}")
        print(f"   Privacy Score: {1.0 - membership_auc:.4f}")

    if "attribute_inference" in privacy_results:
        attr_accuracy = privacy_results["attribute_inference"].get(
            "average_attribute_inference_accuracy", 0.0
        )
        print(f"   Average Attribute Inference Accuracy: {attr_accuracy:.4f}")
        print(f"   Privacy Score: {1.0 - attr_accuracy:.4f}")

    if "nearest_neighbor" in privacy_results:
        nn_metrics = privacy_results["nearest_neighbor"]
        dcr = nn_metrics.get("distance_to_closest_record", 0.0)
        nnr = nn_metrics.get("nearest_neighbor_distance_ratio", 0.0)
        privacy_loss = nn_metrics.get("privacy_loss_percentage", 0.0)

        print(f"   Distance to Closest Record: {dcr:.4f}")
        print(f"   Nearest Neighbor Distance Ratio: {nnr:.4f}")
        print(f"   Privacy Loss Percentage: {privacy_loss:.4f}")

    print("\n✅ Privacy evaluation complete!")


def example_5_utility_focused_evaluation():
    """Example 5: Utility-focused evaluation."""
    print("\n" + "=" * 60)
    print("🎯 EXAMPLE 5: Utility-Focused Evaluation")
    print("=" * 60)

    # Create sample data
    df_real, df_synthetic = create_sample_data()

    # Focus on utility metrics
    utility_results = evaluate_utility_metrics(
        df_real, df_synthetic, target_column="target"
    )

    print("\n🎯 UTILITY METRICS ANALYSIS:")
    print("-" * 30)

    for category, metrics in utility_results.items():
        if isinstance(metrics, dict):
            print(f"\n   {category.upper()}:")
            for metric_name, value in metrics.items():
                if isinstance(value, (int, float)):
                    print(f"     {metric_name}: {value:.4f}")

    print("\n✅ Utility evaluation complete!")


def main():
    """Run all examples."""
    print("🚀 COMPREHENSIVE EVALUATION FRAMEWORK - EXAMPLES")
    print("=" * 70)
    print("This script demonstrates the new evaluation framework with 29+ metrics")
    print(
        "across 5 dimensions: Similarity, Utility, Privacy, Detectability, Missingness"
    )
    print("=" * 70)

    try:
        # Run all examples
        example_1_basic_evaluation()
        example_2_category_specific_evaluation()
        example_3_advanced_usage()
        example_4_privacy_focused_evaluation()
        example_5_utility_focused_evaluation()

        print("\n" + "=" * 70)
        print("🎉 ALL EXAMPLES COMPLETED SUCCESSFULLY!")
        print("📊 Check the generated plot files for visualizations")
        print("📖 See README.md for detailed documentation")
        print("=" * 70)

    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("Please check your installation and dependencies.")


if __name__ == "__main__":
    main()
