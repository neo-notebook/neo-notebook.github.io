"""
Tests for the scoring system.
"""
import pytest
from datetime import datetime, timedelta
from src.scoring.relevance_scorer import RelevanceScorer
from src.scoring.credibility_scorer import CredibilityScorer
from src.scoring.impact_scorer import ImpactScorer
from src.scoring.freshness_scorer import FreshnessScorer
from src.scoring.practicality_scorer import PracticalityScorer
from src.scoring.score_weights import ScoreWeights


class TestRelevanceScorer:
    """Tests for relevance scoring."""

    def test_scores_high_for_relevant_content(self):
        """Test that relevant content gets high scores."""
        scorer = RelevanceScorer()
        item = {
            'title': 'New Agent Security Framework',
            'content': 'This article discusses prompt injection and agentic security...'
        }
        score = scorer.score(item)
        assert score > 0
        assert score <= 100

    def test_scores_zero_for_irrelevant_content(self):
        """Test that irrelevant content gets zero score."""
        scorer = RelevanceScorer()
        item = {
            'title': 'Random Article',
            'content': 'This has nothing to do with AI security.'
        }
        score = scorer.score(item)
        assert score == 0


class TestCredibilityScorer:
    """Tests for credibility scoring."""

    def test_scores_high_tier_sources_highly(self):
        """Test that high tier sources get 100 score."""
        scorer = CredibilityScorer()
        item = {'source': 'NIST', 'credibility_tier': 'high'}
        score = scorer.score(item)
        assert score == 100

    def test_scores_medium_tier_sources_moderately(self):
        """Test that medium tier sources get 70 score."""
        scorer = CredibilityScorer()
        item = {'source': 'Blog', 'credibility_tier': 'medium'}
        score = scorer.score(item)
        assert score == 70

    def test_handles_unknown_tier(self):
        """Test that unknown tier gets default score."""
        scorer = CredibilityScorer()
        item = {'source': 'Unknown'}
        score = scorer.score(item)
        assert score == 50


class TestImpactScorer:
    """Tests for impact scoring."""

    def test_scores_high_for_critical_content(self):
        """Test that critical vulnerabilities get high scores."""
        scorer = ImpactScorer()
        item = {
            'title': 'Critical Zero-Day Exploit',
            'content': 'A critical vulnerability is being actively exploited...'
        }
        score = scorer.score(item)
        assert score >= 40  # At least 2 high-impact keywords

    def test_scores_zero_for_low_impact(self):
        """Test that low-impact content gets zero or low score."""
        scorer = ImpactScorer()
        item = {
            'title': 'Minor Update',
            'content': 'A small change was made.'
        }
        score = scorer.score(item)
        assert score < 20


class TestFreshnessScorer:
    """Tests for freshness scoring."""

    def test_scores_recent_content_highly(self):
        """Test that recent content gets high score."""
        scorer = FreshnessScorer()
        item = {
            'title': 'Recent Article',
            'published_date': datetime.now().isoformat()
        }
        score = scorer.score(item)
        assert score == 100

    def test_scores_old_content_lower(self):
        """Test that old content gets lower score."""
        scorer = FreshnessScorer()
        old_date = datetime.now() - timedelta(days=100)
        item = {
            'title': 'Old Article',
            'published_date': old_date.isoformat()
        }
        score = scorer.score(item)
        assert score <= 50

    def test_handles_missing_date(self):
        """Test that missing date gets default score."""
        scorer = FreshnessScorer()
        item = {'title': 'No Date', 'published_date': 'No date available'}
        score = scorer.score(item)
        assert score == 50


class TestPracticalityScorer:
    """Tests for practicality scoring."""

    def test_scores_high_for_actionable_content(self):
        """Test that actionable content gets high score."""
        scorer = PracticalityScorer()
        item = {
            'title': 'Mitigation Guide',
            'content': 'Here is a fix and remediation steps for prevention...'
        }
        score = scorer.score(item)
        assert score >= 60  # At least 3 practical keywords

    def test_scores_zero_for_theoretical_content(self):
        """Test that non-actionable content gets zero score."""
        scorer = PracticalityScorer()
        item = {
            'title': 'Abstract Theory',
            'content': 'This discusses theoretical concepts.'
        }
        score = scorer.score(item)
        assert score == 0


class TestScoreWeights:
    """Tests for score weight management."""

    def test_loads_weights_from_config(self):
        """Test that weights load from configuration."""
        weights = ScoreWeights()
        assert weights.get_weight('relevance') > 0
        assert weights.get_weight('credibility') > 0

    def test_calculates_weighted_score(self):
        """Test that weighted score is calculated correctly."""
        weights = ScoreWeights()
        scores = {
            'relevance': 100,
            'credibility': 100,
            'impact': 100,
            'freshness': 100,
            'practicality': 100
        }
        final_score = weights.calculate_weighted_score(scores)
        assert final_score == 100

    def test_handles_partial_scores(self):
        """Test that partial scores work."""
        weights = ScoreWeights()
        scores = {
            'relevance': 50,
            'credibility': 50
        }
        final_score = weights.calculate_weighted_score(scores)
        # Should be relevance_weight * 50 + credibility_weight * 50
        # = 0.35 * 50 + 0.25 * 50 = 17.5 + 12.5 = 30
        assert 25 <= final_score <= 35
