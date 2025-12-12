from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from bitpulse.core.exceptions import StorageError
from bitpulse.schemas.types import LlmTrace, SearchQuery, SpanId, TraceSpan, TraceStats, WorkflowTrace
from bitpulse.utils.config import StorageConfig


class StorageBackend(ABC):
    """Abstract base class for storage backends."""

    @abstractmethod
    async def store_span(self, span: TraceSpan) -> None:
        """Store a span.

        Args:
            span: Span to store

        Raises:
            StorageError: If storage fails
        """
        pass

    @abstractmethod
    async def get_span(self, span_id: SpanId) -> Optional[TraceSpan]:
        """Get a span by ID.

        Args:
            span_id: Span ID

        Returns:
            Span if found, None otherwise

        Raises:
            StorageError: If retrieval fails
        """
        pass

    @abstractmethod
    async def search_traces(self, query: SearchQuery) -> List[TraceSpan]:
        """Search for traces matching the query.

        Args:
            query: Search query

        Returns:
            List of matching spans

        Raises:
            StorageError: If search fails
        """
        pass

    @abstractmethod
    async def store_llm_trace(self, trace: LlmTrace) -> None:
        """Store an LLM trace.

        Args:
            trace: LLM trace to store

        Raises:
            StorageError: If storage fails
        """
        pass

    @abstractmethod
    async def get_llm_traces(
        self,
        start_time: datetime,
        end_time: datetime,
        limit: Optional[int] = None,
    ) -> List[LlmTrace]:
        """Get LLM traces in a time range.

        Args:
            start_time: Start time
            end_time: End time
            limit: Optional limit on number of results

        Returns:
            List of LLM traces

        Raises:
            StorageError: If retrieval fails
        """
        pass

    @abstractmethod
    async def get_workflow_traces(
        self,
        start_time: datetime,
        end_time: datetime,
        limit: Optional[int] = None,
    ) -> List[WorkflowTrace]:
        """Get workflow traces in a time range.

        Args:
            start_time: Start time
            end_time: End time
            limit: Optional limit on number of results

        Returns:
            List of workflow traces

        Raises:
            StorageError: If retrieval fails
        """
        pass

    @abstractmethod
    async def get_trace_stats(
        self,
        start_time: datetime,
        end_time: datetime,
    ) -> TraceStats:
        """Get trace statistics for a time period.

        Args:
            start_time: Start time
            end_time: End time

        Returns:
            Trace statistics

        Raises:
            StorageError: If retrieval fails
        """
        pass

    @abstractmethod
    async def cleanup_old_traces(self, older_than: datetime) -> int:
        """Clean up traces older than the specified time.

        Args:
            older_than: Cutoff time

        Returns:
            Number of traces deleted

        Raises:
            StorageError: If cleanup fails
        """
        pass

    @abstractmethod
    async def health_check(self) -> None:
        """Perform health check on the storage backend.

        Raises:
            StorageError: If health check fails
        """
        pass


async def create_storage_backend(config: StorageConfig) -> StorageBackend:
    """Create a storage backend based on configuration.

    Args:
        config: Storage configuration

    Returns:
        Initialized storage backend

    Raises:
        StorageError: If backend creation fails
    """
    if config.type == "memory":
        # Import here to avoid circular import - this is a legitimate exception to PEP 8
        from .memory import MemoryStorageBackend

        backend = MemoryStorageBackend(config.memory_capacity)
    else:
        raise StorageError(f"Unknown storage type: {config.type}. Only 'memory' storage is supported.")

    # Initialize the backend
    await backend.health_check()

    return backend
