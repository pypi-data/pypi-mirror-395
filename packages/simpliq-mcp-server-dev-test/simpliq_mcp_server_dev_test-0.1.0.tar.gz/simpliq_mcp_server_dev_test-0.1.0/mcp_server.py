"""SimpliqData MCP-like POC server.

This server reads a database connection string and authentication settings from
the YAML configuration file (config.yml) and exposes both REST and MCP-style
JSON-RPC endpoints for tool execution and multi-user operations.

Core Endpoints (HTTP / REST):
    - GET /                     : MCP server discovery endpoint (basic metadata + tool list)
    - GET /.well-known/mcp      : MCP protocol information
    - GET /config               : Retrieve current connection string & parsed info
    - POST /config              : Update connection string (persists to YAML)
    - GET /status               : Basic database connectivity status
    - GET /objects              : List basic database objects (schemas, tables, views, users)
    - POST /connect             : Explicitly (re)connect using current config
    - POST /disconnect          : Dispose current SQLAlchemy engine
    - POST /validate            : Full validation (format, network, connect test)
    - POST /build-connection    : Build connection string from individual parameters

MCP / JSON-RPC Methods (POST /):
    - initialize                : Protocol handshake (must return protocolVersion)
    - tools/list                : Enumerate available tools
    - tools/call                : Execute a tool by name
    - prompts/list, resources/list, logging/setLevel : Implemented as no-op / empty for compatibility

Authentication Modes (authentication.type in config.yml):
    - mcp    : Standard authentication via User Manager API. Supports:
               * Bearer JWT in Authorization header
               * Persisted session token stored in .mcp_session.json
    - client : Passthrough identity from headers. Accepts:
               * X-Client-Username (required for identity)
               * X-Client-Email (optional metadata)
               * X-Client-Org (optional organization identifier)
               No token validation is performed; use ONLY in trusted environments
               (e.g., behind an authenticated reverse proxy or local development).

Resolution Order for Authenticated User:
    - client mode: headers -> Bearer token -> stored session
    - mcp mode   : Bearer token -> stored session

If identity cannot be resolved (and endpoint requires auth) a JSON-RPC / REST
error with message from auth_required_message is returned.

Usage:
    python mcp_server.py
    Then open http://127.0.0.1:8000/ for discovery or /config for current settings.
"""

# Clean up any corrupted OPENAI_API_KEY environment variable before loading settings
import os
if 'OPENAI_API_KEY' in os.environ and os.environ['OPENAI_API_KEY'].endswith('_OPENAI'):
    print("[WARNING] Removing corrupted OPENAI_API_KEY ending with '_OPENAI'")
    del os.environ['OPENAI_API_KEY']

from flask import Flask, jsonify, request, Response, g, send_file
from flask_cors import CORS
import yaml
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine.url import make_url
from urllib.parse import urlparse
import json
import socket
import re
import os
import sys
import ssl
import time
import logging
import io
import base64
from functools import wraps
from pathlib import Path
from user_api_client import UserAPIClient
from sql_executor import SQLValidator, SQLExecutor  # Existing validator/executor
from nl_to_sql import NLtoSQLEngine
from llm_client import MockLLMClient, OpenAIClient, AnthropicClient, GeminiClient
from sql_validator import SQLValidator as MinimalSQLValidator  # Lightweight validator for NL->SQL engine
from simple_sql_executor import SimpleSQLExecutor
from schema_introspector import SchemaIntrospector
from semantic_catalog import SemanticCatalog
from semantic_models import SemanticMapping
from plugins.registry import MCPPluginRegistry
from oauth.middleware import OAuthMiddleware, create_oauth_context  # OAuth 2.0 Phase 2
from oauth_client import OAuthClient  # OAuth 2.0 Phase 3 - Client-side flow

"""
Configuration file resolution
Priority order (first found wins):
  1) --config <path> or --config=<path> (also -c) provided in CLI
  2) Environment variables SIMPLIQ_CONFIG or SIMPLIQ_CONFIG_FILE
  3) Default file "config.yml" located next to this script

This runs at import time so logging and other components use the chosen file.
"""

# Resolve config path relative to this file to avoid CWD issues under debuggers
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def _resolve_config_file() -> str:
    """Resolve which YAML config file to use based on CLI args/env/default.

    Returns absolute path to the config file. Falls back to default if the
    provided path doesn't exist, emitting a console warning.
    """
    default_cfg = os.path.abspath(os.path.join(BASE_DIR, "config.yml"))

    # 1) CLI flags: --config <path>, --config=<path>, -c <path>
    try:
        argv = sys.argv[1:] if hasattr(sys, 'argv') else []
        candidate = None
        i = 0
        while i < len(argv):
            arg = argv[i]
            if arg.startswith("--config="):
                candidate = arg.split("=", 1)[1].strip().strip('"')
                break
            elif arg == "--config" or arg == "-c":
                if i + 1 < len(argv):
                    candidate = argv[i + 1].strip().strip('"')
                    break
                else:
                    print("WARNING: --config specified without a path; using default config.yml")
            i += 1
        if not candidate:
            # 2) Environment variables
            candidate = os.environ.get("SIMPLIQ_CONFIG") or os.environ.get("SIMPLIQ_CONFIG_FILE")

        if candidate:
            # If the candidate is a relative path, resolve relative to BASE_DIR for convenience
            cand_path = candidate
            if not os.path.isabs(cand_path):
                cand_path = os.path.normpath(os.path.join(BASE_DIR, cand_path))
            cand_path = os.path.abspath(cand_path)

            if os.path.exists(cand_path):
                return cand_path
            else:
                print(f"WARNING: Config file not found: {cand_path}. Falling back to default: {default_cfg}")
    except Exception as e:
        print(f"WARNING: Failed to resolve --config flag/env: {e}. Using default config.yml")

    return default_cfg

CONFIG_FILE = _resolve_config_file()
SESSION_FILE = Path(BASE_DIR) / ".mcp_session.json"

print(f">>> Using configuration file: {CONFIG_FILE}")

# Initialize logging FIRST
def setup_logging():
    """Setup logging configuration from config file."""
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = yaml.safe_load(f)
            logging_config = config.get('logging', {})

            log_level_str = logging_config.get('level', 'INFO').upper()
            log_level = getattr(logging, log_level_str, logging.INFO)
            log_format = logging_config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

            # Create handlers with explicit level (force stdout)
            console_handler = logging.StreamHandler(stream=sys.stdout)
            console_handler.setLevel(log_level)  # Set explicit level on handler
            console_handler.setFormatter(logging.Formatter(log_format))

            handlers_list = [console_handler]

            # Add file handler if configured
            if logging_config.get('log_to_file', False):
                log_file = logging_config.get('log_file', 'mcp_server.log')
                file_handler = logging.FileHandler(log_file)
                file_handler.setLevel(log_level)  # Set explicit level on handler
                file_handler.setFormatter(logging.Formatter(log_format))
                handlers_list.append(file_handler)

            # Configure root logger with force=True to override any existing config
            logging.basicConfig(
                level=log_level,
                format=log_format,
                force=True,  # Force reconfiguration
                handlers=handlers_list
            )

            # Get root logger and ensure level is set
            root_logger = logging.getLogger()
            root_logger.setLevel(log_level)

            # Create logger for this module
            module_logger = logging.getLogger(__name__)
            module_logger.setLevel(log_level)

            # Print confirmation of logging setup
            print(f">>> Logging configured: Level={log_level_str} (value={log_level})")
            print(f">>> Root logger level: {root_logger.level}")
            print(f">>> Module logger level: {module_logger.level}")
            print(f">>> Handlers: {len(handlers_list)} handler(s)")
            for i, handler in enumerate(handlers_list):
                print(f">>>   Handler {i+1}: {handler.__class__.__name__} (level={handler.level})")

            return module_logger, log_level
    except Exception as e:
        # Fallback to basic logging if config fails
        logging.basicConfig(level=logging.INFO, force=True)
        logger = logging.getLogger(__name__)
        logger.warning(f"Failed to load logging config: {e}. Using default logging.")
        return logger, logging.INFO

logger, log_level = setup_logging()

app = Flask(__name__)

# Configure CORS to allow requests from Claude.ai and other origins
CORS(app, resources={
    r"/*": {
        "origins": ["https://claude.ai", "https://*.claude.ai", "https://*.ngrok-free.app", "*"],
        "methods": ["GET", "POST", "OPTIONS", "HEAD"],
        "allow_headers": ["Content-Type", "Authorization", "ngrok-skip-browser-warning", "Mcp-Session-Id", "MCP-Protocol-Version"],
        "expose_headers": ["Content-Type", "Mcp-Session-Id", "MCP-Protocol-Version"],
        "supports_credentials": True,
        "max_age": 3600
    }
})

# Configure Flask's logger to use our format and level
app.logger.handlers = []  # Clear existing handlers
for handler in logging.getLogger().handlers:
    app.logger.addHandler(handler)
app.logger.setLevel(log_level)  # Use the log_level we got from config
app.logger.propagate = False  # Don't propagate to root to avoid duplicate logs

print(f">>> Flask app.logger level: {app.logger.level}")
print(f">>> Flask app.logger handlers: {len(app.logger.handlers)}")

# Keep werkzeug logs but at WARNING level to reduce noise
werkzeug_logger = logging.getLogger('werkzeug')
# Show access logs (was WARNING). Set to INFO so we can see inbound requests while debugging.
werkzeug_logger.setLevel(logging.INFO)
# Ensure werkzeug logs propagate to root so our stdout handler catches them
werkzeug_logger.propagate = True

# Test that DEBUG logging is working
print("\n>>> Testing DEBUG logging...")
logger.debug("TEST: This is a DEBUG message - if you see this, DEBUG logging works!")
logger.info("TEST: This is an INFO message")
logger.warning("TEST: This is a WARNING message")
print(">>> If you saw DEBUG/INFO/WARNING messages above, logging is working correctly\n")

# ============================================================================
# REQUEST LOGGING MIDDLEWARE
# ============================================================================
# Add comprehensive request/response logging to debug Claude Desktop hanging issue

@app.before_request
def log_request_info():
    """Log detailed information about every incoming request."""
    import time
    # Store request start time for duration calculation
    g.request_start_time = time.time()

    print("\n" + "="*80)
    print(">>> INCOMING REQUEST")
    print("="*80)
    print(f">>> Method: {request.method}")
    print(f">>> Path: {request.path}")
    print(f">>> URL: {request.url}")
    print(f">>> Remote Addr: {request.remote_addr}")
    print(f">>> User-Agent: {request.headers.get('User-Agent', 'N/A')}")
    print(f">>> Content-Type: {request.headers.get('Content-Type', 'N/A')}")
    print(f">>> Content-Length: {request.headers.get('Content-Length', 'N/A')}")

    # Log Authorization header (redacted)
    auth_header = request.headers.get('Authorization', None)
    if auth_header:
        # Show only first 20 chars for security
        print(f">>> Authorization: {auth_header[:20]}... [REDACTED]")
    else:
        print(">>> Authorization: None")

    # Log all headers (for debugging)
    print(">>> All Headers:")
    for key, value in request.headers.items():
        if key.lower() == 'authorization' and value:
            print(f">>>   {key}: {value[:20]}... [REDACTED]")
        else:
            print(f">>>   {key}: {value}")

    # Log request body for POST requests (with size limit)
    if request.method == "POST":
        try:
            # Get raw data
            body_data = request.get_data(as_text=True)
            if body_data:
                # Limit body logging to first 500 chars to avoid huge logs
                if len(body_data) > 500:
                    print(f">>> Request Body (first 500 chars): {body_data[:500]}... [TRUNCATED]")
                else:
                    print(f">>> Request Body: {body_data}")
            else:
                print(">>> Request Body: [EMPTY]")
        except Exception as e:
            print(f">>> Request Body: [ERROR READING: {e}]")

    print("="*80)
    print()

    logger.info(f"REQUEST: {request.method} {request.path} from {request.remote_addr}")


@app.after_request
def log_response_info(response):
    """Log detailed information about every outgoing response."""
    import time

    # Calculate request duration
    if hasattr(g, 'request_start_time'):
        duration = time.time() - g.request_start_time
        duration_ms = duration * 1000
    else:
        duration_ms = 0

    print("\n" + "="*80)
    print(">>> OUTGOING RESPONSE")
    print("="*80)
    print(f">>> Status: {response.status}")
    print(f">>> Status Code: {response.status_code}")
    print(f">>> Content-Type: {response.content_type}")
    print(f">>> Content-Length: {response.content_length or 'N/A'}")
    print(f">>> Duration: {duration_ms:.2f} ms")

    # Log response body (with size limit)
    try:
        response_data = response.get_data(as_text=True)
        if response_data:
            # Limit response logging to first 1000 chars
            if len(response_data) > 1000:
                print(f">>> Response Body (first 1000 chars): {response_data[:1000]}... [TRUNCATED]")
            else:
                print(f">>> Response Body: {response_data}")
        else:
            print(">>> Response Body: [EMPTY]")
    except Exception as e:
        print(f">>> Response Body: [ERROR READING: {e}]")

    print("="*80)
    print()

    logger.info(f"RESPONSE: {response.status_code} for {request.method} {request.path} ({duration_ms:.2f} ms)")

    return response

# ============================================================================
# END REQUEST LOGGING MIDDLEWARE
# ============================================================================

engine = None

# Initialize User Manager API client (will be updated with OAuth client later)
print("=" * 70)
print("MCP SERVER - Initializing...")
print("=" * 70)
logger.info("Initializing User Manager API client...")
users_api = None  # Will be initialized after OAuth client

# Initialize OAuth 2.0 Middleware (Phase 2)
oauth_middleware = None
try:
    with open(CONFIG_FILE, 'r') as f:
        config = yaml.safe_load(f)
        oauth_config = config.get('oauth', {})

        if oauth_config.get('enabled', False):
            provider_url = oauth_config.get('provider_url', 'http://localhost:8002')
            cache_ttl = oauth_config.get('token_validation', {}).get('cache_ttl', 300)

            oauth_middleware = OAuthMiddleware(
                provider_url=provider_url,
                cache_ttl=cache_ttl,
                enabled=True  # Forcing OAuth to be always enabled
            )

            print("=" * 70)
            print("OAuth 2.0 AUTHENTICATION")
            print("=" * 70)
            print(f">>> OAuth Enabled: YES")
            print(f">>> Provider URL: {provider_url}")
            print(f">>> Token Cache TTL: {cache_ttl}s")
            print("=" * 70)
            logger.info(f"OAuth middleware initialized: provider={provider_url}, cache_ttl={cache_ttl}s")
        else:
            print("=" * 70)
            print("OAuth 2.0 AUTHENTICATION")
            print("=" * 70)
            print(">>> OAuth Enabled: NO (legacy authentication mode)")
            print("=" * 70)
            logger.info("OAuth authentication is disabled")
except Exception as e:
    logger.warning(f"Failed to initialize OAuth middleware: {e}")
    print(f">>> WARNING: OAuth middleware initialization failed: {e}")
logger.info("User Manager API client initialized")

# Initialize OAuth 2.0 Client (Phase 3 - Authorization Code Flow)
oauth_client = None
try:
    with open(CONFIG_FILE, 'r') as f:
        config = yaml.safe_load(f)
        oauth_config = config.get('oauth', {})
        client_config = oauth_config.get('client', {})

        if client_config.get('enabled', False):
            print("=" * 70)
            print("OAuth 2.0 CLIENT - Authorization Code Flow")
            print("=" * 70)

            # Get configuration
            client_id = client_config.get('client_id')
            client_secret = os.environ.get('SIMPLIQ_OAUTH_CLIENT_SECRET') or client_config.get('client_secret')
            redirect_uri = client_config.get('redirect_uri', 'http://localhost:3000/callback')
            scopes = client_config.get('scopes', ['admin:org'])
            token_file = client_config.get('token_file', './oauth_tokens.json')
            auto_authenticate = client_config.get('auto_authenticate', True)

            # Validate required config
            if not client_id or not client_secret:
                raise ValueError("OAuth client_id and client_secret are required")

            # Initialize OAuth client
            oauth_client = OAuthClient(
                user_manager_url=oauth_config.get('provider_url', 'http://localhost:8002'),
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=redirect_uri,
                scopes=scopes,
                token_file=token_file
            )

            print(f">>> Client ID: {client_id}")
            print(f">>> Redirect URI: {redirect_uri}")
            print(f">>> Scopes: {', '.join(scopes)}")
            print(f">>> Token File: {token_file}")
            print(f">>> Auto-Authenticate: {auto_authenticate}")
            print("=" * 70)

            # Auto-authenticate if enabled
            if auto_authenticate:
                logger.info("Auto-authentication enabled, obtaining access token...")
                try:
                    access_token = oauth_client.get_access_token()
                    logger.info("Successfully obtained access token")
                    print(">>> [OK] OAuth authentication successful!")
                    print("=" * 70)
                except Exception as auth_error:
                    logger.error(f"Auto-authentication failed: {auth_error}")
                    print(f">>> [WARNING] OAuth authentication failed: {auth_error}")
                    print(">>> Authentication will be attempted on first API call")
                    print("=" * 70)
            else:
                logger.info("Auto-authentication disabled, token will be obtained on first API call")
                print(">>> OAuth client initialized (authentication deferred)")
                print("=" * 70)

        else:
            logger.info("OAuth client-side flow is disabled")

except Exception as e:
    logger.warning(f"Failed to initialize OAuth client: {e}")
    print(f">>> WARNING: OAuth client initialization failed: {e}")

# Initialize User Manager API client with OAuth support
logger.info("Initializing User Manager API client with OAuth support...")
users_api = UserAPIClient(config_file=CONFIG_FILE, oauth_client=oauth_client)
logger.info("User Manager API client initialized")
print("OK - User Manager API client initialized with OAuth support")

# Initialize Semantic Catalog (Sprint 3 - Semantic Mapping)
logger.info("Initializing Semantic Catalog...")
semantic_catalog = SemanticCatalog(storage_dir="semantic_mappings")
logger.info("Semantic Catalog initialized")
print("OK - User Manager API client initialized")

# Initialize Plugin Registry (Sprint 4 - Plugin System)
logger.info("Initializing Plugin Registry...")
plugin_registry = MCPPluginRegistry()
logger.info("Plugin Registry initialized")

# Load plugins dynamically (optional - won't break if plugins are missing)
try:
    # Try to import and register Protheus mapper plugin
    from plugins.protheus import ProtheusMapperPlugin
    plugin_registry.register_plugin('protheus', ProtheusMapperPlugin())
    logger.info("Protheus mapper plugin registered")
except ImportError:
    logger.info("Protheus mapper plugin not available - continuing without it")
except Exception as e:
    logger.warning(f"Failed to load Protheus mapper plugin: {e}")

# Initialize all registered plugins (this will be called after engine is created)
# Note: Plugin initialization is deferred until database connection is established
logger.info(f"Plugin registry ready with {len(plugin_registry.list_plugins())} plugin(s)")

# Log effective authentication mode early for visibility
try:
    auth_cfg = None
    with open(CONFIG_FILE, 'r') as f:
        raw = yaml.safe_load(f) or {}
        auth_cfg = raw.get('authentication', {})
    declared_type = auth_cfg.get('type', 'mcp')
    effective_type = declared_type if str(declared_type).strip().lower() in {"mcp", "client", "apikey", "oauth"} else "mcp"
    if effective_type != str(declared_type).strip().lower():
        logger.warning(f"authentication.type '{declared_type}' não suportado - usando fallback '{effective_type}'")
    logger.info(f"Authentication mode: declared='{declared_type}' effective='{effective_type}'")
    print(f">>> Authentication mode: declared='{declared_type}' effective='{effective_type}'")
    if effective_type == 'client':
        print(
            ">>> CLIENT MODE ATIVO: identidade será lida dos cabeçalhos X-Client-Username/X-Client-Email/X-Client-Org. "
            "Use apenas em ambiente confiável."
        )
    elif effective_type == 'apikey':
        print(
            ">>> API KEY MODE ATIVO: autenticação via API Keys (sk_live_...). "
            "API Keys podem ser configuradas via env var SIMPLIQ_API_KEY ou Authorization header."
        )
except Exception as e:
    logger.warning(f"Failed to log authentication type: {e}")

print("=" * 70)

# -------------------------------------------------
# Session Management (JSON File Persistence)
# -------------------------------------------------

# -------------------------------------------------
# LLM/NL2SQL configuration (optional) from config.yml
# -------------------------------------------------
LLM_SETTINGS = {}

def load_llm_settings():
    """Load optional NL2SQL/LLM settings from config.yml.

        Expected YAML structure (either 'nl2sql' or 'llm'):
            nl2sql:
                provider: mock|openai|anthropic|gemini
        openai:
          api_key: "sk-..."
          model: "gpt-4o-mini"
          base_url: "https://api.openai.com"
          temperature: 0.1
          max_tokens: 800
        anthropic:
          api_key: "anth-sk-..."
          model: "claude-3-5-sonnet-latest"
          base_url: "https://api.anthropic.com"
          temperature: 0.1
          max_tokens: 800
                gemini:
                    api_key: "AIza..."
                    model: "gemini-1.5-pro"
                    base_url: "https://generativelanguage.googleapis.com"
                    temperature: 0.1
                    max_tokens: 800
    """
    try:
        with open(CONFIG_FILE, 'r') as f:
            cfg = yaml.safe_load(f) or {}
            nl2sql = cfg.get('nl2sql') or cfg.get('llm') or {}
            return nl2sql or {}
    except Exception as e:
        logger.warning(f"Could not load LLM settings from config.yml: {e}")
        return {}

def apply_llm_env_from_settings(settings: dict):
    """Optionally seed environment variables from YAML settings if not already set."""
    if not isinstance(settings, dict):
        return
    # Provider
    provider = settings.get('provider')
    if provider and not os.environ.get('SIMPLIQ_NL2SQL_PROVIDER'):
        os.environ['SIMPLIQ_NL2SQL_PROVIDER'] = str(provider)

    # OpenAI
    oai = settings.get('openai', {}) or {}
    if isinstance(oai, dict):
        if oai.get('api_key') and not os.environ.get('OPENAI_API_KEY'):
            os.environ['OPENAI_API_KEY'] = str(oai['api_key'])
        if oai.get('model') and not os.environ.get('SIMPLIQ_OPENAI_MODEL'):
            os.environ['SIMPLIQ_OPENAI_MODEL'] = str(oai['model'])
        if oai.get('base_url') and not os.environ.get('SIMPLIQ_OPENAI_BASE_URL'):
            os.environ['SIMPLIQ_OPENAI_BASE_URL'] = str(oai['base_url'])
        if oai.get('temperature') is not None and not os.environ.get('SIMPLIQ_OPENAI_TEMPERATURE'):
            os.environ['SIMPLIQ_OPENAI_TEMPERATURE'] = str(oai['temperature'])
        if oai.get('max_tokens') is not None and not os.environ.get('SIMPLIQ_OPENAI_MAX_TOKENS'):
            os.environ['SIMPLIQ_OPENAI_MAX_TOKENS'] = str(oai['max_tokens'])

    # Anthropic
    ant = settings.get('anthropic', {}) or {}
    if isinstance(ant, dict):
        if ant.get('api_key') and not os.environ.get('ANTHROPIC_API_KEY'):
            os.environ['ANTHROPIC_API_KEY'] = str(ant['api_key'])
        if ant.get('model') and not os.environ.get('SIMPLIQ_ANTHROPIC_MODEL'):
            os.environ['SIMPLIQ_ANTHROPIC_MODEL'] = str(ant['model'])
        if ant.get('base_url') and not os.environ.get('SIMPLIQ_ANTHROPIC_BASE_URL'):
            os.environ['SIMPLIQ_ANTHROPIC_BASE_URL'] = str(ant['base_url'])
        if ant.get('temperature') is not None and not os.environ.get('SIMPLIQ_ANTHROPIC_TEMPERATURE'):
            os.environ['SIMPLIQ_ANTHROPIC_TEMPERATURE'] = str(ant['temperature'])
        if ant.get('max_tokens') is not None and not os.environ.get('SIMPLIQ_ANTHROPIC_MAX_TOKENS'):
            os.environ['SIMPLIQ_ANTHROPIC_MAX_TOKENS'] = str(ant['max_tokens'])

    # Gemini
    gem = settings.get('gemini', {}) or {}
    if isinstance(gem, dict):
        # API Key: prefer GEMINI_API_KEY, but don't override if already set
        if gem.get('api_key') and not os.environ.get('GEMINI_API_KEY') and not os.environ.get('GOOGLE_API_KEY'):
            os.environ['GEMINI_API_KEY'] = str(gem['api_key'])
        if gem.get('model') and not os.environ.get('SIMPLIQ_GEMINI_MODEL'):
            os.environ['SIMPLIQ_GEMINI_MODEL'] = str(gem['model'])
        if gem.get('base_url') and not os.environ.get('SIMPLIQ_GEMINI_BASE_URL'):
            os.environ['SIMPLIQ_GEMINI_BASE_URL'] = str(gem['base_url'])
        if gem.get('temperature') is not None and not os.environ.get('SIMPLIQ_GEMINI_TEMPERATURE'):
            os.environ['SIMPLIQ_GEMINI_TEMPERATURE'] = str(gem['temperature'])
        if gem.get('max_tokens') is not None and not os.environ.get('SIMPLIQ_GEMINI_MAX_TOKENS'):
            os.environ['SIMPLIQ_GEMINI_MAX_TOKENS'] = str(gem['max_tokens'])

# Load and apply on module import
LLM_SETTINGS = load_llm_settings()
apply_llm_env_from_settings(LLM_SETTINGS)

# Debug: Print which provider is actually active
print(f"[DEBUG] SIMPLIQ_NL2SQL_PROVIDER = {os.environ.get('SIMPLIQ_NL2SQL_PROVIDER', 'NOT SET')}")
print(f"[DEBUG] config.yml provider = {LLM_SETTINGS.get('provider', 'NOT SET')}")

def load_session():
    """
    Load session from JSON file.

    Returns:
        dict: Session data if valid and not expired, None otherwise
    """
    if SESSION_FILE.exists():
        try:
            with open(SESSION_FILE, 'r') as f:
                session = json.load(f)
                # Verifica se não expirou
                if session.get("expires_at", 0) > time.time():
                    logger.info(f"Loaded valid session for user: {session.get('username')}")
                    return session
                else:
                    # Expirou, remove o arquivo
                    logger.info("Session expired, removing session file")
                    SESSION_FILE.unlink()
        except Exception as e:
            logger.warning(f"Failed to load session from file: {e}")
    return None


def save_session(token, username, expires_in=86400):
    """
    Save session to JSON file with automatic expiration.

    Args:
        token: Authentication token
        username: Username
        expires_in: Expiration time in seconds (default: 24 hours)
    """
    try:
        session = {
            "token": token,
            "username": username,
            "created_at": time.time(),
            "expires_at": time.time() + expires_in
        }
        with open(SESSION_FILE, 'w') as f:
            json.dump(session, f, indent=2)

        # Protege o arquivo (somente leitura/escrita pelo owner) - Unix/Linux
        try:
            SESSION_FILE.chmod(0o600)
        except Exception:
            # Windows não suporta chmod da mesma forma, ignora
            pass

        logger.info(f"Session saved for user: {username} (expires in {expires_in}s)")
        print(f">>> Session saved to: {SESSION_FILE}")
    except Exception as e:
        logger.error(f"Failed to save session to file: {e}")


def clear_session():
    """Clear session by removing the session file."""
    try:
        if SESSION_FILE.exists():
            SESSION_FILE.unlink()
            logger.info("Session file removed")
            print(f">>> Session cleared: {SESSION_FILE}")
        return True
    except Exception as e:
        logger.error(f"Failed to clear session: {e}")
        return False

# -------------------------------------------------
# Request/Response logging (Flask)
# -------------------------------------------------
@app.before_request
def _log_request_start():
    """Log basic request info and start timer."""
    try:
        g._req_start = time.perf_counter()
    except Exception:
        g._req_start = None

    try:
        # Simple correlation id (incremental counter) stored on app config
        counter = app.config.get('_req_counter', 0) + 1
        app.config['_req_counter'] = counter
        g.correlation_id = f"req-{counter}"
        path_disp = request.full_path if request.query_string else request.path
        body_preview = ''
        if request.method in ('POST','PUT','PATCH'):
            # Non-consuming peek of body (may be empty if already read)
            raw = request.get_data(cache=True)[:300]
            if raw:
                try:
                    body_preview = raw.decode(errors='replace')
                except Exception:
                    body_preview = str(raw)
                body_preview = body_preview.replace('\n','\\n')
        msg = (
            f"[REQ] {g.correlation_id} {request.method} {path_disp} ct={request.content_type} len={request.content_length} "
            f"ip={request.remote_addr} body='{body_preview}'"
        )
        logger.info(msg)
        print(msg, flush=True)
        # Low-level console write (bypasses overridden sys.stdout in some debuggers)
        try:
            os.write(1, (msg + "\n").encode('utf-8', 'replace'))
        except Exception:
            pass
    except Exception as e:
        logger.debug(f"[REQ] logging failed: {e}")


@app.after_request
def _log_request_end(response):
    """Log response status and duration, and add MCP session headers."""
    try:
        # Add MCP Session ID header if session exists
        session = load_session()
        if session and session.get('token'):
            # Use the username as session identifier
            response.headers["Mcp-Session-Id"] = session.get('username', 'unknown')

        # Check for Mcp-Session-Id in request and echo it back if present
        if request.headers.get('Mcp-Session-Id'):
            response.headers["Mcp-Session-Id"] = request.headers.get('Mcp-Session-Id')

        dur_ms = None
        if getattr(g, "_req_start", None) is not None:
            dur_ms = (time.perf_counter() - g._req_start) * 1000.0
        length = (
            response.calculate_content_length()
            if hasattr(response, "calculate_content_length")
            else None
        ) or response.headers.get("Content-Length")
        cid = getattr(g, 'correlation_id', 'req-?')
        msg = (
            f"[RES] {cid} {request.method} {request.path} -> {response.status_code} in {dur_ms:.1f} ms len={length}"
            if dur_ms is not None else f"[RES] {cid} {request.method} {request.path} -> {response.status_code} len={length}"
        )
        logger.info(msg)
        print(msg, flush=True)
        # Low-level console write (bypasses overridden sys.stdout in some debuggers)
        try:
            os.write(1, (msg + "\n").encode('utf-8', 'replace'))
        except Exception:
            pass
    except Exception as e:
        logger.debug(f"[RES] logging failed: {e}")
    return response

# Helper function for authentication
def extract_client_identity():
    """Extract client-provided identity from custom headers for 'client' auth type.

    Supported headers (case-insensitive):
      - X-Client-Username: the username to assume for this request
      - X-Client-Email: optional email for logging/diagnostics
      - X-Client-Org: optional organization identifier

    Returns:
        tuple[str|None, dict]: (username or None, metadata dict)
    """
    username = request.headers.get('X-Client-Username') or request.headers.get('X-User-Name')
    meta = {
        "email": request.headers.get('X-Client-Email'),
        "org": request.headers.get('X-Client-Org')
    }
    if username:
        try:
            redacted_meta = {k: v for k, v in meta.items() if v}
            logger.debug(f"Client identity passthrough detected: user='{username}', meta={redacted_meta}")
        except Exception:
            pass
        return username, meta
    return None, meta

def get_authenticated_user():
    """Resolve the authenticated user based on configured auth type.

    Resolution order:
      PRIORITY 1: OAuth 2.0 (if active in Flask g context)
      auth.type == 'apikey':
         1. API Key in Authorization header (Bearer sk_live_...)
         2. API Key in environment variable SIMPLIQ_API_KEY
         3. Fallback to JWT token in Authorization header
         4. Stored session file token
      auth.type == 'client':
         1. Client identity headers (X-Client-Username, etc.)
         2. Bearer token in Authorization header
         3. Stored session file token
      auth.type == 'mcp':
         1. Bearer token in Authorization header
         2. Stored session file token

    Returns:
        tuple[str|None, str|None]: (username, token_used_or_None)
    """
    # DEBUG: Log incoming headers
    auth_header = request.headers.get('Authorization') or request.headers.get('authorization')
    print(f"\n>>> [DEBUG] get_authenticated_user() called")
    print(f">>> [DEBUG] Authorization header: {auth_header[:50] if auth_header else 'None'}...")

    # PRIORITY 1: Check if OAuth 2.0 is active (already validated)
    # If OAuth middleware has already validated the request and set g.oauth_user_info,
    # use that instead of trying to validate as session token
    if hasattr(g, 'oauth_user_info') and g.oauth_user_info:
        oauth_user_id = g.oauth_user_info.get('sub')
        print(f">>> [DEBUG] OAuth user found in g context: {oauth_user_id}")
        logger.debug(f"Using OAuth authenticated user: {oauth_user_id}")

        # Extract the actual OAuth token from Authorization header
        # This token will be used for subsequent API calls to User Manager
        oauth_token = None
        if auth_header and auth_header.lower().startswith('bearer '):
            oauth_token = auth_header.split(None, 1)[1].strip()
            print(f">>> [DEBUG] Extracted OAuth token from header: {oauth_token[:30]}...")

        return oauth_user_id, oauth_token
    
    try:
        auth_cfg = get_auth_config()
    except Exception:
        auth_cfg = {"type": "mcp"}

    auth_type = auth_cfg.get("type", "mcp")
    print(f">>> [DEBUG] Auth type: {auth_type}")

    # Helper to validate a JWT token via user manager
    def _validate_token(token: str):
        if not token:
            return None
        try:
            print(f">>> [DEBUG] Validating token: {token[:30]}...")
            valid, username = users_api.validate_session(token)
            print(f">>> [DEBUG] Token validation result: valid={valid}, username={username}")
            if valid and username:
                return username
        except Exception as e:
            print(f">>> [DEBUG] Token validation exception: {e}")
        return None

    # Helper to validate an API key via user manager
    def _validate_api_key(api_key: str):
        if not api_key or not api_key.startswith('sk_'):
            return None
        try:
            valid, username = users_api.validate_api_key(api_key)
            if valid and username:
                logger.debug(f"API key validated for user: {username}")
                return username
        except Exception as e:
            logger.debug(f"API key validation failed: {e}")
        return None

    # API Key authentication mode is disabled to enforce OAuth
    # Client passthrough mode is disabled to enforce OAuth

    # Standard JWT authentication (for both 'mcp' and 'client' modes)
    # 1. Authorization Bearer header
    auth_header = request.headers.get('Authorization') or request.headers.get('authorization')
    print(f">>> [DEBUG] Standard JWT auth - Authorization header: {auth_header[:50] if auth_header else 'None'}...")
    if auth_header and auth_header.lower().startswith('bearer '):
        bearer_token = auth_header.split(None, 1)[1].strip()
        print(f">>> [DEBUG] Extracted bearer token: {bearer_token[:30]}...")
        user_from_token = _validate_token(bearer_token)
        if user_from_token:
            print(f">>> [DEBUG] User authenticated from header: {user_from_token}")
            return user_from_token, bearer_token
        else:
            print(f">>> [DEBUG] Token validation failed, trying session fallback")

    # 2. Session file fallback
    session = load_session()
    if session and session.get('token'):
        print(f">>> [DEBUG] Trying session file token: {session['token'][:30]}...")
        user_from_session = _validate_token(session['token'])
        if user_from_session:
            print(f">>> [DEBUG] User authenticated from session file: {user_from_session}")
            return user_from_session, session['token']

    print(f">>> [DEBUG] No authentication found, returning (None, None)")
    return None, None

def require_auth(f):
    """Decorator to require authentication for endpoints."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        username, token = get_authenticated_user()
        if not username:
            return jsonify({
                "success": False,
                "error": "Authentication Required",
                "message": "No valid identity or token found for this request"
            }), 401

        kwargs['authenticated_user'] = username
        kwargs['auth_token'] = token
        return f(*args, **kwargs)

    return decorated_function

def validate_connection_string_format(connection_string):
    """Validate the format of a SQLAlchemy connection string."""
    result = {
        "valid": False,
        "format_valid": False,
        "components": {},
        "issues": [],
        "warnings": []
    }
    if not connection_string or not isinstance(connection_string, str):
        result["issues"].append("Connection string is empty or not a string")
        return result
    if "://" not in connection_string:
        result["issues"].append("Invalid format: missing '://' separator")
        return result
    try:
        url = make_url(connection_string)
        result["format_valid"] = True
        result["components"] = {
            "dialect": url.drivername.split('+')[0] if '+' in url.drivername else url.drivername,
            "driver": url.drivername.split('+')[1] if '+' in url.drivername else None,
            "username": url.username,
            "password": "***" if url.password else None,
            "host": url.host,
            "port": url.port,
            "database": url.database,
        }
        valid_dialects = ['postgresql', 'mysql', 'sqlite', 'oracle', 'mssql', 'mariadb']
        if result["components"]["dialect"] not in valid_dialects:
            result["warnings"].append(f"Dialect '{result['components']['dialect']}' may not be supported")
        if result["components"]["dialect"] == "sqlite":
            if url.host and url.host != "localhost":
                result["warnings"].append("SQLite typically doesn't use host parameter")
        else:
            if not url.host:
                result["issues"].append("Host is required for non-SQLite databases")
            if not url.database:
                result["issues"].append("Database name is required for non-SQLite databases")
        if url.password and re.search(r'[@:/?#\[\]!$&\'()*+,;=]', url.password):
            result["warnings"].append("Password contains special characters - ensure they are URL-encoded")
        result["valid"] = len(result["issues"]) == 0
    except Exception as e:
        result["issues"].append(f"Failed to parse connection string: {str(e)}")
    return result


def validate_host_port(host, port):
    """Validate if host is reachable and port is open."""
    result = {"host_resolvable": False, "port_open": False, "details": {}}
    if not host:
        result["details"]["error"] = "No host specified"
        return result
    try:
        ip_address = socket.gethostbyname(host)
        result["host_resolvable"] = True
        result["details"]["ip_address"] = ip_address
    except socket.gaierror as e:
        result["details"]["host_error"] = f"Cannot resolve host '{host}': {str(e)}"
        return result
    if port:
        try:
            port_num = int(port)
            if port_num < 1 or port_num > 65535:
                result["details"]["port_error"] = f"Port {port_num} is out of valid range (1-65535)"
                return result
        except (ValueError, TypeError):
            result["details"]["port_error"] = f"Invalid port: {port}"
            return result
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result_code = sock.connect_ex((host, port_num))
            sock.close()
            if result_code == 0:
                result["port_open"] = True
                result["details"]["port_status"] = f"Port {port_num} is open"
            else:
                result["details"]["port_status"] = f"Port {port_num} is closed or filtered"
        except socket.error as e:
            result["details"]["port_error"] = f"Error checking port {port_num}: {str(e)}"
    else:
        result["details"]["port_warning"] = "No port specified (using default)"
    return result


def validate_database_connection(connection_string):
    """Validate actual database connection by attempting to connect and run a simple query."""
    result = {"can_connect": False, "can_execute": False, "details": {}}
    try:
        test_engine = create_engine(
            connection_string,
            echo=False,
            pool_pre_ping=True,
            connect_args={"timeout": 5} if "sqlite" in connection_string.lower() else {},
        )
        with test_engine.connect() as conn:
            result["can_connect"] = True
            result["details"]["connection_status"] = "Successfully connected"
            try:
                conn.execute(text("SELECT 1"))
                result["can_execute"] = True
                result["details"]["query_status"] = "Successfully executed test query"
            except Exception as e:
                result["details"]["query_error"] = f"Failed to execute test query: {str(e)}"
            try:
                result["details"]["dialect"] = test_engine.dialect.name
                result["details"]["driver"] = test_engine.driver
            except Exception:
                pass
        test_engine.dispose()
    except SQLAlchemyError as e:
        result["details"]["connection_error"] = str(e.orig) if hasattr(e, "orig") else str(e)
    except Exception as e:
        result["details"]["error"] = str(e)
    return result


def validate_connection_complete(connection_string):
    """Perform complete validation: format, network (if applicable), and actual connection."""
    validation = {
        "connection_string": connection_string,
        "overall_valid": False,
        "format_validation": {},
        "network_validation": {},
        "connection_validation": {},
        "summary": {
            "format_valid": False,
            "network_accessible": False,
            "connection_successful": False,
        },
    }
    format_result = validate_connection_string_format(connection_string)
    validation["format_validation"] = format_result
    validation["summary"]["format_valid"] = format_result["valid"]
    if not format_result["valid"]:
        validation["summary"]["message"] = "Connection string format is invalid"
        return validation
    components = format_result["components"]
    if components.get("dialect") != "sqlite":
        network_result = validate_host_port(components.get("host"), components.get("port"))
        validation["network_validation"] = network_result
        validation["summary"]["network_accessible"] = network_result.get("host_resolvable", False) and (
            network_result.get("port_open", False) or components.get("port") is None
        )
        if not network_result.get("host_resolvable", False):
            validation["summary"]["message"] = "Host is not resolvable"
            return validation
    else:
        validation["network_validation"] = {"note": "Network validation skipped for SQLite"}
        validation["summary"]["network_accessible"] = True
    connection_result = validate_database_connection(connection_string)
    validation["connection_validation"] = connection_result
    validation["summary"]["connection_successful"] = connection_result.get("can_connect", False)
    validation["overall_valid"] = validation["summary"]["format_valid"] and validation["summary"][
        "connection_successful"
    ]
    if validation["overall_valid"]:
        validation["summary"]["message"] = "Connection string is valid and working"
    elif not validation["summary"]["connection_successful"]:
        validation["summary"]["message"] = "Connection string format is valid but connection failed"
    return validation

def build_connection_string_from_params(params):
    """
    Build and validate a SQLAlchemy connection string from individual parameters.

    Parameters:
        params (dict): Dictionary containing connection parameters:
            - dialect (required): Database dialect (postgresql, mysql, sqlite, oracle, mssql, mariadb)
            - driver (optional): Database driver (e.g., psycopg2, pymysql, mysqlconnector)
            - username (optional): Database username
            - password (optional): Database password
            - host (optional): Database host (required for non-SQLite)
            - port (optional): Database port
            - database (required): Database name or path
            - query (optional): Additional query parameters as dict

    Returns:
        dict: Result containing connection_string, validation details, and parameter-specific errors
    """
    result = {
        "success": False,
        "connection_string": None,
        "validation": {},
        "parameter_errors": {},
        "parameter_warnings": {}
    }

    # Validate required parameter: dialect
    dialect = params.get("dialect", "").lower().strip()
    if not dialect:
        result["parameter_errors"]["dialect"] = "Dialect is required (e.g., postgresql, mysql, sqlite, oracle, mssql)"
        return result

    valid_dialects = ['postgresql', 'mysql', 'sqlite', 'oracle', 'mssql', 'mariadb']
    if dialect not in valid_dialects:
        result["parameter_errors"]["dialect"] = f"Invalid dialect '{dialect}'. Valid options: {', '.join(valid_dialects)}"
        return result

    # Validate driver (optional)
    driver = params.get("driver", "").strip()
    if driver:
        # Common driver validations
        valid_drivers = {
            'postgresql': ['psycopg2', 'pg8000', 'psycopg'],
            'mysql': ['pymysql', 'mysqlconnector', 'mysqldb'],
            'mariadb': ['pymysql', 'mysqlconnector', 'mariadbconnector'],
            'sqlite': ['pysqlite'],
            'oracle': ['cx_oracle', 'oracledb'],
            'mssql': ['pyodbc', 'pymssql']
        }

        if dialect in valid_drivers and driver not in valid_drivers[dialect]:
            result["parameter_warnings"]["driver"] = f"Driver '{driver}' may not be compatible with {dialect}. Common drivers: {', '.join(valid_drivers[dialect])}"

    # Validate database (required)
    database = params.get("database", "").strip()
    if not database:
        result["parameter_errors"]["database"] = "Database name or path is required"
        return result

    # For SQLite, validate database path format
    if dialect == "sqlite":
        if not database.endswith('.db') and not database.endswith('.sqlite') and not database.endswith('.sqlite3') and database != ':memory:':
            result["parameter_warnings"]["database"] = "SQLite database should typically end with .db, .sqlite, .sqlite3, or be ':memory:'"

    # Validate host (required for non-SQLite)
    host = params.get("host", "").strip()
    if dialect != "sqlite":
        if not host:
            result["parameter_errors"]["host"] = f"Host is required for {dialect} databases"
            return result

        # Validate host format (basic check)
        if not re.match(r'^[a-zA-Z0-9.-]+$', host) and host != 'localhost':
            result["parameter_errors"]["host"] = f"Invalid host format '{host}'. Host should contain only letters, numbers, dots, and hyphens"
            return result
    else:
        if host and host != 'localhost':
            result["parameter_warnings"]["host"] = "SQLite typically doesn't use host parameter (will be ignored)"

    # Validate port (optional, but validate if provided)
    port = params.get("port")
    if port is not None:
        try:
            port_num = int(port)
            if port_num < 1 or port_num > 65535:
                result["parameter_errors"]["port"] = f"Port must be between 1 and 65535, got {port_num}"
                return result
            port = port_num
        except (ValueError, TypeError):
            result["parameter_errors"]["port"] = f"Invalid port '{port}'. Port must be a number between 1 and 65535"
            return result

        # Check for common default ports
        default_ports = {
            'postgresql': 5432,
            'mysql': 3306,
            'mariadb': 3306,
            'oracle': 1521,
            'mssql': 1433
        }

        if dialect in default_ports and port != default_ports[dialect]:
            result["parameter_warnings"]["port"] = f"Non-standard port {port} for {dialect} (default is {default_ports[dialect]})"

    # Validate username (optional for SQLite, recommended for others)
    username = params.get("username", "").strip()
    if dialect != "sqlite" and not username:
        result["parameter_warnings"]["username"] = f"Username is typically required for {dialect} databases"

    # Validate password (optional)
    password = params.get("password", "")
    if password and re.search(r'[@:/?#\[\]!$&\'()*+,;=]', password):
        result["parameter_warnings"]["password"] = "Password contains special characters - will be automatically URL-encoded"
        # URL encode the password
        from urllib.parse import quote_plus
        password = quote_plus(password)

    # Return early if there are parameter errors
    if result["parameter_errors"]:
        return result

    # Build connection string
    try:
        # Start with dialect
        drivername = f"{dialect}+{driver}" if driver else dialect

        # Build connection string based on dialect
        if dialect == "sqlite":
            # SQLite format: sqlite:///path/to/database.db or sqlite:///absolute/path
            # For relative paths, use three slashes
            # For absolute paths on Windows (C:\...), use four slashes: sqlite:////C:/...
            if database == ':memory:':
                connection_string = f"{drivername}:///:memory:"
            elif database.startswith('/') or (len(database) > 1 and database[1] == ':'):
                # Absolute path
                connection_string = f"{drivername}:///{database}"
            else:
                # Relative path
                connection_string = f"{drivername}:///{database}"
        else:
            # Standard format: dialect://username:password@host:port/database
            auth = ""
            if username:
                auth = username
                if password:
                    auth = f"{auth}:{password}"
                auth = f"{auth}@"

            port_part = f":{port}" if port else ""
            connection_string = f"{drivername}://{auth}{host}{port_part}/{database}"

        # Add query parameters if provided
        query_params = params.get("query")
        if query_params and isinstance(query_params, dict):
            from urllib.parse import urlencode
            query_string = urlencode(query_params)
            connection_string = f"{connection_string}?{query_string}"

        result["connection_string"] = connection_string

        # Now validate the constructed connection string
        validation = validate_connection_complete(connection_string)
        result["validation"] = validation
        result["success"] = validation["overall_valid"]

        # If validation failed, extract specific error details
        if not validation["overall_valid"]:
            result["validation_summary"] = validation.get("summary", {})

            # Extract format errors
            format_validation = validation.get("format_validation", {})
            if format_validation.get("issues"):
                result["parameter_errors"]["connection_string"] = "; ".join(format_validation["issues"])

            # Extract connection errors
            conn_validation = validation.get("connection_validation", {})
            if conn_validation.get("details", {}).get("connection_error"):
                result["connection_error"] = conn_validation["details"]["connection_error"]

        return result

    except Exception as e:
        result["parameter_errors"]["general"] = f"Failed to build connection string: {str(e)}"
        return result


def load_config():
    """Load configuration from YAML file."""
    try:
        with open(CONFIG_FILE, "r") as file:
            config = yaml.safe_load(file)
            if not isinstance(config, dict):
                raise ValueError("Invalid configuration format. Expected a dictionary.")
            return config
    except FileNotFoundError:
        return {"error": "Configuration file not found."}
    except (yaml.YAMLError, ValueError) as e:
        return {"error": f"Failed to load configuration: {str(e)}"}


def get_server_config():
    """Get server configuration from YAML file with defaults."""
    config = load_config()

    if "error" in config:
        logger.warning(f"{config['error']}. Using default server configuration.")
        return {
            "host": "127.0.0.1",
            "port": 8000,
            "debug": False,
            "ssl_enabled": False,
            "ssl_cert": None,
            "ssl_key": None,
            "name": "SimpliqData",
            "version": "1.0.0"
        }

    # Get server config with defaults
    server_config = config.get("server", {})

    return {
        "host": server_config.get("host", "127.0.0.1"),
        "port": server_config.get("port", 8000),
        "debug": server_config.get("debug", False),
        "ssl_enabled": server_config.get("ssl_enabled", False),
        "ssl_cert": server_config.get("ssl_cert"),
        "ssl_key": server_config.get("ssl_key"),
        "name": server_config.get("name", "SimpliqData"),
        "version": server_config.get("version", "1.0.0")
    }


def get_auth_config():
    """Get authentication configuration from YAML file with defaults."""
    config = load_config()

    if "error" in config:
        return {
            "type": "mcp",
            "require_auth_for_all": False,
            "auth_required_message": "Authentication required. Please login first using the 'user_login' tool."
        }

    # Get authentication config with defaults
    auth_config = config.get("authentication", {})

    default_message = """Authentication required to use this endpoint.

Please login first using the 'user_login' tool with your credentials.

Example:
{
  "tool": "user_login",
  "arguments": {
    "username": "your_username",
    "password": "your_password"
  }
}

After successful login, you'll receive a session token that will be automatically
used for subsequent authenticated requests.

If you don't have an account yet, please contact your administrator or use the
'create_user' tool to create one (if available)."""

    # Read and normalize authentication type; default is 'mcp'
    configured_type_raw = auth_config.get("type", "mcp")
    try:
        configured_type = str(configured_type_raw).strip().lower() if configured_type_raw is not None else "mcp"
    except Exception:
        configured_type = "mcp"

    # Support 'mcp', 'client' passthrough, and 'apikey'. Any other becomes 'mcp'.
    supported_types = {"mcp", "client", "apikey", "oauth"}
    effective_type = configured_type if configured_type in supported_types else "mcp"
    if effective_type != configured_type:
        try:
            logger.warning(f"Unsupported authentication.type='{configured_type_raw}' in config.yml; falling back to '{effective_type}'")
        except Exception:
            pass

    return {
        "type": effective_type,
        "require_auth_for_all": auth_config.get("require_auth_for_all", False),
        "auth_required_message": auth_config.get("auth_required_message", default_message)
    }


def check_auth_required(tool_name, rpc_id):
    """
    Check if authentication is required for all endpoints.

    This function checks both OAuth 2.0 and legacy JWT session authentication.
    If OAuth is enabled and valid, legacy auth is not required.

    Returns:
        tuple: (requires_auth, error_response)
               - requires_auth: bool indicating if auth check should be enforced
               - error_response: JSON response to return if auth is required but user is not authenticated
    """
    # Tools that should always allow unauthenticated access
    ALWAYS_ALLOW_UNAUTH = [
        "user_login",      # Obviously needs to work without auth
        "create_user"      # Allow user creation without auth (can be changed per use case)
    ]

    # If tool is in the allow list, don't require auth
    if tool_name in ALWAYS_ALLOW_UNAUTH:
        return False, None

    # PRIORITY 1: Check if OAuth is active and valid
    # If OAuth authentication is present and valid in Flask's g context,
    # that's sufficient - no need for legacy auth
    print(f"\n>>> [DEBUG check_auth_required] Checking OAuth:")
    print(f">>>   - hasattr(g, 'oauth_user_info'): {hasattr(g, 'oauth_user_info')}")
    if hasattr(g, 'oauth_user_info'):
        print(f">>>   - g.oauth_user_info: {g.oauth_user_info}")
        print(f">>>   - bool(g.oauth_user_info): {bool(g.oauth_user_info)}")

    if hasattr(g, 'oauth_user_info') and g.oauth_user_info:
        logger.debug(f"OAuth authentication found for tool '{tool_name}' - allowing access")
        print(f">>> [DEBUG check_auth_required] OAuth found - ALLOWING ACCESS")
        return False, None
    else:
        print(f">>> [DEBUG check_auth_required] OAuth NOT found - checking legacy auth")

    # PRIORITY 2: Check legacy auth configuration
    auth_config = get_auth_config()

    # If require_auth_for_all is disabled, don't enforce
    if not auth_config.get("require_auth_for_all", False):
        return False, None

    # PRIORITY 3: Check if user is authenticated via legacy JWT session
    authenticated_user, _ = get_authenticated_user()

    # If user is authenticated via legacy method, allow access
    if authenticated_user:
        return False, None

    # User is not authenticated via any method and auth is required
    logger.warning(f"Tool '{tool_name}' requires authentication but user is not authenticated (checked OAuth and legacy auth)")

    error_response = jsonify({
        "jsonrpc": "2.0",
        "id": rpc_id,
        "error": {
            "code": -32600,
            "message": "Authentication Required",
            "data": {
                "details": auth_config.get("auth_required_message"),
                "hint": "Use OAuth 2.0 Bearer token or the 'user_login' tool to authenticate"
            }
        }
    }), 401

    return True, error_response


def create_ssl_context(cert_path, key_path):
    """Create SSL context for HTTPS server."""
    try:
        # Check if certificate files exist
        if not os.path.exists(cert_path):
            raise FileNotFoundError(f"SSL certificate file not found: {cert_path}")
        if not os.path.exists(key_path):
            raise FileNotFoundError(f"SSL key file not found: {key_path}")

        # Create SSL context
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(cert_path, key_path)

        # Set secure options (recommended for production)
        context.minimum_version = ssl.TLSVersion.TLSv1_2

        return context
    except Exception as e:
        raise RuntimeError(f"Failed to create SSL context: {str(e)}")


def _update_connection_string_preserving_file(new_connection_string: str) -> None:
    """Update only the 'connection_string' line in the YAML file, preserving comments and layout.

    This avoids rewriting the entire YAML (which would drop comments) and fixes the bug
    where we previously replaced the whole file content with a minimal dict.
    """
    try:
        # Read current file content
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            content = f.read()

        # Regex to replace the connection_string line while keeping indentation
        # Matches: optional spaces, 'connection_string', optional spaces, ':', rest of line
        pattern = re.compile(r"(?m)^(?P<indent>\s*)connection_string\s*:\s*.*$")
        replacement = None

        def _repl(m):
            indent = m.group('indent') or ''
            return f"{indent}connection_string: {new_connection_string}"

        if pattern.search(content):
            new_content = pattern.sub(_repl, content, count=1)
        else:
            # If key not present, append it to the end with a newline, preserving file as-is
            sep = '' if content.endswith('\n') else '\n'
            new_content = content + f"{sep}connection_string: {new_connection_string}\n"

        # Create a simple backup before writing
        try:
            with open(CONFIG_FILE + '.bak', 'w', encoding='utf-8') as fb:
                fb.write(content)
        except Exception:
            # Backup failures shouldn't block the main write
            pass

        # Atomic-ish write
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            f.write(new_content)
    except FileNotFoundError:
        # If no file yet, create a minimal file with just the updated key
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            f.write(f"connection_string: {new_connection_string}\n")


def _deep_merge_dict(dst: dict, src: dict) -> dict:
    """Recursively merge src into dst and return dst."""
    for k, v in (src or {}).items():
        if isinstance(v, dict) and isinstance(dst.get(k), dict):
            _deep_merge_dict(dst[k], v)
        else:
            dst[k] = v
    return dst


def save_config(config: dict):
    """Safely save configuration updates to YAML without wiping other settings.

    - If only 'connection_string' is provided, update the line in-place to preserve comments.
    - Otherwise, load existing YAML, deep-merge keys, and write back (comments may be lost).
    """
    if list(config.keys()) == ["connection_string"] or (
        len(config.keys()) == 1 and "connection_string" in config
    ):
        _update_connection_string_preserving_file(config.get("connection_string", ""))
        return

    # General case: deep-merge and write back
    existing = {}
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            loaded = yaml.safe_load(f)
            if isinstance(loaded, dict):
                existing = loaded
    except Exception:
        existing = {}

    merged = _deep_merge_dict(existing, config or {})

    # Backup current file
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            prev = f.read()
        with open(CONFIG_FILE + '.bak', 'w', encoding='utf-8') as fb:
            fb.write(prev)
    except Exception:
        pass

    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
        yaml.safe_dump(merged, file, sort_keys=False, allow_unicode=True)


def connect_to_db(connection_string=None):
    """Connect to the database using the connection string from config or parameter.
    
    Args:
        connection_string: Optional connection string. If not provided, loads from config.yml
    """
    global engine
    
    if not connection_string:
        config = load_config()
        
        if "error" in config:
            raise ValueError(config["error"])
        
        connection_string = config.get("connection_string")
    
    if connection_string:
        engine = create_engine(connection_string)
        # Test the connection
        with engine.connect() as conn:
            pass

        # Initialize plugins with database connection
        try:
            plugin_registry.initialize_all(engine, semantic_catalog)
            logger.info("Plugins initialized with database connection")
        except Exception as e:
            logger.warning(f"Failed to initialize plugins: {e}")


def disconnect_from_db():
    """Disconnect from the database."""
    global engine
    if engine:
        engine.dispose()
        engine = None


def get_db_info(connection_string):
    """Extract database information from connection string."""
    try:
        parsed = urlparse(connection_string)
        return {
            "database_type": parsed.scheme.split('+')[0],
            "driver": parsed.scheme.split('+')[1] if '+' in parsed.scheme else None,
            "host": parsed.hostname,
            "port": parsed.port,
            "database": parsed.path.lstrip('/') if parsed.path else None,
            "username": parsed.username
        }
    except Exception as e:
        return {"error": f"Failed to parse connection string: {str(e)}"}


@app.route("/", methods=["GET", "POST", "HEAD", "OPTIONS"])
def root():
    """MCP server discovery and tool execution endpoint."""
    print(f"\n>>> [{request.method}] Request to / endpoint")
    logger.info(f"Received {request.method} request to / endpoint")
    logger.debug(f"Request details: method={request.method}, path={request.path}, headers={dict(request.headers)}")

    if request.method == "OPTIONS":
        # CORS preflight
        return "", 204

    if request.method == "HEAD":
        # HEAD request - return MCP protocol version header for Claude.ai discovery
        response = Response("", 200)
        response.headers["MCP-Protocol-Version"] = "2025-06-18"
        return response

    if request.method == "GET":
        # Calcula dinamicamente a contagem de ferramentas (mantemos a lista inline para simplicidade)
        discovery_tools = [
            {"name": "get_config", "description": "Get current database configuration and connection information", "inputSchema": {"type": "object", "properties": {}}},
            {"name": "update_config", "description": "Update database connection string", "inputSchema": {"type": "object", "properties": {"connection_string": {"type": "string", "description": "SQLAlchemy connection string"}}, "required": ["connection_string"]}},
            {"name": "check_status", "description": "Check database connection status", "inputSchema": {"type": "object", "properties": {}}},
            {"name": "list_objects", "description": "List database objects (schemas, tables, views)", "inputSchema": {"type": "object", "properties": {}}},
            {"name": "execute_sql", "description": "Execute a read-only SQL query (SELECT) against the active database connection", "inputSchema": {"type": "object", "properties": {"sql": {"type": "string", "description": "SQL query to execute (SELECT statements only)"}, "timeout": {"type": "integer", "description": "Query timeout in seconds (default: 30, max: 300)", "minimum": 1, "maximum": 300}, "limit": {"type": "integer", "description": "Maximum number of rows to return (default: 1000, max: 10000)", "minimum": 1, "maximum": 10000}, "include_metadata": {"type": "boolean", "description": "Include column metadata in response (default: false)"}}, "required": ["sql"]}},
            {"name": "run_query", "description": "Alias of execute_sql. Execute a read-only SQL SELECT query with optional timeout, limit, and metadata.", "inputSchema": {"type": "object", "properties": {"sql": {"type": "string", "description": "SQL SELECT query"}, "timeout": {"type": "integer", "description": "Query timeout in seconds (default: 30, max: 300)", "minimum": 1, "maximum": 300}, "limit": {"type": "integer", "description": "Maximum number of rows to return (default: 1000, max: 10000)", "minimum": 1, "maximum": 10000}, "include_metadata": {"type": "boolean", "description": "Include column metadata in response (default: false)"}}, "required": ["sql"]}},
            {"name": "describe_table", "description": "Get complete schema information for a database table (columns, types, primary keys, foreign keys, indexes)", "inputSchema": {"type": "object", "properties": {"table_name": {"type": "string", "description": "Name of the table to describe"}, "schema": {"type": "string", "description": "Optional schema name"}}, "required": ["table_name"]}},
            {"name": "get_table_relationships", "description": "Get all foreign key relationships between tables in the database", "inputSchema": {"type": "object", "properties": {"schema": {"type": "string", "description": "Optional schema name to filter tables"}}}},
            {"name": "connect", "description": "Connect to the database", "inputSchema": {"type": "object", "properties": {}}},
            {"name": "disconnect", "description": "Disconnect from the database", "inputSchema": {"type": "object", "properties": {}}},
            {"name": "validate_connection", "description": "Validate a database connection string (format, network, and actual connection)", "inputSchema": {"type": "object", "properties": {"connection_string": {"type": "string", "description": "SQLAlchemy connection string to validate"}}, "required": ["connection_string"]}},
            {"name": "build_connection", "description": "Build and validate a SQLAlchemy connection string from individual parameters (dialect, host, port, database, etc.)", "inputSchema": {"type": "object", "properties": {"dialect": {"type": "string"}, "driver": {"type": "string"}, "username": {"type": "string"}, "password": {"type": "string"}, "host": {"type": "string"}, "port": {"type": "integer"}, "database": {"type": "string"}, "query": {"type": "object"}}, "required": ["dialect", "database"]}},
            {"name": "create_user", "description": "Create a new user in the multi-user system. Super admins can create users with any role in any organization. Org admins can create common or org_admin users in their organization.", "inputSchema": {"type": "object", "properties": {"username": {"type": "string", "description": "Unique username"}, "password": {"type": "string", "description": "User password"}, "email": {"type": "string", "description": "User email address"}, "full_name": {"type": "string", "description": "User's full name (optional)"}, "role": {"type": "string", "description": "User role: common, org_admin, or super_admin (default: common)", "enum": ["common", "org_admin", "super_admin"]}, "organization_id": {"type": "string", "description": "Organization ID (UUID). If not specified, uses default organization."}}, "required": ["username", "password", "email"]}},
            {"name": "user_login", "description": "Authenticate a user and get session token", "inputSchema": {"type": "object", "properties": {"username": {"type": "string"}, "password": {"type": "string"}}, "required": ["username", "password"]}},
            {"name": "user_logout", "description": "Logout and clear stored session", "inputSchema": {"type": "object", "properties": {}}},
            {"name": "server_logout", "description": "Clear stored session token on server (same as user_logout alias)", "inputSchema": {"type": "object", "properties": {}}},
            {"name": "whoami", "description": "Return currently authenticated user (if any)", "inputSchema": {"type": "object", "properties": {}}},
            {"name": "list_users", "description": "List all users in the system", "inputSchema": {"type": "object", "properties": {}}},
            {"name": "get_user", "description": "Get details for a specific user (default self)", "inputSchema": {"type": "object", "properties": {"username": {"type": "string"}}}},
            {"name": "update_user", "description": "Update a user (email, full_name, password, role). Super admins can change any user's role. Org admins can promote/demote between common and org_admin in their organization.", "inputSchema": {"type": "object", "properties": {"username": {"type": "string", "description": "Username to update"}, "email": {"type": "string", "description": "New email address"}, "full_name": {"type": "string", "description": "New full name"}, "password": {"type": "string", "description": "New password"}, "role": {"type": "string", "description": "New role: common, org_admin, or super_admin", "enum": ["common", "org_admin", "super_admin"]}}, "required": ["username"]}},
            {"name": "delete_user", "description": "Delete a user", "inputSchema": {"type": "object", "properties": {"username": {"type": "string"}}, "required": ["username"]}},
            {"name": "add_connection", "description": "Add a new database connection for the authenticated user", "inputSchema": {"type": "object", "properties": {"name": {"type": "string"}, "connection_string": {"type": "string"}, "description": {"type": "string"}}, "required": ["name", "connection_string"]}},
            {"name": "list_connections", "description": "List all database connections for the authenticated user", "inputSchema": {"type": "object", "properties": {}}},
            {"name": "get_connection", "description": "Get details of a specific connection", "inputSchema": {"type": "object", "properties": {"connection_id": {"type": "string"}}, "required": ["connection_id"]}},
            {"name": "update_connection", "description": "Update a connection (name, connection_string, description)", "inputSchema": {"type": "object", "properties": {"connection_id": {"type": "string"}, "name": {"type": "string"}, "connection_string": {"type": "string"}, "description": {"type": "string"}}, "required": ["connection_id"]}},
            {"name": "get_active_connection", "description": "Get the currently active connection for the authenticated user", "inputSchema": {"type": "object", "properties": {}}},
            {"name": "activate_connection", "description": "Activate a database connection for the authenticated user", "inputSchema": {"type": "object", "properties": {"connection_id": {"type": "string"}}, "required": ["connection_id"]}},
            {"name": "test_connection", "description": "Test a database connection", "inputSchema": {"type": "object", "properties": {"connection_id": {"type": "string"}}, "required": ["connection_id"]}},
            {"name": "remove_connection", "description": "Remove a database connection for the authenticated user", "inputSchema": {"type": "object", "properties": {"connection_id": {"type": "string"}}, "required": ["connection_id"]}},
            {"name": "create_organization", "description": "Create a new organization (super-admin only)", "inputSchema": {"type": "object", "properties": {"name": {"type": "string"}, "display_name": {"type": "string"}, "description": {"type": "string"}}, "required": ["name"]}},
            {"name": "list_organizations", "description": "List organizations (super-admin sees all, org-admin sees own)", "inputSchema": {"type": "object", "properties": {}}},
            {"name": "get_organization", "description": "Get organization details", "inputSchema": {"type": "object", "properties": {"org_name": {"type": "string"}}, "required": ["org_name"]}},
            {"name": "update_organization", "description": "Update organization (super-admin only)", "inputSchema": {"type": "object", "properties": {"org_name": {"type": "string"}, "display_name": {"type": "string"}, "description": {"type": "string"}, "active": {"type": "boolean"}}, "required": ["org_name"]}},
            {"name": "delete_organization", "description": "Delete organization (super-admin only)", "inputSchema": {"type": "object", "properties": {"org_name": {"type": "string"}}, "required": ["org_name"]}},
            {"name": "list_organization_users", "description": "List all users in an organization", "inputSchema": {"type": "object", "properties": {"org_name": {"type": "string"}}, "required": ["org_name"]}},
            {"name": "list_organization_connections", "description": "List all database connections in an organization", "inputSchema": {"type": "object", "properties": {"org_name": {"type": "string"}}, "required": ["org_name"]}},
            {"name": "suggest_semantic_maps", "description": "Auto-suggest semantic entity and relationship mappings from current DB schema (non-destructive)", "inputSchema": {"type": "object", "properties": {"include_columns": {"type": "boolean", "description": "Include column mappings for entities (default: true)"}, "type": {"type": "string", "enum": ["entity", "relationship", "all"], "description": "Suggestion type filter"}, "limit": {"type": "integer", "description": "Max number of suggestions per type"}}}},
            {"name": "create_api_key", "description": "Create a new API key for the authenticated user", "inputSchema": {"type": "object", "properties": {"name": {"type": "string", "description": "Friendly name for the API key"}, "description": {"type": "string", "description": "Optional description"}, "expires_in_days": {"type": "integer", "description": "Days until expiration (1-3650, or omit for no expiration)"}}, "required": ["name"]}},
            {"name": "list_my_api_keys", "description": "List all API keys for the authenticated user", "inputSchema": {"type": "object", "properties": {}}},
            {"name": "revoke_api_key", "description": "Revoke (delete) an API key", "inputSchema": {"type": "object", "properties": {"key_id": {"type": "string", "description": "ID of the API key to revoke"}}, "required": ["key_id"]}},
            {"name": "add_semantic_map", "description": "Add a new semantic mapping between business concepts and database structures", "inputSchema": {"type": "object", "properties": {"concept": {"type": "string"}, "type": {"type": "string", "enum": ["entity", "relationship"]}, "table": {"type": "string"}, "description": {"type": "string"}, "aliases": {"type": "array", "items": {"type": "string"}}, "column_mappings": {"type": "object"}}, "required": ["concept", "type"]}},
            {"name": "list_semantic_maps", "description": "List all semantic mappings for the active connection", "inputSchema": {"type": "object", "properties": {"type": {"type": "string", "enum": ["entity", "relationship"]}}}},
            {"name": "get_semantic_mapping", "description": "Get complete details of a specific semantic mapping by ID", "inputSchema": {"type": "object", "properties": {"mapping_id": {"type": "string", "description": "ID of the mapping to retrieve"}}, "required": ["mapping_id"]}},
            {"name": "update_semantic_map", "description": "Update an existing semantic mapping", "inputSchema": {"type": "object", "properties": {"mapping_id": {"type": "string"}, "description": {"type": "string"}, "aliases": {"type": "array"}}, "required": ["mapping_id"]}},
            {"name": "delete_semantic_map", "description": "Delete a semantic mapping", "inputSchema": {"type": "object", "properties": {"mapping_id": {"type": "string"}}, "required": ["mapping_id"]}}
        ]
        print(f">>> Returning server discovery info ({len(discovery_tools)} tools)")
        logger.info("Processing GET request - returning server discovery info")
        logger.debug(f"GET request handler: Preparing to return {len(discovery_tools)} MCP tools")
        # Discovery endpoint - return server info and available tools
        return jsonify({
            "name": "SimpliqData",
            "version": "1.0.0",
            "description": "A minimal MCP server for database connection management",
            "protocol": "mcp",
            "capabilities": {"tools": True, "prompts": True, "resources": False},
            "tools": [
                {"name": "get_config", "description": "Get current database configuration and connection information", "inputSchema": {"type": "object", "properties": {}}},
                {"name": "update_config", "description": "Update database connection string", "inputSchema": {"type": "object", "properties": {"connection_string": {"type": "string", "description": "SQLAlchemy connection string"}}, "required": ["connection_string"]}},
                {"name": "check_status", "description": "Check database connection status", "inputSchema": {"type": "object", "properties": {}}},
                {"name": "list_objects", "description": "List database objects (schemas, tables, views)", "inputSchema": {"type": "object", "properties": {}}},
                {"name": "execute_sql", "description": "Execute a read-only SQL query (SELECT) against the active database connection", "inputSchema": {"type": "object", "properties": {"sql": {"type": "string", "description": "SQL query to execute (SELECT statements only)"}, "timeout": {"type": "integer", "description": "Query timeout in seconds (default: 30, max: 300)", "minimum": 1, "maximum": 300}, "limit": {"type": "integer", "description": "Maximum number of rows to return (default: 1000, max: 10000)", "minimum": 1, "maximum": 10000}, "include_metadata": {"type": "boolean", "description": "Include column metadata in response (default: false)"}}, "required": ["sql"]}},
                {"name": "run_query", "description": "Alias of execute_sql. Execute a read-only SQL SELECT query with optional timeout, limit, and metadata.", "inputSchema": {"type": "object", "properties": {"sql": {"type": "string", "description": "SQL SELECT query"}, "timeout": {"type": "integer", "description": "Query timeout in seconds (default: 30, max: 300)", "minimum": 1, "maximum": 300}, "limit": {"type": "integer", "description": "Maximum number of rows to return (default: 1000, max: 10000)", "minimum": 1, "maximum": 10000}, "include_metadata": {"type": "boolean", "description": "Include column metadata in response (default: false)"}}, "required": ["sql"]}},
                {"name": "describe_table", "description": "Get complete schema information for a database table (columns, types, primary keys, foreign keys, indexes)", "inputSchema": {"type": "object", "properties": {"table_name": {"type": "string", "description": "Name of the table to describe"}, "schema": {"type": "string", "description": "Optional schema name"}}, "required": ["table_name"]}},
                {"name": "get_table_relationships", "description": "Get all foreign key relationships between tables in the database", "inputSchema": {"type": "object", "properties": {"schema": {"type": "string", "description": "Optional schema name to filter tables"}}}},
                {"name": "connect", "description": "Connect to the database", "inputSchema": {"type": "object", "properties": {}}},
                {"name": "disconnect", "description": "Disconnect from the database", "inputSchema": {"type": "object", "properties": {}}},
                {"name": "validate_connection", "description": "Validate a database connection string (format, network, and actual connection)", "inputSchema": {"type": "object", "properties": {"connection_string": {"type": "string", "description": "SQLAlchemy connection string to validate"}}, "required": ["connection_string"]}},
                {"name": "build_connection", "description": "Build and validate a SQLAlchemy connection string from individual parameters (dialect, host, port, database, etc.)", "inputSchema": {"type": "object", "properties": {"dialect": {"type": "string"}, "driver": {"type": "string"}, "username": {"type": "string"}, "password": {"type": "string"}, "host": {"type": "string"}, "port": {"type": "integer"}, "database": {"type": "string"}, "query": {"type": "object"}}, "required": ["dialect", "database"]}},
                {"name": "create_user", "description": "Create a new user in the multi-user system. Super admins can create users with any role in any organization. Org admins can create common or org_admin users in their organization.", "inputSchema": {"type": "object", "properties": {"username": {"type": "string", "description": "Unique username"}, "password": {"type": "string", "description": "User password"}, "email": {"type": "string", "description": "User email address"}, "full_name": {"type": "string", "description": "User's full name (optional)"}, "role": {"type": "string", "description": "User role: common, org_admin, or super_admin (default: common)", "enum": ["common", "org_admin", "super_admin"]}, "organization_id": {"type": "string", "description": "Organization ID (UUID). If not specified, uses default organization."}}, "required": ["username", "password", "email"]}},
                {"name": "user_login", "description": "Authenticate a user and get session token", "inputSchema": {"type": "object", "properties": {"username": {"type": "string"}, "password": {"type": "string"}}, "required": ["username", "password"]}},
                {"name": "user_logout", "description": "Logout and clear stored session", "inputSchema": {"type": "object", "properties": {}}},
                {"name": "server_logout", "description": "Clear stored session token on server (same as user_logout alias)", "inputSchema": {"type": "object", "properties": {}}},
                {"name": "whoami", "description": "Return currently authenticated user (if any)", "inputSchema": {"type": "object", "properties": {}}},
                {"name": "list_users", "description": "List all users in the system", "inputSchema": {"type": "object", "properties": {}}},
                {"name": "get_user", "description": "Get details for a specific user (default self)", "inputSchema": {"type": "object", "properties": {"username": {"type": "string"}}}},
                {"name": "update_user", "description": "Update a user (email, full_name, password, role). Super admins can change any user's role. Org admins can promote/demote between common and org_admin in their organization.", "inputSchema": {"type": "object", "properties": {"username": {"type": "string", "description": "Username to update"}, "email": {"type": "string", "description": "New email address"}, "full_name": {"type": "string", "description": "New full name"}, "password": {"type": "string", "description": "New password"}, "role": {"type": "string", "description": "New role: common, org_admin, or super_admin", "enum": ["common", "org_admin", "super_admin"]}}, "required": ["username"]}},
                {"name": "delete_user", "description": "Delete a user", "inputSchema": {"type": "object", "properties": {"username": {"type": "string"}}, "required": ["username"]}},
                {"name": "add_connection", "description": "Add a new database connection for the authenticated user", "inputSchema": {"type": "object", "properties": {"name": {"type": "string"}, "connection_string": {"type": "string"}, "description": {"type": "string"}}, "required": ["name", "connection_string"]}},
                {"name": "list_connections", "description": "List all database connections for the authenticated user", "inputSchema": {"type": "object", "properties": {}}},
                {"name": "get_connection", "description": "Get details of a specific connection", "inputSchema": {"type": "object", "properties": {"connection_id": {"type": "string"}}, "required": ["connection_id"]}},
                {"name": "update_connection", "description": "Update a connection (name, connection_string, description)", "inputSchema": {"type": "object", "properties": {"connection_id": {"type": "string"}, "name": {"type": "string"}, "connection_string": {"type": "string"}, "description": {"type": "string"}}, "required": ["connection_id"]}},
                {"name": "get_active_connection", "description": "Get the currently active connection for the authenticated user", "inputSchema": {"type": "object", "properties": {}}},
                {"name": "activate_connection", "description": "Activate a database connection for the authenticated user", "inputSchema": {"type": "object", "properties": {"connection_id": {"type": "string"}}, "required": ["connection_id"]}},
                {"name": "test_connection", "description": "Test a database connection", "inputSchema": {"type": "object", "properties": {"connection_id": {"type": "string"}}, "required": ["connection_id"]}},
                {"name": "remove_connection", "description": "Remove a database connection for the authenticated user", "inputSchema": {"type": "object", "properties": {"connection_id": {"type": "string"}}, "required": ["connection_id"]}},
                {"name": "create_organization", "description": "Create a new organization (super-admin only)", "inputSchema": {"type": "object", "properties": {"name": {"type": "string"}, "display_name": {"type": "string"}, "description": {"type": "string"}}, "required": ["name"]}},
                {"name": "list_organizations", "description": "List organizations (super-admin sees all, org-admin sees own)", "inputSchema": {"type": "object", "properties": {}}},
                {"name": "get_organization", "description": "Get organization details", "inputSchema": {"type": "object", "properties": {"org_name": {"type": "string"}}, "required": ["org_name"]}},
                {"name": "update_organization", "description": "Update organization (super-admin only)", "inputSchema": {"type": "object", "properties": {"org_name": {"type": "string"}, "display_name": {"type": "string"}, "description": {"type": "string"}, "active": {"type": "boolean"}}, "required": ["org_name"]}},
                {"name": "delete_organization", "description": "Delete organization (super-admin only)", "inputSchema": {"type": "object", "properties": {"org_name": {"type": "string"}}, "required": ["org_name"]}},
                {"name": "list_organization_users", "description": "List all users in an organization", "inputSchema": {"type": "object", "properties": {"org_name": {"type": "string"}}, "required": ["org_name"]}},
                {"name": "list_organization_connections", "description": "List all database connections in an organization", "inputSchema": {"type": "object", "properties": {"org_name": {"type": "string"}}, "required": ["org_name"]}},
                {"name": "suggest_semantic_maps", "description": "Auto-suggest semantic entity and relationship mappings from current DB schema (non-destructive)", "inputSchema": {"type": "object", "properties": {"include_columns": {"type": "boolean", "description": "Include column mappings for entities (default: true)"}, "type": {"type": "string", "enum": ["entity", "relationship", "all"], "description": "Suggestion type filter"}, "limit": {"type": "integer", "description": "Max number of suggestions per type"}}}},
                {"name": "create_api_key", "description": "Create a new API key for the authenticated user", "inputSchema": {"type": "object", "properties": {"name": {"type": "string", "description": "Friendly name for the API key"}, "description": {"type": "string", "description": "Optional description"}, "expires_in_days": {"type": "integer", "description": "Days until expiration (1-3650, or omit for no expiration)"}}, "required": ["name"]}},
                {"name": "list_my_api_keys", "description": "List all API keys for the authenticated user", "inputSchema": {"type": "object", "properties": {}}},
                {"name": "revoke_api_key", "description": "Revoke (delete) an API key", "inputSchema": {"type": "object", "properties": {"key_id": {"type": "string", "description": "ID of the API key to revoke"}}, "required": ["key_id"]}}
            ]
        })

    # POST method - JSON-RPC 2.0 and tool execution
    if request.method == "POST":
        try:
            data = request.json
            print(f"\n>>> POST Request received")
            print(f">>> Data: {json.dumps(data, indent=2)}")
            logger.info(f"Received JSON-RPC request: {json.dumps(data, indent=2)}")
            logger.debug(f"POST handler: Request content-type={request.content_type}, data size={len(str(data))}")

            # Handle JSON-RPC 2.0 protocol
            if data.get("jsonrpc") == "2.0":
                rpc_method = data.get("method")
                rpc_params = data.get("params", {})
                rpc_id = data.get("id")

                print(f">>> JSON-RPC Method: {rpc_method}")
                logger.info(f"JSON-RPC Method: {rpc_method}")
                logger.debug(f"JSON-RPC details: method={rpc_method}, params={rpc_params}, id={rpc_id}")

                # Handle initialize request
                if rpc_method == "initialize":
                    logger.info("Handling initialize request")
                    # Include full tool list directly in initialize to help clients (VS Code Copilot) discover
                    # all tools without needing an immediate tools/list, and surface user_login early.
                    tools_list = [
                        {"name": "user_login", "description": "Authenticate a user and get session token", "inputSchema": {"type": "object", "properties": {"username": {"type": "string"}, "password": {"type": "string"}}, "required": ["username", "password"]}},
                        {"name": "user_logout", "description": "Logout and clear stored session", "inputSchema": {"type": "object", "properties": {}}},
                        {"name": "server_logout", "description": "Clear stored session token on server (same as user_logout alias)", "inputSchema": {"type": "object", "properties": {}}},
                        {"name": "whoami", "description": "Return currently authenticated user (if any)", "inputSchema": {"type": "object", "properties": {}}},
                        {"name": "get_config", "description": "Get current database configuration and connection information", "inputSchema": {"type": "object", "properties": {}}},
                        {"name": "update_config", "description": "Update database connection string", "inputSchema": {"type": "object", "properties": {"connection_string": {"type": "string", "description": "SQLAlchemy connection string"}}, "required": ["connection_string"]}},
                        {"name": "check_status", "description": "Check database connection status", "inputSchema": {"type": "object", "properties": {}}},
                        {"name": "list_objects", "description": "List database objects (schemas, tables, views)", "inputSchema": {"type": "object", "properties": {}}},
                        {"name": "execute_sql", "description": "Execute a read-only SQL query (SELECT) against the active database connection", "inputSchema": {"type": "object", "properties": {"sql": {"type": "string", "description": "SQL query to execute (SELECT statements only)"}, "timeout": {"type": "integer", "description": "Query timeout in seconds (default: 30, max: 300)", "minimum": 1, "maximum": 300}, "limit": {"type": "integer", "description": "Maximum number of rows to return (default: 1000, max: 10000)", "minimum": 1, "maximum": 10000}, "include_metadata": {"type": "boolean", "description": "Include column metadata in response (default: false)"}}, "required": ["sql"]}},
                        {"name": "run_query", "description": "Alias of execute_sql. Execute a read-only SQL SELECT query with optional timeout, limit, and metadata.", "inputSchema": {"type": "object", "properties": {"sql": {"type": "string", "description": "SQL SELECT query"}, "timeout": {"type": "integer", "description": "Query timeout in seconds (default: 30, max: 300)", "minimum": 1, "maximum": 300}, "limit": {"type": "integer", "description": "Maximum number of rows to return (default: 1000, max: 10000)", "minimum": 1, "maximum": 10000}, "include_metadata": {"type": "boolean", "description": "Include column metadata in response (default: false)"}}, "required": ["sql"]}},
                        {"name": "connect", "description": "Connect to the database", "inputSchema": {"type": "object", "properties": {}}},
                        {"name": "disconnect", "description": "Disconnect from the database", "inputSchema": {"type": "object", "properties": {}}},
                        {"name": "validate_connection", "description": "Validate a database connection string (format, network, and actual connection)", "inputSchema": {"type": "object", "properties": {"connection_string": {"type": "string", "description": "SQLAlchemy connection string to validate"}}, "required": ["connection_string"]}},
                        {"name": "build_connection", "description": "Build and validate a SQLAlchemy connection string from individual parameters (dialect, host, port, database, etc.)", "inputSchema": {"type": "object", "properties": {"dialect": {"type": "string"}, "driver": {"type": "string"}, "username": {"type": "string"}, "password": {"type": "string"}, "host": {"type": "string"}, "port": {"type": "integer"}, "database": {"type": "string"}, "query": {"type": "object"}}, "required": ["dialect", "database"]}},
                        {"name": "create_user", "description": "Create a new user in the multi-user system. Super admins can create users with any role in any organization. Org admins can create common or org_admin users in their organization.", "inputSchema": {"type": "object", "properties": {"username": {"type": "string", "description": "Unique username"}, "password": {"type": "string", "description": "User password"}, "email": {"type": "string", "description": "User email address"}, "full_name": {"type": "string", "description": "User's full name (optional)"}, "role": {"type": "string", "description": "User role: common, org_admin, or super_admin (default: common)", "enum": ["common", "org_admin", "super_admin"]}, "organization_id": {"type": "string", "description": "Organization ID (UUID). If not specified, uses default organization."}}, "required": ["username", "password", "email"]}},
                        {"name": "list_users", "description": "List all users in the system", "inputSchema": {"type": "object", "properties": {}}},
                        {"name": "get_user", "description": "Get details for a specific user (default self)", "inputSchema": {"type": "object", "properties": {"username": {"type": "string"}}}},
                        {"name": "update_user", "description": "Update a user (email, full_name, password, role). Super admins can change any user's role. Org admins can promote/demote between common and org_admin in their organization.", "inputSchema": {"type": "object", "properties": {"username": {"type": "string", "description": "Username to update"}, "email": {"type": "string", "description": "New email address"}, "full_name": {"type": "string", "description": "New full name"}, "password": {"type": "string", "description": "New password"}, "role": {"type": "string", "description": "New role: common, org_admin, or super_admin", "enum": ["common", "org_admin", "super_admin"]}}, "required": ["username"]}},
                        {"name": "delete_user", "description": "Delete a user", "inputSchema": {"type": "object", "properties": {"username": {"type": "string"}}, "required": ["username"]}},
                        {"name": "add_connection", "description": "Add a new database connection for the authenticated user", "inputSchema": {"type": "object", "properties": {"name": {"type": "string"}, "connection_string": {"type": "string"}, "description": {"type": "string"}}, "required": ["name", "connection_string"]}},
                        {"name": "list_connections", "description": "List all database connections for the authenticated user", "inputSchema": {"type": "object", "properties": {}}},
                        {"name": "get_connection", "description": "Get details of a specific connection", "inputSchema": {"type": "object", "properties": {"connection_id": {"type": "string"}}, "required": ["connection_id"]}},
                        {"name": "update_connection", "description": "Update a connection (name, connection_string, description)", "inputSchema": {"type": "object", "properties": {"connection_id": {"type": "string"}, "name": {"type": "string"}, "connection_string": {"type": "string"}, "description": {"type": "string"}}, "required": ["connection_id"]}},
                        {"name": "get_active_connection", "description": "Get the currently active connection for the authenticated user", "inputSchema": {"type": "object", "properties": {}}},
                        {"name": "activate_connection", "description": "Activate a database connection for the authenticated user", "inputSchema": {"type": "object", "properties": {"connection_id": {"type": "string"}}, "required": ["connection_id"]}},
                        {"name": "test_connection", "description": "Test a database connection", "inputSchema": {"type": "object", "properties": {"connection_id": {"type": "string"}}, "required": ["connection_id"]}},
                        {"name": "remove_connection", "description": "Remove a database connection for the authenticated user", "inputSchema": {"type": "object", "properties": {"connection_id": {"type": "string"}}, "required": ["connection_id"]}},
                        {"name": "create_organization", "description": "Create a new organization (super-admin only)", "inputSchema": {"type": "object", "properties": {"name": {"type": "string"}, "display_name": {"type": "string"}, "description": {"type": "string"}}, "required": ["name"]}},
                        {"name": "list_organizations", "description": "List organizations (super-admin sees all, org-admin sees own)", "inputSchema": {"type": "object", "properties": {}}},
                        {"name": "get_organization", "description": "Get organization details", "inputSchema": {"type": "object", "properties": {"org_name": {"type": "string"}}, "required": ["org_name"]}},
                        {"name": "update_organization", "description": "Update organization (super-admin only)", "inputSchema": {"type": "object", "properties": {"org_name": {"type": "string"}, "display_name": {"type": "string"}, "description": {"type": "string"}, "active": {"type": "boolean"}}, "required": ["org_name"]}},
                        {"name": "delete_organization", "description": "Delete organization (super-admin only)", "inputSchema": {"type": "object", "properties": {"org_name": {"type": "string"}}, "required": ["org_name"]}},
                        {"name": "list_organization_users", "description": "List all users in an organization", "inputSchema": {"type": "object", "properties": {"org_name": {"type": "string"}}, "required": ["org_name"]}},
                        {"name": "list_organization_connections", "description": "List all database connections in an organization", "inputSchema": {"type": "object", "properties": {"org_name": {"type": "string"}}, "required": ["org_name"]}},
                        {"name": "suggest_semantic_maps", "description": "Auto-suggest semantic entity and relationship mappings from current DB schema (non-destructive)", "inputSchema": {"type": "object", "properties": {"include_columns": {"type": "boolean", "description": "Include column mappings for entities (default: true)"}, "type": {"type": "string", "enum": ["entity", "relationship", "all"], "description": "Suggestion type filter"}, "limit": {"type": "integer", "description": "Max number of suggestions per type"}}}},
                        {"name": "describe_table", "description": "Get complete schema information for a database table (columns, types, primary keys, foreign keys, indexes)", "inputSchema": {"type": "object", "properties": {"table_name": {"type": "string", "description": "Name of the table to describe"}, "schema": {"type": "string", "description": "Optional schema name"}}, "required": ["table_name"]}},
                        {"name": "get_table_relationships", "description": "Get all foreign key relationships between tables in the database", "inputSchema": {"type": "object", "properties": {"schema": {"type": "string", "description": "Optional schema name to filter tables"}}}},
                        {"name": "create_api_key", "description": "Create a new API key for the authenticated user", "inputSchema": {"type": "object", "properties": {"name": {"type": "string", "description": "Friendly name for the API key"}, "description": {"type": "string", "description": "Optional description"}, "expires_in_days": {"type": "integer", "description": "Days until expiration (1-3650, or omit for no expiration)"}}, "required": ["name"]}},
                        {"name": "list_my_api_keys", "description": "List all API keys for the authenticated user", "inputSchema": {"type": "object", "properties": {}}},
                        {"name": "revoke_api_key", "description": "Revoke (delete) an API key", "inputSchema": {"type": "object", "properties": {"key_id": {"type": "string", "description": "ID of the API key to revoke"}}, "required": ["key_id"]}},
                        {"name": "add_semantic_map", "description": "Add a new semantic mapping between business concepts and database structures", "inputSchema": {"type": "object", "properties": {"concept": {"type": "string"}, "type": {"type": "string", "enum": ["entity", "relationship"]}, "table": {"type": "string"}, "description": {"type": "string"}, "aliases": {"type": "array", "items": {"type": "string"}}, "column_mappings": {"type": "object"}}, "required": ["concept", "type"]}},
                        {"name": "list_semantic_maps", "description": "List all semantic mappings for the active connection", "inputSchema": {"type": "object", "properties": {"type": {"type": "string", "enum": ["entity", "relationship"]}}}},
                        {"name": "update_semantic_map", "description": "Update an existing semantic mapping", "inputSchema": {"type": "object", "properties": {"mapping_id": {"type": "string"}, "description": {"type": "string"}, "aliases": {"type": "array"}}, "required": ["mapping_id"]}},
                        {"name": "delete_semantic_map", "description": "Delete a semantic mapping", "inputSchema": {"type": "object", "properties": {"mapping_id": {"type": "string"}}, "required": ["mapping_id"]}},
                        {"name": "natural_query", "description": "Gerar e opcionalmente executar SQL seguro a partir de linguagem natural usando contexto semântico e de schema", "inputSchema": {"type": "object", "properties": {"query": {"type": "string", "description": "Pergunta em linguagem natural"}, "run_mode": {"type": "string", "enum": ["generate", "execute"], "description": "Se 'execute', roda a consulta e retorna resultados"}, "limit": {"type": "integer", "description": "Máx linhas (default: configurado)"}, "include_sql": {"type": "boolean", "description": "Sempre retornar SQL gerado"}}, "required": ["query"]}}
                    ]
                    return jsonify({
                        "jsonrpc": "2.0",
                        "id": rpc_id,
                        "result": {
                            "protocolVersion": "2024-11-05",
                            "capabilities": {
                                "tools": {},
                                "prompts": {},
                                "resources": {},
                                "logging": {}
                            },
                            "serverInfo": {
                                "name": "SimpliqData",
                                "version": "1.0.0"
                            },
                            "tools": tools_list
                        }
                    })
                
                # Handle prompts/list request
                elif rpc_method == "prompts/list":
                    prompts = [
                        {
                            "name": "how_to_query",
                            "description": "Guia rápido para executar consultas SQL com execute_sql/run_query",
                            "arguments": []
                        }
                    ]
                    return jsonify({
                        "jsonrpc": "2.0",
                        "id": rpc_id,
                        "result": {"prompts": prompts}
                    })

                # Handle prompts/get request
                elif rpc_method == "prompts/get":
                    prompt_name = rpc_params.get("name")
                    if prompt_name == "how_to_query":
                        messages = [
                            {
                                "role": "system",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": (
                                            "Como consultar o banco de dados via MCP:\n\n"
                                            "1) Autentique-se: use a ferramenta user_login.\n"
                                            "2) Conecte ao banco: use update_config (se necessário) e depois connect.\n"
                                            "3) Execute sua consulta:\n"
                                            "   - Ferramenta: run_query (alias de execute_sql)\n"
                                            "   - Parâmetros: sql (obrigatório), timeout (opcional), limit (opcional), include_metadata (opcional)\n\n"
                                            "Exemplos:\n"
                                            "- run_query { sql: \"SELECT * FROM users LIMIT 5\" }\n"
                                            "- execute_sql { sql: \"SELECT name, email FROM users ORDER BY created_at DESC LIMIT 10\", include_metadata: true }\n\n"
                                            "Observações:\n"
                                            "- Apenas SELECT (somente leitura).\n"
                                            "- É necessário estar autenticado e com conexão ativa (engine) antes de executar."
                                        )
                                    }
                                ]
                            }
                        ]
                        return jsonify({
                            "jsonrpc": "2.0",
                            "id": rpc_id,
                            "result": {
                                "name": "how_to_query",
                                "description": "Guia rápido para executar consultas SQL com execute_sql/run_query",
                                "messages": messages
                            }
                        })
                    else:
                        return jsonify({
                            "jsonrpc": "2.0",
                            "id": rpc_id,
                            "error": {"code": -32601, "message": f"Prompt '{prompt_name}' não encontrado"}
                        }), 404
                
                # Handle resources/list request
                elif rpc_method == "resources/list":
                    return jsonify({
                        "jsonrpc": "2.0",
                        "id": rpc_id,
                        "result": {
                            "resources": []
                        }
                    })
                
                # Handle logging/setLevel request
                elif rpc_method == "logging/setLevel":
                    # Accept but ignore logging level changes for now
                    return jsonify({
                        "jsonrpc": "2.0",
                        "id": rpc_id,
                        "result": {}
                    })
                
                # Handle notifications (id is null)
                elif rpc_id is None:
                    # Notifications don't require a response, but we'll return 200 OK
                    # Common notifications: notifications/initialized, notifications/cancelled, etc.
                    return '', 204  # No Content - successful notification received
                
                # Handle tools/list request
                elif rpc_method == "tools/list":
                    # IMPORTANT: tools/list must be PUBLIC (no authentication required)
                    # This allows Claude Desktop to discover available tools before authentication
                    # Individual tool calls will validate OAuth as needed
                    logger.debug("Processing tools/list request (public endpoint)")

                    # Monta dinamicamente a lista de ferramentas e registra a contagem correta
                    tools_jsonrpc = [
                        {"name": "user_login", "description": "Authenticate a user and get session token", "inputSchema": {"type": "object", "properties": {"username": {"type": "string"}, "password": {"type": "string"}}, "required": ["username", "password"]}},
                        {"name": "user_logout", "description": "Logout and clear stored session", "inputSchema": {"type": "object", "properties": {}}},
                        {"name": "server_logout", "description": "Clear stored session token on server (same as user_logout alias)", "inputSchema": {"type": "object", "properties": {}}},
                        {"name": "whoami", "description": "Return currently authenticated user (if any)", "inputSchema": {"type": "object", "properties": {}}},
                        {"name": "get_config", "description": "Get current database configuration and connection information", "inputSchema": {"type": "object", "properties": {}}},
                        {"name": "update_config", "description": "Update database connection string", "inputSchema": {"type": "object", "properties": {"connection_string": {"type": "string", "description": "SQLAlchemy connection string"}}, "required": ["connection_string"]}},
                        {"name": "check_status", "description": "Check database connection status", "inputSchema": {"type": "object", "properties": {}}},
                        {"name": "list_objects", "description": "List database objects (schemas, tables, views)", "inputSchema": {"type": "object", "properties": {}}},
                        {"name": "execute_sql", "description": "Execute a read-only SQL query (SELECT) against the active database connection", "inputSchema": {"type": "object", "properties": {"sql": {"type": "string", "description": "SQL query to execute (SELECT statements only)"}, "timeout": {"type": "integer", "description": "Query timeout in seconds (default: 30, max: 300)", "minimum": 1, "maximum": 300}, "limit": {"type": "integer", "description": "Maximum number of rows to return (default: 1000, max: 10000)", "minimum": 1, "maximum": 10000}, "include_metadata": {"type": "boolean", "description": "Include column metadata in response (default: false)"}}, "required": ["sql"]}},
                        {"name": "run_query", "description": "Alias of execute_sql. Execute a read-only SQL SELECT query with optional timeout, limit, and metadata.", "inputSchema": {"type": "object", "properties": {"sql": {"type": "string", "description": "SQL SELECT query"}, "timeout": {"type": "integer", "description": "Query timeout in seconds (default: 30, max: 300)", "minimum": 1, "maximum": 300}, "limit": {"type": "integer", "description": "Maximum number of rows to return (default: 1000, max: 10000)", "minimum": 1, "maximum": 10000}, "include_metadata": {"type": "boolean", "description": "Include column metadata in response (default: false)"}}, "required": ["sql"]}},
                        {"name": "connect", "description": "Connect to the database", "inputSchema": {"type": "object", "properties": {}}},
                        {"name": "disconnect", "description": "Disconnect from the database", "inputSchema": {"type": "object", "properties": {}}},
                        {"name": "validate_connection", "description": "Validate a database connection string (format, network, and actual connection)", "inputSchema": {"type": "object", "properties": {"connection_string": {"type": "string", "description": "SQLAlchemy connection string to validate"}}, "required": ["connection_string"]}},
                        {"name": "build_connection", "description": "Build and validate a SQLAlchemy connection string from individual parameters (dialect, host, port, database, etc.)", "inputSchema": {"type": "object", "properties": {"dialect": {"type": "string"}, "driver": {"type": "string"}, "username": {"type": "string"}, "password": {"type": "string"}, "host": {"type": "string"}, "port": {"type": "integer"}, "database": {"type": "string"}, "query": {"type": "object"}}, "required": ["dialect", "database"]}},
                        {"name": "create_user", "description": "Create a new user in the multi-user system. Super admins can create users with any role in any organization. Org admins can create common or org_admin users in their organization.", "inputSchema": {"type": "object", "properties": {"username": {"type": "string", "description": "Unique username"}, "password": {"type": "string", "description": "User password"}, "email": {"type": "string", "description": "User email address"}, "full_name": {"type": "string", "description": "User's full name (optional)"}, "role": {"type": "string", "description": "User role: common, org_admin, or super_admin (default: common)", "enum": ["common", "org_admin", "super_admin"]}, "organization_id": {"type": "string", "description": "Organization ID (UUID). If not specified, uses default organization."}}, "required": ["username", "password", "email"]}},
                        {"name": "list_users", "description": "List all users in the system", "inputSchema": {"type": "object", "properties": {}}},
                        {"name": "get_user", "description": "Get details for a specific user (default self)", "inputSchema": {"type": "object", "properties": {"username": {"type": "string"}}}},
                        {"name": "update_user", "description": "Update a user (email, full_name, password, role). Super admins can change any user's role. Org admins can promote/demote between common and org_admin in their organization.", "inputSchema": {"type": "object", "properties": {"username": {"type": "string", "description": "Username to update"}, "email": {"type": "string", "description": "New email address"}, "full_name": {"type": "string", "description": "New full name"}, "password": {"type": "string", "description": "New password"}, "role": {"type": "string", "description": "New role: common, org_admin, or super_admin", "enum": ["common", "org_admin", "super_admin"]}}, "required": ["username"]}},
                        {"name": "delete_user", "description": "Delete a user", "inputSchema": {"type": "object", "properties": {"username": {"type": "string"}}, "required": ["username"]}},
                        {"name": "add_connection", "description": "Add a new database connection for the authenticated user", "inputSchema": {"type": "object", "properties": {"name": {"type": "string"}, "connection_string": {"type": "string"}, "description": {"type": "string"}}, "required": ["name", "connection_string"]}},
                        {"name": "list_connections", "description": "List all database connections for the authenticated user", "inputSchema": {"type": "object", "properties": {}}},
                        {"name": "get_connection", "description": "Get details of a specific connection", "inputSchema": {"type": "object", "properties": {"connection_id": {"type": "string"}}, "required": ["connection_id"]}},
                        {"name": "update_connection", "description": "Update a connection (name, connection_string, description)", "inputSchema": {"type": "object", "properties": {"connection_id": {"type": "string"}, "name": {"type": "string"}, "connection_string": {"type": "string"}, "description": {"type": "string"}}, "required": ["connection_id"]}},
                        {"name": "get_active_connection", "description": "Get the currently active connection for the authenticated user", "inputSchema": {"type": "object", "properties": {}}},
                        {"name": "activate_connection", "description": "Activate a database connection for the authenticated user", "inputSchema": {"type": "object", "properties": {"connection_id": {"type": "string"}}, "required": ["connection_id"]}},
                        {"name": "test_connection", "description": "Test a database connection", "inputSchema": {"type": "object", "properties": {"connection_id": {"type": "string"}}, "required": ["connection_id"]}},
                        {"name": "remove_connection", "description": "Remove a database connection for the authenticated user", "inputSchema": {"type": "object", "properties": {"connection_id": {"type": "string"}}, "required": ["connection_id"]}},
                        {"name": "create_organization", "description": "Create a new organization (super-admin only)", "inputSchema": {"type": "object", "properties": {"name": {"type": "string"}, "display_name": {"type": "string"}, "description": {"type": "string"}}, "required": ["name"]}},
                        {"name": "list_organizations", "description": "List organizations (super-admin sees all, org-admin sees own)", "inputSchema": {"type": "object", "properties": {}}},
                        {"name": "get_organization", "description": "Get organization details", "inputSchema": {"type": "object", "properties": {"org_name": {"type": "string"}}, "required": ["org_name"]}},
                        {"name": "update_organization", "description": "Update organization (super-admin only)", "inputSchema": {"type": "object", "properties": {"org_name": {"type": "string"}, "display_name": {"type": "string"}, "description": {"type": "string"}, "active": {"type": "boolean"}}, "required": ["org_name"]}},
                        {"name": "delete_organization", "description": "Delete organization (super-admin only)", "inputSchema": {"type": "object", "properties": {"org_name": {"type": "string"}}, "required": ["org_name"]}},
                        {"name": "list_organization_users", "description": "List all users in an organization", "inputSchema": {"type": "object", "properties": {"org_name": {"type": "string"}}, "required": ["org_name"]}},
                        {"name": "list_organization_connections", "description": "List all database connections in an organization", "inputSchema": {"type": "object", "properties": {"org_name": {"type": "string"}}, "required": ["org_name"]}},
                        {"name": "suggest_semantic_maps", "description": "Auto-suggest semantic entity and relationship mappings from current DB schema (non-destructive)", "inputSchema": {"type": "object", "properties": {"include_columns": {"type": "boolean", "description": "Include column mappings for entities (default: true)"}, "type": {"type": "string", "enum": ["entity", "relationship", "all"], "description": "Suggestion type filter"}, "limit": {"type": "integer", "description": "Max number of suggestions per type"}}}},
                        {"name": "create_api_key", "description": "Create a new API key for the authenticated user", "inputSchema": {"type": "object", "properties": {"name": {"type": "string", "description": "Friendly name for the API key"}, "description": {"type": "string", "description": "Optional description"}, "expires_in_days": {"type": "integer", "description": "Days until expiration (1-3650, or omit for no expiration)"}}, "required": ["name"]}},
                        {"name": "list_my_api_keys", "description": "List all API keys for the authenticated user", "inputSchema": {"type": "object", "properties": {}}},
                        {"name": "revoke_api_key", "description": "Revoke (delete) an API key", "inputSchema": {"type": "object", "properties": {"key_id": {"type": "string", "description": "ID of the API key to revoke"}}, "required": ["key_id"]}},
                        {"name": "describe_table", "description": "Get complete schema information for a database table (columns, types, primary keys, foreign keys, indexes)", "inputSchema": {"type": "object", "properties": {"table_name": {"type": "string", "description": "Name of the table to describe"}, "schema": {"type": "string", "description": "Optional schema name"}}, "required": ["table_name"]}},
                        {"name": "get_table_relationships", "description": "Get all foreign key relationships between tables in the database", "inputSchema": {"type": "object", "properties": {"schema": {"type": "string", "description": "Optional schema name to filter tables"}}}},
                        {"name": "add_semantic_map", "description": "Add a new semantic mapping between business concepts and database structures", "inputSchema": {"type": "object", "properties": {"concept": {"type": "string", "description": "Business concept name (e.g., 'cliente', 'pedido')"}, "type": {"type": "string", "enum": ["entity", "relationship"], "description": "Type of mapping"}, "table": {"type": "string", "description": "Table name (for entity mappings)"}, "schema": {"type": "string", "description": "Schema name (optional)"}, "description": {"type": "string", "description": "Description of the concept"}, "aliases": {"type": "array", "items": {"type": "string"}, "description": "Alternative names"}, "column_mappings": {"type": "object", "description": "Map business terms to column names"}, "from_table": {"type": "string", "description": "Source table (for relationships)"}, "to_table": {"type": "string", "description": "Target table (for relationships)"}, "join_condition": {"type": "string", "description": "Join condition (for relationships)"}}, "required": ["concept", "type"]}},
                        {"name": "list_semantic_maps", "description": "List all semantic mappings for the active connection", "inputSchema": {"type": "object", "properties": {"type": {"type": "string", "enum": ["entity", "relationship"], "description": "Optional filter by mapping type"}}}},
                        {"name": "get_semantic_mapping", "description": "Get complete details of a specific semantic mapping by ID", "inputSchema": {"type": "object", "properties": {"mapping_id": {"type": "string", "description": "ID of the mapping to retrieve"}}, "required": ["mapping_id"]}},
                        {"name": "update_semantic_map", "description": "Update an existing semantic mapping", "inputSchema": {"type": "object", "properties": {"mapping_id": {"type": "string", "description": "ID of the mapping to update"}, "description": {"type": "string"}, "aliases": {"type": "array", "items": {"type": "string"}}, "column_mappings": {"type": "object"}}, "required": ["mapping_id"]}},
                        {"name": "delete_semantic_map", "description": "Delete a semantic mapping", "inputSchema": {"type": "object", "properties": {"mapping_id": {"type": "string", "description": "ID of the mapping to delete"}}, "required": ["mapping_id"]}},
                        {"name": "natural_query", "description": "Gerar e opcionalmente executar SQL seguro a partir de linguagem natural usando contexto semântico e de schema", "inputSchema": {"type": "object", "properties": {"query": {"type": "string", "description": "Pergunta em linguagem natural"}, "run_mode": {"type": "string", "enum": ["generate", "execute"], "description": "Se 'execute', roda a consulta e retorna resultados"}, "limit": {"type": "integer", "description": "Máx linhas (default: configurado)"}, "include_sql": {"type": "boolean", "description": "Sempre retornar SQL gerado"}, "include_mappings_used": {"type": "boolean", "description": "Incluir lista de mapeamentos semânticos usados na conversão"}}, "required": ["query"]}},
                        {"name": "oauth_get_login_url", "description": "Get OAuth 2.0 authorization URL for manual authentication (for clients that cannot open browser automatically)", "inputSchema": {"type": "object", "properties": {"client_type": {"type": "string", "enum": ["desktop", "cli", "web"], "description": "Type of client requesting authentication (default: desktop)", "default": "desktop"}}, "required": []}},
                        {"name": "update_claude_config", "description": "🔧 Bootstrap Tool: Automatically configure Claude Desktop with OAuth token (PUBLIC - no auth required). Updates claude_desktop_config.json with the provided token, creates backup, and preserves other MCP servers.", "inputSchema": {"type": "object", "properties": {"token": {"type": "string", "description": "OAuth Bearer token obtained from authentication flow"}, "server_name": {"type": "string", "description": "Optional name of the MCP server to update in Claude Desktop config. If not provided, auto-detects 'Tryton local' or 'SimpliQ MCP Server'"}}, "required": ["token"]}}
                    ]

                    # Add tools from plugins
                    try:
                        plugin_tools = plugin_registry.get_all_tools()
                        for tool_name, tool_def in plugin_tools.items():
                            tools_jsonrpc.append({
                                "name": tool_name,
                                "description": tool_def.get("description", ""),
                                "inputSchema": tool_def.get("inputSchema", {"type": "object", "properties": {}})
                            })
                        logger.info(f"Added {len(plugin_tools)} tools from plugins")
                    except Exception as e:
                        logger.warning(f"Failed to get plugin tools: {e}")

                    logger.info(f"Handling tools/list request - returning {len(tools_jsonrpc)} available tools")
                    return jsonify({
                        "jsonrpc": "2.0",
                        "id": rpc_id,
                        "result": {
                            "tools": tools_jsonrpc
                        }
                    })
                
                # Handle tools/call request
                elif rpc_method == "tools/call":
                    tool_name = rpc_params.get("name")
                    tool_args = rpc_params.get("arguments", {})

                    print(f"\n>>> [EXEC] Executing tool: {tool_name}")
                    print(f">>> Arguments: {tool_args}")
                    logger.info(f"Executing tool: {tool_name} with args: {tool_args}")

                    # OAuth 2.0 Authentication (Phase 2)
                    oauth_user_info = None
                    # IMPORTANT: Skip OAuth validation for public tools:
                    # - user_login, create_user: initial authentication/registration
                    # - oauth_get_login_url: generate OAuth URL for manual authentication
                    # - update_claude_config: bootstrap tool to configure Claude Desktop (chicken-and-egg problem)
                    PUBLIC_TOOLS = ["user_login", "create_user", "oauth_get_login_url", "update_claude_config"]
                    if oauth_middleware and oauth_middleware.enabled and tool_name not in PUBLIC_TOOLS:
                        logger.debug("OAuth validation enabled - validating request")
                        is_valid, oauth_user_info, error_msg = oauth_middleware.validate_request()

                        if not is_valid:
                            logger.warning(f"OAuth validation failed for tool '{tool_name}': {error_msg}")
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32001,  # Custom error code for auth
                                    "message": "OAuth authentication required",
                                    "data": {"detail": error_msg}
                                }
                            }), 401

                        # Propagate OAuth context to Flask's g object
                        g.oauth_user_id = oauth_user_info.get("sub")
                        g.oauth_client_id = oauth_user_info.get("client_id")
                        g.oauth_org_id = oauth_user_info.get("org_id")
                        g.oauth_scope = oauth_user_info.get("scope", "")
                        g.oauth_user_info = oauth_user_info

                        logger.info(f"OAuth authenticated: user={g.oauth_user_id}, org={g.oauth_org_id}, client={g.oauth_client_id}")
                        print(f">>> [AUTH] OAuth User: {g.oauth_user_id}")

                    # Ensure we have authentication context available for any branch that needs it.
                    # Some tool handlers (e.g. execute_sql) referenced 'authenticated_user' without first defining it,
                    # causing UnboundLocalError. We make it universally available here.
                    try:
                        authenticated_user, auth_token = get_authenticated_user()
                    except Exception:
                        authenticated_user, auth_token = None, None

                    # Check if authentication is required for all endpoints (legacy auth)
                    # Debug: Log OAuth context before check
                    print(f"\n>>> [DEBUG] Before check_auth_required:")
                    print(f">>>   - oauth_middleware enabled: {oauth_middleware and oauth_middleware.enabled}")
                    print(f">>>   - g.oauth_user_info exists: {hasattr(g, 'oauth_user_info')}")
                    if hasattr(g, 'oauth_user_info'):
                        print(f">>>   - g.oauth_user_info value: {g.oauth_user_info}")

                    auth_required, auth_error_response = check_auth_required(tool_name, rpc_id)
                    if auth_required:
                        logger.info(f"Tool '{tool_name}' blocked: authentication required")
                        print(f">>> [DEBUG] Tool blocked by check_auth_required")
                        return auth_error_response
                    else:
                        print(f">>> [DEBUG] Tool allowed by check_auth_required")

                    # Route to appropriate tool
                    tool_result = None
                    
                    if tool_name == "get_config":
                        config_data = load_config()
                        if "error" not in config_data:
                            connection_string = config_data.get("connection_string", "")
                            db_info = get_db_info(connection_string)
                            config_data["db_info"] = db_info
                        tool_result = config_data
                    
                    elif tool_name == "update_config":
                        connection_string = tool_args.get("connection_string")
                        if not connection_string:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32602,
                                    "message": "Missing connection_string parameter"
                                }
                            }), 400
                        save_config({"connection_string": connection_string})
                        tool_result = {"message": "Configuration updated successfully"}
                    
                    elif tool_name == "check_status":
                        if engine:
                            try:
                                with engine.connect() as conn:
                                    pass
                                tool_result = {"status": "connected", "message": "Database is accessible"}
                            except SQLAlchemyError as e:
                                tool_result = {"status": "error", "message": "Database connection failed", "details": str(e)}
                        else:
                            tool_result = {"status": "disconnected", "message": "Not connected to any database"}
                    
                    elif tool_name == "list_objects":
                        # Auto-reconnect if engine is not available but user has active connection
                        if not engine:
                            try:
                                authenticated_user, auth_token = get_authenticated_user()
                                if authenticated_user:
                                    success, message, active_conn = users_api.get_active_connection(authenticated_user, auth_token)
                                    if success and active_conn:
                                        connection_string = active_conn.get("connection_string")
                                        if connection_string:
                                            connect_to_db(connection_string)
                                            logger.info(f"Auto-reconnected to database for list_objects (user: '{authenticated_user}')")
                                        else:
                                            return jsonify({
                                                "jsonrpc": "2.0",
                                                "id": rpc_id,
                                                "error": {
                                                    "code": -32600,
                                                    "message": "Active connection has no connection_string"
                                                }
                                            }), 400
                                    else:
                                        return jsonify({
                                            "jsonrpc": "2.0",
                                            "id": rpc_id,
                                            "error": {
                                                "code": -32600,
                                                "message": "Not connected to any database. Use activate_connection or connect tool first."
                                            }
                                        }), 400
                                else:
                                    return jsonify({
                                        "jsonrpc": "2.0",
                                        "id": rpc_id,
                                        "error": {
                                            "code": -32600,
                                            "message": "Not connected to any database. Use connect tool first."
                                        }
                                    }), 400
                            except Exception as e:
                                logger.error(f"Failed to auto-reconnect for list_objects: {e}")
                                return jsonify({
                                    "jsonrpc": "2.0",
                                    "id": rpc_id,
                                    "error": {
                                        "code": -32600,
                                        "message": "Not connected to any database. Use connect tool first."
                                    }
                                }), 400

                        try:
                            inspector = inspect(engine)
                            schemas = inspector.get_schema_names() if hasattr(inspector, 'get_schema_names') else []
                            tables = inspector.get_table_names() if hasattr(inspector, 'get_table_names') else []
                            views = inspector.get_view_names() if hasattr(inspector, 'get_view_names') else []

                            tool_result = {
                                "schemas": schemas,
                                "tables": tables,
                                "views": views,
                                "note": "User information is not available through SQLAlchemy inspection"
                            }
                        except SQLAlchemyError as e:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32603,
                                    "message": f"Failed to retrieve database objects: {str(e)}"
                                }
                            }), 500

                    elif tool_name in ("execute_sql", "run_query"):
                        # 1. Check authentication
                        if not authenticated_user:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32600,
                                    "message": "Authentication required. Please login first."
                                }
                            }), 401

                        # 2. Auto-reconnect if engine is not available but user has active connection
                        if not engine:
                            try:
                                success, message, active_conn = users_api.get_active_connection(authenticated_user, auth_token)
                                if success and active_conn:
                                    connection_string = active_conn.get("connection_string")
                                    if connection_string:
                                        connect_to_db(connection_string)
                                        logger.info(f"Auto-reconnected to database for user '{authenticated_user}' (connection: '{active_conn.get('name')}')")
                                    else:
                                        return jsonify({
                                            "jsonrpc": "2.0",
                                            "id": rpc_id,
                                            "error": {
                                                "code": -32600,
                                                "message": "Active connection has no connection_string"
                                            }
                                        }), 400
                                else:
                                    return jsonify({
                                        "jsonrpc": "2.0",
                                        "id": rpc_id,
                                        "error": {
                                            "code": -32600,
                                            "message": f"No active database connection. {message}"
                                        }
                                    }), 400
                            except Exception as e:
                                logger.error(f"Failed to auto-reconnect: {e}")
                                return jsonify({
                                    "jsonrpc": "2.0",
                                    "id": rpc_id,
                                    "error": {
                                        "code": -32600,
                                        "message": f"Failed to auto-reconnect to database: {str(e)}"
                                    }
                                }), 400

                        # 3. Extract parameters
                        sql = tool_args.get("sql")
                        timeout = tool_args.get("timeout", 30)
                        limit = tool_args.get("limit", 1000)
                        include_metadata = tool_args.get("include_metadata", False)

                        if not sql:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32600,
                                    "message": "Missing required parameter: sql"
                                }
                            }), 400

                        # 4. Validate SQL
                        validator = SQLValidator()
                        validation = validator.validate(sql, timeout, limit)

                        if not validation.is_valid:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32600,
                                    "message": "SQL validation failed",
                                    "data": {
                                        "validation_errors": validation.errors,
                                        "sql_provided": sql,
                                        "error_type": "VALIDATION_ERROR"
                                    }
                                }
                            }), 400

                        # 5. Execute SQL
                        executor = SQLExecutor(engine)
                        exec_result = executor.execute(sql, timeout, limit, include_metadata)

                        # 6. Audit log
                        logger.info(
                            f"[execute_sql] User: {authenticated_user}, "
                            f"SQL: {sql[:100]}..., "
                            f"Success: {exec_result.success}, "
                            f"Rows: {exec_result.row_count}, "
                            f"Time: {exec_result.execution_time_ms}ms"
                        )

                        # 7. Return result
                        if exec_result.success:
                            tool_result = {
                                "success": True,
                                "data": exec_result.data,
                                "row_count": exec_result.row_count,
                                "execution_time_ms": exec_result.execution_time_ms,
                                "truncated": exec_result.truncated
                            }

                            if include_metadata and exec_result.metadata:
                                tool_result["metadata"] = exec_result.metadata

                            if validation.warnings:
                                tool_result["warnings"] = validation.warnings
                        else:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32603,
                                    "message": "SQL execution failed",
                                    "data": {
                                        "error_message": exec_result.error_message,
                                        "error_type": exec_result.error_type,
                                        "sql_provided": sql
                                    }
                                }
                            }), 500

                    elif tool_name == "describe_table":
                        # 1. Check authentication
                        if not authenticated_user:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32600,
                                    "message": "Authentication required. Please login first."
                                }
                            }), 401

                        # 2. Check active database connection
                        if not engine:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32600,
                                    "message": "No active database connection. Use activate_connection first."
                                }
                            }), 400

                        # 3. Extract parameters
                        table_name = tool_args.get("table_name")
                        schema = tool_args.get("schema")

                        if not table_name:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32600,
                                    "message": "Missing required parameter: table_name"
                                }
                            }), 400

                        # 4. Introspect table
                        try:
                            introspector = SchemaIntrospector(engine)
                            description = introspector.describe_table(table_name, schema)

                            # Convert to dict for JSON serialization
                            tool_result = {
                                "table_name": description.table_name,
                                "schema": description.schema,
                                "columns": [
                                    {
                                        "name": col.name,
                                        "type": col.type,
                                        "nullable": col.nullable,
                                        "default": str(col.default) if col.default is not None else None,
                                        "autoincrement": col.autoincrement,
                                        "primary_key": col.primary_key
                                    }
                                    for col in description.columns
                                ],
                                "primary_key": description.primary_key,
                                "foreign_keys": [
                                    {
                                        "name": fk.name,
                                        "constrained_columns": fk.constrained_columns,
                                        "referred_table": fk.referred_table,
                                        "referred_columns": fk.referred_columns,
                                        "ondelete": fk.ondelete,
                                        "onupdate": fk.onupdate
                                    }
                                    for fk in description.foreign_keys
                                ],
                                "indexes": [
                                    {
                                        "name": idx.name,
                                        "unique": idx.unique,
                                        "columns": idx.columns
                                    }
                                    for idx in description.indexes
                                ],
                                "unique_constraints": description.unique_constraints,
                                "check_constraints": description.check_constraints
                            }

                            logger.info(
                                f"[describe_table] User: {authenticated_user}, "
                                f"Table: {table_name}, "
                                f"Columns: {len(description.columns)}"
                            )

                        except ValueError as e:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32600,
                                    "message": str(e)
                                }
                            }), 400
                        except SQLAlchemyError as e:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32603,
                                    "message": f"Database error: {str(e)}"
                                }
                            }), 500

                    elif tool_name == "get_table_relationships":
                        # 1. Check authentication
                        if not authenticated_user:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32600,
                                    "message": "Authentication required. Please login first."
                                }
                            }), 401

                        # 2. Check active database connection
                        if not engine:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32600,
                                    "message": "No active database connection. Use activate_connection first."
                                }
                            }), 400

                        # 3. Extract parameters
                        schema = tool_args.get("schema")

                        # 4. Get relationships
                        try:
                            introspector = SchemaIntrospector(engine)
                            relationships = introspector.get_table_relationships(schema)

                            # Convert to dict for JSON serialization
                            tool_result = {
                                "relationships": [
                                    {
                                        "from_table": rel.from_table,
                                        "to_table": rel.to_table,
                                        "from_columns": rel.from_columns,
                                        "to_columns": rel.to_columns,
                                        "constraint_name": rel.constraint_name,
                                        "ondelete": rel.ondelete,
                                        "onupdate": rel.onupdate
                                    }
                                    for rel in relationships
                                ],
                                "count": len(relationships)
                            }

                            logger.info(
                                f"[get_table_relationships] User: {authenticated_user}, "
                                f"Count: {len(relationships)}"
                            )

                        except SQLAlchemyError as e:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32603,
                                    "message": f"Database error: {str(e)}"
                                }
                            }), 500

                    elif tool_name == "connect":
                        try:
                            # Get active connection for the authenticated user
                            success, message, active_conn = users_api.get_active_connection(authenticated_user, auth_token)
                            
                            if not success or not active_conn:
                                return jsonify({
                                    "jsonrpc": "2.0",
                                    "id": rpc_id,
                                    "error": {
                                        "code": -32603,
                                        "message": f"No active connection found: {message}"
                                    }
                                }), 500
                            
                            # Use the active connection's connection_string
                            connection_string = active_conn.get("connection_string")
                            if not connection_string:
                                return jsonify({
                                    "jsonrpc": "2.0",
                                    "id": rpc_id,
                                    "error": {
                                        "code": -32603,
                                        "message": "Active connection has no connection_string"
                                    }
                                }), 500
                            
                            connect_to_db(connection_string)
                            tool_result = {
                                "message": "Successfully connected to the database",
                                "connection_name": active_conn.get("name"),
                                "connection_id": active_conn.get("id")
                            }
                        except Exception as e:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32603,
                                    "message": f"Failed to connect: {str(e)}"
                                }
                            }), 500
                    
                    elif tool_name == "disconnect":
                        disconnect_from_db()
                        tool_result = {"message": "Successfully disconnected from the database"}
                    
                    elif tool_name == "validate_connection":
                        connection_string = tool_args.get("connection_string")
                        if not connection_string:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32602,
                                    "message": "Missing connection_string parameter"
                                }
                            }), 400

                        tool_result = validate_connection_complete(connection_string)

                    elif tool_name == "build_connection":
                        # Validate that required parameters are present
                        if not tool_args.get("dialect"):
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32602,
                                    "message": "Missing required parameter 'dialect'"
                                }
                            }), 400

                        if not tool_args.get("database"):
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32602,
                                    "message": "Missing required parameter 'database'"
                                }
                            }), 400

                        tool_result = build_connection_string_from_params(tool_args)

                    # Multi-user tools
                    elif tool_name == "create_user":
                        username = tool_args.get("username")
                        password = tool_args.get("password")
                        email = tool_args.get("email")
                        full_name = tool_args.get("full_name", "")
                        role = tool_args.get("role")  # Optional: common, org_admin, super_admin
                        organization_id = tool_args.get("organization_id")  # Optional: UUID of organization

                        if not username or not password or not email:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32602,
                                    "message": "Missing required parameters (username, password, email)"
                                }
                            }), 400

                        # Pass auth_token to enable authenticated user creation (roles/orgs)
                        success, message, user_data = users_api.create_user(
                            username, password, email, full_name, role, organization_id,
                            auth_token=auth_token
                        )

                        if success:
                            tool_result = {
                                "success": True,
                                "message": message,
                                "user": user_data
                            }
                        else:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32603,
                                    "message": message
                                }
                            }), 400

                    elif tool_name == "user_login":
                        username = tool_args.get("username")
                        password = tool_args.get("password")

                        print(f">>> Login attempt for user: {username}")
                        logger.info(f"Login attempt for user: {username}")

                        if not username or not password:
                            logger.warning("Login failed: missing username or password")
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32602,
                                    "message": "Missing required parameters (username, password)"
                                }
                            }), 400

                        success, message, session_token = users_api.authenticate(username, password)

                        if success:
                            print(f">>> Login successful for user: {username}")
                            logger.info(f"User '{username}' logged in successfully")
                            if session_token is None:
                                logger.warning(
                                    "Login succeeded but no token returned. Check User Manager /auth/login response schema."
                                )
                            else:
                                # Salvar sessão no arquivo JSON para persistência
                                save_session(session_token, username, expires_in=86400)  # 24 horas
                        else:
                            print(f">>> Login failed for user '{username}': {message}")
                            logger.warning(f"Login failed for user '{username}': {message}")

                        if success:
                            tool_result = {
                                "success": True,
                                "message": message,
                                "session_token": session_token,
                                "username": username,
                                "session_persisted": True,
                                "note": "Session will be automatically restored on next request"
                            }
                        else:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32603,
                                    "message": message
                                }
                            }), 401

                    elif tool_name == "list_users":
                        # Attempt to use stored session/Authorization header for potentially richer listing
                        authenticated_user, auth_token = get_authenticated_user()
                        token_source = None
                        if auth_token:
                            users_list = users_api.list_users_auth(auth_token)
                            token_source = "authorization_header_or_session"
                        else:
                            users_list = users_api.list_users()
                            token_source = "none"

                        tool_result = {
                            "success": True,
                            "users": users_list,
                            "count": len(users_list),
                            "auth_used": auth_token is not None,
                            "token_source": token_source,
                            "note": "Listing used authenticated request" if auth_token else "Listing performed without auth token; some privileged users may be hidden"
                        }

                    elif tool_name == "whoami":
                        authenticated_user, auth_token = get_authenticated_user()
                        if not authenticated_user:
                            return jsonify({
                                "jsonrpc": "2.0", "id": rpc_id,
                                "error": {"code": -32600, "message": "Not authenticated"}
                            }), 401
                        tool_result = {"username": authenticated_user, "has_token": True}

                    elif tool_name == "oauth_get_login_url":
                        """
                        Generate OAuth 2.0 authorization URL for manual authentication.
                        This is useful for clients (like Claude Desktop with mcp-remote) that cannot
                        automatically open a browser for OAuth flow.
                        """
                        import secrets
                        from urllib.parse import urlencode

                        client_type = tool_args.get("client_type", "desktop")

                        # Get OAuth configuration
                        oauth_config = config.get('oauth', {})
                        provider_url = oauth_config.get('provider_url', 'http://localhost:8002')
                        client_config = oauth_config.get('client', {})
                        client_id = client_config.get('client_id')
                        redirect_uri = client_config.get('redirect_uri', 'http://localhost:3000/callback')
                        scopes = client_config.get('scopes', ['admin:org', 'read:connections', 'write:connections', 'execute:tools'])

                        if not client_id:
                            return jsonify({
                                "jsonrpc": "2.0", "id": rpc_id,
                                "error": {"code": -32603, "message": "OAuth client not configured"}
                            }), 500

                        # Generate random state for CSRF protection
                        state = secrets.token_urlsafe(32)

                        # Build authorization URL
                        auth_params = {
                            'response_type': 'code',
                            'client_id': client_id,
                            'redirect_uri': redirect_uri,
                            'scope': ' '.join(scopes),
                            'state': state
                        }

                        auth_url = f"{provider_url}/oauth/authorize?{urlencode(auth_params)}"

                        # Prepare instructions based on client type
                        instructions = {
                            "desktop": [
                                "1. Open the authorization URL in your browser",
                                "2. Login with your credentials",
                                "3. After successful login, you'll be redirected to the callback URL",
                                "4. Copy the 'access_token' from the response",
                                "5. Update your Claude Desktop config file with the token:",
                                "   - File: C:\\Users\\gerso\\AppData\\Roaming\\Claude\\claude_desktop_config.json",
                                "   - Add: --header \"Authorization: Bearer <YOUR_TOKEN>\" to the args array"
                            ],
                            "cli": [
                                "1. Open the authorization URL in your browser",
                                "2. Login with your credentials",
                                "3. Copy the access_token from the callback response",
                                "4. Use the token in your API calls: -H 'Authorization: Bearer <TOKEN>'"
                            ],
                            "web": [
                                "1. Redirect user to the authorization URL",
                                "2. Handle the OAuth callback",
                                "3. Extract the authorization code",
                                "4. Exchange the code for an access token"
                            ]
                        }

                        tool_result = {
                            "authorization_url": auth_url,
                            "state": state,
                            "client_type": client_type,
                            "instructions": instructions.get(client_type, instructions["desktop"]),
                            "provider": provider_url,
                            "scopes": scopes,
                            "redirect_uri": redirect_uri,
                            "note": "This URL is valid for one-time use. The state parameter protects against CSRF attacks."
                        }

                    elif tool_name == "update_claude_config":
                        """
                        PUBLIC TOOL: Update Claude Desktop configuration with OAuth token.

                        This is a special bootstrap tool that does NOT require authentication
                        because its purpose is to CONFIGURE the authentication itself.

                        It automatically detects the Claude Desktop config file location,
                        creates a backup, and updates the SimpliQ MCP Server configuration
                        with the provided OAuth token.

                        Parameters:
                        - token: OAuth Bearer token (required)
                        - server_name: Name of MCP server to update (optional, auto-detects if not provided)
                        """
                        from claude_config_manager import ClaudeConfigManager

                        token = tool_args.get("token")
                        server_name = tool_args.get("server_name")  # Optional

                        if not token:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32602,
                                    "message": "Missing required parameter: token"
                                }
                            }), 400

                        try:
                            config_manager = ClaudeConfigManager()
                            result = config_manager.auto_configure(token, server_name)

                            tool_result = result

                        except Exception as e:
                            logger.error(f"Error in update_claude_config: {e}", exc_info=True)
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32603,
                                    "message": f"Failed to update Claude Desktop configuration: {str(e)}"
                                }
                            }), 500

                    elif tool_name == "server_logout":
                        cleared = clear_session()
                        tool_result = {"success": cleared, "message": "Session cleared" if cleared else "No session to clear"}

                    elif tool_name == "get_user":
                        authenticated_user, auth_token = get_authenticated_user()
                        if not authenticated_user:
                            return jsonify({
                                "jsonrpc": "2.0", "id": rpc_id,
                                "error": {"code": -32600, "message": "Authentication required. Login first."}
                            }), 401
                        username = tool_args.get("username") or authenticated_user
                        user_data = users_api.get_user(username, auth_token)
                        if user_data:
                            tool_result = {"success": True, "user": user_data}
                        else:
                            return jsonify({
                                "jsonrpc": "2.0", "id": rpc_id,
                                "error": {"code": -32603, "message": f"User '{username}' not found"}
                            }), 404

                    elif tool_name == "update_user":
                        authenticated_user, auth_token = get_authenticated_user()
                        if not authenticated_user:
                            return jsonify({
                                "jsonrpc": "2.0", "id": rpc_id,
                                "error": {"code": -32600, "message": "Authentication required. Login first."}
                            }), 401
                        username = tool_args.get("username")
                        if not username:
                            return jsonify({
                                "jsonrpc": "2.0", "id": rpc_id,
                                "error": {"code": -32602, "message": "Missing required parameter username"}
                            }), 400
                        email = tool_args.get("email")
                        full_name = tool_args.get("full_name")
                        password = tool_args.get("password")
                        role = tool_args.get("role")  # Optional: new role for the user
                        ok, msg = users_api.update_user(username, auth_token, email=email, full_name=full_name, password=password, role=role)
                        if ok:
                            tool_result = {"success": True, "message": msg}
                        else:
                            return jsonify({
                                "jsonrpc": "2.0", "id": rpc_id,
                                "error": {"code": -32603, "message": msg}
                            }), 400

                    elif tool_name == "delete_user":
                        authenticated_user, auth_token = get_authenticated_user()
                        if not authenticated_user:
                            return jsonify({
                                "jsonrpc": "2.0", "id": rpc_id,
                                "error": {"code": -32600, "message": "Authentication required. Login first."}
                            }), 401
                        username = tool_args.get("username")
                        if not username:
                            return jsonify({
                                "jsonrpc": "2.0", "id": rpc_id,
                                "error": {"code": -32602, "message": "Missing required parameter username"}
                            }), 400
                        ok, msg = users_api.delete_user(username, auth_token)
                        if ok:
                            tool_result = {"success": True, "message": msg}
                        else:
                            return jsonify({
                                "jsonrpc": "2.0", "id": rpc_id,
                                "error": {"code": -32603, "message": msg}
                            }), 400

                    elif tool_name == "user_logout":
                        # Clear the stored session
                        success = clear_session()

                        if success:
                            tool_result = {
                                "success": True,
                                "message": "Logged out successfully. Session cleared.",
                                "note": "You will need to login again to access authenticated endpoints"
                            }
                        else:
                            tool_result = {
                                "success": False,
                                "message": "Failed to clear session file"
                            }

                    elif tool_name == "add_connection":
                        # Requires authentication
                        authenticated_user, auth_token = get_authenticated_user()
                        if not authenticated_user:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32600,
                                    "message": "Authentication required. Please login first using user_login tool."
                                }
                            }), 401

                        name = tool_args.get("name")
                        connection_string = tool_args.get("connection_string")
                        description = tool_args.get("description", "")

                        if not name or not connection_string:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32602,
                                    "message": "Missing required parameters (name, connection_string)"
                                }
                            }), 400

                        success, message, connection = users_api.add_connection(
                            authenticated_user, auth_token, name, connection_string, description
                        )

                        if success:
                            tool_result = {
                                "success": True,
                                "message": message,
                                "connection": connection
                            }
                        else:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32603,
                                    "message": message
                                }
                            }), 400

                    elif tool_name == "list_connections":
                        # Requires authentication
                        authenticated_user, auth_token = get_authenticated_user()
                        if not authenticated_user:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32600,
                                    "message": "Authentication required. Please login first using user_login tool."
                                }
                            }), 401

                        success, message, connections = users_api.list_connections(authenticated_user, auth_token)

                        if success:
                            _, _, active_conn = users_api.get_active_connection(authenticated_user, auth_token)
                            active_id = active_conn['id'] if active_conn else None

                            tool_result = {
                                "success": True,
                                "connections": connections,
                                "active_connection_id": active_id,
                                "count": len(connections)
                            }
                        else:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32603,
                                    "message": message
                                }
                            }), 404

                    elif tool_name == "get_active_connection":
                        # Requires authentication
                        authenticated_user, auth_token = get_authenticated_user()
                        if not authenticated_user:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32600,
                                    "message": "Authentication required. Please login first using user_login tool."
                                }
                            }), 401

                        # Fetch active connection for the authenticated user
                        success, message, active_conn = users_api.get_active_connection(authenticated_user, auth_token)

                        if success:
                            tool_result = {
                                "success": True,
                                "active_connection": active_conn if active_conn else None,
                                "message": message if message else "Active connection retrieved successfully"
                            }
                        else:
                            # Not found or error
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32603,
                                    "message": message or "Failed to get active connection"
                                }
                            }), 404

                    elif tool_name == "activate_connection":
                        # Requires authentication
                        authenticated_user, auth_token = get_authenticated_user()
                        if not authenticated_user:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32600,
                                    "message": "Authentication required. Please login first using user_login tool."
                                }
                            }), 401

                        connection_id = tool_args.get("connection_id")

                        if not connection_id:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32602,
                                    "message": "Missing required parameter (connection_id)"
                                }
                            }), 400

                        success, message, connection = users_api.set_active_connection(
                            authenticated_user, auth_token, connection_id
                        )

                        if success:
                            # Automatically connect to the database after activating the connection
                            try:
                                connection_string = connection.get("connection_string")
                                if connection_string:
                                    connect_to_db(connection_string)
                                    logger.info(f"Auto-connected to database after activating connection '{connection.get('name')}'")
                            except Exception as e:
                                logger.warning(f"Failed to auto-connect after activation: {e}")
                                # Don't fail the activation if auto-connect fails
                                # User can still manually call connect tool

                            tool_result = {
                                "success": True,
                                "message": message,
                                "connection": connection
                            }
                        else:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32603,
                                    "message": message
                                }
                            }), 404

                    elif tool_name == "test_connection":
                        # Requires authentication
                        authenticated_user, auth_token = get_authenticated_user()
                        if not authenticated_user:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32600,
                                    "message": "Authentication required. Please login first using user_login tool."
                                }
                            }), 401

                        connection_id = tool_args.get("connection_id")

                        if not connection_id:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32602,
                                    "message": "Missing required parameter (connection_id)"
                                }
                            }), 400

                        success, message, connection = users_api.get_connection(
                            authenticated_user, auth_token, connection_id
                        )

                        if not success:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32603,
                                    "message": message
                                }
                            }), 404

                        # Validate the connection
                        connection_string = connection['connection_string']
                        validation_result = validate_connection_complete(connection_string)

                        # Update test result
                        users_api.update_connection_test_result(
                            authenticated_user, auth_token, connection_id,
                            validation_result['overall_valid'],
                            json.dumps(validation_result['summary'])
                        )

                        tool_result = {
                            "success": True,
                            "connection_id": connection_id,
                            "connection_name": connection['name'],
                            "validation": validation_result
                        }

                    elif tool_name == "remove_connection":
                        # Requires authentication
                        authenticated_user, auth_token = get_authenticated_user()
                        if not authenticated_user:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32600,
                                    "message": "Authentication required. Please login first using user_login tool."
                                }
                            }), 401

                        connection_id = tool_args.get("connection_id")

                        if not connection_id:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32602,
                                    "message": "Missing required parameter (connection_id)"
                                }
                            }), 400

                        success, message = users_api.delete_connection(
                            authenticated_user, auth_token, connection_id
                        )

                        if success:
                            tool_result = {
                                "success": True,
                                "message": message
                            }
                        else:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32603,
                                    "message": message
                                }
                            }), 404

                    # Organization Management tools
                    elif tool_name == "create_organization":
                        logger.info(f"Tool 'create_organization' called with args: {tool_args}")
                        # Requires authentication
                        authenticated_user, auth_token = get_authenticated_user()
                        logger.debug(f"Authenticated user: {authenticated_user}")
                        if not authenticated_user:
                            logger.warning("create_organization failed: not authenticated")
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32600,
                                    "message": "Authentication required. Please login first using user_login tool."
                                }
                            }), 401

                        name = tool_args.get("name")
                        display_name = tool_args.get("display_name")
                        description = tool_args.get("description", "")

                        if not name:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32602,
                                    "message": "Missing required parameter (name)"
                                }
                            }), 400

                        logger.info(f"Calling User Manager API to create organization: {name}")
                        success, message, org_data = users_api.create_organization(
                            auth_token, name, display_name, description
                        )

                        if success:
                            logger.info(f"Organization '{name}' created successfully")
                            tool_result = {
                                "success": True,
                                "message": message,
                                "organization": org_data
                            }
                        else:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32603,
                                    "message": message
                                }
                            }), 400

                    elif tool_name == "list_organizations":
                        print(f">>> [ORG] Listing organizations")
                        logger.info("Tool 'list_organizations' called")
                        # Requires authentication
                        authenticated_user, auth_token = get_authenticated_user()
                        print(f">>> Authenticated user: {authenticated_user}")
                        logger.debug(f"Authenticated user: {authenticated_user}")
                        if not authenticated_user:
                            logger.warning("list_organizations failed: not authenticated")
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32600,
                                    "message": "Authentication required. Please login first using user_login tool."
                                }
                            }), 401

                        print(f">>> Calling User Manager API...")
                        logger.info("Calling User Manager API to list organizations")
                        success, message, organizations = users_api.list_organizations(auth_token)

                        if success:
                            print(f">>> [OK] Retrieved {len(organizations)} organizations")
                            logger.info(f"Successfully retrieved {len(organizations)} organizations")
                            tool_result = {
                                "success": True,
                                "organizations": organizations,
                                "count": len(organizations)
                            }
                        else:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32603,
                                    "message": message
                                }
                            }), 403

                    elif tool_name == "get_organization":
                        # Requires authentication
                        authenticated_user, auth_token = get_authenticated_user()
                        if not authenticated_user:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32600,
                                    "message": "Authentication required. Please login first using user_login tool."
                                }
                            }), 401

                        org_name = tool_args.get("org_name")

                        if not org_name:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32602,
                                    "message": "Missing required parameter (org_name)"
                                }
                            }), 400

                        success, message, org_data = users_api.get_organization(auth_token, org_name)

                        if success:
                            tool_result = org_data
                        else:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32603,
                                    "message": message
                                }
                            }), 404

                    elif tool_name == "update_organization":
                        # Requires authentication
                        authenticated_user, auth_token = get_authenticated_user()
                        if not authenticated_user:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32600,
                                    "message": "Authentication required. Please login first using user_login tool."
                                }
                            }), 401

                        org_name = tool_args.get("org_name")
                        display_name = tool_args.get("display_name")
                        description = tool_args.get("description")
                        active = tool_args.get("active")

                        if not org_name:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32602,
                                    "message": "Missing required parameter (org_name)"
                                }
                            }), 400

                        success, message = users_api.update_organization(
                            auth_token, org_name, display_name, description, active
                        )

                        if success:
                            tool_result = {
                                "success": True,
                                "message": message
                            }
                        else:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32603,
                                    "message": message
                                }
                            }), 400

                    elif tool_name == "delete_organization":
                        # Requires authentication
                        authenticated_user, auth_token = get_authenticated_user()
                        if not authenticated_user:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32600,
                                    "message": "Authentication required. Please login first using user_login tool."
                                }
                            }), 401

                        org_name = tool_args.get("org_name")

                        if not org_name:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32602,
                                    "message": "Missing required parameter (org_name)"
                                }
                            }), 400

                        success, message = users_api.delete_organization(auth_token, org_name)

                        if success:
                            tool_result = {
                                "success": True,
                                "message": message
                            }
                        else:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32603,
                                    "message": message
                                }
                            }), 400

                    elif tool_name == "list_organization_users":
                        # Requires authentication
                        authenticated_user, auth_token = get_authenticated_user()
                        if not authenticated_user:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32600,
                                    "message": "Authentication required. Please login first using user_login tool."
                                }
                            }), 401

                        org_name = tool_args.get("org_name")

                        if not org_name:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32602,
                                    "message": "Missing required parameter (org_name)"
                                }
                            }), 400

                        success, message, users_list = users_api.list_organization_users(auth_token, org_name)

                        if success:
                            tool_result = {
                                "success": True,
                                "users": users_list,
                                "count": len(users_list)
                            }
                        else:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32603,
                                    "message": message
                                }
                            }), 404

                    elif tool_name == "list_organization_connections":
                        # Requires authentication
                        authenticated_user, auth_token = get_authenticated_user()
                        if not authenticated_user:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32600,
                                    "message": "Authentication required. Please login first using user_login tool."
                                }
                            }), 401

                        org_name = tool_args.get("org_name")

                        if not org_name:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32602,
                                    "message": "Missing required parameter (org_name)"
                                }
                            }), 400

                        success, message, connections = users_api.list_organization_connections(auth_token, org_name)

                        if success:
                            tool_result = {
                                "success": True,
                                "connections": connections,
                                "count": len(connections)
                            }
                        else:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32603,
                                    "message": message
                                }
                            }), 404

                    # API Key Management tools
                    elif tool_name == "create_api_key":
                        # Requires authentication
                        authenticated_user, auth_token = get_authenticated_user()
                        if not authenticated_user:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32600,
                                    "message": "Authentication required. Please login first using user_login tool."
                                }
                            }), 401

                        name = tool_args.get("name")
                        description = tool_args.get("description", "")
                        expires_in_days = tool_args.get("expires_in_days")

                        if not name:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32602,
                                    "message": "Missing required parameter (name)"
                                }
                            }), 400

                        success, message, api_key_value, key_info = users_api.create_api_key(
                            username=authenticated_user,
                            token=auth_token,
                            name=name,
                            description=description,
                            expires_in_days=expires_in_days
                        )

                        if success:
                            tool_result = {
                                "success": True,
                                "message": message,
                                "api_key": api_key_value,
                                "key_info": key_info,
                                "warning": "[WARNING] IMPORTANT: Save this API key now! It will not be shown again."
                            }
                        else:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32603,
                                    "message": message
                                }
                            }), 400

                    elif tool_name == "list_my_api_keys":
                        # Requires authentication
                        authenticated_user, auth_token = get_authenticated_user()
                        if not authenticated_user:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32600,
                                    "message": "Authentication required. Please login first using user_login tool."
                                }
                            }), 401

                        success, api_keys = users_api.list_api_keys(authenticated_user, auth_token)

                        if success:
                            tool_result = {
                                "success": True,
                                "api_keys": api_keys,
                                "count": len(api_keys)
                            }
                        else:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32603,
                                    "message": "Failed to list API keys"
                                }
                            }), 400

                    elif tool_name == "revoke_api_key":
                        # Requires authentication
                        authenticated_user, auth_token = get_authenticated_user()
                        if not authenticated_user:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32600,
                                    "message": "Authentication required. Please login first using user_login tool."
                                }
                            }), 401

                        key_id = tool_args.get("key_id")

                        if not key_id:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32602,
                                    "message": "Missing required parameter (key_id)"
                                }
                            }), 400

                        success, message = users_api.delete_api_key(authenticated_user, auth_token, key_id)

                        if success:
                            tool_result = {
                                "success": True,
                                "message": message
                            }
                        else:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32603,
                                    "message": message
                                }
                            }), 404

                    # ========================================
                    # SEMANTIC MAPPING TOOLS (Sprint 3)
                    # ========================================
                    
                    elif tool_name == "add_semantic_map":
                        # Requires authentication
                        authenticated_user, auth_token = get_authenticated_user()
                        if not authenticated_user:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32600,
                                    "message": "Authentication required. Please login first."
                                }
                            }), 401

                        # Get active connection
                        success, message, connection = users_api.get_active_connection(authenticated_user, auth_token)
                        if not success or not connection:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32600,
                                    "message": "No active connection. Please activate a connection first."
                                }
                            }), 400

                        # Extract mapping parameters
                        concept = tool_args.get("concept")
                        mapping_type = tool_args.get("type", "entity")
                        
                        if not concept:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32602,
                                    "message": "Missing required parameter: concept"
                                }
                            }), 400

                        try:
                            # Create mapping object
                            mapping_data = {
                                "organization_id": connection.get("organization_id") or "default",
                                "connection_id": connection["id"],
                                "concept": concept,
                                "type": mapping_type,
                                "description": tool_args.get("description"),
                                "aliases": tool_args.get("aliases", [])
                            }

                            if mapping_type == "entity":
                                table = tool_args.get("table")
                                if not table:
                                    return jsonify({
                                        "jsonrpc": "2.0",
                                        "id": rpc_id,
                                        "error": {
                                            "code": -32602,
                                            "message": "Entity mappings require 'table' parameter"
                                        }
                                    }), 400

                                mapping_data["table"] = table
                                mapping_data["schema"] = tool_args.get("schema")
                                mapping_data["column_mappings"] = tool_args.get("column_mappings", {})

                                # Validate table exists (if connected)
                                if engine:
                                    try:
                                        inspector = inspect(engine)
                                        schema = mapping_data.get("schema")
                                        tables = inspector.get_table_names(schema=schema)
                                        
                                        if table not in tables:
                                            return jsonify({
                                                "jsonrpc": "2.0",
                                                "id": rpc_id,
                                                "error": {
                                                    "code": -32602,
                                                    "message": f"Table '{table}' not found in database. Available tables: {', '.join(tables)}"
                                                }
                                            }), 400

                                        # Validate columns exist
                                        if mapping_data["column_mappings"]:
                                            actual_columns = [c["name"] for c in inspector.get_columns(table, schema=schema)]
                                            invalid_columns = [col for col in mapping_data["column_mappings"].values() 
                                                             if col not in actual_columns]
                                            
                                            if invalid_columns:
                                                return jsonify({
                                                    "jsonrpc": "2.0",
                                                    "id": rpc_id,
                                                    "error": {
                                                        "code": -32602,
                                                        "message": f"Columns not found: {', '.join(invalid_columns)}. Available: {', '.join(actual_columns)}"
                                                    }
                                                }), 400

                                    except Exception as e:
                                        logger.warning(f"Could not validate table/columns: {e}")
                                        # Continue anyway - validation is optional

                            elif mapping_type == "relationship":
                                from_table = tool_args.get("from_table")
                                to_table = tool_args.get("to_table")
                                join_condition = tool_args.get("join_condition")

                                if not all([from_table, to_table, join_condition]):
                                    return jsonify({
                                        "jsonrpc": "2.0",
                                        "id": rpc_id,
                                        "error": {
                                            "code": -32602,
                                            "message": "Relationship mappings require 'from_table', 'to_table', and 'join_condition'"
                                        }
                                    }), 400

                                mapping_data.update({
                                    "from_table": from_table,
                                    "to_table": to_table,
                                    "from_schema": tool_args.get("from_schema"),
                                    "to_schema": tool_args.get("to_schema"),
                                    "join_condition": join_condition
                                })

                                # Validate tables exist (if connected)
                                if engine:
                                    try:
                                        inspector = inspect(engine)
                                        from_schema = mapping_data.get("from_schema")
                                        to_schema = mapping_data.get("to_schema")
                                        
                                        from_tables = inspector.get_table_names(schema=from_schema)
                                        to_tables = inspector.get_table_names(schema=to_schema)
                                        
                                        if from_table not in from_tables:
                                            return jsonify({
                                                "jsonrpc": "2.0",
                                                "id": rpc_id,
                                                "error": {
                                                    "code": -32602,
                                                    "message": f"Source table '{from_table}' not found"
                                                }
                                            }), 400
                                        
                                        if to_table not in to_tables:
                                            return jsonify({
                                                "jsonrpc": "2.0",
                                                "id": rpc_id,
                                                "error": {
                                                    "code": -32602,
                                                    "message": f"Target table '{to_table}' not found"
                                                }
                                            }), 400

                                    except Exception as e:
                                        logger.warning(f"Could not validate relationship tables: {e}")

                            # Create and add mapping
                            mapping = SemanticMapping(**mapping_data)
                            result_mapping = semantic_catalog.add_mapping(
                                mapping.organization_id,
                                mapping.connection_id,
                                mapping
                            )

                            tool_result = {
                                "success": True,
                                "message": f"Semantic mapping for '{concept}' created successfully",
                                "mapping": {
                                    "id": result_mapping.id,
                                    "concept": result_mapping.concept,
                                    "type": result_mapping.type,
                                    "created_at": result_mapping.created_at.isoformat()
                                }
                            }

                        except ValueError as e:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32602,
                                    "message": str(e)
                                }
                            }), 400
                        except Exception as e:
                            logger.error(f"Error adding semantic mapping: {e}")
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32603,
                                    "message": f"Failed to add semantic mapping: {str(e)}"
                                }
                            }), 500

                    elif tool_name == "list_semantic_maps":
                        # Requires authentication
                        authenticated_user, auth_token = get_authenticated_user()
                        if not authenticated_user:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32600,
                                    "message": "Authentication required. Please login first."
                                }
                            }), 401

                        # Get active connection
                        success, message, connection = users_api.get_active_connection(authenticated_user, auth_token)
                        if not success or not connection:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32600,
                                    "message": "No active connection. Please activate a connection first."
                                }
                            }), 400

                        try:
                            organization_id = connection.get("organization_id") or "default"
                            connection_id = connection["id"]
                            mapping_type = tool_args.get("type")  # Optional filter

                            mappings = semantic_catalog.get_mappings(
                                organization_id,
                                connection_id,
                                mapping_type=mapping_type
                            )

                            tool_result = {
                                "success": True,
                                "count": len(mappings),
                                "mappings": [
                                    {
                                        "id": m.id,
                                        "concept": m.concept,
                                        "type": m.type,
                                        "description": m.description,
                                        "aliases": m.aliases,
                                        "table": m.table if m.type == "entity" else None,
                                        "from_table": m.from_table if m.type == "relationship" else None,
                                        "to_table": m.to_table if m.type == "relationship" else None,
                                        "created_at": m.created_at.isoformat(),
                                        "updated_at": m.updated_at.isoformat()
                                    }
                                    for m in mappings
                                ]
                            }

                        except Exception as e:
                            logger.error(f"Error listing semantic mappings: {e}")
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32603,
                                    "message": f"Failed to list semantic mappings: {str(e)}"
                                }
                            }), 500

                    elif tool_name == "update_semantic_map":
                        # Requires authentication
                        authenticated_user, auth_token = get_authenticated_user()
                        if not authenticated_user:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32600,
                                    "message": "Authentication required. Please login first."
                                }
                            }), 401

                        # Get active connection
                        success, message, connection = users_api.get_active_connection(authenticated_user, auth_token)
                        if not success or not connection:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32600,
                                    "message": "No active connection. Please activate a connection first."
                                }
                            }), 400

                        mapping_id = tool_args.get("mapping_id")
                        if not mapping_id:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32602,
                                    "message": "Missing required parameter: mapping_id"
                                }
                            }), 400

                        try:
                            organization_id = connection.get("organization_id") or "default"
                            connection_id = connection["id"]

                            # Build updates dictionary (exclude mapping_id)
                            updates = {k: v for k, v in tool_args.items() if k != "mapping_id"}

                            updated_mapping = semantic_catalog.update_mapping(
                                organization_id,
                                connection_id,
                                mapping_id,
                                updates
                            )

                            tool_result = {
                                "success": True,
                                "message": f"Semantic mapping '{updated_mapping.concept}' updated successfully",
                                "mapping": {
                                    "id": updated_mapping.id,
                                    "concept": updated_mapping.concept,
                                    "type": updated_mapping.type,
                                    "version": updated_mapping.version,
                                    "updated_at": updated_mapping.updated_at.isoformat()
                                }
                            }

                        except ValueError as e:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32602,
                                    "message": str(e)
                                }
                            }), 400
                        except Exception as e:
                            logger.error(f"Error updating semantic mapping: {e}")
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32603,
                                    "message": f"Failed to update semantic mapping: {str(e)}"
                                }
                            }), 500

                    elif tool_name == "delete_semantic_map":
                        # Requires authentication
                        authenticated_user, auth_token = get_authenticated_user()
                        if not authenticated_user:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32600,
                                    "message": "Authentication required. Please login first."
                                }
                            }), 401

                        # Get active connection
                        success, message, connection = users_api.get_active_connection(authenticated_user, auth_token)
                        if not success or not connection:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32600,
                                    "message": "No active connection. Please activate a connection first."
                                }
                            }), 400

                        mapping_id = tool_args.get("mapping_id")
                        if not mapping_id:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32602,
                                    "message": "Missing required parameter: mapping_id"
                                }
                            }), 400

                        try:
                            organization_id = connection.get("organization_id") or "default"
                            connection_id = connection["id"]

                            success = semantic_catalog.delete_mapping(
                                organization_id,
                                connection_id,
                                mapping_id
                            )

                            if success:
                                tool_result = {
                                    "success": True,
                                    "message": f"Semantic mapping deleted successfully"
                                }
                            else:
                                return jsonify({
                                    "jsonrpc": "2.0",
                                    "id": rpc_id,
                                    "error": {
                                        "code": -32602,
                                        "message": f"Mapping with ID '{mapping_id}' not found"
                                    }
                                }), 404

                        except Exception as e:
                            logger.error(f"Error deleting semantic mapping: {e}")
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32603,
                                    "message": f"Failed to delete semantic mapping: {str(e)}"
                                }
                            }), 500

                    elif tool_name == "get_semantic_mapping":
                        # Requires authentication
                        authenticated_user, auth_token = get_authenticated_user()
                        if not authenticated_user:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32600,
                                    "message": "Authentication required. Please login first."
                                }
                            }), 401

                        # Get active connection
                        success, message, connection = users_api.get_active_connection(authenticated_user, auth_token)
                        if not success or not connection:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32600,
                                    "message": "No active connection. Please activate a connection first."
                                }
                            }), 400

                        mapping_id = tool_args.get("mapping_id")
                        if not mapping_id:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32602,
                                    "message": "Missing required parameter: mapping_id"
                                }
                            }), 400

                        try:
                            organization_id = connection.get("organization_id") or "default"
                            connection_id = connection["id"]

                            # Get all mappings and find the specific one
                            all_mappings = semantic_catalog.get_mappings(
                                organization_id,
                                connection_id
                            )
                            
                            mapping = None
                            for m in all_mappings:
                                if m.id == mapping_id:
                                    mapping = m
                                    break

                            if not mapping:
                                return jsonify({
                                    "jsonrpc": "2.0",
                                    "id": rpc_id,
                                    "error": {
                                        "code": -32602,
                                        "message": f"Mapping with ID '{mapping_id}' not found"
                                    }
                                }), 404

                            # Return complete mapping details
                            tool_result = {
                                "success": True,
                                "mapping": {
                                    "id": mapping.id,
                                    "organization_id": mapping.organization_id,
                                    "connection_id": mapping.connection_id,
                                    "concept": mapping.concept,
                                    "type": mapping.type,
                                    "description": mapping.description,
                                    "aliases": mapping.aliases,
                                    "table": mapping.table,
                                    "schema": mapping.schema,
                                    "column_mappings": mapping.column_mappings,
                                    "from_table": mapping.from_table,
                                    "to_table": mapping.to_table,
                                    "from_schema": mapping.from_schema,
                                    "to_schema": mapping.to_schema,
                                    "join_condition": mapping.join_condition,
                                    "created_at": mapping.created_at.isoformat(),
                                    "updated_at": mapping.updated_at.isoformat(),
                                    "version": mapping.version
                                }
                            }

                        except Exception as e:
                            logger.error(f"Error retrieving semantic mapping: {e}")
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32603,
                                    "message": f"Failed to retrieve semantic mapping: {str(e)}"
                                }
                            }), 500

                    elif tool_name == "suggest_semantic_maps":
                        # Requires authentication
                        authenticated_user, auth_token = get_authenticated_user()
                        if not authenticated_user:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32600,
                                    "message": "Authentication required. Please login first."
                                }
                            }), 401

                        # Get active connection
                        success, message, connection = users_api.get_active_connection(authenticated_user, auth_token)
                        if not success or not connection:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32600,
                                    "message": "No active connection. Please activate a connection first."
                                }
                            }), 400

                        try:
                            organization_id = connection.get("organization_id") or "default"
                            connection_id = connection["id"]

                            # Parameters
                            include_columns = tool_args.get("include_columns", True)
                            suggest_type = (tool_args.get("type") or "all").lower()
                            limit = tool_args.get("limit")

                            # Load existing mappings to avoid duplicates
                            existing = semantic_catalog.get_mappings(organization_id, connection_id) or []
                            existing_concepts = {m.concept for m in existing}
                            existing_tables = {m.table for m in existing if m.type == "entity" and m.table}

                            # Prepare engine/inspector
                            local_engine = engine
                            if local_engine is None:
                                from sqlalchemy import create_engine as _create_engine
                                local_engine = _create_engine(connection.get("connection_string"))

                            insp = inspect(local_engine)

                            # Helpers
                            def _humanize(name: str) -> str:
                                return name.replace("_", " ").strip().lower()

                            def _singularize(token: str) -> str:
                                t = token.lower()
                                if t.endswith("ses"):
                                    return t[:-2]  # e.g., "classes" -> "classe" (best-effort)
                                if t.endswith("s") and not t.endswith("ss"):
                                    return t[:-1]
                                return t

                            # Entity suggestions
                            entity_suggestions = []
                            if suggest_type in ("entity", "all"):
                                try:
                                    table_names = insp.get_table_names()
                                except Exception:
                                    table_names = []

                                for t in table_names:
                                    # Skip if already mapped
                                    if t in existing_tables:
                                        continue

                                    concept = _humanize(t)
                                    if concept in existing_concepts:
                                        continue

                                    aliases = list({
                                        _singularize(concept),
                                        concept.replace("_", " ")
                                    } - {concept})

                                    column_mappings = {}
                                    if include_columns:
                                        try:
                                            cols = insp.get_columns(t)
                                            for c in cols:
                                                col = c.get("name")
                                                if not col:
                                                    continue
                                                bt = _humanize(col)
                                                column_mappings[bt] = col
                                        except Exception as e:
                                            logger.debug(f"Could not introspect columns for {t}: {e}")

                                    reason = f"Derived from table '{t}'"
                                    confidence = 0.8
                                    try:
                                        # Boost confidence if common business columns exist
                                        cols_names = [c['name'] for c in insp.get_columns(t)]
                                        if any(n in cols_names for n in ["name", "full_name", "title", "email"]):
                                            confidence = 0.9
                                    except Exception:
                                        pass

                                    entity_suggestions.append({
                                        "suggestion_type": "entity",
                                        "concept": concept,
                                        "table": t,
                                        "schema": None,
                                        "aliases": aliases,
                                        "column_mappings": column_mappings if include_columns else {},
                                        "confidence": confidence,
                                        "reason": reason
                                    })

                                    if limit and len(entity_suggestions) >= limit:
                                        break

                            # Relationship suggestions (from FKs)
                            relationship_suggestions = []
                            if suggest_type in ("relationship", "all"):
                                try:
                                    introspector = SchemaIntrospector(local_engine)
                                    fks = introspector.get_table_relationships()
                                except Exception as e:
                                    logger.debug(f"Could not collect FK relationships: {e}")
                                    fks = []

                                for fk in fks:
                                    # Build join condition
                                    try:
                                        pairs = list(zip(fk.from_columns, fk.to_columns))
                                        cond = " AND ".join([f"{fk.from_table}.{a} = {fk.to_table}.{b}" for a, b in pairs])
                                    except Exception:
                                        cond = None

                                    concept = _humanize(f"{fk.from_table}_to_{fk.to_table}")
                                    aliases = [concept.replace("_", " ")]
                                    reason = f"Derived from foreign key {fk.from_table} -> {fk.to_table}"

                                    relationship_suggestions.append({
                                        "suggestion_type": "relationship",
                                        "concept": concept,
                                        "from_table": fk.from_table,
                                        "to_table": fk.to_table,
                                        "from_schema": None,
                                        "to_schema": None,
                                        "join_condition": cond or "",
                                        "aliases": aliases,
                                        "confidence": 0.85,
                                        "reason": reason
                                    })

                                    if limit and len(relationship_suggestions) >= limit:
                                        break

                            tool_result = {
                                "success": True,
                                "counts": {
                                    "entities": len(entity_suggestions),
                                    "relationships": len(relationship_suggestions)
                                },
                                "entity_suggestions": entity_suggestions,
                                "relationship_suggestions": relationship_suggestions,
                                "note": "Suggestions are not persisted. Use add_semantic_map to accept specific items."
                            }

                        except Exception as e:
                            logger.error(f"Error generating semantic suggestions: {e}")
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32603,
                                    "message": f"Failed to generate suggestions: {str(e)}"
                                }
                            }), 500

                    # ========================================
                    # NL TO SQL TOOL (natural_query)
                    # ========================================
                    elif tool_name == "natural_query":
                        # Autenticação obrigatória
                        authenticated_user, auth_token = get_authenticated_user()
                        if not authenticated_user:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {"code": -32600, "message": "Autenticação requerida. Faça login primeiro."}
                            }), 401

                        user_query = tool_args.get("query")
                        run_mode = tool_args.get("run_mode", "generate")
                        limit = tool_args.get("limit")
                        include_sql = tool_args.get("include_sql", True)
                        include_mappings_used = tool_args.get("include_mappings_used", False)

                        if not user_query or not str(user_query).strip():
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {"code": -32602, "message": "Parâmetro 'query' é obrigatório."}
                            }), 400

                        # Recupera conexão ativa do usuário
                        success, message, connection = users_api.get_active_connection(authenticated_user, auth_token)
                        if not success or not connection:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {"code": -32600, "message": "Nenhuma conexão ativa. Ative uma conexão antes de usar natural_query."}
                            }), 400

                        connection_string = connection.get("connection_string")
                        if not connection_string:
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {"code": -32603, "message": "Conexão ativa sem 'connection_string'."}
                            }), 500

                        # Monta contexto semântico
                        try:
                            organization_id = connection.get("organization_id") or "default"
                            mapped = semantic_catalog.get_mappings(organization_id, connection["id"]) or []
                        except Exception as e:
                            logger.warning(f"Falha ao carregar mappings semânticos: {e}")
                            mapped = []

                        def format_semantic(mappings):
                            lines = []
                            for m in mappings:
                                if m.type == "entity":
                                    cols = ", ".join([f"{k}->{v}" for k, v in (m.column_mappings or {}).items()]) if m.column_mappings else "(sem column_mappings)"
                                    aliases = ", ".join(m.aliases) if m.aliases else "(sem aliases)"
                                    lines.append(f"ENTITY {m.concept} table={m.table} schema={m.schema or '-'} aliases=[{aliases}] cols=[{cols}]")
                                elif m.type == "relationship":
                                    aliases = ", ".join(m.aliases) if m.aliases else "(sem aliases)"
                                    lines.append(f"REL {m.concept} {m.from_table} -> {m.to_table} on {m.join_condition} aliases=[{aliases}]")
                            return "\n" + "\n".join(lines) if lines else ""

                        semantic_context = format_semantic(mapped)

                        # Monta contexto de schema para tabelas mapeadas (somente se engine disponível)
                        schema_context = ""
                        try:
                            # Usa engine global se existir e assume mesma conexão; caso contrário cria executor isolado
                            local_engine = None
                            if engine is not None:
                                local_engine = engine
                            else:
                                # Cria engine temporário apenas para introspecção
                                from sqlalchemy import create_engine as _create_engine
                                local_engine = _create_engine(connection_string)
                            introspector = SchemaIntrospector(local_engine)
                            table_names = [m.table for m in mapped if m.type == "entity" and m.table]
                            short_descriptions = []
                            for t in table_names[:8]:  # Limita contexto para não explodir prompt
                                try:
                                    cols = introspector.inspector.get_columns(t)
                                    col_names = [c['name'] for c in cols]
                                    short_descriptions.append(f"{t}({', '.join(col_names[:15])}{'...' if len(col_names)>15 else ''})")
                                except Exception as e:
                                    logger.debug(f"Falha ao descrever tabela {t}: {e}")
                            if short_descriptions:
                                schema_context = "\n" + "\n".join(short_descriptions)
                        except Exception as e:
                            logger.warning(f"Falha ao gerar contexto de schema: {e}")
                            schema_context = ""

                        # Inicializa engine NL->SQL (mock LLM por enquanto)
                        try:
                            # Detect database dialect from connection string
                            dialect = None
                            try:
                                from sqlalchemy.engine.url import make_url
                                url = make_url(connection_string)
                                # Extract dialect (e.g., 'mssql', 'postgresql', 'mysql')
                                dialect = url.drivername.split('+')[0] if '+' in url.drivername else url.drivername
                                logger.info(f"Detected database dialect: {dialect}")
                            except Exception as e:
                                logger.warning(f"Failed to detect dialect from connection string: {e}")
                                dialect = None
                            
                            provider_mode = os.environ.get("SIMPLIQ_NL2SQL_PROVIDER", "mock").lower()
                            if provider_mode == "mock":
                                # Mock com respostas específicas para queries comuns + fallback
                                mock_responses = {
                                    "clientes": "<SQL>SELECT * FROM users</SQL>",
                                    "cliente": "<SQL>SELECT * FROM users</SQL>",
                                    "users": "<SQL>SELECT * FROM users</SQL>",
                                    "quantos": "<SQL>SELECT COUNT(*) FROM users</SQL>",
                                    "listar": "<SQL>SELECT * FROM users</SQL>",
                                    "liste": "<SQL>SELECT * FROM users</SQL>",
                                    "__default__": "<SQL>SELECT 1 as demo</SQL>"
                                }
                                llm_client = MockLLMClient(mock_responses)
                            elif provider_mode == "openai":
                                llm_client = OpenAIClient()
                            elif provider_mode == "anthropic":
                                llm_client = AnthropicClient()
                            elif provider_mode == "gemini":
                                llm_client = GeminiClient()
                            else:
                                logger.warning(f"Provider desconhecido '{provider_mode}', usando mock.")
                                llm_client = MockLLMClient({"__default__": "<SQL>SELECT 1</SQL>"})

                            # Create validator with detected dialect
                            validator = MinimalSQLValidator(max_rows=limit or 1000, dialect=dialect)
                            sql_executor = SimpleSQLExecutor(connection_string) if run_mode == "execute" else None
                            # Pass dialect to NL engine
                            nl_engine = NLtoSQLEngine(
                                llm_client, 
                                validator=validator, 
                                executor=sql_executor, 
                                config={"max_rows": limit or 1000},
                                dialect=dialect
                            )
                        except Exception as e:
                            logger.error(f"Erro inicializando NLtoSQLEngine: {e}")
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {"code": -32603, "message": f"Falha inicializando engine NL->SQL: {str(e)}"}
                            }), 500

                        try:
                            gen_result = nl_engine.generate_sql(user_query, semantic_context=semantic_context, schema_context=schema_context, include_sql=True, run_mode=run_mode, limit=limit)
                            if not gen_result.get("success"):
                                return jsonify({
                                    "jsonrpc": "2.0",
                                    "id": rpc_id,
                                    "error": {"code": -32602, "message": json.dumps(gen_result.get("error"))}
                                }), 400

                            tool_result = {
                                "success": True,
                                "sql_generated": gen_result.get("sql_generated"),
                                "executed": run_mode == "execute",
                                "row_count": gen_result.get("row_count"),
                                "results": gen_result.get("results"),
                                "execution_time_ms": gen_result.get("execution_time_ms"),
                                "context": {
                                    "semantic_mappings": len(mapped),
                                    "schema_tables": len([m.table for m in mapped if m.type == "entity" and m.table]),
                                    "provider_mode": provider_mode,
                                    "dialect": dialect or "unknown"
                                }
                            }
                            
                            # Include mappings used if requested
                            if include_mappings_used and mapped:
                                # Simple heuristic: check which mappings' concepts/aliases/tables appear in query or generated SQL
                                query_lower = user_query.lower()
                                sql_lower = gen_result.get("sql_generated", "").lower()
                                combined_text = query_lower + " " + sql_lower
                                
                                mappings_used = []
                                for m in mapped:
                                    # Check if concept, aliases, or table names appear in query/SQL
                                    terms_to_check = [m.concept] + (m.aliases or [])
                                    if m.table:
                                        terms_to_check.append(m.table)
                                    if m.from_table:
                                        terms_to_check.append(m.from_table)
                                    if m.to_table:
                                        terms_to_check.append(m.to_table)
                                    
                                    # Check column mappings
                                    if m.column_mappings:
                                        terms_to_check.extend(m.column_mappings.keys())
                                        terms_to_check.extend(m.column_mappings.values())
                                    
                                    # If any term appears in the combined text, consider it used
                                    if any(term.lower() in combined_text for term in terms_to_check if term):
                                        mappings_used.append({
                                            "id": m.id,
                                            "concept": m.concept,
                                            "type": m.type,
                                            "table": m.table if m.type == "entity" else None,
                                            "from_table": m.from_table if m.type == "relationship" else None,
                                            "to_table": m.to_table if m.type == "relationship" else None,
                                            "aliases": m.aliases,
                                            "description": m.description
                                        })
                                
                                tool_result["mappings_used"] = mappings_used
                                tool_result["context"]["mappings_used_count"] = len(mappings_used)
                                
                        except Exception as e:
                            logger.error(f"Erro gerando SQL da consulta natural: {e}")
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {"code": -32603, "message": f"Falha ao gerar SQL: {str(e)}"}
                            }), 500

                    else:
                        # Check if any plugin can handle this tool
                        try:
                            plugin_result = plugin_registry.handle_tool_call(tool_name, tool_args)
                            if plugin_result is not None:
                                tool_result = plugin_result
                                logger.info(f"Tool '{tool_name}' handled by plugin")
                            else:
                                # No plugin handled this tool
                                return jsonify({
                                    "jsonrpc": "2.0",
                                    "id": rpc_id,
                                    "error": {
                                        "code": -32601,
                                        "message": f"Unknown tool: {tool_name}"
                                    }
                                }), 400
                        except Exception as e:
                            logger.error(f"Error executing plugin tool '{tool_name}': {e}")
                            return jsonify({
                                "jsonrpc": "2.0",
                                "id": rpc_id,
                                "error": {
                                    "code": -32603,
                                    "message": f"Plugin tool execution failed: {str(e)}"
                                }
                            }), 500
                    
                    # Return successful tool result
                    return jsonify({
                        "jsonrpc": "2.0",
                        "id": rpc_id,
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": json.dumps(tool_result, indent=2)
                                }
                            ]
                        }
                    })
                
                # Unknown JSON-RPC method
                else:
                    return jsonify({
                        "jsonrpc": "2.0",
                        "id": rpc_id,
                        "error": {
                            "code": -32601,
                            "message": f"Method not found: {rpc_method}"
                        }
                    }), 404
            
            # Fallback to simple tool execution format (for testing)
            tool_name = data.get("method") or data.get("tool") or data.get("name")
            params = data.get("params", {}) or data.get("arguments", {}) or data.get("input", {})
            
            # If no tool name found, return error with helpful message
            if not tool_name:
                return jsonify({
                    "error": "Missing tool name. Expected 'method', 'tool', or 'name' field in request.",
                    "received_data": data
                }), 400
            
            # Route to appropriate tool (simple format)
            if tool_name == "get_config":
                config_data = load_config()
                if "error" not in config_data:
                    connection_string = config_data.get("connection_string", "")
                    db_info = get_db_info(connection_string)
                    config_data["db_info"] = db_info
                return jsonify({"result": config_data})
            
            elif tool_name == "update_config":
                connection_string = params.get("connection_string")
                if not connection_string:
                    return jsonify({"error": "Missing connection_string parameter"}), 400
                save_config({"connection_string": connection_string})
                return jsonify({"result": {"message": "Configuration updated successfully"}})
            
            elif tool_name == "check_status":
                if engine:
                    try:
                        with engine.connect() as conn:
                            pass
                        return jsonify({"result": {"status": "connected", "message": "Database is accessible"}})
                    except SQLAlchemyError as e:
                        return jsonify({"result": {"status": "error", "message": "Database connection failed", "details": str(e)}})
                else:
                    return jsonify({"result": {"status": "disconnected", "message": "Not connected to any database"}})
            
            elif tool_name == "list_objects":
                if not engine:
                    return jsonify({"error": "Not connected to any database. Use connect tool first."}), 400
                
                try:
                    inspector = inspect(engine)
                    schemas = inspector.get_schema_names() if hasattr(inspector, 'get_schema_names') else []
                    tables = inspector.get_table_names() if hasattr(inspector, 'get_table_names') else []
                    views = inspector.get_view_names() if hasattr(inspector, 'get_view_names') else []
                    
                    return jsonify({
                        "result": {
                            "schemas": schemas,
                            "tables": tables,
                            "views": views,
                            "note": "User information is not available through SQLAlchemy inspection"
                        }
                    })
                except SQLAlchemyError as e:
                    return jsonify({"error": f"Failed to retrieve database objects: {str(e)}"}), 500
            
            elif tool_name == "connect":
                try:
                    connect_to_db()
                    return jsonify({"result": {"message": "Successfully connected to the database"}})
                except Exception as e:
                    return jsonify({"error": f"Failed to connect: {str(e)}"}), 500
            
            elif tool_name == "disconnect":
                disconnect_from_db()
                return jsonify({"result": {"message": "Successfully disconnected from the database"}})
            
            elif tool_name == "validate_connection":
                connection_string = params.get("connection_string")
                if not connection_string:
                    return jsonify({"error": "Missing connection_string parameter"}), 400

                result = validate_connection_complete(connection_string)
                return jsonify({"result": result})

            elif tool_name == "build_connection":
                if not params.get("dialect"):
                    return jsonify({"error": "Missing required parameter 'dialect'"}), 400
                if not params.get("database"):
                    return jsonify({"error": "Missing required parameter 'database'"}), 400

                result = build_connection_string_from_params(params)
                return jsonify({"result": result})

            else:
                return jsonify({"error": f"Unknown tool: {tool_name}"}), 400
                
        except Exception as e:
            return jsonify({"error": f"Error executing tool: {str(e)}"}), 500


@app.route("/.well-known/mcp", methods=["GET"])
def mcp_info():
    """MCP protocol information endpoint."""
    return jsonify({
        "mcpVersion": "1.0",
        "serverInfo": {
            "name": "SimpliqData",
            "version": "1.0.0"
        },
        "capabilities": {
            "tools": True
        }
    })


@app.route("/register", methods=["POST"])
def register_client():
    """
    MCP client registration endpoint.

    This endpoint is called by mcp-remote clients (like Claude Desktop) to register
    themselves with the MCP server. It's part of the MCP protocol handshake.

    Returns:
        JSON response with registration confirmation
    """
    try:
        # Get request data
        data = request.get_json() or {}

        logger.info(f"Client registration request: {data}")

        # Extract client information
        client_info = data.get('clientInfo', {})
        client_name = client_info.get('name', 'Unknown Client')
        client_version = client_info.get('version', 'Unknown')

        # Log registration
        logger.info(f"Registered MCP client: {client_name} v{client_version}")

        # Return success response
        return jsonify({
            "success": True,
            "serverInfo": {
                "name": "SimpliqData",
                "version": "1.0.0"
            },
            "capabilities": {
                "tools": True,
                "prompts": False,
                "resources": False,
                "logging": True
            },
            "protocolVersion": "2024-11-05"
        }), 200

    except Exception as e:
        logger.error(f"Error during client registration: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/favicon.ico", methods=["GET"])
def favicon():
    """Serve favicon for the MCP server."""
    # Simple SVG favicon with SD initials (SimpliqData)
    svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
        <rect width="32" height="32" rx="6" fill="#2563eb"/>
        <text x="16" y="22" font-family="Arial, sans-serif" font-size="14" font-weight="bold"
              fill="white" text-anchor="middle">SD</text>
    </svg>'''

    # Convert SVG to bytes
    svg_bytes = io.BytesIO(svg_content.encode('utf-8'))

    return send_file(
        svg_bytes,
        mimetype='image/svg+xml',
        as_attachment=False,
        download_name='favicon.ico'
    )


@app.route("/config", methods=["GET", "POST"])
def config():
    """Retrieve (GET) or update (POST) the server configuration.

    GET: returns the full YAML config plus derived db_info.
    POST: accepts {"connection_string": "..."} and updates it without wiping other keys.
    """
    if request.method == "GET":
        cfg = load_config()
        if "error" in cfg:
            return jsonify(cfg), 404

        # Attach db info for convenience
        conn = cfg.get("connection_string", "")
        cfg["db_info"] = get_db_info(conn) if conn else {}
        return jsonify(cfg)

    # POST - update connection_string
    data = request.json or {}
    new_cs = data.get("connection_string")
    if not new_cs:
        return jsonify({"error": "Missing field: connection_string"}), 400

    try:
        save_config({"connection_string": new_cs})
        return jsonify({"success": True, "message": "Configuration updated successfully"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/connect", methods=["POST"])
def connect():
    """Connect or reconnect to the database."""
    try:
        connect_to_db()
        return jsonify({"message": "Successfully connected to the database."})
    except Exception as e:
        return jsonify({"error": f"Failed to connect: {str(e)}"}), 500


@app.route("/disconnect", methods=["POST"])
def disconnect():
    """Disconnect from the database."""
    disconnect_from_db()
    return jsonify({"message": "Successfully disconnected from the database."})


@app.route("/validate", methods=["POST"])
def validate():
    """Validate a database connection string.

    Request JSON body:
      {"connection_string": "dialect://user:pass@host:port/database"}

    Returns comprehensive validation details (format, network reachability,
    connection test results) produced by validate_connection_complete().
    """
    data = request.json or {}
    if "connection_string" not in data:
        return jsonify({
            "error": "Missing 'connection_string' field",
            "usage": {
                "method": "POST",
                "body": {"connection_string": "dialect://user:pass@host:port/database"}
            }
        }), 400

    connection_string = data["connection_string"]
    validation_result = validate_connection_complete(connection_string)
    return jsonify(validation_result)


@app.route("/build-connection", methods=["POST"])
def build_connection():
    """
    Build and validate a SQLAlchemy connection string from individual parameters.

    This endpoint allows you to construct a connection string by providing separate
    parameters (dialect, host, port, username, password, database, etc.) instead of
    a complete connection string. Each parameter is validated individually, and the
    resulting connection string is tested for validity.

    Request body:
    {
        "dialect": "postgresql",           // Required: postgresql, mysql, sqlite, oracle, mssql, mariadb
        "driver": "psycopg2",              // Optional: specific driver (e.g., psycopg2, pymysql)
        "username": "myuser",              // Optional (required for non-SQLite)
        "password": "mypass",              // Optional (will be URL-encoded if needed)
        "host": "localhost",               // Required for non-SQLite databases
        "port": 5432,                      // Optional (uses default if not specified)
        "database": "mydb",                // Required: database name or path
        "query": {"key": "value"}          // Optional: additional query parameters
    }

    Response:
    {
        "success": true/false,
        "connection_string": "postgresql://...",
        "validation": {...},               // Complete validation results
        "parameter_errors": {...},         // Errors for specific parameters
        "parameter_warnings": {...}        // Warnings for specific parameters
    }
    """
    data = request.json

    if not data:
        return jsonify({
            "error": "Missing request body",
            "usage": {
                "method": "POST",
                "required_fields": ["dialect", "database"],
                "optional_fields": ["driver", "username", "password", "host", "port", "query"],
                "example": {
                    "dialect": "postgresql",
                    "host": "localhost",
                    "port": 5432,
                    "username": "user",
                    "password": "pass",
                    "database": "mydb"
                }
            }
        }), 400

    # Check required parameters
    if "dialect" not in data:
        return jsonify({
            "error": "Missing required parameter 'dialect'",
            "valid_dialects": ["postgresql", "mysql", "sqlite", "oracle", "mssql", "mariadb"]
        }), 400

    if "database" not in data:
        return jsonify({
            "error": "Missing required parameter 'database'",
            "hint": "For SQLite, provide a file path or ':memory:'. For other databases, provide the database name."
        }), 400

    result = build_connection_string_from_params(data)

    return jsonify(result)


# ========================
# Multi-User Endpoints
# ========================

@app.route("/users", methods=["GET", "POST"])
def users():
    """List users (GET) or create a new user (POST)."""
    if request.method == "GET":
        users_list = users_api.list_users()
        return jsonify({"success": True, "users": users_list, "count": len(users_list)})

    data = request.json or {}
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    full_name = data.get("full_name", "")

    missing = [f for f in ["username", "password", "email"] if not data.get(f)]
    if missing:
        return jsonify({"success": False, "error": f"Missing fields: {', '.join(missing)}"}), 400

    success, message, user_data = users_api.create_user(username, password, email, full_name)
    if success:
        return jsonify({"success": True, "message": message, "user": user_data}), 201
    return jsonify({"success": False, "error": message}), 400


@app.route("/users/login", methods=["POST"])
def login():
    """User login endpoint."""
    data = request.json

    if not data:
        return jsonify({"success": False, "error": "Missing request body"}), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"success": False, "error": "Missing username or password"}), 400

    success, message, session_token = users_api.authenticate(username, password)

    if success:
        return jsonify({
            "success": True,
            "message": message,
            "session_token": session_token,
            "username": username
        })
    else:
        return jsonify({"success": False, "error": message}), 401


@app.route("/users/logout", methods=["POST"])
@require_auth
def logout(authenticated_user=None, auth_token=None):
    """User logout endpoint."""
    success, message = users_api.logout(auth_token)

    if success:
        return jsonify({"success": True, "message": message})
    else:
        return jsonify({"success": False, "error": message}), 400


@app.route("/users/<username>", methods=["GET", "PUT", "DELETE"])
@require_auth
def user_detail(username, authenticated_user=None, auth_token=None):
    """Get, update, or delete a specific user."""
    # Users can only access/modify their own data (simple authorization)
    if username != authenticated_user:
        return jsonify({"success": False, "error": "Unauthorized access"}), 403

    if request.method == "GET":
        user_data = users_api.get_user(username, auth_token)

        if user_data:
            return jsonify({"success": True, "user": user_data})
        else:
            return jsonify({"success": False, "error": "User not found"}), 404

    elif request.method == "PUT":
        data = request.json

        if not data:
            return jsonify({"success": False, "error": "Missing request body"}), 400

        email = data.get("email")
        full_name = data.get("full_name")
        password = data.get("password")

        success, message = users_api.update_user(
            username, auth_token, email=email, full_name=full_name, password=password
        )

        if success:
            return jsonify({"success": True, "message": message})
        else:
            return jsonify({"success": False, "error": message}), 400

    elif request.method == "DELETE":
        success, message = users_api.delete_user(username, auth_token)

        if success:
            return jsonify({"success": True, "message": message})
        else:
            return jsonify({"success": False, "error": message}), 400


@app.route("/users/<username>/connections", methods=["GET", "POST"])
@require_auth
def user_connections(username, authenticated_user=None, auth_token=None):
    """List or add connections for a user."""
    # Users can only access their own connections
    if username != authenticated_user:
        return jsonify({"success": False, "error": "Unauthorized access"}), 403

    if request.method == "GET":
        success, message, connections = users_api.list_connections(username, auth_token)

        if success:
            # Get active connection ID
            _, _, active_conn = users_api.get_active_connection(username, auth_token)
            active_id = active_conn['id'] if active_conn else None

            return jsonify({
                "success": True,
                "connections": connections,
                "active_connection_id": active_id,
                "count": len(connections)
            })
        else:
            return jsonify({"success": False, "error": message}), 404

    elif request.method == "POST":
        data = request.json

        if not data:
            return jsonify({"success": False, "error": "Missing request body"}), 400

        name = data.get("name")
        connection_string = data.get("connection_string")
        description = data.get("description", "")

        if not name:
            return jsonify({"success": False, "error": "Missing connection name"}), 400

        if not connection_string:
            return jsonify({"success": False, "error": "Missing connection string"}), 400

        success, message, connection = users_api.add_connection(
            username, auth_token, name, connection_string, description
        )

        if success:
            return jsonify({
                "success": True,
                "message": message,
                "connection": connection
            }), 201
        else:
            return jsonify({"success": False, "error": message}), 400


@app.route("/users/<username>/connections/<connection_id>", methods=["GET", "PUT", "DELETE"])
@require_auth
def user_connection_detail(username, connection_id, authenticated_user=None, auth_token=None):
    """Get, update, or delete a specific connection."""
    if username != authenticated_user:
        return jsonify({"success": False, "error": "Unauthorized access"}), 403

    if request.method == "GET":
        success, message, connection = users_api.get_connection(username, auth_token, connection_id)

        if success:
            return jsonify({"success": True, "connection": connection})
        else:
            return jsonify({"success": False, "error": message}), 404

    elif request.method == "PUT":
        data = request.json

        if not data:
            return jsonify({"success": False, "error": "Missing request body"}), 400

        name = data.get("name")
        connection_string = data.get("connection_string")
        description = data.get("description")

        success, message, connection = users_api.update_connection(
            username, auth_token, connection_id,
            name=name, connection_string=connection_string, description=description
        )

        if success:
            return jsonify({"success": True, "message": message, "connection": connection})
        else:
            return jsonify({"success": False, "error": message}), 400

    elif request.method == "DELETE":
        success, message = users_api.delete_connection(username, auth_token, connection_id)

        if success:
            return jsonify({"success": True, "message": message})
        else:
            return jsonify({"success": False, "error": message}), 400


@app.route("/users/<username>/connections/<connection_id>/activate", methods=["POST"])
@require_auth
def activate_connection(username, connection_id, authenticated_user=None, auth_token=None):
    """Activate a connection for a user."""
    if username != authenticated_user:
        return jsonify({"success": False, "error": "Unauthorized access"}), 403

    success, message, connection = users_api.set_active_connection(username, auth_token, connection_id)

    if success:
        return jsonify({
            "success": True,
            "message": message,
            "connection": connection
        })
    else:
        return jsonify({"success": False, "error": message}), 404


@app.route("/users/<username>/connections/<connection_id>/test", methods=["POST"])
@require_auth
def test_user_connection(username, connection_id, authenticated_user=None, auth_token=None):
    """Test a specific connection."""
    if username != authenticated_user:
        return jsonify({"success": False, "error": "Unauthorized access"}), 403

    # Get the connection
    success, message, connection = users_api.get_connection(username, auth_token, connection_id)

    if not success:
        return jsonify({"success": False, "error": message}), 404

    # Validate the connection
    connection_string = connection['connection_string']
    validation_result = validate_connection_complete(connection_string)

    # Update test result
    users_api.update_connection_test_result(
        username, auth_token, connection_id,
        validation_result['overall_valid'],
        json.dumps(validation_result['summary'])
    )

    return jsonify({
        "success": True,
        "connection_id": connection_id,
        "connection_name": connection['name'],
        "validation": validation_result
    })


if __name__ == "__main__":
    # Load server configuration
    server_config = get_server_config()

    # Print startup information (both print and logger)
    print("\n" + "="*70)
    print(f"Starting {server_config['name']} MCP Server v{server_config['version']}")
    print("="*70)
    logger.info("="*70)
    logger.info(f"Starting {server_config['name']} MCP Server v{server_config['version']}")
    logger.info("="*70)

    # Determine protocol based on SSL configuration
    protocol = "https" if server_config["ssl_enabled"] else "http"
    host = server_config["host"]
    port = server_config["port"]

    # Avoid unicode symbols that break Windows cp1252 console
    print(f"\nServer URL: {protocol}://{host}:{port}")
    logger.info(f"Server will be available at: {protocol}://{host}:{port}")

    # Logging Information
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = yaml.safe_load(f)
            logging_config = config.get('logging', {})
            print(f"\nLogging Configuration:")
            print(f"   Level: {logging_config.get('level', 'INFO')}")
            print(f"   Console: ENABLED (você verá logs aqui)")
            print(f"   File: {logging_config.get('log_to_file', False)}")
            if logging_config.get('log_to_file'):
                print(f"   Log file: {logging_config.get('log_file', 'mcp_server.log')}")
            logger.info(f"\nLogging Configuration:")
            logger.info(f"  Level: {logging_config.get('level', 'INFO')}")
            logger.info(f"  Log to file: {logging_config.get('log_to_file', False)}")
            if logging_config.get('log_to_file'):
                logger.info(f"  Log file: {logging_config.get('log_file', 'mcp_server.log')}")
    except Exception as e:
        logger.warning(f"Could not read logging config: {e}")

    # SSL Information
    if server_config["ssl_enabled"]:
        print(f"\nSSL/HTTPS: ENABLED")
        print(f"   Certificate: {server_config['ssl_cert']}")
        print(f"   Key: {server_config['ssl_key']}")
        logger.info("SSL/HTTPS: ENABLED")
    else:
        print(f"\nSSL/HTTPS: DISABLED (Using HTTP)")
        logger.info("SSL/HTTPS: DISABLED (Using HTTP)")

    print("\n" + "="*70)
    print("MCP TOOLS AVAILABLE (38 tools total)")
    print("="*70)
    print("  Database: 10 tools (includes describe_table, get_table_relationships)")
    print("  User Management: 3 tools")
    print("  Connections: 5 tools")
    print("  Organizations: 7 tools")
    print("  API Keys: 3 tools")
    print("  Authentication: 3 tools")
    print("="*70)

    logger.info("\n" + "="*70)
    logger.info("MCP TOOLS AVAILABLE (38 tools total)")
    logger.info("="*70)
    logger.info("  Database Tools: get_config, update_config, check_status, list_objects,")
    logger.info("                  connect, disconnect, validate_connection, build_connection,")
    logger.info("                  describe_table, get_table_relationships")
    logger.info("")
    logger.info("  User Tools: create_user, user_login, list_users")
    logger.info("")
    logger.info("  Connection Tools: add_connection, list_connections, activate_connection,")
    logger.info("                    test_connection, remove_connection")
    logger.info("")
    logger.info("  Organization Tools: create_organization, list_organizations,")
    logger.info("                      get_organization, update_organization,")
    logger.info("                      delete_organization, list_organization_users,")
    logger.info("                      list_organization_connections")
    logger.info("\n" + "="*70)

    print("\nIMPORTANTE: Você verá logs de requisições abaixo quando o Claude Desktop se conectar e executar ferramentas.")
    print("Servidor pronto! Aguardando conexões...")
    print("(Press CTRL+C to stop)\n")
    logger.info("\nPress CTRL+C to stop the server\n")

    logger.debug("TESTE DEBUG...")

    # Start the server with or without SSL
    try:
        if server_config["ssl_enabled"]:
            # Create SSL context and start HTTPS server
            ssl_context = create_ssl_context(
                server_config["ssl_cert"],
                server_config["ssl_key"]
            )
            logger.info(f"Starting HTTPS server on {host}:{port}...")

            # IMPORTANT: use_reloader=False prevents Flask from restarting the process
            # ssl_context parameter enables HTTPS mode
            app.run(
                host=host,
                port=port,
                ssl_context=ssl_context,  # Pass SSL context to enable HTTPS
                debug=False,  # Disable debug mode to prevent process restart
                use_reloader=False,  # Disable reloader to keep logging config
                threaded=True  # Enable threading for better performance
            )

        else:
            logger.info(f"Starting HTTP server on {host}:{port}...")
            app.run(host=host, port=port, debug=False, use_reloader=False, threaded=True)
        
    except RuntimeError as e:
        logger.error(f"ERROR: {e}")
        logger.error("Please check your SSL configuration in config.yml")
        exit(1)
    except Exception as e:
        logger.error(f"ERROR: Failed to start server: {e}")
        exit(1)