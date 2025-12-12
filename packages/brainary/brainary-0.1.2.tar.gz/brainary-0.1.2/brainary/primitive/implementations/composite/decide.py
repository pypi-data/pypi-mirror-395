"""
Decide: evaluate + compare + choose + commit.
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


class DecideComposite(CompositePrimitive):
    """
    Decide: evaluate + compare + choose + commit.
    
    Makes decisions by evaluating alternatives.
    """
    
    def __init__(self):
        """Initialize primitive."""
        super().__init__()
        self._name = "decide"
        self.sub_primitives = ["evaluate", "think", "remember"]
        self._hint = (
            "Use for decision-making by evaluating alternatives. Best when you "
            "have multiple options and need to select the best one. Composes "
            "evaluate + think + remember primitives. Use for choice selection, "
            "trade-off analysis, option ranking, or any decision requiring "
            "systematic evaluation. Works well with criticality >0.6."
        )
    
    def execute(
        self,
        context: ExecutionContext,
        working_memory: WorkingMemory,
        options: List[Dict[str, Any]],
        criteria: Dict[str, float],
        **kwargs
    ) -> PrimitiveResult:
        """
        Make decision using LLM-powered evaluation.
        
        Args:
            context: Execution context
            working_memory: Working memory
            options: Available options (list of dicts or strings)
            criteria: Decision criteria with weights
            **kwargs: Additional parameters
        
        Returns:
            PrimitiveResult with decision
        """
        start_time = time.time()
        
        try:
            if not options:
                raise ValueError("At least one option required")
            
            # Retrieve relevant context from memory
            memory_items = working_memory.retrieve(
                query=f"decisions criteria {' '.join(str(c) for c in criteria.keys())}",
                top_k=3
            )
            memory_context = "\n".join([f"- {item.content}" for item in memory_items])
            
            # Format options for LLM
            options_text = ""
            for i, opt in enumerate(options, 1):
                if isinstance(opt, dict):
                    opt_str = ", ".join(f"{k}: {v}" for k, v in opt.items())
                else:
                    opt_str = str(opt)
                options_text += f"\nOption {i}: {opt_str}"
            
            # Format criteria
            criteria_text = "\n".join(
                f"- {criterion}: weight {weight:.2f}"
                for criterion, weight in criteria.items()
            )
            
            # Build decision prompt
            prompt = f"""Make a decision by evaluating the following options against the given criteria.

AVAILABLE OPTIONS:{options_text}

DECISION CRITERIA:
{criteria_text}

CONTEXT FROM MEMORY:
{memory_context if memory_context else "No relevant prior context"}

Analyze each option systematically and provide:

1. EVALUATION: Score each option (0-100) against each criterion
2. COMPARISON: Compare options highlighting trade-offs
3. RECOMMENDATION: Select the best option with justification
4. ALTERNATIVES: Identify viable alternatives and when to consider them
5. RISKS: List potential risks of the recommended option

Be systematic and analytical in your evaluation."""

            # Get LLM decision
            llm_manager = get_llm_manager()
            response = llm_manager.request(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )
            
            analysis_text = response.content
            
            # Parse sections
            sections = {}
            section_names = ["EVALUATION:", "COMPARISON:", "RECOMMENDATION:", "ALTERNATIVES:", "RISKS:"]
            for i, section_name in enumerate(section_names):
                start_idx = analysis_text.find(section_name)
                if start_idx == -1:
                    sections[section_name.rstrip(':')] = ""
                    continue
                
                end_idx = len(analysis_text)
                for next_section in section_names[i+1:]:
                    next_idx = analysis_text.find(next_section)
                    if next_idx != -1:
                        end_idx = next_idx
                        break
                
                sections[section_name.rstrip(':')] = analysis_text[start_idx+len(section_name):end_idx].strip()
            
            # Extract recommendation
            recommendation_text = sections.get('RECOMMENDATION', '')
            selected_option = options[0]  # Default to first option
            
            # Try to identify which option was recommended
            for i, opt in enumerate(options):
                opt_str = str(opt) if not isinstance(opt, dict) else str(list(opt.values())[0])
                if opt_str.lower() in recommendation_text.lower():
                    selected_option = opt
                    break
            
            decision = {
                'selected': selected_option,
                'evaluation': sections.get('EVALUATION', ''),
                'comparison': sections.get('COMPARISON', ''),
                'recommendation': sections.get('RECOMMENDATION', ''),
                'alternatives': sections.get('ALTERNATIVES', ''),
                'risks': sections.get('RISKS', ''),
                'criteria': criteria,
                'options_evaluated': len(options),
            }
            
            # Store in memory
            working_memory.store(
                content=f"Decision made: {selected_option} based on criteria {list(criteria.keys())}",
                importance=0.8,
                tags=["decision", "evaluation", "choice"],
            )
            
            execution_time = int((time.time() - start_time) * 1000)
            
            return PrimitiveResult(
                content=decision,
                confidence=ConfidenceMetrics(
                    overall=0.85,
                    reasoning=0.9,
                    completeness=0.85,
                    consistency=0.85,
                    evidence_strength=0.8,
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
                    'options_count': len(options),
                    'criteria_count': len(criteria),
                    'model': 'gpt-4o-mini',
                }
            )
            
        except Exception as e:
            logger.error(f"Decision failed: {e}")
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
        options = kwargs.get('options', [])
        return ResourceEstimate(
            tokens=50 * len(options),
            time_ms=20 * len(options),
            memory_items=1,
            complexity=0.5,
        )
    
    def validate_inputs(self, **kwargs) -> None:
        """Validate inputs."""
        if "options" not in kwargs:
            raise ValueError("'options' parameter required")
        if "criteria" not in kwargs:
            raise ValueError("'criteria' parameter required")
    
    def matches_context(self, context: ExecutionContext, **kwargs) -> float:
        """Check context match."""
        if context.criticality > 0.6:
            return 0.85
        return 0.7
    
    def rollback(self, context: ExecutionContext) -> None:
        """Rollback decision."""
        pass


