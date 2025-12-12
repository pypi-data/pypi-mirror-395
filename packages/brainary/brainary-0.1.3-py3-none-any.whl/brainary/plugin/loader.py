"""
Plugin loader for discovering and loading plugins.
"""

import importlib
import importlib.util
import sys
from pathlib import Path
from typing import List, Optional, Dict, Any

from brainary.plugin.base import Plugin
from brainary.plugin.registry import PluginRegistry


class PluginLoader:
    """
    Loader for discovering and loading Brainary plugins.
    
    Supports loading plugins from:
    - TPL (third-party libraries) directory
    - Python packages
    - Specific paths
    """
    
    def __init__(self, registry: Optional[PluginRegistry] = None):
        """
        Initialize plugin loader.
        
        Args:
            registry: Plugin registry to register loaded plugins.
                     If None, uses global registry.
        """
        self._registry = registry or PluginRegistry.get_global()
        self._tpl_path: Optional[Path] = None
    
    def set_tpl_path(self, path: Path) -> None:
        """
        Set the TPL (third-party libraries) directory path.
        
        Args:
            path: Path to TPL directory
        """
        self._tpl_path = Path(path)
        if not self._tpl_path.exists():
            raise FileNotFoundError(f"TPL path not found: {path}")
    
    def discover_tpl_plugins(self) -> List[str]:
        """
        Discover available plugins in TPL directory.
        
        Returns:
            List of plugin names found in TPL directory
        """
        if not self._tpl_path:
            return []
        
        plugins = []
        for item in self._tpl_path.iterdir():
            if item.is_dir() and not item.name.startswith('_'):
                # Check if it has a plugin.py or __init__.py
                if (item / 'plugin.py').exists() or (item / '__init__.py').exists():
                    plugins.append(item.name)
        
        return plugins
    
    def load_from_tpl(self, plugin_name: str, config: Optional[Dict[str, Any]] = None) -> Plugin:
        """
        Load a plugin from TPL directory.
        
        Args:
            plugin_name: Name of the plugin (directory name in TPL)
            config: Optional configuration for the plugin
            
        Returns:
            Loaded Plugin instance
            
        Raises:
            FileNotFoundError: If plugin not found
            ImportError: If plugin module cannot be imported
            ValueError: If plugin class not found or invalid
        """
        if not self._tpl_path:
            raise ValueError("TPL path not set. Call set_tpl_path() first.")
        
        plugin_path = self._tpl_path / plugin_name
        if not plugin_path.exists():
            raise FileNotFoundError(f"Plugin '{plugin_name}' not found in TPL directory")
        
        # Add TPL to sys.path if not already there
        tpl_str = str(self._tpl_path)
        if tpl_str not in sys.path:
            sys.path.insert(0, tpl_str)
        
        try:
            # Try to import plugin module
            plugin_module_name = f"{plugin_name}.plugin"
            try:
                plugin_module = importlib.import_module(plugin_module_name)
            except ImportError:
                # Try direct import if plugin.py doesn't exist
                plugin_module = importlib.import_module(plugin_name)
            
            # Find Plugin class
            plugin_class = None
            for attr_name in dir(plugin_module):
                attr = getattr(plugin_module, attr_name)
                if (isinstance(attr, type) and 
                    issubclass(attr, Plugin) and 
                    attr is not Plugin):
                    plugin_class = attr
                    break
            
            if not plugin_class:
                raise ValueError(f"No Plugin class found in {plugin_name}")
            
            # Instantiate plugin
            plugin = plugin_class()
            
            # Configure if config provided
            if config:
                plugin.configure(config)
            
            # Register plugin
            self._registry.register(plugin)
            
            return plugin
            
        except Exception as e:
            raise ImportError(f"Failed to load plugin '{plugin_name}': {e}") from e
    
    def load_from_module(self, module_path: str, config: Optional[Dict[str, Any]] = None) -> Plugin:
        """
        Load a plugin from a Python module path.
        
        Args:
            module_path: Full module path (e.g., 'my_package.my_plugin')
            config: Optional configuration for the plugin
            
        Returns:
            Loaded Plugin instance
        """
        try:
            plugin_module = importlib.import_module(module_path)
            
            # Find Plugin class
            plugin_class = None
            for attr_name in dir(plugin_module):
                attr = getattr(plugin_module, attr_name)
                if (isinstance(attr, type) and 
                    issubclass(attr, Plugin) and 
                    attr is not Plugin):
                    plugin_class = attr
                    break
            
            if not plugin_class:
                raise ValueError(f"No Plugin class found in {module_path}")
            
            # Instantiate plugin
            plugin = plugin_class()
            
            # Configure if config provided
            if config:
                plugin.configure(config)
            
            # Register plugin
            self._registry.register(plugin)
            
            return plugin
            
        except Exception as e:
            raise ImportError(f"Failed to load plugin from '{module_path}': {e}") from e


# Global loader instance
_global_loader: Optional[PluginLoader] = None


def get_global_loader() -> PluginLoader:
    """Get the global plugin loader instance."""
    global _global_loader
    if _global_loader is None:
        _global_loader = PluginLoader()
    return _global_loader


def load_plugin(plugin_name: str, 
                from_tpl: bool = True,
                config: Optional[Dict[str, Any]] = None,
                tpl_path: Optional[Path] = None) -> Plugin:
    """
    Convenience function to load a plugin.
    
    Args:
        plugin_name: Name of plugin (directory in TPL) or module path
        from_tpl: If True, load from TPL directory; else treat as module path
        config: Optional plugin configuration
        tpl_path: Optional TPL path (if not set globally)
        
    Returns:
        Loaded Plugin instance
    """
    loader = get_global_loader()
    
    if from_tpl:
        if tpl_path:
            loader.set_tpl_path(tpl_path)
        return loader.load_from_tpl(plugin_name, config)
    else:
        return loader.load_from_module(plugin_name, config)


def list_plugins(tpl_path: Optional[Path] = None) -> List[str]:
    """
    List available plugins in TPL directory.
    
    Args:
        tpl_path: Optional TPL path (if not set globally)
        
    Returns:
        List of available plugin names
    """
    loader = get_global_loader()
    
    if tpl_path:
        loader.set_tpl_path(tpl_path)
    
    return loader.discover_tpl_plugins()
