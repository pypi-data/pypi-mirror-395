#!/bin/bash
set -euo pipefail

# UAA Lambda Testing Script
# Usage: ./test-lambda.sh [environment]
# Example: ./test-lambda.sh dev

ENVIRONMENT=${1:-dev}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TF_DIR="${SCRIPT_DIR}/../environments/${ENVIRONMENT}"

cd "${TF_DIR}"

# Get Lambda function name
FUNCTION_NAME=$(terraform output -raw tool_processor_function_name 2>/dev/null || echo "")

if [ -z "${FUNCTION_NAME}" ]; then
    echo "Error: Lambda function not deployed. Run 'terraform apply' first."
    exit 1
fi

echo "============================================"
echo "Testing Lambda Function: ${FUNCTION_NAME}"
echo "============================================"

# Test 1: Calculator tool (add)
echo ""
echo "Test 1: Calculator (add)"
aws lambda invoke \
  --function-name "${FUNCTION_NAME}" \
  --payload '{"tool_name": "calculator", "tool_input": {"operation": "add", "a": 5, "b": 3}}' \
  --cli-binary-format raw-in-base64-out \
  response.json

echo "Response:"
cat response.json | python -m json.tool
rm -f response.json

# Test 2: Calculator tool (multiply)
echo ""
echo "Test 2: Calculator (multiply)"
aws lambda invoke \
  --function-name "${FUNCTION_NAME}" \
  --payload '{"tool_name": "calculator", "tool_input": {"operation": "multiply", "a": 7, "b": 6}}' \
  --cli-binary-format raw-in-base64-out \
  response.json

echo "Response:"
cat response.json | python -m json.tool
rm -f response.json

# Test 3: Data processor (average)
echo ""
echo "Test 3: Data Processor (average)"
aws lambda invoke \
  --function-name "${FUNCTION_NAME}" \
  --payload '{"tool_name": "data_processor", "tool_input": {"operation": "average", "data": [10, 20, 30, 40, 50]}}' \
  --cli-binary-format raw-in-base64-out \
  response.json

echo "Response:"
cat response.json | python -m json.tool
rm -f response.json

# Test 4: Echo tool
echo ""
echo "Test 4: Echo"
aws lambda invoke \
  --function-name "${FUNCTION_NAME}" \
  --payload '{"tool_name": "echo", "tool_input": {"message": "Hello from UAA!"}}' \
  --cli-binary-format raw-in-base64-out \
  response.json

echo "Response:"
cat response.json | python -m json.tool
rm -f response.json

# Test 5: Error handling (unknown tool)
echo ""
echo "Test 5: Error Handling (unknown tool)"
aws lambda invoke \
  --function-name "${FUNCTION_NAME}" \
  --payload '{"tool_name": "unknown_tool", "tool_input": {}}' \
  --cli-binary-format raw-in-base64-out \
  response.json

echo "Response:"
cat response.json | python -m json.tool
rm -f response.json

echo ""
echo "============================================"
echo "✅ All tests complete!"
echo "============================================"

