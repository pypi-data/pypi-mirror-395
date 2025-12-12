"""Application configuration settings."""

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    """Main application settings."""

    name: str = Field("BitPulse", validation_alias="APP_NAME")
    version: str = Field("1.0.0", validation_alias="APP_VERSION")
    debug: bool = Field(False, validation_alias="DEBUG")
    log_level: str = Field("INFO", validation_alias="LOG_LEVEL")
    env: str = Field("development", validation_alias="ENV")

    @field_validator("log_level")
    def validate_log_level(cls, v):
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of {valid_levels}")
        return v.upper()


app_settings = AppSettings()
