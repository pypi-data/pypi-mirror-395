import numpy as np
from .factory import TVAEFactory


class TVAEAPI:
    """High-level API for TVAE synthetic tabular data generation (basic edition)"""

    def __init__(self, model_type: str = "basic"):
        # Only basic model is supported in the base package
        if model_type != "basic":
            raise ValueError(
                "This package provides only the basic TVAE. For advanced features, import tvae_premium and use TVAEAPI(model_type='premium')."
            )
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
        
        # Calculate cardinalities and transform data to one-hot
        # We assume data is label-encoded (integers) for categorical columns
        
        # 1. Compute cardinalities
        cardinalities = []
        for col_idx in categorical_cols:
            unique_vals = np.unique(data[:, col_idx])
            cardinalities.append(len(unique_vals))
            
        # 2. Transform data to one-hot
        transformed_parts = []
        
        # Add continuous columns
        if continuous_cols:
            transformed_parts.append(data[:, continuous_cols])
            
        # Add one-hot encoded categorical columns
        for i, col_idx in enumerate(categorical_cols):
            col_data = data[:, col_idx].astype(int)
            n_classes = cardinalities[i]
            
            # Create one-hot
            one_hot = np.zeros((len(data), n_classes), dtype=np.float32)
            one_hot[np.arange(len(data)), col_data] = 1.0
            transformed_parts.append(one_hot)
            
        if transformed_parts:
            transformed_data = np.concatenate(transformed_parts, axis=1)
        else:
            transformed_data = np.zeros((len(data), 0))

        # Create basic model only
        # categorical_dims is a list of cardinalities
        self.trainer = TVAEFactory.create_basic_model(
            continuous_dims=list(range(len(continuous_cols))), 
            categorical_dims=cardinalities
        )
        losses = self.trainer.fit(
            transformed_data, epochs=epochs, verbose=kwargs.get("verbose", True)
        )
        self.is_fitted = True
        
        # Store metadata for generation
        self.continuous_cols = continuous_cols
        self.categorical_cols = categorical_cols
        self.cardinalities = cardinalities
        
        return losses

    def generate(self, n_samples: int) -> np.ndarray:
        if not self.is_fitted:
            raise ValueError("Model must be fitted before generating samples")
            
        # Generate raw data (continuous + one-hot)
        raw_data = self.trainer.generate(n_samples)
        
        # Reconstruct original format (continuous + label-encoded categorical)
        n_cont = len(self.continuous_cols)
        
        # Extract continuous part
        continuous_part = raw_data[:, :n_cont]
        
        # Extract and convert categorical part
        categorical_part = raw_data[:, n_cont:]
        
        categorical_labels = []
        start_idx = 0
        for cardinality in self.cardinalities:
            end_idx = start_idx + cardinality
            # Argmax to get label
            labels = np.argmax(categorical_part[:, start_idx:end_idx], axis=1)
            categorical_labels.append(labels.reshape(-1, 1))
            start_idx = end_idx
            
        if categorical_labels:
            categorical_labels = np.concatenate(categorical_labels, axis=1)
        else:
            categorical_labels = np.zeros((n_samples, 0))
            
        # Combine based on original column order
        total_cols = len(self.continuous_cols) + len(self.categorical_cols)
        output = np.zeros((n_samples, total_cols))
        
        cols_data = []
        for i, col_idx in enumerate(self.continuous_cols):
            cols_data.append((col_idx, continuous_part[:, i]))
            
        for i, col_idx in enumerate(self.categorical_cols):
            cols_data.append((col_idx, categorical_labels[:, i]))
            
        cols_data.sort(key=lambda x: x[0])
        result = np.stack([x[1] for x in cols_data], axis=1)
        
        return result

    def get_feature_importance(self):
        if not self.is_fitted:
            raise ValueError("Model must be fitted before getting feature importance")
        return self.trainer.get_feature_importance()

    def save(self, filepath: str):
        if not self.is_fitted:
            raise ValueError("Model must be fitted before saving")
        self.trainer.save_model(filepath)

    def load(self, filepath: str):
        if self.trainer is None:
            raise ValueError("Must create model first (call fit or specify model type)")
        self.trainer.load_model(filepath)
        self.is_fitted = True
