# BCM Pricing Calculator MCP Server

MCP server for AWS Billing and Cost Management Pricing Calculator API - programmatically create cost estimates for planned cloud usage.

**Author**: oreokebu-dev  
**License**: MIT

## Features

### Cost Estimation & Planning

- **Workload Estimates**: Model usage patterns for specific workloads
- **Bill Scenarios**: Create different cost configuration scenarios
- **Bill Estimates**: Generate comprehensive cost projections
- **Line Item Analysis**: View detailed cost breakdowns
- **Commitment Modeling**: Include Savings Plans and Reserved Instances
- **Discount Integration**: Apply your organization's discounts and benefit sharing

### Query with Natural Language

- Ask questions about your cost estimates in plain English
- Create and compare multiple scenarios
- Get detailed cost breakdowns and projections

## Prerequisites

1. Install `uv` from [Astral](https://docs.astral.sh/uv/getting-started/installation/)
2. Install Python using `uv python install 3.10`
3. Set up AWS credentials with access to BCM Pricing Calculator
   - Configure AWS credentials with `aws configure` or environment variables
   - Ensure your IAM role/user has `bcm-pricing-calculator:*` permissions

## Installation

Add to your MCP client config (e.g., `~/.kiro/settings/mcp.json` for Kiro):

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

Restart your MCP client and you're ready to use it!

## Available Tools

### Workload Estimates
- `create_workload_estimate` - Create a new workload estimate
- `list_workload_estimates` - List all workload estimates
- `get_workload_estimate` - Get details of a specific workload estimate

### Bill Scenarios
- `create_bill_scenario` - Create a new bill scenario
- `list_bill_scenarios` - List all bill scenarios for an estimate

### Bill Estimates
- `create_bill_estimate` - Create a new bill estimate
- `list_bill_estimates` - List all bill estimates
- `get_bill_estimate` - Get details of a specific bill estimate
- `list_bill_estimate_line_items` - View detailed cost breakdown

### Preferences
- `get_preferences` - Get your pricing calculator preferences

## Example Usage

### Create a Cost Estimate

```
1. Create a bill estimate: "Create a bill estimate named 'Q1 2025 Migration'"
2. Create a scenario: "Create a bill scenario for the estimate"
3. Add usage modifications (via batch operations)
4. View results: "Show me the line items for this estimate"
```

### Compare Scenarios

```
1. Create multiple scenarios with different configurations
2. Generate estimates for each
3. Compare costs across scenarios
```

## AWS Authentication

The MCP server requires specific AWS permissions:

### Required Permissions
Your AWS IAM role or user must have `bcm-pricing-calculator:*` permissions to access the Pricing Calculator API.

### Configuration

**Environment Variables (optional):**
- `AWS_PROFILE` - AWS profile to use (defaults to "default")
- `AWS_REGION` - Must be "us-east-1" (only supported region)
- `FASTMCP_LOG_LEVEL` - Log level: ERROR, INFO, DEBUG (defaults to INFO)

The server uses your AWS credentials from `~/.aws/credentials` automatically.

## Important Notes

- BCM Pricing Calculator API is only available in `us-east-1` region
- All API calls are free of charge
- Estimates are based on your organization's pricing, discounts, and commitments
- This is different from the AWS Pricing API - it creates estimates rather than querying list prices

## Documentation

### Project Documentation
- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes with usage examples
- **[EXAMPLES.md](EXAMPLES.md)** - Detailed JSON examples and service patterns
- **[SERVICE_MAPPING_DISCOVERY.md](SERVICE_MAPPING_DISCOVERY.md)** - How to find correct serviceCode, usageType, and operation values

### AWS Documentation
- [AWS CLI Reference](https://docs.aws.amazon.com/cli/latest/reference/bcm-pricing-calculator/)
- [Service Authorization Reference](https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsbillingandcostmanagementpricingcalculator.html)
- [AWS Pricing Calculator UI](https://calculator.aws/) - Visual tool for discovering usageType/operation values

## Development

### Local Setup for Contributors

```bash
# Clone and install
git clone <repo-url>
cd bcm-pricing-calculator-mcp-server
uv pip install -e .

# Run tests
./test_local.sh
```

### Configure for Local Development

Use local path in your MCP config:

```json
{
  "mcpServers": {
    "bcm-pricing-calculator": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/bcm-pricing-calculator-mcp-server",
        "run",
        "bcm-pricing-calculator-mcp-server"
      ],
      "env": {
        "AWS_REGION": "us-east-1"
      }
    }
  }
}
```

### Testing

```bash
# Run all tests
./test_local.sh

# Run with coverage
uv run pytest --cov=bcm_pricing_calculator_mcp_server

# Run specific test
uv run pytest tests/test_server.py::test_create_workload_estimate_success
```

### Important Note

**Do NOT run the server directly** - MCP servers communicate via stdio protocol and expect JSON-RPC messages. Always test through an MCP client or use the test suite.

## License

MIT License - see LICENSE file for details
