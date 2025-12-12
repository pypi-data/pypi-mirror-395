variable "function_name" {
  description = "Name of the Lambda function"
  type        = string
}

variable "source_dir" {
  description = "Directory containing Lambda code"
  type        = string
}

variable "handler" {
  description = "Lambda function handler (e.g., 'main.lambda_handler')"
  type        = string
  default     = "main.lambda_handler"
}

variable "runtime" {
  description = "Lambda runtime"
  type        = string
  default     = "python3.12"

  validation {
    condition     = can(regex("^python3\\.", var.runtime))
    error_message = "Runtime must be Python 3.x"
  }
}

variable "timeout" {
  description = "Function timeout in seconds"
  type        = number
  default     = 30

  validation {
    condition     = var.timeout >= 1 && var.timeout <= 900
    error_message = "Timeout must be between 1 and 900 seconds"
  }
}

variable "memory_size" {
  description = "Memory allocated to Lambda in MB"
  type        = number
  default     = 256

  validation {
    condition     = var.memory_size >= 128 && var.memory_size <= 10240
    error_message = "Memory must be between 128 and 10240 MB"
  }
}

variable "dynamodb_table_name" {
  description = "Name of DynamoDB table for state storage"
  type        = string
}

variable "dynamodb_table_arn" {
  description = "ARN of DynamoDB table for IAM permissions"
  type        = string
}

variable "log_level" {
  description = "Log level (DEBUG, INFO, WARNING, ERROR)"
  type        = string
  default     = "INFO"
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

variable "reserved_concurrency" {
  description = "Reserved concurrent executions (-1 for unreserved)"
  type        = number
  default     = -1
}

variable "lambda_layers" {
  description = "List of Lambda Layer ARNs"
  type        = list(string)
  default     = []
}

variable "environment_variables" {
  description = "Environment variables for Lambda"
  type        = map(string)
  default     = {}
  sensitive   = true
}

variable "vpc_config" {
  description = "VPC configuration for Lambda"
  type = object({
    subnet_ids         = list(string)
    security_group_ids = list(string)
  })
  default = null
}

variable "dlq_arn" {
  description = "Dead letter queue ARN"
  type        = string
  default     = null
}

variable "secrets_manager_arns" {
  description = "List of Secrets Manager ARNs Lambda can access"
  type        = list(string)
  default     = []
}

variable "step_function_arns" {
  description = "List of Step Function ARNs Lambda can invoke"
  type        = list(string)
  default     = []
}

variable "enable_function_url" {
  description = "Enable Lambda Function URL"
  type        = bool
  default     = false
}

variable "function_url_auth_type" {
  description = "Function URL authorization type (NONE or AWS_IAM)"
  type        = string
  default     = "AWS_IAM"

  validation {
    condition     = contains(["NONE", "AWS_IAM"], var.function_url_auth_type)
    error_message = "Auth type must be NONE or AWS_IAM"
  }
}

variable "function_url_cors" {
  description = "CORS configuration for Function URL"
  type = object({
    allow_origins     = list(string)
    allow_methods     = list(string)
    allow_headers     = list(string)
    expose_headers    = list(string)
    max_age           = number
    allow_credentials = bool
  })
  default = null
}

variable "exclude_files" {
  description = "Files to exclude from Lambda package"
  type        = list(string)
  default = [
    "*.pyc",
    "__pycache__",
    ".git",
    ".gitignore",
    "tests",
    "*.md",
  ]
}

variable "enable_alarms" {
  description = "Enable CloudWatch alarms"
  type        = bool
  default     = true
}

variable "alarm_actions" {
  description = "List of ARNs to notify on alarm"
  type        = list(string)
  default     = []
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default     = {}
}

