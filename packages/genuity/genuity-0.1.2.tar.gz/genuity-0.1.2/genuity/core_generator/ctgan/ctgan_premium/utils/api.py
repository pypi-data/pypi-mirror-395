import numpy as np
from typing import List, Dict
from .factory import CTGANPremiumFactory


class CTGANPremiumAPI:
    """High-level API for premium CTGAN synthetic tabular data generation"""

    def __init__(self, model_type: str = "premium"):
        self.model_type = model_type
        self.trainer = None
        self.is_fitted = False

    def fit(
        self,
        data: np.ndarray,
        continuous_cols: list,
        categorical_cols: list,
        epochs: int = 1000,
        **kwargs,
    ) -> dict:
        """Fit the premium CTGAN model to data"""

        # Convert column indices to counts
        n_cont = len(continuous_cols)
        n_cat = len(categorical_cols)

        # Extract verbose parameter
        verbose = kwargs.pop("verbose", True)

        # Create model based on type
        if self.model_type == "basic":
            self.trainer = CTGANPremiumFactory.create_basic_model(
                continuous_dims=list(range(n_cont)), categorical_dims=list(range(n_cat))
            )
        elif self.model_type == "premium":
            premium_features = kwargs.get("premium_features", None)
            self.trainer = CTGANPremiumFactory.create_premium_model(
                list(range(n_cont)), list(range(n_cat)), premium_features
            )
        elif self.model_type == "enterprise":
            self.trainer = CTGANPremiumFactory.create_enterprise_model(
                list(range(n_cont)), list(range(n_cat))
            )
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")

        # Fit the model
        losses = self.trainer.fit(data, epochs=epochs, verbose=verbose)
        self.is_fitted = True

        return losses

    def generate(self, n_samples: int) -> np.ndarray:
        """Generate synthetic samples"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before generating samples")

        return self.trainer.generate(n_samples)

    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance scores"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before getting feature importance")

        return self.trainer.get_feature_importance()

    def save(self, filepath: str):
        """Save the model"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before saving")

        self.trainer.save_model(filepath)

    def load(self, filepath: str):
        """Load a saved model"""
        if self.trainer is None:
            # Create a basic trainer if none exists
            # We need to infer the dimensions from the saved model
            import torch

            checkpoint = torch.load(filepath, map_location="cpu")
            config = checkpoint.get("config")
            if config is None:
                raise ValueError("Cannot load model: config not found in saved file")

            # Create trainer based on model type
            if self.model_type == "basic":
                self.trainer = CTGANPremiumFactory.create_basic_model(
                    continuous_dims=config.continuous_dims,
                    categorical_dims=config.categorical_dims,
                )
            elif self.model_type == "premium":
                self.trainer = CTGANPremiumFactory.create_premium_model(
                    continuous_dims=config.continuous_dims,
                    categorical_dims=config.categorical_dims,
                )
            elif self.model_type == "enterprise":
                self.trainer = CTGANPremiumFactory.create_enterprise_model(
                    continuous_dims=config.continuous_dims,
                    categorical_dims=config.categorical_dims,
                )
            else:
                raise ValueError(f"Unknown model type: {self.model_type}")

        self.trainer.load_model(filepath)
        self.is_fitted = True
