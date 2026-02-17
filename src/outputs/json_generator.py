"""
JSON generator for public and private datasets.
"""
import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
from src.utils.logger import get_logger

logger = get_logger(__name__)


class JSONGenerator:
    """Generate JSON datasets for public and private use."""

    def __init__(self):
        """Initialize JSON generator."""
        pass

    def generate_public_brief(self,
                              items: List[Dict[str, Any]],
                              output_path: str,
                              max_items: int = 20) -> None:
        """
        Generate public daily brief JSON.

        Args:
            items: List of items (should be pre-scored and ranked)
            output_path: Path to save JSON file
            max_items: Maximum number of items to include
        """
        # Take top N items
        top_items = items[:max_items]

        # Format for public consumption (sanitize, select fields)
        public_items = []
        for item in top_items:
            public_item = {
                'title': item.get('title', ''),
                'summary': item.get('summary', ''),
                'why_it_matters': item.get('why_it_matters', ''),
                'practical_mitigation': item.get('practical_mitigation', ''),
                'tags': item.get('tags', []),
                'source': item.get('source', ''),
                'published_date': item.get('published_date', ''),
                'url': item.get('url', ''),
                'cluster_id': item.get('cluster_id', 'general')
            }
            public_items.append(public_item)

        # Create output structure
        output = {
            'generated_at': datetime.now().isoformat(),
            'item_count': len(public_items),
            'items': public_items
        }

        # Write to file
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2)

        logger.info(f"Generated public brief: {output_path} ({len(public_items)} items)")

    def generate_private_archive(self,
                                  items: List[Dict[str, Any]],
                                  output_path: str) -> None:
        """
        Generate private archive with full data and scores.

        Args:
            items: List of items with all fields and scores
            output_path: Path to save JSON file
        """
        # Create output structure with full data
        output = {
            'generated_at': datetime.now().isoformat(),
            'item_count': len(items),
            'items': items
        }

        # Write to file
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2)

        logger.info(f"Generated private archive: {output_path} ({len(items)} items)")

    def generate_trends(self,
                        items: List[Dict[str, Any]],
                        output_path: str,
                        days: int = 30) -> None:
        """
        Generate trends JSON from aggregated items.

        Args:
            items: List of items from last N days
            output_path: Path to save JSON file
            days: Number of days covered
        """
        # Aggregate by cluster
        cluster_counts = {}
        for item in items:
            cluster = item.get('cluster_id', 'general')
            cluster_counts[cluster] = cluster_counts.get(cluster, 0) + 1

        # Aggregate by source
        source_counts = {}
        for item in items:
            source = item.get('source', 'Unknown')
            source_counts[source] = source_counts.get(source, 0) + 1

        # Top clusters and sources
        top_clusters = sorted(cluster_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        top_sources = sorted(source_counts.items(), key=lambda x: x[1], reverse=True)[:10]

        # Generate opportunities (simple version - top clusters)
        opportunities = [
            {
                'topic': cluster,
                'article_count': count,
                'opportunity': f"Consider presentation/paper on {cluster.replace('_', ' ')} (trending with {count} articles)"
            }
            for cluster, count in top_clusters[:5]
        ]

        output = {
            'generated_at': datetime.now().isoformat(),
            'period_days': days,
            'total_items': len(items),
            'top_clusters': [{'cluster': c, 'count': n} for c, n in top_clusters],
            'top_sources': [{'source': s, 'count': n} for s, n in top_sources],
            'opportunities': opportunities
        }

        # Write to file
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2)

        logger.info(f"Generated trends: {output_path}")
