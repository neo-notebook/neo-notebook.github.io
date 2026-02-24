# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI Security Intelligence Engine — a Python pipeline that aggregates, scores, and curates AI security content from RSS feeds and APIs. Outputs a public GitHub Pages site (daily briefs, trends) and private archives (PDFs, LinkedIn drafts, presentation points). Uses Ollama for local LLM summarization with a metadata-based fallback.

## Commands

```bash
# Run pipeline
PYTHONPATH=. python src/main.py --mode daily
PYTHONPATH=. python src/main.py --mode weekly

# Tests
PYTHONPATH=. pytest tests/ -v
PYTHONPATH=. pytest tests/test_processors.py -v          # single test file
PYTHONPATH=. pytest tests/test_scoring.py::TestRelevanceScorer -v  # single class
PYTHONPATH=. pytest tests/ --cov=src                     # with coverage

# Docker
docker-compose up -d              # starts pipeline + ollama + nginx
docker-compose logs -f pipeline   # watch pipeline output
```

## Architecture

**6-stage pipeline** orchestrated by `src/main.py`:

1. **Fetch** (`src/fetchers/`) — RSS/Atom feeds via feedparser, with HTTP caching
2. **Process** (`src/processors/`) — parse HTML → normalize fields → deduplicate → cluster topics
3. **Score** (`src/scoring/`) — 5 independent scorers weighted-summed to a 0–100 final score:
   - Relevance (35%) · Credibility (25%) · Impact (15%) · Freshness (15%) · Practicality (10%)
   - Weights and priority keywords configured in `config/scoring_weights.yaml`
4. **Summarize** (`src/summarization/`) — factory dispatches to Ollama LLM or fallback metadata extractor
5. **Rank & Filter** — top 20 for public, all items for private archive
6. **Output** (`src/outputs/`) — JSON, HTML, PDF, LinkedIn drafts, presentation points

### Key patterns

- **Factory pattern**: `SummarizerFactory` tries LLM first, falls back to metadata extraction
- **Strategy pattern**: each scorer is an independent class; weights are YAML-configurable
- **Template method**: `BaseFetcher` defines the interface, `RSSFetcher` implements it
- **Config-driven**: all scoring weights, source lists, and tags live in `config/*.yaml` — behavior changes require zero code changes

## Configuration

All in `config/`:
- `sources.yaml` — RSS/API sources with credibility tiers (high/medium/low) and enable flags
- `scoring_weights.yaml` — dimension weights and priority topic keywords
- `tags_taxonomy.yaml` — content classification tags

`src/config.py` loads these with property accessors and hardcoded defaults for graceful degradation.

## Output Locations

- **Public** (committed): `docs/public/data/brief_today.json`, `docs/public/index.html`
- **Private** (gitignored): `private/feeds/YYYY-MM-DD.json`, `private/artifacts/`

## GitHub Actions

- **Daily** (`.github/workflows/daily.yml`): runs pipeline at 13:00 UTC, commits public outputs
- **Weekly** (`.github/workflows/weekly.yml`): generates PDFs, LinkedIn drafts, trends at 15:00 UTC Sunday

## Docker Services

`docker-compose.yml` defines three services:
- `pipeline` — Python 3.11 app container (depends on ollama)
- `ollama` — local LLM service, auto-pulls llama3.2
- `webserver` — nginx serving `docs/public/` on port 8080

## Testing

87 tests across 7 files using pytest + pytest-mock. `PYTHONPATH=.` is required for all test/run commands. Tests mock external dependencies (feeds, Ollama API) — no network access needed.
