"""
High-level API for TVAE Premium
"""
import numpy as np
from .factory import TVAEFactory


class TVAEPremiumAPI:
    """High-level API for TVAE synthetic tabular data generation (premium edition)"""

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
        # Store column indices
        self.continuous_cols = continuous_cols
        self.categorical_cols = categorical_cols

        # Calculate dimensions
        n_cont = len(continuous_cols)
        n_cat = len(categorical_cols)
        
        # Extract continuous part
        data_cont = data[:, continuous_cols].astype(np.float32)
        
        # Extract and process categorical part
        categorical_dims = []
        data_cat_list = []
        
        if n_cat > 0:
            # We assume input is label-encoded (integers)
            data_cat_raw = data[:, categorical_cols].astype(int)
            
            for i in range(n_cat):
                col = data_cat_raw[:, i]
                # Determine number of classes. 
                # We assume classes are 0, 1, ..., K-1.
                if len(col) > 0:
                    num_classes = int(col.max() + 1)
                else:
                    num_classes = 0
                categorical_dims.append(num_classes)
                
                # One-hot encode
                if num_classes > 0:
                    one_hot = np.zeros((col.size, num_classes), dtype=np.float32)
                    one_hot[np.arange(col.size), col] = 1
                    data_cat_list.append(one_hot)
            
            if data_cat_list:
                data_cat_processed = np.hstack(data_cat_list)
            else:
                data_cat_processed = np.empty((data.shape[0], 0), dtype=np.float32)
        else:
            categorical_dims = []
            data_cat_processed = np.empty((data.shape[0], 0), dtype=np.float32)
            
        # Concatenate: Continuous first, then Categorical
        processed_data = np.hstack([data_cont, data_cat_processed])

        if self.model_type == "basic":
            self.trainer = TVAEFactory.create_basic_model(
                continuous_dims=list(range(n_cont)), categorical_dims=categorical_dims
            )
        elif self.model_type == "premium":
            premium_features = kwargs.get("premium_features", None)
            self.trainer = TVAEFactory.create_premium_model(
                list(range(n_cont)), categorical_dims, premium_features
            )
        elif self.model_type == "enterprise":
            self.trainer = TVAEFactory.create_enterprise_model(
                list(range(n_cont)), categorical_dims
            )
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
        losses = self.trainer.fit(
            processed_data, epochs=epochs, verbose=kwargs.get("verbose", True)
        )
        self.is_fitted = True
        return losses

    def generate(self, n_samples: int) -> np.ndarray:
        if not self.is_fitted:
            raise ValueError("Model must be fitted before generating samples")
        
        # Get raw samples (continuous + one-hot categorical)
        raw_samples = self.trainer.generate(n_samples)
        
        # Split continuous and categorical
        n_cont = len(self.continuous_cols)
        samples_cont = raw_samples[:, :n_cont]
        samples_cat_onehot = raw_samples[:, n_cont:]
        
        # Reverse one-hot encoding
        samples_cat_list = []
        start_idx = 0
        
        # We need to know the dimensions of each categorical feature
        # These are stored in self.trainer.config.categorical_dims if available,
        # or we should have stored them in self.categorical_dims_sizes during fit.
        # However, self.trainer.config.categorical_dims is what we passed to the factory.
        
        categorical_dims = self.trainer.config.categorical_dims
        
        for dim in categorical_dims:
            end_idx = start_idx + dim
            # Extract one-hot block for this feature
            one_hot_block = samples_cat_onehot[:, start_idx:end_idx]
            # Convert to integer (argmax)
            cat_col = np.argmax(one_hot_block, axis=1).reshape(-1, 1)
            samples_cat_list.append(cat_col)
            start_idx = end_idx
            
        if samples_cat_list:
            samples_cat = np.hstack(samples_cat_list)
            # Combine continuous and categorical
            return np.hstack([samples_cont, samples_cat])
        else:
            return samples_cont

    def get_feature_importance(self):
        if not self.is_fitted:
            raise ValueError("Model must be fitted before getting feature importance")
        return self.trainer.get_feature_importance()

    def save(self, filepath: str):
        if not self.is_fitted:
            raise ValueError("Model must be fitted before saving")
        # Save trainer state
        self.trainer.save_model(filepath)
        # Save API state (metadata)
        import pickle
        metadata_path = filepath + ".meta"
        
        # Get categorical dims from trainer config
        categorical_dims = self.trainer.config.categorical_dims
        
        with open(metadata_path, "wb") as f:
            pickle.dump({
                "continuous_cols": self.continuous_cols,
                "categorical_cols": self.categorical_cols,
                "categorical_dims": categorical_dims,
                "model_type": self.model_type,
                "is_fitted": self.is_fitted
            }, f)

    def load(self, filepath: str):
        # Load API state
        import pickle
        metadata_path = filepath + ".meta"
        categorical_dims = []
        
        if os.path.exists(metadata_path):
            with open(metadata_path, "rb") as f:
                metadata = pickle.load(f)
                self.continuous_cols = metadata.get("continuous_cols", [])
                self.categorical_cols = metadata.get("categorical_cols", [])
                self.model_type = metadata.get("model_type", self.model_type)
                self.is_fitted = metadata.get("is_fitted", False)
                categorical_dims = metadata.get("categorical_dims", [])
        
        if self.trainer is None:
            # Recreate trainer if needed
            n_cont = len(self.continuous_cols)
            
            if self.model_type == "basic":
                self.trainer = TVAEFactory.create_basic_model(
                    continuous_dims=list(range(n_cont)), categorical_dims=categorical_dims
                )
            elif self.model_type == "premium":
                # Note: premium_features are not currently saved/loaded. 
                # If they affect architecture (like multi-head decoder), loading weights might fail 
                # if we don't recreate with same features.
                # For now, we assume default or user-provided init args, but ideally we should save premium_features too.
                # Let's try to create a default premium model.
                self.trainer = TVAEFactory.create_premium_model(
                    list(range(n_cont)), categorical_dims
                )
            elif self.model_type == "enterprise":
                self.trainer = TVAEFactory.create_enterprise_model(
                    list(range(n_cont)), categorical_dims
                )
            else:
                # Fallback if model type is unknown or custom
                pass

        if self.trainer is not None:
            self.trainer.load_model(filepath)
            self.is_fitted = True
        else:
            raise ValueError("Could not recreate trainer. Please initialize API with correct model type or ensure metadata exists.")
