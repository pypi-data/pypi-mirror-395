"""BERT (Bidirectional Encoder Representations from Transformers) implementation."""

import torch
import torch.nn as nn
from typing import Optional, Dict, Union
from composennent.basic.encoder import Encoder


class Bert(nn.Module):
    """BERT: Encoder-only Transformer for masked language modeling and NSP.

    Implements BERT architecture with stacked encoder layers, token/position/segment
    embeddings, MLM head for masked token prediction, and NSP head for next
    sentence prediction.

    Args:
        vocab_size: Size of the vocabulary.
        latent_dim: Dimension of the model (embedding size).
        num_heads: Number of attention heads per layer.
        num_layers: Number of encoder layers.
        max_seq_len: Maximum sequence length. Defaults to 512.
        drop_out: Dropout probability. Defaults to 0.1.
        mlp_ratio: MLP expansion ratio for encoder layers. Defaults to 4.

    Example:
        >>> # Create new model
        >>> model = Bert(
        ...     vocab_size=30522,
        ...     latent_dim=768,
        ...     num_heads=12,
        ...     num_layers=12,
        ... )
        >>> 
        >>> # BERT pretraining mode (returns dict with mlm_logits and nsp_logits)
        >>> output = model(input_ids, token_type_ids, attention_mask)
        >>> mlm_logits = output["mlm_logits"]  # (batch, seq_len, vocab_size)
        >>> nsp_logits = output["nsp_logits"]  # (batch, 2)
        >>> 
        >>> # Generic trainer mode (returns only mlm_logits tensor)
        >>> logits = model(input_ids, key_padding_mask=mask, return_dict=False)
        >>> # logits shape: (batch, seq_len, vocab_size)
        >>> 
        >>> # Save model
        >>> model.save("bert_model.pt")
        >>> 
        >>> # Load pretrained model
        >>> loaded_model = Bert.load("bert_model.pt")
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
        self.segment_embedding = nn.Embedding(2, latent_dim)
        self.dropout = nn.Dropout(drop_out)

        self.layers = nn.ModuleList([
            Encoder(latent_dim, num_heads, drop_out, mlp_ratio)
            for _ in range(num_layers)
        ])

        self.pooler = nn.Linear(latent_dim, latent_dim)

        self.mlm_head = nn.Linear(latent_dim, vocab_size, bias=False)
        self.nsp_head = nn.Linear(latent_dim, 2)

        self.mlm_head.weight = self.token_embedding.weight

    def forward(
        self,
        input_ids: torch.Tensor,
        token_type_ids: Optional[torch.Tensor] = None,
        attention_mask: Optional[torch.Tensor] = None,
        key_padding_mask: Optional[torch.Tensor] = None,
        return_dict: bool = True,
    ) -> Union[Dict[str, torch.Tensor], torch.Tensor]:
        """Forward pass for BERT pretraining tasks.

        Args:
            input_ids: Token indices of shape (batch, seq_len).
            token_type_ids: Segment indices (0 for sentence A, 1 for sentence B).
                Shape (batch, seq_len). Defaults to all zeros if not provided.
            attention_mask: Mask indicating valid positions (1) vs padding (0).
                Shape (batch, seq_len). Defaults to all valid if not provided.
            key_padding_mask: Boolean mask where True indicates padding positions.
                Shape (batch, seq_len). Takes precedence over attention_mask if provided.
            return_dict: If True, returns a dictionary with mlm_logits and nsp_logits.
                If False, returns only mlm_logits tensor for compatibility with generic trainers.
                Defaults to True.

        Returns:
            If return_dict is True:
                Dictionary containing:
                    - mlm_logits: Logits for masked language modeling (batch, seq_len, vocab_size)
                    - nsp_logits: Logits for next sentence prediction (batch, 2)
            If return_dict is False:
                Tensor of shape (batch, seq_len, vocab_size) containing mlm_logits only.
        """
        batch_size, seq_len = input_ids.shape
        positions = torch.arange(seq_len, device=input_ids.device).unsqueeze(0)

        if token_type_ids is None:
            token_type_ids = torch.zeros_like(input_ids)

        x = (self.token_embedding(input_ids) +
             self.position_embedding(positions) +
             self.segment_embedding(token_type_ids))
        x = self.dropout(x)

        # Use key_padding_mask if provided, otherwise derive from attention_mask
        if key_padding_mask is None and attention_mask is not None:
            key_padding_mask = (attention_mask == 0)

        for layer in self.layers:
            x = layer(x, key_padding_mask=key_padding_mask)

        mlm_logits = self.mlm_head(x)

        # Return early if only logits are needed (for generic trainer compatibility)
        if not return_dict:
            return mlm_logits

        cls_token = x[:, 0, :]
        cls_pooled = torch.tanh(self.pooler(cls_token))
        nsp_logits = self.nsp_head(cls_pooled)

        return {
            "mlm_logits": mlm_logits,
            "nsp_logits": nsp_logits,
        }
    
    def save(self, path: str):
        """Save model weights and configuration.
        
        Args:
            path: Path to save the model (e.g., "bert_model.pt")
            
        Example:
            >>> model = Bert(vocab_size=30522, latent_dim=768, num_heads=12, num_layers=12)
            >>> # ... train model ...
            >>> model.save("my_bert.pt")
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
    def load(cls, path: str, device: str = "cpu", **model_kwargs):
        """Load model from saved checkpoint.
        
        Args:
            path: Path to the saved model
            device: Device to load model on ("cpu" or "cuda")
            **model_kwargs: If loading old checkpoint without config, provide model parameters
                          (vocab_size, latent_dim, num_heads, num_layers, etc.)
            
        Returns:
            Loaded Bert model
            
        Example:
            >>> # Load new checkpoint (with config)
            >>> model = Bert.load("my_bert.pt")
            >>> 
            >>> # Load on GPU
            >>> model = Bert.load("my_bert.pt", device="cuda")
            >>>
            >>> # Load old checkpoint (without config) - requires model params
            >>> model = Bert.load("old_bert.pt", vocab_size=30000, latent_dim=768,
            ...                   num_heads=12, num_layers=12, max_seq_len=512)
        """
        checkpoint = torch.load(path, map_location=device)
        
        # Handle new checkpoint format (with config)
        if "config" in checkpoint:
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
        else:
            # Handle old checkpoint format (just state_dict or direct state_dict)
            if "model_state_dict" in checkpoint:
                state_dict = checkpoint["model_state_dict"]
            else:
                # Assume checkpoint is the state_dict itself
                state_dict = checkpoint
            
            # Must provide model kwargs for old checkpoints
            if not model_kwargs:
                raise ValueError(
                    "Loading old checkpoint without config requires model parameters. "
                    "Please provide: vocab_size, latent_dim, num_heads, num_layers, "
                    "max_seq_len, drop_out (optional), mlp_ratio (optional)"
                )
            
            # Create model with provided config
            model = cls(**model_kwargs)
            
            # Load weights
            model.load_state_dict(state_dict)
        
        model.to(device)
        model.eval()
        
        return model