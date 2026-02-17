"""
Presentation talking points generator.
"""
import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
from collections import Counter
from src.utils.logger import get_logger

logger = get_logger(__name__)


class PresentationPoints:
    """Generate presentation talking points from trends."""

    def __init__(self):
        """Initialize presentation points generator."""
        pass

    def generate_points(self,
                         items: List[Dict[str, Any]],
                         output_path: str,
                         num_points: int = 10) -> None:
        """
        Generate presentation talking points from weekly trends.

        Args:
            items: List of items from the week
            output_path: Path to save points JSON
            num_points: Number of talking points to generate
        """
        # Analyze clusters to find top themes
        cluster_counts = Counter()
        for item in items:
            cluster = item.get('cluster_id', 'general')
            cluster_counts[cluster] += 1

        top_clusters = cluster_counts.most_common(5)

        points = []

        # Generate talking points based on top clusters
        for cluster, count in top_clusters:
            # Get example items from this cluster
            cluster_items = [item for item in items if item.get('cluster_id') == cluster][:2]

            if cluster_items:
                point = {
                    'theme': cluster.replace('_', ' ').title(),
                    'article_count': count,
                    'talking_point': f"Trend: {cluster.replace('_', ' ').title()} ({count} articles this period)",
                    'examples': [
                        {
                            'title': item.get('title', ''),
                            'source': item.get('source', '')
                        }
                        for item in cluster_items
                    ]
                }
                points.append(point)

        # Add general insights
        if len(items) > 0:
            points.append({
                'theme': 'Overall Activity',
                'talking_point': f"Analyzed {len(items)} AI security articles/papers this period",
                'examples': []
            })

        # Add emerging opportunities
        points.append({
            'theme': 'Research Opportunities',
            'talking_point': f"Top research/presentation opportunities: {', '.join([c.replace('_', ' ') for c, n in top_clusters[:3]])}",
            'examples': []
        })

        # Save points
        output = {
            'generated_at': datetime.now().isoformat(),
            'period_items': len(items),
            'talking_points': points[:num_points]
        }

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2)

        logger.info(f"Generated {len(points)} presentation points: {output_path}")
