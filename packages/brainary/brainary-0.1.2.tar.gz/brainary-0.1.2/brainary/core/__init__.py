"""
Core runtime components for Brainary cognitive system.

This module contains the cognitive kernel (with integrated metacognitive monitoring),
scheduler, resource manager, and other core runtime components.

The metacognitive monitor is a pluggable component of the cognitive kernel that
can be customized or disabled as needed.
"""

from brainary.core.context import (
    ExecutionContext,
    ExecutionMode,
    create_execution_context,
)
from brainary.core.kernel import CognitiveKernel
from brainary.core.metacognitive_monitor import (
    MetacognitiveMonitor,
    MonitoringLevel,
    ExecutionTrace,
    MetacognitiveAssessment,
)
from brainary.core.scheduler import ProgramScheduler
from brainary.core.resource_manager import ResourceManager, ResourceEstimate

__all__ = [
    "ExecutionContext",
    "ExecutionMode",
    "create_execution_context",
    "CognitiveKernel",
    "MetacognitiveMonitor",
    "MonitoringLevel",
    "ExecutionTrace",
    "MetacognitiveAssessment",
    "ProgramScheduler",
    "ResourceManager",
    "ResourceEstimate",
]
