"""
MCP Server for hello-langgraph example.

Usage:
    python run_mcp_server.py

Then configure in Claude Desktop (Windows):
    %APPDATA%\\Claude\\claude_desktop_config.json

    {
      "mcpServers": {
        "uaa-hello": {
          "command": "python",
          "args": ["C:\\\\universal_agent_nexus\\\\examples\\\\hello_mcp\\\\run_mcp_server.py"],
          "env": {
            "OPENAI_API_KEY": "sk-..."
          }
        }
      }
    }

Or test with MCP Inspector:
    npx @modelcontextprotocol/inspector python examples/hello_mcp/run_mcp_server.py
"""

import asyncio
import logging
import sys
from pathlib import Path

# Windows async fix for psycopg
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

logging.basicConfig(level=logging.INFO)


async def main():
    from universal_agent_nexus.adapters.mcp.server import run_mcp_server

    # Path to manifest (relative to this file)
    manifest_path = Path(__file__).parent.parent / "hello_langgraph" / "manifest.yaml"

    # Run MCP server with optional Postgres checkpointing
    # Set postgres_url=None for stateless execution
    await run_mcp_server(
        manifest_path=str(manifest_path),
        postgres_url=None,  # Set to Postgres URL for checkpointing
        name="uaa-hello-server",
    )


if __name__ == "__main__":
    asyncio.run(main())

