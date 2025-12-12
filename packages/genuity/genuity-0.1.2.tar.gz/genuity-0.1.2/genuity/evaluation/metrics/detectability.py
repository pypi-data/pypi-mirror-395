"""
Detectability Metrics for Synthetic Data Evaluation

This module contains all detectability-related metrics:
- Classifier AUC: AUROC, F1-score, Precision, Recall for classifying real vs synthetic
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import warnings
from typing import Dict, List, Tuple, Optional, Union

warnings.filterwarnings("ignore")


class ClassifierAUCMetrics:
    """Classifier-based detectability metrics."""

    def __init__(self, real_data: pd.DataFrame, synthetic_data: pd.DataFrame):
        self.real_data = real_data
        self.synthetic_data = synthetic_data
        self.feature_columns = real_data.columns.tolist()

    def classifier_auc(self) -> float:
        """AUROC for classifying real vs synthetic data."""
        try:
            # Prepare data
            X_real = self.real_data[self.feature_columns].dropna()
            X_synth = self.synthetic_data[self.feature_columns].dropna()

            if len(X_real) == 0 or len(X_synth) == 0:
                return 0.0

            # Create labels (1 for real, 0 for synthetic)
            y_real = np.ones(len(X_real))
            y_synth = np.zeros(len(X_synth))

            # Combine data
            X_combined = pd.concat([X_real, X_synth], ignore_index=True)
            y_combined = np.concatenate([y_real, y_synth])

            # Split into train/test
            X_train, X_test, y_train, y_test = train_test_split(
                X_combined,
                y_combined,
                test_size=0.3,
                random_state=42,
                stratify=y_combined,
            )

            # Train classifier
            classifier = RandomForestClassifier(n_estimators=100, random_state=42)
            classifier.fit(X_train, y_train)

            # Get predictions
            y_pred_proba = classifier.predict_proba(X_test)[:, 1]
            y_pred = classifier.predict(X_test)

            # Calculate AUROC
            auc = roc_auc_score(y_test, y_pred_proba)

            return auc

        except Exception as e:
            print(f"⚠️ Error calculating classifier AUC: {e}")
            return 0.0

    def classifier_f1(self) -> float:
        """F1-score for classifying real vs synthetic data."""
        try:
            # Prepare data
            X_real = self.real_data[self.feature_columns].dropna()
            X_synth = self.synthetic_data[self.feature_columns].dropna()

            if len(X_real) == 0 or len(X_synth) == 0:
                return 0.0

            # Create labels (1 for real, 0 for synthetic)
            y_real = np.ones(len(X_real))
            y_synth = np.zeros(len(X_synth))

            # Combine data
            X_combined = pd.concat([X_real, X_synth], ignore_index=True)
            y_combined = np.concatenate([y_real, y_synth])

            # Split into train/test
            X_train, X_test, y_train, y_test = train_test_split(
                X_combined,
                y_combined,
                test_size=0.3,
                random_state=42,
                stratify=y_combined,
            )

            # Train classifier
            classifier = RandomForestClassifier(n_estimators=100, random_state=42)
            classifier.fit(X_train, y_train)

            # Get predictions
            y_pred = classifier.predict(X_test)

            # Calculate F1-score
            f1 = f1_score(y_test, y_pred)

            return f1

        except Exception as e:
            print(f"⚠️ Error calculating classifier F1: {e}")
            return 0.0

    def classifier_precision(self) -> float:
        """Precision for classifying real vs synthetic data."""
        try:
            # Prepare data
            X_real = self.real_data[self.feature_columns].dropna()
            X_synth = self.synthetic_data[self.feature_columns].dropna()

            if len(X_real) == 0 or len(X_synth) == 0:
                return 0.0

            # Create labels (1 for real, 0 for synthetic)
            y_real = np.ones(len(X_real))
            y_synth = np.zeros(len(X_synth))

            # Combine data
            X_combined = pd.concat([X_real, X_synth], ignore_index=True)
            y_combined = np.concatenate([y_real, y_synth])

            # Split into train/test
            X_train, X_test, y_train, y_test = train_test_split(
                X_combined,
                y_combined,
                test_size=0.3,
                random_state=42,
                stratify=y_combined,
            )

            # Train classifier
            classifier = RandomForestClassifier(n_estimators=100, random_state=42)
            classifier.fit(X_train, y_train)

            # Get predictions
            y_pred = classifier.predict(X_test)

            # Calculate precision
            precision = precision_score(y_test, y_pred)

            return precision

        except Exception as e:
            print(f"⚠️ Error calculating classifier precision: {e}")
            return 0.0

    def classifier_recall(self) -> float:
        """Recall for classifying real vs synthetic data."""
        try:
            # Prepare data
            X_real = self.real_data[self.feature_columns].dropna()
            X_synth = self.synthetic_data[self.feature_columns].dropna()

            if len(X_real) == 0 or len(X_synth) == 0:
                return 0.0

            # Create labels (1 for real, 0 for synthetic)
            y_real = np.ones(len(X_real))
            y_synth = np.zeros(len(X_synth))

            # Combine data
            X_combined = pd.concat([X_real, X_synth], ignore_index=True)
            y_combined = np.concatenate([y_real, y_synth])

            # Split into train/test
            X_train, X_test, y_train, y_test = train_test_split(
                X_combined,
                y_combined,
                test_size=0.3,
                random_state=42,
                stratify=y_combined,
            )

            # Train classifier
            classifier = RandomForestClassifier(n_estimators=100, random_state=42)
            classifier.fit(X_train, y_train)

            # Get predictions
            y_pred = classifier.predict(X_test)

            # Calculate recall
            recall = recall_score(y_test, y_pred)

            return recall

        except Exception as e:
            print(f"⚠️ Error calculating classifier recall: {e}")
            return 0.0

    def evaluate_all(self) -> Dict[str, float]:
        """Evaluate all classifier detectability metrics."""
        return {
            "classifier_auc": self.classifier_auc(),
            "classifier_f1": self.classifier_f1(),
            "classifier_precision": self.classifier_precision(),
            "classifier_recall": self.classifier_recall(),
        }
