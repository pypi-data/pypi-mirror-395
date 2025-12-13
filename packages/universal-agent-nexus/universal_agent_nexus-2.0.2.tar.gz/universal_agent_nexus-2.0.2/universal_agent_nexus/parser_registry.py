"""
Parser Registry for custom source format support.

Enables:
- Custom parser registration
- Parser introspection
- Priority-based selection
- Source type detection
"""

import logging
from dataclasses import dataclass
from typing import Dict, List, Optional, Set

from .ir.parser import Parser

logger = logging.getLogger(__name__)


@dataclass
class ParserInfo:
    """Information about a registered parser."""

    name: str
    description: str
    aliases: Set[str]
    detection_priority: int


class ParserRegistry:
    """
    Central registry for all parsers.

    Enables:
    - Custom parser registration
    - Parser introspection
    - Priority-based selection
    - Source type detection
    """

    def __init__(self):
        self._parsers: Dict[str, Parser] = {}
        self._detection_priority: List[str] = []  # Ordered by detection priority
        self._aliases: Dict[str, str] = {}  # alias -> source_type
        self._info: Dict[str, ParserInfo] = {}

    def register(
        self,
        source_type: str,
        parser: Parser,
        *,
        detection_priority: int = 100,
        aliases: Optional[Set[str]] = None,
        description: Optional[str] = None,
    ) -> None:
        """
        Register a custom parser.

        Args:
            source_type: Unique identifier (e.g., "langgraph", "airflow")
            parser: Parser implementation
            detection_priority: Higher = checked first in auto-detect
            aliases: Alternative names (e.g., {"uaa", "yaml"})
            description: Human-readable description
        """
        if source_type in self._parsers:
            logger.warning(f"Overwriting parser for source type: {source_type}")

        self._parsers[source_type] = parser

        # Register aliases
        if aliases:
            for alias in aliases:
                if alias in self._aliases and self._aliases[alias] != source_type:
                    logger.warning(
                        f"Alias '{alias}' already registered for "
                        f"'{self._aliases[alias]}', overwriting"
                    )
                self._aliases[alias] = source_type

        # Update detection priority
        if source_type not in self._detection_priority:
            # Insert sorted by priority (higher first)
            inserted = False
            for i, existing_type in enumerate(self._detection_priority):
                existing_info = self._info.get(existing_type)
                if existing_info and existing_info.detection_priority < detection_priority:
                    self._detection_priority.insert(i, source_type)
                    inserted = True
                    break
            if not inserted:
                self._detection_priority.append(source_type)
        else:
            # Re-sort if priority changed
            self._detection_priority.remove(source_type)
            inserted = False
            for i, existing_type in enumerate(self._detection_priority):
                existing_info = self._info.get(existing_type)
                if existing_info and existing_info.detection_priority < detection_priority:
                    self._detection_priority.insert(i, source_type)
                    inserted = True
                    break
            if not inserted:
                self._detection_priority.append(source_type)

        # Store metadata
        self._info[source_type] = ParserInfo(
            name=source_type,
            description=description or f"Parser for {source_type}",
            aliases=aliases or set(),
            detection_priority=detection_priority,
        )

        logger.debug(f"Registered parser: {source_type} (priority={detection_priority})")

    def get(self, source_type: str) -> Optional[Parser]:
        """
        Get parser by source type.

        Args:
            source_type: Source type or alias

        Returns:
            Parser instance or None if not found
        """
        # Check direct match
        if source_type in self._parsers:
            return self._parsers[source_type]

        # Check aliases
        if source_type in self._aliases:
            actual_type = self._aliases[source_type]
            return self._parsers.get(actual_type)

        return None

    def detect(self, source: str) -> Optional[str]:
        """
        Auto-detect source type.

        Returns source_type if detected, None if ambiguous/unknown.

        Args:
            source: Path to source file or source string

        Returns:
            Source type string or None
        """
        # Try parsers in priority order
        for source_type in self._detection_priority:
            parser = self._parsers[source_type]
            if parser.can_parse(source):
                return source_type

        return None

    def list_parsers(self) -> Dict[str, ParserInfo]:
        """
        List all registered parsers.

        Returns:
            {source_type: ParserInfo(name, description, aliases)}
        """
        return self._info.copy()

    def unregister(self, source_type: str) -> None:
        """
        Unregister a parser.

        Args:
            source_type: Source type to unregister
        """
        if source_type not in self._parsers:
            logger.warning(f"Parser '{source_type}' not registered")
            return

        # Remove parser
        del self._parsers[source_type]

        # Remove from detection priority
        if source_type in self._detection_priority:
            self._detection_priority.remove(source_type)

        # Remove aliases
        aliases_to_remove = [
            alias for alias, actual_type in self._aliases.items() if actual_type == source_type
        ]
        for alias in aliases_to_remove:
            del self._aliases[alias]

        # Remove info
        if source_type in self._info:
            del self._info[source_type]

        logger.debug(f"Unregistered parser: {source_type}")


# Global instance
_default_registry = ParserRegistry()


def register_parser(
    source_type: str,
    parser: Parser,
    *,
    detection_priority: int = 100,
    aliases: Optional[Set[str]] = None,
    description: Optional[str] = None,
) -> None:
    """
    Convenience function to register a parser in the default registry.

    Args:
        source_type: Unique identifier (e.g., "langgraph", "airflow")
        parser: Parser implementation
        detection_priority: Higher = checked first in auto-detect
        aliases: Alternative names (e.g., {"uaa", "yaml"})
        description: Human-readable description

    Example:
        from universal_agent_nexus.parser_registry import register_parser
        from my_framework import MyFrameworkParser

        register_parser("my_framework", MyFrameworkParser())
    """
    _default_registry.register(
        source_type,
        parser,
        detection_priority=detection_priority,
        aliases=aliases,
        description=description,
    )


def get_parser(source_type: str) -> Parser:
    """
    Convenience function to get a parser from the default registry.

    Args:
        source_type: Source type or alias

    Returns:
        Parser instance

    Raises:
        ValueError: If parser not found
    """
    parser = _default_registry.get(source_type)
    if parser is None:
        available = list(_default_registry.list_parsers().keys())
        raise ValueError(
            f"Unknown source type: {source_type}. "
            f"Available types: {available}"
        )
    return parser


def detect_source_type(source: str) -> str:
    """
    Convenience function to auto-detect source type.

    Args:
        source: Path to source file or source string

    Returns:
        Source type string

    Raises:
        ValueError: If source type cannot be detected
    """
    detected = _default_registry.detect(source)
    if detected is None:
        raise ValueError(f"Cannot detect source type for: {source}")
    return detected


def list_parsers() -> Dict[str, ParserInfo]:
    """
    List all registered parsers.

    Returns:
        {source_type: ParserInfo(...)}
    """
    return _default_registry.list_parsers()


def get_registry() -> ParserRegistry:
    """
    Get the default parser registry instance.

    Returns:
        ParserRegistry instance
    """
    return _default_registry


def _initialize_default_parsers():
    """Initialize default parsers in the registry."""
    # Import here to avoid circular imports
    from .ir.parser import LangGraphParser, AWSParser, YAMLParser

    _default_registry.register(
        "langgraph",
        LangGraphParser(),
        detection_priority=200,
        description="LangGraph Python parser",
    )
    _default_registry.register(
        "aws",
        AWSParser(),
        detection_priority=150,
        description="AWS Step Functions ASL parser",
    )
    _default_registry.register(
        "yaml",
        YAMLParser(),
        detection_priority=100,
        aliases={"uaa"},
        description="UAA YAML manifest parser",
    )


# Initialize default parsers on module import
_initialize_default_parsers()

