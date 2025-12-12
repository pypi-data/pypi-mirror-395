"""Core GraphBit Tracer implementation."""

import asyncio
import random
import uuid
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Dict, List, Optional

from bitpulse.schemas.types import (
    CostInfo,
    SearchQuery,
    SpanEvent,
    SpanId,
    SpanKind,
    SpanStatus,
    TraceId,
    TraceSpan,
    TraceStats,
)
from bitpulse.storage.base import StorageBackend, create_storage_backend
from bitpulse.utils.config import TracerConfig
from bitpulse.utils.ingestion import GraphBitDataIngester
from bitpulse.utils.logging_utils import setup_logging
from bitpulse.utils.metrics import MetricsCollector

from .llm_tracer import LLMTracer

# Pure data collection - no external monitoring tool dependencies


logger = setup_logging()


class TracerError(Exception):
    """Base exception for tracer errors."""

    pass


class GraphBitTracer:
    """Main GraphBit Tracer class for distributed tracing and observability."""

    def __init__(
        self,
        config: TracerConfig,
        storage: StorageBackend,
        metrics: MetricsCollector,
    ):
        """Initialize the tracer.

        Args:
            config: Tracer configuration
            storage: Storage backend
            metrics: Metrics collector
        """
        self._config = config
        self._storage = storage
        self._metrics = metrics
        self._active_spans: Dict[SpanId, TraceSpan] = {}
        self._background_tasks: List[asyncio.Task] = []
        self._shutdown = False

        # Initialize LLM tracer
        self._llm_tracer = LLMTracer(self)

        # Initialize data ingester
        self._ingester = GraphBitDataIngester(self)

        logger.info("GraphBit Tracer initialized", config=config.summary())

    @classmethod
    async def init(cls, config: TracerConfig) -> "GraphBitTracer":
        """Initialize a new tracer instance.

        Args:
            config: Tracer configuration

        Returns:
            Initialized GraphBitTracer instance

        Raises:
            TracerError: If initialization fails
        """
        try:
            # Validate configuration
            errors = config.validate_config()
            if errors:
                raise TracerError(f"Configuration validation failed: {', '.join(errors)}")

            # Create storage backend
            storage = await create_storage_backend(config.storage)

            # Create metrics collector
            metrics = MetricsCollector(config.metrics)
            await metrics.start()

            # Create tracer instance
            tracer = cls(config, storage, metrics)

            # Start background tasks
            await tracer._start_background_tasks()

            return tracer

        except Exception as e:
            logger.error("Failed to initialize tracer", error=str(e))
            raise TracerError(f"Failed to initialize tracer: {e}") from e

    async def _start_background_tasks(self) -> None:
        """Start background tasks for metrics collection and cleanup."""
        if self._config.metrics.enabled:
            task = asyncio.create_task(self._metrics_collection_loop())
            self._background_tasks.append(task)

        # Export functionality removed - data is sent via API instead

        # Start data ingester
        await self._ingester.start()

        # Cleanup task
        task = asyncio.create_task(self._cleanup_loop())
        self._background_tasks.append(task)

    async def _metrics_collection_loop(self) -> None:
        """Background task for metrics collection."""
        while not self._shutdown:
            try:
                await asyncio.sleep(self._config.metrics.collection_interval_seconds)
                if not self._shutdown:
                    await self._collect_system_metrics()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error("Error in metrics collection loop", error=str(e))

    async def _cleanup_loop(self) -> None:
        """Background task for cleanup operations."""
        while not self._shutdown:
            try:
                await asyncio.sleep(3600)  # Run cleanup every hour
                if not self._shutdown:
                    await self._cleanup_old_data()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error("Error in cleanup loop", error=str(e))

    async def _collect_system_metrics(self) -> None:
        """Collect system-level metrics."""
        try:
            # Collect active spans count
            await self._metrics.set_gauge("active_spans", len(self._active_spans))

            # Collect storage metrics
            stats = await self._storage.get_trace_stats(
                datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0), datetime.utcnow()
            )

            await self._metrics.set_gauge("total_traces", stats.total_traces)
            await self._metrics.set_gauge("total_spans", stats.total_spans)
            await self._metrics.set_gauge("error_spans", stats.error_spans)
            await self._metrics.set_gauge("avg_duration_ms", stats.avg_duration_ms)

        except Exception as e:
            logger.error("Failed to collect system metrics", error=str(e))

    async def _cleanup_old_data(self) -> None:
        """Clean up old trace data based on retention policy."""
        try:
            retention_days = self._config.export.retention_days
            cutoff_time = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            cutoff_time = cutoff_time.replace(day=cutoff_time.day - retention_days)

            deleted_count = await self._storage.cleanup_old_traces(cutoff_time)

            if deleted_count > 0:
                logger.info("Cleaned up old traces", deleted_count=deleted_count, cutoff_time=cutoff_time)
                await self._metrics.increment_counter("traces_cleaned_up", deleted_count)

        except Exception as e:
            logger.error("Failed to cleanup old data", error=str(e))

    async def start_span(
        self,
        name: str,
        kind: SpanKind = SpanKind.INTERNAL,
        parent_span_id: Optional[SpanId] = None,
        trace_id: Optional[TraceId] = None,
    ) -> SpanId:
        """Start a new span.

        Args:
            name: Span name
            kind: Span kind
            parent_span_id: Optional parent span ID
            trace_id: Optional trace ID (will be generated if not provided)

        Returns:
            Span ID of the created span

        Raises:
            TracerError: If span creation fails
        """
        if not self._config.enabled:
            return str(uuid.uuid4())  # Return dummy span ID when disabled

        try:
            # Generate IDs
            span_id = str(uuid.uuid4())

            # If parent_span_id is provided, inherit trace_id from parent
            if trace_id is None:
                if parent_span_id:
                    # Check active spans first (parent might not be finished yet)
                    parent_span = self._active_spans.get(parent_span_id)
                    if parent_span:
                        trace_id = parent_span.trace_id
                    else:
                        # Try storage if not in active spans
                        parent_span = await self.get_span(parent_span_id)
                        if parent_span:
                            trace_id = parent_span.trace_id
                        else:
                            trace_id = str(uuid.uuid4())
                else:
                    trace_id = str(uuid.uuid4())

            # Check sampling
            if not self._should_sample():
                return span_id  # Return span ID but don't actually trace

            # Create span
            span = TraceSpan(
                trace_id=trace_id,
                span_id=span_id,
                parent_span_id=parent_span_id,
                name=name,
                kind=kind,
                resource=self._config.resource_attributes.copy(),
            )

            # Store in active spans
            self._active_spans[span_id] = span

            # Record metrics
            await self._metrics.increment_counter("spans_started", labels=[("kind", kind.value)])

            logger.debug("Started span", span_id=span_id, name=name, kind=kind.value)

            return span_id

        except Exception as e:
            logger.error("Failed to start span", error=str(e), name=name)
            raise TracerError(f"Failed to start span: {e}") from e

    def _should_sample(self) -> bool:
        """Determine if a span should be sampled based on sampling rate."""
        return random.random() < self._config.sampling_rate

    async def finish_span(self, span_id: SpanId) -> None:
        """Finish a span successfully.

        Args:
            span_id: Span ID to finish

        Raises:
            TracerError: If span finishing fails
        """
        await self._finish_span_internal(span_id, SpanStatus.OK)

    async def finish_span_with_error(
        self,
        span_id: SpanId,
        error_message: str,
        error_type: Optional[str] = None,
    ) -> None:
        """Finish a span with an error.

        Args:
            span_id: Span ID to finish
            error_message: Error message
            error_type: Optional error type

        Raises:
            TracerError: If span finishing fails
        """
        await self._finish_span_internal(span_id, SpanStatus.ERROR, error_message, error_type)

    async def _finish_span_internal(
        self,
        span_id: SpanId,
        status: SpanStatus,
        error_message: Optional[str] = None,
        error_type: Optional[str] = None,
    ) -> None:
        """Internal method to finish a span."""
        if not self._config.enabled:
            return

        try:
            span = self._active_spans.get(span_id)
            if span is None:
                logger.warning("Attempted to finish unknown span", span_id=span_id)
                return

            # Update span
            span.end_time = datetime.utcnow()
            span.status = status

            if error_message:
                span.set_attribute("error.message", error_message)
            if error_type:
                span.set_attribute("error.type", error_type)

            # Store span
            await self._storage.store_span(span)

            # Remove from active spans
            del self._active_spans[span_id]

            # Record metrics
            await self._metrics.increment_counter("spans_finished", labels=[("status", status.value)])

            if span.duration_ms:
                await self._metrics.record_histogram("span_duration_ms", span.duration_ms)

            logger.debug("Finished span", span_id=span_id, status=status.value, duration_ms=span.duration_ms)

        except Exception as e:
            logger.error("Failed to finish span", error=str(e), span_id=span_id)
            raise TracerError(f"Failed to finish span: {e}") from e

    async def set_span_attribute(self, span_id: SpanId, key: str, value: Any) -> None:
        """Set an attribute on a span.

        Args:
            span_id: Span ID
            key: Attribute key
            value: Attribute value

        Raises:
            TracerError: If setting attribute fails
        """
        if not self._config.enabled:
            return

        try:
            span = self._active_spans.get(span_id)
            if span is None:
                logger.warning("Attempted to set attribute on unknown span", span_id=span_id)
                return

            # Check attribute limits
            if len(span.attributes) >= self._config.max_span_attributes:
                logger.warning("Span attribute limit reached", span_id=span_id, limit=self._config.max_span_attributes)
                return

            span.set_attribute(key, value)
            logger.debug("Set span attribute", span_id=span_id, key=key)

        except Exception as e:
            logger.error("Failed to set span attribute", error=str(e), span_id=span_id, key=key)
            raise TracerError(f"Failed to set span attribute: {e}") from e

    async def add_span_event(self, span_id: SpanId, event: SpanEvent) -> None:
        """Add an event to a span.

        Args:
            span_id: Span ID
            event: Span event to add

        Raises:
            TracerError: If adding event fails
        """
        if not self._config.enabled:
            return

        try:
            span = self._active_spans.get(span_id)
            if span is None:
                logger.warning("Attempted to add event to unknown span", span_id=span_id)
                return

            # Check event limits
            if len(span.events) >= self._config.max_span_events:
                logger.warning("Span event limit reached", span_id=span_id, limit=self._config.max_span_events)
                return

            span.add_event(event)
            logger.debug("Added span event", span_id=span_id, event_name=event.name)

        except Exception as e:
            logger.error("Failed to add span event", error=str(e), span_id=span_id)
            raise TracerError(f"Failed to add span event: {e}") from e

    async def get_span(self, span_id: SpanId) -> Optional[TraceSpan]:
        """Get a span by ID.

        Args:
            span_id: Span ID

        Returns:
            Span if found, None otherwise
        """
        # Check active spans first
        if span_id in self._active_spans:
            return self._active_spans[span_id]

        # Check storage
        try:
            return await self._storage.get_span(span_id)
        except Exception as e:
            logger.error("Failed to get span", error=str(e), span_id=span_id)
            return None

    async def search_traces(self, query: SearchQuery) -> List[TraceSpan]:
        """Search for traces matching the query.

        Args:
            query: Search query parameters

        Returns:
            List of matching spans
        """
        try:
            return await self._storage.search_traces(query)
        except Exception as e:
            logger.error("Failed to search traces", error=str(e))
            raise TracerError(f"Failed to search traces: {e}") from e

    async def get_trace_stats(self, start_time: datetime, end_time: datetime) -> TraceStats:
        """Get trace statistics for a time period.

        Args:
            start_time: Start time
            end_time: End time

        Returns:
            Trace statistics
        """
        try:
            return await self._storage.get_trace_stats(start_time, end_time)
        except Exception as e:
            logger.error("Failed to get trace stats", error=str(e))
            raise TracerError(f"Failed to get trace stats: {e}") from e

    @asynccontextmanager
    async def trace_span(
        self,
        name: str,
        kind: SpanKind = SpanKind.INTERNAL,
        parent_span_id: Optional[SpanId] = None,
    ):
        """Context manager for tracing a span.

        Args:
            name: Span name
            kind: Span kind
            parent_span_id: Optional parent span ID

        Yields:
            Span ID

        Example:
            async with tracer.trace_span("my_operation") as span_id:
                await tracer.set_span_attribute(span_id, "key", "value")
                # Do work
        """
        span_id = await self.start_span(name, kind, parent_span_id)
        try:
            yield span_id
            await self.finish_span(span_id)
        except Exception as e:
            await self.finish_span_with_error(span_id, str(e), type(e).__name__)
            raise

    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on tracer components.

        Returns:
            Health check results
        """
        health = {
            "tracer": {"status": "healthy", "enabled": self._config.enabled},
            "storage": {"status": "unknown"},
            "metrics": {"status": "unknown"},
            "active_spans": len(self._active_spans),
        }

        # Check storage
        try:
            await self._storage.health_check()
            health["storage"]["status"] = "healthy"
        except Exception as e:
            health["storage"]["status"] = "unhealthy"
            health["storage"]["error"] = str(e)

        # Check metrics
        try:
            await self._metrics.health_check()
            health["metrics"]["status"] = "healthy"
        except Exception as e:
            health["metrics"]["status"] = "unhealthy"
            health["metrics"]["error"] = str(e)

        return health

    async def shutdown(self) -> None:
        """Shutdown the tracer and cleanup resources."""
        logger.info("Shutting down GraphBit Tracer")

        self._shutdown = True

        # Cancel background tasks
        for task in self._background_tasks:
            task.cancel()

        # Wait for tasks to complete
        if self._background_tasks:
            await asyncio.gather(*self._background_tasks, return_exceptions=True)

        # Finish any remaining active spans
        for span_id in list(self._active_spans.keys()):
            await self.finish_span_with_error(span_id, "Tracer shutdown", "shutdown")

        # Shutdown components
        if self._ingester:
            await self._ingester.stop()

        if self._metrics:
            await self._metrics.shutdown()

        # Exporter removed - no shutdown needed

        logger.info("GraphBit Tracer shutdown complete")

    # Properties

    @property
    def config(self) -> TracerConfig:
        """Get tracer configuration."""
        return self._config

    # GraphBit Integration Methods

    async def trace_graphbit_llm_response(
        self,
        provider: str,
        model: str,
        graphbit_response: Any,
        request_data: Optional[Dict[str, Any]] = None,
        cost_info: Optional["CostInfo"] = None,
        parent_span_id: Optional[str] = None,
        trace_id: Optional[str] = None,
    ) -> str:
        """Convenience method to trace a GraphBit LLM response.

        This is a high-level method that delegates to the LLM tracer for
        direct GraphBit integration.

        Args:
            provider: LLM provider name (e.g., 'openai', 'anthropic')
            model: Model name
            graphbit_response: GraphBit LlmResponse object
            request_data: Optional request data dictionary
            cost_info: Optional cost information
            parent_span_id: Optional parent span ID
            trace_id: Optional trace ID

        Returns:
            Span ID of the created trace

        Raises:
            ImportError: If GraphBit is not available
        """
        return await self._llm_tracer.trace_graphbit_response(
            provider=provider,
            model=model,
            graphbit_response=graphbit_response,
            request_data=request_data,
            cost_info=cost_info,
            parent_span_id=parent_span_id,
            trace_id=trace_id,
        )
