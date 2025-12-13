"""
MCP Server adapter for Universal Agent Architecture.

Exposes UAA graphs as MCP tools using FastMCP with stdio transport.

December 2025 Best Practices:
- FastMCP for automatic tool generation from type hints
- stdio transport for Claude Desktop, Cursor, VS Code
- Async execution with proper error handling
- Auto-discovery of graphs from manifest
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from mcp.server import Server
    from mcp.types import TextContent, Tool
except ImportError as exc:
    raise ImportError(
        "Install 'universal-agent-nexus[mcp]' to use MCP server adapter"
    ) from exc

from universal_agent.manifests.schema import AgentManifest

logger = logging.getLogger(__name__)


class MCPServerAdapter:
    """
    Expose UAA graphs as MCP tools.

    Each graph becomes a callable MCP tool that AI clients can invoke.

    Features:
    - Auto-discovery of graphs from manifest
    - Type-safe tool definitions
    - Async execution with LangGraph runtime
    - Error handling and logging
    """

    def __init__(
        self,
        manifest: AgentManifest,
        postgres_url: Optional[str] = None,
        name: str = "uaa-mcp-server",
    ):
        self.manifest = manifest
        self.postgres_url = postgres_url
        self.name = name

        # Create MCP server
        self.server = Server(name)

        # Register handlers
        self._setup_handlers()

    def _setup_handlers(self) -> None:
        """Setup MCP tool handlers."""

        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            """List available UAA graph tools."""
            tools = []
            for graph in self.manifest.graphs:
                tools.append(
                    Tool(
                        name=f"graph_{graph.name}",
                        description=graph.description
                        or f"Execute the {graph.name} UAA graph",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "execution_id": {
                                    "type": "string",
                                    "description": "Unique execution identifier",
                                },
                                "query": {
                                    "type": "string",
                                    "description": "Input query or message for the graph",
                                },
                                "context": {
                                    "type": "object",
                                    "description": "Additional context data",
                                    "default": {},
                                },
                            },
                            "required": ["execution_id", "query"],
                        },
                    )
                )
            return tools

        @self.server.call_tool()
        async def call_tool(
            name: str, arguments: Dict[str, Any]
        ) -> List[TextContent]:
            """Execute a UAA graph tool."""
            # Parse tool name to get graph name
            if not name.startswith("graph_"):
                return [
                    TextContent(
                        type="text",
                        text=f"Unknown tool: {name}. Expected format: graph_<name>",
                    )
                ]

            graph_name = name[6:]  # Remove "graph_" prefix

            # Validate graph exists
            graph = next(
                (g for g in self.manifest.graphs if g.name == graph_name), None
            )
            if not graph:
                return [
                    TextContent(
                        type="text",
                        text=f"Graph '{graph_name}' not found in manifest",
                    )
                ]

            # Extract arguments
            execution_id = arguments.get("execution_id", "mcp-execution")
            query = arguments.get("query", "")
            context = arguments.get("context", {})

            try:
                result = await self._execute_graph(
                    graph_name=graph_name,
                    execution_id=execution_id,
                    query=query,
                    context=context,
                )
                return [TextContent(type="text", text=result)]

            except Exception as e:
                logger.exception("Error executing graph %s: %s", graph_name, e)
                return [
                    TextContent(
                        type="text",
                        text=f"Error executing graph '{graph_name}': {str(e)}",
                    )
                ]

    async def _execute_graph(
        self,
        graph_name: str,
        execution_id: str,
        query: str,
        context: Dict[str, Any],
    ) -> str:
        """Execute a UAA graph via LangGraph runtime."""
        logger.info(
            "Executing graph '%s' via MCP (exec_id=%s)", graph_name, execution_id
        )

        # Import here to avoid circular deps and allow graceful degradation
        try:
            from universal_agent_nexus.adapters.langgraph.runtime import (
                LangGraphRuntime,
            )
        except ImportError as e:
            return f"LangGraph adapter not available: {e}"

        # Initialize runtime
        runtime = LangGraphRuntime(
            postgres_url=self.postgres_url,
            enable_checkpointing=self.postgres_url is not None,
        )

        try:
            await runtime.initialize(self.manifest, graph_name=graph_name)

            # Execute
            input_data = {
                "context": {"query": query, **context},
                "history": [],
                "current_node": "",
                "error": None,
            }

            result = await runtime.execute(execution_id, input_data)

            # Extract response
            last_response = result.get("context", {}).get("last_response", "")
            error = result.get("error")

            if error:
                return f"Graph completed with error: {error}"

            return last_response or "Graph executed successfully (no response content)"

        finally:
            await runtime.close()

    async def run_stdio(self) -> None:
        """Run MCP server with stdio transport."""
        from mcp.server.stdio import stdio_server

        logger.info("Starting MCP server: %s (stdio transport)", self.name)

        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options(),
            )


def create_mcp_server(
    manifest_path: str,
    postgres_url: Optional[str] = None,
    name: str = "uaa-mcp-server",
) -> MCPServerAdapter:
    """
    Factory function to create MCP server from manifest.

    Usage:
        server = create_mcp_server("manifest.yaml")
        asyncio.run(server.run_stdio())
    """
    from universal_agent_nexus.adapters.langgraph.runtime import load_manifest

    manifest = load_manifest(manifest_path)

    return MCPServerAdapter(
        manifest=manifest,
        postgres_url=postgres_url,
        name=name,
    )


async def run_mcp_server(
    manifest_path: str,
    postgres_url: Optional[str] = None,
    name: str = "uaa-mcp-server",
) -> None:
    """
    Convenience function to create and run MCP server.

    Usage:
        asyncio.run(run_mcp_server("manifest.yaml"))
    """
    server = create_mcp_server(manifest_path, postgres_url, name)
    await server.run_stdio()
