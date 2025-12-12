import numpy as np
from typing import List, Dict
from .factory import CTGANFactory


class CTGANAPI:
    """High-level API for CTGAN synthetic tabular data generation"""

    def __init__(self):
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
        """Fit the CTGAN model to data"""

        # Calculate cardinalities and transform data to one-hot
        # We assume data is label-encoded (integers) for categorical columns
        
        # 1. Compute cardinalities
        cardinalities = []
        for col_idx in categorical_cols:
            unique_vals = np.unique(data[:, col_idx])
            cardinalities.append(len(unique_vals))
            
        # 2. Transform data to one-hot
        # We need to reconstruct the data: continuous + one-hot categorical
        # Note: This simple transformation assumes continuous cols are already numeric
        
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

        # Extract verbose parameter
        verbose = kwargs.pop("verbose", True)

        # Create model
        # continuous_dims is just a list of indices for the generator to know how many continuous vars
        # categorical_dims is a list of cardinalities
        self.trainer = CTGANFactory.create_model(
            continuous_dims=list(range(len(continuous_cols))),
            categorical_dims=cardinalities,
            **kwargs,
        )

        # Fit the model with transformed data
        losses = self.trainer.fit(transformed_data, epochs=epochs, verbose=verbose)
        self.is_fitted = True
        
        # Store metadata for generation
        self.continuous_cols = continuous_cols
        self.categorical_cols = categorical_cols
        self.cardinalities = cardinalities

        return losses

    def generate(self, n_samples: int) -> np.ndarray:
        """Generate synthetic samples"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before generating samples")

        # Generate raw data (continuous + one-hot)
        raw_data = self.trainer.generate(n_samples)
        
        # Reconstruct original format (continuous + label-encoded categorical)
        # We need to map back to the original column order
        
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
        # We need to put columns back in their original indices
        # self.continuous_cols and self.categorical_cols contain the original indices
        
        total_cols = len(self.continuous_cols) + len(self.categorical_cols)
        # Assuming original data had exactly these columns and they cover 0..total_cols-1?
        # Not necessarily. The user might have passed specific columns.
        # But we should return a matrix with columns corresponding to continuous_cols + categorical_cols
        # OR we should try to reconstruct the full matrix if we know the shape?
        # Usually generate returns a matrix where columns are in the same order as passed to fit?
        # But fit took 'data' which might have extra columns.
        # Standard behavior: return matrix with only the modeled columns, usually in order of (cont, cat) or original?
        # Let's return in the order of (continuous_cols, categorical_cols) concatenated, 
        # OR better: create a result matrix of shape (n_samples, max_idx + 1) and fill it?
        # But we don't know max_idx if we didn't save it.
        # Let's just return continuous then categorical, and let the user (Postprocessor) handle mapping.
        # BUT Postprocessor expects columns in specific order matching 'processed_data'.
        # In the example, we passed 'processed_data' which has columns in some order.
        # And we passed indices.
        # If we return (cont, cat), the order might be different from 'processed_data'.
        
        # Let's try to reconstruct the order if indices are unique and cover a range.
        # But simpler: just return concatenated [continuous, categorical_labels]
        # The Postprocessor usually maps by name, but here we are dealing with numpy array.
        # The example script:
        # synthetic_data = postprocessor.inverse_transform_modified_data(pd.DataFrame(synthetic_raw, columns=processed_data.columns))
        # This assumes synthetic_raw columns match processed_data.columns.
        
        # So we MUST reconstruct the column order.
        
        output = np.zeros((n_samples, total_cols))
        
        # We need to sort indices to know where to put what
        # But wait, we have values for continuous_cols and categorical_cols.
        # If processed_data had columns [C1, Cat1, C2, Cat2], indices are [0, 1, 2, 3].
        # continuous_cols=[0, 2], categorical_cols=[1, 3].
        # We have C1, C2 in continuous_part. Cat1, Cat2 in categorical_labels.
        # We need to put C1 at 0, Cat1 at 1, C2 at 2, Cat2 at 3.
        
        # Mapping
        # But we can't easily do this if we don't know the full shape or if indices are sparse.
        # However, for the example, indices cover all columns.
        
        # Let's create a list of (index, value_array) and sort by index
        cols_data = []
        for i, col_idx in enumerate(self.continuous_cols):
            cols_data.append((col_idx, continuous_part[:, i]))
            
        for i, col_idx in enumerate(self.categorical_cols):
            cols_data.append((col_idx, categorical_labels[:, i]))
            
        # Sort by index
        cols_data.sort(key=lambda x: x[0])
        
        # Stack
        result = np.stack([x[1] for x in cols_data], axis=1)
        
        return result

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

            self.trainer = CTGANFactory.create_model(
                continuous_dims=config.continuous_dims,
                categorical_dims=config.categorical_dims,
            )

        self.trainer.load_model(filepath)
        self.is_fitted = True
