"""
Primitive system for Brainary.

Primitives are the fundamental building blocks of cognitive programs.

The primitive system has clear separation of concerns:
1. Catalog (catalog.py): Defines valid primitive names (WHAT operations exist)
2. Router (router.py): Routes names to implementations (HOW to execute)
3. Base (base.py): Base classes for implementations
4. Registry (registry.py): Manages primitive metadata and PoK libraries
5. Implementations (implementations/): Concrete implementations

Usage:
    >>> from brainary.primitive import get_primitive_catalog, register_implementation
    >>> from brainary.primitive.implementations.core import ThinkDeep
    >>>
    >>> # Check what primitives are available
    >>> catalog = get_primitive_catalog()
    >>> primitives = catalog.list_by_level(PrimitiveLevel.CORE)
    >>>
    >>> # Register an implementation
    >>> register_implementation("think", ThinkDeep())
"""

from brainary.primitive.base import (
    Primitive,
    CorePrimitive,
    CompositePrimitive,
    MetacognitivePrimitive,
    DomainPrimitive,
    ControlPrimitive,
    PrimitiveLevel,
    PrimitiveResult,
    ResourceEstimate,
    CostMetrics,
    ConfidenceScore,
    ConfidenceMetrics,
    MemoryWrite,
    MemoryOperation,
)

from brainary.primitive.registry import (
    PrimitiveRegistry,
    PrimitiveMetadata,
    get_global_registry,
    PoKProgram,
    PoKLibrary,
    PoKLibraryRegistry,
    get_pok_library_registry,
)

from brainary.primitive.catalog import (
    PrimitiveCatalog,
    PrimitiveDef,
    get_primitive_catalog,
    list_primitives,
    is_valid_primitive,
    get_primitive_def,
)

from brainary.primitive.router import (
    PrimitiveRouter,
    RoutingDecision,
    RoutingSource,
    RoutingStatistics,
    ExperienceCache,
    get_primitive_router,
    register_implementation,
    route_primitive,
)


_primitives_registered = False


def register_core_primitives():
    """
    Register all core primitive implementations with the router.
    
    This function should be called at startup to populate the routing system
    with standard implementations. Uses a singleton pattern to only register once.
    """
    global _primitives_registered
    
    if _primitives_registered:
        return
    
    # Import all built-in primitive implementations
    from brainary.primitive.implementations.core import (
        PerceiveLLM,
        ThinkFast,
        ThinkDeep,
        RememberWorkingMemory,
        RecallWorkingMemory,
        AssociateConcepts,
        ActionExecutor,
        MonitorState,
        AdaptStrategy,
    )
    from brainary.primitive.implementations.control import (
        SequenceControl,
        ParallelControl,
        ConditionalControl,
        LoopControl,
        RetryControl,
    )
    from brainary.primitive.implementations.metacognitive import (
        IntrospectMetacognitive,
        SelfAssessMetacognitive,
        SelectStrategyMetacognitive,
        SelfCorrectMetacognitive,
        ReflectMetacognitive,
    )
    
    # Register core primitives (Level 0)
    register_implementation("perceive", PerceiveLLM())
    register_implementation("think", ThinkDeep())  # Default to deep thinking
    register_implementation("remember", RememberWorkingMemory())
    register_implementation("recall", RecallWorkingMemory())
    register_implementation("associate", AssociateConcepts())
    register_implementation("action", ActionExecutor())
    register_implementation("monitor", MonitorState())
    register_implementation("adapt", AdaptStrategy())
    
    # Register control flow primitives (Level 4)
    register_implementation("sequence", SequenceControl())
    register_implementation("parallel", ParallelControl())
    register_implementation("conditional", ConditionalControl())
    register_implementation("loop", LoopControl())
    register_implementation("retry", RetryControl())
    
    # Register metacognitive primitives (Level 2)
    register_implementation("introspect", IntrospectMetacognitive())
    register_implementation("self_assess", SelfAssessMetacognitive())
    register_implementation("select_strategy", SelectStrategyMetacognitive())
    register_implementation("self_correct", SelfCorrectMetacognitive())
    register_implementation("reflect", ReflectMetacognitive())
    
    _primitives_registered = True


__all__ = [
    # Base classes
    'Primitive',
    'CorePrimitive',
    'CompositePrimitive',
    'MetacognitivePrimitive',
    'DomainPrimitive',
    'ControlPrimitive',
    'PrimitiveLevel',
    
    # Result types
    'PrimitiveResult',
    'ResourceEstimate',
    'CostMetrics',
    'ConfidenceScore',
    'ConfidenceMetrics',
    'MemoryWrite',
    'MemoryOperation',
    
    # Registry (old system, for backward compatibility)
    'PrimitiveRegistry',
    'PrimitiveMetadata',
    'get_global_registry',
    
    # PoK
    'PoKProgram',
    'PoKLibrary',
    'PoKLibraryRegistry',
    'get_pok_library_registry',
    
    # Catalog (new system)
    'PrimitiveCatalog',
    'PrimitiveDef',
    'get_primitive_catalog',
    'list_primitives',
    'is_valid_primitive',
    'get_primitive_def',
    
    # Router (new system)
    'PrimitiveRouter',
    'RoutingDecision',
    'RoutingSource',
    'RoutingStatistics',
    'ExperienceCache',
    'get_primitive_router',
    'register_implementation',
    'route_primitive',
    
    
    # Registration
    'register_core_primitives',
]
