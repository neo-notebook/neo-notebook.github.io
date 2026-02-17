"""
HTML generator for static pages.
"""
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
from src.utils.logger import get_logger

logger = get_logger(__name__)


class HTMLGenerator:
    """Generate static HTML pages."""

    def __init__(self):
        """Initialize HTML generator."""
        pass

    def generate_brief_page(self,
                             items: List[Dict[str, Any]],
                             output_path: str,
                             title: str = "Daily AI Security Brief") -> None:
        """
        Generate HTML page for daily brief.

        Args:
            items: List of items to display
            output_path: Path to save HTML file
            title: Page title
        """
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="assets/style.css">
</head>
<body>
    <header>
        <nav>
            <h1>AI Security Intelligence</h1>
            <ul>
                <li><a href="index.html">Daily Brief</a></li>
                <li><a href="learning.html">Learning Resources</a></li>
                <li><a href="trends.html">Trends</a></li>
            </ul>
        </nav>
    </header>
    <main>
        <h2>{title}</h2>
        <p class="generated-at">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        <div id="brief-items">
"""

        # Add items
        for i, item in enumerate(items, 1):
            tags = ', '.join(item.get('tags', []))
            html += f"""
            <article class="brief-item">
                <h3>{i}. {item.get('title', 'Untitled')}</h3>
                <p class="summary">{item.get('summary', 'No summary available')}</p>
                <p class="why-matters"><strong>Why it matters:</strong> {item.get('why_it_matters', 'N/A')}</p>
                <p class="mitigation"><strong>Practical mitigation:</strong> {item.get('practical_mitigation', 'N/A')}</p>
                <p class="meta">
                    <span class="source">Source: {item.get('source', 'Unknown')}</span> |
                    <span class="date">{item.get('published_date', 'No date')}</span> |
                    <span class="tags">Tags: {tags or 'None'}</span>
                </p>
                <p class="link"><a href="{item.get('url', '#')}" target="_blank">Read full article →</a></p>
            </article>
"""

        html += """
        </div>
    </main>
    <footer>
        <p>Generated with Claude Code | AI Security Intelligence Engine</p>
    </footer>
    <script src="assets/app.js"></script>
</body>
</html>
"""

        # Write to file
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w') as f:
            f.write(html)

        logger.info(f"Generated HTML brief: {output_path} ({len(items)} items)")
