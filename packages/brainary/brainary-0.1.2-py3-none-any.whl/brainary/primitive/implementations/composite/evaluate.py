"""
Evaluate quality against criteria.
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


class EvaluateComposite(CompositePrimitive):
    """
    Evaluate quality against criteria.
    
    Uses: perceive + think + remember
    """
    
    # Declare sub-primitives
    sub_primitives = ["perceive", "think", "remember"]
    
    def __init__(self):
        """Initialize primitive."""
        super().__init__()
        self._name = "evaluate"
        self._hint = (
            "Use to assess quality against criteria. Best when objective assessment "
            "needed or comparing alternatives. Applies criteria, measures quality, "
            "provides scores and feedback. Use for quality control, selection, or "
            "validation. Suitable for all domains when evaluation matters."
        )
    
    def execute(
        self,
        context: ExecutionContext,
        working_memory: WorkingMemory,
        target: str,
        criteria: List[str],
        **kwargs
    ) -> PrimitiveResult:
        """
        Evaluate target against criteria using LLM.
        
        Args:
            context: Execution context
            working_memory: Working memory
            target: What to evaluate (text, solution, output, etc.)
            criteria: Evaluation criteria (list of strings)
            **kwargs: Additional parameters (scale, weights)
        
        Returns:
            PrimitiveResult with evaluation
        """
        start_time = time.time()
        
        try:
            # Retrieve relevant evaluation context
            memory_items = working_memory.retrieve(
                query=f"evaluate criteria {' '.join(criteria[:3])}",
                top_k=3
            )
            memory_context = "\n".join([f"- {item.content}" for item in memory_items])
            
            # Extract parameters
            scale = kwargs.get('scale', '1-10')
            weights = kwargs.get('weights', {})
            
            # Format criteria
            criteria_text = ""
            for i, criterion in enumerate(criteria, 1):
                weight = weights.get(criterion, 1.0)
                criteria_text += f"\n{i}. {criterion} (weight: {weight})"
            
            # Build evaluation prompt
            prompt = f"""Evaluate the following target against the given criteria.

TARGET TO EVALUATE:
{target}

EVALUATION CRITERIA:{criteria_text}

EVALUATION SCALE: {scale}

CONTEXT FROM MEMORY:
{memory_context if memory_context else "No prior evaluations"}

Provide a systematic evaluation with:

1. CRITERION SCORES: Score each criterion on the {scale} scale with justification
2. STRENGTHS: Identify specific strengths of the target
3. WEAKNESSES: Identify specific areas for improvement
4. OVERALL ASSESSMENT: Weighted overall score and summary
5. RECOMMENDATIONS: Actionable suggestions for improvement

Be objective and provide specific evidence for your scores."""

            # Get LLM evaluation
            llm_manager = get_llm_manager()
            response = llm_manager.request(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,  # Low temperature for objective evaluation
            )
            
            evaluation_text = response.content
            
            # Parse sections
            sections = {}
            section_names = ["CRITERION SCORES:", "STRENGTHS:", "WEAKNESSES:", "OVERALL ASSESSMENT:", "RECOMMENDATIONS:"]
            for i, section_name in enumerate(section_names):
                start_idx = evaluation_text.find(section_name)
                if start_idx == -1:
                    sections[section_name.rstrip(':')] = ""
                    continue
                
                end_idx = len(evaluation_text)
                for next_section in section_names[i+1:]:
                    next_idx = evaluation_text.find(next_section)
                    if next_idx != -1:
                        end_idx = next_idx
                        break
                
                sections[section_name.rstrip(':')] = evaluation_text[start_idx+len(section_name):end_idx].strip()
            
            # Extract overall score
            overall_text = sections.get('OVERALL ASSESSMENT', '')
            overall_score = 0.75  # Default
            
            # Try to extract numeric score
            import re
            score_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:/\s*10)?', overall_text)
            if score_match:
                score_val = float(score_match.group(1))
                if score_val <= 1.0:
                    overall_score = score_val
                elif score_val <= 10.0:
                    overall_score = score_val / 10.0
            
            result = {
                'target': target[:200] if len(target) > 200 else target,
                'criteria': criteria,
                'criterion_scores': sections.get('CRITERION SCORES', ''),
                'strengths': sections.get('STRENGTHS', ''),
                'weaknesses': sections.get('WEAKNESSES', ''),
                'overall_assessment': sections.get('OVERALL ASSESSMENT', ''),
                'recommendations': sections.get('RECOMMENDATIONS', ''),
                'overall_score': overall_score,
                'passed': overall_score >= 0.7,
                'scale': scale,
            }
            
            # Store in memory
            working_memory.store(
                content=f"Evaluated against {len(criteria)} criteria: score {overall_score:.2f}",
                importance=0.75,
                tags=["evaluation", "assessment", "quality"],
            )
            
            execution_time = int((time.time() - start_time) * 1000)
            
            return PrimitiveResult(
                content=result,
                confidence=ConfidenceMetrics(
                    overall=0.9,
                    reasoning=0.92,
                    completeness=0.88,
                    consistency=0.9,
                    evidence_strength=0.88,
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
                    'criteria_count': len(criteria),
                    'overall_score': overall_score,
                    'model': 'gpt-4o-mini',
                }
            )
            
        except Exception as e:
            logger.error(f"Evaluation failed: {e}")
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
        criteria = kwargs.get('criteria', [])
        return ResourceEstimate(
            tokens=0,
            time_ms=int(10 + 2 * len(criteria)),
            memory_items=1,
            complexity=0.3 + 0.05 * len(criteria),
        )
    
    def validate_inputs(self, **kwargs) -> None:
        """Validate inputs."""
        if "target" not in kwargs:
            raise ValueError("'target' parameter required")
        if "criteria" not in kwargs:
            raise ValueError("'criteria' parameter required")
    
    def matches_context(self, context: ExecutionContext, **kwargs) -> float:
        """Check context match."""
        return 0.85
    
    def rollback(self, context: ExecutionContext) -> None:
        """Rollback evaluation."""
        pass


