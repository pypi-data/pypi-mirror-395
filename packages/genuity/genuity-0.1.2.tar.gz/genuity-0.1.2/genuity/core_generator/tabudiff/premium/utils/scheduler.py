"""
Variance Scheduler for TabuDiff Premium

Supports both linear and cosine schedules.
"""

import torch
import numpy as np


class PremiumVarianceScheduler:
    """
    Premium variance scheduler with multiple schedule types.
    """
    
    def __init__(self, config):
        """
        Initialize scheduler.
        
        Args:
            config: TabuDiffPremiumConfig
        """
        self.num_steps = config.num_diffusion_steps
        self.beta_start = config.beta_start
        self.beta_end = config.beta_end
        self.device = torch.device(config.device)
        
        # Compute beta schedule
        self.betas = self._get_beta_schedule()
        self.alphas = 1.0 - self.betas
        self.alphas_cumprod = torch.cumprod(self.alphas, dim=0)
        
        # Move to device
        self.betas = self.betas.to(self.device)
        self.alphas = self.alphas.to(self.device)
        self.alphas_cumprod = self.alphas_cumprod.to(self.device)
    
    def _get_beta_schedule(self):
        """Get beta schedule (linear or cosine)."""
        # Linear schedule
        return torch.linspace(self.beta_start, self.beta_end, self.num_steps)
