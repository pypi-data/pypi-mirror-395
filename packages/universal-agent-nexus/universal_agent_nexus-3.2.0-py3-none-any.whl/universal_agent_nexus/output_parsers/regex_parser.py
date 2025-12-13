"""
Regex Parser

Generic parser using custom regex patterns.
"""

from typing import Dict
import re
from .base import OutputParser, ParserResult


class RegexParser(OutputParser):
    """
    Generic parser using regex patterns.
    
    Extracts named groups from regex matches.
    
    Example:
        >>> parser = RegexParser({"level": r"(safe|low|medium|high|critical)"})
        >>> result = parser.parse("Risk level: high")
        >>> result.parsed
        {"level": "high"}
    """
    
    def __init__(
        self,
        patterns: Dict[str, str],
        fallback: bool = True
    ):
        """Initialize regex parser.
        
        Args:
            patterns: Dict mapping field names to regex patterns
            fallback: Fallback to raw string if parsing fails
        """
        super().__init__(fallback=fallback)
        self.patterns = patterns
        self._compiled = {}
        for name, pattern in patterns.items():
            try:
                self._compiled[name] = re.compile(pattern, re.IGNORECASE | re.DOTALL)
            except re.error as e:
                raise ValueError(f"Invalid regex for {name}: {e}")
    
    def parse(self, text: str) -> ParserResult:
        """Parse text using regex patterns.
        
        Args:
            text: Text to parse
        
        Returns:
            ParserResult with extracted fields
        """
        if not text or not text.strip():
            return self._handle_error(text, "Empty input text")
        
        parsed = {}
        match_count = 0
        
        for field_name, compiled_pattern in self._compiled.items():
            match = compiled_pattern.search(text)
            if match:
                # Use first group if available, else full match
                parsed[field_name] = match.group(1) if match.groups() else match.group(0)
                match_count += 1
        
        if match_count == 0:
            return self._handle_error(
                text,
                f"No patterns matched. Available: {list(self.patterns.keys())}"
            )
        
        return ParserResult(
            success=True,
            parsed=parsed,
            raw=text,
            confidence=match_count / len(self.patterns) if self.patterns else 0.0
        )
