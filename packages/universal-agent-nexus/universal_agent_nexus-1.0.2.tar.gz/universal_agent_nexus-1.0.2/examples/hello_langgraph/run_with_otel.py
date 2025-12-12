import asyncio

from universal_agent_nexus.adapters.langgraph.runtime import (
    LangGraphRuntime,
    load_manifest,
)
from protocols.otel import setup_otel


async def main():
    tracer = setup_otel(
        service_name="hello-langgraph-example",
        endpoint="http://localhost:4317",
        insecure=True,
    )
    print("✅ OpenTelemetry initialized (traces -> localhost:4317)")

    manifest = load_manifest("manifest.yaml")
    runtime = LangGraphRuntime("postgresql://localhost/uaa_dev")

    with tracer.start_as_current_span("langgraph_execution"):
        await runtime.initialize(manifest)
        with tracer.start_as_current_span("graph_invoke"):
            result = await runtime.execute(
                execution_id="otel-test-001",
                input_data={
                    "context": {"query": "Hello with tracing!"},
                    "history": [],
                    "current_node": "",
                    "error": None,
                },
            )

        print(f"Result: {result.get('context', {}).get('last_response')}")
        print("✅ Execution traced - view in Jaeger at http://localhost:16686")

    await runtime.close()


if __name__ == "__main__":
    asyncio.run(main())

