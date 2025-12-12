"""
LLM integration module.

Provides unified interface for OpenAI, Anthropic, and local models.
Implements ILLMDriver interface from SPECIFICATION.md for hardware abstraction.
"""

from brainary.llm.providers import (
    LLMProvider,
    OpenAIProvider,
    AnthropicProvider,
    OllamaProvider,
    LLMMessage,
    LLMResponse,
    create_provider,
)
from brainary.llm.driver import (
    ILLMDriver,
    OpenAIDriver,
    AnthropicDriver,
    LLMRequest,
    LLMResponseData,
    LLMResponseMetadata,
    LLMCapability,
    create_driver,
)
from brainary.llm.manager import (
    LLMManager,
    get_llm_manager,
    set_llm_manager,
)
from brainary.llm.cost_tracker import (
    CostTracker,
    CostEstimate,
    TokenUsage,
    get_cost_tracker,
)
from brainary.llm.config import (
    load_llm_config,
    get_openai_config,
    get_anthropic_config,
    get_ollama_config,
)

__all__ = [
    # Providers (legacy)
    "LLMProvider",
    "OpenAIProvider",
    "AnthropicProvider",
    "OllamaProvider",
    "create_provider",
    # Driver interface (HAL)
    "ILLMDriver",
    "OpenAIDriver",
    "AnthropicDriver",
    "create_driver",
    # Request/Response
    "LLMRequest",
    "LLMResponseData",
    "LLMResponseMetadata",
    "LLMCapability",
    # Messages and responses (legacy)
    "LLMMessage",
    "LLMResponse",
    # Manager
    "LLMManager",
    "get_llm_manager",
    "set_llm_manager",
    # Cost tracking
    "CostTracker",
    "CostEstimate",
    "TokenUsage",
    "get_cost_tracker",
    # Configuration
    "load_llm_config",
    "get_openai_config",
    "get_anthropic_config",
    "get_ollama_config",
]
