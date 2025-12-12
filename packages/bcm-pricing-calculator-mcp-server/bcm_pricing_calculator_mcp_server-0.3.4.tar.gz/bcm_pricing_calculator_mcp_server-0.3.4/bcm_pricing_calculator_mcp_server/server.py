# Copyright (c) 2025 oreokebu-dev
# SPDX-License-Identifier: MIT

"""BCM Pricing Calculator MCP Server implementation."""

import sys
from typing import Any, Dict, List, Optional, Union

from loguru import logger
from mcp.server.fastmcp import Context, FastMCP
from pydantic import Field

from bcm_pricing_calculator_mcp_server import consts
from bcm_pricing_calculator_mcp_server.client import create_bcm_client, get_aws_account_id
from bcm_pricing_calculator_mcp_server.pricing_discovery import (
    get_pricing_attribute_values as _get_pricing_attribute_values,
)
from bcm_pricing_calculator_mcp_server.pricing_discovery import (
    get_pricing_service_attributes as _get_pricing_service_attributes,
)
from bcm_pricing_calculator_mcp_server.pricing_discovery import (
    get_pricing_service_codes as _get_pricing_service_codes,
)

# Set up logging
logger.remove()
logger.add(sys.stderr, level=consts.LOG_LEVEL)


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


mcp = FastMCP(
    name='bcm-pricing-calculator-mcp-server',
    instructions="""AWS Billing and Cost Management Pricing Calculator - Create cost estimates for planned AWS usage.

    ## CRITICAL VALIDATION RULES (Learn from errors!)

    1. **Names**: ONLY alphanumeric and hyphens `[a-zA-Z0-9-]+` - NO SPACES!
        "My Workload" → "My-Workload"

    2. **Keys**: Max 10 chars, alphanumeric only `[a-zA-Z0-9]{1,10}` - NO HYPHENS!
        "web-server-1" → "web1"

    3. **Account ID**: Exactly 12 digits (get with: aws sts get-caller-identity)

    4. **Region**: Must be "us-east-1" (only supported region)

    5. **Batch Limit**: Max 25 items per batch operation

    ## RECOMMENDED WORKFLOW: Workload Estimates (Simplest)

    **For cost estimates, use Workload Estimates - they're simpler than Bill Estimates:**

    1. **Create ONE workload estimate** (not multiple!)
       ```
       create_workload_estimate(name="My-Application", rate_type="BEFORE_DISCOUNTS")
       ```

    2. **Add ALL services to it** using the `group` field to organize:
       ```
       batch_create_workload_estimate_usage(
           workload_estimate_id="...",
           usage=[
               {serviceCode: "AmazonEC2", usageType: "BoxUsage:t3.medium",
                operation: "RunInstances", key: "web1", usageAccountId: "123456789012",
                amount: 730, group: "prod-us-east-1"},
               {serviceCode: "AmazonRDS", usageType: "InstanceUsage:db.t3.large",
                operation: "CreateDBInstance:0002", key: "db1", usageAccountId: "123456789012",
                amount: 730, group: "prod-database"}
           ]
       )
       ```

    3. **Get the total cost**:
       ```
       get_workload_estimate(identifier="...")
       # Returns: totalCost, costCurrency, and full breakdown by group
       ```

    4. **View detailed usage** (optional):
       ```
       list_workload_estimate_usage(workload_estimate_id="...")
       ```

    ## GROUP ORGANIZATION PATTERNS

    The `group` field is flexible - use any pattern that fits users needs:

    **By Architecture Tier:**
    - "web-tier", "app-tier", "database", "cache", "storage"

    **By Environment:**
    - "prod", "uat", "staging", "dev"

    **By Region:**
    - "us-east-1", "eu-west-1", "ap-southeast-1"

    **By Cost Center:**
    - "engineering", "marketing", "data-science"

    **Hybrid Approaches:**
    - "prod-us-east-1", "uat-eu-west-1"
    - "prod-web-tier", "prod-database"
    - "mobile-backend", "web-frontend", "analytics-pipeline"

    Groups help you analyze costs by any dimension that matters to your organization.

    ## BEST PRACTICES

    **DO**: Use ONE workload estimate with `group` field for organization
    **DO**: Use descriptive groups: "prod", "uat", "us-east-1", "web-tier", etc.
    **DO**: Call get_aws_account_id tool to retrieve usageAccountId
    **DO**: Check AWS docs for correct serviceCode, usageType, operation combinations
    **DO**: Use groups to compare regions, environments, or cost centers

    **DON'T**: Create multiple workload estimates unless comparing alternatives
    **DON'T**: Use spaces in names or hyphens in keys
    **DON'T**: Guess usageType/operation - they must match AWS pricing API exactly

    ## OPERATION FIELD HANDLING

    **CRITICAL DISCOVERY**: usageType is PRIMARY, operation is OPTIONAL

    **Field Hierarchy**: serviceCode (required) → usageType (required) → operation (optional)

    **Best Practice - Try Empty Operation First**:
    1. Discover correct usageType (this is the critical field)
    2. Try operation="" (empty string) first - works for many services
    3. Only if that fails, discover and use specific operation values

    **Why This Works**:
    - usageType is the primary matching key for pricing
    - operation is used for differentiation when multiple pricing tiers exist
    - Many services work fine with operation=""

    **Examples of Empty Operation Working**:
    - Route53: operation="" (no operation attribute exists)
    - SNS: operation="" (has operation attribute but empty works)
    - SQS: operation="" (has operation attribute but empty works)

    **When You Need Specific Operations**:
    - EC2: "RunInstances" (different purchase options)
    - RDS: "CreateDBInstance:0002" (Single-AZ vs Multi-AZ)
    - EKS: "CreateOperation" (different cluster types)

    **Discovery Strategy**:
    ```
    1. Get usageType (REQUIRED - use filters!)
    2. Try operation="" first
    3. If fails, check: get_pricing_service_attributes(serviceCode)
    4. If "operation" exists: get_pricing_attribute_values(serviceCode, "operation")
    5. If no "operation" attribute: try productFamily value or descriptive string
    ```

    ## COMMON SERVICE PATTERNS

    **Quick Reference** - Use these as starting points, then discover variations:

    | Service | usageType Example | operation | Notes |
    |---------|-------------------|-----------|-------|
    | AmazonEC2 | BoxUsage:t3.medium | RunInstances | Try operation="" first |
    | AmazonRDS | InstanceUsage:db.t3.large | CreateDBInstance:0002 | Operation indicates deployment |
    | AmazonEKS | USE1-AmazonEKS-Hours:perCluster | CreateOperation | Region-prefixed |
    | AmazonS3 | TimedStorage-ByteHrs | "" | Empty operation works |
    | AmazonDynamoDB | TimedStorage-ByteHrs | PayPerRequestThroughput | Multiple operations |
    | AmazonElastiCache | NodeUsage:cache.r6gd.12xlarge | CreateCacheCluster:0002 | Node type in usageType |
    | AmazonRoute53 | HostedZone | "" | No operation attribute |
    | AmazonCloudFront | DataTransfer-Out-Bytes | CloudFront | Simple operation |
    | AmazonSNS | Requests-Tier1 | "" | Empty works |
    | AWSQueueService | Requests-RBP | "" | SQS is AWSQueueService! |
    | AmazonSES | Recipients | Send | Requires operation |
    | AmazonCloudWatch | CW:MetricMonitorUsage | "" | Metrics: empty operation |
    | AmazonCloudWatch | USE1-VendedLog-Bytes | PutLogEvents | Logs: needs operation |
    | AWSLambda | Request | Invoke | Request-based |
    | AWSGlue | USE2-Crawler-DPU-Hour | "" | Region-prefixed DPU |

    **Discovery Pattern**:
    1. Check table above for starting point
    2. Use get_pricing_attribute_values(serviceCode, "usagetype", filter="keyword")
    3. Try operation="" first
    4. If fails, discover: get_pricing_attribute_values(serviceCode, "operation")

    ## ALTERNATIVE WORKFLOW: Bill Estimates (More Complex)

    Bill Estimates are for modeling changes to existing bills:
    1. Create bill scenario (requires existing bill data)
    2. Add usage/commitment modifications
    3. Create bill estimate from scenario
    4. View line items

    **Use Bill Estimates when**: Modeling changes to existing infrastructure
    **Use Workload Estimates when**: Estimating new deployments (most common)

    ## TROUBLESHOOTING & ERROR RECOVERY

    **General Strategy**: When you encounter an error, try these adaptive approaches:

    1. **Missing/Invalid Attribute Errors**:
       - If get_pricing_attribute_values() fails for an attribute (e.g., "operation")
       - Check if attribute exists: get_pricing_service_attributes(serviceCode)
       - If attribute is missing from the list, try using empty string "" or a descriptive value
       - Example: Route53 has no "operation" → use operation=""

    2. **Invalid usageType/operation Combination**:
       - ALWAYS try operation="" first (works for most services)
       - Use pricing discovery tools to find valid usageType
       - Try filtering: get_pricing_attribute_values(serviceCode, "usagetype", filter="keyword")
       - Check if usageType needs region prefix (e.g., "USE1-" for us-east-1)
       - Only if operation="" fails, discover specific operation values

    3. **Validation Errors**:
       - Check field constraints: names (alphanumeric + hyphens), keys (10 chars, no hyphens)
       - Verify account ID is exactly 12 digits
       - Ensure batch size ≤ 25 items

    4. **Data Unavailable Errors**:
       - Service might not be available in us-east-1 pricing
       - Try alternative usageType values
       - Check AWS documentation for service-specific requirements

    5. **Simplified Adaptive Discovery Pattern**:
       ```
       # Step 1: Discover usageType (THE CRITICAL FIELD)
       usageTypes = get_pricing_attribute_values(serviceCode, "usagetype", filter="keyword")

       # Step 2: Try with empty operation first
       batch_create_workload_estimate_usage(
           usage=[{
               "serviceCode": serviceCode,
               "usageType": selected_usageType,
               "operation": "",  # Try empty first!
               ...
           }]
       )

       # Step 3: Only if Step 2 fails, discover specific operation
       operations = get_pricing_attribute_values(serviceCode, "operation")
       # Or try productFamily value as operation
       # Or try descriptive string
       ```

    **Key Principles**:
    1. **usageType is PRIMARY** - focus discovery effort here
    2. **operation="" works for most services** - try it first
    3. **BCM API is flexible** - when discovery fails, try:
       - Empty operation string (simplest)
       - Region-prefixed usageTypes (USE1-, USE2-, EU-, etc.)
       - productFamily value as operation
       - Descriptive operation strings

    **Common Error Patterns**:
    - "No matching usage found" → Wrong usageType/operation combo, try discovery tools
    - "No values found for attribute 'operation'" → Use operation=""
    - "Validation error" → Check name/key format constraints
    - "Service quota exceeded" → Reduce batch size to ≤25 items
    - **Empty totalCost**: Call get_workload_estimate() to see calculated total
    """,
    dependencies=['pydantic', 'loguru', 'boto3'],
)


# ============================================================================
# WORKLOAD ESTIMATE OPERATIONS
# ============================================================================


@mcp.tool(
    name='create_workload_estimate',
    description="""Create a workload estimate - the STARTING POINT for cost estimates.

    IMPORTANT: Create ONE estimate per application/project, not one per tier!
    Use the "group" field in batch_create_workload_estimate_usage to organize services.

    Example: "My-Web-App" with groups: "web-tier", "app-tier", "database"
    NOT: "My-Web-App-Web-Tier", "My-Web-App-App-Tier", "My-Web-App-Database"

    Name rules: Only [a-zA-Z0-9-] (NO SPACES!)
    """,
)
async def create_workload_estimate(
    ctx: Context,
    name: str = Field(
        ...,
        description='Name (alphanumeric and hyphens only, NO SPACES). Example: "Production-App"',
    ),
    rate_type: str = Field(
        default='BEFORE_DISCOUNTS',
        description='Rate type: BEFORE_DISCOUNTS (list prices) or AFTER_DISCOUNTS (with your org discounts)',
    ),
) -> Dict[str, Any]:
    """Create a new workload estimate.

    Args:
        ctx: MCP context
        name: Name for the workload estimate
        rate_type: Rate type (BEFORE_DISCOUNTS or AFTER_DISCOUNTS)

    Returns:
        Dictionary containing the created workload estimate details
    """
    try:
        client = create_bcm_client()
    except Exception as e:
        return await create_error_response(
            ctx=ctx,
            error_type='client_creation_failed',
            message=f'Failed to create BCM client: {str(e)}',
        )

    try:
        response = client.create_workload_estimate(
            name=name,
            rateType=rate_type,
        )

        logger.info(f'Created workload estimate: {response.get("id")}')
        await ctx.info(f'Successfully created workload estimate: {name}')

        return {
            'status': 'success',
            'workload_estimate_id': response.get('id'),
            'name': response.get('name'),
            'rate_type': response.get('rateType'),
            'created_at': response.get('createdAt'),
        }
    except Exception as e:
        return await create_error_response(
            ctx=ctx,
            error_type='api_error',
            message=f'Failed to create workload estimate: {str(e)}',
            name=name,
        )


@mcp.tool(
    name='list_workload_estimates',
    description='List all workload estimates in your account',
)
async def list_workload_estimates(
    ctx: Context,
    max_results: int = Field(default=25, description='Maximum number of results to return'),
    next_token: Optional[str] = Field(default=None, description='Pagination token'),
) -> Dict[str, Any]:
    """List workload estimates.

    Args:
        ctx: MCP context
        max_results: Maximum number of results
        next_token: Pagination token

    Returns:
        Dictionary containing list of workload estimates
    """
    try:
        client = create_bcm_client()
    except Exception as e:
        return await create_error_response(
            ctx=ctx,
            error_type='client_creation_failed',
            message=f'Failed to create BCM client: {str(e)}',
        )

    try:
        params = {'maxResults': max_results}
        if next_token:
            params['nextToken'] = next_token

        response = client.list_workload_estimates(**params)

        items = response.get('items', [])
        logger.info(f'Retrieved {len(items)} workload estimates')
        await ctx.info(f'Successfully retrieved {len(items)} workload estimates')

        result = {
            'status': 'success',
            'workload_estimates': items,
            'count': len(items),
        }

        if 'nextToken' in response:
            result['next_token'] = response['nextToken']

        return result
    except Exception as e:
        return await create_error_response(
            ctx=ctx,
            error_type='api_error',
            message=f'Failed to list workload estimates: {str(e)}',
        )


@mcp.tool(
    name='get_workload_estimate',
    description="""Get workload estimate details INCLUDING TOTAL COST.

    This returns the calculated totalCost based on all usage entries added.
    The list view doesn't show costs - you MUST call this to see the total!

    Returns: id, name, status, totalCost, costCurrency, and metadata.
    """,
)
async def get_workload_estimate(
    ctx: Context,
    identifier: str = Field(
        ..., description='Workload estimate ID (UUID from create_workload_estimate)'
    ),
) -> Dict[str, Any]:
    """Get workload estimate details.

    Args:
        ctx: MCP context
        identifier: Workload estimate ID

    Returns:
        Dictionary containing workload estimate details
    """
    try:
        client = create_bcm_client()
    except Exception as e:
        return await create_error_response(
            ctx=ctx,
            error_type='client_creation_failed',
            message=f'Failed to create BCM client: {str(e)}',
        )

    try:
        response = client.get_workload_estimate(identifier=identifier)

        logger.info(f'Retrieved workload estimate: {identifier}')
        await ctx.info(f'Successfully retrieved workload estimate: {identifier}')

        return {
            'status': 'success',
            'workload_estimate': response,
        }
    except Exception as e:
        return await create_error_response(
            ctx=ctx,
            error_type='api_error',
            message=f'Failed to get workload estimate: {str(e)}',
            identifier=identifier,
        )


# ============================================================================
# BILL SCENARIO OPERATIONS
# ============================================================================


@mcp.tool(
    name='create_bill_scenario',
    description='Create a new bill scenario to model different cost configurations',
)
async def create_bill_scenario(
    ctx: Context,
    name: str = Field(..., description='Name for the bill scenario'),
    bill_estimate_id: str = Field(..., description='Bill estimate ID to associate with'),
) -> Dict[str, Any]:
    """Create a new bill scenario.

    Args:
        ctx: MCP context
        name: Name for the bill scenario
        bill_estimate_id: Bill estimate ID

    Returns:
        Dictionary containing the created bill scenario details
    """
    try:
        client = create_bcm_client()
    except Exception as e:
        return await create_error_response(
            ctx=ctx,
            error_type='client_creation_failed',
            message=f'Failed to create BCM client: {str(e)}',
        )

    try:
        response = client.create_bill_scenario(
            name=name,
            billEstimateId=bill_estimate_id,
        )

        logger.info(f'Created bill scenario: {response.get("id")}')
        await ctx.info(f'Successfully created bill scenario: {name}')

        return {
            'status': 'success',
            'bill_scenario_id': response.get('id'),
            'name': response.get('name'),
            'bill_estimate_id': response.get('billEstimateId'),
            'created_at': response.get('createdAt'),
        }
    except Exception as e:
        return await create_error_response(
            ctx=ctx,
            error_type='api_error',
            message=f'Failed to create bill scenario: {str(e)}',
            name=name,
        )


@mcp.tool(
    name='list_bill_scenarios',
    description='List all bill scenarios for a bill estimate',
)
async def list_bill_scenarios(
    ctx: Context,
    bill_estimate_id: str = Field(..., description='Bill estimate ID'),
    max_results: int = Field(default=25, description='Maximum number of results'),
    next_token: Optional[str] = Field(default=None, description='Pagination token'),
) -> Dict[str, Any]:
    """List bill scenarios.

    Args:
        ctx: MCP context
        bill_estimate_id: Bill estimate ID
        max_results: Maximum number of results
        next_token: Pagination token

    Returns:
        Dictionary containing list of bill scenarios
    """
    try:
        client = create_bcm_client()
    except Exception as e:
        return await create_error_response(
            ctx=ctx,
            error_type='client_creation_failed',
            message=f'Failed to create BCM client: {str(e)}',
        )

    try:
        params = {
            'billEstimateId': bill_estimate_id,
            'maxResults': max_results,
        }
        if next_token:
            params['nextToken'] = next_token

        response = client.list_bill_scenarios(**params)

        items = response.get('items', [])
        logger.info(f'Retrieved {len(items)} bill scenarios')
        await ctx.info(f'Successfully retrieved {len(items)} bill scenarios')

        result = {
            'status': 'success',
            'bill_scenarios': items,
            'count': len(items),
        }

        if 'nextToken' in response:
            result['next_token'] = response['nextToken']

        return result
    except Exception as e:
        return await create_error_response(
            ctx=ctx,
            error_type='api_error',
            message=f'Failed to list bill scenarios: {str(e)}',
        )


# ============================================================================
# BILL ESTIMATE OPERATIONS
# ============================================================================


@mcp.tool(
    name='create_bill_estimate',
    description='Create a new bill estimate to generate cost projections',
)
async def create_bill_estimate(
    ctx: Context,
    name: str = Field(..., description='Name for the bill estimate'),
) -> Dict[str, Any]:
    """Create a new bill estimate.

    Args:
        ctx: MCP context
        name: Name for the bill estimate

    Returns:
        Dictionary containing the created bill estimate details
    """
    try:
        client = create_bcm_client()
    except Exception as e:
        return await create_error_response(
            ctx=ctx,
            error_type='client_creation_failed',
            message=f'Failed to create BCM client: {str(e)}',
        )

    try:
        response = client.create_bill_estimate(name=name)

        logger.info(f'Created bill estimate: {response.get("id")}')
        await ctx.info(f'Successfully created bill estimate: {name}')

        return {
            'status': 'success',
            'bill_estimate_id': response.get('id'),
            'name': response.get('name'),
            'created_at': response.get('createdAt'),
        }
    except Exception as e:
        return await create_error_response(
            ctx=ctx,
            error_type='api_error',
            message=f'Failed to create bill estimate: {str(e)}',
            name=name,
        )


@mcp.tool(
    name='list_bill_estimates',
    description='List all bill estimates in your account',
)
async def list_bill_estimates(
    ctx: Context,
    max_results: int = Field(default=25, description='Maximum number of results'),
    next_token: Optional[str] = Field(default=None, description='Pagination token'),
) -> Dict[str, Any]:
    """List bill estimates.

    Args:
        ctx: MCP context
        max_results: Maximum number of results
        next_token: Pagination token

    Returns:
        Dictionary containing list of bill estimates
    """
    try:
        client = create_bcm_client()
    except Exception as e:
        return await create_error_response(
            ctx=ctx,
            error_type='client_creation_failed',
            message=f'Failed to create BCM client: {str(e)}',
        )

    try:
        params = {'maxResults': max_results}
        if next_token:
            params['nextToken'] = next_token

        response = client.list_bill_estimates(**params)

        items = response.get('items', [])
        logger.info(f'Retrieved {len(items)} bill estimates')
        await ctx.info(f'Successfully retrieved {len(items)} bill estimates')

        result = {
            'status': 'success',
            'bill_estimates': items,
            'count': len(items),
        }

        if 'nextToken' in response:
            result['next_token'] = response['nextToken']

        return result
    except Exception as e:
        return await create_error_response(
            ctx=ctx,
            error_type='api_error',
            message=f'Failed to list bill estimates: {str(e)}',
        )


@mcp.tool(
    name='get_bill_estimate',
    description='Get details and line items for a specific bill estimate',
)
async def get_bill_estimate(
    ctx: Context,
    identifier: str = Field(..., description='Bill estimate ID'),
) -> Dict[str, Any]:
    """Get bill estimate details.

    Args:
        ctx: MCP context
        identifier: Bill estimate ID

    Returns:
        Dictionary containing bill estimate details
    """
    try:
        client = create_bcm_client()
    except Exception as e:
        return await create_error_response(
            ctx=ctx,
            error_type='client_creation_failed',
            message=f'Failed to create BCM client: {str(e)}',
        )

    try:
        response = client.get_bill_estimate(identifier=identifier)

        logger.info(f'Retrieved bill estimate: {identifier}')
        await ctx.info(f'Successfully retrieved bill estimate: {identifier}')

        return {
            'status': 'success',
            'bill_estimate': response,
        }
    except Exception as e:
        return await create_error_response(
            ctx=ctx,
            error_type='api_error',
            message=f'Failed to get bill estimate: {str(e)}',
            identifier=identifier,
        )


@mcp.tool(
    name='list_bill_estimate_line_items',
    description='List detailed line items for a bill estimate showing cost breakdown',
)
async def list_bill_estimate_line_items(
    ctx: Context,
    bill_estimate_id: str = Field(..., description='Bill estimate ID'),
    max_results: int = Field(default=25, description='Maximum number of results'),
    next_token: Optional[str] = Field(default=None, description='Pagination token'),
) -> Dict[str, Any]:
    """List bill estimate line items.

    Args:
        ctx: MCP context
        bill_estimate_id: Bill estimate ID
        max_results: Maximum number of results
        next_token: Pagination token

    Returns:
        Dictionary containing list of line items with cost details
    """
    try:
        client = create_bcm_client()
    except Exception as e:
        return await create_error_response(
            ctx=ctx,
            error_type='client_creation_failed',
            message=f'Failed to create BCM client: {str(e)}',
        )

    try:
        params = {
            'billEstimateId': bill_estimate_id,
            'maxResults': max_results,
        }
        if next_token:
            params['nextToken'] = next_token

        response = client.list_bill_estimate_line_items(**params)

        items = response.get('items', [])
        logger.info(f'Retrieved {len(items)} line items')
        await ctx.info(f'Successfully retrieved {len(items)} line items')

        result = {
            'status': 'success',
            'line_items': items,
            'count': len(items),
        }

        if 'nextToken' in response:
            result['next_token'] = response['nextToken']

        return result
    except Exception as e:
        return await create_error_response(
            ctx=ctx,
            error_type='api_error',
            message=f'Failed to list bill estimate line items: {str(e)}',
        )


# ============================================================================
# BATCH OPERATIONS - WORKLOAD ESTIMATE USAGE
# ============================================================================


@mcp.tool(
    name='batch_create_workload_estimate_usage',
    description="""Add AWS services to a workload estimate - THIS IS WHERE COSTS ARE CALCULATED!

    Add up to 25 services at once. Use "group" field to organize by any dimension.

    CRITICAL: Each entry needs ALL these fields:
    - serviceCode: AWS service (e.g., "AmazonEC2", "AmazonRDS")
    - usageType: Specific resource type (e.g., "BoxUsage:t3.medium")
    - operation: Operation name (e.g., "RunInstances")
    - key: Unique identifier, max 10 chars, alphanumeric only (e.g., "web1", "db1")
    - amount: Usage quantity (e.g., 730 hours/month for 24/7)
    - usageAccountId: 12-digit AWS account ID (use get_aws_account_id tool to retrieve)
    - group: (optional) Organize by tier, environment, region, cost center, etc.
      Examples: "prod", "uat", "us-east-1", "web-tier", "prod-database"
    """,
)
async def batch_create_workload_estimate_usage(
    ctx: Context,
    workload_estimate_id: str = Field(
        ..., description='Workload estimate ID from create_workload_estimate'
    ),
    usage: List[Dict[str, Any]] = Field(
        ...,
        description='List of usage entries (max 25). See tool description for required fields and examples.',
    ),
) -> Dict[str, Any]:
    """Batch create workload estimate usage entries.

    Args:
        ctx: MCP context
        workload_estimate_id: The workload estimate ID
        usage: List of usage entries with required fields

    Returns:
        Dictionary containing created usage items and any errors
    """
    try:
        client = create_bcm_client()
    except Exception as e:
        return await create_error_response(
            ctx=ctx,
            error_type='client_creation_failed',
            message=f'Failed to create BCM client: {str(e)}',
        )

    try:
        response = client.batch_create_workload_estimate_usage(
            workloadEstimateId=workload_estimate_id,
            usage=usage,
        )

        items = response.get('items', [])
        errors = response.get('errors', [])

        logger.info(f'Created {len(items)} usage entries, {len(errors)} errors')
        await ctx.info(f'Created {len(items)} usage entries for workload estimate')

        return {
            'status': 'success',
            'items': items,
            'errors': errors,
            'created_count': len(items),
            'error_count': len(errors),
        }
    except Exception as e:
        return await create_error_response(
            ctx=ctx,
            error_type='api_error',
            message=f'Failed to create workload estimate usage: {str(e)}',
            workload_estimate_id=workload_estimate_id,
        )


@mcp.tool(
    name='batch_update_workload_estimate_usage',
    description='Update existing usage entries in a workload estimate',
)
async def batch_update_workload_estimate_usage(
    ctx: Context,
    workload_estimate_id: str = Field(..., description='Workload estimate ID'),
    usage: List[Dict[str, Any]] = Field(
        ...,
        description='List of usage entries to update (max 25). Must include "id" field for each entry.',
    ),
) -> Dict[str, Any]:
    """Batch update workload estimate usage entries.

    Args:
        ctx: MCP context
        workload_estimate_id: The workload estimate ID
        usage: List of usage entries with id and fields to update

    Returns:
        Dictionary containing updated usage items and any errors
    """
    try:
        client = create_bcm_client()
    except Exception as e:
        return await create_error_response(
            ctx=ctx,
            error_type='client_creation_failed',
            message=f'Failed to create BCM client: {str(e)}',
        )

    try:
        # Note: Update operations don't need usageAccountId, only id, group, and amount
        response = client.batch_update_workload_estimate_usage(
            workloadEstimateId=workload_estimate_id,
            usage=usage,
        )

        items = response.get('items', [])
        errors = response.get('errors', [])

        logger.info(f'Updated {len(items)} usage entries, {len(errors)} errors')
        await ctx.info(f'Updated {len(items)} usage entries for workload estimate')

        return {
            'status': 'success',
            'items': items,
            'errors': errors,
            'updated_count': len(items),
            'error_count': len(errors),
        }
    except Exception as e:
        return await create_error_response(
            ctx=ctx,
            error_type='api_error',
            message=f'Failed to update workload estimate usage: {str(e)}',
            workload_estimate_id=workload_estimate_id,
        )


@mcp.tool(
    name='batch_delete_workload_estimate_usage',
    description='Delete usage entries from a workload estimate',
)
async def batch_delete_workload_estimate_usage(
    ctx: Context,
    workload_estimate_id: str = Field(..., description='Workload estimate ID'),
    ids: List[str] = Field(..., description='List of usage entry IDs to delete (max 25)'),
) -> Dict[str, Any]:
    """Batch delete workload estimate usage entries.

    Args:
        ctx: MCP context
        workload_estimate_id: The workload estimate ID
        ids: List of usage entry IDs to delete

    Returns:
        Dictionary containing deletion results and any errors
    """
    try:
        client = create_bcm_client()
    except Exception as e:
        return await create_error_response(
            ctx=ctx,
            error_type='client_creation_failed',
            message=f'Failed to create BCM client: {str(e)}',
        )

    try:
        response = client.batch_delete_workload_estimate_usage(
            workloadEstimateId=workload_estimate_id,
            ids=ids,
        )

        errors = response.get('errors', [])
        deleted_count = len(ids) - len(errors)

        logger.info(f'Deleted {deleted_count} usage entries, {len(errors)} errors')
        await ctx.info(f'Deleted {deleted_count} usage entries from workload estimate')

        return {
            'status': 'success',
            'errors': errors,
            'deleted_count': deleted_count,
            'error_count': len(errors),
        }
    except Exception as e:
        return await create_error_response(
            ctx=ctx,
            error_type='api_error',
            message=f'Failed to delete workload estimate usage: {str(e)}',
            workload_estimate_id=workload_estimate_id,
        )


@mcp.tool(
    name='update_workload_estimate',
    description='Update workload estimate metadata (name, rate type)',
)
async def update_workload_estimate(
    ctx: Context,
    identifier: str = Field(..., description='Workload estimate ID'),
    name: Optional[str] = Field(default=None, description='New name for the workload estimate'),
    rate_type: Optional[str] = Field(
        default=None,
        description='New rate type: BEFORE_DISCOUNTS or AFTER_DISCOUNTS',
    ),
) -> Dict[str, Any]:
    """Update a workload estimate.

    Args:
        ctx: MCP context
        identifier: Workload estimate ID
        name: Optional new name
        rate_type: Optional new rate type

    Returns:
        Dictionary containing updated workload estimate details
    """
    try:
        client = create_bcm_client()
    except Exception as e:
        return await create_error_response(
            ctx=ctx,
            error_type='client_creation_failed',
            message=f'Failed to create BCM client: {str(e)}',
        )

    try:
        params = {'identifier': identifier}
        if name:
            params['name'] = name
        if rate_type:
            params['rateType'] = rate_type

        response = client.update_workload_estimate(**params)

        logger.info(f'Updated workload estimate: {identifier}')
        await ctx.info(f'Successfully updated workload estimate: {identifier}')

        return {
            'status': 'success',
            'workload_estimate_id': response.get('id'),
            'name': response.get('name'),
            'rate_type': response.get('rateType'),
        }
    except Exception as e:
        return await create_error_response(
            ctx=ctx,
            error_type='api_error',
            message=f'Failed to update workload estimate: {str(e)}',
            identifier=identifier,
        )


@mcp.tool(
    name='delete_workload_estimate',
    description='Delete a workload estimate and all its usage entries',
)
async def delete_workload_estimate(
    ctx: Context,
    identifier: str = Field(..., description='Workload estimate ID to delete'),
) -> Dict[str, Any]:
    """Delete a workload estimate.

    Args:
        ctx: MCP context
        identifier: Workload estimate ID

    Returns:
        Dictionary containing deletion confirmation
    """
    try:
        client = create_bcm_client()
    except Exception as e:
        return await create_error_response(
            ctx=ctx,
            error_type='client_creation_failed',
            message=f'Failed to create BCM client: {str(e)}',
        )

    try:
        client.delete_workload_estimate(identifier=identifier)

        logger.info(f'Deleted workload estimate: {identifier}')
        await ctx.info(f'Successfully deleted workload estimate: {identifier}')

        return {
            'status': 'success',
            'message': f'Workload estimate {identifier} deleted successfully',
            'workload_estimate_id': identifier,
        }
    except Exception as e:
        return await create_error_response(
            ctx=ctx,
            error_type='api_error',
            message=f'Failed to delete workload estimate: {str(e)}',
            identifier=identifier,
        )


@mcp.tool(
    name='list_workload_estimate_usage',
    description='List usage entries for a workload estimate',
)
async def list_workload_estimate_usage(
    ctx: Context,
    workload_estimate_id: str = Field(..., description='Workload estimate ID'),
    max_results: int = Field(default=25, description='Maximum number of results'),
    next_token: Optional[str] = Field(default=None, description='Pagination token'),
) -> Dict[str, Any]:
    """List workload estimate usage entries.

    Args:
        ctx: MCP context
        workload_estimate_id: The workload estimate ID
        max_results: Maximum number of results
        next_token: Pagination token

    Returns:
        Dictionary containing list of usage entries
    """
    try:
        client = create_bcm_client()
    except Exception as e:
        return await create_error_response(
            ctx=ctx,
            error_type='client_creation_failed',
            message=f'Failed to create BCM client: {str(e)}',
        )

    try:
        params = {
            'workloadEstimateId': workload_estimate_id,
            'maxResults': max_results,
        }
        if next_token:
            params['nextToken'] = next_token

        response = client.list_workload_estimate_usage(**params)

        items = response.get('items', [])
        logger.info(f'Retrieved {len(items)} usage entries')
        await ctx.info(f'Successfully retrieved {len(items)} usage entries')

        result = {
            'status': 'success',
            'usage_entries': items,
            'count': len(items),
        }

        if 'nextToken' in response:
            result['next_token'] = response['nextToken']

        return result
    except Exception as e:
        return await create_error_response(
            ctx=ctx,
            error_type='api_error',
            message=f'Failed to list workload estimate usage: {str(e)}',
        )


# ============================================================================
# PRICING DISCOVERY TOOLS
# ============================================================================


@mcp.tool(
    name='get_pricing_service_codes',
    description="""Discover AWS service codes available in the Price List API.

    This is the FIRST STEP for discovering service information. Use this to find
    the correct service code before querying pricing or creating estimates.

    By default, returns 30+ common service codes WITHOUT making an API call for
    faster response. Set use_cache=False to get the complete list from AWS API.

    Returns service codes like 'AmazonEC2', 'AWSGlue', 'AmazonRDS' that can be
    used with other pricing tools and BCM Pricing Calculator API.

    Optional filter parameter accepts regex patterns (case-insensitive):
    - "glue" matches "AWSGlue"
    - "^Amazon" matches services starting with "Amazon"
    - "bedrock" matches "AmazonBedrock"

    Common service codes included in cache:
    AmazonEC2, AmazonS3, AmazonRDS, AWSLambda, AmazonDynamoDB, AmazonEKS,
    AWSGlue, AmazonElastiCache, AmazonCloudFront, AmazonRoute53, and more.
    """,
)
async def get_pricing_service_codes(
    ctx: Context,
    filter: Optional[str] = Field(
        default=None, description='Optional regex pattern to filter service codes'
    ),
    use_cache: bool = Field(
        default=True,
        description='Use cached common service codes (True) or fetch complete list from API (False)',
    ),
) -> Union[List[str], Dict[str, Any]]:
    """Get AWS service codes from Price List API."""
    return await _get_pricing_service_codes(ctx, filter, use_cache)


@mcp.tool(
    name='get_pricing_service_attributes',
    description="""Get filterable attributes available for an AWS service.

    Use this AFTER get_pricing_service_codes() to discover what dimensions you
    can filter by for a specific service.

    Returns attribute names like 'instanceType', 'location', 'usageType', 'operation'
    that can be used to query pricing data.

    These attributes help you understand what filters are available when querying
    pricing information for creating BCM estimates.
    """,
)
async def get_pricing_service_attributes(
    ctx: Context,
    service_code: str = Field(..., description='AWS service code (e.g., "AmazonEC2", "AWSGlue")'),
    filter: Optional[str] = Field(
        default=None, description='Optional regex pattern to filter attribute names'
    ),
) -> Union[List[str], Dict[str, Any]]:
    """Get filterable attributes for an AWS service."""
    return await _get_pricing_service_attributes(ctx, service_code, filter)


@mcp.tool(
    name='get_pricing_attribute_values',
    description="""Get valid values for a specific attribute of an AWS service.

    Use this AFTER get_pricing_service_attributes() to discover what values are
    available for a specific attribute.

    **IMPORTANT: Use the filter parameter to avoid context overflow!**
    Many attributes (especially usageType) have hundreds of values. Always use
    a regex filter to narrow results to what you need.

    Examples:
    - For EKS cluster pricing: filter="cluster"
    - For EC2 t3 instances: filter="t3\\."
    - For specific region: filter="^USE1-" (us-east-1)
    - For RDS MySQL: filter="mysql"

    For AWSGlue with attribute 'usageType' and filter="ETL":
    - 'USE1-ETL-DPU-Hour'
    - 'USE2-ETL-DPU-Hour'
    - 'APN1-ETL-DPU-Hour'

    These values can be used directly in BCM Pricing Calculator API calls.
    """,
)
async def get_pricing_attribute_values(
    ctx: Context,
    service_code: str = Field(..., description='AWS service code (e.g., "AmazonEC2", "AWSGlue")'),
    attribute_name: str = Field(
        ..., description='Attribute name (e.g., "usageType", "operation")'
    ),
    filter: Optional[str] = Field(
        default=None,
        description='RECOMMENDED: Regex pattern to filter values (e.g., "cluster", "t3\\.", "^USE1-"). Prevents context overflow.',
    ),
) -> Union[List[str], Dict[str, Any]]:
    """Get valid values for a specific attribute.

    NOTE: If this returns an error for attribute_name="operation", it means the service
    doesn't have operations in the Price List API. In that case, use operation="" (empty string)
    when creating usage entries in BCM Pricing Calculator.
    """
    return await _get_pricing_attribute_values(ctx, service_code, attribute_name, filter)


# ============================================================================
# UTILITY TOOLS
# ============================================================================


@mcp.tool(
    name='get_aws_account_id',
    description='Get the AWS account ID from current credentials. Use this to populate usageAccountId in usage entries.',
)
async def get_aws_account_id_tool(ctx: Context) -> Dict[str, Any]:
    """Get AWS account ID from current credentials.

    Args:
        ctx: MCP context

    Returns:
        Dictionary containing the AWS account ID
    """
    try:
        account_id = get_aws_account_id()

        logger.info(f'Retrieved AWS account ID: {account_id}')
        await ctx.info(f'Successfully retrieved AWS account ID: {account_id}')

        return {
            'status': 'success',
            'account_id': account_id,
        }
    except Exception as e:
        return await create_error_response(
            ctx=ctx,
            error_type='api_error',
            message=f'Failed to get AWS account ID: {str(e)}',
        )


# ============================================================================
# PREFERENCES
# ============================================================================


@mcp.tool(
    name='get_preferences',
    description='Get your pricing calculator preferences including discount and benefit sharing settings',
)
async def get_preferences(ctx: Context) -> Dict[str, Any]:
    """Get pricing calculator preferences.

    Args:
        ctx: MCP context

    Returns:
        Dictionary containing preference settings
    """
    try:
        client = create_bcm_client()
    except Exception as e:
        return await create_error_response(
            ctx=ctx,
            error_type='client_creation_failed',
            message=f'Failed to create BCM client: {str(e)}',
        )

    try:
        response = client.get_preferences()

        logger.info('Retrieved pricing calculator preferences')
        await ctx.info('Successfully retrieved preferences')

        return {
            'status': 'success',
            'preferences': response,
        }
    except Exception as e:
        return await create_error_response(
            ctx=ctx,
            error_type='api_error',
            message=f'Failed to get preferences: {str(e)}',
        )


def main():
    """Main entry point for the MCP server."""
    mcp.run()


if __name__ == '__main__':
    main()
