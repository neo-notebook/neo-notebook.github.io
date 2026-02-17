"""
Centralized scoring weight management.
"""
from typing import Dict
from src.config import Config
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ScoreWeights:
    """Manage scoring weights from configuration."""

    def __init__(self, config: Config = None):
        """
        Initialize score weights.

        Args:
            config: Configuration object (loads from file if not provided)
        """
        self.config = config or Config()
        self.weights = self._load_weights()

    def _load_weights(self) -> Dict[str, float]:
        """
        Load scoring weights from configuration.

        Returns:
            Dictionary of dimension names to weights
        """
        try:
            # Config class already extracts weights for us
            weights = self.config.scoring_weights

            # Validate weights sum to 1.0 (with small tolerance)
            total = sum(weights.values())
            if abs(total - 1.0) > 0.01:
                logger.warning(f"Scoring weights sum to {total}, not 1.0. Consider normalizing.")

            return weights
        except Exception as e:
            logger.error(f"Error loading scoring weights: {e}")
            # Return default weights
            return {
                'relevance': 0.35,
                'credibility': 0.25,
                'impact': 0.15,
                'freshness': 0.15,
                'practicality': 0.10
            }

    def get_weight(self, dimension: str) -> float:
        """
        Get weight for a specific scoring dimension.

        Args:
            dimension: Name of the scoring dimension

        Returns:
            Weight value (0.0 to 1.0)
        """
        return self.weights.get(dimension, 0.0)

    def calculate_weighted_score(self, scores: Dict[str, float]) -> float:
        """
        Calculate final weighted score from individual dimension scores.

        Args:
            scores: Dictionary of dimension names to scores (0-100)

        Returns:
            Final weighted score (0-100)
        """
        weighted_sum = 0.0

        for dimension, score in scores.items():
            weight = self.get_weight(dimension)
            weighted_sum += weight * score

        return weighted_sum
