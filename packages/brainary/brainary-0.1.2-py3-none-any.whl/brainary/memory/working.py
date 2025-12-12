"""
Working memory implementation with intelligent management.

Implements cognitive science constraints (7±2 items) with automatic
snapshot management, on-demand reorganization, and execution-aware operations.

Implements IMemoryManager with 3-tier hierarchy:
- L1 (Working): 7±2 items, <1ms access
- L2 (Episodic): Recent experiences, ~10ms access
- L3 (Semantic): Knowledge graph, ~50ms access
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple
from abc import ABC, abstractmethod
from enum import Enum
import time
import uuid
import threading
from collections import defaultdict


class MemoryTier(Enum):
    """Memory hierarchy tiers."""
    L1_WORKING = "L1"      # Hot cache, 7±2 items, <1ms
    L2_EPISODIC = "L2"     # Recent experiences, ~10ms
    L3_SEMANTIC = "L3"     # Knowledge graph, ~50ms


class MemoryImportance(Enum):
    """Importance levels for memory items."""
    CRITICAL = 1.0
    HIGH = 0.8
    MEDIUM = 0.5
    LOW = 0.3
    MINIMAL = 0.1


@dataclass
class MemoryItem:
    """Item stored in working memory."""
    
    item_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    content: Any = None
    importance: float = 0.5
    access_count: int = 0
    last_access: float = field(default_factory=time.time)
    created_at: float = field(default_factory=time.time)
    tags: List[str] = field(default_factory=list)
    source_primitive: Optional[str] = None
    decay_rate: float = 0.1
    associations: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate importance."""
        if not 0.0 <= self.importance <= 1.0:
            raise ValueError("importance must be in [0.0, 1.0]")
    
    def compute_activation(self) -> float:
        """
        Compute current activation level based on importance, recency, and frequency.
        
        Returns:
            Activation score (0.0-1.0)
        """
        # Base activation from importance
        activation = self.importance
        
        # Recency boost (decay over time)
        time_since_access = time.time() - self.last_access
        recency_factor = max(0.0, 1.0 - (time_since_access * self.decay_rate / 3600))
        activation *= (0.5 + 0.5 * recency_factor)
        
        # Frequency boost (logarithmic)
        import math
        frequency_factor = math.log(1 + self.access_count) / math.log(10)
        activation *= (0.7 + 0.3 * min(1.0, frequency_factor))
        
        return min(1.0, activation)
    
    def access(self) -> None:
        """Record access to this item."""
        self.access_count += 1
        self.last_access = time.time()


@dataclass
class MemorySnapshot:
    """Snapshot of working memory state."""
    
    snapshot_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)
    items: Dict[str, MemoryItem] = field(default_factory=dict)
    focus_items: List[str] = field(default_factory=list)
    primitive_context: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PrefetchRequest:
    """Request for prefetching memory items."""
    
    context_tags: List[str]
    primitive_name: str
    max_items: int = 3
    min_salience: float = 0.3


@dataclass
class MemoryStatistics:
    """Memory system statistics."""
    
    # L1 Statistics
    l1_capacity: int
    l1_size: int
    l1_utilization: float
    l1_hits: int
    l1_misses: int
    l1_evictions: int
    
    # L2 Statistics
    l2_size: int
    l2_hits: int
    l2_consolidations: int
    
    # L3 Statistics
    l3_size: int
    l3_clusters: int
    l3_average_associations: float
    
    # Overall
    total_stores: int
    total_retrievals: int
    prefetch_requests: int
    cache_hit_rate: float


class IMemoryManager(ABC):
    """
    Interface for memory management system.
    
    Based on SPECIFICATION.md Section 2.3: IMemoryManager Interface
    """
    
    @abstractmethod
    def store(
        self,
        content: Any,
        tier: MemoryTier = MemoryTier.L1_WORKING,
        importance: float = 0.5,
        tags: Optional[List[str]] = None,
        **metadata
    ) -> str:
        """Store content in specified memory tier."""
        pass
    
    @abstractmethod
    def retrieve(
        self,
        query: Optional[str] = None,
        tags: Optional[List[str]] = None,
        tier: Optional[MemoryTier] = None,
        top_k: int = 1
    ) -> List[MemoryItem]:
        """Retrieve items matching query/tags across tiers."""
        pass
    
    @abstractmethod
    def prefetch(self, request: PrefetchRequest) -> List[str]:
        """Prefetch relevant items from L2/L3 to L1."""
        pass
    
    @abstractmethod
    def consolidate(self) -> Dict[str, int]:
        """Consolidate L1 items to L2/L3."""
        pass
    
    @abstractmethod
    def get_statistics(self) -> MemoryStatistics:
        """Get memory system statistics."""
        pass


class WorkingMemory(IMemoryManager):
    """
    Working memory with intelligent 3-tier management.
    
    Implements IMemoryManager from SPECIFICATION.md with:
    - L1 (Working): 7±2 items, <1ms access
    - L2 (Episodic): Recent experiences, ~10ms access  
    - L3 (Semantic): Knowledge graph, ~50ms access
    
    Additional features:
    - Automatic eviction of low-activation items
    - Snapshot management for primitive execution
    - On-demand reorganization
    - Attention-based focus
    - Intelligent prefetching with salience scoring
    """
    
    # Class variable to control debug output
    DEBUG_ENABLED = False
    
    @classmethod
    def enable_debug(cls):
        """Enable debug output for all memory operations."""
        cls.DEBUG_ENABLED = True
    
    @classmethod
    def disable_debug(cls):
        """Disable debug output for all memory operations."""
        cls.DEBUG_ENABLED = False
    
    def __init__(
        self,
        capacity: int = 7,
        l2_capacity: int = 100,
        auto_consolidate: bool = True,
        consolidate_threshold: float = 0.9
    ):
        """
        Initialize working memory.
        
        Args:
            capacity: L1 maximum items (default 7)
            l2_capacity: L2 maximum items (default 100)
            auto_consolidate: Automatically consolidate to long-term memory
            consolidate_threshold: L1 capacity ratio to trigger consolidation
        """
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        
        self.capacity = capacity
        self.l2_capacity = l2_capacity
        self.auto_consolidate = auto_consolidate
        self.consolidate_threshold = consolidate_threshold
        
        # L1: Working Memory (hot cache)
        self._l1_items: Dict[str, MemoryItem] = {}
        self._focus_items: List[str] = []  # Currently focused item IDs
        
        # L2: Episodic Memory (recent experiences)
        self._l2_items: Dict[str, MemoryItem] = {}
        self._l2_access_order: List[str] = []  # LRU tracking
        
        # L3: Semantic Memory (knowledge graph)
        self._l3_items: Dict[str, MemoryItem] = {}
        self._l3_associations: Dict[str, List[Tuple[str, float]]] = defaultdict(list)  # item_id -> [(associated_id, strength)]
        self._l3_clusters: Dict[str, List[str]] = {}  # cluster_id -> item_ids
        
        # Snapshots
        self._snapshots: Dict[str, MemorySnapshot] = {}
        self._lock = threading.RLock()
        
        # Statistics
        self.total_stores = 0
        self.total_retrievals = 0
        self.l1_evictions = 0
        self.l2_evictions = 0
        self.l1_hits = 0
        self.l1_misses = 0
        self.l2_hits = 0
        self.l2_consolidations = 0
        self.prefetch_requests = 0
        self.reorganizations = 0
    
    def store(
        self,
        content: Any,
        tier: MemoryTier = MemoryTier.L1_WORKING,
        importance: float = 0.5,
        tags: Optional[List[str]] = None,
        source_primitive: Optional[str] = None,
        **metadata
    ) -> str:
        """
        Store item in specified memory tier.
        
        Implements IMemoryManager.store() from SPECIFICATION.md
        
        Args:
            content: Content to store
            tier: Target memory tier (L1/L2/L3)
            importance: Importance level (0.0-1.0)
            tags: Optional classification tags
            source_primitive: Primitive that created this item
            **metadata: Additional metadata
        
        Returns:
            Item ID
        """
        with self._lock:
            item = MemoryItem(
                content=content,
                importance=importance,
                tags=tags or [],
                source_primitive=source_primitive,
                metadata=metadata,
            )
            
            self.total_stores += 1
            
            # Store in appropriate tier
            if tier == MemoryTier.L1_WORKING:
                # Check L1 capacity and evict if needed
                if len(self._l1_items) >= self.capacity:
                    self._evict_lowest_activation()
                
                self._l1_items[item.item_id] = item
                
                # Print memory content for debugging
                if self.DEBUG_ENABLED:
                    print(f"\n[MEMORY UPDATE - L1] Store:")
                    print(f"  Item ID: {item.item_id}")
                    print(f"  Content: {str(content)[:100]}..." if len(str(content)) > 100 else f"  Content: {content}")
                    print(f"  Importance: {importance}")
                    print(f"  Tags: {tags}")
                    print(f"  Source: {source_primitive}")
                    print(f"  L1 Size: {len(self._l1_items)}/{self.capacity}")
                
                # Auto-consolidate if threshold reached
                if (self.auto_consolidate and 
                    len(self._l1_items) >= self.capacity * self.consolidate_threshold):
                    self._trigger_consolidation()
                    
            elif tier == MemoryTier.L2_EPISODIC:
                # Check L2 capacity
                if len(self._l2_items) >= self.l2_capacity:
                    # Evict oldest item from L2
                    if self._l2_access_order:
                        oldest_id = self._l2_access_order.pop(0)
                        if oldest_id in self._l2_items:
                            # Move to L3 before evicting
                            old_item = self._l2_items.pop(oldest_id)
                            self._l3_items[oldest_id] = old_item
                            self.l2_evictions += 1
                
                self._l2_items[item.item_id] = item
                self._l2_access_order.append(item.item_id)
                
                # Print memory content for debugging
                if self.DEBUG_ENABLED:
                    print(f"\n[MEMORY UPDATE - L2] Store:")
                    print(f"  Item ID: {item.item_id}")
                    print(f"  Content: {str(content)[:100]}..." if len(str(content)) > 100 else f"  Content: {content}")
                    print(f"  Importance: {importance}")
                    print(f"  Tags: {tags}")
                    print(f"  Source: {source_primitive}")
                    print(f"  L2 Size: {len(self._l2_items)}/{self.l2_capacity}")
                
            elif tier == MemoryTier.L3_SEMANTIC:
                self._l3_items[item.item_id] = item
                
                # Print memory content for debugging
                if self.DEBUG_ENABLED:
                    print(f"\n[MEMORY UPDATE - L3] Store:")
                    print(f"  Item ID: {item.item_id}")
                    print(f"  Content: {str(content)[:100]}..." if len(str(content)) > 100 else f"  Content: {content}")
                    print(f"  Importance: {importance}")
                    print(f"  Tags: {tags}")
                    print(f"  Source: {source_primitive}")
                    print(f"  L3 Size: {len(self._l3_items)}")
            
            return item.item_id
    
    def retrieve(
        self,
        query: Optional[str] = None,
        tags: Optional[List[str]] = None,
        tier: Optional[MemoryTier] = None,
        top_k: int = 1,
        min_importance: float = 0.0
    ) -> List[MemoryItem]:
        """
        Retrieve items matching query/tags across memory tiers.
        
        Implements IMemoryManager.retrieve() from SPECIFICATION.md
        Searches L1 → L2 → L3 with automatic promotion to L1.
        
        Args:
            query: Item ID or content query
            tags: Filter by tags (OR logic)
            tier: Specific tier to search (None = search all)
            top_k: Number of top items to return (by activation)
            min_importance: Minimum importance threshold
        
        Returns:
            List of matching MemoryItems
        """
        with self._lock:
            self.total_retrievals += 1
            
            # Retrieve specific item by ID
            if query and not tags:
                item = self._find_item_by_id(query)
                if item:
                    item.access()
                    self._promote_to_l1(query)
                    return [item]
            
            # Search appropriate tiers
            tiers_to_search = []
            if tier:
                tiers_to_search = [tier]
            else:
                tiers_to_search = [MemoryTier.L1_WORKING, MemoryTier.L2_EPISODIC, MemoryTier.L3_SEMANTIC]
            
            candidates = []
            for search_tier in tiers_to_search:
                tier_items = self._get_tier_items(search_tier)
                
                for item in tier_items.values():
                    if min_importance > 0 and item.importance < min_importance:
                        continue
                    if tags and not any(tag in item.tags for tag in tags):
                        continue
                    candidates.append((item, search_tier))
            
            # Sort by activation and return top_k
            candidates.sort(key=lambda x: x[0].compute_activation(), reverse=True)
            results = candidates[:top_k]
            
            # Print memory content for debugging
            if self.DEBUG_ENABLED:
                print(f"\n[MEMORY RETRIEVE] Query:")
                print(f"  Query: {query}")
                print(f"  Tags: {tags}")
                print(f"  Tier: {tier}")
                print(f"  Top-k: {top_k}")
                print(f"  Min Importance: {min_importance}")
                print(f"  Results Found: {len(results)}")
            
            # Record access and promote to L1 if not already there
            result_items = []
            for item, found_tier in results:
                item.access()
                
                # Print retrieved item details
                if self.DEBUG_ENABLED:
                    print(f"  - Item ID: {item.item_id}")
                    print(f"    Content: {str(item.content)[:80]}..." if len(str(item.content)) > 80 else f"    Content: {item.content}")
                    print(f"    Found in: {found_tier.value}")
                    print(f"    Importance: {item.importance:.2f}")
                    print(f"    Activation: {item.compute_activation():.2f}")
                    print(f"    Access Count: {item.access_count}")
                
                if found_tier != MemoryTier.L1_WORKING:
                    self._promote_to_l1(item.item_id)
                    if self.DEBUG_ENABLED:
                        print(f"    Promoted to L1")
                    if found_tier == MemoryTier.L2_EPISODIC:
                        self.l2_hits += 1
                else:
                    self.l1_hits += 1
                result_items.append(item)
            
            if not result_items:
                self.l1_misses += 1
                if self.DEBUG_ENABLED:
                    print("  No results found.")
            
            return result_items
    
    def update(self, item_id: str, **updates) -> bool:
        """
        Update memory item across all tiers.
        
        Args:
            item_id: Item to update
            **updates: Fields to update
        
        Returns:
            True if updated, False if not found
        """
        with self._lock:
            item = self._find_item_by_id(item_id)
            if not item:
                return False
            
            if self.DEBUG_ENABLED:
                print(f"\n[MEMORY UPDATE] Item:")
                print(f"  Item ID: {item_id[:8]}...")
                print(f"  Updates: {list(updates.keys())}")
            
            for key, value in updates.items():
                if hasattr(item, key):
                    if self.DEBUG_ENABLED:
                        old_value = getattr(item, key)
                        setattr(item, key, value)
                        print(f"  {key}: {old_value} → {value}")
                    else:
                        setattr(item, key, value)
            
            item.access()
            return True
    
    def delete(self, item_id: str) -> bool:
        """
        Delete item from memory across all tiers.
        
        Args:
            item_id: Item to delete
        
        Returns:
            True if deleted, False if not found
        """
        with self._lock:
            found = False
            
            if item_id in self._l1_items:
                del self._l1_items[item_id]
                found = True
            if item_id in self._l2_items:
                del self._l2_items[item_id]
                if item_id in self._l2_access_order:
                    self._l2_access_order.remove(item_id)
                found = True
            if item_id in self._l3_items:
                del self._l3_items[item_id]
                # Clean up associations
                if item_id in self._l3_associations:
                    del self._l3_associations[item_id]
                found = True
                
            if item_id in self._focus_items:
                self._focus_items.remove(item_id)
                
            return found
    
    def set_focus(self, item_ids: List[str]) -> None:
        """
        Set attention focus to specific items (promotes to L1 if needed).
        
        Args:
            item_ids: Items to focus on
        """
        with self._lock:
            self._focus_items = []
            for item_id in item_ids:
                if self._find_item_by_id(item_id):
                    self._focus_items.append(item_id)
                    # Ensure focused items are in L1
                    self._promote_to_l1(item_id)
    
    def get_focus(self) -> List[MemoryItem]:
        """
        Get currently focused items.
        
        Returns:
            List of focused MemoryItems
        """
        with self._lock:
            items = []
            for item_id in self._focus_items:
                item = self._find_item_by_id(item_id)
                if item:
                    items.append(item)
            return items
    
    def create_snapshot(
        self,
        primitive_context: str = "",
        **metadata
    ) -> str:
        """
        Create snapshot of current L1 working memory state.
        
        Args:
            primitive_context: Executing primitive name
            **metadata: Additional snapshot metadata
        
        Returns:
            Snapshot ID
        """
        with self._lock:
            snapshot = MemorySnapshot(
                items=self._l1_items.copy(),
                focus_items=self._focus_items.copy(),
                primitive_context=primitive_context,
                metadata=metadata,
            )
            self._snapshots[snapshot.snapshot_id] = snapshot
            return snapshot.snapshot_id
    
    def restore_snapshot(self, snapshot_id: str) -> bool:
        """
        Restore L1 working memory from snapshot.
        
        Args:
            snapshot_id: Snapshot to restore
        
        Returns:
            True if restored, False if not found
        """
        with self._lock:
            snapshot = self._snapshots.get(snapshot_id)
            if not snapshot:
                return False
            
            self._l1_items = snapshot.items.copy()
            self._focus_items = snapshot.focus_items.copy()
            return True
    
    def reorganize(self, strategy: str = "activation") -> None:
        """
        Reorganize L1 working memory based on strategy.
        
        Args:
            strategy: Reorganization strategy
                - "activation": Keep highest activation items
                - "importance": Keep highest importance items
                - "recent": Keep most recently accessed items
        """
        with self._lock:
            if len(self._l1_items) <= self.capacity:
                return
            
            self.reorganizations += 1
            
            # Sort items by strategy
            items = list(self._l1_items.values())
            if strategy == "activation":
                items.sort(key=lambda x: x.compute_activation(), reverse=True)
            elif strategy == "importance":
                items.sort(key=lambda x: x.importance, reverse=True)
            elif strategy == "recent":
                items.sort(key=lambda x: x.last_access, reverse=True)
            else:
                raise ValueError(f"Unknown strategy: {strategy}")
            
            # Keep top capacity items, consolidate rest
            keep_items = items[:self.capacity]
            evict_items = items[self.capacity:]
            
            # Move evicted items to L2
            for item in evict_items:
                if len(self._l2_items) < self.l2_capacity:
                    self._l2_items[item.item_id] = item
                    self._l2_access_order.append(item.item_id)
            
            self._l1_items = {item.item_id: item for item in keep_items}
            
            # Update focus
            self._focus_items = [
                item_id for item_id in self._focus_items
                if item_id in self._l1_items
            ]
    
    def clear(self) -> None:
        """Clear all items from all memory tiers."""
        with self._lock:
            self._l1_items.clear()
            self._l2_items.clear()
            self._l3_items.clear()
            self._focus_items.clear()
            self._l2_access_order.clear()
            self._l3_associations.clear()
            self._l3_clusters.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get memory statistics (legacy method for backward compatibility).
        
        Returns:
            Dictionary of statistics
        """
        stats = self.get_statistics()
        return {
            'capacity': stats.l1_capacity,
            'current_size': stats.l1_size,
            'utilization': stats.l1_utilization,
            'focused_items': len(self._focus_items),
            'total_stores': stats.total_stores,
            'total_retrievals': stats.total_retrievals,
            'evictions': stats.l1_evictions,
            'reorganizations': self.reorganizations,
            'snapshots': len(self._snapshots),
            'l2_size': stats.l2_size,
            'l3_size': stats.l3_size,
            'cache_hit_rate': stats.cache_hit_rate,
        }
    
    def _evict_lowest_activation(self) -> None:
        """Evict item with lowest activation from L1."""
        if not self._l1_items:
            return
        
        # Find item with lowest activation
        items = list(self._l1_items.values())
        lowest = min(items, key=lambda x: x.compute_activation())
        
        # Don't evict focused items
        if lowest.item_id in self._focus_items:
            # Find lowest non-focused item
            non_focused = [
                item for item in items 
                if item.item_id not in self._focus_items
            ]
            if non_focused:
                lowest = min(non_focused, key=lambda x: x.compute_activation())
        
        if self.DEBUG_ENABLED:
            print(f"\n[MEMORY EVICTION - L1]:")
            print(f"  Evicting: {lowest.item_id[:8]}...")
            print(f"  Content: {str(lowest.content)[:60]}...")
            print(f"  Activation: {lowest.compute_activation():.2f}")
            print(f"  Importance: {lowest.importance:.2f}")
            print(f"  Access Count: {lowest.access_count}")
        
        # Move to L2 before evicting from L1
        item_id = lowest.item_id
        if len(self._l2_items) < self.l2_capacity:
            self._l2_items[item_id] = self._l1_items[item_id]
            self._l2_access_order.append(item_id)
            if self.DEBUG_ENABLED:
                print(f"  → Moved to L2")
        else:
            if self.DEBUG_ENABLED:
                print(f"  → Discarded (L2 full)")
        
        del self._l1_items[item_id]
        self.l1_evictions += 1
        if self.DEBUG_ENABLED:
            print(f"  New L1 Size: {len(self._l1_items)}/{self.capacity}")
    
    def prefetch(self, request: PrefetchRequest) -> List[str]:
        """
        Prefetch relevant items from L2/L3 to L1 based on context.
        
        Implements IMemoryManager.prefetch() from SPECIFICATION.md
        Uses salience scoring: experience + associations + semantic relevance
        
        Args:
            request: Prefetch request with context and constraints
        
        Returns:
            List of item IDs prefetched to L1
        """
        with self._lock:
            self.prefetch_requests += 1
            
            candidates = []
            
            # Search L2 (episodic) for relevant experiences
            for item_id, item in self._l2_items.items():
                salience = self._compute_salience(item, request)
                if salience >= request.min_salience:
                    candidates.append((item_id, salience, MemoryTier.L2_EPISODIC))
            
            # Search L3 (semantic) for knowledge
            for item_id, item in self._l3_items.items():
                salience = self._compute_salience(item, request)
                if salience >= request.min_salience:
                    candidates.append((item_id, salience, MemoryTier.L3_SEMANTIC))
            
            # Sort by salience and take top items
            candidates.sort(key=lambda x: x[1], reverse=True)
            prefetched_ids = []
            
            for item_id, salience, tier in candidates[:request.max_items]:
                # Promote to L1
                if self._promote_to_l1(item_id):
                    prefetched_ids.append(item_id)
            
            return prefetched_ids
    
    def consolidate(self) -> Dict[str, int]:
        """
        Consolidate L1 items to L2/L3 based on importance and associations.
        
        Implements IMemoryManager.consolidate() from SPECIFICATION.md
        Strategy:
        - High importance items → L3 (semantic/knowledge)
        - Medium importance → L2 (episodic/recent)
        - Low importance → discard
        
        Returns:
            Dict with consolidation counts: {'to_l2': n, 'to_l3': m, 'discarded': k}
        """
        with self._lock:
            counts = {'to_l2': 0, 'to_l3': 0, 'discarded': 0}
            
            # Get items sorted by activation
            items = list(self._l1_items.items())
            items.sort(key=lambda x: x[1].compute_activation(), reverse=True)
            
            # Keep top capacity items in L1, consolidate rest
            items_to_consolidate = items[self.capacity:]
            
            # Print consolidation start
            if self.DEBUG_ENABLED:
                print(f"\n[MEMORY CONSOLIDATION] Starting:")
                print(f"  L1 Items: {len(self._l1_items)}")
                print(f"  Items to consolidate: {len(items_to_consolidate)}")
            
            for item_id, item in items_to_consolidate:
                # Remove from L1
                del self._l1_items[item_id]
                
                # Decide destination based on importance and associations
                if item.importance >= 0.7 or len(item.associations) > 2:
                    # High value → L3 (semantic)
                    self._l3_items[item_id] = item
                    counts['to_l3'] += 1
                    self.l2_consolidations += 1
                    
                    if self.DEBUG_ENABLED:
                        print(f"  → L3: {item_id[:8]}... (importance={item.importance:.2f}, assocs={len(item.associations)})")
                        print(f"     Content: {str(item.content)[:60]}...")
                    
                    # Build associations in L3
                    for assoc_id in item.associations:
                        self._l3_associations[item_id].append((assoc_id, 0.5))
                        self._l3_associations[assoc_id].append((item_id, 0.5))
                        
                elif item.importance >= 0.3:
                    # Medium value → L2 (episodic)
                    self._l2_items[item_id] = item
                    self._l2_access_order.append(item_id)
                    counts['to_l2'] += 1
                    
                    if self.DEBUG_ENABLED:
                        print(f"  → L2: {item_id[:8]}... (importance={item.importance:.2f})")
                        print(f"     Content: {str(item.content)[:60]}...")
                else:
                    # Low value → discard
                    counts['discarded'] += 1
                    if self.DEBUG_ENABLED:
                        print(f"  → DISCARD: {item_id[:8]}... (importance={item.importance:.2f})")
            
            if self.DEBUG_ENABLED:
                print(f"[MEMORY CONSOLIDATION] Complete:")
                print(f"  To L2: {counts['to_l2']}")
                print(f"  To L3: {counts['to_l3']}")
                print(f"  Discarded: {counts['discarded']}")
                print(f"  New L1 Size: {len(self._l1_items)}/{self.capacity}")
                print(f"  New L2 Size: {len(self._l2_items)}/{self.l2_capacity}")
                print(f"  New L3 Size: {len(self._l3_items)}")
            
            return counts
    
    def get_statistics(self) -> MemoryStatistics:
        """
        Get memory system statistics.
        
        Implements IMemoryManager.get_statistics() from SPECIFICATION.md
        
        Returns:
            MemoryStatistics with comprehensive metrics
        """
        with self._lock:
            # Calculate cache hit rate
            total_accesses = self.l1_hits + self.l1_misses
            hit_rate = self.l1_hits / total_accesses if total_accesses > 0 else 0.0
            
            # Calculate L3 average associations
            total_assocs = sum(len(assocs) for assocs in self._l3_associations.values())
            avg_assocs = total_assocs / len(self._l3_items) if self._l3_items else 0.0
            
            return MemoryStatistics(
                # L1
                l1_capacity=self.capacity,
                l1_size=len(self._l1_items),
                l1_utilization=len(self._l1_items) / self.capacity,
                l1_hits=self.l1_hits,
                l1_misses=self.l1_misses,
                l1_evictions=self.l1_evictions,
                # L2
                l2_size=len(self._l2_items),
                l2_hits=self.l2_hits,
                l2_consolidations=self.l2_consolidations,
                # L3
                l3_size=len(self._l3_items),
                l3_clusters=len(self._l3_clusters),
                l3_average_associations=avg_assocs,
                # Overall
                total_stores=self.total_stores,
                total_retrievals=self.total_retrievals,
                prefetch_requests=self.prefetch_requests,
                cache_hit_rate=hit_rate,
            )
    
    def _compute_salience(self, item: MemoryItem, request: PrefetchRequest) -> float:
        """
        Compute salience score for prefetching.
        
        Factors:
        - Tag overlap with context
        - Activation level
        - Source primitive match
        - Association strength
        """
        score = 0.0
        
        # Tag overlap (40% weight)
        if request.context_tags and item.tags:
            overlap = len(set(request.context_tags) & set(item.tags))
            score += 0.4 * (overlap / len(request.context_tags))
        
        # Activation level (30% weight)
        score += 0.3 * item.compute_activation()
        
        # Source primitive match (20% weight)
        if item.source_primitive == request.primitive_name:
            score += 0.2
        
        # Association count (10% weight)
        if item.associations:
            score += 0.1 * min(1.0, len(item.associations) / 5)
        
        return min(1.0, score)
    
    def _find_item_by_id(self, item_id: str) -> Optional[MemoryItem]:
        """Find item by ID across all tiers."""
        if item_id in self._l1_items:
            return self._l1_items[item_id]
        if item_id in self._l2_items:
            return self._l2_items[item_id]
        if item_id in self._l3_items:
            return self._l3_items[item_id]
        return None
    
    def _get_tier_items(self, tier: MemoryTier) -> Dict[str, MemoryItem]:
        """Get items dictionary for specified tier."""
        if tier == MemoryTier.L1_WORKING:
            return self._l1_items
        elif tier == MemoryTier.L2_EPISODIC:
            return self._l2_items
        elif tier == MemoryTier.L3_SEMANTIC:
            return self._l3_items
        return {}
    
    def _promote_to_l1(self, item_id: str) -> bool:
        """
        Promote item from L2/L3 to L1.
        
        Returns:
            True if promoted, False if already in L1 or not found
        """
        # Already in L1?
        if item_id in self._l1_items:
            return False
        
        # Find in L2/L3
        item = None
        source_tier = None
        
        if item_id in self._l2_items:
            item = self._l2_items[item_id]
            source_tier = MemoryTier.L2_EPISODIC
        elif item_id in self._l3_items:
            item = self._l3_items[item_id]
            source_tier = MemoryTier.L3_SEMANTIC
        
        if not item:
            return False
        
        if self.DEBUG_ENABLED:
            print(f"\n[MEMORY PROMOTION] {source_tier.value} → L1:")
            print(f"  Item ID: {item_id[:8]}...")
            print(f"  Content: {str(item.content)[:60]}...")
            print(f"  Importance: {item.importance:.2f}")
            print(f"  Activation: {item.compute_activation():.2f}")
        
        # Make space in L1 if needed
        if len(self._l1_items) >= self.capacity:
            if self.DEBUG_ENABLED:
                print(f"  L1 Full - triggering eviction")
            self._evict_lowest_activation()
        
        # Move to L1 (keep copy in original tier)
        self._l1_items[item_id] = item
        if self.DEBUG_ENABLED:
            print(f"  New L1 Size: {len(self._l1_items)}/{self.capacity}")
        
        return True
    
    def _trigger_consolidation(self) -> None:
        """Trigger automatic consolidation to L2/L3."""
        self.consolidate()
    
    def __len__(self) -> int:
        """Return total number of items across all tiers."""
        with self._lock:
            return len(self._l1_items) + len(self._l2_items) + len(self._l3_items)
    
    def __repr__(self) -> str:
        with self._lock:
            return (
                f"WorkingMemory(L1={len(self._l1_items)}/{self.capacity}, "
                f"L2={len(self._l2_items)}, "
                f"L3={len(self._l3_items)}, "
                f"focused={len(self._focus_items)})"
            )
    
    def print_memory_state(self, verbose: bool = False) -> None:
        """
        Print current memory state for debugging.
        
        Args:
            verbose: If True, print detailed item information
        """
        with self._lock:
            print("\n" + "="*70)
            print("[MEMORY STATE SUMMARY]")
            print("="*70)
            
            # L1 Working Memory
            print(f"\nL1 (Working Memory): {len(self._l1_items)}/{self.capacity} items")
            if verbose and self._l1_items:
                for item_id, item in list(self._l1_items.items())[:5]:  # Show first 5
                    print(f"  - {item_id[:8]}... | Act: {item.compute_activation():.2f} | Imp: {item.importance:.2f}")
                    print(f"    Content: {str(item.content)[:60]}...")
                if len(self._l1_items) > 5:
                    print(f"  ... and {len(self._l1_items) - 5} more items")
            
            # L2 Episodic Memory
            print(f"\nL2 (Episodic Memory): {len(self._l2_items)}/{self.l2_capacity} items")
            if verbose and self._l2_items:
                for item_id in self._l2_access_order[-5:]:  # Show last 5 accessed
                    if item_id in self._l2_items:
                        item = self._l2_items[item_id]
                        print(f"  - {item_id[:8]}... | Imp: {item.importance:.2f} | Access: {item.access_count}")
                        print(f"    Content: {str(item.content)[:60]}...")
                if len(self._l2_items) > 5:
                    print(f"  ... and {len(self._l2_items) - 5} more items")
            
            # L3 Semantic Memory
            print(f"\nL3 (Semantic Memory): {len(self._l3_items)} items")
            if verbose and self._l3_items:
                items_list = list(self._l3_items.items())[:5]
                for item_id, item in items_list:
                    assoc_count = len(self._l3_associations.get(item_id, []))
                    print(f"  - {item_id[:8]}... | Imp: {item.importance:.2f} | Assoc: {assoc_count}")
                    print(f"    Content: {str(item.content)[:60]}...")
                if len(self._l3_items) > 5:
                    print(f"  ... and {len(self._l3_items) - 5} more items")
            
            # Focus
            if self._focus_items:
                print(f"\nFocused Items: {len(self._focus_items)}")
                if verbose:
                    for item_id in self._focus_items:
                        print(f"  - {item_id[:8]}...")
            
            # Statistics
            print(f"\nStatistics:")
            print(f"  Total Stores: {self.total_stores}")
            print(f"  Total Retrievals: {self.total_retrievals}")
            print(f"  L1 Evictions: {self.l1_evictions}")
            print(f"  L2 Consolidations: {self.l2_consolidations}")
            print(f"  Cache Hit Rate: {self.l1_hits / max(1, self.l1_hits + self.l1_misses) * 100:.1f}%")
            
            print("="*70 + "\n")
