from typing import List, Optional
from ..config.config import CTGANPremiumConfig
from ..trainers.trainer import CTGANPremiumTrainer


class CTGANPremiumFactory:
    """Factory for creating premium CTGAN models"""

    @staticmethod
    def create_basic_model(
        continuous_dims: List[int], categorical_dims: List[int]
    ) -> CTGANPremiumTrainer:
        """Create basic CTGAN model (no premium features)"""
        config = CTGANPremiumConfig(
            continuous_dims=continuous_dims, categorical_dims=categorical_dims
        )
        return CTGANPremiumTrainer(config)

    @staticmethod
    def create_premium_model(
        continuous_dims: List[int],
        categorical_dims: List[int],
        premium_features: List[str] = None,
        config: Optional[CTGANPremiumConfig] = None,
    ) -> CTGANPremiumTrainer:
        """Create CTGAN model with selected premium features"""
        if config is not None:
            # Use provided config object
            pass  # config is already set
        else:
            # Create new config from parameters
            config = CTGANPremiumConfig(
                continuous_dims=continuous_dims, categorical_dims=categorical_dims
            )

        if premium_features is None:
            # Enable all premium features
            premium_features = [
                "mixture_of_experts",
                "memory_augmented",
                "feature_attention",
                "adversarial_disentanglement",
                "progressive_generation",
                "multimodal_discriminator",
                "hierarchical_discriminator",
                "contrastive_discriminator",
                "distributional_discriminator",
                "ensemble_discriminator",
                "gmm_sampling",
                "clustered_sampling",
                "hard_sample_mining",
                "multiscale_noise",
                "flow_sampling",
                "curriculum_learning",
                "pareto_optimization",
                "progressive_training",
                "uncertainty_weighting",
                "contrastive_training",
            ]

        # Enable requested premium features
        for feature in premium_features:
            if hasattr(config, f"use_{feature}"):
                setattr(config, f"use_{feature}", True)

        return CTGANPremiumTrainer(config)

    @staticmethod
    def create_enterprise_model(
        continuous_dims: List[int], categorical_dims: List[int]
    ) -> CTGANPremiumTrainer:
        """Create enterprise-grade model with all features"""
        config = CTGANPremiumConfig(
            continuous_dims=continuous_dims,
            categorical_dims=categorical_dims,
            latent_dim=256,
            hidden_dim=512,
            num_layers=4,
            learning_rate=1e-4,
            batch_size=128,
            # Enable all premium features
            use_mixture_of_experts=True,
            use_memory_augmented=True,
            use_feature_attention=True,
            use_adversarial_disentanglement=True,
            use_progressive_generation=True,
            use_multimodal_discriminator=True,
            use_hierarchical_discriminator=True,
            use_contrastive_discriminator=True,
            use_distributional_discriminator=True,
            use_ensemble_discriminator=True,
            use_gmm_sampling=True,
            use_clustered_sampling=True,
            use_hard_sample_mining=True,
            use_multiscale_noise=True,
            use_flow_sampling=True,
            use_curriculum_learning=True,
            use_pareto_optimization=True,
            use_progressive_training=True,
            use_uncertainty_weighting=True,
            use_contrastive_training=True,
        )

        return CTGANPremiumTrainer(config)
