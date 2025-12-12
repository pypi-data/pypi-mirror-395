# Copyright (c) 2025 oreokebu-dev
# SPDX-License-Identifier: MIT

"""Pricing discovery tools for BCM Pricing Calculator MCP Server.

These tools use the AWS Price List API to discover service codes, attributes,
and values that can be used with the BCM Pricing Calculator API.
"""

import re
import sys
from typing import Any, Dict, List, Optional, Union

import boto3
from botocore.config import Config
from loguru import logger
from mcp.server.fastmcp import Context

from bcm_pricing_calculator_mcp_server import consts

# Set up logging
logger.remove()
logger.add(sys.stderr, level=consts.LOG_LEVEL)


def create_pricing_client(profile: Optional[str] = None) -> Any:
    """Create an AWS Pricing API client.

    The AWS Pricing API is only available in us-east-1.

    Args:
        profile: AWS profile name to use (default: None, uses AWS_PROFILE or default profile)

    Returns:
        boto3 pricing client
    """
    profile_name = profile if profile else consts.AWS_PROFILE
    session = boto3.Session(profile_name=profile_name)

    config = Config(
        region_name='us-east-1',  # Pricing API only available in us-east-1
        user_agent_extra='bcm-pricing-calculator-mcp-server',
    )

    logger.debug(f'Creating pricing client for profile "{profile_name}"')
    return session.client('pricing', config=config)


async def create_error_response(
    ctx: Context,
    error_type: str,
    message: str,
    **kwargs,
) -> Dict[str, Any]:
    """Create a standardized error response."""
    logger.error(message)
    await ctx.error(message)

    return {
        'error_type': error_type,
        'message': message,
        **kwargs,
    }


async def get_pricing_service_codes(
    ctx: Context,
    filter: Optional[str] = None,
    use_cache: bool = True,
) -> Union[List[str], Dict[str, Any]]:
    """Get AWS service codes available in the Price List API.

    This is the starting point for discovering what services are available.

    Args:
        ctx: MCP context
        filter: Optional regex pattern to filter service codes (case-insensitive)
        use_cache: If True, returns common service codes without API call (default: True)

    Returns:
        List of service codes or error dictionary
    """
    # If use_cache is True and no filter, return common service codes
    if use_cache and not filter:
        logger.info(
            f'Returning {len(consts.COMMON_SERVICE_CODES)} common service codes from cache'
        )
        await ctx.info(
            f'Returned {len(consts.COMMON_SERVICE_CODES)} common service codes (use use_cache=False for complete list)'
        )
        return consts.COMMON_SERVICE_CODES

    logger.info('Retrieving AWS service codes from Price List API')

    try:
        pricing_client = create_pricing_client()
    except Exception as e:
        return await create_error_response(
            ctx=ctx,
            error_type='client_creation_failed',
            message=f'Failed to create AWS Pricing client: {str(e)}',
        )

    try:
        service_codes = []
        next_token = None

        while True:
            response = pricing_client.describe_services(
                **({'NextToken': next_token} if next_token else {})
            )
            service_codes.extend([service['ServiceCode'] for service in response['Services']])

            if 'NextToken' not in response:
                break
            next_token = response['NextToken']

    except Exception as e:
        return await create_error_response(
            ctx=ctx,
            error_type='api_error',
            message=f'Failed to retrieve service codes: {str(e)}',
        )

    if not service_codes:
        return await create_error_response(
            ctx=ctx,
            error_type='empty_results',
            message='No service codes returned from AWS Price List API',
        )

    # Apply regex filtering if provided
    if filter:
        try:
            regex_pattern = re.compile(filter, re.IGNORECASE)
            service_codes = [code for code in service_codes if regex_pattern.search(code)]

            if not service_codes:
                return await create_error_response(
                    ctx=ctx,
                    error_type='no_matches_found',
                    message=f'No service codes match the pattern: "{filter}"',
                    filter=filter,
                )
        except re.error as e:
            return await create_error_response(
                ctx=ctx,
                error_type='invalid_regex',
                message=f'Invalid regex pattern "{filter}": {str(e)}',
                filter=filter,
            )

    sorted_codes = sorted(service_codes)
    filter_msg = f' (filtered with pattern: "{filter}")' if filter else ''

    logger.info(f'Successfully retrieved {len(sorted_codes)} service codes{filter_msg}')
    await ctx.info(f'Successfully retrieved {len(sorted_codes)} service codes{filter_msg}')

    return sorted_codes


async def get_pricing_service_attributes(
    ctx: Context,
    service_code: str,
    filter: Optional[str] = None,
) -> Union[List[str], Dict[str, Any]]:
    """Get filterable attributes available for an AWS service.

    Use this to discover what dimensions you can filter by for a service.

    Args:
        ctx: MCP context
        service_code: AWS service code (e.g., 'AmazonEC2', 'AWSGlue')
        filter: Optional regex pattern to filter attribute names (case-insensitive)

    Returns:
        List of attribute names or error dictionary
    """
    logger.info(f'Retrieving attributes for AWS service: {service_code}')

    try:
        pricing_client = create_pricing_client()
    except Exception as e:
        return await create_error_response(
            ctx=ctx,
            error_type='client_creation_failed',
            message=f'Failed to create AWS Pricing client: {str(e)}',
            service_code=service_code,
        )

    try:
        response = pricing_client.describe_services(ServiceCode=service_code)
    except Exception as e:
        return await create_error_response(
            ctx=ctx,
            error_type='api_error',
            message=f'Failed to retrieve attributes for service "{service_code}": {str(e)}',
            service_code=service_code,
        )

    if not response.get('Services'):
        return await create_error_response(
            ctx=ctx,
            error_type='service_not_found',
            message=f'Service "{service_code}" not found',
            service_code=service_code,
        )

    attributes = response['Services'][0].get('AttributeNames', [])

    if not attributes:
        return await create_error_response(
            ctx=ctx,
            error_type='empty_results',
            message=f'Service "{service_code}" has no filterable attributes',
            service_code=service_code,
        )

    # Apply regex filtering if provided
    if filter:
        try:
            regex_pattern = re.compile(filter, re.IGNORECASE)
            attributes = [attr for attr in attributes if regex_pattern.search(attr)]

            if not attributes:
                return await create_error_response(
                    ctx=ctx,
                    error_type='no_matches_found',
                    message=f'No attributes match the pattern: "{filter}"',
                    service_code=service_code,
                    filter=filter,
                )
        except re.error as e:
            return await create_error_response(
                ctx=ctx,
                error_type='invalid_regex',
                message=f'Invalid regex pattern "{filter}": {str(e)}',
                service_code=service_code,
                filter=filter,
            )

    sorted_attributes = sorted(attributes)
    filter_msg = f' (filtered with pattern: "{filter}")' if filter else ''

    logger.info(
        f'Successfully retrieved {len(sorted_attributes)} attributes for {service_code}{filter_msg}'
    )
    await ctx.info(
        f'Successfully retrieved {len(sorted_attributes)} attributes for {service_code}{filter_msg}'
    )

    return sorted_attributes


async def get_pricing_attribute_values(
    ctx: Context,
    service_code: str,
    attribute_name: str,
    filter: Optional[str] = None,
) -> Union[List[str], Dict[str, Any]]:
    """Get valid values for a specific attribute of an AWS service.

    Use this to discover what values are available for filtering.

    Args:
        ctx: MCP context
        service_code: AWS service code (e.g., 'AmazonEC2', 'AWSGlue')
        attribute_name: Attribute name (e.g., 'instanceType', 'location')
        filter: Optional regex pattern to filter values (case-insensitive)

    Returns:
        List of attribute values or error dictionary
    """
    logger.info(f'Retrieving values for attribute "{attribute_name}" of service: {service_code}')

    try:
        pricing_client = create_pricing_client()
    except Exception as e:
        return await create_error_response(
            ctx=ctx,
            error_type='client_creation_failed',
            message=f'Failed to create AWS Pricing client: {str(e)}',
            service_code=service_code,
            attribute_name=attribute_name,
        )

    try:
        values = []
        next_token = None

        while True:
            params = {
                'ServiceCode': service_code,
                'AttributeName': attribute_name,
                'MaxResults': 100,
            }
            if next_token:
                params['NextToken'] = next_token

            response = pricing_client.get_attribute_values(**params)

            for attr_value in response.get('AttributeValues', []):
                if 'Value' in attr_value:
                    values.append(attr_value['Value'])

            if 'NextToken' in response:
                next_token = response['NextToken']
            else:
                break

    except Exception as e:
        return await create_error_response(
            ctx=ctx,
            error_type='api_error',
            message=f'Failed to retrieve values for attribute "{attribute_name}": {str(e)}',
            service_code=service_code,
            attribute_name=attribute_name,
        )

    if not values:
        # Provide helpful guidance for missing attributes
        suggestion = f'This attribute may not exist for this service. Check get_pricing_service_attributes("{service_code}") to see available attributes.'

        if attribute_name.lower() == 'operation':
            suggestion = f'Service "{service_code}" does not have an "operation" attribute. Use operation="" (empty string) when creating usage entries in BCM Pricing Calculator.'

        return await create_error_response(
            ctx=ctx,
            error_type='no_values_found',
            message=f'No values found for attribute "{attribute_name}" of service "{service_code}". {suggestion}',
            service_code=service_code,
            attribute_name=attribute_name,
            suggestion=suggestion,
        )

    # Apply regex filtering if provided
    if filter:
        try:
            regex_pattern = re.compile(filter, re.IGNORECASE)
            values = [value for value in values if regex_pattern.search(value)]

            if not values:
                return await create_error_response(
                    ctx=ctx,
                    error_type='no_matches_found',
                    message=f'No values match the pattern: "{filter}"',
                    service_code=service_code,
                    attribute_name=attribute_name,
                    filter=filter,
                )
        except re.error as e:
            return await create_error_response(
                ctx=ctx,
                error_type='invalid_regex',
                message=f'Invalid regex pattern "{filter}": {str(e)}',
                service_code=service_code,
                attribute_name=attribute_name,
                filter=filter,
            )

    sorted_values = sorted(values)
    filter_msg = f' (filtered with pattern: "{filter}")' if filter else ''

    # Enforce maximum results to prevent context overflow
    if len(sorted_values) > consts.MAX_ATTRIBUTE_VALUES:
        truncated_count = len(sorted_values)
        sorted_values = sorted_values[: consts.MAX_ATTRIBUTE_VALUES]
        warning_msg = f'Results truncated: showing {len(sorted_values)} of {truncated_count} values. Use filter parameter to narrow results.'
        logger.warning(warning_msg)
        await ctx.warning(warning_msg)

    logger.info(
        f'Successfully retrieved {len(sorted_values)} values for {attribute_name}{filter_msg}'
    )
    await ctx.info(
        f'Successfully retrieved {len(sorted_values)} values for {attribute_name}{filter_msg}'
    )

    return sorted_values
