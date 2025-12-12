"""AWS Cost Explorer client wrapper.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import logging
from typing import Any

import boto3
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError

logger = logging.getLogger(__name__)


class CostExplorerError(Exception):
    """Base exception for Cost Explorer errors."""

    pass


class CredentialsError(CostExplorerError):
    """Raised when AWS credentials are not found or invalid."""

    pass


class PermissionError(CostExplorerError):
    """Raised when AWS permissions are insufficient."""

    pass


def get_bedrock_models() -> list[str]:
    """Get list of all Bedrock model names to filter on.

    Returns:
        List of Bedrock model service names for Cost Explorer filtering
    """
    return [
        "Claude 3.5 Haiku (Amazon Bedrock Edition)",
        "Claude Sonnet 4 (Amazon Bedrock Edition)",
        "Claude Sonnet 4.5 (Amazon Bedrock Edition)",
        "Claude Haiku 4.5 (Amazon Bedrock Edition)",
        "Claude Opus 4.5 (Amazon Bedrock Edition)",
        "Claude Opus 4.1 (Amazon Bedrock Edition)",
        "Claude 3 Haiku (Amazon Bedrock Edition)",
        "Claude 3 Sonnet (Amazon Bedrock Edition)",
        "Claude 3 Opus (Amazon Bedrock Edition)",
        "Claude 3.5 Sonnet (Amazon Bedrock Edition)",
        "Claude 3.5 Sonnet v2 (Amazon Bedrock Edition)",
        "Claude 3.7 Sonnet (Amazon Bedrock Edition)",
        "Llama 3.1 405B Instruct (Amazon Bedrock Edition)",
        "Llama 3.1 70B Instruct (Amazon Bedrock Edition)",
        "Llama 3.1 8B Instruct (Amazon Bedrock Edition)",
        "Llama 3.2 90B Instruct (Amazon Bedrock Edition)",
        "Llama 3.2 11B Instruct (Amazon Bedrock Edition)",
        "Llama 3.2 3B Instruct (Amazon Bedrock Edition)",
        "Llama 3.2 1B Instruct (Amazon Bedrock Edition)",
        "Llama 3.3 70B Instruct (Amazon Bedrock Edition)",
        "Amazon Titan Text Express (Amazon Bedrock Edition)",
        "Amazon Titan Text Lite (Amazon Bedrock Edition)",
        "Amazon Titan Text Premier (Amazon Bedrock Edition)",
        "Amazon Titan Embeddings Text (Amazon Bedrock Edition)",
        "Amazon Titan Multimodal Embeddings (Amazon Bedrock Edition)",
        "Amazon Titan Image Generator (Amazon Bedrock Edition)",
        "Amazon Nova Micro (Amazon Bedrock Edition)",
        "Amazon Nova Lite (Amazon Bedrock Edition)",
        "Amazon Nova Pro (Amazon Bedrock Edition)",
        "Amazon Nova Premier (Amazon Bedrock Edition)",
        "Amazon Nova Canvas (Amazon Bedrock Edition)",
        "Amazon Nova Reel (Amazon Bedrock Edition)",
        "Command R (Amazon Bedrock Edition)",
        "Command R+ (Amazon Bedrock Edition)",
        "Embed English (Amazon Bedrock Edition)",
        "Embed Multilingual (Amazon Bedrock Edition)",
        "Cohere Rerank (Amazon Bedrock Edition)",
        "Jamba 1.5 Large (Amazon Bedrock Edition)",
        "Jamba 1.5 Mini (Amazon Bedrock Edition)",
        "DeepSeek-R1 (Amazon Bedrock Edition)",
    ]


def create_cost_explorer_client(profile_name: str | None = None) -> Any:
    """Create AWS Cost Explorer client with proper error handling.

    Args:
        profile_name: AWS profile name (overrides AWS_PROFILE env var)

    Returns:
        boto3 Cost Explorer client

    Raises:
        CredentialsError: If AWS credentials are not found
        CostExplorerError: If client creation fails
    """
    try:
        if profile_name:
            session = boto3.Session(profile_name=profile_name)
        else:
            session = boto3.Session()

        # Cost Explorer is a global service, always use us-east-1
        client = session.client("ce", region_name="us-east-1")

        return client

    except NoCredentialsError:
        raise CredentialsError(
            "AWS credentials not found. Configure credentials using:\n"
            "  1. aws configure --profile PROFILE_NAME\n"
            "  2. Set AWS_PROFILE environment variable\n"
            "  3. Use IAM role (EC2/ECS/Lambda)\n"
            "See: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html"
        )
    except BotoCoreError as e:
        raise CostExplorerError(f"Failed to create AWS client: {e}")


def query_bedrock_costs(
    client: Any, start_date: str, end_date: str, verbose: bool | int = False
) -> dict[str, Any]:
    """Query Cost Explorer for Bedrock model costs.

    Args:
        client: boto3 Cost Explorer client
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        verbose: Enable verbose logging (bool or int count for compatibility)

    Returns:
        Raw Cost Explorer API response

    Raises:
        PermissionError: If insufficient permissions
        CostExplorerError: If API call fails
    """
    try:
        logger.debug(f"Querying Cost Explorer for period {start_date} to {end_date}")
        logger.debug("Building Cost Explorer API request")

        response = client.get_cost_and_usage(
            TimePeriod={"Start": start_date, "End": end_date},
            Granularity="DAILY",
            Metrics=["BlendedCost", "UsageQuantity"],
            GroupBy=[
                {"Type": "DIMENSION", "Key": "SERVICE"},
                {"Type": "DIMENSION", "Key": "USAGE_TYPE"},
            ],
            Filter={"Dimensions": {"Key": "SERVICE", "Values": get_bedrock_models()}},
        )

        result_count = sum(len(r.get("Groups", [])) for r in response.get("ResultsByTime", []))
        logger.debug(f"Received {result_count} cost records from Cost Explorer")
        logger.debug(f"Response contains {len(response.get('ResultsByTime', []))} time periods")

        return dict(response)

    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "")

        if error_code in ["AccessDeniedException", "UnauthorizedOperation"]:
            raise PermissionError(
                "Missing AWS permissions for Cost Explorer.\n"
                "Required permission: ce:GetCostAndUsage\n"
                "See: https://docs.aws.amazon.com/cost-management/latest/userguide/ce-api.html"
            )

        raise CostExplorerError(f"AWS API error: {e}")

    except BotoCoreError as e:
        raise CostExplorerError(f"AWS client error: {e}")
