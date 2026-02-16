"""Configuration loader for YAML config files."""

import os
from pathlib import Path
from typing import Any, Dict, List
import yaml

from .utils.logger import get_logger

logger = get_logger(__name__)


class Config:
    """Configuration manager for loading YAML config files."""

    def __init__(self, config_dir: str = "config"):
        """
        Initialize config loader.

        Args:
            config_dir: Directory containing config YAML files
        """
        self.config_dir = Path(config_dir)

        # Load all config files
        self.sources = self._load_sources()
        self.scoring_config = self._load_scoring_config()
        self.tags_taxonomy = self._load_tags_taxonomy()

    def _load_yaml(self, filename: str) -> Dict[str, Any]:
        """Load YAML file from config directory."""
        filepath = self.config_dir / filename

        if not filepath.exists():
            logger.warning(f"Config file not found: {filepath}")
            return {}

        try:
            with open(filepath, 'r') as f:
                data = yaml.safe_load(f)
                logger.info(f"Loaded config: {filename}")
                return data or {}
        except yaml.YAMLError as e:
            logger.error(f"Failed to parse YAML {filename}: {e}")
            return {}

    def _load_sources(self) -> List[Dict[str, Any]]:
        """Load sources configuration."""
        data = self._load_yaml("sources.yaml")
        sources = data.get('sources', [])

        # Filter to enabled sources only
        enabled_sources = [s for s in sources if s.get('enabled', True)]
        logger.info(f"Loaded {len(enabled_sources)} enabled sources")

        return enabled_sources

    def _load_scoring_config(self) -> Dict[str, Any]:
        """Load scoring configuration."""
        data = self._load_yaml("scoring_weights.yaml")
        return data.get('scoring', {}) if 'scoring' in data else data

    def _load_tags_taxonomy(self) -> Dict[str, Any]:
        """Load tags taxonomy."""
        data = self._load_yaml("tags_taxonomy.yaml")
        return data.get('tags', {})

    @property
    def scoring_weights(self) -> Dict[str, float]:
        """Get scoring dimension weights."""
        dimensions = self.scoring_config.get('dimensions', {})
        if dimensions:
            return {key: val.get('weight', 0.0) for key, val in dimensions.items()}
        return {
            'relevance': 0.35,
            'credibility': 0.25,
            'impact': 0.15,
            'freshness': 0.15,
            'practicality': 0.10
        }

    @property
    def relevance_keywords(self) -> Dict[str, Any]:
        """Get relevance keyword configuration."""
        return self.scoring_config.get('topical_relevance', {}).get('high_priority_topics', {})

    @property
    def credibility_tiers(self) -> Dict[str, int]:
        """Get credibility tier scores."""
        tiers = self.scoring_config.get('credibility_tiers', {})
        if tiers:
            return {k: v.get('score', 70) for k, v in tiers.items()}
        return {
            'high': 90,
            'medium': 70,
            'low': 50
        }
