"""Configuration management for GraphBit Tracer."""

import os
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic_settings import BaseSettings


class ApiClientConfig(BaseSettings):
    """Configuration for API client."""

    api_url: str = Field(
        "https://platform-api.graphbit.ai/api/v1/tracing/single-run",
        alias="BITPULSE_TRACING_API_URL",
        description="API endpoint URL for sending trace records",
    )
    api_key: Optional[str] = Field(
        None,
        alias="BITPULSE_TRACING_API_KEY",
        description="API key for authentication",
    )
    enabled: bool = Field(True, description="Enable API client")
    timeout: float = Field(10.0, description="Request timeout in seconds")
    max_retries: int = Field(3, description="Maximum number of retry attempts")


api_client_config = ApiClientConfig()


class TracingApiConfig(BaseSettings):
    """Configuration for tracing API (converter)."""

    tracing_api_key: str | None = Field(
        None,
        alias="BITPULSE_TRACING_API_KEY",
        description="API key for BitPulse tracing service (mandatory)",
    )
    traceable_project_name: str | None = Field(
        None,
        alias="BITPULSE_TRACEABLE_PROJECT",
        description="Project name for grouping traces (mandatory)",
    )


tracing_api_config = TracingApiConfig()


class RemoteExporterConfig(BaseModel):
    """Configuration for remote span export."""

    endpoint_url: str = Field(..., description="Remote endpoint URL")
    api_key: Optional[str] = Field(None, description="API key for authentication")
    batch_size: int = Field(100, description="Batch size for export")
    timeout_seconds: int = Field(30, description="Request timeout in seconds")
    max_retries: int = Field(3, description="Maximum number of retry attempts")
    retry_delay_seconds: float = Field(1.0, description="Delay between retries in seconds")
    headers: Optional[Dict[str, str]] = Field(None, description="Custom headers")


class StorageConfig(BaseModel):
    """Storage backend configuration."""

    type: str = Field("memory", description="Storage backend type (only 'memory' is supported)")

    # Memory configuration
    memory_capacity: int = Field(10000, description="Memory storage capacity")


class ExportConfig(BaseModel):
    """Data export configuration."""

    enabled: bool = Field(False, description="Enable data export")
    export_interval_seconds: int = Field(3600, description="Export interval in seconds")
    traces_path: Optional[str] = Field("./exports/traces", description="Traces export path")
    llm_traces_path: Optional[str] = Field("./exports/llm", description="LLM traces export path")
    workflow_traces_path: Optional[str] = Field("./exports/workflows", description="Workflow traces export path")
    retention_days: int = Field(30, description="Data retention period in days")


class MetricsConfig(BaseModel):
    """Metrics collection configuration."""

    enabled: bool = Field(True, description="Enable metrics collection")
    collection_interval_seconds: int = Field(60, description="Metrics collection interval")


class IngestionConfig(BaseModel):
    """Data ingestion configuration."""

    enabled: bool = Field(True, description="Enable data ingestion")
    graphbit_monitoring: bool = Field(True, description="Enable GraphBit monitoring")
    monitoring_interval_seconds: int = Field(1, description="GraphBit monitoring interval")
    batch_size: int = Field(100, description="Batch size for ingestion")
    max_queue_size: int = Field(1000, description="Maximum ingestion queue size")
    callback_timeout_seconds: int = Field(30, description="Callback timeout in seconds")


class TracerConfig(BaseSettings):
    """Main tracer configuration."""

    model_config = ConfigDict(env_prefix="BITPULSE_TRACER_", env_file=".env", extra="ignore")

    # Core settings
    enabled: bool = Field(True, description="Enable tracing")
    service_name: str = Field("graphbit-app", description="Service name")
    service_version: Optional[str] = Field(None, description="Service version")
    environment: Optional[str] = Field(None, description="Environment (dev, staging, prod)")
    sampling_rate: float = Field(1.0, description="Sampling rate (0.0 to 1.0)")

    # Resource attributes
    resource_attributes: Dict[str, Any] = Field(default_factory=dict, description="Resource attributes")

    # Component configurations
    storage: StorageConfig = Field(default_factory=StorageConfig, description="Storage configuration")
    export: ExportConfig = Field(default_factory=ExportConfig, description="Export configuration")
    metrics: MetricsConfig = Field(default_factory=MetricsConfig, description="Metrics configuration")
    ingestion: IngestionConfig = Field(default_factory=IngestionConfig, description="Data ingestion configuration")

    # Advanced settings
    max_span_attributes: int = Field(100, description="Maximum span attributes")
    max_span_events: int = Field(100, description="Maximum span events")
    max_span_links: int = Field(100, description="Maximum span links")
    span_processor_batch_size: int = Field(100, description="Span processor batch size")
    span_processor_timeout_ms: int = Field(5000, description="Span processor timeout in milliseconds")

    @classmethod
    def from_env(cls) -> "TracerConfig":
        """Create configuration from environment variables.

        Environment variables:
        - BITPULSE_TRACER_ENABLED: Enable/disable tracing
        - BITPULSE_TRACER_SERVICE_NAME: Service name
        - BITPULSE_TRACER_SERVICE_VERSION: Service version
        - BITPULSE_TRACER_ENVIRONMENT: Environment
        - BITPULSE_TRACER_SAMPLING_RATE: Sampling rate
        - BITPULSE_TRACER_STORAGE_TYPE: Storage type
        - BITPULSE_TRACER_STORAGE_PATH: SQLite database path
        - BITPULSE_TRACER_REDIS_URL: Redis connection URL
        - BITPULSE_TRACER_METRICS_ENABLED: Enable metrics
        - BITPULSE_TRACER_PROMETHEUS_PORT: Prometheus port
        """
        # Create base config
        config = cls()

        # Override with environment variables
        if os.getenv("BITPULSE_TRACER_ENABLED"):
            config.enabled = os.getenv("BITPULSE_TRACER_ENABLED", "true").lower() == "true"

        if os.getenv("BITPULSE_TRACER_SERVICE_NAME"):
            config.service_name = os.getenv("BITPULSE_TRACER_SERVICE_NAME", config.service_name)

        if os.getenv("BITPULSE_TRACER_SERVICE_VERSION"):
            config.service_version = os.getenv("BITPULSE_TRACER_SERVICE_VERSION")

        if os.getenv("BITPULSE_TRACER_ENVIRONMENT"):
            config.environment = os.getenv("BITPULSE_TRACER_ENVIRONMENT")

        if os.getenv("BITPULSE_TRACER_SAMPLING_RATE"):
            config.sampling_rate = float(os.getenv("BITPULSE_TRACER_SAMPLING_RATE", config.sampling_rate))

        # Storage configuration
        if os.getenv("BITPULSE_TRACER_STORAGE_TYPE"):
            config.storage.type = os.getenv("BITPULSE_TRACER_STORAGE_TYPE", config.storage.type)

        if os.getenv("BITPULSE_TRACER_STORAGE_PATH"):
            config.storage.database_path = os.getenv("BITPULSE_TRACER_STORAGE_PATH", config.storage.database_path)

        if os.getenv("BITPULSE_TRACER_REDIS_URL"):
            config.storage.redis_url = os.getenv("BITPULSE_TRACER_REDIS_URL", config.storage.redis_url)

        # Metrics configuration
        if os.getenv("BITPULSE_TRACER_METRICS_ENABLED"):
            config.metrics.enabled = os.getenv("BITPULSE_TRACER_METRICS_ENABLED", "true").lower() == "true"

        if os.getenv("BITPULSE_TRACER_PROMETHEUS_ENABLED"):
            config.metrics.prometheus_enabled = (
                os.getenv("BITPULSE_TRACER_PROMETHEUS_ENABLED", "true").lower() == "true"
            )

        if os.getenv("BITPULSE_TRACER_PROMETHEUS_PORT"):
            config.metrics.prometheus_port = int(
                os.getenv("BITPULSE_TRACER_PROMETHEUS_PORT", config.metrics.prometheus_port)
            )

        # Export configuration
        if os.getenv("BITPULSE_TRACER_EXPORT_ENABLED"):
            config.export.enabled = os.getenv("BITPULSE_TRACER_EXPORT_ENABLED", "false").lower() == "true"

        if os.getenv("BITPULSE_TRACER_EXPORT_INTERVAL"):
            config.export.export_interval_seconds = int(
                os.getenv("BITPULSE_TRACER_EXPORT_INTERVAL", config.export.export_interval_seconds)
            )

        return config

    def validate_config(self) -> List[str]:
        """Validate configuration and return list of errors."""
        errors = []

        if not self.service_name:
            errors.append("Service name cannot be empty")

        if self.sampling_rate < 0.0 or self.sampling_rate > 1.0:
            errors.append("Sampling rate must be between 0.0 and 1.0")

        if self.storage.type not in ["memory", "sqlite", "redis"]:
            errors.append(f"Invalid storage type: {self.storage.type}")

        return errors

    def summary(self) -> str:
        """Get a summary of the configuration (without sensitive data)."""
        return (
            f"GraphBit Tracer Config: "
            f"service={self.service_name}, "
            f"enabled={self.enabled}, "
            f"sampling={self.sampling_rate}, "
            f"storage={self.storage.type}, "
            f"metrics={self.metrics.enabled}"
        )
