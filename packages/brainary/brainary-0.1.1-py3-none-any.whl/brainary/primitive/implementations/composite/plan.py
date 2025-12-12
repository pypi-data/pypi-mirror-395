"""
Create action plans for goals.
"""

from typing import Any, Dict, List, Optional, Tuple
import time
import logging

from brainary.primitive.base import (
    CompositePrimitive,
    PrimitiveResult,
    ResourceEstimate,
    ConfidenceMetrics,
    CostMetrics,
)
from brainary.core.context import ExecutionContext
from brainary.memory.working import WorkingMemory
from brainary.llm.manager import get_llm_manager

logger = logging.getLogger(__name__)


class PlanComposite(CompositePrimitive):
    """
    Create action plans for goals.
    
    Uses: think + decompose + evaluate + remember
    """
    
    # Declare sub-primitives
    sub_primitives = ["think", "decompose", "evaluate", "remember"]
    
    def __init__(self):
        """Initialize primitive."""
        super().__init__()
        self._name = "plan"
        self._hint = (
            "Use to create action plans for achieving goals. Best when systematic "
            "approach needed or multiple steps required. Creates ordered steps, "
            "identifies dependencies, estimates resources. Use for complex tasks, "
            "projects, or multi-step processes. Quality threshold >0.7 recommended."
        )
    
    def execute(
        self,
        context: ExecutionContext,
        working_memory: WorkingMemory,
        goal: str,
        **kwargs
    ) -> PrimitiveResult:
        """
        Create action plan for goal using LLM.
        
        Args:
            context: Execution context
            working_memory: Working memory
            goal: Goal to plan for
            **kwargs: Additional parameters (constraints, resources, time_limit)
        
        Returns:
            PrimitiveResult with plan
        """
        start_time = time.time()
        
        try:
            # Retrieve relevant planning context
            memory_items = working_memory.retrieve(
                query=f"plan strategy {goal[:50]}",
                top_k=4
            )
            memory_context = "\n".join([f"- {item.content}" for item in memory_items])
            
            # Extract parameters
            constraints = kwargs.get('constraints', [])
            resources = kwargs.get('resources', [])
            time_limit = kwargs.get('time_limit', 'not specified')
            
            # Format optional information
            constraints_text = ""
            if constraints:
                constraints_text = "\n\nCONSTRAINTS:\n" + "\n".join(f"- {c}" for c in constraints)
            
            resources_text = ""
            if resources:
                resources_text = "\n\nAVAILABLE RESOURCES:\n" + "\n".join(f"- {r}" for r in resources)
            
            # Build planning prompt
            prompt = f"""Create a detailed, actionable plan to achieve the following goal.

GOAL: {goal}

TIME LIMIT: {time_limit}{constraints_text}{resources_text}

CONTEXT FROM MEMORY:
{memory_context if memory_context else "No prior planning context"}

Provide a comprehensive action plan with:

1. STRATEGY: Overall approach and methodology
2. PHASES: Break down into 3-5 major phases with clear objectives
3. DETAILED STEPS: For each phase, provide specific actionable steps
4. DEPENDENCIES: Identify what must be completed before each step
5. RESOURCES NEEDED: List required resources, tools, or support
6. TIMELINE: Estimated time for each phase
7. RISK MITIGATION: Identify potential risks and mitigation strategies
8. SUCCESS CRITERIA: Define how to measure success

Format steps clearly with numbering (e.g., Phase 1 Step 1, Phase 1 Step 2, etc.)."""

            # Get LLM plan
            llm_manager = get_llm_manager()
            response = llm_manager.request(
                model="gpt-4o",  # Use powerful model for comprehensive planning
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
            )
            
            plan_text = response.content
            
            # Parse sections
            sections = {}
            section_names = ["STRATEGY:", "PHASES:", "DETAILED STEPS:", "DEPENDENCIES:", 
                           "RESOURCES NEEDED:", "TIMELINE:", "RISK MITIGATION:", "SUCCESS CRITERIA:"]
            for i, section_name in enumerate(section_names):
                start_idx = plan_text.find(section_name)
                if start_idx == -1:
                    sections[section_name.rstrip(':')] = ""
                    continue
                
                end_idx = len(plan_text)
                for next_section in section_names[i+1:]:
                    next_idx = plan_text.find(next_section)
                    if next_idx != -1:
                        end_idx = next_idx
                        break
                
                sections[section_name.rstrip(':')] = plan_text[start_idx+len(section_name):end_idx].strip()
            
            # Parse phases
            phases = []
            phases_text = sections.get('PHASES', '')
            if phases_text:
                lines = phases_text.split('\n')
                for line in lines:
                    line = line.strip()
                    if line and (line[0].isdigit() or line.startswith('-')):
                        phases.append(line)
            
            # Parse steps
            steps = []
            steps_text = sections.get('DETAILED STEPS', '')
            if steps_text:
                lines = steps_text.split('\n')
                for line in lines:
                    line = line.strip()
                    if line and (line[0].isdigit() or line.startswith('-') or 'step' in line.lower()):
                        steps.append(line)
            
            plan = {
                'goal': goal,
                'strategy': sections.get('STRATEGY', ''),
                'phases': phases,
                'steps': steps,
                'dependencies': sections.get('DEPENDENCIES', ''),
                'resources_needed': sections.get('RESOURCES NEEDED', ''),
                'timeline': sections.get('TIMELINE', ''),
                'risk_mitigation': sections.get('RISK MITIGATION', ''),
                'success_criteria': sections.get('SUCCESS CRITERIA', ''),
                'total_phases': len(phases),
                'total_steps': len(steps),
                'time_limit': time_limit,
            }
            
            # Store in memory
            working_memory.store(
                content=f"Created plan for '{goal}': {len(phases)} phases, {len(steps)} steps",
                importance=0.85,
                tags=["planning", "action-plan", "strategy"],
            )
            
            execution_time = int((time.time() - start_time) * 1000)
            
            return PrimitiveResult(
                content=plan,
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
                    'phases': len(phases),
                    'steps': len(steps),
                    'model': 'gpt-4o',
                }
            )
            
        except Exception as e:
            logger.error(f"Planning failed: {e}")
            execution_time = int((time.time() - start_time) * 1000)
            return PrimitiveResult(
                content={'error': str(e)},
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
                metadata={'error': str(e)}
            )
    
    def estimate_cost(self, **kwargs) -> ResourceEstimate:
        """Estimate execution cost."""
        goal = kwargs.get('goal', '')
        complexity = len(goal) / 100
        return ResourceEstimate(
            tokens=0,
            time_ms=int(18 + 5 * complexity),
            memory_items=1,
            complexity=0.5 + 0.1 * complexity,
        )
    
    def validate_inputs(self, **kwargs) -> None:
        """Validate inputs."""
        if "goal" not in kwargs:
            raise ValueError("'goal' parameter required")
    
    def matches_context(self, context: ExecutionContext, **kwargs) -> float:
        """Check context match."""
        if context.quality_threshold > 0.7:
            return 0.9
        return 0.75
    
    def rollback(self, context: ExecutionContext) -> None:
        """Rollback plan."""
        pass

