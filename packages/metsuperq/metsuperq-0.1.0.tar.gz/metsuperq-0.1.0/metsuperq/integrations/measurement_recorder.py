"""Measurement recorder for data."""

from __future__ import annotations

from collections.abc import Callable
from contextlib import contextmanager
from typing import Any

from metsuperq.database.client import InfluxDBClient
from metsuperq.database.config import InfluxConfig
from metsuperq.database.exceptions import DatabaseError
from metsuperq.database.writer import MeasurementWriter
from metsuperq.integrations.measurement_processor import MeasurementProcessor
from metsuperq.utils import setup_logging

logger = setup_logging(__name__)

# Avoid magic values (ruff PLR2004)
VISIBLE_TOKEN_TAIL = 4

# Type alias for analysis results
AnalysisResult = dict[str, Any]


class MeasurementRecorder:
    """Recorder for measurements."""

    def __init__(
        self,
        config: InfluxConfig | None = None,
        *,
        config_loader: Callable[[], InfluxConfig] | None = None,
    ) -> None:
        """Initialize measurement recorder.

        Parameters
        ----------
        config : InfluxConfig | None, optional
            InfluxDB configuration. If None, loads from environment.
        """
        self._config: InfluxConfig | None = config
        self._config_loader: Callable[[], InfluxConfig] = config_loader or InfluxConfig.from_env
        self.processor = MeasurementProcessor()

        logger.info("Initialized MeasurementRecorder")
        if self._config is not None:
            self._log_configuration(self._config)
        else:
            logger.debug("Configuration load deferred until first usage")

    def record_measurement(
        self,
        analysis_result: AnalysisResult,
        experiment_id: str,
        device_name: str,
        qubit_name: str,
    ) -> None:
        """Record a single measurement to the database.

        Parameters
        ----------
        analysis_result : AnalysisResult
            Analysis result from BaseAnalyzer.run_full_analysis()
        experiment_id : str
            Experiment unique identifier
        device_name : str
            Name of the quantum device
        qubit_name : str
            Name of the measured qubit
        """
        logger.info("Recording measurement for qubit %s on device %s", qubit_name, device_name)

        try:
            # Process analysis result to measurement points
            points = self.processor.process_analysis_result(
                analysis_result=analysis_result,
                qubit_name=qubit_name,
                device_name=device_name,
                experiment_id=experiment_id,
            )

            if not points:
                logger.warning("No valid measurement points to record")
                return

            with self._get_writer() as writer:
                for point in points:
                    writer.write_point(point)

            logger.info("Successfully recorded %d measurement points", len(points))

        except Exception as e:
            logger.error("Failed to record measurement: %s", e, exc_info=True)
            raise DatabaseError(
                f"Failed to record measurement for {qubit_name}: {e}",
                details={
                    "qubit_name": qubit_name,
                    "device_name": device_name,
                    "error": str(e),
                },
            ) from e

    def health_check(self) -> dict[str, Any]:
        """Run a health check against the database."""
        try:
            with self._get_client() as client:
                return client.health_check()
        except Exception as e:
            logger.error("Health check failed: %s", e, exc_info=True)
            return {"status": "error", "healthy": False, "error": str(e)}

    @contextmanager
    def _get_client(self):
        """Context manager yielding a connected Influx client."""
        config = self._ensure_config()
        client = InfluxDBClient(config)
        try:
            client.connect()
            yield client
        finally:
            client.disconnect()

    @contextmanager
    def _get_writer(self):
        """Context manager yielding a writer bound to a client."""
        with self._get_client() as client:
            writer = MeasurementWriter(client)
            try:
                yield writer
            finally:
                close = getattr(writer, "close", None)
                if callable(close):
                    close()

    def _ensure_config(self) -> InfluxConfig:
        if self._config is None:
            logger.debug("Loading InfluxDB configuration via loader")
            self._config = self._config_loader()
            self._log_configuration(self._config)
        return self._config

    def _log_configuration(self, config: InfluxConfig) -> None:
        logger.debug(
            "Configuration: %s",
            {
                "host": config.host,
                "port": config.port,
                "token": (
                    f"***{config.token[-VISIBLE_TOKEN_TAIL:]}"
                    if len(config.token) >= VISIBLE_TOKEN_TAIL
                    else "***"
                ),
                "org": config.org,
                "bucket": config.bucket,
                "timeout": config.timeout,
                "verify_ssl": config.verify_ssl,
            },
        )


def get_default_recorder() -> MeasurementRecorder:
    """Get or create the default measurement recorder singleton.

    Implemented via a function attribute to avoid ``global`` (ruff PLW0603).
    Tests may reset this by deleting the attribute.
    """
    if not hasattr(get_default_recorder, "_instance"):
        get_default_recorder._instance = MeasurementRecorder()  # type: ignore[attr-defined]
    return get_default_recorder._instance  # type: ignore[no-any-return]


def record_measurement(
    analysis_result: AnalysisResult,
    experiment_id: str,
    device_name: str,
    qubit_name: str,
) -> None:
    """Record a single measurement to the database.

    Parameters
    ----------
    analysis_result : AnalysisResult
        Analysis result from BaseAnalyzer.run_full_analysis()
    experiment_id : str
        Experiment unique identifier
    device_name : str
        Name of the quantum device (e.g., "device_1")
    qubit_name : str
        Name of the measured qubit (e.g., "Q1", "qubit_01")

    Examples
    --------
    >>> from metsuperq.analysis.base_analysis import BaseAnalyzer
    >>> from metsuperq.integrations import record_measurement
    >>>
    >>> analyzer = BaseAnalyzer()
    >>> result = analyzer.run_full_analysis("20250903-173311-935-8d9a03")
    >>> record_measurement(result, "Q1", "my_device")
    """
    recorder = get_default_recorder()
    recorder.record_measurement(
        analysis_result=analysis_result,
        experiment_id=experiment_id,
        device_name=device_name,
        qubit_name=qubit_name,
    )
