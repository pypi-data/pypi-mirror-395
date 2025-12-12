"""
Metacognitive Monitor - Self-Monitoring Component

The Metacognitive Monitor provides self-monitoring and self-regulation 
capabilities through a configurable criteria system.

Key Features:
1. **Configurable**: Customize monitoring through criteria registration
2. **Extensible**: Add domain-specific criteria with embedded actions
3. **Flexible**: Control monitoring level and behavior
4. **Simple**: Single implementation, configured as needed

Architecture:
    CognitiveKernel
        └─ MetacognitiveMonitor (single configurable implementation)
            ├─ Monitor execution quality
            ├─ Detect issues via criteria
            ├─ Trigger actions automatically
            └─ Learn from patterns
"""

import time
import logging
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum

from brainary.core.context import ExecutionContext
from brainary.primitive.base import PrimitiveResult
from brainary.core.metacognitive_rules import (
    MonitoringCriterion,
    CriteriaType,
    CriteriaEvaluation,
    TransitionAction,
    ActionType,
)

logger = logging.getLogger(__name__)


class MonitoringLevel(Enum):
    """Level of metacognitive monitoring."""
    NONE = "none"           # No monitoring
    MINIMAL = "minimal"     # Only track success/failure
    STANDARD = "standard"   # Track quality metrics (default)
    DETAILED = "detailed"   # Detailed execution tracing
    INTROSPECTIVE = "introspective"  # Deep cognitive analysis


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
class MetacognitiveAssessment:
    """Assessment from metacognitive analysis."""
    overall_health: float  # 0.0-1.0
    confidence_in_assessment: float
    detected_issues: List[str]
    recommended_actions: List[str]
    should_intervene: bool
    intervention_urgency: float  # 0.0-1.0
    reasoning: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class MetacognitiveMonitor:
    """
    Configurable metacognitive monitor with extensible criteria system.
    
    This is the single monitor implementation that can be customized through:
    1. Monitoring level (NONE/MINIMAL/STANDARD/DETAILED/INTROSPECTIVE)
    2. Custom criteria registration (domain-specific monitoring)
    3. Configuration parameters (thresholds, learning, etc.)
    
    The monitor observes execution and provides assessments/recommendations,
    but the kernel decides whether to act on them.
    
    Key Methods:
    - register_criterion(): Add custom monitoring criteria
    - before_execution(): Pre-execution assessment
    - after_execution(): Post-execution assessment
    - decide_next_actions(): Determine control interventions
    - get_assessment(): Current metacognitive state
    """
    
    def __init__(
        self,
        monitoring_level: MonitoringLevel = MonitoringLevel.STANDARD,
        confidence_threshold: float = 0.7,
        enable_learning: bool = True,
        enable_default_criteria: bool = True
    ):
        """
        Initialize metacognitive monitor.
        
        Args:
            monitoring_level: Level of monitoring detail
            confidence_threshold: Minimum acceptable confidence
            enable_learning: Whether to learn from patterns
            enable_default_criteria: Register default criteria (security, confidence, resources)
        """
        self.monitoring_level = monitoring_level
        self.confidence_threshold = confidence_threshold
        self.enable_learning = enable_learning
        
        # State
        self.execution_traces: List[ExecutionTrace] = []
        self.confidence_trend: List[float] = []
        self.success_count = 0
        self.failure_count = 0
        self.intervention_suggestions = 0
        
        # Criteria system (criteria include embedded actions)
        self.criteria: List[MonitoringCriterion] = []
        
        # Register default criteria if enabled
        if enable_default_criteria:
            self._register_default_criteria()
    
    def _register_default_criteria(self):
        """
        Register default monitoring criteria (with embedded actions).
        
        Each criterion includes its action, providing out-of-box:
        - Content security filtering (priority 100)
        - Confidence threshold retry (priority 50)
        - Resource limit warnings (priority 10)
        """
        from brainary.core.metacognitive_rules import (
            ContentSecurityCriterion,
            ConfidenceThresholdCriterion,
            ResourceLimitCriterion,
        )
        
        # Content security for memory operations (priority 100, FILTER action)
        self.register_criterion(ContentSecurityCriterion(priority=100))
        
        # Confidence threshold for all operations (priority 50, RETRY action)
        self.register_criterion(
            ConfidenceThresholdCriterion(
                threshold=self.confidence_threshold,
                max_retries=3,
                priority=50
            )
        )
        
        # Resource limits (priority 10, WARN action)
        self.register_criterion(
            ResourceLimitCriterion(
                max_tokens=10000,
                max_time_ms=30000,
                priority=10
            )
        )
        
    def before_execution(
        self,
        primitive_name: str,
        context: ExecutionContext,
        **kwargs
    ) -> Optional[MetacognitiveAssessment]:
        """
        Called before primitive execution.
        
        Evaluates pre-execution criteria and pattern-based checks.
        
        Args:
            primitive_name: Name of primitive to execute
            context: Execution context
            **kwargs: Primitive parameters
            
        Returns:
            Optional assessment with pre-execution recommendations
        """
        if self.monitoring_level == MonitoringLevel.NONE:
            return None
        
        issues = []
        actions = []
        should_intervene = False
        urgency = 0.0
        
        # === CRITERIA SYSTEM: Evaluate pre-execution criteria ===
        evaluations = self.evaluate_criteria(
            primitive_name,
            context,
            CriteriaType.PRE_EXECUTION,
            **kwargs
        )
        
        for eval in evaluations:
            if not eval.passed:
                issues.append(eval.details)
                urgency = max(urgency, eval.severity)
                should_intervene = True
        
        # Get actions from failed criteria
        criterion_actions = self.get_actions_from_evaluations(evaluations)
        for action in criterion_actions:
            actions.append(action.reason)
        
        # === PATTERN-BASED MONITORING: Check trends ===
        # Check recent performance
        if len(self.execution_traces) >= 5:
            recent_traces = self.execution_traces[-5:]
            recent_success_rate = sum(1 for t in recent_traces if t.success) / 5
            
            if recent_success_rate < 0.6:
                issues.append("Low recent success rate (< 60%)")
                actions.append("Consider adjusting quality threshold or strategy")
                should_intervene = True
                urgency = max(urgency, 0.7)
        
        # Check confidence trend
        if len(self.confidence_trend) >= 3:
            recent_conf = sum(self.confidence_trend[-3:]) / 3
            if recent_conf < self.confidence_threshold:
                issues.append(f"Declining confidence trend (avg {recent_conf:.2f})")
                actions.append("Increase reasoning depth or verification")
                urgency = max(urgency, 0.5)
        
        if should_intervene:
            self.intervention_suggestions += 1
        
        health = 1.0 - (len(issues) * 0.2)
        
        return MetacognitiveAssessment(
            overall_health=max(0.0, health),
            confidence_in_assessment=0.8,
            detected_issues=issues,
            recommended_actions=actions,
            should_intervene=should_intervene,
            intervention_urgency=urgency,
            reasoning=f"Pre-execution check: {len(issues)} concerns detected",
            metadata={"phase": "pre-execution"}
        )
    
    def after_execution(
        self,
        trace: ExecutionTrace
    ) -> Optional[MetacognitiveAssessment]:
        """
        Called after primitive execution.
        
        Analyzes execution result and suggests interventions if needed.
        
        Args:
            trace: Execution trace with result
            
        Returns:
            Optional assessment with post-execution recommendations
        """
        if self.monitoring_level == MonitoringLevel.NONE:
            return None
        
        issues = []
        actions = []
        should_intervene = False
        urgency = 0.0
        
        result = trace.result
        
        # Record trace for learning
        if self.enable_learning:
            self.execution_traces.append(trace)
            if trace.confidence:
                self.confidence_trend.append(trace.confidence)
            if trace.success:
                self.success_count += 1
            else:
                self.failure_count += 1
        
        # === CRITERIA SYSTEM: Evaluate post-execution criteria ===
        evaluations = self.evaluate_criteria(
            trace.primitive_name,
            trace.context,
            CriteriaType.POST_EXECUTION,
            result=result
        )
        
        for eval in evaluations:
            if not eval.passed:
                issues.append(eval.details)
                urgency = max(urgency, eval.severity)
                should_intervene = True
        
        # Get actions from failed criteria
        criterion_actions = self.get_actions_from_evaluations(evaluations)
        for action in criterion_actions:
            actions.append(action.reason)
        
        # === BUILT-IN CHECKS ===
        # Check execution success
        if not result.success:
            issues.append(f"Execution failed: {result.error}")
            actions.append("Retry with adjusted parameters")
            should_intervene = True
            urgency = max(urgency, 0.9)
        
        # Check confidence (if not already checked by criteria)
        elif trace.confidence < self.confidence_threshold:
            if not any("confidence" in issue.lower() for issue in issues):
                issues.append(f"Low confidence: {trace.confidence:.2f}")
                actions.append("Consider verification or deeper reasoning")
                urgency = max(urgency, 0.4)
        
        # Check resource efficiency
        expected_tokens = 1000  # Simple heuristic
        if trace.cost_tokens > expected_tokens * 2:
            if not any("token" in issue.lower() for issue in issues):
                issues.append(f"High token usage: {trace.cost_tokens}")
                actions.append("Optimize primitive expansion or use more efficient strategy")
                urgency = max(urgency, 0.2)
        
        if should_intervene:
            self.intervention_suggestions += 1
        
        health = 1.0 - (len(issues) * 0.3)
        
        return MetacognitiveAssessment(
            overall_health=max(0.0, health),
            confidence_in_assessment=0.85,
            detected_issues=issues,
            recommended_actions=actions,
            should_intervene=should_intervene,
            intervention_urgency=urgency,
            reasoning=f"Post-execution: {'success' if result.success else 'failure'}",
            metadata={"phase": "post-execution"}
        )
    
    def get_assessment(self) -> MetacognitiveAssessment:
        """
        Get current overall metacognitive assessment.
        
        Returns:
            Current assessment of cognitive health and recommendations
        """
        stats = self.get_stats()
        
        issues = []
        actions = []
        
        # Assess success rate
        if stats["success_rate"] < 0.7:
            issues.append(f"Success rate below target: {stats['success_rate']:.1%}")
            actions.append("Review execution strategies and parameters")
        
        # Assess confidence
        if stats["average_confidence"] < 0.65:
            issues.append(f"Average confidence low: {stats['average_confidence']:.2f}")
            actions.append("Increase quality thresholds or enable verification")
        
        # Assess intervention frequency
        if stats["total_executions"] > 0:
            intervention_rate = stats["intervention_suggestions"] / stats["total_executions"]
            if intervention_rate > 0.3:
                issues.append(f"High intervention rate: {intervention_rate:.1%}")
                actions.append("System may need parameter tuning")
        
        # Calculate health
        health_factors = [
            stats["success_rate"] * 0.4,
            stats["average_confidence"] * 0.4,
            (1.0 - min(0.3, stats["intervention_suggestions"] / max(1, stats["total_executions"]))) * 0.2
        ]
        overall_health = sum(health_factors)
        
        return MetacognitiveAssessment(
            overall_health=overall_health,
            confidence_in_assessment=0.8,
            detected_issues=issues,
            recommended_actions=actions,
            should_intervene=len(issues) > 0,
            intervention_urgency=0.5 if len(issues) > 0 else 0.0,
            reasoning=f"Overall assessment: {len(issues)} concerns detected",
            metadata={
                "health_grade": (
                    "excellent" if overall_health >= 0.9 else
                    "good" if overall_health >= 0.75 else
                    "fair" if overall_health >= 0.6 else
                    "poor"
                ),
                **stats
            }
        )
    
    def decide_next_actions(
        self,
        primitive_name: str,
        context: ExecutionContext,
        result: Optional[PrimitiveResult],
        assessment: Optional[MetacognitiveAssessment] = None,
        **kwargs
    ) -> List[tuple]:
        """
        Decide next actions based on metacognitive assessment.
        
        This is the CONTROL function of metacognition, complementing monitoring.
        Based on assessment of execution quality, decide whether to:
        - Retry with adjusted parameters
        - Refine the result
        - Add verification steps
        - Continue to next step
        
        Args:
            primitive_name: Name of primitive just executed
            context: Execution context
            result: Execution result (if any)
            assessment: Current metacognitive assessment (uses get_assessment if None)
            **kwargs: Original parameters
            
        Returns:
            List of (primitive_name, kwargs) tuples for next actions.
            Empty list means continue normally (no intervention).
        """
        if not result:
            return []
        
        # Use provided assessment or get current one
        if assessment is None:
            assessment = self.get_assessment()
        
        # Check if re-execution is needed
        should_retry = self._should_retry_execution(
            primitive_name,
            result,
            assessment,
            context,
            **kwargs
        )
        
        if should_retry:
            # Prepare updated parameters for retry
            retry_kwargs = self._prepare_retry_parameters(
                primitive_name,
                result,
                assessment,
                kwargs
            )
            logger.info(f"[METACOGNITION] Control decision: Re-execute '{primitive_name}'")
            return [(primitive_name, retry_kwargs)]
        
        return []
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get monitoring statistics.
        
        Returns:
            Dictionary of monitoring metrics
        """
        total = self.success_count + self.failure_count
        return {
            "monitoring_level": self.monitoring_level.value,
            "total_executions": total,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "success_rate": self.success_count / max(1, total),
            "average_confidence": (
                sum(self.confidence_trend) / len(self.confidence_trend)
                if self.confidence_trend else 0.0
            ),
            "intervention_suggestions": self.intervention_suggestions,
            "traces_stored": len(self.execution_traces),
        }
    
    def record_trace(self, trace: ExecutionTrace):
        """Record execution trace for analysis."""
        if self.monitoring_level == MonitoringLevel.NONE:
            return
        
        self.execution_traces.append(trace)
        
        # Keep last 100 traces
        if len(self.execution_traces) > 100:
            self.execution_traces.pop(0)
        
        # Update statistics
        if trace.success:
            self.success_count += 1
        else:
            self.failure_count += 1
        
        self.confidence_trend.append(trace.confidence)
        if len(self.confidence_trend) > 10:
            self.confidence_trend.pop(0)
    
    def register_criterion(self, criterion: MonitoringCriterion):
        """
        Register a monitoring criterion (with embedded action).
        
        Args:
            criterion: Criterion to register
        """
        # Check for duplicate IDs
        for existing in self.criteria:
            if existing.criterion_id == criterion.criterion_id:
                logger.warning(f"Replacing existing criterion: {criterion.criterion_id}")
                self.criteria.remove(existing)
                break
        
        self.criteria.append(criterion)
        # Sort by priority (highest first)
        self.criteria.sort(key=lambda c: c.priority, reverse=True)
        action_desc = f" with {criterion.action.action_type.value} action" if criterion.action else ""
        logger.info(f"Registered criterion: {criterion.criterion_id} (priority={criterion.priority}){action_desc}")
    
    def evaluate_criteria(
        self,
        primitive_name: str,
        context: ExecutionContext,
        criteria_type: CriteriaType,
        result: Optional[PrimitiveResult] = None,
        **kwargs
    ) -> List[CriteriaEvaluation]:
        """
        Evaluate all applicable criteria.
        
        Args:
            primitive_name: Name of primitive
            context: Execution context
            criteria_type: Type of criteria to evaluate
            result: Execution result (for post-execution)
            **kwargs: Primitive parameters
            
        Returns:
            List of criteria evaluations
        """
        evaluations = []
        
        for criterion in self.criteria:
            # Check if criterion applies
            if criterion.criteria_type != criteria_type:
                continue
            if not criterion.applies_to(primitive_name):
                continue
            
            # Evaluate criterion
            try:
                evaluation = criterion.evaluate(
                    primitive_name, context, result, **kwargs
                )
                evaluations.append(evaluation)
                
                if not evaluation.passed:
                    logger.debug(
                        f"[CRITERION] '{criterion.criterion_id}' failed: {evaluation.details}"
                    )
            except Exception as e:
                logger.error(f"[CRITERION] Error evaluating '{criterion.criterion_id}': {e}")
        
        return evaluations
    
    def get_actions_from_evaluations(
        self,
        evaluations: List[CriteriaEvaluation]
    ) -> List[TransitionAction]:
        """
        Get actions from failed criteria evaluations.
        
        Criteria are already sorted by priority, so actions will be
        returned in priority order.
        
        Args:
            evaluations: List of criteria evaluations
            
        Returns:
            List of actions to take (may be empty)
        """
        actions = []
        
        # Group evaluations by criterion for easy lookup
        eval_map = {e.criterion_id: e for e in evaluations}
        
        # Iterate through criteria in priority order
        for criterion in self.criteria:
            evaluation = eval_map.get(criterion.criterion_id)
            if not evaluation:
                continue
            
            # Get action if criterion failed
            action = criterion.get_action_if_failed(evaluation)
            if action:
                logger.info(
                    f"[CRITERION] '{criterion.criterion_id}' failed, "
                    f"triggering {action.action_type.value} action: {action.reason}"
                )
                actions.append(action)
                
                # For critical interventions, stop processing
                if criterion.priority >= 100:
                    break
        
        return actions
    
    def _should_retry_execution(
        self,
        primitive_name: str,
        result: PrimitiveResult,
        assessment: MetacognitiveAssessment,
        context: ExecutionContext,
        **kwargs
    ) -> bool:
        """
        Determine if execution should be retried based on metacognitive assessment.
        
        Args:
            primitive_name: Primitive that was executed
            result: Execution result
            assessment: Metacognitive assessment
            context: Execution context
            **kwargs: Original parameters
        
        Returns:
            True if execution should be retried
        """
        # Don't retry if execution failed completely
        if not result.success:
            return False
        
        # Check if intervention is recommended
        if not assessment.should_intervene:
            return False
        
        # Check intervention urgency
        if assessment.intervention_urgency < 0.5:
            return False  # Low urgency - don't retry
        
        # Check if already retried (prevent infinite loops)
        retry_count = kwargs.get('_retry_count', 0)
        max_retries = 2  # Maximum number of retries
        if retry_count >= max_retries:
            logger.warning(f"[METACOGNITION] Max retries ({max_retries}) reached for '{primitive_name}'")
            return False
        
        # Check if result confidence is too low
        if hasattr(result, 'confidence') and result.confidence:
            if result.confidence.overall < 0.6:
                logger.info(f"[METACOGNITION] Low confidence ({result.confidence.overall:.2f}) detected")
                return True
        
        # Check for specific issues that warrant retry
        detected_issues = assessment.detected_issues
        retry_keywords = ['low confidence', 'quality', 'uncertain', 'ambiguous']
        for issue in detected_issues:
            if any(keyword in issue.lower() for keyword in retry_keywords):
                return True
        
        return False
    
    def _prepare_retry_parameters(
        self,
        primitive_name: str,
        result: PrimitiveResult,
        assessment: MetacognitiveAssessment,
        original_kwargs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Prepare updated parameters for retry based on metacognitive recommendations.
        
        Args:
            primitive_name: Primitive to retry
            result: Previous execution result
            assessment: Metacognitive assessment
            original_kwargs: Original parameters
        
        Returns:
            Updated parameters for retry
        """
        # Start with original parameters
        retry_kwargs = original_kwargs.copy()
        
        # Increment retry counter
        retry_kwargs['_retry_count'] = retry_kwargs.get('_retry_count', 0) + 1
        
        # Apply recommended actions from metacognition
        recommended_actions = assessment.recommended_actions
        
        for action in recommended_actions:
            action_lower = action.lower()
            
            # Increase depth for deeper reasoning
            if 'depth' in action_lower or 'deeper' in action_lower:
                current_depth = retry_kwargs.get('depth', 0)
                retry_kwargs['depth'] = current_depth + 1
                logger.debug(f"[METACOGNITION] Increasing depth to {retry_kwargs['depth']}")
            
            # Add verification requirement
            if 'verify' in action_lower or 'validation' in action_lower:
                retry_kwargs['require_verification'] = True
                logger.debug(f"[METACOGNITION] Adding verification requirement")
            
            # Increase temperature for more creative responses
            if 'creative' in action_lower or 'alternative' in action_lower:
                retry_kwargs['temperature'] = 0.8
                logger.debug(f"[METACOGNITION] Increasing temperature for creativity")
            
            # Add previous result context
            if 'refine' in action_lower or 'improve' in action_lower:
                retry_kwargs['previous_result'] = result.content
                retry_kwargs['previous_confidence'] = result.confidence.overall if result.confidence else 0.0
                logger.debug(f"[METACOGNITION] Adding previous result context for refinement")
        
        # Store assessment for reference
        retry_kwargs['_metacognitive_feedback'] = {
            'reason': 'Low quality detected by metacognition',
            'issues': assessment.detected_issues,
            'recommendations': recommended_actions
        }
        
        return retry_kwargs
