# Universal Agent Nexus - Terraform Infrastructure

Deploy UAA graphs to AWS using Step Functions + DynamoDB with one command.

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                        AWS Cloud                              │
├──────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────┐                  │
│  │  Step Functions  │───▶│    DynamoDB     │                  │
│  │  State Machine   │    │   Task Store    │                  │
│  └────────┬────────┘    └─────────────────┘                  │
│           │                                                   │
│           ▼                                                   │
│  ┌─────────────────┐    ┌─────────────────┐                  │
│  │     Lambda      │    │   CloudWatch    │                  │
│  │  (Tool Exec)    │    │   Logs/Alarms   │                  │
│  └─────────────────┘    └─────────────────┘                  │
└──────────────────────────────────────────────────────────────┘
```

- **Step Functions**: Executes UAA graphs as state machines
- **DynamoDB**: Persists agent state with single-table design
- **CloudWatch**: Logging and monitoring
- **X-Ray**: Distributed tracing

## Prerequisites

1. **AWS CLI** configured with credentials
2. **Terraform** >= 1.6.0
3. **Python** 3.11+ with `universal-agent-nexus[aws]` installed

## Quick Start

### 1. Compile Manifest to ASL

```bash
# From project root
nexus compile examples/hello_langgraph/manifest.yaml --target aws \
  --output terraform/environments/dev/state_machine.json
```

### 2. Deploy Infrastructure

```bash
cd terraform/environments/dev
terraform init
terraform plan
terraform apply
```

### 3. Execute Graph

```bash
# Get state machine ARN
STATE_MACHINE_ARN=$(terraform output -raw state_machine_arn)

# Start execution
aws stepfunctions start-execution \
  --state-machine-arn $STATE_MACHINE_ARN \
  --input '{"context": {"query": "Hello AWS!"}, "execution_id": "test-001"}'
```

## Automated Deployment

Use the provided scripts for one-command deployment:

```bash
# Compile manifest + deploy
./scripts/compile-and-deploy.sh examples/hello_langgraph/manifest.yaml dev

# Deploy only (ASL already compiled)
./scripts/deploy.sh dev apply

# Destroy infrastructure
./scripts/deploy.sh dev destroy
```

## Module Structure

```
terraform/
├── modules/
│   ├── step_functions/    # State machine, IAM, CloudWatch
│   ├── dynamodb/          # Task store with GSI
│   └── lambda/            # Tool execution functions (future)
├── environments/
│   ├── dev/               # Development environment
│   └── prod/              # Production environment
└── scripts/
    ├── deploy.sh          # Terraform wrapper
    └── compile-and-deploy.sh
```

## Configuration

### Dev Environment

Edit `terraform/environments/dev/terraform.tfvars`:

```hcl
aws_region          = "us-east-1"
dynamodb_table_name = "uaa-agent-state-dev"
state_machine_name  = "uaa-dev"
alarm_email         = "your-email@example.com"
```

### Production Environment

Copy `dev/` to `prod/` and update variables:

```bash
cp -r environments/dev environments/prod
# Edit environments/prod/terraform.tfvars
```

## Remote State (Recommended for Teams)

### 1. Create S3 Bucket for State

```bash
aws s3 mb s3://your-terraform-state-bucket
aws s3api put-bucket-versioning \
  --bucket your-terraform-state-bucket \
  --versioning-configuration Status=Enabled
```

### 2. Create DynamoDB Table for Locking

```bash
aws dynamodb create-table \
  --table-name terraform-state-lock \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST
```

### 3. Uncomment Backend Configuration

Edit `environments/dev/backend.tf`:

```hcl
terraform {
  backend "s3" {
    bucket         = "your-terraform-state-bucket"
    key            = "uaa/dev/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}
```

## Monitoring

### CloudWatch Logs

```bash
# Tail Step Functions logs
aws logs tail /aws/vendedlogs/states/uaa-dev --follow
```

### X-Ray Traces

```bash
# View recent traces
aws xray get-trace-summaries \
  --start-time $(date -u -d '1 hour ago' +%s) \
  --end-time $(date -u +%s)
```

### Alarms

Alarms are automatically created for:
- Execution failures
- Execution throttling
- DynamoDB read/write throttling

## Cost Optimization

### Development
- Use `PAY_PER_REQUEST` billing (on-demand)
- Set log retention to 7 days
- Use `EXPRESS` state machines for high-throughput testing

### Production
- Consider `PROVISIONED` capacity for predictable workloads
- Increase log retention to 30+ days
- Use `STANDARD` state machines for durability

## Troubleshooting

### State Machine Execution Fails

```bash
# Get execution details
aws stepfunctions describe-execution --execution-arn [ARN]

# View CloudWatch logs
aws logs tail /aws/vendedlogs/states/uaa-dev --follow
```

### DynamoDB Throttling

```bash
# Check throttling metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/DynamoDB \
  --metric-name ReadThrottleEvents \
  --dimensions Name=TableName,Value=uaa-agent-state-dev \
  --start-time 2025-12-05T00:00:00Z \
  --end-time 2025-12-05T23:59:59Z \
  --period 3600 \
  --statistics Sum
```

## Resources Created

| Resource | Name | Purpose |
|----------|------|---------|
| DynamoDB Table | `uaa-agent-state-dev` | Task state persistence |
| Step Functions | `uaa-dev-state-machine` | Graph execution |
| IAM Role | `uaa-dev-step-functions-role` | Execution permissions |
| CloudWatch Log Group | `/aws/vendedlogs/states/uaa-dev` | Execution logs |
| CloudWatch Alarms | `uaa-dev-*` | Failure/throttle alerts |

