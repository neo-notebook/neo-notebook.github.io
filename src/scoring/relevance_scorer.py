"""
Relevance scorer for topical match to priority areas.
"""
from typing import Dict, Any, List
from src.config import Config
from src.utils.logger import get_logger

logger = get_logger(__name__)


class RelevanceScorer:
    """Score items based on topical relevance to priority areas."""

    def __init__(self, config: Config = None):
        """
        Initialize relevance scorer.

        Args:
            config: Configuration object (loads from file if not provided)
        """
        self.config = config or Config()
        self.keywords = self._load_keywords()

    def _load_keywords(self) -> Dict[str, List[str]]:
        """
        Load relevance keywords from configuration.

        Returns:
            Dictionary mapping topics to keyword lists
        """
        try:
            # Config class provides relevance_keywords property
            high_priority = self.config.relevance_keywords

            # Extract keywords from nested structure
            keywords = {}
            for topic, config in high_priority.items():
                if isinstance(config, dict) and 'keywords' in config:
                    keywords[topic] = config['keywords']

            return keywords if keywords else self._default_keywords()
        except Exception as e:
            logger.error(f"Error loading relevance keywords: {e}")
            return self._default_keywords()

    def _default_keywords(self) -> Dict[str, List[str]]:
        """Return default keywords if config loading fails."""
        return {
            'agentic': ['agent', 'agentic', 'tool calling'],
            'prompt_injection': ['prompt injection', 'jailbreak'],
            'hitl': ['human-in-the-loop', 'HITL', 'kill switch'],
            'observability': ['observability', 'tracing', 'audit'],
            'shadow_ai': ['shadow AI', 'governance']
        }

    def count_keyword_matches(self, text: str) -> int:
        """
        Count keyword matches in text.

        Args:
            text: Text to search

        Returns:
            Number of keyword matches found
        """
        text_lower = text.lower()
        match_count = 0

        for topic, keyword_list in self.keywords.items():
            for keyword in keyword_list:
                if keyword.lower() in text_lower:
                    match_count += 1

        return match_count

    def score(self, item: Dict[str, Any]) -> float:
        """
        Calculate relevance score for an item.

        Args:
            item: Item to score

        Returns:
            Relevance score (0-100)
        """
        title = item.get('title', '')
        content = item.get('content', '')
        text = f"{title} {content}"

        # Count keyword matches
        matches = self.count_keyword_matches(text)

        # Convert to 0-100 scale
        # Cap at 10 matches for a perfect score
        score = min(matches * 10, 100)

        logger.debug(f"Relevance score for '{title[:50]}...': {score} ({matches} keyword matches)")

        return float(score)
