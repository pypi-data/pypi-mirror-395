"""
UAA Tool Processor Lambda Function

Executes MCP tools and returns results for Step Functions integration.

Environment Variables:
- DYNAMODB_TABLE_NAME: Task store table
- LOG_LEVEL: Logging level (default: INFO)
"""

import json
import logging
import os
from typing import Any, Dict

import boto3
from botocore.exceptions import ClientError

# Setup logging
log_level = os.environ.get("LOG_LEVEL", "INFO")
logger = logging.getLogger()
logger.setLevel(getattr(logging, log_level))

# AWS clients
dynamodb = boto3.resource("dynamodb")
table_name = os.environ.get("DYNAMODB_TABLE_NAME")
table = dynamodb.Table(table_name) if table_name else None


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Main Lambda handler for tool execution.

    Expected event structure:
    {
        "tool_name": "calculator",
        "tool_input": {"operation": "add", "a": 5, "b": 3},
        "execution_id": "exec-001",
        "context": {}
    }

    Returns:
    {
        "tool_result": {...},
        "success": true,
        "error": null
    }
    """
    logger.info(f"Processing tool execution: {json.dumps(event, default=str)}")

    try:
        # Extract parameters
        tool_name = event.get("tool_name")
        tool_input = event.get("tool_input", {})
        execution_id = event.get("execution_id")

        if not tool_name:
            return error_response("Missing required field: tool_name")

        # Route to appropriate tool handler
        if tool_name == "calculator":
            result = handle_calculator(tool_input)
        elif tool_name == "data_processor":
            result = handle_data_processor(tool_input)
        elif tool_name == "valuation_engine":
            result = handle_valuation(tool_input)
        elif tool_name == "echo":
            result = handle_echo(tool_input)
        else:
            return error_response(f"Unknown tool: {tool_name}")

        # Save state to DynamoDB (optional)
        if table and execution_id:
            save_tool_result(execution_id, tool_name, result)

        return success_response(result)

    except Exception as e:
        logger.exception("Tool execution failed")
        return error_response(str(e))


def handle_calculator(tool_input: Dict[str, Any]) -> Dict[str, Any]:
    """Calculator tool for basic math operations."""
    operation = tool_input.get("operation")
    a = tool_input.get("a", 0)
    b = tool_input.get("b", 0)

    operations = {
        "add": lambda x, y: x + y,
        "subtract": lambda x, y: x - y,
        "multiply": lambda x, y: x * y,
        "divide": lambda x, y: x / y if y != 0 else None,
    }

    if operation not in operations:
        raise ValueError(f"Unknown operation: {operation}")

    result = operations[operation](a, b)

    return {"operation": operation, "inputs": {"a": a, "b": b}, "result": result}


def handle_data_processor(tool_input: Dict[str, Any]) -> Dict[str, Any]:
    """Data processing tool for aggregation operations."""
    data = tool_input.get("data", [])
    operation = tool_input.get("operation", "sum")

    if operation == "sum":
        result = sum(data)
    elif operation == "average":
        result = sum(data) / len(data) if data else 0
    elif operation == "max":
        result = max(data) if data else None
    elif operation == "min":
        result = min(data) if data else None
    elif operation == "count":
        result = len(data)
    else:
        raise ValueError(f"Unknown operation: {operation}")

    return {"operation": operation, "data_size": len(data), "result": result}


def handle_valuation(tool_input: Dict[str, Any]) -> Dict[str, Any]:
    """Valuation tool (placeholder for actual valuation logic)."""
    asset = tool_input.get("asset")
    valuation_date = tool_input.get("valuation_date")
    methodology = tool_input.get("methodology", "DCF")

    # Placeholder - replace with actual valuation logic
    result = {
        "asset": asset,
        "valuation_date": valuation_date,
        "methodology": methodology,
        "estimated_value": 1000000,  # Placeholder
        "confidence": 0.85,
        "status": "completed",
    }

    return result


def handle_echo(tool_input: Dict[str, Any]) -> Dict[str, Any]:
    """Echo tool for testing - returns input as output."""
    return {"echo": tool_input, "status": "success"}


def save_tool_result(
    execution_id: str, tool_name: str, result: Dict[str, Any]
) -> None:
    """Save tool execution result to DynamoDB."""
    from datetime import datetime, timezone

    try:
        table.put_item(
            Item={
                "execution_id": execution_id,
                "state_key": f"tool_result#{tool_name}#{datetime.now(timezone.utc).isoformat()}",
                "tool_name": tool_name,
                "result": result,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )
        logger.info(f"Saved tool result for {execution_id}/{tool_name}")
    except ClientError as e:
        logger.error(f"Failed to save tool result: {e}")


def success_response(result: Dict[str, Any]) -> Dict[str, Any]:
    """Format success response."""
    return {"tool_result": result, "success": True, "error": None}


def error_response(error_message: str) -> Dict[str, Any]:
    """Format error response."""
    return {"tool_result": None, "success": False, "error": error_message}

