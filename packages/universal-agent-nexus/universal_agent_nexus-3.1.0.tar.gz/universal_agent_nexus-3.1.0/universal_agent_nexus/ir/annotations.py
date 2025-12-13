"""
Typed annotation system for IR metadata.

Enables typed metadata access and transformation-aware annotations.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Type, TypeVar

T = TypeVar('T')


class Annotation(ABC):
    """
    Base class for custom IR annotations.

    Enables typed metadata access and transformation-aware annotations.
    """

    @classmethod
    @abstractmethod
    def key(cls) -> str:
        """
        Unique key for this annotation type.

        Returns:
            String key used to store/retrieve this annotation
        """
        pass


class CostAnnotation(Annotation):
    """Track estimated execution cost of nodes/edges."""

    @classmethod
    def key(cls) -> str:
        return "cost"

    def __init__(self, tokens: int, latency_ms: float, cost_cents: float):
        """
        Initialize cost annotation.

        Args:
            tokens: Estimated token count
            latency_ms: Estimated latency in milliseconds
            cost_cents: Estimated cost in cents
        """
        self.tokens = tokens
        self.latency_ms = latency_ms
        self.cost_cents = cost_cents

    def __repr__(self) -> str:
        return (
            f"CostAnnotation(tokens={self.tokens}, "
            f"latency_ms={self.latency_ms}, cost_cents={self.cost_cents})"
        )


class MonitoringAnnotation(Annotation):
    """Track monitoring/instrumentation needs."""

    @classmethod
    def key(cls) -> str:
        return "monitoring"

    def __init__(self, trace: bool = True, log_level: str = "INFO"):
        """
        Initialize monitoring annotation.

        Args:
            trace: Whether to enable tracing
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        """
        self.trace = trace
        self.log_level = log_level

    def __repr__(self) -> str:
        return f"MonitoringAnnotation(trace={self.trace}, log_level={self.log_level})"


class PerformanceAnnotation(Annotation):
    """Track performance characteristics."""

    @classmethod
    def key(cls) -> str:
        return "performance"

    def __init__(
        self,
        expected_duration_ms: Optional[float] = None,
        max_concurrency: Optional[int] = None,
        timeout_ms: Optional[float] = None,
    ):
        """
        Initialize performance annotation.

        Args:
            expected_duration_ms: Expected execution duration
            max_concurrency: Maximum concurrent executions
            timeout_ms: Timeout in milliseconds
        """
        self.expected_duration_ms = expected_duration_ms
        self.max_concurrency = max_concurrency
        self.timeout_ms = timeout_ms

    def __repr__(self) -> str:
        return (
            f"PerformanceAnnotation("
            f"expected_duration_ms={self.expected_duration_ms}, "
            f"max_concurrency={self.max_concurrency}, "
            f"timeout_ms={self.timeout_ms})"
        )


class BatchAnnotation(Annotation):
    """
    Mark nodes eligible for batch execution via Anthropic Batch API.

    Compile-time analysis annotates LLM call nodes with batching metadata.
    Runtime uses this to accumulate and batch requests for cost optimization.
    """

    @classmethod
    def key(cls) -> str:
        return "batch"

    def __init__(
        self,
        eligible: bool = True,
        batch_group: Optional[str] = None,
        cache_key: Optional[str] = None,
        priority: int = 0,
        max_wait_ms: float = 5000.0,
    ):
        """
        Initialize batch annotation.

        Args:
            eligible: Whether node is eligible for batching
            batch_group: Group ID for batching similar requests together
            cache_key: Cache key for prompt caching (based on system message hash)
            priority: Batch priority (higher = process sooner)
            max_wait_ms: Max time to wait for batch accumulation before flushing
        """
        self.eligible = eligible
        self.batch_group = batch_group
        self.cache_key = cache_key
        self.priority = priority
        self.max_wait_ms = max_wait_ms

    def __repr__(self) -> str:
        return (
            f"BatchAnnotation(eligible={self.eligible}, "
            f"batch_group={self.batch_group!r}, "
            f"cache_key={self.cache_key!r}, "
            f"priority={self.priority})"
        )

