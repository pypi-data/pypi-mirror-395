"""
Cost tracking for LLM API calls.

Tracks token usage and estimates costs for different models.
"""

from dataclasses import dataclass
from typing import Dict, Optional


# Model costs per 1K tokens (input/output)
MODEL_COSTS = {
    # OpenAI GPT-4o
    "gpt-4o": {"input": 0.0025, "output": 0.01, "input_cached": 0.00125},
    "gpt-4o-2024-11-20": {"input": 0.0025, "output": 0.01, "input_cached": 0.00125},
    "gpt-4o-2024-08-06": {"input": 0.0025, "output": 0.01, "input_cached": 0.00125},
    
    # OpenAI GPT-4o-mini
    "gpt-4o-mini": {"input": 0.00015, "output": 0.0006, "input_cached": 0.000075},
    "gpt-4o-mini-2024-07-18": {"input": 0.00015, "output": 0.0006, "input_cached": 0.000075},
    
    # OpenAI GPT-4 Turbo
    "gpt-4-turbo": {"input": 0.01, "output": 0.03},
    "gpt-4-turbo-2024-04-09": {"input": 0.01, "output": 0.03},
    
    # OpenAI GPT-4
    "gpt-4": {"input": 0.03, "output": 0.06},
    "gpt-4-0613": {"input": 0.03, "output": 0.06},
    
    # OpenAI GPT-3.5
    "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
    "gpt-3.5-turbo-0125": {"input": 0.0005, "output": 0.0015},
    
    # OpenAI o1 models
    "o1": {"input": 0.015, "output": 0.06, "input_cached": 0.0075},
    "o1-mini": {"input": 0.003, "output": 0.012, "input_cached": 0.0015},
    "o1-preview": {"input": 0.015, "output": 0.06, "input_cached": 0.0075},
    
    # Anthropic Claude 3.5
    "claude-3-5-sonnet-20241022": {"input": 0.003, "output": 0.015, "input_cached": 0.0015},
    "claude-3-5-sonnet-20240620": {"input": 0.003, "output": 0.015, "input_cached": 0.0015},
    
    # Anthropic Claude 3
    "claude-3-opus-20240229": {"input": 0.015, "output": 0.075},
    "claude-3-sonnet-20240229": {"input": 0.003, "output": 0.015},
    "claude-3-haiku-20240307": {"input": 0.00025, "output": 0.00125},
    
    # Ollama / Local models (free)
    "ollama": {"input": 0.0, "output": 0.0},
}


@dataclass
class TokenUsage:
    """Token usage statistics."""
    
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    prompt_tokens_cached: int = 0
    
    def __add__(self, other):
        """Add two token usage objects."""
        return TokenUsage(
            prompt_tokens=self.prompt_tokens + other.prompt_tokens,
            completion_tokens=self.completion_tokens + other.completion_tokens,
            total_tokens=self.total_tokens + other.total_tokens,
            prompt_tokens_cached=self.prompt_tokens_cached + other.prompt_tokens_cached,
        )


@dataclass
class CostEstimate:
    """Cost estimate for LLM usage."""
    
    input_cost: float = 0.0
    output_cost: float = 0.0
    total_cost: float = 0.0
    tokens: TokenUsage = None
    
    def __post_init__(self):
        if self.tokens is None:
            self.tokens = TokenUsage()


class CostTracker:
    """
    Track costs for LLM API calls.
    
    Maintains running totals and provides cost estimates.
    """
    
    def __init__(self):
        """Initialize cost tracker."""
        self.total_usage = TokenUsage()
        self.total_cost = 0.0
        self.model_usage: Dict[str, TokenUsage] = {}
        self.model_cost: Dict[str, float] = {}
    
    def estimate_cost(
        self,
        model: str,
        prompt_tokens: int,
        completion_tokens: int = 0,
        prompt_tokens_cached: int = 0,
    ) -> CostEstimate:
        """
        Estimate cost for token usage.
        
        Args:
            model: Model name
            prompt_tokens: Number of input tokens
            completion_tokens: Number of output tokens
            prompt_tokens_cached: Number of cached input tokens
        
        Returns:
            CostEstimate with breakdown
        """
        # Get model costs
        costs = MODEL_COSTS.get(model, {"input": 0.0, "output": 0.0})
        
        # Calculate uncached and cached prompt costs
        prompt_tokens_uncached = prompt_tokens - prompt_tokens_cached
        
        input_cost = (
            costs["input"] * prompt_tokens_uncached / 1000.0 +
            costs.get("input_cached", costs["input"]) * prompt_tokens_cached / 1000.0
        )
        output_cost = costs["output"] * completion_tokens / 1000.0
        total_cost = input_cost + output_cost
        
        usage = TokenUsage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
            prompt_tokens_cached=prompt_tokens_cached,
        )
        
        return CostEstimate(
            input_cost=input_cost,
            output_cost=output_cost,
            total_cost=total_cost,
            tokens=usage,
        )
    
    def record_usage(
        self,
        model: str,
        prompt_tokens: int,
        completion_tokens: int = 0,
        prompt_tokens_cached: int = 0,
    ) -> CostEstimate:
        """
        Record token usage and update totals.
        
        Args:
            model: Model name
            prompt_tokens: Number of input tokens
            completion_tokens: Number of output tokens
            prompt_tokens_cached: Number of cached input tokens
        
        Returns:
            CostEstimate for this usage
        """
        # Estimate cost
        estimate = self.estimate_cost(
            model, prompt_tokens, completion_tokens, prompt_tokens_cached
        )
        
        # Update totals
        self.total_usage += estimate.tokens
        self.total_cost += estimate.total_cost
        
        # Update model-specific totals
        if model not in self.model_usage:
            self.model_usage[model] = TokenUsage()
            self.model_cost[model] = 0.0
        
        self.model_usage[model] += estimate.tokens
        self.model_cost[model] += estimate.total_cost
        
        return estimate
    
    def get_stats(self) -> Dict:
        """
        Get cost statistics.
        
        Returns:
            Dictionary with statistics
        """
        return {
            "total_cost": self.total_cost,
            "total_tokens": self.total_usage.total_tokens,
            "total_prompt_tokens": self.total_usage.prompt_tokens,
            "total_completion_tokens": self.total_usage.completion_tokens,
            "total_cached_tokens": self.total_usage.prompt_tokens_cached,
            "models": {
                model: {
                    "tokens": usage.total_tokens,
                    "cost": self.model_cost[model],
                }
                for model, usage in self.model_usage.items()
            }
        }
    
    def reset(self):
        """Reset all statistics."""
        self.total_usage = TokenUsage()
        self.total_cost = 0.0
        self.model_usage = {}
        self.model_cost = {}


# Global cost tracker singleton
_global_tracker: Optional[CostTracker] = None


def get_cost_tracker() -> CostTracker:
    """
    Get global cost tracker.
    
    Returns:
        CostTracker instance
    """
    global _global_tracker
    
    if _global_tracker is None:
        _global_tracker = CostTracker()
    
    return _global_tracker
