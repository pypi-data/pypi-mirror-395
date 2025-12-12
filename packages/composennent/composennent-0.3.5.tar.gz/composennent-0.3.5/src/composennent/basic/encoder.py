"""Transformer Encoder block implementation."""

from .block import Block
from .sequential import SequentialBlock
import torch
import torch.nn as nn
from typing import Optional


class Encoder(Block):
    """Transformer Encoder block with pre-norm architecture.

    Implements a standard Transformer encoder layer with:
    - Multi-head self-attention
    - Feed-forward network (MLP)

    Uses pre-LayerNorm architecture for improved training stability.

    Args:
        latent_dim: Dimension of the model (embedding size).
        num_heads: Number of attention heads.
        drop_out: Dropout probability. Defaults to 0.1.
        mlp_ratio: Expansion ratio for MLP hidden dimension. Defaults to 4.
        return_attention: Whether to return attention weights. Defaults to False.

    Example:
        >>> encoder = Encoder(latent_dim=512, num_heads=8)
        >>> output = encoder(x)
        >>> # With masks
        >>> output = encoder(x, key_padding_mask=mask, attn_mask=causal_mask)
        >>> # With attention weights
        >>> output, attn_weights = encoder(x, return_attention=True)
    """

    def __init__(
        self,
        latent_dim: int,
        num_heads: int,
        drop_out: float = 0.1,
        mlp_ratio: int = 4,
        return_attention: bool = False,
    ) -> None:
        super().__init__()
        self.latent_dim = latent_dim
        self.return_attention = return_attention

        self.self_attn = nn.MultiheadAttention(
            embed_dim=latent_dim,
            num_heads=num_heads,
            batch_first=True,
            dropout=drop_out,
        )
        self.norm1 = nn.LayerNorm(latent_dim)
        mlp_hidden_dim = latent_dim * mlp_ratio
        self.mlp = SequentialBlock(
            nn.Linear(latent_dim, mlp_hidden_dim),
            nn.GELU(),
            nn.Dropout(drop_out),
            nn.Linear(mlp_hidden_dim, latent_dim),
        )
        self.norm2 = nn.LayerNorm(latent_dim)
        self.dropout = nn.Dropout(drop_out)

    def forward(
        self,
        x: torch.Tensor,
        key_padding_mask: Optional[torch.Tensor] = None,
        attn_mask: Optional[torch.Tensor] = None,
        return_attention: Optional[bool] = None,
    ):
        """Forward pass through the encoder layer.

        Args:
            x: Input tensor of shape (batch, seq_len, latent_dim).
            key_padding_mask: Optional mask for padded positions.
                Shape (batch, seq_len), True indicates padding.
            attn_mask: Optional attention mask for causal or custom masking.
                Shape (seq_len, seq_len) or (batch*num_heads, seq_len, seq_len).
            return_attention: Override instance-level return_attention setting.

        Returns:
            If return_attention is True:
                Tuple of (output tensor, attention weights)
            Otherwise:
                Output tensor of shape (batch, seq_len, latent_dim).
        """
        return_attn = return_attention if return_attention is not None else self.return_attention

        normed = self.norm1(x)
        attn_out, attn_weights = self.self_attn(
            normed, normed, normed,
            key_padding_mask=key_padding_mask,
            attn_mask=attn_mask,
            need_weights=return_attn,
        )
        x = x + self.dropout(attn_out)

        normed = self.norm2(x)
        mlp_out = self.mlp(normed)
        x = x + self.dropout(mlp_out)

        return (x, attn_weights) if return_attn else x
