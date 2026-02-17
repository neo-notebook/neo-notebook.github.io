"""
Safe prompt templates for LLM summarization.
"""
from typing import Dict, Any


class PromptTemplates:
    """Prompt templates for generating grounded summaries."""

    @staticmethod
    def summarize_article(title: str, content: str, source: str) -> str:
        """
        Generate prompt for article summarization.

        Args:
            title: Article title
            content: Article content
            source: Article source

        Returns:
            Formatted prompt
        """
        # Truncate content if too long (keep first 2000 chars)
        truncated_content = content[:2000] if len(content) > 2000 else content

        return f"""You are summarizing an AI security article for cybersecurity professionals.

Article Title: {title}
Source: {source}
Content: {truncated_content}

Provide a JSON response with exactly these three fields:

1. "summary": 1-2 sentence summary of the article (grounded in the content above)
2. "why_it_matters": 1 sentence explaining why this matters to enterprise defenders
3. "practical_mitigation": 1-2 actionable insights or mitigations (if applicable, otherwise "No specific mitigation provided")

IMPORTANT:
- Base your response ONLY on the content provided
- If details are unclear, say "Details limited"
- Do not hallucinate or add information not in the source
- Keep responses concise and practical

Respond ONLY with valid JSON in this format:
{{
  "summary": "...",
  "why_it_matters": "...",
  "practical_mitigation": "..."
}}"""

    @staticmethod
    def extract_key_points(content: str) -> str:
        """
        Generate prompt for extracting key points.

        Args:
            content: Article content

        Returns:
            Formatted prompt
        """
        truncated_content = content[:1500] if len(content) > 1500 else content

        return f"""Extract the most important points from this AI security content.

Content: {truncated_content}

List 3-5 key points as a JSON array of strings.

Respond ONLY with valid JSON in this format:
{{"key_points": ["point 1", "point 2", "point 3"]}}"""
