import numpy as np
import pandas as pd
from sklearn.ensemble import (
    HistGradientBoostingClassifier,
    HistGradientBoostingRegressor,
)
from sklearn.preprocessing import LabelEncoder


class SingleColumnPredictor:
    def __init__(self, column_name, column_type, config):
        """
        Initialize single column predictor

        Args:
            column_name: Name of the column to predict
            column_type: Type of the column ('categorical' or 'continuous')
            config: MaskedPredictorConfig instance
        """
        self.column_name = column_name
        self.column_type = column_type
        self.config = config
        self.model = None
        self.label_encoder = None

    def _encode_categorical_features(self, X):
        """
        Encode categorical features in the input data

        Args:
            X: Input DataFrame

        Returns:
            Encoded DataFrame
        """
        X_encoded = X.copy()

        for col in X.columns:
            if not pd.api.types.is_numeric_dtype(X[col]):
                # Encode categorical columns
                le = LabelEncoder()
                X_encoded[col] = le.fit_transform(X[col].astype(str))

        return X_encoded

    def fit(self, X, y):
        """
        Fit the predictor model

        Args:
            X: Feature matrix
            y: Target values
        """
        try:
            # Encode categorical features
            X_encoded = self._encode_categorical_features(X)

            if self.column_type == "categorical":
                self.model = HistGradientBoostingClassifier(
                    random_state=self.config.random_state
                )
                # Encode target for classification
                self.label_encoder = LabelEncoder()
                y_encoded = self.label_encoder.fit_transform(y.astype(str))
            else:
                self.model = HistGradientBoostingRegressor(
                    random_state=self.config.random_state
                )
                y_encoded = y

            self.model.fit(X_encoded, y_encoded)

        except ValueError as e:
            # Handle wrong model chosen
            if "Unknown label type: continuous" in str(e):
                print(
                    f"[WARN] Misclassified column '{y.name}' as categorical. Switching to regressor."
                )
                self.column_type = "continuous"
                self.model = HistGradientBoostingRegressor(
                    random_state=self.config.random_state
                )
                self.model.fit(X_encoded, y)
            else:
                raise e  # if it's another ValueError, re-raise it

    def predict(self, X):
        """
        Predict values for the given features

        Args:
            X: Feature matrix

        Returns:
            Predicted values
        """
        # Encode categorical features
        X_encoded = self._encode_categorical_features(X)

        # Get predictions
        predictions = self.model.predict(X_encoded)

        # Decode predictions if categorical
        if self.column_type == "categorical" and self.label_encoder is not None:
            predictions = self.label_encoder.inverse_transform(predictions)

        return predictions
