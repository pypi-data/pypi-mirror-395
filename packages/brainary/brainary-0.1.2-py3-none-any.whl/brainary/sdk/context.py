"""
Context Management Utilities

Provides context builder and context manager for scoped execution.
"""

from typing import Any, Dict, Optional, List, TYPE_CHECKING
from dataclasses import dataclass, field
from brainary.core.context import ExecutionContext, ExecutionMode, create_execution_context

if TYPE_CHECKING:
    from brainary.sdk.client import Brainary


@dataclass
class ContextBuilder:
    """
    Fluent builder for creating execution contexts.
    
    Provides a chainable interface for building complex contexts
    without needing to understand all parameters.
    
    Examples:
        >>> from brainary.sdk import ContextBuilder
        >>> context = (ContextBuilder()
        ...     .program("my_app")
        ...     .domain("medical")
        ...     .quality(0.95)
        ...     .budget(5000)
        ...     .fast_mode()
        ...     .build())
    """
    
    _config: Dict[str, Any] = field(default_factory=dict)
    
    def program(self, name: str) -> 'ContextBuilder':
        """Set program name."""
        self._config['program_name'] = name
        return self
    
    def domain(self, domain: str) -> 'ContextBuilder':
        """Set domain/category."""
        self._config['domain'] = domain
        return self
    
    def quality(self, threshold: float) -> 'ContextBuilder':
        """Set quality threshold (0-1)."""
        self._config['quality_threshold'] = threshold
        return self
    
    def budget(self, tokens: int) -> 'ContextBuilder':
        """Set token budget."""
        self._config['token_budget'] = tokens
        return self
    
    def mode(self, mode: ExecutionMode) -> 'ContextBuilder':
        """Set execution mode."""
        self._config['execution_mode'] = mode
        return self
    
    def fast_mode(self) -> 'ContextBuilder':
        """Use fast/System1 execution."""
        self._config['execution_mode'] = ExecutionMode.SYSTEM1
        return self
    
    def deep_mode(self) -> 'ContextBuilder':
        """Use deep/System2 execution."""
        self._config['execution_mode'] = ExecutionMode.SYSTEM2
        return self
    
    def adaptive_mode(self) -> 'ContextBuilder':
        """Use adaptive execution."""
        self._config['execution_mode'] = ExecutionMode.ADAPTIVE
        return self
    
    def cached_mode(self) -> 'ContextBuilder':
        """Use cached execution."""
        self._config['execution_mode'] = ExecutionMode.CACHED
        return self
    
    def metadata(self, **kwargs: Any) -> 'ContextBuilder':
        """Add custom metadata."""
        if 'metadata' not in self._config:
            self._config['metadata'] = {}
        self._config['metadata'].update(kwargs)
        return self
    
    def timeout(self, seconds: float) -> 'ContextBuilder':
        """Set execution timeout in seconds."""
        self._config['time_budget_ms'] = int(seconds * 1000)
        return self
    
    def constraints(self, *constraints: str) -> 'ContextBuilder':
        """
        Add execution constraints.
        Note: Stored in metadata as ExecutionContext doesn't have constraints field.
        """
        if 'metadata' not in self._config:
            self._config['metadata'] = {}
        if 'constraints' not in self._config['metadata']:
            self._config['metadata']['constraints'] = []
        self._config['metadata']['constraints'].extend(constraints)
        return self
    
    def goals(self, *goals: str) -> 'ContextBuilder':
        """
        Add execution goals.
        Note: Stored in metadata as ExecutionContext doesn't have goals field.
        """
        if 'metadata' not in self._config:
            self._config['metadata'] = {}
        if 'goals' not in self._config['metadata']:
            self._config['metadata']['goals'] = []
        self._config['metadata']['goals'].extend(goals)
        return self
    
    def reset(self) -> 'ContextBuilder':
        """Reset to default configuration."""
        self._config.clear()
        return self
    
    def build(self) -> ExecutionContext:
        """
        Build the execution context.
        
        Returns:
            ExecutionContext with configured parameters
        
        Examples:
            >>> builder = ContextBuilder()
            >>> context = builder.program("test").quality(0.9).build()
        """
        return create_execution_context(**self._config)
    
    def __repr__(self) -> str:
        return f"ContextBuilder({len(self._config)} params)"


class ContextManager:
    """
    Context manager for scoped Brainary execution.
    
    Provides 'with' statement support for temporary context overrides.
    
    Examples:
        >>> brain = Brainary()
        >>> with brain.context(domain="medical", quality=0.95):
        ...     result = brain.think("Diagnose symptoms")
    """
    
    def __init__(self, client: 'Brainary', config: Dict[str, Any]):
        """
        Initialize context manager.
        
        Args:
            client: Brainary client instance
            config: Context configuration
        """
        self.client = client
        self.config = config
        self._previous_config: Optional[Dict[str, Any]] = None
        self._context: Optional[ExecutionContext] = None
    
    def __enter__(self) -> ExecutionContext:
        """Enter context."""
        # Save previous config
        self._previous_config = self.client._default_config.copy()
        
        # Apply new config
        self.client._default_config.update(self.config)
        
        # Create context
        self._context = self.client._create_context()
        
        return self._context
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context."""
        # Restore previous config
        if self._previous_config:
            self.client._default_config = self._previous_config
        
        return False


def create_context(
    program_name: str = "brainary_app",
    domain: Optional[str] = None,
    quality_threshold: float = 0.8,
    token_budget: int = 10000,
    execution_mode: ExecutionMode = ExecutionMode.ADAPTIVE,
    **kwargs
) -> ExecutionContext:
    """
    Create execution context with common parameters.
    
    Convenience function for creating contexts without using the builder.
    
    Args:
        program_name: Name for this program
        domain: Domain/category
        quality_threshold: Quality threshold (0-1)
        token_budget: Maximum tokens
        execution_mode: Execution mode
        **kwargs: Additional parameters
    
    Returns:
        ExecutionContext
    
    Examples:
        >>> from brainary.sdk.context import create_context
        >>> context = create_context(
        ...     program_name="analyzer",
        ...     domain="security",
        ...     quality_threshold=0.95
        ... )
    """
    config = {
        'program_name': program_name,
        'quality_threshold': quality_threshold,
        'token_budget': token_budget,
        'execution_mode': execution_mode,
        **kwargs
    }
    
    if domain:
        config['domain'] = domain
    
    return create_execution_context(**config)
