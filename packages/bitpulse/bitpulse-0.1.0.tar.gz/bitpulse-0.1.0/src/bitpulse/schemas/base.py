"""
BitPulse API Schema

This module provides the BitPulse Trace API format with token and LLM
metadata in the metadata field. Only includes data available from BitPulse.

"""

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class TraceRecord(BaseModel):
    """
    GraphBit trace format for LLM observability.

    Structure includes: tracing_api_key, traceable_project, status, run_type, run_name,
    input, output, error, start_time, latency, tokens, metadata, etc.

    Token details (input_tokens, output_tokens, finish_reason, model_name)
    are stored in the metadata field.

    Note: tracing_api_key and traceable_project_name are mandatory and should come from
    environment variables (BITPULSE_TRACING_API_KEY and BITPULSE_TRACEABLE_PROJECT).
    """

    # API and project fields (mandatory, from environment variables)
    tracing_api_key: str = Field(..., description="API key for GraphBit tracing service (from env)")
    traceable_project_name: str = Field(..., description="Project name for grouping traces (from env)")

    # Status and type
    status: Optional[str] = Field(None, description="Execution status (string | null)")
    run_type: Optional[str] = Field("llm", description="Type of run (prompt, llm, parser, chain, draft)")
    run_name: Optional[str] = Field(None, description="Human-readable run name")

    # Input/Output
    input: Any = Field(..., description="Input data (any type)")
    output: Any = Field(None, description="Output data (any type)")

    # Error
    error: Optional[str] = Field(None, description="Error message if failed")

    # Timing
    start_time: Optional[str] = Field(None, description="ISO 8601 start time")
    latency: Optional[float] = Field(None, description="Duration in milliseconds")

    # Tokens (top-level field)
    tokens: Optional[int] = Field(None, description="Total token count")

    # Cost (not available from GraphBit, always null)
    cost: Optional[float] = Field(None, description="Cost in USD (not available)")

    # First token (not available from GraphBit, always null)
    first_token: Optional[str] = Field(None, description="First token time (not available)")

    # Tags
    tags: Optional[list[str]] = Field(None, description="Tags for categorization")

    # Metadata - THIS IS WHERE WE PUT TOKEN DETAILS AND LLM INFO
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Metadata including input_tokens, output_tokens, finish_reason, model_name",
    )

    # Dataset and annotation (optional)
    dataset: Optional[str] = Field(None, description="Dataset name")
    annotation_queue: Optional[str] = Field(None, description="Annotation queue name")
    reference_example: Optional[str] = Field(None, description="Reference example ID")
