"""
OAuth 2.0 Client for SimpliQ MCP Server
Handles Authorization Code Flow with browser-based authentication

Author: Gerson Amorim
Date: 27 de Novembro de 2025
"""

import json
import webbrowser
import secrets
import threading
import time
from datetime import datetime, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlencode, parse_qs, urlparse
from typing import Optional, Dict, Any
from pathlib import Path
import requests
import logging

logger = logging.getLogger(__name__)


class CallbackHandler(BaseHTTPRequestHandler):
    """HTTP request handler for OAuth callback"""

    # Class variable to store authorization code
    authorization_code = None
    state = None
    error = None

    def log_message(self, format, *args):
        """Suppress default logging"""
        pass

    def do_GET(self):
        """Handle GET request to callback endpoint"""
        # Parse query parameters
        query = urlparse(self.path).query
        params = parse_qs(query)

        # Extract code and state
        if 'code' in params:
            CallbackHandler.authorization_code = params['code'][0]
            CallbackHandler.state = params.get('state', [None])[0]

            # Send success response
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>SimpliQ OAuth - Autorização Concluída</title>
                <style>
                    body {
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    }
                    .container {
                        background: white;
                        padding: 40px;
                        border-radius: 10px;
                        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                        text-align: center;
                        max-width: 500px;
                    }
                    .success-icon {
                        font-size: 64px;
                        color: #4CAF50;
                        margin-bottom: 20px;
                    }
                    h1 {
                        color: #333;
                        margin-bottom: 10px;
                    }
                    p {
                        color: #666;
                        line-height: 1.6;
                    }
                    .note {
                        background: #f5f5f5;
                        padding: 15px;
                        border-radius: 5px;
                        margin-top: 20px;
                        font-size: 14px;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="success-icon">✓</div>
                    <h1>Autorização Concluída!</h1>
                    <p>Você autorizou o SimpliQ com sucesso.</p>
                    <p>Você pode fechar esta janela e retornar ao Claude Desktop.</p>
                    <div class="note">
                        <strong>Próximos Passos:</strong><br>
                        O SimpliQ MCP Server agora está autenticado e pronto para uso.
                    </div>
                </div>
                <script>
                    // Auto-close after 3 seconds
                    setTimeout(function() {
                        window.close();
                    }, 3000);
                </script>
            </body>
            </html>
            """
            self.wfile.write(html.encode())

        elif 'error' in params:
            CallbackHandler.error = params['error'][0]
            error_description = params.get('error_description', ['Unknown error'])[0]

            # Send error response
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>SimpliQ OAuth - Erro</title>
                <style>
                    body {{
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                    }}
                    .container {{
                        background: white;
                        padding: 40px;
                        border-radius: 10px;
                        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                        text-align: center;
                        max-width: 500px;
                    }}
                    .error-icon {{
                        font-size: 64px;
                        color: #f44336;
                        margin-bottom: 20px;
                    }}
                    h1 {{
                        color: #333;
                        margin-bottom: 10px;
                    }}
                    p {{
                        color: #666;
                        line-height: 1.6;
                    }}
                    .error-details {{
                        background: #ffebee;
                        padding: 15px;
                        border-radius: 5px;
                        margin-top: 20px;
                        font-size: 14px;
                        color: #c62828;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="error-icon">✗</div>
                    <h1>Erro na Autorização</h1>
                    <p>Não foi possível completar a autorização.</p>
                    <div class="error-details">
                        <strong>Erro:</strong> {CallbackHandler.error}<br>
                        <strong>Descrição:</strong> {error_description}
                    </div>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode())


class OAuthClient:
    """OAuth 2.0 Client for Authorization Code Flow"""

    def __init__(
        self,
        user_manager_url: str,
        client_id: str,
        client_secret: str,
        redirect_uri: str = "http://localhost:3000/callback",
        scopes: list = None,
        token_file: str = None
    ):
        """
        Initialize OAuth Client

        Args:
            user_manager_url: Base URL of User Manager API
            client_id: OAuth client ID
            client_secret: OAuth client secret
            redirect_uri: Callback URI (must match registered redirect_uri)
            scopes: List of OAuth scopes to request
            token_file: Path to file for storing tokens (default: ./oauth_tokens.json)
        """
        self.user_manager_url = user_manager_url.rstrip('/')
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scopes = scopes or ["admin:org", "read:connections", "write:connections", "execute:tools"]

        # Token storage
        if token_file:
            self.token_file = Path(token_file)
        else:
            self.token_file = Path(__file__).parent / "oauth_tokens.json"

        # In-memory token cache
        self._token_data: Optional[Dict[str, Any]] = None
        self._token_expiry: Optional[datetime] = None

        # Load existing tokens
        self._load_token()

    def get_access_token(self) -> str:
        """
        Get a valid access token

        Returns:
            Valid access token

        Raises:
            Exception if unable to obtain token
        """
        # Check if we have a valid token
        if self._is_token_valid():
            logger.info("Using cached access token")
            return self._token_data['access_token']

        # Check if we can refresh the token
        if self._token_data and 'refresh_token' in self._token_data:
            logger.info("Refreshing access token")
            try:
                self._refresh_access_token()
                return self._token_data['access_token']
            except Exception as e:
                logger.warning(f"Failed to refresh token: {e}")
                # Fall through to start new OAuth flow

        # Start new OAuth flow
        logger.info("Starting new OAuth Authorization Code Flow")
        self._start_oauth_flow()
        return self._token_data['access_token']

    def _is_token_valid(self) -> bool:
        """Check if current token is valid"""
        if not self._token_data or 'access_token' not in self._token_data:
            return False

        if not self._token_expiry:
            return False

        # Consider token invalid if it expires in less than 60 seconds
        return datetime.now() < (self._token_expiry - timedelta(seconds=60))

    def _start_oauth_flow(self):
        """Start OAuth Authorization Code Flow"""
        # Generate random state for CSRF protection
        state = secrets.token_urlsafe(32)

        # Build authorization URL
        auth_params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': ' '.join(self.scopes),
            'state': state
        }

        auth_url = f"{self.user_manager_url}/oauth/authorize?{urlencode(auth_params)}"

        logger.info(f"Opening browser for OAuth authorization: {auth_url}")
        print("\n" + "="*80)
        print("SimpliQ OAuth Authorization")
        print("="*80)
        print("\nAbrindo o browser para autenticacao...")
        print(f"\nSe o browser nao abrir automaticamente, acesse:")
        print(f"{auth_url}")
        print("\n" + "="*80 + "\n")

        # Reset callback handler state
        CallbackHandler.authorization_code = None
        CallbackHandler.state = None
        CallbackHandler.error = None

        # Start callback server in background
        server_thread = threading.Thread(
            target=self._run_callback_server,
            daemon=True
        )
        server_thread.start()

        # Wait a moment for server to start
        time.sleep(0.5)

        # Open browser
        webbrowser.open(auth_url)

        # Wait for callback (timeout after 5 minutes)
        timeout = 300  # 5 minutes
        start_time = time.time()

        while CallbackHandler.authorization_code is None and CallbackHandler.error is None:
            if time.time() - start_time > timeout:
                raise TimeoutError("OAuth authorization timed out after 5 minutes")
            time.sleep(0.5)

        # Check for errors
        if CallbackHandler.error:
            raise Exception(f"OAuth authorization failed: {CallbackHandler.error}")

        # Validate state
        if CallbackHandler.state != state:
            raise Exception("Invalid state parameter - possible CSRF attack")

        # Exchange code for token
        logger.info("Authorization code received, exchanging for access token")
        self._exchange_code_for_token(CallbackHandler.authorization_code)

        print("\n" + "="*80)
        print("[OK] Autenticacao OAuth concluida com sucesso!")
        print("="*80 + "\n")

    def _run_callback_server(self):
        """Run HTTP server to capture OAuth callback"""
        # Parse redirect_uri to get port
        parsed = urlparse(self.redirect_uri)
        port = parsed.port or 3000

        server = HTTPServer(('localhost', port), CallbackHandler)

        # Handle only one request
        server.handle_request()

    def _exchange_code_for_token(self, code: str):
        """
        Exchange authorization code for access token

        Args:
            code: Authorization code from callback
        """
        token_url = f"{self.user_manager_url}/oauth/token"

        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri
        }

        logger.info(f"Exchanging authorization code for access token at {token_url}")

        response = requests.post(
            token_url,
            data=data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )

        if response.status_code != 200:
            raise Exception(f"Token exchange failed: {response.status_code} - {response.text}")

        self._token_data = response.json()

        # Calculate token expiry
        expires_in = self._token_data.get('expires_in', 86400)  # Default 24 hours
        self._token_expiry = datetime.now() + timedelta(seconds=expires_in)

        # Save tokens
        self._save_token()

        logger.info("Access token obtained successfully")

    def _refresh_access_token(self):
        """Refresh access token using refresh token"""
        if not self._token_data or 'refresh_token' not in self._token_data:
            raise Exception("No refresh token available")

        token_url = f"{self.user_manager_url}/oauth/token"

        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self._token_data['refresh_token'],
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }

        logger.info("Refreshing access token")

        response = requests.post(
            token_url,
            data=data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )

        if response.status_code != 200:
            raise Exception(f"Token refresh failed: {response.status_code} - {response.text}")

        self._token_data = response.json()

        # Calculate token expiry
        expires_in = self._token_data.get('expires_in', 86400)
        self._token_expiry = datetime.now() + timedelta(seconds=expires_in)

        # Save tokens
        self._save_token()

        logger.info("Access token refreshed successfully")

    def _save_token(self):
        """Save tokens to file"""
        if not self._token_data:
            return

        token_storage = {
            'token_data': self._token_data,
            'expiry': self._token_expiry.isoformat() if self._token_expiry else None,
            'saved_at': datetime.now().isoformat()
        }

        # Ensure directory exists
        self.token_file.parent.mkdir(parents=True, exist_ok=True)

        with open(self.token_file, 'w') as f:
            json.dump(token_storage, f, indent=2)

        logger.info(f"Tokens saved to {self.token_file}")

    def _load_token(self):
        """Load tokens from file"""
        if not self.token_file.exists():
            logger.info(f"No token file found at {self.token_file}")
            return

        try:
            with open(self.token_file, 'r') as f:
                token_storage = json.load(f)

            self._token_data = token_storage.get('token_data')
            expiry_str = token_storage.get('expiry')

            if expiry_str:
                self._token_expiry = datetime.fromisoformat(expiry_str)

            logger.info(f"Tokens loaded from {self.token_file}")

        except Exception as e:
            logger.warning(f"Failed to load tokens: {e}")
            self._token_data = None
            self._token_expiry = None

    def clear_tokens(self):
        """Clear stored tokens"""
        self._token_data = None
        self._token_expiry = None

        if self.token_file.exists():
            self.token_file.unlink()
            logger.info("Tokens cleared")

    def get_auth_headers(self) -> Dict[str, str]:
        """
        Get HTTP headers with Bearer token for authenticated requests

        Returns:
            Dictionary with Authorization header
        """
        access_token = self.get_access_token()
        logger.debug(f"get_auth_headers() - Token length: {len(access_token) if access_token else 0}")
        logger.debug(f"get_auth_headers() - Token preview: {access_token[:50]}..." if access_token else "No token")
        return {
            'Authorization': f'Bearer {access_token}'
        }


if __name__ == '__main__':
    """Test OAuth client"""

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Test configuration
    oauth_client = OAuthClient(
        user_manager_url="http://localhost:8002",
        client_id="3605d770-c384-4aeb-b6aa-b2e950f6bce3",
        client_secret="Ev8sZbjt3PVy2fiWwqbo_nAx6FNdjTj3Olf3-h6W1gM",
        redirect_uri="http://localhost:3000/callback"
    )

    # Get access token (will start OAuth flow if needed)
    try:
        token = oauth_client.get_access_token()
        print(f"\n[OK] Access Token: {token[:50]}...")

        # Test authenticated request
        headers = oauth_client.get_auth_headers()
        response = requests.get(
            "http://localhost:8002/auth/me",
            headers=headers
        )

        if response.status_code == 200:
            user_info = response.json()
            print(f"\n[OK] Authenticated as: {user_info.get('username')}")
            print(f"   Organization: {user_info.get('organization')}")
            print(f"   Role: {user_info.get('role')}")
        else:
            print(f"\n[ERROR] Authentication test failed: {response.status_code}")

    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
