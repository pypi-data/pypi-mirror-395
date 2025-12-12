---
name: skill-aws-bedrock-cost-tool
description: AWS Bedrock cost analysis with reporting
---

# When to use
- Analyze AWS Bedrock model costs and spending patterns
- Generate cost reports with tables and visualizations
- Track token usage and identify cost optimization opportunities

# AWS Bedrock Cost Tool Skill

## Purpose

A professional CLI tool for analyzing AWS Bedrock model costs with comprehensive reporting, visualization, and programmatic access. Provides detailed insights into model usage, token consumption, and spending trends across all Bedrock models.

## When to Use This Skill

**Use this skill when:**
- Analyzing AWS Bedrock costs for budget tracking
- Generating cost reports with tables or charts
- Investigating spending patterns and cost spikes
- Breaking down costs by model, usage type, or region
- Exporting cost data for further analysis
- Integrating cost analysis into automation scripts

**Do NOT use this skill for:**
- Real-time cost monitoring (data has 24hr delay)
- Forecasting future costs (historical analysis only)
- Non-Bedrock AWS service costs
- Modifying AWS resources or settings

## CLI Tool: aws-bedrock-cost-tool

A Python CLI tool that queries AWS Cost Explorer API to analyze Bedrock model costs with flexible reporting options.

### Installation

```bash
# Via pip from GitHub
pip install git+https://github.com/dnvriend/aws-bedrock-cost-tool.git

# Or clone and install with uv
git clone https://github.com/dnvriend/aws-bedrock-cost-tool.git
cd aws-bedrock-cost-tool
uv tool install .
```

### Prerequisites

- Python 3.14+
- AWS credentials configured
- Cost Explorer enabled in AWS account
- IAM permission: `ce:GetCostAndUsage`
- Optional: gnuplot for ASCII plots (`brew install gnuplot`)

### Quick Start

```bash
# Default JSON output (last 30 days)
aws-bedrock-cost-tool

# Quick summary
aws-bedrock-cost-tool --summary-only

# Visual table
aws-bedrock-cost-tool --table

# Complete visual report
aws-bedrock-cost-tool --all-visual
```

## Progressive Disclosure

<details>
<summary><strong>📊 Output Formats (Click to expand)</strong></summary>

### JSON Output (Default)

**Usage:**
```bash
aws-bedrock-cost-tool [--period DURATION]
```

**Output Structure:**
```json
{
  "period_start": "2025-10-21",
  "period_end": "2025-11-20",
  "total_cost": 556.80,
  "has_estimated": true,
  "models": [
    {
      "model_name": "Claude Sonnet 4.5",
      "total_cost": 556.80,
      "estimated": true,
      "usage_breakdown": [
        {
          "usage_type": "CacheReadInputTokenCount",
          "cost": 248.82,
          "quantity": 829.406,
          "estimated": true
        }
      ]
    }
  ],
  "daily_costs": [...]
}
```

**Key Fields:**
- `quantity`: Tokens in millions (M)
- `estimated`: True if costs not finalized
- `usage_breakdown`: Input/output/cache token costs
- `regional_breakdown`: Costs by AWS region (full detail only)

**Pipeline Example:**
```bash
# Filter Sonnet costs
aws-bedrock-cost-tool | jq '.models[] | select(.model_name | contains("Sonnet"))'

# Sum all input token costs
aws-bedrock-cost-tool | jq '[.models[].usage_breakdown[] | select(.usage_type | contains("InputToken")) | .cost] | add'

# Export to CSV
aws-bedrock-cost-tool | jq -r '.models[] | [.model_name, .total_cost] | @csv'
```

---

### Table Output

**Usage:**
```bash
aws-bedrock-cost-tool --table [--detail basic|standard|full]
```

**Detail Levels:**

**Basic**: Model totals only
```
╭─────────────────────┬────────────╮
│ Model               │ Total Cost │
├─────────────────────┼────────────┤
│ Claude Sonnet 4.5   │ ~$556.80   │
│ Claude Haiku 3.5    │ ~$12.34    │
╰─────────────────────┴────────────╯
```

**Standard**: Model + usage type breakdown (default)
```
### Claude Sonnet 4.5 (Total: ~$556.80)
╭───────────────────────────┬──────────┬────────────╮
│ Usage Type                │ Cost     │ Tokens (M) │
├───────────────────────────┼──────────┼────────────┤
│ CacheReadInputTokenCount  │ ~$248.82 │ 829.406    │
│ CacheWriteInputTokenCount │ ~$220.85 │ 58.893     │
│ InputTokenCount           │ ~$3.71   │ 1.236      │
│ OutputTokenCount          │ ~$82.25  │ 5.483      │
╰───────────────────────────┴──────────┴────────────╯
```

**Full**: Model + usage types + regional breakdown
```
### Claude Sonnet 4.5 (Total: ~$556.80)

Usage Breakdown:
[Same as standard]

Regional Breakdown:
╭────────┬──────────╮
│ Region │ Cost     │
├────────┼──────────┤
│ USE1   │ $345.67  │
│ EUC1   │ $211.13  │
╰────────┴──────────╯
```

**Examples:**
```bash
# Standard table (recommended)
aws-bedrock-cost-tool --table

# Basic overview
aws-bedrock-cost-tool --table --detail basic

# Full detail with regions
aws-bedrock-cost-tool --table --detail full --period 90d
```

---

### Summary Output

**Usage:**
```bash
aws-bedrock-cost-tool --summary-only
```

**Output:**
```
AWS Bedrock Cost Summary (2025-10-21 to 2025-11-20)
Total Cost: ~$556.80

Top 3 Models:
1. Claude Sonnet 4.5: ~$556.80
2. Claude Haiku 3.5: ~$12.34
3. Claude Opus 4: ~$5.67
```

**When to Use:**
- Quick cost checks
- Daily standup reports
- Budget alerts
- Scripted notifications

---

### Visual Plots

**Time Series Plot:**
```bash
aws-bedrock-cost-tool --plot-time
```

Shows daily spending trends as ASCII line chart.

**Model Bar Chart:**
```bash
aws-bedrock-cost-tool --plot-models
```

Shows cost comparison by model as horizontal bar chart.

**All Visualizations:**
```bash
aws-bedrock-cost-tool --all-visual
```

Displays: table + time series + bar chart.

**Requirements:**
- gnuplot installed: `brew install gnuplot`
- Terminal with Unicode support

</details>

<details>
<summary><strong>⚙️ Configuration & Options (Click to expand)</strong></summary>

### Time Periods

**Syntax:**
- `Nd`: N days (e.g., `7d`, `30d`, `90d`)
- `Nw`: N weeks (e.g., `1w`, `2w`, `4w`)
- `Nm`: N months (e.g., `1m`, `3m`, `6m`)

**Examples:**
```bash
# Last 7 days
aws-bedrock-cost-tool --period 7d

# Last 2 weeks
aws-bedrock-cost-tool --period 2w

# Last 3 months
aws-bedrock-cost-tool --period 3m

# Maximum: 365 days
aws-bedrock-cost-tool --period 365d
```

**Limits:**
- Minimum: 1 day
- Maximum: 365 days (enforced)

---

### AWS Profile Selection

**Environment Variable:**
```bash
export AWS_PROFILE=my-profile
aws-bedrock-cost-tool
```

**Command Line Flag:**
```bash
aws-bedrock-cost-tool --profile my-profile
```

**Precedence:**
1. `--profile` flag (highest)
2. `AWS_PROFILE` environment variable
3. Default AWS credentials

**Example:**
```bash
# Production account
aws-bedrock-cost-tool --profile prod --period 30d --table

# Development account
aws-bedrock-cost-tool --profile dev --summary-only
```

---

### Verbosity Levels

**Levels:**
- No flag: WARNING only (quiet mode)
- `-v`: INFO level (progress messages)
- `-vv`: DEBUG level (detailed logging)
- `-vvv`: TRACE level (includes boto3/urllib3 logs)

**Examples:**
```bash
# Quiet (default)
aws-bedrock-cost-tool

# Show progress
aws-bedrock-cost-tool -v

# Debugging
aws-bedrock-cost-tool -vv

# Full trace with AWS API calls
aws-bedrock-cost-tool -vvv
```

**Output:**
- Logs always go to stderr
- Data (JSON) always goes to stdout
- Allows safe piping: `aws-bedrock-cost-tool -v | jq`

---

### Detail Levels

**Basic**: Model names and total costs only
```bash
aws-bedrock-cost-tool --detail basic
```

**Standard** (default): Models + usage type breakdown
```bash
aws-bedrock-cost-tool --detail standard
```

**Full**: Models + usage types + regional costs
```bash
aws-bedrock-cost-tool --detail full
```

**Applies to:**
- JSON output
- Table output
- Summary calculations

**Does NOT apply to:**
- Plots (always use aggregated data)

</details>

<details>
<summary><strong>💻 Programmatic Usage (Click to expand)</strong></summary>

### Python Library Import

The tool can be imported as a Python library for custom integrations.

**Installation:**
```bash
pip install git+https://github.com/dnvriend/aws-bedrock-cost-tool.git
```

**Basic Usage:**
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

**Advanced Example:**
```python
from aws_bedrock_cost_tool import (
    create_cost_explorer_client,
    query_bedrock_costs,
    analyze_cost_data,
    calculate_date_range,
    format_date_for_aws,
)
import json

def get_sonnet_costs(days: int = 30) -> dict:
    """Get Claude Sonnet costs for specified period."""
    start_date, end_date = calculate_date_range(days)

    client = create_cost_explorer_client()
    response = query_bedrock_costs(
        client,
        format_date_for_aws(start_date),
        format_date_for_aws(end_date)
    )

    cost_data = analyze_cost_data(response, start_date, end_date)

    # Filter Sonnet models
    sonnet_models = [
        m for m in cost_data['models']
        if 'Sonnet' in m['model_name']
    ]

    return {
        'period_days': days,
        'total_sonnet_cost': sum(m['total_cost'] for m in sonnet_models),
        'models': sonnet_models
    }

# Use in script
if __name__ == "__main__":
    result = get_sonnet_costs(90)
    print(json.dumps(result, indent=2))
```

**Exception Handling:**
```python
from aws_bedrock_cost_tool import (
    create_cost_explorer_client,
    CredentialsError,
    PermissionError,
    CostExplorerError,
)

try:
    client = create_cost_explorer_client(profile_name="prod")
except CredentialsError as e:
    print(f"AWS credentials not found: {e}")
except PermissionError as e:
    print(f"Missing IAM permissions: {e}")
except CostExplorerError as e:
    print(f"Cost Explorer API error: {e}")
```

**Custom Reporting:**
```python
from aws_bedrock_cost_tool import analyze_cost_data
from aws_bedrock_cost_tool.reporting import (
    format_json,
    format_summary,
    render_table,
)

# Get cost data (assume already queried)
cost_data = analyze_cost_data(response, start, end, detail="full")

# Generate different outputs
json_output = format_json(cost_data)
summary_output = format_summary(cost_data)
render_table(cost_data, detail="full")  # Prints to stderr
```

**Type Safety:**
```python
from aws_bedrock_cost_tool.core.models import (
    CostData,
    ModelCost,
    UsageBreakdown,
    DailyCost,
)

def process_costs(cost_data: CostData) -> None:
    """Process cost data with full type safety."""
    for model in cost_data['models']:
        model_name: str = model['model_name']
        total_cost: float = model['total_cost']

        for usage in model['usage_breakdown']:
            usage_type: str = usage['usage_type']
            cost: float = usage['cost']
            quantity: float = usage['quantity']  # Millions of tokens

            print(f"{model_name} - {usage_type}: {quantity:.2f}M tokens = ${cost:.2f}")
```

</details>

<details>
<summary><strong>🔧 Troubleshooting (Click to expand)</strong></summary>

### Common Issues

**Issue: AWS Credentials Not Found**
```bash
ERROR: Unable to locate credentials
```

**Solution:**
```bash
# Configure AWS CLI
aws configure --profile my-profile

# Or set environment variables
export AWS_ACCESS_KEY_ID=your-key
export AWS_SECRET_ACCESS_KEY=your-secret
export AWS_PROFILE=my-profile

# Verify credentials
aws sts get-caller-identity
```

---

**Issue: Permission Denied**
```bash
ERROR: User is not authorized to perform: ce:GetCostAndUsage
```

**Solution:**
Add IAM policy to user/role:
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

Verify with:
```bash
aws ce get-cost-and-usage \
  --time-period Start=2025-11-01,End=2025-11-20 \
  --granularity DAILY \
  --metrics BlendedCost
```

---

**Issue: No Cost Data Found**
```bash
No Bedrock usage found for this period.
```

**Possible Causes:**
- No Bedrock usage during period
- Cost Explorer not enabled
- Data delay (up to 24 hours)
- Wrong AWS account/profile

**Solution:**
```bash
# Try longer period
aws-bedrock-cost-tool --period 90d

# Check different profile
aws-bedrock-cost-tool --profile prod

# Verify Cost Explorer enabled
aws ce describe-cost-category-definition --cost-category-arn "*" 2>&1 | grep -i enabled
```

---

**Issue: gnuplot Not Found**
```bash
ERROR: gnuplot command not found
```

**Solution:**
```bash
# macOS
brew install gnuplot

# Ubuntu/Debian
sudo apt-get install gnuplot

# Verify installation
gnuplot --version
```

---

**Issue: Type Errors During Development**
```bash
mypy error: ...
```

**Solution:**
```bash
# Auto-fix with ruff
uv run ruff check --fix .

# Run type check
uv run python -m mypy aws_bedrock_cost_tool
```

---

**Issue: Period Exceeds Maximum**
```bash
ERROR: Period exceeds maximum of 365 days
```

**Solution:**
```bash
# Use maximum period
aws-bedrock-cost-tool --period 365d

# Or break into smaller chunks and aggregate
aws-bedrock-cost-tool --period 90d > q1.json
aws-bedrock-cost-tool --period 90d --profile prod > q2.json
# ... manually aggregate
```

### Getting Help

```bash
# Main help
aws-bedrock-cost-tool --help

# Version info
aws-bedrock-cost-tool --version

# Verbose logging
aws-bedrock-cost-tool -vvv --summary-only
```

**GitHub Issues:**
https://github.com/dnvriend/aws-bedrock-cost-tool/issues

</details>

<details>
<summary><strong>📋 Reference (Click to expand)</strong></summary>

### Exit Codes

- `0`: Success
- `1`: Client error (invalid arguments, credentials, etc.)
- `2`: Server error (AWS API error)
- `3`: Network error

### Output Formats Summary

| Format | Flag | Output | Use Case |
|--------|------|--------|----------|
| JSON | (default) | stdout | Automation, piping |
| Table | `--table` | stderr | Human review |
| Summary | `--summary-only` | stderr | Quick check |
| Time plot | `--plot-time` | stderr | Trend analysis |
| Model plot | `--plot-models` | stderr | Comparison |
| All visuals | `--all-visual` | stderr | Complete report |

### Token Quantity Units

**All token quantities are in millions (M)**:
- `58.893` = 58.893 million tokens
- `829.406` = 829.406 million tokens
- Displayed in table headers as "Tokens (M)"

**Pricing Reference** (Claude Sonnet 4.5):
- Input tokens: ~$3.00/M
- Output tokens: ~$15.00/M
- Cache read: ~$0.30/M
- Cache write: ~$3.75/M

### Usage Type Prefixes

**Regional Codes:**
- `USE1`: US East (N. Virginia)
- `USE2`: US East (Ohio)
- `USW2`: US West (Oregon)
- `EUC1`: EU (Frankfurt)
- `EUW2`: EU (London)
- `APN1`: Asia Pacific (Tokyo)
- `APS1`: Asia Pacific (Singapore)

**Usage Types:**
- `InputTokenCount`: Regular input tokens
- `OutputTokenCount`: Regular output tokens
- `CacheReadInputTokenCount`: Prompt cache reads
- `CacheWriteInputTokenCount`: Prompt cache writes

### Detail Level Comparison

| Level | Models | Usage Types | Regions | JSON Size |
|-------|--------|-------------|---------|-----------|
| Basic | ✓ | ✗ | ✗ | Small |
| Standard | ✓ | ✓ | ✗ | Medium |
| Full | ✓ | ✓ | ✓ | Large |

### AWS Cost Explorer Limitations

- **Data Delay**: Up to 24 hours
- **Retention**: 12 months of historical data
- **Granularity**: Daily (this tool)
- **Region**: Global service (always us-east-1 endpoint)
- **Estimated Costs**: Recent days marked with `~`

### Best Practices

1. **Regular Monitoring**: Run daily with `--summary-only`
2. **Cost Alerts**: Integrate with notification systems
3. **Trend Analysis**: Use `--plot-time` weekly
4. **Budget Tracking**: Export JSON and aggregate monthly
5. **Model Comparison**: Use `--table --detail full` for deep dives
6. **Cache Optimization**: Monitor cache read/write ratios
7. **Regional Analysis**: Use `--detail full` to identify regional costs

</details>

## Resources

- **GitHub Repository**: https://github.com/dnvriend/aws-bedrock-cost-tool
- **AWS Cost Explorer**: https://docs.aws.amazon.com/cost-management/latest/userguide/ce-api.html
- **AWS Bedrock**: https://aws.amazon.com/bedrock/
- **Boto3 Documentation**: https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
- **Issue Tracker**: https://github.com/dnvriend/aws-bedrock-cost-tool/issues

## Quick Command Reference

```bash
# Common operations
aws-bedrock-cost-tool                              # JSON (30d)
aws-bedrock-cost-tool --summary-only              # Quick summary
aws-bedrock-cost-tool --table                     # Table view
aws-bedrock-cost-tool --all-visual                # Complete report
aws-bedrock-cost-tool --period 90d --table        # 90-day table
aws-bedrock-cost-tool --profile prod              # Specific profile
aws-bedrock-cost-tool -v --plot-time              # Verbose time plot
aws-bedrock-cost-tool | jq '.total_cost'          # Extract total
```
