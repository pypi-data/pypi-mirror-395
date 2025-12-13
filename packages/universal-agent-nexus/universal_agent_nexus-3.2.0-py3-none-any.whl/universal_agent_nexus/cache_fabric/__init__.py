"""
Cache Fabric Layer

Promotion target: universal-agent-nexus
"""

from .base import CacheFabric, ContextScope, ContextEntry
from .backends import InMemoryFabric, RedisFabric, VectorFabric
from .defaults import resolve_fabric_from_env
from .factory import create_cache_fabric

__all__ = [
    "CacheFabric",
    "ContextScope",
    "ContextEntry",
    "InMemoryFabric",
    "RedisFabric",
    "VectorFabric",
    "create_cache_fabric",
    "resolve_fabric_from_env",
]
