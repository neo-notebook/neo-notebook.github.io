"""Base class for content fetchers."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any

from ..utils.logger import get_logger

logger = get_logger(__name__)


class BaseFetcher(ABC):
    """Abstract base class for content fetchers."""

    def __init__(self, source_config: Dict[str, Any] = None):
        """
        Initialize fetcher.

        Args:
            source_config: Source configuration dict
        """
        self.source_config = source_config or {}
        self.source_name = self.source_config.get('name', 'Unknown')

    @abstractmethod
    def fetch(self) -> List[Dict[str, Any]]:
        """
        Fetch content from source.

        Returns:
            List of raw content items (dicts with: url, title, content, pub_date, etc.)
        """
        pass
