variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
  default     = "us-east-1"
}

variable "dynamodb_table_name" {
  description = "Name of DynamoDB task store table"
  type        = string
  default     = "uaa-agent-state-prod"
}

variable "state_machine_name" {
  description = "Name prefix for Step Functions state machine"
  type        = string
  default     = "uaa-prod"
}

variable "lambda_function_arns" {
  description = "List of Lambda function ARNs for state machine"
  type        = list(string)
  default     = []
}

variable "alarm_sns_topics" {
  description = "SNS topic ARNs for CloudWatch alarms"
  type        = list(string)
  default     = []
}

variable "create_alarm_topic" {
  description = "Create SNS topic for alarms"
  type        = bool
  default     = true
}

variable "alarm_email" {
  description = "Email address for alarm notifications"
  type        = string
  default     = ""
}

variable "owner" {
  description = "Owner tag value"
  type        = string
  default     = "devops"
}

