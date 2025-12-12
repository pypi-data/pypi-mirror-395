"""HuggingFace tokenizer wrapper for BaseTokenizer interface."""

from typing import List, Union
from .base import BaseTokenizer


class HuggingFaceTokenizer(BaseTokenizer):
    """Wrapper for HuggingFace tokenizers to match BaseTokenizer interface.

    This allows you to use any HuggingFace tokenizer (GPT2, BERT, LLaMA, etc.)
    with the composennent training pipeline.

    Example:
        >>> from transformers import AutoTokenizer
        >>> from composennent.nlp.tokenizers import HuggingFaceTokenizer
        >>>
        >>> # Load any HF tokenizer
        >>> hf_tok = AutoTokenizer.from_pretrained("gpt2")
        >>> tok = HuggingFaceTokenizer(hf_tok)
        >>>
        >>> # Now works with composennent training
        >>> train(model, texts, tokenizer=tok, pad_token_id=tok.pad_id)
    """

    def __init__(self, hf_tokenizer):
        """Initialize wrapper with a HuggingFace tokenizer.

        Args:
            hf_tokenizer: Any tokenizer from transformers library
                         (AutoTokenizer, GPT2Tokenizer, etc.)
        """
        self.hf = hf_tokenizer

        # Set pad token if not already set (common for GPT-2 style models)
        if self.hf.pad_token is None:
            self.hf.pad_token = self.hf.eos_token

    def train(self, data: Union[str, List[str]]) -> None:
        """Training not supported for pre-trained HF tokenizers.

        Args:
            data: Training data (not used)

        Raises:
            NotImplementedError: HF tokenizers are pre-trained
        """
        raise NotImplementedError(
            "Training HuggingFace tokenizers not supported. "
            "Use a pre-trained tokenizer or train with SentencePieceTokenizer."
        )

    def encode(self, text: str, add_special_tokens: bool = True) -> List[int]:
        """Encode text to token IDs.

        Args:
            text: Input text to encode
            add_special_tokens: Whether to add special tokens (BOS, EOS, etc.)

        Returns:
            List of token IDs
        """
        return self.hf.encode(text, add_special_tokens=add_special_tokens)

    def decode(self, ids: List[int], skip_special_tokens: bool = True) -> str:
        """Decode token IDs back to text.

        Args:
            ids: List of token IDs to decode
            skip_special_tokens: Whether to skip special tokens in output

        Returns:
            Decoded text string
        """
        return self.hf.decode(ids, skip_special_tokens=skip_special_tokens)

    @property
    def vocab_size(self) -> int:
        """Return the vocabulary size."""
        return self.hf.vocab_size

    @property
    def pad_id(self) -> int:
        """Return the padding token ID."""
        return self.hf.pad_token_id

    @property
    def bos_id(self) -> int:
        """Return the beginning-of-sequence token ID."""
        return self.hf.bos_token_id if self.hf.bos_token_id is not None else self.hf.cls_token_id

    @property
    def eos_id(self) -> int:
        """Return the end-of-sequence token ID."""
        return self.hf.eos_token_id if self.hf.eos_token_id is not None else self.hf.sep_token_id

    def save(self, path: str) -> None:
        """Save tokenizer to directory.

        Args:
            path: Path to save the tokenizer model
        """
        self.hf.save_pretrained(path)

    @classmethod
    def from_pretrained(cls, path: str, **kwargs):
        """Load pretrained tokenizer from HuggingFace hub or local directory.

        Args:
            path: Model name on HF Hub (e.g., "gpt2", "bert-base-uncased")
                  or path to local directory
            **kwargs: Additional arguments passed to AutoTokenizer.from_pretrained

        Returns:
            HuggingFaceTokenizer instance

        Example:
            >>> # From HF Hub
            >>> tok = HuggingFaceTokenizer.from_pretrained("gpt2")
            >>>
            >>> # From local directory
            >>> tok = HuggingFaceTokenizer.from_pretrained("./my_tokenizer")
        """
        try:
            from transformers import AutoTokenizer
        except ImportError:
            raise ImportError(
                "transformers library required for HuggingFaceTokenizer. "
                "Install with: pip install transformers"
            )

        hf_tok = AutoTokenizer.from_pretrained(path, **kwargs)
        return cls(hf_tok)
