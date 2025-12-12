"""
Explain: understand + structure + communicate + verify using LLM.
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


class ExplainComposite(CompositePrimitive):
    """
    Explain: understand + structure + communicate + verify.
    
    Provides clear explanations of concepts or processes using LLM.
    """
    
    def __init__(self):
        """Initialize primitive."""
        super().__init__()
        self._name = "explain"
        self.sub_primitives = ["think", "decompose", "synthesize", "verify"]
        self._hint = (
            "Use to provide clear, structured explanations. Best for teaching, "
            "documentation, clarification, and communication. Composes think + "
            "decompose + synthesize + verify primitives. Use when you need to "
            "explain complex concepts, justify decisions, or communicate understanding. "
            "Quality threshold >0.7 recommended for clear explanations."
        )
    
    def execute(
        self,
        context: ExecutionContext,
        working_memory: WorkingMemory,
        subject: str,
        audience: str = "general",
        detail_level: int = 2,
        **kwargs
    ) -> PrimitiveResult:
        """
        Explain subject using LLM with audience-appropriate detail.
        
        Args:
            context: Execution context
            working_memory: Working memory
            subject: Subject to explain
            audience: Target audience (general, expert, beginner, child)
            detail_level: Level of detail (1=brief, 5=comprehensive)
            **kwargs: Additional parameters
        
        Returns:
            PrimitiveResult with structured explanation
        """
        start_time = time.time()
        
        try:
            llm_manager = get_llm_manager()
            
            # Retrieve context
            mem_context = working_memory.retrieve(query=subject, top_k=5)
            context_str = "\n".join([m.content for m in mem_context]) if mem_context else "No prior context."
            
            # Build explanation prompt
            audience_instructions = {
                "general": "Explain clearly for a general audience with no specialized knowledge.",
                "expert": "Provide a technical explanation for domain experts.",
                "beginner": "Explain simply for someone new to the topic.",
                "child": "Explain in simple terms suitable for children.",
            }
            
            detail_instructions = {
                1: "Provide a brief, high-level explanation.",
                2: "Provide a moderate explanation with key details.",
                3: "Provide a comprehensive explanation.",
                4: "Provide a detailed, thorough explanation.",
                5: "Provide an exhaustive explanation covering all aspects.",
            }
            
            prompt = f"""Explain the following topic clearly and structured.

Topic: {subject}

Audience: {audience_instructions.get(audience, audience)}
Detail Level: {detail_instructions.get(detail_level, detail_instructions[2])}

Context from memory:
{context_str}

Provide a structured explanation with the following sections:

1. OVERVIEW
   - Brief introduction to the topic
   - Why it matters

2. KEY CONCEPTS
   - Main ideas or components
   - Important terminology

3. HOW IT WORKS (if applicable)
   - Mechanisms or processes
   - Step-by-step if relevant

4. EXAMPLES
   - Concrete examples appropriate for {audience}
   - Real-world applications

5. COMMON MISCONCEPTIONS (if applicable)
   - What people often get wrong
   - Clarifications

Format your response with clear section headers."""
            
            response = llm_manager.request(
                messages=[{"role": "user", "content": prompt}],
                model="gpt-4o-mini"
            )
            
            content = response.content.strip()
            
            # Parse sections
            sections = []
            current_section = None
            
            for line in content.split('\n'):
                upper_line = line.upper()
                if any(h in upper_line for h in ['OVERVIEW', 'KEY CONCEPTS', 'HOW IT WORKS', 'EXAMPLES', 'MISCONCEPTIONS']):
                    if current_section:
                        sections.append(current_section)
                    # Extract section title
                    for header in ['OVERVIEW', 'KEY CONCEPTS', 'HOW IT WORKS', 'EXAMPLES', 'COMMON MISCONCEPTIONS', 'MISCONCEPTIONS']:
                        if header in upper_line:
                            current_section = {
                                'title': header.title(),
                                'content': []
                            }
                            break
                elif current_section and line.strip():
                    current_section['content'].append(line.strip())
            
            if current_section:
                sections.append(current_section)
            
            # Format sections
            for section in sections:
                section['content'] = '\n'.join(section['content'])
            
            explanation = {
                'subject': subject,
                'audience': audience,
                'sections': sections,
                'full_explanation': content,
                'detail_level': detail_level,
                'model': 'gpt-4o-mini',
            }
            
            working_memory.store(
                content=f"Explained: {subject} for {audience} - {sections[0]['content'][:100] if sections else 'completed'}",
                importance=0.7,
                tags=["explanation", audience, "llm"],
            )
            
            execution_time = int((time.time() - start_time) * 1000)
            
            return PrimitiveResult(
                content=explanation,
                confidence=ConfidenceMetrics(
                    overall=0.85,
                    reasoning=0.9,
                    completeness=0.85,
                    consistency=0.9,
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
                    'audience': audience,
                    'detail_level': detail_level,
                    'section_count': len(sections),
                    'model': 'gpt-4o-mini',
                }
            )
        
        except Exception as e:
            logger.error(f"ExplainComposite execution failed: {e}")
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
        detail_level = kwargs.get('detail_level', 2)
        return ResourceEstimate(
            tokens=200 * detail_level,
            time_ms=50 * detail_level,
            memory_items=1,
            complexity=0.5 + 0.1 * detail_level,
        )
    
    def validate_inputs(self, **kwargs) -> None:
        """Validate inputs."""
        if "subject" not in kwargs:
            raise ValueError("'subject' parameter required")
    
    def matches_context(self, context: ExecutionContext, **kwargs) -> float:
        """Check context match."""
        if context.quality_threshold > 0.7:
            return 0.9
        return 0.7
    
    def rollback(self, context: ExecutionContext) -> None:
        """Rollback explanation."""
        pass
