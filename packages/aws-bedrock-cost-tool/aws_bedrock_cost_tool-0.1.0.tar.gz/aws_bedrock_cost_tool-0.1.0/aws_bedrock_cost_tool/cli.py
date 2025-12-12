"""CLI entry point for aws-bedrock-cost-tool.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import sys

import click

from aws_bedrock_cost_tool.core.analyzer import DetailLevel, analyze_cost_data
from aws_bedrock_cost_tool.core.cost_explorer import (
    CredentialsError,
    PermissionError,
    create_cost_explorer_client,
    query_bedrock_costs,
)
from aws_bedrock_cost_tool.logging_config import get_logger, setup_logging
from aws_bedrock_cost_tool.reporting.iterm2_plots import (
    is_iterm2,
    plot_all_iterm2,
    plot_model_costs_iterm2,
    plot_time_series_iterm2,
)
from aws_bedrock_cost_tool.reporting.json_formatter import format_as_json
from aws_bedrock_cost_tool.reporting.plots import plot_model_bar_chart, plot_time_series
from aws_bedrock_cost_tool.reporting.summary import format_summary
from aws_bedrock_cost_tool.reporting.table_renderer import render_table
from aws_bedrock_cost_tool.utils import (
    PeriodParseError,
    PeriodValidationError,
    calculate_date_range,
    format_date_for_aws,
    parse_period,
    validate_period,
)

logger = get_logger(__name__)


@click.command()
@click.version_option(version="0.1.0")
@click.option(
    "--period",
    default="30d",
    help="Period to analyze (e.g., 7d, 2w, 1m, 3m). Max: 365d. Default: 30d.",
)
@click.option(
    "--profile",
    help="AWS profile name (overrides AWS_PROFILE environment variable)",
)
@click.option(
    "--detail",
    type=click.Choice(["basic", "standard", "full"]),
    default="standard",
    help=(
        "Detail level: basic (models only), standard (+ usage types), "
        "full (+ regions). Default: standard."
    ),
)
@click.option(
    "--table",
    is_flag=True,
    help="Show summary table instead of JSON output",
)
@click.option(
    "--plot-time",
    is_flag=True,
    help="Show time series plot of daily costs instead of JSON output",
)
@click.option(
    "--plot-models",
    is_flag=True,
    help="Show bar chart of model costs instead of JSON output",
)
@click.option(
    "--all-visual",
    is_flag=True,
    help="Show all visualizations (table + time series + bar chart) instead of JSON output",
)
@click.option(
    "--plot-image",
    is_flag=True,
    help="Show matplotlib plots inline in iTerm2 (high-quality graphics)",
)
@click.option(
    "--summary",
    is_flag=True,
    help="Show summary with total, all models, token usage, and cache statistics",
)
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Enable verbose output (use -v for INFO, -vv for DEBUG, -vvv for TRACE)",
)
@click.option(
    "--quiet",
    "-q",
    is_flag=True,
    help="Suppress informational messages",
)
def main(
    period: str,
    profile: str | None,
    detail: DetailLevel,
    table: bool,
    plot_time: bool,
    plot_models: bool,
    all_visual: bool,
    plot_image: bool,
    summary: bool,
    verbose: int,
    quiet: bool,
) -> None:
    """AWS Bedrock Cost Analysis Tool

    Analyzes AWS Bedrock model costs using Cost Explorer API.
    Supports multiple output formats: JSON (default), tables, plots, and summaries.

    Examples:

    \b
    # Default: JSON output for last 30 days
    aws-bedrock-cost-tool

    \b
    # Summary with all models
    aws-bedrock-cost-tool --summary

    \b
    # Visual table for last 90 days
    aws-bedrock-cost-tool --period 90d --table

    \b
    # Full report with all visualizations
    aws-bedrock-cost-tool --all-visual --detail full

    \b
    # Last 2 weeks with specific profile
    aws-bedrock-cost-tool --period 2w --profile production

    \b
    # Time series plot with verbose logging
    aws-bedrock-cost-tool --plot-time -v

    \b
    # High-quality matplotlib plots in iTerm2
    aws-bedrock-cost-tool --plot-image

    \b
    # Debug mode with detailed API calls
    aws-bedrock-cost-tool --period 7d -vv

    \b
    # Trace mode with AWS SDK internals
    aws-bedrock-cost-tool --period 7d -vvv

    \b
    # Pipe JSON to jq for automation
    aws-bedrock-cost-tool | jq '.models[] | select(.model_name | contains("Sonnet"))'
    """
    # Setup logging based on verbosity
    setup_logging(verbose)
    logger.info("AWS Bedrock Cost Analysis started")

    try:
        # Parse and validate period
        logger.debug(f"Parsing period: {period}")
        days = parse_period(period)
        validate_period(days)
        logger.debug(f"Period validated: {days} days")

        # Calculate date range
        start_date, end_date = calculate_date_range(days)
        start_str = format_date_for_aws(start_date)
        end_str = format_date_for_aws(end_date)
        logger.info(f"Analyzing costs from {start_str} to {end_str}")

        # Create Cost Explorer client
        logger.debug("Creating AWS Cost Explorer client")
        client = create_cost_explorer_client(profile)
        logger.debug("Cost Explorer client created")

        # Query costs
        logger.info("Querying AWS Cost Explorer...")
        response = query_bedrock_costs(client, start_str, end_str, verbose=verbose)
        logger.info("Cost data retrieved successfully")

        # Analyze data
        logger.debug(f"Analyzing cost data with detail level: {detail}")
        cost_data = analyze_cost_data(response, start_str, end_str, detail=detail)
        logger.debug(f"Found {len(cost_data['models'])} models with costs")

        # Check for empty results
        if cost_data["total_cost"] == 0:
            if not quiet:
                logger.warning(
                    f"No Bedrock costs found for period {period} ({start_str} to {end_str})"
                )
                logger.warning(
                    "Check if Bedrock was used during this period or try a longer period"
                )
            sys.exit(0)

        # Determine output mode
        visual_mode = table or plot_time or plot_models or all_visual or plot_image or summary
        logger.debug(f"Output mode: {'visual' if visual_mode else 'JSON'}")

        if visual_mode:
            # Visual output modes
            if summary:
                logger.debug("Generating summary output")
                print(format_summary(cost_data))
            elif plot_image:
                # iTerm2 matplotlib plots
                logger.debug("Generating iTerm2 matplotlib plots")
                if not is_iterm2():
                    logger.warning("Not running in iTerm2, images may not display correctly")
                plot_all_iterm2(cost_data)
            else:
                # Check if running in iTerm2 for matplotlib plots
                use_iterm2 = is_iterm2()

                if table or all_visual:
                    logger.debug("Rendering cost table")
                    render_table(cost_data, detail=detail)

                if plot_time or all_visual:
                    if use_iterm2:
                        logger.debug("Generating iTerm2 time series plot")
                        plot_time_series_iterm2(cost_data)
                    else:
                        logger.debug("Generating ASCII time series plot")
                        plot_time_series(cost_data)

                if plot_models or all_visual:
                    if use_iterm2:
                        logger.debug("Generating iTerm2 model bar chart")
                        plot_model_costs_iterm2(cost_data)
                    else:
                        logger.debug("Generating ASCII model bar chart")
                        plot_model_bar_chart(cost_data)
        else:
            # Default: JSON to stdout
            logger.debug("Outputting JSON to stdout")
            print(format_as_json(cost_data))

        logger.info("Analysis completed successfully")

    except PeriodParseError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    except PeriodValidationError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    except CredentialsError as e:
        click.echo(f"AWS Credentials Error:\n{e}", err=True)
        sys.exit(1)

    except PermissionError as e:
        click.echo(f"AWS Permission Error:\n{e}", err=True)
        sys.exit(1)

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        logger.debug("Full traceback:", exc_info=True)
        click.echo(f"Unexpected error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
