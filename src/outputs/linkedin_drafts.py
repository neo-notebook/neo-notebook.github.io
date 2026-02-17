"""
LinkedIn post draft generator.
"""
import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
from src.utils.logger import get_logger

logger = get_logger(__name__)


class LinkedInDrafts:
    """Generate LinkedIn post drafts in different tones."""

    def __init__(self):
        """Initialize LinkedIn draft generator."""
        pass

    def generate_drafts(self,
                         items: List[Dict[str, Any]],
                         output_path: str,
                         num_drafts: int = 3) -> None:
        """
        Generate LinkedIn post drafts from weekly items.

        Args:
            items: List of top items from the week
            output_path: Path to save drafts JSON
            num_drafts: Number of draft variations to generate
        """
        # Get top 3-5 items
        top_items = items[:5]

        drafts = []

        # Draft 1: Practical/Technical tone
        if len(top_items) > 0:
            item = top_items[0]
            drafts.append({
                'tone': 'practical',
                'content': f"""🔐 AI Security Update: {item.get('title', 'New Development')}

{item.get('summary', 'Details limited')}

{item.get('why_it_matters', 'Important for enterprise defenders')}

Key Action: {item.get('practical_mitigation', 'Review and assess impact')}

#AISSecurity #EnterpriseDefense #CyberSecurity"""
            })

        # Draft 2: Research-focused tone
        if len(top_items) > 1:
            item = top_items[1]
            drafts.append({
                'tone': 'research',
                'content': f"""📚 Interesting research on AI security:

"{item.get('title', 'Research update')}"

{item.get('summary', 'Details limited')}

This highlights the evolving landscape of AI security threats and defenses.

Source: {item.get('source', 'Research community')}

#AIResearch #SecurityResearch #MachineLearning"""
            })

        # Draft 3: Leadership/Strategic tone
        if len(top_items) > 2:
            draft3_items = top_items[:3]
            titles = '\\n- '.join([item.get('title', '')[:60] + '...' for item in draft3_items])
            drafts.append({
                'tone': 'leadership',
                'content': f"""🎯 AI Security Trends This Week:

Key developments security leaders should watch:

- {titles}

The AI security landscape is rapidly evolving. Organizations need proactive strategies to manage these emerging risks.

How is your team adapting?

#Leadership #AIGovernance #RiskManagement"""
            })

        # Save drafts
        output = {
            'generated_at': datetime.now().isoformat(),
            'drafts': drafts
        }

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2)

        logger.info(f"Generated {len(drafts)} LinkedIn drafts: {output_path}")
