"""Measurement data writer."""

from __future__ import annotations

from metsuperq.database.client import InfluxDBClient
from metsuperq.database.exceptions import WriteError
from metsuperq.database.schema import InfluxPoint
from metsuperq.utils import setup_logging

logger = setup_logging(__name__)


class MeasurementWriter:
    """Measurement data writer.

    Writes measurement data to InfluxDB using synchronous writes.
    """

    def __init__(self, client: InfluxDBClient, max_retries: int = 3) -> None:
        """Initialize measurement writer.

        Parameters
        ----------
        client : InfluxDBClient
            Connected InfluxDB client
        max_retries : int, optional
            Maximum retry attempts (default: 3)
        """
        self.client = client
        self.max_retries = max_retries
        logger.info("Initialized MeasurementWriter with max_retries=%d", max_retries)

    def write_point(self, point: InfluxPoint) -> None:
        """Write a single measurement point.

        Parameters
        ----------
        point : MeasurementPoint
            Measurement data point to write
        """
        try:
            logger.debug("Writing measurement point: %s", point.measurement)

            write_api = self.client.get_write_api()
            data = point.to_influx_dict()

            # Write immediately (SYNCHRONOUS mode)
            write_api.write(
                bucket=self.client.config.bucket,
                record=data,
            )

            logger.debug("Successfully wrote measurement point: %s", point.measurement)

        except Exception as e:
            logger.error("Failed to write measurement point: %s", e, exc_info=True)
            raise WriteError(
                f"Failed to write measurement point: {e}",
                details={"point": point.model_dump(), "error": str(e)},
            ) from e

    def write_points(self, points: list[InfluxPoint]) -> None:
        """Write multiple measurement points.

        Parameters
        ----------
        points : list[MeasurementPoint]
            List of measurement points to write
        """
        logger.info("Writing %d measurement points", len(points))

        try:
            write_api = self.client.get_write_api()
            data = [point.to_influx_dict() for point in points]

            # Write all points in single request (SYNCHRONOUS mode)
            write_api.write(
                bucket=self.client.config.bucket,
                record=data,
            )

            logger.info("Successfully wrote %d measurement points", len(points))

        except Exception as e:
            logger.error("Failed to write measurement points: %s", e, exc_info=True)
            raise WriteError(
                f"Failed to write {len(points)} measurement points: {e}",
                details={"num_points": len(points), "error": str(e)},
            ) from e
