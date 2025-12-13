"""Vector database backend for semantic search (Qdrant)."""

from typing import Any, Dict, List, Optional, Callable
from datetime import datetime

from ..base import CacheFabric, ContextScope, ContextEntry


class VectorFabric(CacheFabric):
    """Vector database backend for semantic search.
    
    Uses Qdrant for semantic similarity matching of cached contexts.
    Best for LLM response caching with semantic matching.
    """
    
    def __init__(
        self,
        vector_db_url: str = "http://localhost:6333",
        embedding_fn: Optional[Callable[[str], List[float]]] = None,
        collection_name: str = "nexus_cache",
        similarity_threshold: float = 0.9,
    ):
        self.vector_db_url = vector_db_url
        self.embedding_fn = embedding_fn
        self.collection_name = collection_name
        self.threshold = similarity_threshold
        self.client = None
        self._init_qdrant()
    
    def _init_qdrant(self):
        """Initialize Qdrant client."""
        try:
            from qdrant_client import QdrantClient
            from qdrant_client.models import Distance, VectorParams
            
            self.client = QdrantClient(url=self.vector_db_url)
            
            # Create collection if not exists
            try:
                self.client.get_collection(self.collection_name)
            except Exception:
                # Default to 384 dimensions (sentence-transformers/all-MiniLM-L6-v2)
                vector_size = 384
                if self.embedding_fn:
                    # Try to infer size from embedding function
                    test_embedding = self.embedding_fn("test")
                    if isinstance(test_embedding, list):
                        vector_size = len(test_embedding)
                
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
                )
        except ImportError:
            raise ImportError("Install qdrant-client: pip install qdrant-client")
    
    async def set_context(
        self,
        key: str,
        value: Any,
        scope: ContextScope = ContextScope.GLOBAL,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Store context with embedding."""
        if not self.embedding_fn:
            raise ValueError("embedding_fn required for vector fabric")
        
        # Generate embedding from text
        text = str(value) if not isinstance(value, str) else value
        if metadata and "text" in metadata:
            text = metadata["text"]
        
        embedding = self.embedding_fn(text)
        
        from qdrant_client.models import PointStruct
        import json
        
        point = PointStruct(
            id=hash(key) % (10**9),
            vector=embedding,
            payload={
                "key": key,
                "value": json.dumps(value) if isinstance(value, (dict, list)) else str(value),
                "scope": scope.value,
                "metadata": json.dumps(metadata or {}),
                "timestamp": datetime.utcnow().isoformat(),
                "version": 1,
            }
        )
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=[point]
        )
        return True
    
    async def get_context(
        self,
        key: str,
        default: Any = None,
    ) -> Optional[ContextEntry]:
        """Retrieve context by key."""
        # Simple filter search by key
        from qdrant_client.models import Filter, FieldCondition, MatchValue
        import json
        
        results = self.client.scroll(
            collection_name=self.collection_name,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="key", match=MatchValue(value=key))
                ]
            ),
            limit=1,
            with_payload=True,
            with_vectors=False,
        )
        
        for point in results[0]:
            payload = point.payload
            try:
                value = json.loads(payload.get("value", ""))
            except (json.JSONDecodeError, TypeError):
                value = payload.get("value", "")
            
            try:
                metadata = json.loads(payload.get("metadata", "{}"))
            except (json.JSONDecodeError, TypeError):
                metadata = {}
            
            return ContextEntry(
                key=payload.get("key", key),
                value=value,
                scope=ContextScope(payload.get("scope", "global")),
                metadata=metadata,
                version=int(payload.get("version", 1)),
                timestamp=payload.get("timestamp"),
            )
        
        return default
    
    async def update_context(
        self,
        key: str,
        value: Any,
        merge: bool = False,
    ) -> bool:
        """Update context entry."""
        # For vector DB, we just re-embed and upsert
        existing = await self.get_context(key)
        if existing:
            scope = existing.scope
            metadata = existing.metadata
            if merge and isinstance(existing.value, dict) and isinstance(value, dict):
                value = {**existing.value, **value}
        else:
            scope = ContextScope.GLOBAL
            metadata = {}
        
        return await self.set_context(key, value, scope, metadata)
    
    async def track_execution(
        self,
        execution_id: str,
        graph_name: str,
        state: Dict[str, Any],
    ) -> bool:
        """Track execution state."""
        return await self.set_context(
            f"exec:{execution_id}",
            state,
            scope=ContextScope.EXECUTION,
            metadata={"graph_name": graph_name, "type": "execution"},
        )
    
    async def record_feedback(
        self,
        execution_id: str,
        feedback: Dict[str, Any],
    ) -> bool:
        """Record feedback."""
        return await self.set_context(
            f"feedback:{execution_id}",
            feedback,
            scope=ContextScope.GLOBAL,
            metadata={"type": "feedback"},
        )
    
    async def get_metrics(self) -> Dict[str, Any]:
        """Get vector DB metrics."""
        collection_info = self.client.get_collection(self.collection_name)
        
        return {
            "backend": "vector",
            "vector_db": "qdrant",
            "url": self.vector_db_url,
            "collection": self.collection_name,
            "points": collection_info.points_count,
            "threshold": self.threshold,
        }
    
    async def search_similar(
        self,
        query: str,
        limit: int = 10,
    ) -> List[ContextEntry]:
        """Semantic search context by similarity."""
        if not self.embedding_fn:
            raise ValueError("embedding_fn required for semantic search")
        
        # Generate query embedding
        query_embedding = self.embedding_fn(query)
        
        # Search in vector DB
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=limit,
            with_payload=True,
        )
        
        import json
        entries = []
        for result in results:
            if result.score >= self.threshold:
                payload = result.payload
                try:
                    value = json.loads(payload.get("value", ""))
                except (json.JSONDecodeError, TypeError):
                    value = payload.get("value", "")
                
                try:
                    metadata = json.loads(payload.get("metadata", "{}"))
                except (json.JSONDecodeError, TypeError):
                    metadata = {}
                
                metadata["similarity"] = result.score
                
                entries.append(ContextEntry(
                    key=payload.get("key", ""),
                    value=value,
                    scope=ContextScope(payload.get("scope", "global")),
                    metadata=metadata,
                    version=int(payload.get("version", 1)),
                    timestamp=payload.get("timestamp"),
                ))
        
        return entries

