"""
Control flow primitives for program composition.

These primitives enable complex cognitive programs through
sequencing, parallelization, conditionals, and error recovery.
"""

from typing import Any, Dict, List, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

from brainary.primitive.base import (
    ControlPrimitive,
    PrimitiveResult,
    ResourceEstimate,
    ConfidenceMetrics,
    CostMetrics,
)
from brainary.core.context import ExecutionContext
from brainary.memory.working import WorkingMemory
from brainary.core.kernel import get_kernel


class Sequence(ControlPrimitive):
    """
    Execute primitives in sequence.
    
    Each primitive's output can be used in subsequent primitives.
    """
    
    def __init__(self):
        """Initialize primitive."""
        super().__init__("sequence")
    
    def execute(
        self,
        context: ExecutionContext,
        working_memory: WorkingMemory,
        primitives: List[tuple],
        **kwargs
    ) -> PrimitiveResult:
        """
        Execute sequence.
        
        Args:
            context: Execution context
            working_memory: Working memory
            primitives: List of (primitive_name, kwargs) tuples
            **kwargs: Additional parameters
        
        Returns:
            PrimitiveResult with sequence results
        """
        kernel = get_kernel()
        results = []
        
        for i, (prim_name, prim_kwargs) in enumerate(primitives):
            # Create child context
            child_context = context.create_child_context(
                quality_threshold=context.quality_threshold,
                criticality=context.criticality,
            )
            
            # Execute primitive
            result = kernel.execute(
                prim_name,
                context=child_context,
                working_memory=working_memory,
                **prim_kwargs
            )
            
            results.append(result)
            
            # Stop on failure if critical
            if not result.success and context.criticality > 0.8:
                return PrimitiveResult(
                    content=results,
                    primitive_name=self.name,
                    success=False,
                    error=f"Failed at step {i}: {result.error}",
                    confidence=ConfidenceMetrics(
                        overall=0.0,
                        reasoning=0.0,
                        completeness=0.0,
                        consistency=0.0,
                        evidence_strength=0.0,
                    ),
                    execution_mode=context.execution_mode,
                    cost=CostMetrics(tokens=0, latency_ms=0, memory_slots=0, provider_cost_usd=0.0),
                    metadata={'completed_steps': i, 'total_steps': len(primitives)}
                )
        
        # Aggregate confidence
        avg_confidence = sum(r.confidence.overall for r in results) / len(results)
        
        return PrimitiveResult(
            content=results,
            primitive_name=self.name,
            success=True,
            confidence=ConfidenceMetrics(
                overall=avg_confidence,
                reasoning=avg_confidence,
                completeness=0.9,
                consistency=0.9,
                evidence_strength=0.8,
            ),
            cost=CostMetrics(
                tokens=sum(r.cost.tokens for r in results),
                latency_ms=sum(r.cost.latency_ms for r in results),
                memory_slots=sum(r.cost.memory_slots for r in results),
                provider_cost_usd=sum(r.cost.provider_cost_usd for r in results),
            ),
            execution_mode=context.execution_mode,
            metadata={'steps': len(primitives)}
        )
    
    def estimate_cost(self, primitives: List[tuple] = None, **kwargs) -> ResourceEstimate:
        """Estimate execution cost."""
        if not primitives:
            primitives = []
        
        # Estimate based on number of steps
        return ResourceEstimate(
            tokens=len(primitives) * 200,
            time_ms=len(primitives) * 300,
            llm_calls=len(primitives),
            complexity=0.5,
        )
    
    def matches_context(self, context: ExecutionContext) -> float:
        """Check context match."""
        return 1.0


class Parallel(ControlPrimitive):
    """
    Execute primitives in parallel.
    
    Uses thread pool for concurrent execution.
    """
    
    def __init__(self, max_workers: int = 4):
        """Initialize primitive."""
        super().__init__("parallel")
        self.max_workers = max_workers
    
    def execute(
        self,
        context: ExecutionContext,
        working_memory: WorkingMemory,
        primitives: List[tuple],
        **kwargs
    ) -> PrimitiveResult:
        """
        Execute in parallel.
        
        Args:
            context: Execution context
            working_memory: Working memory
            primitives: List of (primitive_name, kwargs) tuples
            **kwargs: Additional parameters
        
        Returns:
            PrimitiveResult with parallel results
        """
        kernel = get_kernel()
        results = []
        
        def execute_one(prim_tuple):
            prim_name, prim_kwargs = prim_tuple
            child_context = context.create_child_context(
                quality_threshold=context.quality_threshold,
                criticality=context.criticality,
            )
            return kernel.execute(
                prim_name,
                context=child_context,
                working_memory=working_memory,
                **prim_kwargs
            )
        
        # Execute in parallel
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(execute_one, prim): i
                for i, prim in enumerate(primitives)
            }
            
            for future in as_completed(futures):
                result = future.result()
                results.append((futures[future], result))
        
        # Sort by original order
        results.sort(key=lambda x: x[0])
        results = [r[1] for r in results]
        
        # Check for failures
        failures = [r for r in results if not r.success]
        if failures and context.criticality > 0.8:
            return PrimitiveResult(
                content=results,
                primitive_name=self.name,
                success=False,
                error=f"{len(failures)} parallel executions failed",
                confidence=ConfidenceMetrics(
                    overall=0.0,
                    reasoning=0.0,
                    completeness=0.0,
                    consistency=0.0,
                    evidence_strength=0.0,
                ),
                execution_mode=context.execution_mode,
                cost=CostMetrics(tokens=0, latency_ms=0, memory_slots=0, provider_cost_usd=0.0),
                metadata={'failures': len(failures), 'total': len(results)}
            )
        
        # Aggregate confidence
        avg_confidence = sum(r.confidence.overall for r in results) / len(results)
        
        return PrimitiveResult(
            content=results,
            primitive_name=self.name,
            success=True,
            confidence=ConfidenceMetrics(
                overall=avg_confidence,
                reasoning=avg_confidence,
                completeness=0.9,
                consistency=0.8,
                evidence_strength=0.8,
            ),
            cost=CostMetrics(
                tokens=sum(r.cost.tokens for r in results),
                latency_ms=max(r.cost.latency_ms for r in results) if results else 0,
                memory_slots=sum(r.cost.memory_slots for r in results),
                provider_cost_usd=sum(r.cost.provider_cost_usd for r in results),
            ),
            execution_mode=context.execution_mode,
            metadata={'parallel_tasks': len(primitives)}
        )
    
    def estimate_cost(self, primitives: List[tuple] = None, **kwargs) -> ResourceEstimate:
        """Estimate execution cost."""
        if not primitives:
            primitives = []
        
        # Time is parallel, tokens are additive
        return ResourceEstimate(
            tokens=len(primitives) * 200,
            time_ms=300,  # Parallel execution time
            llm_calls=len(primitives),
            complexity=0.6,
        )
    
    def matches_context(self, context: ExecutionContext) -> float:
        """Check context match."""
        # Good for time pressure
        if context.time_pressure > 0.7:
            return 0.9
        return 0.7


class Conditional(ControlPrimitive):
    """
    Conditional execution based on LLM evaluation.
    
    Evaluates a condition and executes different branches.
    """
    
    def __init__(self):
        """Initialize primitive."""
        super().__init__("conditional")
    
    def execute(
        self,
        context: ExecutionContext,
        working_memory: WorkingMemory,
        condition: str,
        if_true: tuple,
        if_false: tuple = None,
        **kwargs
    ) -> PrimitiveResult:
        """
        Execute conditional.
        
        Args:
            context: Execution context
            working_memory: Working memory
            condition: Condition to evaluate
            if_true: (primitive_name, kwargs) for true branch
            if_false: Optional (primitive_name, kwargs) for false branch
            **kwargs: Additional parameters
        
        Returns:
            PrimitiveResult with branch result
        """
        kernel = get_kernel()
        
        # Evaluate condition using LLM
        eval_result = kernel.execute(
            "perceive_llm",
            context=context,
            working_memory=working_memory,
            prompt=f"Evaluate this condition as true or false: {condition}\n\nRespond with only 'true' or 'false'."
        )
        
        # Determine branch
        is_true = 'true' in eval_result.content.lower()
        
        # Execute appropriate branch
        if is_true:
            prim_name, prim_kwargs = if_true
            result = kernel.execute(
                prim_name,
                context=context,
                working_memory=working_memory,
                **prim_kwargs
            )
            branch = 'true'
        elif if_false:
            prim_name, prim_kwargs = if_false
            result = kernel.execute(
                prim_name,
                context=context,
                working_memory=working_memory,
                **prim_kwargs
            )
            branch = 'false'
        else:
            # No false branch, return success
            result = PrimitiveResult(
                content=None,
                primitive_name="noop",
                success=True,
            )
            branch = 'false (skipped)'
        
        result.metadata['branch_taken'] = branch
        result.metadata['condition'] = condition
        
        return result
    
    def estimate_cost(self, **kwargs) -> ResourceEstimate:
        """Estimate execution cost."""
        return ResourceEstimate(
            tokens=400,
            time_ms=500,
            llm_calls=2,
            complexity=0.6,
        )
    
    def matches_context(self, context: ExecutionContext) -> float:
        """Check context match."""
        return 0.8


class Retry(ControlPrimitive):
    """
    Retry primitive execution with exponential backoff.
    
    Implements intelligent error recovery.
    """
    
    def __init__(self, max_attempts: int = 3):
        """Initialize primitive."""
        super().__init__("retry")
        self.max_attempts = max_attempts
    
    def execute(
        self,
        context: ExecutionContext,
        working_memory: WorkingMemory,
        primitive: tuple,
        **kwargs
    ) -> PrimitiveResult:
        """
        Execute with retry.
        
        Args:
            context: Execution context
            working_memory: Working memory
            primitive: (primitive_name, kwargs) to retry
            **kwargs: Additional parameters (max_attempts override)
        
        Returns:
            PrimitiveResult from successful execution or final failure
        """
        kernel = get_kernel()
        max_attempts = kwargs.get('max_attempts', self.max_attempts)
        
        prim_name, prim_kwargs = primitive
        
        for attempt in range(max_attempts):
            # Execute primitive
            result = kernel.execute(
                prim_name,
                context=context,
                working_memory=working_memory,
                **prim_kwargs
            )
            
            # Success - return result
            if result.success and result.confidence.overall >= context.quality_threshold:
                result.metadata['retry_attempts'] = attempt + 1
                return result
            
            # Failed - wait before retry
            if attempt < max_attempts - 1:
                # Exponential backoff
                wait_time = (2 ** attempt) * 0.1
                time.sleep(wait_time)
        
        # All attempts failed
        return PrimitiveResult(
            content=None,
            primitive_name=self.name,
            success=False,
            error=f"Failed after {max_attempts} attempts",
            metadata={'attempts': max_attempts}
        )
    
    def estimate_cost(self, **kwargs) -> ResourceEstimate:
        """Estimate execution cost."""
        max_attempts = kwargs.get('max_attempts', self.max_attempts)
        
        return ResourceEstimate(
            tokens=300 * max_attempts,
            time_ms=400 * max_attempts,
            llm_calls=max_attempts,
            complexity=0.5,
        )
    
    def matches_context(self, context: ExecutionContext) -> float:
        """Check context match."""
        # Good for critical tasks
        if context.criticality > 0.8:
            return 0.9
        return 0.6
