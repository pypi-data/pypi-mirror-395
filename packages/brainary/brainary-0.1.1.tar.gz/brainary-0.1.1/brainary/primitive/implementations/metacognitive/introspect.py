"""
Introspect: monitor(self) + analyze(internal_state) using LLM.
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


class IntrospectMetacognitive(MetacognitivePrimitive):
    """
    Introspect: monitor(self) + analyze(internal_state).
    
    Observes and analyzes internal cognitive state.
    """
    
    def __init__(self):
        """Initialize primitive."""
        super().__init__()
        self._name = "introspect"
        self._hint = (
            "Use for self-observation and internal state analysis. Best for "
            "understanding own cognitive processes, monitoring reasoning quality, "
            "and identifying mental patterns. Use when you need metacognitive "
            "awareness, debugging reasoning, or assessing internal state. "
            "Particularly useful with criticality >0.7 or when quality assessment "
            "is needed. Enables second-order thinking about thinking."
        )
    
    def execute(
        self,
        context: ExecutionContext,
        working_memory: WorkingMemory,
        aspect: str = "all",
        **kwargs
    ) -> PrimitiveResult:
        """
        Introspect on internal state using LLM for metacognitive analysis.
        
        Args:
            context: Execution context
            working_memory: Working memory
            aspect: Aspect to introspect (all, reasoning, memory, confidence, process)
            **kwargs: Additional parameters
        
        Returns:
            PrimitiveResult with deep introspection
        """
        start_time = time.time()
        
        try:
            llm_manager = get_llm_manager()
            
            # Gather internal state information
            memory_items = working_memory.get_all_items()
            recent_items = memory_items[-10:] if len(memory_items) > 10 else memory_items
            memory_summary = "\\n".join([f"- {item.content[:80]}..." for item in recent_items])
            
            memory_stats = {
                'total_items': len(working_memory),
                'capacity_used': len(working_memory) / 7.0,  # 7±2 capacity
                'recent_tags': list(set([tag for item in recent_items for tag in item.tags]))[:10],
            }
            
            context_info = {
                'execution_mode': context.execution_mode.value,
                'quality_threshold': context.quality_threshold,
                'criticality': context.criticality,
                'time_pressure': context.time_pressure,
                'token_usage': f"{context.token_usage}/{context.token_budget}",
                'depth': context.depth,
            }
            
            # Build introspection prompt
            prompt = f"""Perform metacognitive introspection - analyze the internal cognitive state.

ASPECT TO ANALYZE: {aspect}

CURRENT CONTEXT:
- Execution Mode: {context_info['execution_mode']}
- Quality Threshold: {context_info['quality_threshold']}
- Criticality: {context_info['criticality']}
- Time Pressure: {context_info['time_pressure']}
- Token Usage: {context_info['token_usage']}
- Processing Depth: {context_info['depth']}

WORKING MEMORY STATE:
- Items in memory: {memory_stats['total_items']}
- Capacity used: {memory_stats['capacity_used']:.1%}
- Recent topics: {', '.join(memory_stats['recent_tags'][:5])}

RECENT MEMORY CONTENTS:
{memory_summary}

Provide a metacognitive analysis with the following:

1. CURRENT STATE ASSESSMENT
   - Evaluate the cognitive state
   - Identify what's going well
   - Note any concerns or issues

2. REASONING QUALITY
   - Assess the quality of recent reasoning
   - Identify patterns in thinking
   - Rate reasoning effectiveness (0.0-1.0)

3. MEMORY UTILIZATION
   - Evaluate memory usage efficiency
   - Note information gaps if any
   - Assess organization and retrieval

4. CONFIDENCE CALIBRATION
   - Evaluate if confidence levels are well-calibrated
   - Identify areas of uncertainty
   - Rate calibration quality (0.0-1.0)

5. RECOMMENDATIONS
   - Suggest improvements or adjustments
   - Identify optimal strategies
   - Note any bottlenecks to address

Be analytical and honest in your assessment."""
            
            response = llm_manager.request(
                messages=[{"role": "user", "content": prompt}],
                model="gpt-4o-mini"
            )
            
            content = response.content.strip()
            
            # Parse introspection sections
            sections = {}
            current_section = None
            
            for line in content.split('\\n'):
                upper_line = line.upper()
                if any(h in upper_line for h in ['STATE ASSESSMENT', 'REASONING QUALITY', 'MEMORY UTILIZATION', 'CONFIDENCE CALIBRATION', 'RECOMMENDATIONS']):
                    for header in ['STATE', 'REASONING', 'MEMORY', 'CONFIDENCE', 'RECOMMENDATIONS']:
                        if header in upper_line:
                            current_section = header.lower()
                            sections[current_section] = []
                            break
                elif current_section and line.strip():
                    sections[current_section].append(line.strip())
            
            introspection = {
                'aspect': aspect,
                'current_state': '\\n'.join(sections.get('state', [])),
                'reasoning_quality': '\\n'.join(sections.get('reasoning', [])),
                'memory_utilization': '\\n'.join(sections.get('memory', [])),
                'confidence_calibration': '\\n'.join(sections.get('confidence', [])),
                'recommendations': '\\n'.join(sections.get('recommendations', [])),
                'full_analysis': content,
                'memory_stats': memory_stats,
                'context_info': context_info,
                'model': 'gpt-4o-mini',
            }
            
            working_memory.store(
                content=f"Introspection ({aspect}): {sections.get('recommendations', [''])[0][:100] if sections.get('recommendations') else 'completed'}",
                importance=0.75,
                tags=["metacognition", "introspection", aspect],
            )
            
            execution_time = int((time.time() - start_time) * 1000)
            
            return PrimitiveResult(
                content=introspection,
                confidence=ConfidenceMetrics(
                    overall=0.9,
                    reasoning=0.95,
                    completeness=0.9,
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
                    'aspect': aspect,
                    'memory_items': len(working_memory),
                    'model': 'gpt-4o-mini',
                }
            )
        
        except Exception as e:
            logger.error(f"IntrospectMetacognitive execution failed: {e}")
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
        return ResourceEstimate(
            tokens=50,
            time_ms=20,
            memory_items=1,
            complexity=0.4,
        )
    
    def validate_inputs(self, **kwargs) -> None:
        """Validate inputs."""
        aspect = kwargs.get('aspect', 'all')
        valid_aspects = ['all', 'reasoning', 'memory', 'confidence']
        if aspect not in valid_aspects:
            raise ValueError(f"aspect must be one of {valid_aspects}")
    
    def matches_context(self, context: ExecutionContext, **kwargs) -> float:
        """Check context match."""
        if context.criticality > 0.7:
            return 0.9
        return 0.7
    
    def rollback(self, context: ExecutionContext) -> None:
        """Rollback introspection."""
        pass


