---
description: Display costs in formatted table view
argument-hint: period
---

Display AWS Bedrock costs in a formatted table with usage breakdown.

## Usage

```bash
aws-bedrock-cost-tool --table [OPTIONS]
```

## Options

- `--period DURATION`: Time period (default: 30d)
- `--detail basic|standard|full`: Detail level
- `--profile NAME`: AWS profile
- `-v/-vv/-vvv`: Verbosity levels

## Examples

```bash
# Standard table (last 30 days)
aws-bedrock-cost-tool --table

# Full detail with regions
aws-bedrock-cost-tool --table --detail full

# Last 90 days
aws-bedrock-cost-tool --period 90d --table
```

## Output

Displays formatted table with:
- Model names
- Total costs per model
- Token usage in millions (M)
- Usage type breakdown (input/output/cache)
- Regional breakdown (full detail only)
