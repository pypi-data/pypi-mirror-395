"""
Cognitive kernel for program execution orchestration.

The kernel is the central orchestrator that coordinates:
- Primitive routing via scheduler
- Resource allocation via resource manager
- Payload assembly and executor selection
- Memory management
- Learning and adaptation
- Metacognitive monitoring (pluggable component)

The kernel implements the OS-style architecture with system calls,
context switching, resource management, and continuous learning.

Metacognition is integrated as a pluggable component that can be:
- Overridden with custom implementations
- Disabled completely (NoOpMonitor)
- Configured with different monitoring levels
"""

import uuid
import time
import logging
from typing import Any, Dict, List, Optional

from brainary.core.context import ExecutionContext, create_execution_context
from brainary.core.scheduler import ProgramScheduler
from brainary.core.resource_manager import ResourceManager
from brainary.core.learning import (
    get_learning_system,
    LearningEvent,
    LearningEventType,
)
from brainary.core.metacognitive_monitor import (
    MetacognitiveMonitor,
    MonitoringLevel,
    ExecutionTrace,
    MetacognitiveAssessment,
)
from brainary.memory.working import WorkingMemory
from brainary.memory.semantic import SemanticMemory, KnowledgeEntry, KnowledgeType
from brainary.executors.base import ExecutionPayload, Executor
from brainary.executors.direct_llm import DirectLLMExecutor
from brainary.executors.react_agent import ReActAgentExecutor
from brainary.primitive.base import Primitive, PrimitiveResult

logger = logging.getLogger(__name__)


class CognitiveKernel:
    """
    Central orchestrator for cognitive program execution.
    
    The kernel coordinates all subsystems to provide intelligent,
    adaptive execution of cognitive programs.
    
    Responsibilities:
    1. Route primitives to optimal implementations
    2. Assemble execution payloads with augmentations
    3. Select optimal executor for payload
    4. Manage resources and memory
    5. Learn from execution traces
    6. Monitor and self-regulate via metacognitive component
    
    Metacognitive Integration:
    The kernel includes a pluggable metacognitive monitor that can:
    - Observe execution quality and patterns
    - Detect anomalies and degrading performance
    - Suggest interventions and adjustments
    - Learn optimal strategies over time
    
    The monitor is overrideable, allowing custom implementations
    or complete disabling of metacognition.
    """
    
    def __init__(
        self,
        enable_learning: bool = True,
        metacognitive_monitor: Optional[MetacognitiveMonitor] = None,
        enable_metacognition: bool = True,
        monitoring_level: MonitoringLevel = MonitoringLevel.STANDARD,
        working_memory: Optional[WorkingMemory] = None,
        semantic_memory: Optional[SemanticMemory] = None
    ):
        """
        Initialize cognitive kernel.
        
        Args:
            enable_learning: Whether to enable learning and adaptation
            metacognitive_monitor: Custom metacognitive monitor (overrides default)
            enable_metacognition: Whether to enable metacognitive monitoring
            monitoring_level: Level of monitoring if using default monitor
            working_memory: Short-term working memory for cross-execution continuity
            semantic_memory: Long-term semantic memory for knowledge-driven execution
        """
        # Register core primitive implementations if not already registered
        from brainary.primitive import register_core_primitives
        register_core_primitives()
        
        # Working memory (L2) - cross-execution continuity and monitoring
        self.working_memory = working_memory if working_memory is not None else WorkingMemory(capacity=7)
        logger.info(f"Working memory initialized: capacity={self.working_memory.capacity}")
        
        # Semantic memory (L3) - long-term knowledge
        self.semantic_memory = semantic_memory if semantic_memory is not None else SemanticMemory()
        logger.info(f"Semantic memory initialized: {self.semantic_memory.get_stats()['total_entries']} entries")
        
        self.scheduler = ProgramScheduler()
        self.resource_manager = ResourceManager()
        self.executors: List[Executor] = [
            DirectLLMExecutor(),
            ReActAgentExecutor(),
            # LangGraphExecutor() would go here
        ]
        
        # Statistics
        self.total_executions = 0
        self.successful_executions = 0
        
        # Learning system integration
        self._enable_learning = enable_learning
        if enable_learning:
            self._learning_system = get_learning_system()
            logger.info("Learning system enabled for kernel orchestration")
        
        # Metacognitive monitor (pluggable component)
        if metacognitive_monitor is not None:
            self.metacognitive_monitor = metacognitive_monitor
            logger.info(f"Using custom metacognitive monitor: {type(metacognitive_monitor).__name__}")
        elif enable_metacognition:
            self.metacognitive_monitor = MetacognitiveMonitor(
                monitoring_level=monitoring_level,
                enable_learning=enable_learning
            )
            logger.info(f"Metacognitive monitoring enabled: level={monitoring_level.value}")
        else:
            self.metacognitive_monitor = MetacognitiveMonitor(
                monitoring_level=MonitoringLevel.NONE
            )
            logger.info("Metacognitive monitoring disabled")
    
    def _create_error_result(
        self,
        primitive_name: str,
        error_message: str,
        context: ExecutionContext,
        **metadata
    ) -> PrimitiveResult:
        """Create an error result with proper structure."""
        from brainary.primitive.base import ConfidenceScore, CostMetrics
        
        return PrimitiveResult(
            content=None,
            primitive_name=primitive_name,
            success=False,
            error=error_message,
            confidence=ConfidenceScore(overall=0.0, reasoning=0.0),
            execution_mode=context.execution_mode,
            cost=CostMetrics(tokens=0, latency_ms=0, memory_slots=0, provider_cost_usd=0.0),
            metadata=metadata
        )
    
    def execute(
        self,
        primitive_name: str,
        context: Optional[ExecutionContext] = None,
        working_memory: Optional[WorkingMemory] = None,
        semantic_memory: Optional[SemanticMemory] = None,
        **kwargs
    ) -> PrimitiveResult:
        """
        Execute a primitive with intelligent routing and execution.
        
        This is the main entry point for primitive execution with
        full learning integration for continuous improvement.
        
        The kernel executes primitives in a loop, allowing the scheduler
        to synthesize or decompose additional primitives via JIT synthesis.
        Execution continues until the scheduler returns no more steps.
        
        Args:
            primitive_name: Name of primitive to execute
            context: Optional execution context (creates default if None)
            working_memory: Optional working memory (uses kernel default if None)
            semantic_memory: Optional semantic memory (uses kernel default if None)
            **kwargs: Primitive-specific parameters
        
        Returns:
            PrimitiveResult from final execution step
        """
        # Record start time for learning
        start_time = time.time()
        
        logger.info("="*80)
        logger.info(f"KERNEL: Executing primitive '{primitive_name}'")
        logger.info("="*80)
        
        # Setup context and memory
        if context is None:
            context = create_execution_context(
                program_name=f"execute_{primitive_name}"
            )
            logger.debug(f"Created default execution context: domain={context.domain}, mode={context.execution_mode}")
        
        # Use kernel's memory by default (enables cross-execution monitoring)
        if working_memory is None:
            working_memory = self.working_memory
            logger.debug(f"Using kernel working memory: capacity={working_memory.capacity}")
        
        if semantic_memory is None:
            semantic_memory = self.semantic_memory
            logger.debug(f"Using kernel semantic memory: {semantic_memory.get_stats()['total_entries']} entries")
        
        # === KNOWLEDGE ENHANCEMENT: Load contextual knowledge from semantic memory ===
        # Retrieve relevant conceptual and factual knowledge to enhance execution context
        context_query = f"{primitive_name} {context.domain} {context.execution_mode.value}"
        contextual_knowledge = semantic_memory.get_contextual_knowledge(
            query=context_query,
            include_concepts=True,
            include_facts=True,
            top_k=5
        )
        if contextual_knowledge:
            logger.debug(f"[SEMANTIC] Loaded {len(contextual_knowledge)} contextual knowledge entries")
            # Store in working memory for primitive access
            for knowledge in contextual_knowledge[:3]:  # Limit to avoid overflow
                working_memory.store(
                    content=knowledge.description,
                    importance=knowledge.importance,
                    tags=["semantic_knowledge", knowledge.knowledge_type.value]
                )
        
        # Initialize execution queue with the initial primitive
        execution_queue = [(primitive_name, kwargs)]
        last_result = None
        step_count = 0
        
        # Execute primitives in a loop until queue is empty
        # This allows scheduler to synthesize/decompose additional primitives
        while execution_queue:
            current_primitive, current_kwargs = execution_queue.pop(0)
            step_count += 1
            
            if step_count > 1:
                logger.info(f"\n{'='*80}")
                logger.info(f"KERNEL: Executing synthesized step {step_count}: '{current_primitive}'")
                logger.info(f"{'='*80}")
            
            # Execute single step (pass semantic_memory to enable knowledge access)
            result = self._execute_single_step(
                current_primitive,
                context,
                working_memory,
                semantic_memory,
                start_time,
                step_count,
                **current_kwargs
            )
            
            last_result = result
            
            # Get metacognitive assessment for this step
            step_assessment = self.metacognitive_monitor.get_assessment()
            
            # === METACOGNITIVE CONTROL: Let metacognition decide interventions ===
            # Metacognition handles quality-based control (retry, refine, verify)
            metacognitive_actions = self.metacognitive_monitor.decide_next_actions(
                current_primitive,
                context,
                result,
                step_assessment,
                **current_kwargs
            )
            
            if metacognitive_actions:
                logger.info(f"\n[METACOGNITION] Control intervention: {len(metacognitive_actions)} action(s)")
                for idx, (next_prim, next_kwargs) in enumerate(metacognitive_actions, 1):
                    logger.info(f"                Action {idx}: {next_prim}")
                execution_queue.extend(metacognitive_actions)
            
            # === COGNITION: Ask scheduler for JIT synthesis/decomposition ===
            # Scheduler handles task-level orchestration
            synthesis_steps = self.scheduler.get_next_steps(
                current_primitive,
                context,
                result,
                **current_kwargs
            )
            
            if synthesis_steps:
                logger.info(f"\n[SCHEDULER] Task synthesis: {len(synthesis_steps)} step(s)")
                for idx, (next_prim, next_kwargs) in enumerate(synthesis_steps, 1):
                    logger.info(f"            Step {idx}: {next_prim}")
                execution_queue.extend(synthesis_steps)
            
            # Stop on failure if critical
            if not result.success and context.criticality > 0.8:
                logger.warning(f"[KERNEL] Critical failure, stopping execution loop")
                break
        
        if step_count > 1:
            logger.info(f"\n{'='*80}")
            logger.info(f"KERNEL: Execution loop complete - {step_count} total steps")
            logger.info(f"{'='*80}")
        
        return last_result
    
    def _execute_single_step(
        self,
        primitive_name: str,
        context: ExecutionContext,
        working_memory: WorkingMemory,
        semantic_memory: SemanticMemory,
        start_time: float,
        step_number: int,
        **kwargs
    ) -> PrimitiveResult:
        """
        Execute a single primitive step.
        
        This is extracted from the main execute() method to support
        the execution loop pattern with JIT synthesis.
        
        Args:
            primitive_name: Name of primitive to execute
            context: Execution context
            working_memory: Working memory
            semantic_memory: Semantic memory
            start_time: Start time of overall execution
            step_number: Current step number in sequence
            **kwargs: Primitive-specific parameters
        
        Returns:
            PrimitiveResult from execution
        """
        # Generate operation ID for this step
        operation_id = str(uuid.uuid4())
        logger.debug(f"Operation ID: {operation_id}")
        
        # === SEMANTIC KNOWLEDGE: Load monitoring rules for metacognition ===
        # Retrieve metacognitive knowledge to guide monitoring
        monitoring_rules = semantic_memory.get_monitoring_rules(
            context_query=f"{primitive_name} {context.domain}",
            top_k=5
        )
        if monitoring_rules:
            logger.debug(f"[SEMANTIC] Loaded {len(monitoring_rules)} monitoring rules")
            # Pass to metacognitive monitor (future enhancement: allow monitor to use rules)
        
        # === METACOGNITION: Pre-execution Assessment ===
        pre_assessment = self.metacognitive_monitor.before_execution(
            primitive_name, context, **kwargs
        )
        if pre_assessment and pre_assessment.detected_issues:
            logger.info(f"[METACOGNITION] Pre-execution concerns detected:")
            for issue in pre_assessment.detected_issues:
                logger.info(f"    • {issue}")
            if pre_assessment.recommended_actions:
                logger.info(f"[METACOGNITION] Recommended actions:")
                for action in pre_assessment.recommended_actions:
                    logger.info(f"    • {action}")
        
        # Learning system will record events during execution
        
        try:
            # === SEMANTIC KNOWLEDGE: Load procedural knowledge for scheduling ===
            # Retrieve custom implementations and domain-specific PoK programs
            procedural_knowledge = semantic_memory.get_procedural_knowledge(
                primitive_name=primitive_name,
                domain=context.domain,
                top_k=3
            )
            if procedural_knowledge:
                logger.debug(f"[SEMANTIC] Found {len(procedural_knowledge)} procedural knowledge entries")
                # Future enhancement: Pass to scheduler to consider custom implementations
                # For now, log the available alternatives
                for proc_entry in procedural_knowledge:
                    logger.debug(f"           • {proc_entry.description} (success_rate={proc_entry.success_rate:.2f})")
            
            # Step 1: Route to optimal implementation
            logger.info(f"Step 1: Routing primitive '{primitive_name}'")
            # (Learning system can be queried for routing suggestions in future)
            primitive = self.scheduler.route(
                primitive_name, context, **kwargs
            )
            logger.info(f"        ✓ Routed to: {primitive.__class__.__name__}")
            
            # Step 1.5: JIT argument completion
            logger.info(f"Step 1.5: Completing arguments via JIT mapping")
            kwargs = self._complete_arguments_jit(primitive, primitive_name, kwargs)
            logger.info(f"        ✓ Arguments completed: {list(kwargs.keys())}")
            
            # Step 2: Estimate resources
            logger.info(f"Step 2: Estimating resource requirements")
            estimate = primitive.estimate_cost(**kwargs)
            logger.info(f"        ✓ Estimated: {estimate.tokens} tokens, {estimate.time_ms}ms, {estimate.llm_calls} LLM calls")
            logger.debug(f"        Complexity: {estimate.complexity:.2f}, Confidence: {estimate.confidence:.2f}")
            
            # Step 3: Check resource availability
            logger.info(f"Step 3: Checking resource availability")
            if not self.resource_manager.check_availability(estimate, context):
                logger.warning(f"        ✗ Insufficient resources available")
                result = self._create_error_result(
                    primitive_name,
                    "Insufficient resources",
                    context,
                    operation_id=operation_id
                )
                
                # Record resource failure for learning
                if self._enable_learning:
                    self._record_execution_complete(
                        primitive_name, context, result, 
                        start_time, operation_id,
                        implementation_name="resource_limited",
                        **kwargs
                    )
                
                logger.info("="*80)
                return result
            logger.info(f"        ✓ Resources available")
            
            # Step 4: Allocate resources
            logger.info(f"Step 4: Allocating resources")
            # Pass ResourceEstimate directly to allocate
            allocation = self.resource_manager.allocate(context, estimate)
            logger.info(f"        ✓ Resources allocated: allocation_id={allocation.allocation_id}")
            
            # Step 5: Assemble execution payload
            logger.info(f"Step 5: Assembling execution payload")
            payload = self.scheduler.assemble_payload(
                primitive, context, **kwargs
            )
            payload.payload_id = operation_id
            logger.info(f"        ✓ Payload assembled: {len(payload.pre_augmentations)} pre-augs, {len(payload.post_augmentations)} post-augs")
            
            # Step 6: Select executor
            logger.info(f"Step 6: Selecting executor")
            executor = self._select_executor(payload, context)
            logger.info(f"        ✓ Selected: {executor.__class__.__name__} (type={executor.executor_type.value})")
            
            # Step 7: Create memory snapshot
            logger.info(f"Step 7: Creating memory snapshot")
            snapshot_id = working_memory.create_snapshot(
                primitive_context=primitive_name
            )
            logger.debug(f"        ✓ Snapshot created: {snapshot_id}")
            
            # Step 8: Execute payload
            logger.info(f"Step 8: Executing payload via {executor.__class__.__name__}")
            result = executor.execute(payload, context, working_memory)
            logger.info(f"        ✓ Execution completed: success={result.success}, confidence={result.confidence.overall:.2f}")
            
            # Step 9: Record resource usage
            logger.info(f"Step 9: Recording resource usage")
            execution_time = (time.time() - start_time) * 1000  # ms
            self.resource_manager.record_usage(
                operation_id,
                tokens_used=result.cost.tokens if result.cost else 0,
                time_used_ms=execution_time,
                context=context
            )
            logger.info(f"        ✓ Usage recorded: {result.cost.tokens if result.cost else 0} tokens, {execution_time:.0f}ms")
            
            # Step 10: Update scheduler from execution
            logger.debug(f"Step 10: Updating scheduler from execution")
            self.scheduler.update_from_execution(
                primitive_name,
                primitive.name,
                context,
                result,
                **kwargs
            )
            
            # Step 11: Record execution trace for learning
            if self._enable_learning:
                logger.debug(f"Step 11: Recording execution trace for learning")
                self._record_execution_complete(
                    primitive_name, context, result,
                    start_time, operation_id,
                    implementation_name=primitive.name if hasattr(primitive, 'name') else "default",
                    **kwargs
                )
            
            # Step 12: Update statistics
            self.total_executions += 1
            if result.success:
                self.successful_executions += 1
            
            # === METACOGNITION: Post-execution Assessment ===
            trace = ExecutionTrace(
                operation_id=operation_id,
                primitive_name=primitive_name,
                start_time=start_time,
                end_time=time.time(),
                success=result.success,
                confidence=result.confidence.overall if result.confidence else 0.0,
                cost_tokens=result.cost.tokens if result.cost else 0,
                cost_time_ms=execution_time,
                context=context,
                result=result,
                metadata={"pre_assessment": pre_assessment}
            )
            
            self.metacognitive_monitor.record_trace(trace)
            post_assessment = self.metacognitive_monitor.after_execution(trace)
            
            if post_assessment and post_assessment.detected_issues:
                logger.info(f"[METACOGNITION] Post-execution assessment:")
                logger.info(f"    Health: {post_assessment.overall_health:.2f}")
                if post_assessment.detected_issues:
                    logger.info(f"    Issues detected:")
                    for issue in post_assessment.detected_issues:
                        logger.info(f"      • {issue}")
                if post_assessment.recommended_actions:
                    logger.info(f"    Recommended actions:")
                    for action in post_assessment.recommended_actions:
                        logger.info(f"      • {action}")
            
            logger.info(f"KERNEL: Execution complete - success={result.success}, total_time={execution_time:.0f}ms")
            logger.info("="*80)
            
            return result
            
        except Exception as e:
            # Handle execution failure
            logger.error("="*80)
            logger.error(f"KERNEL: Execution failed with exception")
            logger.error(f"        Exception: {type(e).__name__}: {str(e)}")
            logger.error("="*80)
            
            self.total_executions += 1
            
            # Create error result
            failure_result = self._create_error_result(
                primitive_name,
                str(e),
                context,
                operation_id=operation_id,
                error_type=type(e).__name__
            )
            
            # Record failure for learning
            if self._enable_learning:
                self._record_execution_complete(
                    primitive_name, context, failure_result,
                    start_time, operation_id,
                    implementation_name="error",
                    **kwargs
                )
            
            # === METACOGNITION: Record failure trace ===
            failure_trace = ExecutionTrace(
                operation_id=operation_id,
                primitive_name=primitive_name,
                start_time=start_time,
                end_time=time.time(),
                success=False,
                confidence=0.0,
                cost_tokens=0,
                cost_time_ms=(time.time() - start_time) * 1000,
                context=context,
                result=failure_result,
                metadata={"error_type": type(e).__name__, "error": str(e)}
            )
            self.metacognitive_monitor.record_trace(failure_trace)
            
            return failure_result
    
    def _record_execution_complete(
        self,
        primitive_name: str,
        context: ExecutionContext,
        result: PrimitiveResult,
        start_time: float,
        operation_id: str,
        implementation_name: str = "default",
        **kwargs
    ) -> None:
        """
        Record execution completion event for learning.
        
        Args:
            primitive_name: Name of the primitive
            context: Execution context
            result: Execution result
            start_time: Start timestamp
            operation_id: Operation identifier
            implementation_name: Name of the implementation used
            **kwargs: Additional parameters
        """
        execution_time_ms = (time.time() - start_time) * 1000
        
        # Create learning event
        event = LearningEvent(
            event_type=(
                LearningEventType.EXECUTION_SUCCESS if result.success
                else LearningEventType.EXECUTION_FAILURE
            ),
            timestamp=time.time(),
            context=context,
            primitive_name=primitive_name,
            implementation_used=implementation_name,
            parameters=kwargs,
            result=result,
            outcome='success' if result.success else 'failure',
            metadata={
                "operation_id": operation_id,
                "execution_time_ms": execution_time_ms,
                "latency_ms": execution_time_ms,
            }
        )
        
        # Record event
        self._learning_system.record_event(event)
    
    def execute_batch(
        self,
        primitives: List[tuple],
        context: Optional[ExecutionContext] = None,
        working_memory: Optional[WorkingMemory] = None,
        semantic_memory: Optional[SemanticMemory] = None
    ) -> List[PrimitiveResult]:
        """
        Execute multiple primitives in sequence.
        
        Args:
            primitives: List of (primitive_name, kwargs) tuples
            context: Optional execution context
            working_memory: Optional working memory (uses kernel default if None)
            semantic_memory: Optional semantic memory (uses kernel default if None)
        
        Returns:
            List of PrimitiveResults
        """
        results = []
        
        for primitive_name, kwargs in primitives:
            result = self.execute(
                primitive_name,
                context=context,
                working_memory=working_memory,
                semantic_memory=semantic_memory,
                **kwargs
            )
            results.append(result)
            
            # Stop on failure if critical
            if not result.success and context and context.criticality > 0.8:
                break
        
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get comprehensive kernel statistics including learning and metacognitive metrics.
        
        Returns:
            Dictionary of statistics from all kernel subsystems
        """
        stats = {
            'kernel': {
                'total_executions': self.total_executions,
                'successful_executions': self.successful_executions,
                'success_rate': (
                    self.successful_executions / max(1, self.total_executions)
                ),
            },
            'scheduler': self.scheduler.get_stats(),
            'resource_manager': self.resource_manager.get_stats(),
            'executors': [
                executor.get_stats() for executor in self.executors
            ],
            'working_memory': self.working_memory.get_stats(),
            'semantic_memory': self.semantic_memory.get_stats(),
        }
        
        # Add learning system stats if enabled
        if self._enable_learning:
            stats['learning'] = self._learning_system.get_stats()
        
        # Add metacognitive monitor stats
        stats['metacognition'] = self.metacognitive_monitor.get_stats()
        
        return stats
    
    def get_learning_insights(self) -> Dict[str, Any]:
        """
        Get insights from the learning system.
        
        Returns:
            Dictionary of learning insights and recommendations
        """
        if not self._enable_learning:
            return {"enabled": False}
        
        return self._learning_system.get_insights()
    
    def get_metacognitive_assessment(self) -> MetacognitiveAssessment:
        """
        Get current metacognitive assessment.
        
        Returns:
            Current assessment of cognitive health and performance
        """
        return self.metacognitive_monitor.get_assessment()
    
    def set_metacognitive_monitor(self, monitor: MetacognitiveMonitor) -> None:
        """
        Replace the current metacognitive monitor with a custom implementation.
        
        This allows runtime override of metacognitive behavior.
        
        Args:
            monitor: New metacognitive monitor to use
        """
        logger.info(f"Replacing metacognitive monitor: {type(self.metacognitive_monitor).__name__} -> {type(monitor).__name__}")
        self.metacognitive_monitor = monitor
    
    def add_semantic_knowledge(self, entry: KnowledgeEntry) -> str:
        """
        Add knowledge to semantic memory.
        
        This allows runtime addition of:
        - Conceptual knowledge (concepts, relationships)
        - Factual knowledge (facts, entities)
        - Procedural knowledge (custom implementations, PoK programs)
        - Metacognitive knowledge (monitoring rules, criteria)
        
        Args:
            entry: Knowledge entry to add
            
        Returns:
            Entry ID
            
        Example:
            >>> from brainary.memory import MetacognitiveKnowledge, create_entry_id, KnowledgeType
            >>> rule = MetacognitiveKnowledge(
            ...     entry_id=create_entry_id(KnowledgeType.METACOGNITIVE, "low confidence retry"),
            ...     key_concepts=["confidence", "retry", "quality"],
            ...     description="Retry execution if confidence < 0.6",
            ...     rule_type="monitoring_rule",
            ...     condition="confidence < 0.6",
            ...     action="retry with higher temperature",
            ...     priority=0.8
            ... )
            >>> kernel.add_semantic_knowledge(rule)
        """
        from brainary.memory.semantic import KnowledgeEntry
        entry_id = self.semantic_memory.add_knowledge(entry)
        logger.info(f"Added {entry.knowledge_type.value} knowledge to semantic memory: {entry_id}")
        return entry_id
    
    def search_semantic_knowledge(
        self,
        query: str,
        knowledge_types: Optional[List[KnowledgeType]] = None,
        top_k: int = 5
    ) -> List[KnowledgeEntry]:
        """
        Search semantic memory for relevant knowledge.
        
        Args:
            query: Search query
            knowledge_types: Filter by knowledge types (None = all types)
            top_k: Maximum results to return
            
        Returns:
            List of matching knowledge entries
            
        Example:
            >>> from brainary.memory import KnowledgeType
            >>> rules = kernel.search_semantic_knowledge(
            ...     "confidence threshold",
            ...     knowledge_types=[KnowledgeType.METACOGNITIVE],
            ...     top_k=3
            ... )
        """
        from brainary.memory.semantic import KnowledgeType
        return self.semantic_memory.search(
            query=query,
            knowledge_types=knowledge_types,
            top_k=top_k
        )
    
    def _complete_arguments_jit(
        self,
        primitive: Primitive,
        primitive_name: str,
        kwargs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        JIT argument completion - use LLM to intelligently map parameter names.
        
        This step bridges the gap between caller parameter names and primitive
        expected parameter names using LLM-based semantic understanding.
        
        Args:
            primitive: Routed primitive implementation
            primitive_name: Original primitive name
            kwargs: Caller-provided arguments
            
        Returns:
            Completed kwargs with LLM-inferred parameter mappings applied
        """
        import inspect
        import json
        
        # Get primitive's execute signature
        try:
            sig = inspect.signature(primitive.execute)
            expected_params = set(sig.parameters.keys()) - {'self', 'context', 'working_memory', 'memory', 'kwargs'}
        except Exception as e:
            logger.debug(f"Could not inspect primitive signature: {e}")
            return kwargs
        
        # Check if there are any missing parameters
        provided_params = set(kwargs.keys())
        missing_params = expected_params - provided_params
        
        if not missing_params:
            # All parameters already provided
            return kwargs
        
        logger.debug(f"           Missing parameters: {missing_params}")
        logger.debug(f"           Available parameters: {provided_params}")
        
        # Use LLM to infer parameter mappings
        try:
            from brainary.llm.manager import get_llm_manager
            llm_manager = get_llm_manager()
            
            # Build parameter info for LLM (with value previews)
            available_params_info = {}
            for k, v in kwargs.items():
                if isinstance(v, str):
                    preview = v[:100] + "..." if len(v) > 100 else v
                else:
                    preview = str(v)[:100]
                available_params_info[k] = {
                    "type": type(v).__name__,
                    "preview": preview
                }
            
            # Construct LLM prompt
            prompt = f"""You are a parameter mapping assistant for a cognitive architecture system.

Task: Map available parameters to missing required parameters based on semantic similarity.

Primitive: {primitive_name}
Required parameters (missing): {list(missing_params)}
Available parameters:
{json.dumps(available_params_info, indent=2)}

Instructions:
1. For each missing parameter, determine if it can be mapped from an available parameter
2. Consider semantic meaning (e.g., 'query' → 'question', 'input' → 'data')
3. Only map if there's clear semantic equivalence
4. Return a JSON object with mappings

Response format (JSON only):
{{
  "mappings": {{
    "missing_param_name": "available_param_name",
    ...
  }},
  "unmapped": ["param1", ...]
}}

Example:
If missing=['question'] and available=['query'], return:
{{
  "mappings": {{"question": "query"}},
  "unmapped": []
}}
"""
            
            response = llm_manager.request(
                messages=prompt,
                temperature=0.0,
                max_tokens=500
            )
            
            # Parse LLM response
            result_text = response.content.strip()
            
            # Extract JSON
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0].strip()
            
            result = json.loads(result_text)
            mappings = result.get("mappings", {})
            
            # Apply mappings
            completed = kwargs.copy()
            for missing_param, source_param in mappings.items():
                if source_param in kwargs:
                    completed[missing_param] = kwargs[source_param]
                    logger.debug(f"           LLM mapped '{source_param}' -> '{missing_param}'")
            
            return completed
            
        except Exception as e:
            logger.warning(f"           LLM-based argument completion failed: {e}")
            # Fallback to simple heuristic mapping
            return self._fallback_argument_completion(kwargs, expected_params)
    
    def _fallback_argument_completion(
        self,
        kwargs: Dict[str, Any],
        expected_params: set
    ) -> Dict[str, Any]:
        """
        Fallback heuristic-based argument completion when LLM is unavailable.
        
        Args:
            kwargs: Provided arguments
            expected_params: Expected parameter names
            
        Returns:
            Completed kwargs with heuristic mappings
        """
        completed = kwargs.copy()
        
        # Simple alias mapping as fallback
        alias_map = {
            'question': ['query', 'prompt', 'message', 'text', 'input'],
            'query': ['question', 'prompt', 'message', 'text', 'input'],
            'input': ['data', 'content', 'text', 'input_data'],
            'data': ['input', 'content', 'input_data'],
            'text': ['content', 'input', 'data', 'message'],
            'content': ['text', 'input', 'data'],
            'target': ['subject', 'item', 'object'],
            'analysis_type': ['mode', 'type', 'approach'],
        }
        
        for param in expected_params:
            if param in completed:
                continue
            
            # Check if we have a known alias
            if param in alias_map:
                for alias in alias_map[param]:
                    if alias in kwargs:
                        completed[param] = kwargs[alias]
                        logger.debug(f"           Fallback mapped '{alias}' -> '{param}'")
                        break
        
        return completed
    
    def _select_executor(
        self,
        payload: ExecutionPayload,
        context: ExecutionContext
    ) -> Executor:
        """
        Select optimal executor for payload.
        
        Args:
            payload: Execution payload
            context: Execution context
        
        Returns:
            Selected executor
        """
        # Score all capable executors
        scored = []
        for executor in self.executors:
            if executor.can_execute(payload, context):
                score = executor.estimate_suitability(payload, context)
                scored.append((score, executor))
        
        if not scored:
            # Fallback to first executor
            return self.executors[0]
        
        # Return highest scoring executor
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[0][1]


# Global kernel singleton
_global_kernel: Optional[CognitiveKernel] = None


def get_kernel() -> CognitiveKernel:
    """
    Get global cognitive kernel.
    
    Returns:
        CognitiveKernel instance
    """
    global _global_kernel
    
    if _global_kernel is None:
        _global_kernel = CognitiveKernel()
    
    return _global_kernel
