"""
Program scheduler for execution orchestration.

The scheduler focuses on:
1. Execution augmentation planning (pre/post primitives)
2. Payload assembly for executors
3. Complexity estimation
4. Verification requirements

For primitive implementation selection, it delegates to the PrimitiveRouter.
This separation ensures clean responsibilities:
- Router: WHAT implementation to use (selection intelligence)
- Scheduler: WHEN/HOW to execute (orchestration intelligence)
"""

import time
import logging
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
import threading

from brainary.primitive.base import Primitive, PrimitiveResult
from brainary.primitive.registry import get_global_registry
from brainary.primitive.router import get_primitive_router, RoutingDecision
from brainary.core.context import ExecutionContext
from brainary.executors.base import ExecutionPayload

logger = logging.getLogger(__name__)


class ProgramScheduler:
    """
    Program scheduler for execution orchestration.
    
    Responsibilities:
    1. Plan pre-execution augmentations (context loading, readiness checks)
    2. Plan post-execution augmentations (validation, memory consolidation)
    3. Assemble execution payloads for executors
    4. Estimate complexity and verification requirements
    5. Track scheduling statistics
    
    For primitive implementation selection, delegates to PrimitiveRouter.
    """
    
    def __init__(self):
        """Initialize scheduler."""
        self._lock = threading.RLock()
        self._router = get_primitive_router()
        
        # Statistics
        self.total_scheduled = 0
        self.augmentation_count = 0
    
    def route(
        self,
        primitive_name: str,
        context: ExecutionContext,
        **kwargs
    ) -> Primitive:
        """
        Route primitive to optimal implementation.
        
        Delegates to PrimitiveRouter for actual routing intelligence.
        
        Args:
            primitive_name: Name of primitive to route
            context: Execution context
            **kwargs: Additional routing parameters
        
        Returns:
            Selected primitive implementation
        """
        logger.debug(f"SCHEDULER: Routing '{primitive_name}' (context: {context.domain}/{context.execution_mode})")
        
        # Delegate to router for implementation selection
        decision = self._router.route(primitive_name, context, **kwargs)
        
        logger.debug(f"           Selected: {decision.implementation.__class__.__name__} "
                    f"(confidence={decision.confidence:.2f}, source={decision.source.value})")
        
        return decision.implementation
    
    def get_next_steps(
        self,
        primitive_name: str,
        context: ExecutionContext,
        result: Optional[PrimitiveResult] = None,
        **kwargs
    ) -> List[tuple]:
        """
        Get next primitives to execute based on JIT synthesis or decomposition.
        
        This focuses on COGNITION-LEVEL control:
        - Task decomposition into sub-primitives
        - Synthesis of follow-up primitives
        - Generation of verification steps
        - Multi-step execution sequencing
        
        NOTE: Metacognitive control (retry, refinement based on quality) is handled
        by the MetacognitiveMonitor.decide_next_actions() method.
        
        Args:
            primitive_name: Name of the primitive just executed
            context: Execution context
            result: Result of the primitive execution (if any)
            **kwargs: Additional parameters
        
        Returns:
            List of (primitive_name, kwargs) tuples to execute next.
            Empty list means no more steps needed.
        """
        next_steps = []
        
        # === JIT SYNTHESIS: Decomposition, verification, etc. ===
        # TODO: Implement synthesis logic
        # 1. Decompose complex primitives into sub-primitives
        # 2. Synthesize follow-up primitives based on intermediate results
        # 3. Generate verification steps
        # 4. Plan multi-step execution sequences
        
        # Example: If result suggests need for verification
        # if result and context.quality_threshold > 0.8:
        #     next_steps.append(('verify', {'target': result}))
        
        return next_steps
    
    def update_from_execution(
        self,
        primitive_name: str,
        impl_name: str,
        context: ExecutionContext,
        result: PrimitiveResult,
        **kwargs
    ) -> None:
        """
        Update routing intelligence from execution feedback.
        
        Delegates to PrimitiveRouter for learning updates.
        
        Args:
            primitive_name: Primitive name
            impl_name: Implementation name used
            context: Execution context
            result: Execution result
            **kwargs: Additional parameters
        """
        # Delegate to router for learning updates
        self._router.record_execution(impl_name, result, context)
    
    def plan_pre_execution_augmentations(
        self,
        primitive_name: str,
        primitive: Primitive,
        context: ExecutionContext,
        **kwargs
    ) -> List[Primitive]:
        """
        Plan pre-execution augmentations.
        
        Args:
            primitive_name: Primitive name
            primitive: Primitive instance
            context: Execution context
            **kwargs: Additional parameters
        
        Returns:
            List of augmentation primitives to execute before main primitive
        """
        augmentations = []
        
        # Rule-based augmentation planning
        # TODO: Implement experience-based filtering
        
        # Augmentation rules from design doc
        if kwargs.get('depth', 0) >= 3:
            # Deep reasoning needs context
            # augmentations.append(retrieve_memory_primitive)
            pass
        
        if context.criticality > 0.8:
            # Critical operations need readiness check
            # augmentations.append(assess_readiness_primitive)
            pass
        
        if context.quality_threshold > 0.9:
            # High quality needs domain knowledge
            # augmentations.append(load_domain_knowledge_primitive)
            pass
        
        if context.domain:
            # Domain-specific operations need context
            # augmentations.append(load_domain_knowledge_primitive)
            pass
        
        return augmentations
    
    def plan_post_execution_augmentations(
        self,
        primitive_name: str,
        primitive: Primitive,
        context: ExecutionContext,
        **kwargs
    ) -> List[Primitive]:
        """
        Plan post-execution augmentations.
        
        Args:
            primitive_name: Primitive name
            primitive: Primitive instance
            context: Execution context
            **kwargs: Additional parameters
        
        Returns:
            List of augmentation primitives to execute after main primitive
        """
        augmentations = []
        
        # Rule-based augmentation planning
        
        if kwargs.get('depth', 0) >= 3:
            # Deep reasoning stores insights
            # augmentations.append(consolidate_memory_primitive)
            pass
        
        if context.criticality > 0.8:
            # Critical operations need validation
            # augmentations.append(self_assess_primitive)
            # augmentations.append(verify_reasoning_primitive)
            pass
        
        if context.quality_threshold > 0.9:
            # High quality needs verification
            # augmentations.append(verify_reasoning_primitive)
            pass
        
        return augmentations
    
    def assemble_payload(
        self,
        primitive: Primitive,
        context: ExecutionContext,
        **kwargs
    ) -> ExecutionPayload:
        """
        Assemble execution payload with augmentations.
        
        Args:
            primitive: Target primitive
            context: Execution context
            **kwargs: Primitive parameters
        
        Returns:
            ExecutionPayload ready for execution
        """
        # Plan augmentations
        pre_aug = self.plan_pre_execution_augmentations(
            primitive.name, primitive, context, **kwargs
        )
        post_aug = self.plan_post_execution_augmentations(
            primitive.name, primitive, context, **kwargs
        )
        
        # Estimate complexity
        complexity = primitive.estimate_cost(**kwargs).complexity
        
        # Create payload
        payload = ExecutionPayload(
            target_primitive=primitive,
            target_params=kwargs,
            pre_augmentations=pre_aug,
            post_augmentations=post_aug,
            complexity=complexity,
            requires_verification=(context.quality_threshold > 0.8),
        )
        
        return payload
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get scheduler statistics.
        
        Returns:
            Dictionary of statistics including routing stats from router
        """
        with self._lock:
            # Get routing stats from router
            router_stats = {}
            for impl_name in ['think_fast', 'think_deep', 'perceive_llm', 'remember', 'recall']:
                stats = self._router.get_statistics(impl_name)
                if stats:
                    router_stats[impl_name] = {
                        'total_calls': stats.total_calls,
                        'success_rate': stats.success_rate,
                        'avg_latency_ms': stats.avg_latency_ms,
                    }
            
            return {
                'total_scheduled': self.total_scheduled,
                'augmentation_count': self.augmentation_count,
                'router_stats': router_stats,
            }
