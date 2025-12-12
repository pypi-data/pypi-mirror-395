"""
Error handling and exception hierarchy for Brainary system.

Implements error hierarchy from SPECIFICATION.md Section 5.2.
"""

import time
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from brainary.core.context import ExecutionContext
    from brainary.primitive.base import Primitive


class BrainaryError(Exception):
    """Base exception for all Brainary errors (matches SPECIFICATION.md)."""
    
    def __init__(
        self,
        message: str,
        context: Optional['ExecutionContext'] = None,
        recoverable: bool = True
    ):
        super().__init__(message)
        self.context = context
        self.recoverable = recoverable
        self.timestamp = time.time()


class PrimitiveExecutionError(BrainaryError):
    """Error during primitive execution (matches SPECIFICATION.md)."""
    
    def __init__(
        self,
        message: str,
        primitive: 'Primitive',
        **kwargs
    ):
        super().__init__(message, **kwargs)
        self.primitive = primitive


class ResourceExhaustedError(BrainaryError):
    """Resource quota exceeded (matches SPECIFICATION.md)."""
    
    def __init__(
        self,
        resource_type: str,
        requested: float,
        available: float,
        **kwargs
    ):
        message = f"{resource_type} exhausted: requested {requested}, available {available}"
        super().__init__(message, **kwargs)
        self.resource_type = resource_type
        self.requested = requested
        self.available = available


class NoImplementationError(BrainaryError):
    """No suitable implementation found (matches SPECIFICATION.md)."""
    
    def __init__(self, message: str, **kwargs):
        kwargs.setdefault('recoverable', False)
        super().__init__(message, **kwargs)


class MemoryFullError(BrainaryError):
    """Memory capacity exceeded."""
    
    def __init__(self, message: str = "Memory full, eviction failed", **kwargs):
        super().__init__(message, **kwargs)


class ValidationError(BrainaryError):
    """Input validation failed."""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(message, **kwargs)


class TimeoutError(BrainaryError):
    """Operation exceeded time budget."""
    
    def __init__(self, message: str, elapsed_ms: float, budget_ms: float, **kwargs):
        super().__init__(message, **kwargs)
        self.elapsed_ms = elapsed_ms
        self.budget_ms = budget_ms


class TransactionError(BrainaryError):
    """Transaction commit/rollback failed."""
    
    def __init__(self, message: str, transaction_id: str, **kwargs):
        super().__init__(message, **kwargs)
        self.transaction_id = transaction_id


class LLMProviderError(BrainaryError):
    """LLM provider API error."""
    
    def __init__(
        self,
        message: str,
        provider: str,
        status_code: Optional[int] = None,
        **kwargs
    ):
        super().__init__(message, **kwargs)
        self.provider = provider
        self.status_code = status_code


class RateLimitError(LLMProviderError):
    """Rate limit exceeded from LLM provider."""
    
    def __init__(self, message: str, provider: str, retry_after: Optional[float] = None, **kwargs):
        super().__init__(message, provider, status_code=429, **kwargs)
        self.retry_after = retry_after


class RecoveryFailedError(BrainaryError):
    """Error recovery attempt failed."""
    
    def __init__(self, message: str, original_error: Exception, **kwargs):
        super().__init__(message, **kwargs)
        self.original_error = original_error
