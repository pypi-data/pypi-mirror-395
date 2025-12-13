#!/bin/bash
set -euo pipefail

# Universal Agent Nexus - Compile Manifest and Deploy
# Usage: ./compile-and-deploy.sh [manifest_path] [environment]
# Example: ./compile-and-deploy.sh examples/hello_langgraph/manifest.yaml dev

MANIFEST_PATH=${1:-""}
ENVIRONMENT=${2:-dev}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
TF_DIR="${SCRIPT_DIR}/../environments/${ENVIRONMENT}"

if [ -z "${MANIFEST_PATH}" ]; then
    echo "Usage: $0 [manifest_path] [environment]"
    echo "Example: $0 examples/hello_langgraph/manifest.yaml dev"
    exit 1
fi

if [ ! -f "${PROJECT_ROOT}/${MANIFEST_PATH}" ]; then
    echo "Error: Manifest not found: ${MANIFEST_PATH}"
    exit 1
fi

echo "============================================"
echo "Universal Agent Nexus - Compile and Deploy"
echo "Manifest: ${MANIFEST_PATH}"
echo "Environment: ${ENVIRONMENT}"
echo "============================================"

# Compile manifest to ASL
echo "Compiling manifest to AWS Step Functions ASL..."
cd "${PROJECT_ROOT}"

python -m universal_agent_nexus.cli.compile \
    "${MANIFEST_PATH}" \
    --target aws \
    --output "${TF_DIR}/state_machine.json"

echo "✅ Compiled ASL saved to: ${TF_DIR}/state_machine.json"

# Deploy with Terraform
echo ""
echo "Deploying to AWS..."
"${SCRIPT_DIR}/deploy.sh" "${ENVIRONMENT}" apply

echo ""
echo "============================================"
echo "✅ Deployment Complete!"
echo "============================================"

# Show outputs
cd "${TF_DIR}"
echo ""
echo "State Machine ARN:"
terraform output -raw state_machine_arn

echo ""
echo ""
echo "To start an execution:"
terraform output -raw execution_command

