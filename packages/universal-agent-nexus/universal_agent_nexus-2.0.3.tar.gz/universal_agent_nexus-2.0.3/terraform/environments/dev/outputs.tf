output "dynamodb_table_name" {
  description = "Name of the DynamoDB table"
  value       = module.dynamodb.table_name
}

output "dynamodb_table_arn" {
  description = "ARN of the DynamoDB table"
  value       = module.dynamodb.table_arn
}

output "state_machine_arn" {
  description = "ARN of the Step Functions state machine"
  value       = module.step_functions.state_machine_arn
}

output "state_machine_name" {
  description = "Name of the Step Functions state machine"
  value       = module.step_functions.state_machine_name
}

output "execution_command" {
  description = "AWS CLI command to start execution"
  value       = <<-EOT
    aws stepfunctions start-execution \
      --state-machine-arn ${module.step_functions.state_machine_arn} \
      --input '{"context": {"query": "Hello UAA!"}, "execution_id": "test-001"}'
  EOT
}

output "tool_processor_function_name" {
  description = "Name of tool processor Lambda"
  value       = module.tool_processor_lambda.function_name
}

output "tool_processor_function_arn" {
  description = "ARN of tool processor Lambda"
  value       = module.tool_processor_lambda.function_arn
}

output "tool_processor_function_url" {
  description = "Function URL for direct testing"
  value       = module.tool_processor_lambda.function_url
}

output "test_lambda_command" {
  description = "AWS CLI command to test Lambda"
  value       = <<-EOT
    aws lambda invoke \
      --function-name ${module.tool_processor_lambda.function_name} \
      --payload '{"tool_name": "calculator", "tool_input": {"operation": "add", "a": 5, "b": 3}}' \
      --cli-binary-format raw-in-base64-out \
      response.json && cat response.json
  EOT
}

