"""
Extraction Parser

Parses text to extract structured fields using patterns.
"""

from typing import Dict, List, Optional, Any
import re
from .base import OutputParser, ParserResult


class ExtractionParser(OutputParser):
    """
    Parser for extracting structured data from text.
    
    Uses patterns (regex or key-value pairs) to extract fields.
    
    Example:
        >>> parser = ExtractionParser(
        ...     fields={"name": r"Name: ([^,]+)", "age": r"Age: (\d+)"}
        ... )
        >>> result = parser.parse("Name: John, Age: 30")
        >>> result.parsed
        {"name": "John", "age": "30"}
    """
    
    def __init__(
        self,
        fields: Dict[str, str],
        required: Optional[List[str]] = None,
        fallback: bool = True
    ):
        """Initialize extraction parser.
        
        Args:
            fields: Dict mapping field names to regex patterns
            required: List of required fields (error if missing)
            fallback: Fallback to raw string if parsing fails
        """
        super().__init__(fallback=fallback)
        self.fields = fields
        self.required = required or []
    
    def parse(self, text: str) -> ParserResult:
        """Parse text to extract fields.
        
        Args:
            text: Text to parse
        
        Returns:
            ParserResult with extracted fields
        """
        if not text or not text.strip():
            return self._handle_error(text, "Empty input text")
        
        extracted = {}
        found_count = 0
        
        for field_name, pattern in self.fields.items():
            try:
                match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
                if match:
                    # Use first group if available, else full match
                    extracted[field_name] = match.group(1) if match.groups() else match.group(0)
                    found_count += 1
            except re.error as e:
                return self._handle_error(text, f"Invalid regex for {field_name}: {e}")
        
        # Check required fields
        missing = [f for f in self.required if f not in extracted]
        if missing:
            return self._handle_error(
                text,
                f"Missing required fields: {missing}"
            )
        
        if found_count == 0:
            return self._handle_error(
                text,
                f"No fields extracted. Patterns: {list(self.fields.keys())}"
            )
        
        return ParserResult(
            success=True,
            parsed=extracted,
            raw=text,
            confidence=found_count / len(self.fields) if self.fields else 0.0
        )
