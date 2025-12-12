"""
Copula-based Synthetic Data Generator - Core Module

This module implements Gaussian copula for tabular synthetic data generation.
"""

import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import norm, gaussian_kde
from sklearn.preprocessing import QuantileTransformer
from typing import List, Tuple, Optional
import warnings

warnings.filterwarnings('ignore')


class CopulaCore:
    """
    Core Gaussian Copula implementation for synthetic data generation.
    
    Supports both continuous and categorical variables through:
    1. Marginal distribution fitting
    2. Transformation to uniform/normal space
   3. Copula (correlation structure) fitting
    4. Sampling and inverse transformation
    """
    
    def __init__(self, copula_type: str = "gaussian", verbose: bool = True):
        """
        Initialize Copula model.
        
        Args:
            copula_type: Type of copula ("gaussian", "t", "vine")
            verbose: Whether to print progress messages
        """
        self.copula_type = copula_type
        self.verbose = verbose
        
        # Storage for fitted components
        self.marginal_distributions = {}
        self.correlation_matrix = None
        self.continuous_cols = None
        self.categorical_cols = None
        self.transformers = {}
        self.is_fitted = False
        
    def _print(self, msg):
        """Print message if verbose."""
        if self.verbose:
            print(f"[CopulaCore] {msg}")
    
    def fit(self, data: np.ndarray, continuous_cols: List[int], categorical_cols: List[int]):
        """
        Fit the Gaussian copula model to data.
        
        Args:
            data: Input data array (n_samples, n_features)
            continuous_cols: List of column indices for continuous variables
            categorical_cols: List of column indices for categorical variables
        """
        self._print("Fitting basic model...")
        self._print(f"Data shape: {data.shape}")
        self._print(f"Continuous columns: {len(continuous_cols)}")
        self._print(f"Categorical columns: {len(categorical_cols)}")
        
        self.continuous_cols = continuous_cols
        self.categorical_cols = categorical_cols
        self.n_features = data.shape[1]
        
        # Step 1:Fit marginal distributions
        self._print("Fitting marginal distributions...")
        self._fit_marginals(data)
        
        # Step 2: Transform to uniform space
        self._print("Transforming to uniform space...")
        uniform_data = self._transform_to_uniform(data)
        
        # Step 3: Transform to normal space
        normal_data = stats.norm.ppf(np.clip(uniform_data, 1e-6, 1 - 1e-6))
        
        # Step 4: Fit copula (estimate correlation)
        self._print("Fitting copula...")
        self._fit_copula(normal_data)
        
        self.is_fitted = True
        self._print("Model fitting complete!")
        
        return {"status": "success"}
    
    def _fit_marginals(self, data: np.ndarray):
        """Fit marginal distributions for each column."""
        for col_idx in range(self.n_features):
            col_data = data[:, col_idx]
            
            if col_idx in self.continuous_cols:
                # For continuous: use quantile transformer
                transformer = QuantileTransformer(
                    output_distribution='uniform',
                    n_quantiles=min(1000, len(col_data)),
                    random_state=42
                )
                transformer.fit(col_data.reshape(-1, 1))
                self.transformers[col_idx] = transformer
                
            elif col_idx in self.categorical_cols:
                # For categorical: store empirical distribution
                unique, counts = np.unique(col_data, return_counts=True)
                probabilities = counts / len(col_data)
                self.transformers[col_idx] = {
                    'unique_values': unique,
                    'probabilities': probabilities
                }
    
    def _transform_to_uniform(self, data: np.ndarray) -> np.ndarray:
        """Transform data to uniform [0, 1] space."""
        uniform_data = np.zeros_like(data)
        
        for col_idx in range(self.n_features):
            col_data = data[:, col_idx]
            
            if col_idx in self.continuous_cols:
                # Transform continuous using quantile transformer
                transformer = self.transformers[col_idx]
                uniform_data[:, col_idx] = transformer.transform(
                    col_data.reshape(-1, 1)
                ).flatten()
                
            elif col_idx in self.categorical_cols:
                # Transform categorical using empirical CDF
                transformer = self.transformers[col_idx]
                unique_vals = transformer['unique_values']
                probs = transformer['probabilities']
                
                # Compute empirical CDF for each value
                cdf_values = np.zeros(len(col_data))
                for i, val in enumerate(col_data):
                    idx = np.where(unique_vals == val)[0]
                    if len(idx) > 0:
                        # Add some jitter to avoid exact 0/1
                        cdf_values[i] = np.sum(probs[:idx[0]+1]) - 0.5 * probs[idx[0]]
                
                uniform_data[:, col_idx] = np.clip(cdf_values, 1e-6, 1 - 1e-6)
        
        return uniform_data
    
    def _fit_copula(self, normal_data: np.ndarray):
        """Fit Gaussian copula by estimating correlation matrix."""
        try:
            # Handle potential NaN/inf values
            normal_data = np.nan_to_num(normal_data, nan=0.0, posinf=3.0, neginf=-3.0)
            
            if self.copula_type == "gaussian":
                # Estimate correlation matrix
                try:
                    from sklearn.covariance import GraphicalLasso
                    gl = GraphicalLasso(alpha=0.01, max_iter=100)
                    gl.fit(normal_data)
                    self.correlation_matrix = gl.covariance_
                except Exception as e:
                    self._print(f"⚠️ Graphical Lasso failed: {e}. Using correlation matrix.")
                    self.correlation_matrix = np.corrcoef(normal_data.T)
            else:
                raise NotImplementedError(f"Copula type '{self.copula_type}' not implemented")
            
            # Validate correlation matrix
            if np.any(np.isnan(self.correlation_matrix)) or np.any(np.isinf(self.correlation_matrix)):
                self._print("⚠️ Correlation matrix contains inf/NaN. Using identity matrix.")
                self.correlation_matrix = np.eye(self.n_features)
                
        except Exception as e:
            self._print(f"⚠️ Error fitting copula: {e}. Using identity correlation.")
            self.correlation_matrix = np.eye(self.n_features)
    
    def generate(self, n_samples: int) -> np.ndarray:
        """
        Generate synthetic samples.
        
        Args:
            n_samples: Number of samples to generate
            
        Returns:
            Generated synthetic data
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before generating samples")
        
        # Step 1: Sample from multivariate normal
        try:
            mean = np.zeros(self.n_features)
            normal_samples = np.random.multivariate_normal(
                mean, self.correlation_matrix, size=n_samples
            )
        except Exception as e:
            self._print(f"⚠️ Error sampling from copula: {e}. Using independent samples.")
            normal_samples = np.random.randn(n_samples, self.n_features)
        
        # Step 2: Transform to uniform space
        uniform_samples = stats.norm.cdf(normal_samples)
        
        # Step 3: Transform to original space
        synthetic_data = self._inverse_transform(uniform_samples)
        
        return synthetic_data
    
    def _inverse_transform(self, uniform_data: np.ndarray) -> np.ndarray:
        """Transform from uniform space back to original data space."""
        synthetic_data = np.zeros_like(uniform_data)
        
        for col_idx in range(self.n_features):
            uniform_col = uniform_data[:, col_idx]
            
            if col_idx in self.continuous_cols:
                # Inverse transform for continuous
                transformer = self.transformers[col_idx]
                synthetic_data[:, col_idx] = transformer.inverse_transform(
                    uniform_col.reshape(-1, 1)
                ).flatten()
                
            elif col_idx in self.categorical_cols:
                # Inverse transform for categorical - sample based on CDF
                transformer = self.transformers[col_idx]
                unique_vals = transformer['unique_values']
                probs = transformer['probabilities']
                
                # Convert uniform values to categorical via inverse CDF
                cumsum = np.cumsum(probs)
                synthetic_col = np.zeros(len(uniform_col))
                
                for i, u in enumerate(uniform_col):
                    idx = np.searchsorted(cumsum, u)
                    idx = min(idx, len(unique_vals) - 1)
                    synthetic_col[i] = unique_vals[idx]
                
                synthetic_data[:, col_idx] = synthetic_col
        
        return synthetic_data
    
    def save_model(self, filepath: str):
        """Save the fitted model."""
        import pickle
        if not self.is_fitted:
            raise ValueError("Model must be fitted before saving")
        
        model_state = {
            'copula_type': self.copula_type,
            'continuous_cols': self.continuous_cols,
            'categorical_cols': self.categorical_cols,
            'n_features': self.n_features,
            'correlation_matrix': self.correlation_matrix,
            'transformers': self.transformers,
            'is_fitted': self.is_fitted
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_state, f)
    
    def load_model(self, filepath: str):
        """Load a saved model."""
        import pickle
        
        with open(filepath, 'rb') as f:
            model_state = pickle.load(f)
        
        self.copula_type = model_state['copula_type']
        self.continuous_cols = model_state['continuous_cols']
        self.categorical_cols = model_state['categorical_cols']
        self.n_features = model_state['n_features']
        self.correlation_matrix = model_state['correlation_matrix']
        self.transformers = model_state['transformers']
        self.is_fitted = model_state['is_fitted']
