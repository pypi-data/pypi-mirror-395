"""
Store information in working memory with intelligent association and organization.
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
from brainary.memory.associative import AssociativeMemory
from brainary.llm.manager import get_llm_manager

logger = logging.getLogger(__name__)


class RememberWorkingMemory(CorePrimitive):
    """
    Store information in working memory.
    
    Retains information for short-term use.
    """
    
    def __init__(self):
        """Initialize primitive."""
        super().__init__()
        self._name = "remember"
        self._hint = (
            "Use to store information in working memory for short-term retention. "
            "Best for intermediate results, context, or information needed later "
            "in processing. Assigns importance and tags for retrieval. Use when "
            "information needs to be available for subsequent operations. Suitable "
            "for all domains."
        )
    
    def execute(
        self,
        context: ExecutionContext,
        working_memory: WorkingMemory,
        content: str,
        importance: float = 0.5,
        tags: List[str] = None,
        **kwargs
    ) -> PrimitiveResult:
        """
        Remember information with intelligent association and organization.
        
        This is not just storage - it builds associations with existing memories,
        assesses importance, generates semantic tags, and may reorganize memory structure.
        
        Args:
            context: Execution context
            working_memory: Working memory
            content: Content to remember
            importance: Initial importance score (0-1), may be adjusted by LLM
            tags: Initial tags, will be enriched by LLM
            **kwargs: Additional parameters (skip_analysis=False to use simple storage)
        
        Returns:
            PrimitiveResult with memory ID and associations
        """
        start_time = time.time()
        
        # Simple storage mode for backward compatibility
        if kwargs.get('skip_analysis', False):
            memory_id = working_memory.store(
                content=content,
                importance=importance,
                tags=tags or [],
            )
            execution_time = int((time.time() - start_time) * 1000)
            return PrimitiveResult(
                content={'content': content, 'memory_id': memory_id, 'importance': importance, 'tags': tags or []},
                confidence=ConfidenceMetrics(overall=1.0, reasoning=1.0, completeness=1.0, consistency=1.0, evidence_strength=1.0),
                execution_mode=context.execution_mode,
                cost=CostMetrics(tokens=0, latency_ms=execution_time, memory_slots=1, provider_cost_usd=0.0),
                primitive_name=self.name,
                success=True,
                metadata={'memory_id': memory_id}
            )
        
        try:
            # Retrieve related memories for association building
            existing_items = working_memory.retrieve(
                query=content[:200],  # Use first 200 chars for semantic search
                top_k=5
            )
            existing_context = "\n".join([
                f"- [{item.importance:.2f}] {item.content[:100]}" 
                for item in existing_items
            ]) if existing_items else "No related memories found"
            
            # Get current memory statistics
            all_items = working_memory.retrieve(query="", top_k=20)
            memory_stats = {
                'total_items': len(all_items),
                'avg_importance': sum(item.importance for item in all_items) / len(all_items) if all_items else 0.5,
            }
            
            # Build memory integration prompt
            prompt = f"""Analyze how to optimally integrate this new information into memory.

NEW INFORMATION TO REMEMBER:
{content}

INITIAL IMPORTANCE: {importance}
INITIAL TAGS: {tags or []}

RELATED EXISTING MEMORIES:
{existing_context}

MEMORY CONTEXT:
- Total items in memory: {memory_stats['total_items']}
- Average importance: {memory_stats['avg_importance']:.2f}

Provide comprehensive memory integration analysis with:

1. IMPORTANCE ASSESSMENT: Evaluate the true importance of this information (0.0-1.0)
   Consider: uniqueness, relevance to goals, temporal value, generalizability

2. SEMANTIC TAGS: Generate rich semantic tags for effective retrieval
   Include: topic, domain, type, concepts, relationships

3. ASSOCIATIONS: Identify associations with existing memories
   List memory indices and explain relationships (causal, temporal, conceptual, etc.)

4. MEMORY ORGANIZATION: Suggest any memory reorganization needed
   Should any existing memories be consolidated, re-tagged, or re-prioritized?

5. CONSOLIDATION OPPORTUNITIES: Can this be merged with existing memories?
   If yes, suggest how to consolidate without losing information

6. RETRIEVAL CUES: What future queries should retrieve this memory?
   List specific phrases or contexts that should trigger recall

Be specific and actionable in your memory integration strategy."""

            # Get LLM memory integration analysis
            llm_manager = get_llm_manager()
            response = llm_manager.request(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )
            
            analysis_text = response.content
            
            # Parse sections
            sections = {}
            section_names = ["IMPORTANCE ASSESSMENT:", "SEMANTIC TAGS:", "ASSOCIATIONS:", 
                           "MEMORY ORGANIZATION:", "CONSOLIDATION OPPORTUNITIES:", "RETRIEVAL CUES:"]
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
            
            # Extract adjusted importance
            importance_text = sections.get('IMPORTANCE ASSESSMENT', '')
            adjusted_importance = importance
            for line in importance_text.split('\n'):
                if 'importance:' in line.lower() or 'score:' in line.lower():
                    import re
                    match = re.search(r'(\d+\.?\d*)', line)
                    if match:
                        score = float(match.group(1))
                        if score <= 1.0:
                            adjusted_importance = score
                        elif score <= 10.0:
                            adjusted_importance = score / 10.0
                        break
            
            # Extract semantic tags
            tags_text = sections.get('SEMANTIC TAGS', '')
            enriched_tags = list(tags) if tags else []
            for line in tags_text.split('\n'):
                line = line.strip('- •*').strip()
                if line and len(line) < 50:
                    # Extract tag-like phrases
                    if ':' in line:
                        parts = line.split(':', 1)
                        if len(parts[1].strip()) < 30:
                            enriched_tags.append(parts[1].strip().lower())
                    elif len(line.split()) <= 3:
                        enriched_tags.append(line.lower())
            
            # Remove duplicates while preserving order
            enriched_tags = list(dict.fromkeys(enriched_tags))[:10]  # Limit to 10 tags
            
            # Extract associations
            associations_text = sections.get('ASSOCIATIONS', '')
            associations = []
            for line in associations_text.split('\n'):
                if line.strip():
                    associations.append(line.strip('- •*').strip())
            
            # Extract consolidation suggestions
            consolidation_text = sections.get('CONSOLIDATION OPPORTUNITIES', '')
            should_consolidate = 'yes' in consolidation_text.lower()[:100] or 'merge' in consolidation_text.lower()[:100]
            
            # Store in memory with enhanced metadata
            memory_id = working_memory.store(
                content=content,
                importance=adjusted_importance,
                tags=enriched_tags,
            )
            
            # Create actual associations in associative memory
            associative_memory = AssociativeMemory(working_memory)
            associations_created = 0
            
            for i, item in enumerate(existing_items):
                # Parse association strength from LLM response
                assoc_strength = 0.5  # Default
                assoc_type = "related"
                
                # Try to extract relationship type from association text
                for assoc_line in associations:
                    if item.content[:30] in assoc_line:
                        if 'causal' in assoc_line.lower():
                            assoc_type = "causal"
                            assoc_strength = 0.7
                        elif 'temporal' in assoc_line.lower() or 'before' in assoc_line.lower() or 'after' in assoc_line.lower():
                            assoc_type = "temporal"
                            assoc_strength = 0.6
                        elif 'conceptual' in assoc_line.lower() or 'similar' in assoc_line.lower():
                            assoc_type = "conceptual"
                            assoc_strength = 0.8
                        elif 'contrast' in assoc_line.lower() or 'opposite' in assoc_line.lower():
                            assoc_type = "contrast"
                            assoc_strength = 0.6
                        break
                
                # Create bidirectional association
                if associative_memory.associate(
                    source_id=memory_id,
                    target_id=item.id,
                    association_type=assoc_type,
                    strength=assoc_strength,
                    bidirectional=True,
                    discovered_by="remember_primitive",
                ):
                    associations_created += 1
            
            result = {
                'content': content,
                'memory_id': memory_id,
                'original_importance': importance,
                'adjusted_importance': adjusted_importance,
                'original_tags': tags or [],
                'enriched_tags': enriched_tags,
                'associations': associations,
                'associations_created': associations_created,
                'should_consolidate': should_consolidate,
                'consolidation_suggestion': consolidation_text,
                'organization_suggestions': sections.get('MEMORY ORGANIZATION', ''),
                'retrieval_cues': sections.get('RETRIEVAL CUES', ''),
            }
            
            # Store memory integration metadata
            working_memory.store(
                content=f"Remembered with {associations_created} graph associations: {content[:100]}",
                importance=0.6,
                tags=["memory-integration", "meta-memory"] + enriched_tags[:3],
            )
            
            execution_time = int((time.time() - start_time) * 1000)
            
            return PrimitiveResult(
                content=result,
                confidence=ConfidenceMetrics(
                    overall=0.88,
                    reasoning=0.9,
                    completeness=0.88,
                    consistency=0.85,
                    evidence_strength=0.88,
                ),
                execution_mode=context.execution_mode,
                cost=CostMetrics(
                    tokens=response.usage.total_tokens,
                    latency_ms=execution_time,
                    memory_slots=1,
                    provider_cost_usd=response.cost,
                ),
                primitive_name=self.name,
                success=True,
                metadata={
                    'memory_id': memory_id,
                    'importance_adjusted': adjusted_importance != importance,
                    'tags_enriched': len(enriched_tags) > len(tags or []),
                    'associations_found': len(associations),
                    'model': 'gpt-4o-mini',
                }
            )
            
        except Exception as e:
            logger.error(f"Intelligent memory storage failed, falling back to simple storage: {e}")
            # Fallback to simple storage
            memory_id = working_memory.store(
                content=content,
                importance=importance,
                tags=tags or [],
            )
            execution_time = int((time.time() - start_time) * 1000)
            return PrimitiveResult(
                content={
                    'content': content,
                    'memory_id': memory_id,
                    'importance': importance,
                    'tags': tags or [],
                    'fallback': True,
                    'error': str(e)
                },
                confidence=ConfidenceMetrics(
                    overall=0.7,
                    reasoning=0.7,
                    completeness=0.7,
                    consistency=0.7,
                    evidence_strength=0.7,
                ),
                execution_mode=context.execution_mode,
                cost=CostMetrics(
                    tokens=0,
                    latency_ms=execution_time,
                    memory_slots=1,
                    provider_cost_usd=0.0,
                ),
                primitive_name=self.name,
                success=True,
                metadata={'memory_id': memory_id, 'fallback': True}
            )
    
    def estimate_cost(self, **kwargs) -> ResourceEstimate:
        """Estimate execution cost."""
        return ResourceEstimate(
            tokens=0,
            time_ms=2,
            memory_items=1,
            complexity=0.1,
        )
    
    def validate_inputs(self, **kwargs) -> None:
        """Validate inputs."""
        if "content" not in kwargs:
            raise ValueError("'content' parameter required")
    
    def matches_context(self, context: ExecutionContext, **kwargs) -> float:
        """Check context match."""
        return 1.0  # Always available
    
    def rollback(self, context: ExecutionContext) -> None:
        """Rollback memory storage."""
        pass


