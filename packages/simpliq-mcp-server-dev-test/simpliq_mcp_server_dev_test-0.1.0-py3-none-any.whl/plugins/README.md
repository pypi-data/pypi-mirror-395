# SimpliQ MCP Server - Plugins

This directory contains the plugin system for SimpliQ MCP Server.

## Directory Structure

```
plugins/
├── __init__.py           # Package initialization, exports IMCPPlugin and MCPPluginRegistry
├── base.py              # IMCPPlugin protocol definition
├── registry.py          # MCPPluginRegistry implementation
├── README.md            # This file
└── [plugin_name].py     # Individual plugin implementations (e.g., protheus_mapper.py)
```

## Quick Start

### Creating a Plugin

1. Create a new Python file in this directory (e.g., `my_plugin.py`)
2. Implement the `IMCPPlugin` protocol:

```python
class MyPlugin:
    def initialize(self, connection, semantic_catalog):
        """Called when plugin is initialized with DB connection."""
        self.connection = connection
        self.catalog = semantic_catalog

    def get_tools(self):
        """Return tools provided by this plugin."""
        return {
            "my_tool": {
                "description": "What this tool does",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "param": {"type": "string"}
                    },
                    "required": ["param"]
                }
            }
        }

    def handle_tool_call(self, tool_name, args):
        """Execute tool and return result."""
        if tool_name == "my_tool":
            return {
                "content": [
                    {"type": "text", "text": f"Result: {args['param']}"}
                ]
            }
        return None
```

3. Register in [mcp_server.py](../mcp_server.py):

```python
try:
    from plugins.my_plugin import MyPlugin
    plugin_registry.register_plugin('my_plugin', MyPlugin())
except ImportError:
    pass
```

## Core Components

### IMCPPlugin Protocol ([base.py](base.py))

Defines the interface all plugins must implement:
- `initialize(connection, semantic_catalog)` - Setup with DB and catalog
- `get_tools()` - Return tool definitions
- `handle_tool_call(tool_name, args)` - Execute tools

### MCPPluginRegistry ([registry.py](registry.py))

Manages plugin lifecycle:
- `register_plugin(name, plugin)` - Register a plugin
- `initialize_all(connection, catalog)` - Initialize all plugins
- `get_all_tools()` - Get all tools from all plugins
- `handle_tool_call(tool_name, args)` - Route tool calls to plugins

## Documentation

See [docs/plugins/PLUGIN_SYSTEM.md](../../docs/plugins/PLUGIN_SYSTEM.md) for complete documentation including:
- Architecture overview
- Plugin creation guide
- Best practices
- API reference
- Troubleshooting

## Available Plugins

| Plugin | Description | Status |
|--------|-------------|--------|
| (none yet) | - | - |

### Planned Plugins

- **protheus_mapper**: Semi-automatic semantic mapping for Protheus TOTVS ERP (Phases 2-6)

## Testing

Unit tests are located in [tests/plugins/](../../.git/logs/refs/heads/plugins).

Run tests:
```bash
cd simpliq_server
python -m pytest tests/plugins/ -v
```

## Plugin Philosophy

SimpliQ is designed to be **generic and reusable** across any database system. Plugins allow you to add ERP-specific or domain-specific functionality without:
- Modifying core server code
- Breaking compatibility with other systems
- Requiring plugins to be present

**Key principle**: The server should work perfectly without any plugins loaded.

## License

Same as SimpliQ MCP Server.

---

**Author**: Gerson Amorim (Anthropic)
**Date**: 2025-11-18
