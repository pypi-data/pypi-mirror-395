"""Core type definitions for BitPulse."""

import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field

# Type aliases for better readability
TraceId = str
SpanId = str


class SpanKind(str, Enum):
    """Span kind enumeration following OpenTelemetry conventions."""

    INTERNAL = "internal"
    CLIENT = "client"
    SERVER = "server"
    PRODUCER = "producer"
    CONSUMER = "consumer"


class SpanStatus(str, Enum):
    """Span status enumeration."""

    OK = "ok"
    ERROR = "error"
    CANCELLED = "cancelled"


class SpanEvent(BaseModel):
    """Represents an event within a span."""

    name: str = Field(..., description="Event name")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Event timestamp")
    attributes: Dict[str, Any] = Field(default_factory=dict, description="Event attributes")

    def with_attribute(self, key: str, value: Any) -> "SpanEvent":
        """Add an attribute to the event.

        Args:
            key: Attribute key
            value: Attribute value

        Returns:
            Self for method chaining
        """
        self.attributes[key] = value
        return self


class TraceSpan(BaseModel):
    """Represents a trace span with all its metadata."""

    trace_id: TraceId = Field(..., description="Unique trace identifier")
    span_id: SpanId = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique span identifier")
    parent_span_id: Optional[SpanId] = Field(None, description="Parent span identifier")
    name: str = Field(..., description="Span name")
    kind: SpanKind = Field(SpanKind.INTERNAL, description="Span kind")
    start_time: datetime = Field(default_factory=datetime.utcnow, description="Span start time")
    end_time: Optional[datetime] = Field(None, description="Span end time")
    status: SpanStatus = Field(SpanStatus.OK, description="Span status")
    attributes: Dict[str, Any] = Field(default_factory=dict, description="Span attributes")
    events: List[SpanEvent] = Field(default_factory=list, description="Span events")
    resource: Dict[str, Any] = Field(default_factory=dict, description="Resource attributes")

    @property
    def duration_ms(self) -> Optional[float]:
        """Calculate span duration in milliseconds."""
        if self.end_time is None:
            return None
        return (self.end_time - self.start_time).total_seconds() * 1000

    def add_event(self, event: SpanEvent) -> None:
        """Add an event to the span."""
        self.events.append(event)

    def set_attribute(self, key: str, value: Any) -> None:
        """Set a span attribute."""
        self.attributes[key] = value


class TokenUsage(BaseModel):
    """Token usage information for LLM calls."""

    prompt_tokens: int = Field(..., description="Number of tokens in the prompt")
    completion_tokens: int = Field(..., description="Number of tokens in the completion")
    total_tokens: int = Field(..., description="Total number of tokens")

    @classmethod
    def from_graphbit(cls, graphbit_usage: Any) -> "TokenUsage":
        """Create TokenUsage from GraphBit LlmUsage object.

        Args:
            graphbit_usage: GraphBit LlmUsage object

        Returns:
            TokenUsage instance
        """
        return cls(
            prompt_tokens=graphbit_usage.prompt_tokens,
            completion_tokens=graphbit_usage.completion_tokens,
            total_tokens=graphbit_usage.total_tokens,
        )


class CostInfo(BaseModel):
    """Cost information for LLM calls."""

    prompt_cost: float = Field(..., description="Cost for prompt tokens")
    completion_cost: float = Field(..., description="Cost for completion tokens")
    total_cost: float = Field(..., description="Total cost")
    currency: str = Field("USD", description="Currency code")


class LlmRequest(BaseModel):
    """LLM request information."""

    messages: List[Dict[str, Any]] = Field(..., description="Request messages")
    model: str = Field(..., description="Model name")
    temperature: Optional[float] = Field(None, description="Temperature parameter")
    max_tokens: Optional[int] = Field(None, description="Maximum tokens to generate")
    tools: List[Dict[str, Any]] = Field(default_factory=list, description="Available tools")
    tool_choice: Optional[Union[str, Dict[str, Any]]] = Field(None, description="Tool choice")
    other_params: Dict[str, Any] = Field(default_factory=dict, description="Other parameters")


class LlmResponse(BaseModel):
    """LLM response information."""

    content: str = Field(..., description="Response content")
    finish_reason: str = Field(..., description="Reason for completion")
    tool_calls: List[Dict[str, Any]] = Field(default_factory=list, description="Tool calls made")
    usage: Optional[TokenUsage] = Field(None, description="Token usage information")
    model: str = Field(..., description="Model used for response")
    other_data: Dict[str, Any] = Field(default_factory=dict, description="Other response data")

    @classmethod
    def from_graphbit(cls, graphbit_response: Any) -> "LlmResponse":
        """Create LlmResponse from GraphBit LlmResponse object.

        Args:
            graphbit_response: GraphBit LlmResponse object

        Returns:
            LlmResponse instance
        """
        # Convert tool calls
        tool_calls = []
        for tool_call in graphbit_response.tool_calls:
            tool_calls.append({"id": tool_call.id, "name": tool_call.name, "parameters": tool_call.parameters})

        # Convert usage if available
        usage = None
        if hasattr(graphbit_response, "usage") and graphbit_response.usage:
            usage = TokenUsage.from_graphbit(graphbit_response.usage)

        # Convert metadata
        other_data = {}
        if hasattr(graphbit_response, "metadata"):
            metadata_dict = graphbit_response.metadata
            if hasattr(metadata_dict, "items"):  # Dict-like object
                other_data = dict(metadata_dict.items())
            elif isinstance(metadata_dict, dict):
                other_data = metadata_dict.copy()

        return cls(
            content=graphbit_response.content,
            finish_reason=str(graphbit_response.finish_reason),
            tool_calls=tool_calls,
            usage=usage,
            model=graphbit_response.model,
            other_data=other_data,
        )


class LlmTrace(BaseModel):
    """Complete LLM trace information."""

    span: TraceSpan = Field(..., description="Associated span")
    provider: str = Field(..., description="LLM provider name")
    model: str = Field(..., description="Model name")
    request: LlmRequest = Field(..., description="Request information")
    response: Optional[LlmResponse] = Field(None, description="Response information")
    usage: Optional[TokenUsage] = Field(None, description="Token usage")
    cost: Optional[CostInfo] = Field(None, description="Cost information")
    error: Optional[str] = Field(None, description="Error message if failed")


class NodeTrace(BaseModel):
    """Trace information for a workflow node."""

    span: TraceSpan = Field(..., description="Associated span")
    node_id: str = Field(..., description="Node identifier")
    node_name: str = Field(..., description="Node name")
    node_type: str = Field(..., description="Node type (agent, transform, condition, etc.)")
    input_data: Dict[str, Any] = Field(default_factory=dict, description="Node input data")
    output_data: Optional[Dict[str, Any]] = Field(None, description="Node output data")
    error: Optional[str] = Field(None, description="Error message if failed")


class WorkflowTrace(BaseModel):
    """Complete workflow trace information."""

    span: TraceSpan = Field(..., description="Associated span")
    workflow_id: str = Field(..., description="Workflow identifier")
    workflow_name: str = Field(..., description="Workflow name")
    node_traces: List[NodeTrace] = Field(default_factory=list, description="Node traces")
    input_data: Dict[str, Any] = Field(default_factory=dict, description="Workflow input")
    output_data: Optional[Dict[str, Any]] = Field(None, description="Workflow output")
    success: bool = Field(True, description="Whether workflow completed successfully")
    error: Optional[str] = Field(None, description="Error message if failed")


class SearchQuery(BaseModel):
    """Query parameters for searching traces."""

    trace_ids: Optional[List[TraceId]] = Field(None, description="Specific trace IDs to search")
    span_names: Optional[List[str]] = Field(None, description="Span names to match")
    span_kinds: Optional[List[SpanKind]] = Field(None, description="Span kinds to match")
    status: Optional[List[SpanStatus]] = Field(None, description="Span statuses to match")
    start_time: Optional[datetime] = Field(None, description="Start time filter")
    end_time: Optional[datetime] = Field(None, description="End time filter")
    attributes: Optional[Dict[str, Any]] = Field(None, description="Attribute filters")
    limit: Optional[int] = Field(100, description="Maximum number of results")
    offset: Optional[int] = Field(0, description="Result offset for pagination")


class TraceStats(BaseModel):
    """Statistics about traces in a time period."""

    total_traces: int = Field(..., description="Total number of traces")
    total_spans: int = Field(..., description="Total number of spans")
    successful_spans: int = Field(..., description="Number of successful spans")
    error_spans: int = Field(..., description="Number of error spans")
    avg_duration_ms: float = Field(..., description="Average span duration in milliseconds")
    total_llm_calls: int = Field(0, description="Total LLM calls")
    total_llm_cost: float = Field(0.0, description="Total LLM cost")
    total_tokens: int = Field(0, description="Total tokens used")
    unique_workflows: int = Field(0, description="Number of unique workflows")
    time_period_start: datetime = Field(..., description="Statistics period start")
    time_period_end: datetime = Field(..., description="Statistics period end")


def create_llm_trace_from_graphbit(
    span: TraceSpan,
    provider: str,
    model: str,
    graphbit_response: Any,
    request_data: Optional[Dict[str, Any]] = None,
    cost_info: Optional[CostInfo] = None,
    error: Optional[str] = None,
) -> "LlmTrace":
    """Create an LlmTrace from GraphBit LlmResponse and other data.

    Args:
        span: The associated trace span
        provider: LLM provider name (e.g., 'openai', 'anthropic')
        model: Model name
        graphbit_response: GraphBit LlmResponse object
        request_data: Optional request data dictionary
        cost_info: Optional cost information
        error: Optional error message

    Returns:
        LlmTrace object compatible with the tracer
    """

    # Convert GraphBit response to tracer format
    response = LlmResponse.from_graphbit(graphbit_response)

    # Create request object if data provided
    request = None
    if request_data:
        request = LlmRequest(
            messages=request_data.get("messages", []),
            model=model,
            temperature=request_data.get("temperature"),
            max_tokens=request_data.get("max_tokens"),
            tools=request_data.get("tools", []),
            tool_choice=request_data.get("tool_choice"),
            other_params={
                k: v
                for k, v in request_data.items()
                if k not in ["messages", "model", "temperature", "max_tokens", "tools", "tool_choice"]
            },
        )

    # Extract usage from response
    usage = response.usage

    return LlmTrace(
        span=span,
        provider=provider,
        model=model,
        request=request,
        response=response,
        usage=usage,
        cost=cost_info,
        error=error,
    )


def is_graphbit_available() -> bool:
    """Check if GraphBit is available for integration.

    Returns:
        Always True since GraphBit is a required dependency.
    """
    return True
