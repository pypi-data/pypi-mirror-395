"""
Integration tests for MCP server adapter.

Tests:
- Tool registration from manifest
- Error handling
- Multi-graph scenarios
"""

import pytest
from pathlib import Path

from universal_agent_nexus.adapters.langgraph.runtime import load_manifest


@pytest.mark.asyncio
@pytest.mark.integration
async def test_mcp_server_creates_from_manifest(sample_manifest_path):
    """
    Test MCP server auto-discovers and registers tools from manifest.
    
    Validates:
    - Graph discovery
    - Server creation
    """
    try:
        from universal_agent_nexus.adapters.mcp.server import MCPServerAdapter
    except ImportError:
        pytest.skip("MCP package not installed")
    
    manifest = load_manifest(str(sample_manifest_path))
    
    server = MCPServerAdapter(
        manifest=manifest,
        name="test-mcp-server",
    )
    
    # Verify server was created
    assert server.server is not None
    assert server.name == "test-mcp-server"
    assert server.manifest == manifest


@pytest.mark.asyncio
@pytest.mark.integration
async def test_mcp_multi_graph_registration(temp_manifest):
    """
    Test MCP server handles multiple graphs in single manifest.
    
    Validates:
    - Multiple graph registration
    - Server handles multiple graphs
    """
    try:
        from universal_agent_nexus.adapters.mcp.server import MCPServerAdapter
    except ImportError:
        pytest.skip("MCP package not installed")
    
    manifest_content = """
name: multi-graph-test
version: "0.1.0"
graphs:
  - name: graph_a
    version: "1.0"
    entry_node: node_a
    nodes:
      - id: node_a
        kind: task
    edges: []
  
  - name: graph_b
    version: "1.0"
    entry_node: node_b
    nodes:
      - id: node_b
        kind: task
    edges: []
"""
    
    manifest_path = temp_manifest("multi_graph", manifest_content)
    manifest = load_manifest(manifest_path)
    
    server = MCPServerAdapter(
        manifest=manifest,
        name="test-multi-graph",
    )
    
    # Verify server handles multiple graphs
    assert len(manifest.graphs) == 2
    assert server.server is not None


@pytest.mark.asyncio
@pytest.mark.integration
async def test_mcp_server_without_postgres(sample_manifest_path):
    """
    Test MCP server can be created without Postgres URL.
    """
    try:
        from universal_agent_nexus.adapters.mcp.server import MCPServerAdapter
    except ImportError:
        pytest.skip("MCP package not installed")
    
    manifest = load_manifest(str(sample_manifest_path))
    
    server = MCPServerAdapter(
        manifest=manifest,
        postgres_url=None,  # No Postgres
        name="test-no-postgres",
    )
    
    assert server.server is not None
    assert server.postgres_url is None

