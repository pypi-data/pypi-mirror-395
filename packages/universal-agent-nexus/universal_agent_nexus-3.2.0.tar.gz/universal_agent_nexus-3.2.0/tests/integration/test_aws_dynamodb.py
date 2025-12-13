"""
Integration tests for AWS DynamoDB task store.

Note: These tests require LocalStack or actual AWS.
moto does not support aioboto3 async operations properly.

Run with LocalStack:
    docker run -d -p 4566:4566 localstack/localstack
    AWS_ENDPOINT_URL=http://localhost:4566 pytest tests/integration/test_aws_dynamodb.py
"""

import asyncio
import os
import sys
from datetime import datetime, timezone

import pytest

# Windows async fix
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from universal_agent.graph.state import ExecutionStatus, GraphState


# Check if LocalStack or AWS is available
def is_localstack_available():
    """Check if LocalStack is running."""
    return os.environ.get("AWS_ENDPOINT_URL") is not None


@pytest.mark.integration
@pytest.mark.skipif(
    not is_localstack_available(),
    reason="Requires LocalStack (AWS_ENDPOINT_URL not set). Run: docker run -d -p 4566:4566 localstack/localstack",
)
class TestDynamoDBTaskStore:
    """DynamoDB integration tests (require LocalStack)."""

    @pytest.fixture(autouse=True)
    def setup_credentials(self):
        """Set up AWS credentials for LocalStack."""
        os.environ.setdefault("AWS_ACCESS_KEY_ID", "testing")
        os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "testing")
        os.environ.setdefault("AWS_DEFAULT_REGION", "us-east-1")
        yield

    @pytest.mark.asyncio
    async def test_dynamodb_table_initialization(self):
        """Test DynamoDB table creation with GSI."""
        from universal_agent_nexus.adapters.aws.dynamodb_store import DynamoDBTaskStore

        store = DynamoDBTaskStore(table_name="test-uaa-init", region="us-east-1")
        try:
            await store.initialize()
            await store.initialize()  # Idempotent
        finally:
            await store.close()

    @pytest.mark.asyncio
    async def test_dynamodb_save_retrieve_cycle(self):
        """Test complete save/retrieve cycle."""
        from universal_agent_nexus.adapters.aws.dynamodb_store import DynamoDBTaskStore

        store = DynamoDBTaskStore(table_name="test-uaa-cycle", region="us-east-1")
        try:
            await store.initialize()

            state = GraphState(
                execution_id="dynamo-test-001",
                graph_name="test-graph",
                graph_version="1.0",
                context={
                    "query": "DynamoDB test",
                    "nested": {"value": 42, "float_val": 3.14159},
                    "boolean": True,
                },
                status=ExecutionStatus.RUNNING,
                created_at=datetime.now(timezone.utc),
            )

            await store.save_task(state)
            retrieved = await store.get_task("dynamo-test-001")

            assert retrieved is not None
            assert retrieved.execution_id == "dynamo-test-001"
            assert retrieved.status == ExecutionStatus.RUNNING
        finally:
            await store.close()

    @pytest.mark.asyncio
    async def test_dynamodb_nonexistent_task(self):
        """Test retrieving non-existent task returns None."""
        from universal_agent_nexus.adapters.aws.dynamodb_store import DynamoDBTaskStore

        store = DynamoDBTaskStore(table_name="test-uaa-notfound", region="us-east-1")
        try:
            await store.initialize()
            result = await store.get_task("nonexistent-id")
            assert result is None
        finally:
            await store.close()


# Unit tests that don't need AWS
class TestDynamoDBStoreUnit:
    """Unit tests for DynamoDB store (no AWS required)."""

    def test_dynamodb_store_import(self):
        """Verify DynamoDB store can be imported."""
        try:
            from universal_agent_nexus.adapters.aws.dynamodb_store import (
                DynamoDBTaskStore,
            )

            assert DynamoDBTaskStore is not None
        except ImportError:
            pytest.skip("aioboto3 not installed")

    def test_dynamodb_store_initialization(self):
        """Test store can be instantiated."""
        try:
            from universal_agent_nexus.adapters.aws.dynamodb_store import (
                DynamoDBTaskStore,
            )

            store = DynamoDBTaskStore(
                table_name="test-table",
                region="us-west-2",
            )
            assert store.table_name == "test-table"
            assert store.region == "us-west-2"
        except ImportError:
            pytest.skip("aioboto3 not installed")

    def test_serialize_context(self):
        """Test context serialization handles nested data."""
        try:
            from decimal import Decimal

            from universal_agent_nexus.adapters.aws.dynamodb_store import (
                DynamoDBTaskStore,
            )

            store = DynamoDBTaskStore(table_name="test", region="us-east-1")

            context = {
                "string": "value",
                "number": 42,
                "float": 3.14,
                "nested": {"key": "val"},
                "list": [1, 2, 3],
            }

            # _serialize_context returns dict with Decimal for floats
            serialized = store._serialize_context(context)
            assert isinstance(serialized, dict)
            assert serialized["string"] == "value"
            assert serialized["number"] == 42
            assert isinstance(serialized["float"], Decimal)

            # Can deserialize back to regular Python types
            deserialized = store._deserialize_context(serialized)
            assert deserialized["string"] == "value"
            assert deserialized["number"] == 42
            assert isinstance(deserialized["float"], float)
        except ImportError:
            pytest.skip("aioboto3 not installed")
