"""Base trainer class with flexible architecture support."""

from typing import Optional, Union, Callable, Dict, Any, List
from abc import ABC, abstractmethod
import torch
from torch.cuda.amp import autocast, GradScaler
from torch.utils.data import DataLoader
from .dataloader import create_dataloader, Batch


class BaseTrainer(ABC):
    """Abstract base class for training different model architectures.
    
    This class provides the core training loop logic while allowing
    subclasses to customize loss computation and output processing.
    
    Args:
        model: The model to train
        tokenizer: Tokenizer instance
        optimizer: Optional custom optimizer. If None, uses AdamW
        lr: Learning rate (used if optimizer is None)
        device: Training device ("cuda" or "cpu")
        use_amp: Enable automatic mixed precision training
        pad_token_id: Padding token ID. If None, uses tokenizer.pad_id
        
    Example:
        >>> class MyTrainer(BaseTrainer):
        ...     def compute_loss(self, model_output, batch):
        ...         logits = self.extract_logits(model_output)
        ...         return F.cross_entropy(logits.view(-1, self.vocab_size), 
        ...                                batch.labels.view(-1))
        >>> 
        >>> trainer = MyTrainer(model, tokenizer)
        >>> trainer.train(texts, epochs=5)
    """
    
    def __init__(
        self,
        model: torch.nn.Module,
        tokenizer,
        optimizer: Optional[torch.optim.Optimizer] = None,
        lr: float = 3e-4,
        device: str = "cuda",
        use_amp: bool = True,
        pad_token_id: Optional[int] = None,
    ):
        self.model = model
        self.tokenizer = tokenizer
        self.lr = lr
        self.use_amp = use_amp
        self.pad_token_id = pad_token_id or tokenizer.pad_id
        
        # Setup device
        self.device = torch.device(device if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        
        # Setup optimizer
        if optimizer is None:
            self.optimizer = torch.optim.AdamW(self.model.parameters(), lr=self.lr)
        else:
            self.optimizer = optimizer
            
        # Setup gradient scaler for mixed precision
        self.scaler = GradScaler(enabled=self.use_amp)
        
        # Cache vocab size
        self.vocab_size = tokenizer.vocab_size
        
    @abstractmethod
    def compute_loss(
        self, 
        model_output: Union[torch.Tensor, Dict[str, torch.Tensor]], 
        batch: Batch
    ) -> torch.Tensor:
        """Compute loss from model output and batch.
        
        Args:
            model_output: Output from model.forward()
            batch: Batch containing input_ids, attention_mask, labels
            
        Returns:
            Loss tensor
        """
        pass
    
    def extract_logits(
        self, 
        output: Union[torch.Tensor, Dict[str, torch.Tensor]], 
        key: str = "logits"
    ) -> torch.Tensor:
        """Extract logits tensor from model output.
        
        Args:
            output: Model output (tensor or dict)
            key: Key to use if output is dict
            
        Returns:
            Logits tensor of shape (batch, seq_len, vocab_size)
        """
        if isinstance(output, dict):
            if key in output:
                return output[key]
            # Try common alternatives
            for k in ["logits", "mlm_logits", "lm_logits", "prediction_logits"]:
                if k in output:
                    return output[k]
            raise KeyError(f"Could not find logits in output. Available keys: {list(output.keys())}")
        return output
    
    def prepare_batch(self, batch_data) -> Batch:
        """Prepare batch by moving to device.
        
        Args:
            batch_data: Raw batch from dataloader (can be Batch or Dict)
            
        Returns:
            Batch with tensors on correct device
        """
        # Handle both Batch namedtuple and dict from collators
        if isinstance(batch_data, dict):
            return Batch(
                input_ids=batch_data["input_ids"].to(self.device, non_blocking=True),
                attention_mask=batch_data["attention_mask"].to(self.device, non_blocking=True),
                labels=batch_data["labels"].to(self.device, non_blocking=True),
            )
        else:
            return Batch(
                input_ids=batch_data.input_ids.to(self.device, non_blocking=True),
                attention_mask=batch_data.attention_mask.to(self.device, non_blocking=True),
                labels=batch_data.labels.to(self.device, non_blocking=True),
            )
    
    def get_model_inputs(self, batch: Batch) -> Dict[str, Any]:
        """Prepare inputs for model.forward().
        
        Override this to customize what gets passed to the model.
        
        Args:
            batch: Prepared batch
            
        Returns:
            Dictionary of keyword arguments for model.forward()
        """
        return {
            "input_ids": batch.input_ids,
            "key_padding_mask": batch.attention_mask == 0,
        }
    
    def training_step(self, batch_data) -> float:
        """Single training step.
        
        Args:
            batch_data: Raw batch from dataloader
            
        Returns:
            Loss value (float)
        """
        # Prepare batch
        batch = self.prepare_batch(batch_data)
        
        # Zero gradients
        self.optimizer.zero_grad()
        
        # Forward pass with mixed precision
        with autocast(enabled=self.use_amp):
            model_inputs = self.get_model_inputs(batch)
            model_output = self.model(**model_inputs)
            loss = self.compute_loss(model_output, batch)
        
        # Backward pass with gradient scaling
        self.scaler.scale(loss).backward()
        self.scaler.step(self.optimizer)
        self.scaler.update()
        
        return loss.item()
    
    def train(
        self,
        texts: Union[List[str], DataLoader] = None,
        dataloader: Optional[DataLoader] = None,
        epochs: int = 3,
        batch_size: int = 8,
        max_length: int = 512,
        padding_strategy: str = "max_length",
        shuffle: bool = True,
        verbose: bool = True,
    ):
        """Main training loop.
        
        Args:
            texts: List of training texts (if not using custom dataloader)
            dataloader: Custom DataLoader (e.g., with InstructionCollator).
                If provided, texts/batch_size/max_length are ignored.
            epochs: Number of epochs
            batch_size: Batch size (ignored if dataloader provided)
            max_length: Maximum sequence length (ignored if dataloader provided)
            padding_strategy: "max_length" or "longest" (ignored if dataloader provided)
            shuffle: Shuffle data each epoch (ignored if dataloader provided)
            verbose: Print progress
            
        Example:
            >>> # Simple usage with texts
            >>> trainer.train(texts=["text1", "text2"], epochs=5)
            >>> 
            >>> # Advanced usage with custom dataloader
            >>> from composennent.instruct import InstructionDataset, InstructionCollatorWithPromptMasking
            >>> dataset = InstructionDataset(data, format_type="chatml")
            >>> collator = InstructionCollatorWithPromptMasking(tokenizer, response_template="<|im_start|>assistant\\n")
            >>> dataloader = DataLoader(dataset, batch_size=4, collate_fn=collator)
            >>> trainer.train(dataloader=dataloader, epochs=5)
        """
        # Use custom dataloader if provided, otherwise create one from texts
        if dataloader is not None:
            train_dataloader = dataloader
        elif texts is not None:
            train_dataloader = create_dataloader(
                texts=texts,
                tokenizer=self.tokenizer,
                max_length=max_length,
                batch_size=batch_size,
                shuffle=shuffle,
                padding_strategy=padding_strategy,
                pad_token_id=self.pad_token_id,
            )
        else:
            raise ValueError("Either 'texts' or 'dataloader' must be provided")
        
        # Training loop
        self.model.train()
        
        for epoch in range(epochs):
            total_loss = 0.0
            num_batches = 0
            
            for batch_data in train_dataloader:
                loss = self.training_step(batch_data)
                total_loss += loss
                num_batches += 1
            
            avg_loss = total_loss / max(1, num_batches)
            
            if verbose:
                print(f"Epoch {epoch + 1}/{epochs}, Loss: {avg_loss:.4f}")
    
    def save_checkpoint(self, path: str):
        """Save model checkpoint.
        
        Args:
            path: Path to save checkpoint
        """
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'scaler_state_dict': self.scaler.state_dict(),
        }, path)
    
    def load_checkpoint(self, path: str):
        """Load model checkpoint.
        
        Args:
            path: Path to checkpoint
        """
        checkpoint = torch.load(path, map_location=self.device)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        if 'scaler_state_dict' in checkpoint:
            self.scaler.load_state_dict(checkpoint['scaler_state_dict'])
