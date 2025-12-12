# Copyright (c) 2025 oreokebu-dev
# SPDX-License-Identifier: MIT

"""Constants for BCM Pricing Calculator MCP Server."""

import os

# Server configuration
MCP_SERVER_NAME = 'bcm-pricing-calculator-mcp-server'

# AWS Configuration
AWS_PROFILE = os.getenv('AWS_PROFILE', 'default')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')

# BCM Pricing Calculator endpoint (only available in us-east-1)
BCM_ENDPOINT = 'https://bcm-pricing-calculator.us-east-1.api.aws'

# Logging
LOG_LEVEL = os.getenv('FASTMCP_LOG_LEVEL', 'INFO')

# Pricing Discovery Limits
MAX_ATTRIBUTE_VALUES = 200  # Maximum attribute values to return (prevents context overflow)

# Service Examples - Quick reference for common patterns
# Format: serviceCode -> (example_usageType, example_operation, notes)
SERVICE_EXAMPLES = {
    'AmazonEC2': (
        'BoxUsage:t3.medium',
        'RunInstances',
        'Instance types vary, operation often needed',
    ),
    'AmazonRDS': (
        'InstanceUsage:db.t3.large',
        'CreateDBInstance:0002',
        'Operation indicates deployment type',
    ),
    'AmazonEKS': (
        'USE1-AmazonEKS-Hours:perCluster',
        'CreateOperation',
        'Region-prefixed usageType',
    ),
    'AmazonS3': ('TimedStorage-ByteHrs', '', 'Empty operation works for storage'),
    'AmazonDynamoDB': (
        'TimedStorage-ByteHrs',
        'PayPerRequestThroughput',
        'Multiple operation types',
    ),
    'AmazonElastiCache': (
        'NodeUsage:cache.r6gd.12xlarge',
        'CreateCacheCluster:0002',
        'Node type in usageType',
    ),
    'AmazonRoute53': ('HostedZone', '', 'No operation attribute - use empty string'),
    'AmazonCloudFront': ('DataTransfer-Out-Bytes', 'CloudFront', 'Simple operation value'),
    'AmazonSNS': ('Requests-Tier1', '', 'Empty operation works'),
    'AWSQueueService': ('Requests-RBP', '', 'Note: SQS is AWSQueueService, not AmazonSQS'),
    'AmazonSES': ('Recipients', 'Send', 'Requires specific operation'),
    'AmazonCloudWatch': ('CW:MetricMonitorUsage', '', 'Metrics use empty operation'),
    'AWSLambda': ('Request', 'Invoke', 'Simple request-based pricing'),
    'AWSGlue': ('USE2-Crawler-DPU-Hour', '', 'Region-prefixed, DPU-based'),
}

# Common AWS Service Codes (for quick reference without API calls)
COMMON_SERVICE_CODES = [
    'AmazonEC2',
    'AmazonS3',
    'AmazonRDS',
    'AWSLambda',
    'AmazonDynamoDB',
    'AmazonEKS',
    'AmazonECS',
    'AmazonCloudFront',
    'AmazonRoute53',
    'AmazonVPC',
    'AWSGlue',
    'AmazonElastiCache',
    'AmazonSNS',
    'AWSQueueService',
    'AmazonSES',
    'AmazonCloudWatch',
    'AmazonBedrock',
    'AmazonOpenSearch',
    'AmazonRedshift',
    'AmazonKinesis',
    'AmazonSageMaker',
    'AmazonAthena',
    'AmazonEMR',
    'AWSDataTransfer',
    'AmazonGuardDuty',
    'AWSSecurityHub',
    'AWSWAF',
    'AmazonAPIGateway',
    'AWSAppSync',
    'AmazonCognito',
]
