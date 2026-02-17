# Content Taxonomy

Tag definitions and scoring weight rationale for the AI Security Intelligence Engine.

## Tags

### agentic_systems
**Description**: Security of autonomous AI agents, tool calling, function execution

**Keywords**: agent, agentic, tool calling, function calling, autonomous, multi-agent

**Use Cases**: Agent security frameworks, tool injection attacks, agent observability

### prompt_injection
**Description**: Prompt injection attacks, jailbreaks, adversarial prompts

**Keywords**: prompt injection, jailbreak, adversarial prompts, indirect injection, instruction injection

**Use Cases**: Prompt attack techniques, defenses, detection methods

### hitl
**Description**: Human-in-the-loop designs, oversight, kill switches

**Keywords**: HITL, human-in-the-loop, human oversight, kill switch, circuit breaker, approval workflow

**Use Cases**: Human oversight patterns, approval workflows, safety controls

### observability
**Description**: Logging, tracing, monitoring, audit trails for AI systems

**Keywords**: observability, logging, tracing, monitoring, audit trail, tool call tracking

**Use Cases**: AI system monitoring, debugging, compliance auditing

### shadow_ai
**Description**: Unauthorized AI use, governance, asset inventory

**Keywords**: shadow AI, rogue AI, unauthorized model, governance, model registry

**Use Cases**: AI governance, asset management, policy enforcement

### data_leakage
**Description**: Data exfiltration, privacy breaches, PII exposure

**Keywords**: data exfiltration, data leakage, information disclosure, PII exposure

**Use Cases**: Data protection, privacy controls, leakage prevention

### model_supply_chain
**Description**: Model poisoning, supply chain attacks, checkpoint integrity

**Keywords**: model poisoning, supply chain, pre-trained model, checkpoint integrity

**Use Cases**: Supply chain security, model verification, dependency management

### vuln_exploit
**Description**: Vulnerabilities, exploits, CVEs, security patches

**Keywords**: vulnerability, exploit, CVE, security patch, zero-day, critical flaw

**Use Cases**: Vulnerability tracking, patch management, exploit analysis

### regulatory
**Description**: Compliance, regulations, standards, governance policies

**Keywords**: regulatory, compliance, NIST, EU AI Act, OSFI, policy, governance

**Use Cases**: Regulatory compliance, policy implementation, standard adoption

## Scoring Dimensions

### Relevance (Weight: 0.35)
**What it measures**: Topical match to priority AI security areas

**Why this weight**: Most important dimension - content must be relevant to be useful

### Credibility (Weight: 0.25)
**What it measures**: Source authority and research quality

**Why this weight**: Second most important - trustworthy sources produce reliable insights

### Impact (Weight: 0.15)
**What it measures**: Severity, affected users, real-world consequences

**Why this weight**: Moderate importance - high-impact events warrant attention

### Freshness (Weight: 0.15)
**What it measures**: Recency of publication

**Why this weight**: Moderate importance - AI security evolves rapidly, recent content valued

### Practicality (Weight: 0.10)
**What it measures**: Actionable defender insights and mitigations

**Why this weight**: Important but not primary - not all valuable content has immediate mitigations

## Customizing Weights

Edit `config/scoring_weights.yaml` to adjust dimension weights or tag keywords.

Weights must sum to 1.0 for proper normalization.
