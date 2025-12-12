"""ASCII plotting with termplotlib.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import sys

import termplotlib as tpl  # type: ignore[import-untyped]

from aws_bedrock_cost_tool.core.models import CostData


def plot_time_series(cost_data: CostData) -> None:
    """Plot time series of daily costs to stderr.

    Args:
        cost_data: Analyzed cost data
    """
    if not cost_data["daily_costs"]:
        print("\nNo daily cost data available for plotting.", file=sys.stderr)
        return

    # Extract dates and costs
    dates = [day["date"] for day in cost_data["daily_costs"]]
    costs = [day["total_cost"] for day in cost_data["daily_costs"]]

    print("\n## Daily Bedrock Costs Over Time", file=sys.stderr)

    try:
        # Create figure
        fig = tpl.figure()
        fig.plot(list(range(len(costs))), costs, xlabel="Day", label="Daily Cost ($)")

        # Show the plot to stderr
        print(fig.get_string(), file=sys.stderr)

        # Print date labels
        print("\nDate labels:", file=sys.stderr)
        for i, date in enumerate(dates):
            print(f"  Day {i}: {date}", file=sys.stderr)
    except FileNotFoundError as e:
        if "gnuplot" in str(e):
            print("\nError: gnuplot is required for plotting but not installed.", file=sys.stderr)
            print("Install gnuplot:", file=sys.stderr)
            print("  macOS:   brew install gnuplot", file=sys.stderr)
            print("  Ubuntu:  sudo apt-get install gnuplot", file=sys.stderr)
            print("  Windows: choco install gnuplot", file=sys.stderr)
        else:
            raise


def plot_model_bar_chart(cost_data: CostData, top_n: int = 10) -> None:
    """Plot bar chart of model costs to stderr.

    Args:
        cost_data: Analyzed cost data
        top_n: Number of top models to display (default: 10)
    """
    if not cost_data["models"]:
        print("\nNo model cost data available for plotting.", file=sys.stderr)
        return

    # Get top N models
    top_models = cost_data["models"][:top_n]

    model_names = [_shorten_model_name(m["model_name"]) for m in top_models]
    costs = [m["total_cost"] for m in top_models]

    print(f"\n## Top {len(top_models)} Models by Cost", file=sys.stderr)

    try:
        # Create horizontal bar chart
        fig = tpl.figure()
        fig.barh(costs, model_names, force_ascii=True)

        # Show the plot to stderr
        print(fig.get_string(), file=sys.stderr)
    except FileNotFoundError as e:
        if "gnuplot" in str(e):
            print("\nError: gnuplot is required for plotting but not installed.", file=sys.stderr)
            print("Install gnuplot:", file=sys.stderr)
            print("  macOS:   brew install gnuplot", file=sys.stderr)
            print("  Ubuntu:  sudo apt-get install gnuplot", file=sys.stderr)
            print("  Windows: choco install gnuplot", file=sys.stderr)
        else:
            raise


def _shorten_model_name(model_name: str) -> str:
    """Shorten model name for display.

    Args:
        model_name: Full model name

    Returns:
        Shortened model name (max 30 chars)
    """
    short = model_name.replace(" (Amazon Bedrock Edition)", "")

    # Truncate if still too long
    if len(short) > 30:
        short = short[:27] + "..."

    return short
