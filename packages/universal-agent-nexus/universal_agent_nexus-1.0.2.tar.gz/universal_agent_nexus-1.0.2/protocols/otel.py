"""
OpenTelemetry setup helpers.

Provides minimal wiring for traces and FastAPI auto-instrumentation.
"""

from typing import Optional

try:
    from opentelemetry import trace
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
except ImportError as exc:  # pragma: no cover - optional dependency
    raise ImportError(
        "Install 'universal-agent-nexus[observability]' to enable OpenTelemetry."
    ) from exc


def setup_otel(
    service_name: str = "universal-agent-nexus",
    endpoint: str = "http://localhost:4317",
    insecure: bool = True,
) -> "trace.Tracer":
    """Initialize OpenTelemetry tracing with OTLP exporter."""
    resource = Resource.create({"service.name": service_name})
    provider = TracerProvider(resource=resource)

    processor = BatchSpanProcessor(
        OTLPSpanExporter(endpoint=endpoint, insecure=insecure)
    )
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    return trace.get_tracer(__name__)


def instrument_fastapi(app) -> object:
    """Auto-instrument a FastAPI application."""
    FastAPIInstrumentor.instrument_app(app)
    return app
