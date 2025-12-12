"""
Plugin registry for managing loaded plugins.
"""

from typing import Dict, List, Optional, Type
from brainary.plugin.base import Plugin, PluginMetadata
from brainary.primitive.base import Primitive
from brainary.primitive.registry import PrimitiveRegistry, get_global_registry


class PluginRegistry:
    """
    Registry for managing Brainary plugins.
    
    Handles plugin registration, primitive overrides, and lifecycle management.
    """
    
    def __init__(self, primitive_registry: Optional[PrimitiveRegistry] = None):
        """
        Initialize plugin registry.
        
        Args:
            primitive_registry: Primitive registry to use for registering primitives.
                              If None, uses global registry.
        """
        self._plugins: Dict[str, Plugin] = {}
        self._primitive_overrides: Dict[str, List[str]] = {}  # primitive_name -> [plugin_names]
        self._primitive_registry = primitive_registry or get_global_registry()
    
    def register(self, plugin: Plugin) -> None:
        """
        Register a plugin.
        
        Args:
            plugin: Plugin instance to register
            
        Raises:
            ValueError: If plugin with same name already registered
        """
        metadata = plugin.metadata
        
        if metadata.name in self._plugins:
            raise ValueError(f"Plugin '{metadata.name}' already registered")
        
        # Check dependencies
        for dep in metadata.depends_on:
            if dep not in self._plugins:
                raise ValueError(f"Plugin '{metadata.name}' depends on '{dep}' which is not loaded")
        
        # Register primitives
        primitives = plugin.get_primitives()
        for prim_name, prim_class in primitives.items():
            # Track if this is an override
            # Check if primitive already exists in registry
            if prim_name in self._primitive_registry._primitives:
                if prim_name not in self._primitive_overrides:
                    self._primitive_overrides[prim_name] = []
                self._primitive_overrides[prim_name].append(metadata.name)
            
            # Instantiate and register the primitive
            prim_instance = prim_class()
            self._primitive_registry.register(prim_instance)
        
        # Store plugin
        self._plugins[metadata.name] = plugin
        
        # Call lifecycle hook
        plugin.on_load()
    
    def unregister(self, plugin_name: str) -> None:
        """
        Unregister a plugin.
        
        Args:
            plugin_name: Name of plugin to unregister
            
        Raises:
            KeyError: If plugin not found
        """
        if plugin_name not in self._plugins:
            raise KeyError(f"Plugin '{plugin_name}' not found")
        
        plugin = self._plugins[plugin_name]
        
        # Call lifecycle hook
        plugin.on_unload()
        
        # TODO: Unregister primitives (need to restore previous implementations)
        # For now, we don't support unregistering primitives
        
        # Remove from registry
        del self._plugins[plugin_name]
    
    def get(self, plugin_name: str) -> Optional[Plugin]:
        """Get a registered plugin by name."""
        return self._plugins.get(plugin_name)
    
    def list(self) -> List[PluginMetadata]:
        """List all registered plugins."""
        return [plugin.metadata for plugin in self._plugins.values()]
    
    def has(self, plugin_name: str) -> bool:
        """Check if a plugin is registered."""
        return plugin_name in self._plugins
    
    def get_overrides(self, primitive_name: str) -> List[str]:
        """
        Get list of plugins that override a primitive.
        
        Args:
            primitive_name: Name of primitive
            
        Returns:
            List of plugin names that override this primitive
        """
        return self._primitive_overrides.get(primitive_name, [])
    
    @classmethod
    def get_global(cls) -> 'PluginRegistry':
        """Get the global plugin registry instance."""
        if not hasattr(cls, '_global_instance'):
            cls._global_instance = cls()
        return cls._global_instance
