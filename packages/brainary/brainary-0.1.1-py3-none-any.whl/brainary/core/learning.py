"""
Learning and adaptation system for Brainary.

Implements continuous learning from execution traces, pattern extraction,
knowledge promotion, and experience accumulation.

The learning system follows a three-layer architecture:
1. Experience Layer: Fast O(1) lookups from execution history
2. Knowledge Layer: Extracted rules and patterns
3. LLM Layer: Reasoning for novel situations

The system evolves from LLM-dependent (80%) to experience-driven (95%+).
"""

import time
import logging
from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from collections import defaultdict
from enum import Enum
import threading

from brainary.primitive.base import PrimitiveResult, CostMetrics
from brainary.core.context import ExecutionContext

logger = logging.getLogger(__name__)


class LearningEventType(Enum):
    """Types of learning events."""
    EXECUTION_SUCCESS = "execution_success"
    EXECUTION_FAILURE = "execution_failure"
    ROUTING_DECISION = "routing_decision"
    RESOURCE_ALLOCATION = "resource_allocation"
    ERROR_RECOVERY = "error_recovery"
    PATTERN_DETECTED = "pattern_detected"
    OPTIMIZATION_APPLIED = "optimization_applied"


@dataclass
class LearningEvent:
    """Event for learning system."""
    
    event_type: LearningEventType
    timestamp: float
    context: ExecutionContext
    primitive_name: str
    implementation_used: str
    parameters: Dict[str, Any]
    result: Optional[PrimitiveResult]
    outcome: str  # 'success', 'failure', 'partial'
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def compute_signature(self) -> str:
        """Compute signature for this event."""
        sig_parts = [
            self.primitive_name,
            self.context.domain or "default",
            str(self.context.execution_mode.value),
            str(sorted(self.parameters.keys())),
        ]
        return "|".join(sig_parts)


@dataclass
class ExperienceRecord:
    """Cached execution experience."""
    
    signature: str
    primitive_name: str
    implementation: str
    parameters: Dict[str, Any]
    context_features: Dict[str, Any]
    
    # Success metrics
    execution_count: int = 0
    success_count: int = 0
    failure_count: int = 0
    
    # Performance metrics
    total_cost: CostMetrics = field(default_factory=lambda: CostMetrics(0, 0, 0, 0.0))
    average_confidence: float = 0.0
    average_latency_ms: float = 0.0
    
    # Metadata
    first_seen: float = field(default_factory=time.time)
    last_used: float = field(default_factory=time.time)
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate."""
        if self.execution_count == 0:
            return 0.0
        return self.success_count / self.execution_count
    
    def update_from_result(self, result: PrimitiveResult, latency_ms: float) -> None:
        """Update metrics from execution result."""
        self.execution_count += 1
        self.last_used = time.time()
        
        if result.success:
            self.success_count += 1
        else:
            self.failure_count += 1
        
        # Update averages (exponential moving average)
        alpha = 0.2  # Learning rate
        self.average_confidence = (
            alpha * result.confidence.overall +
            (1 - alpha) * self.average_confidence
        )
        self.average_latency_ms = (
            alpha * latency_ms +
            (1 - alpha) * self.average_latency_ms
        )
        
        # Accumulate costs
        self.total_cost.tokens += result.cost.tokens
        self.total_cost.latency_ms += result.cost.latency_ms
        self.total_cost.memory_slots += result.cost.memory_slots


@dataclass
class KnowledgeRule:
    """Extracted knowledge rule."""
    
    rule_id: str
    rule_type: str  # 'routing', 'optimization', 'recovery'
    condition: Dict[str, Any]  # When to apply
    action: Dict[str, Any]  # What to do
    confidence: float  # Rule confidence [0-1]
    
    # Evidence
    supporting_examples: int = 0
    counter_examples: int = 0
    
    # Metadata
    created_at: float = field(default_factory=time.time)
    last_validated: float = field(default_factory=time.time)
    
    @property
    def strength(self) -> float:
        """Calculate rule strength."""
        if self.supporting_examples == 0:
            return 0.0
        total = self.supporting_examples + self.counter_examples
        return self.supporting_examples / total * self.confidence


@dataclass
class Pattern:
    """Detected execution pattern."""
    
    pattern_id: str
    pattern_type: str  # 'sequence', 'optimization', 'anti-pattern'
    description: str
    frequency: int = 0
    
    # Pattern definition
    conditions: List[Dict[str, Any]] = field(default_factory=list)
    actions: List[Dict[str, Any]] = field(default_factory=list)
    
    # Metrics
    detected_at: float = field(default_factory=time.time)
    last_seen: float = field(default_factory=time.time)


class ExperienceCache:
    """
    Experience cache for fast O(1) routing decisions.
    
    Caches successful execution patterns for instant replay.
    """
    
    def __init__(self, max_size: int = 10000):
        """
        Initialize experience cache.
        
        Args:
            max_size: Maximum cache entries
        """
        self.max_size = max_size
        self._cache: Dict[str, ExperienceRecord] = {}
        self._access_frequency: Dict[str, int] = defaultdict(int)
        self._lock = threading.RLock()
    
    def lookup(self, signature: str) -> Optional[ExperienceRecord]:
        """
        Look up cached experience.
        
        Args:
            signature: Context signature
        
        Returns:
            ExperienceRecord if found, None otherwise
        """
        with self._lock:
            if signature in self._cache:
                self._access_frequency[signature] += 1
                return self._cache[signature]
            return None
    
    def store(self, record: ExperienceRecord) -> None:
        """
        Store experience record.
        
        Args:
            record: ExperienceRecord to store
        """
        with self._lock:
            # Check cache size
            if len(self._cache) >= self.max_size:
                self._evict_lru()
            
            self._cache[record.signature] = record
            self._access_frequency[record.signature] = 1
    
    def update(self, signature: str, result: PrimitiveResult, latency_ms: float) -> None:
        """
        Update existing record with new execution result.
        
        Args:
            signature: Context signature
            result: Execution result
            latency_ms: Execution latency
        """
        with self._lock:
            if signature in self._cache:
                self._cache[signature].update_from_result(result, latency_ms)
    
    def _evict_lru(self) -> None:
        """Evict least recently used entry."""
        if not self._cache:
            return
        
        # Find LRU entry
        lru_sig = min(
            self._cache.keys(),
            key=lambda sig: (
                self._access_frequency[sig],
                self._cache[sig].last_used
            )
        )
        
        del self._cache[lru_sig]
        del self._access_frequency[lru_sig]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self._lock:
            return {
                'size': len(self._cache),
                'max_size': self.max_size,
                'total_executions': sum(r.execution_count for r in self._cache.values()),
                'average_success_rate': (
                    sum(r.success_rate for r in self._cache.values()) / 
                    max(1, len(self._cache))
                ),
            }


class LearningSystem:
    """
    Continuous learning system.
    
    Learns from execution traces to:
    1. Build experience cache for fast routing
    2. Extract knowledge rules from patterns
    3. Optimize resource allocation
    4. Improve error recovery strategies
    """
    
    def __init__(self):
        """Initialize learning system."""
        self.experience_cache = ExperienceCache()
        self.knowledge_rules: Dict[str, KnowledgeRule] = {}
        self.patterns: Dict[str, Pattern] = {}
        self.events: List[LearningEvent] = []
        
        # Learning configuration
        self.pattern_detection_threshold = 3  # Min frequency to detect pattern
        self.rule_confidence_threshold = 0.7  # Min confidence to apply rule
        self.learning_rate = 0.1  # How fast to adapt
        
        # Statistics
        self.total_events = 0
        self.patterns_detected = 0
        self.rules_extracted = 0
        
        self._lock = threading.RLock()
    
    def record_event(self, event: LearningEvent) -> None:
        """
        Record learning event.
        
        Args:
            event: LearningEvent to record
        """
        with self._lock:
            self.events.append(event)
            self.total_events += 1
            
            # Update experience cache
            if event.outcome == 'success' and event.result:
                signature = event.compute_signature()
                
                existing = self.experience_cache.lookup(signature)
                if existing:
                    # Update existing
                    latency = event.metadata.get('latency_ms', 0)
                    self.experience_cache.update(signature, event.result, latency)
                else:
                    # Create new
                    record = ExperienceRecord(
                        signature=signature,
                        primitive_name=event.primitive_name,
                        implementation=event.implementation_used,
                        parameters=event.parameters,
                        context_features={
                            'domain': event.context.domain,
                            'execution_mode': event.context.execution_mode.value,
                            'quality_threshold': event.context.quality_threshold,
                        },
                    )
                    record.update_from_result(
                        event.result,
                        event.metadata.get('latency_ms', 0)
                    )
                    self.experience_cache.store(record)
            
            # Trigger pattern detection periodically
            if len(self.events) % 100 == 0:
                self._detect_patterns()
    
    def lookup_experience(
        self,
        primitive_name: str,
        context: ExecutionContext,
        parameters: Dict[str, Any]
    ) -> Optional[ExperienceRecord]:
        """
        Look up cached experience.
        
        Args:
            primitive_name: Name of primitive
            context: Execution context
            parameters: Primitive parameters
        
        Returns:
            ExperienceRecord if found, None otherwise
        """
        # Compute signature
        sig_parts = [
            primitive_name,
            context.domain or "default",
            str(context.execution_mode.value),
            str(sorted(parameters.keys())),
        ]
        signature = "|".join(sig_parts)
        
        return self.experience_cache.lookup(signature)
    
    def get_applicable_rules(
        self,
        context: ExecutionContext,
        rule_type: Optional[str] = None
    ) -> List[KnowledgeRule]:
        """
        Get rules applicable to context.
        
        Args:
            context: Execution context
            rule_type: Optional rule type filter
        
        Returns:
            List of applicable rules
        """
        with self._lock:
            applicable = []
            
            for rule in self.knowledge_rules.values():
                # Filter by type
                if rule_type and rule.rule_type != rule_type:
                    continue
                
                # Check confidence threshold
                if rule.strength < self.rule_confidence_threshold:
                    continue
                
                # Check conditions (simplified)
                if self._rule_matches_context(rule, context):
                    applicable.append(rule)
            
            # Sort by strength
            applicable.sort(key=lambda r: r.strength, reverse=True)
            return applicable
    
    def _rule_matches_context(
        self,
        rule: KnowledgeRule,
        context: ExecutionContext
    ) -> bool:
        """Check if rule conditions match context."""
        conditions = rule.condition
        
        # Check domain
        if 'domain' in conditions:
            if conditions['domain'] != context.domain:
                return False
        
        # Check execution mode
        if 'execution_mode' in conditions:
            if conditions['execution_mode'] != context.execution_mode.value:
                return False
        
        # Check quality threshold
        if 'min_quality' in conditions:
            if context.quality_threshold < conditions['min_quality']:
                return False
        
        return True
    
    def _detect_patterns(self) -> None:
        """Detect patterns in recent events."""
        # Analyze recent events for patterns
        recent_events = self.events[-1000:]  # Last 1000 events
        
        # Group by primitive
        by_primitive = defaultdict(list)
        for event in recent_events:
            by_primitive[event.primitive_name].append(event)
        
        # Look for high-frequency patterns
        for primitive, events in by_primitive.items():
            if len(events) >= self.pattern_detection_threshold:
                # Detect common parameter patterns
                param_patterns = defaultdict(int)
                for event in events:
                    param_sig = str(sorted(event.parameters.keys()))
                    param_patterns[param_sig] += 1
                
                # Create pattern for frequent combinations
                for param_sig, freq in param_patterns.items():
                    if freq >= self.pattern_detection_threshold:
                        pattern_id = f"{primitive}_{hash(param_sig)}"
                        if pattern_id not in self.patterns:
                            pattern = Pattern(
                                pattern_id=pattern_id,
                                pattern_type="sequence",
                                description=f"Common pattern for {primitive}",
                                frequency=freq,
                            )
                            self.patterns[pattern_id] = pattern
                            self.patterns_detected += 1
                            
                            logger.info(
                                f"Detected pattern {pattern_id} "
                                f"(frequency: {freq})"
                            )
    
    def extract_knowledge(self) -> int:
        """
        Extract knowledge rules from experience.
        
        Returns:
            Number of new rules extracted
        """
        with self._lock:
            initial_count = len(self.knowledge_rules)
            
            # Analyze experience cache for patterns
            records = list(self.experience_cache._cache.values())
            
            # Group by primitive
            by_primitive = defaultdict(list)
            for record in records:
                if record.success_rate > 0.8 and record.execution_count >= 5:
                    by_primitive[record.primitive_name].append(record)
            
            # Extract routing rules
            for primitive, successful_records in by_primitive.items():
                # Find best implementation for each domain
                by_domain = defaultdict(list)
                for record in successful_records:
                    domain = record.context_features.get('domain', 'default')
                    by_domain[domain].append(record)
                
                for domain, domain_records in by_domain.items():
                    if len(domain_records) >= 3:
                        # Find best implementation
                        best = max(
                            domain_records,
                            key=lambda r: (r.success_rate, -r.average_latency_ms)
                        )
                        
                        rule_id = f"routing_{primitive}_{domain}"
                        if rule_id not in self.knowledge_rules:
                            rule = KnowledgeRule(
                                rule_id=rule_id,
                                rule_type="routing",
                                condition={
                                    'primitive': primitive,
                                    'domain': domain,
                                },
                                action={
                                    'implementation': best.implementation,
                                },
                                confidence=best.success_rate,
                                supporting_examples=best.execution_count,
                            )
                            self.knowledge_rules[rule_id] = rule
                            logger.info(f"Extracted rule: {rule_id}")
            
            new_rules = len(self.knowledge_rules) - initial_count
            self.rules_extracted += new_rules
            return new_rules
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get learning system statistics.
        
        Returns:
            Dictionary of statistics
        """
        with self._lock:
            return {
                'total_events': self.total_events,
                'experience_cache': self.experience_cache.get_stats(),
                'knowledge_rules': len(self.knowledge_rules),
                'patterns_detected': self.patterns_detected,
                'rules_extracted': self.rules_extracted,
                'event_types': defaultdict(int, {
                    event.event_type.value: 1
                    for event in self.events[-1000:]
                }),
            }


# Global learning system singleton
_global_learning_system: Optional[LearningSystem] = None
_learning_system_lock = threading.Lock()


def get_learning_system() -> LearningSystem:
    """
    Get global learning system.
    
    Returns:
        Singleton LearningSystem instance
    """
    global _global_learning_system
    
    if _global_learning_system is None:
        with _learning_system_lock:
            if _global_learning_system is None:
                _global_learning_system = LearningSystem()
    
    return _global_learning_system
