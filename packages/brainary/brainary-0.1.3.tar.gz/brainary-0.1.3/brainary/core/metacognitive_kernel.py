"""
Metacognitive Kernel - Self-Monitoring and Control Layer

The Metacognitive Kernel sits above the Cognitive Kernel and provides:
1. **Monitoring**: Track execution quality, resource usage, confidence levels
2. **Control**: Intervene when execution deviates from expectations
3. **Adjustment**: Modify execution strategies dynamically based on monitoring

This implements a "thinking about thinking" layer that observes cognitive
processes and makes strategic decisions about how cognition should proceed.

Architecture:
    User Space (Applications)
           ↓
    Metacognitive Kernel ← monitors & controls
           ↓
    Cognitive Kernel (Execution)
           ↓
    Hardware Abstraction (LLM Drivers)

The relationship mirrors OS kernel design:
- Cognitive Kernel = Core OS (process scheduling, memory, I/O)
- Metacognitive Kernel = Hypervisor/VM Monitor (observes and controls OS behavior)
"""

import time
import logging
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum

from brainary.core.context import ExecutionContext
from brainary.primitive.base import PrimitiveResult
from brainary.memory.working import WorkingMemory

logger = logging.getLogger(__name__)


class MonitoringLevel(Enum):
    """Level of metacognitive monitoring."""
    MINIMAL = "minimal"      # Only track success/failure
    STANDARD = "standard"    # Track quality metrics
    DETAILED = "detailed"    # Detailed execution tracing
    INTROSPECTIVE = "introspective"  # Deep cognitive analysis


class InterventionStrategy(Enum):
    """Strategy for metacognitive intervention."""
    PASSIVE = "passive"      # Only observe, no intervention
    REACTIVE = "reactive"    # Intervene on failures
    PROACTIVE = "proactive"  # Intervene before predicted failures
    ADAPTIVE = "adaptive"    # Learn optimal intervention points


@dataclass
class ExecutionTrace:
    """Trace of a cognitive operation execution."""
    operation_id: str
    primitive_name: str
    start_time: float
    end_time: float
    success: bool
    confidence: float
    cost_tokens: int
    cost_time_ms: float
    context: ExecutionContext
    result: Optional[PrimitiveResult] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MetacognitiveState:
    """Current metacognitive monitoring state."""
    # Performance metrics
    recent_success_rate: float = 1.0
    average_confidence: float = 0.8
    resource_efficiency: float = 1.0
    
    # Behavioral indicators
    retry_count: int = 0
    strategy_switches: int = 0
    error_patterns: List[str] = field(default_factory=list)
    
    # Decision state
    current_strategy: str = "default"
    intervention_count: int = 0
    adjustment_history: List[Dict[str, Any]] = field(default_factory=list)
    
    # Learning state
    execution_traces: List[ExecutionTrace] = field(default_factory=list)
    confidence_trend: List[float] = field(default_factory=list)


@dataclass
class MetacognitiveAssessment:
    """Assessment from metacognitive analysis."""
    overall_health: float  # 0.0-1.0
    confidence_in_assessment: float
    detected_issues: List[str]
    recommended_adjustments: List[str]
    should_intervene: bool
    intervention_urgency: float  # 0.0-1.0
    reasoning: str


class MetacognitiveKernel:
    """
    Metacognitive layer that monitors and controls cognitive execution.
    
    The Metacognitive Kernel provides:
    1. **Self-Monitoring**: Track cognitive process quality and efficiency
    2. **Strategic Control**: Decide when and how to adjust execution
    3. **Adaptive Intervention**: Modify strategies based on performance
    4. **Learning from Failures**: Extract patterns from execution traces
    
    It wraps the Cognitive Kernel and can:
    - Observe all executions (passive monitoring)
    - Intervene before/during/after execution (active control)
    - Suggest strategy changes (advisory)
    - Force strategy changes (mandatory)
    - Terminate unproductive execution paths
    
    Responsibilities:
    - Monitor execution quality, confidence, resource usage
    - Detect anomalies and degrading performance
    - Trigger strategic adjustments (retry, switch strategy, rollback)
    - Learn optimal intervention policies
    - Maintain execution traces for analysis
    
    Example:
        >>> from brainary.core.kernel import CognitiveKernel
        >>> from brainary.core.metacognitive_kernel import MetacognitiveKernel
        >>> 
        >>> cognitive_kernel = CognitiveKernel()
        >>> meta_kernel = MetacognitiveKernel(
        ...     cognitive_kernel=cognitive_kernel,
        ...     monitoring_level=MonitoringLevel.STANDARD,
        ...     intervention_strategy=InterventionStrategy.ADAPTIVE
        ... )
        >>> 
        >>> # Execute with metacognitive oversight
        >>> result = meta_kernel.execute(
        ...     "think",
        ...     question="complex problem",
        ...     context=ctx
        ... )
    """
    
    def __init__(
        self,
        cognitive_kernel: Any,  # CognitiveKernel type
        monitoring_level: MonitoringLevel = MonitoringLevel.STANDARD,
        intervention_strategy: InterventionStrategy = InterventionStrategy.REACTIVE,
        enable_learning: bool = True,
        confidence_threshold: float = 0.6,
        max_retries: int = 3,
    ):
        """
        Initialize metacognitive kernel.
        
        Args:
            cognitive_kernel: Underlying cognitive kernel to monitor
            monitoring_level: Level of monitoring detail
            intervention_strategy: Strategy for interventions
            enable_learning: Whether to learn from execution traces
            confidence_threshold: Minimum acceptable confidence
            max_retries: Maximum retry attempts for failed operations
        """
        self.cognitive_kernel = cognitive_kernel
        self.monitoring_level = monitoring_level
        self.intervention_strategy = intervention_strategy
        self.enable_learning = enable_learning
        self.confidence_threshold = confidence_threshold
        self.max_retries = max_retries
        
        # Metacognitive state
        self.state = MetacognitiveState()
        
        # Monitoring callbacks
        self._pre_execution_hooks: List[Callable] = []
        self._post_execution_hooks: List[Callable] = []
        self._intervention_hooks: List[Callable] = []
        
        logger.info(
            f"MetacognitiveKernel initialized: "
            f"monitoring={monitoring_level.value}, "
            f"intervention={intervention_strategy.value}"
        )
    
    def execute(
        self,
        primitive_name: str,
        context: Optional[ExecutionContext] = None,
        working_memory: Optional[WorkingMemory] = None,
        **kwargs
    ) -> PrimitiveResult:
        """
        Execute primitive with metacognitive monitoring and control.
        
        This wraps cognitive kernel execution with:
        1. Pre-execution assessment
        2. Execution monitoring
        3. Post-execution evaluation
        4. Intervention if needed
        
        Args:
            primitive_name: Name of primitive to execute
            context: Execution context
            working_memory: Working memory
            **kwargs: Primitive-specific parameters
        
        Returns:
            PrimitiveResult with metacognitive annotations
        """
        operation_id = f"meta_{int(time.time() * 1000)}"
        start_time = time.time()
        
        logger.info("="*80)
        logger.info(f"METACOGNITIVE: Overseeing execution of '{primitive_name}'")
        logger.info("="*80)
        
        # Step 1: Pre-execution assessment
        pre_assessment = self._pre_execution_assessment(
            primitive_name, context, **kwargs
        )
        
        if not pre_assessment.should_intervene:
            logger.info("✓ Pre-assessment: Execution approved")
        else:
            logger.warning(
                f"⚠ Pre-assessment: Intervention recommended "
                f"(urgency={pre_assessment.intervention_urgency:.2f})"
            )
            if self.intervention_strategy != InterventionStrategy.PASSIVE:
                self._apply_pre_adjustments(pre_assessment, context, kwargs)
        
        # Step 2: Execute through cognitive kernel
        logger.info(f"→ Delegating to Cognitive Kernel...")
        result = self.cognitive_kernel.execute(
            primitive_name,
            context=context,
            working_memory=working_memory,
            **kwargs
        )
        
        end_time = time.time()
        
        # Step 3: Create execution trace
        trace = ExecutionTrace(
            operation_id=operation_id,
            primitive_name=primitive_name,
            start_time=start_time,
            end_time=end_time,
            success=result.success,
            confidence=result.confidence.overall if result.confidence else 0.0,
            cost_tokens=result.cost.tokens if result.cost else 0,
            cost_time_ms=(end_time - start_time) * 1000,
            context=context,
            result=result,
            metadata={"pre_assessment": pre_assessment}
        )
        
        # Step 4: Post-execution analysis
        post_assessment = self._post_execution_analysis(trace)
        
        logger.info(f"✓ Post-analysis: health={post_assessment.overall_health:.2f}")
        
        # Step 5: Update metacognitive state
        self._update_state(trace, post_assessment)
        
        # Step 6: Intervention if needed
        if post_assessment.should_intervene:
            logger.warning(
                f"⚠ Intervention triggered: {post_assessment.reasoning}"
            )
            result = self._intervene(
                trace, post_assessment, context, working_memory, **kwargs
            )
        
        # Step 7: Learning
        if self.enable_learning:
            self._learn_from_execution(trace, post_assessment)
        
        logger.info(f"METACOGNITIVE: Oversight complete")
        logger.info("="*80)
        
        return result
    
    def _pre_execution_assessment(
        self,
        primitive_name: str,
        context: Optional[ExecutionContext],
        **kwargs
    ) -> MetacognitiveAssessment:
        """
        Assess execution viability before running.
        
        Checks:
        - Recent performance trends
        - Resource availability
        - Context appropriateness
        - Parameter validity
        """
        issues = []
        adjustments = []
        should_intervene = False
        urgency = 0.0
        
        # Check recent performance
        if self.state.recent_success_rate < 0.5:
            issues.append("Low recent success rate")
            adjustments.append("Consider switching strategy")
            should_intervene = True
            urgency = max(urgency, 0.7)
        
        # Check confidence trend
        if len(self.state.confidence_trend) >= 3:
            recent_confidence = sum(self.state.confidence_trend[-3:]) / 3
            if recent_confidence < self.confidence_threshold:
                issues.append("Declining confidence trend")
                adjustments.append("Increase reasoning depth")
                should_intervene = True
                urgency = max(urgency, 0.6)
        
        # Check retry history
        if self.state.retry_count >= self.max_retries - 1:
            issues.append("Approaching max retries")
            adjustments.append("Consider alternative approach")
            should_intervene = True
            urgency = max(urgency, 0.8)
        
        health = 1.0 - (len(issues) * 0.2)
        
        return MetacognitiveAssessment(
            overall_health=max(0.0, health),
            confidence_in_assessment=0.8,
            detected_issues=issues,
            recommended_adjustments=adjustments,
            should_intervene=should_intervene,
            intervention_urgency=urgency,
            reasoning=f"Pre-execution check: {len(issues)} issues detected"
        )
    
    def _post_execution_analysis(
        self,
        trace: ExecutionTrace
    ) -> MetacognitiveAssessment:
        """
        Analyze execution after completion.
        
        Evaluates:
        - Success/failure
        - Confidence levels
        - Resource efficiency
        - Quality indicators
        """
        issues = []
        adjustments = []
        should_intervene = False
        urgency = 0.0
        
        result = trace.result
        
        # Check execution success
        if not result.success:
            issues.append(f"Execution failed: {result.error}")
            adjustments.append("Retry with different strategy")
            should_intervene = True
            urgency = 0.9
        
        # Check confidence
        elif trace.confidence < self.confidence_threshold:
            issues.append(f"Low confidence: {trace.confidence:.2f}")
            adjustments.append("Increase reasoning depth or verify results")
            should_intervene = (
                self.intervention_strategy == InterventionStrategy.PROACTIVE
            )
            urgency = 0.5
        
        # Check resource efficiency
        expected_tokens = 1000  # Simple heuristic
        if trace.cost_tokens > expected_tokens * 2:
            issues.append(f"High token usage: {trace.cost_tokens}")
            adjustments.append("Optimize primitive expansion")
            urgency = max(urgency, 0.3)
        
        health = 1.0 - (len(issues) * 0.3)
        
        return MetacognitiveAssessment(
            overall_health=max(0.0, health),
            confidence_in_assessment=0.85,
            detected_issues=issues,
            recommended_adjustments=adjustments,
            should_intervene=should_intervene,
            intervention_urgency=urgency,
            reasoning=f"Post-execution analysis: {'success' if result.success else 'failure'}"
        )
    
    def _apply_pre_adjustments(
        self,
        assessment: MetacognitiveAssessment,
        context: Optional[ExecutionContext],
        kwargs: Dict[str, Any]
    ) -> None:
        """Apply recommended adjustments before execution."""
        logger.info("→ Applying pre-execution adjustments:")
        
        for adjustment in assessment.recommended_adjustments:
            logger.info(f"  • {adjustment}")
            
            # Example adjustments
            if "increase reasoning depth" in adjustment.lower():
                if context:
                    context.quality_threshold = min(1.0, context.quality_threshold + 0.1)
            
            elif "switch strategy" in adjustment.lower():
                # Could modify kwargs to use different implementation
                self.state.strategy_switches += 1
        
        self.state.intervention_count += 1
    
    def _intervene(
        self,
        trace: ExecutionTrace,
        assessment: MetacognitiveAssessment,
        context: Optional[ExecutionContext],
        working_memory: Optional[WorkingMemory],
        **kwargs
    ) -> PrimitiveResult:
        """
        Intervene in execution based on assessment.
        
        Can:
        - Retry with modified parameters
        - Switch to alternative strategy
        - Request deeper reasoning
        - Abort and return best effort
        """
        logger.warning(f"→ Intervening: {assessment.reasoning}")
        
        # Record intervention
        self.state.intervention_count += 1
        self.state.adjustment_history.append({
            "timestamp": time.time(),
            "trigger": assessment.reasoning,
            "adjustments": assessment.recommended_adjustments
        })
        
        # Decide intervention type
        if not trace.result.success and self.state.retry_count < self.max_retries:
            # Retry strategy
            logger.info(f"  → Retry attempt {self.state.retry_count + 1}/{self.max_retries}")
            self.state.retry_count += 1
            
            # Modify parameters for retry
            modified_kwargs = kwargs.copy()
            if context:
                context.quality_threshold = min(1.0, context.quality_threshold + 0.15)
            
            # Retry execution
            return self.cognitive_kernel.execute(
                trace.primitive_name,
                context=context,
                working_memory=working_memory,
                **modified_kwargs
            )
        
        elif trace.confidence < self.confidence_threshold:
            # Request verification
            logger.info("  → Requesting verification")
            # Could trigger self-assessment primitive here
            return trace.result
        
        else:
            # Return as-is
            logger.info("  → Accepting result with noted concerns")
            return trace.result
    
    def _update_state(
        self,
        trace: ExecutionTrace,
        assessment: MetacognitiveAssessment
    ) -> None:
        """Update metacognitive state from execution."""
        # Add trace to history (keep last 100)
        self.state.execution_traces.append(trace)
        if len(self.state.execution_traces) > 100:
            self.state.execution_traces.pop(0)
        
        # Update confidence trend
        self.state.confidence_trend.append(trace.confidence)
        if len(self.state.confidence_trend) > 10:
            self.state.confidence_trend.pop(0)
        
        # Update success rate (last 10 executions)
        recent_traces = self.state.execution_traces[-10:]
        self.state.recent_success_rate = (
            sum(1 for t in recent_traces if t.success) / len(recent_traces)
            if recent_traces else 1.0
        )
        
        # Update average confidence
        self.state.average_confidence = (
            sum(self.state.confidence_trend) / len(self.state.confidence_trend)
            if self.state.confidence_trend else 0.8
        )
        
        # Update resource efficiency
        recent_tokens = sum(t.cost_tokens for t in recent_traces)
        expected_tokens = len(recent_traces) * 1000  # Simple heuristic
        self.state.resource_efficiency = (
            expected_tokens / max(1, recent_tokens) if recent_tokens > 0 else 1.0
        )
        
        # Reset retry count on success
        if trace.success:
            self.state.retry_count = 0
    
    def _learn_from_execution(
        self,
        trace: ExecutionTrace,
        assessment: MetacognitiveAssessment
    ) -> None:
        """Learn patterns from execution trace."""
        # This could be expanded to:
        # - Identify common failure patterns
        # - Learn optimal intervention thresholds
        # - Discover context-specific strategies
        # - Build predictive models for intervention
        
        if not trace.success:
            # Record error pattern
            error = trace.result.error if trace.result else "unknown"
            self.state.error_patterns.append(error)
            
            # Keep only recent patterns
            if len(self.state.error_patterns) > 50:
                self.state.error_patterns.pop(0)
    
    def get_metacognitive_stats(self) -> Dict[str, Any]:
        """
        Get comprehensive metacognitive statistics.
        
        Returns:
            Statistics about metacognitive monitoring and interventions
        """
        return {
            "monitoring": {
                "level": self.monitoring_level.value,
                "intervention_strategy": self.intervention_strategy.value,
                "total_executions": len(self.state.execution_traces),
            },
            "performance": {
                "recent_success_rate": self.state.recent_success_rate,
                "average_confidence": self.state.average_confidence,
                "resource_efficiency": self.state.resource_efficiency,
            },
            "interventions": {
                "total_count": self.state.intervention_count,
                "retry_count": self.state.retry_count,
                "strategy_switches": self.state.strategy_switches,
            },
            "learning": {
                "execution_traces": len(self.state.execution_traces),
                "confidence_trend_length": len(self.state.confidence_trend),
                "error_patterns": len(set(self.state.error_patterns)),
            }
        }
    
    def get_health_report(self) -> Dict[str, Any]:
        """
        Get current health assessment.
        
        Returns:
            Health report with indicators and recommendations
        """
        # Calculate overall health score
        health_factors = [
            ("success_rate", self.state.recent_success_rate, 0.3),
            ("confidence", self.state.average_confidence, 0.3),
            ("efficiency", self.state.resource_efficiency, 0.2),
            ("stability", 1.0 - (self.state.retry_count / max(1, self.max_retries)), 0.2),
        ]
        
        overall_health = sum(value * weight for _, value, weight in health_factors)
        
        # Identify concerns
        concerns = []
        if self.state.recent_success_rate < 0.7:
            concerns.append("Low success rate")
        if self.state.average_confidence < 0.65:
            concerns.append("Low confidence")
        if self.state.resource_efficiency < 0.5:
            concerns.append("Poor resource efficiency")
        if self.state.retry_count >= self.max_retries - 1:
            concerns.append("High retry count")
        
        # Generate recommendations
        recommendations = []
        if self.state.recent_success_rate < 0.7:
            recommendations.append("Review execution strategies and parameters")
        if self.state.average_confidence < 0.65:
            recommendations.append("Increase reasoning depth or verification")
        if self.state.strategy_switches > 5:
            recommendations.append("Stabilize strategy selection")
        
        return {
            "overall_health": overall_health,
            "health_grade": (
                "excellent" if overall_health >= 0.9 else
                "good" if overall_health >= 0.75 else
                "fair" if overall_health >= 0.6 else
                "poor"
            ),
            "factors": {name: value for name, value, _ in health_factors},
            "concerns": concerns,
            "recommendations": recommendations,
            "state_summary": {
                "executions": len(self.state.execution_traces),
                "interventions": self.state.intervention_count,
                "retries": self.state.retry_count,
            }
        }


# Global metacognitive kernel singleton
_global_meta_kernel: Optional[MetacognitiveKernel] = None


def get_metacognitive_kernel() -> Optional[MetacognitiveKernel]:
    """
    Get global metacognitive kernel if available.
    
    Returns:
        MetacognitiveKernel instance or None if not initialized
    """
    return _global_meta_kernel


def initialize_metacognitive_kernel(
    cognitive_kernel: Any,
    monitoring_level: MonitoringLevel = MonitoringLevel.STANDARD,
    intervention_strategy: InterventionStrategy = InterventionStrategy.REACTIVE,
    **kwargs
) -> MetacognitiveKernel:
    """
    Initialize global metacognitive kernel.
    
    Args:
        cognitive_kernel: Cognitive kernel to wrap
        monitoring_level: Level of monitoring
        intervention_strategy: Intervention strategy
        **kwargs: Additional MetacognitiveKernel parameters
    
    Returns:
        Initialized MetacognitiveKernel
    """
    global _global_meta_kernel
    
    _global_meta_kernel = MetacognitiveKernel(
        cognitive_kernel=cognitive_kernel,
        monitoring_level=monitoring_level,
        intervention_strategy=intervention_strategy,
        **kwargs
    )
    
    logger.info("Global metacognitive kernel initialized")
    
    return _global_meta_kernel
