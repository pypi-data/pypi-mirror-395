"""
TabuDiff Premium API

High-level interface for enterprise-grade tabular diffusion.
"""

import pandas as pd
import numpy as np
import torch
from ..config.config import TabuDiffPremiumConfig
from ..models.score_network import PremiumScoreNetwork
from ..trainers.trainer import TabuDiffPremiumTrainer
from ..samplers.sampler import PremiumDiffusionSampler
from .scheduler import PremiumVarianceScheduler


class TabuDiffPremiumAPI:
    """
    High-level API for TabuDiff Premium.
    
    Supports enterprise-grade features:
    - Cross-feature attention
    - Mixture density networks
    - Conditional generation
    - Advanced sampling algorithms
    """
    
    def __init__(self, config=None):
        """
        Initialize TabuDiff Premium API.
        
        Args:
            config: TabuDiffPremiumConfig or None for default enterprise config
        """
        self.config = config or TabuDiffPremiumConfig.get_enterprise_config()
        self.config.validate()
        
        self.score_network = None
        self.trainer = None
        self.sampler = None
        self.scheduler = None
        self.is_fitted = False
        
        # Data statistics for normalization
        self.data_mean = None
        self.data_std = None
    
    def fit_dataframe(self, df, normalize=True, verbose=True):
        """
        Fit model to a DataFrame.
        
        Args:
            df: pandas DataFrame
            normalize: Whether to normalize data
            verbose: Show progress
        """
        # Convert to array
        data = torch.tensor(df.values, dtype=torch.float32)
        
        return self.fit(data, normalize=normalize, verbose=verbose)
    
    def fit(self, data, normalize=True, verbose=True):
        """
        Fit model to data.
        
        Args:
            data: torch.Tensor or numpy array
            normalize: Whether to normalize data
            verbose: Show progress
        """
        # Convert to tensor if needed
        if isinstance(data, np.ndarray):
            data = torch.tensor(data, dtype=torch.float32)
        
        # Normalize
        if normalize:
            self.data_mean = data.mean(dim=0, keepdim=True)
            self.data_std = data.std(dim=0, keepdim=True) + 1e-8
            data = (data - self.data_mean) / self.data_std
        
        feature_dim = data.shape[1]
        
        if verbose:
            print("Initializing TabuDiff Premium")
            print(f"   Model type: {self.config.model_type}")
            print(f"   Cross-feature attention: {self.config.cross_feature_attention}")
            print(f"   Mixture density heads: {self.config.mixture_density_heads}")
            print(f"   Sampler: {self.config.sampler_type}")
        
        # Create components
        self.scheduler = PremiumVarianceScheduler(self.config)
        self.score_network = PremiumScoreNetwork(self.config, feature_dim)
        self.trainer = TabuDiffPremiumTrainer(self.score_network, self.scheduler, self.config)
        
        # Train
        result = self.trainer.fit(data, verbose=verbose)
        
        # Create sampler
        self.sampler = PremiumDiffusionSampler(self.score_network, self.scheduler, self.config)
        
        self.is_fitted = True
        return result
    
    def generate_dataframe(self, num_samples, verbose=True):
        """
        Generate synthetic DataFrame.
        
        Args:
            num_samples: Number of samples
            verbose: Show progress
        """
        samples = self.generate(num_samples, verbose=verbose)
        return pd.DataFrame(samples)
    
    def generate(self, num_samples, verbose=True):
        """
        Generate synthetic samples.
        
        Args:
            num_samples: Number of samples
            verbose: Show progress
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before generating samples")
        
        # Get feature dim from score network
        feature_dim = self.score_network.feature_dim
        
        # Generate
        samples = self.sampler.sample(num_samples, feature_dim, verbose=verbose)
        
        # Denormalize
        if self.data_mean is not None and self.data_std is not None:
            samples_tensor = torch.tensor(samples, dtype=torch.float32)
            samples_tensor = samples_tensor * self.data_std + self.data_mean
            samples = samples_tensor.numpy()
        
        return samples
    
    def save(self, filepath):
        """Save model."""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before saving")
        
        self.trainer.save_model(filepath)
    
    def load(self, filepath):
        """Load model."""
        # This requires knowing the feature dimension
        # For now, raise an error
        raise NotImplementedError("Model loading will be implemented in next iteration")
