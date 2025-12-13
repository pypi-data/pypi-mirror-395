"""
UAA Native Adapter - Run Nexus-compiled graphs through the UAA kernel.

This adapter provides:
1. UAANativeGenerator: Compiles ManifestIR directly to UAA AgentManifest format
2. UAANativeRuntime: Executes manifests through the UAA GraphEngine

Usage:
    # Compile to UAA native format
    nexus compile manifest.yaml --target uaa --output agent_manifest.yaml
    
    # Execute through UAA kernel
    from universal_agent_nexus.adapters.uaa import UAANativeRuntime
    
    runtime = UAANativeRuntime(
        task_store=my_task_store,
        llm_client=my_llm_client,
        tool_executors={"mcp": mcp_executor},
    )
    result = await runtime.execute(manifest, graph_name="main", input_data={...})
"""

from .compiler import UAANativeGenerator
from .runtime import UAANativeRuntime

__all__ = [
    "UAANativeGenerator",
    "UAANativeRuntime",
]

