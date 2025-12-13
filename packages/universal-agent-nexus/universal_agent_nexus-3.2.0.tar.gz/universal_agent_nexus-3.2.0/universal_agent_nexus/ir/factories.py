"""
Factory interfaces for creating ToolIR and RouterIR instances.

Enables:
- Custom tool instantiation logic
- Protocol-specific configuration
- Tool validation & registration
- Custom router instantiation logic
- LLM model selection strategies
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from . import RouterIR, RouterStrategy, ToolIR


class ToolFactory(ABC):
    """
    Factory for creating ToolIR instances.

    Enables:
    - Custom tool instantiation logic
    - Protocol-specific configuration
    - Tool validation & registration
    """

    @abstractmethod
    def create_tool(
        self,
        name: str,
        description: str,
        protocol: str,
        config: Dict[str, Any],
    ) -> ToolIR:
        """
        Create ToolIR with custom logic.

        Args:
            name: Tool name
            description: Tool description
            protocol: Protocol (mcp, http, subprocess, aws_lambda, etc.)
            config: Tool configuration

        Returns:
            ToolIR instance
        """
        pass


class RouterFactory(ABC):
    """
    Factory for creating RouterIR instances.

    Enables:
    - Custom router instantiation logic
    - LLM model selection strategies
    - Router validation & registration
    """

    @abstractmethod
    def create_router(
        self,
        name: str,
        strategy: RouterStrategy,
        system_message: Optional[str],
        model_candidates: List[str],
        default_model: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
    ) -> RouterIR:
        """
        Create RouterIR with custom logic.

        Args:
            name: Router name
            strategy: Router strategy (LLM, FUNCTION, SWITCH)
            system_message: System message for LLM routers
            model_candidates: List of model names
            default_model: Default model to use
            config: Additional router configuration

        Returns:
            RouterIR instance
        """
        pass


class DefaultToolFactory(ToolFactory):
    """Default tool factory implementation."""

    def create_tool(
        self,
        name: str,
        description: str,
        protocol: str,
        config: Dict[str, Any],
    ) -> ToolIR:
        """Create ToolIR with default logic."""
        return ToolIR(
            name=name,
            description=description,
            protocol=protocol,
            config=config,
        )


class DefaultRouterFactory(RouterFactory):
    """Default router factory implementation."""

    def create_router(
        self,
        name: str,
        strategy: RouterStrategy,
        system_message: Optional[str],
        model_candidates: List[str],
        default_model: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
    ) -> RouterIR:
        """Create RouterIR with default logic."""
        return RouterIR(
            name=name,
            strategy=strategy,
            system_message=system_message,
            model_candidates=model_candidates,
            default_model=default_model,
            config=config or {},
        )


# Global factories (injectable)
_tool_factory: ToolFactory = DefaultToolFactory()
_router_factory: RouterFactory = DefaultRouterFactory()


def set_tool_factory(factory: ToolFactory) -> None:
    """
    Set global tool factory.

    Args:
        factory: ToolFactory instance

    Example:
        from universal_agent_nexus.ir.factories import set_tool_factory, ToolFactory

        class CustomToolFactory(ToolFactory):
            def create_tool(self, name, description, protocol, config):
                # Add retry logic to all tools
                config["retry"] = {"max_attempts": 3, "backoff_factor": 2}
                return super().create_tool(name, description, protocol, config)

        set_tool_factory(CustomToolFactory())
    """
    global _tool_factory
    _tool_factory = factory


def set_router_factory(factory: RouterFactory) -> None:
    """
    Set global router factory.

    Args:
        factory: RouterFactory instance

    Example:
        from universal_agent_nexus.ir.factories import set_router_factory, RouterFactory

        class CustomRouterFactory(RouterFactory):
            def create_router(self, name, strategy, system_message, model_candidates, ...):
                # Add fallback logic
                if not default_model and model_candidates:
                    default_model = model_candidates[0]
                return super().create_router(...)

        set_router_factory(CustomRouterFactory())
    """
    global _router_factory
    _router_factory = factory


def get_tool_factory() -> ToolFactory:
    """
    Get global tool factory.

    Returns:
        Current ToolFactory instance
    """
    return _tool_factory


def get_router_factory() -> RouterFactory:
    """
    Get global router factory.

    Returns:
        Current RouterFactory instance
    """
    return _router_factory

