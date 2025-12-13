"""
Runtime Abstractions

Promotion target: universal-agent-nexus@3.1.0

This module provides runtime abstractions for executing Universal Agent manifests,
following SOLID principles throughout.
"""

from .runtime_base import (
    NexusRuntime,
    ResultExtractor,
    MessagesStateExtractor,
    ClassificationExtractor,
    JSONExtractor,
)
from .standard_integration import StandardExample
from .registry import ToolRegistry, ToolDefinition, get_registry

__all__ = [
    # Runtime base
    "NexusRuntime",
    "ResultExtractor",
    "MessagesStateExtractor",
    "ClassificationExtractor",
    "JSONExtractor",
    # Standard integration
    "StandardExample",
    # Tool registry
    "ToolRegistry",
    "ToolDefinition",
    "get_registry",
]

