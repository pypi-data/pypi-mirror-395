"""Redis-backed Cache Fabric for production."""

import json
from typing import Any, Dict, List, Optional
from datetime import datetime

from ..base import CacheFabric, ContextScope, ContextEntry


class RedisFabric(CacheFabric):
    """Redis-backed cache fabric for production.
    
    Provides persistent storage, multi-server support, and fast lookups.
    """
    
    def __init__(self, redis_url: str = "redis://localhost:6379", prefix: str = "nexus_cache"):
        self.redis_url = redis_url
        self.prefix = prefix
        self.client = None
        self.stats = {
            "reads": 0,
            "writes": 0,
            "hits": 0,
            "misses": 0,
        }
    
    async def _ensure_connected(self):
        """Ensure Redis client is connected."""
        if not self.client:
            try:
                import redis.asyncio as redis
                self.client = await redis.from_url(self.redis_url, decode_responses=True)
            except ImportError:
                raise ImportError("Install redis: pip install redis[hiredis]")
    
    def _make_key(self, key: str) -> str:
        """Create Redis key with prefix."""
        return f"{self.prefix}:{key}"
    
    async def set_context(
        self,
        key: str,
        value: Any,
        scope: ContextScope = ContextScope.GLOBAL,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        await self._ensure_connected()
        
        # Get current version
        redis_key = self._make_key(key)
        existing = await self.client.hgetall(redis_key)
        version = int(existing.get("version", "0")) + 1 if existing else 1
        
        # Serialize value
        if isinstance(value, (dict, list)):
            value_str = json.dumps(value)
        else:
            value_str = str(value)
        
        entry_data = {
            "key": key,
            "value": value_str,
            "scope": scope.value,
            "metadata": json.dumps(metadata or {}),
            "version": str(version),
            "created_at": existing.get("created_at") or datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        
        await self.client.hset(redis_key, mapping=entry_data)
        self.stats["writes"] += 1
        return True
    
    async def get_context(
        self,
        key: str,
        default: Any = None,
    ) -> Optional[ContextEntry]:
        await self._ensure_connected()
        self.stats["reads"] += 1
        
        redis_key = self._make_key(key)
        data = await self.client.hgetall(redis_key)
        
        if not data:
            self.stats["misses"] += 1
            return default
        
        self.stats["hits"] += 1
        
        # Deserialize value
        value_str = data.get("value", "")
        try:
            value = json.loads(value_str)
        except (json.JSONDecodeError, TypeError):
            value = value_str
        
        # Deserialize metadata
        metadata_str = data.get("metadata", "{}")
        try:
            metadata = json.loads(metadata_str)
        except (json.JSONDecodeError, TypeError):
            metadata = {}
        
        return ContextEntry(
            key=data.get("key", key),
            value=value,
            scope=ContextScope(data.get("scope", "global")),
            metadata=metadata,
            version=int(data.get("version", "1")),
            timestamp=data.get("updated_at"),
        )
    
    async def update_context(
        self,
        key: str,
        value: Any,
        merge: bool = False,
    ) -> bool:
        await self._ensure_connected()
        
        redis_key = self._make_key(key)
        existing = await self.client.hgetall(redis_key)
        
        if not existing:
            return False
        
        # Merge or replace
        if merge:
            existing_value_str = existing.get("value", "")
            try:
                existing_value = json.loads(existing_value_str)
                if isinstance(existing_value, dict) and isinstance(value, dict):
                    value = {**existing_value, **value}
            except (json.JSONDecodeError, TypeError):
                pass
        
        # Serialize new value
        if isinstance(value, (dict, list)):
            value_str = json.dumps(value)
        else:
            value_str = str(value)
        
        version = int(existing.get("version", "0")) + 1
        
        await self.client.hset(redis_key, mapping={
            "value": value_str,
            "version": str(version),
            "updated_at": datetime.utcnow().isoformat(),
        })
        self.stats["writes"] += 1
        return True
    
    async def track_execution(
        self,
        execution_id: str,
        graph_name: str,
        state: Dict[str, Any],
    ) -> bool:
        await self._ensure_connected()
        
        key = f"{self.prefix}:exec:{execution_id}"
        await self.client.hset(
            key,
            mapping={
                "graph_name": graph_name,
                "state": json.dumps(state),
                "timestamp": datetime.utcnow().isoformat(),
            }
        )
        await self.client.expire(key, 86400)  # 24h TTL
        return True
    
    async def record_feedback(
        self,
        execution_id: str,
        feedback: Dict[str, Any],
    ) -> bool:
        await self._ensure_connected()
        
        key = f"{self.prefix}:feedback:{execution_id}"
        await self.client.hset(
            key,
            mapping={
                "data": json.dumps(feedback),
                "timestamp": datetime.utcnow().isoformat(),
            }
        )
        await self.client.expire(key, 2592000)  # 30d TTL
        return True
    
    async def get_metrics(self) -> Dict[str, Any]:
        await self._ensure_connected()
        
        # Count keys
        cursor = "0"
        key_count = 0
        while True:
            cursor, keys = await self.client.scan(cursor, match=f"{self.prefix}:*", count=100)
            key_count += len(keys)
            if cursor == "0":
                break
        
        hit_rate = (self.stats["hits"] / self.stats["reads"] * 100) if self.stats["reads"] > 0 else 0
        
        return {
            "backend": "redis",
            "redis_url": self.redis_url,
            "entries": key_count,
            "cache_hit_rate": f"{hit_rate:.1f}%",
            "stats": self.stats,
        }
    
    async def search_similar(
        self,
        query: str,
        limit: int = 10,
    ) -> List[ContextEntry]:
        """Simple key/value search (not semantic - use VectorFabric for that)."""
        await self._ensure_connected()
        
        results = []
        query_lower = query.lower()
        cursor = "0"
        
        while True:
            cursor, keys = await self.client.scan(cursor, match=f"{self.prefix}:*", count=100)
            
            for key in keys:
                if ":exec:" in key or ":feedback:" in key:
                    continue  # Skip execution/feedback keys
                
                data = await self.client.hgetall(key)
                value_str = data.get("value", "").lower()
                
                if query_lower in value_str:
                    try:
                        value = json.loads(data.get("value", ""))
                    except (json.JSONDecodeError, TypeError):
                        value = data.get("value", "")
                    
                    try:
                        metadata = json.loads(data.get("metadata", "{}"))
                    except (json.JSONDecodeError, TypeError):
                        metadata = {}
                    
                    results.append(ContextEntry(
                        key=data.get("key", key.split(":")[-1]),
                        value=value,
                        scope=ContextScope(data.get("scope", "global")),
                        metadata=metadata,
                        version=int(data.get("version", "1")),
                        timestamp=data.get("updated_at"),
                    ))
                    
                    if len(results) >= limit:
                        return results
            
            if cursor == "0":
                break
        
        return results

