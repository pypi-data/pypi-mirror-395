"""Integration layer for bridging analysis results to database."""

from __future__ import annotations

__all__ = [
    "record_measurement",
    "check_config",
    "MeasurementProcessor",
    "MeasurementRecorder",
    "InfluxConfig",
    "InfluxConfigError",
    "InfluxPoint",
]

import logging

from metsuperq.database.config import InfluxConfig, InfluxConfigError
from metsuperq.database.schema import InfluxPoint
from metsuperq.integrations.measurement_processor import MeasurementProcessor
from metsuperq.integrations.measurement_recorder import (
    MeasurementRecorder,
    record_measurement,
)

logger = logging.getLogger(__name__)


def check_config() -> bool:
    """Return True if InfluxDB config can be loaded from environment.

    Examples use this to provide a friendly readiness check.
    """
    try:
        InfluxConfig.from_env()
        logger.info("InfluxDB config loaded successfully")
        return True
    except InfluxConfigError:
        logger.error("Failed to load InfluxDB config")
        return False
