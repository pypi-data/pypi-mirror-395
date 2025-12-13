"""
Cross-adapter translation helpers.

This module provides bridges for:
- State normalization across runtimes (LangGraph ↔ AWS ↔ UAA)
- Fabric to Architecture schema conversion
- Cross-runtime state synchronization

Usage:
    from universal_agent_nexus.bridges import (
        normalize,
        denormalize,
        NormalizedGraphState,
        StateFormat,
    )
    
    # Normalize LangGraph checkpoint to UAA format
    normalized = normalize(langgraph_checkpoint)
    
    # Convert back to LangGraph format
    langgraph_state = denormalize(normalized, StateFormat.LANGGRAPH)
"""

from .universal_state import (
    # Models
    NormalizedHistoryEntry,
    NormalizedGraphState,
    # Enums
    StateFormat,
    # Functions
    detect_format,
    normalize,
    denormalize,
    sync_state,
)

__all__ = [
    # Models
    "NormalizedHistoryEntry",
    "NormalizedGraphState",
    # Enums
    "StateFormat",
    # Functions
    "detect_format",
    "normalize",
    "denormalize",
    "sync_state",
]
