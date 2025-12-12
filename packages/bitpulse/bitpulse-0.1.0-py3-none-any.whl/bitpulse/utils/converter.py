"""
GraphBit AutoTracer API Converter

Converts internal GraphBit Tracer spans to GraphBit Trace API format.
Token details (input_tokens, output_tokens, finish_reason, model_name) go in metadata field.

Environment Variables Required:
    BITPULSE_TRACING_API_KEY: API key for GraphBit tracing service (mandatory)
    BITPULSE_TRACEABLE_PROJECT: Project name for grouping traces (mandatory)
"""

from datetime import datetime
from typing import List, Optional

from bitpulse.schemas.base import TraceRecord
from bitpulse.schemas.types import TraceSpan
from bitpulse.utils.config import tracing_api_config
from bitpulse.utils.constants import FINISH_REASON_MAPPING


def convert_span_to_trace(
    span: TraceSpan, service_name: Optional[str] = None, environment: Optional[str] = None
) -> TraceRecord:
    """
    Convert a GraphBit TraceSpan to a GraphBit TraceRecord.

    Automatically reads tracing_api_key and traceable_project_name from environment variables:
    - BITPULSE_TRACING_API_KEY (required)
    - BITPULSE_TRACEABLE_PROJECT (required)

    Token details (input_tokens, output_tokens, finish_reason, model_name) are placed
    in the metadata field.

    Args:
        span: GraphBit TraceSpan object
        service_name: Optional service name
        environment: Optional environment (dev, staging, prod)

    Returns:
        TraceRecord object in GraphBit Trace API format

    Raises:
        TypeError: If span is None or not a TraceSpan
        ValueError: If required environment variables are not set
    """
    # Validate input
    if span is None:
        raise TypeError("span cannot be None")
    if not isinstance(span, TraceSpan):
        raise TypeError(f"span must be a TraceSpan, got {type(span).__name__}")

    # Get tracing_api_key and traceable_project_name from environment variables
    if tracing_api_config.tracing_api_key is None or tracing_api_config.traceable_project_name is None:
        # Environment variables not available - use placeholder values
        tracing_api_key, traceable_project_name = "not-configured", "not-configured"
    else:
        tracing_api_key = tracing_api_config.tracing_api_key
        traceable_project_name = tracing_api_config.traceable_project_name
    attrs = span.attributes

    # Extract basic info
    provider = attrs.get("llm.provider", "unknown")
    model = attrs.get("llm.model", "unknown")

    # Format timestamp
    start_time = span.start_time.isoformat() + "Z" if span.start_time else datetime.utcnow().isoformat() + "Z"

    # Determine status (LangSmith uses string status)
    status = "success" if span.status.value == "ok" else "error"

    # Extract error message
    error = None
    if status == "error":
        error = attrs.get("error.message", "An error occurred")

    # Extract token usage
    input_tokens = attrs.get("llm.usage.prompt_tokens")
    output_tokens = attrs.get("llm.usage.completion_tokens")
    total_tokens = attrs.get("llm.usage.total_tokens")

    # If total_tokens not provided, calculate it
    if total_tokens is None and input_tokens is not None and output_tokens is not None:
        total_tokens = input_tokens + output_tokens

    # Extract finish reason
    finish_reason_raw = attrs.get("llm.response.finish_reason")
    finish_reason = _simplify_finish_reason(finish_reason_raw) if finish_reason_raw else None

    # Extract duration (latency in LangSmith terms)
    latency = span.duration_ms

    # Extract request parameters
    temperature = attrs.get("llm.request.temperature")
    max_tokens = attrs.get("llm.request.max_tokens")

    # Build input/output - use actual prompt and response content
    input_data = attrs.get("llm.request.prompt")
    output_data = attrs.get("llm.response.content")

    # Build run_name - use human-readable name
    run_name = "LlmClient"

    # Build tags
    tags = [provider, model, status]
    if environment:
        tags.append(environment)

    # Build metadata - THIS IS WHERE TOKEN DETAILS GO (LangSmith convention)
    metadata = {
        "model_name": model,
        "provider": provider,
    }

    # Add token details to metadata
    if input_tokens is not None:
        metadata["input_tokens"] = input_tokens
    if output_tokens is not None:
        metadata["output_tokens"] = output_tokens
    if total_tokens is not None:
        metadata["total_tokens"] = total_tokens
    if finish_reason is not None:
        metadata["finish_reason"] = finish_reason

    # Add request parameters to metadata
    if temperature is not None:
        metadata["temperature"] = temperature
    if max_tokens is not None:
        metadata["max_tokens"] = max_tokens

    # Add tool call information to metadata if available
    tool_calls = attrs.get("llm.tool_calls")
    if tool_calls:
        metadata["tool_calls"] = tool_calls
        metadata["has_tool_calls"] = True
        metadata["tool_calls_count"] = len(tool_calls) if isinstance(tool_calls, list) else 0

    # Add service context to metadata
    if service_name:
        metadata["service_name"] = service_name
    if environment:
        metadata["environment"] = environment

    return TraceRecord(
        tracing_api_key=tracing_api_key,
        traceable_project_name=traceable_project_name,
        status=status,
        run_type="llm",
        run_name=run_name,
        input=input_data,
        output=output_data,
        error=error,
        start_time=start_time,
        latency=latency,
        tokens=total_tokens,  # Top-level tokens field
        cost=None,  # Not available from GraphBit
        first_token=None,  # Not available from GraphBit
        tags=tags,
        metadata=metadata,  # Token details go here!
        dataset=None,
        annotation_queue=None,
        reference_example=None,
    )


def convert_node_span_to_workflow_trace(
    span: TraceSpan, service_name: Optional[str] = None, environment: Optional[str] = None
) -> TraceRecord:
    """
    Convert a workflow node TraceSpan to a TraceRecord with run_type="workflow".

    This function converts individual LLM calls within a workflow to trace records.
    Each node gets its own separate trace record with its individual metrics.

    Args:
        span: GraphBit TraceSpan object (node-level within a workflow)
        service_name: Optional service name
        environment: Optional environment (dev, staging, prod)

    Returns:
        TraceRecord object in GraphBit Trace API format

    Raises:
        TypeError: If span is None or not a TraceSpan
        ValueError: If required environment variables are not set
    """
    # Validate input
    if span is None:
        raise TypeError("span cannot be None")
    if not isinstance(span, TraceSpan):
        raise TypeError(f"span must be a TraceSpan, got {type(span).__name__}")

    # Get tracing_api_key and traceable_project_name from environment variables
    if tracing_api_config.tracing_api_key is None or tracing_api_config.traceable_project_name is None:
        # Environment variables not available - use placeholder values
        tracing_api_key, traceable_project_name = "not-configured", "not-configured"
    else:
        tracing_api_key = tracing_api_config.tracing_api_key
        traceable_project_name = tracing_api_config.traceable_project_name
    attrs = span.attributes

    # Extract basic info
    provider = attrs.get("llm.provider", "unknown")
    model = attrs.get("llm.model", "unknown")
    node_name = attrs.get("node.name", span.name)

    # Format timestamp
    start_time = span.start_time.isoformat() + "Z" if span.start_time else datetime.utcnow().isoformat() + "Z"

    # Determine status
    status = "success" if span.status.value == "ok" else "error"

    # Extract error message
    error = None
    if status == "error":
        error = attrs.get("error.message", "An error occurred")

    # Extract token usage
    input_tokens = attrs.get("llm.usage.prompt_tokens")
    output_tokens = attrs.get("llm.usage.completion_tokens")
    total_tokens = attrs.get("llm.usage.total_tokens")

    # If total_tokens not provided, calculate it
    if total_tokens is None and input_tokens is not None and output_tokens is not None:
        total_tokens = input_tokens + output_tokens

    # Extract finish reason
    finish_reason_raw = attrs.get("llm.finish_reason")
    finish_reason = _simplify_finish_reason(finish_reason_raw) if finish_reason_raw else None

    # Prefer actual LLM call duration from GraphBit core over span creation overhead
    latency = attrs.get("llm.request.duration_ms")
    if latency is None:
        # Fallback to span duration if actual LLM duration not available
        latency = span.duration_ms

    # Extract the actual prompt from the span attributes
    input_data = attrs.get("llm.request.prompt")
    output_data = attrs.get("llm.response.content")

    # Build run_name - use "Workflow" for API validation
    run_name = "Workflow"

    # Build tags
    tags = ["workflow", provider, model, status]
    if environment:
        tags.append(environment)

    # Build metadata - include node name and LLM details
    metadata = {
        "node_name": node_name,
        "model_name": model,
        "provider": provider,
        "is_workflow_node": True,
    }

    # Add token details to metadata
    if input_tokens is not None:
        metadata["input_tokens"] = input_tokens
    if output_tokens is not None:
        metadata["output_tokens"] = output_tokens
    if total_tokens is not None:
        metadata["total_tokens"] = total_tokens
    if finish_reason is not None:
        metadata["finish_reason"] = finish_reason

    # Add tool call information to metadata if available
    tool_calls = attrs.get("llm.tool_calls")
    if tool_calls:
        metadata["tool_calls"] = tool_calls
        metadata["has_tool_calls"] = True
        metadata["tool_calls_count"] = len(tool_calls) if isinstance(tool_calls, list) else 0

    # Add service context to metadata
    if service_name:
        metadata["service_name"] = service_name
    if environment:
        metadata["environment"] = environment

    return TraceRecord(
        tracing_api_key=tracing_api_key,
        traceable_project_name=traceable_project_name,
        status=status,
        run_type="chain",  # Individual workflow nodes use run_type="chain"
        run_name=run_name,
        input=input_data,
        output=output_data,
        error=error,
        start_time=start_time,
        latency=latency,
        tokens=total_tokens,
        cost=None,
        first_token=None,
        tags=tags,
        metadata=metadata,
        dataset=None,
        annotation_queue=None,
        reference_example=None,
    )


def convert_spans_to_records(
    spans: List[TraceSpan],
    service_name: Optional[str] = None,
    environment: Optional[str] = None,
    include_workflows: bool = True,
) -> List[TraceRecord]:
    """
    Convert a list of GraphBit TraceSpans to a list of TraceRecords.

    For workflows: Each individual node within a workflow is sent as a separate trace record
    with run_type="workflow". Workflow container spans are NOT sent.

    Automatically reads tracing_api_key and traceable_project from environment variables:
    - BITPULSE_TRACING_API_KEY (required)
    - BITPULSE_TRACEABLE_PROJECT (required)

    Args:
        spans: List of GraphBit TraceSpan objects
        service_name: Service name
        environment: Environment (dev, staging, prod)
        include_workflows: Whether to include workflow node spans (default: True)

    Returns:
        List of TraceRecord objects in GraphBit Trace API format (ordered by execution time)

    Raises:
        TypeError: If spans is None or not a list of TraceSpans
        ValueError: If required environment variables are not set
    """
    # Validate input
    if spans is None:
        raise TypeError("spans cannot be None")
    if not isinstance(spans, list):
        raise TypeError(f"spans must be a list, got {type(spans).__name__}")
    if spans and not all(isinstance(span, TraceSpan) for span in spans):
        raise TypeError("All items in spans must be TraceSpan instances")

    if not isinstance(include_workflows, bool):
        raise TypeError(f"include_workflows must be a boolean, got {type(include_workflows).__name__}")

    records = []

    for span in spans:
        # Check span type
        is_workflow_node = "node.name" in span.attributes and "llm.provider" in span.attributes
        is_standalone_llm = "llm.provider" in span.attributes and "node.name" not in span.attributes

        if is_workflow_node and include_workflows:
            # This is a node within a workflow - send as individual workflow trace
            records.append(convert_node_span_to_workflow_trace(span, service_name, environment))
        elif is_standalone_llm:
            # This is a standalone LLM call (not part of a workflow)
            records.append(convert_span_to_trace(span, service_name, environment))

    return records


def convert_spans_to_records_safe(
    spans: List[TraceSpan],
    service_name: Optional[str] = None,
    environment: Optional[str] = None,
    include_workflows: bool = True,
) -> List[TraceRecord] | None:
    """
    Safely convert a list of GraphBit TraceSpans to a list of TraceRecords.

    This is a safe version that returns None if environment variables are missing,
    instead of raising exceptions.

    Args:
        spans: List of GraphBit TraceSpan objects
        service_name: Service name
        environment: Environment (dev, staging, prod)
        include_workflows: Whether to include workflow node spans (default: True)

    Returns:
        List of TraceRecord objects if environment variables are available, None otherwise
    """
    # Check if environment variables are available
    if tracing_api_config.tracing_api_key is None or tracing_api_config.traceable_project_name is None:
        # Environment variables not available - return None silently
        return None

    try:
        # Use the regular conversion function
        return convert_spans_to_records(spans, service_name, environment, include_workflows)
    except (ValueError, TypeError):
        # Any conversion errors - return None silently
        return None


def _simplify_finish_reason(reason_str: str) -> str:
    """
    Simplify finish reason to a standardized string.

    Args:
        reason_str: The finish reason string to simplify

    Returns:
        Simplified finish reason string
    """
    if not reason_str:
        return "unknown"

    reason_lower = str(reason_str).lower()

    # Check each key in the mapping dictionary
    for key, value in FINISH_REASON_MAPPING.items():
        if key in reason_lower:
            return value

    return "other"
