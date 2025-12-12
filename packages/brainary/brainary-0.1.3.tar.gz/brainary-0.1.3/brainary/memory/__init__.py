"""
Memory subsystem for Brainary.

Implements 3-tier memory hierarchy:
- L1 (Working): 7±2 items, <1ms access
- L2 (Episodic): Recent experiences, ~10ms access
- L3 (Semantic): Knowledge graph, ~50ms access
"""

from brainary.memory.working import (
    WorkingMemory,
    MemoryItem,
    MemorySnapshot,
    MemoryImportance,
    MemoryTier,
    PrefetchRequest,
    MemoryStatistics,
    IMemoryManager,
)
from brainary.memory.attention import AttentionMechanism, AttentionFocus
from brainary.memory.associative import AssociativeMemory, Association
from brainary.memory.semantic import (
    SemanticMemory,
    KnowledgeType,
    KnowledgeEntry,
    ConceptualKnowledge,
    FactualKnowledge,
    ProceduralKnowledge,
    MetacognitiveKnowledge,
    create_entry_id,
)

__all__ = [
    # Core
    "WorkingMemory",
    "IMemoryManager",
    # Data structures
    "MemoryItem",
    "MemorySnapshot",
    "MemoryStatistics",
    "PrefetchRequest",
    # Enums
    "MemoryImportance",
    "MemoryTier",
    # Subsystems
    "AttentionMechanism",
    "AttentionFocus",
    "AssociativeMemory",
    "Association",
    # Semantic memory (L3)
    "SemanticMemory",
    "KnowledgeType",
    "KnowledgeEntry",
    "ConceptualKnowledge",
    "FactualKnowledge",
    "ProceduralKnowledge",
    "MetacognitiveKnowledge",
    "create_entry_id",
]
