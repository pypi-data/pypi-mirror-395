---
description: Analyze AWS Bedrock costs for specified period
argument-hint: period
---

Analyze AWS Bedrock model costs for a specified time period.

## Usage

```bash
aws-bedrock-cost-tool [OPTIONS]
```

## Options

**Time Range:**
- `--period DURATION`: Period to analyze (default: 30d)
  - Format: `7d`, `2w`, `1m`, `3m`, `90d`
  - Max: 365d

**AWS Configuration:**
- `--profile NAME`: AWS profile name

**Output Modes:**
- Default: JSON to stdout
- `--table`: Summary table
- `--plot-time`: Time series plot
- `--plot-models`: Bar chart by model
- `--all-visual`: All visualizations
- `--summary-only`: Quick summary

**Detail Level:**
- `--detail basic|standard|full`: Detail level (default: standard)

**Control:**
- `-v/-vv/-vvv`: Verbosity (INFO/DEBUG/TRACE)
- `--quiet` / `-q`: Suppress messages
- `--help` / `-h`: Show help

## Examples

```bash
# Default JSON output (last 30 days)
aws-bedrock-cost-tool

# Quick summary
aws-bedrock-cost-tool --summary-only

# Visual table for last 90 days
aws-bedrock-cost-tool --period 90d --table

# Full report with all visualizations
aws-bedrock-cost-tool --all-visual --detail full

# Pipe to jq for filtering
aws-bedrock-cost-tool | jq '.models[] | select(.model_name | contains("Sonnet"))'
```

## Output

Returns cost data with:
- Total cost for period
- Per-model breakdown
- Usage by type (input/output/cache tokens in millions)
- Daily cost trends
- Estimated cost indicators (~$X.XX)
