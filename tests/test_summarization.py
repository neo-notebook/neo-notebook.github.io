"""
Tests for summarization module.
"""
import pytest
from unittest.mock import Mock, patch
from src.summarization.fallback_summarizer import FallbackSummarizer
from src.summarization.llm_summarizer import LLMSummarizer
from src.summarization.summarizer_factory import SummarizerFactory
from src.summarization.prompt_templates import PromptTemplates


class TestFallbackSummarizer:
    """Tests for fallback summarizer."""

    def test_summarizes_with_metadata(self):
        """Test that fallback summarizer creates conservative summaries."""
        summarizer = FallbackSummarizer()
        item = {
            'title': 'Test Article',
            'content': 'This is a test article about AI security. It discusses various topics.',
            'source': 'TestSource'
        }

        result = summarizer.summarize(item)

        assert 'summary' in result
        assert 'why_it_matters' in result
        assert 'practical_mitigation' in result
        assert len(result['summary']) > 0

    def test_handles_empty_content(self):
        """Test handling of empty content."""
        summarizer = FallbackSummarizer()
        item = {'title': 'Empty', 'content': '', 'source': 'Test'}

        result = summarizer.summarize(item)

        assert result['summary'] == 'No content available'

    def test_extracts_first_sentences(self):
        """Test sentence extraction."""
        summarizer = FallbackSummarizer()
        text = "First sentence here. Second sentence here. Third sentence here."

        result = summarizer._extract_first_sentences(text, 2)

        assert "First sentence" in result
        assert "Second sentence" in result


class TestLLMSummarizer:
    """Tests for LLM summarizer."""

    def test_is_available_checks_connection(self):
        """Test LLM availability check."""
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200

            summarizer = LLMSummarizer()
            assert summarizer.is_available() is True

    def test_is_available_handles_connection_error(self):
        """Test LLM availability when connection fails."""
        with patch('requests.get') as mock_get:
            mock_get.side_effect = Exception("Connection failed")

            summarizer = LLMSummarizer()
            assert summarizer.is_available() is False

    def test_parses_json_response(self):
        """Test JSON parsing from LLM response."""
        summarizer = LLMSummarizer()
        response = '''Here is the summary:
        {
          "summary": "Test summary",
          "why_it_matters": "Test matters",
          "practical_mitigation": "Test mitigation"
        }
        '''

        result = summarizer._parse_json_response(response)

        assert result is not None
        assert result['summary'] == 'Test summary'
        assert result['why_it_matters'] == 'Test matters'

    def test_handles_malformed_json(self):
        """Test handling of malformed JSON."""
        summarizer = LLMSummarizer()
        response = "This is not valid JSON"

        result = summarizer._parse_json_response(response)

        assert result is None

    @patch('requests.post')
    def test_summarize_with_valid_response(self, mock_post):
        """Test successful summarization."""
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            'response': '{"summary": "Test", "why_it_matters": "Important", "practical_mitigation": "Patch"}'
        }

        summarizer = LLMSummarizer()
        item = {
            'title': 'Test Article',
            'content': 'Content here',
            'source': 'TestSource'
        }

        result = summarizer.summarize(item)

        assert result is not None
        assert result['summary'] == 'Test'
        assert result['why_it_matters'] == 'Important'
        assert result['practical_mitigation'] == 'Patch'

    @patch('requests.post')
    def test_summarize_handles_api_error(self, mock_post):
        """Test handling of API errors."""
        mock_post.return_value.status_code = 500

        summarizer = LLMSummarizer()
        item = {'title': 'Test', 'content': 'Content', 'source': 'Test'}

        result = summarizer.summarize(item)

        assert result is None


class TestSummarizerFactory:
    """Tests for summarizer factory."""

    @patch('src.summarization.llm_summarizer.LLMSummarizer.is_available')
    @patch('src.summarization.llm_summarizer.LLMSummarizer.summarize')
    def test_uses_llm_when_available(self, mock_summarize, mock_available):
        """Test that factory uses LLM when available."""
        mock_available.return_value = True
        mock_summarize.return_value = {
            'summary': 'LLM summary',
            'why_it_matters': 'LLM matters',
            'practical_mitigation': 'LLM mitigation'
        }

        factory = SummarizerFactory(prefer_llm=True)
        item = {'title': 'Test', 'content': 'Content', 'source': 'Test'}

        result = factory.summarize(item)

        assert result['summary'] == 'LLM summary'
        mock_summarize.assert_called_once()

    @patch('src.summarization.llm_summarizer.LLMSummarizer.is_available')
    def test_uses_fallback_when_llm_unavailable(self, mock_available):
        """Test that factory uses fallback when LLM unavailable."""
        mock_available.return_value = False

        factory = SummarizerFactory(prefer_llm=True)
        item = {'title': 'Test', 'content': 'Test content here.', 'source': 'Test'}

        result = factory.summarize(item)

        # Should get fallback summary
        assert 'summary' in result
        assert result['summary'] != 'LLM summary'

    @patch('src.summarization.llm_summarizer.LLMSummarizer.is_available')
    @patch('src.summarization.llm_summarizer.LLMSummarizer.summarize')
    def test_falls_back_when_llm_fails(self, mock_summarize, mock_available):
        """Test fallback when LLM summarization fails."""
        mock_available.return_value = True
        mock_summarize.return_value = None  # LLM failed

        factory = SummarizerFactory(prefer_llm=True)
        item = {'title': 'Test', 'content': 'Test content.', 'source': 'Test'}

        result = factory.summarize(item)

        # Should get fallback summary
        assert 'summary' in result

    @patch('src.summarization.llm_summarizer.LLMSummarizer.is_available')
    def test_summarize_batch(self, mock_available):
        """Test batch summarization."""
        mock_available.return_value = False

        factory = SummarizerFactory(prefer_llm=False)
        items = [
            {'title': 'Item 1', 'content': 'Content 1.', 'source': 'Test'},
            {'title': 'Item 2', 'content': 'Content 2.', 'source': 'Test'}
        ]

        results = factory.summarize_batch(items)

        assert len(results) == 2
        assert 'summary' in results[0]
        assert 'summary' in results[1]


class TestPromptTemplates:
    """Tests for prompt templates."""

    def test_summarize_article_prompt(self):
        """Test article summarization prompt."""
        prompt = PromptTemplates.summarize_article(
            title="Test Article",
            content="Test content",
            source="TestSource"
        )

        assert "Test Article" in prompt
        assert "TestSource" in prompt
        assert "JSON" in prompt

    def test_truncates_long_content(self):
        """Test that long content is truncated."""
        long_content = "x" * 5000
        prompt = PromptTemplates.summarize_article(
            title="Test",
            content=long_content,
            source="Test"
        )

        # Should be truncated
        assert len(prompt) < len(long_content)
