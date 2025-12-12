"""
Manifest loading and re-exports from universal-agent-arch.

This module provides a convenient interface for loading manifests
and re-exports the core types from the universal_agent package.
"""

from pathlib import Path
from typing import Union

import yaml

# Re-export core types from universal-agent-arch
from universal_agent import AgentManifest
from universal_agent.manifests.schema import (
    AgentManifest,
    EdgeCondition,
    EdgeTrigger,
    GraphEdgeSpec,
    GraphNodeKind,
    GraphNodeSpec,
    GraphSpec,
    RouterSpec,
    ToolSpec,
)


def load_manifest(path: Union[str, Path]) -> AgentManifest:
    """
    Load an AgentManifest from a YAML file.

    Args:
        path: Path to the manifest YAML file.

    Returns:
        Loaded and validated AgentManifest.

    Raises:
        FileNotFoundError: If the manifest file doesn't exist.
        ValueError: If the manifest is invalid.
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Manifest not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return AgentManifest(**data)


def load_manifest_str(yaml_content: str) -> AgentManifest:
    """
    Load an AgentManifest from a YAML string.

    Args:
        yaml_content: YAML string content.

    Returns:
        Loaded and validated AgentManifest.
    """
    data = yaml.safe_load(yaml_content)
    return AgentManifest(**data)


# ===== EXPORTS =====

__all__ = [
    # Core types (re-exported from universal_agent)
    "AgentManifest",
    "GraphSpec",
    "GraphNodeSpec",
    "GraphEdgeSpec",
    "GraphNodeKind",
    "EdgeTrigger",
    "EdgeCondition",
    "RouterSpec",
    "ToolSpec",
    # Loading functions
    "load_manifest",
    "load_manifest_str",
]
