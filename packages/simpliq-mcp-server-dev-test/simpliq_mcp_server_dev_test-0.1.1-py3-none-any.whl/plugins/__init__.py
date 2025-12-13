# -*- coding: utf-8 -*-
"""
SimpliQ MCP Server - Plugin System

This package contains the plugin infrastructure for extending SimpliQ MCP Server
with ERP-specific functionality without coupling to the core server.

Author: Claude AI (Anthropic)
Date: 2025-11-18
"""

from .base import IMCPPlugin
from .registry import MCPPluginRegistry

__all__ = ['IMCPPlugin', 'MCPPluginRegistry']
