terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# IAM Role for Step Functions execution
resource "aws_iam_role" "step_functions" {
  name               = "${var.name_prefix}-step-functions-role"
  assume_role_policy = data.aws_iam_policy_document.step_functions_assume.json

  tags = merge(
    var.tags,
    {
      Name = "${var.name_prefix}-step-functions-role"
    }
  )
}

data "aws_iam_policy_document" "step_functions_assume" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["states.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

# Policy for Step Functions to invoke Lambdas and access DynamoDB
resource "aws_iam_role_policy" "step_functions_execution" {
  name   = "${var.name_prefix}-step-functions-execution"
  role   = aws_iam_role.step_functions.id
  policy = data.aws_iam_policy_document.step_functions_execution.json
}

data "aws_iam_policy_document" "step_functions_execution" {
  # Lambda invocation permissions
  dynamic "statement" {
    for_each = length(var.lambda_arns) > 0 ? [1] : []
    content {
      effect = "Allow"

      actions = [
        "lambda:InvokeFunction",
      ]

      resources = var.lambda_arns
    }
  }

  # DynamoDB permissions for state persistence
  statement {
    effect = "Allow"

    actions = [
      "dynamodb:PutItem",
      "dynamodb:GetItem",
      "dynamodb:UpdateItem",
      "dynamodb:Query",
      "dynamodb:Scan",
    ]

    resources = [
      var.dynamodb_table_arn,
      "${var.dynamodb_table_arn}/index/*",
    ]
  }

  # CloudWatch Logs permissions
  statement {
    effect = "Allow"

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
      "logs:CreateLogDelivery",
      "logs:GetLogDelivery",
      "logs:UpdateLogDelivery",
      "logs:DeleteLogDelivery",
      "logs:ListLogDeliveries",
      "logs:PutResourcePolicy",
      "logs:DescribeResourcePolicies",
      "logs:DescribeLogGroups",
    ]

    resources = ["*"]
  }

  # X-Ray tracing
  statement {
    effect = "Allow"

    actions = [
      "xray:PutTraceSegments",
      "xray:PutTelemetryRecords",
    ]

    resources = ["*"]
  }
}

# CloudWatch Log Group for Step Functions
resource "aws_cloudwatch_log_group" "step_functions" {
  name              = "/aws/vendedlogs/states/${var.name_prefix}"
  retention_in_days = var.log_retention_days

  tags = var.tags
}

# Step Functions State Machine
resource "aws_sfn_state_machine" "main" {
  name       = "${var.name_prefix}-state-machine"
  role_arn   = aws_iam_role.step_functions.arn
  definition = var.state_machine_definition
  type       = var.state_machine_type

  logging_configuration {
    log_destination        = "${aws_cloudwatch_log_group.step_functions.arn}:*"
    include_execution_data = true
    level                  = var.log_level
  }

  tracing_configuration {
    enabled = var.enable_xray_tracing
  }

  tags = merge(
    var.tags,
    {
      Name = "${var.name_prefix}-state-machine"
    }
  )
}

# CloudWatch Alarms for monitoring
resource "aws_cloudwatch_metric_alarm" "execution_failed" {
  count = var.enable_alarms ? 1 : 0

  alarm_name          = "${var.name_prefix}-execution-failed"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "ExecutionsFailed"
  namespace           = "AWS/States"
  period              = "300"
  statistic           = "Sum"
  threshold           = "0"
  alarm_description   = "Alert when Step Functions execution fails"
  treat_missing_data  = "notBreaching"

  dimensions = {
    StateMachineArn = aws_sfn_state_machine.main.arn
  }

  alarm_actions = var.alarm_actions

  tags = var.tags
}

resource "aws_cloudwatch_metric_alarm" "execution_throttled" {
  count = var.enable_alarms ? 1 : 0

  alarm_name          = "${var.name_prefix}-execution-throttled"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "ExecutionThrottled"
  namespace           = "AWS/States"
  period              = "300"
  statistic           = "Sum"
  threshold           = "0"
  alarm_description   = "Alert when Step Functions executions are throttled"
  treat_missing_data  = "notBreaching"

  dimensions = {
    StateMachineArn = aws_sfn_state_machine.main.arn
  }

  alarm_actions = var.alarm_actions

  tags = var.tags
}

