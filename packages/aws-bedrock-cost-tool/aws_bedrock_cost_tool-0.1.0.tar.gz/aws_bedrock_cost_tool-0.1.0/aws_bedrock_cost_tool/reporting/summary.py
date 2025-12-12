"""Quick summary output formatting.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from aws_bedrock_cost_tool.core.models import CostData


def _format_tokens(tokens_millions: float) -> str:
    """Format token count in millions with appropriate precision.

    Args:
        tokens_millions: Token count in millions

    Returns:
        Formatted string like "~64M tokens" or "~1.2M tokens"
    """
    if tokens_millions >= 1.0:
        return f"~{tokens_millions:.0f}M tokens"
    elif tokens_millions >= 0.01:
        return f"~{tokens_millions:.2f}M tokens"
    else:
        return f"~{tokens_millions:.3f}M tokens"


def format_summary(cost_data: CostData) -> str:
    """Format cost data as summary string.

    Shows total cost and all models with their costs and token usage.

    Args:
        cost_data: Analyzed cost data

    Returns:
        Summary string with total and all models
    """
    lines = []

    # Format total cost with estimated indicator
    if cost_data["has_estimated"]:
        total_str = f"~${cost_data['total_cost']:.2f}"
    else:
        total_str = f"${cost_data['total_cost']:.2f}"

    lines.append(f"Total: {total_str}")
    lines.append("")

    models = cost_data["models"]

    if not models:
        lines.append("No Bedrock usage found")
        return "\n".join(lines)

    # Format all models
    lines.append("Models:")
    for model in models:
        # Shorten model name (remove " (Amazon Bedrock Edition)")
        short_name = model["model_name"].replace(" (Amazon Bedrock Edition)", "")

        # Add estimated indicator if needed
        if model["estimated"]:
            cost_str = f"~${model['total_cost']:.2f}"
        else:
            cost_str = f"${model['total_cost']:.2f}"

        # Calculate tokens from usage breakdown (quantity is in millions)
        usage_breakdown = model.get("usage_breakdown", [])

        # Input/output tokens (not cache)
        io_tokens = sum(
            usage["quantity"]
            for usage in usage_breakdown
            if (
                "InputTokenCount" in usage["usage_type"]
                or "OutputTokenCount" in usage["usage_type"]
            )
            and "Cache" not in usage["usage_type"]
        )

        # Cache read tokens
        cache_read_tokens = sum(
            usage["quantity"] for usage in usage_breakdown if "CacheRead" in usage["usage_type"]
        )

        # Cache write tokens
        cache_write_tokens = sum(
            usage["quantity"] for usage in usage_breakdown if "CacheWrite" in usage["usage_type"]
        )

        # Build token info parts
        token_parts = []
        if io_tokens > 0:
            token_parts.append(_format_tokens(io_tokens))
        if cache_read_tokens > 0:
            token_parts.append(f"cache read: {_format_tokens(cache_read_tokens)}")
        if cache_write_tokens > 0:
            token_parts.append(f"cache write: {_format_tokens(cache_write_tokens)}")

        if token_parts:
            lines.append(f"  {short_name}: {cost_str} ({', '.join(token_parts)})")
        else:
            lines.append(f"  {short_name}: {cost_str}")

    return "\n".join(lines)
