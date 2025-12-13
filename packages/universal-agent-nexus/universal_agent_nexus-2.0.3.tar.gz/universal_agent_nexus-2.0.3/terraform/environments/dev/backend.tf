# Terraform remote state (S3 + DynamoDB locking)
# Uncomment after creating S3 bucket and DynamoDB table

# terraform {
#   backend "s3" {
#     bucket         = "your-terraform-state-bucket"
#     key            = "uaa/dev/terraform.tfstate"
#     region         = "us-east-1"
#     encrypt        = true
#     dynamodb_table = "terraform-state-lock"
#   }
# }

