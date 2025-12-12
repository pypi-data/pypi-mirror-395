"""
Perceive and interpret sensory information using LLM.
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


class PerceiveLLM(CorePrimitive):
    """
    Perceive and interpret sensory information using LLM.
    
    Processes input data and extracts meaning.
    """
    
    def __init__(self):
        """Initialize primitive."""
        super().__init__()
        self._name = "perceive"
        self._hint = (
            "Use for sensing and interpreting information from any modality "
            "(text, structured data, etc.). Best for initial data processing, "
            "pattern recognition, or extracting meaning. Use when raw data needs "
            "interpretation before further processing. Suitable for all domains."
        )
    
    def execute(
        self,
        context: ExecutionContext,
        working_memory: WorkingMemory,
        data: Any,
        modality: str = "text",
        task: str = "interpret",
        **kwargs
    ) -> PrimitiveResult:
        """
        Perceive and interpret data using LLM.
        
        Args:
            context: Execution context
            working_memory: Working memory
            data: Data to perceive
            modality: Data modality (text, image, etc.)
            task: Specific perception task (interpret, extract, classify, etc.)
            **kwargs: Additional parameters
        
        Returns:
            PrimitiveResult with interpretation
        """
        start_time = time.time()
        
        try:
            # Get LLM manager
            llm_manager = get_llm_manager()
            
            # Build perception prompt based on modality and task
            if modality == "text":
                prompt = f"""Analyze and interpret the following text:

Text: {data}

Task: {task.capitalize()} the content.

Provide:
1. Key insights and meaning
2. Important patterns or themes
3. Relevant features or characteristics
4. Any notable implications"""
            
            elif modality == "structured":
                prompt = f"""Analyze the following structured data:

Data: {data}

Task: {task.capitalize()} the data structure.

Provide:
1. Key observations about the data
2. Patterns or anomalies
3. Structural characteristics
4. Meaningful interpretations"""
            
            else:  # Generic
                prompt = f"""Perceive and analyze the following input:

Input: {data}
Modality: {modality}

Task: {task.capitalize()}

Provide a comprehensive interpretation."""
            
            # Use fast model for perception
            response = llm_manager.request(
                messages=[{"role": "user", "content": prompt}],
                model="gpt-4o-mini"
            )
            
            interpretation = response.content.strip()
            
            # Extract basic features
            features = {
                'modality': modality,
                'data_type': type(data).__name__,
                'size': len(str(data)) if data else 0,
            }
            
            if isinstance(data, str):
                features.update({
                    'word_count': len(data.split()),
                    'char_count': len(data),
                })
            
            result = {
                'data': data if len(str(data)) < 500 else str(data)[:500] + "...",
                'modality': modality,
                'task': task,
                'features': features,
                'interpretation': interpretation,
                'model': 'gpt-4o-mini',
            }
            
            # Store perception in memory
            working_memory.store(
                content=f"Perceived ({modality}): {interpretation[:100]}...",
                importance=0.7,
                tags=["perception", modality, task],
            )
            
            execution_time = int((time.time() - start_time) * 1000)
            
            return PrimitiveResult(
                content=result,
                confidence=ConfidenceMetrics(
                    overall=0.85,
                    reasoning=0.85,
                    completeness=0.8,
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
                    'modality': modality,
                    'task': task,
                    'model': 'gpt-4o-mini',
                }
            )
            
        except Exception as e:
            logger.error(f"PerceiveLLM execution failed: {e}")
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
        data = kwargs.get('data', '')
        size = len(str(data)) if data else 0
        return ResourceEstimate(
            tokens=0,
            time_ms=5 + size // 100,
            memory_items=1,
            complexity=0.3,
        )
    
    def validate_inputs(self, **kwargs) -> None:
        """Validate inputs."""
        if "data" not in kwargs:
            raise ValueError("'data' parameter required")
    
    def matches_context(self, context: ExecutionContext, **kwargs) -> float:
        """Check context match."""
        return 1.0  # Always available
    
    def rollback(self, context: ExecutionContext) -> None:
        """Rollback perception."""
        pass


