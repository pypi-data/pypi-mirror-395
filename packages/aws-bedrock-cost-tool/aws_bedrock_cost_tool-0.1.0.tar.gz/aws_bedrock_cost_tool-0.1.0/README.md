<div align="center">
  <img src=".github/assets/logo.png" alt="AWS Bedrock Cost Tool Logo" width="200"/>
</div>

# aws-bedrock-cost-tool

[![CI](https://github.com/dnvriend/aws-bedrock-cost-tool/actions/workflows/ci.yml/badge.svg)](https://github.com/dnvriend/aws-bedrock-cost-tool/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A CLI tool for analyzing AWS Bedrock model costs using the Cost Explorer API.

## Features

- Flexible time periods: days (7d), weeks (2w), months (1m), up to 365 days
- Multiple output formats: JSON, tables, ASCII plots, matplotlib plots (iTerm2), summary
- Three detail levels: basic, standard, full (with regional breakdown)
- Token usage and cache statistics
- AWS profile support
- Importable as Python library

## Installation

Requirements: Python 3.14+, AWS CLI configured, [uv](https://github.com/astral-sh/uv)

```bash
git clone https://github.com/dnvriend/aws-bedrock-cost-tool.git
cd aws-bedrock-cost-tool
uv sync
uv build
uv tool install dist/aws_bedrock_cost_tool-0.1.0-py3-none-any.whl
```

## Configuration

### AWS Credentials

```bash
# Option 1: AWS profile
aws configure --profile my-profile
aws-bedrock-cost-tool --profile my-profile

# Option 2: Environment variables
export AWS_PROFILE=my-profile
```

### Required IAM Permission

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

Cost Explorer must be enabled in AWS Console.

## Usage

```bash
# JSON output (default), last 30 days
aws-bedrock-cost-tool

# Summary with all models, tokens, and cache stats
aws-bedrock-cost-tool --summary

# Table output
aws-bedrock-cost-tool --table

# Specific period and profile
aws-bedrock-cost-tool --period 7d --profile production

# Time series plot
aws-bedrock-cost-tool --plot-time

# Bar chart by model
aws-bedrock-cost-tool --plot-models

# All visualizations (ASCII)
aws-bedrock-cost-tool --all-visual

# High-quality matplotlib plots (iTerm2 only)
aws-bedrock-cost-tool --plot-image

# Full detail with regional breakdown
aws-bedrock-cost-tool --detail full --table
```

### Output Examples

**Summary**:
```
Total: ~$1015.85

Models:
  Claude Sonnet 4.5: ~$962.35 (~24M tokens, cache read: ~1410M tokens, cache write: ~95M tokens)
  Claude Haiku 4.5: ~$35.92 (~24M tokens, cache read: ~20M tokens, cache write: ~5M tokens)
  Claude Sonnet 4: ~$16.95 (~4M tokens)
  Claude Opus 4.5: ~$0.63 (~0.006M tokens)
```

**JSON** (pipe to jq):
```bash
aws-bedrock-cost-tool | jq '.models[] | select(.model_name | contains("Sonnet"))'
```

### Options

| Option | Description |
|--------|-------------|
| `--period` | Time period (7d, 2w, 1m, 3m). Default: 30d, Max: 365d |
| `--profile` | AWS profile name |
| `--detail` | basic, standard (default), full |
| `--table` | Table output |
| `--plot-time` | Time series plot (ASCII) |
| `--plot-models` | Bar chart by model (ASCII) |
| `--all-visual` | All ASCII visualizations |
| `--plot-image` | Matplotlib plots inline in iTerm2 |
| `--summary` | Summary with tokens and cache stats |
| `-v` | Verbose logging (-vv for debug, -vvv for trace) |
| `-q` | Quiet mode |

## Library Usage

```python
from aws_bedrock_cost_tool import (
    create_cost_explorer_client,
    query_bedrock_costs,
    analyze_cost_data,
    parse_period,
    calculate_date_range,
    format_date_for_aws,
)

days = parse_period("30d")
start_date, end_date = calculate_date_range(days)

client = create_cost_explorer_client(profile_name="my-profile")
response = query_bedrock_costs(client, format_date_for_aws(start_date), format_date_for_aws(end_date))
cost_data = analyze_cost_data(response, start_date, end_date, detail="standard")

print(f"Total: ${cost_data['total_cost']:.2f}")
for model in cost_data['models']:
    print(f"{model['model_name']}: ${model['total_cost']:.2f}")
```

## Development

```bash
make install       # Install dependencies
make check         # Run lint + typecheck + test + security
make pipeline      # Full pipeline including build
```

## License

MIT License - see [LICENSE](LICENSE)

## Author

Dennis Vriend - [@dnvriend](https://github.com/dnvriend)
