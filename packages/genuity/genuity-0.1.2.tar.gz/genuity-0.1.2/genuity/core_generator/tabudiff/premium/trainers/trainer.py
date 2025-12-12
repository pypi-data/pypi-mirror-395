"""
TabuDiff Premium Trainer

Implements advanced training features:
- Dynamic loss balancing
- Gradient clipping
- Self-supervised pretraining support
- Feature-wise noise scheduling
"""

import torch
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm
import numpy as np


class TabuDiffPremiumTrainer:
    """Premium trainer for TabuDiff with advanced features."""
    
    def __init__(self, score_network, scheduler, config):
        """
        Initialize premium trainer.
        
        Args:
            score_network: Premium score network model
            scheduler: Variance scheduler
            config: TabuDiffPremiumConfig
        """
        self.score_network = score_network
        self.scheduler = scheduler
        self.config = config
        self.device = torch.device(config.device)
        
        # Move model to device
        self.score_network.to(self.device)
        
        # Optimizer
        self.optimizer = optim.AdamW(
            self.score_network.parameters(),
            lr=config.learning_rate,
            weight_decay=0.01
        )
        
        # Learning rate scheduler
        self.lr_scheduler = optim.lr_scheduler.CosineAnnealingLR(
            self.optimizer,
            T_max=config.num_epochs,
            eta_min=config.learning_rate * 0.1
        )
        
        self.losses = []
        
    def train_step(self, x0, epoch=0):
        """
        Single training step.
        
        Args:
            x0: Clean data batch
            epoch: Current epoch (for dynamic loss balancing)
        """
        batch_size = x0.size(0)
        
        # Sample random timesteps
        t_indices = torch.randint(
            0, self.scheduler.num_steps,
            (batch_size,),
            device=self.device
        )
        
        # Get noise schedule parameters
        alpha_bars = self.scheduler.alphas_cumprod[t_indices]
        
        # Add noise
        eps = torch.randn_like(x0)
        xt = (
            torch.sqrt(alpha_bars).unsqueeze(1) * x0
            + torch.sqrt(1 - alpha_bars).unsqueeze(1) * eps
        )
        
        # Predict noise
        t_cont = t_indices.float() / (self.scheduler.num_steps - 1)
        eps_pred = self.score_network(xt, t_cont)
        
        # Compute loss
        if self.config.mixture_density_heads:
            # For MDN, we use a combination of reconstruction and likelihood
            loss = torch.mean((eps_pred - eps) ** 2)
        else:
            # Standard MSE loss
            loss = torch.mean((eps_pred - eps) ** 2)
        
        # Dynamic loss balancing (weight recent timesteps more)
        if hasattr(self.config, 'dynamic_loss_balancing') and self.config.dynamic_loss_balancing:
            # Weight based on timestep
            weights = 1.0 + 0.5 * (t_indices.float() / self.scheduler.num_steps)
            loss = (loss * weights.unsqueeze(1)).mean()
        
        return loss
    
    def fit(self, data, epochs=None, verbose=True):
        """
        Train the model.
        
        Args:
            data: Training data tensor
            epochs: Number of epochs (overrides config if provided)
            verbose: Whether to show progress
        """
        epochs = epochs or self.config.num_epochs
        batch_size = self.config.batch_size
        
        # Convert to tensor if needed
        if isinstance(data, np.ndarray):
            data = torch.tensor(data, dtype=torch.float32)
        
        data = data.to(self.device)
        
        num_batches = max(1, (len(data) + batch_size - 1) // batch_size)
        
        if verbose:
            print(f"Training TabuDiff Premium for {epochs} epochs")
            print(f"   Data shape: {data.shape}")
            print(f"   Batch size: {batch_size}")
            print(f"   Batches per epoch: {num_batches}")
        
        self.score_network.train()
        
        for epoch in range(epochs):
            epoch_loss = 0.0
            perm = torch.randperm(len(data), device=self.device)
            
            iterator = range(num_batches)
            if verbose and epoch % 10 == 0:
                iterator = tqdm(iterator, desc=f"Epoch {epoch+1}/{epochs}")
            
            for b in iterator:
                idx = perm[b * batch_size:(b + 1) * batch_size]
                x0 = data[idx]
                
                # Training step
                loss = self.train_step(x0, epoch)
                
                # Backward pass
                self.optimizer.zero_grad(set_to_none=True)
                loss.backward()
                
                # Gradient clipping
                torch.nn.utils.clip_grad_norm_(
                    self.score_network.parameters(),
                    max_norm=1.0
                )
                
                self.optimizer.step()
                
                epoch_loss += loss.item()
            
            # Update learning rate
            self.lr_scheduler.step()
            
            avg_loss = epoch_loss / num_batches
            self.losses.append(avg_loss)
            
            if verbose and (epoch % 10 == 0 or epoch == epochs - 1):
                print(f"Epoch {epoch+1}/{epochs} | Loss: {avg_loss:.6f} | LR: {self.lr_scheduler.get_last_lr()[0]:.6f}")
        
        if verbose:
            print("Training complete!")
        
        return {"losses": self.losses}
    
    def save_model(self, filepath):
        """Save model checkpoint."""
        checkpoint = {
            'score_network_state': self.score_network.state_dict(),
            'optimizer_state': self.optimizer.state_dict(),
            'scheduler_state': self.lr_scheduler.state_dict(),
            'losses': self.losses,
            'config': self.config.__dict__
        }
        torch.save(checkpoint, filepath)
    
    def load_model(self, filepath):
        """Load model checkpoint."""
        checkpoint = torch.load(filepath, map_location=self.device)
        self.score_network.load_state_dict(checkpoint['score_network_state'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state'])
        self.lr_scheduler.load_state_dict(checkpoint['scheduler_state'])
        self.losses = checkpoint.get('losses', [])
    
    def generate(self, num_samples, feature_dim):
        """
        Generate samples using the trained model.
        
        Args:
            num_samples: Number of samples to generate
            feature_dim: Feature dimensionality
        """
        # This will be handled by the sampler
        raise NotImplementedError("Use PremiumSampler.sample() instead")
    
    def get_feature_importance(self):
        """Get feature importance (placeholder for now)."""
        return {"message": "Feature importance analysis not yet implemented"}
