variable "name_prefix" {
  description = "Prefix for all resource names"
  type        = string
}

variable "state_machine_definition" {
  description = "ASL definition for the state machine (JSON string)"
  type        = string
}

variable "state_machine_type" {
  description = "Type of state machine: STANDARD or EXPRESS"
  type        = string
  default     = "STANDARD"

  validation {
    condition     = contains(["STANDARD", "EXPRESS"], var.state_machine_type)
    error_message = "state_machine_type must be either STANDARD or EXPRESS"
  }
}

variable "lambda_arns" {
  description = "List of Lambda function ARNs that can be invoked"
  type        = list(string)
  default     = []
}

variable "dynamodb_table_arn" {
  description = "ARN of DynamoDB table for state persistence"
  type        = string
}

variable "log_level" {
  description = "Log level: ALL, ERROR, FATAL, OFF"
  type        = string
  default     = "ERROR"
}

variable "log_retention_days" {
  description = "CloudWatch log retention in days"
  type        = number
  default     = 7
}

variable "enable_xray_tracing" {
  description = "Enable AWS X-Ray tracing"
  type        = bool
  default     = true
}

variable "enable_alarms" {
  description = "Enable CloudWatch alarms"
  type        = bool
  default     = true
}

variable "alarm_actions" {
  description = "List of ARNs to notify on alarm (SNS topics)"
  type        = list(string)
  default     = []
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default     = {}
}

