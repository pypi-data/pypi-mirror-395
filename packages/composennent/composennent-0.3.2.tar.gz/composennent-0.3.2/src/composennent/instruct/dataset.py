"""Instruction tuning dataset for fine-tuning language models."""

from torch.utils.data import Dataset
from typing import List, Dict, Optional
from composennent.instruct.format import FormatterRegistry
from composennent.nlp.tokenizers.base import BaseTokenizer


class InstructionDataset(Dataset):
    """Dataset for instruction tuning with flexible formatting.
    
    This dataset handles instruction-input-output triples and formats them
    according to various prompt templates (ChatML, Alpaca, etc.).
    
    Args:
        data: List of dictionaries with keys:
            - "instruction": The task instruction
            - "input": Optional context/input (can be empty string)
            - "output": The expected response (required for training)
            - "system": Optional system message
        tokenizer: Tokenizer instance (optional, used only for inference mode)
        format_type: Format template to use ("chatml", "alpaca", etc.)
        max_length: Maximum sequence length (default: 2048)
        inference_mode: If True, only format prompts without outputs (default: False)
        
    Example:
        >>> data = [
        ...     {
        ...         "instruction": "What is the capital of France?",
        ...         "input": "",
        ...         "output": "The capital of France is Paris."
        ...     }
        ... ]
        >>> dataset = InstructionDataset(data, format_type="chatml")
        >>> print(dataset[0])
        {'text': '<|im_start|>user\\nWhat is the capital...'}
    """
    
    def __init__(
        self,
        data: List[Dict],
        tokenizer: Optional[BaseTokenizer] = None,
        format_type: str = "chatml",
        max_length: int = 2048,
        inference_mode: bool = False,
    ):
        self.data = data
        self.tokenizer = tokenizer
        self.formatter = FormatterRegistry.get_formatter(format_type)
        self.max_length = max_length
        self.inference_mode = inference_mode
        
        # Validate data
        if not inference_mode:
            for idx, example in enumerate(data):
                if "output" not in example or not example["output"]:
                    raise ValueError(
                        f"Example {idx} missing 'output' field. "
                        f"Set inference_mode=True if you only need prompts."
                    )
    
    def __len__(self) -> int:
        """Return the number of examples in the dataset."""
        return len(self.data)
    
    def __getitem__(self, idx: int) -> Dict[str, str]:
        """Get a single example from the dataset.
        
        Args:
            idx: Index of the example
            
        Returns:
            Dictionary with 'text' key containing formatted prompt/completion
        """
        example = self.data[idx]
        
        if self.inference_mode:
            # For inference: just the prompt, no output
            text = self.formatter.format(
                instruction=example["instruction"],
                input_text=example.get("input", ""),
                system=example.get("system"),
            )
        else:
            # For training: full text with output
            text = self.formatter.format(
                instruction=example["instruction"],
                input_text=example.get("input", ""),
                output=example.get("output"),
                system=example.get("system"),
            )
        
        return {"text": text}
