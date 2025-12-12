"""Configuration management for InfluxDB connection."""

from __future__ import annotations

from typing import Any, Self

from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings

from metsuperq.utils import setup_logging

logger = setup_logging(__name__)


class InfluxConfigError(Exception):
    """Exception raised for InfluxDB configuration errors.

    This exception provides user-friendly error messages for common
    configuration issues like missing environment variables.
    """

    pass


class InfluxConfig(BaseSettings):
    """Configuration for InfluxDB v2 connection.

    Attributes
    ----------
    host : str
        InfluxDB host (required)
        InfluxDB port (required)
    token : str
        Authentication token (required)
    org : str
        Organization name (required)
    bucket : str
        Bucket name for measurements (required)
    timeout : int
        Request timeout in milliseconds (optional, default: 30000)
    verify_ssl : bool
        Whether to verify SSL certificates (optional, default: True)
    """

    host: str = Field(description="InfluxDB host")
    port: int = Field(description="InfluxDB port")
    token: str = Field(description="Authentication token")
    org: str = Field(description="Organization name")
    bucket: str = Field(description="Bucket name for measurements")
    timeout: int = Field(default=30000, description="Request timeout in ms")
    verify_ssl: bool = Field(default=True, description="Verify SSL certificates")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "env_prefix": "INFLUXDB_",
    }

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)

    @property
    def url(self) -> str:
        """Return InfluxDB URL."""
        protocol = "https" if self.verify_ssl else "http"
        return f"{protocol}://{self.host}:{self.port}"

    @classmethod
    def from_env(cls) -> Self:
        """Create configuration from environment variables and .env file.

        Automatically loads from .env file if present, then environment variables.

        Raises
        ------
        InfluxConfigError
            If required environment variables are missing
        """
        logger.debug("Loading InfluxDB configuration from environment and .env file")

        try:
            return cls()
        except ValidationError as e:
            # Use list comprehension to extract missing field names
            missing_fields = [error["loc"][0] for error in e.errors() if error["type"] == "missing"]

            if missing_fields:
                field_mapping = {
                    "token": "INFLUXDB_TOKEN",
                    "org": "INFLUXDB_ORG",
                    "bucket": "INFLUXDB_BUCKET",
                    "host": "INFLUXDB_HOST",
                    "port": "INFLUXDB_PORT",
                    "timeout": "INFLUXDB_TIMEOUT",
                    "verify_ssl": "INFLUXDB_VERIFY_SSL",
                }

                # Map field names to environment variable names
                env_vars = [field_mapping[f] for f in missing_fields if f in field_mapping]

                logger.error("Missing required InfluxDB configuration: %s", missing_fields)
                raise InfluxConfigError(
                    "Missing required InfluxDB configuration.\n\n"
                    "Required environment variables (or .env file entries):\n"
                    + "\n".join(f"  • {var}" for var in env_vars)
                    + "\n\n"
                    "Set these in your .env file:\n"
                    "  INFLUXDB_URL='your-url-here:your-port-here'\n"
                    "  INFLUXDB_TOKEN=your-token-here\n"
                    "  INFLUXDB_ORG=your-org-name\n"
                    "  INFLUXDB_BUCKET=your-bucket-name\n\n"
                    "Or as environment variables:\n"
                    "  export INFLUXDB_URL='your-url-here:your-port-here'\n"
                    "  export INFLUXDB_TOKEN='your-token-here'\n"
                    "  export INFLUXDB_ORG='your-org-name'\n"
                    "  export INFLUXDB_BUCKET='your-bucket-name'\n\n"
                    "Optional variables:\n"
                    "  INFLUXDB_TIMEOUT=30000\n"
                    "  INFLUXDB_VERIFY_SSL=true\n"
                ) from e

            # Re-raise other validation errors
            raise

    def mask_sensitive(self) -> dict[str, Any]:
        """Return config dict with sensitive data masked."""
        config_dict = self.model_dump()
        if config_dict.get("token"):
            config_dict["token"] = f"***{config_dict['token'][-4:]}"
        return config_dict
