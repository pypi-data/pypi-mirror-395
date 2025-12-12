"""
Metrics collection for GraphBit Tracer.
Pure data collection without external monitoring tool dependencies.
"""

import asyncio
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from bitpulse.utils.logging_utils import setup_logging

from .config import MetricsConfig

logger = setup_logging()


class MetricsError(Exception):
    """Base exception for metrics errors."""

    pass


class MetricsCollector:
    """Metrics collector for GraphBit Tracer."""

    def __init__(self, config: MetricsConfig):
        """Initialize metrics collector.

        Args:
            config: Metrics configuration
        """
        self._config = config
        self._enabled = config.enabled

        # Internal metrics storage only
        self._internal_counters: Dict[str, float] = defaultdict(float)
        self._internal_gauges: Dict[str, float] = defaultdict(float)
        self._internal_histograms: Dict[str, List[float]] = defaultdict(list)

        # Background tasks
        self._background_tasks: List[asyncio.Task] = []
        self._shutdown = False

        if self._enabled:
            logger.info("Internal metrics collector initialized")

    async def start(self) -> None:
        """Start the metrics collector."""
        if not self._enabled:
            return

        logger.info("Starting metrics collector")

        # Start background tasks if needed
        # Currently no background tasks, but could add metric aggregation, etc.

    async def increment_counter(
        self,
        name: str,
        value: float = 1.0,
        labels: Optional[List[Tuple[str, str]]] = None,
    ) -> None:
        """Increment a counter metric.

        Args:
            name: Counter name
            value: Value to increment by
            labels: Optional labels
        """
        if not self._enabled:
            return

        try:
            # Update internal counter
            label_key = self._make_label_key(labels)
            self._internal_counters[f"{name}:{label_key}"] += value

        except Exception as e:
            logger.error("Failed to increment counter", error=str(e), name=name)

    async def set_gauge(self, name: str, value: float, labels: Optional[List[Tuple[str, str]]] = None) -> None:
        """Set a gauge metric value.

        Args:
            name: Gauge name
            value: Value to set
            labels: Optional labels
        """
        if not self._enabled:
            return

        try:
            # Update internal gauge
            label_key = self._make_label_key(labels)
            self._internal_gauges[f"{name}:{label_key}"] = value

        except Exception as e:
            logger.error("Failed to set gauge", error=str(e), name=name)

    async def record_histogram(
        self,
        name: str,
        value: float,
        labels: Optional[List[Tuple[str, str]]] = None,
    ) -> None:
        """Record a histogram value.

        Args:
            name: Histogram name
            value: Value to record
            labels: Optional labels
        """
        if not self._enabled:
            return

        try:
            # Update internal histogram
            label_key = self._make_label_key(labels)
            self._internal_histograms[f"{name}:{label_key}"].append(value)

            # Keep only recent values (last 1000)
            if len(self._internal_histograms[f"{name}:{label_key}"]) > 1000:
                self._internal_histograms[f"{name}:{label_key}"] = self._internal_histograms[f"{name}:{label_key}"][
                    -1000:
                ]

        except Exception as e:
            logger.error("Failed to record histogram", error=str(e), name=name)

    def _make_label_key(self, labels: Optional[List[Tuple[str, str]]]) -> str:
        """Create a string key from labels for internal storage."""
        if not labels:
            return ""
        return ",".join(f"{k}={v}" for k, v in sorted(labels))

    # Convenience methods for common metrics

    async def record_llm_request(
        self,
        provider: str,
        model: str,
        duration_ms: float,
        success: bool = True,
    ) -> None:
        """Record an LLM request.

        Args:
            provider: LLM provider name
            model: Model name
            duration_ms: Request duration in milliseconds
            success: Whether the request was successful
        """
        labels = [("provider", provider), ("model", model)]

        await self.increment_counter("llm_requests", labels=labels)
        await self.record_histogram("llm_duration_ms", duration_ms, labels=labels)

        if not success:
            await self.increment_counter("llm_errors", labels=labels)

    async def record_llm_tokens(
        self,
        provider: str,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
    ) -> None:
        """Record LLM token usage.

        Args:
            provider: LLM provider name
            model: Model name
            prompt_tokens: Number of prompt tokens
            completion_tokens: Number of completion tokens
        """
        base_labels = [("provider", provider), ("model", model)]

        await self.increment_counter("llm_tokens", value=prompt_tokens, labels=base_labels + [("type", "prompt")])

        await self.increment_counter(
            "llm_tokens", value=completion_tokens, labels=base_labels + [("type", "completion")]
        )

    async def record_llm_cost(self, provider: str, model: str, cost: float) -> None:
        """Record LLM cost.

        Args:
            provider: LLM provider name
            model: Model name
            cost: Cost in USD
        """
        labels = [("provider", provider), ("model", model)]
        await self.increment_counter("llm_cost", value=cost, labels=labels)

    async def record_workflow_execution(
        self,
        workflow_name: str,
        duration: timedelta,
        success: bool,
    ) -> None:
        """Record a workflow execution.

        Args:
            workflow_name: Workflow name
            duration: Execution duration
            success: Whether execution was successful
        """
        duration_ms = duration.total_seconds() * 1000
        status = "success" if success else "error"

        labels = [("workflow_name", workflow_name)]
        status_labels = labels + [("status", status)]

        await self.increment_counter("workflow_executions", labels=status_labels)
        await self.record_histogram("workflow_duration_ms", duration_ms, labels=labels)

    async def get_metrics_snapshot(self) -> Dict[str, Any]:
        """Get a snapshot of current metrics.

        Returns:
            Dictionary containing current metric values
        """
        return {
            "counters": dict(self._internal_counters),
            "gauges": dict(self._internal_gauges),
            "histograms": {
                name: {
                    "count": len(values),
                    "sum": sum(values),
                    "avg": sum(values) / len(values) if values else 0,
                    "min": min(values) if values else 0,
                    "max": max(values) if values else 0,
                }
                for name, values in self._internal_histograms.items()
            },
            "timestamp": datetime.utcnow().isoformat(),
        }

    async def health_check(self) -> None:
        """Perform health check on metrics collector.

        Raises:
            MetricsError: If health check fails
        """
        if not self._enabled:
            return

        # Check if we can access internal metrics
        try:
            _ = len(self._internal_counters)
            _ = len(self._internal_gauges)
            _ = len(self._internal_histograms)
        except Exception as e:
            raise MetricsError(f"Metrics collector health check failed: {e}") from e

    async def shutdown(self) -> None:
        """Shutdown the metrics collector."""
        logger.info("Shutting down metrics collector")

        self._shutdown = True

        # Cancel background tasks
        for task in self._background_tasks:
            task.cancel()

        # Wait for tasks to complete
        if self._background_tasks:
            await asyncio.gather(*self._background_tasks, return_exceptions=True)

        logger.info("Metrics collector shutdown complete")
