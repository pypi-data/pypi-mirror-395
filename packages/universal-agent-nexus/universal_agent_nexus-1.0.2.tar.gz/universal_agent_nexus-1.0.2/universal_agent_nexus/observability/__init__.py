"""
Observability for Universal Agent Nexus.

Provides structured logging and distributed tracing using OpenTelemetry.
"""

try:
    from .tracing import setup_tracing, get_tracer, trace_execution, instrument_adapter
    from .logging import setup_structured_logging, StructuredFormatter

    __all__ = [
        "setup_tracing",
        "get_tracer",
        "trace_execution",
        "instrument_adapter",
        "setup_structured_logging",
        "StructuredFormatter",
    ]
except ImportError:
    # Observability deps not installed
    __all__ = []

