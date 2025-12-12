"""Base class for transformer language models."""

import torch
import torch.nn as nn
from typing import Optional, Union
from abc import ABC, abstractmethod


class BaseLanguageModel(nn.Module, ABC):
    """Base class for all transformer-based language models.
    
    This class provides common functionality for language models including:
    - Text generation (sampling, greedy, beam search)
    - Model saving and loading with configuration
    - Common interface for forward pass
    
    All transformer models (GPT, BERT, etc.) should inherit from this class.
    """
    
    def __init__(self):
        super().__init__()
        # These should be set by child classes
        self.vocab_size = None
        self.latent_dim = None
        self.num_heads = None
        self.num_layers = None
        self.max_seq_len = None
        self.drop_out = None
        self.mlp_ratio = None
    
    @abstractmethod
    def forward(
        self,
        input_ids: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
        **kwargs
    ) -> torch.Tensor:
        """Forward pass of the model.
        
        Args:
            input_ids: Token IDs of shape (batch, seq_len)
            attention_mask: Optional attention mask
            **kwargs: Additional model-specific arguments
            
        Returns:
            Model outputs (logits, hidden states, etc.)
        """
        pass
    
    def get_config(self) -> dict:
        """Get model configuration as a dictionary.
        
        Returns:
            Dictionary containing model configuration.
        """
        return {
            "vocab_size": self.vocab_size,
            "latent_dim": self.latent_dim,
            "num_heads": self.num_heads,
            "num_layers": self.num_layers,
            "max_seq_len": self.max_seq_len,
            "drop_out": self.drop_out,
            "mlp_ratio": self.mlp_ratio,
        }
    
    def save(self, path: str) -> None:
        """Save model weights and configuration.
        
        Args:
            path: Path to save the model (e.g., "model.pt")
            
        Example:
            >>> model.save("my_model.pt")
        """
        checkpoint = {
            "model_state_dict": self.state_dict(),
            "config": self.get_config(),
            "model_type": self.__class__.__name__,
        }
        torch.save(checkpoint, path)
        print(f"Model saved to {path}")
    
    @classmethod
    def load(cls, path: str, device: str = "cpu", **model_kwargs):
        """Load model from saved checkpoint.
        
        Args:
            path: Path to the saved model
            device: Device to load model on ("cpu" or "cuda")
            **model_kwargs: If loading old checkpoint without config, provide model parameters
            
        Returns:
            Loaded model instance
            
        Example:
            >>> # Load new checkpoint (with config)
            >>> model = GPT.load("my_model.pt")
            >>> 
            >>> # Load on GPU
            >>> model = GPT.load("my_model.pt", device="cuda")
            >>>
            >>> # Load old checkpoint (without config)
            >>> model = GPT.load("old_model.pt", vocab_size=50257, latent_dim=768,
            ...                  num_heads=12, num_layers=12, max_seq_len=1024)
        """
        checkpoint = torch.load(path, map_location=device)
        
        # Handle new checkpoint format (with config)
        if "config" in checkpoint:
            config = checkpoint["config"]
            
            # Create model with saved config
            model = cls(**config)
            
            # Load weights
            model.load_state_dict(checkpoint["model_state_dict"])
        else:
            # Handle old checkpoint format
            if "model_state_dict" in checkpoint:
                state_dict = checkpoint["model_state_dict"]
            else:
                # Assume checkpoint is the state_dict itself
                state_dict = checkpoint
            
            # Must provide model kwargs for old checkpoints
            if not model_kwargs:
                raise ValueError(
                    f"Loading old checkpoint without config requires model parameters. "
                    f"Please provide: vocab_size, latent_dim, num_heads, num_layers, "
                    f"max_seq_len, drop_out (optional), mlp_ratio (optional)"
                )
            
            # Create model with provided config
            model = cls(**model_kwargs)
            
            # Load weights
            model.load_state_dict(state_dict)
        
        model.to(device)
        model.eval()
        
        print(f"Model loaded from {path}")
        return model
    
    def generate(
        self,
        input_ids: Union[torch.Tensor, list],
        max_length: int = 50,
        temperature: float = 1.0,
        top_k: int = 50,
        top_p: float = 0.95,
        eos_token_id: Optional[int] = None,
        pad_token_id: Optional[int] = None,
        do_sample: bool = True,
        num_return_sequences: int = 1,
        device: Optional[str] = None,
    ) -> torch.Tensor:
        """Generate text autoregressively.
        
        Args:
            input_ids: Input token IDs. Can be:
                - torch.Tensor of shape (batch, seq_len)
                - List of token IDs (will be converted to tensor)
            max_length: Maximum number of tokens to generate.
            temperature: Sampling temperature (higher = more random). Only used if do_sample=True.
            top_k: Keep only top k tokens for sampling. Only used if do_sample=True.
            top_p: Nucleus sampling threshold. Only used if do_sample=True.
            eos_token_id: End-of-sequence token ID to stop generation.
            pad_token_id: Padding token ID (for batched generation).
            do_sample: Whether to use sampling (True) or greedy decoding (False).
            num_return_sequences: Number of sequences to generate per input.
            device: Device to use. If None, inferred from input_ids or uses cpu.
            
        Returns:
            Generated token IDs of shape (batch * num_return_sequences, generated_length).
            
        Example:
            >>> model = GPT.load("gpt_model.pt", device="cuda")
            >>> 
            >>> # With tensor
            >>> input_ids = torch.tensor([[1, 2, 3]], device="cuda")
            >>> generated = model.generate(input_ids, max_length=50, temperature=0.8)
            >>> 
            >>> # With list
            >>> input_ids = [1, 2, 3]
            >>> generated = model.generate(input_ids, max_length=50, device="cuda")
            >>> 
            >>> # Greedy generation (deterministic)
            >>> generated = model.generate(input_ids, max_length=50, do_sample=False)
            >>>
            >>> # Generate multiple sequences
            >>> generated = model.generate(input_ids, num_return_sequences=3)
        """
        self.eval()
        
        # Convert list to tensor if needed
        if isinstance(input_ids, list):
            if device is None:
                device = next(self.parameters()).device
            input_ids = torch.tensor([input_ids], dtype=torch.long, device=device)
        
        # Get device from tensor or parameter
        if device is None:
            device = input_ids.device
        else:
            input_ids = input_ids.to(device)
        
        batch_size = input_ids.size(0)
        
        # Expand input for multiple return sequences
        if num_return_sequences > 1:
            input_ids = input_ids.repeat_interleave(num_return_sequences, dim=0)
        
        generated = input_ids
        
        with torch.no_grad():
            for _ in range(max_length):
                # Truncate if exceeds max_seq_len
                if generated.size(1) > self.max_seq_len:
                    input_chunk = generated[:, -self.max_seq_len:]
                else:
                    input_chunk = generated
                
                # Get model predictions
                logits = self.forward(input_chunk)
                
                # Get logits for the last token
                next_token_logits = logits[:, -1, :]
                
                if do_sample:
                    # Apply temperature
                    next_token_logits = next_token_logits / temperature
                    
                    # Apply top-k filtering
                    if top_k > 0:
                        indices_to_remove = next_token_logits < torch.topk(next_token_logits, top_k)[0][..., -1, None]
                        next_token_logits[indices_to_remove] = float('-inf')
                    
                    # Apply top-p (nucleus) filtering
                    if top_p < 1.0:
                        sorted_logits, sorted_indices = torch.sort(next_token_logits, descending=True)
                        cumulative_probs = torch.cumsum(torch.softmax(sorted_logits, dim=-1), dim=-1)
                        
                        # Remove tokens with cumulative probability above the threshold
                        sorted_indices_to_remove = cumulative_probs > top_p
                        # Shift the indices to the right to keep the first token above threshold
                        sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
                        sorted_indices_to_remove[..., 0] = 0
                        
                        indices_to_remove = sorted_indices_to_remove.scatter(1, sorted_indices, sorted_indices_to_remove)
                        next_token_logits[indices_to_remove] = float('-inf')
                    
                    # Sample from the filtered distribution
                    probs = torch.softmax(next_token_logits, dim=-1)
                    next_token = torch.multinomial(probs, num_samples=1)
                else:
                    # Greedy decoding
                    next_token = next_token_logits.argmax(dim=-1, keepdim=True)
                
                # Check if EOS token for any sequence in batch
                if eos_token_id is not None:
                    # If all sequences have generated EOS, stop
                    if (next_token == eos_token_id).all():
                        break
                
                # Append to generated sequence
                generated = torch.cat([generated, next_token], dim=1)
                
                # Stop if max sequence length reached
                if generated.size(1) >= self.max_seq_len:
                    break
        
        return generated
    
    def generate_greedy(
        self,
        input_ids: Union[torch.Tensor, list],
        max_length: int = 50,
        eos_token_id: Optional[int] = None,
        device: Optional[str] = None,
    ) -> torch.Tensor:
        """Generate text using greedy decoding (always pick most likely token).
        
        Convenience method for greedy generation.
        
        Args:
            input_ids: Input token IDs. Can be:
                - torch.Tensor of shape (batch, seq_len)
                - List of token IDs (will be converted to tensor)
            max_length: Maximum number of tokens to generate.
            eos_token_id: End-of-sequence token ID to stop generation.
            device: Device to use. If None, inferred from input_ids or uses cpu.
            
        Returns:
            Generated token IDs.
            
        Example:
            >>> # With tensor
            >>> generated = model.generate_greedy(input_ids, max_length=50)
            >>> 
            >>> # With list
            >>> generated = model.generate_greedy([1, 2, 3], max_length=50, device="cuda")
        """
        return self.generate(
            input_ids,
            max_length=max_length,
            eos_token_id=eos_token_id,
            do_sample=False,
            device=device,
        )
    
    def num_parameters(self, only_trainable: bool = False) -> int:
        """Count the number of parameters in the model.
        
        Args:
            only_trainable: If True, count only trainable parameters.
            
        Returns:
            Number of parameters.
            
        Example:
            >>> print(f"Total parameters: {model.num_parameters():,}")
            >>> print(f"Trainable parameters: {model.num_parameters(only_trainable=True):,}")
        """
        if only_trainable:
            return sum(p.numel() for p in self.parameters() if p.requires_grad)
        return sum(p.numel() for p in self.parameters())
    
    def freeze(self) -> None:
        """Freeze all model parameters (set requires_grad=False).
        
        Example:
            >>> model.freeze()
            >>> # Now model parameters won't be updated during training
        """
        for param in self.parameters():
            param.requires_grad = False
    
    def unfreeze(self) -> None:
        """Unfreeze all model parameters (set requires_grad=True).
        
        Example:
            >>> model.unfreeze()
            >>> # Now model parameters can be updated during training
        """
        for param in self.parameters():
            param.requires_grad = True
    
    def freeze_embeddings(self) -> None:
        """Freeze only the embedding layers.
        
        Example:
            >>> model.freeze_embeddings()
            >>> # Embeddings frozen, rest of model can be trained
        """
        if hasattr(self, 'token_embedding'):
            for param in self.token_embedding.parameters():
                param.requires_grad = False
        if hasattr(self, 'position_embedding'):
            for param in self.position_embedding.parameters():
                param.requires_grad = False
    
    def get_memory_footprint(self) -> dict:
        """Get memory footprint of the model.
        
        Returns:
            Dictionary with memory information in MB.
            
        Example:
            >>> memory = model.get_memory_footprint()
            >>> print(f"Model size: {memory['total_mb']:.2f} MB")
        """
        param_size = sum(p.numel() * p.element_size() for p in self.parameters())
        buffer_size = sum(b.numel() * b.element_size() for b in self.buffers())
        
        total_size = param_size + buffer_size
        
        return {
            "params_mb": param_size / 1024 / 1024,
            "buffers_mb": buffer_size / 1024 / 1024,
            "total_mb": total_size / 1024 / 1024,
        }
    
    def __repr__(self) -> str:
        """String representation of the model."""
        config = self.get_config()
        config_str = ", ".join([f"{k}={v}" for k, v in config.items() if v is not None])
        return f"{self.__class__.__name__}({config_str})"
