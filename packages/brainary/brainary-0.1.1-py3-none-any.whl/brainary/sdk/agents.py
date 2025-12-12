"""
Agent Templates

Provides pre-configured agent templates for common use cases.
Templates define specialized cognitive agents with optimized settings.
"""

from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum

from brainary.sdk.client import Brainary
from brainary.sdk.memory import MemoryManager
from brainary.sdk.context import ContextBuilder
from brainary.primitive.base import PrimitiveResult


class AgentRole(Enum):
    """Predefined agent roles."""
    ANALYST = "analyst"
    RESEARCHER = "researcher"
    CODER = "coder"
    REVIEWER = "reviewer"
    PLANNER = "planner"
    WRITER = "writer"
    TEACHER = "teacher"
    ASSISTANT = "assistant"


@dataclass
class AgentConfig:
    """Configuration for an agent."""
    name: str
    role: AgentRole
    domain: str
    description: str
    
    # Cognitive settings
    quality_threshold: float = 0.8
    memory_capacity: int = 7
    enable_learning: bool = True
    
    # Execution preferences
    default_mode: str = "adaptive"  # "fast", "deep", "adaptive"
    token_budget: int = 10000
    
    # Behavioral traits
    reasoning_style: str = "analytical"  # "analytical", "creative", "practical"
    attention_focus: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    
    # Custom metadata
    metadata: Dict[str, Any] = field(default_factory=dict)


class Agent:
    """
    Specialized cognitive agent with role-specific configuration.
    
    An Agent is a Brainary instance configured for a specific role and domain,
    with predefined behaviors, memory management, and execution preferences.
    
    Examples:
        >>> agent = Agent.create("analyst", domain="security")
        >>> result = agent.analyze(code)
        
        >>> agent = Agent.from_config(custom_config)
        >>> result = agent.process(task)
    """
    
    def __init__(self, config: AgentConfig):
        """
        Initialize agent with configuration.
        
        Args:
            config: Agent configuration
        """
        self.config = config
        
        # Create underlying Brainary instance
        self.brain = Brainary(
            enable_learning=config.enable_learning,
            memory_capacity=config.memory_capacity,
            quality_threshold=config.quality_threshold,
            token_budget=config.token_budget,
            program_name=f"agent_{config.name}"
        )
        
        # Create dedicated memory
        self.memory = MemoryManager(capacity=config.memory_capacity)
        
        # Track agent statistics
        self._task_count = 0
        self._success_count = 0
    
    @classmethod
    def create(
        cls,
        role: str,
        domain: str = "general",
        name: Optional[str] = None,
        **overrides
    ) -> 'Agent':
        """
        Create agent from predefined role template.
        
        Args:
            role: Agent role (analyst, researcher, coder, etc.)
            domain: Domain of expertise
            name: Optional custom name
            **overrides: Override default configuration
        
        Returns:
            Configured Agent instance
        
        Examples:
            >>> agent = Agent.create("analyst", domain="security")
            >>> agent = Agent.create("coder", domain="python", quality_threshold=0.95)
        """
        role_enum = AgentRole(role)
        template = AGENT_TEMPLATES[role_enum]
        
        # Merge template with overrides
        config_dict = {**template, **overrides}
        config_dict['role'] = role_enum
        config_dict['domain'] = domain
        config_dict['name'] = name or f"{role}_{domain}"
        
        config = AgentConfig(**config_dict)
        return cls(config)
    
    @classmethod
    def from_config(cls, config: AgentConfig) -> 'Agent':
        """
        Create agent from custom configuration.
        
        Args:
            config: Agent configuration
        
        Returns:
            Agent instance
        
        Examples:
            >>> config = AgentConfig(
            ...     name="custom_agent",
            ...     role=AgentRole.ANALYST,
            ...     domain="finance",
            ...     quality_threshold=0.9
            ... )
            >>> agent = Agent.from_config(config)
        """
        return cls(config)
    
    def process(self, task: str, **kwargs) -> PrimitiveResult:
        """
        Process a task according to agent's role.
        
        Routes to appropriate cognitive operation based on role.
        
        Args:
            task: Task description
            **kwargs: Additional parameters
        
        Returns:
            PrimitiveResult from processing
        
        Examples:
            >>> agent = Agent.create("analyst")
            >>> result = agent.process("Analyze sales data")
        """
        # Create context based on agent config
        context = self._create_context()
        
        # Route based on role
        role_handlers = {
            AgentRole.ANALYST: self._analyze_task,
            AgentRole.RESEARCHER: self._research_task,
            AgentRole.CODER: self._code_task,
            AgentRole.REVIEWER: self._review_task,
            AgentRole.PLANNER: self._plan_task,
            AgentRole.WRITER: self._write_task,
            AgentRole.TEACHER: self._teach_task,
            AgentRole.ASSISTANT: self._assist_task,
        }
        
        handler = role_handlers.get(self.config.role, self._generic_task)
        result = handler(task, context, **kwargs)
        
        # Update statistics
        self._task_count += 1
        if result.success:
            self._success_count += 1
        
        return result
    
    def think(self, query: str, **kwargs) -> PrimitiveResult:
        """Deep reasoning about a query."""
        context = self._create_context()
        return self.brain.think(query, context=context, **kwargs)
    
    def analyze(self, data: Any, **kwargs) -> PrimitiveResult:
        """Analyze data with agent's domain expertise."""
        context = self._create_context()
        return self.brain.analyze(
            data,
            context=context,
            analysis_type=self.config.domain,
            **kwargs
        )
    
    def solve(self, problem: str, **kwargs) -> PrimitiveResult:
        """Solve a problem with agent's constraints."""
        context = self._create_context()
        return self.brain.solve(
            problem,
            context=context,
            constraints=self.config.constraints,
            **kwargs
        )
    
    def decide(self, options: List[Any], **kwargs) -> PrimitiveResult:
        """Make a decision between options."""
        context = self._create_context()
        return self.brain.decide(options, context=context, **kwargs)
    
    def remember(self, content: Any, importance: float = 0.7, **kwargs) -> None:
        """Store information in agent's memory."""
        self.memory.store(
            content,
            importance=importance,
            tags=[self.config.role.value, self.config.domain],
            **kwargs
        )
    
    def recall(self, query: str, **kwargs) -> List[Any]:
        """Recall information from memory."""
        results = self.memory.search(
            query,
            tags=[self.config.role.value, self.config.domain],
            **kwargs
        )
        return [r.content for r in results]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get agent statistics."""
        brain_stats = self.brain.get_stats()
        
        return {
            'agent': {
                'name': self.config.name,
                'role': self.config.role.value,
                'domain': self.config.domain,
                'tasks_processed': self._task_count,
                'success_rate': self._success_count / max(1, self._task_count),
            },
            'memory': self.memory.get_stats(),
            'brain': brain_stats
        }
    
    def set_focus(self, *keywords: str) -> None:
        """Set attention focus for the agent."""
        self.config.attention_focus = list(keywords)
    
    def add_constraint(self, constraint: str) -> None:
        """Add a behavioral constraint."""
        self.config.constraints.append(constraint)
    
    def _create_context(self):
        """Create execution context from agent config."""
        builder = (ContextBuilder()
            .program(f"agent_{self.config.name}")
            .domain(self.config.domain)
            .quality(self.config.quality_threshold)
            .budget(self.config.token_budget))
        
        # Set mode
        mode_map = {
            'fast': builder.fast_mode,
            'deep': builder.deep_mode,
            'adaptive': builder.adaptive_mode
        }
        mode_fn = mode_map.get(self.config.default_mode, builder.adaptive_mode)
        builder = mode_fn()
        
        # Add metadata
        builder = builder.metadata(
            role=self.config.role.value,
            reasoning_style=self.config.reasoning_style,
            **self.config.metadata
        )
        
        # Add constraints
        if self.config.constraints:
            builder = builder.constraints(*self.config.constraints)
        
        return builder.build()
    
    # Role-specific handlers
    
    def _analyze_task(self, task: str, context, **kwargs) -> PrimitiveResult:
        """Handle task as analyst."""
        return self.brain.analyze(task, context=context, **kwargs)
    
    def _research_task(self, task: str, context, **kwargs) -> PrimitiveResult:
        """Handle task as researcher."""
        # Research involves deep thinking and comprehensive analysis
        return self.brain.think(
            task,
            context=context,
            reasoning_mode="deep",
            **kwargs
        )
    
    def _code_task(self, task: str, context, **kwargs) -> PrimitiveResult:
        """Handle task as coder."""
        return self.brain.solve(
            task,
            context=context,
            constraints=self.config.constraints + ["code_output"],
            **kwargs
        )
    
    def _review_task(self, task: str, context, **kwargs) -> PrimitiveResult:
        """Handle task as reviewer."""
        return self.brain.analyze(
            task,
            context=context,
            analysis_type="critical",
            **kwargs
        )
    
    def _plan_task(self, task: str, context, **kwargs) -> PrimitiveResult:
        """Handle task as planner."""
        return self.brain.solve(
            task,
            context=context,
            constraints=self.config.constraints + ["structured_output"],
            **kwargs
        )
    
    def _write_task(self, task: str, context, **kwargs) -> PrimitiveResult:
        """Handle task as writer."""
        return self.brain.execute(
            "compose",
            context=context,
            content=task,
            **kwargs
        )
    
    def _teach_task(self, task: str, context, **kwargs) -> PrimitiveResult:
        """Handle task as teacher."""
        return self.brain.think(
            task,
            context=context,
            reasoning_mode="explanatory",
            **kwargs
        )
    
    def _assist_task(self, task: str, context, **kwargs) -> PrimitiveResult:
        """Handle task as assistant."""
        return self.brain.think(task, context=context, **kwargs)
    
    def _generic_task(self, task: str, context, **kwargs) -> PrimitiveResult:
        """Generic task handler."""
        return self.brain.think(task, context=context, **kwargs)
    
    def __repr__(self) -> str:
        return (f"Agent(name='{self.config.name}', "
                f"role={self.config.role.value}, "
                f"domain='{self.config.domain}')")


# Agent templates - predefined configurations for each role

AGENT_TEMPLATES: Dict[AgentRole, Dict[str, Any]] = {
    AgentRole.ANALYST: {
        'description': 'Analyzes data and identifies patterns, insights, and trends',
        'quality_threshold': 0.85,
        'memory_capacity': 10,
        'default_mode': 'deep',
        'reasoning_style': 'analytical',
        'attention_focus': ['patterns', 'anomalies', 'correlations'],
        'constraints': ['evidence_based', 'quantitative'],
    },
    
    AgentRole.RESEARCHER: {
        'description': 'Conducts thorough research and gathers comprehensive information',
        'quality_threshold': 0.90,
        'memory_capacity': 12,
        'default_mode': 'deep',
        'reasoning_style': 'analytical',
        'attention_focus': ['sources', 'evidence', 'methodology'],
        'constraints': ['cite_sources', 'comprehensive'],
    },
    
    AgentRole.CODER: {
        'description': 'Writes, debugs, and optimizes code',
        'quality_threshold': 0.85,
        'memory_capacity': 8,
        'default_mode': 'adaptive',
        'reasoning_style': 'practical',
        'attention_focus': ['correctness', 'efficiency', 'readability'],
        'constraints': ['syntactically_valid', 'documented'],
    },
    
    AgentRole.REVIEWER: {
        'description': 'Reviews and critiques work for quality and correctness',
        'quality_threshold': 0.90,
        'memory_capacity': 10,
        'default_mode': 'deep',
        'reasoning_style': 'critical',
        'attention_focus': ['errors', 'improvements', 'best_practices'],
        'constraints': ['constructive', 'specific'],
    },
    
    AgentRole.PLANNER: {
        'description': 'Creates structured plans and strategies',
        'quality_threshold': 0.85,
        'memory_capacity': 10,
        'default_mode': 'deep',
        'reasoning_style': 'strategic',
        'attention_focus': ['goals', 'resources', 'dependencies'],
        'constraints': ['actionable', 'realistic'],
    },
    
    AgentRole.WRITER: {
        'description': 'Composes clear, engaging, and well-structured content',
        'quality_threshold': 0.80,
        'memory_capacity': 8,
        'default_mode': 'adaptive',
        'reasoning_style': 'creative',
        'attention_focus': ['clarity', 'engagement', 'style'],
        'constraints': ['grammatically_correct', 'coherent'],
    },
    
    AgentRole.TEACHER: {
        'description': 'Explains concepts clearly and helps others learn',
        'quality_threshold': 0.85,
        'memory_capacity': 10,
        'default_mode': 'adaptive',
        'reasoning_style': 'explanatory',
        'attention_focus': ['clarity', 'examples', 'understanding'],
        'constraints': ['accessible', 'step_by_step'],
    },
    
    AgentRole.ASSISTANT: {
        'description': 'General-purpose helpful assistant',
        'quality_threshold': 0.80,
        'memory_capacity': 7,
        'default_mode': 'adaptive',
        'reasoning_style': 'practical',
        'attention_focus': ['user_needs', 'clarity', 'helpfulness'],
        'constraints': ['polite', 'concise'],
    },
}


class AgentTeam:
    """
    Coordinate multiple agents working together.
    
    A team manages multiple specialized agents and can route tasks
    to the most appropriate agent or have agents collaborate.
    
    Examples:
        >>> team = AgentTeam()
        >>> team.add_agent(Agent.create("analyst", domain="security"))
        >>> team.add_agent(Agent.create("coder", domain="python"))
        >>> result = team.process("Find and fix security bugs")
    """
    
    def __init__(self, name: str = "default_team"):
        """
        Initialize agent team.
        
        Args:
            name: Team name
        """
        self.name = name
        self.agents: Dict[str, Agent] = {}
        self._task_count = 0
    
    def add_agent(self, agent: Agent, alias: Optional[str] = None) -> None:
        """
        Add agent to team.
        
        Args:
            agent: Agent to add
            alias: Optional alias for the agent
        
        Examples:
            >>> team = AgentTeam()
            >>> team.add_agent(Agent.create("analyst"), alias="data_analyst")
        """
        key = alias or agent.config.name
        self.agents[key] = agent
    
    def remove_agent(self, name: str) -> None:
        """Remove agent from team."""
        self.agents.pop(name, None)
    
    def get_agent(self, name: str) -> Optional[Agent]:
        """Get agent by name."""
        return self.agents.get(name)
    
    def list_agents(self) -> List[str]:
        """List all agent names."""
        return list(self.agents.keys())
    
    def process(
        self,
        task: str,
        agent_name: Optional[str] = None,
        **kwargs
    ) -> PrimitiveResult:
        """
        Process task with appropriate agent.
        
        Args:
            task: Task to process
            agent_name: Optional specific agent to use
            **kwargs: Additional parameters
        
        Returns:
            PrimitiveResult from agent
        
        Examples:
            >>> team = AgentTeam()
            >>> team.add_agent(Agent.create("analyst"))
            >>> result = team.process("Analyze data", agent_name="analyst_general")
        """
        self._task_count += 1
        
        if agent_name:
            agent = self.agents.get(agent_name)
            if not agent:
                raise ValueError(f"Agent '{agent_name}' not found in team")
        else:
            # Auto-select agent based on task
            agent = self._select_agent(task)
        
        return agent.process(task, **kwargs)
    
    def collaborate(
        self,
        task: str,
        agent_names: List[str],
        strategy: str = "sequential"
    ) -> List[PrimitiveResult]:
        """
        Have multiple agents collaborate on a task.
        
        Args:
            task: Task for collaboration
            agent_names: Agents to involve
            strategy: "sequential" or "parallel"
        
        Returns:
            List of results from each agent
        
        Examples:
            >>> team = AgentTeam()
            >>> team.add_agent(Agent.create("analyst"))
            >>> team.add_agent(Agent.create("reviewer"))
            >>> results = team.collaborate(
            ...     "Analyze code for bugs",
            ...     ["analyst_general", "reviewer_general"]
            ... )
        """
        results = []
        
        if strategy == "sequential":
            # Each agent builds on previous results
            current_task = task
            for agent_name in agent_names:
                agent = self.agents[agent_name]
                result = agent.process(current_task)
                results.append(result)
                # Next agent gets previous output
                if result.success:
                    current_task = f"{task}\n\nPrevious analysis: {result.content}"
        
        elif strategy == "parallel":
            # All agents work independently
            for agent_name in agent_names:
                agent = self.agents[agent_name]
                result = agent.process(task)
                results.append(result)
        
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """Get team statistics."""
        return {
            'team': {
                'name': self.name,
                'agent_count': len(self.agents),
                'total_tasks': self._task_count,
            },
            'agents': {
                name: agent.get_stats()
                for name, agent in self.agents.items()
            }
        }
    
    def _select_agent(self, task: str) -> Agent:
        """Select best agent for task (simple heuristic)."""
        if not self.agents:
            raise ValueError("No agents in team")
        
        # Simple keyword matching for now
        task_lower = task.lower()
        
        role_keywords = {
            AgentRole.ANALYST: ['analyze', 'data', 'pattern', 'trend'],
            AgentRole.RESEARCHER: ['research', 'investigate', 'study', 'find'],
            AgentRole.CODER: ['code', 'program', 'implement', 'debug'],
            AgentRole.REVIEWER: ['review', 'check', 'critique', 'evaluate'],
            AgentRole.PLANNER: ['plan', 'strategy', 'organize', 'schedule'],
            AgentRole.WRITER: ['write', 'compose', 'draft', 'document'],
            AgentRole.TEACHER: ['explain', 'teach', 'learn', 'understand'],
        }
        
        # Score each agent
        best_agent = None
        best_score = -1
        
        for agent in self.agents.values():
            keywords = role_keywords.get(agent.config.role, [])
            score = sum(1 for kw in keywords if kw in task_lower)
            
            if score > best_score:
                best_score = score
                best_agent = agent
        
        # Default to first agent if no match
        return best_agent or list(self.agents.values())[0]
    
    def __repr__(self) -> str:
        return f"AgentTeam(name='{self.name}', agents={len(self.agents)})"
