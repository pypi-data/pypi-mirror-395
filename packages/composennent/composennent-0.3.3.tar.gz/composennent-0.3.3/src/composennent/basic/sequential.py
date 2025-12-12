"""Sequential container that supports extra arguments for Block layers."""

from torch import Tensor
from .block import Block
import torch.nn as nn
from typing import Any


class SequentialBlock(Block):
    """Sequential container that passes extra arguments to Block layers only.

    Unlike PyTorch's nn.Sequential, this container can pass additional
    arguments (like attention masks) to layers that inherit from Block,
    while standard nn.Module layers receive only the tensor input.

    Args:
        *layers: Variable number of nn.Module layers to chain together.

    Example:
        >>> seq = SequentialBlock(
        ...     nn.Linear(64, 128),
        ...     nn.ReLU(),
        ...     MyCustomBlock(128, 256),  # Will receive extra args
        ... )
        >>> output = seq(x, mask=attention_mask)
    """

    def __init__(self, *layers: nn.Module) -> None:
        super().__init__()
        self.layers = nn.ModuleList(layers)

    def forward(self, x: Tensor, *args: Any, **kwargs: Any) -> Any:
        """Forward pass through all layers sequentially.

        Args:
            x: Input tensor.
            *args: Additional positional arguments passed to Block layers only.
            **kwargs: Additional keyword arguments passed to Block layers only.

        Returns:
            Output after passing through all layers (typically Tensor, but depends on last layer).
        """
        for layer in self.layers:
            if isinstance(layer, Block):
                x = layer(x, *args, **kwargs)
            else:
                x = layer(x)
        return x
