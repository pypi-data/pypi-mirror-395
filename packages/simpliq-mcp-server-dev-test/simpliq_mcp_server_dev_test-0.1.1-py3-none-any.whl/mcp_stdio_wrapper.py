#!/usr/bin/env python3
"""
SimpliQ MCP Server - STDIO Wrapper
Wrapper que permite Claude Desktop conectar via stdio ao servidor HTTP MCP

Autor: Gerson Amorim
Data: 26 de Novembro de 2025
"""

import sys
import json
import requests
from typing import Dict, Any, Optional
import logging
import os

# Configurar logging para arquivo (não para stdout, que é usado para MCP)
log_path = os.path.join(os.path.dirname(__file__), 'mcp_stdio_wrapper.log')
logging.basicConfig(
    filename=log_path,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# URL do MCP Server HTTP (pode ser customizado via env var)
MCP_SERVER_URL = os.environ.get("MCP_SERVER_URL", "http://localhost:8000")

# API Key authentication (simpler than OAuth)
API_KEY = os.environ.get("SIMPLIQ_API_KEY", None)

# OAuth credentials (fallback se API key não estiver disponível)
OAUTH_CLIENT_ID = None
OAUTH_CLIENT_SECRET = None
OAUTH_TOKEN = None

# Log da configuração
logger.info(f"MCP Server URL configured: {MCP_SERVER_URL}")
if API_KEY:
    logger.info(f"API Key authentication enabled: {API_KEY[:10]}...")


def get_oauth_token() -> Optional[str]:
    """Obtém token OAuth se credenciais estiverem disponíveis"""
    global OAUTH_TOKEN, OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET

    if not OAUTH_CLIENT_ID or not OAUTH_CLIENT_SECRET:
        return None

    if OAUTH_TOKEN:
        return OAUTH_TOKEN

    # URL do OAuth server (customizável via env)
    oauth_token_url = os.environ.get("OAUTH_TOKEN_ENDPOINT", "http://localhost:8002/oauth/token")

    try:
        response = requests.post(
            oauth_token_url,
            data={
                "grant_type": "client_credentials",
                "client_id": OAUTH_CLIENT_ID,
                "client_secret": OAUTH_CLIENT_SECRET,
                "scope": "admin:org"
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

        if response.status_code == 200:
            OAUTH_TOKEN = response.json().get("access_token")
            logger.info("OAuth token obtained successfully")
            return OAUTH_TOKEN
        else:
            logger.error(f"Failed to get OAuth token: {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"Error getting OAuth token: {e}")
        return None


def send_mcp_request(method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Envia requisição JSON-RPC para o MCP Server HTTP"""

    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params or {},
        "id": 1
    }

    headers = {"Content-Type": "application/json"}

    # Adicionar API Key se disponível (prioridade sobre OAuth)
    if API_KEY:
        headers["X-API-Key"] = API_KEY
        logger.debug(f"Using API Key authentication")
    else:
        # Fallback: Adicionar token OAuth se disponível
        token = get_oauth_token()
        if token:
            headers["Authorization"] = f"Bearer {token}"
            logger.debug(f"Using OAuth token authentication")

    logger.debug(f"Sending request: {method} with params: {params}")

    try:
        response = requests.post(
            MCP_SERVER_URL,
            json=payload,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()
        result = response.json()

        logger.debug(f"Response received: {result}")
        return result

    except requests.exceptions.RequestException as e:
        logger.error(f"HTTP request failed: {e}")
        return {
            "jsonrpc": "2.0",
            "error": {
                "code": -32603,
                "message": f"HTTP request failed: {str(e)}"
            },
            "id": 1
        }
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON response: {e}")
        return {
            "jsonrpc": "2.0",
            "error": {
                "code": -32700,
                "message": "Parse error: Invalid JSON response from server"
            },
            "id": 1
        }


def handle_initialize(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle MCP initialize request"""
    return {
        "jsonrpc": "2.0",
        "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {},
                "prompts": {},
                "resources": {}
            },
            "serverInfo": {
                "name": "SimpliQ MCP Server",
                "version": "1.0.0"
            }
        },
        "id": params.get("id", 1)
    }


def handle_tools_list(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle tools/list request - forward to HTTP server"""
    response = send_mcp_request("tools/list", {})
    response["id"] = params.get("id", 1)
    return response


def handle_tools_call(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle tools/call request - forward to HTTP server"""
    response = send_mcp_request("tools/call", params)
    response["id"] = params.get("id", 1)
    return response


def handle_prompts_list(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle prompts/list request"""
    return {
        "jsonrpc": "2.0",
        "result": {
            "prompts": []
        },
        "id": params.get("id", 1)
    }


def handle_resources_list(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle resources/list request"""
    return {
        "jsonrpc": "2.0",
        "result": {
            "resources": []
        },
        "id": params.get("id", 1)
    }


def handle_notifications_cancelled(params: Dict[str, Any]) -> None:
    """Handle notifications/cancelled - just log and ignore"""
    logger.debug(f"Notification cancelled: {params}")
    # Notifications don't require a response
    return None


def handle_notifications_initialized(params: Dict[str, Any]) -> None:
    """Handle notifications/initialized - just log and ignore"""
    logger.debug(f"Client initialized notification received")
    # Notifications don't require a response
    return None


def handle_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Route request to appropriate handler"""

    method = request_data.get("method")
    params = request_data.get("params", {})

    logger.info(f"Handling request: {method}")

    handlers = {
        "initialize": handle_initialize,
        "tools/list": handle_tools_list,
        "tools/call": handle_tools_call,
        "prompts/list": handle_prompts_list,
        "resources/list": handle_resources_list,
        "notifications/cancelled": handle_notifications_cancelled,
        "notifications/initialized": handle_notifications_initialized,
    }

    handler = handlers.get(method)

    if handler:
        try:
            result = handler({"id": request_data.get("id"), **params})
            # Notifications don't need responses
            if result is None:
                return None
            return result
        except Exception as e:
            logger.error(f"Handler error: {e}", exc_info=True)
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                },
                "id": request_data.get("id", 1)
            }
    else:
        logger.warning(f"Unknown method: {method}")
        return {
            "jsonrpc": "2.0",
            "error": {
                "code": -32601,
                "message": f"Method not found: {method}"
            },
            "id": request_data.get("id", 1)
        }


def main():
    """Main stdio loop"""

    logger.info("SimpliQ MCP STDIO Wrapper started")
    logger.info(f"MCP Server URL: {MCP_SERVER_URL}")

    # Ler variáveis de ambiente para OAuth
    import os
    global OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET
    OAUTH_CLIENT_ID = os.environ.get("OAUTH_CLIENT_ID")
    OAUTH_CLIENT_SECRET = os.environ.get("OAUTH_CLIENT_SECRET")

    if OAUTH_CLIENT_ID:
        logger.info(f"OAuth enabled with client_id: {OAUTH_CLIENT_ID[:8]}...")

    try:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue

            logger.debug(f"Received line: {line}")

            try:
                request_data = json.loads(line)
                response = handle_request(request_data)

                # Only send response if not None (notifications don't need responses)
                if response is not None:
                    response_str = json.dumps(response)
                    sys.stdout.write(response_str + "\n")
                    sys.stdout.flush()
                    logger.debug(f"Sent response: {response_str}")
                else:
                    logger.debug("No response needed (notification)")

            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {e}")
                error_response = {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32700,
                        "message": "Parse error: Invalid JSON"
                    },
                    "id": None
                }
                sys.stdout.write(json.dumps(error_response) + "\n")
                sys.stdout.flush()

            except Exception as e:
                logger.error(f"Unexpected error: {e}", exc_info=True)
                error_response = {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32603,
                        "message": f"Internal error: {str(e)}"
                    },
                    "id": None
                }
                sys.stdout.write(json.dumps(error_response) + "\n")
                sys.stdout.flush()

    except KeyboardInterrupt:
        logger.info("Shutting down (KeyboardInterrupt)")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
    finally:
        logger.info("SimpliQ MCP STDIO Wrapper stopped")


if __name__ == "__main__":
    main()
