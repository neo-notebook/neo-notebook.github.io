"""
Clustering for grouping similar articles by topic.
"""
from typing import List, Dict, Any
from collections import defaultdict
from src.utils.logger import get_logger

logger = get_logger(__name__)


class Clustering:
    """Group similar articles by topic using keyword-based clustering."""

    def __init__(self, keywords: Dict[str, List[str]] = None):
        """
        Initialize the clustering engine.

        Args:
            keywords: Dictionary mapping cluster names to keyword lists
        """
        self.keywords = keywords or self._default_keywords()

    def _default_keywords(self) -> Dict[str, List[str]]:
        """
        Get default keyword clusters for AI security topics.

        Returns:
            Dictionary of cluster names to keyword lists
        """
        return {
            'agentic_security': ['agent', 'agentic', 'tool calling', 'function calling', 'autonomous'],
            'prompt_injection': ['prompt injection', 'jailbreak', 'prompt attack', 'indirect injection'],
            'hitl': ['human-in-the-loop', 'HITL', 'kill switch', 'human oversight'],
            'observability': ['observability', 'tracing', 'audit', 'logging', 'monitoring'],
            'shadow_ai': ['shadow AI', 'governance', 'policy', 'compliance'],
            'data_leakage': ['data leakage', 'data exfiltration', 'privacy', 'PII'],
            'model_supply_chain': ['model supply chain', 'model security', 'poisoning', 'backdoor'],
            'vuln_exploit': ['vulnerability', 'exploit', 'CVE', 'zero-day'],
            'regulatory': ['regulation', 'regulatory', 'compliance', 'GDPR', 'AI Act', 'NIST'],
        }

    def find_cluster(self, item: Dict[str, Any]) -> str:
        """
        Find the best cluster for an item based on keyword matching.

        Args:
            item: Item to cluster

        Returns:
            Cluster name (or 'general' if no match)
        """
        title = item.get('title', '').lower()
        content = item.get('content', '').lower()
        text = f"{title} {content}"

        # Count keyword matches for each cluster
        cluster_scores = defaultdict(int)

        for cluster_name, keyword_list in self.keywords.items():
            for keyword in keyword_list:
                if keyword.lower() in text:
                    cluster_scores[cluster_name] += 1

        # Return cluster with highest score, or 'general' if no matches
        if cluster_scores:
            best_cluster = max(cluster_scores, key=cluster_scores.get)
            return best_cluster
        else:
            return 'general'

    def cluster(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Assign cluster IDs to items.

        Args:
            items: List of items to cluster

        Returns:
            List of items with cluster_id field added
        """
        clustered_items = []

        for item in items:
            try:
                cluster_id = self.find_cluster(item)
                item['cluster_id'] = cluster_id
                clustered_items.append(item)
            except Exception as e:
                logger.error(f"Error clustering item: {e}")
                item['cluster_id'] = 'general'
                clustered_items.append(item)

        # Log cluster distribution
        cluster_counts = defaultdict(int)
        for item in clustered_items:
            cluster_counts[item['cluster_id']] += 1

        logger.info(f"Clustered {len(clustered_items)} items into {len(cluster_counts)} clusters")
        logger.debug(f"Cluster distribution: {dict(cluster_counts)}")

        return clustered_items
