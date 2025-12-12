import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, Optional
from ..config.config import CTGANPremiumConfig
from .components import (
    MultiModalDiscriminator,
    HierarchicalDiscriminator,
    ContrastiveLearningDiscriminator,
)


class CTGANPremiumDiscriminator(nn.Module):
    """Premium CTGAN discriminator with all advanced features"""

    def __init__(self, config: CTGANPremiumConfig):
        super().__init__()
        self.config = config
        input_dim = len(config.continuous_dims) + len(config.categorical_dims)
        d_hidden = config.discriminator_hidden_dim
        d_dropout = config.discriminator_dropout

        # Basic discriminator
        self.basic_disc = nn.Sequential(
            nn.Linear(input_dim, d_hidden),
            nn.LeakyReLU(0.2),
            nn.Dropout(d_dropout),
            nn.Linear(d_hidden, d_hidden // 2),
            nn.LeakyReLU(0.2),
            nn.Dropout(d_dropout),
            nn.Linear(d_hidden // 2, 1),
            nn.Sigmoid(),
        )

        # Premium discriminators
        if config.use_multimodal_discriminator:
            self.multimodal_disc = MultiModalDiscriminator(input_dim, config.hidden_dim)

        if config.use_hierarchical_discriminator:
            self.hierarchical_disc = HierarchicalDiscriminator(
                input_dim, config.hidden_dim
            )

        if config.use_contrastive_discriminator:
            self.contrastive_disc = ContrastiveLearningDiscriminator(
                input_dim, config.hidden_dim
            )

        if config.use_distributional_discriminator:
            self.distributional_disc = self._create_distributional_discriminator(
                input_dim
            )

        if config.use_ensemble_discriminator:
            self.ensemble_discs = nn.ModuleList(
                [
                    nn.Sequential(
                        nn.Linear(input_dim, config.hidden_dim),
                        nn.LeakyReLU(0.2),
                        nn.Linear(config.hidden_dim, 1),
                        nn.Sigmoid(),
                    )
                    for _ in range(3)
                ]
            )

    def _create_distributional_discriminator(self, input_dim: int):
        """Create discriminator based on distributional distances"""
        return nn.Sequential(
            nn.Linear(input_dim, self.config.hidden_dim),
            nn.ReLU(),
            nn.Linear(
                self.config.hidden_dim, input_dim * 2
            ),  # Mean and std for each feature
        )

    def forward(
        self, x: torch.Tensor, real_ref: Optional[torch.Tensor] = None
    ) -> Dict[str, torch.Tensor]:
        results = {}

        # Basic discriminator
        results["basic"] = self.basic_disc(x).squeeze()

        # Premium discriminators
        if self.config.use_multimodal_discriminator and hasattr(
            self, "multimodal_disc"
        ):
            results["multimodal"] = self.multimodal_disc(x, real_ref)

        if self.config.use_hierarchical_discriminator and hasattr(
            self, "hierarchical_disc"
        ):
            results["hierarchical"] = self.hierarchical_disc(x)

        if self.config.use_contrastive_discriminator and hasattr(
            self, "contrastive_disc"
        ):
            disc_score, projections = self.contrastive_disc(x)
            results["contrastive"] = disc_score
            results["projections"] = projections

        if self.config.use_ensemble_discriminator and hasattr(self, "ensemble_discs"):
            ensemble_scores = [disc(x).squeeze() for disc in self.ensemble_discs]
            results["ensemble"] = torch.mean(torch.stack(ensemble_scores), dim=0)

        return results

    def compute_gradient_penalty(
        self, real_data: torch.Tensor, fake_data: torch.Tensor
    ) -> torch.Tensor:
        """Compute gradient penalty for WGAN-GP training"""
        if not self.config.use_gradient_penalty:
            return torch.tensor(0.0, device=real_data.device)

        batch_size = real_data.size(0)
        alpha = torch.rand(batch_size, 1, device=real_data.device)
        alpha = alpha.expand_as(real_data)

        interpolated = alpha * real_data + (1 - alpha) * fake_data
        interpolated.requires_grad_(True)

        # Compute discriminator output for interpolated data
        d_interpolated = self.basic_disc(interpolated)

        # Compute gradients
        gradients = torch.autograd.grad(
            outputs=d_interpolated,
            inputs=interpolated,
            grad_outputs=torch.ones_like(d_interpolated),
            create_graph=True,
            retain_graph=True,
            only_inputs=True,
        )[0]

        # Compute gradient penalty
        gradient_norm = gradients.norm(2, dim=1)
        gradient_penalty = ((gradient_norm - 1) ** 2).mean()

        return gradient_penalty
