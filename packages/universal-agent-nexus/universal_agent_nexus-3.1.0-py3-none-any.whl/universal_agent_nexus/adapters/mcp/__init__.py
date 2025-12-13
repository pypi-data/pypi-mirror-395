"""MCP Server adapter for Universal Agent Architecture."""

try:
    from .server import MCPServerAdapter, create_mcp_server, run_mcp_server

    __all__ = ["MCPServerAdapter", "create_mcp_server", "run_mcp_server"]
except ImportError:
    # MCP deps not installed
    __all__ = []
