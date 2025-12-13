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
      Environment = "dev"
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
    Environment = "dev"
    Project     = "universal-agent-nexus"
    Owner       = var.owner
  }
}

# DynamoDB Task Store Module
module "dynamodb" {
  source = "../../modules/dynamodb"

  table_name                    = var.dynamodb_table_name
  billing_mode                  = "PAY_PER_REQUEST" # On-demand for dev
  enable_point_in_time_recovery = true
  enable_alarms                 = true
  alarm_actions                 = var.alarm_sns_topics

  tags = local.tags
}

# Tool Processor Lambda
module "tool_processor_lambda" {
  source = "../../modules/lambda"

  function_name       = "${var.state_machine_name}-tool-processor"
  source_dir          = "${path.module}/../../../lambda/tool_processor"
  handler             = "main.lambda_handler"
  runtime             = "python3.12"
  timeout             = 60
  memory_size         = 512
  dynamodb_table_name = module.dynamodb.table_name
  dynamodb_table_arn  = module.dynamodb.table_arn
  log_level           = "DEBUG" # Verbose for dev
  log_retention_days  = 7
  enable_xray_tracing = true
  enable_alarms       = true
  alarm_actions       = var.alarm_sns_topics

  # Enable Function URL for testing
  enable_function_url    = true
  function_url_auth_type = "NONE" # NONE only for dev/testing

  environment_variables = {
    ENVIRONMENT = "dev"
  }

  tags = local.tags

  depends_on = [module.dynamodb]
}

# Step Functions State Machine Module
module "step_functions" {
  source = "../../modules/step_functions"

  name_prefix              = var.state_machine_name
  state_machine_definition = file("${path.module}/state_machine.json")
  state_machine_type       = "STANDARD"
  dynamodb_table_arn       = module.dynamodb.table_arn
  lambda_arns              = [module.tool_processor_lambda.function_arn]
  log_level                = "ALL" # Verbose logging for dev
  log_retention_days       = 7
  enable_xray_tracing      = true
  enable_alarms            = true
  alarm_actions            = var.alarm_sns_topics

  tags = local.tags

  depends_on = [module.dynamodb, module.tool_processor_lambda]
}

# SNS Topic for alarms (optional)
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

