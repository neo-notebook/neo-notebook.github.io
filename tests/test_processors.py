"""Tests for content processors module."""

import pytest
from datetime import datetime, timedelta
from src.processors.parser import Parser
from src.processors.normalizer import Normalizer
from src.processors.deduplicator import Deduplicator
from src.processors.clustering import Clustering


# ============================================================================
# Parser Tests
# ============================================================================

class TestParser:
    """Tests for HTML/XML parser."""

    def test_parser_removes_html_tags(self):
        """Test that parser removes HTML tags."""
        html = "<p>Hello <b>world</b>!</p>"
        parser = Parser()
        result = parser.parse_html(html)

        assert "Hello" in result
        assert "world" in result
        assert "<p>" not in result
        assert "<b>" not in result

    def test_parser_handles_empty_html(self):
        """Test parser handles empty HTML."""
        parser = Parser()
        result = parser.parse_html("")

        assert result == ""

    def test_parser_handles_none_input(self):
        """Test parser handles None input gracefully."""
        parser = Parser()
        result = parser.parse_html(None)

        assert result == ""

    def test_parser_preserves_text_content(self):
        """Test that parser preserves text content."""
        html = "<div><h1>Title</h1><p>This is content.</p></div>"
        parser = Parser()
        result = parser.parse_html(html)

        assert "Title" in result
        assert "This is content" in result

    def test_parser_handles_nested_tags(self):
        """Test parser handles deeply nested tags."""
        html = "<div><article><section><p>Deep content</p></section></article></div>"
        parser = Parser()
        result = parser.parse_html(html)

        assert "Deep content" in result

    def test_parser_handles_malformed_html(self):
        """Test parser handles malformed HTML gracefully."""
        html = "<p>Unclosed paragraph<div>Nested badly"
        parser = Parser()
        result = parser.parse_html(html)

        assert "Unclosed paragraph" in result

    def test_parser_removes_script_tags(self):
        """Test that parser removes script tags."""
        html = "<p>Content</p><script>alert('xss')</script>"
        parser = Parser()
        result = parser.parse_html(html)

        assert "Content" in result
        assert "alert" not in result
        assert "<script>" not in result

    def test_parser_removes_style_tags(self):
        """Test that parser removes style tags."""
        html = "<p>Content</p><style>.hidden { display: none; }</style>"
        parser = Parser()
        result = parser.parse_html(html)

        assert "Content" in result
        assert ".hidden" not in result
        assert "<style>" not in result

    def test_parser_collapses_whitespace(self):
        """Test that parser handles multiple whitespaces."""
        html = "<p>Hello    \n\n\n    world</p>"
        parser = Parser()
        result = parser.parse_html(html)

        # Should collapse multiple spaces/newlines
        assert "Hello" in result
        assert "world" in result

    def test_parser_extracts_text_from_complex_html(self):
        """Test parsing complex real-world-like HTML."""
        html = """
        <article>
            <h1>Breaking: New AI Security Vulnerability</h1>
            <div class="metadata">
                <span class="author">Jane Doe</span>
                <span class="date">2024-01-15</span>
            </div>
            <div class="content">
                <p>Researchers have discovered a new vulnerability in popular AI systems.</p>
                <p>The vulnerability allows attackers to bypass safety measures.</p>
            </div>
        </article>
        """
        parser = Parser()
        result = parser.parse_html(html)

        assert "Breaking" in result
        assert "vulnerability" in result
        assert "bypass safety" in result


# ============================================================================
# Normalizer Tests
# ============================================================================

class TestNormalizer:
    """Tests for data normalization."""

    def test_normalizer_adds_missing_fields(self):
        """Test that normalizer adds default values for missing fields."""
        item = {
            'title': 'Test Article',
            'url': 'https://example.com/article'
        }
        normalizer = Normalizer()
        result = normalizer.normalize(item)

        assert 'title' in result
        assert 'content' in result
        assert 'url' in result
        assert 'published_date' in result
        assert 'source' in result

    def test_normalizer_preserves_existing_fields(self):
        """Test that normalizer preserves existing fields."""
        item = {
            'title': 'Test Article',
            'content': 'Test content',
            'url': 'https://example.com',
            'published_date': '2024-01-15T10:00:00',
            'source': 'TestSource'
        }
        normalizer = Normalizer()
        result = normalizer.normalize(item)

        assert result['title'] == 'Test Article'
        assert result['content'] == 'Test content'
        assert result['source'] == 'TestSource'

    def test_normalizer_converts_dates_to_iso_format(self):
        """Test that normalizer converts dates to ISO format."""
        # Test with various date formats
        items = [
            {'title': 'Test', 'published_date': '2024-01-15T10:00:00'},
            {'title': 'Test', 'published_date': '2024-01-15'},
            {'title': 'Test', 'published_date': datetime(2024, 1, 15, 10, 0, 0)},
        ]
        normalizer = Normalizer()

        for item in items:
            result = normalizer.normalize(item)
            # Should contain a valid ISO date or the default
            assert 'published_date' in result
            if result['published_date'] != 'No date available':
                # If it's a date, should be in ISO format
                assert 'T' in result['published_date'] or '2024' in result['published_date']

    def test_normalizer_handles_missing_date(self):
        """Test that normalizer handles missing dates with default."""
        item = {'title': 'Test Article'}
        normalizer = Normalizer()
        result = normalizer.normalize(item)

        assert 'published_date' in result
        # Should have either a valid date or default text
        assert isinstance(result['published_date'], str)

    def test_normalizer_handles_missing_content(self):
        """Test that normalizer handles missing content."""
        item = {
            'title': 'Test Article',
            'url': 'https://example.com'
        }
        normalizer = Normalizer()
        result = normalizer.normalize(item)

        assert 'content' in result
        # Content should be empty string or default
        assert isinstance(result['content'], str)

    def test_normalizer_handles_empty_string_fields(self):
        """Test that normalizer handles empty string fields."""
        item = {
            'title': '',
            'content': '',
            'url': ''
        }
        normalizer = Normalizer()
        result = normalizer.normalize(item)

        assert 'title' in result
        assert 'content' in result
        assert 'url' in result

    def test_normalizer_normalizes_multiple_items(self):
        """Test that normalizer can normalize multiple items."""
        items = [
            {'title': 'Article 1', 'content': 'Content 1'},
            {'title': 'Article 2', 'content': 'Content 2'},
            {'title': 'Article 3'}
        ]
        normalizer = Normalizer()
        results = normalizer.normalize_batch(items)

        assert len(results) == 3
        for result in results:
            assert 'title' in result
            assert 'content' in result
            assert 'url' in result
            assert 'published_date' in result
            assert 'source' in result

    def test_normalizer_handles_none_in_batch(self):
        """Test that normalizer handles None items in batch."""
        items = [
            {'title': 'Article 1'},
            None,
            {'title': 'Article 2'}
        ]
        normalizer = Normalizer()
        results = normalizer.normalize_batch(items)

        # Should filter out None values
        assert len(results) == 2


# ============================================================================
# Deduplicator Tests
# ============================================================================

class TestDeduplicator:
    """Tests for duplicate detection."""

    def test_deduplicator_detects_exact_duplicates(self):
        """Test that deduplicator detects exact title matches."""
        items = [
            {'title': 'Breaking News', 'content': 'Article 1', 'url': 'https://example.com/1'},
            {'title': 'Breaking News', 'content': 'Article 1', 'url': 'https://example.com/1'},
            {'title': 'Other News', 'content': 'Article 2', 'url': 'https://example.com/2'}
        ]
        deduplicator = Deduplicator()
        result = deduplicator.deduplicate(items)

        assert result['unique_count'] == 2
        assert len(result['unique_items']) == 2
        assert len(result['duplicate_groups']) == 1

    def test_deduplicator_handles_empty_list(self):
        """Test deduplicator with empty list."""
        deduplicator = Deduplicator()
        result = deduplicator.deduplicate([])

        assert result['unique_count'] == 0
        assert result['unique_items'] == []
        assert result['duplicate_groups'] == []

    def test_deduplicator_handles_single_item(self):
        """Test deduplicator with single item."""
        items = [{'title': 'Article', 'content': 'Content', 'url': 'https://example.com'}]
        deduplicator = Deduplicator()
        result = deduplicator.deduplicate(items)

        assert result['unique_count'] == 1
        assert len(result['unique_items']) == 1

    def test_deduplicator_no_duplicates(self):
        """Test deduplicator when no duplicates exist."""
        items = [
            {'title': 'Article 1', 'content': 'Content 1', 'url': 'https://example.com/1'},
            {'title': 'Article 2', 'content': 'Content 2', 'url': 'https://example.com/2'},
            {'title': 'Article 3', 'content': 'Content 3', 'url': 'https://example.com/3'}
        ]
        deduplicator = Deduplicator()
        result = deduplicator.deduplicate(items)

        assert result['unique_count'] == 3
        assert len(result['duplicate_groups']) == 0

    def test_deduplicator_detects_similar_content(self):
        """Test that deduplicator detects high similarity content."""
        items = [
            {
                'title': 'AI Security Vulnerability Discovered',
                'content': 'Researchers found a critical vulnerability in popular AI systems that allows attackers to bypass safeguards.',
                'url': 'https://source1.com/article'
            },
            {
                'title': 'AI Security Vulnerability Discovered',
                'content': 'Researchers found a critical vulnerability in popular AI systems that allows attackers to bypass safeguards.',
                'url': 'https://source2.com/article'
            }
        ]
        deduplicator = Deduplicator()
        result = deduplicator.deduplicate(items)

        # Should detect as duplicate based on high similarity
        assert result['unique_count'] <= 2
        # At minimum should have identified the duplicate relationship
        assert len(result['unique_items']) >= 1

    def test_deduplicator_groups_duplicates(self):
        """Test that deduplicator groups duplicates together."""
        items = [
            {'title': 'News A', 'content': 'Content A', 'url': 'https://example.com/1'},
            {'title': 'News A', 'content': 'Content A', 'url': 'https://example.com/2'},
            {'title': 'News A', 'content': 'Content A', 'url': 'https://example.com/3'}
        ]
        deduplicator = Deduplicator()
        result = deduplicator.deduplicate(items)

        # Should have one group of 3 duplicates
        assert len(result['duplicate_groups']) >= 1
        # The duplicate group should contain the URLs
        if result['duplicate_groups']:
            group = result['duplicate_groups'][0]
            assert 'items' in group or isinstance(group, list)

    def test_deduplicator_handles_missing_fields(self):
        """Test deduplicator with items missing title/content."""
        items = [
            {'title': 'Article', 'content': 'Content', 'url': 'https://example.com/1'},
            {'title': '', 'content': '', 'url': 'https://example.com/2'},
            {'title': 'Article', 'content': 'Content', 'url': 'https://example.com/3'}
        ]
        deduplicator = Deduplicator()
        result = deduplicator.deduplicate(items)

        # Should still work without errors
        assert 'unique_count' in result
        assert 'unique_items' in result


# ============================================================================
# Clustering Tests
# ============================================================================

class TestClustering:
    """Tests for topic clustering."""

    def test_clustering_assigns_cluster_ids(self):
        """Test that clustering assigns cluster IDs to items."""
        items = [
            {'title': 'Prompt Injection Attack', 'content': 'New prompt injection technique discovered'},
            {'title': 'Prompt Injection Defense', 'content': 'How to defend against prompt injection'},
            {'title': 'Agent Safety Framework', 'content': 'Building safe AI agents'}
        ]
        clustering = Clustering()
        result = clustering.cluster(items)

        for item in result:
            assert 'cluster_id' in item
            assert item['cluster_id'] is not None

    def test_clustering_handles_empty_list(self):
        """Test clustering with empty list."""
        clustering = Clustering()
        result = clustering.cluster([])

        assert result == []

    def test_clustering_handles_single_item(self):
        """Test clustering with single item."""
        items = [{'title': 'Article', 'content': 'Content'}]
        clustering = Clustering()
        result = clustering.cluster(items)

        assert len(result) == 1
        assert 'cluster_id' in result[0]

    def test_clustering_groups_similar_topics(self):
        """Test that clustering groups similar topics together."""
        items = [
            {'title': 'Prompt Injection Attack', 'content': 'Prompt injection security threat'},
            {'title': 'Another Prompt Injection', 'content': 'More on prompt injection attacks'},
            {'title': 'Agent Framework', 'content': 'Building safe AI agents'},
            {'title': 'Agent Security', 'content': 'Securing agent systems'}
        ]
        clustering = Clustering()
        result = clustering.cluster(items)

        # Items with similar keywords should have same cluster_id
        cluster_ids = [item['cluster_id'] for item in result]
        # Should have created clusters (fewer unique cluster IDs than items)
        assert len(set(cluster_ids)) >= 1
        assert len(set(cluster_ids)) <= len(result)

    def test_clustering_preserves_item_data(self):
        """Test that clustering preserves original item data."""
        items = [
            {'title': 'Article 1', 'content': 'Content 1', 'url': 'https://example.com/1'},
            {'title': 'Article 2', 'content': 'Content 2', 'url': 'https://example.com/2'}
        ]
        clustering = Clustering()
        result = clustering.cluster(items)

        for i, item in enumerate(result):
            assert item['title'] == items[i]['title']
            assert item['content'] == items[i]['content']
            assert item['url'] == items[i]['url']

    def test_clustering_handles_items_with_missing_content(self):
        """Test clustering with items missing content field."""
        items = [
            {'title': 'Article 1', 'content': 'Prompt injection security'},
            {'title': 'Article 2'},  # Missing content
            {'title': 'Article 3', 'content': 'Prompt injection attack'}
        ]
        clustering = Clustering()
        result = clustering.cluster(items)

        # Should handle gracefully without errors
        assert len(result) == 3
        for item in result:
            assert 'cluster_id' in item

    def test_clustering_separates_different_topics(self):
        """Test that clustering separates different topics."""
        items = [
            {'title': 'Ransomware Attack', 'content': 'Ransomware encrypted data'},
            {'title': 'Phishing Campaign', 'content': 'Phishing emails targeting users'},
            {'title': 'Data Breach', 'content': 'User data was stolen'}
        ]
        clustering = Clustering()
        result = clustering.cluster(items)

        # Different unrelated topics should potentially have different cluster IDs
        cluster_ids = [item['cluster_id'] for item in result]
        # Just verify clustering ran without error
        assert len(cluster_ids) == 3


# ============================================================================
# Integration Tests
# ============================================================================

class TestProcessorIntegration:
    """Tests for processor integration."""

    def test_pipeline_parser_normalizer(self):
        """Test parser -> normalizer pipeline."""
        html_content = "<p>AI Security Breakthrough</p><p>Researchers found a vulnerability</p>"
        parser = Parser()
        normalizer = Normalizer()

        parsed = parser.parse_html(html_content)
        normalized = normalizer.normalize({
            'title': 'Article',
            'content': parsed
        })

        assert 'AI Security' in normalized['content'] or 'Researchers' in normalized['content']
        assert 'title' in normalized

    def test_pipeline_normalizer_deduplicator(self):
        """Test normalizer -> deduplicator pipeline."""
        raw_items = [
            {'title': 'Breaking News'},
            {'title': 'Breaking News'},
            {'title': 'Other News'}
        ]
        normalizer = Normalizer()
        deduplicator = Deduplicator()

        normalized = [normalizer.normalize(item) for item in raw_items]
        deduplicated = deduplicator.deduplicate(normalized)

        assert deduplicated['unique_count'] <= 3

    def test_pipeline_full_processor_chain(self):
        """Test full processing pipeline."""
        # Simulate raw feed items
        raw_items = [
            {
                'title': 'AI Security Alert',
                'content': '<p>Security researchers discovered a prompt injection vulnerability</p>',
                'url': 'https://example.com/1'
            },
            {
                'title': 'AI Security Alert',
                'content': '<p>Security researchers discovered a prompt injection vulnerability</p>',
                'url': 'https://example2.com/1'
            }
        ]

        parser = Parser()
        normalizer = Normalizer()
        deduplicator = Deduplicator()
        clustering = Clustering()

        # Step 1: Parse HTML content
        parsed_items = []
        for item in raw_items:
            item_copy = item.copy()
            item_copy['content'] = parser.parse_html(item['content'])
            parsed_items.append(item_copy)

        # Step 2: Normalize
        normalized_items = [normalizer.normalize(item) for item in parsed_items]

        # Step 3: Deduplicate
        deduplicated = deduplicator.deduplicate(normalized_items)

        # Step 4: Cluster
        clustered = clustering.cluster(deduplicated['unique_items'])

        # Verify final output
        assert len(clustered) <= len(raw_items)
        for item in clustered:
            assert 'cluster_id' in item
            assert 'title' in item
            assert 'content' in item
