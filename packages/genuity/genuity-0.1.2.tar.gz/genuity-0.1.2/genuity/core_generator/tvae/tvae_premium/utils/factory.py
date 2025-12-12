"""
Simple factory for TVAE Premium - uses basic TVAE with enhancements
"""
import numpy as np


class TVAEFactory:
    """Factory to create TVAE trainer instances"""
    
    @staticmethod
    def create_basic_model(continuous_dims, categorical_dims):
        """Create basic TVAE trainer"""
        # Import here to avoid circular dependencies
        from ...tvae.tvae.trainers.trainer import TVAETrainer
        return TVAETrainer(continuous_dims, categorical_dims)
    
    @staticmethod
    def create_premium_model(continuous_dims, categorical_dims, premium_features=None):
        """Create premium TVAE trainer with enhanced features"""
        from ...tvae.trainers.trainer import TVAETrainer
        from ...tvae.config.config import TVAEConfig
        
        # Create config
        config = TVAEConfig(
            continuous_dims=continuous_dims, 
            categorical_dims=categorical_dims
        )
        
        # Apply premium features to config if provided
        if premium_features:
            for k, v in premium_features.items():
                if hasattr(config, k):
                    setattr(config, k, v)
                    
        trainer = TVAETrainer(config)
        return trainer
    
    @staticmethod
    def create_enterprise_model(continuous_dims, categorical_dims):
        """Create enterprise TVAE trainer"""
        from ...tvae.trainers.trainer import TVAETrainer
        from ...tvae.config.config import TVAEConfig
        
        config = TVAEConfig(
            continuous_dims=continuous_dims, 
            categorical_dims=categorical_dims
        )
        return TVAETrainer(config)
