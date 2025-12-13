"""
OAuth 2.0 Middleware for MCP Server

This middleware validates OAuth tokens in MCP requests and propagates
user context to MCP tools.
"""

import logging
import time
from typing import Optional, Dict, Any, Callable
from functools import wraps
from datetime import datetime, timedelta
from flask import request, g, jsonify

from .client import OAuthClient

logger = logging.getLogger(__name__)


class OAuthMiddleware:
    """
    OAuth 2.0 Middleware for validating tokens in MCP requests.

    Features:
    - Validates Bearer tokens from Authorization header
    - Caches validated tokens (configurable TTL)
    - Propagates user context to request handlers
    - Handles token expiration and refresh
    """

    def __init__(self, provider_url: str, cache_ttl: int = 300, enabled: bool = True):
        """
        Initialize OAuth middleware.

        Args:
            provider_url: Base URL of OAuth provider (User Manager API)
            cache_ttl: Cache time-to-live in seconds (default: 5 minutes)
            enabled: Whether OAuth validation is enabled
        """
        self.provider_url = provider_url
        self.cache_ttl = cache_ttl
        self.enabled = enabled
        self.oauth_client = OAuthClient(provider_url)

        # Token cache: {token: (user_info, expiry_time)}
        self.token_cache: Dict[str, tuple[Dict[str, Any], float]] = {}

        logger.info(
            f"OAuthMiddleware initialized: enabled={enabled}, "
            f"provider={provider_url}, cache_ttl={cache_ttl}s"
        )

    def extract_token_from_request(self, flask_request=None) -> Optional[str]:
        """
        Extract Bearer token from request Authorization header.

        Args:
            flask_request: Flask request object (uses global request if None)

        Returns:
            Access token string if found, None otherwise

        Example:
            Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
        """
        if flask_request is None:
            flask_request = request

        auth_header = flask_request.headers.get("Authorization", "")

        if not auth_header:
            logger.debug("No Authorization header found")
            return None

        # Parse "Bearer <token>"
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            logger.warning(f"Invalid Authorization header format: {auth_header[:20]}...")
            return None

        token = parts[1]
        logger.debug(f"Extracted Bearer token: {token[:20]}...")
        return token

    def validate_token(self, access_token: str, use_cache: bool = True) -> Optional[Dict[str, Any]]:
        """
        Validate an OAuth access token.

        Args:
            access_token: JWT access token
            use_cache: Whether to use cached validation results

        Returns:
            User information dict if valid, None if invalid

        Example return:
            {
                "sub": "user-123",
                "client_id": "client-456",
                "org_id": "org-789",
                "scope": "read:connections write:connections",
                "exp": 1234567890,
                "iat": 1234564290
            }
        """
        # Check cache first
        if use_cache and access_token in self.token_cache:
            user_info, expiry_time = self.token_cache[access_token]

            # Check if cache entry is still valid
            if time.time() < expiry_time:
                logger.debug(f"Token found in cache (valid for {expiry_time - time.time():.0f}s)")
                return user_info
            else:
                # Cache expired, remove entry
                logger.debug("Cached token expired, removing from cache")
                del self.token_cache[access_token]

        # Validate token via OAuth provider
        logger.debug("Validating token with OAuth provider")
        user_info = self.oauth_client.validate_token(access_token)

        if user_info is None:
            logger.warning("Token validation failed")
            return None

        # Cache the validated token
        expiry_time = time.time() + self.cache_ttl
        self.token_cache[access_token] = (user_info, expiry_time)
        logger.info(f"Token validated and cached for user: {user_info.get('sub')}")

        return user_info

    def validate_request(self, flask_request=None) -> tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
        """
        Validate OAuth token in a Flask request.

        Args:
            flask_request: Flask request object (uses global request if None)

        Returns:
            Tuple of (is_valid, user_info, error_message)

        Example:
            is_valid, user_info, error = middleware.validate_request()
            if not is_valid:
                return jsonify({"error": error}), 401
        """
        if not self.enabled:
            logger.debug("OAuth validation is disabled")
            return True, {"sub": "anonymous", "scope": "all"}, None

        # Extract token
        access_token = self.extract_token_from_request(flask_request)
        if not access_token:
            logger.warning("[DEBUG] No token extracted from request!")
            return False, None, "Missing or invalid Authorization header"

        logger.info(f"[DEBUG] Extracted token from request: {access_token[:50]}... (length: {len(access_token)})")

        # Validate token
        user_info = self.validate_token(access_token)
        if not user_info:
            return False, None, "Invalid or expired access token"

        return True, user_info, None

    def require_oauth(self, func: Callable) -> Callable:
        """
        Decorator to require OAuth authentication on a Flask route.

        Usage:
            @app.route("/protected")
            @oauth_middleware.require_oauth
            def protected_route():
                user_id = g.oauth_user_id
                return f"Hello {user_id}"

        The decorator adds the following to Flask's g object:
            - g.oauth_user_id: User ID from token
            - g.oauth_client_id: Client ID from token
            - g.oauth_org_id: Organization ID from token
            - g.oauth_scope: Space-separated scopes
            - g.oauth_user_info: Full user info dict
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not self.enabled:
                # OAuth disabled, skip validation
                g.oauth_user_id = "anonymous"
                g.oauth_client_id = "anonymous"
                g.oauth_org_id = None
                g.oauth_scope = "all"
                g.oauth_user_info = {"sub": "anonymous"}
                return func(*args, **kwargs)

            # Validate request
            is_valid, user_info, error = self.validate_request()

            if not is_valid:
                logger.warning(f"OAuth validation failed: {error}")
                return jsonify({
                    "error": "unauthorized",
                    "error_description": error
                }), 401

            # Propagate user context to Flask g
            g.oauth_user_id = user_info.get("sub")
            g.oauth_client_id = user_info.get("client_id")
            g.oauth_org_id = user_info.get("org_id")
            g.oauth_scope = user_info.get("scope", "")
            g.oauth_user_info = user_info

            logger.debug(f"OAuth context set: user={g.oauth_user_id}, org={g.oauth_org_id}")

            return func(*args, **kwargs)

        return wrapper

    def clear_cache(self):
        """Clear all cached tokens."""
        count = len(self.token_cache)
        self.token_cache.clear()
        logger.info(f"Token cache cleared: {count} entries removed")

    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dict with cache size and valid entries count
        """
        now = time.time()
        valid_count = sum(1 for _, expiry in self.token_cache.values() if expiry > now)

        return {
            "total_entries": len(self.token_cache),
            "valid_entries": valid_count,
            "expired_entries": len(self.token_cache) - valid_count,
            "cache_ttl": self.cache_ttl
        }

    def cleanup_expired_cache(self):
        """Remove expired tokens from cache."""
        now = time.time()
        expired_tokens = [
            token for token, (_, expiry) in self.token_cache.items()
            if expiry <= now
        ]

        for token in expired_tokens:
            del self.token_cache[token]

        if expired_tokens:
            logger.info(f"Cleaned up {len(expired_tokens)} expired cache entries")

    def close(self):
        """Close OAuth client and cleanup resources."""
        self.oauth_client.close()
        self.clear_cache()
        logger.info("OAuthMiddleware closed")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


def create_oauth_context(user_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create OAuth context dict from user info for MCP tools.

    Args:
        user_info: User info from validated token

    Returns:
        Context dict suitable for MCP tool execution

    Example:
        context = create_oauth_context(user_info)
        result = execute_tool(tool_name, arguments, context)
    """
    return {
        "oauth": {
            "user_id": user_info.get("sub"),
            "client_id": user_info.get("client_id"),
            "organization_id": user_info.get("org_id"),
            "scope": user_info.get("scope", ""),
            "scopes": user_info.get("scope", "").split(),
            "authenticated": True,
            "token_exp": user_info.get("exp"),
            "token_iat": user_info.get("iat")
        }
    }


def check_scope(required_scope: str, user_info: Dict[str, Any]) -> bool:
    """
    Check if user has a required scope.

    Args:
        required_scope: Scope to check (e.g., "read:connections")
        user_info: User info from validated token

    Returns:
        True if user has the scope, False otherwise
    """
    user_scopes = user_info.get("scope", "").split()
    return required_scope in user_scopes
