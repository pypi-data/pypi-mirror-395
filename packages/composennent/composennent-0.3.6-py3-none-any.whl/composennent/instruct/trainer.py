"""Trainer for instruction tuning."""

import torch
import torch.nn as nn
from typing import Optional, Callable, Dict, Any, Union
from torch.utils.data import DataLoader
from tqdm.auto import tqdm
import time


class InstructTrainer:
    """Trainer optimized for instruction tuning/fine-tuning.

    This trainer handles the training loop for instruction tuning,
    including gradient accumulation, mixed precision (AMP), and logging.

    It is designed to be flexible: you can override the `train_step` method
    or pass a custom training function.

    Args:
        model: The language model to train (must return logits)
        tokenizer: Tokenizer for decoding/logging
        optimizer: Optimizer instance
        scheduler: Learning rate scheduler (optional)
        device: Device to train on ("cuda", "cpu", "mps")
        use_amp: Whether to use Automatic Mixed Precision (default: True)
        grad_accum_steps: Gradient accumulation steps (default: 1)
        max_grad_norm: Max gradient norm for clipping (default: 1.0)

    Example:
        >>> trainer = InstructTrainer(model, tokenizer, optimizer, device="cuda")
        >>> trainer.train(dataloader, epochs=3)

    Custom Training Step:
        You can customize the training logic by overriding `train_step`
        or assigning a new function to it:

        >>> def my_train_step(batch):
        ...     # Custom logic
        ...     loss = model(batch['input_ids'], labels=batch['labels'])
        ...     return loss
        >>>
        >>> trainer.train_step = my_train_step
        >>> trainer.train(dataloader)
    """

    def __init__(
        self,
        model: nn.Module,
        tokenizer: Any,
        optimizer: torch.optim.Optimizer,
        scheduler: Optional[Any] = None,
        device: str = "cuda",
        use_amp: bool = True,
        grad_accum_steps: int = 1,
        max_grad_norm: float = 1.0,
    ):
        self.model = model
        self.tokenizer = tokenizer
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.device = device
        self.use_amp = use_amp
        self.grad_accum_steps = grad_accum_steps
        self.max_grad_norm = max_grad_norm


        self.scaler = torch.cuda.amp.GradScaler(enabled=use_amp)


        self.model.to(self.device)


        self.global_step = 0

    def train_step(self, batch: Dict[str, torch.Tensor]) -> torch.Tensor:
        """Single training step. Can be overridden by user.

        Args:
            batch: Dictionary containing input_ids, attention_mask, labels

        Returns:
            loss: scalar tensor
        """

        input_ids = batch["input_ids"].to(self.device)
        attention_mask = batch["attention_mask"].to(self.device)
        labels = batch["labels"].to(self.device)






        outputs = self.model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=labels
        )


        if isinstance(outputs, dict):
            loss = outputs.get("loss")
            logits = outputs.get("logits")
        elif isinstance(outputs, (tuple, list)):
            loss = outputs[0]
            logits = outputs[1] if len(outputs) > 1 else None
        else:

            logits = outputs
            loss = None

        if loss is None:


            shift_logits = logits[..., :-1, :].contiguous()
            shift_labels = labels[..., 1:].contiguous()

            loss_fct = nn.CrossEntropyLoss()
            loss = loss_fct(
                shift_logits.view(-1, shift_logits.size(-1)),
                shift_labels.view(-1)
            )

        return loss

    def train(
        self,
        train_dataloader: DataLoader,
        val_dataloader: Optional[DataLoader] = None,
        epochs: int = 3,
        log_interval: int = 10,
        eval_interval: int = 100,
        save_path: Optional[str] = None,
    ):
        """Main training loop.

        Args:
            train_dataloader: DataLoader for training data
            val_dataloader: Optional DataLoader for validation
            epochs: Number of epochs
            log_interval: How often to log training stats (steps)
            eval_interval: How often to evaluate (steps)
            save_path: Path to save best model
        """
        self.model.train()
        total_steps = len(train_dataloader) * epochs

        print(f"Starting training for {epochs} epochs ({total_steps} steps)...")
        start_time = time.time()

        for epoch in range(epochs):
            pbar = tqdm(train_dataloader, desc=f"Epoch {epoch+1}/{epochs}")
            epoch_loss = 0.0

            for step, batch in enumerate(pbar):

                with torch.cuda.amp.autocast(enabled=self.use_amp):
                    loss = self.train_step(batch)


                    loss = loss / self.grad_accum_steps


                self.scaler.scale(loss).backward()


                if (step + 1) % self.grad_accum_steps == 0:

                    self.scaler.unscale_(self.optimizer)
                    torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.max_grad_norm)


                    self.scaler.step(self.optimizer)
                    self.scaler.update()
                    self.optimizer.zero_grad()


                    if self.scheduler:
                        self.scheduler.step()

                    self.global_step += 1


                current_loss = loss.item() * self.grad_accum_steps
                epoch_loss += current_loss

                if step % log_interval == 0:
                    lr = self.scheduler.get_last_lr()[0] if self.scheduler else self.optimizer.param_groups[0]['lr']
                    pbar.set_postfix({
                        "loss": f"{current_loss:.4f}",
                        "lr": f"{lr:.2e}",
                        "step": self.global_step
                    })


                if val_dataloader and self.global_step % eval_interval == 0 and (step + 1) % self.grad_accum_steps == 0:
                    val_loss = self.evaluate(val_dataloader)
                    print(f"\nStep {self.global_step} - Val Loss: {val_loss:.4f}")


                    if save_path:
                        self.model.save(save_path)

                    self.model.train()

            avg_epoch_loss = epoch_loss / len(train_dataloader)
            print(f"Epoch {epoch+1} finished - Avg Loss: {avg_epoch_loss:.4f}")

            if save_path:

                if hasattr(self.model, "save"):
                    self.model.save(f"{save_path}_ep{epoch+1}.pt")
                else:
                    torch.save(self.model.state_dict(), f"{save_path}_ep{epoch+1}.pt")

        total_time = time.time() - start_time
        print(f"Training finished in {total_time/60:.2f} minutes.")

    @torch.no_grad()
    def evaluate(self, dataloader: DataLoader) -> float:
        """Run evaluation loop."""
        self.model.eval()
        total_loss = 0.0

        for batch in tqdm(dataloader, desc="Evaluating", leave=False):






            input_ids = batch["input_ids"].to(self.device)
            attention_mask = batch["attention_mask"].to(self.device)
            labels = batch["labels"].to(self.device)

            outputs = self.model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                labels=labels
            )

            if isinstance(outputs, dict):
                loss = outputs.get("loss")
            elif isinstance(outputs, (tuple, list)):
                loss = outputs[0]
            else:

                logits = outputs
                shift_logits = logits[..., :-1, :].contiguous()
                shift_labels = labels[..., 1:].contiguous()
                loss_fct = nn.CrossEntropyLoss()
                loss = loss_fct(shift_logits.view(-1, shift_logits.size(-1)), shift_labels.view(-1))

            total_loss += loss.item()

        return total_loss / len(dataloader)
