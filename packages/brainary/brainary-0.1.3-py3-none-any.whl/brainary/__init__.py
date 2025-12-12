"""
Brainary - Programmable Intelligence System

A cognitive computing platform where intelligence is expressed as executable programs
built from cognitive primitives (perceive, think, remember, action).
"""

__version__ = "0.1.0"

# Core imports for convenient access
from brainary.core.context import (
    ExecutionContext,
    ExecutionMode,
    create_execution_context,
)
from brainary.core.kernel import CognitiveKernel, get_kernel
from brainary.core.scheduler import ProgramScheduler
from brainary.core.resource_manager import (
    ResourceManager,
    ResourceQuota,
    ResourceAllocation,
    IResourceManager,
)
from brainary.core.errors import (
    BrainaryError,
    PrimitiveExecutionError,
    ResourceExhaustedError,
    NoImplementationError,
    ValidationError,
    MemoryFullError,
    TimeoutError,
    TransactionError,
    LLMProviderError,
    RateLimitError,
)

# Primitive system imports
from brainary.primitive.base import (
    Primitive,
    CorePrimitive,
    CompositePrimitive,
    MetacognitivePrimitive,
    DomainPrimitive,
    ControlPrimitive,
    PrimitiveResult,
    ResourceEstimate,
    ConfidenceMetrics,
    CostMetrics,
    ConfidenceScore,
    MemoryOperation,
)
from brainary.primitive.registry import (
    PrimitiveRegistry,
    get_global_registry,
    PoKLibrary,
    PoKLibraryRegistry,
    get_pok_library_registry,
)
from brainary.primitive.implementations import (
    PerceiveLLM,
    ThinkFast,
    ThinkDeep,
    RememberWorkingMemory,
    RecallWorkingMemory,
)

# Memory system imports
from brainary.memory.working import (
    WorkingMemory,
    IMemoryManager,
    MemoryItem,
    MemorySnapshot,
    MemoryTier,
    MemoryStatistics,
    PrefetchRequest,
)
from brainary.memory.attention import AttentionMechanism
from brainary.memory.associative import AssociativeMemory

# LLM integration imports
from brainary.llm.driver import (
    ILLMDriver,
    OpenAIDriver,
    LLMRequest,
    LLMResponseData,
    LLMCapability,
    create_driver,
)

# Executor imports
from brainary.executors.base import Executor, ExecutionPayload, ExecutorType
from brainary.executors.direct_llm import DirectLLMExecutor
from brainary.executors.react_agent import ReActAgentExecutor

# Control flow imports
from brainary.control.flow import Sequence, Parallel, Conditional, Retry

__all__ = [
    # Version
    "__version__",
    # Core
    "ExecutionContext",
    "ExecutionMode",
    "create_execution_context",
    "CognitiveKernel",
    "get_kernel",
    "ProgramScheduler",
    "ResourceManager",
    "ResourceQuota",
    "ResourceAllocation",
    "IResourceManager",
    # Errors
    "BrainaryError",
    "PrimitiveExecutionError",
    "ResourceExhaustedError",
    "NoImplementationError",
    "ValidationError",
    "MemoryFullError",
    "TimeoutError",
    "TransactionError",
    "LLMProviderError",
    "RateLimitError",
    # Primitives
    "Primitive",
    "CorePrimitive",
    "CompositePrimitive",
    "MetacognitivePrimitive",
    "DomainPrimitive",
    "ControlPrimitive",
    "PrimitiveResult",
    "ResourceEstimate",
    "ConfidenceMetrics",
    "CostMetrics",
    "ConfidenceScore",
    "MemoryOperation",
    "PrimitiveRegistry",
    "get_global_registry",
    "PoKLibrary",
    "PoKLibraryRegistry",
    "get_pok_library_registry",
    # Primitive implementations
    "PerceiveLLM",
    "ThinkFast",
    "ThinkDeep",
    "RememberWorkingMemory",
    "RecallWorkingMemory",
    # Memory
    "WorkingMemory",
    "IMemoryManager",
    "MemoryItem",
    "MemorySnapshot",
    "MemoryTier",
    "MemoryStatistics",
    "PrefetchRequest",
    "AttentionMechanism",
    "AssociativeMemory",
    # LLM
    "ILLMDriver",
    "OpenAIDriver",
    "LLMRequest",
    "LLMResponseData",
    "LLMCapability",
    "create_driver",
    # Executors
    "Executor",
    "ExecutionPayload",
    "ExecutorType",
    "DirectLLMExecutor",
    "ReActAgentExecutor",
    # Control
    "Sequence",
    "Parallel",
    "Conditional",
    "Retry",
]
