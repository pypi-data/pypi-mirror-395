# Copyright (c) 2025 oreokebu-dev
# SPDX-License-Identifier: MIT

"""Tests for BCM Pricing Calculator MCP Server."""

from unittest.mock import MagicMock, patch

import pytest

from bcm_pricing_calculator_mcp_server.client import get_aws_account_id
from bcm_pricing_calculator_mcp_server.server import (
    batch_create_workload_estimate_usage,
    batch_delete_workload_estimate_usage,
    batch_update_workload_estimate_usage,
    create_bill_estimate,
    create_bill_scenario,
    create_workload_estimate,
    delete_workload_estimate,
    get_aws_account_id_tool,
    get_bill_estimate,
    get_preferences,
    get_workload_estimate,
    list_bill_estimate_line_items,
    list_bill_estimates,
    list_bill_scenarios,
    list_workload_estimate_usage,
    list_workload_estimates,
    update_workload_estimate,
)


@pytest.fixture
def mock_context():
    """Create a mock MCP context."""
    ctx = MagicMock()

    # Make async methods return coroutines
    async def async_mock(*args, **kwargs):
        pass

    ctx.info = MagicMock(side_effect=async_mock)
    ctx.error = MagicMock(side_effect=async_mock)
    return ctx


@pytest.mark.asyncio
async def test_create_workload_estimate_success(mock_context):
    """Test successful workload estimate creation."""
    with patch('bcm_pricing_calculator_mcp_server.server.create_bcm_client') as mock_client:
        mock_bcm = MagicMock()
        mock_bcm.create_workload_estimate.return_value = {
            'id': 'test-workload-123',
            'name': 'Test Workload',
            'rateType': 'BEFORE_DISCOUNTS',
            'createdAt': '2025-01-01T00:00:00Z',
        }
        mock_client.return_value = mock_bcm

        result = await create_workload_estimate(
            ctx=mock_context,
            name='Test Workload',
            rate_type='BEFORE_DISCOUNTS',
        )

        assert result['status'] == 'success'
        assert result['workload_estimate_id'] == 'test-workload-123'
        assert result['name'] == 'Test Workload'
        mock_context.info.assert_called_once()


@pytest.mark.asyncio
async def test_list_workload_estimates_success(mock_context):
    """Test successful workload estimates listing."""
    with patch('bcm_pricing_calculator_mcp_server.server.create_bcm_client') as mock_client:
        mock_bcm = MagicMock()
        mock_bcm.list_workload_estimates.return_value = {
            'items': [
                {'id': 'workload-1', 'name': 'Workload 1'},
                {'id': 'workload-2', 'name': 'Workload 2'},
            ]
        }
        mock_client.return_value = mock_bcm

        result = await list_workload_estimates(ctx=mock_context)

        assert result['status'] == 'success'
        assert result['count'] == 2
        assert len(result['workload_estimates']) == 2
        mock_context.info.assert_called_once()


@pytest.mark.asyncio
async def test_create_bill_estimate_success(mock_context):
    """Test successful bill estimate creation."""
    with patch('bcm_pricing_calculator_mcp_server.server.create_bcm_client') as mock_client:
        mock_bcm = MagicMock()
        mock_bcm.create_bill_estimate.return_value = {
            'id': 'test-bill-123',
            'name': 'Test Bill',
            'createdAt': '2025-01-01T00:00:00Z',
        }
        mock_client.return_value = mock_bcm

        result = await create_bill_estimate(
            ctx=mock_context,
            name='Test Bill',
        )

        assert result['status'] == 'success'
        assert result['bill_estimate_id'] == 'test-bill-123'
        assert result['name'] == 'Test Bill'
        mock_context.info.assert_called_once()


@pytest.mark.asyncio
async def test_client_creation_failure(mock_context):
    """Test handling of client creation failure."""
    with patch('bcm_pricing_calculator_mcp_server.server.create_bcm_client') as mock_client:
        mock_client.side_effect = Exception('AWS credentials not found')

        result = await create_workload_estimate(
            ctx=mock_context,
            name='Test Workload',
        )

        assert result['error_type'] == 'client_creation_failed'
        assert 'AWS credentials not found' in result['message']
        mock_context.error.assert_called_once()


@pytest.mark.asyncio
async def test_get_workload_estimate_success(mock_context):
    """Test successful workload estimate retrieval."""
    with patch('bcm_pricing_calculator_mcp_server.server.create_bcm_client') as mock_client:
        mock_bcm = MagicMock()
        mock_bcm.get_workload_estimate.return_value = {
            'id': 'test-workload-123',
            'name': 'Test Workload',
            'totalCost': 100.50,
            'costCurrency': 'USD',
        }
        mock_client.return_value = mock_bcm

        result = await get_workload_estimate(
            ctx=mock_context,
            identifier='test-workload-123',
        )

        assert result['status'] == 'success'
        assert result['workload_estimate']['id'] == 'test-workload-123'
        assert result['workload_estimate']['totalCost'] == 100.50
        mock_context.info.assert_called_once()


@pytest.mark.asyncio
async def test_update_workload_estimate_success(mock_context):
    """Test successful workload estimate update."""
    with patch('bcm_pricing_calculator_mcp_server.server.create_bcm_client') as mock_client:
        mock_bcm = MagicMock()
        mock_bcm.update_workload_estimate.return_value = {
            'id': 'test-workload-123',
            'name': 'Updated Workload',
            'rateType': 'AFTER_DISCOUNTS',
        }
        mock_client.return_value = mock_bcm

        result = await update_workload_estimate(
            ctx=mock_context,
            identifier='test-workload-123',
            name='Updated Workload',
            rate_type='AFTER_DISCOUNTS',
        )

        assert result['status'] == 'success'
        assert result['name'] == 'Updated Workload'
        assert result['rate_type'] == 'AFTER_DISCOUNTS'
        mock_context.info.assert_called_once()


@pytest.mark.asyncio
async def test_delete_workload_estimate_success(mock_context):
    """Test successful workload estimate deletion."""
    with patch('bcm_pricing_calculator_mcp_server.server.create_bcm_client') as mock_client:
        mock_bcm = MagicMock()
        mock_bcm.delete_workload_estimate.return_value = {}
        mock_client.return_value = mock_bcm

        result = await delete_workload_estimate(
            ctx=mock_context,
            identifier='test-workload-123',
        )

        assert result['status'] == 'success'
        assert 'deleted successfully' in result['message']
        mock_context.info.assert_called_once()


@pytest.mark.asyncio
async def test_batch_create_workload_estimate_usage_success(mock_context):
    """Test successful batch creation of workload estimate usage."""
    with patch('bcm_pricing_calculator_mcp_server.server.create_bcm_client') as mock_client:
        mock_bcm = MagicMock()
        mock_bcm.batch_create_workload_estimate_usage.return_value = {
            'items': [
                {'id': 'usage-1', 'serviceCode': 'AmazonEC2'},
                {'id': 'usage-2', 'serviceCode': 'AmazonS3'},
            ],
            'errors': [],
        }
        mock_client.return_value = mock_bcm

        usage_entries = [
            {
                'serviceCode': 'AmazonEC2',
                'key': 'web1',
                'amount': 730,
                'usageAccountId': '123456789012',
            },
            {
                'serviceCode': 'AmazonS3',
                'key': 's3',
                'amount': 100,
                'usageAccountId': '123456789012',
            },
        ]

        result = await batch_create_workload_estimate_usage(
            ctx=mock_context,
            workload_estimate_id='test-workload-123',
            usage=usage_entries,
        )

        assert result['status'] == 'success'
        assert result['created_count'] == 2
        assert result['error_count'] == 0
        mock_context.info.assert_called_once()


@pytest.mark.asyncio
async def test_batch_update_workload_estimate_usage_success(mock_context):
    """Test successful batch update of workload estimate usage."""
    with patch('bcm_pricing_calculator_mcp_server.server.create_bcm_client') as mock_client:
        mock_bcm = MagicMock()
        mock_bcm.batch_update_workload_estimate_usage.return_value = {
            'items': [{'id': 'usage-1', 'amount': 1460}],
            'errors': [],
        }
        mock_client.return_value = mock_bcm

        usage_entries = [{'id': 'usage-1', 'amount': 1460}]

        result = await batch_update_workload_estimate_usage(
            ctx=mock_context,
            workload_estimate_id='test-workload-123',
            usage=usage_entries,
        )

        assert result['status'] == 'success'
        assert result['updated_count'] == 1
        mock_context.info.assert_called_once()


@pytest.mark.asyncio
async def test_batch_delete_workload_estimate_usage_success(mock_context):
    """Test successful batch deletion of workload estimate usage."""
    with patch('bcm_pricing_calculator_mcp_server.server.create_bcm_client') as mock_client:
        mock_bcm = MagicMock()
        mock_bcm.batch_delete_workload_estimate_usage.return_value = {
            'errors': [],
        }
        mock_client.return_value = mock_bcm

        result = await batch_delete_workload_estimate_usage(
            ctx=mock_context,
            workload_estimate_id='test-workload-123',
            ids=['usage-1', 'usage-2'],
        )

        assert result['status'] == 'success'
        assert result['deleted_count'] == 2
        assert result['error_count'] == 0
        mock_context.info.assert_called_once()


@pytest.mark.asyncio
async def test_list_workload_estimate_usage_success(mock_context):
    """Test successful listing of workload estimate usage."""
    with patch('bcm_pricing_calculator_mcp_server.server.create_bcm_client') as mock_client:
        mock_bcm = MagicMock()
        mock_bcm.list_workload_estimate_usage.return_value = {
            'items': [
                {'id': 'usage-1', 'serviceCode': 'AmazonEC2'},
                {'id': 'usage-2', 'serviceCode': 'AmazonS3'},
            ],
        }
        mock_client.return_value = mock_bcm

        result = await list_workload_estimate_usage(
            ctx=mock_context,
            workload_estimate_id='test-workload-123',
        )

        assert result['status'] == 'success'
        assert result['count'] == 2
        assert len(result['usage_entries']) == 2
        mock_context.info.assert_called_once()


@pytest.mark.asyncio
async def test_get_preferences_success(mock_context):
    """Test successful preferences retrieval."""
    with patch('bcm_pricing_calculator_mcp_server.server.create_bcm_client') as mock_client:
        mock_bcm = MagicMock()
        mock_bcm.get_preferences.return_value = {
            'managementAccountRateTypeSelections': ['BEFORE_DISCOUNTS', 'AFTER_DISCOUNTS'],
            'memberAccountRateTypeSelections': ['BEFORE_DISCOUNTS'],
        }
        mock_client.return_value = mock_bcm

        result = await get_preferences(ctx=mock_context)

        assert result['status'] == 'success'
        assert 'managementAccountRateTypeSelections' in result['preferences']
        mock_context.info.assert_called_once()


@pytest.mark.asyncio
async def test_api_error_handling(mock_context):
    """Test handling of API errors."""
    with patch('bcm_pricing_calculator_mcp_server.server.create_bcm_client') as mock_client:
        mock_bcm = MagicMock()
        mock_bcm.get_workload_estimate.side_effect = Exception('API rate limit exceeded')
        mock_client.return_value = mock_bcm

        result = await get_workload_estimate(
            ctx=mock_context,
            identifier='test-workload-123',
        )

        assert result['error_type'] == 'api_error'
        assert 'API rate limit exceeded' in result['message']
        mock_context.error.assert_called_once()


# ============================================================================
# BILL ESTIMATE TESTS
# ============================================================================


@pytest.mark.asyncio
async def test_list_bill_estimates_success(mock_context):
    """Test successful bill estimates listing."""
    with patch('bcm_pricing_calculator_mcp_server.server.create_bcm_client') as mock_client:
        mock_bcm = MagicMock()
        mock_bcm.list_bill_estimates.return_value = {
            'items': [
                {'id': 'bill-1', 'name': 'Bill 1'},
                {'id': 'bill-2', 'name': 'Bill 2'},
                {'id': 'bill-3', 'name': 'Bill 3'},
            ]
        }
        mock_client.return_value = mock_bcm

        result = await list_bill_estimates(ctx=mock_context)

        assert result['status'] == 'success'
        assert result['count'] == 3
        assert len(result['bill_estimates']) == 3
        mock_context.info.assert_called_once()


@pytest.mark.asyncio
async def test_get_bill_estimate_success(mock_context):
    """Test successful bill estimate retrieval."""
    with patch('bcm_pricing_calculator_mcp_server.server.create_bcm_client') as mock_client:
        mock_bcm = MagicMock()
        mock_bcm.get_bill_estimate.return_value = {
            'id': 'bill-123',
            'name': 'Test Bill',
            'status': 'VALID',
        }
        mock_client.return_value = mock_bcm

        result = await get_bill_estimate(
            ctx=mock_context,
            identifier='bill-123',
        )

        assert result['status'] == 'success'
        assert result['bill_estimate']['id'] == 'bill-123'
        mock_context.info.assert_called_once()


@pytest.mark.asyncio
async def test_list_bill_estimate_line_items_success(mock_context):
    """Test successful bill estimate line items listing."""
    with patch('bcm_pricing_calculator_mcp_server.server.create_bcm_client') as mock_client:
        mock_bcm = MagicMock()
        mock_bcm.list_bill_estimate_line_items.return_value = {
            'items': [
                {'id': 'line-1', 'serviceCode': 'AmazonEC2', 'cost': 50.0},
                {'id': 'line-2', 'serviceCode': 'AmazonS3', 'cost': 10.0},
            ]
        }
        mock_client.return_value = mock_bcm

        result = await list_bill_estimate_line_items(
            ctx=mock_context,
            bill_estimate_id='bill-123',
        )

        assert result['status'] == 'success'
        assert result['count'] == 2
        assert len(result['line_items']) == 2
        mock_context.info.assert_called_once()


@pytest.mark.asyncio
async def test_list_bill_estimate_line_items_with_pagination(mock_context):
    """Test bill estimate line items with pagination."""
    with patch('bcm_pricing_calculator_mcp_server.server.create_bcm_client') as mock_client:
        mock_bcm = MagicMock()
        mock_bcm.list_bill_estimate_line_items.return_value = {
            'items': [{'id': f'line-{i}'} for i in range(25)],
            'nextToken': 'next-page-token',
        }
        mock_client.return_value = mock_bcm

        result = await list_bill_estimate_line_items(
            ctx=mock_context,
            bill_estimate_id='bill-123',
            max_results=25,
        )

        assert result['status'] == 'success'
        assert result['count'] == 25
        assert 'next_token' in result
        assert result['next_token'] == 'next-page-token'


# ============================================================================
# BILL SCENARIO TESTS
# ============================================================================


@pytest.mark.asyncio
async def test_create_bill_scenario_success(mock_context):
    """Test successful bill scenario creation."""
    with patch('bcm_pricing_calculator_mcp_server.server.create_bcm_client') as mock_client:
        mock_bcm = MagicMock()
        mock_bcm.create_bill_scenario.return_value = {
            'id': 'scenario-123',
            'name': 'Test Scenario',
            'billEstimateId': 'bill-123',
            'createdAt': '2025-01-01T00:00:00Z',
        }
        mock_client.return_value = mock_bcm

        result = await create_bill_scenario(
            ctx=mock_context,
            name='Test Scenario',
            bill_estimate_id='bill-123',
        )

        assert result['status'] == 'success'
        assert result['bill_scenario_id'] == 'scenario-123'
        assert result['name'] == 'Test Scenario'
        assert result['bill_estimate_id'] == 'bill-123'
        mock_context.info.assert_called_once()


@pytest.mark.asyncio
async def test_list_bill_scenarios_success(mock_context):
    """Test successful bill scenarios listing."""
    with patch('bcm_pricing_calculator_mcp_server.server.create_bcm_client') as mock_client:
        mock_bcm = MagicMock()
        mock_bcm.list_bill_scenarios.return_value = {
            'items': [
                {'id': 'scenario-1', 'name': 'Scenario 1'},
                {'id': 'scenario-2', 'name': 'Scenario 2'},
            ]
        }
        mock_client.return_value = mock_bcm

        result = await list_bill_scenarios(
            ctx=mock_context,
            bill_estimate_id='bill-123',
        )

        assert result['status'] == 'success'
        assert result['count'] == 2
        assert len(result['bill_scenarios']) == 2
        mock_context.info.assert_called_once()


# ============================================================================
# PAGINATION TESTS
# ============================================================================


@pytest.mark.asyncio
async def test_list_workload_estimates_with_pagination(mock_context):
    """Test workload estimates listing with pagination."""
    with patch('bcm_pricing_calculator_mcp_server.server.create_bcm_client') as mock_client:
        mock_bcm = MagicMock()
        mock_bcm.list_workload_estimates.return_value = {
            'items': [{'id': f'workload-{i}'} for i in range(25)],
            'nextToken': 'pagination-token',
        }
        mock_client.return_value = mock_bcm

        result = await list_workload_estimates(
            ctx=mock_context,
            max_results=25,
            next_token='previous-token',
        )

        assert result['status'] == 'success'
        assert result['count'] == 25
        assert 'next_token' in result
        assert result['next_token'] == 'pagination-token'


@pytest.mark.asyncio
async def test_list_workload_estimate_usage_with_pagination(mock_context):
    """Test usage listing with pagination."""
    with patch('bcm_pricing_calculator_mcp_server.server.create_bcm_client') as mock_client:
        mock_bcm = MagicMock()
        mock_bcm.list_workload_estimate_usage.return_value = {
            'items': [{'id': f'usage-{i}'} for i in range(10)],
            'nextToken': 'next-page',
        }
        mock_client.return_value = mock_bcm

        result = await list_workload_estimate_usage(
            ctx=mock_context,
            workload_estimate_id='workload-123',
            max_results=10,
        )

        assert result['status'] == 'success'
        assert result['count'] == 10
        assert 'next_token' in result


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================


@pytest.mark.asyncio
async def test_batch_create_usage_with_errors(mock_context):
    """Test batch create with partial errors."""
    with patch('bcm_pricing_calculator_mcp_server.server.create_bcm_client') as mock_client:
        mock_bcm = MagicMock()
        mock_bcm.batch_create_workload_estimate_usage.return_value = {
            'items': [{'id': 'usage-1'}],
            'errors': [{'key': 'invalid', 'errorMessage': 'Invalid usage type'}],
        }
        mock_client.return_value = mock_bcm

        result = await batch_create_workload_estimate_usage(
            ctx=mock_context,
            workload_estimate_id='workload-123',
            usage=[
                {'key': 'web1', 'usageAccountId': '123456789012'},
                {'key': 'invalid', 'usageAccountId': '123456789012'},
            ],
        )

        assert result['status'] == 'success'
        assert result['created_count'] == 1
        assert result['error_count'] == 1
        assert len(result['errors']) == 1


@pytest.mark.asyncio
async def test_batch_delete_usage_with_errors(mock_context):
    """Test batch delete with partial errors."""
    with patch('bcm_pricing_calculator_mcp_server.server.create_bcm_client') as mock_client:
        mock_bcm = MagicMock()
        mock_bcm.batch_delete_workload_estimate_usage.return_value = {
            'errors': [{'id': 'usage-2', 'errorMessage': 'Not found'}],
        }
        mock_client.return_value = mock_bcm

        result = await batch_delete_workload_estimate_usage(
            ctx=mock_context,
            workload_estimate_id='workload-123',
            ids=['usage-1', 'usage-2', 'usage-3'],
        )

        assert result['status'] == 'success'
        assert result['deleted_count'] == 2
        assert result['error_count'] == 1


@pytest.mark.asyncio
async def test_update_workload_estimate_name_only(mock_context):
    """Test updating only the name."""
    with patch('bcm_pricing_calculator_mcp_server.server.create_bcm_client') as mock_client:
        mock_bcm = MagicMock()
        mock_bcm.update_workload_estimate.return_value = {
            'id': 'workload-123',
            'name': 'New Name',
            'rateType': 'BEFORE_DISCOUNTS',
        }
        mock_client.return_value = mock_bcm

        result = await update_workload_estimate(
            ctx=mock_context,
            identifier='workload-123',
            name='New Name',
        )

        assert result['status'] == 'success'
        assert result['name'] == 'New Name'


@pytest.mark.asyncio
async def test_create_bill_estimate_api_error(mock_context):
    """Test bill estimate creation with API error."""
    with patch('bcm_pricing_calculator_mcp_server.server.create_bcm_client') as mock_client:
        mock_bcm = MagicMock()
        mock_bcm.create_bill_estimate.side_effect = Exception('Validation failed')
        mock_client.return_value = mock_bcm

        result = await create_bill_estimate(
            ctx=mock_context,
            name='Test Bill',
        )

        assert result['error_type'] == 'api_error'
        assert 'Validation failed' in result['message']
        mock_context.error.assert_called_once()


# ============================================================================
# CLIENT AND HELPER TESTS
# ============================================================================


def test_get_aws_account_id_success():
    """Test successful AWS account ID retrieval."""
    with patch('bcm_pricing_calculator_mcp_server.client.boto3.Session') as mock_session:
        mock_sts = MagicMock()
        mock_sts.get_caller_identity.return_value = {'Account': '123456789012'}
        mock_session.return_value.client.return_value = mock_sts

        account_id = get_aws_account_id()

        assert account_id == '123456789012'
        mock_sts.get_caller_identity.assert_called_once()


def test_get_aws_account_id_with_profile():
    """Test AWS account ID retrieval with specific profile."""
    with patch('bcm_pricing_calculator_mcp_server.client.boto3.Session') as mock_session:
        mock_sts = MagicMock()
        mock_sts.get_caller_identity.return_value = {'Account': '999999999999'}
        mock_session.return_value.client.return_value = mock_sts

        account_id = get_aws_account_id(profile='production')

        assert account_id == '999999999999'
        mock_session.assert_called_with(profile_name='production')


@pytest.mark.asyncio
async def test_get_aws_account_id_tool_success(mock_context):
    """Test successful AWS account ID retrieval via tool."""
    with patch('bcm_pricing_calculator_mcp_server.server.get_aws_account_id') as mock_get_id:
        mock_get_id.return_value = '123456789012'

        result = await get_aws_account_id_tool(ctx=mock_context)

        assert result['status'] == 'success'
        assert result['account_id'] == '123456789012'
        mock_get_id.assert_called_once()
        mock_context.info.assert_called_once()


@pytest.mark.asyncio
async def test_get_aws_account_id_tool_error(mock_context):
    """Test AWS account ID retrieval error."""
    with patch('bcm_pricing_calculator_mcp_server.server.get_aws_account_id') as mock_get_id:
        mock_get_id.side_effect = Exception('No credentials found')

        result = await get_aws_account_id_tool(ctx=mock_context)

        assert result['error_type'] == 'api_error'
        assert 'No credentials found' in result['message']
        mock_context.error.assert_called_once()
