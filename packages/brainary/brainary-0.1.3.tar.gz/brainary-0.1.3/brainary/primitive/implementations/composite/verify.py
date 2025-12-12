"""
Verify correctness and validity.
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


class VerifyComposite(CompositePrimitive):
    """
    Verify correctness and validity.
    
    Uses: think + evaluate + recall
    """
    
    # Declare sub-primitives
    sub_primitives = ["think", "evaluate", "recall"]
    
    def __init__(self):
        """Initialize primitive."""
        super().__init__()
        self._name = "verify"
        self._hint = (
            "Use to check correctness and validity. Best when accuracy critical "
            "or validation needed. Checks logic, consistency, and constraints. "
            "Use for validation, testing, or quality assurance. Quality threshold "
            ">0.8 recommended. Suitable for all domains when correctness matters."
        )
    
    def execute(
        self,
        context: ExecutionContext,
        working_memory: WorkingMemory,
        target: str,
        constraints: List[str],
        **kwargs
    ) -> PrimitiveResult:
        """
        Verify target against constraints using LLM.
        
        Args:
            context: Execution context
            working_memory: Working memory
            target: What to verify (solution, output, answer, etc.)
            constraints: Constraints to check (list of requirements)
            **kwargs: Additional parameters (strict_mode)
        
        Returns:
            PrimitiveResult with verification
        """
        start_time = time.time()
        
        try:
            # Retrieve relevant verification context
            memory_items = working_memory.retrieve(
                query=f"verify constraints validation {target[:50]}",
                top_k=3
            )
            memory_context = "\n".join([f"- {item.content}" for item in memory_items])
            
            # Extract parameters
            strict_mode = kwargs.get('strict_mode', False)
            
            # Format constraints
            constraints_text = ""
            for i, constraint in enumerate(constraints, 1):
                constraints_text += f"\n{i}. {constraint}"
            
            # Build verification prompt
            prompt = f"""Verify the following target against the given constraints.

TARGET TO VERIFY:
{target}

CONSTRAINTS TO CHECK:{constraints_text}

VERIFICATION MODE: {"Strict (all must pass)" if strict_mode else "Standard"}

CONTEXT FROM MEMORY:
{memory_context if memory_context else "No prior verifications"}

Provide a systematic verification with:

1. CONSTRAINT CHECKS: For each constraint, determine if PASSED or FAILED with evidence
2. LOGIC VERIFICATION: Check internal consistency and logical soundness
3. EDGE CASES: Identify potential edge cases or failure modes
4. ISSUES FOUND: List any violations, errors, or concerns
5. VERDICT: Overall pass/fail determination with confidence level

Be thorough and provide specific evidence for each check."""

            # Get LLM verification
            llm_manager = get_llm_manager()
            response = llm_manager.request(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,  # Very low temperature for precise verification
            )
            
            verification_text = response.content
            
            # Parse sections
            sections = {}
            section_names = ["CONSTRAINT CHECKS:", "LOGIC VERIFICATION:", "EDGE CASES:", "ISSUES FOUND:", "VERDICT:"]
            for i, section_name in enumerate(section_names):
                start_idx = verification_text.find(section_name)
                if start_idx == -1:
                    sections[section_name.rstrip(':')] = ""
                    continue
                
                end_idx = len(verification_text)
                for next_section in section_names[i+1:]:
                    next_idx = verification_text.find(next_section)
                    if next_idx != -1:
                        end_idx = next_idx
                        break
                
                sections[section_name.rstrip(':')] = verification_text[start_idx+len(section_name):end_idx].strip()
            
            # Determine pass/fail
            verdict_text = sections.get('VERDICT', '').lower()
            passed = 'pass' in verdict_text and 'fail' not in verdict_text.replace('pass', '')
            
            # Extract confidence
            confidence = 0.95 if passed else 0.6
            import re
            conf_match = re.search(r'confidence[:\s]+(\d+)%', verdict_text)
            if conf_match:
                confidence = int(conf_match.group(1)) / 100.0
            
            # Parse individual constraint checks
            checks = []
            constraint_checks_text = sections.get('CONSTRAINT CHECKS', '')
            for constraint in constraints:
                check_passed = True
                check_message = "OK"
                
                # Look for PASSED or FAILED in the constraint section
                if constraint.lower() in constraint_checks_text.lower():
                    relevant_section = constraint_checks_text.lower()
                    if 'failed' in relevant_section or 'violation' in relevant_section:
                        check_passed = False
                        check_message = "Failed verification"
                
                checks.append({
                    'constraint': constraint,
                    'passed': check_passed,
                    'message': check_message,
                })
            
            result = {
                'target': target[:200] if len(target) > 200 else target,
                'constraints': constraints,
                'checks': checks,
                'constraint_checks': sections.get('CONSTRAINT CHECKS', ''),
                'logic_verification': sections.get('LOGIC VERIFICATION', ''),
                'edge_cases': sections.get('EDGE CASES', ''),
                'issues_found': sections.get('ISSUES FOUND', ''),
                'verdict': sections.get('VERDICT', ''),
                'passed': passed,
                'verified': passed,
                'confidence': confidence,
                'strict_mode': strict_mode,
            }
            
            # Store in memory
            working_memory.store(
                content=f"Verified: {'PASSED' if passed else 'FAILED'} ({len(constraints)} constraints, confidence {confidence:.2f})",
                importance=0.85,
                tags=["verification", "validation", "passed" if passed else "failed"],
            )
            
            execution_time = int((time.time() - start_time) * 1000)
            
            return PrimitiveResult(
                content=result,
                confidence=ConfidenceMetrics(
                    overall=confidence,
                    reasoning=0.92,
                    completeness=0.9,
                    consistency=0.95,
                    evidence_strength=0.9,
                ),
                execution_mode=context.execution_mode,
                cost=CostMetrics(
                    tokens=response.usage.total_tokens,
                    latency_ms=execution_time,
                    memory_slots=1,
                    provider_cost_usd=response.cost,
                ),
                primitive_name=self.name,
                success=passed,
                metadata={
                    'constraints_count': len(constraints),
                    'passed': passed,
                    'strict_mode': strict_mode,
                    'model': 'gpt-4o-mini',
                }
            )
            
        except Exception as e:
            logger.error(f"Verification failed: {e}")
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
        constraints = kwargs.get('constraints', [])
        return ResourceEstimate(
            tokens=0,
            time_ms=int(8 + 2 * len(constraints)),
            memory_items=1,
            complexity=0.35 + 0.05 * len(constraints),
        )
    
    def validate_inputs(self, **kwargs) -> None:
        """Validate inputs."""
        if "target" not in kwargs:
            raise ValueError("'target' parameter required")
        if "constraints" not in kwargs:
            raise ValueError("'constraints' parameter required")
    
    def matches_context(self, context: ExecutionContext, **kwargs) -> float:
        """Check context match."""
        if context.quality_threshold > 0.8:
            return 0.95
        return 0.8
    
    def rollback(self, context: ExecutionContext) -> None:
        """Rollback verification."""
        pass


