"""
Impact scorer for severity and affected users assessment.
"""
from typing import Dict, Any, List
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ImpactScorer:
    """Score items based on impact and severity."""

    # High-impact keywords
    HIGH_IMPACT_KEYWORDS = [
        'critical', 'severe', 'zero-day', 'widespread', 'exploit',
        'vulnerability', 'breach', 'CVE', 'actively exploited',
        'major', 'emergency', 'urgent'
    ]

    # Medium-impact keywords
    MEDIUM_IMPACT_KEYWORDS = [
        'moderate', 'important', 'significant', 'notable',
        'affected', 'impacted', 'exposure'
    ]

    def __init__(self):
        """Initialize impact scorer."""
        pass

    def count_impact_keywords(self, text: str) -> tuple:
        """
        Count high and medium impact keywords in text.

        Args:
            text: Text to analyze

        Returns:
            Tuple of (high_impact_count, medium_impact_count)
        """
        text_lower = text.lower()

        high_count = sum(1 for keyword in self.HIGH_IMPACT_KEYWORDS if keyword in text_lower)
        medium_count = sum(1 for keyword in self.MEDIUM_IMPACT_KEYWORDS if keyword in text_lower)

        return high_count, medium_count

    def score(self, item: Dict[str, Any]) -> float:
        """
        Calculate impact score for an item.

        Args:
            item: Item to score

        Returns:
            Impact score (0-100)
        """
        title = item.get('title', '')
        content = item.get('content', '')
        text = f"{title} {content}"

        high_count, medium_count = self.count_impact_keywords(text)

        # Calculate score: high impact keywords worth more
        score = min(high_count * 20 + medium_count * 10, 100)

        logger.debug(f"Impact score for '{title[:50]}...': {score} (high:{high_count}, medium:{medium_count})")

        return float(score)
