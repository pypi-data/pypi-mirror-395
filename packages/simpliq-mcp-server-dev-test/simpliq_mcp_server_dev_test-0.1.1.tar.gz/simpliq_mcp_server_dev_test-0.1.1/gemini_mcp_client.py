#!/usr/bin/env python3
"""
SimpliqData MCP Client for Google Gemini
========================================

This script demonstrates how to use the SimpliqData MCP server with Google Gemini AI.

API key resolution (preferred first):
1) simpliq_server/config.yml -> nl2sql.gemini.api_key
2) Environment variables: GEMINI_API_KEY, then GOOGLE_API_KEY

Requirements:
    pip install google-generativeai requests pyyaml

Usage:
    # Preferred: put your key in simpliq_server/config.yml under nl2sql.gemini.api_key
    # Fallback: set an environment variable
    #   PowerShell:  $env:GEMINI_API_KEY = "your-api-key"
    #   bash/zsh:    export GEMINI_API_KEY="your-api-key"
    python gemini_mcp_client.py
"""

import os
import json
from pathlib import Path

import requests
try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover - optional dependency for reading config
    yaml = None  # Fallback to env-only if PyYAML isn't available

try:
    import google.generativeai as genai  # type: ignore
except ImportError as e:  # pragma: no cover - clearer guidance when dependency missing
    raise ImportError(
        "google-generativeai package is required. Install it with: pip install google-generativeai"
    ) from e

# Configure Gemini API (prefer config.yml over environment)
CONFIG_PATH = Path(__file__).with_name("config.yml")

def _load_gemini_settings():
    """Load Gemini settings from config.yml if present.

    Returns a dict possibly containing: api_key, model, temperature, max_tokens.
    """
    settings = {}
    try:
        if yaml is not None and CONFIG_PATH.exists():
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = yaml.safe_load(f) or {}
            nl2sql = cfg.get("nl2sql") or {}
            gemini = nl2sql.get("gemini") or {}
            if isinstance(gemini, dict):
                settings["api_key"] = gemini.get("api_key") or gemini.get("apikey")
                settings["model"] = gemini.get("model")
                settings["temperature"] = gemini.get("temperature")
                settings["max_tokens"] = gemini.get("max_tokens") or gemini.get("max_output_tokens")
    except Exception:
        # Ignore config errors and fallback to environment
        pass
    return settings

_gem = _load_gemini_settings()
GEMINI_API_KEY = (
    _gem.get("api_key")
    or os.environ.get("GEMINI_API_KEY")
    or os.environ.get("GOOGLE_API_KEY")
)

if not GEMINI_API_KEY:
    raise ValueError(
        "Missing Gemini API key. Define nl2sql.gemini.api_key in config.yml or set GEMINI_API_KEY/GOOGLE_API_KEY."
    )

genai.configure(api_key=GEMINI_API_KEY)

# Model configuration: prefer config.yml, then env override, then sensible default
_model_name = _gem.get("model") or os.environ.get("SIMPLIQ_GEMINI_MODEL") or "gemini-1.5-pro"
_gen_config = {}
if _gem.get("temperature") is not None:
    _gen_config["temperature"] = _gem.get("temperature")
if _gem.get("max_tokens") is not None:
    try:
        _gen_config["max_output_tokens"] = int(_gem.get("max_tokens"))
    except Exception:
        pass

def _list_supported_models():
    """Return a dict of {model_name: model_obj} for models supporting generateContent."""
    try:
        models = genai.list_models()
        supported = {}
        for m in models:
            # Some SDK versions expose 'supported_generation_methods', others expose 'generation_methods'
            methods = getattr(m, "supported_generation_methods", None) or getattr(m, "generation_methods", [])
            if methods and ("generateContent" in methods or "generate_content" in methods):
                # m.name usually looks like 'models/gemini-1.5-pro' — normalize to short name for matching
                short_name = m.name.split("/")[-1]
                supported[short_name] = m
        return supported
    except Exception:
        return {}


def _choose_model(preferred: str | None) -> str:
    """Choose a model supported for generateContent, honoring a preferred name when possible.

    Fallback priority is tuned for wide availability.
    """
    supported = _list_supported_models()
    # If we can use preferred as-is, do it
    if preferred and preferred in supported:
        return preferred
    # Common aliases sometimes used in docs
    aliases = {
        "gemini-pro": ["gemini-1.5-pro", "gemini-1.5-pro-latest"],
        "gemini-1.5-pro": ["gemini-1.5-pro-latest", "gemini-pro"],
    }
    if preferred in aliases:
        for alt in aliases[preferred]:
            if alt in supported:
                return alt
    # General fallback order
    for candidate in [
        "gemini-1.5-pro",
        "gemini-1.5-pro-latest",
        "gemini-1.5-flash",
        "gemini-1.5-flash-8b",
        "gemini-pro",
    ]:
        if candidate in supported:
            return candidate
    # If SDK couldn't list models, keep preferred to let the API decide
    return preferred or "gemini-1.5-pro"


_selected_model_name = _choose_model(_model_name)
model = genai.GenerativeModel(_selected_model_name, generation_config=_gen_config or None)

# SimpliqData MCP Server URL
MCP_SERVER = "http://127.0.0.1:8000"


def call_mcp_tool(tool_name, arguments=None):
    """Call a SimpliqData MCP tool via JSON-RPC 2.0"""
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments or {}
        }
    }
    
    try:
        response = requests.post(MCP_SERVER, json=payload)
        response.raise_for_status()
        
        result = response.json()
        if "result" in result:
            content = result["result"]["content"][0]["text"]
            return json.loads(content)
        elif "error" in result:
            return {"error": result["error"]["message"]}
    except requests.exceptions.ConnectionError:
        return {"error": "Cannot connect to SimpliqData server. Is it running?"}
    except Exception as e:
        return {"error": str(e)}
    
    return None


def list_mcp_tools():
    """List available MCP tools"""
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list",
        "params": {}
    }
    
    try:
        response = requests.post(MCP_SERVER, json=payload)
        response.raise_for_status()
        result = response.json()
        return result["result"]["tools"]
    except Exception as e:
        print(f"Error listing tools: {e}")
        return []


def chat_with_gemini_and_mcp(user_message):
    """Chat with Gemini using MCP tools"""
    
    # First, get MCP tools
    tools = list_mcp_tools()
    tools_description = "\n".join([
        f"- {tool['name']}: {tool['description']}" 
        for tool in tools
    ])
    
    # Create context for Gemini
    context = f"""
You have access to a database management system called SimpliqData with these tools:

{tools_description}

When the user asks about database information, you can use these tools.
For example:
- To see database config: use get_config
- To check connection: use check_status
- To list tables/views: first use connect, then use list_objects
- To change connection: use update_config

User question: {user_message}

Provide a helpful answer based on the available tools.
"""
    
    # Get Gemini's response
    try:
        response = model.generate_content(context)
        return response.text
    except Exception as e:
        # Retry once with a best-effort fallback model if the error suggests unsupported model
        msg = str(e)
        if "404" in msg or "not found" in msg.lower() or "not supported" in msg.lower():
            fallback_name = _choose_model(None)
            if fallback_name and fallback_name != _selected_model_name:
                try:
                    fallback_model = genai.GenerativeModel(fallback_name, generation_config=_gen_config or None)
                    response = fallback_model.generate_content(context)
                    return response.text
                except Exception as e2:
                    return f"Error communicating with Gemini (fallback to {fallback_name} failed): {e2}"
        return f"Error communicating with Gemini: {e}"


def main():
    """Main function demonstrating SimpliqData + Gemini integration"""
    
    print("="*60)
    print("  SimpliqData MCP + Google Gemini Integration")
    print("="*60)
    print()
    
    # Check server connection
    print("🔍 Checking SimpliqData server...")
    try:
        response = requests.get(MCP_SERVER)
        server_info = response.json()
        print(f"✅ Connected to {server_info['name']} v{server_info['version']}")
    except:
        print("❌ Cannot connect to SimpliqData server!")
        print("   Make sure the server is running on http://127.0.0.1:8000")
        return
    
    print()
    print("="*60)
    print()
    
    # Example 1: List tools
    print("📋 Available MCP Tools:")
    print()
    tools = list_mcp_tools()
    for i, tool in enumerate(tools, 1):
        print(f"  {i}. {tool['name']}")
        print(f"     {tool['description']}")
        print()
    
    print("="*60)
    print()
    
    # Example 2: Get database config
    print("🔧 Database Configuration:")
    print()
    config = call_mcp_tool("get_config")
    if "error" not in config:
        print(f"  Connection String: {config['connection_string']}")
        print(f"  Database Type: {config['db_info']['database_type']}")
        print(f"  Database: {config['db_info']['database']}")
    else:
        print(f"  Error: {config['error']}")
    
    print()
    print("="*60)
    print()
    
    # Example 3: Check status
    print("📊 Connection Status:")
    print()
    status = call_mcp_tool("check_status")
    if "error" not in status:
        print(f"  Status: {status['status']}")
        print(f"  Message: {status['message']}")
    else:
        print(f"  Error: {status['error']}")
    
    print()
    print("="*60)
    print()
    
    # Example 4: Connect to database
    print("🔌 Connecting to database...")
    connect_result = call_mcp_tool("connect")
    if "error" not in connect_result:
        print(f"  ✅ {connect_result['message']}")
    else:
        print(f"  ❌ {connect_result['error']}")
    
    print()
    print("="*60)
    print()
    
    # Example 5: List database objects
    print("📚 Database Objects:")
    print()
    objects = call_mcp_tool("list_objects")
    if "error" not in objects:
        print(f"  Schemas: {', '.join(objects['schemas']) or 'None'}")
        print(f"  Tables: {', '.join(objects['tables']) or 'None'}")
        print(f"  Views: {', '.join(objects['views']) or 'None'}")
    else:
        print(f"  Error: {objects['error']}")
    
    print()
    print("="*60)
    print()
    
    # Example 6: Chat with Gemini
    print("💬 Gemini AI Integration:")
    print()
    question = "What database am I connected to and what objects does it contain?"
    print(f"  Question: {question}")
    print()
    answer = chat_with_gemini_and_mcp(question)
    print(f"  Gemini: {answer}")
    
    print()
    print("="*60)
    print()
    print("✨ Demo completed!")
    print()
    print("Try running this script interactively:")
    print("  python -i gemini_mcp_client.py")
    print()
    print("Then you can call:")
    print("  result = call_mcp_tool('get_config')")
    print("  answer = chat_with_gemini_and_mcp('your question')")
    print()


if __name__ == "__main__":
    main()
