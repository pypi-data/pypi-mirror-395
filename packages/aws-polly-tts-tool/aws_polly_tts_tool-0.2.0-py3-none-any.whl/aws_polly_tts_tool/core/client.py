"""
AWS Polly client initialization and credential validation.

Centralizes boto3 Polly client creation with comprehensive error
handling and credential validation. This module ensures AWS credentials
are properly configured before attempting TTS operations, providing
clear, actionable error messages when credentials are missing or invalid.

By testing credentials proactively, we fail fast with helpful guidance
rather than allowing users to encounter cryptic boto3 errors during
synthesis operations.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from typing import Any

import boto3
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError


def get_polly_client(region: str | None = None) -> Any:
    """
    Initialize and return AWS Polly client.

    Provides a consistent entry point for creating Polly clients with
    optional region override. This function handles AWS SDK initialization
    and raises clear exceptions if credentials are not configured, avoiding
    confusing boto3 errors downstream.

    Args:
        region: AWS region name (e.g., 'us-east-1'). If None, uses default
               from AWS config or environment variable AWS_DEFAULT_REGION.

    Returns:
        boto3 Polly client instance ready for TTS operations

    Raises:
        ValueError: If AWS credentials are not configured or invalid
        Exception: If client initialization fails for other reasons

    Example:
        >>> client = get_polly_client('us-east-1')
        >>> response = client.describe_voices(MaxResults=1)
    """
    try:
        # Create client with optional region override
        if region:
            client = boto3.client("polly", region_name=region)
        else:
            client = boto3.client("polly")

        # Test credentials by making a minimal API call
        # WHY: Fail fast with clear error rather than waiting for first synthesis
        client.describe_voices()

        return client

    except NoCredentialsError:
        raise ValueError(
            "AWS credentials not configured.\n\n"
            "Configure with one of these methods:\n"
            "1. Run: aws configure\n"
            "2. Set environment variables:\n"
            "   export AWS_ACCESS_KEY_ID='your-access-key'\n"
            "   export AWS_SECRET_ACCESS_KEY='your-secret-key'\n"
            "   export AWS_DEFAULT_REGION='us-east-1'\n\n"
            "Get credentials from: https://console.aws.amazon.com/iam/home#/security_credentials"
        )
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_msg = e.response["Error"]["Message"]

        if error_code == "InvalidClientTokenId":
            raise ValueError(
                "AWS credentials are invalid or expired.\n\n"
                f"Error: {error_msg}\n\n"
                "Verify credentials with: aws sts get-caller-identity\n"
                "Update credentials with: aws configure"
            )
        elif error_code == "AccessDeniedException":
            raise ValueError(
                "AWS IAM permissions insufficient for Polly access.\n\n"
                f"Error: {error_msg}\n\n"
                "Required IAM permissions:\n"
                "  - polly:DescribeVoices\n"
                "  - polly:SynthesizeSpeech\n\n"
                "Contact your AWS administrator to grant Polly permissions."
            )
        else:
            raise ValueError(f"AWS API error [{error_code}]: {error_msg}")

    except BotoCoreError as e:
        raise Exception(f"AWS SDK error: {e}")
    except Exception as e:
        raise Exception(f"Failed to initialize Polly client: {e}")


def test_aws_credentials() -> dict[str, str]:
    """
    Test AWS credentials and return identity information.

    Provides diagnostic information about the current AWS identity for
    troubleshooting authentication issues. This function helps users verify
    they're using the correct AWS account and IAM credentials.

    Returns:
        Dictionary with keys: UserId, Account, Arn

    Raises:
        ValueError: If credentials are invalid or missing
        Exception: If STS call fails

    Example:
        >>> identity = test_aws_credentials()
        >>> print(f"AWS Account: {identity['Account']}")
    """
    try:
        sts = boto3.client("sts")
        response = sts.get_caller_identity()

        return {
            "UserId": response["UserId"],
            "Account": response["Account"],
            "Arn": response["Arn"],
        }

    except NoCredentialsError:
        raise ValueError(
            "AWS credentials not configured.\n"
            "Run: aws configure\n"
            "Or set: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION"
        )
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_msg = e.response["Error"]["Message"]
        raise ValueError(f"AWS credential test failed [{error_code}]: {error_msg}")
    except Exception as e:
        raise Exception(f"Failed to test AWS credentials: {e}")
