"""GPT (Generative Pre-trained Transformer) implementation."""

import torch
import torch.nn as nn
from typing import Optional
from composennent.basic.decoder import Decoder
from composennent.attention import causal_mask


class GPT(nn.Module):
    """GPT: Decoder-only Transformer for autoregressive language modeling.

    Implements a GPT-style architecture with stacked decoder layers,
    token embeddings, learned positional embeddings, and weight tying
    between the input embeddings and output projection.

    Args:
        vocab_size: Size of the vocabulary.
        latent_dim: Dimension of the model (embedding size).
        num_heads: Number of attention heads per layer.
        num_layers: Number of decoder layers.
        max_seq_len: Maximum sequence length. Defaults to 512.
        drop_out: Dropout probability. Defaults to 0.1.
        mlp_ratio: MLP expansion ratio for decoder layers. Defaults to 4.

    Example:
        >>> # Create new model
        >>> model = GPT(
        ...     vocab_size=50257,
        ...     latent_dim=768,
        ...     num_heads=12,
        ...     num_layers=12,
        ... )
        >>> logits = model(input_ids)  # (batch, seq_len, vocab_size)
        >>> 
        >>> # Save model
        >>> model.save("gpt_model.pt")
        >>> 
        >>> # Load pretrained model
        >>> loaded_model = GPT.load("gpt_model.pt")

    Note:
        Uses weight tying between token embeddings and language model head
        for improved parameter efficiency.
    """

    def __init__(
        self,
        vocab_size: int,
        latent_dim: int,
        num_heads: int,
        num_layers: int,
        max_seq_len: int = 512,
        drop_out: float = 0.1,
        mlp_ratio: int = 4,
    ) -> None:
        super().__init__()
        self.latent_dim = latent_dim
        self.vocab_size = vocab_size
        self.num_heads = num_heads
        self.num_layers = num_layers
        self.max_seq_len = max_seq_len
        self.drop_out = drop_out
        self.mlp_ratio = mlp_ratio

        self.token_embedding = nn.Embedding(vocab_size, latent_dim)
        self.position_embedding = nn.Embedding(max_seq_len, latent_dim)
        self.dropout = nn.Dropout(drop_out)

        self.layers = nn.ModuleList([
            Decoder(latent_dim, num_heads, drop_out, mlp_ratio)
            for _ in range(num_layers)
        ])

        self.ln_f = nn.LayerNorm(latent_dim)
        self.lm_head = nn.Linear(latent_dim, vocab_size, bias=False)

        self.lm_head.weight = self.token_embedding.weight

    def forward(
        self,
        input_ids: torch.Tensor,
        key_padding_mask: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """Forward pass for language modeling.

        Args:
            input_ids: Token indices of shape (batch, seq_len).
            key_padding_mask: Optional mask for padded positions.
                Shape (batch, seq_len), True indicates padding.

        Returns:
            Logits over vocabulary of shape (batch, seq_len, vocab_size).
        """
        batch_size, seq_len = input_ids.shape
        positions = torch.arange(seq_len, device=input_ids.device).unsqueeze(0)

        x = self.token_embedding(input_ids) + self.position_embedding(positions)
        x = self.dropout(x)

        mask = causal_mask(seq_len, x.device)

        for layer in self.layers:
            x = layer(x, memory=None, tgt_mask=mask, tgt_key_padding_mask=key_padding_mask)

        x = self.ln_f(x)
        logits = self.lm_head(x)

        return logits
    
    def save(self, path: str):
        """Save model weights and configuration.
        
        Args:
            path: Path to save the model (e.g., "gpt_model.pt")
            
        Example:
            >>> model = GPT(vocab_size=50257, latent_dim=768, num_heads=12, num_layers=12)
            >>> # ... train model ...
            >>> model.save("my_gpt.pt")
        """
        checkpoint = {
            "model_state_dict": self.state_dict(),
            "config": {
                "vocab_size": self.vocab_size,
                "latent_dim": self.latent_dim,
                "num_heads": self.num_heads,
                "num_layers": self.num_layers,
                "max_seq_len": self.max_seq_len,
                "drop_out": self.drop_out,
                "mlp_ratio": self.mlp_ratio,
            }
        }
        torch.save(checkpoint, path)
    
    @classmethod
    def load(cls, path: str, device: str = "cpu"):
        """Load model from saved checkpoint.
        
        Args:
            path: Path to the saved model
            device: Device to load model on ("cpu" or "cuda")
            
        Returns:
            Loaded GPT model
            
        Example:
            >>> # Load pretrained model
            >>> model = GPT.load("my_gpt.pt")
            >>> 
            >>> # Load on GPU
            >>> model = GPT.load("my_gpt.pt", device="cuda")
        """
        checkpoint = torch.load(path, map_location=device)
        config = checkpoint["config"]
        
        # Create model with saved config
        model = cls(
            vocab_size=config["vocab_size"],
            latent_dim=config["latent_dim"],
            num_heads=config["num_heads"],
            num_layers=config["num_layers"],
            max_seq_len=config["max_seq_len"],
            drop_out=config["drop_out"],
            mlp_ratio=config["mlp_ratio"],
        )
        
        # Load weights
        model.load_state_dict(checkpoint["model_state_dict"])
        model.to(device)
        model.eval()
        
        return model
