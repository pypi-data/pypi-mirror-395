"""Data collators for instruction tuning datasets."""

import torch
from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from composennent.nlp.tokenizers.base import BaseTokenizer


@dataclass
class InstructionCollator:
    """Basic collator for instruction tuning datasets.
    
    This collator:
    1. Tokenizes text samples
    2. Pads them to the same length
    3. Creates labels for training
    4. Creates attention masks
    
    Args:
        tokenizer: Tokenizer instance
        max_length: Maximum sequence length (default: 2048)
        padding: Padding strategy - "longest" or "max_length" (default: "longest")
        ignore_index: Index to use for masked tokens in labels (default: -100)
        
    Example:
        >>> from torch.utils.data import DataLoader
        >>> collator = InstructionCollator(tokenizer, max_length=2048)
        >>> dataloader = DataLoader(dataset, batch_size=4, collate_fn=collator)
    """
    
    tokenizer: BaseTokenizer
    max_length: int = 2048
    padding: str = "longest"  # or "max_length"
    ignore_index: int = -100
    
    def __call__(self, batch: List[Dict[str, str]]) -> Dict[str, torch.Tensor]:
        """Collate a batch of examples into tensors.
        
        Args:
            batch: List of dictionaries with 'text' key
            
        Returns:
            Dictionary with:
                - input_ids: Tokenized and padded input (batch_size, seq_len)
                - attention_mask: Mask for valid tokens (batch_size, seq_len)
                - labels: Labels for training (batch_size, seq_len)
        """
        texts = [item["text"] for item in batch]
        
        # Determine padding length
        if self.padding == "max_length":
            pad_length = self.max_length
        else:
            # Find longest sequence in batch
            all_tokens = [self.tokenizer.encode(text) for text in texts]
            pad_length = min(max(len(t) for t in all_tokens), self.max_length)
        
        # Tokenize and pad each text
        input_ids_list = []
        attention_mask_list = []
        
        for text in texts:
            tokens = self.tokenizer.encode(text)
            
            # Truncate if needed
            if len(tokens) > self.max_length:
                tokens = tokens[:self.max_length]
            
            # Create attention mask (1 for real tokens, 0 for padding)
            attention_mask = [1] * len(tokens)
            
            # Pad to target length
            padding_length = pad_length - len(tokens)
            if padding_length > 0:
                tokens = tokens + [self.tokenizer.pad_token_id] * padding_length
                attention_mask = attention_mask + [0] * padding_length
            
            input_ids_list.append(tokens)
            attention_mask_list.append(attention_mask)
        
        # Convert to tensors
        input_ids = torch.tensor(input_ids_list, dtype=torch.long)
        attention_mask = torch.tensor(attention_mask_list, dtype=torch.long)
        
        # Create labels (copy of input_ids for causal LM training)
        labels = input_ids.clone()
        
        # Mask padding tokens in labels
        labels[labels == self.tokenizer.pad_token_id] = self.ignore_index
        
        return {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "labels": labels,
        }


@dataclass
class InstructionCollatorWithPromptMasking(InstructionCollator):
    """Advanced collator that masks the prompt in labels.
    
    This collator trains the model only on the response portion,
    not on the instruction/input. This is the recommended approach
    for instruction tuning as it prevents the model from learning
    to generate instructions.
    
    Args:
        tokenizer: Tokenizer instance
        max_length: Maximum sequence length (default: 2048)
        padding: Padding strategy - "longest" or "max_length" (default: "longest")
        ignore_index: Index to use for masked tokens in labels (default: -100)
        response_template: String that marks the start of the response.
            For ChatML: "<|im_start|>assistant\n"
            For Alpaca: "### Response:\n"
            
    Example:
        >>> collator = InstructionCollatorWithPromptMasking(
        ...     tokenizer,
        ...     response_template="<|im_start|>assistant\\n"
        ... )
        >>> dataloader = DataLoader(dataset, collate_fn=collator)
    """
    
    response_template: str = "<|im_start|>assistant\n"
    
    def __call__(self, batch: List[Dict[str, str]]) -> Dict[str, torch.Tensor]:
        """Collate batch with prompt masking.
        
        Args:
            batch: List of dictionaries with 'text' key
            
        Returns:
            Dictionary with input_ids, attention_mask, and labels (prompt masked)
        """
        texts = [item["text"] for item in batch]
        
        # Determine padding length
        if self.padding == "max_length":
            pad_length = self.max_length
        else:
            all_tokens = [self.tokenizer.encode(text) for text in texts]
            pad_length = min(max(len(t) for t in all_tokens), self.max_length)
        
        # Tokenize and pad
        input_ids_list = []
        attention_mask_list = []
        labels_list = []
        
        for text in texts:
            tokens = self.tokenizer.encode(text)
            
            # Truncate if needed
            if len(tokens) > self.max_length:
                tokens = tokens[:self.max_length]
            
            # Create labels and find response start
            labels = tokens.copy()
            
            # Find where response starts in the text
            response_start_idx = text.find(self.response_template)
            
            if response_start_idx != -1:
                # Tokenize the prompt portion to find its length
                prompt_text = text[:response_start_idx + len(self.response_template)]
                prompt_tokens = self.tokenizer.encode(prompt_text)
                prompt_length = min(len(prompt_tokens), len(tokens))
                
                # Mask all prompt tokens in labels
                labels[:prompt_length] = [self.ignore_index] * prompt_length
            else:
                # If response template not found, mask everything (safety)
                # This prevents training on malformed examples
                labels = [self.ignore_index] * len(tokens)
            
            # Create attention mask
            attention_mask = [1] * len(tokens)
            
            # Pad to target length
            padding_length = pad_length - len(tokens)
            if padding_length > 0:
                tokens = tokens + [self.tokenizer.pad_token_id] * padding_length
                attention_mask = attention_mask + [0] * padding_length
                labels = labels + [self.ignore_index] * padding_length
            
            input_ids_list.append(tokens)
            attention_mask_list.append(attention_mask)
            labels_list.append(labels)
        
        # Convert to tensors
        input_ids = torch.tensor(input_ids_list, dtype=torch.long)
        attention_mask = torch.tensor(attention_mask_list, dtype=torch.long)
        labels = torch.tensor(labels_list, dtype=torch.long)
        
        return {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "labels": labels,
        }


@dataclass
class InferenceCollator:
    """Collator for inference (no labels needed).
    
    Use this when generating text, not training.
    
    Args:
        tokenizer: Tokenizer instance
        max_length: Maximum sequence length (default: 2048)
        padding: Padding strategy (default: "longest")
        
    Example:
        >>> collator = InferenceCollator(tokenizer)
        >>> dataloader = DataLoader(dataset, collate_fn=collator)
        >>> for batch in dataloader:
        ...     outputs = model.generate(**batch)
    """
    
    tokenizer: BaseTokenizer
    max_length: int = 2048
    padding: str = "longest"
    
    def __call__(self, batch: List[Dict[str, str]]) -> Dict[str, torch.Tensor]:
        """Collate batch for inference.
        
        Args:
            batch: List of dictionaries with 'text' key
            
        Returns:
            Dictionary with input_ids and attention_mask only
        """
        texts = [item["text"] for item in batch]
        
        # Determine padding length
        if self.padding == "max_length":
            pad_length = self.max_length
        else:
            all_tokens = [self.tokenizer.encode(text) for text in texts]
            pad_length = min(max(len(t) for t in all_tokens), self.max_length)
        
        # Tokenize and pad
        input_ids_list = []
        attention_mask_list = []
        
        for text in texts:
            tokens = self.tokenizer.encode(text)
            
            # Truncate if needed
            if len(tokens) > self.max_length:
                tokens = tokens[:self.max_length]
            
            # Create attention mask
            attention_mask = [1] * len(tokens)
            
            # Pad
            padding_length = pad_length - len(tokens)
            if padding_length > 0:
                tokens = tokens + [self.tokenizer.pad_token_id] * padding_length
                attention_mask = attention_mask + [0] * padding_length
            
            input_ids_list.append(tokens)
            attention_mask_list.append(attention_mask)
        
        # Convert to tensors
        input_ids = torch.tensor(input_ids_list, dtype=torch.long)
        attention_mask = torch.tensor(attention_mask_list, dtype=torch.long)
        
        return {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
        }
