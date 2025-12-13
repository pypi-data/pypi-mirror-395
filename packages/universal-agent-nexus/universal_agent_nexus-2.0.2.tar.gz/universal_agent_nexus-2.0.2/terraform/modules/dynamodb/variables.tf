variable "table_name" {
  description = "Name of the DynamoDB table"
  type        = string
}

variable "billing_mode" {
  description = "Billing mode: PROVISIONED or PAY_PER_REQUEST"
  type        = string
  default     = "PAY_PER_REQUEST"

  validation {
    condition     = contains(["PROVISIONED", "PAY_PER_REQUEST"], var.billing_mode)
    error_message = "billing_mode must be either PROVISIONED or PAY_PER_REQUEST"
  }
}

variable "read_capacity" {
  description = "Read capacity units (if PROVISIONED)"
  type        = number
  default     = 5
}

variable "write_capacity" {
  description = "Write capacity units (if PROVISIONED)"
  type        = number
  default     = 5
}

variable "gsi_read_capacity" {
  description = "GSI read capacity units (if PROVISIONED)"
  type        = number
  default     = 5
}

variable "gsi_write_capacity" {
  description = "GSI write capacity units (if PROVISIONED)"
  type        = number
  default     = 5
}

variable "enable_ttl" {
  description = "Enable Time To Live for automatic cleanup"
  type        = bool
  default     = false
}

variable "enable_point_in_time_recovery" {
  description = "Enable point-in-time recovery (backups)"
  type        = bool
  default     = true
}

variable "enable_streams" {
  description = "Enable DynamoDB Streams"
  type        = bool
  default     = false
}

variable "kms_key_arn" {
  description = "ARN of KMS key for encryption (default uses AWS managed key)"
  type        = string
  default     = null
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

