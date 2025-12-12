"""
Unit tests for manifest loading and validation.
"""

import pytest
from pathlib import Path


class TestManifestLoading:
    """Test manifest loading functionality."""

    def test_load_manifest_from_path(self, sample_manifest_path: Path):
        """Test loading manifest from file path."""
        from universal_agent_nexus.manifest import load_manifest

        manifest = load_manifest(str(sample_manifest_path))

        assert manifest is not None
        assert manifest.name == "test-manifest"
        assert manifest.version == "0.1.0"

    def test_manifest_has_graphs(self, sample_manifest_path: Path):
        """Test that loaded manifest has graphs."""
        from universal_agent_nexus.manifest import load_manifest

        manifest = load_manifest(str(sample_manifest_path))

        assert len(manifest.graphs) == 1
        assert manifest.graphs[0].name == "main"

    def test_manifest_graph_has_nodes(self, sample_manifest_path: Path):
        """Test that graph has nodes."""
        from universal_agent_nexus.manifest import load_manifest

        manifest = load_manifest(str(sample_manifest_path))
        graph = manifest.graphs[0]

        assert len(graph.nodes) == 2
        node_ids = [n.id for n in graph.nodes]
        assert "start" in node_ids
        assert "process" in node_ids

    def test_manifest_graph_has_edges(self, sample_manifest_path: Path):
        """Test that graph has edges."""
        from universal_agent_nexus.manifest import load_manifest

        manifest = load_manifest(str(sample_manifest_path))
        graph = manifest.graphs[0]

        assert len(graph.edges) == 1
        edge = graph.edges[0]
        assert edge.from_node == "start"
        assert edge.to_node == "process"

    def test_manifest_has_routers(self, sample_manifest_path: Path):
        """Test that manifest has routers."""
        from universal_agent_nexus.manifest import load_manifest

        manifest = load_manifest(str(sample_manifest_path))

        assert len(manifest.routers) == 1
        router = manifest.routers[0]
        assert router.name == "test-router"
        assert router.default_model == "gpt-4o-mini"

    def test_load_nonexistent_file_raises(self):
        """Test that loading nonexistent file raises error."""
        from universal_agent_nexus.manifest import load_manifest

        with pytest.raises(FileNotFoundError):
            load_manifest("/nonexistent/path/manifest.yaml")

    def test_load_manifest_str(self):
        """Test loading manifest from YAML string."""
        from universal_agent_nexus.manifest import load_manifest_str

        yaml_content = """
name: test
version: 1.0.0
description: Test manifest
graphs:
  - name: main
    entry_node: start
    nodes:
      - id: start
        kind: task
        label: Start
    edges: []
routers: []
tools: []
"""
        manifest = load_manifest_str(yaml_content)
        assert manifest.name == "test"
        assert manifest.version == "1.0.0"
