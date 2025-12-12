"""
Brainary SDK - User-Oriented API

This module provides high-level, user-friendly APIs for interacting with
the Brainary cognitive computing platform.

Quick Start:
    >>> from brainary.sdk import Brainary
    >>> 
    >>> # Initialize Brainary
    >>> brain = Brainary()
    >>> 
    >>> # Execute cognitive operations
    >>> result = brain.think("What is 2+2?")
    >>> print(result.content)
    
Main Components:
    - Brainary: Main SDK interface
    - primitives: Core cognitive operations
    - memory: Memory management
    - context: Execution context management
"""

from brainary.sdk.client import Brainary
from brainary.sdk.primitives import (
    # Core primitives
    perceive,
    think,
    remember,
    recall,
    associate,
    action,
    # Composite primitives
    analyze,
    solve,
    decide,
    create,
    decompose,
    synthesize,
    evaluate,
    verify,
    explain,
    plan,
    # Metacognitive primitives
    introspect,
    self_assess,
    select_strategy,
    self_correct,
    reflect,
    # Utilities
    configure,
    get_stats,
    clear_memory,
)
from brainary.sdk.memory import MemoryManager
from brainary.sdk.context import ContextBuilder, ContextManager, create_context
from brainary.sdk.agents import Agent, AgentTeam, AgentRole, AgentConfig
from brainary.sdk.template_agent import (
    TemplateAgent,
    SimpleAgent,
)

__all__ = [
    # Main client
    'Brainary',
    
    # Core primitives
    'perceive',
    'think',
    'remember',
    'recall',
    'associate',
    'action',
    
    # Composite primitives
    'analyze',
    'solve',
    'decide',
    'create',
    'decompose',
    'synthesize',
    'evaluate',
    'verify',
    'explain',
    'plan',
    
    # Metacognitive primitives
    'introspect',
    'self_assess',
    'select_strategy',
    'self_correct',
    'reflect',
    
    # Configuration
    'configure',
    'get_stats',
    'clear_memory',
    
    # Memory
    'MemoryManager',
    
    # Context
    'ContextBuilder',
    'ContextManager',
    'create_context',
    
    # Agents
    'Agent',
    'AgentTeam',
    'AgentRole',
    'AgentConfig',
    
    # Template Agent
    'TemplateAgent',
    'SimpleAgent',
]

__version__ = '0.9.0'
