"""Base tokenizer interface."""

from abc import ABC, abstractmethod
from typing import Union, List


class BaseTokenizer(ABC):
    """Abstract base class for all tokenizers.

    Provides a unified interface for different tokenization methods
    (BPE, WordPiece, Unigram, etc.).
    """

    @abstractmethod
    def train(self, data: Union[str, List[str]]) -> None:
        """Train the tokenizer on data.

        Args:
            data: Training data. Can be:
                - File path (str) to text file
                - List of strings
                - Dataset object with text field
        """
        ...

    @abstractmethod
    def encode(self, text: str, add_special_tokens: bool = True) -> List[int]:
        """Encode text to token IDs.

        Args:
            text: Input text to encode.
            add_special_tokens: Whether to add special tokens (BOS, EOS, etc.).

        Returns:
            List of token IDs.
        """
        ...

    @abstractmethod
    def decode(self, ids: List[int], skip_special_tokens: bool = True) -> str:
        """Decode token IDs back to text.

        Args:
            ids: List of token IDs to decode.
            skip_special_tokens: Whether to skip special tokens in output.

        Returns:
            Decoded text string.
        """
        ...

    @property
    @abstractmethod
    def vocab_size(self) -> int:
        """Return the vocabulary size."""
        ...

    @property
    def pad_id(self) -> int:
        """Return the padding token ID.

        Override this in subclasses to provide tokenizer-specific pad ID.
        Default returns 0.
        """
        return 0

    @property
    def bos_id(self) -> int:
        """Return the beginning-of-sequence token ID.

        Override this in subclasses to provide tokenizer-specific BOS ID.
        Default returns 1.
        """
        return 1

    @property
    def eos_id(self) -> int:
        """Return the end-of-sequence token ID.

        Override this in subclasses to provide tokenizer-specific EOS ID.
        Default returns 2.
        """
        return 2

    @abstractmethod
    def save(self, path: str) -> None:
        """Save tokenizer model to file.

        Args:
            path: Path to save the tokenizer model.
        """
        ...

    @classmethod
    @abstractmethod
    def from_pretrained(cls, path: str):
        """Load pretrained tokenizer from file.

        Args:
            path: Path to the saved tokenizer model.

        Returns:
            Loaded tokenizer instance.
        """
        ...
