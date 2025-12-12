import torch
import numpy as np
from sklearn.mixture import GaussianMixture
from sklearn.cluster import KMeans


class GMMLatentSampler:
    """Gaussian Mixture Model for latent sampling"""

    def __init__(self, n_components: int = 8):
        self.n_components = n_components
        self.gmm = None

    def fit(self, real_data: np.ndarray):
        """Fit GMM to real data distribution"""
        self.gmm = GaussianMixture(n_components=self.n_components, random_state=42)
        self.gmm.fit(real_data)

    def sample(
        self, n_samples: int, latent_dim: int, device: torch.device
    ) -> torch.Tensor:
        """Sample from learned distribution"""
        if self.gmm is None:
            # Fallback to standard normal sampling
            return torch.randn(n_samples, latent_dim, device=device)

        try:
            samples, _ = self.gmm.sample(n_samples)
            # Pad or truncate to match latent_dim
            if samples.shape[1] < latent_dim:
                padding = np.random.randn(n_samples, latent_dim - samples.shape[1])
                samples = np.concatenate([samples, padding], axis=1)
            elif samples.shape[1] > latent_dim:
                samples = samples[:, :latent_dim]
            return torch.tensor(samples, dtype=torch.float32, device=device)
        except:
            return torch.randn(n_samples, latent_dim, device=device)


class ClusteredConditionalSampler:
    """Sample based on discovered data clusters"""

    def __init__(self, n_clusters: int = 5):
        self.n_clusters = n_clusters
        self.kmeans = None
        self.cluster_centers = None

    def fit(self, real_data: np.ndarray):
        """Discover clusters in real data"""
        self.kmeans = KMeans(n_clusters=self.n_clusters, random_state=42)
        self.kmeans.fit(real_data)
        self.cluster_centers = self.kmeans.cluster_centers_

    def sample(
        self, n_samples: int, latent_dim: int, device: torch.device
    ) -> torch.Tensor:
        """Sample conditioned on clusters"""
        if self.cluster_centers is None:
            return torch.randn(n_samples, latent_dim, device=device)

        # Randomly select clusters
        cluster_ids = np.random.choice(self.n_clusters, n_samples)
        samples = []

        for cluster_id in cluster_ids:
            # Sample around cluster center
            center = self.cluster_centers[cluster_id]
            if len(center) >= latent_dim:
                base = center[:latent_dim]
            else:
                base = np.pad(center, (0, latent_dim - len(center)), "constant")

            # Add noise around center
            noise = np.random.randn(latent_dim) * 0.1
            sample = base + noise
            samples.append(sample)

        return torch.tensor(np.array(samples), dtype=torch.float32, device=device)
