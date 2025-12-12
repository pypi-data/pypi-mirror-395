"""
Direct LLM executor for simple payloads.

Optimizes simple payloads into a single LLM call with a unified prompt,
suitable for straightforward operations without complex control flow.
"""

import time
import logging
from typing import TYPE_CHECKING

from brainary.executors.base import Executor, ExecutorType, ExecutionPayload
from brainary.primitive.base import PrimitiveResult

if TYPE_CHECKING:
    from brainary.core.context import ExecutionContext
    from brainary.memory.working import WorkingMemory

logger = logging.getLogger(__name__)


class DirectLLMExecutor(Executor):
    """
    Single optimized prompt executor for simple payloads.
    
    Best for:
    - Simple primitives with complexity ≤ 0.4
    - No complex control flow
    - Minimal augmentations (0-1)
    - Fast execution requirements
    
    Strategy:
    1. Combine all operations into single prompt
    2. Execute single LLM call
    3. Parse and validate result
    """
    
    def __init__(self):
        """Initialize DirectLLM executor."""
        super().__init__(ExecutorType.DIRECT_LLM)
        self.max_complexity = 0.4
        self.max_augmentations = 1
    
    def can_execute(
        self,
        payload: ExecutionPayload,
        context: 'ExecutionContext'
    ) -> bool:
        """
        Check if payload is suitable for direct execution.
        
        Args:
            payload: Execution payload
            context: Execution context
        
        Returns:
            True if complexity low and few augmentations
        """
        complexity = payload.compute_total_complexity()
        aug_count = (
            len(payload.pre_augmentations) + 
            len(payload.post_augmentations)
        )
        
        return (
            complexity <= self.max_complexity and
            aug_count <= self.max_augmentations and
            not payload.requires_state_management
        )
    
    def estimate_suitability(
        self,
        payload: ExecutionPayload,
        context: 'ExecutionContext'
    ) -> float:
        """
        Estimate suitability for direct execution.
        
        Args:
            payload: Execution payload
            context: Execution context
        
        Returns:
            Suitability score (0.0-1.0)
        """
        if not self.can_execute(payload, context):
            return 0.0
        
        complexity = payload.compute_total_complexity()
        
        # Higher score for simpler payloads
        score = 1.0 - complexity
        
        # Boost for time-critical contexts
        if context.time_pressure > 0.7:
            score *= 1.2
        
        # Boost for System 1 mode
        if context.execution_mode.value == "system1":
            score *= 1.3
        
        return min(1.0, score)
    
    def execute(
        self,
        payload: ExecutionPayload,
        context: 'ExecutionContext',
        working_memory: 'WorkingMemory'
    ) -> PrimitiveResult:
        """
        Execute payload with single LLM call.
        
        Args:
            payload: Execution payload
            context: Execution context
            working_memory: Working memory
        
        Returns:
            PrimitiveResult from execution
        """
        start_time = time.time()
        
        primitive_name = payload.target_primitive.name
        logger.info("="*80)
        logger.info(f"DirectLLMExecutor: Executing primitive '{primitive_name}'")
        logger.info("="*80)
        
        try:
            # Step 1: Execute pre-augmentations if any
            pre_results = []
            if payload.pre_augmentations:
                logger.info(f"Step 1: Executing {len(payload.pre_augmentations)} pre-augmentations")
            for pre_aug in payload.pre_augmentations:
                result = pre_aug.execute(
                    context=context,
                    working_memory=working_memory,
                    **payload.target_params
                )
                pre_results.append(result)
            
            # Step 2: Execute target primitive
            logger.info(f"Step 2: Executing target primitive '{primitive_name}'")
            logger.info(f"         Class: {payload.target_primitive.__class__.__name__}")
            logger.info(f"         Parameters: {list(payload.target_params.keys())}")
            
            result = payload.target_primitive.execute(
                context=context,
                working_memory=working_memory,
                **payload.target_params
            )
            
            logger.info(f"         ✓ Primitive '{primitive_name}' completed successfully")
            logger.info(f"         Result: {result.success}, Confidence: {result.confidence.overall:.2f}")
            
            # Step 3: Execute post-augmentations if any
            post_results = []
            if payload.post_augmentations:
                logger.info(f"Step 3: Executing {len(payload.post_augmentations)} post-augmentations")
            for post_aug in payload.post_augmentations:
                post_result = post_aug.execute(
                    context=context,
                    working_memory=working_memory,
                    previous_result=result,
                    **payload.target_params
                )
                post_results.append(post_result)
            
            # Step 4: Record statistics
            elapsed_ms = int((time.time() - start_time) * 1000)
            tokens = result.cost.tokens
            self.record_execution(
                success=result.success,
                time_ms=elapsed_ms,
                tokens=tokens
            )
            
            logger.info(f"DirectLLMExecutor: Completed in {elapsed_ms}ms, {tokens} tokens")
            logger.info("="*80)
            
            # Step 5: Add execution metadata
            result.metadata['executor'] = self.name
            result.metadata['executor_type'] = self.executor_type.value
            result.metadata['execution_time_ms'] = elapsed_ms
            result.metadata['pre_augmentation_count'] = len(pre_results)
            result.metadata['post_augmentation_count'] = len(post_results)
            
            return result
            
        except Exception as e:
            # Record failure
            elapsed_ms = int((time.time() - start_time) * 1000)
            self.record_execution(
                success=False,
                time_ms=elapsed_ms,
                tokens=0
            )
            
            logger.error(f"DirectLLMExecutor: Failed to execute '{primitive_name}'")
            logger.error(f"                   Error: {type(e).__name__}: {str(e)}")
            logger.error("="*80)
            
            # Return error result
            from brainary.primitive.base import ConfidenceScore, CostMetrics
            
            return PrimitiveResult(
                content=None,
                primitive_name=payload.target_primitive.name,
                success=False,
                error=str(e),
                confidence=ConfidenceScore(overall=0.0, reasoning=0.0),
                execution_mode=context.execution_mode,
                cost=CostMetrics(tokens=0, latency_ms=elapsed_ms, memory_slots=0, provider_cost_usd=0.0),
                metadata={
                    'executor': self.name,
                    'executor_type': self.executor_type.value,
                    'error_type': type(e).__name__,
                }
            )
