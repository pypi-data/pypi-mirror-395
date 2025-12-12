import torch
import torch.nn as nn
import torch.nn.functional as F
import math
from typing import Tuple, Optional
from scipy import stats
import numpy as np


class MemoryBank(nn.Module):
    """External memory bank for storing real data patterns"""

    def __init__(self, memory_size: int, feature_dim: int, input_dim: int = None):
        super().__init__()
        self.memory_size = memory_size
        self.feature_dim = feature_dim
        self.register_buffer("memory", torch.randn(memory_size, feature_dim))
        self.register_buffer("age", torch.zeros(memory_size))

        # if input_dim is provided and differs, project into feature_dim
        if input_dim is not None and input_dim != feature_dim:
            self.proj = nn.Linear(input_dim, feature_dim)
        else:
            self.proj = None

    def update(self, features: torch.Tensor):
        """Update memory with new features (will project if needed)"""
        if self.proj is not None:
            features = self.proj(features.to(self.memory.device))
        batch_size = features.size(0)
        oldest_idx = torch.argsort(self.age)[:batch_size]
        self.memory[oldest_idx] = features.detach()
        self.age[oldest_idx] = 0
        self.age += 1

    def query(self, query_features: torch.Tensor, k: int = 5) -> torch.Tensor:
        similarities = F.cosine_similarity(
            query_features.unsqueeze(1), self.memory.unsqueeze(0), dim=2
        )
        _, top_idx = similarities.topk(k, dim=1)
        return self.memory[top_idx].mean(dim=1)


class MixtureOfExperts(nn.Module):
    """Mixture of experts for specialized feature generation"""

    def __init__(self, input_dim: int, hidden_dim: int, num_experts: int = 4):
        super().__init__()
        self.num_experts = num_experts

        # Router network
        self.router = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, num_experts),
            nn.Softmax(dim=-1),
        )

        # Expert networks
        self.experts = nn.ModuleList(
            [
                nn.Sequential(
                    nn.Linear(input_dim, hidden_dim),
                    nn.ReLU(),
                    nn.Linear(hidden_dim, hidden_dim),
                )
                for _ in range(num_experts)
            ]
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Get routing weights
        router_weights = self.router(x)  # [batch, num_experts]

        # Apply experts
        expert_outputs = []
        for expert in self.experts:
            expert_outputs.append(expert(x))
        expert_outputs = torch.stack(
            expert_outputs, dim=1
        )  # [batch, num_experts, hidden]

        # Weighted combination
        output = torch.sum(router_weights.unsqueeze(-1) * expert_outputs, dim=1)
        return output


class FeatureAttention(nn.Module):
    """Cross-feature attention mechanism"""

    def __init__(self, feature_dim: int, num_heads: int = 8):
        super().__init__()
        self.num_heads = num_heads
        self.feature_dim = feature_dim
        self.head_dim = feature_dim // num_heads

        self.query = nn.Linear(feature_dim, feature_dim)
        self.key = nn.Linear(feature_dim, feature_dim)
        self.value = nn.Linear(feature_dim, feature_dim)
        self.output = nn.Linear(feature_dim, feature_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch_size, seq_len = x.size(0), x.size(1)

        # Multi-head attention
        Q = self.query(x).view(batch_size, seq_len, self.num_heads, self.head_dim)
        K = self.key(x).view(batch_size, seq_len, self.num_heads, self.head_dim)
        V = self.value(x).view(batch_size, seq_len, self.num_heads, self.head_dim)

        # Attention scores
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.head_dim)
        attention = F.softmax(scores, dim=-1)

        # Apply attention
        out = torch.matmul(attention, V)
        out = out.view(batch_size, seq_len, self.feature_dim)

        return self.output(out)


class AdversarialDisentangler(nn.Module):
    """Separate latent spaces for different feature types"""

    def __init__(self, latent_dim: int, continuous_dim: int, categorical_dim: int):
        super().__init__()
        self.continuous_encoder = nn.Sequential(
            nn.Linear(latent_dim, latent_dim // 2),
            nn.ReLU(),
            nn.Linear(latent_dim // 2, continuous_dim),
        )

        self.categorical_encoder = nn.Sequential(
            nn.Linear(latent_dim, latent_dim // 2),
            nn.ReLU(),
            nn.Linear(latent_dim // 2, categorical_dim),
        )

        # Discriminator to enforce disentanglement
        self.feature_discriminator = nn.Sequential(
            nn.Linear(continuous_dim + categorical_dim, latent_dim),
            nn.ReLU(),
            nn.Linear(latent_dim, 1),
            nn.Sigmoid(),
        )

    def forward(self, z: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        continuous_features = self.continuous_encoder(z)
        categorical_features = self.categorical_encoder(z)
        return continuous_features, categorical_features


class MultiModalDiscriminator(nn.Module):
    """Discriminator combining neural and statistical testing"""

    def __init__(self, input_dim: int, hidden_dim: int):
        super().__init__()
        # Neural component
        self.neural_disc = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.3),
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.3),
            nn.Linear(hidden_dim // 2, 1),
        )

        # Statistical testing component
        self.stat_tests = ["ks_test", "anderson_test", "chi2_test"]

    def statistical_score(
        self, real_data: torch.Tensor, fake_data: torch.Tensor
    ) -> torch.Tensor:
        """Compute statistical test scores"""
        scores = []

        real_np = real_data.detach().cpu().numpy()
        fake_np = fake_data.detach().cpu().numpy()

        for i in range(real_data.size(1)):
            try:
                # Kolmogorov-Smirnov test
                ks_stat, _ = stats.ks_2samp(real_np[:, i], fake_np[:, i])
                scores.append(ks_stat)
            except:
                scores.append(0.5)  # Fallback

        return torch.tensor(np.mean(scores), device=real_data.device)

    def forward(
        self, x: torch.Tensor, real_ref: Optional[torch.Tensor] = None
    ) -> torch.Tensor:
        neural_score = torch.sigmoid(self.neural_disc(x))

        if real_ref is not None:
            stat_score = self.statistical_score(real_ref, x)
            # Combine neural and statistical scores
            return 0.7 * neural_score.squeeze() + 0.3 * stat_score
        else:
            return neural_score.squeeze()


class HierarchicalDiscriminator(nn.Module):
    """Multi-scale discriminator at different feature granularities"""

    def __init__(self, input_dim: int, hidden_dim: int):
        super().__init__()
        # Feature-level discriminator
        self.feature_disc = nn.Sequential(
            nn.Linear(1, hidden_dim // 4),
            nn.LeakyReLU(0.2),
            nn.Linear(hidden_dim // 4, 1),
        )

        # Group-level discriminator (groups of features)
        self.group_disc = nn.Sequential(
            nn.Linear(input_dim // 2, hidden_dim // 2),
            nn.LeakyReLU(0.2),
            nn.Linear(hidden_dim // 2, 1),
        )

        # Global discriminator
        self.global_disc = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.LeakyReLU(0.2),
            nn.Linear(hidden_dim, 1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch_size = x.size(0)

        # Feature-level scores
        feature_scores = []
        for i in range(x.size(1)):
            score = self.feature_disc(x[:, i : i + 1])
            feature_scores.append(score)
        feature_score = torch.mean(torch.cat(feature_scores, dim=1), dim=1)

        # Group-level score
        mid_point = x.size(1) // 2
        group_score = self.group_disc(x[:, :mid_point]).squeeze()

        # Global score
        global_score = self.global_disc(x).squeeze()

        # Combine scores
        combined = (feature_score + group_score + global_score) / 3
        return torch.sigmoid(combined)


class ContrastiveLearningDiscriminator(nn.Module):
    """Self-supervised representation learning discriminator"""

    def __init__(self, input_dim: int, hidden_dim: int, projection_dim: int = 128):
        super().__init__()
        # Encoder
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
        )

        # Projection head for contrastive learning
        self.projection_head = nn.Sequential(
            nn.Linear(hidden_dim // 2, projection_dim),
            nn.ReLU(),
            nn.Linear(projection_dim, projection_dim),
        )

        # Discriminator head
        self.discriminator_head = nn.Sequential(
            nn.Linear(hidden_dim // 2, 1), nn.Sigmoid()
        )

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        # Get representations
        representations = self.encoder(x)

        # Get projections for contrastive learning
        projections = self.projection_head(representations)

        # Get discriminator scores
        disc_scores = self.discriminator_head(representations).squeeze()

        return disc_scores, projections
