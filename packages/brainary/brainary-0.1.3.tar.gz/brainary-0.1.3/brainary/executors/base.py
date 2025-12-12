"""
Executor system for Brainary.

Provides base classes and implementations for different execution strategies
that run primitives and execution payloads.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from brainary.primitive.base import Primitive, PrimitiveResult, ResourceEstimate
    from brainary.core.context import ExecutionContext
    from brainary.memory.working import WorkingMemory


@dataclass
class ExecutionPayload:
    """
    Unified structure wrapping primitives with augmentations.
    
    The payload is the fundamental unit of execution, combining:
    - Pre-augmentations: Support operations before main execution
    - Target primitive: The core operation to execute
    - Post-augmentations: Support operations after main execution
    - Meta-cognitive injections: Monitoring and control operations
    
    Executors receive payloads and determine optimal execution strategy.
    """
    
    # Core primitive
    target_primitive: 'Primitive'
    target_params: Dict[str, Any] = field(default_factory=dict)
    
    # Augmentations
    pre_augmentations: List['Primitive'] = field(default_factory=list)
    post_augmentations: List['Primitive'] = field(default_factory=list)
    
    # Meta-cognitive injections
    monitoring_primitives: List['Primitive'] = field(default_factory=list)
    control_primitives: List['Primitive'] = field(default_factory=list)
    
    # Metadata
    payload_id: str = ""
    complexity: float = 0.5  # Estimated complexity (0.0-1.0)
    estimated_cost: Optional['ResourceEstimate'] = None
    requires_verification: bool = False
    requires_state_management: bool = False
    
    def compute_total_complexity(self) -> float:
        """
        Compute total payload complexity.
        
        Returns:
            Complexity score (0.0-1.0)
        """
        # Base complexity from target
        total = self.complexity
        
        # Add complexity from augmentations (weighted lower)
        aug_count = len(self.pre_augmentations) + len(self.post_augmentations)
        total += aug_count * 0.05
        
        # Add complexity from meta-cognitive operations
        meta_count = len(self.monitoring_primitives) + len(self.control_primitives)
        total += meta_count * 0.03
        
        # Cap at 1.0
        return min(1.0, total)
    
    def has_validation(self) -> bool:
        """Check if payload includes validation operations."""
        validation_keywords = ['verify', 'validate', 'check', 'assess']
        
        for aug in self.post_augmentations:
            if any(kw in aug.name.lower() for kw in validation_keywords):
                return True
        
        return self.requires_verification
    
    def __repr__(self) -> str:
        return (
            f"ExecutionPayload("
            f"target={self.target_primitive.name}, "
            f"pre_aug={len(self.pre_augmentations)}, "
            f"post_aug={len(self.post_augmentations)}, "
            f"complexity={self.complexity:.2f})"
        )


class ExecutorType(Enum):
    """Types of executors available."""
    DIRECT_LLM = "direct_llm"
    REACT_AGENT = "react_agent"
    LANGGRAPH = "langgraph"
    LANGCHAIN = "langchain"


class Executor(ABC):
    """
    Base class for execution strategies.
    
    Executors determine how to execute a payload based on its complexity,
    requirements, and available resources.
    """
    
    def __init__(self, executor_type: ExecutorType):
        """
        Initialize executor.
        
        Args:
            executor_type: Type of this executor
        """
        self.executor_type = executor_type
        self.name = self.__class__.__name__
        self.executions = 0
        self.successes = 0
        self.total_time_ms = 0
        self.total_tokens = 0
    
    @abstractmethod
    def can_execute(
        self,
        payload: ExecutionPayload,
        context: 'ExecutionContext'
    ) -> bool:
        """
        Check if this executor can handle the payload.
        
        Args:
            payload: Execution payload
            context: Execution context
        
        Returns:
            True if executor can handle this payload
        """
        pass
    
    @abstractmethod
    def execute(
        self,
        payload: ExecutionPayload,
        context: 'ExecutionContext',
        working_memory: 'WorkingMemory'
    ) -> 'PrimitiveResult':
        """
        Execute the payload.
        
        Args:
            payload: Execution payload to run
            context: Execution context
            working_memory: Working memory instance
        
        Returns:
            PrimitiveResult from execution
        """
        pass
    
    @abstractmethod
    def estimate_suitability(
        self,
        payload: ExecutionPayload,
        context: 'ExecutionContext'
    ) -> float:
        """
        Estimate how suitable this executor is for the payload.
        
        Args:
            payload: Execution payload
            context: Execution context
        
        Returns:
            Suitability score (0.0-1.0), higher is better
        """
        pass
    
    def record_execution(
        self,
        success: bool,
        time_ms: int,
        tokens: int
    ) -> None:
        """
        Record execution statistics.
        
        Args:
            success: Whether execution succeeded
            time_ms: Execution time in milliseconds
            tokens: Tokens consumed
        """
        self.executions += 1
        if success:
            self.successes += 1
        self.total_time_ms += time_ms
        self.total_tokens += tokens
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get executor statistics.
        
        Returns:
            Dictionary of statistics
        """
        return {
            'executor_type': self.executor_type.value,
            'name': self.name,
            'executions': self.executions,
            'success_rate': self.successes / max(1, self.executions),
            'avg_time_ms': self.total_time_ms / max(1, self.executions),
            'avg_tokens': self.total_tokens / max(1, self.executions),
            'total_tokens': self.total_tokens,
        }
    
    def __repr__(self) -> str:
        return f"{self.name}(type={self.executor_type.value})"
