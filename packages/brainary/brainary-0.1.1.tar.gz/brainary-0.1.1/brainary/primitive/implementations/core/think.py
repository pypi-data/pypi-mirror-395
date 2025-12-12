"""
Thinking primitives - fast and deep.
"""

from typing import Any, Dict, List, Optional, Tuple
import time
import logging

from brainary.primitive.base import (
    CorePrimitive,
    PrimitiveResult,
    ResourceEstimate,
    ConfidenceMetrics,
    CostMetrics,
)
from brainary.core.context import ExecutionContext
from brainary.memory.working import WorkingMemory
from brainary.llm.manager import get_llm_manager

logger = logging.getLogger(__name__)


class ThinkFast(CorePrimitive):
    """
    Fast, intuitive thinking primitive.
    
    Provides quick responses using heuristics.
    """
    
    def __init__(self):
        """Initialize primitive."""
        super().__init__()
        self._name = "think"
        self._hint = (
            "Use for quick, intuitive responses when time pressure is high (>0.7) "
            "or quality requirements are moderate (<0.7). Best for simple questions, "
            "pattern matching, or when speed matters more than depth. Uses heuristics "
            "and cached patterns. Suitable for all domains when fast response needed."
        )
    
    def execute(
        self,
        context: ExecutionContext,
        working_memory: WorkingMemory,
        question: str,
        **kwargs
    ) -> PrimitiveResult:
        """
        Think quickly about question using LLM with fast model.
        
        Args:
            context: Execution context
            working_memory: Working memory
            question: Question to think about
            **kwargs: Additional parameters
        
        Returns:
            PrimitiveResult with answer
        """
        start_time = time.time()
        
        try:
            # Get LLM manager
            llm_manager = get_llm_manager()
            
            # Retrieve relevant context from working memory
            mem_context = working_memory.retrieve(query=question, top_k=3)
            context_str = "\n".join([m.content for m in mem_context]) if mem_context else "No prior context."
            
            # Build fast-thinking prompt
            prompt = f"""You are performing fast, intuitive thinking. Answer quickly and directly.

Context from memory:
{context_str}

Question: {question}

Provide a quick, concise answer based on patterns and heuristics. Focus on speed over depth."""
            
            # Use fast model (gpt-4o-mini or equivalent)
            # Note: Don't pass temperature/max_tokens in kwargs as provider sets them
            response = llm_manager.request(
                messages=[{"role": "user", "content": prompt}],
                model="gpt-4o-mini"
            )
            
            answer = response.content.strip()
            
            result = {
                'question': question,
                'answer': answer,
                'reasoning': 'Fast LLM-based intuitive response',
                'mode': 'fast',
                'model': 'gpt-4o-mini',
            }
            
            # Store in memory
            working_memory.store(
                content=f"Fast thinking: Q: {question[:50]}... A: {answer[:50]}...",
                importance=0.6,
                tags=["thinking", "fast", "llm"],
            )
            
            execution_time = int((time.time() - start_time) * 1000)
            
            return PrimitiveResult(
                content=result,
                confidence=ConfidenceMetrics(
                    overall=0.75,
                    reasoning=0.7,
                    completeness=0.7,
                    consistency=0.8,
                    evidence_strength=0.7,
                ),
                execution_mode=context.execution_mode,
                cost=CostMetrics(
                    tokens=response.usage.total_tokens,
                    latency_ms=execution_time,
                    memory_slots=1,
                    provider_cost_usd=0.0,  # Cost tracking handled separately by cost_tracker
                ),
                primitive_name=self.name,
                success=True,
                metadata={
                    'mode': 'fast',
                    'model': 'gpt-4o-mini',
                }
            )
            
        except Exception as e:
            logger.error(f"ThinkFast execution failed: {e}")
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
            tokens=0,
            time_ms=5,
            memory_items=1,
            complexity=0.2,
        )
    
    def validate_inputs(self, **kwargs) -> None:
        """Validate inputs."""
        if "question" not in kwargs:
            raise ValueError("'question' parameter required")
    
    def matches_context(self, context: ExecutionContext, **kwargs) -> float:
        """Check context match."""
        # Better when time pressure is high
        if context.time_pressure > 0.7:
            return 0.95
        if context.quality_threshold < 0.7:
            return 0.85
        return 0.6
    
    def rollback(self, context: ExecutionContext) -> None:
        """Rollback thinking."""
        pass


class ThinkDeep(CorePrimitive):
    """
    Deep, analytical thinking primitive.
    
    Provides thorough analysis and reasoning.
    """
    
    def __init__(self):
        """Initialize primitive."""
        super().__init__()
        self._name = "think"
        self._hint = (
            "Use for careful, analytical thinking when quality requirements are "
            "high (>0.8) or time pressure is low (<0.5). Best for complex reasoning, "
            "detailed analysis, or when accuracy is critical. Explores multiple "
            "perspectives and validates conclusions. Suitable for all domains when "
            "quality matters more than speed."
        )
    
    def execute(
        self,
        context: ExecutionContext,
        working_memory: WorkingMemory,
        question: str,
        **kwargs
    ) -> PrimitiveResult:
        """
        Think deeply about question using LLM with analytical reasoning.
        
        Args:
            context: Execution context
            working_memory: Working memory
            question: Question to think about
            **kwargs: Additional parameters
        
        Returns:
            PrimitiveResult with detailed analysis
        """
        start_time = time.time()
        
        try:
            # Get LLM manager
            llm_manager = get_llm_manager()
            
            # Retrieve relevant context from working memory
            mem_context = working_memory.retrieve(query=question, top_k=5)
            context_str = "\n".join([m.content for m in mem_context]) if mem_context else "No prior context."
            
            # Build deep-thinking prompt with structured reasoning
            prompt = f"""You are performing deep, analytical thinking. Think carefully and systematically.

Context from memory:
{context_str}

Question: {question}

Provide a thorough analysis following this structure:
1. Main Answer: Your comprehensive response
2. Reasoning Steps: List the key reasoning steps you took
3. Alternative Perspectives: Consider at least 2 alternative viewpoints
4. Confidence Assessment: Evaluate the strength of your conclusion

Be thorough, consider multiple angles, and validate your logic."""
            
            # Use more capable model for deep thinking
            # Note: Don't pass temperature/max_tokens in kwargs as provider sets them
            response = llm_manager.request(
                messages=[{"role": "user", "content": prompt}],
                model="gpt-4o"  # More capable model
            )
            
            content = response.content.strip()
            
            # Parse structured response (simple heuristic)
            sections = content.split('\n\n')
            answer = content  # Full response
            
            # Try to extract structured parts
            reasoning_steps = []
            alternatives = []
            
            for i, section in enumerate(sections):
                if any(keyword in section.lower() for keyword in ['reasoning', 'steps', 'because']):
                    reasoning_steps.append(section)
                elif any(keyword in section.lower() for keyword in ['alternative', 'however', 'another']):
                    alternatives.append(section)
            
            if not reasoning_steps:
                reasoning_steps = ["Comprehensive analytical reasoning applied"]
            if not alternatives:
                alternatives = ["Multiple perspectives considered"]
            
            result = {
                'question': question,
                'answer': answer,
                'reasoning': reasoning_steps,
                'alternatives': alternatives,
                'mode': 'deep',
                'model': 'gpt-4o',
            }
            
            # Store in memory with high importance
            working_memory.store(
                content=f"Deep analysis: Q: {question[:50]}... A: {answer[:100]}...",
                importance=0.85,
                tags=["thinking", "deep", "llm", "analysis"],
            )
            
            execution_time = int((time.time() - start_time) * 1000)
            
            return PrimitiveResult(
                content=result,
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
                    provider_cost_usd=0.0,  # Cost tracking handled separately by cost_tracker
                ),
                primitive_name=self.name,
                success=True,
                metadata={
                    'mode': 'deep',
                    'model': 'gpt-4o',
                    'reasoning_steps': len(reasoning_steps),
                    'alternatives': len(alternatives),
                }
            )
            
        except Exception as e:
            logger.error(f"ThinkDeep execution failed: {e}")
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
        question = kwargs.get('question', '')
        complexity = len(question) / 100
        return ResourceEstimate(
            tokens=0,
            time_ms=int(20 + 10 * complexity),
            memory_items=2,
            complexity=0.7 + 0.1 * complexity,
        )
    
    def validate_inputs(self, **kwargs) -> None:
        """Validate inputs."""
        if "question" not in kwargs:
            raise ValueError("'question' parameter required")
    
    def matches_context(self, context: ExecutionContext, **kwargs) -> float:
        """Check context match."""
        # Better when quality matters
        if context.quality_threshold > 0.8:
            return 0.95
        if context.time_pressure < 0.5:
            return 0.9
        return 0.7
    
    def rollback(self, context: ExecutionContext) -> None:
        """Rollback thinking."""
        pass
