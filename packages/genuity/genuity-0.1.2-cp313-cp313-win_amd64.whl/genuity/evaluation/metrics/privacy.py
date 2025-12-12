"""
Privacy Metrics for Synthetic Data Evaluation

This module contains all privacy-related metrics:
- Membership Inference: ROC-AUC for membership inference attack
- Attribute Inference: Accuracy for attribute inference
- Nearest Neighbor: DCR, NNDR, Privacy loss percentage
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, accuracy_score
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import warnings
from typing import Dict, List, Tuple, Optional, Union

warnings.filterwarnings("ignore")


class MembershipInferenceMetrics:
    """Membership inference attack metrics."""

    def __init__(self, real_data: pd.DataFrame, synthetic_data: pd.DataFrame):
        self.real_data = real_data
        self.synthetic_data = synthetic_data
        self.feature_columns = real_data.columns.tolist()

    def membership_inference_auc(self) -> float:
        """ROC-AUC for membership inference attack."""
        try:
            # Prepare data
            X_real = self.real_data[self.feature_columns].dropna()
            X_synth = self.synthetic_data[self.feature_columns].dropna()

            if len(X_real) == 0 or len(X_synth) == 0:
                return 0.0

            # Create membership labels (1 for real, 0 for synthetic)
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

            # Train membership inference classifier
            classifier = RandomForestClassifier(n_estimators=100, random_state=42)
            classifier.fit(X_train, y_train)

            # Get predictions
            y_pred_proba = classifier.predict_proba(X_test)[:, 1]

            # Calculate ROC-AUC
            auc = roc_auc_score(y_test, y_pred_proba)

            # Return privacy score (lower AUC is better for privacy)
            privacy_score = 1.0 - auc
            return privacy_score

        except Exception as e:
            print(f"⚠️ Error calculating membership inference AUC: {e}")
            return 0.0

    def evaluate_all(self) -> Dict[str, float]:
        """Evaluate all membership inference metrics."""
        return {"membership_inference_auc": self.membership_inference_auc()}


class AttributeInferenceMetrics:
    """Attribute inference attack metrics."""

    def __init__(self, real_data: pd.DataFrame, synthetic_data: pd.DataFrame):
        self.real_data = real_data
        self.synthetic_data = synthetic_data
        self.feature_columns = real_data.columns.tolist()

    def attribute_inference_accuracy(self, target_attribute: str) -> float:
        """Accuracy for attribute inference attack on a specific attribute."""
        if target_attribute not in self.feature_columns:
            return 0.0

        try:
            # Prepare data
            feature_cols = [
                col for col in self.feature_columns if col != target_attribute
            ]
            if len(feature_cols) == 0:
                return 0.0

            X_real = self.real_data[feature_cols].dropna()
            y_real = self.real_data[target_attribute].dropna()

            # Align indices
            common_idx = X_real.index.intersection(y_real.index)
            X_real = X_real.loc[common_idx]
            y_real = y_real.loc[common_idx]

            if len(X_real) == 0:
                return 0.0

            # Split into train/test
            X_train, X_test, y_train, y_test = train_test_split(
                X_real, y_real, test_size=0.3, random_state=42, stratify=y_real
            )

            # Train attribute inference classifier
            classifier = RandomForestClassifier(n_estimators=100, random_state=42)
            classifier.fit(X_train, y_train)

            # Get predictions
            y_pred = classifier.predict(X_test)

            # Calculate accuracy
            accuracy = accuracy_score(y_test, y_pred)

            # Return privacy score (lower accuracy is better for privacy)
            privacy_score = 1.0 - accuracy
            return privacy_score

        except Exception as e:
            print(f"⚠️ Error calculating attribute inference accuracy: {e}")
            return 0.0

    def average_attribute_inference_accuracy(self) -> float:
        """Average attribute inference accuracy across all attributes."""
        accuracies = []

        for col in self.feature_columns:
            if col in self.real_data.columns and col in self.synthetic_data.columns:
                acc = self.attribute_inference_accuracy(col)
                accuracies.append(acc)

        return np.mean(accuracies) if accuracies else 0.0

    def evaluate_all(self) -> Dict[str, float]:
        """Evaluate all attribute inference metrics."""
        return {
            "average_attribute_inference_accuracy": self.average_attribute_inference_accuracy()
        }


class NearestNeighborMetrics:
    """Nearest neighbor privacy metrics."""

    def __init__(self, real_data: pd.DataFrame, synthetic_data: pd.DataFrame):
        self.real_data = real_data
        self.synthetic_data = synthetic_data
        self.numerical_columns = real_data.select_dtypes(
            include=[np.number]
        ).columns.tolist()

    def distance_to_closest_record(self) -> float:
        """Distance to Closest Record (DCR) metric."""
        if len(self.numerical_columns) == 0:
            return 0.0

        try:
            # Prepare numerical data
            real_numerical = self.real_data[self.numerical_columns].dropna()
            synth_numerical = self.synthetic_data[self.numerical_columns].dropna()

            if len(real_numerical) == 0 or len(synth_numerical) == 0:
                return 0.0

            # Standardize data
            scaler = StandardScaler()
            real_scaled = scaler.fit_transform(real_numerical)
            synth_scaled = scaler.transform(synth_numerical)

            # Find nearest neighbors
            nn = NearestNeighbors(n_neighbors=1)
            nn.fit(real_scaled)

            # Calculate distances from synthetic to real
            distances, _ = nn.kneighbors(synth_scaled)

            # Calculate average distance
            avg_distance = np.mean(distances)

            # Normalize to 0-1 scale (higher distance is better for privacy)
            # Use exponential decay to normalize
            normalized_distance = 1.0 - np.exp(-avg_distance)

            return normalized_distance

        except Exception as e:
            print(f"⚠️ Error calculating DCR: {e}")
            return 0.0

    def nearest_neighbor_distance_ratio(self) -> float:
        """Nearest Neighbor Distance Ratio (NNDR) metric."""
        if len(self.numerical_columns) == 0:
            return 0.0

        try:
            # Prepare numerical data
            real_numerical = self.real_data[self.numerical_columns].dropna()
            synth_numerical = self.synthetic_data[self.numerical_columns].dropna()

            if len(real_numerical) == 0 or len(synth_numerical) == 0:
                return 0.0

            # Standardize data
            scaler = StandardScaler()
            real_scaled = scaler.fit_transform(real_numerical)
            synth_scaled = scaler.transform(synth_numerical)

            # Find nearest neighbors
            nn = NearestNeighbors(n_neighbors=2)
            nn.fit(real_scaled)

            # Calculate distances from synthetic to real
            distances, _ = nn.kneighbors(synth_scaled)

            # Calculate NNDR (ratio of 2nd nearest to 1st nearest)
            nnr = distances[:, 1] / (
                distances[:, 0] + 1e-8
            )  # Add small epsilon to avoid division by zero

            # Calculate average NNDR
            avg_nnr = np.mean(nnr)

            # Normalize to 0-1 scale (higher ratio is better for privacy)
            normalized_nnr = 1.0 - np.exp(-avg_nnr)

            return normalized_nnr

        except Exception as e:
            print(f"⚠️ Error calculating NNDR: {e}")
            return 0.0

    def privacy_loss_percentage(self) -> float:
        """Privacy loss percentage based on nearest neighbor analysis."""
        if len(self.numerical_columns) == 0:
            return 0.0

        try:
            # Prepare numerical data
            real_numerical = self.real_data[self.numerical_columns].dropna()
            synth_numerical = self.synthetic_data[self.numerical_columns].dropna()

            if len(real_numerical) == 0 or len(synth_numerical) == 0:
                return 0.0

            # Standardize data
            scaler = StandardScaler()
            real_scaled = scaler.fit_transform(real_numerical)
            synth_scaled = scaler.transform(synth_numerical)

            # Find nearest neighbors
            nn = NearestNeighbors(n_neighbors=1)
            nn.fit(real_scaled)

            # Calculate distances from synthetic to real
            distances, _ = nn.kneighbors(synth_scaled)

            # Define threshold for privacy loss (e.g., distance < 0.1)
            threshold = 0.1
            privacy_loss_count = np.sum(distances < threshold)
            privacy_loss_percentage = (privacy_loss_count / len(distances)) * 100

            # Convert to privacy score (lower percentage is better)
            privacy_score = 1.0 - (privacy_loss_percentage / 100.0)

            return privacy_score

        except Exception as e:
            print(f"⚠️ Error calculating privacy loss percentage: {e}")
            return 0.0

    def evaluate_all(self) -> Dict[str, float]:
        """Evaluate all nearest neighbor privacy metrics."""
        return {
            "distance_to_closest_record": self.distance_to_closest_record(),
            "nearest_neighbor_distance_ratio": self.nearest_neighbor_distance_ratio(),
            "privacy_loss_percentage": self.privacy_loss_percentage(),
        }
