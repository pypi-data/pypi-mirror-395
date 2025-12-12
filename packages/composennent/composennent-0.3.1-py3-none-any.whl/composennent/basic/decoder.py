"""Transformer Decoder block implementation."""

from .block import Block
from .sequential import SequentialBlock
import torch
import torch.nn as nn
from typing import Optional 


class Decoder(Block):
    """Transformer Decoder block with pre-norm architecture.

    Implements a standard Transformer decoder layer with:
    - Masked (causal) self-attention for autoregressive generation
    - Cross-attention to encoder outputs (optional)
    - Feed-forward network (MLP)

    Uses pre-LayerNorm architecture for improved training stability.

    Args:
        latent_dim: Dimension of the model (embedding size).
        num_heads: Number of attention heads.
        drop_out: Dropout probability. Defaults to 0.1.
        mlp_ratio: Expansion ratio for MLP hidden dimension. Defaults to 4.
        return_attention: Whether to return attention weights. Defaults to False.

    Example:
        >>> decoder = Decoder(latent_dim=512, num_heads=8)
        >>> # Self-attention only (GPT-style) with custom mask
        >>> output = decoder(x, tgt_mask=my_mask)
        >>> # With cross-attention (encoder-decoder)
        >>> output = decoder(x, memory=encoder_output, tgt_mask=causal_mask)
        >>> # With attention weights
        >>> output, (self_attn, cross_attn) = decoder(x, memory=enc_out, return_attention=True)
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

        self.cross_attn = nn.MultiheadAttention(
            embed_dim=latent_dim,
            num_heads=num_heads,
            batch_first=True,
            dropout=drop_out,
        )
        self.norm2 = nn.LayerNorm(latent_dim)

        mlp_hidden_dim = latent_dim * mlp_ratio
        self.mlp = SequentialBlock(
            nn.Linear(latent_dim, mlp_hidden_dim),
            nn.GELU(),
            nn.Dropout(drop_out),
            nn.Linear(mlp_hidden_dim, latent_dim),
        )
        self.norm3 = nn.LayerNorm(latent_dim)
        self.dropout = nn.Dropout(drop_out)

    def forward(
        self,
        x: torch.Tensor,
        memory: Optional[torch.Tensor] = None,
        tgt_mask: Optional[torch.Tensor] = None,
        tgt_key_padding_mask: Optional[torch.Tensor] = None,
        memory_key_padding_mask: Optional[torch.Tensor] = None,
        return_attention: Optional[bool] = None,
    ):
        """Forward pass through the decoder layer.

        Args:
            x: Target sequence tensor of shape (batch, seq_len, latent_dim).
            memory: Encoder output for cross-attention. If None, skips cross-attention.
            tgt_mask: Optional attention mask for target sequence (e.g., causal mask).
                Shape (seq_len, seq_len) or (batch*num_heads, seq_len, seq_len).
            tgt_key_padding_mask: Mask for padded positions in target sequence.
                Shape (batch, seq_len), True indicates padding.
            memory_key_padding_mask: Mask for padded positions in encoder output.
                Shape (batch, src_len), True indicates padding.
            return_attention: Override instance-level return_attention setting.

        Returns:
            If return_attention is True:
                Tuple of (output tensor, (self_attn_weights, cross_attn_weights))
                cross_attn_weights is None if memory is None.
            Otherwise:
                Output tensor of shape (batch, seq_len, latent_dim).
        """
        return_attn = return_attention if return_attention is not None else self.return_attention

        normed = self.norm1(x)
        self_attn_out, self_attn_weights = self.self_attn(
            normed, normed, normed,
            attn_mask=tgt_mask,
            key_padding_mask=tgt_key_padding_mask,
            need_weights=return_attn,
        )
        x = x + self.dropout(self_attn_out)

        cross_attn_weights = None
        if memory is not None:
            normed = self.norm2(x)
            cross_attn_out, cross_attn_weights = self.cross_attn(
                normed, memory, memory,
                key_padding_mask=memory_key_padding_mask,
                need_weights=return_attn,
            )
            x = x + self.dropout(cross_attn_out)

        normed = self.norm3(x)
        mlp_out = self.mlp(normed)
        x = x + self.dropout(mlp_out)

        return (x, (self_attn_weights, cross_attn_weights)) if return_attn else x
