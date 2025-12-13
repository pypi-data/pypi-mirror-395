# -*- coding: utf-8 -*-
"""
SimpliQ MCP Server - Plugin Registry

Manages registration and lifecycle of MCP plugins.

Author: Claude AI (Anthropic)
Date: 2025-11-18
"""

from typing import Dict, Any, Optional, List
import logging

from .base import IMCPPlugin


logger = logging.getLogger(__name__)


class MCPPluginRegistry:
    """
    Registry for managing MCP plugins.

    The registry maintains a collection of plugins and provides methods
    for registering, initializing, and using plugins.

    Example:
        registry = MCPPluginRegistry()

        # Register a plugin
        registry.register_plugin('protheus', ProtheusMapperPlugin())

        # Initialize all plugins
        registry.initialize_all(db_connection, semantic_catalog)

        # Get all tools from all plugins
        tools = registry.get_all_tools()

        # Handle a tool call
        result = registry.handle_tool_call('protheus_tool', {'param': 'value'})
    """

    def __init__(self):
        """Initialize the plugin registry."""
        self.plugins: Dict[str, IMCPPlugin] = {}
        self.tools: Dict[str, str] = {}  # tool_name -> plugin_name mapping
        self._initialized = False

    def register_plugin(self, name: str, plugin: IMCPPlugin) -> None:
        """
        Register a plugin with the registry.

        Args:
            name: Unique name for the plugin
            plugin: Plugin instance implementing IMCPPlugin

        Raises:
            ValueError: If a plugin with the same name is already registered
        """
        if name in self.plugins:
            logger.warning(f"Plugin '{name}' is already registered. Skipping.")
            return

        self.plugins[name] = plugin
        logger.info(f"Registered plugin: {name}")

        # If registry is already initialized, initialize this plugin now
        if self._initialized and hasattr(self, '_connection') and hasattr(self, '_catalog'):
            try:
                plugin.initialize(self._connection, self._catalog)
                self._register_plugin_tools(name, plugin)
                logger.info(f"Plugin '{name}' initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize plugin '{name}': {e}")

    def initialize_all(self, connection: Any, semantic_catalog: Any) -> None:
        """
        Initialize all registered plugins.

        This should be called once when the MCP server starts, after the
        database connection and semantic catalog are available.

        Args:
            connection: Database connection object
            semantic_catalog: SemanticCatalog instance
        """
        self._connection = connection
        self._catalog = semantic_catalog
        self._initialized = True

        logger.info(f"Initializing {len(self.plugins)} plugin(s)...")

        for name, plugin in self.plugins.items():
            try:
                plugin.initialize(connection, semantic_catalog)
                self._register_plugin_tools(name, plugin)
                logger.info(f"Plugin '{name}' initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize plugin '{name}': {e}")

    def _register_plugin_tools(self, plugin_name: str, plugin: IMCPPlugin) -> None:
        """
        Register tools provided by a plugin.

        Args:
            plugin_name: Name of the plugin
            plugin: Plugin instance
        """
        try:
            plugin_tools = plugin.get_tools()
            for tool_name in plugin_tools.keys():
                if tool_name in self.tools:
                    logger.warning(
                        f"Tool '{tool_name}' from plugin '{plugin_name}' "
                        f"conflicts with plugin '{self.tools[tool_name]}'. Skipping."
                    )
                    continue
                self.tools[tool_name] = plugin_name
                logger.debug(f"Registered tool '{tool_name}' from plugin '{plugin_name}'")
        except Exception as e:
            logger.error(f"Failed to register tools for plugin '{plugin_name}': {e}")

    def get_all_tools(self) -> Dict[str, Dict]:
        """
        Get all tools from all registered plugins.

        Returns:
            Dictionary mapping tool names to their definitions
        """
        all_tools = {}

        for plugin_name, plugin in self.plugins.items():
            try:
                plugin_tools = plugin.get_tools()
                all_tools.update(plugin_tools)
            except Exception as e:
                logger.error(f"Failed to get tools from plugin '{plugin_name}': {e}")

        return all_tools

    def handle_tool_call(self, tool_name: str, args: Dict) -> Optional[Dict]:
        """
        Route a tool call to the appropriate plugin.

        Args:
            tool_name: Name of the tool being called
            args: Dictionary of arguments

        Returns:
            Tool execution result, or None if no plugin handles this tool
        """
        # Find which plugin owns this tool
        plugin_name = self.tools.get(tool_name)
        if not plugin_name:
            return None

        plugin = self.plugins.get(plugin_name)
        if not plugin:
            logger.error(f"Plugin '{plugin_name}' not found for tool '{tool_name}'")
            return None

        try:
            return plugin.handle_tool_call(tool_name, args)
        except Exception as e:
            logger.error(f"Error calling tool '{tool_name}' in plugin '{plugin_name}': {e}")
            raise

    def get_plugin(self, name: str) -> Optional[IMCPPlugin]:
        """
        Get a plugin by name.

        Args:
            name: Plugin name

        Returns:
            Plugin instance, or None if not found
        """
        return self.plugins.get(name)

    def list_plugins(self) -> List[str]:
        """
        List all registered plugin names.

        Returns:
            List of plugin names
        """
        return list(self.plugins.keys())

    def unregister_plugin(self, name: str) -> bool:
        """
        Unregister a plugin.

        Args:
            name: Plugin name

        Returns:
            True if plugin was unregistered, False if not found
        """
        if name not in self.plugins:
            return False

        # Remove plugin's tools
        tools_to_remove = [tool for tool, plugin in self.tools.items() if plugin == name]
        for tool in tools_to_remove:
            del self.tools[tool]

        # Remove plugin
        del self.plugins[name]
        logger.info(f"Unregistered plugin: {name}")
        return True
