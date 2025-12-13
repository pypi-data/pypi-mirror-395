"""Shared defaults for selecting a Cache Fabric backend across examples.

Examples should rely on this helper instead of re-implementing backend
selection logic. It makes the default (in-memory) explicit and allows
users to opt into Redis or vector backends with environment variables.
"""

import os
from typing import Dict, Tuple

from .factory import create_cache_fabric

DEFAULT_BACKEND = "memory"
DEFAULT_REDIS_URL = "redis://localhost:6379"
DEFAULT_VECTOR_URL = "http://localhost:6333"


def resolve_fabric_from_env(default_backend: str = DEFAULT_BACKEND) -> Tuple[object, Dict[str, str]]:
    """Create a Cache Fabric instance based on environment configuration.

    Environment variables:
    - CACHE_BACKEND: one of [memory|redis|vector] (defaults to ``memory``)
    - REDIS_URL: connection string used when CACHE_BACKEND=redis
    - VECTOR_URL or CACHE_VECTOR_URL: base URL used when CACHE_BACKEND=vector

    Returns a tuple of (fabric_instance, metadata_used_for_selection).
    """

    backend = os.getenv("CACHE_BACKEND", default_backend)
    
    # Validate backend
    if backend not in ["memory", "redis", "vector"]:
        raise ValueError(f"Invalid CACHE_BACKEND: {backend}. Must be one of: memory, redis, vector")
    
    redis_url = os.getenv("REDIS_URL", DEFAULT_REDIS_URL)
    vector_url = os.getenv("VECTOR_URL", os.getenv("CACHE_VECTOR_URL", DEFAULT_VECTOR_URL))

    kwargs = {}
    if backend == "redis":
        kwargs["redis_url"] = redis_url
    elif backend == "vector":
        kwargs["vector_db_url"] = vector_url

    fabric = create_cache_fabric(backend, **kwargs)

    metadata = {
        "backend": backend,
        "redis_url": redis_url if backend == "redis" else None,
        "vector_url": vector_url if backend == "vector" else None,
    }
    return fabric, metadata
