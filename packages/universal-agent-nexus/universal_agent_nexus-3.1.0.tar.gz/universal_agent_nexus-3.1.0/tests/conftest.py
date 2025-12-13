"""
Pytest configuration and fixtures for Universal Agent Nexus tests.
"""

import asyncio
import sys
from pathlib import Path
from typing import Any, Dict

import pytest

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Windows async fix for psycopg
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest.fixture
def sample_manifest_dict() -> Dict[str, Any]:
    """Sample manifest as a dictionary for testing."""
    return {
        "name": "test-manifest",
        "version": "0.1.0",
        "description": "Test manifest for unit tests",
        "graphs": [
            {
                "name": "main",
                "version": "0.1.0",
                "description": "Test graph",
                "entry_node": "start",
                "nodes": [
                    {
                        "id": "start",
                        "kind": "router",
                        "label": "Start Router",
                        "router": {"name": "test-router"},
                    },
                    {
                        "id": "process",
                        "kind": "task",
                        "label": "Process Task",
                    },
                ],
                "edges": [
                    {
                        "from_node": "start",
                        "to_node": "process",
                        "condition": {"trigger": "success"},
                    },
                ],
            }
        ],
        "routers": [
            {
                "name": "test-router",
                "strategy": "llm",
                "model_candidates": ["gpt-4o-mini"],
                "default_model": "gpt-4o-mini",
                "system_message": "You are a test assistant.",
            }
        ],
        "tools": [],
    }


@pytest.fixture
def sample_manifest_path(tmp_path: Path, sample_manifest_dict: Dict[str, Any]) -> Path:
    """Create a temporary manifest file for testing."""
    import yaml

    manifest_path = tmp_path / "manifest.yaml"
    with open(manifest_path, "w") as f:
        yaml.dump(sample_manifest_dict, f)
    return manifest_path


@pytest.fixture
def mock_postgres_url() -> str:
    """Mock Postgres URL for testing (not a real connection)."""
    return "postgresql://test:test@localhost:5432/test_db"


@pytest.fixture
def mock_dynamodb_table() -> str:
    """Mock DynamoDB table name for testing."""
    return "test-uaa-agent-state"

