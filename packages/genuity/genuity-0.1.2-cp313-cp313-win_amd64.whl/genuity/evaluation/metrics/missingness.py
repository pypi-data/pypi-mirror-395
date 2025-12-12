"""
Missingness Metrics for Synthetic Data Evaluation

This module contains all missingness-related metrics:
- Missing Rate Similarity: Per-column missing rate similarity
- Missing Pattern Chi-Square: Missingness-pattern chi-square test
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import chi2_contingency
import warnings
from typing import Dict, List, Tuple, Optional, Union

warnings.filterwarnings("ignore")


class MissingnessPatternMetrics:
    """Missingness pattern metrics for synthetic data evaluation."""

    def __init__(self, real_data: pd.DataFrame, synthetic_data: pd.DataFrame):
        self.real_data = real_data
        self.synthetic_data = synthetic_data
        self.feature_columns = real_data.columns.tolist()

    def missing_rate_similarity(self) -> Dict[str, float]:
        """Per-column missing rate similarity between real and synthetic data."""
        results = {}

        for col in self.feature_columns:
            if col in self.real_data.columns and col in self.synthetic_data.columns:
                # Calculate missing rates
                real_missing_rate = self.real_data[col].isna().mean()
                synth_missing_rate = self.synthetic_data[col].isna().mean()

                # Calculate similarity (1 - absolute difference)
                similarity = 1.0 - abs(real_missing_rate - synth_missing_rate)
                results[f"missing_rate_similarity_{col}"] = max(0.0, similarity)

        return results

    def missing_pattern_chi_square(self) -> float:
        """Chi-square test for missingness patterns between real and synthetic data."""
        try:
            # Create missingness indicator matrices
            real_missing = self.real_data.isna().astype(int)
            synth_missing = self.synthetic_data.isna().astype(int)

            # Calculate missingness patterns (combinations of missing values)
            real_patterns = real_missing.apply(tuple, axis=1).value_counts()
            synth_patterns = synth_missing.apply(tuple, axis=1).value_counts()

            # Get all unique patterns
            all_patterns = set(real_patterns.index) | set(synth_patterns.index)

            # Create contingency table
            contingency_data = []
            for pattern in all_patterns:
                real_count = real_patterns.get(pattern, 0)
                synth_count = synth_patterns.get(pattern, 0)
                contingency_data.append([real_count, synth_count])

            if len(contingency_data) < 2:
                return 0.0

            # Perform chi-square test
            chi2_stat, p_value, _, _ = chi2_contingency(contingency_data)

            # Convert to similarity score (higher p-value = more similar)
            # Use log scale to handle very small p-values
            similarity = 1.0 / (1.0 - np.log10(max(p_value, 1e-10)))

            return min(1.0, max(0.0, similarity))

        except Exception as e:
            print(f"⚠️ Error calculating missing pattern chi-square: {e}")
            return 0.0

    def overall_missing_similarity(self) -> float:
        """Overall missingness similarity score."""
        # Calculate average missing rate similarity
        missing_rate_sims = self.missing_rate_similarity()
        avg_missing_rate_sim = (
            np.mean(list(missing_rate_sims.values())) if missing_rate_sims else 0.0
        )

        # Get pattern similarity
        pattern_sim = self.missing_pattern_chi_square()

        # Combine scores (equal weight)
        overall_sim = (avg_missing_rate_sim + pattern_sim) / 2.0

        return overall_sim

    def missing_pattern_distribution(self) -> Dict[str, float]:
        """Distribution of missing patterns in real vs synthetic data."""
        try:
            # Create missingness indicator matrices
            real_missing = self.real_data.isna().astype(int)
            synth_missing = self.synthetic_data.isna().astype(int)

            # Calculate pattern distributions
            real_patterns = real_missing.apply(tuple, axis=1).value_counts(
                normalize=True
            )
            synth_patterns = synth_missing.apply(tuple, axis=1).value_counts(
                normalize=True
            )

            # Get all unique patterns
            all_patterns = set(real_patterns.index) | set(synth_patterns.index)

            # Calculate distribution similarity for each pattern
            similarities = []
            for pattern in all_patterns:
                real_prob = real_patterns.get(pattern, 0.0)
                synth_prob = synth_patterns.get(pattern, 0.0)

                # Calculate similarity (1 - absolute difference)
                similarity = 1.0 - abs(real_prob - synth_prob)
                similarities.append(similarity)

            return {
                "pattern_distribution_similarity": (
                    np.mean(similarities) if similarities else 0.0
                ),
                "unique_patterns_real": len(real_patterns),
                "unique_patterns_synthetic": len(synth_patterns),
                "total_patterns": len(all_patterns),
            }

        except Exception as e:
            print(f"⚠️ Error calculating missing pattern distribution: {e}")
            return {
                "pattern_distribution_similarity": 0.0,
                "unique_patterns_real": 0,
                "unique_patterns_synthetic": 0,
                "total_patterns": 0,
            }

    def evaluate_all(self) -> Dict[str, Union[Dict[str, float], float]]:
        """Evaluate all missingness pattern metrics."""
        return {
            "missing_rate_similarity": self.missing_rate_similarity(),
            "missing_pattern_chi_square": self.missing_pattern_chi_square(),
            "overall_missing_similarity": self.overall_missing_similarity(),
            "missing_pattern_distribution": self.missing_pattern_distribution(),
        }
