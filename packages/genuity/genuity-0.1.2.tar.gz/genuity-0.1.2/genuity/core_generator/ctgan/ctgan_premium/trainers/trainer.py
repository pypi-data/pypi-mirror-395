import torch
import torch.nn.functional as F
import numpy as np
from collections import defaultdict
from typing import Dict, List, Union
import logging

from ..config.config import CTGANPremiumConfig
from ..models.generator import CTGANPremiumGenerator
from ..models.discriminator import CTGANPremiumDiscriminator
from ..samplers.sampler import CTGANPremiumSampler
from .training_strategies import CurriculumLearner, ParetoOptimizer, ProgressiveTrainer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CTGANPremiumTrainer:
    """Premium CTGAN trainer with all advanced features"""

    def __init__(self, config: CTGANPremiumConfig):
        self.config = config
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Initialize components
        self.generator = CTGANPremiumGenerator(config).to(self.device)
        self.discriminator = CTGANPremiumDiscriminator(config).to(self.device)
        self.sampler = CTGANPremiumSampler(config)

        # Optimizers
        self.g_optimizer = torch.optim.Adam(
            self.generator.parameters(), lr=config.learning_rate, betas=(0.5, 0.999)
        )
        self.d_optimizer = torch.optim.Adam(
            self.discriminator.parameters(), lr=config.learning_rate, betas=(0.5, 0.999)
        )

        # Premium training features
        if config.use_curriculum_learning:
            self.curriculum_learner = CurriculumLearner()

        if config.use_pareto_optimization:
            self.pareto_optimizer = ParetoOptimizer(
                ["generator_loss", "discriminator_loss", "diversity_loss"]
            )

        if config.use_progressive_training:
            self.progressive_trainer = ProgressiveTrainer()

        # Loss tracking
        self.losses = defaultdict(list)
        self.uncertainty_weights = torch.ones(
            len(config.continuous_dims + config.categorical_dims)
        ).to(self.device)

    def compute_contrastive_loss(
        self,
        projections_real: torch.Tensor,
        projections_fake: torch.Tensor,
        temperature: float = 0.07,
    ) -> torch.Tensor:
        """Compute contrastive loss for discriminator training"""
        # Normalize projections
        projections_real = F.normalize(projections_real, dim=1)
        projections_fake = F.normalize(projections_fake, dim=1)

        # Compute similarity matrix
        logits = torch.matmul(projections_real, projections_fake.T) / temperature

        # Labels (diagonal should be positive pairs)
        batch_size = projections_real.size(0)
        labels = torch.arange(batch_size).to(self.device)

        # Contrastive loss
        loss = F.cross_entropy(logits, labels)
        return loss

    def compute_diversity_loss(self, generated_samples: torch.Tensor) -> torch.Tensor:
        """Compute diversity loss to prevent mode collapse"""
        # Compute pairwise distances
        distances = torch.cdist(generated_samples, generated_samples, p=2)

        # Encourage diversity by maximizing minimum distance
        min_distances = torch.min(
            distances + torch.eye(distances.size(0), device=self.device) * 1e6, dim=1
        )[0]
        diversity_loss = -torch.mean(min_distances)

        return diversity_loss

    def compute_uncertainty_weights(
        self, real_data: torch.Tensor, fake_data: torch.Tensor
    ):
        """Update uncertainty weights based on feature-wise performance"""
        if not self.config.use_uncertainty_weighting:
            return

        # Compute feature-wise differences
        feature_diffs = torch.abs(real_data.mean(dim=0) - fake_data.mean(dim=0))

        # Update weights (higher weight for more uncertain features)
        self.uncertainty_weights = 0.9 * self.uncertainty_weights + 0.1 * (
            1 + feature_diffs
        )

    def train_step(self, real_data: torch.Tensor, epoch: int) -> Dict[str, float]:
        """Single training step with all premium features"""
        batch_size = real_data.size(0)
        losses = {}

        # Get current difficulty and stage
        difficulty = 1.0
        stage = -1

        if self.config.use_curriculum_learning and hasattr(self, "curriculum_learner"):
            difficulty = self.curriculum_learner.get_difficulty()

        if self.config.use_progressive_training and hasattr(
            self, "progressive_trainer"
        ):
            stage = self.progressive_trainer.get_current_stage()
            self.progressive_trainer.current_epoch += 1

        # Sample latent codes
        z = self.sampler.sample(batch_size, self.device, difficulty)
        # Generate fake data
        fake_data = self.generator(z, stage)

        # Update memory bank if enabled
        if self.config.use_memory_augmented and hasattr(self.generator, "memory_bank"):
            # Extract features for memory bank update
            with torch.no_grad():
                # Use a simple projection to get features for memory bank
                real_features = torch.mean(real_data, dim=1, keepdim=True).expand(
                    real_data.size(0), self.config.hidden_dim
                )
                self.generator.memory_bank.update(real_features)

        # Train Discriminator
        self.d_optimizer.zero_grad()

        # Real data discrimination
        real_scores = self.discriminator(real_data, real_data)
        fake_scores = self.discriminator(fake_data.detach())

        # Compute discriminator losses
        d_loss_real = 0
        d_loss_fake = 0

        for key in real_scores:
            if key == "projections":
                continue
            real_loss = F.binary_cross_entropy(
                real_scores[key], torch.ones_like(real_scores[key])
            )
            fake_loss = F.binary_cross_entropy(
                fake_scores[key], torch.zeros_like(fake_scores[key])
            )

            d_loss_real += real_loss
            d_loss_fake += fake_loss

        d_loss = (d_loss_real + d_loss_fake) / len(
            [k for k in real_scores.keys() if k != "projections"]
        )

        # Add gradient penalty if enabled
        if self.config.use_gradient_penalty:
            gradient_penalty = self.discriminator.compute_gradient_penalty(
                real_data, fake_data.detach()
            )
            d_loss += self.config.gradient_penalty_weight * gradient_penalty
            losses["gradient_penalty"] = gradient_penalty.item()

        # Add contrastive loss if enabled
        if (
            self.config.use_contrastive_training
            and "projections" in real_scores
            and "projections" in fake_scores
        ):
            contrastive_loss = self.compute_contrastive_loss(
                real_scores["projections"], fake_scores["projections"]
            )
            d_loss += 0.1 * contrastive_loss
            losses["contrastive_loss"] = contrastive_loss.item()

        d_loss.backward()
        self.d_optimizer.step()

        # Train Generator
        self.g_optimizer.zero_grad()

        # Generate new fake data
        z = self.sampler.sample(batch_size, self.device, difficulty)
        fake_data = self.generator(z, stage)

        # Get discriminator scores for fake data
        fake_scores = self.discriminator(fake_data)

        # Compute generator loss
        g_loss = 0
        for key in fake_scores:
            if key == "projections":
                continue
            loss = F.binary_cross_entropy(
                fake_scores[key], torch.ones_like(fake_scores[key])
            )

            # Apply uncertainty weighting
            if self.config.use_uncertainty_weighting:
                # Feature-wise weighting (simplified)
                weighted_loss = loss * self.uncertainty_weights.mean()
                g_loss += weighted_loss
            else:
                g_loss += loss

        g_loss = g_loss / len([k for k in fake_scores.keys() if k != "projections"])

        # Add diversity loss
        diversity_loss = self.compute_diversity_loss(fake_data)
        g_loss += self.config.diversity_loss_weight * diversity_loss

        g_loss.backward()

        # Update hard samples for mining
        if hasattr(self.sampler, "update_hard_samples"):
            with torch.no_grad():
                sample_losses = F.binary_cross_entropy(
                    fake_scores["basic"],
                    torch.ones_like(fake_scores["basic"]),
                    reduction="none",
                )
                self.sampler.update_hard_samples(z, sample_losses)

        self.g_optimizer.step()

        # Update uncertainty weights
        self.compute_uncertainty_weights(real_data, fake_data.detach())

        # Update curriculum difficulty
        if self.config.use_curriculum_learning and hasattr(self, "curriculum_learner"):
            # Use discriminator accuracy as performance metric
            with torch.no_grad():
                real_acc = (real_scores["basic"] > 0.5).float().mean()
                fake_acc = (fake_scores["basic"] < 0.5).float().mean()
                overall_acc = (real_acc + fake_acc) / 2
                self.curriculum_learner.update_difficulty(overall_acc.item())

        # Progressive training stage advancement
        if self.config.use_progressive_training and hasattr(
            self, "progressive_trainer"
        ):
            if self.progressive_trainer.should_advance_stage():
                self.progressive_trainer.advance_stage()
                logger.info(
                    f"Advanced to training stage {self.progressive_trainer.current_stage}"
                )

        # Store losses
        losses.update(
            {
                "generator_loss": g_loss.item(),
                "discriminator_loss": d_loss.item(),
                "diversity_loss": diversity_loss.item(),
                "d_loss_real": d_loss_real.item(),
                "d_loss_fake": d_loss_fake.item(),
            }
        )

        # Pareto optimization
        if self.config.use_pareto_optimization and hasattr(self, "pareto_optimizer"):
            self.pareto_optimizer.update_pareto_front(losses)

        return losses

    def fit(
        self, real_data: np.ndarray, epochs: int = 1000, verbose: bool = True
    ) -> Dict[str, List[float]]:
        """Train the model with all premium features"""
        real_data = np.array(real_data, dtype=np.float32)
        real_tensor = torch.tensor(real_data, dtype=torch.float32).to(self.device)

        # Fit samplers
        self.sampler.fit(real_data)

        # Training loop
        for epoch in range(epochs):
            # Create batches
            n_samples = real_tensor.size(0)
            indices = torch.randperm(n_samples)

            epoch_losses = defaultdict(list)

            for i in range(0, n_samples, self.config.batch_size):
                end_idx = min(i + self.config.batch_size, n_samples)
                batch_indices = indices[i:end_idx]
                batch_data = real_tensor[batch_indices]

                # Skip if batch too small
                if batch_data.size(0) < 2:
                    continue

                # Training step
                step_losses = self.train_step(batch_data, epoch)

                # Accumulate losses
                for key, value in step_losses.items():
                    epoch_losses[key].append(value)

            # Average epoch losses
            for key, values in epoch_losses.items():
                if values:  # Check if list is not empty
                    avg_loss = np.mean(values)
                    self.losses[key].append(avg_loss)

            # Verbose logging
            if verbose and epoch % 100 == 0:
                log_msg = f"Epoch {epoch}:"
                for key, values in self.losses.items():
                    if values:  # Check if list is not empty
                        log_msg += f" {key}={values[-1]:.4f}"

                if self.config.use_curriculum_learning and hasattr(
                    self, "curriculum_learner"
                ):
                    log_msg += (
                        f" difficulty={self.curriculum_learner.get_difficulty():.3f}"
                    )

                if self.config.use_progressive_training and hasattr(
                    self, "progressive_trainer"
                ):
                    log_msg += f" stage={self.progressive_trainer.get_current_stage()}"

                logger.info(log_msg)

        return dict(self.losses)

    def generate(
        self, n_samples: int, return_numpy: bool = True
    ) -> Union[torch.Tensor, np.ndarray]:
        """Generate synthetic samples"""
        self.generator.eval()

        with torch.no_grad():
            # Sample latent codes
            z = self.sampler.sample(n_samples, self.device)

            # Generate samples with hard categorical for inference
            fake_data = self.generator(z, hard_categorical=True)

        self.generator.train()

        if return_numpy:
            return fake_data.cpu().numpy()
        return fake_data

    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance scores"""
        importances = {}

        if self.config.use_uncertainty_weighting:
            weights = self.uncertainty_weights.cpu().numpy()
            for i, dim in enumerate(
                self.config.continuous_dims + self.config.categorical_dims
            ):
                importances[f"feature_{dim}"] = (
                    float(weights[i]) if i < len(weights) else 1.0
                )

        return importances

    def save_model(self, filepath: str):
        """Save the trained model"""
        torch.save(
            {
                "generator_state_dict": self.generator.state_dict(),
                "discriminator_state_dict": self.discriminator.state_dict(),
                "config": self.config,
                "losses": dict(self.losses),
            },
            filepath,
        )

    def load_model(self, filepath: str):
        """Load a trained model"""
        checkpoint = torch.load(filepath, map_location=self.device)
        self.generator.load_state_dict(checkpoint["generator_state_dict"])
        self.discriminator.load_state_dict(checkpoint["discriminator_state_dict"])
        self.losses = defaultdict(list, checkpoint["losses"])
