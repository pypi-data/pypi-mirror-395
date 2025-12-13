# -*- coding: utf-8 -*-
"""
SimpliQ MCP Server - Plugin Base Interface

Defines the base interface that all MCP plugins must implement.

Author: Claude AI (Anthropic)
Date: 2025-11-18
"""

from typing import Dict, Any, Protocol, Optional


class IMCPPlugin(Protocol):
    """
    Interface for MCP plugins.

    This protocol defines the contract that all MCP plugins must implement.
    Plugins can provide additional MCP tools and handle tool execution.

    Example:
        class MyPlugin:
            def initialize(self, connection, semantic_catalog):
                self.connection = connection
                self.catalog = semantic_catalog

            def get_tools(self):
                return {
                    "my_tool": {
                        "description": "My custom tool",
                        "inputSchema": {
                            "type": "object",
                            "properties": {...}
                        }
                    }
                }

            def handle_tool_call(self, tool_name, args):
                if tool_name == "my_tool":
                    return {"result": "success"}
                return None
    """

    def initialize(self, connection: Any, semantic_catalog: Any) -> None:
        """
        Initialize the plugin with database connection and semantic catalog.

        This method is called when the plugin is registered with the server.
        The plugin should store references to these objects for later use.

        Args:
            connection: Database connection object (e.g., psycopg2 connection)
            semantic_catalog: SemanticCatalog instance for accessing mappings
        """
        ...

    def get_tools(self) -> Dict[str, Dict]:
        """
        Return MCP tools provided by this plugin.

        Each tool is defined with:
        - description: Human-readable description
        - inputSchema: JSON Schema for tool parameters

        Returns:
            Dictionary mapping tool names to their definitions.
            Example:
            {
                "tool_name": {
                    "description": "Tool description",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "param1": {"type": "string", "description": "Param description"}
                        },
                        "required": ["param1"]
                    }
                }
            }
        """
        ...

    def handle_tool_call(self, tool_name: str, args: Dict) -> Optional[Dict]:
        """
        Handle execution of a tool call.

        This method is called when a tool provided by this plugin is invoked.
        The plugin should execute the requested operation and return the result.

        Args:
            tool_name: Name of the tool being called
            args: Dictionary of arguments passed to the tool

        Returns:
            Tool execution result as a dictionary, or None if the tool is not
            handled by this plugin. The result format should follow MCP conventions:
            {
                "content": [
                    {
                        "type": "text",
                        "text": "Result text or JSON string"
                    }
                ]
            }
        """
        ...
