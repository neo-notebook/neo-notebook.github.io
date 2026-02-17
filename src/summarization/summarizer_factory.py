"""
Summarizer factory for dispatching to LLM or fallback.
"""
from typing import Dict, Any, List
from src.utils.logger import get_logger
from src.summarization.llm_summarizer import LLMSummarizer
from src.summarization.fallback_summarizer import FallbackSummarizer

logger = get_logger(__name__)


class SummarizerFactory:
    """Factory for creating and dispatching summarizers."""

    def __init__(self,
                 ollama_url: str = "http://localhost:11434",
                 model: str = "llama3.2",
                 prefer_llm: bool = True):
        """
        Initialize summarizer factory.

        Args:
            ollama_url: Ollama API URL
            model: Model to use
            prefer_llm: Try LLM first if available
        """
        self.prefer_llm = prefer_llm
        self.llm_summarizer = LLMSummarizer(ollama_url, model)
        self.fallback_summarizer = FallbackSummarizer()

        # Check LLM availability at init
        self.llm_available = self.llm_summarizer.is_available()

        if self.llm_available:
            logger.info(f"LLM summarization available (model: {model})")
        else:
            logger.warning("LLM not available - using fallback summarization")

    def summarize(self, item: Dict[str, Any]) -> Dict[str, str]:
        """
        Summarize an item using best available method.

        Args:
            item: Item to summarize

        Returns:
            Dictionary with summary fields
        """
        # Try LLM if preferred and available
        if self.prefer_llm and self.llm_available:
            result = self.llm_summarizer.summarize(item)
            if result:
                return result
            else:
                logger.info("LLM summarization failed, falling back to metadata extraction")

        # Use fallback
        return self.fallback_summarizer.summarize(item)

    def summarize_batch(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Summarize multiple items.

        Args:
            items: List of items to summarize

        Returns:
            List of items with added summary fields
        """
        summarized_items = []

        for item in items:
            try:
                summary = self.summarize(item)

                # Add summary fields to item
                item['summary'] = summary.get('summary', '')
                item['why_it_matters'] = summary.get('why_it_matters', '')
                item['practical_mitigation'] = summary.get('practical_mitigation', '')

                summarized_items.append(item)

            except Exception as e:
                logger.error(f"Error summarizing item: {e}")
                # Add item without summary
                item['summary'] = "Summarization failed"
                item['why_it_matters'] = "N/A"
                item['practical_mitigation'] = "N/A"
                summarized_items.append(item)

        logger.info(f"Summarized {len(summarized_items)} items")

        return summarized_items
