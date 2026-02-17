# Content Sources

This document lists all configured sources for the AI Security Intelligence Engine.

## Configuration

Sources are configured in `config/sources.yaml`. Each source includes:
- **name**: Human-readable source name
- **type**: Source type (`rss` or `arxiv`)
- **url**: Feed URL (for RSS sources)
- **query**: Search query (for arXiv sources)
- **category**: Source category
- **credibility_tier**: Source credibility (`high`, `medium`, `low`)
- **enabled**: Whether source is active

## Currently Configured Sources

### Example Security Blog
- **Type**: RSS
- **URL**: https://example-security-blog.com/feed.xml
- **Category**: security_research
- **Credibility**: Medium
- **Why included**: Placeholder example source

### arXiv AI Security Research
- **Type**: arXiv
- **Query**: prompt injection OR agent security OR AI safety
- **Category**: research
- **Credibility**: High
- **Why included**: Academic research on AI security topics

## Adding New Sources

1. Edit `config/sources.yaml`
2. Add new entry with required fields
3. Set `enabled: true`
4. Test with `python src/main.py --mode daily`

## Source Categories

- **security_research**: Security research publications
- **research**: Academic papers and conferences
- **high_impact_cyber**: Major vulnerability/exploit news
- **regulatory**: Standards and compliance updates

## Credibility Tiers

- **High**: Standards bodies (NIST, OSFI), academic conferences, peer-reviewed journals
- **Medium**: Established security publications, corporate research labs
- **Low**: Individual blogs (use sparingly, require strong topical relevance)
