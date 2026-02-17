"""
Freshness scorer for recency assessment.
"""
from typing import Dict, Any
from datetime import datetime, timedelta
from dateutil import parser as date_parser
from src.utils.logger import get_logger

logger = get_logger(__name__)


class FreshnessScorer:
    """Score items based on recency."""

    def __init__(self):
        """Initialize freshness scorer."""
        pass

    def parse_date(self, date_value: Any) -> datetime:
        """
        Parse date value to datetime object.

        Args:
            date_value: Date in various formats

        Returns:
            Datetime object or None if parsing fails
        """
        if not date_value or date_value == "No date available":
            return None

        try:
            if isinstance(date_value, datetime):
                return date_value
            elif isinstance(date_value, str):
                return date_parser.parse(date_value)
            else:
                return None
        except Exception as e:
            logger.warning(f"Error parsing date '{date_value}': {e}")
            return None

    def score(self, item: Dict[str, Any]) -> float:
        """
        Calculate freshness score for an item.

        Args:
            item: Item to score

        Returns:
            Freshness score (0-100)
        """
        published_date = self.parse_date(item.get('published_date'))

        if not published_date:
            # No date available - assume medium freshness
            return 50.0

        now = datetime.now(published_date.tzinfo) if published_date.tzinfo else datetime.now()
        age = now - published_date

        # Score based on age:
        # 0-1 day: 100
        # 1-7 days: 90
        # 7-30 days: 70
        # 30-90 days: 50
        # >90 days: 30

        if age < timedelta(days=1):
            score = 100.0
        elif age < timedelta(days=7):
            score = 90.0
        elif age < timedelta(days=30):
            score = 70.0
        elif age < timedelta(days=90):
            score = 50.0
        else:
            score = 30.0

        logger.debug(f"Freshness score for '{item.get('title', '')[:50]}...': {score} (age: {age.days} days)")

        return score
