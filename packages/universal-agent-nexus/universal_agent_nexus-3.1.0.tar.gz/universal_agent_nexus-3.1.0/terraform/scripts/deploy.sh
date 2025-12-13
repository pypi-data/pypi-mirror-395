#!/bin/bash
set -euo pipefail

# Universal Agent Nexus - Terraform Deployment Script
# Usage: ./deploy.sh [environment] [action]
# Example: ./deploy.sh dev apply

ENVIRONMENT=${1:-dev}
ACTION=${2:-plan}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
TF_DIR="${SCRIPT_DIR}/../environments/${ENVIRONMENT}"

echo "============================================"
echo "Universal Agent Nexus - Terraform Deployment"
echo "Environment: ${ENVIRONMENT}"
echo "Action: ${ACTION}"
echo "============================================"

# Check if environment exists
if [ ! -d "${TF_DIR}" ]; then
    echo "Error: Environment '${ENVIRONMENT}' not found"
    echo "Available environments:"
    ls -1 "${SCRIPT_DIR}/../environments/"
    exit 1
fi

# Navigate to environment directory
cd "${TF_DIR}"

# Initialize Terraform (if not already done)
if [ ! -d ".terraform" ]; then
    echo "Initializing Terraform..."
    terraform init
fi

# Format check
echo "Checking Terraform formatting..."
terraform fmt -check || {
    echo "Warning: Terraform files need formatting"
    echo "Run: terraform fmt -recursive"
}

# Validate configuration
echo "Validating Terraform configuration..."
terraform validate

# Execute action
case ${ACTION} in
    plan)
        echo "Running Terraform plan..."
        terraform plan
        ;;

    apply)
        echo "Running Terraform apply..."
        terraform plan -out=tfplan
        echo ""
        echo "Review the plan above. Press Enter to apply, Ctrl+C to cancel..."
        read -r
        terraform apply tfplan
        rm -f tfplan

        echo ""
        echo "============================================"
        echo "Deployment Complete!"
        echo "============================================"
        terraform output
        ;;

    destroy)
        echo "WARNING: This will destroy all resources!"
        echo "Press Enter to continue, Ctrl+C to cancel..."
        read -r
        terraform destroy
        ;;

    *)
        echo "Unknown action: ${ACTION}"
        echo "Valid actions: plan, apply, destroy"
        exit 1
        ;;
esac

