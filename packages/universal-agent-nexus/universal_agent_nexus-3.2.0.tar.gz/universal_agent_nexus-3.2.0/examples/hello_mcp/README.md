# MCP Server Example

Expose UAA graphs as MCP tools callable from Claude Desktop, Cursor, VS Code, etc.

## Quick Start

1. **Install dependencies:**

```bash
pip install -e ".[mcp,langgraph]"
```

2. **Set OpenAI API key:**

```bash
export OPENAI_API_KEY="sk-..."
```

3. **Test with MCP Inspector:**

```bash
npx @modelcontextprotocol/inspector python examples/hello_mcp/run_mcp_server.py
```

Opens web UI at http://localhost:5173 where you can test tool invocation.

## Configure Claude Desktop

Add to `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "uaa-hello": {
      "command": "python",
      "args": ["C:\\universal_agent_nexus\\examples\\hello_mcp\\run_mcp_server.py"],
      "env": {
        "OPENAI_API_KEY": "sk-..."
      }
    }
  }
}
```

Then restart Claude Desktop and look for the `graph_main` tool.

## Usage in Claude

Ask Claude:
- "Use the graph_main tool with execution_id='test-1' and query='Hello!'"
- Claude will call your UAA graph and return the response.

## Available Tools

The MCP server auto-discovers graphs from the manifest:

| Tool Name | Description |
|-----------|-------------|
| `graph_main` | Execute the main greeting graph |

## Architecture

```
UAA Manifest → MCP Server → stdio → Claude Desktop
     ↓              ↓
  graphs      MCP tools
  [main]      [graph_main]
```

