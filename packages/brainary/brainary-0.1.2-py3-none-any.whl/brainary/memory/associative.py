"""
Associative memory for building semantic relationships.

Implements graph-based associations between memory items to enable
relationship-based retrieval and reasoning.
"""

from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
import threading

from brainary.memory.working import WorkingMemory, MemoryItem


@dataclass
class Association:
    """Association between two memory items."""
    
    source_id: str
    target_id: str
    association_type: str = "related"  # Type of relationship
    strength: float = 0.5              # Association strength (0.0-1.0)
    bidirectional: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate strength."""
        if not 0.0 <= self.strength <= 1.0:
            raise ValueError("strength must be in [0.0, 1.0]")


class AssociativeMemory:
    """
    Associative memory for semantic relationships.
    
    Builds and traverses semantic graph of memory items to enable:
    - Relationship-based retrieval
    - Spreading activation
    - Analogical reasoning
    - Concept clustering
    """
    
    def __init__(self, working_memory: WorkingMemory):
        """
        Initialize associative memory.
        
        Args:
            working_memory: WorkingMemory instance
        """
        self.working_memory = working_memory
        self._associations: Dict[str, List[Association]] = {}  # source_id -> associations
        self._reverse_index: Dict[str, List[str]] = {}  # target_id -> source_ids
        self._lock = threading.RLock()
    
    def associate(
        self,
        source_id: str,
        target_id: str,
        association_type: str = "related",
        strength: float = 0.5,
        bidirectional: bool = True,
        **metadata
    ) -> bool:
        """
        Create association between two items.
        
        Args:
            source_id: Source item ID
            target_id: Target item ID
            association_type: Type of relationship
            strength: Association strength (0.0-1.0)
            bidirectional: If True, create reverse association too
            **metadata: Additional metadata
        
        Returns:
            True if created, False if items not found
        """
        with self._lock:
            # Verify items exist
            if source_id not in self.working_memory._items:
                return False
            if target_id not in self.working_memory._items:
                return False
            
            # Create forward association
            assoc = Association(
                source_id=source_id,
                target_id=target_id,
                association_type=association_type,
                strength=strength,
                bidirectional=bidirectional,
                metadata=metadata,
            )
            
            if source_id not in self._associations:
                self._associations[source_id] = []
            self._associations[source_id].append(assoc)
            
            # Update reverse index
            if target_id not in self._reverse_index:
                self._reverse_index[target_id] = []
            self._reverse_index[target_id].append(source_id)
            
            # Create reverse association if bidirectional
            if bidirectional:
                reverse_assoc = Association(
                    source_id=target_id,
                    target_id=source_id,
                    association_type=association_type,
                    strength=strength,
                    bidirectional=False,  # Prevent infinite recursion
                    metadata=metadata,
                )
                
                if target_id not in self._associations:
                    self._associations[target_id] = []
                self._associations[target_id].append(reverse_assoc)
                
                if source_id not in self._reverse_index:
                    self._reverse_index[source_id] = []
                self._reverse_index[source_id].append(target_id)
            
            # Update item associations list
            source_item = self.working_memory._items[source_id]
            if target_id not in source_item.associations:
                source_item.associations.append(target_id)
            
            if bidirectional:
                target_item = self.working_memory._items[target_id]
                if source_id not in target_item.associations:
                    target_item.associations.append(source_id)
            
            return True
    
    def get_associated(
        self,
        item_id: str,
        association_type: Optional[str] = None,
        min_strength: float = 0.0,
        max_depth: int = 1
    ) -> List[Tuple[MemoryItem, float, int]]:
        """
        Get items associated with given item.
        
        Args:
            item_id: Source item ID
            association_type: Filter by association type
            min_strength: Minimum association strength
            max_depth: Maximum traversal depth (1 = direct associations)
        
        Returns:
            List of (MemoryItem, cumulative_strength, depth) tuples
        """
        with self._lock:
            visited: Set[str] = set()
            results: List[Tuple[MemoryItem, float, int]] = []
            
            self._traverse_associations(
                item_id=item_id,
                depth=0,
                max_depth=max_depth,
                cumulative_strength=1.0,
                association_type=association_type,
                min_strength=min_strength,
                visited=visited,
                results=results,
            )
            
            # Sort by strength * recency
            results.sort(key=lambda x: x[1], reverse=True)
            
            return results
    
    def strengthen_association(
        self,
        source_id: str,
        target_id: str,
        delta: float = 0.1
    ) -> bool:
        """
        Strengthen existing association.
        
        Args:
            source_id: Source item ID
            target_id: Target item ID
            delta: Strength increase amount
        
        Returns:
            True if strengthened, False if not found
        """
        with self._lock:
            associations = self._associations.get(source_id, [])
            
            for assoc in associations:
                if assoc.target_id == target_id:
                    assoc.strength = min(1.0, assoc.strength + delta)
                    
                    # Strengthen reverse if bidirectional
                    if assoc.bidirectional:
                        self.strengthen_association(target_id, source_id, delta)
                    
                    return True
            
            return False
    
    def weaken_association(
        self,
        source_id: str,
        target_id: str,
        delta: float = 0.1
    ) -> bool:
        """
        Weaken existing association.
        
        Args:
            source_id: Source item ID
            target_id: Target item ID
            delta: Strength decrease amount
        
        Returns:
            True if weakened, False if not found
        """
        with self._lock:
            associations = self._associations.get(source_id, [])
            
            for assoc in associations:
                if assoc.target_id == target_id:
                    assoc.strength = max(0.0, assoc.strength - delta)
                    
                    # Remove if strength drops to zero
                    if assoc.strength == 0.0:
                        self.remove_association(source_id, target_id)
                    elif assoc.bidirectional:
                        self.weaken_association(target_id, source_id, delta)
                    
                    return True
            
            return False
    
    def remove_association(self, source_id: str, target_id: str) -> bool:
        """
        Remove association between items.
        
        Args:
            source_id: Source item ID
            target_id: Target item ID
        
        Returns:
            True if removed, False if not found
        """
        with self._lock:
            associations = self._associations.get(source_id, [])
            
            for i, assoc in enumerate(associations):
                if assoc.target_id == target_id:
                    is_bidirectional = assoc.bidirectional
                    
                    # Remove forward association
                    del associations[i]
                    
                    # Update reverse index
                    if target_id in self._reverse_index:
                        try:
                            self._reverse_index[target_id].remove(source_id)
                        except ValueError:
                            pass
                    
                    # Remove reverse association if bidirectional
                    if is_bidirectional:
                        self.remove_association(target_id, source_id)
                    
                    return True
            
            return False
    
    def find_paths(
        self,
        start_id: str,
        end_id: str,
        max_depth: int = 3
    ) -> List[List[str]]:
        """
        Find paths between two items in association graph.
        
        Args:
            start_id: Start item ID
            end_id: End item ID
            max_depth: Maximum path length
        
        Returns:
            List of paths (each path is list of item IDs)
        """
        with self._lock:
            paths: List[List[str]] = []
            self._find_paths_recursive(
                current_id=start_id,
                end_id=end_id,
                current_path=[start_id],
                max_depth=max_depth,
                visited=set([start_id]),
                paths=paths,
            )
            return paths
    
    def cluster_by_associations(
        self,
        min_cluster_size: int = 2,
        min_strength: float = 0.5
    ) -> List[List[str]]:
        """
        Cluster items by association strength.
        
        Args:
            min_cluster_size: Minimum items per cluster
            min_strength: Minimum association strength for clustering
        
        Returns:
            List of clusters (each cluster is list of item IDs)
        """
        with self._lock:
            visited: Set[str] = set()
            clusters: List[List[str]] = []
            
            for item_id in self.working_memory._items.keys():
                if item_id in visited:
                    continue
                
                # Build cluster from this seed
                cluster = self._build_cluster(item_id, min_strength, visited)
                
                if len(cluster) >= min_cluster_size:
                    clusters.append(cluster)
            
            return clusters
    
    def _traverse_associations(
        self,
        item_id: str,
        depth: int,
        max_depth: int,
        cumulative_strength: float,
        association_type: Optional[str],
        min_strength: float,
        visited: Set[str],
        results: List[Tuple[MemoryItem, float, int]],
    ) -> None:
        """Recursively traverse association graph."""
        if depth >= max_depth or item_id in visited:
            return
        
        visited.add(item_id)
        associations = self._associations.get(item_id, [])
        
        for assoc in associations:
            if association_type and assoc.association_type != association_type:
                continue
            
            strength = cumulative_strength * assoc.strength
            if strength < min_strength:
                continue
            
            target_item = self.working_memory._items.get(assoc.target_id)
            if target_item:
                results.append((target_item, strength, depth + 1))
                
                # Recurse
                self._traverse_associations(
                    item_id=assoc.target_id,
                    depth=depth + 1,
                    max_depth=max_depth,
                    cumulative_strength=strength,
                    association_type=association_type,
                    min_strength=min_strength,
                    visited=visited,
                    results=results,
                )
    
    def _find_paths_recursive(
        self,
        current_id: str,
        end_id: str,
        current_path: List[str],
        max_depth: int,
        visited: Set[str],
        paths: List[List[str]],
    ) -> None:
        """Recursively find paths in association graph."""
        if len(current_path) > max_depth:
            return
        
        if current_id == end_id:
            paths.append(current_path.copy())
            return
        
        associations = self._associations.get(current_id, [])
        for assoc in associations:
            if assoc.target_id not in visited:
                visited.add(assoc.target_id)
                current_path.append(assoc.target_id)
                
                self._find_paths_recursive(
                    current_id=assoc.target_id,
                    end_id=end_id,
                    current_path=current_path,
                    max_depth=max_depth,
                    visited=visited,
                    paths=paths,
                )
                
                current_path.pop()
                visited.remove(assoc.target_id)
    
    def _build_cluster(
        self,
        seed_id: str,
        min_strength: float,
        visited: Set[str]
    ) -> List[str]:
        """Build cluster from seed item using BFS."""
        cluster = [seed_id]
        visited.add(seed_id)
        queue = [seed_id]
        
        while queue:
            current_id = queue.pop(0)
            associations = self._associations.get(current_id, [])
            
            for assoc in associations:
                if assoc.target_id in visited:
                    continue
                if assoc.strength < min_strength:
                    continue
                
                cluster.append(assoc.target_id)
                visited.add(assoc.target_id)
                queue.append(assoc.target_id)
        
        return cluster
