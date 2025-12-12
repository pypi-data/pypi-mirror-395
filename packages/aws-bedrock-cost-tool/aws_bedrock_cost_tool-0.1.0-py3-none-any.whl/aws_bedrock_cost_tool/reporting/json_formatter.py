"""JSON output formatting.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import json

from aws_bedrock_cost_tool.core.models import CostData


def format_as_json(cost_data: CostData) -> str:
    """Format cost data as JSON string.

    Args:
        cost_data: Analyzed cost data

    Returns:
        JSON string representation
    """
    return json.dumps(cost_data, indent=2)
