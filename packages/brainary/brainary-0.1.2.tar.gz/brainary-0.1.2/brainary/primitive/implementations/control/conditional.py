"""
Execute operations conditionally with LLM-based semantic evaluation.
"""

from typing import Any, Dict, List, Optional, Tuple
import time
import logging

from brainary.primitive.base import (
    ControlPrimitive,
    PrimitiveResult,
    ResourceEstimate,
    ConfidenceMetrics,
    CostMetrics,
)
from brainary.core.context import ExecutionContext
from brainary.memory.working import WorkingMemory
from brainary.llm.manager import get_llm_manager

logger = logging.getLogger(__name__)


class ConditionalControl(ControlPrimitive):
    """
    Execute operations conditionally with intelligent semantic evaluation.
    
    Branches execution based on conditions, supporting both:
    - Simple boolean conditions ("true", "false", "yes", "no")
    - Complex natural language conditions evaluated by LLM
    
    Examples:
        Simple: condition="true"
        Semantic: condition="the code contains security vulnerabilities"
    """
    
    def __init__(self):
        """Initialize primitive."""
        super().__init__()
        self._name = "conditional"
        self._hint = (
            "Use for conditional branching based on conditions. Supports both simple "
            "boolean conditions and complex natural language conditions evaluated "
            "semantically by LLM. Best when execution path depends on runtime "
            "conditions, data, or context. Use for decision trees, adaptive workflows, "
            "context-dependent processing, or intelligent condition evaluation. "
            "Suitable for all domains when behavior needs to vary based on conditions."
        )
    
    def execute(
        self,
        context: ExecutionContext,
        working_memory: WorkingMemory,
        condition: str,
        if_true: str,
        if_false: str = None,
        **kwargs
    ) -> PrimitiveResult:
        """
        Execute conditionally with intelligent semantic evaluation.
        
        For simple boolean conditions ("true", "false", "yes", "no"), uses direct
        evaluation. For complex natural language conditions, uses LLM to evaluate
        the condition semantically based on provided context.
        
        Args:
            context: Execution context
            working_memory: Working memory
            condition: Condition to evaluate (simple or complex natural language)
            if_true: Operation if condition is true
            if_false: Operation if condition is false
            **kwargs: Additional context for condition evaluation (code, data, description, etc.)
        
        Returns:
            PrimitiveResult with executed branch and evaluation details
        
        Examples:
            # Simple condition
            execute(..., condition="true", if_true="proceed", if_false="stop")
            
            # Semantic condition
            execute(..., 
                condition="the code contains SQL injection vulnerability",
                if_true="flag_finding", 
                if_false="continue",
                code=code_snippet,
                file_path=path)
        """
        start_time = time.time()
        tokens_used = 0
        
        try:
            # Evaluate condition with semantic intelligence
            condition_result, evaluation_method, confidence = self._evaluate_condition(
                condition, working_memory, **kwargs
            )
            
            if evaluation_method == "llm":
                # Track token usage from LLM call
                tokens_used = len(condition.split()) + sum(len(str(v).split()) for v in kwargs.values()) + 20
            
            # Execute appropriate branch
            if condition_result:
                executed = if_true
                branch = "if_true"
            else:
                executed = if_false or "no_operation"
                branch = "if_false"
            
            result = {
                'condition': condition,
                'condition_result': condition_result,
                'branch_taken': branch,
                'executed': executed,
                'evaluation_method': evaluation_method,
                'confidence': confidence,
                'output': f"Result of {executed}",
            }
            
            # Store decision in working memory for learning
            working_memory.store(
                content=f"Conditional '{condition[:50]}...' evaluated to {condition_result} via {evaluation_method}, took {branch} branch",
                importance=0.7,
                tags=["control-flow", "conditional", "decision", evaluation_method],
            )
            
            execution_time = int((time.time() - start_time) * 1000)
            
            return PrimitiveResult(
                content=result,
                confidence=ConfidenceMetrics(
                    overall=confidence,
                    reasoning=confidence,
                    completeness=0.95,
                    consistency=0.9,
                    evidence_strength=0.85 if evaluation_method == "llm" else 1.0,
                ),
                execution_mode=context.execution_mode,
                cost=CostMetrics(
                    tokens=tokens_used,
                    latency_ms=execution_time,
                    memory_slots=1,
                    provider_cost_usd=tokens_used * 0.000002 if tokens_used > 0 else 0.0,  # Rough estimate
                ),
                primitive_name=self.name,
                success=True,
                metadata={
                    'branch': branch,
                    'evaluation_method': evaluation_method,
                    'condition_type': 'simple' if evaluation_method == 'direct' else 'semantic',
                }
            )
        
        except Exception as e:
            logger.error(f"Conditional evaluation failed: {e}")
            execution_time = int((time.time() - start_time) * 1000)
            
            # Conservative fallback: execute if_true for safety in critical contexts
            fallback_result = context.criticality > 0.7
            
            return PrimitiveResult(
                content={
                    'condition': condition,
                    'condition_result': fallback_result,
                    'branch_taken': 'if_true' if fallback_result else 'if_false',
                    'executed': if_true if fallback_result else (if_false or "no_operation"),
                    'evaluation_method': 'fallback',
                    'confidence': 0.5,
                    'error': str(e),
                },
                confidence=ConfidenceMetrics(
                    overall=0.5,
                    reasoning=0.3,
                    completeness=0.5,
                    consistency=0.5,
                    evidence_strength=0.3,
                ),
                execution_mode=context.execution_mode,
                cost=CostMetrics(
                    tokens=0,
                    latency_ms=execution_time,
                    memory_slots=1,
                    provider_cost_usd=0.0,
                ),
                primitive_name=self.name,
                success=False,
                error=f"Condition evaluation failed: {e}",
                metadata={'evaluation_method': 'fallback', 'error': str(e)}
            )
    
    def _evaluate_condition(
        self, 
        condition: str, 
        working_memory: WorkingMemory,
        **context_data
    ) -> Tuple[bool, str, float]:
        """
        Evaluate condition using appropriate method.
        
        Args:
            condition: Condition to evaluate
            working_memory: Working memory for context
            **context_data: Additional context for semantic evaluation
        
        Returns:
            Tuple of (result: bool, method: str, confidence: float)
            method can be 'direct', 'llm', or 'heuristic'
        """
        # Check if condition is simple boolean
        condition_lower = condition.lower().strip()
        
        # Direct evaluation for simple conditions
        if condition_lower in ["true", "yes", "1", "t", "y"]:
            return (True, "direct", 1.0)
        elif condition_lower in ["false", "no", "0", "f", "n"]:
            return (False, "direct", 1.0)
        
        # Check for simple boolean expressions without context
        if not context_data or len(condition_lower) < 10:
            # Heuristic: check for positive indicators
            if any(word in condition_lower for word in ["true", "yes", "success", "valid", "correct"]):
                return (True, "heuristic", 0.7)
            elif any(word in condition_lower for word in ["false", "no", "fail", "invalid", "incorrect"]):
                return (False, "heuristic", 0.7)
        
        # Complex condition - use LLM for semantic evaluation
        return self._evaluate_semantic_condition(condition, working_memory, context_data)
    
    def _evaluate_semantic_condition(
        self, 
        condition: str, 
        working_memory: WorkingMemory,
        context_data: Dict[str, Any]
    ) -> Tuple[bool, str, float]:
        """
        Evaluate complex natural language condition using LLM.
        
        Args:
            condition: Natural language condition to evaluate
            working_memory: Working memory for additional context
            context_data: Additional context for evaluation
        
        Returns:
            Tuple of (result: bool, method: str, confidence: float)
        """
        try:
            # Retrieve relevant context from memory
            memory_items = working_memory.retrieve(
                query=condition,
                top_k=3
            )
            memory_context = "\n".join([f"- {item.content}" for item in memory_items[:3]]) if memory_items else "No relevant history"
            
            # Format context data
            context_str = "\n".join([
                f"{key}: {str(value)[:200]}{'...' if len(str(value)) > 200 else ''}"
                for key, value in context_data.items()
                if value is not None
            ])
            
            # Build evaluation prompt
            prompt = f"""Evaluate whether the following condition is TRUE or FALSE based on the provided context.

CONDITION TO EVALUATE:
{condition}

CONTEXT INFORMATION:
{context_str if context_str else "No additional context provided"}

RELEVANT HISTORY:
{memory_context}

INSTRUCTIONS:
1. Analyze the condition carefully considering all context
2. Determine if the condition is satisfied (TRUE) or not (FALSE)
3. Respond with ONLY a JSON object in this exact format:
{{"result": true/false, "confidence": 0.0-1.0, "reasoning": "brief explanation"}}

Be precise and objective in your evaluation."""

            # Get LLM evaluation
            llm_manager = get_llm_manager()
            
            response = llm_manager.request(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,  # Low temperature for deterministic evaluation
                max_tokens=150,
                model="gpt-4o-mini"  # Fast model for condition evaluation
            )
            
            # Parse response
            import json
            response_text = response.content.strip()
            
            # Try to extract JSON
            if "{" in response_text and "}" in response_text:
                json_start = response_text.index("{")
                json_end = response_text.rindex("}") + 1
                json_str = response_text[json_start:json_end]
                parsed = json.loads(json_str)
                
                result = bool(parsed.get("result", False))
                confidence = float(parsed.get("confidence", 0.7))
                reasoning = parsed.get("reasoning", "")
                
                logger.debug(f"LLM condition evaluation: {condition[:50]}... -> {result} (confidence: {confidence})")
                logger.debug(f"Reasoning: {reasoning}")
                
                return (result, "llm", confidence)
            else:
                # Fallback: parse as simple true/false
                result = "true" in response_text.lower()
                confidence = 0.6
                logger.warning(f"LLM response not in expected format, using fallback parsing: {response_text}")
                return (result, "llm", confidence)
        
        except Exception as e:
            logger.error(f"LLM semantic evaluation failed: {e}")
            # Fallback to conservative heuristic
            # If condition contains negative words, assume false; otherwise true
            negative_words = ["not", "no", "without", "lacking", "missing", "absent"]
            has_negative = any(word in condition.lower() for word in negative_words)
            return (not has_negative, "heuristic", 0.5)
    
    def estimate_cost(self, **kwargs) -> ResourceEstimate:
        """
        Estimate execution cost.
        
        Cost varies based on condition complexity:
        - Simple conditions: minimal cost
        - Semantic conditions: LLM call cost
        """
        condition = kwargs.get('condition', '')
        condition_lower = condition.lower().strip()
        
        # Check if simple condition
        is_simple = condition_lower in ["true", "false", "yes", "no", "1", "0", "t", "f", "y", "n"]
        
        # Check if has context data (indicates semantic evaluation likely)
        has_context = any(k not in ['condition', 'if_true', 'if_false'] for k in kwargs.keys())
        
        if is_simple and not has_context:
            # Simple boolean - minimal cost
            return ResourceEstimate(
                tokens=0,
                time_ms=5,
                memory_items=1,
                complexity=0.2,
                llm_calls=0,
            )
        else:
            # Semantic evaluation - LLM cost
            # Estimate: condition + context ~= 100-200 tokens
            estimated_tokens = len(condition.split()) * 2 + sum(len(str(v).split()) for v in kwargs.values() if v is not None) + 50
            
            return ResourceEstimate(
                tokens=estimated_tokens,
                time_ms=300,  # LLM call latency
                memory_items=1,
                complexity=0.6,
                llm_calls=1,
            )
    
    def validate_inputs(self, **kwargs) -> None:
        """Validate inputs."""
        if "condition" not in kwargs:
            raise ValueError("'condition' parameter required")
        if "if_true" not in kwargs:
            raise ValueError("'if_true' parameter required")
    
    def matches_context(self, context: ExecutionContext, **kwargs) -> float:
        """Check context match."""
        return 1.0  # Always available
    
    def rollback(self, context: ExecutionContext) -> None:
        """Rollback conditional."""
        pass


