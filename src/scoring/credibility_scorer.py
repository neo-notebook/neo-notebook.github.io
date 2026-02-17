"""
Credibility scorer for source authority assessment.
"""
from typing import Dict, Any
from src.utils.logger import get_logger

logger = get_logger(__name__)


class CredibilityScorer:
    """Score items based on source credibility."""

    # Credibility tier to score mapping
    TIER_SCORES = {
        'high': 100,
        'medium': 70,
        'low': 40,
        'unknown': 50
    }

    def __init__(self):
        """Initialize credibility scorer."""
        pass

    def score(self, item: Dict[str, Any]) -> float:
        """
        Calculate credibility score for an item.

        Args:
            item: Item to score (should have 'credibility_tier' field from source)

        Returns:
            Credibility score (0-100)
        """
        # Get credibility tier from item (set during fetching from source config)
        tier = item.get('credibility_tier', 'unknown').lower()

        score = self.TIER_SCORES.get(tier, 50)

        logger.debug(f"Credibility score for '{item.get('source', 'Unknown')}': {score} (tier: {tier})")

        return float(score)
