"""
Base classes for the primitive system.

Defines the 5-level primitive hierarchy:
- Level 0: Core Cognitive Primitives (perceive, think, remember, action, etc.)
- Level 1: Composite Primitives (analyze, solve, decide, create, explain)
- Level 2: Metacognitive Primitives (introspect, self_assess, select_strategy)
- Level 3: Domain-Specific Primitives (medical.diagnose, legal.analyze_contract)
- Level 4: Execution Control Primitives (sequence, parallel, conditional, loop)
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from brainary.core.context import ExecutionContext, ExecutionMode
    from brainary.memory.working import WorkingMemory
else:
    # Runtime import for ExecutionMode
    from brainary.core.context import ExecutionMode


class PrimitiveLevel(Enum):
    """Primitive hierarchy levels."""
    CORE = 0           # Core cognitive primitives
    COMPOSITE = 1      # Composed from core primitives
    METACOGNITIVE = 2  # Self-awareness and regulation
    DOMAIN = 3         # Domain-specific implementations
    CONTROL = 4        # Execution control flow


@dataclass
class CostMetrics:
    """Resource consumption metrics (matches SPECIFICATION.md)."""
    
    tokens: int = 0                 # Token consumption
    latency_ms: float = 0.0         # Execution latency
    memory_slots: int = 0           # Memory slots used
    provider_cost_usd: float = 0.0  # Provider cost in USD
    
    def __add__(self, other: 'CostMetrics') -> 'CostMetrics':
        """Combine cost metrics."""
        return CostMetrics(
            tokens=self.tokens + other.tokens,
            latency_ms=self.latency_ms + other.latency_ms,
            memory_slots=self.memory_slots + other.memory_slots,
            provider_cost_usd=self.provider_cost_usd + other.provider_cost_usd,
        )


@dataclass
class ResourceEstimate:
    """Estimated resource requirements for primitive execution (pre-execution)."""
    
    tokens: int = 1000              # Estimated token consumption
    time_ms: int = 1000             # Estimated execution time (ms)
    memory_items: int = 1           # Working memory slots needed
    llm_calls: int = 1              # Number of LLM API calls
    complexity: float = 0.5         # Complexity score (0.0-1.0)
    confidence: float = 0.8         # Estimate confidence (0.0-1.0)
    
    def __add__(self, other: 'ResourceEstimate') -> 'ResourceEstimate':
        """Combine resource estimates."""
        return ResourceEstimate(
            tokens=self.tokens + other.tokens,
            time_ms=self.time_ms + other.time_ms,
            memory_items=self.memory_items + other.memory_items,
            llm_calls=self.llm_calls + other.llm_calls,
            complexity=max(self.complexity, other.complexity),
            confidence=min(self.confidence, other.confidence),
        )


@dataclass
class ConfidenceScore:
    """Multi-dimensional confidence assessment (matches SPECIFICATION.md)."""
    
    overall: float = 0.7            # [0-1] Overall confidence
    reasoning: float = 0.7          # [0-1] Quality of reasoning process
    evidence: float = 0.7           # [0-1] Strength of supporting evidence
    
    def __post_init__(self):
        """Validate confidence scores."""
        for field_name, value in [
            ('overall', self.overall),
            ('reasoning', self.reasoning),
            ('evidence', self.evidence),
        ]:
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"Confidence scores must be in [0, 1], got {field_name}={value}")


@dataclass
class ConfidenceMetrics:
    """Extended confidence metrics for primitive results (backward compatibility)."""
    
    overall: float = 0.7            # Overall confidence (0.0-1.0)
    reasoning: float = 0.7          # Reasoning quality
    completeness: float = 0.7       # Result completeness
    consistency: float = 0.7        # Internal consistency
    evidence_strength: float = 0.7  # Supporting evidence
    
    def __post_init__(self):
        """Validate metrics."""
        for field_name, value in [
            ('overall', self.overall),
            ('reasoning', self.reasoning),
            ('completeness', self.completeness),
            ('consistency', self.consistency),
            ('evidence_strength', self.evidence_strength),
        ]:
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{field_name} must be in [0.0, 1.0]")
    
    def to_confidence_score(self) -> 'ConfidenceScore':
        """Convert to ConfidenceScore (SPECIFICATION format)."""
        return ConfidenceScore(
            overall=self.overall,
            reasoning=self.reasoning,
            evidence=self.evidence_strength,
        )


@dataclass
class MemoryWrite:
    """Proposed memory write operation."""
    
    content: Any                    # Content to store
    importance: float = 0.5         # Importance (0.0-1.0)
    tags: List[str] = field(default_factory=list)  # Memory tags
    associations: List[str] = field(default_factory=list)  # Associated item IDs
    memory_type: str = "working"    # Target memory type


@dataclass
class MemoryOperation:
    """Pending memory modification (matches SPECIFICATION.md)."""
    
    operation_type: str             # 'store', 'update', 'delete'
    item: Any                       # Memory item (MemoryItem object)
    transaction_id: str


@dataclass
class PrimitiveResult:
    """
    Standardized result structure for all primitives (matches SPECIFICATION.md).
    
    All primitives return this structure, enabling:
    - Consistent composition and chaining
    - Quality assessment and validation
    - Resource tracking
    - Memory management
    - Learning and adaptation
    """
    
    # Core result
    content: Any                    # Primary output
    confidence: ConfidenceScore     # Quality metrics
    execution_mode: 'ExecutionMode' # How it was executed (imported from context)
    cost: CostMetrics               # Resource usage
    metadata: Dict[str, Any] = field(default_factory=dict)  # Traceability info
    memory_writes: List[MemoryOperation] = field(default_factory=list)  # Pending memory updates
    
    # Additional fields for backward compatibility
    primitive_name: str = "unknown" # Primitive that produced this
    success: bool = True            # Whether execution succeeded
    reads: List[str] = field(default_factory=list)  # Memory items read
    error: Optional[str] = None     # Error message if failed
    
    def meets_threshold(self, threshold: float) -> bool:
        """Check if result meets quality threshold."""
        return self.success and self.confidence.overall >= threshold
    
    @property
    def success_property(self) -> bool:
        """Check if execution was successful (SPECIFICATION property)."""
        return self.confidence.overall >= 0.5


class Primitive(ABC):
    """
    Base class for all primitives (matches SPECIFICATION.md IPrimitive interface).
    
    All cognitive operations in Brainary are primitives that inherit from this class.
    Primitives are executable, composable, and return standardized results.
    """
    
    def __init__(self):
        """Initialize primitive."""
        self._name: str = self.__class__.__name__
        self._version: str = "1.0.0"
        self._capabilities: Dict[str, Any] = {}
        self.description: str = self.__class__.__doc__ or "No description"
        self.level: PrimitiveLevel = PrimitiveLevel.CORE
        self._hint: str = ""  # LLM routing hint
    
    @property
    def name(self) -> str:
        """Unique identifier for this primitive."""
        return self._name
    
    @property
    def version(self) -> str:
        """Semantic version (e.g., '1.0.0')."""
        return self._version
    
    @property
    def capabilities(self) -> Dict[str, Any]:
        """
        Capability declaration for scheduler routing.
        
        Returns:
            Dict with keys:
                - domain: str (e.g., 'general', 'medical', 'finance')
                - depth: int (max reasoning depth supported)
                - modes: List[ExecutionMode] (supported execution modes)
                - quality_range: Tuple[float, float] (min, max quality)
                - resource_profile: Dict (typical resource usage)
        """
        return self._capabilities
    
    @property
    def hint(self) -> str:
        """
        LLM routing hint describing suitable application scenarios.
        
        This hint helps LLM-based routing (Layer 4) make intelligent decisions
        when rule-based routing (Layers 1-3) cannot confidently select an implementation.
        
        Returns:
            Human-readable description of when to use this implementation.
            
        Example:
            "Use for quick, intuitive responses when time pressure is high (>0.7) and "
            "quality requirements are moderate (<0.7). Best for initial brainstorming, "
            "rapid prototyping, or real-time interactions. Not suitable for critical "
            "decisions or deep analysis."
        """
        return self._hint
    
    @abstractmethod
    def validate_inputs(self, **kwargs) -> None:
        """
        Validate input parameters before execution.
        
        Args:
            **kwargs: Input parameters to validate
            
        Raises:
            ValueError: If validation fails with detailed error message
        """
        pass
    
    @abstractmethod
    def estimate_cost(self, **kwargs) -> CostMetrics:
        """
        Estimate resource requirements before execution.
        
        Args:
            **kwargs: Input parameters
            
        Returns:
            CostMetrics: Predicted resource consumption
        """
        pass
    
    @abstractmethod
    def execute(
        self,
        context: 'ExecutionContext',
        memory: 'WorkingMemory',
        **kwargs
    ) -> PrimitiveResult:
        """
        Execute the primitive operation.
        
        Args:
            context: Current execution context
            memory: Memory manager for access/storage
            **kwargs: Primitive-specific parameters
            
        Returns:
            PrimitiveResult: Execution result with metadata
            
        Raises:
            PrimitiveExecutionError: On execution failure
        """
        pass
    
    @abstractmethod
    def rollback(self, context: 'ExecutionContext') -> None:
        """
        Revert side effects for transaction support.
        
        Args:
            context: Execution context to rollback
        """
        pass
    
    def construct_conversation(
        self,
        context: 'ExecutionContext',
        memory: 'WorkingMemory',
        **kwargs
    ) -> List[Dict[str, str]]:
        """
        Construct conversation messages for LLM invocation.
        
        This method builds the conversation history dynamically for each primitive
        execution, allowing primitives to customize how they interact with LLMs.
        
        Default implementation:
        1. Uses existing conversation history from context
        2. Adds a new user message based on primitive parameters
        3. Retrieves relevant context from memory
        
        Override this method in concrete implementations to:
        - Add custom system prompts
        - Include domain-specific context
        - Format parameters in specific ways
        - Inject retrieved knowledge
        - Add few-shot examples
        
        Args:
            context: Execution context with conversation history
            memory: Working memory for retrieving relevant context
            **kwargs: Primitive-specific parameters
        
        Returns:
            List of message dicts in LLM API format:
            [
                {'role': 'system', 'content': '...'},
                {'role': 'user', 'content': '...'},
                {'role': 'assistant', 'content': '...'},
                ...
            ]
        
        Example Override:
            def construct_conversation(self, context, memory, **kwargs):
                # Start with system prompt
                messages = []
                if not context.conversation.system_prompt:
                    context.set_system_prompt("You are an expert analyzer.")
                
                # Get base conversation
                messages = context.get_conversation_history(max_messages=10)
                
                # Add new user message with parameters
                query = kwargs.get('query', '')
                messages.append({
                    'role': 'user',
                    'content': f"Analyze: {query}"
                })
                
                return messages
        """
        messages = []
        
        # Get existing conversation history (if any)
        if context.conversation.messages:
            messages = context.get_conversation_history(max_messages=20)
        else:
            # Set default system prompt if not set
            if not context.conversation.system_prompt:
                context.set_system_prompt(
                    f"You are an intelligent cognitive primitive: {self.name}. "
                    f"{self.description}"
                )
            messages = context.get_conversation_history(include_system=True)
        
        # Retrieve relevant context from memory (if available)
        relevant_items = memory.retrieve(
            tags=[self.name, context.domain] if context.domain else [self.name],
            top_k=3,
            min_importance=0.5
        )
        
        # Build new user message with parameters and context
        user_content_parts = []
        
        # Add memory context if relevant
        if relevant_items:
            user_content_parts.append("Relevant context from memory:")
            for item in relevant_items:
                user_content_parts.append(f"- {str(item.content)[:200]}")
            user_content_parts.append("")
        
        # Add primitive-specific request
        user_content_parts.append(f"Execute {self.name} with parameters:")
        for key, value in kwargs.items():
            user_content_parts.append(f"- {key}: {value}")
        
        messages.append({
            'role': 'user',
            'content': '\n'.join(user_content_parts)
        })
        
        return messages
    
    def matches_context(
        self,
        context: 'ExecutionContext',
        **kwargs
    ) -> float:
        """
        Score how well this primitive matches the execution context.
        
        Used by intelligent routing to select optimal implementations.
        Higher score = better match.
        
        Args:
            context: Execution context
            **kwargs: Primitive-specific parameters
        
        Returns:
            Match score (0.0-1.0), where:
            - 0.0: Cannot handle this context
            - 0.5: Generic/default implementation
            - 1.0: Perfect specialized match
        """
        # Default implementation: basic capability matching
        score = 0.5  # Default score for generic implementation
        
        # Boost score if domain matches
        if context.domain and hasattr(self, 'supported_domains'):
            if context.domain in self.supported_domains:
                score += 0.3
        
        # Boost score if capabilities match
        if context.capabilities and self.capabilities:
            matching = set(context.capabilities) & set(self.capabilities)
            if matching:
                score += 0.2 * (len(matching) / len(context.capabilities))
        
        return min(1.0, score)
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(level={self.level.name})"


class CorePrimitive(Primitive):
    """
    Base class for Level 0 core cognitive primitives.
    
    Core primitives are the foundation operations:
    - perceive: Process and interpret inputs
    - think: Reason about information
    - remember: Store in memory
    - associate: Create concept connections
    - action: Execute actions
    - monitor: Track system state
    - adapt: Modify approaches
    """
    
    def __init__(self):
        super().__init__()
        self.level = PrimitiveLevel.CORE


class CompositePrimitive(Primitive):
    """
    Base class for Level 1 composite primitives.
    
    Composite primitives are domain-general workflows composed from Level 0:
    - analyze: perceive + decompose + think + relate
    - solve: analyze + generate + test + refine
    - decide: evaluate + compare + choose + commit
    - create: imagine + generate + combine + refine
    - explain: understand + structure + communicate + verify
    """
    
    def __init__(self):
        super().__init__()
        self.level = PrimitiveLevel.COMPOSITE
        self.sub_primitives: List[str] = []  # Names of composed primitives


class MetacognitivePrimitive(Primitive):
    """
    Base class for Level 2 metacognitive primitives.
    
    Metacognitive primitives enable self-awareness and self-regulation:
    - introspect: monitor(self) + analyze(internal_state)
    - self_assess: evaluate(own_performance) + calibrate(confidence)
    - select_strategy: assess_situation + match_approach + commit
    - self_correct: detect_error + adjust_strategy + retry
    """
    
    def __init__(self):
        super().__init__()
        self.level = PrimitiveLevel.METACOGNITIVE


class DomainPrimitive(Primitive):
    """
    Base class for Level 3 domain-specific primitives.
    
    Domain primitives are specialized operations for specific domains:
    - medical.diagnose: Medical diagnosis
    - finance.analyze_portfolio: Financial analysis
    - legal.analyze_contract: Contract analysis
    - research.experiment_design: Experimental design
    """
    
    def __init__(self):
        super().__init__()
        self.level = PrimitiveLevel.DOMAIN
        self.supported_domains: List[str] = []  # Domains this primitive handles


class ControlPrimitive(Primitive):
    """
    Base class for Level 4 execution control primitives.
    
    Control primitives manage program flow and resource control:
    - sequence: Sequential execution
    - parallel: Parallel execution
    - conditional: Branching
    - loop: Iteration
    - transaction: Atomic operations
    """
    
    def __init__(self):
        super().__init__()
        self.level = PrimitiveLevel.CONTROL
