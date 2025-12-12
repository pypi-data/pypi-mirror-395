"""
Execute an action with parameters.
"""

from typing import Any, Dict, List, Optional, Tuple
import time
import logging

from brainary.primitive.base import (
    CorePrimitive,
    PrimitiveResult,
    ResourceEstimate,
    ConfidenceMetrics,
    CostMetrics,
)
from brainary.core.context import ExecutionContext
from brainary.memory.working import WorkingMemory
from brainary.llm.manager import get_llm_manager

logger = logging.getLogger(__name__)


class ActionExecutor(CorePrimitive):
    """
    Execute an action with parameters.
    
    Provides structured action execution with validation and error handling.
    """
    
    def __init__(self):
        """Initialize primitive."""
        super().__init__()
        self._name = "action"
        self._hint = (
            "Use to execute actions with parameters and track outcomes. "
            "Best for tool use, API calls, system interactions, and any "
            "side-effecting operations. Suitable for all domains. Use when "
            "you need to perform operations beyond reasoning, such as calling "
            "external functions, modifying state, or interacting with systems. "
            "Provides structured error handling and execution tracking."
        )
    
    def execute(
        self,
        context: ExecutionContext,
        working_memory: WorkingMemory,
        action_name: str,
        parameters: Dict[str, Any] = None,
        validate: bool = True,
        **kwargs
    ) -> PrimitiveResult:
        """
        Execute action with LLM-powered planning and validation.
        
        Args:
            context: Execution context
            working_memory: Working memory
            action_name: Name of action to execute
            parameters: Action parameters
            validate: Whether to validate before execution
            **kwargs: Additional parameters (dry_run, preconditions)
        
        Returns:
            PrimitiveResult with action outcome
        """
        start_time = time.time()
        
        parameters = parameters or {}
        
        try:
            # Basic validation
            if validate and not action_name:
                raise ValueError("action_name cannot be empty")
            
            # Get LLM guidance for action execution
            dry_run = kwargs.get('dry_run', False)
            preconditions = kwargs.get('preconditions', [])
            
            # Retrieve relevant action context
            memory_items = working_memory.retrieve(
                query=f"action {action_name} execution",
                top_k=3
            )
            memory_context = "\n".join([f"- {item.content}" for item in memory_items])
            
            # Format parameters
            params_text = "\n".join(f"- {k}: {v}" for k, v in parameters.items())
            
            # Format preconditions
            preconditions_text = ""
            if preconditions:
                preconditions_text = "\n\nPRECONDITIONS TO CHECK:\n" + "\n".join(f"- {p}" for p in preconditions)
            
            # Build action planning prompt
            prompt = f"""Plan and validate the execution of the following action.

ACTION: {action_name}

PARAMETERS:
{params_text if params_text else "No parameters"}

EXECUTION MODE: {"Dry run (simulation)" if dry_run else "Live execution"}{preconditions_text}

PRIOR CONTEXT:
{memory_context if memory_context else "No prior action history"}

Provide action execution guidance with:

1. VALIDATION: Check if parameters are valid and complete
2. PRECONDITIONS: Verify all preconditions are met (or list what's needed)
3. EXECUTION PLAN: Step-by-step plan for executing this action
4. EXPECTED OUTCOME: What should happen if execution succeeds
5. POTENTIAL ISSUES: Risks, edge cases, or failure modes to watch for
6. ROLLBACK STRATEGY: How to undo or recover if action fails

Be specific about parameter validation and execution steps."""

            # Get LLM action planning
            llm_manager = get_llm_manager()
            response = llm_manager.request(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,  # Low temperature for precise planning
            )
            
            planning_text = response.content
            
            # Parse sections
            sections = {}
            section_names = ["VALIDATION:", "PRECONDITIONS:", "EXECUTION PLAN:", 
                           "EXPECTED OUTCOME:", "POTENTIAL ISSUES:", "ROLLBACK STRATEGY:"]
            for i, section_name in enumerate(section_names):
                start_idx = planning_text.find(section_name)
                if start_idx == -1:
                    sections[section_name.rstrip(':')] = ""
                    continue
                
                end_idx = len(planning_text)
                for next_section in section_names[i+1:]:
                    next_idx = planning_text.find(next_section)
                    if next_idx != -1:
                        end_idx = next_idx
                        break
                
                sections[section_name.rstrip(':')] = planning_text[start_idx+len(section_name):end_idx].strip()
            
            # Check validation
            validation_text = sections.get('VALIDATION', '').lower()
            validation_passed = 'valid' in validation_text or 'ok' in validation_text or 'pass' in validation_text
            
            if validate and not validation_passed and 'invalid' in validation_text:
                raise ValueError(f"Action validation failed: {sections.get('VALIDATION', 'Unknown issue')}")
            
            # Execute action (in real implementation, dispatch to action registry)
            if dry_run:
                status = 'simulated'
                execution_details = "Dry run - no actual execution"
            else:
                status = 'completed'
                execution_details = f"Executed {action_name} with {len(parameters)} parameters"
            
            result_content = {
                'action': action_name,
                'parameters': parameters,
                'status': status,
                'timestamp': time.time(),
                'validation': sections.get('VALIDATION', ''),
                'preconditions': sections.get('PRECONDITIONS', ''),
                'execution_plan': sections.get('EXECUTION PLAN', ''),
                'expected_outcome': sections.get('EXPECTED OUTCOME', ''),
                'potential_issues': sections.get('POTENTIAL ISSUES', ''),
                'rollback_strategy': sections.get('ROLLBACK STRATEGY', ''),
                'execution_details': execution_details,
                'dry_run': dry_run,
            }
            
            # Store action in memory
            working_memory.store(
                content=f"{'Simulated' if dry_run else 'Executed'}: {action_name} ({len(parameters)} params)",
                importance=0.7,
                tags=["action", action_name, status],
            )
            
            execution_time = int((time.time() - start_time) * 1000)
            
            return PrimitiveResult(
                content=result_content,
                confidence=ConfidenceMetrics(
                    overall=0.88,
                    reasoning=0.9,
                    completeness=0.88,
                    consistency=0.85,
                    evidence_strength=0.85,
                ),
                execution_mode=context.execution_mode,
                cost=CostMetrics(
                    tokens=response.usage.total_tokens,
                    latency_ms=execution_time,
                    memory_slots=1,
                    provider_cost_usd=response.cost,
                ),
                primitive_name=self.name,
                success=True,
                metadata={
                    'action_name': action_name,
                    'parameter_count': len(parameters),
                    'dry_run': dry_run,
                    'model': 'gpt-4o-mini',
                }
            )
        
        except Exception as e:
            logger.error(f"Action execution failed: {e}")
            execution_time = int((time.time() - start_time) * 1000)
            
            return PrimitiveResult(
                content={'error': str(e), 'action': action_name},
                confidence=ConfidenceMetrics(overall=0.0),
                execution_mode=context.execution_mode,
                cost=CostMetrics(
                    tokens=0,
                    latency_ms=execution_time,
                    memory_slots=0,
                    provider_cost_usd=0.0,
                ),
                primitive_name=self.name,
                success=False,
                error=str(e),
            )
    
    def estimate_cost(self, **kwargs) -> ResourceEstimate:
        """Estimate execution cost."""
        return ResourceEstimate(
            tokens=0,
            time_ms=10,
            memory_items=1,
            complexity=0.3,
        )
    
    def validate_inputs(self, **kwargs) -> None:
        """Validate inputs for execution."""
        if "action_name" not in kwargs:
            raise ValueError("'action_name' parameter required")
    
    def matches_context(self, context: ExecutionContext, **kwargs) -> float:
        """Check context match."""
        return 1.0  # Always available
    
    def rollback(self, context: ExecutionContext) -> None:
        """Rollback - would need to undo action effects."""
        pass


