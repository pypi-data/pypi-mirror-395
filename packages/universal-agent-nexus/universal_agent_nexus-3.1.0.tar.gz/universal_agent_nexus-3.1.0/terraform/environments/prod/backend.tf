# Terraform remote state (S3 + DynamoDB locking)
# REQUIRED for production - uncomment and configure

# terraform {
#   backend "s3" {
#     bucket         = "your-terraform-state-bucket"
#     key            = "uaa/prod/terraform.tfstate"
#     region         = "us-east-1"
#     encrypt        = true
#     dynamodb_table = "terraform-state-lock"
#   }
# }

