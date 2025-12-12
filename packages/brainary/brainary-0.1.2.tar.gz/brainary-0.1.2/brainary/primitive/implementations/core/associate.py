"""
Create connections between concepts in memory using LLM-powered semantic understanding.
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


class AssociateConcepts(CorePrimitive):
    """
    Create connections between concepts in memory.
    
    Uses spreading activation to find and strengthen relationships.
    """
    
    def __init__(self):
        """Initialize primitive."""
        super().__init__()
        self._name = "associate"
        self._hint = (
            "Use to create or strengthen connections between concepts in memory. "
            "Best for relationship discovery, analogical reasoning, and building "
            "semantic networks. Suitable for all domains. Use when you need to "
            "link related information, find patterns, or discover non-obvious "
            "relationships. Strengthens memory through association."
        )
    
    def execute(
        self,
        context: ExecutionContext,
        working_memory: WorkingMemory,
        concept1: str,
        concept2: str = None,
        strength: float = None,
        bidirectional: bool = True,
        discover_mode: bool = False,
        **kwargs
    ) -> PrimitiveResult:
        """
        Create or discover associations between concepts using LLM.
        
        Args:
            context: Execution context
            working_memory: Working memory
            concept1: First concept (or query concept in discover mode)
            concept2: Second concept (optional in discover mode)
            strength: Association strength (0-1), auto-computed if None
            bidirectional: Whether association is bidirectional
            discover_mode: If True, LLM discovers related concepts
            **kwargs: Additional parameters
        
        Returns:
            PrimitiveResult with associations
        """
        start_time = time.time()
        
        try:
            llm_manager = get_llm_manager()
            
            # Retrieve context from memory
            mem_context = working_memory.retrieve(query=concept1, top_k=5)
            context_str = "\n".join([m.content for m in mem_context]) if mem_context else "No prior context."
            
            if discover_mode or concept2 is None:
                # LLM discovers related concepts
                prompt = f"""Find related concepts and associations for: {concept1}

Context from memory:
{context_str}

Identify 5-7 concepts that are meaningfully related to "{concept1}". For each:
1. State the related concept
2. Explain the relationship
3. Rate the association strength (0.0-1.0)

Format each as:
- Concept: <name>
  Relationship: <explanation>
  Strength: <0.0-1.0>"""
                
                response = llm_manager.request(
                    messages=[{"role": "user", "content": prompt}],
                    model="gpt-4o-mini"
                )
                
                # Parse associations
                associations = []
                lines = response.content.strip().split('\n')
                current_assoc = {}
                
                for line in lines:
                    line = line.strip()
                    if line.startswith('- Concept:') or line.startswith('Concept:'):
                        if current_assoc:
                            associations.append(current_assoc)
                        current_assoc = {'concept': line.split(':', 1)[1].strip()}
                    elif 'Relationship:' in line:
                        current_assoc['relationship'] = line.split(':', 1)[1].strip()
                    elif 'Strength:' in line:
                        try:
                            strength_str = line.split(':', 1)[1].strip()
                            current_assoc['strength'] = float(strength_str)
                        except:
                            current_assoc['strength'] = 0.5
                
                if current_assoc:
                    associations.append(current_assoc)
                
                # Create associative memory manager
                associative_memory = AssociativeMemory(working_memory)
                
                # Store concept1 in memory if not already there
                concept1_items = working_memory.retrieve(query=concept1, top_k=1)
                if concept1_items and concept1 in concept1_items[0].content:
                    concept1_id = concept1_items[0].id
                else:
                    concept1_id = working_memory.store(
                        content=concept1,
                        importance=0.7,
                        tags=["concept", "source"],
                    )
                
                # Store discovered associations in both memory and associative graph
                graph_associations_created = 0
                for assoc in associations:
                    concept2_name = assoc.get('concept', 'unknown')
                    relationship = assoc.get('relationship', 'related')
                    assoc_strength = assoc.get('strength', 0.5)
                    
                    # Store association description in memory
                    assoc_content = f"{concept1} <-> {concept2_name}: {relationship}"
                    concept2_id = working_memory.store(
                        content=assoc_content,
                        importance=assoc_strength,
                        tags=["association", concept1, concept2_name],
                    )
                    
                    # Create graph association
                    if associative_memory.associate(
                        source_id=concept1_id,
                        target_id=concept2_id,
                        association_type="conceptual",
                        strength=assoc_strength,
                        bidirectional=bidirectional,
                        relationship=relationship,
                        discovered_by="associate_primitive",
                    ):
                        graph_associations_created += 1
                
                result = {
                    'source_concept': concept1,
                    'associations': associations,
                    'count': len(associations),
                    'graph_associations_created': graph_associations_created,
                    'mode': 'discover',
                    'model': 'gpt-4o-mini',
                }
                
                execution_time = int((time.time() - start_time) * 1000)
                
                return PrimitiveResult(
                    content=result,
                    confidence=ConfidenceMetrics(
                        overall=0.85,
                        reasoning=0.85,
                        completeness=0.8,
                        consistency=0.85,
                        evidence_strength=0.8,
                    ),
                    execution_mode=context.execution_mode,
                    cost=CostMetrics(
                        tokens=response.usage.total_tokens,
                        latency_ms=execution_time,
                        memory_slots=len(associations),
                        provider_cost_usd=response.cost,
                    ),
                    primitive_name=self.name,
                    success=True,
                    metadata={
                        'associations_found': len(associations),
                        'mode': 'discover',
                    }
                )
            
            else:
                # Explicit association with LLM-computed strength
                if strength is None:
                    prompt = f"""Analyze the relationship between these two concepts:

Concept 1: {concept1}
Concept 2: {concept2}

Context from memory:
{context_str}

Provide:
1. Relationship explanation (1-2 sentences)
2. Association strength rating (0.0-1.0):
   - 0.0-0.3: Weak or distant relationship
   - 0.4-0.6: Moderate relationship
   - 0.7-0.9: Strong relationship
   - 0.9-1.0: Very strong or essential relationship

Format:
Relationship: <explanation>
Strength: <0.0-1.0>"""
                    
                    response = llm_manager.request(
                        messages=[{"role": "user", "content": prompt}],
                        model="gpt-4o-mini"
                    )
                    
                    content = response.content.strip()
                    
                    # Extract strength and relationship
                    relationship = "related"
                    computed_strength = 0.5
                    
                    for line in content.split('\n'):
                        if 'Relationship:' in line:
                            relationship = line.split(':', 1)[1].strip()
                        elif 'Strength:' in line:
                            try:
                                strength_str = line.split(':', 1)[1].strip()
                                computed_strength = float(strength_str)
                            except:
                                pass
                    
                    strength = computed_strength
                    tokens = response.usage.total_tokens
                    cost = response.cost
                else:
                    relationship = "explicitly associated"
                    tokens = 0
                    cost = 0.0
                
                # Store concepts in memory if not already there
                concept1_items = working_memory.retrieve(query=concept1, top_k=1)
                if concept1_items and concept1 in concept1_items[0].content:
                    concept1_id = concept1_items[0].id
                else:
                    concept1_id = working_memory.store(
                        content=concept1,
                        importance=0.7,
                        tags=["concept"],
                    )
                
                concept2_items = working_memory.retrieve(query=concept2, top_k=1)
                if concept2_items and concept2 in concept2_items[0].content:
                    concept2_id = concept2_items[0].id
                else:
                    concept2_id = working_memory.store(
                        content=concept2,
                        importance=0.7,
                        tags=["concept"],
                    )
                
                # Store association description
                assoc_content = f"{concept1} <-> {concept2}: {relationship} (strength: {strength:.2f})"
                item_id = working_memory.store(
                    content=assoc_content,
                    importance=strength,
                    tags=["association", concept1, concept2],
                )
                
                # Create graph association using AssociativeMemory
                associative_memory = AssociativeMemory(working_memory)
                graph_created = associative_memory.associate(
                    source_id=concept1_id,
                    target_id=concept2_id,
                    association_type="explicit",
                    strength=strength,
                    bidirectional=bidirectional,
                    relationship=relationship,
                    discovered_by="associate_primitive",
                )
                
                result = {
                    'concept1': concept1,
                    'concept2': concept2,
                    'relationship': relationship,
                    'strength': strength,
                    'bidirectional': bidirectional,
                    'graph_created': graph_created,
                    'mode': 'explicit',
                }
                
                execution_time = int((time.time() - start_time) * 1000)
                
                return PrimitiveResult(
                    content=result,
                    confidence=ConfidenceMetrics(
                        overall=0.9,
                        reasoning=0.9,
                        completeness=1.0,
                        consistency=0.9,
                        evidence_strength=0.85,
                    ),
                    execution_mode=context.execution_mode,
                    cost=CostMetrics(
                        tokens=tokens,
                        latency_ms=execution_time,
                        memory_slots=1 if not bidirectional else 2,
                        provider_cost_usd=cost,
                    ),
                    primitive_name=self.name,
                    success=True,
                    metadata={
                        'association_id': item_id,
                        'strength': strength,
                        'bidirectional': bidirectional,
                        'mode': 'explicit',
                    }
                )
        
        except Exception as e:
            logger.error(f"AssociateConcepts execution failed: {e}")
            execution_time = int((time.time() - start_time) * 1000)
            
            return PrimitiveResult(
                content=None,
                confidence=ConfidenceMetrics(overall=0.0),
                execution_mode=context.execution_mode,
                cost=CostMetrics(
                    tokens=0,
                    latency_ms=execution_time,
                    memory_slots=0,
                    provider_cost_usd=0.0,
                ),
                primitive_name=self.name,
                success=False,
                error=str(e),
            )
    
    def estimate_cost(self, **kwargs) -> ResourceEstimate:
        """Estimate execution cost."""
        bidirectional = kwargs.get('bidirectional', True)
        return ResourceEstimate(
            tokens=0,
            time_ms=2,
            memory_items=1 if not bidirectional else 2,
            complexity=0.2,
        )
    
    def validate_inputs(self, **kwargs) -> None:
        """Validate inputs for execution."""
        if "concept1" not in kwargs or "concept2" not in kwargs:
            raise ValueError("'concept1' and 'concept2' parameters required")
        
        strength = kwargs.get('strength', 0.5)
        if not 0.0 <= strength <= 1.0:
            raise ValueError(f"'strength' must be in [0, 1], got {strength}")
    
    def matches_context(self, context: ExecutionContext, **kwargs) -> float:
        """Check context match."""
        return 1.0  # Always available
    
    def rollback(self, context: ExecutionContext) -> None:
        """Rollback - would need to remove association from memory."""
        pass


