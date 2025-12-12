"""Tests for aws_bedrock_cost_tool.utils module.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from datetime import date, timedelta

import pytest

from aws_bedrock_cost_tool.utils import (
    PeriodParseError,
    PeriodValidationError,
    calculate_date_range,
    format_date_for_aws,
    parse_period,
    validate_period,
)


def test_parse_period_days() -> None:
    """Test parsing period in days format."""
    assert parse_period("7d") == 7
    assert parse_period("30d") == 30
    assert parse_period("90d") == 90
    assert parse_period("365d") == 365


def test_parse_period_weeks() -> None:
    """Test parsing period in weeks format."""
    assert parse_period("1w") == 7
    assert parse_period("2w") == 14
    assert parse_period("4w") == 28


def test_parse_period_months() -> None:
    """Test parsing period in months format."""
    assert parse_period("1m") == 30
    assert parse_period("3m") == 90
    assert parse_period("12m") == 360


def test_parse_period_case_insensitive() -> None:
    """Test that period parsing is case insensitive."""
    assert parse_period("7D") == 7
    assert parse_period("2W") == 14
    assert parse_period("1M") == 30


def test_parse_period_invalid_format() -> None:
    """Test that invalid period format raises PeriodParseError."""
    with pytest.raises(PeriodParseError) as exc_info:
        parse_period("7x")
    assert "Invalid period format" in str(exc_info.value)
    assert "7x" in str(exc_info.value)

    with pytest.raises(PeriodParseError):
        parse_period("invalid")

    with pytest.raises(PeriodParseError):
        parse_period("d7")


def test_validate_period_positive() -> None:
    """Test that positive periods are valid."""
    # Should not raise
    validate_period(1)
    validate_period(7)
    validate_period(30)
    validate_period(365)


def test_validate_period_zero() -> None:
    """Test that zero period raises PeriodValidationError."""
    with pytest.raises(PeriodValidationError) as exc_info:
        validate_period(0)
    assert "must be positive" in str(exc_info.value)


def test_validate_period_negative() -> None:
    """Test that negative period raises PeriodValidationError."""
    with pytest.raises(PeriodValidationError) as exc_info:
        validate_period(-7)
    assert "must be positive" in str(exc_info.value)


def test_validate_period_exceeds_maximum() -> None:
    """Test that period exceeding 365 days raises PeriodValidationError."""
    with pytest.raises(PeriodValidationError) as exc_info:
        validate_period(400)
    assert "exceeds maximum" in str(exc_info.value)
    assert "365" in str(exc_info.value)


def test_calculate_date_range() -> None:
    """Test calculating date range from period."""
    start, end = calculate_date_range(7)

    # End should be today
    assert end == date.today()

    # Start should be 7 days before end
    assert start == end - timedelta(days=7)


def test_calculate_date_range_30_days() -> None:
    """Test calculating 30-day date range."""
    start, end = calculate_date_range(30)

    assert end == date.today()
    assert start == end - timedelta(days=30)
    assert (end - start).days == 30


def test_format_date_for_aws() -> None:
    """Test formatting date for AWS API."""
    test_date = date(2025, 1, 15)
    formatted = format_date_for_aws(test_date)

    assert formatted == "2025-01-15"
    assert isinstance(formatted, str)


def test_format_date_for_aws_different_dates() -> None:
    """Test formatting various dates for AWS API."""
    assert format_date_for_aws(date(2024, 12, 1)) == "2024-12-01"
    assert format_date_for_aws(date(2025, 6, 30)) == "2025-06-30"
    assert format_date_for_aws(date(2025, 11, 14)) == "2025-11-14"
