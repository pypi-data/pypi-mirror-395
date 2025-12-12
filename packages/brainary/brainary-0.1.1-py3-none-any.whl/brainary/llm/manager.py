"""
LLM manager for Brainary.

Provides a high-level interface for LLM operations with automatic
provider selection and cost tracking.
"""

import logging
from typing import Optional, Union, List, Dict, Any

from brainary.llm.providers import (
    LLMProvider,
    OpenAIProvider,
    AnthropicProvider,
    OllamaProvider,
    LLMMessage,
    LLMResponse,
    create_provider,
)
from brainary.llm.cost_tracker import get_cost_tracker


logger = logging.getLogger(__name__)


class LLMManager:
    """
    High-level LLM manager.
    
    Manages multiple providers and provides a unified interface.
    """
    
    def __init__(
        self,
        default_provider: str = "openai",
        default_model: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize LLM manager.
        
        Args:
            default_provider: Default provider to use
            default_model: Default model for the provider
            **kwargs: Additional provider parameters
        """
        self.default_provider = default_provider
        self.default_model = default_model
        self.provider_kwargs = kwargs
        self.cost_tracker = get_cost_tracker()
        
        # Cache for provider instances
        self._providers: Dict[str, LLMProvider] = {}
    
    def get_provider(
        self,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        **kwargs
    ) -> LLMProvider:
        """
        Get or create provider instance.
        
        Args:
            provider: Provider name (uses default if None)
            model: Model name (uses default if None)
            **kwargs: Additional parameters
        
        Returns:
            LLMProvider instance
        """
        provider = provider or self.default_provider
        model = model or self.default_model
        
        # Create cache key
        cache_key = f"{provider}:{model}"
        
        # Return cached instance if available
        if cache_key in self._providers:
            return self._providers[cache_key]
        
        # Create new provider
        merged_kwargs = {**self.provider_kwargs, **kwargs}
        provider_instance = create_provider(provider, model, **merged_kwargs)
        
        # Cache and return
        self._providers[cache_key] = provider_instance
        return provider_instance
    
    def request(
        self,
        messages: Union[str, List[LLMMessage], List[Dict]],
        provider: Optional[str] = None,
        model: Optional[str] = None,
        **kwargs
    ) -> LLMResponse:
        """
        Send request to LLM.
        
        Args:
            messages: Messages to send
            provider: Optional provider override
            model: Optional model override
            **kwargs: Additional parameters
        
        Returns:
            LLMResponse
        """
        # Get provider
        llm_provider = self.get_provider(provider, model, **kwargs)
        
        # Log request at manager level
        provider_name = provider or self.default_provider
        model_name = model or self.default_model or llm_provider.model
        logger.debug(f"LLMManager routing request to {provider_name}/{model_name}")
        
        # Make request
        response = llm_provider.request(messages, **kwargs)
        
        # Log completion at manager level
        stats = self.cost_tracker.get_stats()
        logger.debug(f"LLMManager received response: {response.usage.total_tokens} tokens, cumulative cost: ${stats['total_cost']:.6f}")
        
        return response
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get usage statistics.
        
        Returns:
            Dictionary with cost and usage statistics
        """
        return self.cost_tracker.get_stats()
    
    def reset_stats(self):
        """Reset cost tracking statistics."""
        self.cost_tracker.reset()


# Global LLM manager singleton
_global_manager: Optional[LLMManager] = None


def get_llm_manager(
    default_provider: str = "openai",
    default_model: Optional[str] = None,
    **kwargs
) -> LLMManager:
    """
    Get global LLM manager.
    
    Args:
        default_provider: Default provider
        default_model: Default model
        **kwargs: Additional parameters
    
    Returns:
        LLMManager instance
    """
    global _global_manager
    
    if _global_manager is None:
        _global_manager = LLMManager(default_provider, default_model, **kwargs)
    
    return _global_manager


def set_llm_manager(manager: LLMManager):
    """
    Set global LLM manager.
    
    Args:
        manager: LLMManager instance
    """
    global _global_manager
    _global_manager = manager
