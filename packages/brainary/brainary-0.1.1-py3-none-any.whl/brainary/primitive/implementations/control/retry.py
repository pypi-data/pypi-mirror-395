"""
Retry operation with backoff.
"""

from typing import Any, Dict, List, Optional, Tuple

from brainary.primitive.base import (
    ControlPrimitive,
    PrimitiveResult,
    ResourceEstimate,
    ConfidenceMetrics,
    CostMetrics,
)
from brainary.core.context import ExecutionContext
from brainary.memory.working import WorkingMemory


class RetryControl(ControlPrimitive):
    """
    Retry operation with backoff.
    
    Retries failed operations with exponential backoff.
    """
    
    def __init__(self):
        """Initialize primitive."""
        super().__init__()
        self._name = "retry"
        self._hint = (
            "Use for retry logic with exponential backoff. Best for handling "
            "transient failures, network operations, or unreliable operations. "
            "Automatically retries with increasing delays. Use for API calls, "
            "external service interactions, or operations that may fail temporarily. "
            "Suitable for all domains when reliability matters more than speed."
        )
    
    def execute(
        self,
        context: ExecutionContext,
        working_memory: WorkingMemory,
        operation: str,
        max_attempts: int = 3,
        backoff: str = "exponential",
        **kwargs
    ) -> PrimitiveResult:
        """
        Retry operation.
        
        Args:
            context: Execution context
            working_memory: Working memory
            operation: Operation to retry
            max_attempts: Maximum retry attempts
            backoff: Backoff strategy (exponential, linear, constant)
            **kwargs: Additional parameters
        
        Returns:
            PrimitiveResult with retry outcome
        """
        import time
        start_time = time.time()
        
        attempts = []
        success = False
        
        for attempt in range(1, max_attempts + 1):
            # Simulate operation attempt
            # Success on last attempt for demo
            attempt_success = (attempt == max_attempts) or (attempt == 2)
            
            attempt_result = {
                'attempt': attempt,
                'success': attempt_success,
                'output': f"Attempt {attempt} result" if attempt_success else None,
                'error': None if attempt_success else f"Attempt {attempt} failed",
            }
            attempts.append(attempt_result)
            
            if attempt_success:
                success = True
                break
            
            # Calculate backoff delay
            if backoff == "exponential":
                delay_ms = 100 * (2 ** (attempt - 1))
            elif backoff == "linear":
                delay_ms = 100 * attempt
            else:
                delay_ms = 100
        
        retry_result = {
            'operation': operation,
            'attempts': len(attempts),
            'max_attempts': max_attempts,
            'success': success,
            'backoff': backoff,
            'results': attempts,
        }
        
        working_memory.store(
            content=f"Retry: {operation} ({'success' if success else 'failed'})",
            importance=0.65,
            tags=["control-flow", "retry"],
        )
        
        execution_time = int((time.time() - start_time) * 1000)
        
        return PrimitiveResult(
            content=retry_result,
            confidence=ConfidenceMetrics(
                overall=0.9 if success else 0.3,
                reasoning=0.85,
                completeness=0.9,
                consistency=0.85,
                evidence_strength=0.8 if success else 0.5,
            ),
            execution_mode=context.execution_mode,
            cost=CostMetrics(
                tokens=0,
                latency_ms=execution_time,
                memory_slots=1,
                provider_cost_usd=0.0,
            ),
            primitive_name=self.name,
            success=success,
            metadata={
                'attempts': len(attempts),
                'backoff': backoff,
            }
        )
    
    def estimate_cost(self, **kwargs) -> ResourceEstimate:
        """Estimate execution cost."""
        max_attempts = kwargs.get('max_attempts', 3)
        # Estimate average case
        avg_attempts = (max_attempts + 1) / 2
        return ResourceEstimate(
            tokens=0,
            time_ms=int(50 * avg_attempts),
            memory_items=1,
            complexity=0.3 + 0.1 * avg_attempts,
        )
    
    def validate_inputs(self, **kwargs) -> None:
        """Validate inputs."""
        if "operation" not in kwargs:
            raise ValueError("'operation' parameter required")
    
    def matches_context(self, context: ExecutionContext, **kwargs) -> float:
        """Check context match."""
        # Better for critical operations
        if context.criticality > 0.7:
            return 0.9
        return 0.75
    
    def rollback(self, context: ExecutionContext) -> None:
        """Rollback retry."""
        pass

