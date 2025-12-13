"""Abstract base class for neural network blocks."""

import torch.nn as nn
from abc import ABC, abstractmethod
from torch import Tensor
from typing import Any


class Block(nn.Module, ABC):
    """Abstract base class for all custom neural network blocks.

    This class serves as the foundation for all neural network components
    in the BlockForge library. It combines PyTorch's nn.Module with Python's
    ABC to enforce a consistent interface across all building blocks.

    All subclasses must implement the `forward` method.

    Example:
        >>> class MyBlock(Block):
        ...     def __init__(self, in_features, out_features):
        ...         super().__init__()
        ...         self.linear = nn.Linear(in_features, out_features)
        ...
        ...     def forward(self, x):
        ...         return self.linear(x)
    """

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def forward(self, x: Tensor, *args: Any, **kwargs: Any) -> Any:
        """Forward pass of the block.

        Args:
            x: Input tensor.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Output after processing (typically Tensor, but can be tuple, dict, etc.).
        """
        ...
