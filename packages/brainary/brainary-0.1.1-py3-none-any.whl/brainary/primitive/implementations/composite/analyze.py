"""
Analyze: perceive + decompose + think + relate.
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


class AnalyzeComposite(CompositePrimitive):
    """
    Analyze: perceive + decompose + think + relate.
    
    Performs structured analysis of inputs.
    """
    
    def __init__(self):
        """Initialize primitive."""
        super().__init__()
        self._name = "analyze"
        self.sub_primitives = ["perceive", "decompose", "think", "associate"]
        self._hint = (
            "Use for structured analysis of complex inputs. Best when you need "
            "to break down and examine components, identify relationships, and "
            "extract insights. Suitable for all domains. Composes perceive + "
            "decompose + think + associate primitives. Use for data analysis, "
            "problem examination, system understanding, or investigative tasks. "
            "Quality threshold >0.6 recommended."
        )
    
    def execute(
        self,
        context: ExecutionContext,
        working_memory: WorkingMemory,
        subject: Any,
        focus: str = "general",
        depth: int = 2,
        **kwargs
    ) -> PrimitiveResult:
        """
        Analyze subject using LLM with structured decomposition and reasoning.
        
        Args:
            context: Execution context
            working_memory: Working memory
            subject: Subject to analyze
            focus: Analysis focus (e.g., "technical", "business", "ethical")
            depth: Analysis depth (1=shallow, 2=moderate, 3=deep)
            **kwargs: Additional parameters
        
        Returns:
            PrimitiveResult with structured analysis
        """
        start_time = time.time()
        
        try:
            # Get LLM manager
            llm_manager = get_llm_manager()
            
            # Retrieve relevant context from memory
            mem_context = working_memory.retrieve(query=str(subject), top_k=5)
            context_str = "\n".join([m.content for m in mem_context]) if mem_context else "No prior context."
            
            # Build structured analysis prompt
            depth_instructions = {
                1: "Provide a concise analysis focusing on key points.",
                2: "Provide a thorough analysis with moderate detail.",
                3: "Provide an in-depth, comprehensive analysis with extensive detail."
            }
            
            prompt = f"""Perform a structured analysis of the following subject.

Subject: {subject}

Focus: {focus}
Analysis Depth: {depth_instructions.get(depth, depth_instructions[2])}

Context from memory:
{context_str}

Please provide a comprehensive analysis with the following structure:

1. OVERVIEW
   - Brief description of the subject
   - Key characteristics

2. COMPONENTS
   - Break down into {depth * 2} key components
   - Explain each component

3. RELATIONSHIPS
   - Identify {depth * 2} important relationships between components
   - Explain how they interact

4. INSIGHTS
   - Extract {depth * 2} key insights
   - Explain their significance

5. IMPLICATIONS
   - Discuss broader implications
   - Consider multiple perspectives

Format your response clearly with headers and bullet points."""
            
            # Choose model based on depth
            model = "gpt-4o" if depth >= 3 else "gpt-4o-mini"
            
            response = llm_manager.request(
                messages=[{"role": "user", "content": prompt}],
                model=model
            )
            
            content = response.content.strip()
            
            # Parse structured response
            sections = {}
            current_section = None
            for line in content.split('\n'):
                if any(header in line.upper() for header in ['OVERVIEW', 'COMPONENTS', 'RELATIONSHIPS', 'INSIGHTS', 'IMPLICATIONS']):
                    for header in ['OVERVIEW', 'COMPONENTS', 'RELATIONSHIPS', 'INSIGHTS', 'IMPLICATIONS']:
                        if header in line.upper():
                            current_section = header.lower()
                            sections[current_section] = []
                            break
                elif current_section and line.strip():
                    sections[current_section].append(line.strip())
            
            # Build structured analysis result
            analysis = {
                'subject': str(subject),
                'focus': focus,
                'depth': depth,
                'overview': '\n'.join(sections.get('overview', [])),
                'components': sections.get('components', []),
                'relationships': sections.get('relationships', []),
                'insights': sections.get('insights', []),
                'implications': sections.get('implications', []),
                'full_analysis': content,
                'model': model,
            }
            
            # Store in memory with high importance
            working_memory.store(
                content=f"Analysis of {str(subject)[:50]}: {sections.get('insights', [''])[ 0][:100] if sections.get('insights') else 'completed'}",
                importance=0.8,
                tags=["analysis", focus, "llm"],
            )
            
            execution_time = int((time.time() - start_time) * 1000)
            
            return PrimitiveResult(
                content=analysis,
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
                    'depth': depth,
                    'focus': focus,
                    'model': model,
                    'component_count': len(analysis['components']),
                    'insight_count': len(analysis['insights']),
                }
            )
            
        except Exception as e:
            logger.error(f"AnalyzeComposite execution failed: {e}")
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
        depth = kwargs.get('depth', 2)
        return ResourceEstimate(
            tokens=100 * depth,
            time_ms=50 * depth,
            memory_items=1,
            complexity=0.5 + 0.1 * depth,
        )
    
    def validate_inputs(self, **kwargs) -> None:
        """Validate inputs."""
        if "subject" not in kwargs:
            raise ValueError("'subject' parameter required")
    
    def matches_context(self, context: ExecutionContext, **kwargs) -> float:
        """Check context match."""
        if context.quality_threshold > 0.6:
            return 0.8
        return 0.6
    
    def rollback(self, context: ExecutionContext) -> None:
        """Rollback analysis."""
        pass


