"""
Deduplicator for detecting duplicate articles.
"""
from typing import List, Dict, Any
from difflib import SequenceMatcher
from src.utils.logger import get_logger

logger = get_logger(__name__)


class Deduplicator:
    """Detect and remove duplicate articles."""

    def __init__(self, similarity_threshold: float = 0.8):
        """
        Initialize the deduplicator.

        Args:
            similarity_threshold: Minimum similarity ratio (0-1) to consider items duplicates
        """
        self.similarity_threshold = similarity_threshold

    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate similarity between two text strings.

        Args:
            text1: First text string
            text2: Second text string

        Returns:
            Similarity ratio between 0 and 1
        """
        if not text1 or not text2:
            return 0.0

        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()

    def are_duplicates(self, item1: Dict[str, Any], item2: Dict[str, Any]) -> bool:
        """
        Check if two items are duplicates.

        Args:
            item1: First item
            item2: Second item

        Returns:
            True if items are considered duplicates
        """
        # Exact title match
        title1 = item1.get('title', '').strip()
        title2 = item2.get('title', '').strip()

        if title1 and title2 and title1.lower() == title2.lower():
            return True

        # High content similarity (only for longer content to avoid false positives)
        content1 = item1.get('content', '')
        content2 = item2.get('content', '')

        # Require minimum content length to check similarity
        MIN_CONTENT_LENGTH = 50
        if content1 and content2 and len(content1) >= MIN_CONTENT_LENGTH and len(content2) >= MIN_CONTENT_LENGTH:
            similarity = self.calculate_similarity(content1, content2)
            if similarity >= self.similarity_threshold:
                return True

        return False

    def deduplicate(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Remove duplicates from a list of items.

        Args:
            items: List of items to deduplicate

        Returns:
            Dictionary with keys:
            - unique_count: Number of unique items
            - unique_items: List of unique items (first occurrence of each duplicate group)
            - duplicate_groups: List of lists, each containing duplicate items
        """
        if not items:
            return {
                'unique_count': 0,
                'unique_items': [],
                'duplicate_groups': []
            }

        unique_items = []
        duplicate_groups = []
        processed_indices = set()

        for i, item in enumerate(items):
            if i in processed_indices:
                continue

            # Find all duplicates of this item
            duplicates = [item]
            processed_indices.add(i)

            for j in range(i + 1, len(items)):
                if j in processed_indices:
                    continue

                if self.are_duplicates(item, items[j]):
                    duplicates.append(items[j])
                    processed_indices.add(j)

            # Add to unique items (first occurrence)
            unique_items.append(item)

            # If there were duplicates, add to duplicate groups
            if len(duplicates) > 1:
                duplicate_groups.append(duplicates)

        logger.info(f"Deduplication: {len(items)} items → {len(unique_items)} unique ({len(items) - len(unique_items)} duplicates removed)")

        return {
            'unique_count': len(unique_items),
            'unique_items': unique_items,
            'duplicate_groups': duplicate_groups
        }
