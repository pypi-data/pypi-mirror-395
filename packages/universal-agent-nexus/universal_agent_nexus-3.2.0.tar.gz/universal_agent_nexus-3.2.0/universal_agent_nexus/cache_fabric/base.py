"""Base Cache Fabric abstraction."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime
from enum import Enum
from dataclasses import dataclass


class ContextScope(Enum):
    """Scope for context entries."""
    GLOBAL = "global"  # Shared across all executions
    EXECUTION = "execution"  # Per-execution context
    TENANT = "tenant"  # Per-tenant context
    FEEDBACK = "feedback"  # Feedback data for executions


@dataclass
class ContextEntry:
    """Context entry structure."""
    key: str
    value: Any
    scope: ContextScope
    metadata: Dict[str, Any]
    version: int = 1
    timestamp: Optional[str] = None


class CacheFabric(ABC):
    """Abstract base class for Cache Fabric implementations.
    
    The Cache Fabric sits between Nexus (compilation) and Agent (runtime),
    enabling live context updates, semantic caching, and feedback loops.
    """
    
    @abstractmethod
    async def set_context(
        self,
        key: str,
        value: Any,
        scope: ContextScope = ContextScope.GLOBAL,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Store context entry (system prompt, tool definition, etc.).
        
        Args:
            key: Context key (e.g., 'system_prompt', 'tool_definitions')
            value: Context value (string, dict, etc.)
            scope: Context scope (GLOBAL, EXECUTION, TENANT)
            metadata: Optional metadata (version, timestamp, etc.)
        
        Returns:
            True if successful
        """
        pass
    
    @abstractmethod
    async def get_context(
        self,
        key: str,
        default: Any = None,
    ) -> Optional[ContextEntry]:
        """Retrieve context entry.
        
        Args:
            key: Context key
            default: Default value if not found
        
        Returns:
            ContextEntry or None
        """
        pass
    
    @abstractmethod
    async def update_context(
        self,
        key: str,
        value: Any,
        merge: bool = False,
    ) -> bool:
        """Update existing context entry (increments version).
        
        Args:
            key: Context key
            value: New value
            merge: If True, merge with existing value (for dicts)
        
        Returns:
            True if successful
        """
        pass
    
    @abstractmethod
    async def track_execution(
        self,
        execution_id: str,
        graph_name: str,
        state: Dict[str, Any],
    ) -> bool:
        """Track execution state for analysis and feedback.
        
        Args:
            execution_id: Unique execution identifier
            graph_name: Graph name
            state: Execution state (input, output, nodes executed, etc.)
        
        Returns:
            True if successful
        """
        pass
    
    @abstractmethod
    async def record_feedback(
        self,
        execution_id: str,
        feedback: Dict[str, Any],
    ) -> bool:
        """Record feedback for an execution (for feedback loops).
        
        Args:
            execution_id: Execution identifier
            feedback: Feedback data (status, classification, user_rating, etc.)
        
        Returns:
            True if successful
        """
        pass
    
    @abstractmethod
    async def get_metrics(self) -> Dict[str, Any]:
        """Get cache fabric metrics.
        
        Returns:
            Dict with: hit_rate, avg_latency, cost_saved, speedup, etc.
        """
        pass
    
    @abstractmethod
    async def search_similar(
        self,
        query: str,
        limit: int = 10,
    ) -> List[ContextEntry]:
        """Semantic search for similar cached contexts (vector DB only).
        
        Args:
            query: Search query
            limit: Max results
        
        Returns:
            List of similar context entries
        """
        pass

