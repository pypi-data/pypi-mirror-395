"""
Comprehensive Synthetic Data Evaluation Framework

This module provides a complete evaluation suite for assessing synthetic data quality
across multiple dimensions: similarity, utility, privacy, detectability, and missingness.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional, Union
import warnings

# Import all metric classes
from .metrics.similarity import (
    UnivariateSimilarityMetrics,
    MultivariateSimilarityMetrics,
    CorrelationSimilarityMetrics,
    SDMetricsSimilarity,
)
from .metrics.utility import (
    TSTRMetrics,
    TRTSMetrics,
    PredictionAgreementMetrics,
    LikelihoodLeakMetrics,
)
from .metrics.privacy import (
    MembershipInferenceMetrics,
    AttributeInferenceMetrics,
    NearestNeighborMetrics,
)
from .metrics.detectability import ClassifierAUCMetrics
from .metrics.missingness import MissingnessPatternMetrics

warnings.filterwarnings("ignore")

# Set style for plots
plt.style.use("default")
sns.set_palette("husl")


class ComprehensiveSyntheticEvaluator:
    """
    Comprehensive evaluation framework for synthetic data quality assessment.

    Evaluates synthetic data across 5 dimensions:
    1. Similarity: Statistical similarity between real and synthetic data
    2. Utility: Data utility for downstream tasks
    3. Privacy: Privacy preservation capabilities
    4. Detectability: How well synthetic data can be detected
    5. Missingness: Missing value pattern preservation
    """

    def __init__(
        self,
        real_data: pd.DataFrame,
        synthetic_data: pd.DataFrame,
        target_column: Optional[str] = None,
        categorical_columns: Optional[List[str]] = None,
    ):
        """
        Initialize the evaluator.

        Args:
            real_data: Original real dataset
            synthetic_data: Generated synthetic dataset
            target_column: Target variable for utility evaluation
            categorical_columns: List of categorical column names
        """
        self.real_data = real_data.copy()
        self.synthetic_data = synthetic_data.copy()
        self.target_column = target_column
        self.categorical_columns = categorical_columns or []

        # Auto-detect categorical columns if not provided
        if not self.categorical_columns:
            self.categorical_columns = self._auto_detect_categorical()

        self.numerical_columns = [
            col
            for col in real_data.columns
            if col
            not in self.categorical_columns + ([target_column] if target_column else [])
        ]

        # Ensure same columns
        common_cols = set(real_data.columns) & set(synthetic_data.columns)
        self.real_data = self.real_data[list(common_cols)]
        self.synthetic_data = self.synthetic_data[list(common_cols)]

        print(f"📊 Evaluation Setup: {len(common_cols)} columns")
        print(f"   Real data: {self.real_data.shape}")
        print(f"   Synthetic data: {self.synthetic_data.shape}")
        print(f"   Numerical columns: {len(self.numerical_columns)}")
        print(f"   Categorical columns: {len(self.categorical_columns)}")

        # Initialize results storage
        self.results = {}

        # Validate data requirements
        self._validate_data_requirements()

    def _auto_detect_categorical(self) -> List[str]:
        """Auto-detect categorical columns."""
        categorical_cols = []
        for col in self.real_data.columns:
            if (
                self.real_data[col].dtype == "object"
                or self.real_data[col].dtype == "category"
            ):
                categorical_cols.append(col)
            elif len(self.real_data[col].unique()) < min(10, len(self.real_data) * 0.1):
                categorical_cols.append(col)
        return categorical_cols

    def _validate_data_requirements(self):
        """Validate minimum data requirements for evaluation."""
        print("\n🔍 VALIDATING DATA REQUIREMENTS")
        print("=" * 50)

        # Check minimum sample sizes
        min_real_samples = 50
        min_synthetic_samples = 10

        if len(self.real_data) < min_real_samples:
            print(
                f"⚠️ Warning: Real data has only {len(self.real_data)} samples (minimum: {min_real_samples})"
            )

        if len(self.synthetic_data) < min_synthetic_samples:
            print(
                f"⚠️ Warning: Synthetic data has only {len(self.synthetic_data)} samples (minimum: {min_synthetic_samples})"
            )

        # Check for sufficient numerical columns
        if len(self.numerical_columns) < 2:
            print(
                f"⚠️ Warning: Only {len(self.numerical_columns)} numerical columns found (minimum: 2)"
            )

        # Check for sufficient categorical columns
        if len(self.categorical_columns) < 1:
            print(
                f"⚠️ Warning: Only {len(self.categorical_columns)} categorical columns found (minimum: 1)"
            )

        # Check for target column if utility metrics are needed
        if not self.target_column:
            print("ℹ️ No target column specified - utility metrics will be skipped")

        print("✅ Data validation complete")

    def _provide_recommendations(self):
        """Provide recommendations based on evaluation results."""
        print("\n💡 RECOMMENDATIONS")
        print("=" * 50)

        recommendations = []

        # Check for common issues
        if len(self.synthetic_data) < 100:
            recommendations.append(
                "📈 Increase synthetic data size to at least 100 samples for better evaluation"
            )

        if len(self.real_data) < 100:
            recommendations.append(
                "📈 Increase real data size to at least 100 samples for better evaluation"
            )

        if len(self.numerical_columns) < 3:
            recommendations.append(
                "📊 Add more numerical features for comprehensive similarity evaluation"
            )

        if len(self.categorical_columns) < 2:
            recommendations.append(
                "📊 Add more categorical features for comprehensive evaluation"
            )

        # Check for missing dependencies
        try:
            import sdmetrics
        except ImportError:
            recommendations.append(
                "📦 Install SDMetrics: pip install sdmetrics (for advanced similarity metrics)"
            )

        # Check for target column issues
        if not self.target_column:
            recommendations.append("🎯 Specify a target column for utility evaluation")

        # Check for data quality issues
        if self.synthetic_data.isnull().sum().sum() > 0:
            recommendations.append("🧹 Clean missing values in synthetic data")

        if self.real_data.isnull().sum().sum() > 0:
            recommendations.append("🧹 Clean missing values in real data")

        if recommendations:
            for rec in recommendations:
                print(f"   {rec}")
        else:
            print("   ✅ No specific recommendations at this time")

        print("=" * 50)

    def evaluate_similarity_metrics(self) -> Dict:
        """Evaluate all similarity metrics."""
        print("\n📏 EVALUATING SIMILARITY METRICS")
        print("=" * 50)

        similarity_results = {}

        try:
            # Initialize similarity metric evaluators
            univariate = UnivariateSimilarityMetrics(
                self.real_data, self.synthetic_data
            )
            similarity_results["univariate"] = univariate.evaluate_all()
        except Exception as e:
            print(f"⚠️ Error in univariate similarity metrics: {e}")
            similarity_results["univariate"] = {}

        try:
            multivariate = MultivariateSimilarityMetrics(
                self.real_data, self.synthetic_data
            )
            similarity_results["multivariate"] = multivariate.evaluate_all()
        except Exception as e:
            print(f"⚠️ Error in multivariate similarity metrics: {e}")
            similarity_results["multivariate"] = {}

        try:
            correlation = CorrelationSimilarityMetrics(
                self.real_data, self.synthetic_data
            )
            similarity_results["correlation"] = correlation.evaluate_all()
        except Exception as e:
            print(f"⚠️ Error in correlation similarity metrics: {e}")
            similarity_results["correlation"] = {}

        try:
            sdmetrics = SDMetricsSimilarity(self.real_data, self.synthetic_data)
            similarity_results["sdmetrics"] = sdmetrics.evaluate_all()
        except Exception as e:
            print(f"⚠️ Error in SDMetrics similarity metrics: {e}")
            similarity_results["sdmetrics"] = {}

        self.results["similarity"] = similarity_results
        print("✅ Similarity metrics evaluation complete")
        return similarity_results

    def evaluate_utility_metrics(self) -> Dict:
        """Evaluate all utility metrics."""
        print("\n🎯 EVALUATING UTILITY METRICS")
        print("=" * 50)

        if not self.target_column:
            print("⚠️ No target column specified. Skipping utility metrics.")
            self.results["utility"] = {}
            return {}

        utility_results = {}

        try:
            tstr = TSTRMetrics(self.real_data, self.synthetic_data, self.target_column)
            utility_results["tstr"] = tstr.evaluate_all()
        except Exception as e:
            print(f"⚠️ Error in TSTR metrics: {e}")
            utility_results["tstr"] = {}

        try:
            trts = TRTSMetrics(self.real_data, self.synthetic_data, self.target_column)
            utility_results["trts"] = trts.evaluate_all()
        except Exception as e:
            print(f"⚠️ Error in TRTS metrics: {e}")
            utility_results["trts"] = {}

        try:
            prediction_agreement = PredictionAgreementMetrics(
                self.real_data, self.synthetic_data, self.target_column
            )
            utility_results["prediction_agreement"] = (
                prediction_agreement.evaluate_all()
            )
        except Exception as e:
            print(f"⚠️ Error in prediction agreement metrics: {e}")
            utility_results["prediction_agreement"] = {}

        try:
            likelihood_leak = LikelihoodLeakMetrics(self.real_data, self.synthetic_data)
            utility_results["likelihood_leak"] = likelihood_leak.evaluate_all()
        except Exception as e:
            print(f"⚠️ Error in likelihood leak metrics: {e}")
            utility_results["likelihood_leak"] = {}

        self.results["utility"] = utility_results
        print("✅ Utility metrics evaluation complete")
        return utility_results

    def evaluate_privacy_metrics(self) -> Dict:
        """Evaluate all privacy metrics."""
        print("\n🔒 EVALUATING PRIVACY METRICS")
        print("=" * 50)

        privacy_results = {}

        try:
            membership_inference = MembershipInferenceMetrics(
                self.real_data, self.synthetic_data
            )
            privacy_results["membership_inference"] = (
                membership_inference.evaluate_all()
            )
        except Exception as e:
            print(f"⚠️ Error in membership inference metrics: {e}")
            privacy_results["membership_inference"] = {}

        try:
            attribute_inference = AttributeInferenceMetrics(
                self.real_data, self.synthetic_data
            )
            privacy_results["attribute_inference"] = attribute_inference.evaluate_all()
        except Exception as e:
            print(f"⚠️ Error in attribute inference metrics: {e}")
            privacy_results["attribute_inference"] = {}

        try:
            nearest_neighbor = NearestNeighborMetrics(
                self.real_data, self.synthetic_data
            )
            privacy_results["nearest_neighbor"] = nearest_neighbor.evaluate_all()
        except Exception as e:
            print(f"⚠️ Error in nearest neighbor metrics: {e}")
            privacy_results["nearest_neighbor"] = {}

        self.results["privacy"] = privacy_results
        print("✅ Privacy metrics evaluation complete")
        return privacy_results

    def evaluate_detectability_metrics(self) -> Dict:
        """Evaluate all detectability metrics."""
        print("\n🔍 EVALUATING DETECTABILITY METRICS")
        print("=" * 50)

        detectability_results = {}

        try:
            classifier_auc = ClassifierAUCMetrics(self.real_data, self.synthetic_data)
            detectability_results["classifier_auc"] = classifier_auc.evaluate_all()
        except Exception as e:
            print(f"⚠️ Error in classifier AUC metrics: {e}")
            detectability_results["classifier_auc"] = {}

        self.results["detectability"] = detectability_results
        print("✅ Detectability metrics evaluation complete")
        return detectability_results

    def evaluate_missingness_metrics(self) -> Dict:
        """Evaluate all missingness metrics."""
        print("\n❓ EVALUATING MISSINGNESS METRICS")
        print("=" * 50)

        try:
            missingness = MissingnessPatternMetrics(self.real_data, self.synthetic_data)
            missingness_results = missingness.evaluate_all()
        except Exception as e:
            print(f"⚠️ Error in missingness metrics: {e}")
            missingness_results = {}

        self.results["missingness"] = missingness_results
        print("✅ Missingness metrics evaluation complete")
        return missingness_results

    def comprehensive_evaluation(self) -> Dict:
        """Run comprehensive evaluation across all dimensions."""
        print("🚀 COMPREHENSIVE SYNTHETIC DATA EVALUATION")
        print("=" * 60)

        # Run all evaluations
        self.evaluate_similarity_metrics()
        self.evaluate_utility_metrics()
        self.evaluate_privacy_metrics()
        self.evaluate_detectability_metrics()
        self.evaluate_missingness_metrics()

        # Calculate overall scores
        self._calculate_overall_scores()

        return self.results

    def _calculate_overall_scores(self):
        """Calculate overall quality scores for each category."""
        print("\n📊 CALCULATING OVERALL SCORES")
        print("=" * 50)

        overall_scores = {}

        # Similarity score
        if "similarity" in self.results:
            similarity_scores = []
            for category, metrics in self.results["similarity"].items():
                if isinstance(metrics, dict):
                    for metric_name, value in metrics.items():
                        if isinstance(value, dict):
                            # Handle nested dictionaries (e.g., per-column metrics)
                            valid_values = [
                                v
                                for v in value.values()
                                if isinstance(v, (int, float)) and not np.isnan(v)
                            ]
                            similarity_scores.extend(valid_values)
                        elif isinstance(value, (int, float)) and not np.isnan(value):
                            similarity_scores.append(value)

            overall_scores["similarity"] = (
                np.mean(similarity_scores) if similarity_scores else 0.0
            )

        # Utility score
        if "utility" in self.results:
            utility_scores = []
            for category, metrics in self.results["utility"].items():
                if isinstance(metrics, dict):
                    for metric_name, value in metrics.items():
                        if isinstance(value, (int, float)) and not np.isnan(value):
                            utility_scores.append(value)

            overall_scores["utility"] = (
                np.mean(utility_scores) if utility_scores else 0.0
            )

        # Privacy score
        if "privacy" in self.results:
            privacy_scores = []
            for category, metrics in self.results["privacy"].items():
                if isinstance(metrics, dict):
                    for metric_name, value in metrics.items():
                        if isinstance(value, (int, float)) and not np.isnan(value):
                            privacy_scores.append(value)

            overall_scores["privacy"] = (
                np.mean(privacy_scores) if privacy_scores else 0.0
            )

        # Detectability score (inverted - lower is better)
        if "detectability" in self.results:
            detectability_scores = []
            for category, metrics in self.results["detectability"].items():
                if isinstance(metrics, dict):
                    for metric_name, value in metrics.items():
                        if isinstance(value, (int, float)) and not np.isnan(value):
                            detectability_scores.append(value)

            # Invert detectability scores (lower detectability = better privacy)
            avg_detectability = (
                np.mean(detectability_scores) if detectability_scores else 0.0
            )
            overall_scores["detectability"] = 1.0 - avg_detectability

        # Missingness score
        if "missingness" in self.results:
            missingness_scores = []
            for metric_name, value in self.results["missingness"].items():
                if isinstance(value, (int, float)) and not np.isnan(value):
                    missingness_scores.append(value)
                elif isinstance(value, dict):
                    # Handle nested dictionaries
                    valid_values = [
                        v
                        for v in value.values()
                        if isinstance(v, (int, float)) and not np.isnan(v)
                    ]
                    missingness_scores.extend(valid_values)

            overall_scores["missingness"] = (
                np.mean(missingness_scores) if missingness_scores else 0.0
            )

        # Overall quality score - filter out NaN values
        valid_category_scores = [
            score
            for score in overall_scores.values()
            if isinstance(score, (int, float)) and not np.isnan(score)
        ]

        if valid_category_scores:
            overall_scores["overall"] = np.mean(valid_category_scores)
        else:
            overall_scores["overall"] = 0.0

        self.results["overall_scores"] = overall_scores

        # Print summary
        print("\n📈 OVERALL QUALITY SCORES:")
        for category, score in overall_scores.items():
            if np.isnan(score):
                print(f"   {category.capitalize()}: N/A (insufficient data)")
            else:
                print(f"   {category.capitalize()}: {score:.4f}")

        # Quality assessment
        overall_score = overall_scores.get("overall", 0.0)
        if np.isnan(overall_score):
            assessment = "❌ INSUFFICIENT DATA"
        elif overall_score >= 0.8:
            assessment = "🌟 EXCELLENT"
        elif overall_score >= 0.6:
            assessment = "✅ GOOD"
        elif overall_score >= 0.4:
            assessment = "⚠️ FAIR"
        else:
            assessment = "❌ POOR"

        print(f"\n🏆 OVERALL ASSESSMENT: {assessment} ({overall_score:.4f})")

        # Provide recommendations if there are issues
        self._provide_recommendations()

    def generate_visualizations(self, save_path: str = "evaluation_plots.png"):
        """Generate comprehensive visualizations."""
        print(f"\n📊 GENERATING VISUALIZATIONS")
        print("=" * 50)

        fig, axes = plt.subplots(2, 3, figsize=(20, 12))
        fig.suptitle("Comprehensive Synthetic Data Evaluation Results", fontsize=16)

        # 1. Category-level bar chart
        if "overall_scores" in self.results:
            scores = self.results["overall_scores"]
            categories = list(scores.keys())
            values = list(scores.values())

            axes[0, 0].bar(
                categories,
                values,
                color=[
                    "#2E86AB",
                    "#A23B72",
                    "#F18F01",
                    "#C73E1D",
                    "#8B5A3C",
                    "#4A90E2",
                ],
            )
            axes[0, 0].set_title("Overall Quality Scores by Category", fontsize=12)
            axes[0, 0].set_ylabel("Score")
            axes[0, 0].tick_params(axis="x", rotation=45)
            axes[0, 0].set_ylim(0, 1)

        # 2. Heatmap of correlation differences
        if "similarity" in self.results and "correlation" in self.results["similarity"]:
            corr_metrics = self.results["similarity"]["correlation"]
            if corr_metrics:
                metric_names = list(corr_metrics.keys())
                metric_values = list(corr_metrics.values())

                # Create heatmap data
                heatmap_data = np.array(metric_values).reshape(1, -1)
                sns.heatmap(
                    heatmap_data,
                    annot=True,
                    fmt=".3f",
                    xticklabels=metric_names,
                    yticklabels=["Correlation"],
                    ax=axes[0, 1],
                    cmap="RdYlBu_r",
                )
                axes[0, 1].set_title("Correlation Similarity Metrics", fontsize=12)

        # 3. ROC Curves (simplified representation)
        if (
            "privacy" in self.results
            and "membership_inference" in self.results["privacy"]
        ):
            membership_auc = self.results["privacy"]["membership_inference"].get(
                "membership_inference_auc", 0.0
            )
            axes[0, 2].bar(
                ["Membership\nInference AUC"], [membership_auc], color="#FF6B6B"
            )
            axes[0, 2].set_title("Privacy Metrics", fontsize=12)
            axes[0, 2].set_ylabel("Score")
            axes[0, 2].set_ylim(0, 1)

        # 4. Utility metrics
        if "utility" in self.results:
            utility_metrics = []
            utility_values = []
            for category, metrics in self.results["utility"].items():
                if isinstance(metrics, dict):
                    for metric_name, value in metrics.items():
                        if isinstance(value, (int, float)):
                            utility_metrics.append(f"{category}_{metric_name}")
                            utility_values.append(value)

            if utility_metrics:
                axes[1, 0].bar(utility_metrics, utility_values, color="#4ECDC4")
                axes[1, 0].set_title("Utility Metrics", fontsize=12)
                axes[1, 0].set_ylabel("Score")
                axes[1, 0].tick_params(axis="x", rotation=45)
                axes[1, 0].set_ylim(0, 1)

        # 5. Detectability metrics
        if (
            "detectability" in self.results
            and "classifier_auc" in self.results["detectability"]
        ):
            detect_metrics = self.results["detectability"]["classifier_auc"]
            if detect_metrics:
                metric_names = list(detect_metrics.keys())
                metric_values = list(detect_metrics.values())

                axes[1, 1].bar(metric_names, metric_values, color="#45B7D1")
                axes[1, 1].set_title("Detectability Metrics", fontsize=12)
                axes[1, 1].set_ylabel("Score")
                axes[1, 1].tick_params(axis="x", rotation=45)
                axes[1, 1].set_ylim(0, 1)

        # 6. Missingness metrics
        if "missingness" in self.results:
            missing_metrics = []
            missing_values = []
            for metric_name, value in self.results["missingness"].items():
                if isinstance(value, (int, float)):
                    missing_metrics.append(metric_name)
                    missing_values.append(value)

            if missing_metrics:
                axes[1, 2].bar(missing_metrics, missing_values, color="#96CEB4")
                axes[1, 2].set_title("Missingness Metrics", fontsize=12)
                axes[1, 2].set_ylabel("Score")
                axes[1, 2].tick_params(axis="x", rotation=45)
                axes[1, 2].set_ylim(0, 1)

        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        plt.show()
        print(f"📊 Visualizations saved to: {save_path}")


# Convenience functions
def evaluate_synthetic_data_comprehensive(
    real_data: pd.DataFrame,
    synthetic_data: pd.DataFrame,
    target_column: Optional[str] = None,
    categorical_columns: Optional[List[str]] = None,
    generate_plots: bool = True,
    save_plots_path: str = "evaluation_plots.png",
) -> Dict:
    """Comprehensive evaluation of synthetic data quality."""
    evaluator = ComprehensiveSyntheticEvaluator(
        real_data, synthetic_data, target_column, categorical_columns
    )

    results = evaluator.comprehensive_evaluation()

    if generate_plots:
        evaluator.generate_visualizations(save_plots_path)

    return results


def evaluate_similarity_metrics(
    real_data: pd.DataFrame, synthetic_data: pd.DataFrame
) -> Dict:
    """Evaluate similarity metrics only."""
    evaluator = ComprehensiveSyntheticEvaluator(real_data, synthetic_data)
    return evaluator.evaluate_similarity_metrics()


def evaluate_utility_metrics(
    real_data: pd.DataFrame, synthetic_data: pd.DataFrame, target_column: str
) -> Dict:
    """Evaluate utility metrics only."""
    evaluator = ComprehensiveSyntheticEvaluator(
        real_data, synthetic_data, target_column
    )
    return evaluator.evaluate_utility_metrics()


def evaluate_privacy_metrics(
    real_data: pd.DataFrame, synthetic_data: pd.DataFrame
) -> Dict:
    """Evaluate privacy metrics only."""
    evaluator = ComprehensiveSyntheticEvaluator(real_data, synthetic_data)
    return evaluator.evaluate_privacy_metrics()


def evaluate_detectability_metrics(
    real_data: pd.DataFrame, synthetic_data: pd.DataFrame
) -> Dict:
    """Evaluate detectability metrics only."""
    evaluator = ComprehensiveSyntheticEvaluator(real_data, synthetic_data)
    return evaluator.evaluate_detectability_metrics()


def evaluate_missingness_metrics(
    real_data: pd.DataFrame, synthetic_data: pd.DataFrame
) -> Dict:
    """Evaluate missingness metrics only."""
    evaluator = ComprehensiveSyntheticEvaluator(real_data, synthetic_data)
    return evaluator.evaluate_missingness_metrics()
