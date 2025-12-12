# aws-bedrock-cost-tool - Developer Guide

## Overview

A professional CLI tool for analyzing AWS Bedrock model costs with comprehensive reporting and visualization capabilities.

### Tech Stack

- **Python**: 3.14+
- **Package Manager**: uv (fast Python tooling)
- **CLI Framework**: Click
- **AWS Integration**: boto3
- **Visualization**: termplotlib (ASCII plots), termtables (tables)
- **Type Safety**: mypy (strict mode)
- **Linting**: ruff
- **Testing**: pytest
- **Build**: hatchling

## Architecture

### Project Structure

```
aws_bedrock_cost_tool/
├── __init__.py              # Public API exports, version
├── cli.py                   # Click CLI entry point (main command)
├── utils.py                 # Period parsing, date utilities, validation
├── core/                    # Core library functions (importable, CLI-independent)
│   ├── __init__.py
│   ├── models.py           # TypedDict data models (CostData, ModelCost, etc.)
│   ├── cost_explorer.py    # boto3 Cost Explorer client wrapper
│   └── analyzer.py         # Cost aggregation and analysis logic
└── reporting/               # Reporting and visualization modules
    ├── __init__.py
    ├── json_formatter.py   # JSON output formatting
    ├── summary.py          # Summary formatting (--summary)
    ├── table_renderer.py   # termtables rendering (--table)
    └── plots.py            # termplotlib charts (--plot-time, --plot-models)
```

### Key Design Principles

1. **Separation of Concerns**: Core library functions (`core/`) are independent of CLI
2. **Exception-Based Errors**: Core functions raise exceptions (NOT sys.exit), CLI handles formatting/exit codes
3. **Importable Library**: Expose public API via `__init__.py` for programmatic use
4. **Composability**: JSON to stdout, logs/errors to stderr for piping
5. **Agent-Friendly**: Rich error messages that AI agents can parse and act upon (ReAct loops)
6. **Type Safety**: Comprehensive type hints, passes strict mypy checks

### Module Responsibilities

**utils.py**:
- `parse_period(period_str)`: Parse period strings (7d, 2w, 1m) to days
- `validate_period(days)`: Validate period is within limits (max 365 days)
- `calculate_date_range(days)`: Calculate start/end dates from period
- `format_date_for_aws(date)`: Format date for AWS API (YYYY-MM-DD)

**core/models.py**:
- TypedDict definitions for structured data
- `CostData`: Complete cost analysis result
- `ModelCost`: Cost information for a single model
- `UsageBreakdown`: Usage by type (input/output tokens, cache)
- `DailyCost`: Cost for a single day
- `CostSummary`: Quick summary data

**core/cost_explorer.py**:
- `create_cost_explorer_client(profile)`: Create boto3 Cost Explorer client
- `query_bedrock_costs(client, start, end)`: Query Cost Explorer API
- `get_bedrock_models()`: List of all Bedrock model service names
- Custom exceptions: `CredentialsError`, `PermissionError`, `CostExplorerError`

**core/analyzer.py**:
- `analyze_cost_data(response, start, end, detail)`: Analyze API response
- Detail levels: `basic` (models only), `standard` (+ usage types), `full` (+ regions)
- Aggregates costs by model, usage type, and region
- Marks estimated vs. final costs

**reporting/**:
- `json_formatter.py`: Convert `CostData` to JSON string
- `summary.py`: Format summary with all models, token usage, and cache statistics
- `table_renderer.py`: Render tables with termtables (supports all detail levels)
- `plots.py`: Create ASCII plots with termplotlib (time series, bar charts)

**cli.py**:
- Main Click command with all options
- Orchestrates: parse period → query API → analyze → output
- Error handling with informative messages
- Routes output based on flags (JSON default, visuals optional)

## CLI Commands

### Main Command

```bash
aws-bedrock-cost-tool [OPTIONS]
```

### Options

**Time Range**:
- `--period DURATION` - Period to analyze (default: 30d)
  - Format: `Nd` (days), `Nw` (weeks), `Nm` (months)
  - Examples: 7d, 2w, 1m, 3m, 90d
  - Max: 365d (enforced with clear error)

**AWS Configuration**:
- `--profile NAME` - AWS profile (overrides AWS_PROFILE env var)

**Output Modes** (mutually exclusive, suppress JSON if used):
- Default: JSON to stdout
- `--table` - Summary table (termtables)
- `--plot-time` - Time series plot, ASCII (cost over time)
- `--plot-models` - Bar chart, ASCII (cost by model)
- `--all-visual` - All ASCII visualizations (table + both plots)
- `--plot-image` - Matplotlib plots inline in iTerm2 (high-quality graphics)
- `--summary` - Summary with all models, token usage, and cache statistics

**Detail Level** (applies to all outputs):
- `--detail basic|standard|full` (default: standard)
  - `basic`: Model totals only
  - `standard`: Models + usage type breakdown
  - `full`: Models + usage types + regional breakdown

**Control Flags**:
- `--verbose` / `-V` - Log API calls and processing to stderr
- `--quiet` / `-q` - Suppress informational messages
- `--help` / `-h` - Show help with examples
- `--version` - Show version (0.1.0)

### Example Commands

```bash
# Default: JSON output, last 30 days
aws-bedrock-cost-tool

# Summary with all models, tokens, and cache
aws-bedrock-cost-tool --summary

# Visual table for last 90 days
aws-bedrock-cost-tool --period 90d --table

# Full report with all visualizations
aws-bedrock-cost-tool --all-visual --detail full

# Last 2 weeks with specific profile
aws-bedrock-cost-tool --period 2w --profile production

# Time series plot with verbose logging
aws-bedrock-cost-tool --plot-time --verbose

# High-quality matplotlib plots in iTerm2
aws-bedrock-cost-tool --plot-image

# Pipe JSON to jq for automation
aws-bedrock-cost-tool | jq '.models[] | select(.model_name | contains("Sonnet"))'
```

## Library Usage

Import and use programmatically:

```python
from aws_bedrock_cost_tool import (
    create_cost_explorer_client,
    query_bedrock_costs,
    analyze_cost_data,
    parse_period,
    calculate_date_range,
    format_date_for_aws,
)

# Parse period and calculate dates
days = parse_period("30d")
start_date, end_date = calculate_date_range(days)

# Create client and query
client = create_cost_explorer_client(profile_name="my-profile")
response = query_bedrock_costs(
    client,
    format_date_for_aws(start_date),
    format_date_for_aws(end_date),
    verbose=False
)

# Analyze data
cost_data = analyze_cost_data(response, start_date, end_date, detail="standard")

# Access results
print(f"Total: ${cost_data['total_cost']:.2f}")
for model in cost_data['models']:
    print(f"{model['model_name']}: ${model['total_cost']:.2f}")
```

## Development Commands

### Quick Start

```bash
# Clone and setup
git clone https://github.com/dnvriend/aws-bedrock-cost-tool.git
cd aws-bedrock-cost-tool

# Install dependencies
make install
```

### Quality Checks

```bash
# Format code (auto-fix style issues)
make format

# Lint (check code style)
make lint

# Type check (strict mypy)
make typecheck

# Run tests
make test

# Run all checks (lint + typecheck + test)
make check

# Full pipeline (format, lint, typecheck, test, build, install-global)
make pipeline
```

### Build & Install

```bash
# Build package
make build

# Install globally
make install-global

# Clean build artifacts
make clean
```

### Running Locally

```bash
# Run with uv (development)
make run ARGS="--period 7d --table"

# Or directly
uv run aws-bedrock-cost-tool --period 7d --table
```

## Code Standards

### Type Safety

- Use type hints for ALL functions
- Pass strict mypy checks
- Use Python 3.14+ modern syntax (dict/list over Dict/List)

### Documentation

- Module-level docstrings with AI generation acknowledgment
- Function docstrings with Args, Returns, Raises sections
- Inline comments for complex logic

### Error Handling

- Custom exceptions for specific error types
- Core functions raise exceptions (never sys.exit)
- CLI catches exceptions and formats user-friendly messages
- Include troubleshooting steps in error messages

### Code Style

- Line length: 100 characters
- Format with ruff
- Follow PEP 8 guidelines
- Use descriptive variable names

## Testing

### Running Tests

```bash
# Run all tests
make test

# Verbose output
uv run pytest tests/ -v

# Specific test file
uv run pytest tests/test_utils.py -v

# With coverage
uv run pytest tests/ --cov=aws_bedrock_cost_tool --cov-report=html
```

### Test Coverage

Current test coverage:
- `utils.py`: Period parsing, date calculations, validation
- Future: Add tests for analyzer, cost_explorer (mocking boto3)

## Important Notes

### Core Dependencies

- **boto3** (>=1.34.0): AWS SDK for Python - [Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- **click** (>=8.1.7): CLI framework - [Documentation](https://click.palletsprojects.com/)
- **termplotlib** (>=0.3.9): ASCII plotting - [GitHub](https://github.com/nschloe/termplotlib)
- **termtables** (>=0.2.4): Terminal tables - [GitHub](https://github.com/nschloe/termtables)

### AWS Cost Explorer

- **Global Service**: Cost Explorer is global, always uses `us-east-1` region for API calls
- **Cost Explorer must be enabled**: Navigate to AWS Console → Cost Explorer → Enable
- **Data Delay**: Cost data may have up to 24-hour delay
- **Regional Prefixes**: Usage types contain regional codes (USE1-MP, EUC1-MP, etc.)
- **Estimated Costs**: Recent costs are marked as estimated until finalized

### Authentication

- Supports AWS profiles via `--profile` flag or `AWS_PROFILE` env var
- Supports environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)
- Supports IAM roles (EC2/ECS/Lambda automatic detection)
- Required permission: `ce:GetCostAndUsage`

### Version Sync

**IMPORTANT**: Version must be synced across:
- `pyproject.toml` → `[project]` → `version = "0.1.0"`
- `cli.py` → `@click.version_option(version="0.1.0")`
- `__init__.py` → `__version__ = "0.1.0"`

### Output Design

- **Default**: JSON to stdout (agent-friendly, pipeable)
- **Visualizations**: Output to stderr (allows piping JSON while showing visuals)
- **Logs**: Always to stderr (with `--verbose` flag)
- **Errors**: Always to stderr

## Known Issues & Future Enhancements

### Current Implementation

- ✅ Period parsing with flexible syntax (7d, 2w, 1m)
- ✅ Three detail levels (basic, standard, full)
- ✅ Multiple output formats (JSON, tables, plots, summary)
- ✅ Comprehensive error handling with troubleshooting
- ✅ Type-safe with strict mypy
- ✅ Estimated cost indicators (~$X.XX)

### Future Enhancements

- [ ] Cache support (optional, with TTL)
- [ ] Model filtering (e.g., --models "Claude*")
- [ ] Export to CSV/Excel
- [ ] Cost trend alerts (% change detection)
- [ ] Budget threshold warnings
- [ ] Integration tests with mocked boto3
- [ ] Performance benchmarks

## Troubleshooting

### AWS Credentials Not Found

```bash
# Configure AWS profile
aws configure --profile my-profile

# Set environment variable
export AWS_PROFILE=my-profile

# Or use specific credentials
export AWS_ACCESS_KEY_ID=your-key
export AWS_SECRET_ACCESS_KEY=your-secret
```

### Permission Denied

Ensure IAM user/role has `ce:GetCostAndUsage` permission:

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": "ce:GetCostAndUsage",
    "Resource": "*"
  }]
}
```

### No Cost Data

- Verify Bedrock was used during the period
- Try longer period (e.g., `--period 90d`)
- Check Cost Explorer is enabled in AWS Console
- Remember: data may have 24-hour delay

### Type Errors During Development

Run auto-fix:
```bash
uv run ruff check --fix .
```

Common fixes:
- `Dict` → `dict`
- `List` → `list`
- `Optional[str]` → `str | None`

## Agent Integration

This CLI follows agent-friendly design principles:

### ReAct Loop Compatibility
- Structured commands enable reasoning and action
- Clear error messages guide next steps
- JSON output provides parseable data

### Composability
- JSON to stdout for piping
- Stderr for logs (doesn't interfere with data)
- Exit codes signal success/failure

### Reusability
- Commands serve as building blocks
- Importable library for custom integration
- Predictable behavior for automation

### Reliability
- Type-safe implementation
- Comprehensive testing
- Consistent error handling

---

**Generated with Claude Code**

This project demonstrates professional CLI-first design optimized for both human users and AI agent integration.
