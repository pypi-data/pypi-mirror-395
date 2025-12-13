output "table_name" {
  description = "Name of the DynamoDB table"
  value       = aws_dynamodb_table.task_store.name
}

output "table_arn" {
  description = "ARN of the DynamoDB table"
  value       = aws_dynamodb_table.task_store.arn
}

output "table_id" {
  description = "ID of the DynamoDB table"
  value       = aws_dynamodb_table.task_store.id
}

output "stream_arn" {
  description = "ARN of the DynamoDB stream (if enabled)"
  value       = var.enable_streams ? aws_dynamodb_table.task_store.stream_arn : null
}

