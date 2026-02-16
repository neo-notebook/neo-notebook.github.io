"""
HTML/XML parser for extracting clean text from web content.
"""
from typing import Optional
from bs4 import BeautifulSoup
from src.utils.logger import get_logger

logger = get_logger(__name__)


class Parser:
    """Parse HTML/XML content and extract clean text."""

    def __init__(self):
        """Initialize the parser."""
        pass

    def parse_html(self, html_content: str) -> str:
        """
        Extract clean text from HTML content.

        Args:
            html_content: Raw HTML string

        Returns:
            Clean text with HTML tags removed
        """
        if not html_content:
            return ""

        try:
            soup = BeautifulSoup(html_content, 'html.parser')

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Get text and clean up whitespace
            text = soup.get_text(separator=' ', strip=True)

            # Collapse multiple spaces
            text = ' '.join(text.split())

            return text
        except Exception as e:
            logger.error(f"Error parsing HTML: {e}")
            return html_content  # Return original if parsing fails

    def parse(self, content: str, content_type: Optional[str] = None) -> str:
        """
        Parse content based on type.

        Args:
            content: Raw content string
            content_type: Content type hint (e.g., 'html', 'xml')

        Returns:
            Clean text
        """
        if not content:
            return ""

        # Default to HTML parsing
        if content_type in [None, 'html', 'xml']:
            return self.parse_html(content)

        # For plain text, just return as-is
        return content
