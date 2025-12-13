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
      --input '{"context": {"query": "Hello UAA!"}, "execution_id": "prod-001"}'
  EOT
}

