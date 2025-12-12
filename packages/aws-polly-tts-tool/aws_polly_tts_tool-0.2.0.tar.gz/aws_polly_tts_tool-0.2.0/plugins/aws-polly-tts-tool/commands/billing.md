---
description: Query AWS billing for Polly usage costs
argument-hint:
---

Query AWS Cost Explorer for actual Amazon Polly usage costs with engine breakdown.

## Usage

```bash
aws-polly-tts-tool billing [OPTIONS]
```

## Options

- `--days INT` / `-d INT`: Number of days to query (default: 30)
- `--start-date TEXT`: Custom start date (YYYY-MM-DD)
- `--end-date TEXT`: Custom end date (YYYY-MM-DD)
- `--region TEXT` / `-r TEXT`: AWS region for Cost Explorer
- `-V/-VV/-VVV`: Verbosity (INFO/DEBUG/TRACE)

## Examples

```bash
# Last 30 days of Polly costs
aws-polly-tts-tool billing

# Last 7 days
aws-polly-tts-tool billing --days 7

# Custom date range
aws-polly-tts-tool billing --start-date 2025-01-01 --end-date 2025-01-31
```

## Output

Returns total cost and breakdown by engine (Standard, Neural, Generative, Long-form).

Requires IAM permission: `ce:GetCostAndUsage`
