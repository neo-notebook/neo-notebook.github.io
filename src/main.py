"""Main pipeline orchestrator."""

import argparse
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path

from .config import Config
from .fetchers.rss_fetcher import RSSFetcher
from .processors.parser import Parser
from .processors.normalizer import Normalizer
from .processors.deduplicator import Deduplicator
from .processors.clustering import Clustering
from .scoring.relevance_scorer import RelevanceScorer
from .scoring.credibility_scorer import CredibilityScorer
from .scoring.impact_scorer import ImpactScorer
from .scoring.freshness_scorer import FreshnessScorer
from .scoring.practicality_scorer import PracticalityScorer
from .scoring.score_weights import ScoreWeights
from .summarization.summarizer_factory import SummarizerFactory
from .outputs.json_generator import JSONGenerator
from .outputs.html_generator import HTMLGenerator
from .utils.logger import get_logger

logger = get_logger(__name__)


def main(mode: str = 'daily') -> Dict[str, Any]:
    """
    Run intelligence pipeline.

    Args:
        mode: 'daily' or 'weekly'

    Returns:
        Pipeline execution summary
    """
    logger.info(f"Starting {mode} pipeline")
    start_time = datetime.now()

    # 1. Load configuration
    config = Config()
    logger.info(f"Loaded {len(config.sources)} sources")

    # 2. Fetch content
    all_items = []
    for source in config.sources:
        if source.get('type') == 'rss':
            fetcher = RSSFetcher(source)
            items = fetcher.fetch()
            all_items.extend(items)

    logger.info(f"Fetched {len(all_items)} total items")

    # 3. Process: Parse, Normalize, Deduplicate, Cluster
    logger.info("Processing items...")
    parser = Parser()
    normalizer = Normalizer()
    deduplicator = Deduplicator()
    clustering = Clustering()

    # Parse HTML content
    for item in all_items:
        content = item.get('content', '')
        item['content'] = parser.parse(content)

    # Normalize
    normalized_items = normalizer.normalize_batch(all_items)
    logger.info(f"Normalized {len(normalized_items)} items")

    # Deduplicate
    dedup_result = deduplicator.deduplicate(normalized_items)
    unique_items = dedup_result['unique_items']
    logger.info(f"Deduplicated: {len(unique_items)} unique items")

    # Cluster
    clustered_items = clustering.cluster(unique_items)
    logger.info(f"Clustered {len(clustered_items)} items")

    # 4. Score: Calculate multi-dimensional scores
    logger.info("Scoring items...")
    relevance_scorer = RelevanceScorer(config)
    credibility_scorer = CredibilityScorer()
    impact_scorer = ImpactScorer()
    freshness_scorer = FreshnessScorer()
    practicality_scorer = PracticalityScorer()
    score_weights = ScoreWeights(config)

    for item in clustered_items:
        scores = {
            'relevance': relevance_scorer.score(item),
            'credibility': credibility_scorer.score(item),
            'impact': impact_scorer.score(item),
            'freshness': freshness_scorer.score(item),
            'practicality': practicality_scorer.score(item)
        }
        item['scores'] = scores
        item['final_score'] = score_weights.calculate_weighted_score(scores)

    # Sort by final score
    ranked_items = sorted(clustered_items, key=lambda x: x['final_score'], reverse=True)
    logger.info(f"Scored and ranked {len(ranked_items)} items")

    # 5. Summarize: Top 20 items
    logger.info("Summarizing top items...")
    top_items = ranked_items[:20]
    summarizer = SummarizerFactory()
    summarized_items = summarizer.summarize_batch(top_items)
    logger.info(f"Summarized {len(summarized_items)} items")

    # 6. Generate Outputs
    logger.info("Generating outputs...")
    json_gen = JSONGenerator()
    html_gen = HTMLGenerator()

    # Public outputs
    today = datetime.now().strftime('%Y-%m-%d')
    json_gen.generate_public_brief(
        summarized_items,
        'docs/public/data/brief_today.json',
        max_items=20
    )
    html_gen.generate_brief_page(
        summarized_items[:10],  # Top 10 for HTML
        'docs/public/index.html'
    )

    # Private archive
    json_gen.generate_private_archive(
        ranked_items,  # All items with scores
        f'private/feeds/{today}.json'
    )

    elapsed = (datetime.now() - start_time).total_seconds()
    logger.info(f"Pipeline complete in {elapsed:.2f}s")

    return {
        'mode': mode,
        'items_fetched': len(all_items),
        'items_processed': len(normalized_items),
        'items_unique': len(unique_items),
        'items_scored': len(ranked_items),
        'items_summarized': len(summarized_items),
        'elapsed_seconds': elapsed
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AI Security Intelligence Pipeline')
    parser.add_argument('--mode', choices=['daily', 'weekly'], default='daily',
                        help='Pipeline mode: daily or weekly')
    args = parser.parse_args()

    main(mode=args.mode)
