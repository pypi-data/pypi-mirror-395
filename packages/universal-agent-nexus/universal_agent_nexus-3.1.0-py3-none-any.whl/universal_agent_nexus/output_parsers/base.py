"""
Base OutputParser class.

Defines interface for all parsers.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from abc import ABC, abstractmethod
import json
import logging

logger = logging.getLogger(__name__)


@dataclass
class ParserResult:
    """Result from parsing operation."""
    success: bool
    parsed: Dict[str, Any] | List[Any] | str
    raw: str
    error: Optional[str] = None
    confidence: Optional[float] = None
    
    def __repr__(self):
        return f"ParserResult(success={self.success}, parsed={self.parsed}, confidence={self.confidence})"


class OutputParser(ABC):
    """
    Abstract base class for output parsers.
    
    Parsers convert unstructured LLM output into structured data.
    """
    
    def __init__(self, fallback: bool = True):
        """Initialize parser.
        
        Args:
            fallback: If True, fallback to returning raw string on failure
        """
        self.fallback = fallback
    
    @abstractmethod
    def parse(self, text: str) -> ParserResult:
        """Parse text into structured output.
        
        Args:
            text: Text to parse
        
        Returns:
            ParserResult with parsed data or error
        """
        raise NotImplementedError
    
    def _handle_error(self, text: str, error: str) -> ParserResult:
        """Handle parsing error with fallback.
        
        Args:
            text: Original text
            error: Error message
        
        Returns:
            ParserResult with error or fallback value
        """
        logger.warning(f"Parse error: {error}")
        if self.fallback:
            return ParserResult(
                success=True,  # Fallback is considered successful
                parsed=text,
                raw=text,
                error=error,
                confidence=0.0  # Low confidence for fallback
            )
        else:
            return ParserResult(
                success=False,
                parsed=None,
                raw=text,
                error=error
            )
    
    @staticmethod
    def try_json(text: str) -> Optional[Dict | List]:
        """Try to parse text as JSON.
        
        Args:
            text: Text to parse
        
        Returns:
            Parsed JSON or None
        """
        try:
            return json.loads(text)
        except (json.JSONDecodeError, ValueError):
            return None
