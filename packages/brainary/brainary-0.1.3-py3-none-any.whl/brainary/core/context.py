"""
Execution context management for cognitive operations.

Provides ExecutionContext that flows through all layers of the system,
carrying quality thresholds, resource budgets, execution mode, and other
configuration that guides intelligent decision-making.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid


class ExecutionMode(Enum):
    """Cognitive execution modes based on dual-process theory."""
    SYSTEM1 = "system1"      # Fast, intuitive, low resource
    SYSTEM2 = "system2"      # Slow, analytical, high resource
    CACHED = "cached"        # From experience cache (fastest)
    ADAPTIVE = "adaptive"    # Dynamic selection based on context


@dataclass
class ConversationMessage:
    """
    Single message in LLM conversation.
    
    Represents a message exchanged with the LLM, following standard chat format.
    """
    role: str  # 'system', 'user', 'assistant'
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=lambda: __import__('time').time())


@dataclass
class ConversationState:
    """
    Conversation state for LLM interactions per program execution.
    
    Maintains the conversation history and context for LLM calls within
    a single program execution. This is lightweight and request-scoped.
    
    The actual message content is stored in working memory for persistence,
    while this structure maintains references and conversation flow.
    """
    conversation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    messages: List[ConversationMessage] = field(default_factory=list)
    system_prompt: Optional[str] = None
    total_tokens: int = 0
    total_cost_usd: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Memory references (item IDs in working memory)
    memory_refs: List[str] = field(default_factory=list)
    
    def add_message(
        self,
        role: str,
        content: str,
        memory_ref: Optional[str] = None,
        **metadata
    ) -> ConversationMessage:
        """
        Add message to conversation.
        
        Args:
            role: Message role ('system', 'user', 'assistant')
            content: Message content
            memory_ref: Optional reference to memory item storing full content
            **metadata: Additional message metadata
        
        Returns:
            Created ConversationMessage
        """
        msg = ConversationMessage(
            role=role,
            content=content,
            metadata=metadata
        )
        self.messages.append(msg)
        
        if memory_ref:
            self.memory_refs.append(memory_ref)
        
        return msg
    
    def get_messages_for_llm(
        self,
        include_system: bool = True,
        max_messages: Optional[int] = None
    ) -> List[Dict[str, str]]:
        """
        Get messages in LLM API format.
        
        Args:
            include_system: Include system prompt
            max_messages: Maximum number of recent messages to include
        
        Returns:
            List of message dicts for LLM API
        """
        messages = []
        
        # Add system prompt if available
        if include_system and self.system_prompt:
            messages.append({
                'role': 'system',
                'content': self.system_prompt
            })
        
        # Add conversation messages
        conv_messages = self.messages
        if max_messages:
            conv_messages = conv_messages[-max_messages:]
        
        for msg in conv_messages:
            messages.append({
                'role': msg.role,
                'content': msg.content
            })
        
        return messages
    
    def summarize(self) -> Dict[str, Any]:
        """
        Get conversation summary for logging.
        
        Returns:
            Summary dictionary
        """
        return {
            'conversation_id': self.conversation_id,
            'message_count': len(self.messages),
            'total_tokens': self.total_tokens,
            'total_cost_usd': self.total_cost_usd,
            'has_system_prompt': self.system_prompt is not None,
            'memory_refs_count': len(self.memory_refs),
        }


@dataclass
class ExecutionContext:
    """
    Execution context that flows through all cognitive operations.
    
    This context carries configuration that guides intelligent routing,
    augmentation, resource allocation, and execution strategies.
    
    Attributes:
        context_id: Unique identifier for this execution context
        program_name: Name of the program being executed
        execution_mode: System 1 (fast) vs System 2 (analytical) vs Adaptive
        quality_threshold: Minimum acceptable confidence (0.0-1.0)
        criticality: How critical this operation is (0.0-1.0)
        time_pressure: Time sensitivity (0.0=none, 1.0=urgent)
        token_budget: Maximum tokens allowed for this execution
        token_usage: Current token consumption
        domain: Domain context (medical, legal, finance, etc.)
        metadata: Additional context-specific metadata
        parent_context: Parent context for nested operations
        conversation: Conversation state for LLM interactions
    """
    
    # Identity
    context_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    program_name: str = "unnamed_program"
    
    # Execution control
    execution_mode: ExecutionMode = ExecutionMode.ADAPTIVE
    quality_threshold: float = 0.7
    criticality: float = 0.5
    time_pressure: float = 0.3
    
    # Resource management
    token_budget: int = 10000
    token_usage: int = 0
    time_budget_ms: Optional[int] = None
    time_usage_ms: int = 0
    
    # Domain and specialization
    domain: Optional[str] = None
    capabilities: list[str] = field(default_factory=list)
    
    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    parent_context: Optional['ExecutionContext'] = None
    
    # Runtime state
    depth: int = 0  # Nesting depth
    attempt_number: int = 1  # For retries
    
    # Conversation state for LLM interactions
    conversation: ConversationState = field(default_factory=ConversationState)
    
    def __post_init__(self):
        """Validate context parameters."""
        if not 0.0 <= self.quality_threshold <= 1.0:
            raise ValueError("quality_threshold must be in [0.0, 1.0]")
        if not 0.0 <= self.criticality <= 1.0:
            raise ValueError("criticality must be in [0.0, 1.0]")
        if not 0.0 <= self.time_pressure <= 1.0:
            raise ValueError("time_pressure must be in [0.0, 1.0]")
        if self.token_budget <= 0:
            raise ValueError("token_budget must be positive")
    
    def create_child_context(
        self,
        program_name: Optional[str] = None,
        **overrides
    ) -> 'ExecutionContext':
        """
        Create a child context for nested operations.
        
        Inherits configuration from parent but can override specific values.
        Automatically increments depth and manages resource inheritance.
        
        Args:
            program_name: Name for child program (default: parent + suffix)
            **overrides: Any context attributes to override
        
        Returns:
            New ExecutionContext with parent reference
        """
        child_data = {
            'context_id': str(uuid.uuid4()),
            'program_name': program_name or f"{self.program_name}_child",
            'execution_mode': self.execution_mode,
            'quality_threshold': self.quality_threshold,
            'criticality': self.criticality,
            'time_pressure': self.time_pressure,
            'token_budget': max(0, self.token_budget - self.token_usage),
            'token_usage': 0,
            'time_budget_ms': (
                max(0, self.time_budget_ms - self.time_usage_ms) 
                if self.time_budget_ms else None
            ),
            'time_usage_ms': 0,
            'domain': self.domain,
            'capabilities': self.capabilities.copy(),
            'metadata': self.metadata.copy(),
            'parent_context': self,
            'depth': self.depth + 1,
            'attempt_number': 1,
        }
        
        # Apply overrides
        child_data.update(overrides)
        
        return ExecutionContext(**child_data)
    
    def consume_tokens(self, tokens: int) -> None:
        """
        Record token consumption.
        
        Args:
            tokens: Number of tokens consumed
        
        Raises:
            RuntimeError: If token budget exceeded
        """
        self.token_usage += tokens
        if self.token_usage > self.token_budget:
            raise RuntimeError(
                f"Token budget exceeded: {self.token_usage} > {self.token_budget}"
            )
    
    def consume_time(self, milliseconds: int) -> None:
        """
        Record time consumption.
        
        Args:
            milliseconds: Time consumed in milliseconds
        
        Raises:
            RuntimeError: If time budget exceeded
        """
        self.time_usage_ms += milliseconds
        if self.time_budget_ms and self.time_usage_ms > self.time_budget_ms:
            raise RuntimeError(
                f"Time budget exceeded: {self.time_usage_ms}ms > {self.time_budget_ms}ms"
            )
    
    def has_capacity(self, tokens: int = 0, milliseconds: int = 0) -> bool:
        """
        Check if context has capacity for additional resource consumption.
        
        Args:
            tokens: Additional tokens needed
            milliseconds: Additional time needed
        
        Returns:
            True if resources available, False otherwise
        """
        token_ok = (self.token_usage + tokens) <= self.token_budget
        time_ok = (
            self.time_budget_ms is None or
            (self.time_usage_ms + milliseconds) <= self.time_budget_ms
        )
        return token_ok and time_ok
    
    def add_conversation_message(
        self,
        role: str,
        content: str,
        memory: Optional['WorkingMemory'] = None,
        **metadata
    ) -> ConversationMessage:
        """
        Add message to conversation and optionally persist to working memory.
        
        Args:
            role: Message role ('system', 'user', 'assistant')
            content: Message content
            memory: Optional working memory for persistence
            **metadata: Additional message metadata
        
        Returns:
            Created ConversationMessage
        """
        # Store in memory if provided
        memory_ref = None
        if memory is not None:
            from brainary.memory.working import MemoryTier
            # Extract importance from metadata or use default
            importance = metadata.pop('importance', 0.6)
            memory_ref = memory.store(
                content={
                    'role': role,
                    'content': content,
                    'conversation_id': self.conversation.conversation_id,
                    'metadata': metadata
                },
                tier=MemoryTier.L2_EPISODIC,  # Conversations go to L2 for persistence
                importance=importance,
                tags=['conversation', f'role:{role}', f'program:{self.program_name}'],
                source_primitive='conversation_manager',
                **metadata
            )
        
        # Add to conversation state
        return self.conversation.add_message(
            role=role,
            content=content,
            memory_ref=memory_ref,
            **metadata
        )
    
    def get_conversation_history(
        self,
        include_system: bool = True,
        max_messages: Optional[int] = None
    ) -> List[Dict[str, str]]:
        """
        Get conversation history in LLM API format.
        
        Args:
            include_system: Include system prompt
            max_messages: Maximum number of recent messages
        
        Returns:
            List of message dicts for LLM API
        """
        return self.conversation.get_messages_for_llm(
            include_system=include_system,
            max_messages=max_messages
        )
    
    def set_system_prompt(self, prompt: str) -> None:
        """
        Set system prompt for LLM conversations.
        
        Args:
            prompt: System prompt text
        """
        self.conversation.system_prompt = prompt
    
    def update_conversation_cost(self, tokens: int, cost_usd: float) -> None:
        """
        Update conversation token and cost tracking.
        
        Args:
            tokens: Tokens consumed
            cost_usd: Cost in USD
        """
        self.conversation.total_tokens += tokens
        self.conversation.total_cost_usd += cost_usd
        self.consume_tokens(tokens)
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """
        Get conversation summary.
        
        Returns:
            Summary dictionary
        """
        return self.conversation.summarize()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert context to dictionary representation."""
        return {
            'context_id': self.context_id,
            'program_name': self.program_name,
            'execution_mode': self.execution_mode.value,
            'quality_threshold': self.quality_threshold,
            'criticality': self.criticality,
            'time_pressure': self.time_pressure,
            'token_budget': self.token_budget,
            'token_usage': self.token_usage,
            'time_budget_ms': self.time_budget_ms,
            'time_usage_ms': self.time_usage_ms,
            'domain': self.domain,
            'capabilities': self.capabilities,
            'metadata': self.metadata,
            'depth': self.depth,
            'attempt_number': self.attempt_number,
            'conversation_summary': self.conversation.summarize(),
        }


def create_execution_context(
    program_name: str = "unnamed_program",
    execution_mode: ExecutionMode = ExecutionMode.ADAPTIVE,
    quality_threshold: float = 0.7,
    criticality: float = 0.5,
    time_pressure: float = 0.3,
    token_budget: int = 10000,
    domain: Optional[str] = None,
    **kwargs
) -> ExecutionContext:
    """
    Convenience function to create an execution context.
    
    Args:
        program_name: Name of the program
        execution_mode: Execution mode (SYSTEM1/SYSTEM2/ADAPTIVE)
        quality_threshold: Minimum confidence threshold (0.0-1.0)
        criticality: Operation criticality (0.0-1.0)
        time_pressure: Time sensitivity (0.0-1.0)
        token_budget: Maximum tokens allowed
        domain: Domain specialization
        **kwargs: Additional context attributes
    
    Returns:
        New ExecutionContext instance
    """
    return ExecutionContext(
        program_name=program_name,
        execution_mode=execution_mode,
        quality_threshold=quality_threshold,
        criticality=criticality,
        time_pressure=time_pressure,
        token_budget=token_budget,
        domain=domain,
        **kwargs
    )
