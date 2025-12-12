import math
import torch
import torch.nn as nn
from typing import Optional
from composennent.basic.decoder import Decoder
from composennent.attention import causal_mask
from composennent.basic.encoder import Encoder

class Transformer(nn.Module):
    """Transformer: Encoder-Decoder architecture for sequence-to-sequence tasks.

    Implements a standard Transformer architecture with stacked encoder and decoder layers,
    token embeddings, learned positional embeddings, and weight tying between the input
    embeddings and output projection.

    Args:
        vocab_size: Size of the vocabulary.
        latent_dim: Dimension of the model (embedding size).
        num_heads: Number of attention heads per layer.
        num_encoder_layers: Number of encoder layers.
        num_decoder_layers: Number of decoder layers.
        max_seq_len: Maximum sequence length. Defaults to 512.
        drop_out: Dropout probability. Defaults to 0.1.
        mlp_ratio: MLP expansion ratio for encoder and decoder layers. Defaults to 4.

    Example:
        >>> model = Transformer(
        ...     vocab_size=32000,
        ...     latent_dim=512,
        ...     num_heads=8,
        ...     num_encoder_layers=6,
        ...     num_decoder_layers=6,
        ... )
        >>> logits = model(src_input_ids, tgt_input_ids)  # (batch, tgt_seq_len, vocab_size)

    Note:
        Uses weight tying between token embeddings and language model head
        for improved parameter efficiency.
    """

    def __init__(
        self,
        vocab_size: int,
        latent_dim: int,
        num_heads: int,
        num_encoder_layers: int,
        num_decoder_layers: int,
        max_seq_len: int = 512,
        drop_out: float = 0.1,
        mlp_ratio: int = 4,
    ) -> None:
        super().__init__()
        self.latent_dim = latent_dim

        self.token_embedding = nn.Embedding(vocab_size, latent_dim)
        self.position_embedding = nn.Embedding(max_seq_len, latent_dim)
        self.dropout = nn.Dropout(drop_out)

        self.encoder_layers = nn.ModuleList([
            Encoder(latent_dim, num_heads, drop_out, mlp_ratio)
            for _ in range(num_encoder_layers)
        ])

        self.decoder_layers = nn.ModuleList([
            Decoder(latent_dim, num_heads, drop_out, mlp_ratio)
            for _ in range(num_decoder_layers)
        ])
        self.ln_f = nn.LayerNorm(latent_dim)
        self.lm_head = nn.Linear(latent_dim, vocab_size, bias=False)
        self.lm_head.weight = self.token_embedding.weight
        
    def forward(
        self,
        src_input_ids: torch.Tensor,
        tgt_input_ids: torch.Tensor,
        src_key_padding_mask: Optional[torch.Tensor] = None,
        tgt_key_padding_mask: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """Forward pass for sequence-to-sequence tasks.

        Args:
            src_input_ids: Source input token IDs of shape (batch, src_seq_len).
            tgt_input_ids: Target input token IDs of shape (batch, tgt_seq_len).
            src_key_padding_mask: Optional mask for source keys (batch, src_seq_len).
            tgt_key_padding_mask: Optional mask for target keys (batch, tgt_seq_len).

        Returns:
            Logits over vocabulary of shape (batch, tgt_seq_len, vocab_size).
        """
        batch_size, src_seq_len = src_input_ids.shape
        positions = torch.arange(src_seq_len, device=src_input_ids.device).unsqueeze(0)
        src_embeddings = self.token_embedding(src_input_ids) * math.sqrt(self.latent_dim) + self.position_embedding(positions)
        src_embeddings = self.dropout(src_embeddings)
        
        for layer in self.encoder_layers:
            src_embeddings = layer(src_embeddings, src_key_padding_mask)
        
        batch_size, tgt_seq_len = tgt_input_ids.shape
        positions = torch.arange(tgt_seq_len, device=tgt_input_ids.device).unsqueeze(0)
        tgt_embeddings = self.token_embedding(tgt_input_ids) * math.sqrt(self.latent_dim) + self.position_embedding(positions)
        tgt_embeddings = self.dropout(tgt_embeddings)
        
        mask = causal_mask(tgt_seq_len, tgt_embeddings.device)
        
        for layer in self.decoder_layers:
            tgt_embeddings = layer(
                tgt_embeddings,
                memory=src_embeddings,
                tgt_mask=mask,
                tgt_key_padding_mask=tgt_key_padding_mask,
                memory_key_padding_mask=src_key_padding_mask,
            )
        
        tgt_embeddings = self.ln_f(tgt_embeddings)
        logits = self.lm_head(tgt_embeddings)
        return logits