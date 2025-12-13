"""
User Manager API Client

HTTP client for communicating with the User Manager API.
This replaces direct database access for user and connection management.
"""

import requests
from typing import Dict, List, Optional, Tuple
import yaml
import logging

# Get logger for this module
logger = logging.getLogger(__name__)


class UserAPIClient:
    """HTTP client for User Manager API."""

    def __init__(self, config_file: str = "config.yml", oauth_client=None):
        """
        Initialize the API client.

        Args:
            config_file: Path to configuration file
            oauth_client: Optional OAuthClient instance for authentication
        """
        self.config_file = config_file
        self.base_url = None
        self.timeout = 30
        self.oauth_client = oauth_client
        self._load_config()

    def _load_config(self):
        """Load API configuration from YAML file."""
        try:
            with open(self.config_file, 'r') as f:
                config = yaml.safe_load(f)
                api_config = config.get('user_manager_api', {})
                # Default port updated to 8002 (FastAPI User Manager). If config missing, use 8002.
                self.base_url = api_config.get('base_url', 'http://127.0.0.1:8002')
                self.timeout = api_config.get('timeout', 30)
        except Exception as e:
            logger.warning(f"Could not load API config: {e}. Using defaults.")
            self.base_url = 'http://127.0.0.1:8002'
            self.timeout = 30

    def _make_request(self, method: str, endpoint: str, data: dict = None,
                     headers: dict = None, params: dict = None) -> Dict:
        """
        Make an HTTP request to the API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (e.g., '/users')
            data: Request body data
            headers: Request headers
            params: Query parameters

        Returns:
            Response JSON data

        Raises:
            Exception: If request fails
        """
        url = f"{self.base_url}{endpoint}"
        headers = headers or {}
        headers['Content-Type'] = 'application/json'

        # Add OAuth authentication if available
        if self.oauth_client:
            try:
                auth_headers = self.oauth_client.get_auth_headers()
                headers.update(auth_headers)
                logger.debug("Added OAuth Bearer token to request headers")
                # Log token for debugging (first 30 chars only)
                if 'Authorization' in auth_headers:
                    token_preview = auth_headers['Authorization'][:50] + '...' if len(auth_headers['Authorization']) > 50 else auth_headers['Authorization']
                    logger.debug(f"Authorization header: {token_preview}")
            except Exception as e:
                logger.warning(f"Failed to get OAuth token: {e}")
                # Continue without OAuth - let the API return 401 if needed

        # Log all headers (redact Authorization)
        headers_log = {k: (v[:50] + '...' if k == 'Authorization' and len(v) > 50 else v) for k, v in headers.items()}
        logger.debug(f"Making {method} request to {url}")
        logger.debug(f"Request headers: {headers_log}")
        logger.debug(f"Request data: {data}, params: {params}")

        try:
            response = requests.request(
                method=method,
                url=url,
                json=data,
                headers=headers,
                params=params,
                timeout=self.timeout
            )

            # Handle successful responses
            if response.status_code in [200, 201]:
                logger.debug(f"Request successful: {response.status_code}")
                return response.json()

            # Handle client errors (4xx)
            if 400 <= response.status_code < 500:
                try:
                    error_data = response.json()
                    error_msg = error_data.get('detail', f"API error: {response.status_code}")
                    logger.warning(f"API client error ({response.status_code}): {error_msg}")
                    logger.warning(f"Full error response: {error_data}")
                except:
                    error_msg = f"API error: {response.status_code} - {response.text}"
                    logger.warning(f"API client error: {error_msg}")
                raise Exception(error_msg)

            # Handle server errors (5xx)
            if response.status_code >= 500:
                logger.error(f"API server error: {response.status_code}")
                raise Exception(f"API server error: {response.status_code}")

            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect to User Manager API at {url}: {str(e)}")
            raise Exception(f"Failed to connect to User Manager API: {str(e)}")

    # ========================
    # User Management Methods
    # ========================

    def create_user(self, username: str, password: str, email: str,
                   full_name: str = "", role: str = None,
                   organization_id: str = None, auth_token: str = None) -> Tuple[bool, str, Dict]:
        """Create a new user.

        Args:
            username: Unique username
            password: User password
            email: User email address
            full_name: User's full name (optional)
            role: User role (common, org_admin, super_admin). Defaults to common.
            organization_id: Organization ID (UUID). If not specified, uses default organization.
            auth_token: JWT token for authenticated request (required to set custom role/org)

        Returns:
            Tuple of (success, message, user_data)
        """
        try:
            data = {
                "username": username,
                "password": password,
                "email": email,
                "full_name": full_name
            }

            # Add optional parameters if provided
            if role:
                data["role"] = role
            if organization_id:
                data["organization_id"] = organization_id

            # Use authentication if token provided
            headers = {}
            if auth_token:
                headers['Authorization'] = f'Bearer {auth_token}'

            result = self._make_request('POST', '/users', data=data, headers=headers)
            return True, f"User '{username}' created successfully with role '{result.get('role', 'common')}'", result
        except Exception as e:
            return False, str(e), {}

    def get_user(self, username: str, token: str) -> Optional[Dict]:
        """Get user information."""
        try:
            headers = {'Authorization': f'Bearer {token}'}
            result = self._make_request('GET', f'/users/{username}', headers=headers)
            return result
        except:
            return None

    def list_users(self) -> List[Dict]:
        """List all users."""
        try:
            result = self._make_request('GET', '/users')
            return result.get('users', [])
        except:
            return []

    def list_users_auth(self, token: str) -> List[Dict]:
        """List all users using authentication token (may include privileged users)."""
        if not token:
            return self.list_users()
        try:
            headers = {'Authorization': f'Bearer {token}'}
            result = self._make_request('GET', '/users', headers=headers)
            return result.get('users', [])
        except Exception as e:
            logger.debug(f"Authenticated list_users failed, falling back to unauthenticated list: {e}")
            return self.list_users()

    def update_user(self, username: str, token: str, email: str = None,
                   full_name: str = None, password: str = None,
                   role: str = None) -> Tuple[bool, str]:
        """Update user information.

        Args:
            username: Username to update
            token: Authentication token
            email: New email address (optional)
            full_name: New full name (optional)
            password: New password (optional)
            role: New role - common, org_admin, or super_admin (optional)

        Returns:
            Tuple of (success, message)
        """
        try:
            headers = {'Authorization': f'Bearer {token}'}
            data = {}
            if email is not None:
                data['email'] = email
            if full_name is not None:
                data['full_name'] = full_name
            if password is not None:
                data['password'] = password
            if role is not None:
                data['role'] = role

            result = self._make_request('PUT', f'/users/{username}', data=data, headers=headers)
            return True, result.get('message', 'User updated successfully')
        except Exception as e:
            return False, str(e)

    def delete_user(self, username: str, token: str) -> Tuple[bool, str]:
        """Delete a user."""
        try:
            headers = {'Authorization': f'Bearer {token}'}
            result = self._make_request('DELETE', f'/users/{username}', headers=headers)
            return True, result.get('message', 'User deleted successfully')
        except Exception as e:
            return False, str(e)

    # ========================
    # Authentication Methods
    # ========================

    def authenticate(self, username: str, password: str) -> Tuple[bool, str, Optional[str]]:
        """Authenticate a user and get JWT access token."""
        try:
            data = {
                "username": username,
                "password": password
            }
            result = self._make_request('POST', '/auth/login', data=data)
            # Try multiple possible token field names for backward compatibility
            token = (
                result.get('access_token') or
                result.get('token') or
                result.get('session_token')
            )
            # Debug log keys present to diagnose null token issues
            logger.debug(
                f"Authentication response keys: {list(result.keys())}. "
                f"Resolved token present={token is not None}"
            )
            if not token:
                logger.warning(
                    f"No token found in authentication response for user '{username}'. "
                    f"Expected one of ['access_token','token','session_token']."
                )
            else:
                logger.debug(f"Authentication successful for {username}, token length={len(token)}")
            return True, result.get('message', 'Authentication successful'), token
        except Exception as e:
            logger.error(f"Authentication failed for {username}: {str(e)}")
            return False, str(e), None

    def validate_session(self, session_token: str) -> Tuple[bool, Optional[str]]:
        """Validate a JWT access token (stored as session_token for compatibility)."""
        try:
            data = {"session_token": session_token}
            result = self._make_request('POST', '/auth/validate', data=data)
            valid = result.get('valid', False)
            username = result.get('username')
            logger.debug(f"Token validation: valid={valid}, username={username}")
            return valid, username
        except Exception as e:
            logger.warning(f"Token validation failed: {str(e)}")
            return False, None

    def logout(self, session_token: str) -> Tuple[bool, str]:
        """Logout a user."""
        try:
            headers = {'Authorization': f'Bearer {session_token}'}
            result = self._make_request('POST', '/auth/logout', headers=headers)
            return True, result.get('message', 'Logout successful')
        except Exception as e:
            return False, str(e)

    # ========================
    # Connection Management Methods
    # ========================

    def add_connection(self, username: str, token: str, name: str,
                      connection_string: str, description: str = "") -> Tuple[bool, str, Optional[Dict]]:
        """Add a connection for a user."""
        try:
            headers = {'Authorization': f'Bearer {token}'}
            data = {
                "name": name,
                "connection_string": connection_string,
                "description": description
            }
            result = self._make_request('POST', f'/users/{username}/connections', data=data, headers=headers)
            return True, f"Connection '{name}' added successfully", result
        except Exception as e:
            return False, str(e), None

    def list_connections(self, username: str, token: str) -> Tuple[bool, str, List[Dict]]:
        """List all connections for a user."""
        try:
            headers = {'Authorization': f'Bearer {token}'}
            result = self._make_request('GET', f'/users/{username}/connections', headers=headers)
            return True, "Connections retrieved successfully", result.get('connections', [])
        except Exception as e:
            return False, str(e), []

    def get_connection(self, username: str, token: str, connection_id: str) -> Tuple[bool, str, Optional[Dict]]:
        """Get a specific connection."""
        try:
            headers = {'Authorization': f'Bearer {token}'}
            result = self._make_request('GET', f'/users/{username}/connections/{connection_id}', headers=headers)
            return True, "Connection retrieved successfully", result
        except Exception as e:
            return False, str(e), None

    def update_connection(self, username: str, token: str, connection_id: str,
                         name: str = None, connection_string: str = None,
                         description: str = None) -> Tuple[bool, str, Optional[Dict]]:
        """Update a connection."""
        try:
            headers = {'Authorization': f'Bearer {token}'}
            data = {}
            if name is not None:
                data['name'] = name
            if connection_string is not None:
                data['connection_string'] = connection_string
            if description is not None:
                data['description'] = description

            result = self._make_request('PUT', f'/users/{username}/connections/{connection_id}',
                                       data=data, headers=headers)
            return True, "Connection updated successfully", result
        except Exception as e:
            return False, str(e), None

    def delete_connection(self, username: str, token: str, connection_id: str) -> Tuple[bool, str]:
        """Delete a connection."""
        try:
            headers = {'Authorization': f'Bearer {token}'}
            result = self._make_request('DELETE', f'/users/{username}/connections/{connection_id}', headers=headers)
            return True, result.get('message', 'Connection deleted successfully')
        except Exception as e:
            return False, str(e)

    def get_active_connection(self, username: str, token: str) -> Tuple[bool, str, Optional[Dict]]:
        """Get the active connection for a user."""
        try:
            headers = {'Authorization': f'Bearer {token}'}
            result = self._make_request('GET', f'/users/{username}/connections/active', headers=headers)
            return True, "Active connection retrieved successfully", result
        except Exception as e:
            return False, str(e), None

    def set_active_connection(self, username: str, token: str, connection_id: str) -> Tuple[bool, str, Optional[Dict]]:
        """Set the active connection for a user."""
        try:
            headers = {'Authorization': f'Bearer {token}'}
            result = self._make_request('POST', f'/users/{username}/connections/{connection_id}/activate',
                                       headers=headers)
            return True, result.get('message', 'Connection activated successfully'), result.get('connection')
        except Exception as e:
            return False, str(e), None

    def update_connection_test_result(self, username: str, token: str, connection_id: str,
                                     success: bool, details: str = ""):
        """Update the test result for a connection."""
        try:
            headers = {'Authorization': f'Bearer {token}'}
            params = {
                'test_success': success,
                'details': details
            }
            self._make_request('POST', f'/users/{username}/connections/{connection_id}/test',
                             headers=headers, params=params)
        except:
            pass  # Silently fail for test result updates

    # ========================
    # Organization Management Methods
    # ========================

    def create_organization(self, token: str, name: str, display_name: str = None,
                           description: str = "") -> Tuple[bool, str, Optional[Dict]]:
        """Create a new organization (super-admin only)."""
        try:
            headers = {'Authorization': f'Bearer {token}'}
            data = {
                "name": name,
                "display_name": display_name or name,
                "description": description
            }
            result = self._make_request('POST', '/organizations', data=data, headers=headers)
            return True, f"Organization '{name}' created successfully", result
        except Exception as e:
            return False, str(e), None

    def list_organizations(self, token: str) -> Tuple[bool, str, List[Dict]]:
        """List organizations (super-admin sees all, org-admin sees own)."""
        logger.info("Listing organizations via User Manager API")
        try:
            # If OAuth client is configured, don't pass token (let OAuth handle it)
            # Otherwise, use the provided token for legacy auth
            headers = {}
            if not self.oauth_client and token:
                headers = {'Authorization': f'Bearer {token}'}

            result = self._make_request('GET', '/organizations', headers=headers)
            orgs = result.get('organizations', [])
            logger.info(f"Retrieved {len(orgs)} organizations from API")
            return True, "Organizations retrieved successfully", orgs
        except Exception as e:
            logger.error(f"Failed to list organizations: {str(e)}")
            return False, str(e), []

    def get_organization(self, token: str, org_name: str) -> Tuple[bool, str, Optional[Dict]]:
        """Get organization details."""
        try:
            headers = {'Authorization': f'Bearer {token}'}
            result = self._make_request('GET', f'/organizations/{org_name}', headers=headers)
            return True, "Organization retrieved successfully", result
        except Exception as e:
            return False, str(e), None

    def update_organization(self, token: str, org_name: str, display_name: str = None,
                           description: str = None, active: bool = None) -> Tuple[bool, str]:
        """Update organization (super-admin only)."""
        try:
            headers = {'Authorization': f'Bearer {token}'}
            data = {}
            if display_name is not None:
                data['display_name'] = display_name
            if description is not None:
                data['description'] = description
            if active is not None:
                data['active'] = active

            result = self._make_request('PUT', f'/organizations/{org_name}', data=data, headers=headers)
            return True, result.get('message', 'Organization updated successfully')
        except Exception as e:
            return False, str(e)

    def delete_organization(self, token: str, org_name: str) -> Tuple[bool, str]:
        """Delete organization (super-admin only)."""
        try:
            headers = {'Authorization': f'Bearer {token}'}
            result = self._make_request('DELETE', f'/organizations/{org_name}', headers=headers)
            return True, result.get('message', 'Organization deleted successfully')
        except Exception as e:
            return False, str(e)

    def list_organization_users(self, token: str, org_name: str) -> Tuple[bool, str, List[Dict]]:
        """List users in an organization."""
        try:
            headers = {'Authorization': f'Bearer {token}'}
            result = self._make_request('GET', f'/organizations/{org_name}/users', headers=headers)
            return True, "Users retrieved successfully", result.get('users', [])
        except Exception as e:
            return False, str(e), []

    def list_organization_connections(self, token: str, org_name: str) -> Tuple[bool, str, List[Dict]]:
        """List all connections in an organization."""
        try:
            headers = {'Authorization': f'Bearer {token}'}
            result = self._make_request('GET', f'/organizations/{org_name}/connections', headers=headers)
            return True, "Connections retrieved successfully", result.get('connections', [])
        except Exception as e:
            return False, str(e), []

    # ========================
    # API Key Methods
    # ========================

    def validate_api_key(self, api_key: str) -> Tuple[bool, Optional[str]]:
        """
        Validate an API key.

        Args:
            api_key: Full API key value (e.g., sk_live_abc123...)

        Returns:
            Tuple of (is_valid, username)
        """
        try:
            headers = {'X-API-Key': api_key}
            result = self._make_request('POST', '/api-keys/validate', headers=headers)

            is_valid = result.get('valid', False)
            username = result.get('username')

            if is_valid and username:
                logger.debug(f"API key validated successfully for user: {username}")
                return True, username
            else:
                logger.debug("API key validation failed")
                return False, None
        except Exception as e:
            logger.warning(f"API key validation error: {e}")
            return False, None

    def create_api_key(self, username: str, token: str, name: str,
                      description: str = "", expires_in_days: int = None) -> Tuple[bool, str, Optional[str], Optional[Dict]]:
        """
        Create a new API key for a user.

        Args:
            username: Username who will own the key
            token: JWT authentication token
            name: Friendly name for the key
            description: Optional description
            expires_in_days: Days until expiration (None for no expiration)

        Returns:
            Tuple of (success, message, api_key_value, key_info)
        """
        try:
            headers = {'Authorization': f'Bearer {token}'}
            data = {
                "name": name,
                "description": description
            }
            if expires_in_days is not None:
                data["expires_in_days"] = expires_in_days

            result = self._make_request('POST', f'/api-keys/users/{username}/keys',
                                       data=data, headers=headers)

            api_key_value = result.get('api_key')
            key_info = result.get('key_info')
            message = result.get('message', 'API key created successfully')

            logger.info(f"API key '{name}' created for user: {username}")
            return True, message, api_key_value, key_info
        except Exception as e:
            logger.error(f"Failed to create API key: {e}")
            return False, str(e), None, None

    def list_api_keys(self, username: str, token: str) -> Tuple[bool, str, List[Dict]]:
        """
        List all API keys for a user.

        Args:
            username: Username
            token: JWT authentication token

        Returns:
            Tuple of (success, message, list of api_keys)
        """
        try:
            headers = {'Authorization': f'Bearer {token}'}
            result = self._make_request('GET', f'/api-keys/users/{username}/keys', headers=headers)

            api_keys = result.get('api_keys', [])
            logger.info(f"Retrieved {len(api_keys)} API keys for user: {username}")
            return True, "API keys retrieved successfully", api_keys
        except Exception as e:
            logger.error(f"Failed to list API keys: {e}")
            return False, str(e), []

    def get_api_key(self, username: str, token: str, key_id: str) -> Tuple[bool, str, Optional[Dict]]:
        """
        Get details of a specific API key.

        Args:
            username: Username
            token: JWT authentication token
            key_id: API key ID

        Returns:
            Tuple of (success, message, key_info)
        """
        try:
            headers = {'Authorization': f'Bearer {token}'}
            result = self._make_request('GET', f'/api-keys/users/{username}/keys/{key_id}', headers=headers)
            return True, "API key retrieved successfully", result
        except Exception as e:
            logger.error(f"Failed to get API key: {e}")
            return False, str(e), None

    def update_api_key(self, username: str, token: str, key_id: str,
                      name: str = None, description: str = None, active: bool = None) -> Tuple[bool, str, Optional[Dict]]:
        """
        Update an API key.

        Args:
            username: Username
            token: JWT authentication token
            key_id: API key ID
            name: New name (optional)
            description: New description (optional)
            active: Active status (optional)

        Returns:
            Tuple of (success, message, updated_key_info)
        """
        try:
            headers = {'Authorization': f'Bearer {token}'}
            data = {}
            if name is not None:
                data['name'] = name
            if description is not None:
                data['description'] = description
            if active is not None:
                data['active'] = active

            result = self._make_request('PATCH', f'/api-keys/users/{username}/keys/{key_id}',
                                       data=data, headers=headers)

            logger.info(f"API key {key_id} updated for user: {username}")
            return True, "API key updated successfully", result
        except Exception as e:
            logger.error(f"Failed to update API key: {e}")
            return False, str(e), None

    def delete_api_key(self, username: str, token: str, key_id: str) -> Tuple[bool, str]:
        """
        Delete/revoke an API key.

        Args:
            username: Username
            token: JWT authentication token
            key_id: API key ID

        Returns:
            Tuple of (success, message)
        """
        try:
            headers = {'Authorization': f'Bearer {token}'}
            result = self._make_request('DELETE', f'/api-keys/users/{username}/keys/{key_id}', headers=headers)

            message = result.get('message', 'API key deleted successfully')
            logger.info(f"API key {key_id} deleted for user: {username}")
            return True, message
        except Exception as e:
            logger.error(f"Failed to delete API key: {e}")
            return False, str(e)
