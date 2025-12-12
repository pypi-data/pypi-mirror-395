"""In-memory storage backend for GraphBit Tracer."""

import asyncio
from collections import OrderedDict
from datetime import datetime, timedelta
from typing import List, Optional

from bitpulse.core.exceptions import StorageError
from bitpulse.schemas.types import LlmTrace, SearchQuery, SpanId, SpanStatus, TraceSpan, TraceStats, WorkflowTrace
from bitpulse.storage.base import StorageBackend


class MemoryStorageBackend(StorageBackend):
    """In-memory storage backend for development and testing."""

    def __init__(self, capacity: int = 10000):
        """Initialize memory storage.

        Args:
            capacity: Maximum number of spans to store
        """
        self._capacity = capacity
        self._spans: OrderedDict[SpanId, TraceSpan] = OrderedDict()
        self._llm_traces: OrderedDict[SpanId, LlmTrace] = OrderedDict()
        self._workflow_traces: OrderedDict[SpanId, WorkflowTrace] = OrderedDict()
        self._lock = asyncio.Lock()

    async def store_span(self, span: TraceSpan) -> None:
        """Store a span in memory."""
        async with self._lock:
            # Remove oldest spans if at capacity
            while len(self._spans) >= self._capacity:
                oldest_span_id = next(iter(self._spans))
                del self._spans[oldest_span_id]
                # Also remove from specialized traces
                self._llm_traces.pop(oldest_span_id, None)
                self._workflow_traces.pop(oldest_span_id, None)

            self._spans[span.span_id] = span

    async def get_span(self, span_id: SpanId) -> Optional[TraceSpan]:
        """Get a span by ID."""
        async with self._lock:
            return self._spans.get(span_id)

    async def search_traces(self, query: SearchQuery) -> List[TraceSpan]:
        """Search for traces matching the query."""
        async with self._lock:
            results = []

            for span in self._spans.values():
                # Apply filters
                if query.trace_ids and span.trace_id not in query.trace_ids:
                    continue

                if query.span_names and span.name not in query.span_names:
                    continue

                if query.span_kinds and span.kind not in query.span_kinds:
                    continue

                if query.status and span.status not in query.status:
                    continue

                if query.start_time and span.start_time < query.start_time:
                    continue

                if query.end_time and span.start_time > query.end_time:
                    continue

                # Check attribute filters
                if query.attributes:
                    match = True
                    for key, value in query.attributes.items():
                        if key not in span.attributes or span.attributes[key] != value:
                            match = False
                            break
                    if not match:
                        continue

                results.append(span)

            # Sort by start time (newest first)
            results.sort(key=lambda s: s.start_time, reverse=True)

            # Apply pagination
            offset = query.offset or 0
            limit = query.limit or len(results)

            return results[offset : offset + limit]

    async def store_llm_trace(self, trace: LlmTrace) -> None:
        """Store an LLM trace."""
        async with self._lock:
            # Note: The span should already be stored by the tracer when it's finished
            # We only need to store the LLM-specific data here
            self._llm_traces[trace.span.span_id] = trace

    async def get_llm_traces(
        self,
        start_time: datetime,
        end_time: datetime,
        limit: Optional[int] = None,
    ) -> List[LlmTrace]:
        """Get LLM traces in a time range."""
        async with self._lock:
            results = []

            for trace in self._llm_traces.values():
                if start_time <= trace.span.start_time <= end_time:
                    results.append(trace)

            # Sort by start time (newest first)
            results.sort(key=lambda t: t.span.start_time, reverse=True)

            if limit:
                results = results[:limit]

            return results

    async def get_recent_llm_traces(
        self,
        minutes: int = 5,
        limit: Optional[int] = None,
    ) -> List[LlmTrace]:
        """Get recent LLM traces from the last N minutes."""
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(minutes=minutes)
        return await self.get_llm_traces(start_time, end_time, limit)

    async def get_workflow_traces(
        self,
        start_time: datetime,
        end_time: datetime,
        limit: Optional[int] = None,
    ) -> List[WorkflowTrace]:
        """Get workflow traces in a time range."""
        async with self._lock:
            results = []

            for trace in self._workflow_traces.values():
                if start_time <= trace.span.start_time <= end_time:
                    results.append(trace)

            # Sort by start time (newest first)
            results.sort(key=lambda t: t.span.start_time, reverse=True)

            if limit:
                results = results[:limit]

            return results

    async def get_trace_stats(
        self,
        start_time: datetime,
        end_time: datetime,
    ) -> TraceStats:
        """Get trace statistics for a time period."""
        async with self._lock:
            # Filter spans in time range
            spans_in_range = [span for span in self._spans.values() if start_time <= span.start_time <= end_time]

            if not spans_in_range:
                return TraceStats(
                    total_traces=0,
                    total_spans=0,
                    successful_spans=0,
                    error_spans=0,
                    avg_duration_ms=0.0,
                    total_llm_calls=0,
                    total_llm_cost=0.0,
                    total_tokens=0,
                    unique_workflows=0,
                    time_period_start=start_time,
                    time_period_end=end_time,
                )

            # Calculate basic stats
            total_spans = len(spans_in_range)
            successful_spans = len([s for s in spans_in_range if s.status == SpanStatus.OK])
            error_spans = len([s for s in spans_in_range if s.status == SpanStatus.ERROR])

            # Calculate average duration
            finished_spans = [s for s in spans_in_range if s.duration_ms is not None]
            avg_duration_ms = (
                sum(s.duration_ms for s in finished_spans) / len(finished_spans) if finished_spans else 0.0
            )

            # Count unique traces
            unique_traces = len(set(span.trace_id for span in spans_in_range))

            # LLM stats
            llm_traces_in_range = [
                trace for trace in self._llm_traces.values() if start_time <= trace.span.start_time <= end_time
            ]

            total_llm_calls = len(llm_traces_in_range)
            total_llm_cost = sum(trace.cost.total_cost for trace in llm_traces_in_range if trace.cost is not None)
            total_tokens = sum(trace.usage.total_tokens for trace in llm_traces_in_range if trace.usage is not None)

            # Workflow stats
            workflow_traces_in_range = [
                trace for trace in self._workflow_traces.values() if start_time <= trace.span.start_time <= end_time
            ]
            unique_workflows = len(set(trace.workflow_name for trace in workflow_traces_in_range))

            return TraceStats(
                total_traces=unique_traces,
                total_spans=total_spans,
                successful_spans=successful_spans,
                error_spans=error_spans,
                avg_duration_ms=avg_duration_ms,
                total_llm_calls=total_llm_calls,
                total_llm_cost=total_llm_cost,
                total_tokens=total_tokens,
                unique_workflows=unique_workflows,
                time_period_start=start_time,
                time_period_end=end_time,
            )

    async def cleanup_old_traces(self, older_than: datetime) -> int:
        """Clean up traces older than the specified time."""
        async with self._lock:
            old_span_ids = [span_id for span_id, span in self._spans.items() if span.start_time < older_than]

            for span_id in old_span_ids:
                del self._spans[span_id]
                self._llm_traces.pop(span_id, None)
                self._workflow_traces.pop(span_id, None)

            return len(old_span_ids)

    async def health_check(self) -> None:
        """Perform health check."""
        # Memory backend is always healthy if we can access the data structures
        async with self._lock:
            if not isinstance(self._spans, OrderedDict):
                raise StorageError("Memory storage corrupted")
