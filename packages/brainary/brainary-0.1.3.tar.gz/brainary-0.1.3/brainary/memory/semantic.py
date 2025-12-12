"""
Semantic memory (L3) for long-term knowledge storage.

Implements persistent knowledge storage with semantic search and matching
across four knowledge types:
- Conceptual: Abstract concepts, categories, and their relationships
- Factual: Concrete facts, entities, and their properties
- Procedural: How-to knowledge, primitive implementations, domain-specific PoK programs
- Metacognitive: Monitoring rules, criteria, control strategies

Each knowledge type supports semantic search and retrieval to guide
kernel execution intelligently.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple
from enum import Enum
import time
import hashlib
import logging

logger = logging.getLogger(__name__)


class KnowledgeType(Enum):
    """Types of knowledge in semantic memory."""
    CONCEPTUAL = "conceptual"       # Abstract concepts and categories
    FACTUAL = "factual"             # Concrete facts and entities
    PROCEDURAL = "procedural"       # How-to knowledge and procedures
    METACOGNITIVE = "metacognitive" # Monitoring rules and control strategies


@dataclass
class KnowledgeEntry:
    """
    Base class for all knowledge entries in semantic memory.
    
    All entries support semantic search via:
    - key_concepts: Primary concepts for matching
    - description: Natural language description
    - metadata: Additional searchable attributes
    """
    entry_id: str
    knowledge_type: KnowledgeType
    key_concepts: List[str]  # Primary concepts for semantic matching
    description: str         # Natural language description
    importance: float = 0.5  # 0.0-1.0 relevance score
    created_at: float = field(default_factory=time.time)
    accessed_count: int = 0
    last_accessed: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def matches(self, query: str, threshold: float = 0.3) -> float:
        """
        Simple semantic matching score.
        
        Args:
            query: Search query
            threshold: Minimum match score
            
        Returns:
            Match score (0.0-1.0)
        """
        query_lower = query.lower()
        query_tokens = set(query_lower.split())
        score = 0.0
        
        # Check key concepts (high weight)
        for concept in self.key_concepts:
            concept_lower = concept.lower()
            # Exact match
            if query_lower in concept_lower or concept_lower in query_lower:
                score += 0.4
            # Token overlap
            concept_tokens = set(concept_lower.split())
            overlap = query_tokens.intersection(concept_tokens)
            if overlap:
                score += 0.2 * (len(overlap) / len(query_tokens))
        
        # Check description (medium weight) - check both full match and token overlap
        description_lower = self.description.lower()
        if query_lower in description_lower:
            score += 0.3
        else:
            # Token overlap in description
            description_tokens = set(description_lower.split())
            overlap = query_tokens.intersection(description_tokens)
            if overlap:
                score += 0.2 * (len(overlap) / len(query_tokens))
        
        # Check metadata (low weight)
        for key, value in self.metadata.items():
            if query_lower in str(value).lower():
                score += 0.1
        
        return min(1.0, score)
    
    def record_access(self) -> None:
        """Record an access to this entry."""
        self.accessed_count += 1
        self.last_accessed = time.time()


@dataclass
class ConceptualKnowledge(KnowledgeEntry):
    """
    Abstract conceptual knowledge.
    
    Examples:
    - "optimization" is-a "problem-solving strategy"
    - "recursion" related-to "iteration"
    - "classification" category-of ["supervised learning"]
    """
    knowledge_type: KnowledgeType = field(default=KnowledgeType.CONCEPTUAL, init=False)
    relationships: List[Tuple[str, str, str]] = field(default_factory=list)  # (concept1, relation, concept2)
    subconcepts: List[str] = field(default_factory=list)
    superconcepts: List[str] = field(default_factory=list)


@dataclass
class FactualKnowledge(KnowledgeEntry):
    """
    Concrete factual knowledge.
    
    Examples:
    - "Python 3.11 was released on October 24, 2022"
    - "GPT-4 has 1.76 trillion parameters"
    - "The user prefers verbose explanations"
    """
    knowledge_type: KnowledgeType = field(default=KnowledgeType.FACTUAL, init=False)
    entity: str = ""
    properties: Dict[str, Any] = field(default_factory=dict)
    source: str = ""
    confidence: float = 1.0


@dataclass
class ProceduralKnowledge(KnowledgeEntry):
    """
    Procedural how-to knowledge.
    
    Examples:
    - Custom primitive implementation for domain-specific "perceive"
    - PoK program for "analyze_sentiment"
    - Optimization strategy: "use caching for repeated queries"
    """
    knowledge_type: KnowledgeType = field(default=KnowledgeType.PROCEDURAL, init=False)
    procedure_type: str = ""  # "primitive_impl", "pok_program", "strategy"
    implementation: Optional[Any] = None  # Actual code/program
    preconditions: List[str] = field(default_factory=list)
    postconditions: List[str] = field(default_factory=list)
    success_rate: float = 0.0
    avg_cost_tokens: int = 0
    avg_latency_ms: float = 0.0


@dataclass
class MetacognitiveKnowledge(KnowledgeEntry):
    """
    Metacognitive monitoring and control knowledge.
    
    Examples:
    - Monitoring rule: "if confidence < 0.6, trigger verification"
    - Criterion: "output must be valid JSON"
    - Control strategy: "retry with higher temperature on failure"
    """
    knowledge_type: KnowledgeType = field(default=KnowledgeType.METACOGNITIVE, init=False)
    rule_type: str = ""  # "monitoring_rule", "criterion", "control_strategy"
    condition: str = ""   # When this rule applies
    action: str = ""      # What to do when triggered
    priority: float = 0.5
    trigger_count: int = 0
    success_count: int = 0
    
    def get_success_rate(self) -> float:
        """Calculate success rate of this rule."""
        if self.trigger_count == 0:
            return 0.0
        return self.success_count / self.trigger_count


class SemanticMemory:
    """
    Long-term semantic memory with knowledge-based search.
    
    Stores four types of knowledge:
    - Conceptual: Abstract concepts and relationships
    - Factual: Concrete facts and entities
    - Procedural: Implementations and strategies
    - Metacognitive: Monitoring rules and criteria
    
    All knowledge supports semantic search to assist:
    - Metacognitive monitor: Load monitoring rules
    - Scheduler: Load procedural knowledge (implementations, PoK programs)
    - Context enhancement: Load conceptual/factual knowledge
    """
    
    def __init__(self, enable_logging: bool = True):
        """
        Initialize semantic memory.
        
        Args:
            enable_logging: Whether to log memory operations
        """
        self.entries: Dict[str, KnowledgeEntry] = {}
        self.index_by_type: Dict[KnowledgeType, Set[str]] = {
            kt: set() for kt in KnowledgeType
        }
        self.index_by_concept: Dict[str, Set[str]] = {}
        self.enable_logging = enable_logging
        
        # Statistics
        self.total_searches = 0
        self.total_retrievals = 0
    
    def add_knowledge(self, entry: KnowledgeEntry) -> str:
        """
        Add knowledge entry to semantic memory.
        
        Args:
            entry: Knowledge entry to add
            
        Returns:
            Entry ID
        """
        entry_id = entry.entry_id
        self.entries[entry_id] = entry
        
        # Index by type
        self.index_by_type[entry.knowledge_type].add(entry_id)
        
        # Index by concepts
        for concept in entry.key_concepts:
            concept_lower = concept.lower()
            if concept_lower not in self.index_by_concept:
                self.index_by_concept[concept_lower] = set()
            self.index_by_concept[concept_lower].add(entry_id)
        
        if self.enable_logging:
            logger.info(f"Added {entry.knowledge_type.value} knowledge: {entry.description[:50]}...")
        
        return entry_id
    
    def search(
        self,
        query: str,
        knowledge_types: Optional[List[KnowledgeType]] = None,
        top_k: int = 5,
        min_score: float = 0.3
    ) -> List[KnowledgeEntry]:
        """
        Search semantic memory with semantic matching.
        
        Args:
            query: Search query
            knowledge_types: Filter by knowledge types (None = all types)
            top_k: Maximum results to return
            min_score: Minimum match score threshold
            
        Returns:
            List of matching knowledge entries, sorted by relevance
        """
        self.total_searches += 1
        
        # Determine which entries to search
        if knowledge_types is None:
            candidate_ids = set(self.entries.keys())
        else:
            candidate_ids = set()
            for kt in knowledge_types:
                candidate_ids.update(self.index_by_type[kt])
        
        # Quick concept-based filtering
        query_tokens = query.lower().split()
        concept_matches = set()
        for token in query_tokens:
            for concept, entry_ids in self.index_by_concept.items():
                if token in concept or concept in token:
                    concept_matches.update(entry_ids)
        
        # If we have concept matches, prioritize them
        if concept_matches:
            candidate_ids = candidate_ids.intersection(concept_matches)
        
        # Score all candidates
        scored_entries = []
        for entry_id in candidate_ids:
            entry = self.entries[entry_id]
            score = entry.matches(query, threshold=min_score)
            
            # Boost by importance and access count
            score *= (0.7 + 0.3 * entry.importance)
            score *= (0.9 + 0.1 * min(1.0, entry.accessed_count / 10.0))
            
            if score >= min_score:
                scored_entries.append((score, entry))
        
        # Sort by score and return top-k
        scored_entries.sort(reverse=True, key=lambda x: x[0])
        results = [entry for _, entry in scored_entries[:top_k]]
        
        # Record accesses
        for entry in results:
            entry.record_access()
        
        self.total_retrievals += len(results)
        
        if self.enable_logging and results:
            logger.debug(f"Search '{query}' found {len(results)} results (types: {knowledge_types})")
        
        return results
    
    def get_monitoring_rules(
        self,
        context_query: str = "",
        top_k: int = 10
    ) -> List[MetacognitiveKnowledge]:
        """
        Get metacognitive monitoring rules for current context.
        
        Args:
            context_query: Description of current context
            top_k: Maximum rules to return
            
        Returns:
            List of relevant monitoring rules
        """
        results = self.search(
            query=context_query if context_query else "monitoring",
            knowledge_types=[KnowledgeType.METACOGNITIVE],
            top_k=top_k,
            min_score=0.2
        )
        return [r for r in results if isinstance(r, MetacognitiveKnowledge)]
    
    def get_procedural_knowledge(
        self,
        primitive_name: str = "",
        domain: str = "",
        top_k: int = 5
    ) -> List[ProceduralKnowledge]:
        """
        Get procedural knowledge for primitive scheduling.
        
        Args:
            primitive_name: Name of primitive to find implementations for
            domain: Domain context
            top_k: Maximum results to return
            
        Returns:
            List of relevant procedural knowledge
        """
        query = f"{primitive_name} {domain}".strip()
        results = self.search(
            query=query if query else "procedure",
            knowledge_types=[KnowledgeType.PROCEDURAL],
            top_k=top_k,
            min_score=0.2
        )
        return [r for r in results if isinstance(r, ProceduralKnowledge)]
    
    def get_contextual_knowledge(
        self,
        query: str,
        include_concepts: bool = True,
        include_facts: bool = True,
        top_k: int = 10
    ) -> List[KnowledgeEntry]:
        """
        Get conceptual and factual knowledge for context enhancement.
        
        Args:
            query: Context description
            include_concepts: Include conceptual knowledge
            include_facts: Include factual knowledge
            top_k: Maximum results to return
            
        Returns:
            List of relevant conceptual/factual knowledge
        """
        knowledge_types = []
        if include_concepts:
            knowledge_types.append(KnowledgeType.CONCEPTUAL)
        if include_facts:
            knowledge_types.append(KnowledgeType.FACTUAL)
        
        if not knowledge_types:
            return []
        
        return self.search(
            query=query,
            knowledge_types=knowledge_types,
            top_k=top_k,
            min_score=0.3
        )
    
    def get_entry(self, entry_id: str) -> Optional[KnowledgeEntry]:
        """Get entry by ID."""
        return self.entries.get(entry_id)
    
    def remove_entry(self, entry_id: str) -> bool:
        """
        Remove entry from memory.
        
        Args:
            entry_id: ID of entry to remove
            
        Returns:
            True if entry was removed
        """
        if entry_id not in self.entries:
            return False
        
        entry = self.entries[entry_id]
        
        # Remove from type index
        self.index_by_type[entry.knowledge_type].discard(entry_id)
        
        # Remove from concept index
        for concept in entry.key_concepts:
            concept_lower = concept.lower()
            if concept_lower in self.index_by_concept:
                self.index_by_concept[concept_lower].discard(entry_id)
        
        # Remove entry
        del self.entries[entry_id]
        
        if self.enable_logging:
            logger.info(f"Removed knowledge entry: {entry_id}")
        
        return True
    
    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics."""
        type_counts = {
            kt.value: len(entry_ids)
            for kt, entry_ids in self.index_by_type.items()
        }
        
        return {
            "total_entries": len(self.entries),
            "entries_by_type": type_counts,
            "total_searches": self.total_searches,
            "total_retrievals": self.total_retrievals,
            "avg_retrievals_per_search": (
                self.total_retrievals / max(1, self.total_searches)
            ),
        }
    
    def clear(self) -> None:
        """Clear all knowledge entries."""
        self.entries.clear()
        for entry_set in self.index_by_type.values():
            entry_set.clear()
        self.index_by_concept.clear()
        
        if self.enable_logging:
            logger.info("Cleared all semantic memory")


def create_entry_id(knowledge_type: KnowledgeType, description: str) -> str:
    """
    Create unique entry ID from type and description.
    
    Args:
        knowledge_type: Type of knowledge
        description: Entry description
        
    Returns:
        Unique entry ID
    """
    content = f"{knowledge_type.value}:{description}:{time.time()}"
    hash_obj = hashlib.md5(content.encode())
    return f"{knowledge_type.value}_{hash_obj.hexdigest()[:12]}"
