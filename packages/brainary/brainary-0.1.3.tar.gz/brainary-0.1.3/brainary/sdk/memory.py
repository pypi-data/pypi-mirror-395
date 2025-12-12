"""
Memory Management Utilities

Provides simplified memory management interface.
NOTE: This is a thin convenience wrapper around WorkingMemory.
"""

from typing import Any, List, Optional, Dict
from brainary.memory.working import WorkingMemory, MemoryItem
import time


class MemoryManager:
    """
    High-level memory management interface.
    
    Provides intuitive methods for storing and retrieving memories
    without needing to understand the underlying memory architecture.
    
    Examples:
        >>> from brainary.sdk import MemoryManager
        >>> memory = MemoryManager(capacity=10)
        >>> memory.store("Important fact", importance=0.9, tags=["critical"])
        >>> results = memory.search("fact", limit=5)
    """
    
    def __init__(self, capacity: int = 7):
        """
        Initialize memory manager.
        
        Args:
            capacity: Maximum working memory capacity (default: 7±2)
        """
        self._working_memory = WorkingMemory(capacity=capacity)
    
    def store(
        self,
        content: Any,
        importance: float = 0.5,
        tags: Optional[List[str]] = None,
        **kwargs
    ) -> str:
        """
        Store information in memory.
        
        Args:
            content: Content to store
            importance: Importance score (0-1, default: 0.5)
            tags: Tags for categorization and retrieval
            **kwargs: Additional parameters passed to WorkingMemory.store()
        
        Returns:
            Memory item ID (string)
        
        Examples:
            >>> memory = MemoryManager()
            >>> mem_id = memory.store(
            ...     "User prefers dark mode",
            ...     importance=0.7,
            ...     tags=["preference", "ui"]
            ... )
        """
        # Direct delegation to WorkingMemory - no duplication
        return self._working_memory.store(
            content=content,
            importance=importance,
            tags=tags or [],
            **kwargs
        )
    
    def retrieve(
        self,
        query: Optional[str] = None,
        tags: Optional[List[str]] = None,
        top_k: int = 5
    ) -> List[MemoryItem]:
        """
        Retrieve memories from working memory.
        
        Args:
            query: Optional search query
            tags: Optional tag filter
            top_k: Number of results to return
        
        Returns:
            List of MemoryItem objects
        
        Examples:
            >>> memory = MemoryManager()
            >>> idx = memory.store("test")
            >>> items = memory.retrieve("test", tags=None, top_k=1)
            >>> print(items[0].content if items else "Not found")
        """
        return self._working_memory.retrieve(query=query, tags=tags, top_k=top_k)
    
    def search(
        self,
        query: str,
        tags: Optional[List[str]] = None,
        min_importance: float = 0.0,
        limit: int = 10
    ) -> List[MemoryItem]:
        """
        Search memories by query and filters.
        
        Args:
            query: Search query
            tags: Filter by tags (optional)
            min_importance: Minimum importance threshold
            limit: Maximum results to return
        
        Returns:
            List of matching MemoryItems
        
        Examples:
            >>> memory = MemoryManager()
            >>> results = memory.search(
            ...     "user preference",
            ...     tags=["preference"],
            ...     min_importance=0.5
            ... )
        """
        # Retrieve from working memory
        all_results = self._working_memory.retrieve(
            query=query,
            tags=tags,
            top_k=limit * 2  # Get more to filter
        )
        
        # Filter by importance
        results = [
            item for item in all_results
            if item.importance >= min_importance
        ]
        
        return results[:limit]
    
    def get_by_tags(self, tags: List[str], limit: int = 10) -> List[MemoryItem]:
        """
        Retrieve memories by tags.
        
        Args:
            tags: Tags to search for
            limit: Maximum results
        
        Returns:
            List of matching MemoryItems
        
        Examples:
            >>> memory = MemoryManager()
            >>> preferences = memory.get_by_tags(["preference", "user"])
        """
        # Direct delegation to WorkingMemory
        return self._working_memory.retrieve(
            query=None,
            tags=tags,
            top_k=limit
        )
    
    def get_recent(self, count: int = 5) -> List[MemoryItem]:
        """
        Get most recent memories.
        
        Args:
            count: Number of recent entries to return
        
        Returns:
            List of recent MemoryItems
        
        Examples:
            >>> memory = MemoryManager()
            >>> recent = memory.get_recent(10)
        """
        # Get all items and sort by recency
        all_items = self._working_memory.retrieve(query=None, top_k=count * 2)
        sorted_items = sorted(
            all_items,
            key=lambda item: item.timestamp,
            reverse=True
        )
        return sorted_items[:count]
    
    def get_important(self, count: int = 5, threshold: float = 0.7) -> List[MemoryItem]:
        """
        Get most important memories.
        
        Args:
            count: Number of important entries to return
            threshold: Minimum importance threshold
        
        Returns:
            List of important MemoryItems
        
        Examples:
            >>> memory = MemoryManager()
            >>> important = memory.get_important(threshold=0.8)
        """
        # Get all items and filter by importance
        all_items = self._working_memory.retrieve(query=None, top_k=count * 2)
        filtered = [item for item in all_items if item.importance >= threshold]
        sorted_items = sorted(
            filtered,
            key=lambda item: item.importance,
            reverse=True
        )
        return sorted_items[:count]
    
    def clear(self) -> None:
        """
        Clear all memories.
        
        Examples:
            >>> memory = MemoryManager()
            >>> memory.clear()
        """
        # Recreate working memory to clear it
        capacity = self._working_memory.capacity
        self._working_memory = WorkingMemory(capacity=capacity)
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get memory statistics.
        
        Returns:
            Dictionary with memory statistics
        
        Examples:
            >>> memory = MemoryManager()
            >>> stats = memory.get_stats()
            >>> print(f"Total memories: {stats['total']}")
        """
        # Get statistics from WorkingMemory
        return self._working_memory.get_statistics().__dict__
    
    @property
    def working_memory(self) -> WorkingMemory:
        """Get underlying working memory instance."""
        return self._working_memory
    
    def __len__(self) -> int:
        """Return number of items in working memory."""
        stats = self._working_memory.get_statistics()
        return stats.total_items
    
    def __repr__(self) -> str:
        return f"MemoryManager(items={len(self)}, capacity={self._working_memory.capacity})"
