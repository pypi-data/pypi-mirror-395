"""Base class for transformer language models."""

import torch
import torch.nn as nn
from typing import Optional, Union, Callable, Dict, Any
from abc import ABC, abstractmethod


class BaseLanguageModel(nn.Module, ABC):
    """Base class for all transformer-based language models.

    This class provides common functionality for language models including:
    - Text generation (sampling, greedy, beam search)
    - Model saving and loading with configuration
    - Common interface for forward pass

    All transformer models (GPT, BERT, etc.) should inherit from this class.
    """

    def __init__(self):
        super().__init__()

        self.vocab_size = None
        self.latent_dim = None
        self.num_heads = None
        self.num_layers = None
        self.max_seq_len = None
        self.drop_out = None
        self.mlp_ratio = None

    @abstractmethod
    def forward(
        self,
        input_ids: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
        **kwargs
    ) -> torch.Tensor:
        """Forward pass of the model.

        Args:
            input_ids: Token IDs of shape (batch, seq_len)
            attention_mask: Optional attention mask
            **kwargs: Additional model-specific arguments

        Returns:
            Model outputs (logits, hidden states, etc.)
        """
        pass

    def get_config(self) -> dict:
        """Get model configuration as a dictionary.

        Returns:
            Dictionary containing model configuration.
        """
        return {
            "vocab_size": self.vocab_size,
            "latent_dim": self.latent_dim,
            "num_heads": self.num_heads,
            "num_layers": self.num_layers,
            "max_seq_len": self.max_seq_len,
            "drop_out": self.drop_out,
            "mlp_ratio": self.mlp_ratio,
        }

    def save(self, path: str) -> None:
        """Save model weights and configuration.

        Args:
            path: Path to save the model (e.g., "model.pt")

        Example:
            >>> model.save("my_model.pt")
        """
        checkpoint = {
            "model_state_dict": self.state_dict(),
            "config": self.get_config(),
            "model_type": self.__class__.__name__,
        }
        torch.save(checkpoint, path)
        print(f"Model saved to {path}")

    @classmethod
    def load(cls, path: str, device: str = "cpu", **model_kwargs):
        """Load model from saved checkpoint.

        Args:
            path: Path to the saved model
            device: Device to load model on ("cpu" or "cuda")
            **model_kwargs: If loading old checkpoint without config, provide model parameters

        Returns:
            Loaded model instance

        Example:
            >>> # Load new checkpoint (with config)
            >>> model = GPT.load("my_model.pt")
            >>>
            >>> # Load on GPU
            >>> model = GPT.load("my_model.pt", device="cuda")
            >>>
            >>> # Load old checkpoint (without config)
            >>> model = GPT.load("old_model.pt", vocab_size=50257, latent_dim=768,
            ...                  num_heads=12, num_layers=12, max_seq_len=1024)
        """
        checkpoint = torch.load(path, map_location=device)


        if "config" in checkpoint:
            config = checkpoint["config"]


            model = cls(**config)


            model.load_state_dict(checkpoint["model_state_dict"])
        else:

            if "model_state_dict" in checkpoint:
                state_dict = checkpoint["model_state_dict"]
            else:

                state_dict = checkpoint


            if not model_kwargs:
                raise ValueError(
                    f"Loading old checkpoint without config requires model parameters. "
                    f"Please provide: vocab_size, latent_dim, num_heads, num_layers, "
                    f"max_seq_len, drop_out (optional), mlp_ratio (optional)"
                )


            model = cls(**model_kwargs)


            model.load_state_dict(state_dict)

        model.to(device)
        model.eval()

        print(f"Model loaded from {path}")
        return model

    def generate(
        self,
        input: Union[str, torch.Tensor, list],
        tokenizer,
        max_length: int = 50,
        temperature: float = 1.0,
        top_k: int = 50,
        top_p: float = 0.95,
        do_sample: bool = True,
        num_return_sequences: int = 1,
        device: Optional[str] = None,
    ) -> Union[str, list]:
        """Generate text from input.

        Simple interface: pass text, get text back.

        Args:
            input: Input text string, or token IDs (tensor/list)
            tokenizer: Tokenizer instance for encoding/decoding
            max_length: Maximum number of tokens to generate (default: 50)
            temperature: Sampling temperature (higher = more random) (default: 1.0)
            top_k: Keep only top k tokens for sampling (default: 50)
            top_p: Nucleus sampling threshold (default: 0.95)
            do_sample: Whether to use sampling (True) or greedy (False) (default: True)
            num_return_sequences: Number of sequences to generate (default: 1)
            device: Device to use. If None, inferred from model

        Returns:
            Generated text string (if num_return_sequences=1)
            List of text strings (if num_return_sequences>1)

        Example:
            >>> model = GPT.load("models/gpt.pt")
            >>>
            >>> # Simple usage - pass text, get text
            >>> output = model.generate("Hello", tokenizer, max_length=50)
            >>> print(output)  # "Hello world! How are you today?..."
            >>>
            >>> # Generate multiple sequences
            >>> outputs = model.generate("Hello", tokenizer, num_return_sequences=3)
            >>> for text in outputs:
            ...     print(text)
        """
        self.eval()


        if isinstance(input, str):

            input_ids = tokenizer.encode(input)
            if not isinstance(input_ids, torch.Tensor):
                input_ids = torch.tensor([input_ids], dtype=torch.long)
            elif input_ids.dim() == 1:
                input_ids = input_ids.unsqueeze(0)
        elif isinstance(input, list):

            input_ids = torch.tensor([input], dtype=torch.long)
        else:

            input_ids = input
            if input_ids.dim() == 1:
                input_ids = input_ids.unsqueeze(0)


        if device is None:
            device = next(self.parameters()).device
        input_ids = input_ids.to(device)


        eos_token_id = getattr(tokenizer, 'eos_token_id', None) or getattr(tokenizer, 'eos_id', None)


        if num_return_sequences > 1:
            input_ids = input_ids.repeat_interleave(num_return_sequences, dim=0)

        generated = input_ids

        with torch.no_grad():
            for _ in range(max_length):

                if generated.size(1) > self.max_seq_len:
                    input_chunk = generated[:, -self.max_seq_len:]
                else:
                    input_chunk = generated


                logits = self.forward(input_chunk)


                next_token_logits = logits[:, -1, :]

                if do_sample:

                    next_token_logits = next_token_logits / temperature


                    if top_k > 0:
                        indices_to_remove = next_token_logits < torch.topk(next_token_logits, top_k)[0][..., -1, None]
                        next_token_logits[indices_to_remove] = float('-inf')


                    if top_p < 1.0:
                        sorted_logits, sorted_indices = torch.sort(next_token_logits, descending=True)
                        cumulative_probs = torch.cumsum(torch.softmax(sorted_logits, dim=-1), dim=-1)


                        sorted_indices_to_remove = cumulative_probs > top_p

                        sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
                        sorted_indices_to_remove[..., 0] = 0

                        indices_to_remove = sorted_indices_to_remove.scatter(1, sorted_indices, sorted_indices_to_remove)
                        next_token_logits[indices_to_remove] = float('-inf')


                    probs = torch.softmax(next_token_logits, dim=-1)
                    next_token = torch.multinomial(probs, num_samples=1)
                else:

                    next_token = next_token_logits.argmax(dim=-1, keepdim=True)


                if eos_token_id is not None:

                    if (next_token == eos_token_id).all():
                        break


                generated = torch.cat([generated, next_token], dim=1)


                if generated.size(1) >= self.max_seq_len:
                    break


        if num_return_sequences == 1:

            output_ids = generated[0].tolist()
            return tokenizer.decode(output_ids, skip_special_tokens=True)
        else:

            outputs = []
            for seq in generated:
                output_ids = seq.tolist()
                outputs.append(tokenizer.decode(output_ids, skip_special_tokens=True))
            return outputs

    def generate_greedy(
        self,
        input_ids: Union[torch.Tensor, list],
        max_length: int = 50,
        eos_token_id: Optional[int] = None,
        device: Optional[str] = None,
    ) -> torch.Tensor:
        """Generate text using greedy decoding (always pick most likely token).

        Convenience method for greedy generation.

        Args:
            input_ids: Input token IDs. Can be:
                - torch.Tensor of shape (batch, seq_len)
                - List of token IDs (will be converted to tensor)
            max_length: Maximum number of tokens to generate.
            eos_token_id: End-of-sequence token ID to stop generation.
            device: Device to use. If None, inferred from input_ids or uses cpu.

        Returns:
            Generated token IDs.

        Example:
            >>> # With tensor
            >>> generated = model.generate_greedy(input_ids, max_length=50)
            >>>
            >>> # With list
            >>> generated = model.generate_greedy([1, 2, 3], max_length=50, device="cuda")
        """
        return self.generate(
            input_ids,
            max_length=max_length,
            eos_token_id=eos_token_id,
            do_sample=False,
            device=device,
        )

    def decode_outputs(self, outputs: torch.Tensor, tokenizer, skip_special_tokens: bool = True):
        """Decode model outputs to text using a tokenizer.

        Helper method to convert generate() outputs to text.

        Args:
            outputs: Output tensor from generate() of shape (batch, seq_len)
            tokenizer: Tokenizer with a decode() method
            skip_special_tokens: Whether to skip special tokens

        Returns:
            Single string if batch_size=1, otherwise list of strings

        Example:
            >>> output = model.generate(input_ids, max_length=50)
            >>> text = model.decode_outputs(output, tokenizer)
            >>> print(text)
            >>>
            >>> # Multiple sequences
            >>> outputs = model.generate(input_ids, num_return_sequences=3)
            >>> texts = model.decode_outputs(outputs, tokenizer)
            >>> for text in texts:
            ...     print(text)
        """

        if outputs.size(0) == 1:
            return tokenizer.decode(outputs[0].tolist(), skip_special_tokens=skip_special_tokens)


        return [
            tokenizer.decode(seq.tolist(), skip_special_tokens=skip_special_tokens)
            for seq in outputs
        ]

    def num_parameters(self, only_trainable: bool = False) -> int:
        """Count the number of parameters in the model.

        Args:
            only_trainable: If True, count only trainable parameters.

        Returns:
            Number of parameters.

        Example:
            >>> print(f"Total parameters: {model.num_parameters():,}")
            >>> print(f"Trainable parameters: {model.num_parameters(only_trainable=True):,}")
        """
        if only_trainable:
            return sum(p.numel() for p in self.parameters() if p.requires_grad)
        return sum(p.numel() for p in self.parameters())

    def freeze(self) -> None:
        """Freeze all model parameters (set requires_grad=False).

        Example:
            >>> model.freeze()
            >>> # Now model parameters won't be updated during training
        """
        for param in self.parameters():
            param.requires_grad = False

    def unfreeze(self) -> None:
        """Unfreeze all model parameters (set requires_grad=True).

        Example:
            >>> model.unfreeze()
            >>> # Now model parameters can be updated during training
        """
        for param in self.parameters():
            param.requires_grad = True

    def freeze_embeddings(self) -> None:
        """Freeze only the embedding layers.

        Example:
            >>> model.freeze_embeddings()
            >>> # Embeddings frozen, rest of model can be trained
        """
        if hasattr(self, 'token_embedding'):
            for param in self.token_embedding.parameters():
                param.requires_grad = False
        if hasattr(self, 'position_embedding'):
            for param in self.position_embedding.parameters():
                param.requires_grad = False

    def get_memory_footprint(self) -> dict:
        """Get memory footprint of the model.

        Returns:
            Dictionary with memory information in MB.

        Example:
            >>> memory = model.get_memory_footprint()
            >>> print(f"Model size: {memory['total_mb']:.2f} MB")
        """
        param_size = sum(p.numel() * p.element_size() for p in self.parameters())
        buffer_size = sum(b.numel() * b.element_size() for b in self.buffers())

        total_size = param_size + buffer_size

        return {
            "params_mb": param_size / 1024 / 1024,
            "buffers_mb": buffer_size / 1024 / 1024,
            "total_mb": total_size / 1024 / 1024,
        }

    def __repr__(self) -> str:
        """String representation of the model."""
        config = self.get_config()
        config_str = ", ".join([f"{k}={v}" for k, v in config.items() if v is not None])
        return f"{self.__class__.__name__}({config_str})"

    def pretrain(
        self,
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
        """Pre-train the model from scratch.

        This method provides a simple interface for pre-training language models
        with support for various training paradigms (causal LM, masked LM, seq2seq, etc.).

        Args:
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
                - "causal_lm": Causal language modeling (GPT-style) - default
                - "mlm": Masked language modeling (BERT-style)
                - "seq2seq": Sequence-to-sequence (T5, BART-style)
                - "multitask": Multi-task learning (BERT MLM+NSP)
                - "custom": Use custom loss function
            logits_key: Key to extract logits from dict output
            loss_fn: Custom loss function (required if model_type="custom")
            task_weights: Task weights for multitask learning
            shuffle: Shuffle data each epoch (default: True)
            verbose: Print training progress (default: True)

        Returns:
            The trainer instance (can be used for checkpointing, etc.)

        Example:
            >>> # Simple GPT-style pre-training
            >>> model = GPT(vocab_size=50257, latent_dim=768, num_heads=12, num_layers=12)
            >>> model.pretrain(texts, tokenizer, epochs=5, batch_size=16)
            >>>
            >>> # BERT-style masked language modeling
            >>> bert_model = BERT(vocab_size=30522, latent_dim=768, num_heads=12, num_layers=12)
            >>> bert_model.pretrain(texts, tokenizer, model_type="mlm", epochs=3)
            >>>
            >>> # Custom loss function
            >>> def my_loss(output, batch, vocab_size):
            ...     return custom_computation(output, batch)
            >>> model.pretrain(texts, tokenizer, model_type="custom", loss_fn=my_loss)
        """

        from composennent.training import train as training_fn


        trainer = training_fn(
            model=self,
            texts=texts,
            tokenizer=tokenizer,
            epochs=epochs,
            batch_size=batch_size,
            max_length=max_length,
            optimizer=optimizer,
            lr=lr,
            device=device,
            padding_strategy=padding_strategy,
            pad_token_id=pad_token_id,
            use_amp=use_amp,
            model_type=model_type,
            logits_key=logits_key,
            loss_fn=loss_fn,
            task_weights=task_weights,
            shuffle=shuffle,
            verbose=verbose,
        )

        return trainer

    def fine_tune(
        self,
        texts,
        tokenizer,
        epochs: int = 3,
        batch_size: int = 8,
        max_length: int = 512,
        optimizer: Optional[torch.optim.Optimizer] = None,
        lr: float = 5e-5,
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
        """Fine-tune the model on task-specific data.

        Use this for adapting a pre-trained model to a specific task or domain
        (e.g., sentiment analysis, text classification) with task-specific data.

        Args:
            texts: List of training texts
            tokenizer: Tokenizer instance
            epochs: Number of training epochs (default: 3)
            batch_size: Batch size (default: 8)
            max_length: Maximum sequence length (default: 512)
            optimizer: Optional custom optimizer. If None, uses AdamW
            lr: Learning rate (default: 5e-5, lower than pre-training)
            device: Training device - "cuda" or "cpu" (default: "cuda")
            padding_strategy: "max_length" or "longest" (default: "max_length")
            pad_token_id: Padding token ID. If None, uses tokenizer.pad_id
            use_amp: Enable automatic mixed precision (default: True)
            model_type: "causal_lm", "mlm", "seq2seq", etc.
            logits_key: Key to extract logits from dict output
            loss_fn: Custom loss function
            task_weights: Task weights for multitask learning
            shuffle: Shuffle data each epoch (default: True)
            verbose: Print training progress (default: True)

        Returns:
            The trainer instance

        Example:
            >>> # Fine-tune on sentiment analysis data
            >>> model = GPT.load("models/pretrained.pt")
            >>> sentiment_texts = ["I love this!", "This is terrible", ...]
            >>> model.fine_tune(sentiment_texts, tokenizer, epochs=3)
            >>> model.save("models/sentiment_model.pt")
        """

        from composennent.training import train as training_fn


        trainer = training_fn(
            model=self,
            texts=texts,
            tokenizer=tokenizer,
            epochs=epochs,
            batch_size=batch_size,
            max_length=max_length,
            optimizer=optimizer,
            lr=lr,
            device=device,
            padding_strategy=padding_strategy,
            pad_token_id=pad_token_id,
            use_amp=use_amp,
            model_type=model_type,
            logits_key=logits_key,
            loss_fn=loss_fn,
            task_weights=task_weights,
            shuffle=shuffle,
            verbose=verbose,
        )

        return trainer

    def instruct(
        self,
        data,
        tokenizer,
        epochs: int = 3,
        batch_size: int = 8,
        max_length: int = 512,
        optimizer: Optional[torch.optim.Optimizer] = None,
        scheduler: Optional[Any] = None,
        lr: float = 5e-5,
        device: str = "cuda",
        use_amp: bool = True,
        grad_accum_steps: int = 1,
        max_grad_norm: float = 1.0,
        log_interval: int = 10,
        eval_interval: int = 100,
        val_data = None,
        save_path: Optional[str] = None,
        prompt_format: str = "chatml",
        mask_prompt: bool = True,
        verbose: bool = True,
    ):
        """Instruction tune the model to follow natural language commands.

        This teaches the model to follow diverse, natural language commands
        (e.g., "Summarize this text", "Translate to Spanish") using
        instruction-response pairs, making it more versatile and aligned
        with user intent.

        Different from fine_tune() which adapts to a specific task.

        Args:
            data: Instruction data. Can be:
                - List of dicts with "instruction", "input", "output" keys (Alpaca format)
                - List of dicts with "messages" key (ChatML format)
            tokenizer: Tokenizer instance
            epochs: Number of training epochs (default: 3)
            batch_size: Batch size (default: 8)
            max_length: Maximum sequence length (default: 512)
            optimizer: Optional custom optimizer. If None, uses AdamW with lr
            scheduler: Optional learning rate scheduler
            lr: Learning rate (default: 5e-5)
            device: Training device (default: "cuda")
            use_amp: Enable automatic mixed precision (default: True)
            grad_accum_steps: Gradient accumulation steps (default: 1)
            max_grad_norm: Max gradient norm for clipping (default: 1.0)
            log_interval: How often to log (default: 10)
            eval_interval: How often to evaluate (default: 100)
            val_data: Optional validation data
            save_path: Path to save checkpoints
            prompt_format: "chatml" or "alpaca" (default: "chatml")
            mask_prompt: Mask prompt tokens in loss (default: True)
            verbose: Print training progress (default: True)

        Returns:
            The trainer instance

        Example:
            >>> model = GPT.load("models/pretrained.pt")
            >>> instruction_data = [
            ...     {"instruction": "Summarize", "input": "Long text...", "output": "Short."},
            ...     {"instruction": "Translate to Spanish", "input": "Hello", "output": "Hola"},
            ... ]
            >>> model.instruct(instruction_data, tokenizer, epochs=3)
            >>> model.save("models/instructed.pt")
        """

        from composennent.instruct import (
            InstructTrainer,
            InstructionDataset,
            InstructionCollator,
            InstructionCollatorWithPromptMasking,
        )
        from torch.utils.data import DataLoader


        if not isinstance(data, InstructionDataset):
            dataset = InstructionDataset(data, tokenizer, max_length=max_length)
        else:
            dataset = data


        if mask_prompt:
            collator = InstructionCollatorWithPromptMasking(
                tokenizer=tokenizer,
                max_length=max_length,
                padding=True,
            )
        else:
            collator = InstructionCollator(
                tokenizer=tokenizer,
                max_length=max_length,
                padding=True,
            )


        train_dataloader = DataLoader(
            dataset,
            batch_size=batch_size,
            shuffle=True,
            collate_fn=collator,
        )


        val_dataloader = None
        if val_data is not None:
            if not isinstance(val_data, InstructionDataset):
                val_dataset = InstructionDataset(val_data, tokenizer, max_length=max_length)
            else:
                val_dataset = val_data

            val_dataloader = DataLoader(
                val_dataset,
                batch_size=batch_size,
                shuffle=False,
                collate_fn=collator,
            )


        if optimizer is None:
            optimizer = torch.optim.AdamW(self.parameters(), lr=lr)


        trainer = InstructTrainer(
            model=self,
            tokenizer=tokenizer,
            optimizer=optimizer,
            scheduler=scheduler,
            device=device,
            use_amp=use_amp,
            grad_accum_steps=grad_accum_steps,
            max_grad_norm=max_grad_norm,
        )


        trainer.train(
            train_dataloader=train_dataloader,
            val_dataloader=val_dataloader,
            epochs=epochs,
            log_interval=log_interval,
            eval_interval=eval_interval,
            save_path=save_path,
        )

        return trainer
