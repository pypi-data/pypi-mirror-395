"""Cost analysis and aggregation logic.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from collections import defaultdict
from typing import Any, Literal

from aws_bedrock_cost_tool.core.models import CostData, DailyCost, ModelCost, UsageBreakdown

DetailLevel = Literal["basic", "standard", "full"]


def analyze_cost_data(
    response: dict[str, Any], start_date: str, end_date: str, detail: DetailLevel = "standard"
) -> CostData:
    """Analyze Cost Explorer response and aggregate costs by detail level.

    Args:
        response: Raw Cost Explorer API response
        start_date: Period start date (YYYY-MM-DD)
        end_date: Period end date (YYYY-MM-DD)
        detail: Detail level for aggregation (basic/standard/full)

    Returns:
        Analyzed and aggregated cost data
    """
    results_by_time = response.get("ResultsByTime", [])

    # Extract daily costs
    daily_costs: list[DailyCost] = []
    has_estimated = False

    for result in results_by_time:
        date_str = result["TimePeriod"]["Start"]
        is_estimated = result.get("Estimated", False)

        if is_estimated:
            has_estimated = True

        # Process groups for this day
        day_models = _process_daily_groups(result.get("Groups", []), is_estimated, detail)

        # Calculate daily total
        day_total = sum(m["total_cost"] for m in day_models)

        daily_costs.append(
            DailyCost(
                date=date_str,
                total_cost=day_total,
                estimated=is_estimated,
                models=day_models,
            )
        )

    # Aggregate across all days for overall model costs
    overall_models = _aggregate_models_across_days(daily_costs)

    # Calculate total cost
    total_cost = sum(m["total_cost"] for m in overall_models)

    return CostData(
        period_start=start_date,
        period_end=end_date,
        total_cost=total_cost,
        has_estimated=has_estimated,
        daily_costs=daily_costs,
        models=overall_models,
    )


def _process_daily_groups(
    groups: list[dict[str, Any]], is_estimated: bool, detail: DetailLevel
) -> list[ModelCost]:
    """Process groups for a single day and aggregate by model.

    Args:
        groups: Cost Explorer groups for one day
        is_estimated: Whether costs are estimated
        detail: Detail level for aggregation

    Returns:
        List of model costs for the day
    """
    # Group by model
    model_data: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"cost": 0.0, "usage_types": defaultdict(lambda: {"cost": 0.0, "quantity": 0.0})}
    )

    for group in groups:
        keys = group.get("Keys", [])
        if len(keys) < 2:
            continue

        model_name = keys[0]
        usage_type = keys[1]

        metrics = group.get("Metrics", {})
        cost = float(metrics.get("BlendedCost", {}).get("Amount", 0))
        quantity = float(metrics.get("UsageQuantity", {}).get("Amount", 0))

        model_data[model_name]["cost"] += cost
        model_data[model_name]["usage_types"][usage_type]["cost"] += cost
        model_data[model_name]["usage_types"][usage_type]["quantity"] += quantity

    # Build model cost objects
    models: list[ModelCost] = []

    for model_name, data in model_data.items():
        # Build usage breakdown if needed
        usage_breakdown: list[UsageBreakdown] = []

        if detail in ["standard", "full"]:
            for usage_type, usage_data in data["usage_types"].items():
                usage_breakdown.append(
                    UsageBreakdown(
                        usage_type=usage_type,
                        cost=usage_data["cost"],
                        quantity=usage_data["quantity"],
                        estimated=is_estimated,
                    )
                )

        # Regional breakdown only for full detail
        regional_breakdown = None
        if detail == "full":
            regional_breakdown = _extract_regional_breakdown(data["usage_types"])

        models.append(
            ModelCost(
                model_name=model_name,
                total_cost=data["cost"],
                estimated=is_estimated,
                usage_breakdown=usage_breakdown,
                regional_breakdown=regional_breakdown,
            )
        )

    return models


def _extract_regional_breakdown(usage_types: dict[str, dict[str, float]]) -> dict[str, float]:
    """Extract regional cost breakdown from usage types.

    Usage types contain regional prefixes like USE1, EUC1, etc.

    Args:
        usage_types: Dictionary of usage type data

    Returns:
        Dictionary mapping region codes to costs
    """
    regions: dict[str, float] = defaultdict(float)

    for usage_type, data in usage_types.items():
        # Extract region prefix (e.g., USE1-MP, EUC1-MP)
        parts = usage_type.split("-")
        if parts:
            region = parts[0]
            regions[region] += data["cost"]

    return dict(regions)


def _aggregate_models_across_days(daily_costs: list[DailyCost]) -> list[ModelCost]:
    """Aggregate model costs across all days.

    Args:
        daily_costs: List of daily cost data

    Returns:
        List of aggregated model costs
    """
    model_agg: dict[str, dict[str, Any]] = defaultdict(
        lambda: {
            "cost": 0.0,
            "estimated": False,
            "usage_breakdown": defaultdict(
                lambda: {"cost": 0.0, "quantity": 0.0, "estimated": False}
            ),
            "regional_breakdown": defaultdict(float),
        }
    )

    for day in daily_costs:
        for model in day["models"]:
            model_name = model["model_name"]

            model_agg[model_name]["cost"] += model["total_cost"]
            model_agg[model_name]["estimated"] = (
                model_agg[model_name]["estimated"] or model["estimated"]
            )

            # Aggregate usage breakdown
            for usage in model["usage_breakdown"]:
                usage_type = usage["usage_type"]
                model_agg[model_name]["usage_breakdown"][usage_type]["cost"] += usage["cost"]
                model_agg[model_name]["usage_breakdown"][usage_type]["quantity"] += usage[
                    "quantity"
                ]
                model_agg[model_name]["usage_breakdown"][usage_type]["estimated"] = (
                    model_agg[model_name]["usage_breakdown"][usage_type]["estimated"]
                    or usage["estimated"]
                )

            # Aggregate regional breakdown
            if model["regional_breakdown"]:
                for region, cost in model["regional_breakdown"].items():
                    model_agg[model_name]["regional_breakdown"][region] += cost

    # Build final model list
    models: list[ModelCost] = []

    for model_name, data in model_agg.items():
        usage_breakdown: list[UsageBreakdown] = [
            UsageBreakdown(
                usage_type=usage_type,
                cost=usage_data["cost"],
                quantity=usage_data["quantity"],
                estimated=usage_data["estimated"],
            )
            for usage_type, usage_data in data["usage_breakdown"].items()
        ]

        regional_breakdown = (
            dict(data["regional_breakdown"]) if data["regional_breakdown"] else None
        )

        models.append(
            ModelCost(
                model_name=model_name,
                total_cost=data["cost"],
                estimated=data["estimated"],
                usage_breakdown=usage_breakdown,
                regional_breakdown=regional_breakdown,
            )
        )

    # Sort by cost (descending)
    models.sort(key=lambda m: m["total_cost"], reverse=True)

    return models
