"""
Boolean Parser

Parses text for yes/no or true/false responses.
"""

from typing import Optional
import re
from .base import OutputParser, ParserResult


class BooleanParser(OutputParser):
    """
    Parser for boolean (yes/no, true/false) responses.
    
    Example:
        >>> parser = BooleanParser()
        >>> result = parser.parse("The answer is yes")
        >>> result.parsed
        {"value": True}
    """
    
    def __init__(
        self,
        true_keywords: Optional[list] = None,
        false_keywords: Optional[list] = None,
        fallback: bool = True
    ):
        """Initialize boolean parser.
        
        Args:
            true_keywords: Words indicating True
            false_keywords: Words indicating False
            fallback: Fallback to raw string if parsing fails
        """
        super().__init__(fallback=fallback)
        self.true_keywords = true_keywords or [
            "yes", "true", "correct", "right", "affirmative", "positive", "approved", "accepted"
        ]
        self.false_keywords = false_keywords or [
            "no", "false", "incorrect", "wrong", "negative", "rejected", "denied", "declined"
        ]
    
    def parse(self, text: str) -> ParserResult:
        """Parse text for boolean value.
        
        Args:
            text: Text to parse
        
        Returns:
            ParserResult with boolean value
        """
        if not text or not text.strip():
            return self._handle_error(text, "Empty input text")
        
        search_text = text.lower()
        
        # Count matches
        true_count = sum(1 for kw in self.true_keywords if re.search(rf'\b{re.escape(kw)}\b', search_text))
        false_count = sum(1 for kw in self.false_keywords if re.search(rf'\b{re.escape(kw)}\b', search_text))
        
        if true_count == 0 and false_count == 0:
            return self._handle_error(
                text,
                f"No boolean indicator found. True keywords: {self.true_keywords}, False keywords: {self.false_keywords}"
            )
        
        # Majority vote
        value = true_count >= false_count
        confidence = max(true_count, false_count) / (true_count + false_count) if (true_count + false_count) > 0 else 0.0
        
        return ParserResult(
            success=True,
            parsed={"value": value},
            raw=text,
            confidence=confidence
        )
