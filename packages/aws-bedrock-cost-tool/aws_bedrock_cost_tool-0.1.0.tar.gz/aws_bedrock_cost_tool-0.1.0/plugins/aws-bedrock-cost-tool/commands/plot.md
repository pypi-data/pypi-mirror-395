---
description: Visualize costs with ASCII plots
argument-hint: type
---

Generate ASCII visualizations of AWS Bedrock costs.

## Usage

```bash
aws-bedrock-cost-tool --plot-time [OPTIONS]    # Time series
aws-bedrock-cost-tool --plot-models [OPTIONS]  # Bar chart
aws-bedrock-cost-tool --all-visual [OPTIONS]   # All plots
```

## Plot Types

**Time Series (`--plot-time`):**
- Daily cost trends over time
- Shows spending patterns
- Identifies cost spikes

**Models Bar Chart (`--plot-models`):**
- Cost by model comparison
- Horizontal bar chart
- Quick cost distribution view

**All Visuals (`--all-visual`):**
- Table + Time series + Bar chart
- Comprehensive cost overview

## Examples

```bash
# Time series for last 30 days
aws-bedrock-cost-tool --plot-time

# Model comparison for last 90 days
aws-bedrock-cost-tool --period 90d --plot-models

# Complete visual report
aws-bedrock-cost-tool --all-visual --detail full
```

## Requirements

- gnuplot (install: `brew install gnuplot`)
- Plots render in terminal as ASCII art
