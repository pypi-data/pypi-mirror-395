"""
Create: imagine + generate + combine + refine.
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


class CreateComposite(CompositePrimitive):
    """
    Create: imagine + generate + combine + refine.
    
    Generates new content or solutions creatively.
    """
    
    def __init__(self):
        """Initialize primitive."""
        super().__init__()
        self._name = "create"
        self.sub_primitives = ["think", "synthesize", "evaluate"]
        self._hint = (
            "Use for creative generation of new content, ideas, or solutions. "
            "Best for brainstorming, content creation, ideation, and innovation. "
            "Composes think + synthesize + evaluate primitives. Use when you need "
            "novel ideas, creative solutions, or original content. Works best with "
            "time pressure <0.5 to allow creative exploration."
        )
    
    def execute(
        self,
        context: ExecutionContext,
        working_memory: WorkingMemory,
        goal: str,
        style: str = "creative",
        quantity: int = 1,
        **kwargs
    ) -> PrimitiveResult:
        """
        Create content using LLM-powered generation.
        
        Args:
            context: Execution context
            working_memory: Working memory
            goal: Creation goal (what to create)
            style: Creation style (creative, technical, formal, casual, etc.)
            quantity: Number of items to create (1-5)
            **kwargs: Additional parameters (constraints, tone, etc.)
        
        Returns:
            PrimitiveResult with created content
        """
        start_time = time.time()
        
        try:
            # Retrieve relevant inspiration from memory
            memory_items = working_memory.retrieve(
                query=f"create {goal} {style}",
                top_k=3
            )
            memory_context = "\n".join([f"- {item.content}" for item in memory_items])
            
            # Extract additional parameters
            constraints = kwargs.get('constraints', [])
            tone = kwargs.get('tone', style)
            format_spec = kwargs.get('format', 'any')
            
            # Build creative prompt
            constraints_text = ""
            if constraints:
                constraints_text = "\n\nCONSTRAINTS:\n" + "\n".join(f"- {c}" for c in constraints)
            
            prompt = f"""Generate creative content based on the following specifications.

GOAL: {goal}

STYLE: {style}
TONE: {tone}
FORMAT: {format_spec}
QUANTITY: Generate {quantity} distinct {'variant' if quantity == 1 else 'variants'}{constraints_text}

INSPIRATION FROM MEMORY:
{memory_context if memory_context else "No prior context - be original"}

For each item, provide:

1. CONCEPT: Core idea and creative approach
2. CONTENT: The actual created content (detailed and complete)
3. RATIONALE: Why this approach works for the goal
4. VARIATIONS: Possible alternative directions

Generate {quantity} creative {'item' if quantity == 1 else 'items'}, each separated by "---"."""

            # Get LLM creation
            llm_manager = get_llm_manager()
            
            # Use gpt-4o for high-quality creative content
            model = "gpt-4o" if quantity == 1 or style == "technical" else "gpt-4o-mini"
            
            response = llm_manager.request(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,  # Higher temperature for creativity
            )
            
            content_text = response.content
            
            # Parse created items
            items = []
            if "---" in content_text:
                raw_items = content_text.split("---")
            else:
                raw_items = [content_text]
            
            for i, raw_item in enumerate(raw_items[:quantity], 1):
                item = {
                    'id': i,
                    'concept': '',
                    'content': '',
                    'rationale': '',
                    'variations': '',
                }
                
                # Parse sections
                for section in ['CONCEPT:', 'CONTENT:', 'RATIONALE:', 'VARIATIONS:']:
                    start_idx = raw_item.find(section)
                    if start_idx != -1:
                        end_idx = len(raw_item)
                        for next_section in ['CONCEPT:', 'CONTENT:', 'RATIONALE:', 'VARIATIONS:']:
                            if next_section != section:
                                next_idx = raw_item.find(next_section, start_idx + len(section))
                                if next_idx != -1 and next_idx < end_idx:
                                    end_idx = next_idx
                        
                        item[section.rstrip(':').lower()] = raw_item[start_idx+len(section):end_idx].strip()
                
                # If parsing failed, use whole item as content
                if not item['content']:
                    item['content'] = raw_item.strip()
                
                items.append(item)
            
            creation = {
                'goal': goal,
                'style': style,
                'tone': tone,
                'items': items,
                'count': len(items),
                'model': model,
            }
            
            # Store in memory
            working_memory.store(
                content=f"Created {len(items)} {'item' if len(items) == 1 else 'items'}: {goal} ({style} style)",
                importance=0.75,
                tags=["creation", "creative", style],
            )
            
            execution_time = int((time.time() - start_time) * 1000)
            
            return PrimitiveResult(
                content=creation,
                confidence=ConfidenceMetrics(
                    overall=0.8,
                    reasoning=0.85,
                    completeness=0.8,
                    consistency=0.75,
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
                    'style': style,
                    'items_created': len(items),
                    'model': model,
                    'temperature': 0.8,
                }
            )
            
        except Exception as e:
            logger.error(f"Creation failed: {e}")
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
        quantity = kwargs.get('quantity', 1)
        return ResourceEstimate(
            tokens=150 * quantity,
            time_ms=80 * quantity,
            memory_items=1,
            complexity=0.6,
        )
    
    def validate_inputs(self, **kwargs) -> None:
        """Validate inputs."""
        if "goal" not in kwargs:
            raise ValueError("'goal' parameter required")
    
    def matches_context(self, context: ExecutionContext, **kwargs) -> float:
        """Check context match."""
        # Better for creative tasks with less time pressure
        if context.time_pressure < 0.5:
            return 0.8
        return 0.6
    
    def rollback(self, context: ExecutionContext) -> None:
        """Rollback creation."""
        pass


