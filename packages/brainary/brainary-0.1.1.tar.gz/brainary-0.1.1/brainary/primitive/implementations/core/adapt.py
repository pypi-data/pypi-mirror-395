"""
Modify approach or strategy based on feedback.
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


class AdaptStrategy(CorePrimitive):
    """
    Modify approach or strategy based on feedback.
    
    Enables adaptive behavior and dynamic strategy adjustment.
    """
    
    def __init__(self):
        """Initialize primitive."""
        super().__init__()
        self._name = "adapt"
        self._hint = (
            "Use to modify approach or strategy based on feedback or changing conditions. "
            "Best for adaptive behavior, strategy refinement, and dynamic adjustment. "
            "Suitable for all domains. Use when initial approach isn't working, "
            "environment changes, or feedback indicates need for adjustment. "
            "Enables learning and optimization during execution. Most effective "
            "when criticality is high (>0.7) or when feedback indicates poor performance."
        )
    
    def execute(
        self,
        context: ExecutionContext,
        working_memory: WorkingMemory,
        current_strategy: str,
        feedback: Dict[str, Any],
        constraints: List[str] = None,
        **kwargs
    ) -> PrimitiveResult:
        """
        Adapt strategy using LLM-powered feedback analysis.
        
        Args:
            context: Execution context
            working_memory: Working memory
            current_strategy: Current approach/strategy
            feedback: Feedback on current strategy performance
            constraints: Constraints for new strategy
            **kwargs: Additional parameters (goals, environment_changes)
        
        Returns:
            PrimitiveResult with adapted strategy
        """
        start_time = time.time()
        
        try:
            constraints = constraints or []
            
            # Retrieve adaptation history from memory
            memory_items = working_memory.retrieve(
                query=f"adapt strategy {current_strategy}",
                top_k=4
            )
            memory_context = "\n".join([f"- {item.content}" for item in memory_items])
            
            # Extract feedback components
            success_indicators = feedback.get('success', 0.0)
            issues = feedback.get('issues', [])
            observations = feedback.get('observations', '')
            metrics = feedback.get('metrics', {})
            
            # Extract additional context
            goals = kwargs.get('goals', [])
            environment_changes = kwargs.get('environment_changes', [])
            
            # Format feedback
            feedback_text = f"""
Success Score: {success_indicators:.2f} (0.0 = complete failure, 1.0 = complete success)

Issues Encountered:
{chr(10).join(f'- {issue}' for issue in issues) if issues else '- No specific issues reported'}

Observations:
{observations if observations else 'No additional observations'}

Performance Metrics:
{chr(10).join(f'- {k}: {v}' for k, v in metrics.items()) if metrics else '- No metrics provided'}
"""
            
            # Format constraints
            constraints_text = ""
            if constraints:
                constraints_text = "\n\nCONSTRAINTS FOR NEW STRATEGY:\n" + "\n".join(f"- {c}" for c in constraints)
            
            # Format goals
            goals_text = ""
            if goals:
                goals_text = "\n\nGOALS:\n" + "\n".join(f"- {g}" for g in goals)
            
            # Format environment changes
            env_text = ""
            if environment_changes:
                env_text = "\n\nENVIRONMENT CHANGES:\n" + "\n".join(f"- {e}" for e in environment_changes)
            
            # Build adaptation prompt
            prompt = f"""Analyze feedback and adapt the current strategy to improve performance.

CURRENT STRATEGY: {current_strategy}

FEEDBACK:{feedback_text}{goals_text}{env_text}{constraints_text}

ADAPTATION HISTORY:
{memory_context if memory_context else "No prior adaptations"}

Provide comprehensive strategy adaptation with:

1. FEEDBACK ANALYSIS: Analyze what worked and what didn't
2. ROOT CAUSES: Identify root causes of issues or suboptimal performance  
3. ADAPTATION TYPE: Classify as fine-tuning, minor adjustment, major change, or complete pivot
4. NEW STRATEGY: Describe the adapted strategy in detail
5. KEY CHANGES: List specific changes from current to new strategy
6. EXPECTED IMPROVEMENTS: Explain how changes address the identified issues
7. IMPLEMENTATION GUIDANCE: Provide guidance on implementing the new strategy

Be specific about what to change and why."""

            # Get LLM adaptation analysis
            llm_manager = get_llm_manager()
            response = llm_manager.request(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
            )
            
            adaptation_text = response.content
            
            # Parse sections
            sections = {}
            section_names = ["FEEDBACK ANALYSIS:", "ROOT CAUSES:", "ADAPTATION TYPE:", 
                           "NEW STRATEGY:", "KEY CHANGES:", "EXPECTED IMPROVEMENTS:", 
                           "IMPLEMENTATION GUIDANCE:"]
            for i, section_name in enumerate(section_names):
                start_idx = adaptation_text.find(section_name)
                if start_idx == -1:
                    sections[section_name.rstrip(':')] = ""
                    continue
                
                end_idx = len(adaptation_text)
                for next_section in section_names[i+1:]:
                    next_idx = adaptation_text.find(next_section)
                    if next_idx != -1:
                        end_idx = next_idx
                        break
                
                sections[section_name.rstrip(':')] = adaptation_text[start_idx+len(section_name):end_idx].strip()
            
            # Determine adaptation type
            adaptation_type_text = sections.get('ADAPTATION TYPE', '').lower()
            if 'pivot' in adaptation_type_text or 'complete' in adaptation_type_text:
                adaptation_type = 'complete_pivot'
            elif 'major' in adaptation_type_text:
                adaptation_type = 'major_change'
            elif 'minor' in adaptation_type_text or 'adjustment' in adaptation_type_text:
                adaptation_type = 'minor_adjustment'
            else:
                adaptation_type = 'fine_tuning'
            
            result_content = {
                'old_strategy': current_strategy,
                'new_strategy': sections.get('NEW STRATEGY', ''),
                'adaptation_type': adaptation_type,
                'feedback_analysis': sections.get('FEEDBACK ANALYSIS', ''),
                'root_causes': sections.get('ROOT CAUSES', ''),
                'key_changes': sections.get('KEY CHANGES', ''),
                'expected_improvements': sections.get('EXPECTED IMPROVEMENTS', ''),
                'implementation_guidance': sections.get('IMPLEMENTATION GUIDANCE', ''),
                'success_score': success_indicators,
                'issues_count': len(issues),
                'constraints_applied': constraints,
            }
            
            # Store adaptation in memory
            working_memory.store(
                content=f"Adapted strategy ({adaptation_type}): {current_strategy} → new approach (success was {success_indicators:.1f})",
                importance=0.8,
                tags=["adaptation", "strategy", adaptation_type],
            )
            
            execution_time = int((time.time() - start_time) * 1000)
            
            return PrimitiveResult(
                content=result_content,
                confidence=ConfidenceMetrics(
                    overall=0.85,
                    reasoning=0.88,
                    completeness=0.85,
                    consistency=0.82,
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
                    'adaptation_type': adaptation_type,
                    'issues_addressed': len(issues),
                    'success_score': success_indicators,
                    'model': 'gpt-4o-mini',
                }
            )
            
        except Exception as e:
            logger.error(f"Strategy adaptation failed: {e}")
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
        return ResourceEstimate(
            tokens=0,
            time_ms=10,
            memory_items=1,
            complexity=0.4,
        )
    
    def validate_inputs(self, **kwargs) -> None:
        """Validate inputs for execution."""
        if "current_strategy" not in kwargs:
            raise ValueError("'current_strategy' parameter required")
        if "feedback" not in kwargs:
            raise ValueError("'feedback' parameter required")
    
    def matches_context(self, context: ExecutionContext, **kwargs) -> float:
        """Check context match."""
        # Better match when criticality is high
        if context.criticality > 0.7:
            return 0.9
        return 0.7
    
    def rollback(self, context: ExecutionContext) -> None:
        """Rollback - would need to revert to previous strategy."""
        pass

