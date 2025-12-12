"""
Minimal JSON API schema for BitPulse span data transmission.
Industry-standard format similar to LangSmith with fixed structure.
"""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class LlmData(BaseModel):
    """LLM operation data."""

    provider: Optional[str] = None
    model: Optional[str] = None
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    total_tokens: Optional[int] = None
    request_time_ms: Optional[float] = None
    finish_reason: Optional[str] = None


class ToolData(BaseModel):
    """Tool execution data."""

    name: Optional[str] = None
    success: Optional[bool] = None
    execution_time_ms: Optional[float] = None
    error: Optional[str] = None


class HttpData(BaseModel):
    """HTTP request data."""

    method: Optional[str] = None
    url: Optional[str] = None
    status_code: Optional[int] = None


class ErrorData(BaseModel):
    """Error information."""

    type: Optional[str] = None
    message: Optional[str] = None


class StandardSpan(BaseModel):
    """Fixed JSON structure for span transmission."""

    # Core identifiers
    span_id: str
    trace_id: str
    parent_span_id: Optional[str] = None

    # Essential metadata
    name: str
    kind: str  # "client", "server", "internal"
    status: str  # "ok", "error"
    service_name: str

    # Timing (ISO 8601)
    start_time: str
    end_time: str
    duration_ms: float

    # Categorized attributes
    llm: Optional[LlmData] = None
    tool: Optional[ToolData] = None
    http: Optional[HttpData] = None
    error: Optional[ErrorData] = None

    # Additional attributes
    custom: Optional[Dict[str, Union[str, int, float, bool]]] = None


class SpanBatch(BaseModel):
    """Batch format for efficient transmission."""

    batch_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    service_name: str
    spans: List[StandardSpan]


def convert_raw_span(raw_span: Dict[str, Any], service_name: str = "graphbit-tracer") -> StandardSpan:
    """Convert raw GraphBit span to standard format."""

    # Extract timing
    start_time = raw_span.get("start_time")
    end_time = raw_span.get("end_time")

    # Handle datetime objects or strings
    if isinstance(start_time, datetime):
        start_iso = start_time.isoformat()
    else:
        start_iso = str(start_time) if start_time else datetime.utcnow().isoformat()

    if isinstance(end_time, datetime):
        end_iso = end_time.isoformat()
    else:
        end_iso = str(end_time) if end_time else datetime.utcnow().isoformat()

    # Calculate duration
    duration_ms = 0.0
    if start_time and end_time:
        try:
            if isinstance(start_time, datetime) and isinstance(end_time, datetime):
                duration_ms = (end_time - start_time).total_seconds() * 1000
            else:
                start_dt = datetime.fromisoformat(start_iso.replace("Z", "+00:00"))
                end_dt = datetime.fromisoformat(end_iso.replace("Z", "+00:00"))
                duration_ms = (end_dt - start_dt).total_seconds() * 1000
        except Exception:
            duration_ms = 0.0

    # Extract attributes
    attrs = raw_span.get("attributes", {})

    # Build LLM data
    llm_data = None
    if any(k.startswith("llm.") for k in attrs.keys()):
        llm_data = LlmData(
            provider=attrs.get("llm.provider"),
            model=attrs.get("llm.model"),
            input_tokens=attrs.get("llm.usage.prompt_tokens"),
            output_tokens=attrs.get("llm.usage.completion_tokens"),
            total_tokens=attrs.get("llm.usage.total_tokens"),
            request_time_ms=attrs.get("llm.request_time_ms"),
            finish_reason=attrs.get("llm.response.finish_reason"),
        )

    # Build tool data
    tool_data = None
    if any(k.startswith("tool.") for k in attrs.keys()):
        tool_data = ToolData(
            name=attrs.get("tool.name"),
            success=attrs.get("tool.success"),
            execution_time_ms=attrs.get("tool.execution_time_ms"),
            error=attrs.get("tool.error"),
        )

    # Build HTTP data
    http_data = None
    if any(k.startswith("http.") for k in attrs.keys()):
        http_data = HttpData(
            method=attrs.get("http.method"), url=attrs.get("http.url"), status_code=attrs.get("http.status_code")
        )

    # Build error data
    error_data = None
    if any(k.startswith("error.") for k in attrs.keys()) or raw_span.get("status") == "error":
        error_data = ErrorData(type=attrs.get("error.type"), message=attrs.get("error.message"))

    # Custom attributes
    custom_attrs = {}
    for key, value in attrs.items():
        if not any(key.startswith(p) for p in ["llm.", "tool.", "http.", "error."]):
            if isinstance(value, (str, int, float, bool)):
                custom_attrs[key] = value

    return StandardSpan(
        span_id=str(raw_span.get("span_id", "")),
        trace_id=str(raw_span.get("trace_id", "")),
        parent_span_id=raw_span.get("parent_span_id"),
        name=str(raw_span.get("name", "unknown")),
        kind=str(raw_span.get("kind", "internal")),
        status=str(raw_span.get("status", "ok")),
        service_name=service_name,
        start_time=start_iso,
        end_time=end_iso,
        duration_ms=duration_ms,
        llm=llm_data,
        tool=tool_data,
        http=http_data,
        error=error_data,
        custom=custom_attrs if custom_attrs else None,
    )


def convert_spans_to_batch(raw_spans: List[Dict[str, Any]], service_name: str = "graphbit-tracer") -> SpanBatch:
    """Convert list of raw spans to transmission batch."""
    standard_spans = [convert_raw_span(span, service_name) for span in raw_spans]

    return SpanBatch(service_name=service_name, spans=standard_spans)
