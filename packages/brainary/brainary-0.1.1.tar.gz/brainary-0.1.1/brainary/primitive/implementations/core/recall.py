"""
Retrieve information from working memory with intelligent attention and focus.
"""

from typing import Any, Dict, List, Optional, Tuple
import time
import logging

from brainary.primitive.base import (
    CorePrimitive,
    PrimitiveResult,
    ResourceEstimate,
    ConfidenceMetrics,
    CostMetrics,
)
from brainary.core.context import ExecutionContext
from brainary.memory.working import WorkingMemory
from brainary.memory.attention import AttentionMechanism, AttentionFocus
from brainary.memory.associative import AssociativeMemory
from brainary.llm.manager import get_llm_manager

logger = logging.getLogger(__name__)


class RecallWorkingMemory(CorePrimitive):
    """
    Retrieve information from working memory.
    
    Recalls stored information.
    """
    
    def __init__(self):
        """Initialize primitive."""
        super().__init__()
        self._name = "recall"
        self._hint = (
            "Use to retrieve information from working memory. Best when previously "
            "stored information is needed for current processing. Searches by tags, "
            "recency, or importance. Use when context from earlier operations is "
            "required. Suitable for all domains."
        )
    
    def execute(
        self,
        context: ExecutionContext,
        working_memory: WorkingMemory,
        query: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 5,
        **kwargs
    ) -> PrimitiveResult:
        """
        Recall information with intelligent attention and focus mechanisms.
        
        This is not just retrieval - it applies attention to focus on relevant memories,
        ranks by contextual relevance, synthesizes information across memories, and
        may discover emergent patterns.
        
        Args:
            context: Execution context
            working_memory: Working memory
            query: Search query (what information is needed?)
            tags: Filter by tags
            limit: Maximum results to retrieve initially
            **kwargs: Additional parameters (skip_analysis=False, current_goal, focus_type)
        
        Returns:
            PrimitiveResult with intelligently recalled and synthesized memories
        """
        start_time = time.time()
        
        # Simple retrieval mode for backward compatibility
        if kwargs.get('skip_analysis', False):
            items = working_memory.retrieve(query=query, tags=tags, limit=limit)
            execution_time = int((time.time() - start_time) * 1000)
            return PrimitiveResult(
                content={'query': query, 'tags': tags, 'items': items, 'count': len(items)},
                confidence=ConfidenceMetrics(overall=0.9 if items else 0.5, reasoning=0.9, completeness=0.85, consistency=0.9, evidence_strength=0.8 if items else 0.5),
                execution_mode=context.execution_mode,
                cost=CostMetrics(tokens=0, latency_ms=execution_time, memory_slots=0, provider_cost_usd=0.0),
                primitive_name=self.name,
                success=True,
                metadata={'count': len(items)}
            )
        
        try:
            # Retrieve more items than requested for intelligent filtering
            initial_limit = min(limit * 3, 20)
            
            # Retrieve candidate memories
            items = working_memory.retrieve(
                query=query,
                tags=tags,
                limit=initial_limit,
            )
            
            if not items:
                execution_time = int((time.time() - start_time) * 1000)
                return PrimitiveResult(
                    content={
                        'query': query,
                        'tags': tags,
                        'items': [],
                        'count': 0,
                        'message': 'No memories found matching query'
                    },
                    confidence=ConfidenceMetrics(overall=0.5, reasoning=0.5, completeness=0.5, consistency=0.5, evidence_strength=0.3),
                    execution_mode=context.execution_mode,
                    cost=CostMetrics(tokens=0, latency_ms=execution_time, memory_slots=0, provider_cost_usd=0.0),
                    primitive_name=self.name,
                    success=True,
                    metadata={'count': 0}
                )
            
            # Extract additional context
            current_goal = kwargs.get('current_goal', '')
            focus_type = kwargs.get('focus_type', 'general')  # general, detailed, pattern, summary
            
            # Format candidate memories
            candidates_text = "\n".join([
                f"[{i+1}] Importance: {item.importance:.2f} | Tags: {', '.join(item.tags[:3])} | Content: {item.content[:150]}"
                for i, item in enumerate(items)
            ])
            
            # Build intelligent recall prompt
            prompt = f"""Apply attention and focus mechanisms to intelligently recall relevant memories.

RECALL QUERY:
{query if query else "General memory retrieval"}

CANDIDATE MEMORIES (retrieved by semantic similarity):
{candidates_text}

CONTEXT:
- Current Goal: {current_goal if current_goal else "Not specified"}
- Focus Type: {focus_type}
- Requested Limit: {limit}

Provide comprehensive recall analysis with:

1. ATTENTION FOCUS: Which memories deserve focused attention and why?
   Rank the top {limit} most relevant memories by index [1, 2, 3...]
   Explain attention allocation reasoning

2. RELEVANCE ANALYSIS: For each selected memory, explain its relevance
   Why is this memory important for the current query/goal?

3. MEMORY SYNTHESIS: Synthesize information across selected memories
   What coherent understanding emerges from these memories together?

4. PATTERN DETECTION: Identify patterns or themes across memories
   Are there recurring concepts, trends, or relationships?

5. CONTEXTUAL CONNECTIONS: How do these memories relate to each other?
   Temporal, causal, conceptual, or hierarchical relationships?

6. MISSING INFORMATION: What relevant information seems to be missing?
   What gaps exist that might need additional recall or new information?

7. RETRIEVAL CONFIDENCE: How confident are you this recall is complete?
   Rate 0.0-1.0 and explain uncertainty sources

Be specific about which memory indices are most relevant and why."""

            # Get LLM attention and recall analysis
            llm_manager = get_llm_manager()
            response = llm_manager.request(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
            )
            
            analysis_text = response.content
            
            # Parse sections
            sections = {}
            section_names = ["ATTENTION FOCUS:", "RELEVANCE ANALYSIS:", "MEMORY SYNTHESIS:", 
                           "PATTERN DETECTION:", "CONTEXTUAL CONNECTIONS:", "MISSING INFORMATION:", 
                           "RETRIEVAL CONFIDENCE:"]
            for i, section_name in enumerate(section_names):
                start_idx = analysis_text.find(section_name)
                if start_idx == -1:
                    sections[section_name.rstrip(':')] = ""
                    continue
                
                end_idx = len(analysis_text)
                for next_section in section_names[i+1:]:
                    next_idx = analysis_text.find(next_section)
                    if next_idx != -1:
                        end_idx = next_idx
                        break
                
                sections[section_name.rstrip(':')] = analysis_text[start_idx+len(section_name):end_idx].strip()
            
            # Extract ranked memory indices
            attention_text = sections.get('ATTENTION FOCUS', '')
            ranked_indices = []
            import re
            for match in re.finditer(r'\[(\d+)\]', attention_text):
                idx = int(match.group(1)) - 1  # Convert to 0-based
                if 0 <= idx < len(items) and idx not in ranked_indices:
                    ranked_indices.append(idx)
            
            # If no indices found, use first N items
            if not ranked_indices:
                ranked_indices = list(range(min(limit, len(items))))
            
            # Select focused memories (limit to requested count)
            focused_items = [items[idx] for idx in ranked_indices[:limit]]
            
            # Apply attention mechanism to boost activation of focused items
            attention_mechanism = AttentionMechanism(working_memory)
            
            # Extract keywords from query for attention focus
            if query:
                keywords = [word for word in query.split() if len(word) > 3][:5]
                if keywords:
                    attention_mechanism.set_focus(
                        keywords=keywords,
                        importance_bias=0.2,  # Boost importance for attended items
                        recency_weight=0.3,
                    )
            
            # Retrieve associated memories using associative graph
            associative_memory = AssociativeMemory(working_memory)
            associated_items = []
            for item in focused_items:
                # Get items associated with this memory
                associations = associative_memory.get_associated(
                    item_id=item.id,
                    min_strength=0.5,
                    max_depth=1  # Only direct associations
                )
                for assoc_item, strength, depth in associations[:2]:  # Top 2 associations per item
                    if assoc_item.id not in [fi.id for fi in focused_items]:
                        associated_items.append((assoc_item, strength))
            
            # Extract retrieval confidence
            confidence_text = sections.get('RETRIEVAL CONFIDENCE', '').lower()
            retrieval_confidence = 0.8  # Default
            conf_match = re.search(r'(\d+\.?\d*)', confidence_text)
            if conf_match:
                score = float(conf_match.group(1))
                if score <= 1.0:
                    retrieval_confidence = score
                elif score <= 10.0:
                    retrieval_confidence = score / 10.0
            
            # Check for high confidence indicators
            if 'very confident' in confidence_text or 'highly confident' in confidence_text:
                retrieval_confidence = max(retrieval_confidence, 0.9)
            elif 'not confident' in confidence_text or 'uncertain' in confidence_text:
                retrieval_confidence = min(retrieval_confidence, 0.6)
            
            result = {
                'query': query,
                'tags': tags,
                'items': focused_items,
                'count': len(focused_items),
                'total_candidates': len(items),
                'associated_items': [item for item, _ in associated_items],
                'associated_count': len(associated_items),
                'attention_ranking': [idx + 1 for idx in ranked_indices[:limit]],
                'attention_focus': sections.get('ATTENTION FOCUS', ''),
                'relevance_analysis': sections.get('RELEVANCE ANALYSIS', ''),
                'synthesis': sections.get('MEMORY SYNTHESIS', ''),
                'patterns': sections.get('PATTERN DETECTION', ''),
                'connections': sections.get('CONTEXTUAL CONNECTIONS', ''),
                'missing_information': sections.get('MISSING INFORMATION', ''),
                'retrieval_confidence': retrieval_confidence,
                'focus_type': focus_type,
                'attention_mechanism_used': bool(query and len(query.split()) > 0),
                'associative_retrieval_used': len(associated_items) > 0,
            }
            
            # Store recall event for meta-memory
            working_memory.store(
                content=f"Recalled {len(focused_items)} memories for: {query if query else 'general retrieval'}",
                importance=0.5,
                tags=["memory-recall", "meta-memory", "attention"] + (tags or [])[:2],
            )
            
            execution_time = int((time.time() - start_time) * 1000)
            
            return PrimitiveResult(
                content=result,
                confidence=ConfidenceMetrics(
                    overall=min(0.92, retrieval_confidence + 0.05),
                    reasoning=0.88,
                    completeness=retrieval_confidence,
                    consistency=0.85,
                    evidence_strength=0.9 if focused_items else 0.5,
                ),
                execution_mode=context.execution_mode,
                cost=CostMetrics(
                    tokens=response.usage.total_tokens,
                    latency_ms=execution_time,
                    memory_slots=0,
                    provider_cost_usd=response.cost,
                ),
                primitive_name=self.name,
                success=True,
                metadata={
                    'count': len(focused_items),
                    'candidates_evaluated': len(items),
                    'attention_applied': True,
                    'synthesis_generated': bool(sections.get('MEMORY SYNTHESIS')),
                    'patterns_found': bool(sections.get('PATTERN DETECTION')),
                    'model': 'gpt-4o-mini',
                }
            )
            
        except Exception as e:
            logger.error(f"Intelligent recall failed, falling back to simple retrieval: {e}")
            # Fallback to simple retrieval
            items = working_memory.retrieve(query=query, tags=tags, limit=limit)
            execution_time = int((time.time() - start_time) * 1000)
            return PrimitiveResult(
                content={
                    'query': query,
                    'tags': tags,
                    'items': items,
                    'count': len(items),
                    'fallback': True,
                    'error': str(e)
                },
                confidence=ConfidenceMetrics(
                    overall=0.7 if items else 0.5,
                    reasoning=0.7,
                    completeness=0.7,
                    consistency=0.7,
                    evidence_strength=0.7 if items else 0.5,
                ),
                execution_mode=context.execution_mode,
                cost=CostMetrics(
                    tokens=0,
                    latency_ms=execution_time,
                    memory_slots=0,
                    provider_cost_usd=0.0,
                ),
                primitive_name=self.name,
                success=True,
                metadata={'count': len(items), 'fallback': True}
            )
    
    def estimate_cost(self, **kwargs) -> ResourceEstimate:
        """Estimate execution cost."""
        return ResourceEstimate(
            tokens=0,
            time_ms=3,
            memory_items=0,
            complexity=0.2,
        )
    
    def validate_inputs(self, **kwargs) -> None:
        """Validate inputs."""
        pass  # No required parameters
    
    def matches_context(self, context: ExecutionContext, **kwargs) -> float:
        """Check context match."""
        return 1.0  # Always available
    
    def rollback(self, context: ExecutionContext) -> None:
        """Rollback recall."""
        pass


