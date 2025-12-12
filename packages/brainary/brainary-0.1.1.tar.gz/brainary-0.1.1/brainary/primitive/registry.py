"""
Primitive registry and discovery system.

Provides registration, discovery, and binding mechanisms for primitives and
Program-as-Knowledge (PoK) libraries, enabling extensibility and intelligent routing.
"""

from typing import Any, Callable, Dict, List, Optional, Set
from dataclasses import dataclass, field
import threading

from brainary.primitive.base import Primitive, PrimitiveLevel
from brainary.core.context import ExecutionContext


@dataclass
class PrimitiveMetadata:
    """Metadata for registered primitives."""
    
    primitive: Primitive
    name: str # Unique name within the namesapce
    namespace: List[str] = field(default_factory=list)
    bind_to: Optional[str] = None  # Core primitive name to bind to
    domain: Optional[str] = None
    capabilities: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    version: str = "1.0.0"
    author: Optional[str] = None
    description: Optional[str] = None
    performance_profile: Dict[str, Any] = field(default_factory=dict)


class PrimitiveRegistry:
    """
    Global registry for primitive discovery and binding.
    
    The registry enables:
    1. Primitive registration with metadata
    2. Binding domain-specific implementations to core primitives
    3. Discovery by domain, capabilities, tags
    4. Intelligent routing to optimal implementations
    """
    
    def __init__(self):
        """Initialize empty registry."""
        self._namespaces = {}
        self._primitives: Dict[str, List[PrimitiveMetadata]] = {}
        self._bindings: Dict[str, List[PrimitiveMetadata]] = {}  # Core name -> implementations
        self._domain_index: Dict[str, Set[str]] = {}  # Domain -> primitive names
        self._capability_index: Dict[str, Set[str]] = {}  # Capability -> primitive names
        self._tag_index: Dict[str, Set[str]] = {}  # Tag -> primitive names
        self._lock = threading.RLock()
    
    def register(
        self,
        primitive: Primitive,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Register a primitive with metadata.
        
        Args:
            primitive: Primitive instance to register
            metadata: Optional metadata dict with keys:
                - bind_to: Core primitive name to bind to
                - domain: Domain specialization
                - capabilities: List of capabilities
                - tags: Classification tags
                - version: Version string
                - author: Author name
                - description: Description text
                - performance_profile: Performance characteristics
        """
        with self._lock:
            metadata = metadata or {}
            namespace = primitive.name.split(".")
            unique_name = namespace[-1]
            namespace = [n for n in namespace[:-1] if len(n) != 0]
            
            cur_ns = self._namespaces
            for seg in namespace:
                if seg not in cur_ns:
                    cur_ns[seg] = {}
                cur_ns = cur_ns[seg] 
            
            if unique_name in cur_ns:
                raise ValueError(f"Primitive {primitive.name} already registered within namespace {namespace}")
            
            # Create metadata object
            prim_metadata = PrimitiveMetadata(
                primitive=primitive,
                namespace=namespace,
                name=unique_name,
                bind_to=metadata.get('bind_to'),
                domain=metadata.get('domain'),
                capabilities=metadata.get('capabilities', []),
                tags=metadata.get('tags', []),
                version=metadata.get('version', '1.0.0'),
                author=metadata.get('author'),
                description=metadata.get('description', primitive.description),
                performance_profile=metadata.get('performance_profile', {}),
            )
    
            cur_ns[unique_name] = prim_metadata
            # Register by primitive name
            prim_name = primitive.name
            if prim_name not in self._primitives:
                self._primitives[prim_name] = []
            self._primitives[prim_name].append(prim_metadata)
            
            # Register binding if specified
            if prim_metadata.bind_to:
                bind_name = prim_metadata.bind_to
                if bind_name not in self._bindings:
                    self._bindings[bind_name] = []
                self._bindings[bind_name].append(prim_metadata)
            
            # Update domain index
            if prim_metadata.domain:
                if prim_metadata.domain not in self._domain_index:
                    self._domain_index[prim_metadata.domain] = set()
                self._domain_index[prim_metadata.domain].add(prim_name)
            
            # Update capability index
            for capability in prim_metadata.capabilities:
                if capability not in self._capability_index:
                    self._capability_index[capability] = set()
                self._capability_index[capability].add(prim_name)
            
            # Update tag index
            for tag in prim_metadata.tags:
                if tag not in self._tag_index:
                    self._tag_index[tag] = set()
                self._tag_index[tag].add(prim_name)
    
    def get_namespace_primitives(self, namespace: Optional[str]) -> List[PrimitiveMetadata]:
        with self._lock:
            cur_namespace = self._namespaces
            if namespace:
                namespace = [n for n in namespace.split(".") if len(n) != 0]
                for seg in namespace:
                    if seg not in cur_namespace:
                        raise ValueError(f"Undefined namespace {seg}")
                    cur_namespace = cur_namespace[seg]
            out = []
            for (k, v) in cur_namespace.items():
                if not isinstance(v, dict):
                    out.append(v)
            return out

    def get(self, name: str) -> Optional[List[PrimitiveMetadata]]:
        """
        Get all registered primitives with given name.
        
        Args:
            name: Primitive name
        
        Returns:
            List of PrimitiveMetadata, or None if not found
        """
        with self._lock:
            return self._primitives.get(name)
    
    def get_bound_implementations(
        self,
        core_primitive: str,
        context: Optional[ExecutionContext] = None
    ) -> List[PrimitiveMetadata]:
        """
        Get all implementations bound to a core primitive.
        
        Args:
            core_primitive: Core primitive name (e.g., "think", "perceive")
            context: Optional execution context for filtering
        
        Returns:
            List of bound implementations, filtered by context if provided
        """
        with self._lock:
            implementations = self._bindings.get(core_primitive, [])
            
            if context:
                # Filter by domain
                if context.domain:
                    implementations = [
                        impl for impl in implementations
                        if not impl.domain or impl.domain == context.domain
                    ]
                
                # Filter by capabilities
                if context.capabilities:
                    implementations = [
                        impl for impl in implementations
                        if any(cap in impl.capabilities for cap in context.capabilities)
                        or not impl.capabilities  # Include generic implementations
                    ]
            
            return implementations
    
    def discover_by_domain(self, domain: str) -> List[PrimitiveMetadata]:
        """
        Discover primitives by domain.
        
        Args:
            domain: Domain name (e.g., "medical", "legal", "finance")
        
        Returns:
            List of primitives for this domain
        """
        with self._lock:
            primitive_names = self._domain_index.get(domain, set())
            results = []
            for name in primitive_names:
                results.extend(self._primitives[name])
            return results
    
    def discover_by_capability(self, capability: str) -> List[PrimitiveMetadata]:
        """
        Discover primitives by capability.
        
        Args:
            capability: Capability name
        
        Returns:
            List of primitives with this capability
        """
        with self._lock:
            primitive_names = self._capability_index.get(capability, set())
            results = []
            for name in primitive_names:
                results.extend(self._primitives[name])
            return results
    
    def discover_by_tags(self, tags: List[str]) -> List[PrimitiveMetadata]:
        """
        Discover primitives by tags.
        
        Args:
            tags: List of tags
        
        Returns:
            List of primitives matching any tag
        """
        with self._lock:
            primitive_names = set()
            for tag in tags:
                primitive_names.update(self._tag_index.get(tag, set()))
            
            results = []
            for name in primitive_names:
                results.extend(self._primitives[name])
            return results
    
    def list_all(self) -> Dict[str, List[PrimitiveMetadata]]:
        """
        List all registered primitives.
        
        Returns:
            Dictionary mapping primitive names to metadata lists
        """
        with self._lock:
            return self._primitives.copy()
    
    def clear(self) -> None:
        """Clear all registrations (primarily for testing)."""
        with self._lock:
            self._namespaces.clear()
            self._primitives.clear()
            self._bindings.clear()
            self._domain_index.clear()
            self._capability_index.clear()
            self._tag_index.clear()


# Global registry singleton
_global_registry: Optional[PrimitiveRegistry] = None
_registry_lock = threading.Lock()


def get_global_registry() -> PrimitiveRegistry:
    """
    Get the global primitive registry.
    
    Returns:
        Singleton PrimitiveRegistry instance
    """
    global _global_registry
    
    if _global_registry is None:
        with _registry_lock:
            if _global_registry is None:
                _global_registry = PrimitiveRegistry()
    
    return _global_registry


@dataclass
class PoKProgram:
    """Program-as-Knowledge: Reusable cognitive program."""
    
    name: str
    program: Callable
    description: str
    domain: Optional[str] = None
    input_spec: Dict[str, Any] = field(default_factory=dict)
    output_spec: Dict[str, Any] = field(default_factory=dict)
    version: str = "1.0.0"
    author: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class PoKLibrary:
    """
    Program-as-Knowledge Library.
    
    A PoK library packages domain expertise as executable programs,
    enabling knowledge portability and reuse.
    """
    
    def __init__(
        self,
        name: str,
        domain: str,
        version: str = "1.0.0",
        description: str = ""
    ):
        """
        Initialize PoK library.
        
        Args:
            name: Library name
            domain: Domain specialization
            version: Version string
            description: Library description
        """
        self.name = name
        self.domain = domain
        self.version = version
        self.description = description
        self._programs: Dict[str, PoKProgram] = {}
        self._lock = threading.RLock()
    
    def register_program(
        self,
        name: str,
        program: Callable,
        description: str,
        **metadata
    ) -> None:
        """
        Register a program in the library.
        
        Args:
            name: Program name
            program: Callable program implementation
            description: Program description
            **metadata: Additional metadata
        """
        with self._lock:
            pok_program = PoKProgram(
                name=name,
                program=program,
                description=description,
                domain=self.domain,
                version=metadata.get('version', '1.0.0'),
                author=metadata.get('author'),
                input_spec=metadata.get('input_spec', {}),
                output_spec=metadata.get('output_spec', {}),
                metadata=metadata,
            )
            self._programs[name] = pok_program
    
    def get_program(self, name: str) -> Optional[PoKProgram]:
        """
        Get a program by name.
        
        Args:
            name: Program name
        
        Returns:
            PoKProgram if found, None otherwise
        """
        with self._lock:
            return self._programs.get(name)
    
    def list_programs(self) -> List[PoKProgram]:
        """
        List all programs in library.
        
        Returns:
            List of PoKProgram instances
        """
        with self._lock:
            return list(self._programs.values())


class PoKLibraryRegistry:
    """Registry for PoK libraries."""
    
    def __init__(self):
        """Initialize empty registry."""
        self._libraries: Dict[str, PoKLibrary] = {}
        self._domain_index: Dict[str, List[str]] = {}
        self._lock = threading.RLock()
    
    def register(self, library: PoKLibrary) -> None:
        """
        Register a PoK library.
        
        Args:
            library: PoKLibrary instance
        """
        with self._lock:
            self._libraries[library.name] = library
            
            # Update domain index
            if library.domain not in self._domain_index:
                self._domain_index[library.domain] = []
            self._domain_index[library.domain].append(library.name)
    
    def get(self, name: str) -> Optional[PoKLibrary]:
        """
        Get library by name.
        
        Args:
            name: Library name
        
        Returns:
            PoKLibrary if found, None otherwise
        """
        with self._lock:
            return self._libraries.get(name)
    
    def discover_by_domain(self, domain: str) -> List[PoKLibrary]:
        """
        Discover libraries by domain.
        
        Args:
            domain: Domain name
        
        Returns:
            List of libraries for this domain
        """
        with self._lock:
            library_names = self._domain_index.get(domain, [])
            return [self._libraries[name] for name in library_names]
    
    def list_all(self) -> List[PoKLibrary]:
        """
        List all registered libraries.
        
        Returns:
            List of all PoKLibrary instances
        """
        with self._lock:
            return list(self._libraries.values())


# Global PoK library registry singleton
_pok_library_registry: Optional[PoKLibraryRegistry] = None
_pok_registry_lock = threading.Lock()


def get_pok_library_registry() -> PoKLibraryRegistry:
    """
    Get the global PoK library registry.
    
    Returns:
        Singleton PoKLibraryRegistry instance
    """
    global _pok_library_registry
    
    if _pok_library_registry is None:
        with _pok_registry_lock:
            if _pok_library_registry is None:
                _pok_library_registry = PoKLibraryRegistry()
    
    return _pok_library_registry
