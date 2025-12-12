"""
Execute operations sequentially.
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


class SequenceControl(ControlPrimitive):
    """
    Execute operations sequentially.
    
    Runs operations in order, passing results forward.
    """
    
    def __init__(self):
        """Initialize primitive."""
        super().__init__()
        self._name = "sequence"
        self._hint = (
            "Use for sequential execution where order matters and later steps "
            "depend on earlier results. Best for workflows, pipelines, and "
            "multi-step processes. Each operation gets results from previous "
            "step. Use when operations have dependencies or side effects that "
            "must occur in specific order. Suitable for all domains."
        )
    
    def execute(
        self,
        context: ExecutionContext,
        working_memory: WorkingMemory,
        operations: List[str],
        initial_input: Any = None,
        **kwargs
    ) -> PrimitiveResult:
        """
        Execute operations in sequence.
        
        Args:
            context: Execution context
            working_memory: Working memory
            operations: List of operation names
            initial_input: Input for first operation
            **kwargs: Additional parameters
        
        Returns:
            PrimitiveResult with final result
        """
        import time
        start_time = time.time()
        
        results = []
        current_input = initial_input
        
        for i, operation in enumerate(operations):
            # Simulate operation execution
            result = {
                'operation': operation,
                'input': current_input,
                'output': f"Result of {operation}",
                'step': i + 1,
            }
            results.append(result)
            current_input = result['output']
        
        final_result = {
            'operations': operations,
            'steps_completed': len(operations),
            'results': results,
            'final_output': current_input,
        }
        
        working_memory.store(
            content=f"Sequence completed: {len(operations)} steps",
            importance=0.6,
            tags=["control-flow", "sequence"],
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
                'steps': len(operations),
            }
        )
    
    def estimate_cost(self, **kwargs) -> ResourceEstimate:
        """Estimate execution cost."""
        operations = kwargs.get('operations', [])
        return ResourceEstimate(
            tokens=0,
            time_ms=10 * len(operations),
            memory_items=1,
            complexity=0.3 + 0.05 * len(operations),
        )
    
    def validate_inputs(self, **kwargs) -> None:
        """Validate inputs."""
        if "operations" not in kwargs:
            raise ValueError("'operations' parameter required")
        if not kwargs["operations"]:
            raise ValueError("At least one operation required")
    
    def matches_context(self, context: ExecutionContext, **kwargs) -> float:
        """Check context match."""
        return 1.0  # Always available
    
    def rollback(self, context: ExecutionContext) -> None:
        """Rollback sequence."""
        pass


