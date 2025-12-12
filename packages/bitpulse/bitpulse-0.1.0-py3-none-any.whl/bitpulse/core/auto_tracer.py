"""
GraphBit Auto Tracer - Zero-Configuration Automatic Instrumentation

This module provides a user-friendly wrapper that automatically extracts ALL metadata
from GraphBit framework responses without requiring manual configuration.

Usage:
    from graphbit_tracer.auto_tracer import AutoTracer

    # Initialize with minimal configuration
    tracer = await AutoTracer.create()

    # Wrap your LLM client
    traced_client = tracer.wrap_client(llm_client)

    # Make LLM calls - they're automatically traced!
    response = await traced_client.complete_full_async(prompt)

    # Export traces
    await tracer.export()
"""

import re
from datetime import datetime
from typing import Any, Dict, List, Optional

# GraphBit is a required dependency
from graphbit import Executor, LlmClient, LlmConfig, Workflow

from bitpulse.api.client import TracingApiClient
from bitpulse.core.core import GraphBitTracer
from bitpulse.instrumentation.base import AutoInstrumentation
from bitpulse.schemas.types import SpanKind
from bitpulse.utils.config import ExportConfig, StorageConfig, TracerConfig
from bitpulse.utils.converter import convert_spans_to_records_safe
from bitpulse.utils.logging_utils import setup_logging

logger = setup_logging()


class TracedLlmClient:
    """
    Wrapper for GraphBit LlmClient that automatically traces all LLM calls.

    This wrapper intercepts LLM calls and automatically extracts all metadata
    from GraphBit LlmResponse objects.
    """

    def __init__(self, client: LlmClient, tracer: GraphBitTracer, config: LlmConfig):
        """
        Initialize TracedLlmClient.

        Args:
            client: GraphBit LlmClient instance
            tracer: GraphBitTracer instance
            config: GraphBit LlmConfig instance
        """
        self._client = client
        self._tracer = tracer
        self._config = config
        self._provider = config.provider()
        self._model = config.model()

    async def complete_full_async(
        self, prompt: str, max_tokens: Optional[int] = None, temperature: Optional[float] = None
    ) -> Any:
        """
        Complete with full response object (asynchronous) - automatically traced.

        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature

        Returns:
            GraphBit LlmResponse object
        """
        # Start span for this LLM call
        span_name = f"llm.{self._provider}.complete"
        span_id = await self._tracer.start_span(span_name, SpanKind.CLIENT)

        start_time = datetime.now()

        try:
            # Set request attributes
            await self._tracer.set_span_attribute(span_id, "llm.provider", self._provider)
            await self._tracer.set_span_attribute(span_id, "llm.model", self._model)
            await self._tracer.set_span_attribute(span_id, "llm.request.prompt_length", len(prompt))

            # Store the actual prompt content
            await self._tracer.set_span_attribute(span_id, "llm.request.prompt", prompt)

            if max_tokens is not None:
                await self._tracer.set_span_attribute(span_id, "llm.request.max_tokens", max_tokens)
            if temperature is not None:
                await self._tracer.set_span_attribute(span_id, "llm.request.temperature", temperature)

            # Make the actual LLM call
            response = await self._client.complete_full_async(
                prompt=prompt, max_tokens=max_tokens, temperature=temperature
            )

            # Calculate duration
            end_time = datetime.now()
            duration_ms = (end_time - start_time).total_seconds() * 1000

            # Extract ALL metadata from GraphBit LlmResponse
            await self._tracer.set_span_attribute(span_id, "llm.response.model", response.model)
            await self._tracer.set_span_attribute(span_id, "llm.response.content_length", len(response.content))
            await self._tracer.set_span_attribute(span_id, "llm.response.finish_reason", str(response.finish_reason))

            # Store the actual response content
            await self._tracer.set_span_attribute(span_id, "llm.response.content", response.content)

            if response.id:
                await self._tracer.set_span_attribute(span_id, "llm.response.id", response.id)

            # Extract token usage
            usage = response.usage
            await self._tracer.set_span_attribute(span_id, "llm.usage.prompt_tokens", usage.prompt_tokens)
            await self._tracer.set_span_attribute(span_id, "llm.usage.completion_tokens", usage.completion_tokens)
            await self._tracer.set_span_attribute(span_id, "llm.usage.total_tokens", usage.total_tokens)

            # Extract tool calls if present\
            if response.has_tool_calls():
                tool_calls = response.tool_calls
                await self._tracer.set_span_attribute(span_id, "llm.response.tool_calls_count", len(tool_calls))

            # Add timing
            await self._tracer.set_span_attribute(span_id, "llm.request.duration_ms", duration_ms)

            # Finish span successfully
            await self._tracer.finish_span(span_id)

            return response

        except Exception as e:
            # Finish span with error
            await self._tracer.finish_span_with_error(span_id, str(e), type(e).__name__)
            raise

    def __getattr__(self, name: str) -> Any:
        """Forward all other attributes to the wrapped client."""
        return getattr(self._client, name)


class AutoTracer:
    """
    User-friendly wrapper for GraphBit Tracer with automatic metadata extraction.

    This class provides zero-configuration automatic instrumentation that extracts
    ALL metadata from GraphBit framework responses without manual field mapping.
    """

    def __init__(self, tracer: GraphBitTracer, auto_instr: AutoInstrumentation):
        """Initialize AutoTracer (use create() instead)."""
        self.tracer = tracer
        self.auto_instr = auto_instr
        self._initialized = False
        self._export_dir = "traces"

    @classmethod
    async def create(cls, export_dir: str = "traces", service_name: str = "graphbit-service") -> "AutoTracer":
        """
        Create and initialize AutoTracer with automatic instrumentation.

        Args:
            export_dir: Directory for exporting trace data (default: "traces")
            service_name: Service name for trace identification (default: "graphbit-service")

        Returns:
            Initialized AutoTracer instance

        Example:
            tracer = await AutoTracer.create(export_dir="my_traces")
        """
        # Create tracer configuration with proper structure
        config = TracerConfig(
            service_name=service_name,
            storage=StorageConfig(type="memory"),
            export=ExportConfig(enabled=True, traces_path=export_dir),
        )

        # Initialize tracer
        tracer = await GraphBitTracer.init(config)

        # Enable automatic instrumentation
        auto_instr = AutoInstrumentation(tracer)
        await auto_instr.enable_llm_instrumentation()

        instance = cls(tracer, auto_instr)
        instance._initialized = True
        instance._export_dir = export_dir

        return instance

    def wrap_client(self, client: LlmClient, config: LlmConfig) -> TracedLlmClient:
        """
        Wrap a GraphBit LlmClient to automatically trace all LLM calls.

        Args:
            client: GraphBit LlmClient instance
            config: GraphBit LlmConfig instance

        Returns:
            TracedLlmClient that automatically captures all LLM metadata

        Raises:
            TypeError: If client is not an LlmClient or config is not an LlmConfig

        Example:
            from graphbit import LlmClient, LlmConfig

            llm_config = LlmConfig.openai(api_key="key", model="gpt-4")
            llm_client = LlmClient(llm_config)
            traced_client = tracer.wrap_client(llm_client, llm_config)

            # Now all calls are automatically traced!
            response = await traced_client.complete_full_async("Hello!")
        """
        # Validate inputs
        if client is None:
            raise TypeError("client cannot be None")
        if not isinstance(client, LlmClient):
            raise TypeError(f"client must be an LlmClient, got {type(client).__name__}")

        if config is None:
            raise TypeError("config cannot be None")
        if not isinstance(config, LlmConfig):
            raise TypeError(f"config must be an LlmConfig, got {type(config).__name__}")

        return TracedLlmClient(client, self.tracer, config)

    def wrap_executor(
        self, executor: Executor, llm_config: LlmConfig, node_llm_configs: Optional[Dict[str, LlmConfig]] = None
    ) -> "TracedExecutor":
        """
        Wrap a GraphBit Executor to enable automatic workflow tracing.

        Args:
            executor: GraphBit Executor instance
            llm_config: LLM configuration used by the executor
            node_llm_configs: Optional dict mapping node names to their specific LlmConfig for multi-provider workflows

        Returns:
            TracedExecutor that automatically traces workflow executions

        Raises:
            TypeError: If executor is not an Executor or llm_config is not an LlmConfig

        Example:
            from graphbit import Executor, Workflow, Node, LlmConfig

            llm_config = LlmConfig.openai(api_key="key", model="gpt-4o-mini")
            executor = Executor(llm_config)
            traced_executor = tracer.wrap_executor(executor, llm_config)

            # Execute workflow - automatically traced!
            result = traced_executor.execute(workflow)

        Example with multiple LLM providers:
            llm_config_openai = LlmConfig.openai(api_key="key", model="gpt-4o-mini")
            llm_config_anthropic = LlmConfig.anthropic(api_key="key", model="claude-3-sonnet")
            executor = Executor(llm_config_openai)

            node_configs = {
                "Review Agent": llm_config_anthropic,
                "Formatter": llm_config_openai,
            }
            traced_executor = tracer.wrap_executor(executor, llm_config_openai, node_llm_configs=node_configs)
        """
        # Validate inputs
        if executor is None:
            raise TypeError("executor cannot be None")
        if not isinstance(executor, Executor):
            raise TypeError(f"executor must be an Executor, got {type(executor).__name__}")

        if llm_config is None:
            raise TypeError("llm_config cannot be None")
        if not isinstance(llm_config, LlmConfig):
            raise TypeError(f"llm_config must be an LlmConfig, got {type(llm_config).__name__}")

        # Validate node_llm_configs if provided
        if node_llm_configs is not None:
            if not isinstance(node_llm_configs, dict):
                raise TypeError(f"node_llm_configs must be a dict, got {type(node_llm_configs).__name__}")
            for node_name, node_config in node_llm_configs.items():
                if not isinstance(node_name, str):
                    raise TypeError(f"node_llm_configs keys must be strings, got {type(node_name).__name__}")
                if not isinstance(node_config, LlmConfig):
                    raise TypeError(
                        f"node_llm_configs values must be LlmConfig instances, "
                        f"got {type(node_config).__name__} for node '{node_name}'"
                    )

        return TracedExecutor(executor, self.tracer, llm_config, node_llm_configs=node_llm_configs)

    async def get_spans(self) -> List[Any]:
        """
        Get all captured trace spans (public API).

        This is the public API for retrieving spans. Use this instead of _get_all_spans().

        Returns:
            List of TraceSpan objects

        Example:
            spans = await tracer.get_spans()
            for span in spans:
                logger.info(f"Span: {span.name}, Duration: {span.duration_ms}ms")
        """
        return await self._get_all_spans()

    async def send(self, auto_submit: bool = True, auto_shutdown: bool = True) -> Dict[str, Any]:
        """
        Send all collected traces to the remote API endpoint.

        This is a convenience method that combines span retrieval, conversion, and API submission.
        Simplifies the common pattern of tracing, converting, and sending traces.

        Args:
            auto_submit: If True, automatically submit traces to API (default: True)
            auto_shutdown: If True, automatically shutdown tracer after sending (default: False)

        Returns:
            Dictionary with submission results: {'sent': int, 'failed': int}
            Returns {'sent': 0, 'failed': 0} if API keys are not configured

        Never raises exceptions - gracefully handles missing API keys and configuration issues.

        Example:
            tracer = await AutoTracer.create()
            traced_client = tracer.wrap_client(llm_client, llm_config)
            await traced_client.complete_full_async("Hello!")
            results = await tracer.send(auto_shutdown=True)
            logger.info(f"Sent: {results['sent']}, Failed: {results['failed']}")
        """
        if not auto_submit:
            return {"sent": 0, "failed": 0}

        # Get spans and convert to records safely
        spans = await self.get_spans()
        if not spans:
            if auto_shutdown:
                await self.shutdown()
            return {"sent": 0, "failed": 0}

        # Use safe conversion that returns None if API keys are missing
        trace_records = convert_spans_to_records_safe(spans)
        if trace_records is None:
            # API keys not configured - return silently without error
            if auto_shutdown:
                await self.shutdown()
            return {"sent": 0, "failed": 0}

        try:
            # Send to API
            api_client = TracingApiClient()
            results = await api_client.send_trace_records(trace_records)

            # Shutdown if requested
            if auto_shutdown:
                await self.shutdown()

            return results
        except Exception:
            # Network or API errors - return silently without raising
            if auto_shutdown:
                await self.shutdown()
            return {"sent": 0, "failed": 0}

    async def shutdown(self):
        """
        Shutdown the tracer and disable instrumentation.

        Example:
            await tracer.shutdown()
        """
        if self._initialized:
            await self.auto_instr.disable_all()
            await self.tracer.shutdown()
            self._initialized = False

    async def _get_all_spans(self) -> List[Any]:
        """Get all spans from storage."""
        # Access storage directly
        if hasattr(self.tracer, "_storage"):
            if hasattr(self.tracer._storage, "_spans"):
                return list(self.tracer._storage._spans.values())
        return []

    def __enter__(self):
        """Context manager support (sync - not recommended)."""
        raise NotImplementedError("Use 'async with' instead of 'with'")

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.shutdown()
        return False


class TracedExecutor:
    """
    Wrapper for GraphBit Executor that automatically traces workflow executions.

    This wrapper intercepts workflow execution and creates trace spans for each
    node execution, capturing LLM calls, timing, and results.
    """

    def __init__(
        self,
        executor: "Executor",
        tracer: GraphBitTracer,
        llm_config: LlmConfig,
        node_llm_configs: Optional[Dict[str, LlmConfig]] = None,
    ):
        """
        Initialize TracedExecutor.

        Args:
            executor: GraphBit Executor instance
            tracer: GraphBitTracer instance
            llm_config: LLM configuration used by the executor
            node_llm_configs: Optional dict mapping node names to their specific LlmConfig
        """
        self._executor = executor
        self._tracer = tracer
        self._llm_config = llm_config
        self._provider = llm_config.provider()
        self._model = llm_config.model()
        self._node_llm_configs = node_llm_configs or {}

    async def execute(self, workflow: "Workflow") -> Any:
        """
        Execute workflow and automatically trace all node executions.

        Args:
            workflow: GraphBit Workflow to execute

        Returns:
            WorkflowResult from the executor
        """
        # Record start time BEFORE creating span
        start_time = datetime.utcnow()

        # Create a workflow-level span
        workflow_span_id = await self._tracer.start_span(f"workflow.{workflow.name()}", SpanKind.INTERNAL)

        # Override the span's start_time to match actual workflow start
        span = self._tracer._active_spans.get(workflow_span_id)
        if span:
            span.start_time = start_time

        end_time = None
        try:
            # Execute the workflow (synchronous call)
            result = self._executor.execute(workflow)

            # Record end time immediately after execution
            end_time = datetime.utcnow()
            latency_ms = (end_time - start_time).total_seconds() * 1000

            # Set workflow-level attributes
            await self._tracer.set_span_attribute(workflow_span_id, "workflow.name", workflow.name())
            await self._tracer.set_span_attribute(workflow_span_id, "workflow.latency_ms", latency_ms)

            # Check if workflow succeeded
            if result.is_success():
                await self._tracer.set_span_attribute(workflow_span_id, "workflow.status", "success")

                # Create spans for each node execution with complete LLM metadata
                try:
                    node_outputs = result.get_all_node_outputs()

                    # Get all LLM response metadata (NEW: captures tokens, cost, finish_reason, etc.)
                    node_metadata = {}
                    try:
                        node_metadata = result.get_all_node_response_metadata()
                    except Exception as e:
                        # Fallback for older GraphBit versions without metadata support
                        logger.debug("Metadata extraction failed, using fallback", error=str(e), exc_info=True)
                        node_metadata = {}

                    if node_outputs and isinstance(node_outputs, dict):
                        uuid_pattern = re.compile(
                            r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.IGNORECASE
                        )

                        # Separate node names from node IDs
                        node_names = {}
                        node_ids = {}
                        for key, output in node_outputs.items():
                            if uuid_pattern.match(key):
                                node_ids[key] = output
                            else:
                                node_names[key] = output

                        # Prefer node names over node IDs for tracing
                        # If we have both, use names; if only IDs, use those
                        nodes_to_trace = node_names if node_names else node_ids

                        # Sort nodes by execution timestamp to preserve chronological order
                        # GraphBit stores execution_timestamp in metadata for each node
                        def get_execution_timestamp(node_name):
                            if node_name in node_metadata:
                                metadata = node_metadata[node_name]
                                return metadata.get("execution_timestamp", "")
                            return ""

                        # Sort nodes by execution timestamp (chronological order)
                        sorted_nodes = sorted(nodes_to_trace.items(), key=lambda x: get_execution_timestamp(x[0]))

                        for node_name, node_output in sorted_nodes:
                            if node_output:
                                node_span_id = await self._tracer.start_span(
                                    f"workflow.node.{node_name}", SpanKind.CLIENT, parent_span_id=workflow_span_id
                                )

                                # Determine which LLM config this node uses
                                node_provider = self._provider
                                node_model = self._model
                                if node_name in self._node_llm_configs:
                                    node_config = self._node_llm_configs[node_name]
                                    node_provider = node_config.provider()
                                    node_model = node_config.model()

                                # Set basic node attributes
                                await self._tracer.set_span_attribute(node_span_id, "node.name", node_name)
                                await self._tracer.set_span_attribute(node_span_id, "llm.provider", node_provider)
                                await self._tracer.set_span_attribute(node_span_id, "llm.model", node_model)
                                await self._tracer.set_span_attribute(
                                    node_span_id, "llm.response.content", str(node_output)
                                )
                                await self._tracer.set_span_attribute(
                                    node_span_id, "llm.response.content_length", len(str(node_output))
                                )

                                # Mark that this span's timing is not accurate
                                await self._tracer.set_span_attribute(node_span_id, "timing.accurate", False)
                                await self._tracer.set_span_attribute(
                                    node_span_id,
                                    "timing.note",
                                    "Span created after execution; timing reflects span creation overhead only",
                                )

                                # Set complete LLM metadata if available (NEW!)
                                if node_name in node_metadata:
                                    metadata = node_metadata[node_name]

                                    # Request prompt (NEW: now available from GraphBit core)
                                    if "prompt" in metadata:
                                        await self._tracer.set_span_attribute(
                                            node_span_id, "llm.request.prompt", metadata["prompt"]
                                        )

                                    # Actual LLM call duration (NEW: for accurate latency tracking)
                                    if "duration_ms" in metadata:
                                        await self._tracer.set_span_attribute(
                                            node_span_id, "llm.request.duration_ms", metadata["duration_ms"]
                                        )
                                        # Mark timing as accurate since we have the actual LLM duration
                                        await self._tracer.set_span_attribute(node_span_id, "timing.accurate", True)
                                        await self._tracer.set_span_attribute(
                                            node_span_id, "timing.note", "Actual LLM call duration from GraphBit core"
                                        )

                                    # Token usage
                                    if "usage" in metadata:
                                        usage = metadata["usage"]
                                        if "prompt_tokens" in usage:
                                            await self._tracer.set_span_attribute(
                                                node_span_id, "llm.usage.prompt_tokens", usage["prompt_tokens"]
                                            )
                                        if "completion_tokens" in usage:
                                            await self._tracer.set_span_attribute(
                                                node_span_id, "llm.usage.completion_tokens", usage["completion_tokens"]
                                            )
                                        if "total_tokens" in usage:
                                            await self._tracer.set_span_attribute(
                                                node_span_id, "llm.usage.total_tokens", usage["total_tokens"]
                                            )

                                    # Finish reason
                                    if "finish_reason" in metadata:
                                        await self._tracer.set_span_attribute(
                                            node_span_id, "llm.finish_reason", metadata["finish_reason"]
                                        )

                                    # Response ID
                                    if "id" in metadata:
                                        await self._tracer.set_span_attribute(
                                            node_span_id, "llm.response.id", metadata["id"]
                                        )

                                    # Tool calls - store complete information for observability
                                    if "tool_calls" in metadata and metadata["tool_calls"]:
                                        tool_calls = metadata["tool_calls"]
                                        await self._tracer.set_span_attribute(node_span_id, "llm.has_tool_calls", True)
                                        await self._tracer.set_span_attribute(
                                            node_span_id, "llm.tool_calls_count", len(tool_calls)
                                        )
                                        # Store the complete tool calls data as JSON for API export
                                        await self._tracer.set_span_attribute(
                                            node_span_id, "llm.tool_calls", tool_calls
                                        )

                                # Finish the node span
                                await self._tracer.finish_span(node_span_id)
                except Exception as e:
                    # Log but don't fail if node tracing fails
                    logger.warning("Failed to trace node execution", error=str(e), exc_info=True)
            else:
                await self._tracer.set_span_attribute(workflow_span_id, "workflow.status", "failed")
                if hasattr(result, "error") and result.error():
                    await self._tracer.set_span_attribute(workflow_span_id, "workflow.error", str(result.error()))

            # Override the span's end_time to match actual workflow end
            span = self._tracer._active_spans.get(workflow_span_id)
            if span and end_time:
                span.end_time = end_time

            # Finish the workflow span (this will use the overridden end_time)
            await self._tracer.finish_span(workflow_span_id)

            return result

        except Exception as e:
            # Record end time for error case
            if end_time is None:
                end_time = datetime.utcnow()

            # Override the span's end_time to match actual workflow end
            span = self._tracer._active_spans.get(workflow_span_id)
            if span:
                span.end_time = end_time

            # Record error and finish span with error
            await self._tracer.set_span_attribute(workflow_span_id, "workflow.status", "error")
            await self._tracer.set_span_attribute(workflow_span_id, "workflow.error", str(e))
            await self._tracer.finish_span_with_error(workflow_span_id, str(e))
            raise
