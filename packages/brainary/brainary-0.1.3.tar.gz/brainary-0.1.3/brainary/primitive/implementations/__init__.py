"""Primitive implementations package."""

# Core primitives
from .core import (
    PerceiveLLM,
    ThinkFast,
    ThinkDeep,
    RememberWorkingMemory,
    RecallWorkingMemory,
    AssociateConcepts,
    ActionExecutor,
    MonitorState,
    AdaptStrategy,
)

# Composite primitives
from .composite import (
    AnalyzeComposite,
    SolveComposite,
    DecideComposite,
    CreateComposite,
    ExplainComposite,
    DecomposeComposite,
    SynthesizeComposite,
    EvaluateComposite,
    VerifyComposite,
    PlanComposite,
)

# Metacognitive primitives
from .metacognitive import (
    IntrospectMetacognitive,
    SelfAssessMetacognitive,
    SelectStrategyMetacognitive,
    SelfCorrectMetacognitive,
    ReflectMetacognitive,
)

# Control flow primitives
from .control import (
    SequenceControl,
    ParallelControl,
    ConditionalControl,
    LoopControl,
    RetryControl,
)

__all__ = [
    # Core
    "PerceiveLLM",
    "ThinkFast",
    "ThinkDeep",
    "RememberWorkingMemory",
    "RecallWorkingMemory",
    "AssociateConcepts",
    "ActionExecutor",
    "MonitorState",
    "AdaptStrategy",
    # Composite
    "AnalyzeComposite",
    "SolveComposite",
    "DecideComposite",
    "CreateComposite",
    "ExplainComposite",
    "DecomposeComposite",
    "SynthesizeComposite",
    "EvaluateComposite",
    "VerifyComposite",
    "PlanComposite",
    # Metacognitive
    "IntrospectMetacognitive",
    "SelfAssessMetacognitive",
    "SelectStrategyMetacognitive",
    "SelfCorrectMetacognitive",
    "ReflectMetacognitive",
    # Control
    "SequenceControl",
    "ParallelControl",
    "ConditionalControl",
    "LoopControl",
    "RetryControl",
]

