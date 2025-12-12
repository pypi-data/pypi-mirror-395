"""
Decompose complex problems into manageable parts.
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


class DecomposeComposite(CompositePrimitive):
    """
    Decompose complex problems into manageable parts.
    
    Uses: perceive + think + evaluate
    """
    
    # Declare sub-primitives
    sub_primitives = ["perceive", "think", "evaluate"]
    
    def __init__(self):
        """Initialize primitive."""
        super().__init__()
        self._name = "decompose"
        self._hint = (
            "Use to break down complex problems into manageable parts. Best when "
            "problem is too large/complex to solve directly. Identifies sub-problems, "
            "dependencies, and decomposition strategy. Use for large tasks, complex "
            "systems, or hierarchical problems. Quality threshold >0.7 recommended."
        )
    
    def execute(
        self,
        context: ExecutionContext,
        working_memory: WorkingMemory,
        problem: str,
        **kwargs
    ) -> PrimitiveResult:
        """
        Decompose problem into manageable parts using LLM.
        
        Args:
            context: Execution context
            working_memory: Working memory
            problem: Problem to decompose
            **kwargs: Additional parameters (max_depth, strategy)
        
        Returns:
            PrimitiveResult with decomposition
        """
        start_time = time.time()
        
        try:
            # Retrieve relevant problem-solving context
            memory_items = working_memory.retrieve(
                query=f"decompose problem solving {problem[:50]}",
                top_k=3
            )
            memory_context = "\n".join([f"- {item.content}" for item in memory_items])
            
            # Extract parameters
            max_depth = kwargs.get('max_depth', 3)
            strategy = kwargs.get('strategy', 'hierarchical')
            
            # Build decomposition prompt
            prompt = f"""Decompose the following complex problem into manageable, solvable parts.

PROBLEM: {problem}

DECOMPOSITION STRATEGY: {strategy}
MAX DEPTH: {max_depth} levels

CONTEXT FROM MEMORY:
{memory_context if memory_context else "No prior context"}

Provide a systematic decomposition with:

1. OVERVIEW: Brief analysis of the problem's complexity and structure
2. MAIN COMPONENTS: Identify 3-7 major parts (with clear labels)
3. SUB-COMPONENTS: Break down complex parts further (if needed)
4. DEPENDENCIES: Identify which parts depend on others
5. EXECUTION ORDER: Suggest optimal sequence to solve parts

Format each component as:
- Component Name: Description
- Complexity: [low/medium/high]
- Dependencies: [list of other components]

Be specific and actionable in your decomposition."""

            # Get LLM decomposition
            llm_manager = get_llm_manager()
            response = llm_manager.request(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
            )
            
            decomposition_text = response.content
            
            # Parse sections
            sections = {}
            section_names = ["OVERVIEW:", "MAIN COMPONENTS:", "SUB-COMPONENTS:", "DEPENDENCIES:", "EXECUTION ORDER:"]
            for i, section_name in enumerate(section_names):
                start_idx = decomposition_text.find(section_name)
                if start_idx == -1:
                    sections[section_name.rstrip(':')] = ""
                    continue
                
                end_idx = len(decomposition_text)
                for next_section in section_names[i+1:]:
                    next_idx = decomposition_text.find(next_section)
                    if next_idx != -1:
                        end_idx = next_idx
                        break
                
                sections[section_name.rstrip(':')] = decomposition_text[start_idx+len(section_name):end_idx].strip()
            
            # Parse main components
            components = []
            main_components_text = sections.get('MAIN COMPONENTS', '')
            if main_components_text:
                lines = main_components_text.split('\n')
                current_component = None
                
                for line in lines:
                    line = line.strip()
                    if line.startswith('-') and ':' in line:
                        if current_component:
                            components.append(current_component)
                        
                        parts = line[1:].split(':', 1)
                        current_component = {
                            'name': parts[0].strip(),
                            'description': parts[1].strip() if len(parts) > 1 else '',
                            'complexity': 'medium',
                            'dependencies': [],
                        }
                    elif current_component and 'complexity:' in line.lower():
                        complexity = line.split(':', 1)[1].strip().lower()
                        current_component['complexity'] = complexity
                    elif current_component and 'dependencies:' in line.lower():
                        deps = line.split(':', 1)[1].strip()
                        if deps and deps.lower() != 'none':
                            current_component['dependencies'] = [d.strip() for d in deps.split(',')]
                
                if current_component:
                    components.append(current_component)
            
            result = {
                'problem': problem,
                'overview': sections.get('OVERVIEW', ''),
                'components': components,
                'sub_components': sections.get('SUB-COMPONENTS', ''),
                'dependencies': sections.get('DEPENDENCIES', ''),
                'execution_order': sections.get('EXECUTION ORDER', ''),
                'strategy': strategy,
                'total_parts': len(components),
            }
            
            # Store in memory
            working_memory.store(
                content=f"Decomposed '{problem}' into {len(components)} components using {strategy} strategy",
                importance=0.8,
                tags=["decomposition", "problem-solving", strategy],
            )
            
            execution_time = int((time.time() - start_time) * 1000)
            
            return PrimitiveResult(
                content=result,
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
                    'parts': len(components),
                    'strategy': strategy,
                    'model': 'gpt-4o-mini',
                }
            )
            
        except Exception as e:
            logger.error(f"Decomposition failed: {e}")
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
        problem = kwargs.get('problem', '')
        complexity = len(problem) / 100
        return ResourceEstimate(
            tokens=0,
            time_ms=int(15 + 5 * complexity),
            memory_items=1,
            complexity=0.4 + 0.1 * complexity,
        )
    
    def validate_inputs(self, **kwargs) -> None:
        """Validate inputs."""
        if "problem" not in kwargs:
            raise ValueError("'problem' parameter required")
    
    def matches_context(self, context: ExecutionContext, **kwargs) -> float:
        """Check context match."""
        if context.quality_threshold > 0.7:
            return 0.9
        return 0.75
    
    def rollback(self, context: ExecutionContext) -> None:
        """Rollback decomposition."""
        pass


