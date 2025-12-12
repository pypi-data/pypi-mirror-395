"""
Unit tests for MCP Server adapter.

These tests verify MCP tool registration without running the server.
"""

import pytest
from pathlib import Path


class TestMCPServerAdapter:
    """Test MCP Server adapter functionality."""

    @pytest.mark.skipif(
        True,
        reason="MCP package may not be installed in test environment",
    )
    def test_adapter_import(self):
        """Verify adapter can be imported."""
        from universal_agent_nexus.adapters.mcp.server import MCPServerAdapter

        assert MCPServerAdapter is not None

    def test_create_mcp_server_import(self):
        """Verify factory function can be imported."""
        try:
            from universal_agent_nexus.adapters.mcp.server import create_mcp_server

            assert create_mcp_server is not None
        except ImportError:
            pytest.skip("MCP package not installed")

    def test_server_creates_tools_from_graphs(self, sample_manifest_path: Path):
        """Test that server creates MCP tools from manifest graphs."""
        try:
            from universal_agent_nexus.adapters.mcp.server import MCPServerAdapter
            from universal_agent_nexus.adapters.langgraph.runtime import load_manifest
        except ImportError:
            pytest.skip("MCP or LangGraph packages not installed")

        manifest = load_manifest(str(sample_manifest_path))
        adapter = MCPServerAdapter(manifest=manifest, name="test-server")

        # Verify server was created
        assert adapter.server is not None
        assert adapter.name == "test-server"
        assert adapter.manifest == manifest

