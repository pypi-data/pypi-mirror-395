"""In-memory Cache Fabric backend."""

from typing import Any, Dict, List, Optional
from datetime import datetime

from ..base import CacheFabric, ContextScope, ContextEntry


class InMemoryFabric(CacheFabric):
    """In-memory Cache Fabric (for development/testing).
    
    Fast, no dependencies, but data lost on restart.
    """
    
    def __init__(self):
        self.contexts: Dict[str, Dict[str, Any]] = {}
        self.executions: List[Dict[str, Any]] = []
        self.feedback: List[Dict[str, Any]] = []
        self.metrics = {
            "total_requests": 0,
            "cache_hits": 0,
            "total_latency": 0,
            "latencies": [],
        }
        self._version_counter: Dict[str, int] = {}
    
    async def set_context(
        self,
        key: str,
        value: Any,
        scope: ContextScope = ContextScope.GLOBAL,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        if key not in self._version_counter:
            self._version_counter[key] = 0
        self._version_counter[key] += 1
        
        self.contexts[key] = {
            "key": key,
            "value": value,
            "scope": scope.value,
            "metadata": metadata or {},
            "version": self._version_counter[key],
            "timestamp": datetime.utcnow().isoformat(),
        }
        return True
    
    async def get_context(
        self,
        key: str,
        default: Any = None,
    ) -> Optional[ContextEntry]:
        entry = self.contexts.get(key)
        if entry:
            self.metrics["cache_hits"] += 1
            return ContextEntry(
                key=entry["key"],
                value=entry["value"],
                scope=ContextScope(entry["scope"]),
                metadata=entry["metadata"],
                version=entry["version"],
                timestamp=entry["timestamp"],
            )
        return default
    
    async def update_context(
        self,
        key: str,
        value: Any,
        merge: bool = False,
    ) -> bool:
        if key not in self.contexts:
            return False
        
        if merge and isinstance(value, dict) and isinstance(self.contexts[key]["value"], dict):
            self.contexts[key]["value"] = {**self.contexts[key]["value"], **value}
        else:
            self.contexts[key]["value"] = value
        
        self._version_counter[key] += 1
        self.contexts[key]["version"] = self._version_counter[key]
        self.contexts[key]["timestamp"] = datetime.utcnow().isoformat()
        return True
    
    async def track_execution(
        self,
        execution_id: str,
        graph_name: str,
        state: Dict[str, Any],
    ) -> bool:
        self.executions.append({
            "execution_id": execution_id,
            "graph_name": graph_name,
            "state": state,
            "timestamp": datetime.utcnow().isoformat(),
        })
        return True
    
    async def record_feedback(
        self,
        execution_id: str,
        feedback: Dict[str, Any],
    ) -> bool:
        self.feedback.append({
            "execution_id": execution_id,
            "feedback": feedback,
            "timestamp": datetime.utcnow().isoformat(),
        })
        return True
    
    async def get_metrics(self) -> Dict[str, Any]:
        hit_rate = (
            (self.metrics["cache_hits"] / self.metrics["total_requests"] * 100)
            if self.metrics["total_requests"] > 0
            else 0.0
        )
        
        avg_latency = (
            sum(self.metrics["latencies"]) / len(self.metrics["latencies"])
            if self.metrics["latencies"]
            else 0.0
        )
        
        cost_saved = self.metrics["cache_hits"] * 0.001  # $0.001 per cache hit
        
        # Calculate speedup (cache hit latency vs miss latency)
        if self.metrics["latencies"]:
            avg_miss = 150.0  # Typical LLM latency
            avg_hit = 50.0   # Typical cache hit latency
            speedup = avg_miss / (avg_latency if avg_latency > 0 else avg_hit)
        else:
            speedup = 1.0
        
        return {
            "backend": "memory",
            "total_requests": self.metrics["total_requests"],
            "cache_hits": self.metrics["cache_hits"],
            "hit_rate": round(hit_rate, 1),
            "avg_latency": round(avg_latency, 0),
            "cost_saved": round(cost_saved, 3),
            "speedup": round(speedup, 1),
        }
    
    async def search_similar(
        self,
        query: str,
        limit: int = 10,
    ) -> List[ContextEntry]:
        # Simple substring matching for in-memory (not semantic)
        results = []
        query_lower = query.lower()
        
        for key, entry in self.contexts.items():
            value_str = str(entry["value"]).lower()
            if query_lower in value_str or value_str in query_lower:
                results.append(ContextEntry(
                    key=entry["key"],
                    value=entry["value"],
                    scope=ContextScope(entry["scope"]),
                    metadata=entry["metadata"],
                    version=entry["version"],
                    timestamp=entry["timestamp"],
                ))
                if len(results) >= limit:
                    break
        
        return results

