"""Table rendering with termtables.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import sys

import termtables as tt  # type: ignore[import-untyped]

from aws_bedrock_cost_tool.core.analyzer import DetailLevel
from aws_bedrock_cost_tool.core.models import CostData


def render_table(cost_data: CostData, detail: DetailLevel = "standard") -> None:
    """Render cost data as formatted table to stderr.

    Args:
        cost_data: Analyzed cost data
        detail: Detail level (basic/standard/full)
    """
    # Print header
    print("\nAWS Bedrock Cost Report", file=sys.stderr)
    print(f"Period: {cost_data['period_start']} to {cost_data['period_end']}", file=sys.stderr)

    if cost_data["has_estimated"]:
        print("Note: ~ indicates estimated costs (data not yet finalized)", file=sys.stderr)

    print(
        f"\nTotal Cost: {_format_cost(cost_data['total_cost'], cost_data['has_estimated'])}",
        file=sys.stderr,
    )

    if not cost_data["models"]:
        print("\nNo Bedrock usage found for this period.", file=sys.stderr)
        return

    # Render based on detail level
    if detail == "basic":
        _render_basic_table(cost_data)
    elif detail == "standard":
        _render_standard_table(cost_data)
    elif detail == "full":
        _render_full_table(cost_data)


def _render_basic_table(cost_data: CostData) -> None:
    """Render basic model totals table."""
    print("\n## Model Costs", file=sys.stderr)

    headers = ["Model", "Total Cost"]
    rows = []

    for model in cost_data["models"]:
        model_name = _shorten_model_name(model["model_name"])
        cost = _format_cost(model["total_cost"], model["estimated"])
        rows.append([model_name, cost])

    table_str = tt.to_string(rows, header=headers, style=tt.styles.rounded)
    print(table_str, file=sys.stderr)


def _render_standard_table(cost_data: CostData) -> None:
    """Render table with usage type breakdown."""
    print("\n## Model Costs with Usage Breakdown", file=sys.stderr)

    for model in cost_data["models"]:
        model_name = _shorten_model_name(model["model_name"])
        total_cost = _format_cost(model["total_cost"], model["estimated"])

        print(f"\n### {model_name} (Total: {total_cost})", file=sys.stderr)

        if model["usage_breakdown"]:
            headers = ["Usage Type", "Cost", "Tokens (M)"]
            rows = []

            for usage in model["usage_breakdown"]:
                usage_type = _shorten_usage_type(usage["usage_type"])
                cost = _format_cost(usage["cost"], usage["estimated"])
                quantity = f"{usage['quantity']:.3f}"
                rows.append([usage_type, cost, quantity])

            table_str = tt.to_string(rows, header=headers, style=tt.styles.rounded)
            print(table_str, file=sys.stderr)


def _render_full_table(cost_data: CostData) -> None:
    """Render table with full breakdown (usage types + regions)."""
    print("\n## Model Costs with Full Breakdown", file=sys.stderr)

    for model in cost_data["models"]:
        model_name = _shorten_model_name(model["model_name"])
        total_cost = _format_cost(model["total_cost"], model["estimated"])

        print(f"\n### {model_name} (Total: {total_cost})", file=sys.stderr)

        # Usage breakdown
        if model["usage_breakdown"]:
            print("\nUsage Breakdown:", file=sys.stderr)
            headers = ["Usage Type", "Cost", "Tokens (M)"]
            rows = []

            for usage in model["usage_breakdown"]:
                usage_type = _shorten_usage_type(usage["usage_type"])
                cost = _format_cost(usage["cost"], usage["estimated"])
                quantity = f"{usage['quantity']:.3f}"
                rows.append([usage_type, cost, quantity])

            table_str = tt.to_string(rows, header=headers, style=tt.styles.rounded)
            print(table_str, file=sys.stderr)

        # Regional breakdown
        if model["regional_breakdown"]:
            print("\nRegional Breakdown:", file=sys.stderr)
            headers_region = ["Region", "Cost"]
            rows_region: list[list[str]] = []

            for region, region_cost in sorted(model["regional_breakdown"].items()):
                cost_str = f"${region_cost:.2f}"
                rows_region.append([region, cost_str])

            table_str = tt.to_string(rows_region, header=headers_region, style=tt.styles.rounded)
            print(table_str, file=sys.stderr)


def _format_cost(cost: float, estimated: bool) -> str:
    """Format cost with estimated indicator.

    Args:
        cost: Cost amount
        estimated: Whether cost is estimated

    Returns:
        Formatted cost string (e.g., "$12.34" or "~$12.34")
    """
    if estimated:
        return f"~${cost:.2f}"
    return f"${cost:.2f}"


def _shorten_model_name(model_name: str) -> str:
    """Shorten model name by removing common suffix.

    Args:
        model_name: Full model name

    Returns:
        Shortened model name
    """
    return model_name.replace(" (Amazon Bedrock Edition)", "")


def _shorten_usage_type(usage_type: str) -> str:
    """Shorten usage type for display.

    Simplifies long usage type strings while preserving key information.

    Args:
        usage_type: Full usage type string

    Returns:
        Shortened usage type
    """
    # Remove region prefix but keep the rest
    # e.g., "USE1-MP:USE1_InputTokenCount-Units" -> "InputTokenCount"
    parts = usage_type.split(":")
    if len(parts) > 1:
        # Take second part and remove trailing info
        simplified = parts[1].replace("_Global-Units", "").replace("-Units", "")
        # Remove region prefix from the second part too
        simplified = simplified.split("_", 1)[-1] if "_" in simplified else simplified
        return simplified

    return usage_type
