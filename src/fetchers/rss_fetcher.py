"""RSS feed fetcher using feedparser."""

from typing import List, Dict, Any
from datetime import datetime
import feedparser

from .base_fetcher import BaseFetcher
from ..utils.logger import get_logger

logger = get_logger(__name__)


class RSSFetcher(BaseFetcher):
    """Fetcher for RSS/Atom feeds."""

    def fetch(self) -> List[Dict[str, Any]]:
        """
        Fetch and parse RSS feed.

        Returns:
            List of parsed feed items
        """
        feed_url = self.source_config.get('url')
        if not feed_url:
            logger.error(f"No URL provided for source: {self.source_name}")
            return []

        logger.info(f"Fetching RSS feed: {self.source_name} ({feed_url})")

        try:
            # Parse feed
            feed = feedparser.parse(feed_url)

            items = []
            for entry in feed.entries:
                item = self._parse_entry(entry)
                if item:
                    items.append(item)

            logger.info(f"Fetched {len(items)} items from {self.source_name}")
            return items

        except Exception as e:
            logger.error(f"Failed to fetch RSS feed {self.source_name}: {e}")
            return []

    def _parse_entry(self, entry: Any) -> Dict[str, Any]:
        """Parse a single feed entry."""
        try:
            # Extract published date
            pub_date = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                pub_date = datetime(*entry.published_parsed[:6]).isoformat()
            elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                pub_date = datetime(*entry.updated_parsed[:6]).isoformat()

            return {
                'title': entry.get('title', 'Untitled'),
                'url': entry.get('link', ''),
                'content': entry.get('summary', ''),
                'pub_date': pub_date,
                'source': self.source_name,
                'source_url': self.source_config.get('url'),
                'authors': [author.get('name', 'Unknown') for author in entry.get('authors', [])],
                'fetched_date': datetime.now().isoformat()
            }
        except Exception as e:
            logger.warning(f"Failed to parse entry: {e}")
            return None
