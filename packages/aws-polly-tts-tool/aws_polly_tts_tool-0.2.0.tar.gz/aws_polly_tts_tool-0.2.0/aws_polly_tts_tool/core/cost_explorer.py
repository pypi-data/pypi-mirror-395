"""
AWS Cost Explorer queries for Polly billing data.

Provides accurate billing information by querying AWS's Cost Explorer
API, enabling users to track actual Polly usage costs across different
engines and time periods. This complements character-based cost estimates
with real billing data for financial planning and budget monitoring.

The module handles Cost Explorer's complex API structure, date ranges, and
filtering to present Polly costs in a clear, actionable format.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from datetime import datetime, timedelta
from typing import Any

import boto3
from botocore.exceptions import ClientError


def get_polly_costs(
    days: int = 30,
    start_date: str | None = None,
    end_date: str | None = None,
    region: str | None = None,
) -> dict[str, Any]:
    """
    Query AWS Cost Explorer for Polly usage costs.

    Retrieves actual billing data from AWS to provide accurate cost
    tracking for Polly TTS usage. This enables budget monitoring, cost
    attribution, and financial planning based on real AWS charges rather
    than estimates.

    Args:
        days: Number of days to query (default: 30). Ignored if start_date provided.
        start_date: Custom start date in YYYY-MM-DD format
        end_date: Custom end date in YYYY-MM-DD format. Defaults to today.
        region: AWS region for Cost Explorer client

    Returns:
        Dictionary with keys:
            - total_cost: Total Polly cost as float
            - currency: Currency code (e.g., 'USD')
            - start_date: Query start date
            - end_date: Query end date
            - by_engine: Dict mapping engine types to costs
            - by_day: List of daily cost entries

    Raises:
        ValueError: If Cost Explorer access is denied or dates are invalid
        Exception: If Cost Explorer API call fails

    Example:
        >>> costs = get_polly_costs(days=30)
        >>> print(f"Total cost: ${costs['total_cost']:.2f}")
        >>> print(f"By engine: {costs['by_engine']}")
    """
    try:
        # Initialize Cost Explorer client
        ce = boto3.client("ce", region_name=region) if region else boto3.client("ce")

        # Calculate date range
        if start_date and end_date:
            # Use custom date range
            start = start_date
            end = end_date
        elif start_date:
            # Start date provided, end date defaults to today
            start = start_date
            end = datetime.now().strftime("%Y-%m-%d")
        else:
            # Use days parameter
            end_dt = datetime.now()
            start_dt = end_dt - timedelta(days=days)
            start = start_dt.strftime("%Y-%m-%d")
            end = end_dt.strftime("%Y-%m-%d")

        # Query Cost Explorer for Polly costs
        # WHY: Filter by Polly service and group by usage type to separate engines
        response = ce.get_cost_and_usage(
            TimePeriod={"Start": start, "End": end},
            Granularity="DAILY",
            Metrics=["UnblendedCost"],
            Filter={
                "Dimensions": {
                    "Key": "SERVICE",
                    "Values": ["Amazon Polly"],
                }
            },
            GroupBy=[
                {"Type": "DIMENSION", "Key": "USAGE_TYPE"},
            ],
        )

        # Parse response
        total_cost = 0.0
        by_engine: dict[str, float] = {
            "standard": 0.0,
            "neural": 0.0,
            "generative": 0.0,
            "long-form": 0.0,
            "other": 0.0,
        }
        by_day: list[dict[str, Any]] = []

        for result in response["ResultsByTime"]:
            day_start = result["TimePeriod"]["Start"]
            day_total = 0.0

            for group in result["Groups"]:
                usage_type = group["Keys"][0]
                amount = float(group["Metrics"]["UnblendedCost"]["Amount"])
                day_total += amount

                # Map usage type to engine
                # WHY: AWS usage types contain engine identifiers
                engine_key = _map_usage_type_to_engine(usage_type)
                by_engine[engine_key] += amount

            total_cost += day_total
            by_day.append({"date": day_start, "cost": day_total})

        currency = (
            response["ResultsByTime"][0]["Groups"][0]["Metrics"]["UnblendedCost"]["Unit"]
            if response["ResultsByTime"] and response["ResultsByTime"][0]["Groups"]
            else "USD"
        )

        return {
            "total_cost": total_cost,
            "currency": currency,
            "start_date": start,
            "end_date": end,
            "by_engine": by_engine,
            "by_day": by_day,
        }

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_msg = e.response["Error"]["Message"]

        if error_code == "AccessDeniedException":
            raise ValueError(
                "Access denied to AWS Cost Explorer.\n\n"
                f"Error: {error_msg}\n\n"
                "Required IAM permissions:\n"
                "  - ce:GetCostAndUsage\n\n"
                "Contact your AWS administrator to grant Cost Explorer access.\n"
                "Note: Cost Explorer may not be enabled in your AWS account."
            )
        else:
            raise ValueError(f"Cost Explorer API error [{error_code}]: {error_msg}")

    except Exception as e:
        raise Exception(f"Failed to query Polly costs: {e}") from e


def _map_usage_type_to_engine(usage_type: str) -> str:
    """
    Map AWS usage type to Polly engine category.

    AWS reports usage types with technical identifiers that need to be
    mapped to user-friendly engine names. This helper provides consistent
    categorization across different AWS usage type formats.

    Args:
        usage_type: AWS usage type string (e.g., 'USE1-SynthesizeSpeech-Neural')

    Returns:
        Engine category: 'standard', 'neural', 'generative', 'long-form', or 'other'

    Example:
        >>> _map_usage_type_to_engine('USE1-SynthesizeSpeech-Neural')
        'neural'
    """
    usage_lower = usage_type.lower()

    # WHY: Pattern matching based on AWS's usage type naming conventions
    if "neural" in usage_lower:
        return "neural"
    elif "generative" in usage_lower:
        return "generative"
    elif "longform" in usage_lower or "long-form" in usage_lower:
        return "long-form"
    elif "standard" in usage_lower or "speech" in usage_lower:
        # WHY: Many standard requests just say "SynthesizeSpeech" without engine
        return "standard"
    else:
        return "other"
