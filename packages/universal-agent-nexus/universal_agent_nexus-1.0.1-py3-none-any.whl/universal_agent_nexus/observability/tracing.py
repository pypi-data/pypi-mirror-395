"""
OpenTelemetry distributed tracing for UAA.

Provides automatic instrumentation across LangGraph, AWS, and MCP adapters.
"""

import logging
from contextlib import asynccontextmanager
from functools import wraps
from typing import Any, Callable, Dict, Optional

try:
    from opentelemetry import trace
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
except ImportError as exc:
    raise ImportError(
        "Install 'universal-agent-nexus[observability]' for tracing support"
    ) from exc

logger = logging.getLogger(__name__)

_tracer_provider: Optional[TracerProvider] = None


def setup_tracing(
    service_name: str = "universal-agent-nexus",
    otlp_endpoint: Optional[str] = None,
    environment: str = "production",
) -> trace.Tracer:
    """
    Initialize OpenTelemetry tracing.

    Args:
        service_name: Name of the service
        otlp_endpoint: OTLP collector endpoint (default: localhost:4317)
        environment: Deployment environment (dev, staging, production)

    Returns:
        Tracer instance for manual instrumentation
    """
    global _tracer_provider

    # Create resource with service metadata
    resource = Resource.create(
        {
            "service.name": service_name,
            "deployment.environment": environment,
        }
    )

    # Setup tracer provider
    _tracer_provider = TracerProvider(resource=resource)

    # Configure OTLP exporter
    if otlp_endpoint:
        exporter = OTLPSpanExporter(endpoint=otlp_endpoint)
    else:
        # Default to localhost (for local development)
        exporter = OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True)

    # Add batch span processor
    processor = BatchSpanProcessor(exporter)
    _tracer_provider.add_span_processor(processor)

    # Set global tracer provider
    trace.set_tracer_provider(_tracer_provider)

    logger.info(
        "OpenTelemetry tracing initialized: service=%s, env=%s",
        service_name,
        environment,
    )

    return trace.get_tracer(service_name)


def get_tracer(name: str = "universal-agent-nexus") -> trace.Tracer:
    """Get tracer instance for manual instrumentation."""
    return trace.get_tracer(name)


@asynccontextmanager
async def trace_execution(
    span_name: str,
    execution_id: Optional[str] = None,
    graph_name: Optional[str] = None,
    attributes: Optional[Dict[str, Any]] = None,
):
    """
    Context manager for tracing async execution.

    Usage:
        async with trace_execution("execute_graph", execution_id="exec-001"):
            result = await runtime.execute(...)

    Args:
        span_name: Name of the span
        execution_id: Execution identifier
        graph_name: Graph name
        attributes: Additional span attributes
    """
    tracer = get_tracer()

    with tracer.start_as_current_span(span_name) as span:
        # Set standard attributes
        if execution_id:
            span.set_attribute("execution.id", execution_id)
        if graph_name:
            span.set_attribute("graph.name", graph_name)

        # Set custom attributes
        if attributes:
            for key, value in attributes.items():
                span.set_attribute(key, str(value))

        try:
            yield span

        except Exception as e:
            # Record exception in span
            span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
            span.record_exception(e)
            raise


def instrument_adapter(adapter_name: str) -> Callable:
    """
    Decorator to automatically instrument adapter methods.

    Usage:
        @instrument_adapter("langgraph")
        async def execute(self, execution_id, input_data):
            ...
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            tracer = get_tracer()
            span_name = f"{adapter_name}.{func.__name__}"

            with tracer.start_as_current_span(span_name) as span:
                span.set_attribute("adapter", adapter_name)

                try:
                    result = await func(*args, **kwargs)
                    span.set_status(trace.Status(trace.StatusCode.OK))
                    return result

                except Exception as e:
                    span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
                    span.record_exception(e)
                    raise

        return wrapper

    return decorator

