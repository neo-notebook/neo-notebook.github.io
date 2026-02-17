# Setup Guide

Complete installation and configuration guide for the AI Security Intelligence Engine.

## Prerequisites

- Python 3.11+
- Git
- (Optional) Ollama for LLM summarization

## Installation

### 1. Clone Repository

```bash
git clone <repository-url>
cd neo-notebook.github.io
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Sources

Edit `config/sources.yaml` to add your RSS feeds:

```yaml
sources:
  - name: "Your Source Name"
    type: "rss"
    url: "https://example.com/feed.xml"
    category: "security_research"
    credibility_tier: "medium"
    enabled: true
```

## Running the Pipeline

### Daily Pipeline (Local)

```bash
python src/main.py --mode daily
```

This will:
1. Fetch content from configured sources
2. Process, score, and rank items
3. Summarize top items
4. Generate public brief and private archive

### Weekly Pipeline (Local)

```bash
python -c "
from src.outputs.json_generator import JSONGenerator
from src.outputs.pdf_generator import PDFGenerator
import json, glob

# Load last 30 days
items = []
for f in glob.glob('private/feeds/*.json'):
    with open(f) as file:
        items.extend(json.load(file)['items'])

# Generate weekly outputs
JSONGenerator().generate_trends(items, 'docs/public/data/trends_30d.json')
PDFGenerator().generate_weekly_brief(items[:50], 'private/artifacts/weekly_brief.pdf')
"
```

## GitHub Actions Setup

### 1. Enable GitHub Pages

- Go to repository Settings → Pages
- Source: Deploy from branch `main`
- Folder: `/docs/public`

### 2. Set Secrets (Optional)

If using cloud LLM instead of Ollama:

- Go to Settings → Secrets → Actions
- Add secret: `OLLAMA_URL` or `LLM_API_KEY`

### 3. Enable Workflows

GitHub Actions will automatically run:
- **Daily**: 7:00 AM America/Edmonton (13:00 UTC)
- **Weekly**: Sunday 9:00 AM America/Edmonton (15:00 UTC)

## Optional: Ollama Setup

For local LLM summarization:

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull model
ollama pull llama3.2

# Start Ollama (runs on localhost:11434)
ollama serve
```

The pipeline will automatically use Ollama if available, otherwise falls back to metadata-based summaries.

## Customization

### Adjust Scoring Weights

Edit `config/scoring_weights.yaml`:

```yaml
dimensions:
  relevance:
    weight: 0.35  # Adjust to prioritize different dimensions
```

### Add/Remove Sources

Edit `config/sources.yaml` and set `enabled: true/false`

### Modify Tags

Edit `config/tags_taxonomy.yaml` to add custom tags

## Troubleshooting

### No items fetched
- Check RSS feed URLs are valid
- Verify `enabled: true` in sources.yaml
- Test feeds manually: `curl <feed-url>`

### Tests failing
```bash
PYTHONPATH=. pytest tests/ -v
```

### GitHub Actions not running
- Check workflow files in `.github/workflows/`
- Verify Actions are enabled in repository settings

## Directory Structure

```
├── .github/workflows/      # GitHub Actions
├── config/                 # Configuration files
├── docs/                   # Documentation
│   └── public/            # GitHub Pages site
├── private/               # Private outputs (gitignored)
│   ├── feeds/            # Daily archives
│   └── artifacts/        # Weekly PDFs, drafts
├── src/                   # Python source code
└── tests/                 # Test suite
```

## Next Steps

1. Add real RSS feeds to `config/sources.yaml`
2. Run daily pipeline locally to verify
3. Push to GitHub to enable automation
4. Monitor GitHub Pages site at `https://<username>.github.io`
