"""
Normalizer for standardizing data schema across different sources.
"""
from typing import Dict, Any, List
from datetime import datetime
from dateutil import parser as date_parser
from src.utils.logger import get_logger

logger = get_logger(__name__)


class Normalizer:
    """Standardize data schema across all sources."""

    REQUIRED_FIELDS = ['title', 'content', 'url', 'published_date', 'source']

    def __init__(self):
        """Initialize the normalizer."""
        pass

    def normalize_date(self, date_value: Any) -> str:
        """
        Normalize date to ISO format string.

        Args:
            date_value: Date in various formats (string, datetime, etc.)

        Returns:
            ISO format date string or default value
        """
        if not date_value:
            return "No date available"

        try:
            if isinstance(date_value, datetime):
                return date_value.isoformat()
            elif isinstance(date_value, str):
                parsed_date = date_parser.parse(date_value)
                return parsed_date.isoformat()
            else:
                return str(date_value)
        except Exception as e:
            logger.warning(f"Error parsing date '{date_value}': {e}")
            return "No date available"

    def normalize_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize a single item to standard schema.

        Args:
            item: Raw item dictionary

        Returns:
            Normalized item with all required fields
        """
        normalized = {}

        # Ensure all required fields exist
        normalized['title'] = item.get('title', 'Untitled')
        normalized['content'] = item.get('content') or item.get('summary') or item.get('description') or ""
        normalized['url'] = item.get('url') or item.get('link') or ""
        normalized['published_date'] = self.normalize_date(item.get('published_date') or item.get('published') or item.get('pubDate'))
        normalized['source'] = item.get('source', 'Unknown')

        # Preserve any extra fields
        for key, value in item.items():
            if key not in normalized:
                normalized[key] = value

        return normalized

    def normalize(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize a single item to standard schema.

        Args:
            item: Raw item dictionary

        Returns:
            Normalized item with all required fields
        """
        return self.normalize_item(item)

    def normalize_batch(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Normalize a list of items.

        Args:
            items: List of raw item dictionaries

        Returns:
            List of normalized items
        """
        normalized_items = []

        for item in items:
            if item is None:
                continue

            try:
                normalized_item = self.normalize_item(item)
                normalized_items.append(normalized_item)
            except Exception as e:
                logger.error(f"Error normalizing item: {e}")
                continue

        logger.info(f"Normalized {len(normalized_items)} items")
        return normalized_items
