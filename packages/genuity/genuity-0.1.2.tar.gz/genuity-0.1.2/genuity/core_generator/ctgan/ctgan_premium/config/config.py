from dataclasses import dataclass
from typing import List


@dataclass
class CTGANPremiumConfig:
    """Configuration for the premium CTGAN model with all advanced features"""

    # Basic settings
    latent_dim: int = 128
    hidden_dim: int = 256
    discriminator_hidden_dim: int = 256
    discriminator_dropout: float = 0.3
    num_layers: int = 3
    learning_rate: float = 1e-4
    batch_size: int = 128

    # Premium feature flags
    use_mixture_of_experts: bool = False
    use_memory_augmented: bool = False
    use_feature_attention: bool = False
    use_adversarial_disentanglement: bool = False
    use_progressive_generation: bool = False

    use_multimodal_discriminator: bool = False
    use_hierarchical_discriminator: bool = False
    use_contrastive_discriminator: bool = False
    use_distributional_discriminator: bool = False
    use_ensemble_discriminator: bool = False

    use_gmm_sampling: bool = False
    use_clustered_sampling: bool = False
    use_hard_sample_mining: bool = False
    use_multiscale_noise: bool = False
    use_flow_sampling: bool = False

    use_curriculum_learning: bool = False
    use_pareto_optimization: bool = False
    use_progressive_training: bool = False
    use_uncertainty_weighting: bool = False
    use_contrastive_training: bool = False

    # Feature dimensions
    continuous_dims: List[int] = None
    categorical_dims: List[int] = None

    # Training stability improvements
    use_spectral_norm: bool = True
    use_gradient_penalty: bool = True
    gradient_penalty_weight: float = 10.0

    # Loss balancing
    generator_loss_weight: float = 1.0
    discriminator_loss_weight: float = 1.0
    diversity_loss_weight: float = 0.01

    def __post_init__(self):
        if self.continuous_dims is None:
            self.continuous_dims = []
        if self.categorical_dims is None:
            self.categorical_dims = []
