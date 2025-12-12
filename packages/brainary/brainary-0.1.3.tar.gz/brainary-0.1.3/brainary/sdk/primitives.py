"""
Primitive Function Wrappers

Provides standalone function-based API for primitives.
These are convenience functions that work without creating a client.
"""

from typing import Any, Optional, List, Dict, TYPE_CHECKING
from brainary.primitive.base import PrimitiveResult

if TYPE_CHECKING:
    from brainary.sdk.client import Brainary

# Global singleton client for function API
_global_client: Optional['Brainary'] = None


def _get_client() -> 'Brainary':
    """Get or create global client."""
    global _global_client
    if _global_client is None:
        from brainary.sdk.client import Brainary
        _global_client = Brainary()
    return _global_client


def configure(
    enable_learning: bool = True,
    memory_capacity: int = 7,
    quality_threshold: float = 0.8,
    **kwargs
) -> None:
    """
    Configure global Brainary settings.
    
    Args:
        enable_learning: Enable learning system
        memory_capacity: Working memory capacity
        quality_threshold: Quality threshold
        **kwargs: Additional configuration
    
    Examples:
        >>> from brainary.sdk import configure, think
        >>> configure(enable_learning=True, quality_threshold=0.9)
        >>> result = think("Complex problem")
    """
    global _global_client
    from brainary.sdk.client import Brainary
    _global_client = Brainary(
        enable_learning=enable_learning,
        memory_capacity=memory_capacity,
        quality_threshold=quality_threshold,
        **kwargs
    )


def think(query: str, reasoning_mode: str = "adaptive", **kwargs) -> PrimitiveResult:
    """
    Execute deep reasoning about a query.
    
    Args:
        query: Question or problem to reason about
        reasoning_mode: "fast", "deep", or "adaptive"
        **kwargs: Additional parameters
    
    Returns:
        PrimitiveResult with reasoning output
    
    Examples:
        >>> from brainary.sdk import think
        >>> result = think("What causes climate change?")
        >>> print(result.content)
    """
    return _get_client().think(query, reasoning_mode=reasoning_mode, **kwargs)


def perceive(
    input_data: Any,
    attention_focus: Optional[List[str]] = None,
    **kwargs
) -> PrimitiveResult:
    """
    Process and interpret input data.
    
    Args:
        input_data: Data to perceive
        attention_focus: Keywords to focus on
        **kwargs: Additional parameters
    
    Returns:
        PrimitiveResult with interpreted data
    
    Examples:
        >>> from brainary.sdk import perceive
        >>> result = perceive("source code", attention_focus=["bugs"])
        >>> print(result.content)
    """
    return _get_client().perceive(input_data, attention_focus=attention_focus, **kwargs)


def remember(
    content: Any,
    importance: float = 0.5,
    tags: Optional[List[str]] = None,
    **kwargs
) -> PrimitiveResult:
    """
    Store information in memory with intelligent association building.
    
    Uses LLM to identify and create associations with existing memories,
    organizing the memory structure for better retrieval.
    
    Args:
        content: Information to remember
        importance: Importance score (0-1)
        tags: Tags for retrieval
        **kwargs: Additional parameters
    
    Returns:
        PrimitiveResult with memory confirmation and associations created
    
    Examples:
        >>> from brainary.sdk import remember
        >>> result = remember("Python 3.11 improved performance", importance=0.9, tags=["python"])
        >>> print(f"Stored with {result.metadata.get('associations_created', 0)} associations")
    """
    return _get_client().remember(content, importance=importance, tags=tags, **kwargs)


def recall(
    query: Optional[str] = None,
    tags: Optional[List[str]] = None,
    limit: int = 5,
    **kwargs
) -> PrimitiveResult:
    """
    Retrieve information from memory with attention and spreading activation.
    
    Uses attention mechanisms to focus on relevant memories and spreads
    activation through the associative network to retrieve related information.
    
    Args:
        query: Search query for memory retrieval
        tags: Optional tag filters
        limit: Maximum number of items to retrieve
        **kwargs: Additional parameters
    
    Returns:
        PrimitiveResult with retrieved memories and associations
    
    Examples:
        >>> from brainary.sdk import recall
        >>> result = recall("Python performance", limit=10)
        >>> print(f"Found {len(result.content)} items")
        >>> print(f"Associated items: {result.metadata.get('associated_count', 0)}")
    """
    return _get_client().recall(query=query, tags=tags, limit=limit, **kwargs)


def associate(
    concept1: str,
    concept2: Optional[str] = None,
    strength: Optional[float] = None,
    discover_mode: bool = False,
    **kwargs
) -> PrimitiveResult:
    """
    Create associations between concepts in memory.
    
    Can operate in explicit mode (linking two concepts) or discover mode
    (finding related concepts automatically using LLM).
    
    Args:
        concept1: First concept or query for discovery
        concept2: Second concept (for explicit linking)
        strength: Association strength (0-1), auto-determined if None
        discover_mode: If True, discovers related concepts automatically
        **kwargs: Additional parameters
    
    Returns:
        PrimitiveResult with created associations
    
    Examples:
        >>> from brainary.sdk import associate
        >>> # Explicit mode: link two concepts
        >>> result = associate("Python", "performance", strength=0.8)
        >>> 
        >>> # Discover mode: find related concepts
        >>> result = associate("machine learning", discover_mode=True)
        >>> print(f"Found {len(result.content)} related concepts")
    """
    return _get_client().associate(
        concept1=concept1,
        concept2=concept2,
        strength=strength,
        discover_mode=discover_mode,
        **kwargs
    )


def action(
    action_type: str,
    parameters: Optional[Dict[str, Any]] = None,
    **kwargs
) -> PrimitiveResult:
    """
    Execute an action in the environment.
    
    Args:
        action_type: Type of action to perform
        parameters: Action parameters
        **kwargs: Additional parameters
    
    Returns:
        PrimitiveResult with action result
    
    Examples:
        >>> from brainary.sdk import action
        >>> result = action("write_file", {"path": "output.txt", "content": "data"})
    """
    return _get_client().execute(
        "action",
        action_type=action_type,
        parameters=parameters or {},
        **kwargs
    )


def analyze(
    data: Any,
    analysis_type: str = "general",
    **kwargs
) -> PrimitiveResult:
    """
    Perform comprehensive analysis.
    
    Args:
        data: Data to analyze
        analysis_type: Type of analysis
        **kwargs: Additional parameters
    
    Returns:
        PrimitiveResult with analysis
    
    Examples:
        >>> from brainary.sdk import analyze
        >>> result = analyze(source_code, analysis_type="security")
    """
    return _get_client().analyze(data, analysis_type=analysis_type, **kwargs)


def solve(
    problem: str,
    constraints: Optional[List[str]] = None,
    **kwargs
) -> PrimitiveResult:
    """
    Solve a problem with constraints.
    
    Args:
        problem: Problem description
        constraints: List of constraints
        **kwargs: Additional parameters
    
    Returns:
        PrimitiveResult with solution
    
    Examples:
        >>> from brainary.sdk import solve
        >>> result = solve("Optimize query", constraints=["< 100ms"])
    """
    return _get_client().solve(problem, constraints=constraints, **kwargs)


def decide(
    options: List[Any],
    criteria: Optional[List[str]] = None,
    **kwargs
) -> PrimitiveResult:
    """
    Make a decision between options.
    
    Args:
        options: List of options
        criteria: Decision criteria
        **kwargs: Additional parameters
    
    Returns:
        PrimitiveResult with decision
    
    Examples:
        >>> from brainary.sdk import decide
        >>> result = decide(["option_a", "option_b"], criteria=["cost", "speed"])
    """
    return _get_client().decide(options, criteria=criteria, **kwargs)


def get_stats() -> Dict[str, Any]:
    """
    Get execution statistics.
    
    Returns:
        Dictionary with statistics
    
    Examples:
        >>> from brainary.sdk import get_stats
        >>> stats = get_stats()
        >>> print(stats)
    """
    return _get_client().get_stats()


def clear_memory() -> None:
    """
    Clear working memory.
    
    Examples:
        >>> from brainary.sdk import clear_memory
        >>> clear_memory()
    """
    _get_client().clear_memory()


# ============================================================================
# Composite Primitives
# ============================================================================

def create(
    goal: str,
    constraints: Optional[List[str]] = None,
    **kwargs
) -> PrimitiveResult:
    """
    Generate novel solutions or artifacts.
    
    Args:
        goal: What to create
        constraints: Creation constraints
        **kwargs: Additional parameters
    
    Returns:
        PrimitiveResult with created artifact
    
    Examples:
        >>> from brainary.sdk import create
        >>> result = create("REST API design", constraints=["RESTful", "scalable"])
    """
    return _get_client().execute("create", goal=goal, constraints=constraints or [], **kwargs)


def decompose(
    problem: str,
    strategy: str = "top-down",
    **kwargs
) -> PrimitiveResult:
    """
    Break down complex problems into manageable parts.
    
    Args:
        problem: Problem to decompose
        strategy: Decomposition strategy ("top-down", "bottom-up")
        **kwargs: Additional parameters
    
    Returns:
        PrimitiveResult with decomposed components
    
    Examples:
        >>> from brainary.sdk import decompose
        >>> result = decompose("Build web application", strategy="top-down")
    """
    return _get_client().execute("decompose", problem=problem, strategy=strategy, **kwargs)


def synthesize(
    components: List[Any],
    goal: Optional[str] = None,
    **kwargs
) -> PrimitiveResult:
    """
    Combine components into coherent whole.
    
    Args:
        components: Parts to synthesize
        goal: Synthesis objective
        **kwargs: Additional parameters
    
    Returns:
        PrimitiveResult with synthesized result
    
    Examples:
        >>> from brainary.sdk import synthesize
        >>> result = synthesize(["auth module", "data layer", "API"], goal="complete system")
    """
    return _get_client().execute("synthesize", components=components, goal=goal, **kwargs)


def evaluate(
    subject: Any,
    criteria: Optional[List[str]] = None,
    **kwargs
) -> PrimitiveResult:
    """
    Assess quality and characteristics.
    
    Args:
        subject: What to evaluate
        criteria: Evaluation criteria
        **kwargs: Additional parameters
    
    Returns:
        PrimitiveResult with evaluation
    
    Examples:
        >>> from brainary.sdk import evaluate
        >>> result = evaluate(code, criteria=["maintainability", "performance"])
    """
    return _get_client().execute("evaluate", subject=subject, criteria=criteria or [], **kwargs)


def verify(
    claim: str,
    evidence: Optional[List[str]] = None,
    **kwargs
) -> PrimitiveResult:
    """
    Verify correctness and validity.
    
    Args:
        claim: Claim to verify
        evidence: Supporting evidence
        **kwargs: Additional parameters
    
    Returns:
        PrimitiveResult with verification status
    
    Examples:
        >>> from brainary.sdk import verify
        >>> result = verify("Algorithm is O(n log n)", evidence=["implementation", "tests"])
    """
    return _get_client().execute("verify", claim=claim, evidence=evidence or [], **kwargs)


def explain(
    subject: Any,
    audience: str = "general",
    **kwargs
) -> PrimitiveResult:
    """
    Generate clear explanations.
    
    Args:
        subject: What to explain
        audience: Target audience ("general", "expert", "beginner")
        **kwargs: Additional parameters
    
    Returns:
        PrimitiveResult with explanation
    
    Examples:
        >>> from brainary.sdk import explain
        >>> result = explain(algorithm, audience="beginner")
    """
    return _get_client().execute("explain", subject=subject, audience=audience, **kwargs)


def plan(
    goal: str,
    constraints: Optional[List[str]] = None,
    **kwargs
) -> PrimitiveResult:
    """
    Create action plans to achieve goals.
    
    Args:
        goal: Goal to achieve
        constraints: Planning constraints
        **kwargs: Additional parameters
    
    Returns:
        PrimitiveResult with action plan
    
    Examples:
        >>> from brainary.sdk import plan
        >>> result = plan("Migrate to microservices", constraints=["zero downtime"])
    """
    return _get_client().execute("plan", goal=goal, constraints=constraints or [], **kwargs)


# ============================================================================
# Metacognitive Primitives
# ============================================================================

def introspect(**kwargs) -> PrimitiveResult:
    """
    Examine internal cognitive state and processes.
    
    Returns:
        PrimitiveResult with introspection insights
    
    Examples:
        >>> from brainary.sdk import introspect
        >>> result = introspect()
        >>> print(result.content)  # Current cognitive state
    """
    return _get_client().execute("introspect", **kwargs)


def self_assess(
    task: str,
    performance: Optional[Dict[str, Any]] = None,
    **kwargs
) -> PrimitiveResult:
    """
    Assess own capabilities and performance.
    
    Args:
        task: Task to assess capability for
        performance: Optional performance metrics
        **kwargs: Additional parameters
    
    Returns:
        PrimitiveResult with self-assessment
    
    Examples:
        >>> from brainary.sdk import self_assess
        >>> result = self_assess("code review", performance={"accuracy": 0.85})
    """
    return _get_client().execute("self_assess", task=task, performance=performance, **kwargs)


def select_strategy(
    problem: str,
    available_strategies: Optional[List[str]] = None,
    **kwargs
) -> PrimitiveResult:
    """
    Choose appropriate problem-solving strategy.
    
    Args:
        problem: Problem to solve
        available_strategies: Available strategies
        **kwargs: Additional parameters
    
    Returns:
        PrimitiveResult with selected strategy
    
    Examples:
        >>> from brainary.sdk import select_strategy
        >>> result = select_strategy("optimize database", available_strategies=["index", "cache", "shard"])
    """
    return _get_client().execute(
        "select_strategy",
        problem=problem,
        available_strategies=available_strategies or [],
        **kwargs
    )


def self_correct(
    error: str,
    context: Optional[str] = None,
    **kwargs
) -> PrimitiveResult:
    """
    Identify and correct own mistakes.
    
    Args:
        error: Error or mistake to correct
        context: Context of the error
        **kwargs: Additional parameters
    
    Returns:
        PrimitiveResult with correction
    
    Examples:
        >>> from brainary.sdk import self_correct
        >>> result = self_correct("Logic error in function", context="sorting algorithm")
    """
    return _get_client().execute("self_correct", error=error, context=context, **kwargs)


def reflect(
    experience: str,
    **kwargs
) -> PrimitiveResult:
    """
    Reflect on experiences for learning.
    
    Args:
        experience: Experience to reflect on
        **kwargs: Additional parameters
    
    Returns:
        PrimitiveResult with insights and learnings
    
    Examples:
        >>> from brainary.sdk import reflect
        >>> result = reflect("Failed deployment due to missing config")
    """
    return _get_client().execute("reflect", experience=experience, **kwargs)
