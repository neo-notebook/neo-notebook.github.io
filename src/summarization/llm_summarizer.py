"""
LLM-based summarizer using Ollama API.
"""
import json
from typing import Dict, Any, Optional
import requests
from src.utils.logger import get_logger
from src.summarization.prompt_templates import PromptTemplates

logger = get_logger(__name__)


class LLMSummarizer:
    """Summarize articles using local Ollama LLM."""

    def __init__(self,
                 ollama_url: str = "http://localhost:11434",
                 model: str = "llama3.2",
                 timeout: int = 30):
        """
        Initialize LLM summarizer.

        Args:
            ollama_url: Ollama API base URL
            model: Model name to use
            timeout: Request timeout in seconds
        """
        self.ollama_url = ollama_url
        self.model = model
        self.timeout = timeout
        self.prompt_templates = PromptTemplates()

    def is_available(self) -> bool:
        """
        Check if Ollama is available.

        Returns:
            True if Ollama is running and accessible
        """
        try:
            response = requests.get(
                f"{self.ollama_url}/api/tags",
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            logger.debug(f"Ollama not available: {e}")
            return False

    def _call_ollama(self, prompt: str) -> Optional[str]:
        """
        Call Ollama API with prompt.

        Args:
            prompt: Prompt to send

        Returns:
            Response text or None if failed
        """
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=self.timeout
            )

            if response.status_code == 200:
                result = response.json()
                return result.get('response', '')
            else:
                logger.error(f"Ollama API error: {response.status_code}")
                return None

        except Exception as e:
            logger.error(f"Error calling Ollama: {e}")
            return None

    def _parse_json_response(self, response: str) -> Optional[Dict[str, str]]:
        """
        Parse JSON response from LLM.

        Args:
            response: Raw LLM response

        Returns:
            Parsed dictionary or None if failed
        """
        try:
            # Try to find JSON in response (might have extra text)
            start = response.find('{')
            end = response.rfind('}') + 1

            if start >= 0 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
            else:
                logger.warning("No JSON found in LLM response")
                return None

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {e}")
            return None

    def summarize(self, item: Dict[str, Any]) -> Optional[Dict[str, str]]:
        """
        Summarize article using LLM.

        Args:
            item: Item to summarize

        Returns:
            Dictionary with summary, why_it_matters, practical_mitigation
            or None if summarization failed
        """
        title = item.get('title', 'Untitled')
        content = item.get('content', '')
        source = item.get('source', 'Unknown')

        # Generate prompt
        prompt = self.prompt_templates.summarize_article(title, content, source)

        # Call Ollama
        response = self._call_ollama(prompt)

        if not response:
            logger.warning(f"LLM summarization failed for: {title[:50]}...")
            return None

        # Parse response
        parsed = self._parse_json_response(response)

        if not parsed:
            logger.warning(f"Failed to parse LLM response for: {title[:50]}...")
            return None

        # Validate required fields
        required_fields = ['summary', 'why_it_matters', 'practical_mitigation']
        if all(field in parsed for field in required_fields):
            logger.info(f"LLM summarization successful for: {title[:50]}...")
            return parsed
        else:
            logger.warning(f"LLM response missing required fields for: {title[:50]}...")
            return None
