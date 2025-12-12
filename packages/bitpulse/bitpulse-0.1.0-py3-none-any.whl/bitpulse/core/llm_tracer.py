"""Enhanced LLM tracing capabilities for comprehensive observability."""

import json
from contextlib import asynccontextmanager
from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional

if TYPE_CHECKING:
    from .core import GraphBitTracer

from bitpulse.schemas.types import (
    CostInfo,
    LlmRequest,
    LlmResponse,
    LlmTrace,
    SpanEvent,
    SpanKind,
    SpanStatus,
    TokenUsage,
    TraceSpan,
    create_llm_trace_from_graphbit,
    is_graphbit_available,
)
from bitpulse.utils.logging_utils import setup_logging

logger = setup_logging()


class LLMTracer:
    """Enhanced LLM tracer for comprehensive observability."""

    def __init__(self, tracer: "GraphBitTracer"):
        """Initialize LLM tracer.

        Args:
            tracer: Main GraphBit tracer instance
        """
        self._tracer = tracer
        self._active_llm_traces: Dict[str, LlmTrace] = {}

    @asynccontextmanager
    async def trace_llm_call(self, provider: str, model: str, request_data: Dict[str, Any], **kwargs):
        """Context manager for tracing LLM calls with comprehensive logging.

        Args:
            provider: LLM provider name (e.g., 'openai', 'anthropic')
            model: Model name
            request_data: Request payload data
            **kwargs: Additional parameters

        Yields:
            LLM trace context with methods for updating trace data
        """
        span_name = f"llm.{provider}.{model}"
        trace_id = None

        span_id = await self._tracer.start_span(span_name, SpanKind.CLIENT)
        start_time = datetime.utcnow()

        try:
            # Create LLM request object
            llm_request = self._create_llm_request(request_data, model, **kwargs)

            # Get the span for the trace
            span = await self._tracer.get_span(span_id)
            if span:
                trace_id = span.trace_id

            # Create initial LLM trace
            llm_trace = LlmTrace(
                span=span,
                provider=provider,
                model=model,
                request=llm_request,
                response=None,
                usage=None,
                cost=None,
                error=None,
            )

            # Store active trace
            self._active_llm_traces[span_id] = llm_trace

            # Set comprehensive span attributes
            await self._set_request_attributes(span_id, provider, model, llm_request)

            # Add start event
            start_event = SpanEvent(name="llm.request.start")
            start_event.with_attribute("provider", provider)
            start_event.with_attribute("model", model)
            start_event.with_attribute("request.message_count", len(llm_request.messages))
            start_event.with_attribute("request.has_tools", len(llm_request.tools) > 0)
            start_event.with_attribute("timestamp", start_time.isoformat())
            await self._tracer.add_span_event(span_id, start_event)

            # Create trace context
            trace_context = LLMTraceContext(span_id=span_id, trace_id=trace_id, llm_tracer=self, start_time=start_time)

            try:
                yield trace_context

                # Finish span successfully
                await self._tracer.finish_span(span_id)

                # Finalize successful trace AFTER span is finished
                await self._finalize_trace(span_id, success=True)

            except Exception as e:
                # Finish span with error
                await self._tracer.finish_span_with_error(span_id, str(e), type(e).__name__)

                # Handle error trace
                await self._handle_trace_error(span_id, e, start_time)
                raise

        finally:
            # Clean up active trace
            self._active_llm_traces.pop(span_id, None)

    def _create_llm_request(self, request_data: Dict[str, Any], model: str, **kwargs) -> LlmRequest:
        """Create LLM request object from request data."""
        messages = request_data.get("messages", [])
        if isinstance(messages, str):
            messages = [{"role": "user", "content": messages}]

        return LlmRequest(
            messages=messages,
            model=model,
            temperature=request_data.get("temperature") or kwargs.get("temperature"),
            max_tokens=request_data.get("max_tokens") or kwargs.get("max_tokens"),
            tools=request_data.get("tools", []),
            tool_choice=request_data.get("tool_choice"),
            other_params={
                k: v
                for k, v in request_data.items()
                if k not in ["messages", "model", "temperature", "max_tokens", "tools", "tool_choice"]
            },
        )

    async def _set_request_attributes(self, span_id: str, provider: str, model: str, request: LlmRequest) -> None:
        """Set comprehensive request attributes on span."""
        await self._tracer.set_span_attribute(span_id, "llm.provider", provider)
        await self._tracer.set_span_attribute(span_id, "llm.model", model)
        await self._tracer.set_span_attribute(span_id, "llm.request.message_count", len(request.messages))

        if request.temperature is not None:
            await self._tracer.set_span_attribute(span_id, "llm.request.temperature", request.temperature)
        if request.max_tokens is not None:
            await self._tracer.set_span_attribute(span_id, "llm.request.max_tokens", request.max_tokens)
        if request.tools:
            await self._tracer.set_span_attribute(span_id, "llm.request.tools_count", len(request.tools))
            await self._tracer.set_span_attribute(span_id, "llm.request.has_tools", True)

        # Calculate approximate input size
        total_chars = sum(len(json.dumps(msg)) for msg in request.messages)
        await self._tracer.set_span_attribute(span_id, "llm.request.input_size_chars", total_chars)

    async def _finalize_trace(self, span_id: str, success: bool) -> None:
        """Finalize the LLM trace."""
        llm_trace = self._active_llm_traces.get(span_id)
        if not llm_trace:
            return

        # Update span with final attributes
        span = await self._tracer.get_span(span_id)
        if span:
            llm_trace.span = span

        # Store the completed trace
        await self._tracer.storage.store_llm_trace(llm_trace)

        # Record metrics (only if enabled)
        if self._tracer.config.metrics.enabled:
            duration_ms = llm_trace.span.duration_ms or 0
            await self._tracer.metrics.record_llm_request(
                llm_trace.provider, llm_trace.model, duration_ms, success=success
            )

            # Record token metrics if available
            if llm_trace.usage:
                await self._tracer.metrics.record_llm_tokens(
                    llm_trace.provider,
                    llm_trace.model,
                    llm_trace.usage.prompt_tokens,
                    llm_trace.usage.completion_tokens,
                )

            # Record cost metrics if available
            if llm_trace.cost:
                await self._tracer.metrics.record_llm_cost(
                    llm_trace.provider, llm_trace.model, llm_trace.cost.total_cost
                )

        # Broadcast real-time update (only if dashboard enabled)
        if hasattr(self._tracer, "_dashboard") and self._tracer._dashboard:
            await self._tracer._dashboard.broadcast_llm_trace_update(llm_trace)

        # Add completion event
        completion_event = SpanEvent(name="llm.request.complete")
        completion_event.with_attribute("success", success)
        completion_event.with_attribute("duration_ms", llm_trace.span.duration_ms or 0)
        completion_event.with_attribute("timestamp", datetime.utcnow().isoformat())
        await self._tracer.add_span_event(span_id, completion_event)

    async def _handle_trace_error(self, span_id: str, error: Exception, start_time: datetime) -> None:
        """Handle LLM trace error."""
        llm_trace = self._active_llm_traces.get(span_id)
        if llm_trace:
            llm_trace.error = str(error)

        # Calculate duration
        duration_ms = (datetime.utcnow() - start_time).total_seconds() * 1000

        # Set error attributes
        await self._tracer.set_span_attribute(span_id, "error", True)
        await self._tracer.set_span_attribute(span_id, "error.type", type(error).__name__)
        await self._tracer.set_span_attribute(span_id, "error.message", str(error))

        # Add error event
        error_event = SpanEvent(name="llm.request.error")
        error_event.with_attribute("error.type", type(error).__name__)
        error_event.with_attribute("error.message", str(error))
        error_event.with_attribute("duration_ms", duration_ms)
        error_event.with_attribute("timestamp", datetime.utcnow().isoformat())
        await self._tracer.add_span_event(span_id, error_event)

        # Finalize error trace
        await self._finalize_trace(span_id, success=False)

    async def trace_graphbit_response(
        self,
        provider: str,
        model: str,
        graphbit_response: Any,
        request_data: Optional[Dict[str, Any]] = None,
        cost_info: Optional[CostInfo] = None,
        parent_span_id: Optional[str] = None,
        trace_id: Optional[str] = None,
    ) -> str:
        """Trace a GraphBit LLM response directly.

        This method allows direct integration with GraphBit's LlmResponse objects,
        automatically converting them to the tracer's format.

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
        if not is_graphbit_available():
            raise ImportError("GraphBit is not available. Install with: pip install graphbit")

        # Create span for the LLM call
        span_id = await self._tracer.start_span(
            name=f"llm.{provider}.{model}", kind=SpanKind.CLIENT, parent_span_id=parent_span_id, trace_id=trace_id
        )

        # Create span object
        span = TraceSpan(
            span_id=span_id,
            trace_id=trace_id or span_id,
            name=f"llm.{provider}.{model}",
            kind=SpanKind.CLIENT,
            start_time=datetime.utcnow(),
        )

        try:
            # Create LLM trace from GraphBit response
            llm_trace = create_llm_trace_from_graphbit(
                span=span,
                provider=provider,
                model=model,
                graphbit_response=graphbit_response,
                request_data=request_data,
                cost_info=cost_info,
            )

            # Set span attributes
            await self._tracer.set_span_attribute(span_id, "llm.provider", provider)
            await self._tracer.set_span_attribute(span_id, "llm.model", model)
            await self._tracer.set_span_attribute(span_id, "llm.response.content", graphbit_response.content)
            await self._tracer.set_span_attribute(
                span_id, "llm.response.finish_reason", str(graphbit_response.finish_reason)
            )

            # Set usage attributes if available
            if hasattr(graphbit_response, "usage") and graphbit_response.usage:
                usage = graphbit_response.usage
                await self._tracer.set_span_attribute(span_id, "llm.usage.prompt_tokens", usage.prompt_tokens)
                await self._tracer.set_span_attribute(span_id, "llm.usage.completion_tokens", usage.completion_tokens)
                await self._tracer.set_span_attribute(span_id, "llm.usage.total_tokens", usage.total_tokens)

            # Set cost attributes if available
            if cost_info:
                await self._tracer.set_span_attribute(span_id, "llm.cost.prompt_cost", cost_info.prompt_cost)
                await self._tracer.set_span_attribute(span_id, "llm.cost.completion_cost", cost_info.completion_cost)
                await self._tracer.set_span_attribute(span_id, "llm.cost.total_cost", cost_info.total_cost)
                await self._tracer.set_span_attribute(span_id, "llm.cost.currency", cost_info.currency)

            # Set tool call attributes if available
            if hasattr(graphbit_response, "tool_calls") and graphbit_response.tool_calls:
                await self._tracer.set_span_attribute(
                    span_id, "llm.tool_calls.count", len(graphbit_response.tool_calls)
                )
                for i, tool_call in enumerate(graphbit_response.tool_calls):
                    await self._tracer.set_span_attribute(span_id, f"llm.tool_calls.{i}.id", tool_call.id)
                    await self._tracer.set_span_attribute(span_id, f"llm.tool_calls.{i}.name", tool_call.name)

            # Store the trace
            self._active_llm_traces[span_id] = llm_trace

            # End span successfully
            await self._tracer.end_span(span_id, SpanStatus.OK)

            # Broadcast update if dashboard is available
            if hasattr(self._tracer, "dashboard") and self._tracer.dashboard:
                await self._tracer.dashboard.broadcast_llm_trace_update(llm_trace)

            logger.info(
                "GraphBit LLM response traced successfully",
                span_id=span_id,
                provider=provider,
                model=model,
                content_length=len(graphbit_response.content),
                tool_calls=len(graphbit_response.tool_calls) if hasattr(graphbit_response, "tool_calls") else 0,
            )

            return span_id

        except Exception as e:
            # End span with error
            await self._tracer.end_span(span_id, SpanStatus.ERROR, str(e))
            logger.error("Failed to trace GraphBit LLM response", error=str(e), span_id=span_id)
            raise


class LLMTraceContext:
    """Context for an active LLM trace with methods to update trace data."""

    def __init__(self, span_id: str, trace_id: str, llm_tracer: LLMTracer, start_time: datetime):
        self.span_id = span_id
        self.trace_id = trace_id
        self._llm_tracer = llm_tracer
        self._start_time = start_time

    async def set_response(
        self, content: str, finish_reason: str = "stop", tool_calls: Optional[List[Dict[str, Any]]] = None, **kwargs
    ) -> None:
        """Set LLM response data."""
        llm_trace = self._llm_tracer._active_llm_traces.get(self.span_id)
        if not llm_trace:
            return

        # Create response object
        llm_response = LlmResponse(
            content=content,
            finish_reason=finish_reason,
            tool_calls=tool_calls or [],
            usage=None,  # Will be set separately
            model=llm_trace.model,
            other_data=kwargs,
        )

        llm_trace.response = llm_response

        # Set response attributes
        await self._llm_tracer._tracer.set_span_attribute(self.span_id, "llm.response.content_length", len(content))
        await self._llm_tracer._tracer.set_span_attribute(self.span_id, "llm.response.finish_reason", finish_reason)
        if tool_calls:
            await self._llm_tracer._tracer.set_span_attribute(
                self.span_id, "llm.response.tool_calls_count", len(tool_calls)
            )

    async def set_token_usage(
        self, prompt_tokens: int, completion_tokens: int, total_tokens: Optional[int] = None
    ) -> None:
        """Set token usage information."""
        llm_trace = self._llm_tracer._active_llm_traces.get(self.span_id)
        if not llm_trace:
            return

        if total_tokens is None:
            total_tokens = prompt_tokens + completion_tokens

        usage = TokenUsage(prompt_tokens=prompt_tokens, completion_tokens=completion_tokens, total_tokens=total_tokens)

        llm_trace.usage = usage

        # Set usage attributes
        await self._llm_tracer._tracer.set_span_attribute(self.span_id, "llm.usage.prompt_tokens", prompt_tokens)
        await self._llm_tracer._tracer.set_span_attribute(
            self.span_id, "llm.usage.completion_tokens", completion_tokens
        )
        await self._llm_tracer._tracer.set_span_attribute(self.span_id, "llm.usage.total_tokens", total_tokens)

    async def set_cost(self, prompt_cost: float, completion_cost: float, currency: str = "USD") -> None:
        """Set cost information."""
        llm_trace = self._llm_tracer._active_llm_traces.get(self.span_id)
        if not llm_trace:
            return

        total_cost = prompt_cost + completion_cost
        cost = CostInfo(
            prompt_cost=prompt_cost, completion_cost=completion_cost, total_cost=total_cost, currency=currency
        )

        llm_trace.cost = cost

        # Set cost attributes
        await self._llm_tracer._tracer.set_span_attribute(self.span_id, "llm.cost.prompt_cost", prompt_cost)
        await self._llm_tracer._tracer.set_span_attribute(self.span_id, "llm.cost.completion_cost", completion_cost)
        await self._llm_tracer._tracer.set_span_attribute(self.span_id, "llm.cost.total_cost", total_cost)

    async def add_event(self, name: str, **attributes) -> None:
        """Add a custom event to the trace."""
        event = SpanEvent(name=name)
        for key, value in attributes.items():
            event.with_attribute(key, value)
        await self._llm_tracer._tracer.add_span_event(self.span_id, event)

    async def set_attribute(self, key: str, value: Any) -> None:
        """Set a custom attribute on the trace."""
        await self._llm_tracer._tracer.set_span_attribute(self.span_id, key, value)
