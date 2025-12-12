import torch
import torch.nn as nn
import torch.nn.functional as F
import math

class CrossFeatureAttention(nn.Module):
    """Multi-head attention for capturing feature interactions."""
    def __init__(self, embed_dim, num_heads, dropout=0.1):
        super().__init__()
        self.multihead_attn = nn.MultiheadAttention(embed_dim, num_heads, dropout=dropout, batch_first=True)
        self.norm = nn.LayerNorm(embed_dim)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        # x shape: (batch_size, num_features, embed_dim)
        attn_output, _ = self.multihead_attn(x, x, x)
        x = x + self.dropout(attn_output)
        x = self.norm(x)
        return x

class MixtureDensityHead(nn.Module):
    """Mixture density network for complex distributions."""
    def __init__(self, input_dim, output_dim, num_gaussians=3):
        super().__init__()
        self.num_gaussians = num_gaussians
        self.output_dim = output_dim
        
        self.pi_layer = nn.Linear(input_dim, num_gaussians * output_dim)
        self.sigma_layer = nn.Linear(input_dim, num_gaussians * output_dim)
        self.mu_layer = nn.Linear(input_dim, num_gaussians * output_dim)

    def forward(self, x):
        # x shape: (batch_size, input_dim)
        batch_size = x.shape[0]
        
        pi = self.pi_layer(x).view(batch_size, self.output_dim, self.num_gaussians)
        pi = F.softmax(pi, dim=2)
        
        sigma = self.sigma_layer(x).view(batch_size, self.output_dim, self.num_gaussians)
        sigma = torch.exp(sigma) + 1e-6  # Ensure positive
        
        mu = self.mu_layer(x).view(batch_size, self.output_dim, self.num_gaussians)
        
        return pi, sigma, mu
    
    def sample(self, pi, sigma, mu):
        """Sample from mixture density."""
        batch_size, output_dim, num_gaussians = pi.shape
        
        # Sample which Gaussian to use for each output dimension
        component_idx = torch.multinomial(pi.view(-1, num_gaussians), 1).view(batch_size, output_dim)
        
        # Gather the selected mu and sigma
        mu_selected = torch.gather(mu, 2, component_idx.unsqueeze(2)).squeeze(2)
        sigma_selected = torch.gather(sigma, 2, component_idx.unsqueeze(2)).squeeze(2)
        
        # Sample from selected Gaussians
        noise = torch.randn_like(mu_selected)
        samples = mu_selected + sigma_selected * noise
        
        return samples


class PremiumScoreNetwork(nn.Module):
    """
    Premium score network with advanced features:
    - Cross-feature attention for capturing feature interactions
    - Mixture density heads for complex distributions
    - Conditional diffusion support
    - Time embeddings with sinusoidal encoding
    """
    def __init__(self, config, feature_dim):
        super().__init__()
        self.config = config
        self.feature_dim = feature_dim
        self.hidden_dim = config.hidden_dim
        
        # Sinusoidal time embedding
        self.time_embed_dim = self.hidden_dim
        self.register_buffer("time_embed_freqs", torch.exp(
            torch.linspace(0, math.log(10000), self.time_embed_dim // 2)
        ))
        self.time_mlp = nn.Sequential(
            nn.Linear(self.time_embed_dim, self.hidden_dim),
            nn.GELU(),
            nn.Linear(self.hidden_dim, self.hidden_dim)
        )
        
        # Feature-wise input projection for cross-attention
        if config.cross_feature_attention:
            # Project each feature individually to enable cross-feature attention
            self.feature_proj = nn.Linear(1, config.attention_dim)
            self.num_features_for_attn = feature_dim
            
            # Cross-feature attention layers
            self.attention_layers = nn.ModuleList([
                CrossFeatureAttention(config.attention_dim, config.attention_heads, config.dropout)
                for _ in range(max(1, config.num_layers // 2))
            ])
            
            # Flatten attention output
            self.attn_flatten = nn.Linear(self.num_features_for_attn * config.attention_dim, self.hidden_dim)
        else:
            # Simple input projection
            self.input_proj = nn.Linear(feature_dim, self.hidden_dim)
        
        # Conditional embeddings
        if config.conditional_diffusion and config.class_conditional_embeddings:
            self.class_embed = nn.Embedding(config.num_classes if hasattr(config, 'num_classes') else 10, self.hidden_dim)
        
        # Main MLP layers with residual connections
        self.mlp_layers = nn.ModuleList()
        for i in range(config.num_layers):
            self.mlp_layers.append(nn.ModuleDict({
                'linear': nn.Linear(self.hidden_dim, self.hidden_dim),
                'norm': nn.LayerNorm(self.hidden_dim),
                'activation': nn.GELU(),
                'dropout': nn.Dropout(config.dropout) if config.dropout > 0 else nn.Identity()
            }))
        
        # Output heads
        if config.mixture_density_heads:
            self.mdn_head = MixtureDensityHead(self.hidden_dim, feature_dim, config.num_gaussians)
        else:
            self.output_head = nn.Linear(self.hidden_dim, feature_dim)

    def get_time_embedding(self, t):
        """Sinusoidal time embedding."""
        # t: (batch_size, 1) or (batch_size,)
        if t.dim() == 1:
            t = t.unsqueeze(1)
        
        # Create sinusoidal embeddings
        angles = t * self.time_embed_freqs.unsqueeze(0)  # (batch, time_embed_dim//2)
        embeddings = torch.cat([torch.sin(angles), torch.cos(angles)], dim=-1)  # (batch, time_embed_dim)
        
        return self.time_mlp(embeddings)

    def forward(self, x, t, y=None, return_mdn_params=False):
        """
        Forward pass of premium score network.
        
        Args:
            x: Input features (batch_size, feature_dim)
            t: Timestep (batch_size,) or (batch_size, 1)
            y: Optional class labels for conditional generation
            return_mdn_params: If True, return MDN parameters instead of samples
        """
        batch_size = x.shape[0]
        
        # Time embedding
        t_emb = self.get_time_embedding(t)  # (batch_size, hidden_dim)
        
        # Input processing with cross-feature attention
        if self.config.cross_feature_attention:
            # Reshape to (batch, num_features, 1) for per-feature projection
            x_reshaped = x.unsqueeze(2)  # (batch, feature_dim, 1)
            
            # Project each feature
            x_proj = self.feature_proj(x_reshaped)  # (batch, feature_dim, attention_dim)
            
            # Apply cross-feature attention
            for attn_layer in self.attention_layers:
                x_proj = attn_layer(x_proj)
            
            # Flatten
            x_emb = self.attn_flatten(x_proj.view(batch_size, -1))  # (batch, hidden_dim)
        else:
            x_emb = self.input_proj(x)  # (batch, hidden_dim)
        
        # Combine with time embedding
        h = x_emb + t_emb
        
        # Add conditional info if available
        if self.config.conditional_diffusion and y is not None:
            if self.config.class_conditional_embeddings:
                y_emb = self.class_embed(y)
                h = h + y_emb
        
        # Main MLP with residual connections
        for layer_dict in self.mlp_layers:
            residual = h
            h = layer_dict['linear'](h)
            h = layer_dict['norm'](h)
            h = layer_dict['activation'](h)
            h = layer_dict['dropout'](h)
            h = h + residual  # Residual connection
        
        # Output
        if self.config.mixture_density_heads:
            pi, sigma, mu = self.mdn_head(h)
            if return_mdn_params:
                return pi, sigma, mu
            # Sample from mixture for score prediction
            out = self.mdn_head.sample(pi, sigma, mu)
        else:
            out = self.output_head(h)
        
        return out
