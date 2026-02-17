"""
Practicality scorer for actionable insights assessment.
"""
from typing import Dict, Any, List
from src.utils.logger import get_logger

logger = get_logger(__name__)


class PracticalityScorer:
    """Score items based on actionable insights and practical value."""

    # Practical/actionable keywords
    PRACTICAL_KEYWORDS = [
        'mitigation', 'remediation', 'fix', 'patch', 'solution',
        'recommendation', 'best practice', 'how to', 'guide',
        'implementation', 'defense', 'prevention', 'detection',
        'response', 'control', 'configuration', 'setting'
    ]

    def __init__(self):
        """Initialize practicality scorer."""
        pass

    def count_practical_keywords(self, text: str) -> int:
        """
        Count practical/actionable keywords in text.

        Args:
            text: Text to analyze

        Returns:
            Number of practical keyword matches
        """
        text_lower = text.lower()
        count = sum(1 for keyword in self.PRACTICAL_KEYWORDS if keyword in text_lower)
        return count

    def score(self, item: Dict[str, Any]) -> float:
        """
        Calculate practicality score for an item.

        Args:
            item: Item to score

        Returns:
            Practicality score (0-100)
        """
        title = item.get('title', '')
        content = item.get('content', '')
        text = f"{title} {content}"

        practical_count = self.count_practical_keywords(text)

        # Convert to 0-100 scale
        # Cap at 5 matches for a perfect score
        score = min(practical_count * 20, 100)

        logger.debug(f"Practicality score for '{title[:50]}...': {score} ({practical_count} practical keywords)")

        return float(score)
