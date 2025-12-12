import torch
import numpy as np
from ..config.config import CTGANPremiumConfig
from .sampling_strategies import GMMLatentSampler, ClusteredConditionalSampler


class CTGANPremiumSampler:
    """Premium CTGAN sampler with advanced sampling strategies"""

    def __init__(self, config: CTGANPremiumConfig):
        self.config = config
        self.latent_dim = config.latent_dim

        # Premium samplers
        if config.use_gmm_sampling:
            self.gmm_sampler = GMMLatentSampler()

        if config.use_clustered_sampling:
            self.clustered_sampler = ClusteredConditionalSampler()

        if config.use_hard_sample_mining:
            self.hard_samples_buffer = []

    def fit(self, real_data: np.ndarray):
        """Fit samplers to real data"""
        if self.config.use_gmm_sampling and hasattr(self, "gmm_sampler"):
            self.gmm_sampler.fit(real_data)

        if self.config.use_clustered_sampling and hasattr(self, "clustered_sampler"):
            self.clustered_sampler.fit(real_data)

    def sample(
        self, n_samples: int, device: torch.device, difficulty_level: float = 1.0
    ) -> torch.Tensor:
        """Sample latent codes with premium features"""

        # Choose sampling strategy
        if self.config.use_gmm_sampling and hasattr(self, "gmm_sampler"):
            samples = self.gmm_sampler.sample(n_samples, self.latent_dim, device)
        elif self.config.use_clustered_sampling and hasattr(self, "clustered_sampler"):
            samples = self.clustered_sampler.sample(n_samples, self.latent_dim, device)
        else:
            # Standard normal sampling
            samples = torch.randn(n_samples, self.latent_dim, device=device)

        # Apply multi-scale noise injection
        if self.config.use_multiscale_noise:
            # Add noise at different scales
            for scale in [0.1, 0.05, 0.01]:
                noise = torch.randn_like(samples) * scale * difficulty_level
                samples = samples + noise

        # Hard sample mining
        if self.config.use_hard_sample_mining and self.hard_samples_buffer:
            # Replace some samples with hard samples
            n_hard = min(n_samples // 4, len(self.hard_samples_buffer))
            if n_hard > 0:
                hard_samples = torch.stack(self.hard_samples_buffer[-n_hard:])
                samples[:n_hard] = hard_samples

        return samples

    def update_hard_samples(self, samples: torch.Tensor, losses: torch.Tensor):
        """Update hard samples buffer based on high losses"""
        if not self.config.use_hard_sample_mining:
            return

        # Keep samples with highest losses
        high_loss_idx = losses.argsort(descending=True)[: len(losses) // 4]
        hard_samples = samples[high_loss_idx]

        # Update buffer (keep last 100 hard samples)
        self.hard_samples_buffer.extend(hard_samples.cpu())
        if len(self.hard_samples_buffer) > 100:
            self.hard_samples_buffer = self.hard_samples_buffer[-100:]
