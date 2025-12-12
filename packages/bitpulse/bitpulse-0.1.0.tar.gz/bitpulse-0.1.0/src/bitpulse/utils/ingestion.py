"""Data ingestion module for consuming tracing data from GraphBit's observability features."""

import asyncio
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional

from bitpulse.schemas.types import CostInfo, is_graphbit_available

if TYPE_CHECKING:
    from bitpulse.core.core import GraphBitTracer

from bitpulse.utils.logging_utils import setup_logging

logger = setup_logging()


class IngestionError(Exception):
    """Base exception for data ingestion errors."""

    pass


class GraphBitDataIngester:
    """Data ingester for consuming tracing data from GraphBit's observability features."""

    def __init__(self, tracer: "GraphBitTracer"):
        """Initialize data ingester.

        Args:
            tracer: Main GraphBit tracer instance
        """
        self._tracer = tracer
        self._config = tracer.config
        self._active_ingestion_tasks: List[asyncio.Task] = []
        self._shutdown = False
        self._callbacks: Dict[str, List[Callable]] = {
            "llm_response": [],
            "workflow_event": [],
            "span_event": [],
            "error": [],
        }

        # GraphBit integration check
        if not is_graphbit_available():
            logger.warning("GraphBit is not available. Some ingestion features will be limited.")

    async def start(self) -> None:
        """Start the data ingester."""
        logger.info("Starting GraphBit data ingester")

        # Start background ingestion tasks
        if is_graphbit_available():
            task = asyncio.create_task(self._graphbit_monitoring_loop())
            self._active_ingestion_tasks.append(task)

        logger.info("GraphBit data ingester started")

    async def stop(self) -> None:
        """Stop the data ingester."""
        logger.info("Stopping GraphBit data ingester")
        self._shutdown = True

        # Cancel all active tasks
        for task in self._active_ingestion_tasks:
            task.cancel()

        # Wait for tasks to complete
        if self._active_ingestion_tasks:
            await asyncio.gather(*self._active_ingestion_tasks, return_exceptions=True)

        logger.info("GraphBit data ingester stopped")

    async def ingest_graphbit_response(
        self,
        provider: str,
        model: str,
        graphbit_response: Any,
        request_data: Optional[Dict[str, Any]] = None,
        cost_info: Optional[CostInfo] = None,
        parent_span_id: Optional[str] = None,
        trace_id: Optional[str] = None,
    ) -> str:
        """Ingest a GraphBit LLM response and create a trace.

        Args:
            provider: LLM provider name
            model: Model name
            graphbit_response: GraphBit LlmResponse object
            request_data: Optional request data
            cost_info: Optional cost information
            parent_span_id: Optional parent span ID
            trace_id: Optional trace ID

        Returns:
            Span ID of the created trace
        """
        try:
            # Use the tracer's GraphBit integration method
            span_id = await self._tracer.trace_graphbit_llm_response(
                provider=provider,
                model=model,
                graphbit_response=graphbit_response,
                request_data=request_data,
                cost_info=cost_info,
                parent_span_id=parent_span_id,
                trace_id=trace_id,
            )

            # Trigger callbacks
            await self._trigger_callbacks(
                "llm_response",
                {
                    "span_id": span_id,
                    "provider": provider,
                    "model": model,
                    "response": graphbit_response,
                    "request_data": request_data,
                    "cost_info": cost_info,
                },
            )

            return span_id

        except Exception as e:
            logger.error("Failed to ingest GraphBit response", error=str(e))
            await self._trigger_callbacks(
                "error", {"error": str(e), "provider": provider, "model": model, "response": graphbit_response}
            )
            raise IngestionError(f"Failed to ingest GraphBit response: {e}") from e

    async def ingest_batch_responses(self, responses: List[Dict[str, Any]]) -> List[str]:
        """Ingest a batch of GraphBit responses.

        Args:
            responses: List of response dictionaries with keys:
                - provider: str
                - model: str
                - graphbit_response: GraphBit response object
                - request_data: Optional[Dict]
                - cost_info: Optional[CostInfo]
                - parent_span_id: Optional[str]
                - trace_id: Optional[str]

        Returns:
            List of span IDs for created traces
        """
        span_ids = []

        for response_data in responses:
            try:
                span_id = await self.ingest_graphbit_response(**response_data)
                span_ids.append(span_id)
            except Exception as e:
                logger.error("Failed to ingest response in batch", error=str(e), response=response_data)
                # Continue with other responses
                continue

        logger.info("Batch ingestion completed", total=len(responses), successful=len(span_ids))
        return span_ids

    async def ingest_from_stream(
        self, stream_source: Any, parser: Optional[Callable[[Any], Dict[str, Any]]] = None
    ) -> None:
        """Ingest data from a streaming source.

        Args:
            stream_source: Streaming data source (e.g., WebSocket, message queue)
            parser: Optional parser function to convert stream data to ingestion format
        """
        logger.info("Starting stream ingestion")

        try:
            async for data in stream_source:
                if self._shutdown:
                    break

                try:
                    # Parse data if parser provided
                    if parser:
                        parsed_data = parser(data)
                    else:
                        parsed_data = data

                    # Ingest the data
                    await self.ingest_graphbit_response(**parsed_data)

                except Exception as e:
                    logger.error("Failed to ingest stream data", error=str(e), data=data)
                    await self._trigger_callbacks("error", {"error": str(e), "data": data, "source": "stream"})

        except Exception as e:
            logger.error("Stream ingestion failed", error=str(e))
            raise IngestionError(f"Stream ingestion failed: {e}") from e

    async def _graphbit_monitoring_loop(self) -> None:
        """Background task to monitor GraphBit for new tracing data."""
        logger.info("Starting GraphBit monitoring loop")

        while not self._shutdown:
            try:
                # This would integrate with GraphBit's observability hooks
                # For now, this is a placeholder for future GraphBit integration
                await asyncio.sleep(1.0)

                # TODO: Implement actual GraphBit monitoring
                # This could involve:
                # 1. Polling GraphBit's internal trace buffer
                # 2. Subscribing to GraphBit's event system
                # 3. Reading from GraphBit's observability endpoints

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error("Error in GraphBit monitoring loop", error=str(e))
                await asyncio.sleep(5.0)  # Back off on error

    async def _trigger_callbacks(self, event_type: str, data: Dict[str, Any]) -> None:
        """Trigger registered callbacks for an event type.

        Args:
            event_type: Type of event
            data: Event data to pass to callbacks
        """
        callbacks = self._callbacks.get(event_type, [])

        for callback in callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(data)
                else:
                    callback(data)
            except Exception as e:
                logger.error("Callback failed", event_type=event_type, callback=callback.__name__, error=str(e))


# Utility functions for common ingestion patterns


async def create_ingester(tracer: "GraphBitTracer") -> GraphBitDataIngester:
    """Create and start a data ingester.

    Args:
        tracer: GraphBit tracer instance

    Returns:
        Started data ingester
    """
    ingester = GraphBitDataIngester(tracer)
    await ingester.start()
    return ingester
