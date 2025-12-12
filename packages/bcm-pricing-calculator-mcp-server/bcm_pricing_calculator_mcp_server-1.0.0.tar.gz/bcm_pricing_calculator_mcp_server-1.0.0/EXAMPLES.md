# BCM Pricing Calculator - Complete Examples

## Example 1: Simple Web Application

### Step 1: Get AWS Account ID
```bash
aws sts get-caller-identity --query Account --output text
# Returns: 123456789012
```

### Step 2: Create Workload Estimate
```
"Create a workload estimate named Simple-Web-App"
```

Returns: `workload_estimate_id: "abc-123-def"`

### Step 3: Add Services
```
"Add these services to workload abc-123-def:
- 2 EC2 t3.medium instances for web servers
- 1 Application Load Balancer
- 100GB S3 storage"
```

Behind the scenes, this calls:
```json
{
  "workload_estimate_id": "abc-123-def",
  "usage": [
    {
      "serviceCode": "AmazonEC2",
      "usageType": "BoxUsage:t3.medium",
      "operation": "RunInstances",
      "key": "web1",
      "usageAccountId": "123456789012",
      "amount": 730,
      "group": "web"
    },
    {
      "serviceCode": "AmazonEC2",
      "usageType": "BoxUsage:t3.medium",
      "operation": "RunInstances",
      "key": "web2",
      "usageAccountId": "123456789012",
      "amount": 730,
      "group": "web"
    },
    {
      "serviceCode": "AWSELB",
      "usageType": "LoadBalancerUsage",
      "operation": "LoadBalancing",
      "key": "alb1",
      "usageAccountId": "123456789012",
      "amount": 730,
      "group": "web"
    },
    {
      "serviceCode": "AmazonS3",
      "usageType": "TimedStorage-ByteHrs",
      "operation": "StandardStorage",
      "key": "s3web",
      "usageAccountId": "123456789012",
      "amount": 100,
      "group": "storage"
    }
  ]
}
```

### Step 4: Get Total Cost
```
"What's the total cost for workload abc-123-def?"
```

Returns: `totalCost: $93.04/month`

---

## Example 2: Three-Tier Application (CORRECT WAY)

### ✅ Use ONE Workload Estimate with Groups

```
"Create a workload estimate named Production-App"
```

```
"Add these services to the workload:

Web Tier:
- 2 EC2 t3.medium web servers
- 1 Application Load Balancer
- CloudFront with 1TB data transfer
- 100GB S3 storage

Application Tier:
- 3 EC2 t3.large app servers

Database Tier:
- 1 RDS db.t3.large PostgreSQL instance
- 100GB RDS storage"
```

This creates ONE estimate with organized groups:
- `group: "web-tier"` - 4 services
- `group: "app-tier"` - 3 services
- `group: "db-tier"` - 2 services

**Total: $464.27/month in ONE estimate**

### ❌ WRONG WAY: Multiple Estimates

Don't do this:
```
"Create workload estimate Web-Tier"
"Create workload estimate App-Tier"
"Create workload estimate DB-Tier"
```

This requires 3 separate API calls to get costs and is harder to manage.

---

## Example 3: Common Service Patterns

### EC2 Instances (24/7)
```json
{
  "serviceCode": "AmazonEC2",
  "usageType": "BoxUsage:t3.medium",
  "operation": "RunInstances",
  "key": "web1",
  "usageAccountId": "123456789012",
  "amount": 730,
  "group": "compute"
}
```

### RDS Database
```json
{
  "serviceCode": "AmazonRDS",
  "usageType": "InstanceUsage:db.t3.large",
  "operation": "CreateDBInstance:0002",
  "key": "maindb",
  "usageAccountId": "123456789012",
  "amount": 730,
  "group": "database"
}
```

### RDS Storage
```json
{
  "serviceCode": "AmazonRDS",
  "usageType": "RDS:GP2-Storage",
  "operation": "CreateDBInstance:0002",
  "key": "dbstor",
  "usageAccountId": "123456789012",
  "amount": 100,
  "group": "database"
}
```

### Application Load Balancer
```json
{
  "serviceCode": "AWSELB",
  "usageType": "LoadBalancerUsage",
  "operation": "LoadBalancing",
  "key": "alb1",
  "usageAccountId": "123456789012",
  "amount": 730,
  "group": "networking"
}
```

### CloudFront CDN
```json
{
  "serviceCode": "AmazonCloudFront",
  "usageType": "DataTransfer-Out-Bytes",
  "operation": "CloudFront",
  "key": "cdn1",
  "usageAccountId": "123456789012",
  "amount": 1000,
  "group": "cdn"
}
```

### S3 Storage
```json
{
  "serviceCode": "AmazonS3",
  "usageType": "TimedStorage-ByteHrs",
  "operation": "StandardStorage",
  "key": "s3main",
  "usageAccountId": "123456789012",
  "amount": 100,
  "group": "storage"
}
```

---

## Example 4: Comparing Alternatives

When you DO want multiple workload estimates:

```
"Create workload estimate Option-A-MySQL"
"Create workload estimate Option-B-PostgreSQL"
```

Add different database configurations to each, then compare:

```
"Compare costs between Option-A-MySQL and Option-B-PostgreSQL"
```

---

## Common Errors and Solutions

### Error: "Validation error: Member must satisfy regular expression pattern"

**Problem**: Name has spaces or invalid characters
```
❌ "My Web App"
✅ "My-Web-App"
```

### Error: "Key must have length less than or equal to 10"

**Problem**: Key too long or has hyphens
```
❌ "web-server-1"
✅ "web1"
```

### Error: "No matching usage found"

**Problem**: Wrong usageType/operation combination
```
❌ usageType: "NodeUsage:cache.t3.medium", operation: "CreateCacheCluster"
✅ Check AWS Pricing API docs for correct combinations
```

### Error: "Missing required parameter: billScenarioId"

**Problem**: Trying to use Bill Estimates workflow
```
❌ create_bill_estimate(name="...")
✅ Use Workload Estimates instead (simpler)
```

---

## Quick Reference: Usage Amounts

- **EC2/RDS 24/7**: 730 hours/month
- **EC2/RDS 8hrs/day, 5 days/week**: ~173 hours/month
- **S3 Storage**: Amount in GB
- **Data Transfer**: Amount in GB
- **Load Balancer**: 730 hours/month (always on)

---

## Workflow Cheat Sheet

```
1. Get account ID
   → aws sts get-caller-identity

2. Create ONE workload estimate
   → create_workload_estimate(name="My-App")

3. Add ALL services with groups
   → batch_create_workload_estimate_usage(...)

4. Get total cost
   → get_workload_estimate(identifier="...")

5. View details (optional)
   → list_workload_estimate_usage(...)
```

---

## Pro Tips

1. **Always use groups** to organize services within one estimate
2. **Get account ID first** - you'll need it for every usage entry
3. **Use descriptive keys** - "web1", "db1", "cache1" (max 10 chars)
4. **730 hours = 24/7** - Most common amount for always-on services
5. **Check the docs** - usageType/operation must match AWS Pricing API exactly
6. **One estimate per project** - Not one per tier/service
