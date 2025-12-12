from dataclasses import dataclass
from typing import Optional, List
from torch.utils.data import DataLoader, Dataset
import torch


@dataclass
class Batch:
    """Data structure for a training batch.

    Extensible design for text, vision-language, and mixture-of-experts models.
    """
    input_ids: torch.Tensor  # (batch_size, seq_len)
    attention_mask: torch.Tensor  # (batch_size, seq_len)
    labels: torch.Tensor  # (batch_size, seq_len)

    # Optional fields for future VLM/MoE support
    pixel_values: Optional[torch.Tensor] = None  # For vision inputs
    expert_ids: Optional[torch.Tensor] = None  # For MoE routing


def collate_batch(batch_list: List[dict]) -> Batch:
    """Custom collate function that properly handles batching.

    Args:
        batch_list: List of dicts with keys: input_ids, attention_mask, labels, etc.

    Returns:
        Batch object with stacked tensors
    """
    input_ids = torch.stack([item["input_ids"] for item in batch_list])
    attention_mask = torch.stack([item["attention_mask"] for item in batch_list])
    labels = torch.stack([item["labels"] for item in batch_list])

    pixel_values = None
    if "pixel_values" in batch_list[0] and batch_list[0]["pixel_values"] is not None:
        pixel_values = torch.stack([item["pixel_values"] for item in batch_list])

    expert_ids = None
    if "expert_ids" in batch_list[0] and batch_list[0]["expert_ids"] is not None:
        expert_ids = torch.stack([item["expert_ids"] for item in batch_list])

    return Batch(
        input_ids=input_ids,
        attention_mask=attention_mask,
        labels=labels,
        pixel_values=pixel_values,
        expert_ids=expert_ids,
    )


class TextDataset(Dataset):
    """Custom Dataset for text data.

    Supports both fixed-length and dynamic padding strategies.
    """

    def __init__(
        self,
        texts: List[str],
        tokenizer,
        max_length: int,
        padding_strategy: str = "max_length",
        pad_token_id: int = 0,
    ):
        """
        Args:
            texts: List of text strings to tokenize
            tokenizer: Any BaseTokenizer implementation
            max_length: Maximum sequence length
            padding_strategy: "max_length" (pad inside __getitem__) or "longest" (dynamic padding in collate)
            pad_token_id: Token ID to use for padding
        """
        self.texts = texts
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.padding_strategy = padding_strategy
        self.pad_token_id = pad_token_id

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]

        # BaseTokenizer API: use encode() method
        ids = self.tokenizer.encode(text, add_special_tokens=True)
        ids = ids[: self.max_length]
        input_ids = torch.tensor(ids, dtype=torch.long)

        # 1 for real tokens (we'll pad later if needed)
        attention_mask = torch.ones_like(input_ids, dtype=torch.long)

        if self.padding_strategy == "max_length":
            pad_len = self.max_length - input_ids.size(0)
            if pad_len > 0:
                pad_ids = torch.full((pad_len,), self.pad_token_id, dtype=torch.long)
                pad_mask = torch.zeros((pad_len,), dtype=torch.long)
                input_ids = torch.cat([input_ids, pad_ids], dim=0)
                attention_mask = torch.cat([attention_mask, pad_mask], dim=0)

        labels = input_ids.clone()

        return {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "labels": labels,
        }


def collate_dynamic_padding(batch_list: List[dict], pad_token_id: int = 0) -> Batch:
    """Collate function with dynamic padding to longest sequence in batch.

    More efficient than max_length padding when sequences vary in length.

    Args:
        batch_list: List of dicts with variable-length tensors
        pad_token_id: Token ID to use for padding

    Returns:
        Batch object with dynamically padded tensors
    """
    max_len = max(item["input_ids"].size(0) for item in batch_list)

    batch_size = len(batch_list)

    input_ids = torch.full((batch_size, max_len), pad_token_id, dtype=torch.long)
    attention_mask = torch.zeros((batch_size, max_len), dtype=torch.long)
    labels = torch.full((batch_size, max_len), -100, dtype=torch.long)

    for i, item in enumerate(batch_list):
        seq_len = item["input_ids"].size(0)
        input_ids[i, :seq_len] = item["input_ids"]
        attention_mask[i, :seq_len] = item["attention_mask"]
        labels[i, :seq_len] = item["labels"]

    return Batch(
        input_ids=input_ids,
        attention_mask=attention_mask,
        labels=labels,
    )


def create_dataloader(
    texts: List[str],
    tokenizer,
    max_length: int = 512,
    batch_size: int = 32,
    shuffle: bool = True,
    num_workers: int = 0,
    padding_strategy: str = "max_length",
    pad_token_id: int = 0,
    pin_memory: bool = True,
) -> DataLoader:
    """Utility function to create a DataLoader with proper collate function.

    Args:
        texts: List of text strings
        tokenizer: Tokenizer instance
        max_length: Maximum sequence length
        batch_size: Batch size
        shuffle: Whether to shuffle data
        num_workers: Number of worker processes
        padding_strategy: "max_length" or "longest" (dynamic)
        pad_token_id: Padding token ID for dynamic padding
        pin_memory: Use pinned memory for faster GPU transfer (default: True)

    Returns:
        DataLoader instance ready for training

    Example:
        >>> dataloader = create_dataloader(
        ...     texts=train_texts,
        ...     tokenizer=my_tokenizer,
        ...     batch_size=32,
        ...     padding_strategy="longest"  # More efficient
        ... )
        >>> for batch in dataloader:
        ...     # batch is a Batch object
        ...     logits = model(batch.input_ids, batch.attention_mask)
    """
    dataset = TextDataset(
        texts=texts,
        tokenizer=tokenizer,
        max_length=max_length,
        padding_strategy=padding_strategy,
        pad_token_id=pad_token_id,
    )

    if padding_strategy == "longest":
        collate_fn = lambda batch: collate_dynamic_padding(batch, pad_token_id)
    else:
        collate_fn = collate_batch

    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=num_workers,
        collate_fn=collate_fn,
        pin_memory=pin_memory,
    )