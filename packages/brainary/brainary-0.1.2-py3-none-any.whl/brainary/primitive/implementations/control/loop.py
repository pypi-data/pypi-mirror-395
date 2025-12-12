"""
Execute operations iteratively.
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


class LoopControl(ControlPrimitive):
    """
    Execute operations iteratively.
    
    Repeats operations until condition met or max iterations reached.
    """
    
    def __init__(self):
        """Initialize primitive."""
        super().__init__()
        self._name = "loop"
        self._hint = (
            "Use for iterative execution until condition met. Best for repeated "
            "operations, convergence problems, or batch processing. Supports "
            "condition-based termination and max iteration limits. Use for "
            "optimization, refinement, or processing collections. Suitable for "
            "all domains when iteration is needed."
        )
    
    def execute(
        self,
        context: ExecutionContext,
        working_memory: WorkingMemory,
        operation: str,
        condition: str,
        max_iterations: int = 10,
        **kwargs
    ) -> PrimitiveResult:
        """
        Execute loop.
        
        Args:
            context: Execution context
            working_memory: Working memory
            operation: Operation to repeat
            condition: Termination condition
            max_iterations: Maximum iterations
            **kwargs: Additional parameters
        
        Returns:
            PrimitiveResult with loop results
        """
        import time
        start_time = time.time()
        
        results = []
        iterations = 0
        condition_met = False
        
        # Execute loop (simplified)
        while iterations < max_iterations and not condition_met:
            result = {
                'operation': operation,
                'iteration': iterations + 1,
                'output': f"Result of {operation} iteration {iterations + 1}",
            }
            results.append(result)
            iterations += 1
            
            # Check condition (simplified - terminate after 2-3 iterations)
            if iterations >= 2:
                condition_met = True
        
        loop_result = {
            'operation': operation,
            'condition': condition,
            'iterations': iterations,
            'condition_met': condition_met,
            'max_iterations': max_iterations,
            'results': results,
        }
        
        working_memory.store(
            content=f"Loop completed: {iterations} iterations",
            importance=0.6,
            tags=["control-flow", "loop"],
        )
        
        execution_time = int((time.time() - start_time) * 1000)
        
        return PrimitiveResult(
            content=loop_result,
            confidence=ConfidenceMetrics(
                overall=0.85,
                reasoning=0.85,
                completeness=0.9 if condition_met else 0.7,
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
                'iterations': iterations,
                'condition_met': condition_met,
            }
        )
    
    def estimate_cost(self, **kwargs) -> ResourceEstimate:
        """Estimate execution cost."""
        max_iterations = kwargs.get('max_iterations', 10)
        # Estimate average case (half of max)
        avg_iterations = max_iterations / 2
        return ResourceEstimate(
            tokens=0,
            time_ms=int(10 * avg_iterations),
            memory_items=1,
            complexity=0.4 + 0.05 * avg_iterations,
        )
    
    def validate_inputs(self, **kwargs) -> None:
        """Validate inputs."""
        if "operation" not in kwargs:
            raise ValueError("'operation' parameter required")
        if "condition" not in kwargs:
            raise ValueError("'condition' parameter required")
    
    def matches_context(self, context: ExecutionContext, **kwargs) -> float:
        """Check context match."""
        return 0.8
    
    def rollback(self, context: ExecutionContext) -> None:
        """Rollback loop."""
        pass


