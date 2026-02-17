"""
Fallback summarizer using metadata extraction when LLM is unavailable.
"""
from typing import Dict, Any
from src.utils.logger import get_logger

logger = get_logger(__name__)


class FallbackSummarizer:
    """Conservative metadata-based summarization when LLM unavailable."""

    def __init__(self):
        """Initialize fallback summarizer."""
        pass

    def _extract_first_sentences(self, text: str, num_sentences: int = 2) -> str:
        """
        Extract first N sentences from text.

        Args:
            text: Text to extract from
            num_sentences: Number of sentences to extract

        Returns:
            First N sentences
        """
        if not text:
            return "No content available"

        # Simple sentence splitting (not perfect but works for basic cases)
        sentences = []
        current = ""

        for char in text:
            current += char
            if char in '.!?' and len(current) > 20:
                sentences.append(current.strip())
                current = ""
                if len(sentences) >= num_sentences:
                    break

        if sentences:
            return ' '.join(sentences)
        else:
            # If no sentence breaks found, return first 200 chars
            return text[:200] + "..." if len(text) > 200 else text

    def summarize(self, item: Dict[str, Any]) -> Dict[str, str]:
        """
        Generate conservative summary from metadata.

        Args:
            item: Item to summarize

        Returns:
            Dictionary with summary, why_it_matters, practical_mitigation
        """
        title = item.get('title', 'Untitled')
        content = item.get('content', '')
        source = item.get('source', 'Unknown')

        # Summary: first 2 sentences from content
        summary = self._extract_first_sentences(content, 2)

        # Why it matters: generic based on title/source
        why_it_matters = f"AI security update from {source}"

        # Practical mitigation: conservative default
        practical_mitigation = "Details limited - review full article for mitigation guidance"

        result = {
            'summary': summary,
            'why_it_matters': why_it_matters,
            'practical_mitigation': practical_mitigation
        }

        logger.info(f"Fallback summarization for: {title[:50]}...")

        return result
