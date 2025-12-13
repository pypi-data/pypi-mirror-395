"""
Batch Accumulator for Anthropic Batch API integration.

Accumulates LLM requests and submits them in batches for cost optimization.
Integrates with prompt caching for additional savings.

Usage:
    accumulator = BatchAccumulator(api_key=os.environ["ANTHROPIC_API_KEY"])
    
    # Queue requests
    future1 = await accumulator.queue_request(request1, batch_group="claude:abc123")
    future2 = await accumulator.queue_request(request2, batch_group="claude:abc123")
    
    # Flush when ready (or auto-flush on timeout/size)
    await accumulator.flush()
    
    # Get results
    result1 = await future1
    result2 = await future2
"""

import asyncio
import hashlib
import logging
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple
from enum import Enum

logger = logging.getLogger(__name__)


class BatchStatus(str, Enum):
    """Status of a batch request."""
    PENDING = "pending"
    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class BatchRequest:
    """A single request to be batched."""
    
    id: str
    messages: List[Dict[str, Any]]
    model: str = "claude-sonnet-4-20250514"
    system: Optional[str] = None
    max_tokens: int = 1024
    cache_key: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Internal state
    created_at: float = field(default_factory=time.time)
    future: Optional[asyncio.Future] = None


@dataclass
class BatchGroup:
    """Group of requests to be submitted together."""
    
    group_key: str
    requests: List[BatchRequest] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    max_wait_ms: float = 5000.0
    max_size: int = 100
    
    @property
    def is_full(self) -> bool:
        """Check if batch is at capacity."""
        return len(self.requests) >= self.max_size
    
    @property
    def is_expired(self) -> bool:
        """Check if batch has waited too long."""
        elapsed_ms = (time.time() - self.created_at) * 1000
        return elapsed_ms >= self.max_wait_ms
    
    @property
    def should_flush(self) -> bool:
        """Check if batch should be flushed."""
        return self.is_full or self.is_expired


class BatchAccumulator:
    """
    Accumulates and batches LLM requests for Anthropic Batch API.
    
    Features:
    - Groups requests by model/system message for cache efficiency
    - Auto-flushes on size limit or timeout
    - Supports prompt caching via cache_control headers
    - Async-native with proper cleanup
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        max_batch_size: int = 100,
        max_wait_ms: float = 5000.0,
        auto_flush: bool = True,
        flush_interval_ms: float = 1000.0,
    ):
        """
        Initialize batch accumulator.
        
        Args:
            api_key: Anthropic API key (or use ANTHROPIC_API_KEY env var)
            max_batch_size: Maximum requests per batch
            max_wait_ms: Maximum wait time before flushing
            auto_flush: Whether to auto-flush on timer
            flush_interval_ms: How often to check for flush
        """
        self.api_key = api_key
        self.max_batch_size = max_batch_size
        self.max_wait_ms = max_wait_ms
        self.auto_flush = auto_flush
        self.flush_interval_ms = flush_interval_ms
        
        # State
        self._groups: Dict[str, BatchGroup] = {}
        self._lock = asyncio.Lock()
        self._flush_task: Optional[asyncio.Task] = None
        self._request_counter = 0
        self._client = None
        
        # Metrics
        self.stats = {
            "requests_queued": 0,
            "batches_submitted": 0,
            "requests_completed": 0,
            "cache_hits": 0,
            "total_tokens": 0,
            "total_cost_cents": 0.0,
        }
    
    async def start(self) -> None:
        """Start the accumulator (initializes client and auto-flush)."""
        # Initialize Anthropic client
        await self._init_client()
        
        # Start auto-flush task if enabled
        if self.auto_flush:
            self._flush_task = asyncio.create_task(self._auto_flush_loop())
            logger.info("BatchAccumulator started with auto-flush enabled")
    
    async def stop(self) -> None:
        """Stop the accumulator and flush remaining requests."""
        # Cancel auto-flush
        if self._flush_task:
            self._flush_task.cancel()
            try:
                await self._flush_task
            except asyncio.CancelledError:
                pass
        
        # Final flush
        await self.flush_all()
        logger.info("BatchAccumulator stopped")
    
    async def _init_client(self) -> None:
        """Initialize Anthropic client."""
        try:
            import anthropic
            
            self._client = anthropic.AsyncAnthropic(
                api_key=self.api_key,
            )
            logger.info("Anthropic client initialized")
        except ImportError:
            logger.warning("anthropic package not installed, batch API disabled")
            self._client = None
    
    async def queue_request(
        self,
        messages: List[Dict[str, Any]],
        *,
        model: str = "claude-sonnet-4-20250514",
        system: Optional[str] = None,
        max_tokens: int = 1024,
        batch_group: Optional[str] = None,
        cache_key: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> asyncio.Future:
        """
        Queue a request for batching.
        
        Args:
            messages: Chat messages
            model: Model to use
            system: System message
            max_tokens: Max response tokens
            batch_group: Group key for batching
            cache_key: Cache key for prompt caching
            metadata: Additional metadata
            
        Returns:
            Future that resolves to the response
        """
        async with self._lock:
            # Generate request ID
            self._request_counter += 1
            request_id = f"req_{self._request_counter:08d}"
            
            # Create future for result
            loop = asyncio.get_event_loop()
            future = loop.create_future()
            
            # Create request
            request = BatchRequest(
                id=request_id,
                messages=messages,
                model=model,
                system=system,
                max_tokens=max_tokens,
                cache_key=cache_key,
                metadata=metadata or {},
                future=future,
            )
            
            # Determine batch group
            group_key = batch_group or self._compute_group_key(request)
            
            # Get or create group
            if group_key not in self._groups:
                self._groups[group_key] = BatchGroup(
                    group_key=group_key,
                    max_wait_ms=self.max_wait_ms,
                    max_size=self.max_batch_size,
                )
            
            group = self._groups[group_key]
            group.requests.append(request)
            self.stats["requests_queued"] += 1
            
            logger.debug(
                f"Queued request {request_id} to group '{group_key}' "
                f"({len(group.requests)}/{group.max_size})"
            )
            
            # Check if we should flush immediately
            if group.should_flush:
                asyncio.create_task(self._flush_group(group_key))
        
        return future
    
    def _compute_group_key(self, request: BatchRequest) -> str:
        """Compute batch group key from request."""
        parts = [request.model]
        
        if request.system:
            sys_hash = hashlib.md5(request.system.encode()).hexdigest()[:8]
            parts.append(sys_hash)
        
        return ":".join(parts)
    
    async def _auto_flush_loop(self) -> None:
        """Background loop to auto-flush expired batches."""
        while True:
            try:
                await asyncio.sleep(self.flush_interval_ms / 1000)
                await self._check_and_flush()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.exception(f"Error in auto-flush loop: {e}")
    
    async def _check_and_flush(self) -> None:
        """Check for expired batches and flush them."""
        async with self._lock:
            expired_groups = [
                key for key, group in self._groups.items()
                if group.should_flush and group.requests
            ]
        
        for group_key in expired_groups:
            await self._flush_group(group_key)
    
    async def _flush_group(self, group_key: str) -> None:
        """Flush a specific batch group."""
        async with self._lock:
            if group_key not in self._groups:
                return
            
            group = self._groups.pop(group_key)
            
            if not group.requests:
                return
        
        logger.info(f"Flushing batch group '{group_key}' with {len(group.requests)} requests")
        
        try:
            await self._submit_batch(group)
            self.stats["batches_submitted"] += 1
        except Exception as e:
            logger.exception(f"Failed to submit batch: {e}")
            # Fail all futures in the batch
            for request in group.requests:
                if request.future and not request.future.done():
                    request.future.set_exception(e)
    
    async def _submit_batch(self, group: BatchGroup) -> None:
        """
        Submit batch to Anthropic Batch API.
        
        Uses prompt caching headers for shared system messages.
        """
        if not self._client:
            # Fallback: execute requests individually
            await self._submit_individual(group)
            return
        
        # Build batch requests with cache control
        batch_requests = []
        for request in group.requests:
            req_params = {
                "custom_id": request.id,
                "params": {
                    "model": request.model,
                    "max_tokens": request.max_tokens,
                    "messages": request.messages,
                },
            }
            
            # Add system message with cache control
            if request.system:
                req_params["params"]["system"] = [
                    {
                        "type": "text",
                        "text": request.system,
                        "cache_control": {"type": "ephemeral"},
                    }
                ]
            
            batch_requests.append(req_params)
        
        try:
            # Submit to Batch API
            batch = await self._client.messages.batches.create(
                requests=batch_requests
            )
            
            logger.info(f"Submitted batch {batch.id} with {len(batch_requests)} requests")
            
            # Poll for completion
            await self._poll_batch(batch.id, group)
            
        except Exception as e:
            logger.error(f"Batch API error: {e}")
            # Fallback to individual requests
            await self._submit_individual(group)
    
    async def _poll_batch(self, batch_id: str, group: BatchGroup) -> None:
        """Poll batch status and resolve futures."""
        # Map request IDs to futures
        futures_map = {req.id: req.future for req in group.requests}
        
        while True:
            batch = await self._client.messages.batches.retrieve(batch_id)
            
            if batch.processing_status == "ended":
                # Fetch results
                async for result in await self._client.messages.batches.results(batch_id):
                    req_id = result.custom_id
                    future = futures_map.get(req_id)
                    
                    if future and not future.done():
                        if result.result.type == "succeeded":
                            future.set_result(result.result.message)
                            self.stats["requests_completed"] += 1
                            
                            # Track cache hits from usage
                            usage = result.result.message.usage
                            if hasattr(usage, "cache_read_input_tokens"):
                                if usage.cache_read_input_tokens > 0:
                                    self.stats["cache_hits"] += 1
                        else:
                            future.set_exception(
                                Exception(f"Batch request failed: {result.result}")
                            )
                break
            
            # Wait before polling again
            await asyncio.sleep(1.0)
    
    async def _submit_individual(self, group: BatchGroup) -> None:
        """Fallback: submit requests individually."""
        logger.warning(f"Falling back to individual requests for group '{group.group_key}'")
        
        for request in group.requests:
            try:
                if self._client:
                    # Build params
                    params = {
                        "model": request.model,
                        "max_tokens": request.max_tokens,
                        "messages": request.messages,
                    }
                    if request.system:
                        params["system"] = request.system
                    
                    response = await self._client.messages.create(**params)
                    
                    if request.future and not request.future.done():
                        request.future.set_result(response)
                        self.stats["requests_completed"] += 1
                else:
                    # No client - return mock response
                    if request.future and not request.future.done():
                        request.future.set_result({
                            "content": [{"type": "text", "text": "[Batch API not available]"}],
                        })
            except Exception as e:
                if request.future and not request.future.done():
                    request.future.set_exception(e)
    
    async def flush_all(self) -> None:
        """Flush all pending batch groups."""
        async with self._lock:
            group_keys = list(self._groups.keys())
        
        for group_key in group_keys:
            await self._flush_group(group_key)
    
    async def flush(self) -> None:
        """Alias for flush_all."""
        await self.flush_all()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get accumulator statistics."""
        return {
            **self.stats,
            "pending_groups": len(self._groups),
            "pending_requests": sum(len(g.requests) for g in self._groups.values()),
        }

