"""
Hello LangGraph example - production-ready with checkpoint persistence.
"""

import asyncio
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(name)s:%(message)s",
)

# Windows async fix for psycopg
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from universal_agent_nexus.adapters.langgraph.runtime import LangGraphRuntime, load_manifest


async def main():
    manifest = load_manifest("manifest.yaml")

    # Enable checkpointing (requires Postgres with autocommit=True pattern)
    runtime = LangGraphRuntime(
        postgres_url="postgresql://postgres:password@localhost:5432/uaa_dev",
        enable_checkpointing=True,
        pool_size=5,
    )

    try:
        await runtime.initialize(manifest)

        result = await runtime.execute(
            execution_id="hello-123",
            input_data={
                "context": {"query": "Hello! How are you?"},
                "history": [],
                "current_node": "",
                "error": None,
            },
        )

        print(f"\n[OK] Result: {result}")
        print(f"[RESPONSE] Last Response: {result.get('context', {}).get('last_response')}")

    finally:
        await runtime.close()


if __name__ == "__main__":
    asyncio.run(main())
