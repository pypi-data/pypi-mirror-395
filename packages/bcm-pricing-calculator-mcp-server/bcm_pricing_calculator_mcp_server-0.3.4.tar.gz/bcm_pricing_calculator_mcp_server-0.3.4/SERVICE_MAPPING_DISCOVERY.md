# AWS BCM Pricing Calculator - Service Mapping Discovery Guide

## Overview

This document explains how to discover the correct `serviceCode`, `usageType`, and `operation` values needed for the BCM Pricing Calculator API, based on research into AWS documentation and the relationship between the Price List API and BCM API.

## Key Finding: The Pricing Calculator UI Connection

**CRITICAL DISCOVERY**: The AWS Pricing Calculator UI at https://calculator.aws/ provides a "Condensed configuration" mode that shows the exact `usageType` and `operation` values you need!

From AWS Documentation:
> "You can use the condensed configuration if you are familiar with usage types and operations of products that you want to model usage for. Usage types are the units that each service uses to measure the usage of a specific type of resource. For example, the BoxUsage:t2.micro(Hrs) usage type filters by the running hours of Amazon EC2 t2.micro instances. Operation are requests made to a service and tasks performed by a service, such as write and get requests to Amazon S3.
>
> **Usage types and operation are available through the Price List API `GetProducts`. On Pricing Calculator console's Condensed configuration, you will be able to find the usage types and operations in their respective dropdown without needing to query Price List API.**"

Source: [Configure new services in my workload estimate](https://docs.aws.amazon.com/cost-management/latest/userguide/pc-create-workload-configure-service.html)

## Discovery Methods (In Order of Preference)

### Method 1: AWS Pricing Calculator UI (Easiest)

**Best for**: Quick discovery, visual exploration, seeing all options

1. Go to https://calculator.aws/
2. Create a new estimate
3. Add the service you want to price
4. Choose "Condensed configuration" mode
5. Browse the dropdowns for:
   - **Usage Type**: The exact usageType values
   - **Operation**: The exact operation values

**Advantages**:
- No API calls needed
- Visual interface shows all options
- Grouped by service for easy browsing
- Shows human-readable descriptions

**Limitations**:
- Manual process (not programmatic)
- Requires web browser access

### Method 2: Price List Query API (Programmatic)

**Best for**: Automation, filtering, integration into tools

The Price List Query API provides the same data that powers the Pricing Calculator UI.

#### Step 1: Find Service Codes

```bash
# List all services
aws pricing describe-services --region us-east-1

# Find specific service
aws pricing describe-services --region us-east-1 --service-code AmazonEC2
```

#### Step 2: Get Available Attributes

```bash
# See what attributes are available for filtering
aws pricing describe-services --region us-east-1 --service-code AmazonEC2
```

Returns attributes like: `usageType`, `operation`, `location`, `instanceType`, etc.

#### Step 3: Get Attribute Values

```bash
# Get all usageType values for a service
aws pricing get-attribute-values \
  --service-code AmazonEC2 \
  --attribute-name usageType \
  --region us-east-1

# Get all operation values
aws pricing get-attribute-values \
  --service-code AmazonEC2 \
  --attribute-name operation \
  --region us-east-1
```

**Pro Tip**: Use our MCP tools with filters to avoid context overflow:
```python
# Filter usageType values
get_pricing_attribute_values(
    service_code="AmazonEC2",
    attribute_name="usageType",
    filter="t3.medium"  # Regex filter
)
```

#### Step 4: Find Products (Optional)

```bash
# Get detailed product information
aws pricing get-products \
  --service-code AmazonEC2 \
  --region us-east-1 \
  --filters Type=TERM_MATCH,Field=usageType,Value="BoxUsage:t3.medium"
```

### Method 3: AWS Documentation

**Best for**: Understanding concepts, service-specific guidance

- [Price List Query API Guide](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/using-price-list-query-api.html)
- [BCM Pricing Calculator User Guide](https://docs.aws.amazon.com/cost-management/latest/userguide/pricing-calculator.html)
- Service-specific pricing pages (e.g., EC2 pricing, RDS pricing)

## Understanding the Field Hierarchy

**CRITICAL**: The fields have a hierarchy of importance:

```
serviceCode (required) → usageType (required) → operation (optional)
```

### serviceCode
- The AWS service identifier
- Examples: `AmazonEC2`, `AmazonRDS`, `AWSGlue`
- **Gotcha**: Some services have unexpected codes:
  - SQS is `AWSQueueService` (not `AmazonSQS`)
  - Check with `get_pricing_service_codes()` if unsure

### usageType
- **THE PRIMARY MATCHING KEY** for pricing
- Specifies the exact resource type and measurement unit
- Examples:
  - `BoxUsage:t3.medium` - EC2 instance hours
  - `InstanceUsage:db.t3.large` - RDS instance hours
  - `TimedStorage-ByteHrs` - S3 storage
  - `USE1-AmazonEKS-Hours:perCluster` - EKS cluster hours (region-prefixed)

**Common Patterns**:
- Instance types: `BoxUsage:INSTANCE_TYPE` or `InstanceUsage:INSTANCE_TYPE`
- Storage: `TimedStorage-ByteHrs`, `VolumeUsage`
- Data transfer: `DataTransfer-Out-Bytes`, `DataTransfer-In-Bytes`
- Requests: `Requests`, `Requests-Tier1`, `Recipients`
- Region-prefixed: `USE1-`, `USE2-`, `EU-`, `APN1-` (us-east-1, us-east-2, eu-west-1, ap-northeast-1)

### operation
- **OPTIONAL** - used for differentiation when multiple pricing tiers exist
- Many services work with `operation=""`
- Examples where specific operations matter:
  - EC2: `RunInstances` (vs `RunInstances:0002` for Reserved)
  - RDS: `CreateDBInstance:0002` (Single-AZ vs Multi-AZ)
  - SES: `Send` (required for email sending)
  - CloudWatch Logs: `PutLogEvents` (required for log ingestion)

## Recommended Discovery Workflow

### For Interactive/Manual Discovery:

1. **Start with Pricing Calculator UI**
   - Go to https://calculator.aws/
   - Add your service
   - Use "Condensed configuration"
   - Copy the exact usageType and operation values

2. **Verify with BCM API**
   - Create a test workload estimate
   - Add a single usage entry with the values from UI
   - Check if it calculates cost correctly

### For Programmatic/Automated Discovery:

1. **Get service code** (if unsure):
   ```python
   get_pricing_service_codes(filter="keyword")
   ```

2. **Discover usageType** (THE CRITICAL FIELD):
   ```python
   get_pricing_attribute_values(
       service_code="AmazonEC2",
       attribute_name="usagetype",
       filter="t3.medium"  # Use filter to narrow results!
   )
   ```

3. **Try operation="" first**:
   ```python
   batch_create_workload_estimate_usage(
       usage=[{
           "serviceCode": "AmazonEC2",
           "usageType": "BoxUsage:t3.medium",
           "operation": "",  # Try empty first!
           "key": "test1",
           "amount": 730,
           "usageAccountId": "123456789012"
       }]
   )
   ```

4. **Only if step 3 fails, discover specific operation**:
   ```python
   # Check if operation attribute exists
   get_pricing_service_attributes(service_code="AmazonEC2")
   
   # If it exists, get values
   get_pricing_attribute_values(
       service_code="AmazonEC2",
       attribute_name="operation",
       filter="RunInstances"
   )
   ```

## Common Gotchas and Solutions

### Gotcha 1: Service Code Mismatch
**Problem**: Using `AmazonSQS` when it should be `AWSQueueService`

**Solution**: Always verify with `get_pricing_service_codes(filter="sqs")`

### Gotcha 2: Region Prefixes
**Problem**: Using `AmazonEKS-Hours:perCluster` when it should be `USE1-AmazonEKS-Hours:perCluster`

**Solution**: Check if usageType values include region prefixes in the discovery results

### Gotcha 3: Operation Attribute Missing
**Problem**: Trying to discover operation values for Route53, but the attribute doesn't exist

**Solution**: Use `operation=""` - BCM API accepts empty strings for services without operations

### Gotcha 4: Too Many Results
**Problem**: `get_pricing_attribute_values` returns 500+ usageType values, overflowing context

**Solution**: Always use the `filter` parameter with regex patterns:
```python
get_pricing_attribute_values(
    service_code="AmazonEC2",
    attribute_name="usagetype",
    filter="t3\\.medium"  # Escape special regex chars
)
```

### Gotcha 5: Wrong Field Focus
**Problem**: Spending time discovering perfect operation when usageType is wrong

**Solution**: Focus on usageType first - it's the primary matching key. Operation is secondary.

## Examples by Service Category

### Compute Services
- **EC2**: `BoxUsage:t3.medium` + `RunInstances` or `""`
- **Lambda**: `Request` + `Invoke` or `""`
- **EKS**: `USE1-AmazonEKS-Hours:perCluster` + `CreateOperation` or `""`

### Database Services
- **RDS**: `InstanceUsage:db.t3.large` + `CreateDBInstance:0002`
- **DynamoDB**: `TimedStorage-ByteHrs` + `PayPerRequestThroughput` or `""`
- **ElastiCache**: `NodeUsage:cache.r6gd.12xlarge` + `CreateCacheCluster:0002`

### Storage Services
- **S3**: `TimedStorage-ByteHrs` + `""` (empty operation works)
- **EBS**: `VolumeUsage` + `""` or specific volume type

### Networking Services
- **CloudFront**: `DataTransfer-Out-Bytes` + `CloudFront`
- **Route53**: `HostedZone` + `""` (no operation attribute exists)

### Application Services
- **SQS**: `Requests-RBP` + `""` (service code is `AWSQueueService`)
- **SNS**: `Requests-Tier1` + `""`
- **SES**: `Recipients` + `Send` (operation required)

### Monitoring Services
- **CloudWatch Metrics**: `CW:MetricMonitorUsage` + `""`
- **CloudWatch Logs**: `USE1-VendedLog-Bytes` + `PutLogEvents` (operation required)

### Analytics Services
- **Glue**: `USE2-Crawler-DPU-Hour` + `""` (region-prefixed)

## Best Practices

1. **Start with the UI**: Use https://calculator.aws/ for quick discovery
2. **Use filters**: Always filter API results to avoid context overflow
3. **Try empty operation first**: Most services work with `operation=""`
4. **Focus on usageType**: It's the primary matching key
5. **Document your findings**: Add successful combinations to your reference map
6. **Test incrementally**: Add one service at a time to isolate issues
7. **Check region prefixes**: Some usageTypes include region codes
8. **Verify service codes**: Don't assume - check with discovery tools

## References

- [AWS Pricing Calculator](https://calculator.aws/)
- [BCM Pricing Calculator API Reference](https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_Operations_AWS_Billing_and_Cost_Management_Pricing_Calculator.html)
- [Price List Query API Guide](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/using-price-list-query-api.html)
- [Configure Services in Workload Estimate](https://docs.aws.amazon.com/cost-management/latest/userguide/pc-create-workload-configure-service.html)

