"""Factory function for creating and using trainers automatically."""

from typing import Optional, Callable, Dict
import torch
from .trainers import (
    CausalLMTrainer,
    MaskedLMTrainer,
    Seq2SeqTrainer,
    CustomTrainer,
    MultiTaskTrainer,
)


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

