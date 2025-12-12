"""Utility functions for aws-bedrock-cost-tool.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import re
from datetime import date, timedelta


class PeriodParseError(Exception):
    """Raised when period parsing fails."""

    pass


class PeriodValidationError(Exception):
    """Raised when period validation fails."""

    pass


def parse_period(period_str: str) -> int:
    """Parse period string to number of days.

    Supports flexible duration syntax:
    - Nd: N days (e.g., 7d, 30d)
    - Nw: N weeks (e.g., 2w, 4w)
    - Nm: N months (approx 30 days each, e.g., 1m, 3m)

    Args:
        period_str: Period string in format Nd, Nw, or Nm

    Returns:
        Number of days

    Raises:
        PeriodParseError: If period format is invalid
    """
    pattern = r"^(\d+)([dwm])$"
    match = re.match(pattern, period_str.lower())

    if not match:
        raise PeriodParseError(
            f"Invalid period format '{period_str}'. "
            f"Use: 7d (days), 2w (weeks), 1m (months). "
            f"Examples: 7d, 2w, 1m, 3m, 90d"
        )

    value, unit = match.groups()
    num_value = int(value)

    if unit == "d":
        return num_value
    elif unit == "w":
        return num_value * 7
    elif unit == "m":
        return num_value * 30
    else:
        # Should never reach here due to regex
        raise PeriodParseError(f"Unknown unit: {unit}")


def validate_period(days: int) -> None:
    """Validate period is within acceptable range.

    Args:
        days: Number of days to validate

    Raises:
        PeriodValidationError: If period exceeds maximum (365 days)
    """
    max_days = 365

    if days <= 0:
        raise PeriodValidationError(
            f"Period must be positive, got {days} days. Try: aws-bedrock-cost-tool --period 7d"
        )

    if days > max_days:
        raise PeriodValidationError(
            f"Period {days}d exceeds maximum allowed ({max_days}d). "
            f"Try: aws-bedrock-cost-tool --period 365d"
        )


def calculate_date_range(days: int) -> tuple[date, date]:
    """Calculate start and end dates from period in days.

    End date is today, start date is today minus the specified number of days.

    Args:
        days: Number of days to look back

    Returns:
        Tuple of (start_date, end_date)
    """
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    return start_date, end_date


def format_date_for_aws(d: date) -> str:
    """Format date for AWS Cost Explorer API.

    Args:
        d: Date to format

    Returns:
        Date string in YYYY-MM-DD format
    """
    return d.strftime("%Y-%m-%d")
