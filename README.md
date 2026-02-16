# AI Security Intelligence Engine

A dual-mode AI Security Intelligence system for curated AI security content.

## Setup

1. **Install Python 3.11+**
2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Install Ollama (optional, for LLM summarization):**
   - Visit https://ollama.ai/download
   - Install and run: `ollama pull llama3.2`

## Usage

**Run daily pipeline:**
```bash
python src/main.py --mode daily
```

**Run weekly pipeline:**
```bash
python src/main.py --mode weekly
```

## Configuration

Edit `config/sources.yaml` to add/remove RSS feeds.

## GitHub Pages

The public site is served from `docs/public/` and auto-deploys via GitHub Actions.
