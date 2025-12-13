"""
SimpliQ MCP Server - OAuth 2.0 Client Module

This module implements OAuth 2.0 client functionality for the SimpliQ MCP Server,
allowing it to validate and use OAuth tokens from the User Manager API.

Phase 2 of OAuth 2.0 Implementation.
"""

__version__ = "1.0.0"

from .middleware import OAuthMiddleware
from .client import OAuthClient

__all__ = ["OAuthMiddleware", "OAuthClient"]
