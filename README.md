# AI Security Intelligence Engine

A dual-mode AI security intelligence system that aggregates, scores, and curates AI security content from multiple sources.

## Overview

**Private backend** aggregates AI security content → scores with multi-dimensional scoring → summarizes with LLM → generates private artifacts

**Public GitHub Pages frontend** publishes curated daily briefs, trends, and learning resources

Built to support career transition into AI Security Research roles and generate presentation/paper ideas.

## Features

### 🔍 Content Aggregation
- RSS feed fetching with caching and rate limiting
- arXiv API integration for academic papers
- Configurable source credibility tiers
- Deduplication and clustering

### 📊 Multi-Dimensional Scoring
- **Relevance**: Keyword matching to AI security priorities
- **Credibility**: Source authority assessment
- **Impact**: Severity and affected users
- **Freshness**: Recency scoring with time decay
- **Practicality**: Actionable insights detection

Final weighted score (0-100) for intelligent ranking.

### 🤖 LLM Summarization
- Local Ollama integration (zero API cost)
- Fallback to metadata-based summaries
- Generates: summary, why_it_matters, practical_mitigation
- Grounded prompts prevent hallucination

### 📈 Automated Workflows
- **Daily** (7 AM America/Edmonton): Fetch → Process → Score → Summarize → Publish
- **Weekly** (Sunday 9 AM): Generate PDF briefs, LinkedIn drafts, presentation points, trends

### 🌐 GitHub Pages Site
- Daily brief with top 10-20 items
- Learning resources (categorized: Start/Intermediate/Deep Dive)
- 30-day trends dashboard
- Professional, mobile-responsive design

## Quick Start

```bash
# Clone and setup
git clone <repository-url>
cd neo-notebook.github.io
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure sources
# Edit config/sources.yaml to add your RSS feeds

# Run daily pipeline
python src/main.py --mode daily

# View outputs
open docs/public/index.html
```

See [docs/setup.md](docs/setup.md) for complete installation guide.

## Project Structure

```
├── .github/workflows/     # GitHub Actions (daily/weekly)
├── config/               # Configuration (sources, scoring, tags)
├── docs/                 # Documentation
│   └── public/          # GitHub Pages site
├── private/             # Private outputs (gitignored)
│   ├── feeds/          # Daily JSON archives
│   └── artifacts/      # Weekly PDFs, LinkedIn drafts
├── src/                 # Python pipeline
│   ├── fetchers/       # RSS/arXiv fetching
│   ├── processors/     # Parse, normalize, dedupe, cluster
│   ├── scoring/        # 5-dimensional scoring
│   ├── summarization/  # LLM + fallback
│   └── outputs/        # JSON, HTML, PDF generators
└── tests/              # 87 tests, 100% passing
```

## Technology Stack

- **Backend**: Python 3.11+
- **LLM**: Ollama (local, zero-cost)
- **Frontend**: Pure HTML/CSS/JS (no build step)
- **Automation**: GitHub Actions
- **Testing**: pytest (87 tests)

## Configuration

### Content Focus
High priority: Agentic security, prompt injection, HITL, observability, shadow AI

Filters: Excludes generic ransomware/breach recaps without technical insights

### Scoring Weights
```yaml
relevance: 0.35      # Topic match
credibility: 0.25    # Source authority
impact: 0.15         # Severity
freshness: 0.15      # Recency
practicality: 0.10   # Actionable insights
```

Fully configurable in `config/scoring_weights.yaml`

## Documentation

- [Setup Guide](docs/setup.md) - Installation and configuration
- [Sources](docs/sources.md) - Source list and credibility tiers
- [Taxonomy](docs/taxonomy.md) - Tags and scoring rationale

## Testing

```bash
# Run all tests
PYTHONPATH=. pytest tests/ -v

# Run specific test suite
PYTHONPATH=. pytest tests/test_processors.py -v
```

**Test Coverage**: 87 tests covering:
- Processors (35 tests)
- Scoring system (15 tests)
- Summarization (15 tests)
- Output generators (8 tests)
- Utilities (9 tests)
- Integration (5 tests)

## License

MIT License

## Contributing

Built with Claude Code. Contributions welcome via pull requests.

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
