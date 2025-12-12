"""Specific trainer implementations for different model architectures."""

import torch
import torch.nn.functional as F
from typing import Optional, Union, Dict, Any, Callable
from .base_trainer import BaseTrainer, Batch


class CausalLMTrainer(BaseTrainer):
    """Trainer for causal language models (GPT-style).
    
    Uses next-token prediction objective where the model predicts
    token i from tokens 0..i-1.
    
    Args:
        model: Causal language model
        tokenizer: Tokenizer instance
        logits_key: Key to extract logits from dict output (default: "logits")
        **kwargs: Additional arguments passed to BaseTrainer
        
    Example:
        >>> from composennent.nlp.transformers import GPT
        >>> model = GPT(vocab_size=50000, latent_dim=768, num_heads=12, num_layers=12)
        >>> trainer = CausalLMTrainer(model, tokenizer)
        >>> trainer.train(texts, epochs=5, batch_size=16)
    """
    
    def __init__(
        self,
        model: torch.nn.Module,
        tokenizer,
        logits_key: str = "logits",
        **kwargs
    ):
        super().__init__(model, tokenizer, **kwargs)
        self.logits_key = logits_key
        self.criterion = torch.nn.CrossEntropyLoss(ignore_index=self.pad_token_id)
    
    def compute_loss(
        self, 
        model_output: Union[torch.Tensor, Dict[str, torch.Tensor]], 
        batch: Batch
    ) -> torch.Tensor:
        """Compute causal LM loss (next-token prediction).
        
        Args:
            model_output: Model output (tensor or dict)
            batch: Batch with input_ids and labels
            
        Returns:
            Cross-entropy loss
        """
        logits = self.extract_logits(model_output, key=self.logits_key)
        
        # Shift for next-token prediction
        logits_shifted = logits[:, :-1, :].contiguous()
        labels_shifted = batch.labels[:, 1:].contiguous()
        
        loss = self.criterion(
            logits_shifted.view(-1, self.vocab_size),
            labels_shifted.view(-1),
        )
        return loss


class MaskedLMTrainer(BaseTrainer):
    """Trainer for masked language models (BERT-style).
    
    Uses masked language modeling objective where random tokens
    are masked and the model predicts them.
    
    Args:
        model: Masked language model
        tokenizer: Tokenizer instance
        logits_key: Key to extract logits from dict output (default: "mlm_logits")
        **kwargs: Additional arguments passed to BaseTrainer
        
    Example:
        >>> from composennent.nlp.transformers import Bert
        >>> model = Bert(vocab_size=30000, latent_dim=768, num_heads=12, num_layers=12)
        >>> trainer = MaskedLMTrainer(model, tokenizer, logits_key="mlm_logits")
        >>> trainer.train(texts, epochs=5)
    """
    
    def __init__(
        self,
        model: torch.nn.Module,
        tokenizer,
        logits_key: str = "mlm_logits",
        **kwargs
    ):
        super().__init__(model, tokenizer, **kwargs)
        self.logits_key = logits_key
        # Ignore positions with label -100 (non-masked tokens)
        self.criterion = torch.nn.CrossEntropyLoss(ignore_index=-100)
    
    def compute_loss(
        self, 
        model_output: Union[torch.Tensor, Dict[str, torch.Tensor]], 
        batch: Batch
    ) -> torch.Tensor:
        """Compute masked LM loss.
        
        Args:
            model_output: Model output (tensor or dict)
            batch: Batch with input_ids and labels (with -100 for non-masked)
            
        Returns:
            Cross-entropy loss only on masked positions
        """
        logits = self.extract_logits(model_output, key=self.logits_key)
        
        # No shifting - predict masked positions directly
        loss = self.criterion(
            logits.view(-1, self.vocab_size),
            batch.labels.view(-1),
        )
        return loss
    
    def get_model_inputs(self, batch: Batch) -> Dict[str, Any]:
        """Prepare inputs for BERT model.
        
        Adds token_type_ids and uses attention_mask instead of key_padding_mask.
        
        Args:
            batch: Prepared batch
            
        Returns:
            Dictionary with BERT-specific inputs
        """
        return {
            "input_ids": batch.input_ids,
            "attention_mask": batch.attention_mask,
            "token_type_ids": None,  # Can be customized
        }


class Seq2SeqTrainer(BaseTrainer):
    """Trainer for sequence-to-sequence models (T5, BART-style).
    
    Uses encoder-decoder architecture for sequence-to-sequence tasks.
    
    Args:
        model: Seq2seq model
        tokenizer: Tokenizer instance
        logits_key: Key to extract logits from dict output
        **kwargs: Additional arguments passed to BaseTrainer
        
    Example:
        >>> from composennent.nlp.transformers import T5
        >>> model = T5(vocab_size=32000, latent_dim=768, num_heads=12, num_layers=12)
        >>> trainer = Seq2SeqTrainer(model, tokenizer)
        >>> trainer.train(texts, epochs=5)
    """
    
    def __init__(
        self,
        model: torch.nn.Module,
        tokenizer,
        logits_key: str = "logits",
        **kwargs
    ):
        super().__init__(model, tokenizer, **kwargs)
        self.logits_key = logits_key
        self.criterion = torch.nn.CrossEntropyLoss(ignore_index=self.pad_token_id)
    
    def compute_loss(
        self, 
        model_output: Union[torch.Tensor, Dict[str, torch.Tensor]], 
        batch: Batch
    ) -> torch.Tensor:
        """Compute seq2seq loss.
        
        Args:
            model_output: Model output (tensor or dict)
            batch: Batch with input_ids and labels
            
        Returns:
            Cross-entropy loss
        """
        logits = self.extract_logits(model_output, key=self.logits_key)
        
        loss = self.criterion(
            logits.view(-1, self.vocab_size),
            batch.labels.view(-1),
        )
        return loss
    
    def get_model_inputs(self, batch: Batch) -> Dict[str, Any]:
        """Prepare inputs for seq2seq model.
        
        Args:
            batch: Prepared batch
            
        Returns:
            Dictionary with encoder and decoder inputs
        """
        return {
            "input_ids": batch.input_ids,
            "attention_mask": batch.attention_mask,
            "decoder_input_ids": batch.labels,  # Can be customized
            "decoder_attention_mask": None,
        }


class CustomTrainer(BaseTrainer):
    """Trainer with custom loss function.
    
    Allows complete customization of the loss computation.
    
    Args:
        model: The model to train
        tokenizer: Tokenizer instance
        loss_fn: Custom loss function with signature:
            loss_fn(model_output, batch, vocab_size) -> loss
        logits_key: Key to extract logits from dict output
        **kwargs: Additional arguments passed to BaseTrainer
        
    Example:
        >>> def my_loss(model_output, batch, vocab_size):
        ...     logits = model_output if isinstance(model_output, torch.Tensor) else model_output["logits"]
        ...     return F.cross_entropy(logits.view(-1, vocab_size), batch.labels.view(-1))
        >>> 
        >>> trainer = CustomTrainer(model, tokenizer, loss_fn=my_loss)
        >>> trainer.train(texts, epochs=5)
    """
    
    def __init__(
        self,
        model: torch.nn.Module,
        tokenizer,
        loss_fn: callable,
        logits_key: str = "logits",
        **kwargs
    ):
        super().__init__(model, tokenizer, **kwargs)
        self.loss_fn = loss_fn
        self.logits_key = logits_key
    
    def compute_loss(
        self, 
        model_output: Union[torch.Tensor, Dict[str, torch.Tensor]], 
        batch: Batch
    ) -> torch.Tensor:
        """Compute loss using custom function.
        
        Args:
            model_output: Model output (tensor or dict)
            batch: Batch with input_ids and labels
            
        Returns:
            Loss from custom function
        """
        return self.loss_fn(model_output, batch, self.vocab_size)


class MultiTaskTrainer(BaseTrainer):
    """Trainer for multi-task learning (e.g., BERT with MLM + NSP).
    
    Supports models that output multiple losses or predictions.
    
    Args:
        model: Multi-task model
        tokenizer: Tokenizer instance
        task_weights: Dictionary mapping task names to loss weights
        **kwargs: Additional arguments passed to BaseTrainer
        
    Example:
        >>> # BERT with MLM + NSP
        >>> model = Bert(vocab_size=30000, latent_dim=768, num_heads=12, num_layers=12)
        >>> trainer = MultiTaskTrainer(
        ...     model, 
        ...     tokenizer,
        ...     task_weights={"mlm": 1.0, "nsp": 0.5}
        ... )
        >>> trainer.train(texts, epochs=5)
    """
    
    def __init__(
        self,
        model: torch.nn.Module,
        tokenizer,
        task_weights: Optional[Dict[str, float]] = None,
        **kwargs
    ):
        super().__init__(model, tokenizer, **kwargs)
        self.task_weights = task_weights or {"mlm": 1.0, "nsp": 1.0}
        
        # Setup criteria for different tasks
        self.mlm_criterion = torch.nn.CrossEntropyLoss(ignore_index=-100)
        self.nsp_criterion = torch.nn.CrossEntropyLoss()
    
    def compute_loss(
        self, 
        model_output: Dict[str, torch.Tensor], 
        batch: Batch
    ) -> torch.Tensor:
        """Compute weighted multi-task loss.
        
        Args:
            model_output: Dictionary with task outputs
            batch: Batch with input_ids and labels
            
        Returns:
            Weighted sum of task losses
        """
        total_loss = 0.0
        
        # MLM loss
        if "mlm_logits" in model_output and "mlm" in self.task_weights:
            mlm_logits = model_output["mlm_logits"]
            mlm_loss = self.mlm_criterion(
                mlm_logits.view(-1, self.vocab_size),
                batch.labels.view(-1),
            )
            total_loss += self.task_weights["mlm"] * mlm_loss
        
        # NSP loss
        if "nsp_logits" in model_output and "nsp" in self.task_weights:
            # Assuming batch has nsp_labels attribute
            nsp_logits = model_output["nsp_logits"]
            nsp_labels = getattr(batch, "nsp_labels", torch.zeros(nsp_logits.size(0), dtype=torch.long, device=nsp_logits.device))
            nsp_loss = self.nsp_criterion(nsp_logits, nsp_labels)
            total_loss += self.task_weights["nsp"] * nsp_loss
        
        return total_loss
    
    def get_model_inputs(self, batch: Batch) -> Dict[str, Any]:
        """Prepare inputs for multi-task model.
        
        Args:
            batch: Prepared batch
            
        Returns:
            Dictionary with model inputs
        """
        return {
            "input_ids": batch.input_ids,
            "attention_mask": batch.attention_mask,
            "token_type_ids": getattr(batch, "token_type_ids", None),
        }


# ============================================================================
# Factory function for automatic trainer selection
# ============================================================================

def train(
    model: torch.nn.Module,
    texts,
    tokenizer,
    epochs: int = 3,
    batch_size: int = 8,
    max_length: int = 512,
    optimizer: Optional[torch.optim.Optimizer] = None,
    lr: float = 3e-4,
    device: str = "cuda",
    padding_strategy: str = "max_length",
    pad_token_id: Optional[int] = None,
    use_amp: bool = True,
    model_type: str = "causal_lm",
    logits_key: str = None,
    loss_fn: Optional[Callable] = None,
    task_weights: Optional[Dict[str, float]] = None,
    shuffle: bool = True,
    verbose: bool = True,
):
    """Automatic trainer selection and training.
    
    This function automatically selects the appropriate trainer class
    based on the model_type parameter, creates a trainer instance,
    and runs training.
    
    Args:
        model: The model to train
        texts: List of training texts
        tokenizer: Tokenizer instance
        epochs: Number of training epochs (default: 3)
        batch_size: Batch size (default: 8)
        max_length: Maximum sequence length (default: 512)
        optimizer: Optional custom optimizer. If None, uses AdamW
        lr: Learning rate (default: 3e-4)
        device: Training device - "cuda" or "cpu" (default: "cuda")
        padding_strategy: "max_length" or "longest" (default: "max_length")
        pad_token_id: Padding token ID. If None, uses tokenizer.pad_id
        use_amp: Enable automatic mixed precision (default: True)
        model_type: Type of trainer to use. Options:
            - "causal_lm": Causal language modeling (GPT-style)
            - "mlm": Masked language modeling (BERT-style)
            - "seq2seq": Sequence-to-sequence (T5, BART-style)
            - "multitask": Multi-task learning (BERT MLM+NSP)
            - "custom": Use custom loss function
        logits_key: Key to extract logits from dict output.
            Defaults: "logits" for causal_lm, "mlm_logits" for mlm
        loss_fn: Custom loss function (required if model_type="custom")
        task_weights: Task weights for multitask learning (e.g., {"mlm": 1.0, "nsp": 0.5})
        shuffle: Shuffle data each epoch (default: True)
        verbose: Print training progress (default: True)
    
    Returns:
        The trainer instance (can be used for checkpointing, etc.)
    
    Examples:
        >>> # GPT-style causal LM (default)
        >>> train(gpt_model, texts, tokenizer, epochs=5)
        
        >>> # BERT masked LM
        >>> train(bert_model, texts, tokenizer, model_type="mlm", logits_key="mlm_logits")
        
        >>> # Custom loss
        >>> def my_loss(output, batch, vocab_size):
        ...     return custom_computation(output, batch)
        >>> train(model, texts, tokenizer, model_type="custom", loss_fn=my_loss)
        
        >>> # Multi-task BERT
        >>> train(bert_model, texts, tokenizer, model_type="multitask",
        ...       task_weights={"mlm": 1.0, "nsp": 0.5})
    """
    # Auto-set default logits_key based on model_type if not provided
    if logits_key is None:
        logits_key_defaults = {
            "causal_lm": "logits",
            "mlm": "mlm_logits",
            "seq2seq": "logits",
            "custom": "logits",
            "multitask": "mlm_logits",
        }
        logits_key = logits_key_defaults.get(model_type, "logits")
    
    # Select and create appropriate trainer
    if model_type == "causal_lm":
        trainer = CausalLMTrainer(
            model=model,
            tokenizer=tokenizer,
            optimizer=optimizer,
            lr=lr,
            device=device,
            use_amp=use_amp,
            pad_token_id=pad_token_id,
            logits_key=logits_key,
        )
    
    elif model_type == "mlm":
        trainer = MaskedLMTrainer(
            model=model,
            tokenizer=tokenizer,
            optimizer=optimizer,
            lr=lr,
            device=device,
            use_amp=use_amp,
            pad_token_id=pad_token_id,
            logits_key=logits_key,
        )
    
    elif model_type == "seq2seq":
        trainer = Seq2SeqTrainer(
            model=model,
            tokenizer=tokenizer,
            optimizer=optimizer,
            lr=lr,
            device=device,
            use_amp=use_amp,
            pad_token_id=pad_token_id,
            logits_key=logits_key,
        )
    
    elif model_type == "multitask":
        trainer = MultiTaskTrainer(
            model=model,
            tokenizer=tokenizer,
            optimizer=optimizer,
            lr=lr,
            device=device,
            use_amp=use_amp,
            pad_token_id=pad_token_id,
            task_weights=task_weights,
        )
    
    elif model_type == "custom":
        if loss_fn is None:
            raise ValueError("loss_fn must be provided when model_type='custom'")
        trainer = CustomTrainer(
            model=model,
            tokenizer=tokenizer,
            optimizer=optimizer,
            lr=lr,
            device=device,
            use_amp=use_amp,
            pad_token_id=pad_token_id,
            loss_fn=loss_fn,
            logits_key=logits_key,
        )
    
    else:
        raise ValueError(
            f"Unknown model_type: '{model_type}'. "
            f"Choose from: 'causal_lm', 'mlm', 'seq2seq', 'multitask', or 'custom'"
        )
    
    # Run training
    trainer.train(
        texts=texts,
        epochs=epochs,
        batch_size=batch_size,
        max_length=max_length,
        padding_strategy=padding_strategy,
        shuffle=shuffle,
        verbose=verbose,
    )
    
    # Return trainer instance for checkpointing, etc.
    return trainer

