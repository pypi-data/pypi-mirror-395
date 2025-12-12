"""AWS Step Functions adapter for Universal Agent Architecture."""

from .step_functions import StepFunctionsCompiler

__all__ = ["StepFunctionsCompiler"]

# Runtime and DynamoDB require boto3 - import lazily
try:
    from .dynamodb_store import DynamoDBTaskStore
    from .runtime import StepFunctionsRuntime

    __all__.extend(["StepFunctionsRuntime", "DynamoDBTaskStore"])
except ImportError:
    pass  # boto3 not installed
