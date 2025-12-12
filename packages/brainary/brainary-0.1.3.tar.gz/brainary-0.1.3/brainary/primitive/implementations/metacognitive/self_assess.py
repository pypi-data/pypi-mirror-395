"""
Self-assess: evaluate(own_performance) + calibrate(confidence).
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


class SelfAssessMetacognitive(MetacognitivePrimitive):
    """
    Self-assess: evaluate(own_performance) + calibrate(confidence).
    
    Evaluates own performance and calibrates confidence.
    """
    
    def __init__(self):
        """Initialize primitive."""
        super().__init__()
        self._name = "self_assess"
        self._hint = (
            "Use for self-evaluation and confidence calibration. Best for "
            "assessing own performance, identifying weaknesses, and calibrating "
            "confidence scores. Use after completing tasks, before committing to "
            "decisions, or when quality assurance is critical. Essential when "
            "quality_threshold >0.8 or criticality >0.7. Helps prevent overconfidence "
            "and identify areas needing improvement."
        )
    
    def execute(
        self,
        context: ExecutionContext,
        working_memory: WorkingMemory,
        task: str,
        result: Any,
        criteria: Dict[str, float] = None,
        **kwargs
    ) -> PrimitiveResult:
        """
        Self-assess performance using LLM for objective analysis.
        
        Args:
            context: Execution context
            working_memory: Working memory
            task: Task that was performed
            result: Result to assess (string or dict)
            criteria: Assessment criteria with weights
            **kwargs: Additional parameters
        
        Returns:
            PrimitiveResult with self-assessment
        """
        start_time = time.time()
        
        try:
            criteria = criteria or {'accuracy': 1.0, 'completeness': 1.0, 'quality': 1.0}
            
            # Retrieve relevant assessment context
            memory_items = working_memory.retrieve(
                query=f"assessment performance {task[:50]}",
                top_k=3
            )
            memory_context = "\n".join([f"- {item.content}" for item in memory_items])
            
            # Format result
            result_text = str(result) if not isinstance(result, dict) else str(result)
            if len(result_text) > 500:
                result_text = result_text[:500] + "... (truncated)"
            
            # Format criteria
            criteria_text = "\n".join(
                f"- {criterion}: weight {weight:.2f}"
                for criterion, weight in criteria.items()
            )
            
            # Build self-assessment prompt
            prompt = f"""Perform an objective self-assessment of the following task performance.

TASK: {task}

RESULT PRODUCED:
{result_text}

ASSESSMENT CRITERIA:
{criteria_text}

PRIOR CONTEXT:
{memory_context if memory_context else "No prior assessment history"}

Provide a thorough self-assessment with:

1. PERFORMANCE SCORES: Score each criterion (0-100) with specific evidence
2. STRENGTHS: What was done well and why
3. WEAKNESSES: Areas that need improvement with specific examples
4. CONFIDENCE CALIBRATION: Is the initial confidence justified? Adjust if needed
5. IMPROVEMENT ACTIONS: Specific steps to improve future performance

Be honest, objective, and specific. Identify both what worked and what didn't."""

            # Get LLM self-assessment
            llm_manager = get_llm_manager()
            response = llm_manager.request(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )
            
            assessment_text = response.content
            
            # Parse sections
            sections = {}
            section_names = ["PERFORMANCE SCORES:", "STRENGTHS:", "WEAKNESSES:", 
                           "CONFIDENCE CALIBRATION:", "IMPROVEMENT ACTIONS:"]
            for i, section_name in enumerate(section_names):
                start_idx = assessment_text.find(section_name)
                if start_idx == -1:
                    sections[section_name.rstrip(':')] = ""
                    continue
                
                end_idx = len(assessment_text)
                for next_section in section_names[i+1:]:
                    next_idx = assessment_text.find(next_section)
                    if next_idx != -1:
                        end_idx = next_idx
                        break
                
                sections[section_name.rstrip(':')] = assessment_text[start_idx+len(section_name):end_idx].strip()
            
            # Extract scores
            import re
            scores = {}
            scores_text = sections.get('PERFORMANCE SCORES', '')
            for criterion in criteria.keys():
                pattern = rf'{criterion}[:\s]+(\d+)'
                match = re.search(pattern, scores_text, re.IGNORECASE)
                if match:
                    scores[criterion] = int(match.group(1)) / 100.0
                else:
                    scores[criterion] = 0.75  # Default
            
            # Calculate weighted overall score
            if criteria:
                overall_score = sum(scores[c] * criteria[c] for c in criteria.keys()) / sum(criteria.values())
            else:
                overall_score = sum(scores.values()) / len(scores) if scores else 0.75
            
            # Extract confidence calibration
            calibration_text = sections.get('CONFIDENCE CALIBRATION', '').lower()
            if 'overconfident' in calibration_text or 'too high' in calibration_text:
                calibrated_confidence = overall_score * 0.85
            elif 'underconfident' in calibration_text or 'too low' in calibration_text:
                calibrated_confidence = min(overall_score * 1.1, 0.95)
            else:
                calibrated_confidence = overall_score
            
            # Identify strengths and weaknesses
            strengths_text = sections.get('STRENGTHS', '')
            weaknesses_text = sections.get('WEAKNESSES', '')
            
            assessment = {
                'task': task,
                'scores': scores,
                'overall_score': overall_score,
                'uncalibrated_confidence': overall_score,
                'calibrated_confidence': calibrated_confidence,
                'strengths': strengths_text,
                'weaknesses': weaknesses_text,
                'improvement_actions': sections.get('IMPROVEMENT ACTIONS', ''),
                'confidence_calibration': sections.get('CONFIDENCE CALIBRATION', ''),
                'identified_weaknesses': [c for c, s in scores.items() if s < 0.7],
                'identified_strengths': [c for c, s in scores.items() if s >= 0.8],
            }
            
            # Store in memory
            working_memory.store(
                content=f"Self-assessment: {task} scored {overall_score:.2f}, confidence {calibrated_confidence:.2f}",
                importance=0.85,
                tags=["metacognition", "self-assessment", "performance"],
            )
            
            execution_time = int((time.time() - start_time) * 1000)
            
            return PrimitiveResult(
                content=assessment,
                confidence=ConfidenceMetrics(
                    overall=calibrated_confidence,
                    reasoning=0.88,
                    completeness=0.85,
                    consistency=0.88,
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
                    'overall_score': overall_score,
                    'calibrated_confidence': calibrated_confidence,
                    'criteria_count': len(criteria),
                    'model': 'gpt-4o-mini',
                }
            )
            
        except Exception as e:
            logger.error(f"Self-assessment failed: {e}")
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
        criteria = kwargs.get('criteria', {})
        return ResourceEstimate(
            tokens=80,
            time_ms=30,
            memory_items=1,
            complexity=0.5,
        )
    
    def validate_inputs(self, **kwargs) -> None:
        """Validate inputs."""
        if "task" not in kwargs:
            raise ValueError("'task' parameter required")
        if "result" not in kwargs:
            raise ValueError("'result' parameter required")
    
    def matches_context(self, context: ExecutionContext, **kwargs) -> float:
        """Check context match."""
        if context.quality_threshold > 0.8 or context.criticality > 0.7:
            return 0.95
        return 0.75
    
    def rollback(self, context: ExecutionContext) -> None:
        """Rollback self-assessment."""
        pass


