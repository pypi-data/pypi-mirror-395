terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Environment = "prod"
      Project     = "universal-agent-nexus"
      ManagedBy   = "terraform"
    }
  }
}

# Data source for current AWS account
data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

locals {
  account_id = data.aws_caller_identity.current.account_id
  region     = data.aws_region.current.name

  tags = {
    Environment = "prod"
    Project     = "universal-agent-nexus"
    Owner       = var.owner
  }
}

# DynamoDB Task Store Module
module "dynamodb" {
  source = "../../modules/dynamodb"

  table_name                    = var.dynamodb_table_name
  billing_mode                  = "PAY_PER_REQUEST"
  enable_point_in_time_recovery = true
  enable_alarms                 = true
  alarm_actions                 = var.alarm_sns_topics

  tags = local.tags
}

# Step Functions State Machine Module
module "step_functions" {
  source = "../../modules/step_functions"

  name_prefix              = var.state_machine_name
  state_machine_definition = file("${path.module}/state_machine.json")
  state_machine_type       = "STANDARD"
  dynamodb_table_arn       = module.dynamodb.table_arn
  lambda_arns              = var.lambda_function_arns
  log_level                = "ERROR" # Less verbose for prod
  log_retention_days       = 30
  enable_xray_tracing      = true
  enable_alarms            = true
  alarm_actions            = var.alarm_sns_topics

  tags = local.tags

  depends_on = [module.dynamodb]
}

# SNS Topic for alarms
resource "aws_sns_topic" "alarms" {
  count = var.create_alarm_topic ? 1 : 0

  name = "${var.state_machine_name}-alarms"

  tags = local.tags
}

resource "aws_sns_topic_subscription" "alarms_email" {
  count = var.create_alarm_topic && var.alarm_email != "" ? 1 : 0

  topic_arn = aws_sns_topic.alarms[0].arn
  protocol  = "email"
  endpoint  = var.alarm_email
}

