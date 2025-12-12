"""
LLM Driver Interface (HAL - Hardware Abstraction Layer).

Implements ILLMDriver from SPECIFICATION.md Section 2.6
Provides uniform interface to multiple LLM providers (OpenAI, Anthropic, etc.)
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Protocol
from abc import ABC, abstractmethod
from enum import Enum
import time

from brainary.llm.providers import LLMProvider, OpenAIProvider, LLMMessage, LLMResponse
from brainary.llm.cost_tracker import TokenUsage
from brainary.core.errors import LLMProviderError, RateLimitError


class LLMCapability(Enum):
    """LLM capabilities."""
    TEXT_GENERATION = "text_generation"
    FUNCTION_CALLING = "function_calling"
    VISION = "vision"
    REASONING = "reasoning"  # o1-style reasoning
    STREAMING = "streaming"
    JSON_MODE = "json_mode"


@dataclass
class LLMRequest:
    """
    Standardized LLM request.
    
    Based on SPECIFICATION.md Section 2.6: ILLMDriver Interface
    """
    
    messages: List[LLMMessage]
    model: str = "gpt-4o-mini"
    temperature: float = 1.0
    max_tokens: int = 16384
    
    # Optional parameters
    stop_sequences: Optional[List[str]] = None
    top_p: Optional[float] = None
    frequency_penalty: Optional[float] = None
    presence_penalty: Optional[float] = None
    
    # Function calling
    functions: Optional[List[Dict[str, Any]]] = None
    function_call: Optional[str] = None  # "auto", "none", or specific function
    
    # Response format
    response_format: Optional[Dict[str, Any]] = None  # {"type": "json_object"}
    
    # Streaming
    stream: bool = False
    
    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_string(
        cls,
        prompt: str,
        model: str = "gpt-4o-mini",
        **kwargs
    ) -> "LLMRequest":
        """Create request from simple string prompt."""
        return cls(
            messages=[LLMMessage.user(prompt)],
            model=model,
            **kwargs
        )
    
    @classmethod
    def from_messages(
        cls,
        messages: List[LLMMessage],
        model: str = "gpt-4o-mini",
        **kwargs
    ) -> "LLMRequest":
        """Create request from message list."""
        return cls(
            messages=messages,
            model=model,
            **kwargs
        )


@dataclass
class LLMResponseMetadata:
    """Metadata about LLM response."""
    
    model: str
    provider: str
    latency_ms: float
    
    # Token usage
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    reasoning_tokens: int = 0  # For o1-style models
    
    # Cost
    cost_usd: float = 0.0
    
    # Status
    finish_reason: Optional[str] = None
    cached: bool = False  # Whether response was cached


@dataclass
class LLMResponseData:
    """
    Standardized LLM response.
    
    Based on SPECIFICATION.md Section 2.6: ILLMDriver Interface
    """
    
    content: str
    metadata: LLMResponseMetadata
    
    # Optional fields
    reasoning: Optional[str] = None  # For models with explicit reasoning
    function_call: Optional[Dict[str, Any]] = None
    
    # Raw response for debugging
    raw_response: Optional[Any] = None


class ILLMDriver(ABC):
    """
    Interface for LLM driver (Hardware Abstraction Layer).
    
    Based on SPECIFICATION.md Section 2.6: ILLMDriver Interface
    
    The LLM Driver provides:
    1. Uniform interface across providers
    2. Rate limiting and retry logic
    3. Cost tracking
    4. Error handling
    5. Request/response normalization
    """
    
    @abstractmethod
    def invoke(self, request: LLMRequest) -> LLMResponseData:
        """
        Invoke LLM with request.
        
        Args:
            request: Standardized LLM request
        
        Returns:
            Standardized LLM response
        
        Raises:
            LLMProviderError: On provider errors
            RateLimitError: On rate limit errors
            ValidationError: On invalid requests
        """
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[LLMCapability]:
        """
        Get capabilities supported by this driver.
        
        Returns:
            List of supported capabilities
        """
        pass
    
    @abstractmethod
    def estimate_cost(self, request: LLMRequest) -> float:
        """
        Estimate cost for request in USD.
        
        Args:
            request: LLM request to estimate
        
        Returns:
            Estimated cost in USD
        """
        pass
    
    @abstractmethod
    def health_check(self) -> bool:
        """
        Check if provider is available.
        
        Returns:
            True if healthy, False otherwise
        """
        pass


class OpenAIDriver(ILLMDriver):
    """
    OpenAI driver implementation.
    
    Supports GPT-4, GPT-4o, GPT-3.5, o1, and other OpenAI models.
    """
    
    def __init__(
        self,
        model: str = "gpt-4o-mini",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        max_retries: int = 3,
        timeout: float = 60.0,
    ):
        """
        Initialize OpenAI driver.
        
        Args:
            model: Model name
            api_key: Optional API key
            base_url: Optional base URL
            max_retries: Maximum retry attempts
            timeout: Request timeout in seconds
        """
        self.model = model
        self.max_retries = max_retries
        self.timeout = timeout
        
        # Create underlying provider
        self._provider = OpenAIProvider(
            model=model,
            api_key=api_key,
            base_url=base_url,
        )
        
        # Detect capabilities based on model
        self._capabilities = self._detect_capabilities(model)
    
    def invoke(self, request: LLMRequest) -> LLMResponseData:
        """
        Invoke OpenAI model with request.
        
        Implements retry logic and error handling.
        
        Args:
            request: LLM request
        
        Returns:
            LLM response
        
        Raises:
            LLMProviderError: On provider errors
            RateLimitError: On rate limit errors
        """
        start_time = time.time()
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                # Update provider settings from request
                self._provider.model = request.model or self.model
                self._provider.temperature = request.temperature
                self._provider.max_tokens = request.max_tokens
                
                # Build kwargs
                kwargs = {}
                if request.stop_sequences:
                    kwargs['stop'] = request.stop_sequences
                if request.top_p is not None:
                    kwargs['top_p'] = request.top_p
                if request.frequency_penalty is not None:
                    kwargs['frequency_penalty'] = request.frequency_penalty
                if request.presence_penalty is not None:
                    kwargs['presence_penalty'] = request.presence_penalty
                if request.response_format:
                    kwargs['response_format'] = request.response_format
                if request.functions:
                    kwargs['functions'] = request.functions
                    kwargs['function_call'] = request.function_call or "auto"
                if request.stream:
                    kwargs['stream'] = True
                
                # Make request
                response = self._provider.request(
                    messages=request.messages,
                    **kwargs
                )
                
                # Build metadata
                latency_ms = (time.time() - start_time) * 1000
                metadata = LLMResponseMetadata(
                    model=response.model,
                    provider="openai",
                    latency_ms=latency_ms,
                    prompt_tokens=response.usage.prompt_tokens,
                    completion_tokens=response.usage.completion_tokens,
                    total_tokens=response.usage.total_tokens,
                    reasoning_tokens=getattr(response.usage, 'reasoning_tokens', 0),
                    cost_usd=response.usage.cost,
                    finish_reason=response.finish_reason,
                    cached=False,
                )
                
                return LLMResponseData(
                    content=response.content,
                    metadata=metadata,
                    reasoning=response.reasoning,
                    raw_response=response.raw_response,
                )
                
            except Exception as e:
                last_error = e
                
                # Check if it's a rate limit error
                error_str = str(e).lower()
                if 'rate limit' in error_str or 'rate_limit' in error_str:
                    if attempt < self.max_retries - 1:
                        wait_time = 2 ** attempt  # Exponential backoff
                        time.sleep(wait_time)
                        continue
                    else:
                        raise RateLimitError(
                            message=f"Rate limit exceeded after {self.max_retries} retries",
                            provider="openai",
                            retry_after=None,
                        ) from e
                
                # Other errors
                if attempt < self.max_retries - 1:
                    time.sleep(1)  # Brief wait before retry
                    continue
                else:
                    raise LLMProviderError(
                        message=f"OpenAI request failed: {str(e)}",
                        provider="openai",
                        model=request.model,
                        error_type=type(e).__name__,
                    ) from e
        
        # Should not reach here, but just in case
        raise LLMProviderError(
            message=f"OpenAI request failed after {self.max_retries} retries: {last_error}",
            provider="openai",
            model=request.model,
            error_type=type(last_error).__name__ if last_error else "Unknown",
        )
    
    def get_capabilities(self) -> List[LLMCapability]:
        """Get capabilities for current model."""
        return self._capabilities
    
    def estimate_cost(self, request: LLMRequest) -> float:
        """
        Estimate cost for request.
        
        Uses approximate token counts and known pricing.
        
        Args:
            request: Request to estimate
        
        Returns:
            Estimated cost in USD
        """
        # Simple estimation: ~4 chars per token
        prompt_chars = sum(len(msg.content) for msg in request.messages)
        estimated_prompt_tokens = prompt_chars // 4
        estimated_completion_tokens = request.max_tokens // 2  # Assume 50% usage
        
        # Get pricing for model (approximate)
        pricing = self._get_model_pricing(request.model or self.model)
        
        cost = (
            estimated_prompt_tokens * pricing['input'] / 1_000_000 +
            estimated_completion_tokens * pricing['output'] / 1_000_000
        )
        
        return cost
    
    def health_check(self) -> bool:
        """
        Check if OpenAI API is available.
        
        Returns:
            True if healthy, False otherwise
        """
        try:
            # Simple test request
            test_request = LLMRequest.from_string(
                "test",
                model=self.model,
                max_tokens=1,
            )
            self.invoke(test_request)
            return True
        except Exception:
            return False
    
    def _detect_capabilities(self, model: str) -> List[LLMCapability]:
        """Detect capabilities based on model name."""
        capabilities = [LLMCapability.TEXT_GENERATION]
        
        if 'gpt-4' in model or 'gpt-3.5' in model:
            capabilities.extend([
                LLMCapability.FUNCTION_CALLING,
                LLMCapability.STREAMING,
                LLMCapability.JSON_MODE,
            ])
        
        if 'vision' in model or 'gpt-4o' in model:
            capabilities.append(LLMCapability.VISION)
        
        if 'o1' in model or 'o3' in model:
            capabilities.append(LLMCapability.REASONING)
        
        return capabilities
    
    def _get_model_pricing(self, model: str) -> Dict[str, float]:
        """
        Get pricing for model (per million tokens).
        
        Returns:
            Dict with 'input' and 'output' costs
        """
        # Approximate pricing (as of 2024)
        pricing_map = {
            'gpt-4o': {'input': 2.50, 'output': 10.00},
            'gpt-4o-mini': {'input': 0.15, 'output': 0.60},
            'gpt-4-turbo': {'input': 10.00, 'output': 30.00},
            'gpt-4': {'input': 30.00, 'output': 60.00},
            'gpt-3.5-turbo': {'input': 0.50, 'output': 1.50},
            'o1-preview': {'input': 15.00, 'output': 60.00},
            'o1-mini': {'input': 3.00, 'output': 12.00},
        }
        
        # Match model name to pricing
        for key, price in pricing_map.items():
            if key in model:
                return price
        
        # Default fallback
        return {'input': 5.00, 'output': 15.00}


class AnthropicDriver(ILLMDriver):
    """
    Anthropic driver implementation.
    
    Supports Claude models (Opus, Sonnet, Haiku).
    """
    
    def __init__(
        self,
        model: str = "claude-3-5-sonnet-20241022",
        api_key: Optional[str] = None,
        max_retries: int = 3,
        timeout: float = 60.0,
    ):
        """
        Initialize Anthropic driver.
        
        Args:
            model: Model name
            api_key: Optional API key
            max_retries: Maximum retry attempts
            timeout: Request timeout in seconds
        """
        self.model = model
        self.max_retries = max_retries
        self.timeout = timeout
        
        # Import Anthropic provider if available
        try:
            from brainary.llm.providers import AnthropicProvider
            self._provider = AnthropicProvider(
                model=model,
                api_key=api_key,
            )
        except ImportError:
            raise ImportError("Anthropic provider not available")
        
        self._capabilities = [
            LLMCapability.TEXT_GENERATION,
            LLMCapability.VISION,  # Claude 3+ supports vision
            LLMCapability.STREAMING,
        ]
    
    def invoke(self, request: LLMRequest) -> LLMResponseData:
        """
        Invoke Anthropic model with request.
        
        Similar implementation to OpenAI driver with Anthropic-specific handling.
        """
        # Similar implementation pattern as OpenAI
        # Left as exercise - can be implemented when needed
        raise NotImplementedError("Anthropic driver invoke() not yet implemented")
    
    def get_capabilities(self) -> List[LLMCapability]:
        """Get capabilities."""
        return self._capabilities
    
    def estimate_cost(self, request: LLMRequest) -> float:
        """Estimate cost."""
        # Claude pricing
        pricing_map = {
            'claude-3-opus': {'input': 15.00, 'output': 75.00},
            'claude-3-5-sonnet': {'input': 3.00, 'output': 15.00},
            'claude-3-haiku': {'input': 0.25, 'output': 1.25},
        }
        
        # Find matching pricing
        pricing = {'input': 3.00, 'output': 15.00}  # Default to Sonnet
        for key, price in pricing_map.items():
            if key in self.model:
                pricing = price
                break
        
        # Estimate tokens
        prompt_chars = sum(len(msg.content) for msg in request.messages)
        estimated_prompt_tokens = prompt_chars // 4
        estimated_completion_tokens = request.max_tokens // 2
        
        cost = (
            estimated_prompt_tokens * pricing['input'] / 1_000_000 +
            estimated_completion_tokens * pricing['output'] / 1_000_000
        )
        
        return cost
    
    def health_check(self) -> bool:
        """Check health."""
        try:
            test_request = LLMRequest.from_string("test", model=self.model, max_tokens=1)
            self.invoke(test_request)
            return True
        except Exception:
            return False


def create_driver(
    provider: str = "openai",
    model: Optional[str] = None,
    **kwargs
) -> ILLMDriver:
    """
    Factory function to create LLM driver.
    
    Args:
        provider: Provider name ("openai", "anthropic")
        model: Optional model name (uses provider default if not specified)
        **kwargs: Additional driver parameters
    
    Returns:
        ILLMDriver implementation
    
    Raises:
        ValueError: If provider not supported
    """
    if provider.lower() == "openai":
        return OpenAIDriver(model=model or "gpt-4o-mini", **kwargs)
    elif provider.lower() == "anthropic":
        return AnthropicDriver(model=model or "claude-3-5-sonnet-20241022", **kwargs)
    else:
        raise ValueError(f"Unsupported provider: {provider}")
