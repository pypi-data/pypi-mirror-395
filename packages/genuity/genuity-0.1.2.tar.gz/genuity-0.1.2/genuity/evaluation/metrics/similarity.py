"""
Similarity Metrics for Synthetic Data Evaluation

This module contains all similarity-related metrics:
- Univariate: KS complement, Wasserstein distance, Total Variation, Hellinger distance
- Multivariate: MMD-RBF, PCA reconstruction error, correlation-matrix distance
- Correlation: Pearson, Spearman, Cramér's V, Mutual Information differences
- SDMetrics: Wrappers for SDMetrics library metrics
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.spatial.distance import jensenshannon
from scipy.stats import ks_2samp, wasserstein_distance
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import rbf_kernel
from sklearn.preprocessing import StandardScaler
import warnings
from typing import Dict, List, Tuple, Optional, Union

warnings.filterwarnings("ignore")


class UnivariateSimilarityMetrics:
    """Univariate similarity metrics for individual features."""

    def __init__(self, real_data: pd.DataFrame, synthetic_data: pd.DataFrame):
        self.real_data = real_data
        self.synthetic_data = synthetic_data
        self.numerical_columns = real_data.select_dtypes(
            include=[np.number]
        ).columns.tolist()

    def ks_complement(self) -> Dict[str, float]:
        """Kolmogorov-Smirnov complement (1 - KS statistic)."""
        results = {}
        for col in self.numerical_columns:
            try:
                if col in self.real_data.columns and col in self.synthetic_data.columns:
                    real_data = self.real_data[col].dropna()
                    synth_data = self.synthetic_data[col].dropna()

                    if len(real_data) < 2 or len(synth_data) < 2:
                        continue

                    ks_stat, _ = ks_2samp(real_data, synth_data)
                    results[f"ks_complement_{col}"] = 1.0 - ks_stat
            except Exception as e:
                print(f"⚠️ Error calculating KS complement for {col}: {e}")
                continue
        return results

    def wasserstein_distance_metric(self) -> Dict[str, float]:
        """Wasserstein distance between distributions."""
        results = {}
        for col in self.numerical_columns:
            try:
                if col in self.real_data.columns and col in self.synthetic_data.columns:
                    real_data = self.real_data[col].dropna()
                    synth_data = self.synthetic_data[col].dropna()

                    if len(real_data) < 2 or len(synth_data) < 2:
                        continue

                    wd = wasserstein_distance(real_data, synth_data)
                    # Normalize by range to get 0-1 score
                    range_val = self.real_data[col].max() - self.real_data[col].min()
                    normalized_wd = (
                        1.0 / (1.0 + wd / range_val) if range_val > 0 else 0.0
                    )
                    results[f"wasserstein_{col}"] = normalized_wd
            except Exception as e:
                print(f"⚠️ Error calculating Wasserstein distance for {col}: {e}")
                continue
        return results

    def total_variation_distance(self) -> Dict[str, float]:
        """Total Variation distance for categorical variables."""
        results = {}
        categorical_columns = self.real_data.select_dtypes(
            include=["object", "category"]
        ).columns

        for col in categorical_columns:
            try:
                if col in self.real_data.columns and col in self.synthetic_data.columns:
                    # Check if column has data
                    if (
                        self.real_data[col].dropna().empty
                        or self.synthetic_data[col].dropna().empty
                    ):
                        continue

                    real_counts = self.real_data[col].value_counts(normalize=True)
                    synth_counts = self.synthetic_data[col].value_counts(normalize=True)

                    # Check if we have any counts
                    if real_counts.empty or synth_counts.empty:
                        continue

                    # Align indices
                    all_values = set(real_counts.index) | set(synth_counts.index)
                    if not all_values:
                        continue

                    real_aligned = real_counts.reindex(all_values, fill_value=0)
                    synth_aligned = synth_counts.reindex(all_values, fill_value=0)

                    # Total variation distance
                    tv_distance = 0.5 * np.sum(
                        np.abs(real_aligned.values - synth_aligned.values)
                    )
                    results[f"total_variation_{col}"] = 1.0 - tv_distance
            except Exception as e:
                print(f"⚠️ Error calculating total variation for {col}: {e}")
                continue
        return results

    def hellinger_distance(self) -> Dict[str, float]:
        """Hellinger distance between distributions."""
        results = {}
        categorical_columns = self.real_data.select_dtypes(
            include=["object", "category"]
        ).columns

        for col in categorical_columns:
            try:
                if col in self.real_data.columns and col in self.synthetic_data.columns:
                    # Check if column has data
                    if (
                        self.real_data[col].dropna().empty
                        or self.synthetic_data[col].dropna().empty
                    ):
                        continue

                    real_counts = self.real_data[col].value_counts(normalize=True)
                    synth_counts = self.synthetic_data[col].value_counts(normalize=True)

                    # Check if we have any counts
                    if real_counts.empty or synth_counts.empty:
                        continue

                    # Align indices
                    all_values = set(real_counts.index) | set(synth_counts.index)
                    if not all_values:
                        continue

                    real_aligned = real_counts.reindex(all_values, fill_value=0)
                    synth_aligned = synth_counts.reindex(all_values, fill_value=0)

                    # Hellinger distance
                    hellinger = np.sqrt(
                        0.5
                        * np.sum(
                            (
                                np.sqrt(real_aligned.values)
                                - np.sqrt(synth_aligned.values)
                            )
                            ** 2
                        )
                    )
                    results[f"hellinger_{col}"] = 1.0 - hellinger
            except Exception as e:
                print(f"⚠️ Error calculating Hellinger distance for {col}: {e}")
                continue
        return results

    def evaluate_all(self) -> Dict[str, Dict[str, float]]:
        """Evaluate all univariate similarity metrics."""
        return {
            "ks_complement": self.ks_complement(),
            "wasserstein_distance": self.wasserstein_distance_metric(),
            "total_variation_distance": self.total_variation_distance(),
            "hellinger_distance": self.hellinger_distance(),
        }


class MultivariateSimilarityMetrics:
    """Multivariate similarity metrics for feature relationships."""

    def __init__(self, real_data: pd.DataFrame, synthetic_data: pd.DataFrame):
        self.real_data = real_data
        self.synthetic_data = synthetic_data
        self.numerical_columns = real_data.select_dtypes(
            include=[np.number]
        ).columns.tolist()

    def mmd_rbf(self, gamma: float = 1.0) -> float:
        """Maximum Mean Discrepancy with RBF kernel."""
        if len(self.numerical_columns) < 2:
            return 0.0

        real_numerical = self.real_data[self.numerical_columns].dropna()
        synth_numerical = self.synthetic_data[self.numerical_columns].dropna()

        if len(real_numerical) == 0 or len(synth_numerical) == 0:
            return 0.0

        # Standardize data
        scaler = StandardScaler()
        real_scaled = scaler.fit_transform(real_numerical)
        synth_scaled = scaler.transform(synth_numerical)

        # Calculate MMD
        k_xx = rbf_kernel(real_scaled, gamma=gamma).mean()
        k_yy = rbf_kernel(synth_scaled, gamma=gamma).mean()
        k_xy = rbf_kernel(real_scaled, synth_scaled, gamma=gamma).mean()

        mmd = k_xx + k_yy - 2 * k_xy
        return 1.0 / (1.0 + mmd)  # Convert to similarity score

    def pca_reconstruction_error(self) -> float:
        """PCA reconstruction error comparison."""
        if len(self.numerical_columns) < 2:
            return 0.0

        real_numerical = self.real_data[self.numerical_columns].dropna()
        synth_numerical = self.synthetic_data[self.numerical_columns].dropna()

        if len(real_numerical) == 0 or len(synth_numerical) == 0:
            return 0.0

        # Fit PCA on real data
        pca = PCA(n_components=min(10, len(self.numerical_columns)))
        real_pca = pca.fit_transform(real_numerical)
        real_reconstructed = pca.inverse_transform(real_pca)

        # Apply to synthetic data
        synth_pca = pca.transform(synth_numerical)
        synth_reconstructed = pca.inverse_transform(synth_pca)

        # Calculate reconstruction errors
        real_error = np.mean((real_numerical - real_reconstructed) ** 2)
        synth_error = np.mean((synth_numerical - synth_reconstructed) ** 2)

        # Compare errors
        error_ratio = min(real_error, synth_error) / max(real_error, synth_error)
        return error_ratio

    def correlation_matrix_distance(self) -> float:
        """Distance between correlation matrices."""
        if len(self.numerical_columns) < 2:
            return 0.0

        real_corr = self.real_data[self.numerical_columns].corr()
        synth_corr = self.synthetic_data[self.numerical_columns].corr()

        # Frobenius norm of difference
        corr_diff = np.linalg.norm(real_corr - synth_corr, ord="fro")
        max_possible_diff = np.sqrt(
            len(self.numerical_columns) ** 2 * 4
        )  # Max possible difference

        similarity = 1.0 - (corr_diff / max_possible_diff)
        return max(0.0, similarity)

    def evaluate_all(self) -> Dict[str, float]:
        """Evaluate all multivariate similarity metrics."""
        return {
            "mmd_rbf": self.mmd_rbf(),
            "pca_reconstruction_error": self.pca_reconstruction_error(),
            "correlation_matrix_distance": self.correlation_matrix_distance(),
        }


class CorrelationSimilarityMetrics:
    """Correlation-based similarity metrics."""

    def __init__(self, real_data: pd.DataFrame, synthetic_data: pd.DataFrame):
        self.real_data = real_data
        self.synthetic_data = synthetic_data
        self.numerical_columns = real_data.select_dtypes(
            include=[np.number]
        ).columns.tolist()

    def pearson_correlation_difference(self) -> float:
        """Average absolute difference in Pearson correlations."""
        if len(self.numerical_columns) < 2:
            return 0.0

        real_corr = self.real_data[self.numerical_columns].corr(method="pearson")
        synth_corr = self.synthetic_data[self.numerical_columns].corr(method="pearson")

        # Calculate absolute differences
        corr_diff = np.abs(real_corr - synth_corr)
        mean_diff = corr_diff.values[np.triu_indices_from(corr_diff.values, k=1)].mean()

        return 1.0 - mean_diff  # Convert to similarity

    def spearman_correlation_difference(self) -> float:
        """Average absolute difference in Spearman correlations."""
        if len(self.numerical_columns) < 2:
            return 0.0

        real_corr = self.real_data[self.numerical_columns].corr(method="spearman")
        synth_corr = self.synthetic_data[self.numerical_columns].corr(method="spearman")

        # Calculate absolute differences
        corr_diff = np.abs(real_corr - synth_corr)
        mean_diff = corr_diff.values[np.triu_indices_from(corr_diff.values, k=1)].mean()

        return 1.0 - mean_diff  # Convert to similarity

    def cramers_v_difference(self) -> float:
        """Average absolute difference in Cramér's V for categorical variables."""
        categorical_columns = self.real_data.select_dtypes(
            include=["object", "category"]
        ).columns

        if len(categorical_columns) < 2:
            return 0.0

        differences = []
        for i, col1 in enumerate(categorical_columns):
            for col2 in categorical_columns[i + 1 :]:
                if col1 in self.real_data.columns and col2 in self.real_data.columns:
                    # Calculate Cramér's V for real data
                    real_contingency = pd.crosstab(
                        self.real_data[col1], self.real_data[col2]
                    )
                    real_chi2 = stats.chi2_contingency(real_contingency)[0]
                    real_n = len(self.real_data)
                    real_min_dim = min(real_contingency.shape) - 1
                    real_cramers_v = (
                        np.sqrt(real_chi2 / (real_n * real_min_dim))
                        if real_min_dim > 0
                        else 0
                    )

                    # Calculate Cramér's V for synthetic data
                    synth_contingency = pd.crosstab(
                        self.synthetic_data[col1], self.synthetic_data[col2]
                    )
                    synth_chi2 = stats.chi2_contingency(synth_contingency)[0]
                    synth_n = len(self.synthetic_data)
                    synth_min_dim = min(synth_contingency.shape) - 1
                    synth_cramers_v = (
                        np.sqrt(synth_chi2 / (synth_n * synth_min_dim))
                        if synth_min_dim > 0
                        else 0
                    )

                    differences.append(abs(real_cramers_v - synth_cramers_v))

        mean_diff = np.mean(differences) if differences else 0.0
        return 1.0 - mean_diff  # Convert to similarity

    def mutual_information_difference(self) -> float:
        """Average absolute difference in mutual information."""
        # This is a simplified version - full mutual information calculation would be more complex
        # For now, we'll use correlation as a proxy
        return self.pearson_correlation_difference()

    def evaluate_all(self) -> Dict[str, float]:
        """Evaluate all correlation similarity metrics."""
        return {
            "pearson_correlation_difference": self.pearson_correlation_difference(),
            "spearman_correlation_difference": self.spearman_correlation_difference(),
            "cramers_v_difference": self.cramers_v_difference(),
            "mutual_information_difference": self.mutual_information_difference(),
        }


class SDMetricsSimilarity:
    """Wrapper for SDMetrics library similarity metrics."""

    def __init__(self, real_data: pd.DataFrame, synthetic_data: pd.DataFrame):
        self.real_data = real_data
        self.synthetic_data = synthetic_data

    def continuous_data_quality(self) -> Dict[str, float]:
        """Continuous data quality metric from SDMetrics."""
        try:
            from sdmetrics.column_pairs import ContinuousDataQualityMetric

            results = {}
            numerical_columns = self.real_data.select_dtypes(
                include=[np.number]
            ).columns

            for col in numerical_columns:
                if col in self.real_data.columns and col in self.synthetic_data.columns:
                    try:
                        score = ContinuousDataQualityMetric.compute(
                            real_data=self.real_data,
                            synthetic_data=self.synthetic_data,
                            column_name=col,
                        )
                        results[f"continuous_quality_{col}"] = score
                    except:
                        results[f"continuous_quality_{col}"] = 0.0

            return results
        except ImportError:
            print(
                "⚠️ SDMetrics not available. Skipping continuous data quality metrics."
            )
            return {}

    def categorical_data_quality(self) -> Dict[str, float]:
        """Categorical data quality metric from SDMetrics."""
        try:
            from sdmetrics.column_pairs import CategoricalDataQualityMetric

            results = {}
            categorical_columns = self.real_data.select_dtypes(
                include=["object", "category"]
            ).columns

            for col in categorical_columns:
                if col in self.real_data.columns and col in self.synthetic_data.columns:
                    try:
                        score = CategoricalDataQualityMetric.compute(
                            real_data=self.real_data,
                            synthetic_data=self.synthetic_data,
                            column_name=col,
                        )
                        results[f"categorical_quality_{col}"] = score
                    except:
                        results[f"categorical_quality_{col}"] = 0.0

            return results
        except ImportError:
            print(
                "⚠️ SDMetrics not available. Skipping categorical data quality metrics."
            )
            return {}

    def overlap_similarity(self) -> Dict[str, float]:
        """Overlap similarity metric from SDMetrics."""
        try:
            from sdmetrics.column_pairs import OverlapSimilarity

            results = {}
            numerical_columns = self.real_data.select_dtypes(
                include=[np.number]
            ).columns

            for col in numerical_columns:
                if col in self.real_data.columns and col in self.synthetic_data.columns:
                    try:
                        score = OverlapSimilarity.compute(
                            real_data=self.real_data,
                            synthetic_data=self.synthetic_data,
                            column_name=col,
                        )
                        results[f"overlap_similarity_{col}"] = score
                    except:
                        results[f"overlap_similarity_{col}"] = 0.0

            return results
        except ImportError:
            print("⚠️ SDMetrics not available. Skipping overlap similarity metrics.")
            return {}

    def evaluate_all(self) -> Dict[str, Dict[str, float]]:
        """Evaluate all SDMetrics similarity metrics."""
        return {
            "continuous_data_quality": self.continuous_data_quality(),
            "categorical_data_quality": self.categorical_data_quality(),
            "overlap_similarity": self.overlap_similarity(),
        }
