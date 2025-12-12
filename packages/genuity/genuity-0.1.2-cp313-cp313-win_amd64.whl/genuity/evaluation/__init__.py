#!/usr/bin/env python3
"""
Comprehensive Evaluation Framework for Synthetic Data Generation

This module provides a complete evaluation suite for assessing synthetic data quality
across multiple dimensions: similarity, utility, privacy, detectability, and missingness.

Available Functions:
- evaluate_synthetic_data_comprehensive(): Complete evaluation with all metrics
- evaluate_similarity_metrics(): Statistical similarity measures
- evaluate_utility_metrics(): Data utility assessment
- evaluate_privacy_metrics(): Privacy preservation evaluation
- evaluate_detectability_metrics(): Synthetic data detection
- evaluate_missingness_metrics(): Missing value pattern analysis
- generate_evaluation_report(): Generate comprehensive PDF report
- plot_evaluation_results(): Create visualization plots

Legacy Functions (for backward compatibility):
- evaluate_pre_post_processing(): Simple evaluation with auto-detection
- smart_dataframe_comparison(): Smart comparison with method selection
- evaluate_pre_post_dataframes(): Comprehensive evaluation
"""

from .evaluate_synthetic_data import evaluate_pre_post_processing
from .smart_comparison import smart_dataframe_comparison
from .synthetic_evaluation import evaluate_pre_post_dataframes
from .comprehensive_evaluator import (
    ComprehensiveSyntheticEvaluator,
    evaluate_synthetic_data_comprehensive,
    evaluate_similarity_metrics,
    evaluate_utility_metrics,
    evaluate_privacy_metrics,
    evaluate_detectability_metrics,
    evaluate_missingness_metrics,
)


__version__ = "0.1.1"
__author__ = "Genuity IO"

__all__ = [
    # Legacy functions (for backward compatibility)
    "evaluate_pre_post_processing",
    "smart_dataframe_comparison",
    "evaluate_pre_post_dataframes",
    # Comprehensive evaluation framework
    "ComprehensiveSyntheticEvaluator",
    "evaluate_synthetic_data_comprehensive",
    "evaluate_similarity_metrics",
    "evaluate_utility_metrics",
    "evaluate_privacy_metrics",
    "evaluate_detectability_metrics",
    "evaluate_missingness_metrics",
]

# Silenced verbose import messages - functionality unchanged
# print("Evaluation Framework Loaded Successfully!")
# print("Available functions:")
# print("  - evaluate_synthetic_data_comprehensive(real_data, synthetic_data, categorical_columns=None)")
# print("  - evaluate_pre_post_processing(pre_df, post_df, target_column=None)")
# print("  - evaluate_pre_post_dataframes(pre_df, post_df, target_column=None)")
# print("  - evaluate_dataframe_comparison(pre_df, post_df, target_column=None)")
# print("  - compare_dataframes(pre_df, post_df, target_column=None)")
# print("See README.md for detailed usage")
# print("  Note: target_column is optional - framework will auto-detect or you can specify")
# print("Comprehensive evaluation with 29+ metrics across 5 categories!")
