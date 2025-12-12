"""Data models for AWS Bedrock cost analysis.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from typing import TypedDict


class UsageBreakdown(TypedDict):
    """Usage breakdown by type (input/output tokens, cache).

    Note: quantity is in millions of tokens as returned by AWS Cost Explorer.
    """

    usage_type: str
    cost: float
    quantity: float  # Millions of tokens
    estimated: bool


class ModelCost(TypedDict):
    """Cost information for a single model."""

    model_name: str
    total_cost: float
    estimated: bool
    usage_breakdown: list[UsageBreakdown]
    regional_breakdown: dict[str, float] | None


class DailyCost(TypedDict):
    """Cost for a single day."""

    date: str
    total_cost: float
    estimated: bool
    models: list[ModelCost]


class CostData(TypedDict):
    """Complete cost analysis data."""

    period_start: str
    period_end: str
    total_cost: float
    has_estimated: bool
    daily_costs: list[DailyCost]
    models: list[ModelCost]


class CostSummary(TypedDict):
    """Quick cost summary."""

    total_cost: float
    top_models: list[tuple[str, float]]  # (model_name, cost)
    period_start: str
    period_end: str
    has_estimated: bool
