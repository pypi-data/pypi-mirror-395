"""
Brainary Client - Main SDK Interface

Provides a high-level, user-friendly interface to the Brainary system.
"""

from typing import Any, Dict, Optional, List
import logging

from brainary.core.kernel import CognitiveKernel
from brainary.core.context import create_execution_context, ExecutionContext, ExecutionMode
from brainary.memory.working import WorkingMemory
from brainary.primitive.base import PrimitiveResult
from brainary.primitive import register_core_primitives

logger = logging.getLogger(__name__)

# Register primitives on module import
_primitives_registered = False
def _ensure_primitives_registered():
    global _primitives_registered
    if not _primitives_registered:
        register_core_primitives()
        _primitives_registered = True


class Brainary:
    """
    Main Brainary SDK client.
    
    This class provides a simple, high-level interface to the Brainary
    cognitive computing platform. It manages the kernel, memory, and
    execution context automatically.
    
    Examples:
        Basic usage:
        >>> brain = Brainary()
        >>> result = brain.think("Analyze this code for bugs")
        >>> print(result.content)
        
        With custom configuration:
        >>> brain = Brainary(
        ...     enable_learning=True,
        ...     memory_capacity=10,
        ...     quality_threshold=0.9
        ... )
        >>> result = brain.think("Complex reasoning task")
        
        With explicit context:
        >>> brain = Brainary()
        >>> with brain.context(domain="medical", quality=0.95):
        ...     result = brain.think("Diagnose symptoms")
    """
    
    def __init__(
        self,
        enable_learning: bool = True,
        memory_capacity: int = 7,
        quality_threshold: float = 0.8,
        token_budget: int = 10000,
        program_name: str = "brainary_app",
        **kwargs
    ):
        """
        Initialize Brainary client.
        
        Args:
            enable_learning: Enable learning and adaptation
            memory_capacity: Working memory capacity (default: 7)
            quality_threshold: Minimum acceptable quality (default: 0.8)
            token_budget: Maximum tokens per operation (default: 10000)
            program_name: Name for this program instance
            **kwargs: Additional configuration options
        """
        # Ensure primitives are registered
        _ensure_primitives_registered()
        
        # Initialize kernel
        self.kernel = CognitiveKernel(enable_learning=enable_learning)
        
        # Create default memory
        self.memory = WorkingMemory(capacity=memory_capacity)
        
        # Store default configuration
        self._default_config = {
            'program_name': program_name,
            'quality_threshold': quality_threshold,
            'token_budget': token_budget,
            **kwargs
        }
        
        # Track statistics
        self._execution_count = 0
        
        logger.info(f"Brainary client initialized: {program_name}")
    
    def think(
        self,
        query: str,
        context: Optional[ExecutionContext] = None,
        reasoning_mode: str = "adaptive",
        **kwargs
    ) -> PrimitiveResult:
        """
        Execute deep reasoning about a query.
        
        Args:
            query: The question or problem to reason about
            context: Optional execution context
            reasoning_mode: "fast", "deep", or "adaptive" (default)
            **kwargs: Additional parameters
        
        Returns:
            PrimitiveResult with reasoning output
        
        Examples:
            >>> brain = Brainary()
            >>> result = brain.think("What causes inflation?")
            >>> print(result.content)
        """
        ctx = context or self._create_context(
            execution_mode=self._mode_from_string(reasoning_mode)
        )
        
        result = self.kernel.execute(
            "think",
            context=ctx,
            working_memory=self.memory,
            query=query,
            **kwargs
        )
        
        self._execution_count += 1
        return result
    
    def perceive(
        self,
        input_data: Any,
        context: Optional[ExecutionContext] = None,
        attention_focus: Optional[List[str]] = None,
        **kwargs
    ) -> PrimitiveResult:
        """
        Process and interpret input data.
        
        Args:
            input_data: Data to perceive (text, image, structured data)
            context: Optional execution context
            attention_focus: Keywords to focus attention on
            **kwargs: Additional parameters
        
        Returns:
            PrimitiveResult with interpreted data
        
        Examples:
            >>> brain = Brainary()
            >>> result = brain.perceive(
            ...     "Large code file with multiple functions",
            ...     attention_focus=["bugs", "security"]
            ... )
        """
        ctx = context or self._create_context()
        
        result = self.kernel.execute(
            "perceive",
            context=ctx,
            working_memory=self.memory,
            input=input_data,
            attention_focus=attention_focus or [],
            **kwargs
        )
        
        self._execution_count += 1
        return result
    
    def remember(
        self,
        content: Any,
        context: Optional[ExecutionContext] = None,
        importance: float = 0.5,
        tags: Optional[List[str]] = None,
        **kwargs
    ) -> PrimitiveResult:
        """
        Store information in memory with intelligent association building.
        
        Uses LLM to identify and create associations with existing memories.
        
        Args:
            content: Information to remember
            context: Optional execution context
            importance: Importance score (0-1, default: 0.5)
            tags: Tags for retrieval
            **kwargs: Additional parameters
        
        Returns:
            PrimitiveResult with memory confirmation and associations created
        
        Examples:
            >>> brain = Brainary()
            >>> result = brain.remember(
            ...     "Python 3.11 improved performance significantly",
            ...     importance=0.8,
            ...     tags=["python", "performance"]
            ... )
            >>> print(f"Created {result.metadata.get('associations_created', 0)} associations")
        """
        ctx = context or self._create_context()
        
        result = self.kernel.execute(
            "remember",
            context=ctx,
            working_memory=self.memory,
            content=content,
            importance=importance,
            tags=tags or [],
            **kwargs
        )
        
        self._execution_count += 1
        return result
    
    def recall(
        self,
        query: Optional[str] = None,
        context: Optional[ExecutionContext] = None,
        tags: Optional[List[str]] = None,
        limit: int = 5,
        **kwargs
    ) -> PrimitiveResult:
        """
        Retrieve information from memory with attention and spreading activation.
        
        Uses attention mechanisms to focus on relevant memories and spreads
        activation through the associative network.
        
        Args:
            query: Search query for memory retrieval
            context: Optional execution context
            tags: Optional tag filters
            limit: Maximum number of items to retrieve
            **kwargs: Additional parameters
        
        Returns:
            PrimitiveResult with retrieved memories and associations
        
        Examples:
            >>> brain = Brainary()
            >>> result = brain.recall("Python performance improvements", limit=10)
            >>> print(f"Retrieved {len(result.content)} items")
            >>> print(f"Associated items: {result.metadata.get('associated_count', 0)}")
        """
        ctx = context or self._create_context()
        
        result = self.kernel.execute(
            "recall",
            context=ctx,
            working_memory=self.memory,
            query=query,
            tags=tags,
            limit=limit,
            **kwargs
        )
        
        self._execution_count += 1
        return result
    
    def associate(
        self,
        concept1: str,
        concept2: Optional[str] = None,
        context: Optional[ExecutionContext] = None,
        strength: Optional[float] = None,
        discover_mode: bool = False,
        **kwargs
    ) -> PrimitiveResult:
        """
        Create associations between concepts in memory.
        
        Args:
            concept1: First concept or query for discovery
            concept2: Second concept (for explicit linking)
            context: Optional execution context
            strength: Association strength (0-1), auto-determined if None
            discover_mode: If True, discovers related concepts automatically
            **kwargs: Additional parameters
        
        Returns:
            PrimitiveResult with created associations
        
        Examples:
            >>> brain = Brainary()
            >>> # Explicit mode
            >>> result = brain.associate("Python", "performance", strength=0.8)
            >>> 
            >>> # Discover mode
            >>> result = brain.associate("machine learning", discover_mode=True)
            >>> print(f"Found {len(result.content)} related concepts")
        """
        ctx = context or self._create_context()
        
        result = self.kernel.execute(
            "associate",
            context=ctx,
            working_memory=self.memory,
            concept1=concept1,
            concept2=concept2,
            strength=strength,
            discover_mode=discover_mode,
            **kwargs
        )
        
        self._execution_count += 1
        return result
    
    def analyze(
        self,
        data: Any,
        context: Optional[ExecutionContext] = None,
        analysis_type: str = "general",
        **kwargs
    ) -> PrimitiveResult:
        """
        Perform comprehensive analysis of data.
        
        Args:
            data: Data to analyze
            context: Optional execution context
            analysis_type: Type of analysis ("general", "security", "performance")
            **kwargs: Additional parameters
        
        Returns:
            PrimitiveResult with analysis results
        
        Examples:
            >>> brain = Brainary()
            >>> result = brain.analyze(
            ...     source_code,
            ...     analysis_type="security"
            ... )
        """
        ctx = context or self._create_context()
        
        result = self.kernel.execute(
            "analyze",
            context=ctx,
            working_memory=self.memory,
            data=data,
            analysis_type=analysis_type,
            **kwargs
        )
        
        self._execution_count += 1
        return result
    
    def solve(
        self,
        problem: str,
        context: Optional[ExecutionContext] = None,
        constraints: Optional[List[str]] = None,
        **kwargs
    ) -> PrimitiveResult:
        """
        Solve a problem with given constraints.
        
        Args:
            problem: Problem description
            context: Optional execution context
            constraints: List of constraints
            **kwargs: Additional parameters
        
        Returns:
            PrimitiveResult with solution
        
        Examples:
            >>> brain = Brainary()
            >>> result = brain.solve(
            ...     "Optimize database query performance",
            ...     constraints=["< 100ms", "read-heavy workload"]
            ... )
        """
        ctx = context or self._create_context()
        
        result = self.kernel.execute(
            "solve",
            context=ctx,
            working_memory=self.memory,
            problem=problem,
            constraints=constraints or [],
            **kwargs
        )
        
        self._execution_count += 1
        return result
    
    def decide(
        self,
        options: List[Any],
        context: Optional[ExecutionContext] = None,
        criteria: Optional[List[str]] = None,
        **kwargs
    ) -> PrimitiveResult:
        """
        Make a decision between multiple options.
        
        Args:
            options: List of options to choose from
            context: Optional execution context
            criteria: Decision criteria
            **kwargs: Additional parameters
        
        Returns:
            PrimitiveResult with decision and justification
        
        Examples:
            >>> brain = Brainary()
            >>> result = brain.decide(
            ...     options=["MySQL", "PostgreSQL", "MongoDB"],
            ...     criteria=["performance", "reliability", "ecosystem"]
            ... )
        """
        ctx = context or self._create_context()
        
        result = self.kernel.execute(
            "decide",
            context=ctx,
            working_memory=self.memory,
            options=options,
            criteria=criteria or [],
            **kwargs
        )
        
        self._execution_count += 1
        return result
    
    def execute(
        self,
        primitive_name: str,
        context: Optional[ExecutionContext] = None,
        **kwargs
    ) -> PrimitiveResult:
        """
        Execute any primitive by name.
        
        This is a low-level method that gives direct access to the kernel.
        Use specific methods (think, perceive, etc.) when available.
        
        Args:
            primitive_name: Name of primitive to execute
            context: Optional execution context
            **kwargs: Primitive-specific parameters
        
        Returns:
            PrimitiveResult from execution
        
        Examples:
            >>> brain = Brainary()
            >>> result = brain.execute(
            ...     "custom_primitive",
            ...     param1="value1"
            ... )
        """
        ctx = context or self._create_context()
        
        result = self.kernel.execute(
            primitive_name,
            context=ctx,
            working_memory=self.memory,
            **kwargs
        )
        
        self._execution_count += 1
        return result
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get comprehensive statistics.
        
        Returns:
            Dictionary with kernel and client statistics
        
        Examples:
            >>> brain = Brainary()
            >>> # ... perform operations ...
            >>> stats = brain.get_stats()
            >>> print(f"Success rate: {stats['kernel']['success_rate']:.2%}")
        """
        kernel_stats = self.kernel.get_stats()
        
        return {
            'client': {
                'executions': self._execution_count,
            },
            **kernel_stats
        }
    
    def get_learning_insights(self) -> Dict[str, Any]:
        """
        Get insights from the learning system.
        
        Returns:
            Dictionary of learning insights and recommendations
        
        Examples:
            >>> brain = Brainary()
            >>> insights = brain.get_learning_insights()
            >>> for suggestion in insights.get('suggestions', []):
            ...     print(suggestion)
        """
        return self.kernel.get_learning_insights()
    
    def clear_memory(self) -> None:
        """
        Clear working memory.
        
        Examples:
            >>> brain = Brainary()
            >>> brain.clear_memory()
        """
        self.memory = WorkingMemory(capacity=self.memory.capacity)
        logger.info("Working memory cleared")
    
    def context(
        self,
        domain: Optional[str] = None,
        quality: Optional[float] = None,
        mode: Optional[str] = None,
        **kwargs
    ) -> 'ContextManager':
        """
        Create a context manager for scoped execution.
        
        Args:
            domain: Domain for this context
            quality: Quality threshold
            mode: Execution mode ("fast", "deep", "adaptive")
            **kwargs: Additional context parameters
        
        Returns:
            ContextManager for use with 'with' statement
        
        Examples:
            >>> brain = Brainary()
            >>> with brain.context(domain="medical", quality=0.95):
            ...     result = brain.think("Diagnose patient")
        """
        from brainary.sdk.context import ContextManager
        
        config = {}
        if domain:
            config['domain'] = domain
        if quality:
            config['quality_threshold'] = quality
        if mode:
            config['execution_mode'] = self._mode_from_string(mode)
        config.update(kwargs)
        
        return ContextManager(self, config)
    
    def _create_context(
        self,
        execution_mode: Optional[ExecutionMode] = None,
        **overrides
    ) -> ExecutionContext:
        """Create execution context with defaults."""
        config = {**self._default_config, **overrides}
        if execution_mode:
            config['execution_mode'] = execution_mode
        
        return create_execution_context(**config)
    
    def _mode_from_string(self, mode: str) -> ExecutionMode:
        """Convert string mode to ExecutionMode."""
        mode_map = {
            'fast': ExecutionMode.SYSTEM1,
            'system1': ExecutionMode.SYSTEM1,
            'deep': ExecutionMode.SYSTEM2,
            'system2': ExecutionMode.SYSTEM2,
            'cached': ExecutionMode.CACHED,
            'adaptive': ExecutionMode.ADAPTIVE,
        }
        return mode_map.get(mode.lower(), ExecutionMode.ADAPTIVE)
    
    def __repr__(self) -> str:
        return f"Brainary(executions={self._execution_count}, learning={self.kernel._enable_learning})"
