"""
Attention mechanism for working memory.

Implements attention-based focus that prioritizes important information
and optimizes retrieval based on context.
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass

from brainary.memory.working import WorkingMemory, MemoryItem


@dataclass
class AttentionFocus:
    """Attention focus configuration."""
    
    keywords: List[str]
    importance_bias: float = 0.0  # Boost to importance scores
    recency_weight: float = 0.3
    frequency_weight: float = 0.2
    semantic_threshold: float = 0.6


class AttentionMechanism:
    """
    Attention mechanism for working memory focus.
    
    Manages attention by:
    - Filtering items based on relevance
    - Boosting activation of attended items
    - Prioritizing retrieval based on attention
    """
    
    def __init__(self, working_memory: WorkingMemory):
        """
        Initialize attention mechanism.
        
        Args:
            working_memory: WorkingMemory instance to manage
        """
        self.working_memory = working_memory
        self.current_focus: Optional[AttentionFocus] = None
        self.attention_history: List[AttentionFocus] = []
    
    def set_focus(
        self,
        keywords: List[str],
        importance_bias: float = 0.2,
        recency_weight: float = 0.3,
        frequency_weight: float = 0.2
    ) -> None:
        """
        Set attention focus.
        
        Args:
            keywords: Keywords to focus on
            importance_bias: Boost to importance for focused items
            recency_weight: Weight for recency in attention
            frequency_weight: Weight for frequency in attention
        """
        focus = AttentionFocus(
            keywords=keywords,
            importance_bias=importance_bias,
            recency_weight=recency_weight,
            frequency_weight=frequency_weight,
        )
        
        self.current_focus = focus
        self.attention_history.append(focus)
        
        # Update working memory focus
        focused_items = self._compute_focused_items()
        self.working_memory.set_focus(focused_items)
    
    def clear_focus(self) -> None:
        """Clear current attention focus."""
        self.current_focus = None
        self.working_memory.set_focus([])
    
    def retrieve_attended(
        self,
        top_k: int = 3,
        min_relevance: float = 0.5
    ) -> List[MemoryItem]:
        """
        Retrieve items matching current attention focus.
        
        Args:
            top_k: Number of top items to return
            min_relevance: Minimum relevance threshold
        
        Returns:
            List of relevant MemoryItems
        """
        if not self.current_focus:
            # No focus set, return highest activation items
            return self.working_memory.retrieve(top_k=top_k)
        
        # Score all items by relevance to focus
        scored_items = []
        for item_id, item in self.working_memory._items.items():
            relevance = self._compute_relevance(item)
            if relevance >= min_relevance:
                scored_items.append((relevance, item))
        
        # Sort by relevance and return top_k
        scored_items.sort(key=lambda x: x[0], reverse=True)
        results = [item for _, item in scored_items[:top_k]]
        
        # Record access
        for item in results:
            item.access()
        
        return results
    
    def boost_attention(self, item_id: str, boost: float = 0.2) -> bool:
        """
        Boost attention/importance of specific item.
        
        Args:
            item_id: Item to boost
            boost: Importance boost amount
        
        Returns:
            True if boosted, False if not found
        """
        item = self.working_memory._items.get(item_id)
        if not item:
            return False
        
        new_importance = min(1.0, item.importance + boost)
        return self.working_memory.update(item_id, importance=new_importance)
    
    def _compute_focused_items(self) -> List[str]:
        """
        Compute item IDs matching current focus.
        
        Returns:
            List of focused item IDs
        """
        if not self.current_focus:
            return []
        
        focused_ids = []
        for item_id, item in self.working_memory._items.items():
            relevance = self._compute_relevance(item)
            if relevance >= self.current_focus.semantic_threshold:
                focused_ids.append(item_id)
        
        return focused_ids
    
    def _compute_relevance(self, item: MemoryItem) -> float:
        """
        Compute relevance of item to current focus.
        
        Args:
            item: Memory item
        
        Returns:
            Relevance score (0.0-1.0)
        """
        if not self.current_focus:
            return 0.0
        
        # Keyword matching (simple string containment for now)
        keyword_score = 0.0
        content_str = str(item.content).lower()
        for keyword in self.current_focus.keywords:
            if keyword.lower() in content_str:
                keyword_score += 1.0
        keyword_score = min(1.0, keyword_score / len(self.current_focus.keywords))
        
        # Tag matching
        tag_score = 0.0
        for keyword in self.current_focus.keywords:
            if keyword in item.tags:
                tag_score += 1.0
        tag_score = min(1.0, tag_score / len(self.current_focus.keywords))
        
        # Combine scores
        relevance = 0.6 * keyword_score + 0.4 * tag_score
        
        # Apply recency and frequency weights
        activation = item.compute_activation()
        relevance = (
            0.7 * relevance +
            self.current_focus.recency_weight * activation +
            self.current_focus.frequency_weight * (item.access_count / 10.0)
        )
        
        return min(1.0, relevance)
