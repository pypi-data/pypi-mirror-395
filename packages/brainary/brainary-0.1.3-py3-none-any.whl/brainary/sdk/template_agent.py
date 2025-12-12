"""
Template Agent - Base template for creating intelligent agents with Brainary

Provides a flexible template that includes:
- Working Memory (L2): Cross-execution continuity and short-term context
- Semantic Memory (L3): Long-term knowledge base
- Metacognition: Self-monitoring and adaptation
- Kernel: Intelligent execution orchestration
- Hook Interface: Customizable logic with primitives and control flow
"""

from typing import Any, Dict, List, Optional, Callable, Union
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import logging

from brainary.core import CognitiveKernel, create_execution_context, ExecutionContext
from brainary.memory import WorkingMemory, SemanticMemory, KnowledgeType, ConceptualKnowledge, FactualKnowledge, ProceduralKnowledge, MetacognitiveKnowledge, create_entry_id, MemoryItem
from brainary.core.metacognitive_monitor import MetacognitiveMonitor, MonitoringLevel
from brainary.primitive.base import PrimitiveResult

logger = logging.getLogger(__name__)


@dataclass
class AgentConfig:
    """Configuration for template agent."""
    
    # Identity
    name: str
    description: str = ""
    domain: str = "general"
    
    # Memory configuration
    working_memory_capacity: int = 10
    enable_semantic_memory: bool = True
    
    # Metacognition configuration
    enable_metacognition: bool = True
    monitoring_level: MonitoringLevel = MonitoringLevel.STANDARD
    
    # Kernel configuration
    enable_learning: bool = True
    quality_threshold: float = 0.8
    
    # Execution preferences
    default_execution_mode: str = "adaptive"
    max_token_budget: int = 10000
    
    # Custom metadata
    metadata: Dict[str, Any] = field(default_factory=dict)


class TemplateAgent(ABC):
    """
    Template Agent with kernel-scoped memories and abstract process method.
    
    This template provides:
    1. Working Memory: Cross-execution continuity and short-term context
    2. Semantic Memory: Long-term knowledge base for domain expertise
    3. Metacognition: Self-monitoring and adaptive behavior
    4. Kernel: Intelligent orchestration of primitive execution
    5. Abstract process(): Customizable logic with primitives and control flow
    
    Subclass this and implement the process() method to define your agent's behavior.
    
    Examples:
        Custom agent implementation:
        >>> class MyAgent(TemplateAgent):
        ...     def process(self, input_data, context, **kwargs):
        ...         # Your custom logic with primitives
        ...         result = self.kernel.execute("think", context=context, question=input_data)
        ...         return result
        ...
        >>> agent = MyAgent(name="my_agent")
        >>> result = agent.run("Hello, help me analyze this data")
        
        With pre-populated knowledge:
        >>> class ExpertAgent(TemplateAgent):
        ...     def process(self, input_data, context, **kwargs):
        ...         # Search knowledge first
        ...         knowledge = self.search_knowledge(input_data, top_k=3)
        ...         # Then think with context
        ...         return self.kernel.execute("think", context=context, question=input_data)
        ...
        >>> agent = ExpertAgent(name="expert")
        >>> agent.add_knowledge(ConceptualKnowledge(...))
        >>> result = agent.run(task)
    """
    
    def __init__(
        self,
        name: str,
        description: str = "",
        config: Optional[AgentConfig] = None,
        working_memory: Optional[WorkingMemory] = None,
        semantic_memory: Optional[SemanticMemory] = None,
        metacognitive_monitor: Optional[MetacognitiveMonitor] = None,
        **config_overrides
    ):
        """
        Initialize template agent.
        
        Args:
            name: Agent name
            description: Agent description
            config: Agent configuration (or use config_overrides)
            working_memory: Custom working memory instance
            semantic_memory: Custom semantic memory instance
            metacognitive_monitor: Custom metacognitive monitor
            **config_overrides: Override config parameters
        """
        # Build configuration
        if config is None:
            config = AgentConfig(
                name=name,
                description=description,
                **config_overrides
            )
        
        self.config = config
        self.name = config.name
        self.description = config.description
        
        # Initialize memories (kernel-scoped for cross-execution learning)
        self.working_memory = working_memory or WorkingMemory(
            capacity=config.working_memory_capacity
        )
        
        self.semantic_memory = semantic_memory or (
            SemanticMemory() if config.enable_semantic_memory else None
        )
        
        # Initialize kernel with kernel-scoped memories
        self.kernel = CognitiveKernel(
            working_memory=self.working_memory,
            semantic_memory=self.semantic_memory,
            metacognitive_monitor=metacognitive_monitor,
            enable_metacognition=config.enable_metacognition,
            monitoring_level=config.monitoring_level,
            enable_learning=config.enable_learning
        )
        
        # Statistics
        self._run_count = 0
        self._success_count = 0
        
        logger.info(f"TemplateAgent '{self.name}' initialized")
        logger.info(f"  - Working Memory: {self.working_memory.capacity} capacity")
        if self.semantic_memory:
            logger.info(f"  - Semantic Memory: {self.semantic_memory.get_stats()['total_entries']} entries")
        logger.info(f"  - Metacognition: {config.enable_metacognition}")
        logger.info(f"  - Learning: {config.enable_learning}")
    
    @abstractmethod
    def process(
        self,
        input_data: Any,
        context: ExecutionContext,
        **kwargs
    ) -> PrimitiveResult:
        """
        Process input using agent's kernel and primitives.
        
        Implement this method to define your agent's behavior using
        primitives (think, perceive, decide, etc.) and control flow.
        
        Args:
            input_data: Input data to process
            context: Execution context
            **kwargs: Additional parameters
            
        Returns:
            PrimitiveResult from final primitive execution
            
        Example:
            >>> def process(self, input_data, context, **kwargs):
            ...     # Step 1: Think about the input
            ...     result = self.kernel.execute("think", context=context, question=input_data)
            ...     return result
        """
        pass
    
    def run(
        self,
        input_data: Any,
        context: Optional[ExecutionContext] = None,
        **kwargs
    ) -> PrimitiveResult:
        """
        Run agent on input data using the process method.
        
        Args:
            input_data: Input data to process
            context: Optional execution context (creates default if None)
            **kwargs: Additional parameters passed to process
            
        Returns:
            PrimitiveResult from processing
            
        Examples:
            >>> class MyAgent(TemplateAgent):
            ...     def process(self, input_data, context, **kwargs):
            ...         return self.kernel.execute("think", context=context, question=input_data)
            ...
            >>> agent = MyAgent(name="assistant")
            >>> result = agent.run("What is machine learning?")
            >>> print(result.content)
        """
        self._run_count += 1
        
        # Create context if not provided
        if context is None:
            context = create_execution_context(
                program_name=f"agent_{self.name}",
                domain=self.config.domain
            )
        
        try:
            # Main processing via abstract process method
            result = self.process(input_data, context, **kwargs)
            
            # Update statistics
            if result.success:
                self._success_count += 1
            
            return result
            
        except Exception as e:
            logger.error(f"Agent '{self.name}' error: {e}")
            
            # Create error result
            from brainary.primitive.base import ConfidenceScore, CostMetrics
            return PrimitiveResult(
                content=None,
                primitive_name="agent_run",
                success=False,
                error=str(e),
                confidence=ConfidenceScore(overall=0.0, reasoning=0.0),
                execution_mode=context.execution_mode,
                cost=CostMetrics(tokens=0, latency_ms=0, memory_slots=0, provider_cost_usd=0.0)
            )
    
    def add_knowledge(
        self,
        knowledge: Union[ConceptualKnowledge, FactualKnowledge, ProceduralKnowledge, MetacognitiveKnowledge]
    ) -> str:
        """
        Add knowledge to agent's semantic memory.
        
        Args:
            knowledge: Knowledge entry to add
            
        Returns:
            Entry ID
            
        Examples:
            >>> agent = TemplateAgent(name="expert")
            >>> agent.add_knowledge(ConceptualKnowledge(
            ...     entry_id=create_entry_id(KnowledgeType.CONCEPTUAL, "ml"),
            ...     key_concepts=["machine learning", "AI"],
            ...     description="Machine learning is a subset of AI"
            ... ))
        """
        if not self.semantic_memory:
            raise ValueError("Semantic memory not enabled for this agent")
        
        return self.semantic_memory.add_knowledge(knowledge)
    
    def search_knowledge(
        self,
        query: str,
        knowledge_types: Optional[List[KnowledgeType]] = None,
        top_k: int = 5
    ) -> List:
        """
        Search agent's knowledge base.
        
        Args:
            query: Search query
            knowledge_types: Optional filter by knowledge types
            top_k: Maximum results to return
            
        Returns:
            List of matching knowledge entries
        """
        if not self.semantic_memory:
            return []
        
        return self.semantic_memory.search(
            query=query,
            knowledge_types=knowledge_types,
            top_k=top_k
        )
    
    def remember(self, content: Any, importance: float = 0.7, tags: Optional[List[str]] = None) -> None:
        """
        Store information in working memory.
        
        Args:
            content: Content to remember
            importance: Importance score (0-1)
            tags: Optional tags for categorization
        """
        self.working_memory.store(
            content=content,
            importance=importance,
            tags=tags or []
        )
    
    def recall(self, query: Optional[str] = None, top_k: int = 5) -> List[MemoryItem]:
        """
        Recall information from working memory.
        
        Args:
            query: Optional query for semantic search
            top_k: Maximum results
            
        Returns:
            List of recalled items
        """
        # Retrieve items from working memory (retrieve all by using large top_k and no filters)
        items = self.working_memory.retrieve(
            query=query,
            top_k=top_k if query else 100,  # Get all items if no query
            tier=None  # Search all tiers
        )
        
        return items[:top_k]
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get comprehensive agent statistics.
        
        Returns:
            Dictionary with agent, memory, and kernel stats
        """
        stats = {
            'agent': {
                'name': self.name,
                'description': self.description,
                'domain': self.config.domain,
                'runs': self._run_count,
                'success_rate': self._success_count / max(1, self._run_count),
            },
            'working_memory': self.working_memory.get_stats(),
            'kernel': self.kernel.get_stats()
        }
        
        if self.semantic_memory:
            stats['semantic_memory'] = self.semantic_memory.get_stats()
        
        return stats
    
    def reset_working_memory(self) -> None:
        """Clear working memory (keeps semantic memory intact)."""
        self.working_memory = WorkingMemory(capacity=self.config.working_memory_capacity)
        self.kernel.working_memory = self.working_memory
    
    def __repr__(self) -> str:
        return f"TemplateAgent(name='{self.name}', domain='{self.config.domain}')"


class SimpleAgent(TemplateAgent):
    """
    Simple concrete implementation of TemplateAgent.
    
    Uses the "think" primitive for processing. Good for quick prototyping
    or as a starting point for custom agents.
    
    Examples:
        >>> agent = SimpleAgent(name="assistant")
        >>> result = agent.run("What is machine learning?")
    """
    
    def process(
        self,
        input_data: Any,
        context: ExecutionContext,
        **kwargs
    ) -> PrimitiveResult:
        """Use think primitive for processing."""
        return self.kernel.execute(
            "think",
            context=context,
            question=str(input_data),
            **kwargs
        )
