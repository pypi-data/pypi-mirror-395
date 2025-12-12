import torch
from sklearn.mixture import GaussianMixture


class TVAESampler:
    def __init__(self, config):
        self.config = config
        self.latent_dim = config.latent_dim
        self.gmm = None  # Will be set after training

    def set_gmm(self, gmm: GaussianMixture):
        """Attach trained GMM model after training."""
        self.gmm = gmm

    def sample(self, n_samples, device=None, use_gmm=False):
        """Sample latent vectors for generation.

        Args:
            n_samples (int): Number of samples to generate
            device (torch.device): Torch device
            use_gmm (bool): Whether to use GMM if available

        Returns:
            torch.Tensor: Latent vectors [n_samples, latent_dim]
        """
        if device is None:
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # GMM sampling
        if use_gmm and self.gmm is not None:
            try:
                z_np = self.gmm.sample(n_samples)[0]  # [n_samples, latent_dim]
                return torch.tensor(z_np, dtype=torch.float32).to(device)
            except Exception as e:
                print(f"⚠️ GMM sampling failed: {e}. Falling back to standard normal.")

        # Standard normal fallback
        return torch.randn(n_samples, self.latent_dim).to(device)
