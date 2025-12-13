"""
Sentiment Parser

Parses text for sentiment analysis results.
"""

from typing import Optional
import re
from .base import OutputParser, ParserResult


class SentimentParser(OutputParser):
    """
    Parser for sentiment analysis results.
    
    Extracts sentiment (positive/negative/neutral) and optional score.
    
    Example:
        >>> parser = SentimentParser()
        >>> result = parser.parse("This is great! Sentiment: positive, 0.95")
        >>> result.parsed
        {"sentiment": "positive", "score": 0.95}
    """
    
    def __init__(
        self,
        sentiment_keywords: Optional[dict] = None,
        fallback: bool = True
    ):
        """Initialize sentiment parser.
        
        Args:
            sentiment_keywords: Dict mapping sentiment to keyword lists
            fallback: Fallback to raw string if parsing fails
        """
        super().__init__(fallback=fallback)
        self.sentiment_keywords = sentiment_keywords or {
            "positive": ["positive", "good", "great", "excellent", "happy", "love", "best"],
            "negative": ["negative", "bad", "terrible", "awful", "hate", "worst", "poor"],
            "neutral": ["neutral", "okay", "average", "normal", "fine"],
        }
    
    def parse(self, text: str) -> ParserResult:
        """Parse text for sentiment.
        
        Args:
            text: Text to parse
        
        Returns:
            ParserResult with sentiment and optional score
        """
        if not text or not text.strip():
            return self._handle_error(text, "Empty input text")
        
        search_text = text.lower()
        
        # Find sentiment matches
        sentiment_scores = {}
        for sentiment, keywords in self.sentiment_keywords.items():
            score = sum(1 for kw in keywords if kw in search_text)
            if score > 0:
                sentiment_scores[sentiment] = score
        
        if not sentiment_scores:
            return self._handle_error(
                text,
                f"No sentiment detected"
            )
        
        # Get best sentiment
        best_sentiment = max(sentiment_scores, key=sentiment_scores.get)
        
        # Try to extract numeric score
        score_match = re.search(r'(\d+\.?\d*)(?:%|)?(?:\s*out of)?', text)
        numeric_score = None
        if score_match:
            raw_score = float(score_match.group(1))
            # Normalize to 0-1 range if percentage
            numeric_score = raw_score / 100 if raw_score > 1 else raw_score
        
        parsed = {"sentiment": best_sentiment}
        if numeric_score is not None:
            parsed["score"] = round(numeric_score, 2)
        
        return ParserResult(
            success=True,
            parsed=parsed,
            raw=text,
            confidence=min(1.0, sentiment_scores[best_sentiment] / len(self.sentiment_keywords[best_sentiment]))
        )
