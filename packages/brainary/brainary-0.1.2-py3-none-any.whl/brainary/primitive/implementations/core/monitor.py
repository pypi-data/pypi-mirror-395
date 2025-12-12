"""
Track system or process state.
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


class MonitorState(CorePrimitive):
    """
    Track system or process state.
    
    Monitors metrics, status, and changes over time.
    """
    
    def __init__(self):
        """Initialize primitive."""
        super().__init__()
        self._name = "monitor"
        self._hint = (
            "Use to track system state, process metrics, or execution progress. "
            "Best for observability, debugging, and performance monitoring. "
            "Suitable for all domains. Use when you need to observe system "
            "behavior, track changes over time, collect metrics, or maintain "
            "awareness of process status. Provides snapshots and trends."
        )
    
    def execute(
        self,
        context: ExecutionContext,
        working_memory: WorkingMemory,
        target: str,
        metrics: List[str] = None,
        interval_ms: int = 1000,
        **kwargs
    ) -> PrimitiveResult:
        """
        Monitor state with LLM-powered analysis and anomaly detection.
        
        Args:
            context: Execution context
            working_memory: Working memory
            target: What to monitor (system, process, metric)
            metrics: List of metrics to track
            interval_ms: Monitoring interval
            **kwargs: Additional parameters (current_values, thresholds)
        
        Returns:
            PrimitiveResult with monitoring analysis
        """
        start_time = time.time()
        
        try:
            metrics = metrics or ["status", "health", "performance"]
            
            # Get current metric values if provided
            current_values = kwargs.get('current_values', {})
            thresholds = kwargs.get('thresholds', {})
            
            # Retrieve monitoring history from memory
            memory_items = working_memory.retrieve(
                query=f"monitor {target} metrics",
                top_k=5
            )
            memory_context = "\n".join([f"- {item.content}" for item in memory_items])
            
            # Format metrics
            metrics_text = "\n".join(f"- {m}" for m in metrics)
            
            # Format current values
            values_text = ""
            if current_values:
                values_text = "\n\nCURRENT VALUES:\n" + "\n".join(
                    f"- {k}: {v}" for k, v in current_values.items()
                )
            
            # Format thresholds
            thresholds_text = ""
            if thresholds:
                thresholds_text = "\n\nTHRESHOLDS:\n" + "\n".join(
                    f"- {k}: {v}" for k, v in thresholds.items()
                )
            
            # Build monitoring analysis prompt
            prompt = f"""Analyze the current state and metrics of the following monitoring target.

TARGET: {target}

METRICS TO MONITOR:
{metrics_text}{values_text}{thresholds_text}

MONITORING HISTORY:
{memory_context if memory_context else "No prior monitoring data"}

MONITORING INTERVAL: Every {interval_ms}ms

Provide comprehensive monitoring analysis with:

1. STATE ASSESSMENT: Overall health and status of the target
2. METRIC ANALYSIS: Analyze each metric's current state and trends
3. ANOMALY DETECTION: Identify any unusual patterns or threshold violations
4. TREND ANALYSIS: Describe any trends (improving, degrading, stable)
5. ALERTS: List any immediate concerns or alerts that need attention
6. RECOMMENDATIONS: Suggest actions if issues detected or optimization opportunities

Be specific about metric values and highlight any concerns."""

            # Get LLM monitoring analysis
            llm_manager = get_llm_manager()
            response = llm_manager.request(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,  # Low temperature for factual analysis
            )
            
            analysis_text = response.content
            
            # Parse sections
            sections = {}
            section_names = ["STATE ASSESSMENT:", "METRIC ANALYSIS:", "ANOMALY DETECTION:", 
                           "TREND ANALYSIS:", "ALERTS:", "RECOMMENDATIONS:"]
            for i, section_name in enumerate(section_names):
                start_idx = analysis_text.find(section_name)
                if start_idx == -1:
                    sections[section_name.rstrip(':')] = ""
                    continue
                
                end_idx = len(analysis_text)
                for next_section in section_names[i+1:]:
                    next_idx = analysis_text.find(next_section)
                    if next_idx != -1:
                        end_idx = next_idx
                        break
                
                sections[section_name.rstrip(':')] = analysis_text[start_idx+len(section_name):end_idx].strip()
            
            # Detect alerts
            alerts_text = sections.get('ALERTS', '').lower()
            has_alerts = bool(alerts_text and alerts_text.strip() and 'none' not in alerts_text and 'no alert' not in alerts_text)
            
            # Assess overall health
            state_text = sections.get('STATE ASSESSMENT', '').lower()
            if 'healthy' in state_text or 'normal' in state_text or 'good' in state_text:
                health_status = 'healthy'
            elif 'warning' in state_text or 'concern' in state_text:
                health_status = 'warning'
            elif 'critical' in state_text or 'failed' in state_text or 'error' in state_text:
                health_status = 'critical'
            else:
                health_status = 'unknown'
            
            snapshot = {
                'target': target,
                'timestamp': time.time(),
                'metrics': metrics,
                'current_values': current_values,
                'interval_ms': interval_ms,
                'health_status': health_status,
                'state_assessment': sections.get('STATE ASSESSMENT', ''),
                'metric_analysis': sections.get('METRIC ANALYSIS', ''),
                'anomaly_detection': sections.get('ANOMALY DETECTION', ''),
                'trend_analysis': sections.get('TREND ANALYSIS', ''),
                'alerts': sections.get('ALERTS', ''),
                'recommendations': sections.get('RECOMMENDATIONS', ''),
                'has_alerts': has_alerts,
            }
            
            # Store monitoring snapshot in memory
            importance = 0.8 if has_alerts else 0.6
            working_memory.store(
                content=f"Monitor {target}: {health_status} ({'ALERTS' if has_alerts else 'no alerts'})",
                importance=importance,
                tags=["monitoring", target, health_status],
            )
            
            execution_time = int((time.time() - start_time) * 1000)
            
            return PrimitiveResult(
                content=snapshot,
                confidence=ConfidenceMetrics(
                    overall=0.9,
                    reasoning=0.92,
                    completeness=0.9,
                    consistency=0.9,
                    evidence_strength=0.88,
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
                    'target': target,
                    'metric_count': len(metrics),
                    'health_status': health_status,
                    'has_alerts': has_alerts,
                    'model': 'gpt-4o-mini',
                }
            )
            
        except Exception as e:
            logger.error(f"Monitoring failed: {e}")
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
        metrics = kwargs.get('metrics', ["status"])
        return ResourceEstimate(
            tokens=0,
            time_ms=5,
            memory_items=1,
            complexity=0.2,
        )
    
    def validate_inputs(self, **kwargs) -> None:
        """Validate inputs for execution."""
        if "target" not in kwargs:
            raise ValueError("'target' parameter required")
    
    def matches_context(self, context: ExecutionContext, **kwargs) -> float:
        """Check context match."""
        return 1.0  # Always available
    
    def rollback(self, context: ExecutionContext) -> None:
        """Rollback - monitoring is read-only, no side effects to undo."""
        pass


