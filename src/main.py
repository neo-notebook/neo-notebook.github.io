"""Main pipeline orchestrator."""

import argparse
from datetime import datetime
from typing import List, Dict, Any

from .config import Config
from .fetchers.rss_fetcher import RSSFetcher
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

    # TODO: Processing, scoring, summarization, generation

    elapsed = (datetime.now() - start_time).total_seconds()
    logger.info(f"Pipeline complete in {elapsed:.2f}s")

    return {
        'mode': mode,
        'items_fetched': len(all_items),
        'elapsed_seconds': elapsed
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AI Security Intelligence Pipeline')
    parser.add_argument('--mode', choices=['daily', 'weekly'], default='daily',
                        help='Pipeline mode: daily or weekly')
    args = parser.parse_args()

    main(mode=args.mode)
