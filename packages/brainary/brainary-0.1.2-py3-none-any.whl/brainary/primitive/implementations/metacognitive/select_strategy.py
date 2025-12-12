"""
Select strategy: assess_situation + match_approach + commit.
"""

from typing import Any, Dict, List, Optional, Tuple
import time
import logging

from brainary.primitive.base import (
    MetacognitivePrimitive,
    PrimitiveResult,
    ResourceEstimate,
    ConfidenceMetrics,
    CostMetrics,
)
from brainary.core.context import ExecutionContext
from brainary.memory.working import WorkingMemory
from brainary.llm.manager import get_llm_manager

logger = logging.getLogger(__name__)


class SelectStrategyMetacognitive(MetacognitivePrimitive):
    """
    Select strategy: assess_situation + match_approach + commit.
    
    Chooses optimal strategy based on situation assessment.
    """
    
    def __init__(self):
        """Initialize primitive."""
        super().__init__()
        self._name = "select_strategy"
        self._hint = (
            "Use for strategy selection based on situation assessment. Best when "
            "starting new tasks, facing uncertainty, or when multiple approaches "
            "are available. Analyzes context (time, quality, criticality) and "
            "matches to optimal strategy. Use at task initialization or when "
            "current strategy is unclear. Considers trade-offs between speed, "
            "quality, and resource usage."
        )
    
    def execute(
        self,
        context: ExecutionContext,
        working_memory: WorkingMemory,
        task: str,
        available_strategies: List[str] = None,
        **kwargs
    ) -> PrimitiveResult:
        """
        Select optimal strategy using LLM-powered situational analysis.
        
        Args:
            context: Execution context
            working_memory: Working memory
            task: Task to perform
            available_strategies: Available strategies (list of strategy names)
            **kwargs: Additional parameters (complexity, constraints)
        
        Returns:
            PrimitiveResult with selected strategy
        """
        start_time = time.time()
        
        try:
            available_strategies = available_strategies or ['fast', 'balanced', 'thorough', 'creative', 'systematic']
            
            # Retrieve relevant strategy context
            memory_items = working_memory.retrieve(
                query=f"strategy approach {task[:50]}",
                top_k=3
            )
            memory_context = "\n".join([f"- {item.content}" for item in memory_items])
            
            # Extract parameters
            complexity = kwargs.get('complexity', 0.5)
            constraints = kwargs.get('constraints', [])
            
            # Format strategies
            strategies_text = "\n".join(f"{i+1}. {s}" for i, s in enumerate(available_strategies))
            
            # Format constraints
            constraints_text = ""
            if constraints:
                constraints_text = "\n\nCONSTRAINTS:\n" + "\n".join(f"- {c}" for c in constraints)
            
            # Build strategy selection prompt
            prompt = f"""Select the optimal strategy for the following task based on comprehensive situational analysis.

TASK: {task}

AVAILABLE STRATEGIES:
{strategies_text}

SITUATION ASSESSMENT:
- Time Pressure: {context.time_pressure:.2f} (0=none, 1=extreme urgency)
- Quality Requirement: {context.quality_threshold:.2f} (0=low, 1=highest)
- Criticality: {context.criticality:.2f} (0=low impact, 1=mission critical)
- Task Complexity: {complexity:.2f} (0=simple, 1=highly complex){constraints_text}

PRIOR CONTEXT:
{memory_context if memory_context else "No prior strategy history"}

Provide comprehensive strategy analysis with:

1. SITUATION ANALYSIS: Analyze key factors (time, quality, criticality, complexity)
2. STRATEGY EVALUATION: Assess each available strategy's suitability
3. RECOMMENDATION: Select best strategy with detailed justification
4. TRADE-OFFS: Explain gains and sacrifices of this choice
5. FALLBACK: Suggest alternative if primary strategy fails or conditions change

Consider balance between speed, quality, resource usage, and risk."""

            # Get LLM strategy selection
            llm_manager = get_llm_manager()
            response = llm_manager.request(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )
            
            selection_text = response.content
            
            # Parse sections
            sections = {}
            section_names = ["SITUATION ANALYSIS:", "STRATEGY EVALUATION:", "RECOMMENDATION:", 
                           "TRADE-OFFS:", "FALLBACK:"]
            for i, section_name in enumerate(section_names):
                start_idx = selection_text.find(section_name)
                if start_idx == -1:
                    sections[section_name.rstrip(':')] = ""
                    continue
                
                end_idx = len(selection_text)
                for next_section in section_names[i+1:]:
                    next_idx = selection_text.find(next_section)
                    if next_idx != -1:
                        end_idx = next_idx
                        break
                
                sections[section_name.rstrip(':')] = selection_text[start_idx+len(section_name):end_idx].strip()
            
            # Extract selected strategy
            recommendation_text = sections.get('RECOMMENDATION', '').lower()
            selected = available_strategies[0]  # Default
            for strategy in available_strategies:
                if strategy.lower() in recommendation_text:
                    selected = strategy
                    break
            
            selection = {
                'task': task,
                'selected_strategy': selected,
                'situation_analysis': sections.get('SITUATION ANALYSIS', ''),
                'strategy_evaluation': sections.get('STRATEGY EVALUATION', ''),
                'recommendation': sections.get('RECOMMENDATION', ''),
                'trade_offs': sections.get('TRADE-OFFS', ''),
                'fallback': sections.get('FALLBACK', ''),
                'alternatives': [s for s in available_strategies if s != selected],
                'context_factors': {
                    'time_pressure': context.time_pressure,
                    'quality_threshold': context.quality_threshold,
                    'criticality': context.criticality,
                    'complexity': complexity,
                },
            }
            
            # Store in memory
            working_memory.store(
                content=f"Strategy selected for '{task}': {selected} (time:{context.time_pressure:.1f}, quality:{context.quality_threshold:.1f})",
                importance=0.8,
                tags=["metacognition", "strategy", selected],
            )
            
            execution_time = int((time.time() - start_time) * 1000)
            
            return PrimitiveResult(
                content=selection,
                confidence=ConfidenceMetrics(
                    overall=0.85,
                    reasoning=0.88,
                    completeness=0.85,
                    consistency=0.85,
                    evidence_strength=0.82,
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
                    'selected': selected,
                    'strategies_evaluated': len(available_strategies),
                    'model': 'gpt-4o-mini',
                }
            )
            
        except Exception as e:
            logger.error(f"Strategy selection failed: {e}")
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
        strategies = kwargs.get('available_strategies', [])
        return ResourceEstimate(
            tokens=60,
            time_ms=25,
            memory_items=1,
            complexity=0.4,
        )
    
    def validate_inputs(self, **kwargs) -> None:
        """Validate inputs."""
        if "task" not in kwargs:
            raise ValueError("'task' parameter required")
    
    def matches_context(self, context: ExecutionContext, **kwargs) -> float:
        """Check context match."""
        return 0.8  # Generally useful
    
    def rollback(self, context: ExecutionContext) -> None:
        """Rollback strategy selection."""
        pass


