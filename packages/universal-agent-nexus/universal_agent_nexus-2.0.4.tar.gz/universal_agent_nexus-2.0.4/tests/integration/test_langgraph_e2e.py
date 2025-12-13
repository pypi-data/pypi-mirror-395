"""
LangGraph E2E integration tests.

These tests require:
- Postgres running (docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=password postgres:16-alpine)
- DATABASE_URL environment variable set

Run with:
    DATABASE_URL=postgresql://postgres:password@localhost:5432/uaa_test pytest tests/integration/test_langgraph_e2e.py
"""

import os
from pathlib import Path

import pytest

try:
    from universal_agent_nexus.adapters.langgraph.runtime import (
        LangGraphRuntime,
        load_manifest,
    )
except ImportError:
    LangGraphRuntime = None  # type: ignore
    load_manifest = None  # type: ignore


def is_postgres_available():
    """Check if Postgres is available."""
    return os.environ.get("DATABASE_URL") is not None


@pytest.mark.asyncio
@pytest.mark.integration
@pytest.mark.skipif(
    LangGraphRuntime is None, reason="LangGraph runtime dependencies not installed"
)
@pytest.mark.skipif(
    not is_postgres_available(),
    reason="Requires Postgres (DATABASE_URL not set). Run: docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=password postgres:16-alpine",
)
async def test_hello_world_end_to_end():
    """Full E2E test with real Postgres and LLM."""
    postgres_url = os.environ.get(
        "DATABASE_URL", "postgresql://postgres:password@localhost:5432/uaa_test"
    )
    manifest_path = (
        Path(__file__).parent.parent / "../examples/hello_langgraph/manifest.yaml"
    ).resolve()
    manifest = load_manifest(str(manifest_path))

    runtime = LangGraphRuntime(postgres_url)
    try:
        await runtime.initialize(manifest)
        result = await runtime.execute(
            execution_id="e2e-test-001",
            input_data={
                "context": {"query": "What's 2+2?"},
                "history": [],
                "current_node": "",
                "error": None,
            },
        )
        assert result is not None
        assert result.get("error") is None
        task = await runtime.checkpointer.get_task("e2e-test-001")
        assert task is not None
        assert task.execution_id == "e2e-test-001"
    finally:
        await runtime.close()


def test_langgraph_e2e_placeholder():
    """Placeholder test to ensure file is picked up."""
    assert True
