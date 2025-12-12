"""
Solve: analyze + generate + test + refine using LLM.
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


class SolveComposite(CompositePrimitive):
    """
    Solve: analyze + generate + test + refine.
    
    Finds solutions to problems through iterative refinement.
    """
    
    def __init__(self):
        """Initialize primitive."""
        super().__init__()
        self._name = "solve"
        self.sub_primitives = ["analyze", "create", "evaluate", "adapt"]
        self._hint = (
            "Use for problem-solving through iterative refinement. Best for "
            "finding solutions to well-defined problems. Composes analyze + "
            "create + evaluate + adapt primitives. Use for mathematical problems, "
            "optimization tasks, constraint satisfaction, or any problem requiring "
            "solution generation and validation. Quality threshold >0.7 recommended."
        )
    
    def execute(
        self,
        context: ExecutionContext,
        working_memory: WorkingMemory,
        problem: str,
        constraints: List[str] = None,
        max_iterations: int = 3,
        **kwargs
    ) -> PrimitiveResult:
        """
        Solve problem using LLM with iterative refinement.
        
        Args:
            context: Execution context
            working_memory: Working memory
            problem: Problem to solve
            constraints: Problem constraints
            max_iterations: Maximum solution iterations
            **kwargs: Additional parameters
        
        Returns:
            PrimitiveResult with solution
        """
        start_time = time.time()
        
        try:
            llm_manager = get_llm_manager()
            constraints = constraints or []
            
            # Retrieve context
            mem_context = working_memory.retrieve(query=problem, top_k=5)
            context_str = "\n".join([m.content for m in mem_context]) if mem_context else "No prior context."
            
            # Build problem-solving prompt
            constraints_str = "\n".join([f"- {c}" for c in constraints]) if constraints else "None specified"
            
            prompt = f"""Solve the following problem systematically.

Problem: {problem}

Constraints:
{constraints_str}

Context from memory:
{context_str}

Provide a comprehensive solution with the following structure:

1. PROBLEM ANALYSIS
   - Restate the problem clearly
   - Identify key components
   - Note any constraints

2. SOLUTION APPROACH
   - Describe your solution strategy
   - Explain key steps

3. DETAILED SOLUTION
   - Provide the complete solution
   - Show work/reasoning if applicable

4. VALIDATION
   - Verify the solution meets all constraints
   - Test edge cases if relevant
   - Assess confidence level (0.0-1.0)

5. ALTERNATIVE APPROACHES
   - Mention 1-2 alternative solutions if applicable"""
            
            response = llm_manager.request(
                messages=[{"role": "user", "content": prompt}],
                model="gpt-4o"
            )
            
            content = response.content.strip()
            
            # Parse structured response
            sections = {}
            current_section = None
            for line in content.split('\n'):
                upper_line = line.upper()
                if any(h in upper_line for h in ['PROBLEM ANALYSIS', 'SOLUTION APPROACH', 'DETAILED SOLUTION', 'VALIDATION', 'ALTERNATIVE']):
                    for header in ['ANALYSIS', 'APPROACH', 'SOLUTION', 'VALIDATION', 'ALTERNATIVE']:
                        if header in upper_line:
                            current_section = header.lower()
                            sections[current_section] = []
                            break
                elif current_section and line.strip():
                    sections[current_section].append(line.strip())
            
            solution = {
                'problem': problem,
                'analysis': '\n'.join(sections.get('analysis', [])),
                'approach': '\n'.join(sections.get('approach', [])),
                'solution': '\n'.join(sections.get('solution', [])),
                'validation': '\n'.join(sections.get('validation', [])),
                'alternatives': '\n'.join(sections.get('alternative', [])),
                'full_solution': content,
                'constraints': constraints,
                'iterations': 1,
                'model': 'gpt-4o',
            }
            
            working_memory.store(
                content=f"Solved: {problem[:50]}... - {sections.get('solution', [''])[0][:100] if sections.get('solution') else 'completed'}",
                importance=0.85,
                tags=["solution", "problem-solving", "llm"],
            )
            
            execution_time = int((time.time() - start_time) * 1000)
            
            return PrimitiveResult(
                content=solution,
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
                    'iterations': 1,
                    'model': 'gpt-4o',
                    'constraints_count': len(constraints),
                }
            )
        
        except Exception as e:
            logger.error(f"SolveComposite execution failed: {e}")
            execution_time = int((time.time() - start_time) * 1000)
            
            return PrimitiveResult(
                content=None,
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
        max_iterations = kwargs.get('max_iterations', 3)
        return ResourceEstimate(
            tokens=200 * max_iterations,
            time_ms=100 * max_iterations,
            memory_items=1,
            complexity=0.7,
        )
    
    def validate_inputs(self, **kwargs) -> None:
        """Validate inputs."""
        if "problem" not in kwargs:
            raise ValueError("'problem' parameter required")
    
    def matches_context(self, context: ExecutionContext, **kwargs) -> float:
        """Check context match."""
        if context.quality_threshold > 0.7:
            return 0.85
        return 0.65
    
    def rollback(self, context: ExecutionContext) -> None:
        """Rollback solution."""
        pass


