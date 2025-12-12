"""
Cost Tracking

Real-time token counting and cost estimation for LLM API calls.
Supports OpenAI, Anthropic, and OpenRouter pricing.

Example:
    >>> tracker = CostTracker()
    >>> estimate = tracker.estimate("Hello world", "gpt-4o-mini")
    >>> print(f"Estimated cost: ${estimate.total:.4f}")
"""

from dataclasses import dataclass
from typing import Optional
import re


# Model pricing per 1K tokens (as of Dec 2024)
MODEL_PRICING: dict[str, dict[str, float]] = {
    # OpenAI
    "gpt-4o": {"input": 0.0025, "output": 0.01},
    "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
    "gpt-4-turbo": {"input": 0.01, "output": 0.03},
    "gpt-4-turbo-preview": {"input": 0.01, "output": 0.03},
    "gpt-4": {"input": 0.03, "output": 0.06},
    "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
    "o1-preview": {"input": 0.015, "output": 0.06},
    "o1-mini": {"input": 0.003, "output": 0.012},
    
    # Anthropic
    "claude-3-5-sonnet-latest": {"input": 0.003, "output": 0.015},
    "claude-3-5-sonnet-20241022": {"input": 0.003, "output": 0.015},
    "claude-3-5-haiku-latest": {"input": 0.001, "output": 0.005},
    "claude-3-opus-latest": {"input": 0.015, "output": 0.075},
    "claude-3-sonnet-20240229": {"input": 0.003, "output": 0.015},
    "claude-3-haiku-20240307": {"input": 0.00025, "output": 0.00125},
    
    # Google (via OpenRouter)
    "google/gemini-pro-1.5": {"input": 0.00125, "output": 0.005},
    "google/gemini-flash-1.5": {"input": 0.000075, "output": 0.0003},
    
    # Meta (via OpenRouter)
    "meta-llama/llama-3.1-70b-instruct": {"input": 0.00052, "output": 0.00075},
    "meta-llama/llama-3.1-405b-instruct": {"input": 0.003, "output": 0.003},
    "meta-llama/llama-3.1-8b-instruct": {"input": 0.00006, "output": 0.00006},
    
    # Mistral (via OpenRouter)
    "mistralai/mistral-large-latest": {"input": 0.002, "output": 0.006},
    "mistralai/mistral-small-latest": {"input": 0.0001, "output": 0.0003},
    "mistralai/mixtral-8x7b-instruct": {"input": 0.00024, "output": 0.00024},
    
    # DeepSeek
    "deepseek/deepseek-chat": {"input": 0.00014, "output": 0.00028},
    "deepseek/deepseek-coder": {"input": 0.00014, "output": 0.00028},
    
    # Qwen
    "qwen/qwen-2.5-72b-instruct": {"input": 0.00035, "output": 0.0004},
}

# Aliases for common model names
MODEL_ALIASES: dict[str, str] = {
    "claude-3-5-sonnet": "claude-3-5-sonnet-latest",
    "claude-3-5-haiku": "claude-3-5-haiku-latest",
    "claude-3-opus": "claude-3-opus-latest",
    "gemini-pro": "google/gemini-pro-1.5",
    "gemini-flash": "google/gemini-flash-1.5",
    "llama-3.1-70b": "meta-llama/llama-3.1-70b-instruct",
    "llama-3.1-405b": "meta-llama/llama-3.1-405b-instruct",
    "mistral-large": "mistralai/mistral-large-latest",
    "mistral-small": "mistralai/mistral-small-latest",
}


@dataclass
class CostEstimate:
    """
    Cost estimate for a prompt.
    
    Attributes:
        model: Model name.
        input_tokens: Estimated input tokens.
        output_tokens: Estimated output tokens.
        input_cost: Cost for input tokens.
        output_cost: Cost for output tokens.
        total: Total estimated cost.
    """
    
    model: str
    input_tokens: int
    output_tokens: int
    input_cost: float
    output_cost: float
    total: float


class CostTracker:
    """
    Track and estimate costs for LLM API calls.
    
    Provides:
    - Token counting (approximate)
    - Cost estimation before calls
    - Cost tracking after calls
    - Budget management
    
    Example:
        >>> tracker = CostTracker()
        >>> 
        >>> # Estimate before calling
        >>> est = tracker.estimate("What is 2+2?", "gpt-4o-mini")
        >>> print(f"Estimated: ${est.total:.4f}")
        >>> 
        >>> # Track actual usage
        >>> tracker.track_usage("gpt-4o-mini", input_tokens=10, output_tokens=50)
        >>> print(f"Session total: ${tracker.session_cost:.4f}")
    """
    
    def __init__(
        self,
        daily_budget: Optional[float] = None,
        session_budget: Optional[float] = None,
    ) -> None:
        """
        Initialize cost tracker.
        
        Args:
            daily_budget: Optional daily spending limit.
            session_budget: Optional session spending limit.
        """
        self.daily_budget = daily_budget
        self.session_budget = session_budget
        self.session_cost = 0.0
        self.session_tokens = 0
        self._usage_log: list[dict] = []
    
    def count_tokens(self, text: str) -> int:
        """
        Estimate token count for text.
        
        Uses simple heuristic (~4 chars per token for English).
        For exact counts, use tiktoken or model-specific tokenizers.
        
        Args:
            text: Text to count tokens for.
            
        Returns:
            Estimated token count.
        """
        # Simple heuristic: ~4 characters per token for English
        # This is approximate - use tiktoken for exact counts
        return max(1, len(text) // 4)
    
    def get_pricing(self, model: str) -> dict[str, float]:
        """
        Get pricing for a model.
        
        Args:
            model: Model name or alias.
            
        Returns:
            Dict with 'input' and 'output' prices per 1K tokens.
        """
        # Check aliases
        resolved = MODEL_ALIASES.get(model, model)
        
        # Get pricing or default
        if resolved in MODEL_PRICING:
            return MODEL_PRICING[resolved]
        
        # Default pricing if unknown
        return {"input": 0.001, "output": 0.002}
    
    def estimate(
        self,
        prompt: str,
        model: str,
        expected_output_tokens: Optional[int] = None,
        system_prompt: Optional[str] = None,
    ) -> CostEstimate:
        """
        Estimate cost for a prompt before calling the API.
        
        Args:
            prompt: User prompt text.
            model: Model to use.
            expected_output_tokens: Expected output length (default: 500).
            system_prompt: Optional system prompt.
            
        Returns:
            CostEstimate with breakdown.
            
        Example:
            >>> tracker = CostTracker()
            >>> est = tracker.estimate(
            ...     "Write a poem about AI",
            ...     "gpt-4o-mini",
            ...     expected_output_tokens=200
            ... )
            >>> print(f"Input: {est.input_tokens}, Output: ~{est.output_tokens}")
        """
        # Count input tokens
        input_text = prompt
        if system_prompt:
            input_text = system_prompt + "\n" + prompt
        
        input_tokens = self.count_tokens(input_text)
        output_tokens = expected_output_tokens or 500
        
        # Get pricing
        pricing = self.get_pricing(model)
        
        input_cost = (input_tokens / 1000) * pricing["input"]
        output_cost = (output_tokens / 1000) * pricing["output"]
        
        return CostEstimate(
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            input_cost=input_cost,
            output_cost=output_cost,
            total=input_cost + output_cost,
        )
    
    def calculate_cost(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int,
    ) -> float:
        """
        Calculate exact cost from token counts.
        
        Args:
            model: Model name.
            input_tokens: Actual input tokens.
            output_tokens: Actual output tokens.
            
        Returns:
            Total cost in dollars.
        """
        pricing = self.get_pricing(model)
        
        input_cost = (input_tokens / 1000) * pricing["input"]
        output_cost = (output_tokens / 1000) * pricing["output"]
        
        return input_cost + output_cost
    
    def track_usage(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int,
    ) -> float:
        """
        Track actual API usage.
        
        Updates session totals and returns the cost.
        
        Args:
            model: Model used.
            input_tokens: Actual input tokens.
            output_tokens: Actual output tokens.
            
        Returns:
            Cost for this call.
        """
        cost = self.calculate_cost(model, input_tokens, output_tokens)
        
        self.session_cost += cost
        self.session_tokens += input_tokens + output_tokens
        
        self._usage_log.append({
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost": cost,
        })
        
        return cost
    
    def check_budget(self, estimated_cost: float) -> bool:
        """
        Check if estimated cost is within budget.
        
        Args:
            estimated_cost: Cost to check.
            
        Returns:
            True if within budget, False otherwise.
        """
        if self.session_budget is not None:
            if self.session_cost + estimated_cost > self.session_budget:
                return False
        
        return True
    
    def get_summary(self) -> dict:
        """
        Get session cost summary.
        
        Returns:
            Dict with session statistics.
        """
        return {
            "total_cost": self.session_cost,
            "total_tokens": self.session_tokens,
            "num_calls": len(self._usage_log),
            "budget_remaining": (
                self.session_budget - self.session_cost
                if self.session_budget else None
            ),
        }
    
    def reset_session(self) -> None:
        """Reset session tracking."""
        self.session_cost = 0.0
        self.session_tokens = 0
        self._usage_log = []

