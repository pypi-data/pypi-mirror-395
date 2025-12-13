"""
Classification Parser

Parses text into one of a fixed set of categories.
"""

from typing import List, Optional
import re
from .base import OutputParser, ParserResult


class ClassificationParser(OutputParser):
    """
    Parser for categorical classification.
    
    Extracts a classification result from text matching one of provided categories.
    
    Example:
        >>> parser = ClassificationParser(categories=["safe", "unsafe", "review"])
        >>> result = parser.parse("This content is UNSAFE")
        >>> result.parsed
        {"category": "unsafe"}
    """
    
    def __init__(
        self,
        categories: List[str],
        confidence_threshold: float = 0.0,
        case_insensitive: bool = True,
        fallback: bool = True
    ):
        """Initialize classification parser.
        
        Args:
            categories: List of valid category names
            confidence_threshold: Minimum confidence score (0.0-1.0)
            case_insensitive: Ignore case when matching categories
            fallback: Fallback to raw string if parsing fails
        """
        super().__init__(fallback=fallback)
        self.categories = [c.lower() if case_insensitive else c for c in categories]
        self.case_insensitive = case_insensitive
        self.confidence_threshold = confidence_threshold
    
    def parse(self, text: str) -> ParserResult:
        """Parse text for classification.
        
        Args:
            text: Text to parse
        
        Returns:
            ParserResult with category and confidence
        """
        if not text or not text.strip():
            return self._handle_error(text, "Empty input text")
        
        search_text = text.lower() if self.case_insensitive else text
        
        # Find all matching categories
        matches = []
        for category in self.categories:
            # Try exact word match first
            if re.search(rf'\b{re.escape(category)}\b', search_text, re.IGNORECASE):
                matches.append((category, 1.0))
            # Then try partial match
            elif category in search_text:
                matches.append((category, 0.7))
        
        if not matches:
            return self._handle_error(
                text,
                f"No category matched. Valid: {self.categories}"
            )
        
        # Sort by confidence descending
        matches.sort(key=lambda x: x[1], reverse=True)
        best_match, confidence = matches[0]
        
        if confidence < self.confidence_threshold:
            return self._handle_error(
                text,
                f"Confidence {confidence} below threshold {self.confidence_threshold}"
            )
        
        return ParserResult(
            success=True,
            parsed={"category": best_match},
            raw=text,
            confidence=confidence
        )
