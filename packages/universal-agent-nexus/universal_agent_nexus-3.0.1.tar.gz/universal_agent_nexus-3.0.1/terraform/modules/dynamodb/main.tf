terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# DynamoDB Table with Single-Table Design
resource "aws_dynamodb_table" "task_store" {
  name         = var.table_name
  billing_mode = var.billing_mode
  hash_key     = "execution_id"
  range_key    = "state_key"

  # Partition Key: execution_id (string)
  attribute {
    name = "execution_id"
    type = "S"
  }

  # Sort Key: state_key (string) - format: "checkpoint#timestamp"
  attribute {
    name = "state_key"
    type = "S"
  }

  # GSI attributes
  attribute {
    name = "graph_name"
    type = "S"
  }

  attribute {
    name = "status_timestamp"
    type = "S"
  }

  # Global Secondary Index for querying by graph and status
  global_secondary_index {
    name            = "status-index"
    hash_key        = "graph_name"
    range_key       = "status_timestamp"
    projection_type = "ALL"
  }

  # Time To Live for automatic cleanup (optional)
  dynamic "ttl" {
    for_each = var.enable_ttl ? [1] : []
    content {
      attribute_name = "expiration_time"
      enabled        = true
    }
  }

  # Point-in-time recovery (production best practice)
  point_in_time_recovery {
    enabled = var.enable_point_in_time_recovery
  }

  # Server-side encryption
  server_side_encryption {
    enabled     = true
    kms_key_arn = var.kms_key_arn
  }

  # Stream for change data capture (optional)
  dynamic "stream_specification" {
    for_each = var.enable_streams ? [1] : []
    content {
      stream_enabled   = true
      stream_view_type = "NEW_AND_OLD_IMAGES"
    }
  }

  tags = merge(
    var.tags,
    {
      Name = var.table_name
    }
  )
}

# CloudWatch Alarms for DynamoDB
resource "aws_cloudwatch_metric_alarm" "read_throttle" {
  count = var.enable_alarms ? 1 : 0

  alarm_name          = "${var.table_name}-read-throttle"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "ReadThrottleEvents"
  namespace           = "AWS/DynamoDB"
  period              = "300"
  statistic           = "Sum"
  threshold           = "10"
  alarm_description   = "Alert when DynamoDB read operations are throttled"
  treat_missing_data  = "notBreaching"

  dimensions = {
    TableName = aws_dynamodb_table.task_store.name
  }

  alarm_actions = var.alarm_actions

  tags = var.tags
}

resource "aws_cloudwatch_metric_alarm" "write_throttle" {
  count = var.enable_alarms ? 1 : 0

  alarm_name          = "${var.table_name}-write-throttle"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "WriteThrottleEvents"
  namespace           = "AWS/DynamoDB"
  period              = "300"
  statistic           = "Sum"
  threshold           = "10"
  alarm_description   = "Alert when DynamoDB write operations are throttled"
  treat_missing_data  = "notBreaching"

  dimensions = {
    TableName = aws_dynamodb_table.task_store.name
  }

  alarm_actions = var.alarm_actions

  tags = var.tags
}

