"""
universal_agent_nexus.adapters.base

Defines the contract for a Nexus Adapter.
An adapter translates the Universal Manifest into a target ecosystem's format.
"""

from abc import ABC, abstractmethod
from typing import Any

from universal_agent.manifests.schema import AgentManifest


class BaseCompiler(ABC):
    """Abstract base class for compiling UAA Graphs into target runtime artifacts."""

    @abstractmethod
    def compile(self, manifest: AgentManifest, graph_name: str) -> Any:
        """
        Translates a specific graph from the manifest into the target format.

        Args:
            manifest: The source Universal Agent definition.
            graph_name: Which graph in the manifest to compile.

        Returns:
            The target artifact (e.g., a LangGraph Runnable, a JSON dict for ASL, etc.)
        """
        pass

