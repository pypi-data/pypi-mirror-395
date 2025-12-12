"""Instrumentation for GraphBit components."""

import functools
from datetime import datetime
from typing import Any, Callable, Dict

from graphbit import Executor, LlmClient

from bitpulse.core.core import GraphBitTracer
from bitpulse.schemas.types import LlmRequest, LlmResponse, LlmTrace, SpanEvent, SpanKind, TokenUsage
from bitpulse.utils.logging_utils import setup_logging

logger = setup_logging()


class AutoInstrumentation:
    """Automatic instrumentation for GraphBit components."""

    def __init__(self, tracer: GraphBitTracer):
        """Initialize auto-instrumentation.

        Args:
            tracer: GraphBit tracer instance
        """
        self._tracer = tracer
        self._enabled = False
        self._original_methods: Dict[str, Any] = {}

    async def enable_llm_instrumentation(self) -> None:
        """Enable LLM provider instrumentation."""
        # Store original method
        if hasattr(LlmClient, "complete") and "LlmClient.complete" not in self._original_methods:
            self._original_methods["LlmClient.complete"] = LlmClient.complete

            # Wrap the complete method
            LlmClient.complete = self._instrument_llm_complete(LlmClient.complete)

            logger.info("LLM instrumentation enabled")

    def _instrument_llm_complete(self, original_method: Callable) -> Callable:
        """Instrument LLM complete method with comprehensive tracing."""

        @functools.wraps(original_method)
        async def wrapper(self, *args, **kwargs):
            # Extract request information
            messages = []
            temperature = None
            max_tokens = None
            tools = []
            tool_choice = None
            other_params = {}

            # Parse arguments to extract request details
            if args:
                request_arg = args[0]
                if hasattr(request_arg, "messages"):
                    messages = request_arg.messages
                elif isinstance(request_arg, str):
                    # Simple string prompt
                    messages = [{"role": "user", "content": request_arg}]
                elif isinstance(request_arg, list):
                    # List of messages
                    messages = request_arg

            # Extract additional parameters from kwargs
            temperature = kwargs.get("temperature")
            max_tokens = kwargs.get("max_tokens")
            tools = kwargs.get("tools", [])
            tool_choice = kwargs.get("tool_choice")

            # Collect other parameters
            for key, value in kwargs.items():
                if key not in ["temperature", "max_tokens", "tools", "tool_choice"]:
                    other_params[key] = value

            # Get provider and model info
            provider = getattr(self, "_provider", "unknown")
            model = getattr(self, "_model", "unknown")

            # Try to get model from config if available
            if hasattr(self, "_config"):
                config = self._config
                if hasattr(config, "model"):
                    model = config.model
                if hasattr(config, "provider"):
                    provider = config.provider

            span_name = f"llm.{provider}.complete"

            async with self._tracer.trace_span(span_name, SpanKind.CLIENT) as span_id:
                start_time = datetime.utcnow()

                # Create LLM request object
                llm_request = LlmRequest(
                    messages=messages,
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    tools=tools,
                    tool_choice=tool_choice,
                    other_params=other_params,
                )

                # Set comprehensive LLM attributes
                await self._tracer.set_span_attribute(span_id, "llm.provider", provider)
                await self._tracer.set_span_attribute(span_id, "llm.model", model)
                await self._tracer.set_span_attribute(span_id, "llm.request.message_count", len(messages))

                # Add request details
                if temperature is not None:
                    await self._tracer.set_span_attribute(span_id, "llm.request.temperature", temperature)
                if max_tokens is not None:
                    await self._tracer.set_span_attribute(span_id, "llm.request.max_tokens", max_tokens)
                if tools:
                    await self._tracer.set_span_attribute(span_id, "llm.request.tools_count", len(tools))

                # Add start event with request details
                start_event = SpanEvent(name="llm.request.start").with_attributes(
                    {"request.message_count": len(messages), "request.model": model, "request.provider": provider}
                )
                await self._tracer.add_span_event(span_id, start_event)

                try:
                    # Call original method
                    result = await original_method(self, *args, **kwargs)
                    end_time = datetime.utcnow()
                    duration_ms = (end_time - start_time).total_seconds() * 1000

                    # Extract comprehensive response information
                    content = ""
                    finish_reason = "unknown"
                    tool_calls = []
                    usage = None

                    if hasattr(result, "content"):
                        content = result.content
                        await self._tracer.set_span_attribute(span_id, "llm.response.content_length", len(content))

                    if hasattr(result, "finish_reason"):
                        finish_reason = result.finish_reason
                        await self._tracer.set_span_attribute(span_id, "llm.response.finish_reason", finish_reason)

                    if hasattr(result, "tool_calls"):
                        tool_calls = result.tool_calls or []
                        await self._tracer.set_span_attribute(span_id, "llm.response.tool_calls_count", len(tool_calls))

                    # Extract token usage if available
                    if hasattr(result, "usage") and result.usage:
                        usage_data = result.usage
                        prompt_tokens = getattr(usage_data, "prompt_tokens", 0)
                        completion_tokens = getattr(usage_data, "completion_tokens", 0)
                        total_tokens = getattr(usage_data, "total_tokens", prompt_tokens + completion_tokens)

                        usage = TokenUsage(
                            prompt_tokens=prompt_tokens, completion_tokens=completion_tokens, total_tokens=total_tokens
                        )

                        # Set token attributes
                        await self._tracer.set_span_attribute(span_id, "llm.usage.prompt_tokens", prompt_tokens)
                        await self._tracer.set_span_attribute(span_id, "llm.usage.completion_tokens", completion_tokens)
                        await self._tracer.set_span_attribute(span_id, "llm.usage.total_tokens", total_tokens)

                        # Record token metrics
                        await self._tracer.metrics.record_llm_tokens(provider, model, prompt_tokens, completion_tokens)

                    # Create LLM response object
                    llm_response = LlmResponse(
                        content=content,
                        finish_reason=finish_reason,
                        tool_calls=tool_calls,
                        usage=usage,
                        model=model,
                        other_data={},
                    )

                    # Record metrics
                    await self._tracer.metrics.record_llm_request(provider, model, duration_ms, success=True)

                    # Create and store comprehensive LLM trace
                    span = await self._tracer.get_span(span_id)
                    if span:
                        llm_trace = LlmTrace(
                            span=span,
                            provider=provider,
                            model=model,
                            request=llm_request,
                            response=llm_response,
                            usage=usage,
                            cost=None,
                            error=None,
                        )

                        # Store the LLM trace using the enhanced LLM tracer
                        await self._tracer.storage.store_llm_trace(llm_trace)

                        # Broadcast real-time update if dashboard is available
                        if hasattr(self._tracer, "_dashboard") and self._tracer._dashboard:
                            await self._tracer._dashboard.broadcast_llm_trace_update(llm_trace)

                    # Add completion event
                    completion_event = SpanEvent(name="llm.request.complete")
                    completion_event.with_attribute("response.content_length", len(content))
                    completion_event.with_attribute("response.finish_reason", finish_reason)
                    completion_event.with_attribute("duration_ms", duration_ms)
                    await self._tracer.add_span_event(span_id, completion_event)

                    return result

                except Exception as e:
                    end_time = datetime.utcnow()
                    duration_ms = (end_time - start_time).total_seconds() * 1000
                    error_message = str(e)

                    # Record error metrics
                    await self._tracer.metrics.record_llm_request(provider, model, duration_ms, success=False)

                    # Create error LLM trace
                    span = await self._tracer.get_span(span_id)
                    if span:
                        llm_trace = LlmTrace(
                            span=span,
                            provider=provider,
                            model=model,
                            request=llm_request,
                            response=None,
                            usage=None,
                            cost=None,
                            error=error_message,
                        )

                        # Store the error trace
                        await self._tracer.storage.store_llm_trace(llm_trace)

                        # Broadcast error update
                        if hasattr(self._tracer, "_dashboard") and self._tracer._dashboard:
                            await self._tracer._dashboard.broadcast_llm_trace_update(llm_trace)

                    # Add error event
                    error_event = SpanEvent(name="llm.request.error")
                    error_event.with_attribute("error.message", error_message)
                    error_event.with_attribute("error.type", type(e).__name__)
                    error_event.with_attribute("duration_ms", duration_ms)
                    await self._tracer.add_span_event(span_id, error_event)

                    raise

        return wrapper

    async def disable_all(self) -> None:
        """Disable all instrumentation and restore original methods."""
        if not self._enabled:
            return

        # Restore original methods
        for method_path, original_method in self._original_methods.items():
            if method_path == "LlmClient.complete":
                LlmClient.complete = original_method
            elif method_path == "Executor.execute":
                Executor.execute = original_method

        self._original_methods.clear()
        self._enabled = False

        logger.info("Auto-instrumentation disabled")
