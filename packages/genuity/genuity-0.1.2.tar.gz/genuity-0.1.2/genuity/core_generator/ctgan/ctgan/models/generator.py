import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List
from ..config.config import CTGANConfig


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


class CTGANGenerator(nn.Module):
    """Improved CTGAN generator with better accuracy and stability"""

    def __init__(self, config: CTGANConfig):
        super().__init__()
        self.config = config
        self.latent_dim = config.latent_dim
        self.hidden_dim = config.hidden_dim

        # Feature dimensions
        self.continuous_dim = len(config.continuous_dims)
        self.categorical_dims = config.categorical_dims
        self.output_dim = self.continuous_dim + sum(self.categorical_dims)

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

    def forward(self, z: torch.Tensor, hard_categorical: bool = False) -> torch.Tensor:
        """
        Generate synthetic data from latent vector

        Args:
            z: latent vector (batch_size, latent_dim)
            hard_categorical: if True, convert categorical soft-probs to hard one-hot
        """
        # Core forward pass
        x = self.core(z)
        output = self.output_layer(x)

        # Handle categorical features
        if self.categorical_dims:
            continuous_part = output[:, : self.continuous_dim]
            categorical_part = output[:, self.continuous_dim :]

            # Split categorical part into chunks
            categorical_outputs = []
            start_idx = 0
            
            for dim in self.categorical_dims:
                end_idx = start_idx + dim
                chunk = categorical_part[:, start_idx:end_idx]
                
                if dim > 1:
                    # Multi-class: Softmax
                    probs = F.softmax(chunk, dim=1)
                    if hard_categorical:
                        indices = torch.argmax(probs, dim=1, keepdim=True)
                        onehot = torch.zeros_like(chunk)
                        onehot.scatter_(1, indices, 1)
                        categorical_outputs.append(onehot)
                    else:
                        categorical_outputs.append(probs)
                else:
                    # Binary (if represented as 1 dim): Sigmoid
                    # But usually binary is 2 dims in one-hot. 
                    # If dim=1, it's sigmoid.
                    probs = torch.sigmoid(chunk)
                    if hard_categorical:
                        categorical_outputs.append(torch.round(probs))
                    else:
                        categorical_outputs.append(probs)
                
                start_idx = end_idx
            
            categorical_combined = torch.cat(categorical_outputs, dim=1)
            output = torch.cat([continuous_part, categorical_combined], dim=1)

        return output
