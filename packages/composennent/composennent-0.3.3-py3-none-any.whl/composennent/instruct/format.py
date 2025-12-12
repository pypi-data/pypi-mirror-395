from typing import Dict, Optional, List
from abc import ABC, abstractmethod

class BaseFormatter(ABC):
    """Base class for all instruction formatters."""
    
    @abstractmethod
    def format(self, instruction: str, input_text: Optional[str] = None, 
               output: Optional[str] = None, system: Optional[str] = None) -> str:
        """Format the instruction with optional components."""
        pass
    
    def construct_prompt(self, example: Dict[str, Optional[str]]) -> str:
        """Construct a prompt for training/inference."""
        return self.format(
            instruction=example.get("instruction", ""),
            input_text=example.get("input"),
            output=example.get("output"),  # For training
            system=example.get("system")
        )
    
    def parse_response(self, response: str) -> str:
        """Extract response after the prompt."""
        return response.strip()


class AlpacaFormatter(BaseFormatter):
    """Alpaca-style formatting."""
    
    def format(self, instruction: str, input_text: Optional[str] = None,
               output: Optional[str] = None, system: Optional[str] = None) -> str:
        prompt = f"### Instruction:\n{instruction}\n\n"
        if input_text:
            prompt += f"### Input:\n{input_text}\n\n"
        prompt += "### Response:\n"
        if output:
            prompt += output
        return prompt


class ChatMLFormatter(BaseFormatter):
    """ChatML-style formatting."""
    
    def format(self, instruction: str, input_text: Optional[str] = None,
               output: Optional[str] = None, system: Optional[str] = None) -> str:
        messages = []
        if system:
            messages.append(f"<|im_start|>system\n{system}<|im_end|>")
        
        user_msg = instruction
        if input_text:
            user_msg += f"\n\n{input_text}"
        messages.append(f"<|im_start|>user\n{user_msg}<|im_end|>")
        
        if output:
            messages.append(f"<|im_start|>assistant\n{output}<|im_end|>")
        else:
            messages.append("<|im_start|>assistant\n")
        
        return "\n".join(messages)


class LlamaFormatter(BaseFormatter):
    """Llama/Mistral [INST] style formatting."""
    
    def format(self, instruction: str, input_text: Optional[str] = None,
               output: Optional[str] = None, system: Optional[str] = None) -> str:
        content = instruction
        if input_text:
            content += f"\n\n{input_text}"
        
        if system:
            prompt = f"[INST] <<SYS>>\n{system}\n<</SYS>>\n\n{content} [/INST]"
        else:
            prompt = f"[INST] {content} [/INST]"
        
        if output:
            prompt += f" {output}"
        
        return prompt


class FormatterRegistry:
    """Registry for managing different formatters."""
    
    _formatters = {
        "alpaca": AlpacaFormatter,
        "chatml": ChatMLFormatter,
        "llama": LlamaFormatter,
    }
    
    @classmethod
    def get_formatter(cls, format_type: str) -> BaseFormatter:
        """Get formatter by type."""
        formatter_class = cls._formatters.get(format_type.lower())
        if not formatter_class:
            raise ValueError(f"Unknown format: {format_type}. Available: {list(cls._formatters.keys())}")
        return formatter_class()
    
    @classmethod
    def register(cls, name: str, formatter_class: type):
        """Register a custom formatter."""
        cls._formatters[name] = formatter_class



def process_dataset(examples: List[Dict], format_type: str = "chatml") -> List[str]:
    formatter = FormatterRegistry.get_formatter(format_type)
    return [formatter.construct_prompt(ex) for ex in examples]