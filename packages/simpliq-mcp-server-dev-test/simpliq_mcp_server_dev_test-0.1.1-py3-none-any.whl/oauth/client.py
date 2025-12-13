"""
OAuth 2.0 Client for MCP Server

This module provides an HTTP client to interact with the User Manager OAuth API.
"""

import httpx
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class OAuthClient:
    """
    OAuth 2.0 HTTP Client for communicating with User Manager API.

    This client handles:
    - Token validation requests
    - Token introspection
    - Token refresh
    - Communication with OAuth endpoints
    """

    def __init__(self, provider_url: str, timeout: int = 10):
        """
        Initialize OAuth client.

        Args:
            provider_url: Base URL of User Manager API (e.g., http://localhost:8002)
            timeout: Request timeout in seconds
        """
        self.provider_url = provider_url.rstrip("/")
        self.timeout = timeout
        self.client = httpx.Client(timeout=timeout)

        logger.info(f"OAuthClient initialized with provider: {self.provider_url}")

    def validate_token(self, access_token: str) -> Optional[Dict[str, Any]]:
        """
        Validate an OAuth access token by calling the userinfo endpoint.

        Args:
            access_token: The JWT access token to validate

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
        try:
            url = f"{self.provider_url}/oauth/userinfo"
            headers = {"Authorization": f"Bearer {access_token}"}

            logger.debug(f"Validating token at: {url}")
            logger.info(f"[DEBUG] Sending token to User Manager: {access_token[:50]}... (length: {len(access_token)})")

            response = self.client.get(url, headers=headers)

            logger.info(f"[DEBUG] User Manager response: status={response.status_code}, body={response.text[:200]}")

            if response.status_code == 200:
                user_info = response.json()
                logger.info(f"Token validated successfully for user: {user_info.get('sub')}")
                return user_info
            elif response.status_code == 401:
                logger.warning("Token validation failed: Unauthorized")
                return None
            else:
                logger.error(f"Token validation failed: HTTP {response.status_code}")
                return None

        except httpx.RequestError as e:
            logger.error(f"Token validation request failed: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error validating token: {e}")
            return None

    def introspect_token(self, token: str, token_type_hint: str = "access_token") -> Optional[Dict[str, Any]]:
        """
        Introspect a token using OAuth 2.0 Token Introspection (RFC 7662).

        Note: This requires the User Manager to implement the introspection endpoint.
        For Phase 2, we'll use the userinfo endpoint instead.

        Args:
            token: The token to introspect
            token_type_hint: Type of token (access_token or refresh_token)

        Returns:
            Introspection response if successful, None otherwise
        """
        try:
            url = f"{self.provider_url}/oauth/introspect"
            data = {
                "token": token,
                "token_type_hint": token_type_hint
            }

            logger.debug(f"Introspecting token at: {url}")

            response = self.client.post(url, data=data)

            if response.status_code == 200:
                introspection = response.json()
                logger.info(f"Token introspected: active={introspection.get('active')}")
                return introspection
            else:
                logger.error(f"Token introspection failed: HTTP {response.status_code}")
                return None

        except httpx.RequestError as e:
            logger.error(f"Token introspection request failed: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error introspecting token: {e}")
            return None

    def refresh_access_token(self, refresh_token: str, client_id: str, client_secret: str) -> Optional[Dict[str, Any]]:
        """
        Refresh an access token using a refresh token.

        Args:
            refresh_token: The refresh token
            client_id: OAuth client ID
            client_secret: OAuth client secret

        Returns:
            New token response if successful, None otherwise

        Example return:
            {
                "access_token": "eyJhbGc...",
                "token_type": "Bearer",
                "expires_in": 3600,
                "refresh_token": "new_refresh_token",
                "scope": "read:connections write:connections"
            }
        """
        try:
            url = f"{self.provider_url}/oauth/token"
            data = {
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": client_id,
                "client_secret": client_secret
            }

            logger.debug(f"Refreshing token at: {url}")

            response = self.client.post(url, data=data)

            if response.status_code == 200:
                token_response = response.json()
                logger.info("Access token refreshed successfully")
                return token_response
            else:
                logger.error(f"Token refresh failed: HTTP {response.status_code}")
                return None

        except httpx.RequestError as e:
            logger.error(f"Token refresh request failed: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error refreshing token: {e}")
            return None

    def revoke_token(self, token: str, token_type_hint: str = "access_token") -> bool:
        """
        Revoke an OAuth token.

        Args:
            token: The token to revoke
            token_type_hint: Type of token (access_token or refresh_token)

        Returns:
            True if revoked successfully, False otherwise
        """
        try:
            url = f"{self.provider_url}/oauth/revoke"
            data = {
                "token": token,
                "token_type_hint": token_type_hint
            }

            logger.debug(f"Revoking token at: {url}")

            response = self.client.post(url, data=data)

            if response.status_code == 200:
                logger.info("Token revoked successfully")
                return True
            else:
                logger.error(f"Token revocation failed: HTTP {response.status_code}")
                return False

        except httpx.RequestError as e:
            logger.error(f"Token revocation request failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error revoking token: {e}")
            return False

    def close(self):
        """Close the HTTP client."""
        self.client.close()
        logger.debug("OAuthClient closed")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
