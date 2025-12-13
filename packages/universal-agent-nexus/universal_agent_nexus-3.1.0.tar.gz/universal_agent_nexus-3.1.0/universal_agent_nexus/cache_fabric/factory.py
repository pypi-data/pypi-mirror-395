"""Factory for creating Cache Fabric instances."""

from typing import Any, Dict

from .base import CacheFabric
from .backends import InMemoryFabric, RedisFabric, VectorFabric


def create_cache_fabric(backend: str = "memory", **kwargs) -> CacheFabric:
    """Create a Cache Fabric instance.
    
    Args:
        backend: Backend type ('memory', 'redis', 'vector')
        **kwargs: Backend-specific configuration:
            - redis: redis_url, prefix
            - vector: vector_db_url, embedding_fn, collection_name, similarity_threshold
    
    Returns:
        CacheFabric instance
    
    Examples:
        >>> # In-memory (development)
        >>> fabric = create_cache_fabric("memory")
        
        >>> # Redis (production)
        >>> fabric = create_cache_fabric("redis", redis_url="redis://localhost:6379")
        
        >>> # Vector DB (semantic search)
        >>> from sentence_transformers import SentenceTransformer
        >>> model = SentenceTransformer('all-MiniLM-L6-v2')
        >>> fabric = create_cache_fabric("vector", embedding_fn=model.encode)
    """
    if backend == "memory":
        return InMemoryFabric()
    elif backend == "redis":
        redis_url = kwargs.get("redis_url", "redis://localhost:6379")
        prefix = kwargs.get("prefix", "nexus_cache")
        return RedisFabric(redis_url=redis_url, prefix=prefix)
    elif backend == "vector":
        vector_db_url = kwargs.get("vector_db_url", "http://localhost:6333")
        embedding_fn = kwargs.get("embedding_fn")
        collection_name = kwargs.get("collection_name", "nexus_cache")
        similarity_threshold = kwargs.get("similarity_threshold", 0.9)
        
        if not embedding_fn:
            raise ValueError("embedding_fn required for vector backend")
        
        return VectorFabric(
            vector_db_url=vector_db_url,
            embedding_fn=embedding_fn,
            collection_name=collection_name,
            similarity_threshold=similarity_threshold,
        )
    else:
        raise ValueError(f"Unknown backend: {backend}. Choose from: memory, redis, vector")

