"""
LLM provider implementations.

Supports OpenAI, Anthropic, and local models (Ollama).
"""

import re
import logging
from typing import List, Optional, Union, Dict, Any
from abc import ABC, abstractmethod
from dataclasses import dataclass

from brainary.llm.config import get_openai_config, get_anthropic_config, get_ollama_config
from brainary.llm.cost_tracker import get_cost_tracker, TokenUsage


logger = logging.getLogger(__name__)


@dataclass
class LLMMessage:
    """Standardized message format."""
    
    role: str  # "system", "user", "assistant"
    content: str
    
    @classmethod
    def system(cls, content: str):
        """Create system message."""
        return cls(role="system", content=content)
    
    @classmethod
    def user(cls, content: str):
        """Create user message."""
        return cls(role="user", content=content)
    
    @classmethod
    def assistant(cls, content: str):
        """Create assistant message."""
        return cls(role="assistant", content=content)


@dataclass
class LLMResponse:
    """Standardized response format."""
    
    content: str
    model: str
    usage: TokenUsage
    reasoning: Optional[str] = None  # For models with reasoning tokens
    finish_reason: Optional[str] = None
    raw_response: Optional[Any] = None


class LLMProvider(ABC):
    """
    Abstract base class for LLM providers.
    
    All providers must implement the request method.
    """
    
    def __init__(self, model: str, temperature: float = 1.0, max_tokens: int = 16384):
        """
        Initialize provider.
        
        Args:
            model: Model name
            temperature: Sampling temperature
            max_tokens: Maximum completion tokens
        """
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.cost_tracker = get_cost_tracker()
    
    @abstractmethod
    def request(
        self,
        messages: Union[str, List[LLMMessage], List[Dict]],
        **kwargs
    ) -> LLMResponse:
        """
        Send request to LLM.
        
        Args:
            messages: Messages to send (can be string, list of LLMMessage, or list of dicts)
            **kwargs: Additional provider-specific parameters
        
        Returns:
            LLMResponse with model output
        """
        pass
    
    def _normalize_messages(
        self,
        messages: Union[str, List[LLMMessage], List[Dict]]
    ) -> List[LLMMessage]:
        """
        Normalize messages to standard format.
        
        Args:
            messages: Input messages in various formats
        
        Returns:
            List of LLMMessage objects
        """
        if isinstance(messages, str):
            return [LLMMessage.user(messages)]
        
        normalized = []
        for msg in messages:
            if isinstance(msg, LLMMessage):
                normalized.append(msg)
            elif isinstance(msg, dict):
                normalized.append(LLMMessage(role=msg["role"], content=msg["content"]))
            elif isinstance(msg, tuple):
                role, content = msg
                normalized.append(LLMMessage(role=role, content=content))
            else:
                normalized.append(LLMMessage.user(str(msg)))
        
        return normalized
    
    @staticmethod
    def _clean_response(response: str) -> str:
        """
        Clean response by removing code blocks and extra whitespace.
        
        Args:
            response: Raw response text
        
        Returns:
            Cleaned response
        """
        lines = response.strip().split("\n")
        if lines and lines[0].startswith("```") and lines[-1].startswith("```"):
            lines = lines[1:-1]
        return "\n".join(lines).strip()
    
    @staticmethod
    def _remove_thinking(response: str) -> str:
        """
        Remove thinking tags from response.
        
        Args:
            response: Response text possibly containing <think></think> tags
        
        Returns:
            Response without thinking tags
        """
        if "</think>" not in response:
            return response.strip()
        return response.split("</think>")[1].strip()
    
    @staticmethod
    def _escape_format_string(s: str) -> str:
        """
        Escape curly braces in format strings.
        
        Args:
            s: String to escape
        
        Returns:
            Escaped string
        """
        # Replace single { not followed by another {
        s = re.sub(r'(?<!{){(?!{)', '{{', s)
        # Replace single } not preceded by another }
        s = re.sub(r'(?<!})}(?!})', '}}', s)
        return s


class OpenAIProvider(LLMProvider):
    """
    OpenAI provider implementation.
    
    Supports GPT-4, GPT-4o, GPT-3.5, and other OpenAI models.
    """
    
    def __init__(
        self,
        model: str = "gpt-4o-mini",
        temperature: float = 1.0,
        max_tokens: int = 16384,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        """
        Initialize OpenAI provider.
        
        Args:
            model: Model name
            temperature: Sampling temperature
            max_tokens: Maximum completion tokens
            api_key: Optional API key (will load from config if not provided)
            base_url: Optional base URL (will load from config if not provided)
        """
        super().__init__(model, temperature, max_tokens)
        
        # Get configuration
        config_key, config_url = get_openai_config()
        self.api_key = api_key or config_key
        self.base_url = base_url or config_url
        
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set it in llm.yml or OPENAI_API_KEY environment variable.")
        
        # Import here to make it optional
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        except ImportError:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
    
    def request(
        self,
        messages: Union[str, List[LLMMessage], List[Dict]],
        **kwargs
    ) -> LLMResponse:
        """
        Send request to OpenAI API.
        
        Args:
            messages: Messages to send
            **kwargs: Additional parameters
        
        Returns:
            LLMResponse
        """
        # Normalize messages
        normalized = self._normalize_messages(messages)
        
        # Convert to OpenAI format
        openai_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in normalized
        ]
        
        # Log detailed request info
        logger.info(f"╔{'═' * 78}╗")
        logger.info(f"║ LLM REQUEST: {self.model:<63} ║")
        logger.info(f"╠{'═' * 78}╣")
        logger.info(f"║ Provider: OpenAI{' ' * 62}║")
        logger.info(f"║ Model: {self.model:<68}║")
        logger.info(f"║ Temperature: {self.temperature:<62}║")
        logger.info(f"║ Max Tokens: {self.max_tokens:<63}║")
        logger.info(f"║ Messages: {len(openai_messages):<65}║")
        logger.info(f"╠{'═' * 78}╣")
        
        # Log complete message contents
        for i, msg in enumerate(openai_messages):
            logger.info(f"║ Message [{i+1}] - {msg['role'].upper()}{' ' * (69 - len(msg['role']))}║")
            # Split content into lines that fit within the box
            content_lines = msg['content'].split('\n')
            for line in content_lines:
                # Wrap long lines
                while len(line) > 76:
                    logger.info(f"║ {line[:76]:<76} ║")
                    line = line[76:]
                if line:  # Log remaining content
                    logger.info(f"║ {line:<76} ║")
        
        logger.info(f"╚{'═' * 78}╝")
        
        # Make request
        try:
            # Merge instance defaults with kwargs (kwargs take precedence)
            request_params = {
                'model': self.model,
                'messages': openai_messages,
                'temperature': self.temperature,
                'max_tokens': self.max_tokens,
            }
            request_params.update(kwargs)
            
            response = self.client.chat.completions.create(**request_params)
            
            # Extract response
            choice = response.choices[0]
            content = choice.message.content or ""
            
            # Extract reasoning if present (for o1 models)
            reasoning = None
            if hasattr(choice.message, "reasoning_content"):
                reasoning = choice.message.reasoning_content
            
            # Create usage object
            usage = TokenUsage(
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens,
                prompt_tokens_cached=getattr(response.usage, "prompt_tokens_cached", 0),
            )
            
            # Record cost
            cost_estimate = self.cost_tracker.record_usage(
                self.model,
                usage.prompt_tokens,
                usage.completion_tokens,
                usage.prompt_tokens_cached,
            )
            
            # Log detailed response info
            logger.info(f"╔{'═' * 78}╗")
            logger.info(f"║ LLM RESPONSE: {self.model:<62} ║")
            logger.info(f"╠{'═' * 78}╣")
            logger.info(f"║ Finish Reason: {choice.finish_reason:<60}║")
            logger.info(f"║ Prompt Tokens: {usage.prompt_tokens:<60}║")
            logger.info(f"║ Completion Tokens: {usage.completion_tokens:<56}║")
            logger.info(f"║ Total Tokens: {usage.total_tokens:<61}║")
            if usage.prompt_tokens_cached > 0:
                logger.info(f"║ Cached Tokens: {usage.prompt_tokens_cached:<60}║")
            cost_str = f"${cost_estimate.total_cost:.6f}"
            logger.info(f"║ Estimated Cost: {cost_str:<62}║")
            logger.info(f"╠{'═' * 78}╣")
            
            # Log complete content
            logger.info(f"║ CONTENT:{' ' * 69}║")
            content_lines = content.split('\n')
            for line in content_lines:
                # Wrap long lines
                while len(line) > 76:
                    logger.info(f"║ {line[:76]:<76} ║")
                    line = line[76:]
                if line or not content_lines:  # Log empty lines and remaining content
                    logger.info(f"║ {line:<76} ║")
            
            if reasoning:
                logger.info(f"╠{'═' * 78}╣")
                logger.info(f"║ REASONING:{' ' * 67}║")
                reasoning_lines = reasoning.split('\n')
                for line in reasoning_lines:
                    # Wrap long lines
                    while len(line) > 76:
                        logger.info(f"║ {line[:76]:<76} ║")
                        line = line[76:]
                    if line or not reasoning_lines:
                        logger.info(f"║ {line:<76} ║")
            
            logger.info(f"╚{'═' * 78}╝")
            
            # Clean response
            cleaned_content = self._clean_response(self._remove_thinking(content))
            
            return LLMResponse(
                content=cleaned_content,
                model=self.model,
                usage=usage,
                reasoning=reasoning,
                finish_reason=choice.finish_reason,
                raw_response=response,
            )
        
        except Exception as e:
            logger.error(f"OpenAI request failed: {e}")
            raise


class AnthropicProvider(LLMProvider):
    """
    Anthropic Claude provider implementation.
    
    Supports Claude 3.5 Sonnet, Opus, and other Claude models.
    """
    
    def __init__(
        self,
        model: str = "claude-3-5-sonnet-20241022",
        temperature: float = 1.0,
        max_tokens: int = 8192,
        api_key: Optional[str] = None,
    ):
        """
        Initialize Anthropic provider.
        
        Args:
            model: Model name
            temperature: Sampling temperature
            max_tokens: Maximum completion tokens
            api_key: Optional API key (will load from config if not provided)
        """
        super().__init__(model, temperature, max_tokens)
        
        # Get configuration
        config_key = get_anthropic_config()
        self.api_key = api_key or config_key
        
        if not self.api_key:
            raise ValueError("Anthropic API key not found. Set it in llm.yml or ANTHROPIC_API_KEY environment variable.")
        
        # Import here to make it optional
        try:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=self.api_key)
        except ImportError:
            raise ImportError("Anthropic package not installed. Run: pip install anthropic")
    
    def request(
        self,
        messages: Union[str, List[LLMMessage], List[Dict]],
        system: Optional[str] = None,
        **kwargs
    ) -> LLMResponse:
        """
        Send request to Anthropic API.
        
        Args:
            messages: Messages to send
            system: Optional system message
            **kwargs: Additional parameters
        
        Returns:
            LLMResponse
        """
        # Normalize messages
        normalized = self._normalize_messages(messages)
        
        # Separate system messages
        system_messages = []
        user_messages = []
        
        for msg in normalized:
            if msg.role == "system":
                system_messages.append(msg.content)
            else:
                user_messages.append(msg)
        
        # Combine system messages
        if system_messages:
            system = "\n\n".join(system_messages)
        
        # Convert to Anthropic format
        anthropic_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in user_messages
        ]
        
        # Log detailed request info
        logger.info(f"╔{'═' * 78}╗")
        logger.info(f"║ LLM REQUEST: {self.model:<63} ║")
        logger.info(f"╠{'═' * 78}╣")
        logger.info(f"║ Provider: Anthropic{' ' * 59}║")
        logger.info(f"║ Model: {self.model:<68}║")
        logger.info(f"║ Temperature: {self.temperature:<62}║")
        logger.info(f"║ Max Tokens: {self.max_tokens:<63}║")
        logger.info(f"║ Messages: {len(anthropic_messages):<65}║")
        logger.info(f"╠{'═' * 78}╣")
        
        # Log complete system message if present
        if system:
            logger.info(f"║ SYSTEM MESSAGE:{' ' * 62}║")
            system_lines = system.split('\n')
            for line in system_lines:
                while len(line) > 76:
                    logger.info(f"║ {line[:76]:<76} ║")
                    line = line[76:]
                if line:
                    logger.info(f"║ {line:<76} ║")
            logger.info(f"╠{'═' * 78}╣")
        
        # Log complete message contents
        for i, msg in enumerate(anthropic_messages):
            logger.info(f"║ Message [{i+1}] - {msg['role'].upper()}{' ' * (69 - len(msg['role']))}║")
            content_lines = msg['content'].split('\n')
            for line in content_lines:
                while len(line) > 76:
                    logger.info(f"║ {line[:76]:<76} ║")
                    line = line[76:]
                if line:
                    logger.info(f"║ {line:<76} ║")
        
        logger.info(f"╚{'═' * 78}╝")
        
        # Make request
        try:
            request_params = {
                "model": self.model,
                "messages": anthropic_messages,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                **kwargs
            }
            
            if system:
                request_params["system"] = system
            
            response = self.client.messages.create(**request_params)
            
            # Extract response
            content = response.content[0].text
            
            # Create usage object
            usage = TokenUsage(
                prompt_tokens=response.usage.input_tokens,
                completion_tokens=response.usage.output_tokens,
                total_tokens=response.usage.input_tokens + response.usage.output_tokens,
                prompt_tokens_cached=getattr(response.usage, "cache_read_input_tokens", 0),
            )
            
            # Record cost
            cost_estimate = self.cost_tracker.record_usage(
                self.model,
                usage.prompt_tokens,
                usage.completion_tokens,
                usage.prompt_tokens_cached,
            )
            
            # Log detailed response info
            logger.info(f"╔{'═' * 78}╗")
            logger.info(f"║ LLM RESPONSE: {self.model:<62} ║")
            logger.info(f"╠{'═' * 78}╣")
            logger.info(f"║ Finish Reason: {response.stop_reason:<60}║")
            logger.info(f"║ Prompt Tokens: {usage.prompt_tokens:<60}║")
            logger.info(f"║ Completion Tokens: {usage.completion_tokens:<56}║")
            logger.info(f"║ Total Tokens: {usage.total_tokens:<61}║")
            if usage.prompt_tokens_cached > 0:
                logger.info(f"║ Cached Tokens: {usage.prompt_tokens_cached:<60}║")
            cost_str = f"${cost_estimate.total_cost:.6f}"
            logger.info(f"║ Estimated Cost: {cost_str:<62}║")
            logger.info(f"╠{'═' * 78}╣")
            
            # Log complete content
            logger.info(f"║ CONTENT:{' ' * 69}║")
            content_lines = content.split('\n')
            for line in content_lines:
                while len(line) > 76:
                    logger.info(f"║ {line[:76]:<76} ║")
                    line = line[76:]
                if line or not content_lines:
                    logger.info(f"║ {line:<76} ║")
            
            logger.info(f"╚{'═' * 78}╝")
            
            # Clean response
            cleaned_content = self._clean_response(content)
            
            return LLMResponse(
                content=cleaned_content,
                model=self.model,
                usage=usage,
                finish_reason=response.stop_reason,
                raw_response=response,
            )
        
        except Exception as e:
            logger.error(f"Anthropic request failed: {e}")
            raise


class OllamaProvider(LLMProvider):
    """
    Ollama local model provider implementation.
    
    Supports local models through Ollama.
    """
    
    def __init__(
        self,
        model: str = "llama3.2",
        temperature: float = 1.0,
        max_tokens: int = 8192,
        base_url: Optional[str] = None,
    ):
        """
        Initialize Ollama provider.
        
        Args:
            model: Model name
            temperature: Sampling temperature
            max_tokens: Maximum completion tokens
            base_url: Optional base URL (will load from config if not provided)
        """
        super().__init__(model, temperature, max_tokens)
        
        # Get configuration
        config_url = get_ollama_config()
        self.base_url = base_url or config_url
        
        # Import here to make it optional
        try:
            import requests
            self.requests = requests
        except ImportError:
            raise ImportError("Requests package not installed. Run: pip install requests")
    
    def request(
        self,
        messages: Union[str, List[LLMMessage], List[Dict]],
        **kwargs
    ) -> LLMResponse:
        """
        Send request to Ollama API.
        
        Args:
            messages: Messages to send
            **kwargs: Additional parameters
        
        Returns:
            LLMResponse
        """
        # Normalize messages
        normalized = self._normalize_messages(messages)
        
        # Convert to Ollama format
        ollama_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in normalized
        ]
        
        # Log detailed request info
        logger.info(f"╔{'═' * 78}╗")
        logger.info(f"║ LLM REQUEST: {self.model:<63} ║")
        logger.info(f"╠{'═' * 78}╣")
        logger.info(f"║ Provider: Ollama (Local){' ' * 54}║")
        logger.info(f"║ Model: {self.model:<68}║")
        logger.info(f"║ Temperature: {self.temperature:<62}║")
        logger.info(f"║ Max Tokens: {self.max_tokens:<63}║")
        logger.info(f"║ Base URL: {self.base_url:<65}║")
        logger.info(f"║ Messages: {len(ollama_messages):<65}║")
        logger.info(f"╠{'═' * 78}╣")
        
        # Log complete message contents
        for i, msg in enumerate(ollama_messages):
            logger.info(f"║ Message [{i+1}] - {msg['role'].upper()}{' ' * (69 - len(msg['role']))}║")
            content_lines = msg['content'].split('\n')
            for line in content_lines:
                while len(line) > 76:
                    logger.info(f"║ {line[:76]:<76} ║")
                    line = line[76:]
                if line:
                    logger.info(f"║ {line:<76} ║")
        
        logger.info(f"╚{'═' * 78}╝")
        
        # Make request
        try:
            response = self.requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": ollama_messages,
                    "stream": False,
                    "options": {
                        "temperature": self.temperature,
                        "num_predict": self.max_tokens,
                    },
                    **kwargs
                }
            )
            response.raise_for_status()
            
            result = response.json()
            
            # Extract response
            content = result["message"]["content"]
            
            # Estimate token usage (Ollama doesn't always provide exact counts)
            prompt_tokens = result.get("prompt_eval_count", 0)
            completion_tokens = result.get("eval_count", 0)
            
            usage = TokenUsage(
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=prompt_tokens + completion_tokens,
            )
            
            # Log detailed response info
            logger.info(f"╔{'═' * 78}╗")
            logger.info(f"║ LLM RESPONSE: {self.model:<62} ║")
            logger.info(f"╠{'═' * 78}╣")
            logger.info(f"║ Finish Reason: {result.get('done_reason', 'N/A'):<60}║")
            logger.info(f"║ Prompt Tokens: ~{usage.prompt_tokens:<59}║")
            logger.info(f"║ Completion Tokens: ~{usage.completion_tokens:<55}║")
            logger.info(f"║ Total Tokens: ~{usage.total_tokens:<60}║")
            logger.info(f"║ Cost: FREE (Local){' ' * 58}║")
            logger.info(f"╠{'═' * 78}╣")
            
            # Log complete content
            logger.info(f"║ CONTENT:{' ' * 69}║")
            content_lines = content.split('\n')
            for line in content_lines:
                while len(line) > 76:
                    logger.info(f"║ {line[:76]:<76} ║")
                    line = line[76:]
                if line or not content_lines:
                    logger.info(f"║ {line:<76} ║")
            
            logger.info(f"╚{'═' * 78}╝")
            
            # Clean response
            cleaned_content = self._clean_response(content)
            
            return LLMResponse(
                content=cleaned_content,
                model=self.model,
                usage=usage,
                finish_reason=result.get("done_reason"),
                raw_response=result,
            )
        
        except Exception as e:
            logger.error(f"Ollama request failed: {e}")
            raise


def create_provider(
    provider: str = "openai",
    model: Optional[str] = None,
    **kwargs
) -> LLMProvider:
    """
    Factory function to create LLM provider.
    
    Args:
        provider: Provider name ("openai", "anthropic", "ollama")
        model: Optional model name (uses defaults if not provided)
        **kwargs: Additional provider-specific parameters
    
    Returns:
        LLMProvider instance
    """
    provider = provider.lower()
    
    if provider == "openai":
        model = model or "gpt-4o-mini"
        return OpenAIProvider(model=model, **kwargs)
    elif provider == "anthropic":
        model = model or "claude-3-5-sonnet-20241022"
        return AnthropicProvider(model=model, **kwargs)
    elif provider == "ollama":
        model = model or "llama3.2"
        return OllamaProvider(model=model, **kwargs)
    else:
        raise ValueError(f"Unknown provider: {provider}. Supported: openai, anthropic, ollama")
