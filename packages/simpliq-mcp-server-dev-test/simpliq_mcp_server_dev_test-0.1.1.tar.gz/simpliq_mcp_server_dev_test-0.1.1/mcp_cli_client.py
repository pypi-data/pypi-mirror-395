#!/usr/bin/env python3
"""
SimpliqData MCP CLI Client
==========================

Simple command-line client to interact with SimpliqData MCP server.
No external dependencies beyond requests.

Requirements:
    pip install requests

Usage:
    python mcp_cli_client.py
"""

import json
import requests
import sys

# SimpliqData MCP Server URL
MCP_SERVER = "http://127.0.0.1:8000"


def json_rpc_call(method, params=None):
    """Make a JSON-RPC 2.0 call to the MCP server"""
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params or {}
    }
    
    try:
        response = requests.post(MCP_SERVER, json=payload, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"error": {"message": "Cannot connect to server. Is it running?"}}
    except requests.exceptions.Timeout:
        return {"error": {"message": "Request timed out"}}
    except Exception as e:
        return {"error": {"message": str(e)}}


def call_tool(tool_name, arguments=None):
    """Call an MCP tool"""
    result = json_rpc_call("tools/call", {
        "name": tool_name,
        "arguments": arguments or {}
    })
    
    if "error" in result:
        return {"error": result["error"]["message"]}
    
    if "result" in result and "content" in result["result"]:
        content_text = result["result"]["content"][0]["text"]
        return json.loads(content_text)
    
    return result


def list_tools():
    """List available MCP tools"""
    result = json_rpc_call("tools/list")
    
    if "error" in result:
        print(f"Error: {result['error']['message']}")
        return []
    
    return result.get("result", {}).get("tools", [])


def print_separator():
    """Print a line separator"""
    print("-" * 70)


def main_menu():
    """Display main menu"""
    print("\n" + "="*70)
    print("  SimpliqData MCP CLI Client")
    print("="*70)
    print("\nCommands:")
    print("  1. List Tools         - Show available MCP tools")
    print("  2. Get Config         - Show database configuration")
    print("  3. Check Status       - Check connection status")
    print("  4. Connect            - Connect to database")
    print("  5. List Objects       - List database tables/views")
    print("  6. Update Config      - Update connection string")
    print("  7. Disconnect         - Disconnect from database")
    print("  8. Custom Tool Call   - Call any tool with custom arguments")
    print("  9. Server Info        - Show MCP server information")
    print("  0. Exit")
    print("="*70)


def show_server_info():
    """Show MCP server information"""
    result = json_rpc_call("initialize", {
        "protocolVersion": "2025-06-18",
        "capabilities": {},
        "clientInfo": {
            "name": "SimpliqData CLI Client",
            "version": "1.0.0"
        }
    })
    
    if "result" in result:
        server_info = result["result"]["serverInfo"]
        print(f"\n📡 Server Name: {server_info['name']}")
        print(f"📌 Version: {server_info['version']}")
        print(f"📝 Description: {server_info.get('description', 'N/A')}")
        print(f"🔗 Protocol Version: {result['result']['protocolVersion']}")


def list_tools_command():
    """List all available tools"""
    tools = list_tools()
    
    if not tools:
        print("\n❌ No tools available or server error")
        return
    
    print(f"\n📋 Available Tools ({len(tools)}):\n")
    for i, tool in enumerate(tools, 1):
        print(f"{i}. {tool['name']}")
        print(f"   {tool['description']}")
        
        if 'inputSchema' in tool and 'properties' in tool['inputSchema']:
            props = tool['inputSchema']['properties']
            if props:
                print(f"   Parameters: {', '.join(props.keys())}")
        print()


def get_config_command():
    """Get database configuration"""
    result = call_tool("get_config")
    
    if "error" in result:
        print(f"\n❌ Error: {result['error']}")
        return
    
    print(f"\n🔧 Database Configuration:")
    print(f"   Connection String: {result['connection_string']}")
    print(f"   Database Type: {result['db_info']['database_type']}")
    print(f"   Database: {result['db_info']['database']}")
    
    if result['db_info']['host']:
        print(f"   Host: {result['db_info']['host']}")
    if result['db_info']['port']:
        print(f"   Port: {result['db_info']['port']}")


def check_status_command():
    """Check connection status"""
    result = call_tool("check_status")
    
    if "error" in result:
        print(f"\n❌ Error: {result['error']}")
        return
    
    status_icon = "✅" if result['status'] == "connected" else "⚠️"
    print(f"\n{status_icon} Status: {result['status']}")
    print(f"   {result['message']}")


def connect_command():
    """Connect to database"""
    result = call_tool("connect")
    
    if "error" in result:
        print(f"\n❌ Error: {result['error']}")
        return
    
    print(f"\n✅ {result['message']}")
    print(f"   Database: {result['database']}")


def list_objects_command():
    """List database objects"""
    result = call_tool("list_objects")
    
    if "error" in result:
        print(f"\n❌ Error: {result['error']}")
        return
    
    print(f"\n📚 Database Objects:")
    
    if result['schemas']:
        print(f"   Schemas: {', '.join(result['schemas'])}")
    else:
        print(f"   Schemas: None")
    
    if result['tables']:
        print(f"   Tables ({len(result['tables'])}): {', '.join(result['tables'])}")
    else:
        print(f"   Tables: None")
    
    if result['views']:
        print(f"   Views ({len(result['views'])}): {', '.join(result['views'])}")
    else:
        print(f"   Views: None")


def update_config_command():
    """Update database configuration"""
    print("\nCurrent connection string examples:")
    print("  SQLite: sqlite:///example.db")
    print("  PostgreSQL: postgresql://user:pass@localhost:5432/dbname")
    print("  MySQL: mysql://user:pass@localhost:3306/dbname")
    print()
    
    new_connection = input("Enter new connection string (or 'cancel'): ").strip()
    
    if new_connection.lower() == 'cancel':
        print("Cancelled.")
        return
    
    result = call_tool("update_config", {"connection_string": new_connection})
    
    if "error" in result:
        print(f"\n❌ Error: {result['error']}")
        return
    
    print(f"\n✅ {result['message']}")
    print(f"   Old: {result['old_connection']}")
    print(f"   New: {result['new_connection']}")


def disconnect_command():
    """Disconnect from database"""
    result = call_tool("disconnect")
    
    if "error" in result:
        print(f"\n❌ Error: {result['error']}")
        return
    
    print(f"\n✅ {result['message']}")


def custom_tool_call():
    """Call a custom tool with user-provided arguments"""
    tools = list_tools()
    
    if not tools:
        print("\n❌ No tools available")
        return
    
    print("\nAvailable tools:")
    for i, tool in enumerate(tools, 1):
        print(f"  {i}. {tool['name']}")
    
    choice = input("\nEnter tool number (or 'cancel'): ").strip()
    
    if choice.lower() == 'cancel':
        print("Cancelled.")
        return
    
    try:
        tool_idx = int(choice) - 1
        if tool_idx < 0 or tool_idx >= len(tools):
            print("Invalid choice.")
            return
    except ValueError:
        print("Invalid input.")
        return
    
    tool = tools[tool_idx]
    tool_name = tool['name']
    
    print(f"\nCalling tool: {tool_name}")
    
    # Check if tool has parameters
    if 'inputSchema' in tool and 'properties' in tool['inputSchema']:
        props = tool['inputSchema']['properties']
        if props:
            print("Parameters:")
            for param_name, param_info in props.items():
                print(f"  - {param_name}: {param_info.get('description', 'N/A')}")
            
            print("\nEnter arguments as JSON (e.g., {\"key\": \"value\"}) or press Enter for no args:")
            args_input = input().strip()
            
            if args_input:
                try:
                    arguments = json.loads(args_input)
                except json.JSONDecodeError:
                    print("Invalid JSON. Calling without arguments.")
                    arguments = {}
            else:
                arguments = {}
        else:
            arguments = {}
    else:
        arguments = {}
    
    result = call_tool(tool_name, arguments)
    
    print("\nResult:")
    print(json.dumps(result, indent=2))


def main():
    """Main CLI loop"""
    # Check server connection on startup
    try:
        response = requests.get(MCP_SERVER, timeout=2)
        if response.status_code != 200:
            print(f"⚠️  Warning: Server returned status {response.status_code}")
    except:
        print("❌ Cannot connect to SimpliqData server!")
        print(f"   Make sure it's running on {MCP_SERVER}")
        sys.exit(1)
    
    commands = {
        '1': ('List Tools', list_tools_command),
        '2': ('Get Config', get_config_command),
        '3': ('Check Status', check_status_command),
        '4': ('Connect', connect_command),
        '5': ('List Objects', list_objects_command),
        '6': ('Update Config', update_config_command),
        '7': ('Disconnect', disconnect_command),
        '8': ('Custom Tool Call', custom_tool_call),
        '9': ('Server Info', show_server_info),
        '0': ('Exit', None)
    }
    
    while True:
        main_menu()
        choice = input("\nEnter command number: ").strip()
        
        if choice == '0':
            print("\n👋 Goodbye!")
            break
        
        if choice in commands:
            cmd_name, cmd_func = commands[choice]
            if cmd_func:
                print_separator()
                try:
                    cmd_func()
                except KeyboardInterrupt:
                    print("\n\n⚠️  Interrupted")
                except Exception as e:
                    print(f"\n❌ Error: {e}")
                print_separator()
                input("\nPress Enter to continue...")
        else:
            print("\n❌ Invalid choice. Try again.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
