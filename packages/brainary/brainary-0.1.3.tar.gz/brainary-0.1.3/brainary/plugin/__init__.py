"""
Plugin system for domain-specific primitive libraries.

Enables extending Brainary with specialized cognitive primitives
for specific domains like security analysis, code generation, etc.
"""

from .base import Plugin, PluginMetadata
from .loader import PluginLoader, load_plugin, list_plugins
from .registry import PluginRegistry

__all__ = [
    'Plugin',
    'PluginMetadata',
    'PluginLoader',
    'PluginRegistry',
    'load_plugin',
    'list_plugins',
]
