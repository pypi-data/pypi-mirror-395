"""
Base classes for Brainary plugins.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Type, Any
from brainary.primitive.base import Primitive


@dataclass
class PluginMetadata:
    """Metadata for a plugin."""
    
    name: str
    version: str
    description: str
    author: str
    domain: str
    
    # Dependencies
    requires_brainary: str = ">=0.1.0"
    depends_on: List[str] = field(default_factory=list)
    
    # Plugin capabilities
    provides_primitives: List[str] = field(default_factory=list)
    overrides_primitives: List[str] = field(default_factory=list)
    
    # Additional metadata
    tags: List[str] = field(default_factory=list)
    homepage: Optional[str] = None
    license: str = "MIT"


class Plugin(ABC):
    """
    Base class for Brainary plugins.
    
    A plugin can:
    1. Override existing primitives with domain-specific implementations
    2. Define new domain-specific primitives
    3. Provide domain-specific utilities and helpers
    
    Example:
        >>> class VulnDetectionPlugin(Plugin):
        ...     @property
        ...     def metadata(self):
        ...         return PluginMetadata(
        ...             name="vuln_detection",
        ...             version="1.0.0",
        ...             description="Vulnerability detection primitives",
        ...             author="Security Team",
        ...             domain="security"
        ...         )
        ...
        ...     def get_primitives(self):
        ...         return {
        ...             'detect_vuln': DetectVulnerabilityPrimitive,
        ...             'think': SecurityThinkPrimitive,  # Override
        ...         }
    """
    
    @property
    @abstractmethod
    def metadata(self) -> PluginMetadata:
        """Return plugin metadata."""
        pass
    
    @abstractmethod
    def get_primitives(self) -> Dict[str, Type[Primitive]]:
        """
        Return dictionary of primitive implementations.
        
        Returns:
            Dict mapping primitive names to Primitive classes
            
        Note:
            - New primitives will be registered
            - Primitives matching existing names will override them
        """
        pass
    
    def on_load(self) -> None:
        """
        Called when plugin is loaded.
        
        Use this for initialization, resource setup, etc.
        """
        pass
    
    def on_unload(self) -> None:
        """
        Called when plugin is unloaded.
        
        Use this for cleanup, resource release, etc.
        """
        pass
    
    def get_config_schema(self) -> Optional[Dict[str, Any]]:
        """
        Return configuration schema for the plugin.
        
        Returns:
            Dict describing configuration options, or None if no config needed
        """
        return None
    
    def configure(self, config: Dict[str, Any]) -> None:
        """
        Configure the plugin with user-provided settings.
        
        Args:
            config: Configuration dictionary
        """
        pass
