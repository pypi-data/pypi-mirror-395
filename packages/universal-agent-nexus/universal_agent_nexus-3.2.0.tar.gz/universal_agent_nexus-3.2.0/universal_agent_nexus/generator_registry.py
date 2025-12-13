"""
Generator Registry for custom target format support.

Enables:
- Custom generator registration
- Target introspection
- Runtime selection
"""

import logging
from dataclasses import dataclass
from typing import Dict, Optional, Set

from .ir.generator import Generator

logger = logging.getLogger(__name__)


@dataclass
class GeneratorInfo:
    """Information about a registered generator."""

    name: str
    description: str
    aliases: Set[str]
    default_options: Dict


class GeneratorRegistry:
    """
    Central registry for all generators.

    Enables:
    - Custom generator registration
    - Target introspection
    - Runtime selection
    """

    def __init__(self):
        self._generators: Dict[str, Generator] = {}
        self._aliases: Dict[str, str] = {}  # alias -> target_type
        self._info: Dict[str, GeneratorInfo] = {}

    def register(
        self,
        target_type: str,
        generator: Generator,
        *,
        aliases: Optional[Set[str]] = None,
        default_options: Optional[Dict] = None,
        description: Optional[str] = None,
    ) -> None:
        """
        Register a custom generator.

        Args:
            target_type: Unique identifier (e.g., "langgraph", "temporal")
            generator: Generator implementation
            aliases: Alternative names
            default_options: Default generation options
            description: Human-readable description
        """
        if target_type in self._generators:
            logger.warning(f"Overwriting generator for target type: {target_type}")

        self._generators[target_type] = generator

        # Register aliases
        if aliases:
            for alias in aliases:
                if alias in self._aliases and self._aliases[alias] != target_type:
                    logger.warning(
                        f"Alias '{alias}' already registered for "
                        f"'{self._aliases[alias]}', overwriting"
                    )
                self._aliases[alias] = target_type

        # Store metadata
        self._info[target_type] = GeneratorInfo(
            name=target_type,
            description=description or f"Generator for {target_type}",
            aliases=aliases or set(),
            default_options=default_options or {},
        )

        logger.debug(f"Registered generator: {target_type}")

    def get(self, target_type: str) -> Optional[Generator]:
        """
        Get generator by target type.

        Args:
            target_type: Target type or alias

        Returns:
            Generator instance or None if not found
        """
        # Check direct match
        if target_type in self._generators:
            return self._generators[target_type]

        # Check aliases
        if target_type in self._aliases:
            actual_type = self._aliases[target_type]
            return self._generators.get(actual_type)

        return None

    def list_generators(self) -> Dict[str, GeneratorInfo]:
        """
        List all registered generators.

        Returns:
            {target_type: GeneratorInfo(...)}
        """
        return self._info.copy()

    def unregister(self, target_type: str) -> None:
        """
        Unregister a generator.

        Args:
            target_type: Target type to unregister
        """
        if target_type not in self._generators:
            logger.warning(f"Generator '{target_type}' not registered")
            return

        # Remove generator
        del self._generators[target_type]

        # Remove aliases
        aliases_to_remove = [
            alias for alias, actual_type in self._aliases.items() if actual_type == target_type
        ]
        for alias in aliases_to_remove:
            del self._aliases[alias]

        # Remove info
        if target_type in self._info:
            del self._info[target_type]

        logger.debug(f"Unregistered generator: {target_type}")


# Global instance
_default_registry = GeneratorRegistry()


def register_generator(
    target_type: str,
    generator: Generator,
    *,
    aliases: Optional[Set[str]] = None,
    default_options: Optional[Dict] = None,
    description: Optional[str] = None,
) -> None:
    """
    Convenience function to register a generator in the default registry.

    Args:
        target_type: Unique identifier (e.g., "langgraph", "temporal")
        generator: Generator implementation
        aliases: Alternative names
        default_options: Default generation options
        description: Human-readable description

    Example:
        from universal_agent_nexus.generator_registry import register_generator
        from my_platform import TemporalGenerator

        register_generator("temporal", TemporalGenerator())
    """
    _default_registry.register(
        target_type,
        generator,
        aliases=aliases,
        default_options=default_options,
        description=description,
    )


def get_generator(target_type: str) -> Generator:
    """
    Convenience function to get a generator from the default registry.

    Args:
        target_type: Target type or alias

    Returns:
        Generator instance

    Raises:
        ValueError: If generator not found
    """
    generator = _default_registry.get(target_type)
    if generator is None:
        available = list(_default_registry.list_generators().keys())
        raise ValueError(
            f"Unknown target type: {target_type}. "
            f"Available types: {available}"
        )
    return generator


def list_generators() -> Dict[str, GeneratorInfo]:
    """
    List all registered generators.

    Returns:
        {target_type: GeneratorInfo(...)}
    """
    return _default_registry.list_generators()


def get_registry() -> GeneratorRegistry:
    """
    Get the default generator registry instance.

    Returns:
        GeneratorRegistry instance
    """
    return _default_registry


def _initialize_default_generators():
    """Initialize default generators in the registry."""
    # Import here to avoid circular imports
    from .ir.generator import LangGraphGenerator, AWSGenerator, YAMLGenerator

    _default_registry.register(
        "langgraph",
        LangGraphGenerator(),
        description="LangGraph Python code generator",
    )
    _default_registry.register(
        "aws",
        AWSGenerator(),
        description="AWS Step Functions ASL generator",
    )
    _default_registry.register(
        "yaml",
        YAMLGenerator(),
        description="UAA YAML manifest generator",
    )
    
    # Register UAA Native Generator if universal-agent-arch is available
    try:
        from .adapters.uaa.compiler import UAANativeGenerator
        _default_registry.register(
            "uaa",
            UAANativeGenerator(),
            aliases={"uaa_native", "kernel"},
            description="Native manifest for the Universal Agent Architecture kernel",
        )
    except ImportError:
        # UAA not installed, register a fallback that produces YAML
        _default_registry.register(
            "uaa",
            YAMLGenerator(),
            aliases={"uaa_native", "kernel"},
            description="UAA YAML manifest (install universal-agent-arch for native support)",
        )


# Initialize default generators on module import
_initialize_default_generators()

