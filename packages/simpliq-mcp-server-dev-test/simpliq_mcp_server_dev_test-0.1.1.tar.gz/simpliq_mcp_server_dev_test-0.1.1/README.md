# SimpliqData MCP Server

<!-- mcp-name: io.github.gersonfreire/simpliq-server -->

> **Database Management via Model Context Protocol (MCP)**

This POC demonstrates a **Model Context Protocol (MCP)** server for managing database connections using SQLAlchemy. The server implements the JSON-RPC 2.0 protocol for VS Code Copilot integration, reads database connection strings from a YAML configuration file, and provides tools to query and manage database connections.

## 📚 Documentation

- **[CARD.md](docs/CARD.md)** - Project overview card (visual summary) ⭐
- **[QUICKSTART.md](docs/QUICKSTART.md)** - Quick reference guide
- **[SERVER_CONFIGURATION.md](docs/SERVER_CONFIGURATION.md)** - Server configuration guide (host, port, SSL/HTTPS) ⭐ NEW!
- **[README_MULTI_USER.md](docs/README_MULTI_USER.md)** - Multi-user system complete guide ⭐ NEW!
- **[MULTI_USER_CLIENT_INTEGRATION.md](docs/MULTI_USER_CLIENT_INTEGRATION.md)** - Claude Desktop & VS Code integration ⭐ NEW!
- **[MCP_TOOLS_REFERENCE.md](docs/MCP_TOOLS_REFERENCE.md)** - MCP Tools quick reference ⭐ NEW!
- **[MIGRATION_GUIDE.md](docs/MIGRATION_GUIDE.md)** - Migration from single-user to multi-user ⭐ NEW!
- **[VALIDATION_GUIDE.md](docs/VALIDATION_GUIDE.md)** - Connection string validation guide
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System architecture and diagrams
- **[GEMINI_CLI_INTEGRATION.md](docs/GEMINI_CLI_INTEGRATION.md)** - Google Gemini AI setup
- **[SUMMARY.md](docs/SUMMARY.md)** - Project status and statistics
- **[INDEX.md](docs/INDEX.md)** - Complete file index and navigation
- **[CHANGELOG.md](docs/CHANGELOG.md)** - Version history
- **[CHANGELOG_SERVER_CONFIG.md](CHANGELOG_SERVER_CONFIG.md)** - Server configuration changelog ⭐ NEW!
- **[MULTI_USER_IMPLEMENTATION_PLAN.md](docs/MULTI_USER_IMPLEMENTATION_PLAN.md)** - Multi-user system implementation plan

## Key Features

- ✅ **JSON-RPC 2.0 Protocol** - Full MCP protocol implementation for VS Code Copilot
- ✅ **SQLAlchcreemy Integration** - Support for multiple database types (SQLite, PostgreSQL, MySQL, etc.)
- ✅ **YAML Configuration** - Database and server configuration via YAML
- ✅ **Configurable Server** - Host, port, debug mode configurable via YAML ⭐ NEW!
- ✅ **SSL/HTTPS Support** - Let's Encrypt/Certbot certificate support ⭐ NEW!
- ✅ **Multi-User System** - User authentication and isolated connections ⭐ NEW!
- ✅ **Configurable Authentication Modes** - Standard token validation (mcp) or header passthrough (client) ⭐ NEW!
- ✅ **16 MCP Tools** - User management, connection management, validation, and more
- ✅ **Connection String Validation** - Complete validation (format, network, connection)
- ✅ **REST Endpoints** - Alternative HTTP endpoints for testing and automation
- ✅ **Hot Reload** - Update configurations without code changes

## Files

- `mcp_server.py`: The main Flask server script with REST API endpoints and MCP tools.
- `config.yml`: YAML configuration file for the database connection string.

## Authentication Modes (mcp vs client)

The server now supports two authentication strategies configured via `authentication.type` in `config.yml`:

| Mode       | How Identity Is Resolved                                   | Order of Resolution                    | Use Case                                | Security                   |
| ---------- | ---------------------------------------------------------- | -------------------------------------- | --------------------------------------- | -------------------------- |
| `mcp`    | Validates JWT token with User Manager API                  | Bearer token → session file           | Production, normal multi-user           | Strong (token verified)    |
| `client` | Trusts headers (`X-Client-Username`, optional email/org) | Header → Bearer token → session file | Local dev, behind trusted reverse proxy | Weak (no token validation) |

Header passthrough (client mode) example:

```http
GET /config HTTP/1.1
Host: localhost:8000
X-Client-Username: dev_user
X-Client-Email: dev_user@example.com
X-Client-Org: demo-org
```

Add to `config.yml`:

```yaml
authentication:
  type: client   # or mcp
  require_auth_for_all: false
```

If `require_auth_for_all: true` is set, even discovery endpoints will require a resolved identity.

Português (resumo):
O modo `client` aceita identidade via cabeçalhos (X-Client-Username, X-Client-Email, X-Client-Org) sem validar token. Use somente em ambiente confiável (localhost, proxy autenticado). Para produção, mantenha `type: mcp`.

Startup logs show both the declared and effective mode; valores desconhecidos fazem fallback para `mcp`.

- `test_client.py`: Script to test all server endpoints.
- `test_validation.py`: Script to test connection string validation (interactive & suite). ⭐ NEW!
- `create_test_db.py`: Script to create a sample SQLite database for testing.
- `requirements.txt`: Python dependencies (Flask, SQLAlchemy, PyYAML).
- `example.db`: SQLite database file (created by `create_test_db.py`).
- `mcp_cli_client.py`: Interactive CLI client for SimpliqData MCP server.
- `gemini_mcp_client.py`: Google Gemini AI integration example.
- `docs/GEMINI_CLI_INTEGRATION.md`: Step-by-step guide for using with Google Gemini CLI.
- `docs/VALIDATION_GUIDE.md`: Complete guide for connection string validation. ⭐ NEW!
- `docs/TEST_README.md`: Testing guide for all test scripts. ⭐ NEW!
- `docs/QUICK_START_CONNECT_MONITOR.md`: Quick start for connect & monitor test. ⭐ NEW!

## Quick Start

### 1. Set up the environment

```powershell
# Navigate to the poc/db directory
cd C:\Users\gerso\source\repo\gerson\simpliq\pocs\db

# Create and activate virtual environment (if not already done at repo root)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Create the test database

```powershell
# This creates example.db with sample tables (users, products, orders)
python create_test_db.py
```

### 3. Run the MCP server

```powershell
# Start the Flask server on http://127.0.0.1:8000
python mcp_server.py
```

Tip: use an alternate config file

```powershell
# CLI flag (relative or absolute path)
python mcp_server.py --config .\config.dev.yml
python mcp_server.py -c C:\envs\simpliq\config.prod.yml

# Or via environment variable
$env:SIMPLIQ_CONFIG = ".\config.dev.yml"; python mcp_server.py
# (Also supported: SIMPLIQ_CONFIG_FILE)
```

The server prints the selected file at startup as:

>>> Using configuration file: C:\full\path\to\config.yml
>>>
>>

### 4. Test the server

#### Option A: Interactive CLI Client (Recommended)

The easiest way to interact with SimpliqData:

```powershell
# Activate the virtual environment
cd C:\Users\gerso\source\repo\gerson\simpliq\pocs\db
.\.venv\Scripts\Activate.ps1

# Run the interactive CLI client
python mcp_cli_client.py
```

This provides a user-friendly menu with all available tools.

#### Option B: REST API Test Client

For programmatic testing:

```powershell
# Run the test client
python test_client.py
```

#### Option C: Google Gemini CLI Integration

For AI-powered database interactions as a client, see **[GEMINI_CLI_INTEGRATION.md](docs/GEMINI_CLI_INTEGRATION.md)** for step-by-step instructions on using SimpliqData with Google Gemini CLI.

### NL→SQL Providers (mock, openai, anthropic, gemini)

You can choose which LLM provider the server uses to translate natural language into SQL.

- Via environment variables (highest priority):

  - `SIMPLIQ_NL2SQL_PROVIDER=gemini` (or `openai`, `anthropic`, `mock`)
  - For Gemini: set `GEMINI_API_KEY` (or `GOOGLE_API_KEY`)
    - Optional: `SIMPLIQ_GEMINI_MODEL` (default: `gemini-1.5-pro`)
    - Optional: `SIMPLIQ_GEMINI_BASE_URL` (default: `https://generativelanguage.googleapis.com`)
  - For OpenAI: `OPENAI_API_KEY`, optional `SIMPLIQ_OPENAI_MODEL`, `SIMPLIQ_OPENAI_BASE_URL`
  - For Anthropic: `ANTHROPIC_API_KEY`, optional `SIMPLIQ_ANTHROPIC_MODEL`, `SIMPLIQ_ANTHROPIC_BASE_URL`
- Via `config.yml` (lower priority than env):

```yaml
nl2sql:
  provider: gemini  # mock | openai | anthropic | gemini
  gemini:
    api_key: "AIza..."
    model: "gemini-1.5-pro"
    base_url: "https://generativelanguage.googleapis.com"
    temperature: 0.1
    max_tokens: 800
```

After setting the provider and keys, restart the server, then try:

```powershell
# Example natural language query via MCP tool
python mcp_cli_client.py
# Choose: natural_query → "liste todos os usuários"
```

## Available MCP Tools

O servidor agora disponibiliza um conjunto ampliado de ferramentas MCP (contagem dinâmica). Além das originais de conexão, foram adicionadas ferramentas multi-usuário, organizações, chaves de API, inspeção de esquema e execução de SQL (somente leitura). A contagem exata é calculada em tempo de execução.

Principais destaques novos:

- `execute_sql` / alias `run_query`: execução de consultas SELECT, com `timeout`, `limit` e `include_metadata`.
- Ferramentas de esquema: `describe_table`, `get_table_relationships`.
- Prompt MCP: `how_to_query` (guia rápido de uso).
- Paridade de listagem: discovery (GET /), initialize e tools/list retornam conjuntos sincronizados.

Ferramentas base (exemplo simplificado):

| Tool                        | Descrição (PT-BR)                               | Parâmetros principais                                         |
| --------------------------- | ------------------------------------------------- | -------------------------------------------------------------- |
| `get_config`              | Retorna configuração atual e info do banco      | —                                                             |
| `update_config`           | Atualiza a connection string                      | `connection_string` (obrigatório)                           |
| `check_status`            | Verifica status da conexão                       | —                                                             |
| `list_objects`            | Lista schemas, tabelas e views                    | —                                                             |
| `connect`                 | Conecta usando a config atual                     | —                                                             |
| `disconnect`              | Desconecta o engine                               | —                                                             |
| `execute_sql`             | Executa SELECT somente leitura                    | `sql` (obrig.), `timeout`, `limit`, `include_metadata` |
| `run_query`               | Alias de `execute_sql`                          | Mesmos parâmetros de `execute_sql`                          |
| `describe_table`          | Descreve colunas, PK, FKs, índices de uma tabela | `table_name` (obrig.), `schema` (opcional)                 |
| `get_table_relationships` | Lista relacionamentos (FKs)                       | `schema` (opcional)                                          |
| `user_login`              | Autentica usuário                                | `username`, `password`                                     |
| `whoami`                  | Retorna usuário autenticado                      | —                                                             |
| `list_users`              | Lista usuários                                   | —                                                             |
| `add_connection`          | Adiciona uma conexão para o usuário             | `name`, `connection_string` (obrig.)                       |
| `list_connections`        | Lista conexões do usuário                       | —                                                             |
| `get_active_connection`   | Retorna conexão ativa                            | —                                                             |
| `activate_connection`     | Ativa uma conexão específica                    | `connection_id` (obrig.)                                     |
| `create_api_key`          | Cria chave de API                                 | `name` (obrig.), `description`, `expires_in_days`        |
| `list_my_api_keys`        | Lista chaves do usuário                          | —                                                             |
| `revoke_api_key`          | Revoga chave de API                               | `key_id` (obrig.)                                            |

Observação: outras ferramentas de organização (create/update/delete/list) também estão disponíveis; consultar `tools/list` para a lista completa.

### Prompt MCP `how_to_query`

Disponível via:

```bash
curl -X POST http://127.0.0.1:8000/ -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":10,"method":"prompts/list","params":{}}'
curl -X POST http://127.0.0.1:8000/ -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":11,"method":"prompts/get","params":{"name":"how_to_query"}}'
```

Resumo do conteúdo do prompt (PT-BR): autenticar → configurar/`connect` → consultar com `run_query` ou `execute_sql`.

Exemplo JSON-RPC para consulta:

```bash
curl -X POST http://127.0.0.1:8000/ -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":20,"method":"tools/call","params":{"name":"run_query","arguments":{"sql":"SELECT * FROM users LIMIT 5"}}}'
```

Se receber erro de conexão ausente:

```bash
curl -X POST http://127.0.0.1:8000/ -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":21,"method":"tools/call","params":{"name":"update_config","arguments":{"connection_string":"sqlite:///example.db"}}}'
curl -X POST http://127.0.0.1:8000/ -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":22,"method":"tools/call","params":{"name":"connect","arguments":{}}}'
```

Depois repita a consulta.

### Example Usage

#### In CLI Client:

```powershell
python mcp_cli_client.py
# Then select from menu: 2 (Get Config), 4 (Connect), 5 (List Objects), etc.
```

#### In Google Gemini:

```powershell
python gemini_mcp_client.py "What database am I connected to?"
```

See **[GEMINI_CLI_INTEGRATION.md](docs/GEMINI_CLI_INTEGRATION.md)** for complete setup instructions.

#### In VS Code Copilot:

Once configured in `.vscode/mcp.json`, use the `/list` command to see available tools:

```
/list
# Shows: mcp_SimpliqData_get_config, mcp_SimpliqData_connect, etc.
```

**Note**: VS Code Copilot integration is functional for tool discovery, but @ symbol reference may not work in all cases. For reliable usage, use the CLI client or Gemini integration.

## API Endpoints

### MCP Protocol Endpoints

#### GET /

MCP server discovery endpoint. Returns server information and available tools.

**Response:**

```json
{
  "name": "Database MCP POC Server",
  "version": "1.0.0",
  "description": "A minimal MCP server for database connection management",
  "protocol": "mcp",
  "capabilities": {
    "tools": true,
    "prompts": false,
    "resources": false
  },
  "tools": [...]
}
```

#### POST /

MCP tool execution endpoint using **JSON-RPC 2.0 protocol**. This endpoint handles MCP protocol initialization, tool listing, and tool execution as required by VS Code Copilot.

**Supported JSON-RPC 2.0 Methods:**

##### 1. `initialize` - Protocol Handshake

**Request:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-06-18",
    "capabilities": {},
    "clientInfo": {
      "name": "Visual Studio Code",
      "version": "1.105.1"
    }
  }
}
```

**Response:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2025-06-18",
    "capabilities": {
      "tools": {},
      "prompts": {},
      "resources": {},
      "logging": {}
    },
    "serverInfo": {
      "name": "Database MCP POC Server",
      "version": "1.0.0"
    }
  }
}
```

##### 2. `tools/list` - List Available Tools

**Request:**

```bash
curl -X POST http://127.0.0.1:8000/ -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'
```

**Response:**

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "tools": [
      {
        "name": "get_config",
        "description": "Get current database configuration and connection information",
        "inputSchema": {"type": "object", "properties": {}}
      },
      ...
    ]
  }
}
```

##### Optional MCP Methods

The server also implements these optional MCP protocol methods for full compatibility:

**`prompts/list`** - Returns empty list (prompts feature not implemented)

```bash
curl -X POST http://127.0.0.1:8000/ -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":10,"method":"prompts/list","params":{}}'
# Response: {"jsonrpc":"2.0","id":10,"result":{"prompts":[]}}
```

**`resources/list`** - Returns empty list (resources feature not implemented)

```bash
curl -X POST http://127.0.0.1:8000/ -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":11,"method":"resources/list","params":{}}'
# Response: {"jsonrpc":"2.0","id":11,"result":{"resources":[]}}
```

**`logging/setLevel`** - Accepts logging requests (no-op implementation)

```bash
curl -X POST http://127.0.0.1:8000/ -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":12,"method":"logging/setLevel","params":{"level":"info"}}'
# Response: {"jsonrpc":"2.0","id":12,"result":{}}
```

**JSON-RPC Notifications** - Accepts notifications (id=null, no response required)

```bash
curl -X POST http://127.0.0.1:8000/ -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":null,"method":"notifications/initialized","params":{}}'
# Response: HTTP 204 No Content (successful notification received)
```

> **Note**: Notifications are JSON-RPC messages with `"id": null`. They don't require a response. Common notifications include `notifications/initialized`, `notifications/cancelled`, etc.

##### 3. `tools/call` - Execute a Tool

**Example - Get Config:**

```bash
curl -X POST http://127.0.0.1:8000/ -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"get_config","arguments":{}}}'
```

**Example - Connect to Database:**

```bash
curl -X POST http://127.0.0.1:8000/ -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"connect","arguments":{}}}'
```

**Example - List Database Objects:**

```bash
curl -X POST http://127.0.0.1:8000/ -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":5,"method":"tools/call","params":{"name":"list_objects","arguments":{}}}'
```

**Tool Call Response Format:**

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{\"connection_string\": \"sqlite:///example.db\", \"db_info\": {...}}"
      }
    ]
  }
}
```

#### GET /.well-known/mcp

MCP protocol information endpoint.

**Response:**

```json
{
  "mcpVersion": "1.0",
  "serverInfo": {
    "name": "Database MCP POC Server",
    "version": "1.0.0"
  },
  "capabilities": {
    "tools": true
  }
}
```

### Database Management Endpoints

#### GET /config

Retrieve the current database configuration and connection information.

**Response:**

```json
{
  "connection_string": "sqlite:///example.db",
  "db_info": {
    "database_type": "sqlite",
    "database": "example.db",
    "driver": null,
    "host": null,
    "port": null
  }
}
```

### POST /config

Update the database connection string.

**Request body:**

```json
{
  "connection_string": "sqlite:///new_database.db"
}
```

### GET /status

Check if the database is accessible and connected.

**Response:**

```json
{
  "status": "connected",
  "message": "Database is accessible"
}
```

### GET /objects

List all database objects (schemas, tables, views) visible to the connected user.

**Response:**

```json
{
  "schemas": [],
  "tables": ["users", "products", "orders"],
  "views": ["order_details"],
  "note": "User information is not available through SQLAlchemy inspection"
}
```

### POST /connect

Connect or reconnect to the database using the current configuration.

**Response:**

```json
{
  "message": "Successfully connected to the database."
}
```

### POST /disconnect

Close the current database connection.

**Response:**

```json
{
  "message": "Successfully disconnected from the database."
}
```

## Using with VS Code Copilot (Configure Tools)

### Detailed Steps to Add This MCP Server to VS Code Copilot

#### Step 1: Start the MCP Server

Ensure the server is running on `http://127.0.0.1:8000`:

```powershell
python mcp_server.py
```

#### Step 2: Open VS Code Copilot Chat

1. Open VS Code
2. Click on the **Chat icon** in the left sidebar (or press `Ctrl+Alt+I`)
3. The GitHub Copilot Chat panel will open

#### Step 3: Access the Attach Context Menu

1. In the Chat input field at the bottom, you'll see an **attachment icon** (📎 or a paperclip)
2. Click on the attachment icon
3. A menu will appear showing different context options

#### Step 4: Add Custom Tool

1. In the attach context menu, look for **"Tools"** or **"Add Tool"** option
2. Click on it to expand the tools section
3. You should see an option like **"Add Custom Tool"** or **"Configure Tools"**
4. Click on **"Configure Tools"**

#### Step 5: Configure the MCP Server

1. A configuration panel will appear
2. Enter the following information:

   - **Name**: `database-mcp-poc`
   - **Discovery URL** or **Base URL**: `http://127.0.0.1:8000`
   - **Description** (optional): `Database connection and query tool`
3. Click **Save** or **Add**

**Alternative: Manual Configuration**

You can also manually add the server to `.vscode/mcp.json`:

```json
{
  "servers": {
    "database-mcp-poc": {
      "url": "http://127.0.0.1:8000",
      "type": "http"
    }
  },
  "inputs": []
}
```

#### Step 6: Verify the Tool is Added

1. After saving, the tool should appear in your available tools list
2. You can now reference it in chat using `@database-mcp-poc` or similar (depending on how VS Code names it)

#### Step 7: Use the Tool in Chat

You can now ask Copilot questions like:

- "Using the database tool, what tables are available?"
- "Check the database connection status"
- "Show me the database configuration"

### Alternative Method: Using the Settings UI

If the chat interface doesn't show the tools option:

1. Open VS Code Settings (`Ctrl+,`)
2. Search for **"Copilot Tools"** or **"GitHub Copilot Tools"**
3. Look for an option to add custom tools or MCP servers
4. Add the discovery URL: `http://127.0.0.1:8000/config`

### Troubleshooting

**If you can't find the "Configure Tools" option:**

- Make sure you have the latest version of the GitHub Copilot extension
- The feature might be called differently: try looking for "Agents", "Tools", "Extensions", or "Add-ons"
- Check if your Copilot subscription includes access to tools/MCP features

**If the tool doesn't connect:**

- Verify the server is running: open `http://127.0.0.1:8000` in your browser (should return JSON server info)
- Check that no firewall is blocking localhost connections
- Review the server terminal output for any error messages
- Look for JSON-RPC requests in the server console (should show `"jsonrpc": "2.0"` messages)

**If you see HTTP 400 or 405 errors:**

- The server now uses **JSON-RPC 2.0 protocol** (updated implementation)
- Restart the server to ensure the latest code is running
- Verify the URL in `.vscode/mcp.json` is exactly `http://127.0.0.1:8000` (no `/config` or other paths)
- Check the server console for debug logs showing the received POST data

**Protocol Information:**

The server implements the Model Context Protocol (MCP) using JSON-RPC 2.0:

- **Protocol version**: `2025-06-18`
- **Core methods**: `initialize`, `tools/list`, `tools/call`
- **Optional methods**: `prompts/list`, `resources/list`, `logging/setLevel` (implemented but return empty/no-op)
- **Notifications**: All JSON-RPC notifications (id=null) are accepted and return HTTP 204
- **Response format**: All tool results are wrapped in `{"content": [{"type": "text", "text": "..."}]}`
- **Error codes**: Standard JSON-RPC 2.0 error codes (-32600 to -32603)

## Testing the Server

### Testing JSON-RPC 2.0 Protocol (MCP)

Test the MCP protocol that VS Code Copilot uses:

```powershell
# 1. Initialize handshake
$body = '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18"}}'
curl -X POST http://127.0.0.1:8000/ -H "Content-Type: application/json" -d $body

# 2. List available tools
$body = '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'
curl -X POST http://127.0.0.1:8000/ -H "Content-Type: application/json" -d $body

# 3. Call get_config tool
$body = '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"get_config","arguments":{}}}'
curl -X POST http://127.0.0.1:8000/ -H "Content-Type: application/json" -d $body

# 4. Connect to database
$body = '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"connect","arguments":{}}}'
curl -X POST http://127.0.0.1:8000/ -H "Content-Type: application/json" -d $body

# 5. List database objects
$body = '{"jsonrpc":"2.0","id":5,"method":"tools/call","params":{"name":"list_objects","arguments":{}}}'
curl -X POST http://127.0.0.1:8000/ -H "Content-Type: application/json" -d $body
```

### Testing REST Endpoints (Legacy)

You can also test the REST endpoints directly:

```powershell
# Get configuration
curl http://127.0.0.1:8000/config

# Check status
curl http://127.0.0.1:8000/status

# Connect to database
curl -X POST http://127.0.0.1:8000/connect

# List database objects
curl http://127.0.0.1:8000/objects

# Update configuration
curl -X POST http://127.0.0.1:8000/config -H "Content-Type: application/json" -d '{\"connection_string\":\"sqlite:///test.db\"}'

# Disconnect
curl -X POST http://127.0.0.1:8000/disconnect
```

## Sample Database Structure

The `create_test_db.py` script creates the following structure:

**Tables:**

- `users`: id, username, email, created_at
- `products`: id, name, description, price, stock
- `orders`: id, user_id, product_id, quantity, order_date

**Views:**

- `order_details`: Joins orders with users and products information

## Technical Details

### Protocol Implementation

This server implements the **Model Context Protocol (MCP)** specification:

- **Transport**: HTTP with JSON-RPC 2.0
- **Protocol Version**: `2025-06-18`
- **Capabilities**: Tools (prompts and resources not implemented in this POC)
- **Content Types**: Text responses with JSON-formatted data

### Architecture

```
┌─────────────────┐      JSON-RPC 2.0        ┌──────────────────┐
│  VS Code        │ ◄──────────────────────► │  Flask Server    │
│  Copilot        │   initialize, tools/*    │  (mcp_server.py)  │
└─────────────────┘                          └──────────────────┘
                                                      │
                                                      ▼
                                             ┌──────────────────┐
                                             │  SQLAlchemy      │
                                             │  (DB Abstraction)│
                                             └──────────────────┘
                                                      │
                                                      ▼
                                             ┌──────────────────┐
                                             │  SQLite/         │
                                             │  PostgreSQL/etc  │
                                             └──────────────────┘
```

## Notes

### Database Support

- **SQLite**: Used by default for simplicity and portability (no installation required)
- **PostgreSQL**: Update `config.yml` with `postgresql://user:password@localhost:5432/dbname`
- **MySQL**: Update `config.yml` with `mysql+pymysql://user:password@localhost:3306/dbname`
- **Others**: Any SQLAlchemy-supported database (Oracle, SQL Server, etc.)

**Installing drivers for other databases:**

```powershell
# PostgreSQL
pip install psycopg2-binary

# MySQL
pip install pymysql

# SQL Server
pip install pyodbc
```

### Development vs Production

**Current setup (Development):**

- Flask development server (single-threaded, not secure)
- Debug logging enabled
- No authentication/authorization
- HTTP only (no HTTPS)

**For production use, implement:**

- WSGI server (Gunicorn, uWSGI, or Waitress)
- Authentication and authorization (API keys, OAuth)
- HTTPS/TLS encryption
- Rate limiting and request validation
- Proper error logging and monitoring
- Connection pooling for databases
- Environment-based configuration

---

✅ Servidor MCP Corrigido - Suporte POST Implementado!
🔧 Problema Resolvido:
O erro 405 Method Not Allowed no POST / foi corrigido. O servidor agora suporta:

GET / - Descoberta do servidor (lista de ferramentas)
POST / - Execução de ferramentas MCP
✨ Mudanças Implementadas:
Endpoint raiz atualizado - Agora aceita GET e POST

Roteamento de ferramentas - POST processa as seguintes ferramentas:

get_config - Retorna configuração do banco
update_config - Atualiza connection string
check_status - Verifica status da conexão
list_objects - Lista tabelas, views e schemas
connect - Conecta ao banco
disconnect - Desconecta do banco
Formato de requisição MCP:

{  "method": "tool_name",  "params": { }}
🧪 Testes Realizados:
✅ POST / {"method":"get_config"} → Retornou configuração
✅ POST / {"method":"check_status"} → Status: disconnected
✅ POST / {"method":"connect"} → Conectado com sucesso
✅ POST / {"method":"list_objects"} → Listou tabelas: users, products, orders, view: order_details

🚀 Próximos Passos:
Recarregue o VS Code - Pressione Ctrl+Shift+P → "Reload Window"
Teste no Copilot Chat:
"@database-mcp-poc get config"
"@database-mcp-poc list tables"
"Using the database tool, show me what's in the database"
O servidor agora está 100% compatível com o protocolo MCP e pronto para uso no VS Code Copilot! 🎉

---

Uso no chat Copilot VsCode

Vou verificar o status da conexão e também obter a configuração:

Ran `check_status`
Completed with input: {}

Ran `get_config`
Completed with input: {}

Perfeito! 🎉 **As ferramentas MCP do SimpliqData estão funcionando no Claude Desktop!**

## Status Atual

### Conexão ao Banco

- **Status**: ⚠️ Desconectado
- **Mensagem**: "Not connected to any database"

### Configuração do Banco

- **Connection String**: `sqlite:///example.db`
- **Tipo de Banco**: SQLite
- **Database**: example.db
- **Host**: N/A (arquivo local)
- **Driver**: Padrão SQLite

## Próximos Passos

Quer que eu:

1. **Conecte ao banco de dados**? Use: `#mcp_simpliqdata_connect`
2. **Liste os objetos do banco**? (após conectar)
3. **Atualize a configuração**? Para outro banco de dados

**Exemplo para conectar**:

```
#mcp_simpliqdata_connect
```

Depois de conectar, posso listar todas as tabelas e views disponíveis! 😊

---
