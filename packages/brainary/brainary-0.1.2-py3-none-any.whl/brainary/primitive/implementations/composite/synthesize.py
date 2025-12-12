"""
Synthesize information into coherent wholes.
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


class SynthesizeComposite(CompositePrimitive):
    """
    Synthesize information into coherent wholes.
    
    Uses: think + evaluate + verify
    """
    
    # Declare sub-primitives
    sub_primitives = ["think", "evaluate", "verify"]
    
    def __init__(self):
        """Initialize primitive."""
        super().__init__()
        self._name = "synthesize"
        self._hint = (
            "Use to combine information into coherent wholes. Best when multiple "
            "pieces need integration or when creating unified understanding. "
            "Identifies connections, resolves conflicts, creates coherent output. "
            "Use for summaries, integration, or combining diverse information. "
            "Quality threshold >0.7 recommended."
        )
    
    def execute(
        self,
        context: ExecutionContext,
        working_memory: WorkingMemory,
        parts: List[str],
        **kwargs
    ) -> PrimitiveResult:
        """
        Synthesize parts into coherent whole using LLM.
        
        Args:
            context: Execution context
            working_memory: Working memory
            parts: Parts to synthesize (list of strings or concepts)
            **kwargs: Additional parameters (style, focus)
        
        Returns:
            PrimitiveResult with synthesis
        """
        start_time = time.time()
        
        try:
            if not parts:
                raise ValueError("At least one part required")
            
            # Retrieve relevant synthesis context
            memory_items = working_memory.retrieve(
                query=f"synthesize integrate {' '.join(parts[:2])}",
                top_k=3
            )
            memory_context = "\n".join([f"- {item.content}" for item in memory_items])
            
            # Extract parameters
            style = kwargs.get('style', 'comprehensive')
            focus = kwargs.get('focus', 'integration')
            
            # Format parts
            parts_text = ""
            for i, part in enumerate(parts, 1):
                parts_text += f"\n{i}. {part}"
            
            # Build synthesis prompt
            prompt = f"""Synthesize the following parts into a coherent, unified whole.

PARTS TO SYNTHESIZE:{parts_text}

SYNTHESIS STYLE: {style}
FOCUS: {focus}

CONTEXT FROM MEMORY:
{memory_context if memory_context else "No prior context"}

Provide a comprehensive synthesis with:

1. UNIFIED NARRATIVE: Integrate all parts into a coherent whole
2. KEY CONNECTIONS: Identify relationships and links between parts
3. COMMON THEMES: Extract overarching themes and patterns
4. CONFLICTS RESOLVED: Address any contradictions or tensions
5. EMERGENT INSIGHTS: Identify insights that emerge from synthesis

Create a synthesis that is greater than the sum of its parts."""

            # Get LLM synthesis
            llm_manager = get_llm_manager()
            response = llm_manager.request(
                model="gpt-4o",  # Use powerful model for synthesis
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
            )
            
            synthesis_text = response.content
            
            # Parse sections
            sections = {}
            section_names = ["UNIFIED NARRATIVE:", "KEY CONNECTIONS:", "COMMON THEMES:", "CONFLICTS RESOLVED:", "EMERGENT INSIGHTS:"]
            for i, section_name in enumerate(section_names):
                start_idx = synthesis_text.find(section_name)
                if start_idx == -1:
                    sections[section_name.rstrip(':')] = ""
                    continue
                
                end_idx = len(synthesis_text)
                for next_section in section_names[i+1:]:
                    next_idx = synthesis_text.find(next_section)
                    if next_idx != -1:
                        end_idx = next_idx
                        break
                
                sections[section_name.rstrip(':')] = synthesis_text[start_idx+len(section_name):end_idx].strip()
            
            result = {
                'parts': parts,
                'parts_count': len(parts),
                'unified_narrative': sections.get('UNIFIED NARRATIVE', ''),
                'connections': sections.get('KEY CONNECTIONS', ''),
                'themes': sections.get('COMMON THEMES', ''),
                'conflicts_resolved': sections.get('CONFLICTS RESOLVED', ''),
                'emergent_insights': sections.get('EMERGENT INSIGHTS', ''),
                'style': style,
                'focus': focus,
            }
            
            # Store in memory
            working_memory.store(
                content=f"Synthesized {len(parts)} parts focusing on {focus}",
                importance=0.8,
                tags=["synthesis", "integration", focus],
            )
            
            execution_time = int((time.time() - start_time) * 1000)
            
            return PrimitiveResult(
                content=result,
                confidence=ConfidenceMetrics(
                    overall=0.88,
                    reasoning=0.9,
                    completeness=0.85,
                    consistency=0.9,
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
                    'parts': len(parts),
                    'style': style,
                    'model': 'gpt-4o',
                }
            )
            
        except Exception as e:
            logger.error(f"Synthesis failed: {e}")
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
        parts = kwargs.get('parts', [])
        return ResourceEstimate(
            tokens=0,
            time_ms=int(12 + 3 * len(parts)),
            memory_items=1,
            complexity=0.4 + 0.05 * len(parts),
        )
    
    def validate_inputs(self, **kwargs) -> None:
        """Validate inputs."""
        if "parts" not in kwargs:
            raise ValueError("'parts' parameter required")
        if not kwargs["parts"]:
            raise ValueError("At least one part required")
    
    def matches_context(self, context: ExecutionContext, **kwargs) -> float:
        """Check context match."""
        if context.quality_threshold > 0.7:
            return 0.9
        return 0.75
    
    def rollback(self, context: ExecutionContext) -> None:
        """Rollback synthesis."""
        pass


