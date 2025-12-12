"""Simple synchronous InfluxDB v2 client wrapper."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from influxdb_client.client.query_api import QueryApi
    from influxdb_client.client.write_api import WriteApi

from influxdb_client.client.exceptions import InfluxDBError
from influxdb_client.client.influxdb_client import InfluxDBClient as _InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

from metsuperq.database.config import InfluxConfig
from metsuperq.database.exceptions import InfluxDBConnectionError
from metsuperq.utils import setup_logging

logger = setup_logging(__name__)


class InfluxDBClient:
    """Synchronous InfluxDB v2 client wrapper."""

    def __init__(self, config: InfluxConfig) -> None:
        """Initialize client with configuration.

        Parameters
        ----------
        config : InfluxConfig
            InfluxDB connection configuration
        """
        self.config = config
        self._client: _InfluxDBClient | None = None
        self._write_api: WriteApi | None = None
        self._query_api: QueryApi | None = None
        logger.info("Initialized InfluxDBClient for %s bucket=%s", config.url, config.bucket)

    def connect(self) -> None:
        """Establish connection to InfluxDB."""
        try:
            logger.debug("Connecting to InfluxDB at %s", self.config.url)

            self._client = _InfluxDBClient(
                url=self.config.url,
                token=self.config.token,
                org=self.config.org,
                timeout=self.config.timeout,
                verify_ssl=self.config.verify_ssl,
            )

            # Test connection
            if self._client is not None:
                self._client.ping()

                # Initialize APIs with SYNCHRONOUS writes
                self._write_api = self._client.write_api(write_options=SYNCHRONOUS)
                self._query_api = self._client.query_api()

            logger.info("Successfully connected to InfluxDB")

        except InfluxDBError as e:
            logger.error("Failed to connect to InfluxDB: %s", e, exc_info=True)
            raise InfluxDBConnectionError(
                f"Failed to connect to InfluxDB at {self.config.url}", details={"error": str(e)}
            ) from e

    def disconnect(self) -> None:
        """Close connection to InfluxDB."""
        if self._client:
            try:
                logger.debug("Disconnecting from InfluxDB")
                self._client.close()
                self._client = None
                self._write_api = None
                self._query_api = None
                logger.info("Disconnected from InfluxDB")
            except Exception as e:
                logger.warning("Error during disconnect: %s", e)

    def __enter__(self) -> InfluxDBClient:
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        self.disconnect()

    @property
    def is_connected(self) -> bool:
        """Check if client is connected."""
        if self._client is None:
            return False
        try:
            return self._client.ping()
        except Exception:
            return False

    def get_write_api(self) -> WriteApi:
        """Get write API instance."""
        if not self._write_api:
            raise InfluxDBConnectionError("Client not connected")
        return self._write_api

    def get_query_api(self) -> QueryApi:
        """Get query API instance."""
        if not self._query_api:
            raise InfluxDBConnectionError("Client not connected")
        return self._query_api

    def health_check(self) -> dict[str, Any]:
        """Perform health check and return status."""
        try:
            if not self._client:
                return {"status": "disconnected", "healthy": False}

            # Ping check
            ping_result = self._client.ping()

            # Bucket existence check
            buckets_api = self._client.buckets_api()
            bucket_exists = buckets_api.find_bucket_by_name(self.config.bucket)

            return {
                "status": "connected",
                "healthy": ping_result and bucket_exists is not None,
                "bucket_exists": bucket_exists is not None,
                "config": self.config.mask_sensitive(),
            }
        except Exception as e:
            logger.error("Health check failed: %s", e, exc_info=True)
            return {
                "status": "error",
                "healthy": False,
                "error": str(e),
            }

    def close(self) -> None:
        """Close the client connection (alias for disconnect)."""
        self.disconnect()
