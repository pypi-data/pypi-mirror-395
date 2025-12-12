"""
Utility Metrics for Synthetic Data Evaluation

This module contains all utility-related metrics:
- TSTR: Train on Synthetic, Test on Real
- TRTS: Train on Real, Test on Synthetic
- Prediction Agreement: Percent identical predictions
- Likelihood Leak: Log-likelihood gap between real and synthetic
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (
    mean_squared_error,
    r2_score,
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import warnings
from typing import Dict, List, Tuple, Optional, Union

warnings.filterwarnings("ignore")


class TSTRMetrics:
    """Train on Synthetic, Test on Real metrics."""

    def __init__(
        self, real_data: pd.DataFrame, synthetic_data: pd.DataFrame, target_column: str
    ):
        self.real_data = real_data
        self.synthetic_data = synthetic_data
        self.target_column = target_column
        self.feature_columns = [
            col for col in real_data.columns if col != target_column
        ]

    def tstr_accuracy(self) -> float:
        """TSTR accuracy for classification tasks."""
        if (
            self.target_column not in self.real_data.columns
            or self.target_column not in self.synthetic_data.columns
        ):
            return 0.0

        # Check if it's a classification task
        target_values = self.real_data[self.target_column].dropna()
        if target_values.dtype == "object" or len(target_values.unique()) < 10:
            # Classification task
            X_synth = self.synthetic_data[self.feature_columns].dropna()
            y_synth = self.synthetic_data[self.target_column].dropna()
            X_real = self.real_data[self.feature_columns].dropna()
            y_real = self.real_data[self.target_column].dropna()

            # Align indices
            common_idx = X_synth.index.intersection(y_synth.index)
            X_synth = X_synth.loc[common_idx]
            y_synth = y_synth.loc[common_idx]

            common_idx = X_real.index.intersection(y_real.index)
            X_real = X_real.loc[common_idx]
            y_real = y_real.loc[common_idx]

            if len(X_synth) == 0 or len(X_real) == 0:
                return 0.0

            # Train on synthetic, test on real
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_synth, y_synth)
            y_pred = model.predict(X_real)

            return accuracy_score(y_real, y_pred)
        else:
            return 0.0

    def tstr_r2(self) -> float:
        """TSTR R² for regression tasks."""
        if (
            self.target_column not in self.real_data.columns
            or self.target_column not in self.synthetic_data.columns
        ):
            return 0.0

        # Check if it's a regression task
        target_values = self.real_data[self.target_column].dropna()
        if (
            target_values.dtype in ["int64", "float64"]
            and len(target_values.unique()) >= 10
        ):
            # Regression task
            X_synth = self.synthetic_data[self.feature_columns].dropna()
            y_synth = self.synthetic_data[self.target_column].dropna()
            X_real = self.real_data[self.feature_columns].dropna()
            y_real = self.real_data[self.target_column].dropna()

            # Align indices
            common_idx = X_synth.index.intersection(y_synth.index)
            X_synth = X_synth.loc[common_idx]
            y_synth = y_synth.loc[common_idx]

            common_idx = X_real.index.intersection(y_real.index)
            X_real = X_real.loc[common_idx]
            y_real = y_real.loc[common_idx]

            if len(X_synth) == 0 or len(X_real) == 0:
                return 0.0

            # Train on synthetic, test on real
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_synth, y_synth)
            y_pred = model.predict(X_real)

            return r2_score(y_real, y_pred)
        else:
            return 0.0

    def evaluate_all(self) -> Dict[str, float]:
        """Evaluate all TSTR metrics."""
        return {"tstr_accuracy": self.tstr_accuracy(), "tstr_r2": self.tstr_r2()}


class TRTSMetrics:
    """Train on Real, Test on Synthetic metrics."""

    def __init__(
        self, real_data: pd.DataFrame, synthetic_data: pd.DataFrame, target_column: str
    ):
        self.real_data = real_data
        self.synthetic_data = synthetic_data
        self.target_column = target_column
        self.feature_columns = [
            col for col in real_data.columns if col != target_column
        ]

    def trts_accuracy(self) -> float:
        """TRTS accuracy for classification tasks."""
        if (
            self.target_column not in self.real_data.columns
            or self.target_column not in self.synthetic_data.columns
        ):
            return 0.0

        # Check if it's a classification task
        target_values = self.real_data[self.target_column].dropna()
        if target_values.dtype == "object" or len(target_values.unique()) < 10:
            # Classification task
            X_real = self.real_data[self.feature_columns].dropna()
            y_real = self.real_data[self.target_column].dropna()
            X_synth = self.synthetic_data[self.feature_columns].dropna()
            y_synth = self.synthetic_data[self.target_column].dropna()

            # Align indices
            common_idx = X_real.index.intersection(y_real.index)
            X_real = X_real.loc[common_idx]
            y_real = y_real.loc[common_idx]

            common_idx = X_synth.index.intersection(y_synth.index)
            X_synth = X_synth.loc[common_idx]
            y_synth = y_synth.loc[common_idx]

            if len(X_real) == 0 or len(X_synth) == 0:
                return 0.0

            # Train on real, test on synthetic
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_real, y_real)
            y_pred = model.predict(X_synth)

            return accuracy_score(y_synth, y_pred)
        else:
            return 0.0

    def trts_r2(self) -> float:
        """TRTS R² for regression tasks."""
        if (
            self.target_column not in self.real_data.columns
            or self.target_column not in self.synthetic_data.columns
        ):
            return 0.0

        # Check if it's a regression task
        target_values = self.real_data[self.target_column].dropna()
        if (
            target_values.dtype in ["int64", "float64"]
            and len(target_values.unique()) >= 10
        ):
            # Regression task
            X_real = self.real_data[self.feature_columns].dropna()
            y_real = self.real_data[self.target_column].dropna()
            X_synth = self.synthetic_data[self.feature_columns].dropna()
            y_synth = self.synthetic_data[self.target_column].dropna()

            # Align indices
            common_idx = X_real.index.intersection(y_real.index)
            X_real = X_real.loc[common_idx]
            y_real = y_real.loc[common_idx]

            common_idx = X_synth.index.intersection(y_synth.index)
            X_synth = X_synth.loc[common_idx]
            y_synth = y_synth.loc[common_idx]

            if len(X_real) == 0 or len(X_synth) == 0:
                return 0.0

            # Train on real, test on synthetic
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_real, y_real)
            y_pred = model.predict(X_synth)

            return r2_score(y_synth, y_pred)
        else:
            return 0.0

    def evaluate_all(self) -> Dict[str, float]:
        """Evaluate all TRTS metrics."""
        return {"trts_accuracy": self.trts_accuracy(), "trts_r2": self.trts_r2()}


class PredictionAgreementMetrics:
    """Prediction agreement metrics between models trained on real vs synthetic."""

    def __init__(
        self, real_data: pd.DataFrame, synthetic_data: pd.DataFrame, target_column: str
    ):
        self.real_data = real_data
        self.synthetic_data = synthetic_data
        self.target_column = target_column
        self.feature_columns = [
            col for col in real_data.columns if col != target_column
        ]

    def prediction_agreement_percentage(self) -> float:
        """Percentage of identical predictions between models trained on real vs synthetic."""
        if (
            self.target_column not in self.real_data.columns
            or self.target_column not in self.synthetic_data.columns
        ):
            return 0.0

        # Prepare data
        X_real = self.real_data[self.feature_columns].dropna()
        y_real = self.real_data[self.target_column].dropna()
        X_synth = self.synthetic_data[self.feature_columns].dropna()
        y_synth = self.synthetic_data[self.target_column].dropna()

        # Align indices
        common_idx = X_real.index.intersection(y_real.index)
        X_real = X_real.loc[common_idx]
        y_real = y_real.loc[common_idx]

        common_idx = X_synth.index.intersection(y_synth.index)
        X_synth = X_synth.loc[common_idx]
        y_synth = y_synth.loc[common_idx]

        if len(X_real) == 0 or len(X_synth) == 0:
            return 0.0

        # Check if it's classification or regression
        target_values = self.real_data[self.target_column].dropna()
        is_classification = (
            target_values.dtype == "object" or len(target_values.unique()) < 10
        )

        if is_classification:
            # Classification task
            model_real = RandomForestClassifier(n_estimators=100, random_state=42)
            model_synth = RandomForestClassifier(n_estimators=100, random_state=42)

            model_real.fit(X_real, y_real)
            model_synth.fit(X_synth, y_synth)

            # Get predictions on a common test set
            test_size = min(len(X_real), len(X_synth)) // 4
            if test_size < 10:
                return 0.0

            X_test = X_real.iloc[:test_size]
            pred_real = model_real.predict(X_test)
            pred_synth = model_synth.predict(X_test)

            # Calculate agreement percentage
            agreement = np.mean(pred_real == pred_synth)
            return agreement
        else:
            # Regression task
            model_real = RandomForestRegressor(n_estimators=100, random_state=42)
            model_synth = RandomForestRegressor(n_estimators=100, random_state=42)

            model_real.fit(X_real, y_real)
            model_synth.fit(X_synth, y_synth)

            # Get predictions on a common test set
            test_size = min(len(X_real), len(X_synth)) // 4
            if test_size < 10:
                return 0.0

            X_test = X_real.iloc[:test_size]
            pred_real = model_real.predict(X_test)
            pred_synth = model_synth.predict(X_test)

            # Calculate agreement based on similar predictions (within tolerance)
            tolerance = 0.1 * (y_real.max() - y_real.min())
            agreement = np.mean(np.abs(pred_real - pred_synth) <= tolerance)
            return agreement

    def evaluate_all(self) -> Dict[str, float]:
        """Evaluate all prediction agreement metrics."""
        return {
            "prediction_agreement_percentage": self.prediction_agreement_percentage()
        }


class LikelihoodLeakMetrics:
    """Likelihood leak metrics using SDV models."""

    def __init__(self, real_data: pd.DataFrame, synthetic_data: pd.DataFrame):
        self.real_data = real_data
        self.synthetic_data = synthetic_data

    def likelihood_leak_gap(self) -> float:
        """Log-likelihood gap between real and synthetic using SDV models."""
        try:
            from sdv.single_table import GaussianCopulaSynthesizer
            from sdv.metadata import SingleTableMetadata

            # Create metadata
            metadata = SingleTableMetadata()
            metadata.detect_from_dataframe(data=self.real_data)

            # Fit synthesizer on real data
            synthesizer = GaussianCopulaSynthesizer(metadata)
            synthesizer.fit(self.real_data)

            # Calculate log-likelihood on real data
            real_ll = synthesizer.get_likelihood(self.real_data)

            # Calculate log-likelihood on synthetic data
            synth_ll = synthesizer.get_likelihood(self.synthetic_data)

            # Calculate gap
            ll_gap = abs(real_ll - synth_ll)

            # Normalize to 0-1 scale (lower is better)
            normalized_gap = 1.0 / (1.0 + ll_gap)

            return normalized_gap

        except ImportError:
            print("⚠️ SDV not available. Skipping likelihood leak metrics.")
            return 0.0
        except Exception as e:
            print(f"⚠️ Error calculating likelihood leak: {e}")
            return 0.0

    def evaluate_all(self) -> Dict[str, float]:
        """Evaluate all likelihood leak metrics."""
        return {"likelihood_leak_gap": self.likelihood_leak_gap()}
