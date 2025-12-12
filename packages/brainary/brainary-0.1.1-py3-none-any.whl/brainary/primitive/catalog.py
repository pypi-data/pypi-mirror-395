"""
Primitive Catalog - Canonical list of cognitive primitives.

This module defines the complete set of valid primitive names in Brainary,
organized by the 5-level hierarchy. Each primitive can have multiple implementations.

The catalog enables:
1. Clear separation between primitive definitions (operations) and implementations
2. Validation of primitive names (only registered names are valid)
3. Discovery of available operations at each cognitive level
4. Extensibility through dynamic registration

Primitive Hierarchy (from DESIGN.md):
- Level 0: Core Cognitive (perceive, think, remember, associate, action, monitor, adapt)
- Level 1: Composite (analyze, solve, decide, create, explain)  
- Level 2: Metacognitive (introspect, self_assess, select_strategy, self_correct)
- Level 3: Domain-Specific (medical.*, finance.*, legal.*, etc.)
- Level 4: Control Flow (sequence, parallel, conditional, loop, retry)
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Set
import threading

from brainary.primitive.base import PrimitiveLevel


@dataclass
class PrimitiveDef:
    """
    Definition of a cognitive primitive operation.
    
    This defines WHAT the primitive does (the interface),
    not HOW it's implemented (implementations are separate).
    """
    
    name: str                           # Unique primitive name
    level: PrimitiveLevel              # Hierarchy level
    description: str                    # Human-readable description
    input_schema: Dict = None          # Expected inputs (optional)
    output_schema: Dict = None         # Expected outputs (optional)
    parent: Optional[str] = None       # Parent primitive (for bindings)
    aliases: List[str] = None          # Alternative names
    tags: Set[str] = None              # Classification tags
    
    def __post_init__(self):
        """Initialize default values."""
        if self.input_schema is None:
            self.input_schema = {}
        if self.output_schema is None:
            self.output_schema = {}
        if self.aliases is None:
            self.aliases = []
        if self.tags is None:
            self.tags = set()


class PrimitiveCatalog:
    """
    Central catalog of all valid primitive names.
    
    This is the authoritative registry of primitive definitions,
    separate from implementations. It defines the "vocabulary"
    of cognitive operations available in Brainary.
    """
    
    def __init__(self):
        """Initialize empty catalog."""
        self._primitives: Dict[str, PrimitiveDef] = {}
        self._level_index: Dict[PrimitiveLevel, Set[str]] = {
            level: set() for level in PrimitiveLevel
        }
        self._tag_index: Dict[str, Set[str]] = {}
        self._aliases: Dict[str, str] = {}  # alias -> canonical name
        self._lock = threading.RLock()
        
        # Initialize with standard primitives
        self._register_standard_primitives()
    
    def register(self, primitive_def: PrimitiveDef) -> None:
        """
        Register a primitive definition.
        
        Args:
            primitive_def: Primitive definition to register
        """
        with self._lock:
            name = primitive_def.name
            
            # Check for duplicates
            if name in self._primitives:
                raise ValueError(f"Primitive '{name}' already registered")
            
            # Register primitive
            self._primitives[name] = primitive_def
            
            # Update level index
            self._level_index[primitive_def.level].add(name)
            
            # Update tag index
            for tag in primitive_def.tags:
                if tag not in self._tag_index:
                    self._tag_index[tag] = set()
                self._tag_index[tag].add(name)
            
            # Register aliases
            for alias in primitive_def.aliases:
                if alias in self._aliases:
                    raise ValueError(f"Alias '{alias}' already registered")
                self._aliases[alias] = name
    
    def get(self, name: str) -> Optional[PrimitiveDef]:
        """
        Get primitive definition by name.
        
        Args:
            name: Primitive name or alias
            
        Returns:
            PrimitiveDef if found, None otherwise
        """
        with self._lock:
            # Check if it's an alias
            if name in self._aliases:
                name = self._aliases[name]
            
            return self._primitives.get(name)
    
    def is_valid(self, name: str) -> bool:
        """
        Check if a primitive name is valid.
        
        Args:
            name: Primitive name to check
            
        Returns:
            True if name is registered, False otherwise
        """
        return self.get(name) is not None
    
    def list_by_level(self, level: PrimitiveLevel) -> List[PrimitiveDef]:
        """
        List all primitives at a specific level.
        
        Args:
            level: Primitive level
            
        Returns:
            List of primitive definitions
        """
        with self._lock:
            names = self._level_index.get(level, set())
            return [self._primitives[name] for name in names]
    
    def list_by_tag(self, tag: str) -> List[PrimitiveDef]:
        """
        List all primitives with a specific tag.
        
        Args:
            tag: Tag name
            
        Returns:
            List of primitive definitions
        """
        with self._lock:
            names = self._tag_index.get(tag, set())
            return [self._primitives[name] for name in names]
    
    def list_all(self) -> List[PrimitiveDef]:
        """
        List all registered primitives.
        
        Returns:
            List of all primitive definitions
        """
        with self._lock:
            return list(self._primitives.values())
    
    def _register_standard_primitives(self) -> None:
        """Register the standard set of primitives from DESIGN.md."""
        
        # ====================================================================
        # LEVEL 0: CORE COGNITIVE PRIMITIVES
        # ====================================================================
        
        self.register(PrimitiveDef(
            name="perceive",
            level=PrimitiveLevel.CORE,
            description="Process and interpret inputs with attention focus",
            input_schema={"input": "any", "attention_focus": "str"},
            output_schema={"content": "any", "confidence": "float"},
            tags={"input", "sensing", "attention"},
        ))
        
        self.register(PrimitiveDef(
            name="think",
            level=PrimitiveLevel.CORE,
            description="Reason about information (fast or deep)",
            input_schema={"query": "str", "reasoning_mode": "str", "depth": "int"},
            output_schema={"content": "str", "reasoning_steps": "list"},
            aliases=["reason", "infer"],
            tags={"reasoning", "analysis", "cognition"},
        ))
        
        self.register(PrimitiveDef(
            name="remember",
            level=PrimitiveLevel.CORE,
            description="Store information in memory with importance",
            input_schema={"content": "any", "importance": "float", "tags": "list"},
            output_schema={"item_id": "str", "success": "bool"},
            aliases=["store", "memorize"],
            tags={"memory", "storage"},
        ))
        
        self.register(PrimitiveDef(
            name="recall",
            level=PrimitiveLevel.CORE,
            description="Retrieve information from memory",
            input_schema={"query": "str", "tags": "list", "limit": "int"},
            output_schema={"items": "list", "relevance_scores": "list"},
            aliases=["retrieve", "fetch"],
            tags={"memory", "retrieval"},
        ))
        
        self.register(PrimitiveDef(
            name="associate",
            level=PrimitiveLevel.CORE,
            description="Create connections between concepts",
            input_schema={"concept_a": "str", "concept_b": "str", "strength": "float"},
            output_schema={"link_id": "str", "success": "bool"},
            aliases=["link", "connect"],
            tags={"memory", "association", "relationships"},
        ))
        
        self.register(PrimitiveDef(
            name="action",
            level=PrimitiveLevel.CORE,
            description="Execute an action with parameters",
            input_schema={"command": "str", "parameters": "dict"},
            output_schema={"result": "any", "success": "bool"},
            aliases=["act", "execute", "do"],
            tags={"action", "execution"},
        ))
        
        self.register(PrimitiveDef(
            name="monitor",
            level=PrimitiveLevel.CORE,
            description="Track system or process state",
            input_schema={"target": "any", "metrics": "list"},
            output_schema={"status": "dict", "alerts": "list"},
            aliases=["observe", "watch", "track"],
            tags={"monitoring", "observation"},
        ))
        
        self.register(PrimitiveDef(
            name="adapt",
            level=PrimitiveLevel.CORE,
            description="Modify approach or strategy",
            input_schema={"feedback": "any", "adjustment": "dict"},
            output_schema={"new_strategy": "dict", "confidence": "float"},
            aliases=["adjust", "modify", "tune"],
            tags={"adaptation", "learning"},
        ))
        
        # ====================================================================
        # LEVEL 1: COMPOSITE PRIMITIVES
        # ====================================================================
        
        self.register(PrimitiveDef(
            name="analyze",
            level=PrimitiveLevel.COMPOSITE,
            description="Comprehensive analysis: perceive + decompose + think + relate",
            input_schema={"data": "any", "approach": "str", "depth": "int"},
            output_schema={"analysis": "dict", "insights": "list"},
            tags={"analysis", "composite"},
        ))
        
        self.register(PrimitiveDef(
            name="solve",
            level=PrimitiveLevel.COMPOSITE,
            description="Problem solving: analyze + generate + test + refine",
            input_schema={"problem": "any", "constraints": "list"},
            output_schema={"solution": "any", "confidence": "float"},
            aliases=["resolve", "fix"],
            tags={"problem-solving", "composite"},
        ))
        
        self.register(PrimitiveDef(
            name="decide",
            level=PrimitiveLevel.COMPOSITE,
            description="Decision making: evaluate + compare + choose + commit",
            input_schema={"options": "list", "criteria": "dict"},
            output_schema={"decision": "any", "rationale": "str"},
            aliases=["choose", "select"],
            tags={"decision-making", "composite"},
        ))
        
        self.register(PrimitiveDef(
            name="create",
            level=PrimitiveLevel.COMPOSITE,
            description="Creative generation: imagine + generate + combine + refine",
            input_schema={"goal": "str", "constraints": "list", "style": "str"},
            output_schema={"output": "any", "novelty_score": "float"},
            aliases=["generate", "produce"],
            tags={"creativity", "generation", "composite"},
        ))
        
        self.register(PrimitiveDef(
            name="explain",
            level=PrimitiveLevel.COMPOSITE,
            description="Explanation: understand + structure + communicate + verify",
            input_schema={"concept": "any", "audience": "str", "detail_level": "int"},
            output_schema={"explanation": "str", "clarity_score": "float"},
            aliases=["describe", "clarify"],
            tags={"communication", "explanation", "composite"},
        ))
        
        # ====================================================================
        # LEVEL 2: METACOGNITIVE PRIMITIVES
        # ====================================================================
        
        self.register(PrimitiveDef(
            name="introspect",
            level=PrimitiveLevel.METACOGNITIVE,
            description="Self-observation: monitor(self) + analyze(internal_state)",
            input_schema={"aspect": "str"},
            output_schema={"state": "dict", "assessment": "str"},
            aliases=["self_monitor", "self_observe"],
            tags={"metacognition", "self-awareness"},
        ))
        
        self.register(PrimitiveDef(
            name="self_assess",
            level=PrimitiveLevel.METACOGNITIVE,
            description="Self-evaluation: evaluate(own_performance) + calibrate(confidence)",
            input_schema={"result": "any", "criteria": "list"},
            output_schema={"scores": "dict", "calibrated_confidence": "float"},
            aliases=["self_evaluate", "self_check"],
            tags={"metacognition", "evaluation"},
        ))
        
        self.register(PrimitiveDef(
            name="select_strategy",
            level=PrimitiveLevel.METACOGNITIVE,
            description="Strategy selection: assess_situation + match_approach + commit",
            input_schema={"situation": "dict", "options": "list"},
            output_schema={"strategy": "str", "rationale": "str"},
            aliases=["choose_approach", "pick_strategy"],
            tags={"metacognition", "strategy"},
        ))
        
        self.register(PrimitiveDef(
            name="self_correct",
            level=PrimitiveLevel.METACOGNITIVE,
            description="Self-correction: detect_error + adjust_strategy + retry",
            input_schema={"result": "any", "expected": "any"},
            output_schema={"corrected": "any", "adjustments": "list"},
            aliases={"fix_self", "auto_correct"},
            tags={"metacognition", "error-correction"},
        ))
        
        # ====================================================================
        # LEVEL 4: CONTROL FLOW PRIMITIVES
        # ====================================================================
        
        self.register(PrimitiveDef(
            name="sequence",
            level=PrimitiveLevel.CONTROL,
            description="Execute operations sequentially: A → B → C → ...",
            input_schema={"operations": "list", "continue_on_error": "bool"},
            output_schema={"results": "list", "success": "bool"},
            aliases=["sequential", "chain"],
            tags={"control-flow", "composition"},
        ))
        
        self.register(PrimitiveDef(
            name="parallel",
            level=PrimitiveLevel.CONTROL,
            description="Execute operations concurrently: A || B || C → Merge",
            input_schema={"operations": "list", "merge_strategy": "str"},
            output_schema={"results": "list", "merged": "any"},
            aliases=["concurrent", "parallel_exec"],
            tags={"control-flow", "parallelism"},
        ))
        
        self.register(PrimitiveDef(
            name="conditional",
            level=PrimitiveLevel.CONTROL,
            description="Conditional branching: if(condition) → then_branch else else_branch",
            input_schema={"condition": "callable", "then_op": "callable", "else_op": "callable"},
            output_schema={"result": "any", "branch_taken": "str"},
            aliases=["if_else", "branch"],
            tags={"control-flow", "branching"},
        ))
        
        self.register(PrimitiveDef(
            name="loop",
            level=PrimitiveLevel.CONTROL,
            description="Iterative execution: repeat(operation) while/until condition",
            input_schema={"operation": "callable", "condition": "callable", "max_iterations": "int"},
            output_schema={"results": "list", "iterations": "int"},
            aliases=["iterate", "repeat"],
            tags={"control-flow", "iteration"},
        ))
        
        self.register(PrimitiveDef(
            name="retry",
            level=PrimitiveLevel.CONTROL,
            description="Retry operation with backoff: retry(operation, max_attempts, strategy)",
            input_schema={"operation": "callable", "max_attempts": "int", "backoff": "str"},
            output_schema={"result": "any", "attempts": "int", "success": "bool"},
            aliases=["retry_with_backoff"],
            tags={"control-flow", "error-handling"},
        ))
        
        # Add more specialized primitives...
        
        self.register(PrimitiveDef(
            name="decompose",
            level=PrimitiveLevel.COMPOSITE,
            description="Break down complex problem into sub-problems",
            input_schema={"problem": "any", "strategy": "str"},
            output_schema={"sub_problems": "list", "structure": "dict"},
            tags={"analysis", "decomposition"},
        ))
        
        self.register(PrimitiveDef(
            name="synthesize",
            level=PrimitiveLevel.COMPOSITE,
            description="Combine multiple inputs into coherent whole",
            input_schema={"inputs": "list", "approach": "str"},
            output_schema={"synthesis": "any", "coherence_score": "float"},
            tags={"synthesis", "integration"},
        ))
        
        self.register(PrimitiveDef(
            name="evaluate",
            level=PrimitiveLevel.COMPOSITE,
            description="Assess quality/value against criteria",
            input_schema={"subject": "any", "criteria": "dict"},
            output_schema={"scores": "dict", "overall": "float"},
            tags={"evaluation", "assessment"},
        ))
        
        self.register(PrimitiveDef(
            name="verify",
            level=PrimitiveLevel.COMPOSITE,
            description="Check correctness/validity of result",
            input_schema={"result": "any", "expected": "any", "tolerance": "float"},
            output_schema={"valid": "bool", "errors": "list"},
            tags={"verification", "validation"},
        ))
        
        self.register(PrimitiveDef(
            name="plan",
            level=PrimitiveLevel.COMPOSITE,
            description="Create action plan to achieve goal",
            input_schema={"goal": "str", "constraints": "list", "resources": "dict"},
            output_schema={"plan": "list", "estimated_cost": "dict"},
            tags={"planning", "strategy"},
        ))
        
        self.register(PrimitiveDef(
            name="reflect",
            level=PrimitiveLevel.METACOGNITIVE,
            description="Reflect on experience to extract lessons",
            input_schema={"experience": "dict", "focus": "str"},
            output_schema={"insights": "list", "lessons": "list"},
            tags={"metacognition", "learning", "reflection"},
        ))


# Global catalog singleton
_global_catalog: Optional[PrimitiveCatalog] = None
_catalog_lock = threading.Lock()


def get_primitive_catalog() -> PrimitiveCatalog:
    """
    Get the global primitive catalog.
    
    Returns:
        Singleton PrimitiveCatalog instance
    """
    global _global_catalog
    
    if _global_catalog is None:
        with _catalog_lock:
            if _global_catalog is None:
                _global_catalog = PrimitiveCatalog()
    
    return _global_catalog


def list_primitives(level: Optional[PrimitiveLevel] = None) -> List[PrimitiveDef]:
    """
    List available primitives.
    
    Args:
        level: Optional level filter
        
    Returns:
        List of primitive definitions
    """
    catalog = get_primitive_catalog()
    if level is not None:
        return catalog.list_by_level(level)
    return catalog.list_all()


def is_valid_primitive(name: str) -> bool:
    """
    Check if a primitive name is valid.
    
    Args:
        name: Primitive name to check
        
    Returns:
        True if valid, False otherwise
    """
    catalog = get_primitive_catalog()
    return catalog.is_valid(name)


def get_primitive_def(name: str) -> Optional[PrimitiveDef]:
    """
    Get primitive definition by name.
    
    Args:
        name: Primitive name
        
    Returns:
        PrimitiveDef if found, None otherwise
    """
    catalog = get_primitive_catalog()
    return catalog.get(name)
