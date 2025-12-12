"""
ReAct (Reasoning + Acting) agent executor for moderate complexity.

Implements iterative reasoning-action-observation loop suitable for
operations requiring multi-step reasoning or validation.
"""

import time
import logging
from typing import Any, Dict, List, TYPE_CHECKING

from brainary.executors.base import Executor, ExecutorType, ExecutionPayload
from brainary.primitive.base import PrimitiveResult

if TYPE_CHECKING:
    from brainary.core.context import ExecutionContext
    from brainary.memory.working import WorkingMemory

logger = logging.getLogger(__name__)


class ReActAgentExecutor(Executor):
    """
    ReAct agent executor for iterative reasoning.
    
    Best for:
    - Moderate complexity (0.4-0.7)
    - Operations requiring validation
    - Multi-step reasoning
    - Iterative refinement
    
    Strategy:
    1. Reason: Analyze current state and plan next action
    2. Act: Execute planned action (primitive)
    3. Observe: Evaluate result and update state
    4. Repeat until goal achieved or max iterations
    """
    
    def __init__(self, max_iterations: int = 5):
        """
        Initialize ReAct executor.
        
        Args:
            max_iterations: Maximum reasoning-action cycles
        """
        super().__init__(ExecutorType.REACT_AGENT)
        self.max_iterations = max_iterations
        self.min_complexity = 0.4
        self.max_complexity = 0.7
    
    def can_execute(
        self,
        payload: ExecutionPayload,
        context: 'ExecutionContext'
    ) -> bool:
        """
        Check if payload suitable for ReAct execution.
        
        Args:
            payload: Execution payload
            context: Execution context
        
        Returns:
            True if moderate complexity with validation needs
        """
        complexity = payload.compute_total_complexity()
        
        return (
            self.min_complexity <= complexity <= self.max_complexity or
            payload.has_validation() or
            payload.requires_verification
        )
    
    def estimate_suitability(
        self,
        payload: ExecutionPayload,
        context: 'ExecutionContext'
    ) -> float:
        """
        Estimate suitability for ReAct execution.
        
        Args:
            payload: Execution payload
            context: Execution context
        
        Returns:
            Suitability score (0.0-1.0)
        """
        complexity = payload.compute_total_complexity()
        
        # Base score from complexity match
        if complexity < self.min_complexity:
            score = 0.3  # Can do it, but not optimal
        elif complexity > self.max_complexity:
            score = 0.5  # Can do it, but may be better options
        else:
            # Sweet spot
            score = 1.0 - abs(complexity - 0.55) / 0.15
        
        # Boost for validation requirements
        if payload.has_validation():
            score *= 1.3
        
        # Boost for System 2 mode
        if context.execution_mode.value == "system2":
            score *= 1.2
        
        # Boost for high quality threshold
        if context.quality_threshold > 0.8:
            score *= 1.1
        
        return min(1.0, score)
    
    def execute(
        self,
        payload: ExecutionPayload,
        context: 'ExecutionContext',
        working_memory: 'WorkingMemory'
    ) -> PrimitiveResult:
        """
        Execute payload with ReAct loop.
        
        Args:
            payload: Execution payload
            context: Execution context
            working_memory: Working memory
        
        Returns:
            PrimitiveResult from execution
        """
        start_time = time.time()
        total_tokens = 0
        
        primitive_name = payload.target_primitive.name
        logger.info("="*80)
        logger.info(f"ReActAgentExecutor: Executing primitive '{primitive_name}'")
        logger.info("="*80)
        
        try:
            # Initialize state
            state = {
                'iteration': 0,
                'completed': False,
                'observations': [],
                'actions_taken': [],
            }
            logger.info(f"Initialized ReAct state: max_iterations={self.max_iterations}")
            
            # Step 1: Execute pre-augmentations
            if payload.pre_augmentations:
                logger.info(f"Step 1: Executing {len(payload.pre_augmentations)} pre-augmentations")
            for pre_aug in payload.pre_augmentations:
                result = pre_aug.execute(
                    context=context,
                    working_memory=working_memory,
                    **payload.target_params
                )
                total_tokens += result.cost.tokens
                state['observations'].append({
                    'type': 'pre_augmentation',
                    'primitive': pre_aug.name,
                    'result': result,
                })
            
            # Step 2: ReAct loop
            logger.info(f"Step 2: Starting ReAct iteration loop")
            final_result = None
            while state['iteration'] < self.max_iterations and not state['completed']:
                state['iteration'] += 1
                logger.info(f"  Iteration {state['iteration']}/{self.max_iterations}")
                
                # Reason: Analyze state and decide action
                logger.debug(f"    → Reasoning phase")
                thought = self._reason(state, payload, context, working_memory)
                state['observations'].append({
                    'type': 'thought',
                    'iteration': state['iteration'],
                    'content': thought,
                })
                
                # Act: Execute target primitive
                logger.debug(f"    → Acting: executing '{payload.target_primitive.name}'")
                result = payload.target_primitive.execute(
                    context=context,
                    working_memory=working_memory,
                    **payload.target_params
                )
                total_tokens += result.cost.tokens
                logger.debug(f"    → Action result: success={result.success}, confidence={result.confidence.overall:.2f}")
                state['actions_taken'].append({
                    'primitive': payload.target_primitive.name,
                    'result': result,
                })
                
                # Observe: Evaluate result
                logger.debug(f"    → Observing result")
                observation = self._observe(result, payload, context)
                state['observations'].append({
                    'type': 'observation',
                    'iteration': state['iteration'],
                    'content': observation,
                    'confidence': result.confidence.overall,
                })
                
                # Check termination
                if self._should_terminate(result, context, state):
                    logger.info(f"    ✓ Termination condition met")
                    state['completed'] = True
                    final_result = result
            
            # Use last result if not completed
            if final_result is None and state['actions_taken']:
                final_result = state['actions_taken'][-1]['result']
            
            # Step 3: Execute post-augmentations
            if final_result:
                for post_aug in payload.post_augmentations:
                    post_result = post_aug.execute(
                        context=context,
                        working_memory=working_memory,
                        previous_result=final_result,
                        **payload.target_params
                    )
                    total_tokens += post_result.cost.tokens
                    state['observations'].append({
                        'type': 'post_augmentation',
                        'primitive': post_aug.name,
                        'result': post_result,
                    })
            
            # Step 4: Record statistics
            elapsed_ms = int((time.time() - start_time) * 1000)
            self.record_execution(
                success=final_result.success if final_result else False,
                time_ms=elapsed_ms,
                tokens=total_tokens
            )
            
            # Step 5: Add execution metadata
            if final_result:
                final_result.metadata['executor'] = self.name
                final_result.metadata['executor_type'] = self.executor_type.value
                final_result.metadata['execution_time_ms'] = elapsed_ms
                final_result.metadata['iterations'] = state['iteration']
                final_result.metadata['react_state'] = state
            
            if not final_result:
                from brainary.primitive.base import ConfidenceScore, CostMetrics
                final_result = PrimitiveResult(
                    content=None,
                    primitive_name=payload.target_primitive.name,
                    success=False,
                    error="No result produced",
                    confidence=ConfidenceScore(overall=0.0, reasoning=0.0),
                    execution_mode=context.execution_mode,
                    cost=CostMetrics(tokens=total_tokens, latency_ms=elapsed_ms, memory_slots=0, provider_cost_usd=0.0),
                )
            
            return final_result
            
        except Exception as e:
            # Record failure
            elapsed_ms = int((time.time() - start_time) * 1000)
            self.record_execution(
                success=False,
                time_ms=elapsed_ms,
                tokens=total_tokens
            )
            
            # Return error result
            from brainary.primitive.base import ConfidenceScore, CostMetrics
            
            return PrimitiveResult(
                content=None,
                primitive_name=payload.target_primitive.name,
                success=False,
                error=str(e),
                confidence=ConfidenceScore(overall=0.0, reasoning=0.0),
                execution_mode=context.execution_mode,
                cost=CostMetrics(tokens=total_tokens, latency_ms=elapsed_ms, memory_slots=0, provider_cost_usd=0.0),
                metadata={
                    'executor': self.name,
                    'executor_type': self.executor_type.value,
                    'error_type': type(e).__name__,
                    'iterations_completed': state.get('iteration', 0),
                }
            )
    
    def _reason(
        self,
        state: Dict[str, Any],
        payload: ExecutionPayload,
        context: 'ExecutionContext',
        working_memory: 'WorkingMemory'
    ) -> str:
        """
        Reason about current state and plan next action.
        
        Args:
            state: Current execution state
            payload: Execution payload
            context: Execution context
            working_memory: Working memory
        
        Returns:
            Reasoning thought
        """
        try:
            # Use LLM for sophisticated reasoning
            from brainary.llm.manager import get_llm_manager
            
            # Build context for reasoning
            iteration = state['iteration']
            observations = state['observations']
            actions_taken = state['actions_taken']
            
            # Format observation history
            obs_history = []
            for obs in observations[-3:]:  # Last 3 observations
                if obs['type'] == 'observation':
                    obs_history.append(
                        f"- Iteration {obs.get('iteration', 0)}: "
                        f"{obs['content']} (confidence: {obs.get('confidence', 0.0):.2f})"
                    )
                elif obs['type'] == 'thought':
                    obs_history.append(
                        f"- Thought {obs.get('iteration', 0)}: {obs['content']}"
                    )
            
            obs_text = '\n'.join(obs_history) if obs_history else 'No previous observations'
            
            # Build reasoning prompt
            prompt = f"""You are an intelligent reasoning agent using the ReAct (Reasoning + Acting) framework.

Task: Execute primitive '{payload.target_primitive.name}'
Iteration: {iteration} of {self.max_iterations}

Execution Context:
- Quality threshold: {context.quality_threshold}
- Time pressure: {context.time_pressure}
- Criticality: {context.criticality}
- Domain: {context.domain or 'general'}

Recent History:
{obs_text}

Actions taken so far: {len(actions_taken)}

Analyze the current state and determine what should be done in the next iteration:
1. Has the goal been achieved? (confidence >= {context.quality_threshold})
2. What progress has been made?
3. What should be the focus of the next action?
4. Should we refine the approach or continue?

Provide a concise reasoning thought (1-2 sentences) that explains your analysis and next steps."""
            
            # Call LLM
            llm_manager = get_llm_manager()
            response = llm_manager.request(
                messages=prompt,
                temperature=0.7,  # Moderate temperature for reasoning
                max_tokens=150
            )
            
            return response.content.strip()
            
        except Exception as e:
            # Fallback to simple reasoning on error
            import logging
            logging.getLogger(__name__).warning(
                f"LLM reasoning failed: {e}, using fallback logic"
            )
            
            # Simple fallback reasoning
            if state['iteration'] == 1:
                return f"Starting execution of {payload.target_primitive.name}"
            else:
                prev_obs = state['observations'][-1] if state['observations'] else None
                if prev_obs and prev_obs['type'] == 'observation':
                    confidence = prev_obs.get('confidence', 0.0)
                    if confidence >= context.quality_threshold:
                        return "Result meets quality threshold, proceeding to completion"
                    else:
                        return f"Result confidence {confidence:.2f} below threshold, refining approach"
                return "Continuing execution"
    
    def _observe(
        self,
        result: PrimitiveResult,
        payload: ExecutionPayload,
        context: 'ExecutionContext'
    ) -> str:
        """
        Observe and evaluate execution result.
        
        Args:
            result: Primitive result to observe
            payload: Execution payload
            context: Execution context
        
        Returns:
            Observation description
        """
        if not result.success:
            return f"Execution failed: {result.error}"
        
        confidence = result.confidence.overall
        if confidence >= context.quality_threshold:
            return f"Success with confidence {confidence:.2f}, meets threshold"
        else:
            return f"Success with confidence {confidence:.2f}, below threshold {context.quality_threshold}"
    
    def _should_terminate(
        self,
        result: PrimitiveResult,
        context: 'ExecutionContext',
        state: Dict[str, Any]
    ) -> bool:
        """
        Determine if ReAct loop should terminate.
        
        Args:
            result: Latest result
            context: Execution context
            state: Current state
        
        Returns:
            True if should terminate
        """
        # Terminate on failure
        if not result.success:
            return True
        
        # Terminate if quality threshold met
        if result.confidence.overall >= context.quality_threshold:
            return True
        
        # Terminate if max iterations reached
        if state['iteration'] >= self.max_iterations:
            return True
        
        # Continue by default
        return False
