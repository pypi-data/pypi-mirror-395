"""
GraphBit AutoTracer API Client

Handles HTTP POST requests to send trace records to remote API endpoints.
"""

import asyncio
from typing import List, Optional

import httpx

from bitpulse.schemas.base import TraceRecord
from bitpulse.utils.config import api_client_config
from bitpulse.utils.logging_utils import setup_logging

logger = setup_logging()


class TracingApiClient:
    """Client for sending trace records to remote API endpoints."""

    def __init__(
        self,
        api_url: Optional[str] = None,
        api_key: Optional[str] = None,
        enabled: bool = True,
        timeout: float = 10.0,
        max_retries: int = 3,
    ):
        """
        Initialize the API client.

        Args:
            api_url: API endpoint URL (default: from BITPULSE_TRACING_API_URL env var)
            api_key: API key for authentication (default: from BITPULSE_TRACING_API_KEY env var)
            enabled: Whether to enable remote submission (default: True)
            timeout: Request timeout in seconds (default: 10.0)
            max_retries: Maximum number of retry attempts (default: 3)

        Raises:
            ValueError: If timeout <= 0 or max_retries < 0
            TypeError: If parameters have invalid types
        """
        # Validate timeout
        if not isinstance(timeout, (int, float)):
            raise TypeError(f"timeout must be a number, got {type(timeout).__name__}")
        if timeout <= 0:
            raise ValueError(f"timeout must be positive, got {timeout}")

        # Validate max_retries
        if not isinstance(max_retries, int):
            raise TypeError(f"max_retries must be an integer, got {type(max_retries).__name__}")
        if max_retries < 0:
            raise ValueError(f"max_retries must be non-negative, got {max_retries}")

        # Validate enabled
        if not isinstance(enabled, bool):
            raise TypeError(f"enabled must be a boolean, got {type(enabled).__name__}")

        # Use provided values or load from centralized config
        if api_url is None or api_key is None:
            api_url = api_url or api_client_config.api_url
            api_key = api_key or api_client_config.api_key

        self.api_url = api_url
        self.api_key = api_key
        self.enabled = enabled
        self.timeout = timeout
        self.max_retries = max_retries
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        """
        Get or create the reusable HTTP client session.

        Returns:
            httpx.AsyncClient instance
        """
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self.timeout)
        return self._client

    async def close(self) -> None:
        """
        Close the HTTP client session.

        Should be called when the client is no longer needed to properly
        clean up resources and close connections.
        """
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    async def send_trace_record(self, trace_record: TraceRecord) -> bool:
        """
        Send a single trace record to the API endpoint.

        Args:
            trace_record: TraceRecord object to send

        Returns:
            True if successful, False otherwise
        """
        # Convert TraceRecord to dict
        trace_data = trace_record.model_dump()

        # Prepare headers
        headers = {
            "Content-Type": "application/json",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        # Send POST request using reusable client (Issue 2: Fix HTTP Session Recreation)
        try:
            client = await self._get_client()
            response = await client.post(self.api_url, json=trace_data, headers=headers)

            if response.status_code in (200, 201, 202):
                logger.info(
                    "Trace record sent successfully",
                    run_name=trace_record.run_name,
                    status_code=response.status_code,
                )
                return True
            else:
                logger.warning(
                    "Failed to send trace record",
                    run_name=trace_record.run_name,
                    status_code=response.status_code,
                    response_text=response.text[:200],
                )
                return False
        except Exception as e:
            logger.error(
                "Error sending trace record",
                run_name=trace_record.run_name,
                error=str(e),
            )
            return False

    async def send_trace_records(self, trace_records: List[TraceRecord]) -> dict:
        """
        Send multiple trace records to the API endpoint

        Args:
            trace_records: List of TraceRecord objects to send

        Returns:
            Dictionary with success/failure counts
        """
        results = {"sent": 0, "failed": 0, "total": len(trace_records)}

        if not trace_records:
            logger.info("No trace records to send")
            return results

        # Send all trace records concurrently (Issue 1: Sequential Request Processing)
        tasks = [self.send_trace_record(record) for record in trace_records]
        results_list = await asyncio.gather(*tasks, return_exceptions=False)

        # Count successes and failures
        for success in results_list:
            if success:
                results["sent"] += 1
            else:
                results["failed"] += 1

        logger.info(
            "Trace records submission complete",
            sent=results["sent"],
            failed=results["failed"],
            total=results["total"],
        )

        return results
