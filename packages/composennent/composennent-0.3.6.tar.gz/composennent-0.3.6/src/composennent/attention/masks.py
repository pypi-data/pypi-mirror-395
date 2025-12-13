import torch


def causal_mask(seq_len: int, device=None) -> torch.Tensor:
    """Generate upper-triangular causal mask for autoregressive attention.

    Args:
        seq_len: Length of the sequence.
        device: Device to create the mask on. Defaults to CPU.

    Returns:
        Boolean mask of shape (seq_len, seq_len) where True indicates
        positions to be masked (future tokens that should not be attended to).

    Example:
        >>> mask = causal_mask(4)
        >>> # Token at position i can only attend to positions <= i
    """
    mask = torch.triu(
        torch.ones(seq_len, seq_len, device=device, dtype=torch.bool),
        diagonal=1,
    )
    return mask