terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.4"
    }
  }
}

# Lambda Execution Role
resource "aws_iam_role" "lambda" {
  name               = "${var.function_name}-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume.json

  tags = merge(
    var.tags,
    {
      Name = "${var.function_name}-role"
    }
  )
}

data "aws_iam_policy_document" "lambda_assume" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

# Lambda Execution Policy
resource "aws_iam_role_policy" "lambda_execution" {
  name   = "${var.function_name}-execution"
  role   = aws_iam_role.lambda.id
  policy = data.aws_iam_policy_document.lambda_execution.json
}

data "aws_iam_policy_document" "lambda_execution" {
  # CloudWatch Logs
  statement {
    effect = "Allow"

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]

    resources = ["arn:aws:logs:*:*:*"]
  }

  # DynamoDB access (for task store)
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

  # X-Ray tracing
  statement {
    effect = "Allow"

    actions = [
      "xray:PutTraceSegments",
      "xray:PutTelemetryRecords",
    ]

    resources = ["*"]
  }

  # Secrets Manager (for API keys, credentials)
  dynamic "statement" {
    for_each = length(var.secrets_manager_arns) > 0 ? [1] : []

    content {
      effect = "Allow"

      actions = [
        "secretsmanager:GetSecretValue",
      ]

      resources = var.secrets_manager_arns
    }
  }

  # Step Functions (for invoking other graphs)
  dynamic "statement" {
    for_each = length(var.step_function_arns) > 0 ? [1] : []

    content {
      effect = "Allow"

      actions = [
        "states:StartExecution",
        "states:DescribeExecution",
      ]

      resources = var.step_function_arns
    }
  }
}

# Package Lambda code into ZIP
data "archive_file" "lambda" {
  type        = "zip"
  source_dir  = var.source_dir
  output_path = "${path.module}/.build/${var.function_name}.zip"

  excludes = var.exclude_files
}

# CloudWatch Log Group (create before Lambda)
resource "aws_cloudwatch_log_group" "lambda" {
  name              = "/aws/lambda/${var.function_name}"
  retention_in_days = var.log_retention_days

  tags = var.tags
}

# Lambda Function
resource "aws_lambda_function" "main" {
  filename         = data.archive_file.lambda.output_path
  function_name    = var.function_name
  role             = aws_iam_role.lambda.arn
  handler          = var.handler
  runtime          = var.runtime
  timeout          = var.timeout
  memory_size      = var.memory_size
  source_code_hash = data.archive_file.lambda.output_base64sha256

  # Environment variables
  environment {
    variables = merge(
      {
        DYNAMODB_TABLE_NAME     = var.dynamodb_table_name
        LOG_LEVEL               = var.log_level
        POWERTOOLS_SERVICE_NAME = var.function_name
      },
      var.environment_variables
    )
  }

  # VPC configuration (optional)
  dynamic "vpc_config" {
    for_each = var.vpc_config != null ? [var.vpc_config] : []

    content {
      subnet_ids         = vpc_config.value.subnet_ids
      security_group_ids = vpc_config.value.security_group_ids
    }
  }

  # Tracing
  tracing_config {
    mode = var.enable_xray_tracing ? "Active" : "PassThrough"
  }

  # Reserved concurrency (optional)
  reserved_concurrent_executions = var.reserved_concurrency

  # Dead letter queue (optional)
  dynamic "dead_letter_config" {
    for_each = var.dlq_arn != null ? [var.dlq_arn] : []

    content {
      target_arn = dead_letter_config.value
    }
  }

  # Lambda Layers (for shared dependencies)
  layers = var.lambda_layers

  tags = merge(
    var.tags,
    {
      Name = var.function_name
    }
  )

  depends_on = [
    aws_iam_role_policy.lambda_execution,
    aws_cloudwatch_log_group.lambda,
  ]
}

# Lambda Function URL (optional - for direct HTTP invocation)
resource "aws_lambda_function_url" "main" {
  count = var.enable_function_url ? 1 : 0

  function_name      = aws_lambda_function.main.function_name
  authorization_type = var.function_url_auth_type

  # CORS configuration
  dynamic "cors" {
    for_each = var.function_url_cors != null ? [var.function_url_cors] : []

    content {
      allow_origins     = cors.value.allow_origins
      allow_methods     = cors.value.allow_methods
      allow_headers     = cors.value.allow_headers
      expose_headers    = cors.value.expose_headers
      max_age           = cors.value.max_age
      allow_credentials = cors.value.allow_credentials
    }
  }
}

# CloudWatch Alarms
resource "aws_cloudwatch_metric_alarm" "errors" {
  count = var.enable_alarms ? 1 : 0

  alarm_name          = "${var.function_name}-errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = "300"
  statistic           = "Sum"
  threshold           = "5"
  alarm_description   = "Alert when Lambda function has errors"
  treat_missing_data  = "notBreaching"

  dimensions = {
    FunctionName = aws_lambda_function.main.function_name
  }

  alarm_actions = var.alarm_actions

  tags = var.tags
}

resource "aws_cloudwatch_metric_alarm" "throttles" {
  count = var.enable_alarms ? 1 : 0

  alarm_name          = "${var.function_name}-throttles"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "Throttles"
  namespace           = "AWS/Lambda"
  period              = "300"
  statistic           = "Sum"
  threshold           = "5"
  alarm_description   = "Alert when Lambda function is throttled"
  treat_missing_data  = "notBreaching"

  dimensions = {
    FunctionName = aws_lambda_function.main.function_name
  }

  alarm_actions = var.alarm_actions

  tags = var.tags
}

resource "aws_cloudwatch_metric_alarm" "duration" {
  count = var.enable_alarms ? 1 : 0

  alarm_name          = "${var.function_name}-duration"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "Duration"
  namespace           = "AWS/Lambda"
  period              = "300"
  statistic           = "Average"
  threshold           = var.timeout * 1000 * 0.8 # 80% of timeout
  alarm_description   = "Alert when Lambda function approaches timeout"
  treat_missing_data  = "notBreaching"

  dimensions = {
    FunctionName = aws_lambda_function.main.function_name
  }

  alarm_actions = var.alarm_actions

  tags = var.tags
}

