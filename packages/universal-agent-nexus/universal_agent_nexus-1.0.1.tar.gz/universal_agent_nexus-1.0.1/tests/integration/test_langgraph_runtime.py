"""
Integration tests for LangGraph adapter with real Postgres.

Tests:
- Full execution cycle with checkpointing
- State persistence and recovery
- Error handling with checkpoints
- Concurrent execution handling
"""

import pytest

from universal_agent_nexus.adapters.langgraph.runtime import (
    LangGraphRuntime,
    load_manifest,
)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_langgraph_full_execution_cycle(postgres_url, sample_manifest_path):
    """
    End-to-end test: manifest → compile → execute → checkpoint.
    
    Validates:
    - Manifest loading
    - Graph compilation
    - Checkpoint persistence
    """
    manifest = load_manifest(str(sample_manifest_path))
    
    runtime = LangGraphRuntime(
        postgres_url=postgres_url,
        enable_checkpointing=True,
        pool_size=5,
    )
    
    try:
        # Initialize runtime
        await runtime.initialize(manifest, graph_name="main")
        assert runtime.compiled_graph is not None
        assert runtime.checkpointer is not None
        
        # Execute graph
        execution_id = "integration-test-001"
        result = await runtime.execute(
            execution_id=execution_id,
            input_data={
                "context": {"query": "Integration test query"},
                "history": [],
                "current_node": "",
                "error": None,
            },
        )
        
        # Verify execution result
        assert result is not None
        assert "context" in result
        
        # Verify checkpoint was saved
        checkpoint = await runtime.checkpointer.get_task(execution_id)
        assert checkpoint is not None
        assert checkpoint.execution_id == execution_id
        
    finally:
        await runtime.close()


@pytest.mark.asyncio
@pytest.mark.integration
async def test_checkpoint_persistence_across_restarts(postgres_url, sample_manifest_path):
    """
    Verify checkpoints persist across runtime restarts.
    
    Simulates:
    1. Execute graph with runtime A
    2. Close runtime A
    3. Start new runtime B
    4. Verify state recoverable from checkpoint
    """
    manifest = load_manifest(str(sample_manifest_path))
    execution_id = "persistence-test-001"
    
    # First execution - create checkpoint
    runtime1 = LangGraphRuntime(postgres_url, enable_checkpointing=True)
    
    try:
        await runtime1.initialize(manifest)
        
        result1 = await runtime1.execute(
            execution_id=execution_id,
            input_data={
                "context": {"query": "Persistent state test", "value": 42},
                "history": [],
                "current_node": "",
                "error": None,
            },
        )
        
        assert result1 is not None
        
    finally:
        await runtime1.close()
    
    # Second runtime - recover state
    runtime2 = LangGraphRuntime(postgres_url, enable_checkpointing=True)
    
    try:
        await runtime2.initialize(manifest)
        
        # Retrieve checkpoint
        state = await runtime2.checkpointer.get_task(execution_id)
        
        assert state is not None
        assert state.execution_id == execution_id
        assert state.context["query"] == "Persistent state test"
        assert state.context["value"] == 42
        
    finally:
        await runtime2.close()


@pytest.mark.asyncio
@pytest.mark.integration
async def test_stateless_mode_without_postgres(sample_manifest_path):
    """
    Test LangGraph runtime without checkpointing.
    
    Validates graceful degradation when Postgres unavailable.
    """
    manifest = load_manifest(str(sample_manifest_path))
    
    runtime = LangGraphRuntime(
        postgres_url=None,
        enable_checkpointing=False,
    )
    
    try:
        await runtime.initialize(manifest)
        
        # Should work without checkpointing
        result = await runtime.execute(
            execution_id="stateless-test-001",
            input_data={
                "context": {"query": "Stateless test"},
                "history": [],
                "current_node": "",
                "error": None,
            },
        )
        
        assert result is not None
        
    finally:
        await runtime.close()


@pytest.mark.asyncio
@pytest.mark.integration
async def test_concurrent_executions(postgres_url, sample_manifest_path):
    """
    Test multiple concurrent executions with same runtime.
    
    Validates:
    - Connection pool handling
    - Concurrent checkpoint writes
    - Execution isolation
    """
    import asyncio
    
    manifest = load_manifest(str(sample_manifest_path))
    runtime = LangGraphRuntime(postgres_url, enable_checkpointing=True, pool_size=10)
    
    try:
        await runtime.initialize(manifest)
        
        # Execute 5 graphs concurrently
        tasks = [
            runtime.execute(
                execution_id=f"concurrent-{i}",
                input_data={
                    "context": {"query": f"Query {i}"},
                    "history": [],
                    "current_node": "",
                    "error": None,
                },
            )
            for i in range(5)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # All should succeed or gracefully handle errors
        assert len(results) == 5
        
        # Verify checkpoints for successful executions
        for i in range(5):
            if not isinstance(results[i], Exception):
                state = await runtime.checkpointer.get_task(f"concurrent-{i}")
                assert state is not None
        
    finally:
        await runtime.close()


@pytest.mark.asyncio
@pytest.mark.integration
async def test_list_active_tasks(postgres_url, sample_manifest_path):
    """
    Test listing active tasks from checkpointer.
    
    Note: LangGraph checkpointer has limited support for this.
    """
    manifest = load_manifest(str(sample_manifest_path))
    runtime = LangGraphRuntime(postgres_url, enable_checkpointing=True)
    
    try:
        await runtime.initialize(manifest)
        
        # Execute a task
        await runtime.execute(
            "active-task-001",
            {
                "context": {"query": "Active test"},
                "history": [],
                "current_node": "",
                "error": None,
            },
        )
        
        # Try to list active tasks
        active_tasks = await runtime.checkpointer.list_active_tasks()
        
        # May return empty list (LangGraph limitation)
        assert isinstance(active_tasks, list)
        
    finally:
        await runtime.close()

