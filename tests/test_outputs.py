"""
Tests for output generators.
"""
import pytest
import json
import tempfile
from pathlib import Path
from src.outputs.json_generator import JSONGenerator
from src.outputs.html_generator import HTMLGenerator
from src.outputs.pdf_generator import PDFGenerator
from src.outputs.linkedin_drafts import LinkedInDrafts
from src.outputs.presentation_points import PresentationPoints


@pytest.fixture
def sample_items():
    """Sample items for testing."""
    return [
        {
            'title': 'Test Article 1',
            'summary': 'Summary 1',
            'why_it_matters': 'Matters 1',
            'practical_mitigation': 'Mitigation 1',
            'tags': ['tag1', 'tag2'],
            'source': 'Source1',
            'published_date': '2024-01-01',
            'url': 'https://example.com/1',
            'cluster_id': 'agentic_systems',
            'score': 95
        },
        {
            'title': 'Test Article 2',
            'summary': 'Summary 2',
            'why_it_matters': 'Matters 2',
            'practical_mitigation': 'Mitigation 2',
            'tags': ['tag3'],
            'source': 'Source2',
            'published_date': '2024-01-02',
            'url': 'https://example.com/2',
            'cluster_id': 'prompt_injection',
            'score': 90
        }
    ]


class TestJSONGenerator:
    """Tests for JSON generator."""

    def test_generates_public_brief(self, sample_items):
        """Test public brief generation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "brief.json"
            generator = JSONGenerator()

            generator.generate_public_brief(sample_items, str(output_path))

            assert output_path.exists()

            with open(output_path) as f:
                data = json.load(f)

            assert 'generated_at' in data
            assert data['item_count'] == 2
            assert len(data['items']) == 2
            assert data['items'][0]['title'] == 'Test Article 1'

    def test_limits_max_items(self, sample_items):
        """Test that max_items limit is respected."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "brief.json"
            generator = JSONGenerator()

            generator.generate_public_brief(sample_items, str(output_path), max_items=1)

            with open(output_path) as f:
                data = json.load(f)

            assert len(data['items']) == 1

    def test_generates_private_archive(self, sample_items):
        """Test private archive generation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "archive.json"
            generator = JSONGenerator()

            generator.generate_private_archive(sample_items, str(output_path))

            assert output_path.exists()

            with open(output_path) as f:
                data = json.load(f)

            assert data['item_count'] == 2
            assert 'score' in data['items'][0]  # Private includes scores

    def test_generates_trends(self, sample_items):
        """Test trends generation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "trends.json"
            generator = JSONGenerator()

            generator.generate_trends(sample_items, str(output_path))

            assert output_path.exists()

            with open(output_path) as f:
                data = json.load(f)

            assert 'top_clusters' in data
            assert 'top_sources' in data
            assert 'opportunities' in data


class TestHTMLGenerator:
    """Tests for HTML generator."""

    def test_generates_brief_page(self, sample_items):
        """Test HTML brief generation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "index.html"
            generator = HTMLGenerator()

            generator.generate_brief_page(sample_items, str(output_path))

            assert output_path.exists()

            with open(output_path) as f:
                html = f.read()

            assert 'Test Article 1' in html
            assert 'Test Article 2' in html
            assert 'Summary 1' in html


class TestPDFGenerator:
    """Tests for PDF generator."""

    def test_generates_weekly_brief(self, sample_items):
        """Test PDF brief generation (placeholder)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "brief.pdf"
            generator = PDFGenerator()

            generator.generate_weekly_brief(sample_items, str(output_path))

            # Placeholder creates .txt file
            text_path = output_path.with_suffix('.txt')
            assert text_path.exists()

            with open(text_path) as f:
                content = f.read()

            assert 'Weekly Brief' in content
            assert 'Test Article 1' in content


class TestLinkedInDrafts:
    """Tests for LinkedIn drafts."""

    def test_generates_drafts(self, sample_items):
        """Test LinkedIn draft generation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "drafts.json"
            generator = LinkedInDrafts()

            generator.generate_drafts(sample_items, str(output_path))

            assert output_path.exists()

            with open(output_path) as f:
                data = json.load(f)

            assert 'drafts' in data
            assert len(data['drafts']) > 0
            assert 'tone' in data['drafts'][0]
            assert 'content' in data['drafts'][0]


class TestPresentationPoints:
    """Tests for presentation points."""

    def test_generates_points(self, sample_items):
        """Test presentation points generation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "points.json"
            generator = PresentationPoints()

            generator.generate_points(sample_items, str(output_path))

            assert output_path.exists()

            with open(output_path) as f:
                data = json.load(f)

            assert 'talking_points' in data
            assert len(data['talking_points']) > 0
            assert 'theme' in data['talking_points'][0]
            assert 'talking_point' in data['talking_points'][0]
