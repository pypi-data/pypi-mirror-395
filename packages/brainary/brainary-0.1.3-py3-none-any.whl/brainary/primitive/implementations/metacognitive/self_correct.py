"""
Self-correct: detect_error + adjust_strategy + retry.
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


class SelfCorrectMetacognitive(MetacognitivePrimitive):
    """
    Self-correct: detect_error + adjust_strategy + retry.
    
    Detects errors and adjusts approach for correction.
    """
    
    def __init__(self):
        """Initialize primitive."""
        super().__init__()
        self._name = "self_correct"
        self._hint = (
            "Use for error detection and strategy adjustment. Best when mistakes "
            "are detected, results don't meet expectations, or validation fails. "
            "Analyzes errors, identifies root causes, adjusts strategy, and retries. "
            "Essential when criticality >0.7 or quality_threshold >0.8. Enables "
            "learning from mistakes and adaptive behavior. Use after failures or "
            "when self-assessment reveals issues."
        )
    
    def execute(
        self,
        context: ExecutionContext,
        working_memory: WorkingMemory,
        error: str,
        previous_strategy: str,
        **kwargs
    ) -> PrimitiveResult:
        """
        Self-correct error using LLM-powered root cause analysis.
        
        Args:
            context: Execution context
            working_memory: Working memory
            error: Error description or failure message
            previous_strategy: Strategy that failed
            **kwargs: Additional parameters (context_info, attempted_solution)
        
        Returns:
            PrimitiveResult with correction strategy
        """
        start_time = time.time()
        
        try:
            # Retrieve error correction history
            memory_items = working_memory.retrieve(
                query=f"error correction {error[:50]}",
                top_k=3
            )
            memory_context = "\n".join([f"- {item.content}" for item in memory_items])
            
            # Extract additional context
            context_info = kwargs.get('context_info', '')
            attempted_solution = kwargs.get('attempted_solution', '')
            
            # Format context
            context_text = ""
            if context_info:
                context_text = f"\n\nCONTEXT:\n{context_info}"
            
            # Format attempted solution
            attempt_text = ""
            if attempted_solution:
                attempt_text = f"\n\nPREVIOUS ATTEMPT:\n{attempted_solution}"
            
            # Build self-correction prompt
            prompt = f"""Analyze the following error and provide a corrective strategy.

ERROR ENCOUNTERED:
{error}

STRATEGY THAT FAILED: {previous_strategy}{context_text}{attempt_text}

CORRECTION HISTORY:
{memory_context if memory_context else "No prior corrections for this type of error"}

Provide comprehensive error correction with:

1. ERROR CLASSIFICATION: Categorize the error type and severity
2. ROOT CAUSE ANALYSIS: Identify the underlying cause of the error
3. WHY STRATEGY FAILED: Explain specifically why the previous strategy didn't work
4. CORRECTIVE STRATEGY: Propose a new strategy to avoid this error
5. SPECIFIC ADJUSTMENTS: List concrete changes to make
6. RETRY RECOMMENDATION: Should we retry? If yes, what preconditions?
7. LEARNING: What can we learn to prevent similar errors in the future?

Be specific and actionable in your corrections."""

            # Get LLM correction analysis
            llm_manager = get_llm_manager()
            response = llm_manager.request(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )
            
            correction_text = response.content
            
            # Parse sections
            sections = {}
            section_names = ["ERROR CLASSIFICATION:", "ROOT CAUSE ANALYSIS:", "WHY STRATEGY FAILED:", 
                           "CORRECTIVE STRATEGY:", "SPECIFIC ADJUSTMENTS:", "RETRY RECOMMENDATION:", 
                           "LEARNING:"]
            for i, section_name in enumerate(section_names):
                start_idx = correction_text.find(section_name)
                if start_idx == -1:
                    sections[section_name.rstrip(':')] = ""
                    continue
                
                end_idx = len(correction_text)
                for next_section in section_names[i+1:]:
                    next_idx = correction_text.find(next_section)
                    if next_idx != -1:
                        end_idx = next_idx
                        break
                
                sections[section_name.rstrip(':')] = correction_text[start_idx+len(section_name):end_idx].strip()
            
            # Determine retry recommendation
            retry_text = sections.get('RETRY RECOMMENDATION', '').lower()
            retry_recommended = 'yes' in retry_text or 'should retry' in retry_text or 'recommend retry' in retry_text
            
            # Extract error classification
            classification_text = sections.get('ERROR CLASSIFICATION', '').lower()
            if 'critical' in classification_text or 'severe' in classification_text:
                severity = 'critical'
            elif 'moderate' in classification_text or 'medium' in classification_text:
                severity = 'moderate'
            else:
                severity = 'minor'
            
            correction = {
                'error': error,
                'error_classification': sections.get('ERROR CLASSIFICATION', ''),
                'severity': severity,
                'root_cause': sections.get('ROOT CAUSE ANALYSIS', ''),
                'why_failed': sections.get('WHY STRATEGY FAILED', ''),
                'previous_strategy': previous_strategy,
                'new_strategy': sections.get('CORRECTIVE STRATEGY', ''),
                'specific_adjustments': sections.get('SPECIFIC ADJUSTMENTS', ''),
                'retry_recommendation': sections.get('RETRY RECOMMENDATION', ''),
                'retry_recommended': retry_recommended,
                'learning': sections.get('LEARNING', ''),
            }
            
            # Store correction in memory
            working_memory.store(
                content=f"Self-corrected {severity} error: {previous_strategy} → new corrective strategy",
                importance=0.85,
                tags=["metacognition", "self-correction", "error-handling", severity],
            )
            
            execution_time = int((time.time() - start_time) * 1000)
            
            return PrimitiveResult(
                content=correction,
                confidence=ConfidenceMetrics(
                    overall=0.82,
                    reasoning=0.85,
                    completeness=0.82,
                    consistency=0.8,
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
                    'severity': severity,
                    'retry_recommended': retry_recommended,
                    'model': 'gpt-4o-mini',
                }
            )
            
        except Exception as e:
            logger.error(f"Self-correction failed: {e}")
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
            tokens=70,
            time_ms=30,
            memory_items=1,
            complexity=0.5,
        )
    
    def validate_inputs(self, **kwargs) -> None:
        """Validate inputs."""
        if "error" not in kwargs:
            raise ValueError("'error' parameter required")
        if "previous_strategy" not in kwargs:
            raise ValueError("'previous_strategy' parameter required")
    
    def matches_context(self, context: ExecutionContext, **kwargs) -> float:
        """Check context match."""
        if context.criticality > 0.7:
            return 0.95
        return 0.8
    
    def rollback(self, context: ExecutionContext) -> None:
        """Rollback self-correction."""
        pass


