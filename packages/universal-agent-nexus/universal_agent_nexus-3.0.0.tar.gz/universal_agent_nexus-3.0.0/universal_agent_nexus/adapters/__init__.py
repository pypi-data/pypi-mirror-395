"""
Adapter interfaces and implementations for Universal Agent Nexus.

Available Adapters:
- langgraph: LangGraph Python runtime
- aws: AWS Step Functions + Lambda + DynamoDB
- mcp: Model Context Protocol servers
- uaa: Universal Agent Architecture native kernel

Usage:
    from universal_agent_nexus.adapters.langgraph import LangGraphRuntime
    from universal_agent_nexus.adapters.aws import AWSCompiler
    from universal_agent_nexus.adapters.uaa import UAANativeRuntime, UAANativeGenerator
"""

# Import adapters with graceful fallback for missing dependencies
_available_adapters = []

try:
    from . import langgraph
    _available_adapters.append("langgraph")
except ImportError:
    pass

try:
    from . import aws
    _available_adapters.append("aws")
except ImportError:
    pass

try:
    from . import mcp
    _available_adapters.append("mcp")
except ImportError:
    pass

try:
    from . import uaa
    _available_adapters.append("uaa")
except ImportError:
    pass


def list_available_adapters():
    """List all available adapters (those with installed dependencies)."""
    return _available_adapters.copy()


__all__ = [
    "list_available_adapters",
]
