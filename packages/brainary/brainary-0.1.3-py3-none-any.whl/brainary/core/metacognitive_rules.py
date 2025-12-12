"""
Metacognitive monitoring criteria and transition rules.

Provides a structured way to define:
1. Monitoring Criteria: Conditions to check during execution
2. Transition Rules: Actions to take when criteria are met

Example Use Cases:
- Content security check for memory operations
- Quality gates for reasoning depth
- Resource usage limits
- Domain-specific validation
"""

import logging
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod

from brainary.core.context import ExecutionContext
from brainary.primitive.base import PrimitiveResult

logger = logging.getLogger(__name__)


class CriteriaType(Enum):
    """Type of monitoring criteria."""
    PRE_EXECUTION = "pre_execution"    # Check before execution
    POST_EXECUTION = "post_execution"  # Check after execution
    CONTINUOUS = "continuous"          # Check throughout execution


class ActionType(Enum):
    """Type of intervention action."""
    FILTER = "filter"           # Filter/sanitize content
    REJECT = "reject"           # Reject execution entirely
    RETRY = "retry"             # Retry with modifications
    AUGMENT = "augment"         # Add additional steps
    WARN = "warn"               # Log warning, continue
    TRANSFORM = "transform"     # Transform parameters/result


@dataclass
class CriteriaEvaluation:
    """Result of evaluating a monitoring criterion."""
    criterion_id: str
    passed: bool
    severity: float  # 0.0-1.0 (how severe if failed)
    details: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TransitionAction:
    """Action to take based on criteria evaluation."""
    action_type: ActionType
    target_primitive: Optional[str] = None
    modified_params: Optional[Dict[str, Any]] = None
    filter_function: Optional[Callable] = None
    reason: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


class MonitoringCriterion(ABC):
    """
    Abstract base class for monitoring criteria.
    
    A criterion defines:
    1. WHAT to check (evaluation logic)
    2. WHEN to check (pre/post execution)
    3. WHERE to check (which primitives)
    4. WHAT TO DO if check fails (action)
    
    This merges the previous Criterion + Rule pattern into a single,
    more cohesive concept.
    """
    
    def __init__(
        self,
        criterion_id: str,
        criteria_type: CriteriaType,
        description: str,
        applicable_primitives: Optional[List[str]] = None,
        severity: float = 0.5,
        action: Optional[TransitionAction] = None,
        priority: int = 50
    ):
        """
        Initialize monitoring criterion.
        
        Args:
            criterion_id: Unique identifier for this criterion
            criteria_type: When to evaluate this criterion
            description: Human-readable description
            applicable_primitives: List of primitives this applies to (None = all)
            severity: Severity if criterion fails (0.0-1.0)
            action: Action to take when criterion fails (None = warn only)
            priority: Priority for action execution (higher = first)
        """
        self.criterion_id = criterion_id
        self.criteria_type = criteria_type
        self.description = description
        self.applicable_primitives = applicable_primitives
        self.severity = severity
        self.action = action
        self.priority = priority
    
    def applies_to(self, primitive_name: str) -> bool:
        """Check if criterion applies to given primitive."""
        if self.applicable_primitives is None:
            return True
        return primitive_name in self.applicable_primitives
    
    @abstractmethod
    def evaluate(
        self,
        primitive_name: str,
        context: ExecutionContext,
        result: Optional[PrimitiveResult] = None,
        **kwargs
    ) -> CriteriaEvaluation:
        """
        Evaluate the criterion.
        
        Args:
            primitive_name: Name of primitive being executed
            context: Execution context
            result: Execution result (for post-execution criteria)
            **kwargs: Primitive parameters
            
        Returns:
            CriteriaEvaluation with pass/fail and details
        """
        pass
    
    def get_action_if_failed(self, evaluation: CriteriaEvaluation) -> Optional[TransitionAction]:
        """
        Get action to take if criterion failed.
        
        Args:
            evaluation: The failed evaluation result
            
        Returns:
            TransitionAction if action defined, else None
        """
        if not evaluation.passed and self.action:
            return self.action
        return None


class TransitionRule:
    """
    A transition rule defines what action to take when criteria are met.
    
    Format: IF <condition> THEN <action>
    """
    
    def __init__(
        self,
        rule_id: str,
        description: str,
        condition: Callable[[List[CriteriaEvaluation]], bool],
        action: TransitionAction,
        priority: int = 0
    ):
        """
        Initialize transition rule.
        
        Args:
            rule_id: Unique identifier for this rule
            description: Human-readable description
            condition: Function that checks if rule should fire
            action: Action to take if condition is met
            priority: Priority (higher = evaluated first)
        """
        self.rule_id = rule_id
        self.description = description
        self.condition = condition
        self.action = action
        self.priority = priority
        self.activation_count = 0
    
    def evaluate(
        self,
        evaluations: List[CriteriaEvaluation]
    ) -> Optional[TransitionAction]:
        """
        Evaluate rule condition and return action if triggered.
        
        Args:
            evaluations: List of criteria evaluations
            
        Returns:
            TransitionAction if rule fires, None otherwise
        """
        try:
            if self.condition(evaluations):
                self.activation_count += 1
                logger.debug(f"[RULE] '{self.rule_id}' activated (count: {self.activation_count})")
                return self.action
        except Exception as e:
            logger.error(f"[RULE] Error evaluating '{self.rule_id}': {e}")
        
        return None


# ============================================================================
# Built-in Criteria Examples
# ============================================================================

class ContentSecurityCriterion(MonitoringCriterion):
    """Check for security issues in content (e.g., PII, sensitive data)."""
    
    def __init__(
        self,
        criterion_id: str = "content_security",
        applicable_primitives: Optional[List[str]] = None,
        patterns: Optional[List[str]] = None,
        priority: int = 100
    ):
        # Simple pattern matching (can be enhanced with ML models)
        self.patterns = patterns or [
            r'\b\d{3}-\d{2}-\d{4}\b',  # SSN pattern
            r'\b\d{16}\b',              # Credit card pattern
            r'password\s*[:=]',         # Password in text
            r'api[_-]?key\s*[:=]',      # API keys
            r'(auth|token)\s*[:=]',     # Auth tokens
        ]
        
        # Define filter function for redacting sensitive data
        def filter_sensitive_content(content: str) -> str:
            """Redact sensitive patterns from content."""
            import re
            filtered = content
            filtered = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN-REDACTED]', filtered)
            filtered = re.sub(r'\b\d{16}\b', '[CC-REDACTED]', filtered)
            filtered = re.sub(r'(password|api[_-]?key|auth|token)\s*[:=]\s*\S+', 
                            r'\1=[REDACTED]', filtered, flags=re.IGNORECASE)
            return filtered
        
        # Create action that filters content when security issues detected
        security_action = TransitionAction(
            action_type=ActionType.FILTER,
            filter_function=filter_sensitive_content,
            reason="Security criterion failed - filtering sensitive content",
            metadata={"patterns": self.patterns}
        )
        
        super().__init__(
            criterion_id=criterion_id,
            criteria_type=CriteriaType.PRE_EXECUTION,
            description="Check content for security issues",
            applicable_primitives=applicable_primitives or ["remember", "store"],
            severity=0.9,
            action=security_action,
            priority=priority
        )
    
    def evaluate(
        self,
        primitive_name: str,
        context: ExecutionContext,
        result: Optional[PrimitiveResult] = None,
        **kwargs
    ) -> CriteriaEvaluation:
        """Check for sensitive content."""
        import re
        
        # Check in parameters
        content_to_check = []
        if 'content' in kwargs:
            content_to_check.append(str(kwargs['content']))
        if 'text' in kwargs:
            content_to_check.append(str(kwargs['text']))
        if 'data' in kwargs:
            content_to_check.append(str(kwargs['data']))
        
        detected_issues = []
        for content in content_to_check:
            for pattern in self.patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    detected_issues.append(f"Potential sensitive data: {pattern}")
        
        passed = len(detected_issues) == 0
        
        return CriteriaEvaluation(
            criterion_id=self.criterion_id,
            passed=passed,
            severity=self.severity if not passed else 0.0,
            details=(
                "Content security check passed"
                if passed
                else f"Security issues detected: {', '.join(detected_issues)}"
            ),
            metadata={"patterns_checked": len(self.patterns)}
        )


class ConfidenceThresholdCriterion(MonitoringCriterion):
    """Check if execution confidence meets threshold."""
    
    def __init__(
        self,
        criterion_id: str = "confidence_threshold",
        threshold: float = 0.7,
        applicable_primitives: Optional[List[str]] = None,
        max_retries: int = 3,
        priority: int = 50
    ):
        self.threshold = threshold
        self.max_retries = max_retries
        
        # Create action that retries on low confidence
        retry_action = TransitionAction(
            action_type=ActionType.RETRY,
            reason=f"Confidence below threshold ({threshold})",
            metadata={"max_retries": max_retries, "threshold": threshold}
        )
        
        super().__init__(
            criterion_id=criterion_id,
            criteria_type=CriteriaType.POST_EXECUTION,
            description=f"Check confidence >= {threshold}",
            applicable_primitives=applicable_primitives,
            severity=0.5,
            action=retry_action,
            priority=priority
        )
    
    def evaluate(
        self,
        primitive_name: str,
        context: ExecutionContext,
        result: Optional[PrimitiveResult] = None,
        **kwargs
    ) -> CriteriaEvaluation:
        """Check confidence level."""
        if not result or not result.confidence:
            return CriteriaEvaluation(
                criterion_id=self.criterion_id,
                passed=False,
                severity=0.3,
                details="No confidence score available",
                metadata={}
            )
        
        confidence = result.confidence.overall
        passed = confidence >= self.threshold
        
        return CriteriaEvaluation(
            criterion_id=self.criterion_id,
            passed=passed,
            severity=self.severity if not passed else 0.0,
            details=(
                f"Confidence {confidence:.2f} >= {self.threshold:.2f}"
                if passed
                else f"Confidence {confidence:.2f} < {self.threshold:.2f}"
            ),
            metadata={"confidence": confidence, "threshold": self.threshold}
        )


class ResourceLimitCriterion(MonitoringCriterion):
    """Check if resource usage is within limits."""
    
    def __init__(
        self,
        criterion_id: str = "resource_limit",
        max_tokens: Optional[int] = None,
        max_time_ms: Optional[float] = None,
        priority: int = 10
    ):
        self.max_tokens = max_tokens
        self.max_time_ms = max_time_ms
        
        # Create action that warns on resource excess
        warn_action = TransitionAction(
            action_type=ActionType.WARN,
            reason="Resource limits exceeded",
            metadata={"max_tokens": max_tokens, "max_time_ms": max_time_ms}
        )
        
        super().__init__(
            criterion_id=criterion_id,
            criteria_type=CriteriaType.POST_EXECUTION,
            description="Check resource usage within limits",
            applicable_primitives=None,
            severity=0.4,
            action=warn_action,
            priority=priority
        )
    
    def evaluate(
        self,
        primitive_name: str,
        context: ExecutionContext,
        result: Optional[PrimitiveResult] = None,
        **kwargs
    ) -> CriteriaEvaluation:
        """Check resource usage."""
        if not result or not result.cost:
            return CriteriaEvaluation(
                criterion_id=self.criterion_id,
                passed=True,
                severity=0.0,
                details="No cost data available",
                metadata={}
            )
        
        issues = []
        
        if self.max_tokens and result.cost.tokens > self.max_tokens:
            issues.append(
                f"Token usage {result.cost.tokens} > limit {self.max_tokens}"
            )
        
        if self.max_time_ms and result.cost.latency_ms > self.max_time_ms:
            issues.append(
                f"Latency {result.cost.latency_ms:.0f}ms > limit {self.max_time_ms:.0f}ms"
            )
        
        passed = len(issues) == 0
        
        return CriteriaEvaluation(
            criterion_id=self.criterion_id,
            passed=passed,
            severity=self.severity if not passed else 0.0,
            details=(
                "Resource usage within limits"
                if passed
                else "; ".join(issues)
            ),
            metadata={
                "tokens": result.cost.tokens,
                "latency_ms": result.cost.latency_ms
            }
        )


# ============================================================================
# Rule Builder Utilities
# ============================================================================

def create_security_filter_rule(
    criterion_id: str = "content_security",
    filter_func: Optional[Callable] = None
) -> TransitionRule:
    """
    Create a rule that filters content when security issues detected.
    
    Args:
        criterion_id: ID of security criterion to check
        filter_func: Function to sanitize content
        
    Returns:
        TransitionRule that filters insecure content
    """
    def condition(evals: List[CriteriaEvaluation]) -> bool:
        for e in evals:
            if e.criterion_id == criterion_id and not e.passed:
                return True
        return False
    
    def default_filter(content: str) -> str:
        """Simple filter that removes common sensitive patterns."""
        import re
        filtered = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN-REDACTED]', content)
        filtered = re.sub(r'\b\d{16}\b', '[CC-REDACTED]', filtered)
        filtered = re.sub(r'password\s*[:=]\s*\S+', 'password=[REDACTED]', filtered, flags=re.IGNORECASE)
        return filtered
    
    return TransitionRule(
        rule_id="security_filter",
        description="Filter content when security issues detected",
        condition=condition,
        action=TransitionAction(
            action_type=ActionType.FILTER,
            filter_function=filter_func or default_filter,
            reason="Security criterion failed - filtering sensitive content"
        ),
        priority=100  # High priority
    )


def create_low_confidence_retry_rule(
    criterion_id: str = "confidence_threshold",
    max_retries: int = 2
) -> TransitionRule:
    """
    Create a rule that retries when confidence is low.
    
    Args:
        criterion_id: ID of confidence criterion
        max_retries: Maximum retry attempts
        
    Returns:
        TransitionRule that retries on low confidence
    """
    def condition(evals: List[CriteriaEvaluation]) -> bool:
        for e in evals:
            if e.criterion_id == criterion_id and not e.passed:
                # Check retry count in metadata
                retry_count = e.metadata.get('_retry_count', 0)
                return retry_count < max_retries
        return False
    
    return TransitionRule(
        rule_id="low_confidence_retry",
        description="Retry execution when confidence is low",
        condition=condition,
        action=TransitionAction(
            action_type=ActionType.RETRY,
            modified_params={'depth': 2},  # Increase depth on retry
            reason="Confidence below threshold - retry with deeper reasoning"
        ),
        priority=50
    )


def create_resource_limit_warning_rule(
    criterion_id: str = "resource_limit"
) -> TransitionRule:
    """
    Create a rule that warns when resource limits exceeded.
    
    Args:
        criterion_id: ID of resource limit criterion
        
    Returns:
        TransitionRule that logs warning
    """
    def condition(evals: List[CriteriaEvaluation]) -> bool:
        for e in evals:
            if e.criterion_id == criterion_id and not e.passed:
                return True
        return False
    
    return TransitionRule(
        rule_id="resource_limit_warning",
        description="Warn when resource limits exceeded",
        condition=condition,
        action=TransitionAction(
            action_type=ActionType.WARN,
            reason="Resource usage exceeds configured limits"
        ),
        priority=10  # Low priority
    )
