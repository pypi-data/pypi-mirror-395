import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List
from ..config.config import CTGANPremiumConfig
from .components import (
    MemoryBank,
    MixtureOfExperts,
    FeatureAttention,
    AdversarialDisentangler,
)


class ResidualBlock(nn.Module):
    """Improved residual block with better gradient flow"""

    def __init__(self, dim_in: int, dim_out: int, use_spectral_norm: bool = True):
        super().__init__()

        # Apply spectral normalization if requested
        if use_spectral_norm:
            self.fc1 = nn.utils.spectral_norm(nn.Linear(dim_in, dim_out))
            self.fc2 = nn.utils.spectral_norm(nn.Linear(dim_out, dim_out))
        else:
            self.fc1 = nn.Linear(dim_in, dim_out)
            self.fc2 = nn.Linear(dim_out, dim_out)

        self.ln1 = nn.LayerNorm(dim_out)
        self.ln2 = nn.LayerNorm(dim_out)
        self.act = nn.LeakyReLU(0.2, inplace=True)
        self.dropout = nn.Dropout(0.1)  # Light dropout

        # Skip connection
        if dim_in != dim_out:
            if use_spectral_norm:
                self.skip = nn.utils.spectral_norm(nn.Linear(dim_in, dim_out))
            else:
                self.skip = nn.Linear(dim_in, dim_out)
        else:
            self.skip = nn.Identity()

    def forward(self, x):
        residual = self.skip(x)

        out = self.fc1(x)
        out = self.ln1(out)
        out = self.act(out)
        out = self.dropout(out)

        out = self.fc2(out)
        out = self.ln2(out)

        return self.act(out + residual)


class CTGANPremiumGenerator(nn.Module):
    """Premium CTGAN generator with all advanced features"""

    def __init__(self, config: CTGANPremiumConfig):
        super().__init__()
        self.config = config
        self.latent_dim = config.latent_dim
        self.hidden_dim = config.hidden_dim

        # Feature dimensions
        self.continuous_dim = len(config.continuous_dims)
        self.categorical_dim = len(config.categorical_dims)
        self.output_dim = self.continuous_dim + self.categorical_dim

        # Core generator network with residual blocks
        blocks = []
        in_dim = self.latent_dim

        for i in range(config.num_layers):
            blocks.append(
                ResidualBlock(
                    in_dim, self.hidden_dim, use_spectral_norm=config.use_spectral_norm
                )
            )
            in_dim = self.hidden_dim

        self.core = nn.Sequential(*blocks)

        # Output layer
        if config.use_spectral_norm:
            self.output_layer = nn.utils.spectral_norm(
                nn.Linear(self.hidden_dim, self.output_dim)
            )
        else:
            self.output_layer = nn.Linear(self.hidden_dim, self.output_dim)

        # Premium features
        if config.use_mixture_of_experts:
            self.moe = MixtureOfExperts(self.hidden_dim, self.hidden_dim)

        if config.use_memory_augmented:
            mem_size = getattr(config, "memory_size", 1000)
            self.memory_bank = MemoryBank(
                memory_size=mem_size,
                feature_dim=self.hidden_dim,
                input_dim=self.hidden_dim,  # Use hidden_dim instead of output_dim
            )

        if config.use_feature_attention:
            # Find a suitable number of heads
            for h in [8, 4, 2, 1]:
                if self.output_dim % h == 0:
                    num_heads = h
                    break
            else:
                num_heads = 1
            self.attention = FeatureAttention(self.output_dim, num_heads=num_heads)

        if config.use_adversarial_disentanglement:
            self.disentangler = AdversarialDisentangler(
                self.latent_dim, self.continuous_dim, self.categorical_dim
            )

        # Progressive generation
        if config.use_progressive_generation:
            self.progressive_layers = nn.ModuleList()
            for factor in [4, 2, 1]:
                self.progressive_layers.append(
                    nn.Sequential(
                        nn.Linear(self.hidden_dim, self.hidden_dim // factor),
                        nn.ReLU(),
                        nn.Linear(self.hidden_dim // factor, self.output_dim),
                    )
                )

    def forward(
        self, z: torch.Tensor, stage: int = -1, hard_categorical: bool = False
    ) -> torch.Tensor:
        """
        Generate synthetic data from latent vector

        Args:
            z: latent vector (batch_size, latent_dim)
            stage: which progressive stage to use; -1 means normal output_layer
            hard_categorical: if True, convert categorical soft-probs to hard one-hot
        """
        # Core forward pass
        x = self.core(z)

        # Apply premium features
        if self.config.use_mixture_of_experts and hasattr(self, "moe"):
            x = x + 0.2 * self.moe(x)

        if self.config.use_memory_augmented and hasattr(self, "memory_bank"):
            memory_features = self.memory_bank.query(x)
            x = x + 0.1 * memory_features

        # Progressive generation
        if self.config.use_progressive_generation and hasattr(
            self, "progressive_layers"
        ):
            if stage >= 0 and stage < len(self.progressive_layers):
                output = self.progressive_layers[stage](x)
            else:
                output = self.output_layer(x)
        else:
            output = self.output_layer(x)

        # Feature attention
        if self.config.use_feature_attention and hasattr(self, "attention"):
            output = output.unsqueeze(1)  # Add sequence dimension
            output = self.attention(output)
            output = output.squeeze(1)  # Remove sequence dimension

        # Handle categorical features
        if self.categorical_dim > 0:
            continuous_part = output[:, : self.continuous_dim]
            categorical_part = output[:, self.continuous_dim :]

            # Apply softmax for categorical features
            if self.categorical_dim > 1:
                # Multi-class categorical features
                cat_probs = F.softmax(categorical_part, dim=1)

                if hard_categorical:
                    # Convert to hard one-hot for inference
                    cat_indices = torch.argmax(cat_probs, dim=1, keepdim=True)
                    cat_onehot = torch.zeros_like(categorical_part)
                    cat_onehot.scatter_(1, cat_indices, 1)
                    categorical_part = cat_onehot
                else:
                    # Keep soft probabilities for training
                    categorical_part = cat_probs
            else:
                # Binary categorical features
                cat_probs = torch.sigmoid(categorical_part)

                if hard_categorical:
                    categorical_part = torch.round(cat_probs)
                else:
                    categorical_part = cat_probs

            output = torch.cat([continuous_part, categorical_part], dim=1)

        return output
