"""
Integration test fixtures using Testcontainers.

Provides:
- Postgres container for LangGraph runtime tests
- AWS mock credentials for DynamoDB tests
- Sample manifests
"""

import asyncio
import os
import sys
from pathlib import Path

import pytest

# Windows async fix
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest.fixture(scope="session")
def postgres_container():
    """
    Session-scoped Postgres container for all integration tests.
    
    Uses testcontainers to spin up real Postgres instance.
    Automatically tears down after test session.
    """
    try:
        from testcontainers.postgres import PostgresContainer
    except ImportError:
        pytest.skip("testcontainers not installed")
    
    with PostgresContainer("postgres:16-alpine") as postgres:
        yield postgres


@pytest.fixture
def postgres_url(postgres_container):
    """Get Postgres connection URL for each test."""
    return postgres_container.get_connection_url()


@pytest.fixture
def aws_credentials():
    """
    Mock AWS credentials for moto tests.
    
    Required for DynamoDB integration tests using moto.
    """
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
    
    yield
    
    # Cleanup
    for key in ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", 
                "AWS_SECURITY_TOKEN", "AWS_SESSION_TOKEN"]:
        os.environ.pop(key, None)


@pytest.fixture
def sample_manifest_path():
    """Path to hello_langgraph example manifest."""
    base = Path(__file__).parent.parent.parent
    return base / "examples" / "hello_langgraph" / "manifest.yaml"


@pytest.fixture
def temp_manifest(tmp_path):
    """
    Create temporary manifest for testing.
    
    Returns function that creates manifests with custom content.
    """
    def _create(name: str, content: str):
        manifest_path = tmp_path / f"{name}.yaml"
        manifest_path.write_text(content)
        return str(manifest_path)
    
    return _create

