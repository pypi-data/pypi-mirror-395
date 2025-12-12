"""aws-bedrock-cost-tool: A CLI tool that reports on the cost per model on AWS Bedrock

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from aws_bedrock_cost_tool.core.analyzer import analyze_cost_data
from aws_bedrock_cost_tool.core.cost_explorer import (
    create_cost_explorer_client,
    get_bedrock_models,
    query_bedrock_costs,
)
from aws_bedrock_cost_tool.core.models import (
    CostData,
    CostSummary,
    DailyCost,
    ModelCost,
    UsageBreakdown,
)
from aws_bedrock_cost_tool.logging_config import get_logger, setup_logging
from aws_bedrock_cost_tool.utils import (
    calculate_date_range,
    format_date_for_aws,
    parse_period,
    validate_period,
)

__version__ = "0.1.0"

__all__ = [
    "__version__",
    # Core analysis
    "analyze_cost_data",
    "create_cost_explorer_client",
    "query_bedrock_costs",
    "get_bedrock_models",
    # Data models
    "CostData",
    "CostSummary",
    "DailyCost",
    "ModelCost",
    "UsageBreakdown",
    # Utilities
    "parse_period",
    "validate_period",
    "calculate_date_range",
    "format_date_for_aws",
    # Logging
    "setup_logging",
    "get_logger",
]
