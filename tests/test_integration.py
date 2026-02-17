"""
Integration tests for complete pipeline.
"""
import pytest
import tempfile
import json
from pathlib import Path
from unittest.mock import Mock, patch
from src.main import main


class TestPipelineIntegration:
    """End-to-end pipeline tests."""

    @patch('src.fetchers.rss_fetcher.feedparser.parse')
    def test_complete_daily_pipeline(self, mock_parse):
        """Test complete daily pipeline with mocked feed."""
        # Mock RSS feed response
        mock_parse.return_value = Mock(
            entries=[
                Mock(
                    title='Test AI Security Article',
                    link='https://example.com/article1',
                    summary='This article discusses prompt injection attacks.',
                    published_parsed=(2024, 1, 15, 10, 0, 0, 0, 0, 0)
                )
            ]
        )

        # Run pipeline
        result = main('daily')

        # Verify pipeline completed
        assert result['mode'] == 'daily'
        assert result['items_fetched'] >= 0
        assert 'elapsed_seconds' in result

        # Verify outputs created
        brief_file = Path('docs/public/data/brief_today.json')
        assert brief_file.exists()

        with open(brief_file) as f:
            brief_data = json.load(f)
        assert 'generated_at' in brief_data
        assert 'items' in brief_data

    def test_pipeline_handles_no_items(self):
        """Test pipeline gracefully handles empty feed."""
        # Run pipeline (example feeds return 0 items)
        result = main('daily')

        assert result['items_fetched'] == 0
        assert result['items_processed'] == 0
        assert result['items_unique'] == 0

    @patch('src.fetchers.rss_fetcher.feedparser.parse')
    def test_pipeline_processes_multiple_sources(self, mock_parse):
        """Test pipeline handles multiple sources."""
        # Mock RSS responses
        mock_parse.return_value = Mock(
            entries=[
                Mock(
                    title=f'Article from source',
                    link='https://example.com/article',
                    summary='Security content.',
                    published_parsed=(2024, 1, 15, 10, 0, 0, 0, 0, 0)
                )
            ]
        )

        result = main('daily')

        # Should process items from all enabled sources
        assert result['items_fetched'] >= 0


class TestComponentIntegration:
    """Tests for component integration."""

    def test_processor_to_scorer_integration(self):
        """Test processors output works with scorers."""
        from src.processors.parser import Parser
        from src.processors.normalizer import Normalizer
        from src.scoring.relevance_scorer import RelevanceScorer

        # Process an item
        parser = Parser()
        normalizer = Normalizer()

        item = {
            'title': 'AI Agent Security',
            'content': '<p>This discusses agentic systems and prompt injection.</p>',
            'source': 'Test'
        }

        # Parse
        item['content'] = parser.parse(item['content'])

        # Normalize
        normalized = normalizer.normalize(item)

        # Score
        scorer = RelevanceScorer()
        score = scorer.score(normalized)

        # Should get non-zero relevance score
        assert score > 0

    def test_scorer_to_summarizer_integration(self):
        """Test scorers output works with summarizers."""
        from src.scoring.relevance_scorer import RelevanceScorer
        from src.summarization.fallback_summarizer import FallbackSummarizer

        item = {
            'title': 'Test Article',
            'content': 'Article content about AI security.',
            'source': 'Test'
        }

        # Score
        scorer = RelevanceScorer()
        item['relevance_score'] = scorer.score(item)

        # Summarize
        summarizer = FallbackSummarizer()
        summary = summarizer.summarize(item)

        assert 'summary' in summary
        assert 'why_it_matters' in summary
        assert 'practical_mitigation' in summary
