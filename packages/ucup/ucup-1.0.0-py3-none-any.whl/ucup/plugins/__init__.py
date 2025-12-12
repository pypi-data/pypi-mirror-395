"""
UCUP Plugin System

This package contains example plugins and utilities for extending UCUP.
"""

from ..plugins import (
    PluginManager, PluginInterface, AgentPlugin, StrategyPlugin,
    MonitorPlugin, SerializerPlugin, PluginMetadata, PluginHook,
    get_plugin_manager, initialize_plugin_system
)

__version__ = "0.1.0"
__all__ = [
    'PluginManager',
    'PluginInterface',
    'AgentPlugin',
    'StrategyPlugin',
    'MonitorPlugin',
    'SerializerPlugin',
    'PluginMetadata',
    'PluginHook',
    'get_plugin_manager',
    'initialize_plugin_system'
]
