# Quick Start Guide

Get started with BCM Pricing Calculator MCP Server in 5 minutes.

## Prerequisites

1. **Install uv**: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. **AWS credentials**: Run `aws configure` with credentials that have `bcm-pricing-calculator:*` permissions
3. **MCP client**: Kiro, Claude Desktop, or any MCP-compatible client

## Installation

Add to your MCP config (e.g., `~/.kiro/settings/mcp.json`):

```json
{
  "mcpServers": {
    "bcm-pricing-calculator": {
      "command": "uvx",
      "args": ["bcm-pricing-calculator-mcp-server@latest"],
      "env": {
        "AWS_REGION": "us-east-1"
      }
    }
  }
}
```

Restart your MCP client and you're ready!

## Quick Usage Examples

### 1. Discover Service Pricing Information

```
"What are the valid service codes for Glue?"
"Show me EC2 t3.medium usage types"
"What operations are available for RDS?"
```

### 2. Create a Cost Estimate

```
"Create a workload estimate named Production-App"
```

Returns a workload estimate ID.

### 3. Add Services to Your Estimate

```
"Add 2 t3.medium EC2 instances running 24/7 to workload estimate <id>"
"Add an RDS db.t3.large database to workload estimate <id>"
```

### 4. View Total Cost

```
"Get the total cost for workload estimate <id>"
```

Returns the calculated monthly cost.

### 5. View Detailed Breakdown

```
"List all usage entries for workload estimate <id>"
```

## Complete Example Workflow

```
User: "Create a workload estimate named Web-Application"
→ Returns: workload_estimate_id: abc-123

User: "Get my AWS account ID"
→ Returns: 123456789012

User: "Add these services to workload abc-123:
      - 2 t3.medium EC2 instances (730 hours each)
      - 1 db.t3.large RDS instance (730 hours)
      - 100GB S3 storage"
→ Creates usage entries

User: "What's the total cost for workload abc-123?"
→ Returns: $250.45/month
```

## Key Concepts

- **Workload Estimate**: Container for modeling usage and costs
- **Usage Entry**: Specific service usage (EC2 instance, RDS database, etc.)
- **Service Code**: AWS service identifier (e.g., `AmazonEC2`, `AmazonRDS`)
- **Usage Type**: Specific resource type (e.g., `BoxUsage:t3.medium`)
- **Operation**: Operation name (e.g., `RunInstances`) - often can be empty `""`

## Discovery Tools

Use these to find correct values:

```
"Find service codes matching 'glue'"
→ Returns: AWSGlue

"Get usage types for AmazonEC2 matching 't3.medium'"
→ Returns: BoxUsage:t3.medium, etc.

"What operations are available for AmazonRDS?"
→ Returns: CreateDBInstance:0002, etc.
```

**Pro Tip**: Always use filters to avoid overwhelming results!

## Common Patterns

| Service | Usage Type Example | Operation |
|---------|-------------------|-----------|
| EC2 | `BoxUsage:t3.medium` | `RunInstances` or `""` |
| RDS | `InstanceUsage:db.t3.large` | `CreateDBInstance:0002` |
| S3 | `TimedStorage-ByteHrs` | `""` |
| Lambda | `Request` | `Invoke` or `""` |
| DynamoDB | `TimedStorage-ByteHrs` | `""` |

See [SERVICE_MAPPING_DISCOVERY.md](SERVICE_MAPPING_DISCOVERY.md) for comprehensive guide.

## Troubleshooting

### "Failed to create BCM client"
- Check: `aws sts get-caller-identity`
- Verify IAM permissions: `bcm-pricing-calculator:*`

### "Region not supported"
- BCM Pricing Calculator only works in `us-east-1`
- Set `AWS_REGION=us-east-1` in config

### "Invalid service code"
- Use discovery tools: `"Find service codes matching 'keyword'"`
- Check [EXAMPLES.md](EXAMPLES.md) for service patterns

### "No matching usage found"
- Wrong usageType/operation combination
- Try `operation=""` first (works for most services)
- Use discovery tools with filters

## Next Steps

- 📖 Read [SERVICE_MAPPING_DISCOVERY.md](SERVICE_MAPPING_DISCOVERY.md) - Learn how to find correct values and understand operation field behavior
- 📖 See [EXAMPLES.md](EXAMPLES.md) - Detailed JSON examples and service patterns

## Resources

- [AWS CLI Reference](https://docs.aws.amazon.com/cli/latest/reference/bcm-pricing-calculator/)
- [IAM Permissions](https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsbillingandcostmanagementpricingcalculator.html)
- [AWS Pricing Calculator UI](https://calculator.aws/) - Visual tool for discovering values

---

**Need help?** Check the documentation files or open an issue on GitHub.
