import torch
import torch.nn as nn
import torch.optim as optim
from ..models.encoder import TVAEEncoder
from ..models.decoder import TVAEDecoder
from ..models.components import (
    VampPrior,
    BetaDivergenceLoss,
    BetaVAE,
    MultiHeadDecoder,
    TransformerAttention,
    GMMLatentClustering,
    CyclicalKLAnnealing,
    GradientNoiseInjection,
    WassersteinLoss,
    QualityGatingSystem,
)
from ..samplers.sampler import TVAESampler


class TVAETrainer:
    def __init__(self, config):
        self.config = config
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.n_cont = len(config.continuous_dims)
        self.n_cat = len(config.categorical_dims)
        self.input_dim = self.n_cont + self.n_cat
        self.latent_dim = config.latent_dim
        self.encoder = TVAEEncoder(self.input_dim, self.latent_dim, config).to(
            self.device
        )
        self.decoder = TVAEDecoder(
            self.latent_dim, self.input_dim, config, self.n_cont, self.n_cat
        ).to(self.device)
        self.sampler = TVAESampler(config)
        self.optimizer = optim.Adam(
            list(self.encoder.parameters()) + list(self.decoder.parameters()),
            lr=config.learning_rate,
        )
        # Advanced features
        self.beta_loss = BetaDivergenceLoss() if config.use_beta_divergence else None
        self.wasserstein_loss = (
            WassersteinLoss() if config.use_wasserstein_loss else None
        )
        self.kl_annealing = (
            CyclicalKLAnnealing(config) if config.use_cyclical_kl else None
        )
        self.gradient_noise = (
            GradientNoiseInjection(config) if config.use_gradient_noise else None
        )
        self.quality_gating = (
            QualityGatingSystem(config) if config.use_quality_gating else None
        )

    def fit(self, data, epochs=1000, verbose=True):
        data = torch.tensor(data, dtype=torch.float32, device=self.device)
        losses = {"recon": [], "kl": [], "total": [], "kl_weight": []}

        for epoch in range(epochs):
            self.encoder.train()
            self.decoder.train()
            self.optimizer.zero_grad()

            mu, logvar = self.encoder(data)
            std = torch.exp(0.5 * logvar)
            eps = torch.randn_like(std)
            z = mu + eps * std

            # Decode
            if self.config.use_multi_head_decoder:
                try:
                    recon_cont, recon_cat = self.decoder(z)
                    recon = torch.cat([recon_cont, recon_cat], dim=1)
                except Exception as e:
                    print(f"⚠️ Multi-head decoder failed: {e}. Falling back to standard decoder.")
                    recon = self.decoder(z)
            else:
                recon = self.decoder(z)

            # Reconstruction loss
            recon_loss = nn.MSELoss()(recon, data)

            # KL loss
            if self.config.use_vampprior:
                try:
                    prior_mu, prior_logvar = self.encoder.get_vampprior()
                    kl_loss = self._kl_divergence(mu, logvar, prior_mu, prior_logvar)
                except Exception as e:
                    print(f"⚠️ VampPrior failed: {e}. Falling back to standard KL.")
                    kl_loss = (
                        -0.5
                        * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
                        / data.size(0)
                    )
            else:
                kl_loss = (
                    -0.5
                    * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
                    / data.size(0)
                )

            # KL annealing to prevent posterior collapse
            kl_weight = self._compute_kl_weight(epoch, epochs)

            # Apply β-VAE weighting
            if self.config.use_beta_divergence:
                kl_loss = self.config.beta * kl_loss

            # Monitor and prevent posterior collapse
            if epoch > 50 and kl_loss.item() < 1e-4:
                # If KL is too small, increase the weight temporarily
                kl_weight = min(kl_weight * 2.0, 2.0)

            # Advanced losses
            if self.wasserstein_loss:
                try:
                    w_loss = self.wasserstein_loss(recon, data)
                    total_loss = recon_loss + kl_weight * kl_loss + w_loss
                except Exception as e:
                    print(f"⚠️ Wasserstein loss failed: {e}. Using standard loss.")
                    total_loss = recon_loss + kl_weight * kl_loss
            else:
                total_loss = recon_loss + kl_weight * kl_loss

            # Additional annealing if configured
            if self.kl_annealing:
                try:
                    annealing_factor = self.kl_annealing(epoch)
                    total_loss *= annealing_factor
                except Exception as e:
                    print(f"⚠️ KL annealing failed: {e}. Skipping annealing.")

            if self.gradient_noise:
                try:
                    noise = self.gradient_noise(total_loss, epoch)
                    total_loss += noise
                except Exception as e:
                    print(f"⚠️ Gradient noise injection failed: {e}. Skipping noise.")

            total_loss.backward()
            self.optimizer.step()

            losses["recon"].append(recon_loss.item())
            losses["kl"].append(kl_loss.item())
            losses["total"].append(total_loss.item())
            losses["kl_weight"].append(kl_weight)

            if verbose and (epoch % 100 == 0 or epoch == epochs - 1):
                print(
                    f"Epoch {epoch}: Recon {recon_loss.item():.4f}, KL {kl_loss.item():.4f}, "
                    f"KL Weight {kl_weight:.4f}, Total {total_loss.item():.4f}"
                )
        return losses

    def generate(self, n_samples):
        self.encoder.eval()
        self.decoder.eval()
        with torch.no_grad():
            z = self.sampler.sample(n_samples, device=self.device)
            if self.config.use_multi_head_decoder:
                try:
                    cont, cat = self.decoder(z)
                    samples = torch.cat([cont, cat], dim=1)
                except Exception as e:
                    print(f"⚠️ Multi-head decoder failed during generation: {e}. Using standard decoder.")
                    samples = self.decoder(z)
            else:
                samples = self.decoder(z)
            samples = samples.cpu().numpy()
            # Robust categorical assignment
            if self.n_cat > 0:
                samples[:, self.n_cont :] = self._assign_categorical(
                    samples[:, self.n_cont :]
                )
            if self.quality_gating:
                try:
                    samples = self.quality_gating(samples)
                except Exception as e:
                    print(f"⚠️ Quality gating failed: {e}. Returning samples without gating.")
            return samples

    def save_model(self, filepath):
        torch.save(
            {
                "encoder": self.encoder.state_dict(),
                "decoder": self.decoder.state_dict(),
            },
            filepath,
        )

    def load_model(self, filepath):
        checkpoint = torch.load(filepath, map_location=self.device)
        self.encoder.load_state_dict(checkpoint["encoder"])
        self.decoder.load_state_dict(checkpoint["decoder"])

    def get_feature_importance(self):
        # Placeholder: could use mutual information or decoder weights
        return {}

    def _kl_divergence(self, mu, logvar, prior_mu=None, prior_logvar=None):
        if prior_mu is not None and prior_logvar is not None:
            # VampPrior KL - compute KL for each pseudo-input and take the minimum
            batch_size = mu.size(0)
            num_pseudos = prior_mu.size(0)

            # Expand mu and logvar to match prior dimensions for broadcasting
            mu_expanded = mu.unsqueeze(1).expand(
                -1, num_pseudos, -1
            )  # (batch_size, num_pseudos, latent_dim)
            logvar_expanded = logvar.unsqueeze(1).expand(
                -1, num_pseudos, -1
            )  # (batch_size, num_pseudos, latent_dim)
            prior_mu_expanded = prior_mu.unsqueeze(0).expand(
                batch_size, -1, -1
            )  # (batch_size, num_pseudos, latent_dim)
            prior_logvar_expanded = prior_logvar.unsqueeze(0).expand(
                batch_size, -1, -1
            )  # (batch_size, num_pseudos, latent_dim)

            # Compute KL divergence for each pseudo-input
            kl_per_pseudo = 0.5 * (
                prior_logvar_expanded
                - logvar_expanded
                + (logvar_expanded.exp() + (mu_expanded - prior_mu_expanded).pow(2))
                / prior_logvar_expanded.exp()
                - 1
            )  # (batch_size, num_pseudos, latent_dim)

            # Sum over latent dimensions and take minimum over pseudo-inputs
            kl_per_sample = torch.sum(kl_per_pseudo, dim=2)  # (batch_size, num_pseudos)
            kl_min = torch.min(kl_per_sample, dim=1)[0]  # (batch_size,)

            # Return mean over batch
            return torch.mean(kl_min)
        else:
            # Standard Gaussian KL
            return -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp()) / mu.size(0)

    def _compute_kl_weight(self, epoch, total_epochs):
        """Compute KL weight with warmup to prevent posterior collapse"""
        if epoch < self.config.warmup_epochs:
            # Linear warmup from 0 to max_kl_weight
            return (epoch / self.config.warmup_epochs) * self.config.max_kl_weight
        else:
            return self.config.max_kl_weight

    def _assign_categorical(self, cat_logits):
        # Assign each row to the most probable class for each categorical feature
        return (cat_logits == cat_logits.max(axis=1, keepdims=True)).astype(float)
