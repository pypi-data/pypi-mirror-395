"""
GraphBit Tracer - Automatically capture and send LLM trace data to your observability API endpoint.

This library provides automatic tracing for GraphBit LLM clients and sends trace data
to remote API endpoints via HTTP POST.
"""

from bitpulse.api.client import TracingApiClient

# Import from reorganized modules while maintaining backward compatibility
from bitpulse.core.auto_tracer import AutoTracer, TracedExecutor

# Also expose core functionality for advanced users
from bitpulse.core.core import GraphBitTracer
from bitpulse.utils.converter import convert_spans_to_records

__version__ = "0.1.0"
__author__ = "GraphBit Team"
__email__ = "team@graphbit.ai"

__all__ = [
    "AutoTracer",
    "TracedExecutor",
    "TracingApiClient",
    "GraphBitTracer",
    "convert_spans_to_records",
    "__version__",
]
