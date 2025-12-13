"""
Universal Agent Nexus package.

The Translation Layer: Build Once, Run Anywhere.

Compile universal agent architectures to LangGraph, AWS Step Functions,
MCP, or the UAA Kernel—without rewriting code.

Usage:
    # Compile a manifest
    nexus compile agent.yaml --target langgraph --output agent.py
    nexus compile agent.yaml --target aws --output state_machine.json
    nexus compile agent.yaml --target uaa --output kernel_manifest.yaml
    
    # Load and work with manifests
    from universal_agent_nexus import load_manifest
    manifest = load_manifest("agent.yaml")
    
    # Cross-runtime state normalization
    from universal_agent_nexus.bridges import normalize, NormalizedGraphState
    normalized = normalize(langgraph_checkpoint)
"""

__version__ = "3.1.0"

__all__ = [
    # Version
    "__version__",
    # Manifest loading
    "load_manifest",
    "load_manifest_str",
    # Submodules
    "bridges",
    "enrichment",
    "adapters",
    "runtime",
    "cache_fabric",
    "output_parsers",
    # State normalization (re-exported from bridges)
    "normalize",
    "denormalize",
    "NormalizedGraphState",
    "StateFormat",
]


def load_manifest(path):
    """Load a manifest from a YAML file path."""
    from .manifest import load_manifest as _load_manifest
    return _load_manifest(path)


def load_manifest_str(yaml_content):
    """Load a manifest from a YAML string."""
    from .manifest import load_manifest_str as _load_manifest_str
    return _load_manifest_str(yaml_content)


# Re-export state normalization functions at package level
try:
    from .bridges.universal_state import (
        normalize,
        denormalize,
        NormalizedGraphState,
        NormalizedHistoryEntry,
        StateFormat,
        sync_state,
    )
except ImportError:
    # Define stubs if bridges not available
    def normalize(*args, **kwargs):
        raise ImportError("bridges module not available")
    
    def denormalize(*args, **kwargs):
        raise ImportError("bridges module not available")
    
    NormalizedGraphState = None
    StateFormat = None


# Import submodules lazily to avoid import errors when deps not installed
try:
    from . import adapters
except ImportError:
    pass

try:
    from . import bridges
except ImportError:
    pass

try:
    from . import observability
except ImportError:
    pass

try:
    from . import cli
except ImportError:
    pass

try:
    from . import runtime
except ImportError:
    pass

try:
    from . import cache_fabric
except ImportError:
    pass

try:
    from . import output_parsers
except ImportError:
    pass
