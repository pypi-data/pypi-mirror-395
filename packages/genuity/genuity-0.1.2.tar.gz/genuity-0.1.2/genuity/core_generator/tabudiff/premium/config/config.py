"""
Configuration for TabuDiff Premium with advanced features.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class TabuDiffPremiumConfig:
    # Model Architecture
    model_type: str = "enterprise"
    hidden_dim: int = 512
    num_layers: int = 6
    dropout: float = 0.1
    activation: str = "gelu"
    
    # Training Parameters
    learning_rate: float = 5e-4
    batch_size: int = 256
    num_epochs: int = 100
    seed: int = 42
    device: str = "cpu"
    
    # Diffusion Parameters
    num_diffusion_steps: int = 500
    beta_start: float = 1e-4
    beta_end: float = 0.02

    # Advanced Features - Attention
    cross_feature_attention: bool = True
    attention_heads: int = 8
    attention_dim: int = 64

    # Advanced Features - Mixture Density
    mixture_density_heads: bool = True
    num_gaussians: int = 3
    categorical_temperature: float = 1.0

    # Advanced Features - Conditional Generation
    conditional_diffusion: bool = True
    class_conditional_embeddings: bool = True
    mask_aware_conditioning: bool = True

    # Advanced Features - Contrastive Learning
    contrastive_alignment: bool = True
    info_nce_temperature: float = 0.1
    feature_pair_weight: float = 0.1

    # Advanced Sampling
    sampler_type: str = "dpm_solver_plus"
    num_sampling_steps: int = 50
    adaptive_step_correction: bool = True
    error_threshold: float = 1e-4

    # Quality Control
    quality_gating: bool = True
    distribution_threshold: float = 0.90
    correlation_threshold: float = 0.95
    feature_interaction_threshold: float = 0.85

    # Performance
    memory_limit_gb: float = 6.0
    parallel_processing: bool = True
    n_jobs: int = -1
    
    model_save_path: str = "tabudiff_premium_score_network.pt"

    def validate(self):
        """Validate configuration parameters."""
        if self.hidden_dim <= 0:
            raise ValueError("hidden_dim must be positive")
        if self.num_layers <= 0:
            raise ValueError("num_layers must be positive")
        if self.attention_heads <= 0:
            raise ValueError("attention_heads must be positive")
        if self.hidden_dim % self.attention_heads != 0:
            raise ValueError("hidden_dim must be divisible by attention_heads")
        return True

    @classmethod
    def get_basic_config(cls):
        return cls(
            model_type="basic",
            cross_feature_attention=False,
            mixture_density_heads=False,
            conditional_diffusion=False,
            contrastive_alignment=False,
            quality_gating=False
        )

    @classmethod
    def get_premium_config(cls):
        return cls(
            model_type="premium",
            cross_feature_attention=True,
            mixture_density_heads=True,
            conditional_diffusion=True,
            contrastive_alignment=False,
            quality_gating=True
        )

    @classmethod
    def get_enterprise_config(cls):
        return cls()  # Default is enterprise
