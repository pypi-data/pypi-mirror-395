"""
LangGraph conformance tests.

These tests verify the checkpointer implements the ITaskStore contract.
Requires Postgres to be running.
"""

import os

import pytest

try:
    from datetime import datetime, timezone

    from universal_agent.graph.state import ExecutionStatus, GraphState
    from universal_agent_nexus.adapters.langgraph.checkpointer import (
        LangGraphCheckpointerBridge,
    )
except ImportError:
    LangGraphCheckpointerBridge = None  # type: ignore
    GraphState = None  # type: ignore
    ExecutionStatus = None  # type: ignore


def is_postgres_available():
    """Check if Postgres is available."""
    return os.environ.get("DATABASE_URL") is not None


@pytest.mark.asyncio
@pytest.mark.skipif(
    LangGraphCheckpointerBridge is None, reason="LangGraph dependencies not installed"
)
@pytest.mark.skipif(
    not is_postgres_available(),
    reason="Requires Postgres (DATABASE_URL not set). Run: docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=password postgres:16-alpine",
)
async def test_langgraph_checkpointer_save_retrieve():
    """Test checkpointer save/retrieve with real Postgres."""
    postgres_url = os.environ.get(
        "DATABASE_URL", "postgresql://postgres:password@localhost:5432/uaa_test"
    )
    store = LangGraphCheckpointerBridge(postgres_url)
    try:
        await store.initialize()
        state = GraphState(
            execution_id="test-checkpoint-001",
            graph_name="test-graph",
            graph_version="1.0",
            context={"test": "data"},
            status=ExecutionStatus.RUNNING,
            created_at=datetime.now(timezone.utc),
        )
        await store.save_task(state)
        retrieved = await store.get_task("test-checkpoint-001")
        assert retrieved is not None
        assert retrieved.execution_id == "test-checkpoint-001"
        assert retrieved.context["test"] == "data"
    finally:
        await store.close()
