"""
Output Parsers

Promotion target: universal-agent-nexus
"""

from .base import OutputParser, ParserResult
from .classification import ClassificationParser
from .sentiment import SentimentParser
from .extraction import ExtractionParser
from .boolean import BooleanParser
from .regex_parser import RegexParser

__all__ = [
    "OutputParser",
    "ParserResult",
    "ClassificationParser",
    "SentimentParser",
    "ExtractionParser",
    "BooleanParser",
    "RegexParser",
]


def get_parser(parser_type: str, **kwargs) -> OutputParser:
    """
    Factory function to get parser by type.
    
    Args:
        parser_type: 'classification', 'sentiment', 'extraction', 'boolean', 'regex'
        **kwargs: Parser-specific configuration
    
    Returns:
        Configured OutputParser instance
    """
    parsers = {
        "classification": ClassificationParser,
        "sentiment": SentimentParser,
        "extraction": ExtractionParser,
        "boolean": BooleanParser,
        "regex": RegexParser,
    }
    
    parser_class = parsers.get(parser_type.lower())
    if not parser_class:
        raise ValueError(f"Unknown parser type: {parser_type}. Available: {list(parsers.keys())}")
    
    return parser_class(**kwargs)
