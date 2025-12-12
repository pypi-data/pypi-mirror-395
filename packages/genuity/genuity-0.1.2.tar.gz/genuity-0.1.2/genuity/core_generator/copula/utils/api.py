"""
Copula API - High-level interface for Copula-based synthetic data generation
"""

import numpy as np
from typing import List, Optional
from ..copula.copula_core import CopulaCore


class CopulaAPI:
    """
    High-level API for Copula synthetic tabular data generation.
    
    Provides easy-to-use interface for:
    - Fitting Gaussian copula models
    - Generating synthetic samples
    - Saving/loading models
    """
    
    def __init__(self, model_type: str = "basic", verbose: bool = True):
        """
        Initialize Copula API.
        
        Args:
            model_type: Type of model ("basic", "premium")
            verbose: Whether to print progress
        """
        self.model_type = model_type
        self.verbose = verbose
        self.model = None
        self.is_fitted = False
    
    def fit(
        self,
        data: np.ndarray,
        continuous_cols: List[int],
        categorical_cols: List[int],
        **kwargs
    ) -> dict:
        """
        Fit the Copula model to data.
        
        Args:
            data: Input data array (n_samples, n_features)
            continuous_cols: List of column indices for continuous variables
            categorical_cols: List of column indices for categorical variables
            **kwargs: Additional arguments
            
        Returns:
            Dictionary with fitting results
        """
        # Create model
        copula_type = kwargs.get('copula_type', 'gaussian')
        self.model = CopulaCore(copula_type=copula_type, verbose=self.verbose)
        
        # Fit
        result = self.model.fit(data, continuous_cols, categorical_cols)
        self.is_fitted = True
        
        return result
    
    def generate(self, n_samples: int) -> np.ndarray:
        """
        Generate synthetic samples.
        
        Args:
            n_samples: Number of samples to generate
            
        Returns:
            Synthetic data array
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before generating samples")
        
        return self.model.generate(n_samples)
    
    def save(self, filepath: str):
        """Save the model."""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before saving")
        
        self.model.save_model(filepath)
    
    def load(self, filepath: str):
        """Load a saved model."""
        self.model = CopulaCore(verbose=self.verbose)
        self.model.load_model(filepath)
        self.is_fitted = True
