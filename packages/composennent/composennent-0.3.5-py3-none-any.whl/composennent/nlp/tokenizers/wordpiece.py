from typing import Union, List, Optional, Dict
from .base import BaseTokenizer
import os
import json
from collections import defaultdict
from composennent.utils.text_preprocessing import pre_tokenize

class WordPieceTrainer:
    def __init__(self, vocab_size: int, min_frequency: int = 2, special_tokens: Optional[List[str]] = None):
        self.vocab_size = vocab_size
        self.min_frequency = min_frequency
        self.special_tokens = special_tokens or ['<pad>', '<unk>', '<cls>', '<sep>', '<mask>']
        self.word_freqs = defaultdict(int)
        self.vocab = {}

    def train(self, texts: List[str], lowercase: bool = True) -> Dict[str, int]:
        """Train WordPiece tokenizer on the given texts.

        Args:
            texts: List of text strings to train on
            lowercase: Whether to lowercase the text

        Returns:
            Dictionary mapping tokens to their IDs
        """
        # Initialize word frequencies
        for text in texts:
            words = pre_tokenize(text, lowercase)
            for word in words:
                self.word_freqs[word] += 1

        # Filter by minimum frequency
        self.word_freqs = {
            word: freq for word, freq in self.word_freqs.items()
            if freq >= self.min_frequency
        }

        # Initialize splits with character-level tokens
        splits = self._split_into_chars()

        # Build initial vocabulary from characters
        alphabet = set()
        for word in self.word_freqs.keys():
            for i, char in enumerate(word):
                if i == 0:
                    alphabet.add(char)
                else:
                    alphabet.add(f"##{char}")

        # Start with special tokens
        vocab = self.special_tokens.copy()
        vocab.extend(sorted(alphabet))

        # Iteratively merge pairs until target vocab size
        while len(vocab) < self.vocab_size:
            pair_scores = self._compute_pair_scores(splits)
            if not pair_scores:
                break

            best = self._best_pair(pair_scores)
            splits = self._merge_pair(best, splits)

            # Add merged token to vocabulary
            new_token = best[0] + best[1].replace("##", "")
            vocab.append(new_token)

        # Convert to dictionary
        self.vocab = {token: idx for idx, token in enumerate(vocab)}
        return self.vocab

    def _split_into_chars(self) -> Dict[str, List[str]]:
        """Split words into character tokens with ## prefix for non-first chars."""
        return {
            word: [c if i == 0 else f"##{c}" for i, c in enumerate(word)]
            for word in self.word_freqs.keys()
        }

    def _compute_pair_scores(self, splits: Dict[str, List[str]]) -> Dict[tuple, float]:
        """Compute scores for all adjacent token pairs."""
        letter_freqs = defaultdict(int)
        pair_freqs = defaultdict(int)

        for word, freq in self.word_freqs.items():
            split = splits[word]
            if len(split) == 1:
                letter_freqs[split[0]] += freq
                continue
            for i in range(len(split) - 1):
                pair = (split[i], split[i + 1])
                letter_freqs[split[i]] += freq
                pair_freqs[pair] += freq
            letter_freqs[split[-1]] += freq

        scores = {
            pair: freq / (letter_freqs[pair[0]] * letter_freqs[pair[1]])
            for pair, freq in pair_freqs.items()
        }
        return scores

    def _best_pair(self, pair_scores: Dict[tuple, float]) -> tuple:
        """Find the pair with highest score."""
        return max(pair_scores.items(), key=lambda x: x[1])[0]

    def _merge_pair(self, best_pair: tuple, splits: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """Merge the best pair in all word splits."""
        first, second = best_pair
        new_splits = {}

        for word, split in splits.items():
            new_split = []
            i = 0
            while i < len(split):
                if i < len(split) - 1 and split[i] == first and split[i + 1] == second:
                    new_split.append(first + second.replace("##", ""))
                    i += 2
                else:
                    new_split.append(split[i])
                    i += 1
            new_splits[word] = new_split

        return new_splits
    
    

class WordPieceTokenizer(BaseTokenizer):
    """Wrapper around WordPiece tokenization.

    Provides a clean interface to train and use WordPiece models
    for subword tokenization.

    Args:
        vocab_size: Target vocabulary size. Defaults to 30000.
        model_prefix: Prefix for saved model files. Defaults to 'wordpiece_tokenizer'.
        special_tokens: List of special tokens to add. Defaults to common tokens.
        min_frequency: Minimum frequency for words to be included. Defaults to 2.
        lowercase: Whether to lowercase text during training. Defaults to True.
        **kwargs: Additional arguments passed to the WordPiece trainer.

    Example:
        >>> tokenizer = WordPieceTokenizer(vocab_size=30000)
        >>> tokenizer.train('corpus.txt')
        >>> tokenizer.save('my_wordpiece_tokenizer.json')
        >>> tokenizer = WordPieceTokenizer.from_pretrained('my_wordpiece_tokenizer.json')
        >>> ids = tokenizer.encode("Hello world!")
        >>> text = tokenizer.decode(ids)
    """
    def __init__(
        self,
        vocab_size: int = 30000,
        model_prefix: str = 'wordpiece_tokenizer',
        special_tokens: Optional[List[str]] = None,
        min_frequency: int = 2,
        lowercase: bool = True,
        **kwargs
    ) -> None:
        self._vocab_size = vocab_size
        self.model_prefix = model_prefix
        self.special_tokens = special_tokens or ['<pad>', '<unk>', '<cls>', '<sep>', '<mask>']
        self.min_frequency = min_frequency
        self.lowercase = lowercase
        self.kwargs = kwargs
        self.vocab = {}
        self.id_to_token = {}
        self.trainer = None  
    
    
    def train(
        self,
        data: Union[str, List[str]],
        output_dir: Optional[str] = None
    ) -> None:
        """Trains the WordPiece tokenizer on the given data.

        Args:
            data: Training data. Can be:
                - Path to a text file
                - List of strings (will be processed directly)
            output_dir: Directory to save the model. If None, uses current directory.
        """
        # Load text data
        if isinstance(data, list):
            texts = data
        elif isinstance(data, str) and os.path.isfile(data):
            with open(data, 'r', encoding='utf-8') as f:
                texts = [line.strip() for line in f if line.strip()]
        else:
            raise ValueError(
                "data must be either a file path or a list of strings"
            )

        # Train the tokenizer
        self.trainer = WordPieceTrainer(
            vocab_size=self._vocab_size,
            min_frequency=self.min_frequency,
            special_tokens=self.special_tokens
        )
        self.vocab = self.trainer.train(texts, lowercase=self.lowercase)
        self.id_to_token = {idx: token for token, idx in self.vocab.items()}

        # Save the model if output directory is specified
        if output_dir is not None:
            os.makedirs(output_dir, exist_ok=True)
            model_path = os.path.join(output_dir, f'{self.model_prefix}.json')
            self.save(model_path)
    
    def save(self, model_path: str) -> None:
        """Saves the trained WordPiece model to the specified path.

        Args:
            model_path: Path to save the model (should end with .json).
        """
        if not self.vocab:
            raise RuntimeError("No trained model to save. Call train() first.")

        model_data = {
            'vocab': self.vocab,
            'vocab_size': self._vocab_size,
            'special_tokens': self.special_tokens,
            'min_frequency': self.min_frequency,
            'lowercase': self.lowercase,
            'model_prefix': self.model_prefix
        }

        with open(model_path, 'w', encoding='utf-8') as f:
            json.dump(model_data, f, ensure_ascii=False, indent=2)

    @classmethod
    def from_pretrained(cls, model_path: str) -> 'WordPieceTokenizer':
        """Loads a pretrained WordPiece model from the specified path.

        Args:
            model_path: Path to the pretrained model (.json file).

        Returns:
            Loaded WordPiece tokenizer.
        """
        with open(model_path, 'r', encoding='utf-8') as f:
            model_data = json.load(f)

        tokenizer = cls(
            vocab_size=model_data.get('vocab_size', 30000),
            model_prefix=model_data.get('model_prefix', 'wordpiece_tokenizer'),
            special_tokens=model_data.get('special_tokens'),
            min_frequency=model_data.get('min_frequency', 2),
            lowercase=model_data.get('lowercase', True)
        )
        tokenizer.vocab = model_data['vocab']
        tokenizer.id_to_token = {idx: token for token, idx in tokenizer.vocab.items()}

        return tokenizer

    def _tokenize_word(self, word: str) -> List[str]:
        """Tokenize a single word using the WordPiece algorithm.

        Args:
            word: The word to tokenize.

        Returns:
            List of subword tokens.
        """
        if word in self.vocab:
            return [word]

        tokens = []
        start = 0

        while start < len(word):
            end = len(word)
            found = False

            while start < end:
                substr = word[start:end]
                if start > 0:
                    substr = f"##{substr}"

                if substr in self.vocab:
                    tokens.append(substr)
                    found = True
                    break
                end -= 1

            if not found:
                # Unknown token - use <unk>
                return ['<unk>']

            start = end

        return tokens

    def encode(self, text: str, add_special_tokens: bool = True) -> List[int]:
        """Encodes the input text into a list of token IDs.

        Args:
            text: Input text to encode.
            add_special_tokens: Whether to add special tokens (CLS, SEP).

        Returns:
            List of token IDs.
        """
        if not self.vocab:
            raise RuntimeError(
                "Tokenizer not trained or loaded. "
                "Call train() or use from_pretrained() first."
            )

        # Pre-tokenize
        words = pre_tokenize(text, self.lowercase)

        # Tokenize each word
        tokens = []
        for word in words:
            tokens.extend(self._tokenize_word(word))

        # Convert to IDs
        ids = [self.vocab.get(token, self.vocab.get('<unk>', 1)) for token in tokens]

        # Add special tokens if requested
        if add_special_tokens:
            cls_id = self.vocab.get('<cls>', 2)
            sep_id = self.vocab.get('<sep>', 3)
            ids = [cls_id] + ids + [sep_id]

        return ids

    def decode(self, ids: List[int], skip_special_tokens: bool = True) -> str:
        """Decodes a list of token IDs back into text.

        Args:
            ids: List of token IDs to decode.
            skip_special_tokens: Whether to skip special tokens in output.

        Returns:
            Decoded text.
        """
        if not self.id_to_token:
            raise RuntimeError(
                "Tokenizer not trained or loaded. "
                "Call train() or use from_pretrained() first."
            )

        # Convert IDs to tokens
        tokens = []
        for idx in ids:
            token = self.id_to_token.get(idx, '<unk>')

            # Skip special tokens if requested
            if skip_special_tokens and token in self.special_tokens:
                continue

            tokens.append(token)

        # Join tokens and remove ## markers
        text = ' '.join(tokens).replace(' ##', '').replace('##', '')
        return text
    
    @property
    def vocab_size(self) -> int:
        """Returns the size of the vocabulary."""
        if self.vocab:
            return len(self.vocab)
        return self._vocab_size

    @property
    def pad_id(self) -> int:
        """Returns the ID of the padding token."""
        return self.vocab.get('<pad>', 0)

    @property
    def unk_id(self) -> int:
        """Returns the ID of the unknown token."""
        return self.vocab.get('<unk>', 1)

    @property
    def bos_id(self) -> int:
        """Returns the ID of the beginning-of-sequence token."""
        return self.vocab.get('<cls>', 2)

    @property
    def eos_id(self) -> int:
        """Returns the ID of the end-of-sequence token."""
        return self.vocab.get('<sep>', 3)
    
    