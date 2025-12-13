import asyncio

from universal_agent_nexus.adapters.langgraph.runtime import (
    LangGraphRuntime,
    load_manifest,
)


async def main():
    manifest = load_manifest("manifest.yaml")
    runtime = LangGraphRuntime("postgresql://localhost/uaa_dev")
    await runtime.initialize(manifest)

    result = await runtime.execute(
        execution_id="mcp-test-001",
        input_data={
            "context": {"query": "List files in /tmp directory"},
            "history": [],
            "current_node": "",
            "error": None,
        },
    )

    print(f"Result: {result}")
    print(f"Last Response: {result.get('context', {}).get('last_response')}")
    print(f"Tool Result: {result.get('context', {}).get('tool_result')}")
    await runtime.close()


if __name__ == "__main__":
    asyncio.run(main())

