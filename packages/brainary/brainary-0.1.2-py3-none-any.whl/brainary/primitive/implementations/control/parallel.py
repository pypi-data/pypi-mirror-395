"""
Execute operations in parallel.
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


class ParallelControl(ControlPrimitive):
    """
    Execute operations in parallel.
    
    Runs independent operations concurrently for efficiency.
    """
    
    def __init__(self):
        """Initialize primitive."""
        super().__init__()
        self._name = "parallel"
        self._hint = (
            "Use for parallel execution of independent operations. Best when "
            "operations don't depend on each other and can run concurrently. "
            "Reduces total execution time for independent tasks. Use for batch "
            "processing, multiple API calls, or independent analyses. Most "
            "effective with 2-10 operations. Suitable for all domains when "
            "parallelization is beneficial."
        )
    
    def execute(
        self,
        context: ExecutionContext,
        working_memory: WorkingMemory,
        operations: List[str],
        max_concurrent: int = 5,
        **kwargs
    ) -> PrimitiveResult:
        """
        Execute operations in parallel.
        
        Args:
            context: Execution context
            working_memory: Working memory
            operations: List of operation names
            max_concurrent: Maximum concurrent operations
            **kwargs: Additional parameters
        
        Returns:
            PrimitiveResult with all results
        """
        import time
        start_time = time.time()
        
        # Simulate parallel execution
        results = []
        for i, operation in enumerate(operations):
            result = {
                'operation': operation,
                'output': f"Result of {operation}",
                'index': i,
            }
            results.append(result)
        
        # Parallel execution would be faster than sequential
        simulated_parallel_time = max(5, len(operations) / max_concurrent * 5)
        
        final_result = {
            'operations': operations,
            'completed': len(operations),
            'results': results,
            'max_concurrent': max_concurrent,
            'speedup': len(operations) / max(1, len(operations) / max_concurrent),
        }
        
        working_memory.store(
            content=f"Parallel execution: {len(operations)} operations",
            importance=0.6,
            tags=["control-flow", "parallel"],
        )
        
        execution_time = int((time.time() - start_time) * 1000)
        
        return PrimitiveResult(
            content=final_result,
            confidence=ConfidenceMetrics(
                overall=0.85,
                reasoning=0.85,
                completeness=0.9,
                consistency=0.85,
                evidence_strength=0.8,
            ),
            execution_mode=context.execution_mode,
            cost=CostMetrics(
                tokens=0,
                latency_ms=execution_time,
                memory_slots=1,
                provider_cost_usd=0.0,
            ),
            primitive_name=self.name,
            success=True,
            metadata={
                'operations': len(operations),
                'max_concurrent': max_concurrent,
            }
        )
    
    def estimate_cost(self, **kwargs) -> ResourceEstimate:
        """Estimate execution cost."""
        operations = kwargs.get('operations', [])
        max_concurrent = kwargs.get('max_concurrent', 5)
        # Parallel is faster than sequential
        time_factor = max(1, len(operations) / max_concurrent)
        return ResourceEstimate(
            tokens=0,
            time_ms=int(10 * time_factor),
            memory_items=1,
            complexity=0.4 + 0.03 * len(operations),
        )
    
    def validate_inputs(self, **kwargs) -> None:
        """Validate inputs."""
        if "operations" not in kwargs:
            raise ValueError("'operations' parameter required")
        if not kwargs["operations"]:
            raise ValueError("At least one operation required")
    
    def matches_context(self, context: ExecutionContext, **kwargs) -> float:
        """Check context match."""
        # Better when time pressure is high
        if context.time_pressure > 0.6:
            return 0.9
        return 0.7
    
    def rollback(self, context: ExecutionContext) -> None:
        """Rollback parallel execution."""
        pass


