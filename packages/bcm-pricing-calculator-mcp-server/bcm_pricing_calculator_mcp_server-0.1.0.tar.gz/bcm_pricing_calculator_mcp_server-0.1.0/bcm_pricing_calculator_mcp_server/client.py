# Copyright (c) 2025 oreokebu-dev
# SPDX-License-Identifier: MIT

"""BCM Pricing Calculator client utilities."""

import sys
from typing import Any, Optional

import boto3
from botocore.config import Config
from loguru import logger

from bcm_pricing_calculator_mcp_server import __version__, consts

# Set up logging
logger.remove()
logger.add(sys.stderr, level=consts.LOG_LEVEL)


def create_bcm_client(profile: Optional[str] = None, region: Optional[str] = None) -> Any:
    """Create an AWS BCM Pricing Calculator client.

    Args:
        profile: AWS profile name to use (default: None, uses AWS_PROFILE or default profile)
        region: AWS region name (default: us-east-1, BCM Pricing Calculator only available here)

    Returns:
        boto3 bcm-pricing-calculator client
    """
    profile_name = profile if profile else consts.AWS_PROFILE
    session = boto3.Session(profile_name=profile_name)

    # BCM Pricing Calculator is only available in us-east-1
    bcm_region = region if region else 'us-east-1'

    config = Config(
        region_name=bcm_region,
        user_agent_extra=f'awslabs/mcp/{consts.MCP_SERVER_NAME}/{__version__}',
    )

    logger.debug(
        f'Creating BCM Pricing Calculator client for region "{bcm_region}" and profile "{profile_name}"'
    )

    return session.client('bcm-pricing-calculator', config=config)


def get_aws_account_id(profile: Optional[str] = None) -> str:
    """Get the AWS account ID from the current credentials.

    Args:
        profile: AWS profile name to use (default: None, uses AWS_PROFILE or default profile)

    Returns:
        AWS account ID as a string

    Raises:
        Exception: If unable to retrieve account ID from AWS STS
    """
    profile_name = profile if profile else consts.AWS_PROFILE
    session = boto3.Session(profile_name=profile_name)
    sts_client = session.client('sts')

    response = sts_client.get_caller_identity()
    account_id = response['Account']
    logger.debug(f'Retrieved AWS account ID: {account_id}')
    return account_id
