# Docker Testing Guide

Complete step-by-step guide to test the AI Security Intelligence Engine locally using Docker.

## Prerequisites

- Docker Desktop installed and running
- Docker Compose installed (included with Docker Desktop)
- ~5 GB free disk space (for Ollama models)

## Quick Start (5 Minutes)

```bash
# 1. Build and start all services
docker-compose up -d

# 2. View logs
docker-compose logs -f pipeline

# 3. Check outputs
ls -la docs/public/data/
ls -la private/feeds/

# 4. View the site
open http://localhost:8080

# 5. Cleanup
docker-compose down
```

## Detailed Step-by-Step Testing

### Step 1: Verify Docker Installation

```bash
# Check Docker is running
docker --version
# Expected: Docker version 20.x or higher

docker-compose --version
# Expected: Docker Compose version 2.x or higher
```

### Step 2: Build the Pipeline Container

```bash
# Build without cache (ensures fresh build)
docker-compose build --no-cache pipeline

# Expected output:
# ✓ Successfully built <image-id>
# ✓ Successfully tagged ai-security-intelligence-engine_pipeline:latest
```

**Verify build succeeded:**
```bash
docker images | grep pipeline
# Should show the pipeline image
```

### Step 3: Start Services (Without Ollama)

**Option A: Test without LLM (faster, uses fallback summarization)**

```bash
# Start only pipeline and webserver
docker-compose up -d pipeline webserver

# Check containers are running
docker ps
# Should show: ai-security-pipeline and ai-security-web
```

### Step 4: Run the Daily Pipeline

```bash
# Execute the daily pipeline
docker-compose exec pipeline python src/main.py --mode daily

# Expected output:
# INFO - Starting daily pipeline
# INFO - Loaded 2 sources
# INFO - Fetched X items
# INFO - Normalized X items
# INFO - Deduplicated: X unique items
# INFO - Scored and ranked X items
# INFO - Summarized X items
# INFO - Generated public brief: docs/public/data/brief_today.json
# INFO - Pipeline complete in X.XXs
```

### Step 5: Verify Outputs Created

```bash
# Check public outputs
ls -lah docs/public/data/
# Expected files:
# - brief_today.json

ls -lah docs/public/
# Expected files:
# - index.html
# - learning.html
# - trends.html

# Check private outputs
ls -lah private/feeds/
# Expected: YYYY-MM-DD.json files

# Inspect public brief
cat docs/public/data/brief_today.json | head -30
```

### Step 6: Run Tests Inside Container

```bash
# Run complete test suite
docker-compose exec pipeline pytest tests/ -v

# Expected: 87 passed

# Run specific test suites
docker-compose exec pipeline pytest tests/test_processors.py -v
docker-compose exec pipeline pytest tests/test_scoring.py -v
docker-compose exec pipeline pytest tests/test_integration.py -v
```

### Step 7: View the Website

```bash
# Access the GitHub Pages site locally
open http://localhost:8080

# Or manually navigate to:
# - http://localhost:8080/index.html (Daily Brief)
# - http://localhost:8080/learning.html (Learning Resources)
# - http://localhost:8080/trends.html (Trends Dashboard)
```

### Step 8: Test with Real RSS Feeds (Optional)

```bash
# 1. Stop current containers
docker-compose down

# 2. Edit config/sources.yaml to add real RSS feeds
# Example:
cat >> config/sources.yaml <<'EOF'
  - name: "Krebs on Security"
    type: "rss"
    url: "https://krebsonsecurity.com/feed/"
    category: "high_impact_cyber"
    credibility_tier: "high"
    enabled: true
EOF

# 3. Restart pipeline
docker-compose up -d pipeline

# 4. Run pipeline with real feeds
docker-compose exec pipeline python src/main.py --mode daily

# 5. Check outputs
cat docs/public/data/brief_today.json | jq '.items | length'
# Should show number of items fetched
```

### Step 9: Test with Ollama LLM (Optional)

**This provides better summarization but takes longer to start**

```bash
# 1. Start all services including Ollama
docker-compose up -d

# 2. Wait for Ollama to download model (first time only, ~2-3 minutes)
docker-compose logs -f ollama
# Wait for: "successfully loaded model llama3.2"

# 3. Verify Ollama is running
curl http://localhost:11434/api/tags
# Should return JSON with model info

# 4. Run pipeline with LLM
docker-compose exec pipeline python src/main.py --mode daily

# 5. Check logs for LLM usage
docker-compose logs pipeline | grep "LLM"
# Should see: "LLM summarization available"
```

### Step 10: Test Weekly Pipeline

```bash
# 1. Create some sample data first
docker-compose exec pipeline python src/main.py --mode daily

# 2. Run weekly pipeline
docker-compose exec pipeline python -c "
import json, glob
from datetime import datetime
from src.outputs.json_generator import JSONGenerator
from src.outputs.pdf_generator import PDFGenerator
from src.outputs.linkedin_drafts import LinkedInDrafts
from src.outputs.presentation_points import PresentationPoints

# Load data
all_items = []
for f in glob.glob('private/feeds/*.json'):
    with open(f) as file:
        all_items.extend(json.load(file)['items'])

print(f'Loaded {len(all_items)} items')

# Generate outputs
today = datetime.now().strftime('%Y-%m-%d')
JSONGenerator().generate_trends(all_items, 'docs/public/data/trends_30d.json')
PDFGenerator().generate_weekly_brief(all_items[:50], f'private/artifacts/weekly_brief_{today}.pdf')
LinkedInDrafts().generate_drafts(all_items[:10], f'private/artifacts/linkedin_drafts_{today}.json')
PresentationPoints().generate_points(all_items, f'private/artifacts/presentation_points_{today}.json')

print('Weekly artifacts generated successfully')
"

# 3. Verify weekly outputs
ls -lah private/artifacts/
ls -lah docs/public/data/trends_30d.json
```

### Step 11: Interactive Testing

```bash
# Open a shell inside the container for interactive testing
docker-compose exec pipeline /bin/bash

# Inside container, you can:
# - Run Python scripts: python src/main.py --mode daily
# - Run tests: pytest tests/ -v
# - Inspect files: cat config/sources.yaml
# - Check logs: ls -la private/feeds/

# Exit when done
exit
```

### Step 12: Monitor Logs

```bash
# Follow logs in real-time
docker-compose logs -f pipeline

# View last 100 lines
docker-compose logs --tail=100 pipeline

# View logs from all services
docker-compose logs -f
```

### Step 13: Cleanup

```bash
# Stop all services
docker-compose down

# Remove volumes (including Ollama data)
docker-compose down -v

# Remove images
docker rmi ai-security-intelligence-engine_pipeline

# Clean all Docker resources (careful!)
docker system prune -a
```

## Troubleshooting

### Issue: Container exits immediately

```bash
# Check logs
docker-compose logs pipeline

# Common causes:
# - Missing dependencies (rebuild with --no-cache)
# - Python errors (check syntax in source files)
```

### Issue: Tests fail inside container

```bash
# Check Python path
docker-compose exec pipeline python -c "import sys; print(sys.path)"

# Run with verbose output
docker-compose exec pipeline pytest tests/ -vv

# Check specific failing test
docker-compose exec pipeline pytest tests/test_processors.py::test_name -vv
```

### Issue: Ollama not responding

```bash
# Check Ollama logs
docker-compose logs ollama

# Verify Ollama is healthy
docker-compose exec ollama ollama list

# Manually pull model
docker-compose exec ollama ollama pull llama3.2
```

### Issue: Port 8080 already in use

```bash
# Edit docker-compose.yml and change port
# Change "8080:80" to "8081:80"

# Or kill process using port 8080
lsof -ti:8080 | xargs kill -9
```

### Issue: Permission errors

```bash
# Fix file permissions
chmod -R 755 config/ src/ tests/
chmod -R 777 private/ docs/public/data/

# Or run container as current user
docker-compose run --user $(id -u):$(id -g) pipeline python src/main.py
```

## Performance Benchmarks

**Without Ollama (Fallback mode):**
- Build time: ~30 seconds
- Pipeline execution: ~5-10 seconds (0 items), ~30-60 seconds (100 items)
- Memory: ~200 MB
- Disk: ~500 MB

**With Ollama:**
- Build time: ~30 seconds
- Ollama startup: ~2-3 minutes (first time), ~10 seconds (subsequent)
- Pipeline execution: ~30-60 seconds (0 items), ~5-10 minutes (100 items)
- Memory: ~2 GB (Ollama model loaded)
- Disk: ~4 GB (model storage)

## CI/CD Testing

```bash
# Run in CI mode (non-interactive)
docker-compose run --rm pipeline pytest tests/ --junitxml=test-results.xml

# Check exit code
echo $?
# 0 = all tests passed
# 1 = some tests failed
```

## Next Steps After Testing

Once you've verified everything works in Docker:

1. **For local development**: Continue using Docker or switch to local Python venv
2. **For production**: Push to GitHub and let GitHub Actions run the pipeline
3. **For deployment**: Use the Docker images in your production environment

## Security Notes

- Docker containers run as root by default - consider using non-root user for production
- Ollama model data is stored in named volume - backup if needed
- Private outputs are mounted to host - ensure `.gitignore` is configured correctly
- Never commit `.env` files with secrets to the repository

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Ollama Documentation](https://ollama.ai/docs)
