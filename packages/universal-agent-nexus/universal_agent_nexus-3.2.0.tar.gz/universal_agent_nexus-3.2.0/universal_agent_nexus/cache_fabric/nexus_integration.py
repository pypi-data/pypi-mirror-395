"""Nexus compiler integration - Store system prompts in fabric during compilation."""

from typing import Optional
from universal_agent_nexus.ir import ManifestIR

from .base import CacheFabric, ContextScope


async def store_manifest_contexts(
    manifest: ManifestIR,
    fabric: CacheFabric,
    graph_name: Optional[str] = None,
) -> None:
    """Extract and store system prompts from manifest into fabric.
    
    This is called after manifest parsing/optimization, before runtime initialization.
    
    Args:
        manifest: Parsed and optimized ManifestIR
        fabric: Cache Fabric instance
        graph_name: Optional graph name filter
    """
    # Store router system prompts
    for router in manifest.routers or []:
        if router.system_message:
            key = f"router:{router.name}:system_prompt"
            await fabric.set_context(
                key=key,
                value=router.system_message,
                scope=ContextScope.GLOBAL,
                metadata={
                    "router_name": router.name,
                    "graph": graph_name or "main",
                    "type": "system_prompt",
                },
            )
    
    # Store tool definitions
    for tool in manifest.tools or []:
        key = f"tool:{tool.name}:definition"
        await fabric.set_context(
            key=key,
            value={
                "name": tool.name,
                "description": tool.description or "",
                "protocol": tool.protocol or "",
                "config": tool.config or {},
            },
            scope=ContextScope.GLOBAL,
            metadata={
                "tool_name": tool.name,
                "type": "tool_definition",
            },
        )
    
    # Store graph metadata
    for graph in manifest.graphs or []:
        graph_key = f"graph:{graph.name}:metadata"
        await fabric.set_context(
            key=graph_key,
            value={
                "name": graph.name,
                "entry_node": graph.entry_node or "",
                "node_count": len(graph.nodes or []),
            },
            scope=ContextScope.GLOBAL,
            metadata={
                "graph_name": graph.name,
                "type": "graph_metadata",
            },
        )


async def get_router_prompt_from_fabric(
    router_name: str,
    fabric: CacheFabric,
    default: Optional[str] = None,
) -> Optional[str]:
    """Get router system prompt from fabric (hot-reload enabled).
    
    Args:
        router_name: Router name
        fabric: Cache Fabric instance
        default: Default prompt if not found in fabric
    
    Returns:
        System prompt from fabric (latest version) or default
    """
    key = f"router:{router_name}:system_prompt"
    entry = await fabric.get_context(key)
    
    if entry:
        return entry.value
    
    return default

