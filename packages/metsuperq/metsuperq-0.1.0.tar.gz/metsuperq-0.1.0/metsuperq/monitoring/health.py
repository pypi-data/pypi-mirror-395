"""Health checking and system monitoring for MetSuperQ."""

from __future__ import annotations

import os
import tempfile
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

import h5py
import lmfit
import numpy as np
import psutil
from pydantic import BaseModel, Field

from metsuperq.analysis.base_analysis import BaseAnalyzer
from metsuperq.database.client import InfluxDBClient
from metsuperq.database.config import InfluxConfig
from metsuperq.database.exceptions import InfluxDBConnectionError
from metsuperq.utils import setup_logging

logger = setup_logging(__name__)

# Health check thresholds
LOW_DISK_SPACE_GB = 1.0  # Disk space below this triggers degraded status
CRITICAL_MEMORY_PERCENT = 90  # Memory usage above this is critical
HIGH_MEMORY_PERCENT = 80  # Memory usage above this triggers warning

# Unit conversion constants
BYTES_PER_GB = 1024**3  # Bytes in a gigabyte
BYTES_PER_MB = 1024**2  # Bytes in a megabyte
MS_PER_SECOND = 1000  # Milliseconds per second


class HealthStatus(str, Enum):
    """Health check status levels."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


class ComponentType(str, Enum):
    """Types of system components to monitor."""

    DATABASE = "database"
    ANALYSIS_ENGINE = "analysis_engine"
    FILE_SYSTEM = "file_system"
    MEMORY = "memory"
    NETWORK = "network"


@dataclass
class HealthCheck:
    """Individual health check result."""

    component: ComponentType
    status: HealthStatus
    message: str
    response_time_ms: float
    timestamp: float
    details: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert health check to dictionary."""
        return {
            "component": self.component.value,
            "status": self.status.value,
            "message": self.message,
            "response_time_ms": self.response_time_ms,
            "timestamp": self.timestamp,
            "details": self.details or {},
        }


class SystemHealth(BaseModel):
    """Overall system health status."""

    overall_status: HealthStatus = Field(description="Overall system health")
    checks: list[HealthCheck] = Field(default_factory=list, description="Individual health checks")
    timestamp: float = Field(default_factory=time.time, description="Health check timestamp")
    uptime_seconds: float = Field(ge=0, description="System uptime")
    message: str = Field(description="Health check message")

    def add_check(self, check: HealthCheck) -> None:
        """Add a health check result and recalculate overall status."""
        self.checks.append(check)
        self._recalculate_overall_status_from_checks()

    def _recalculate_overall_status_from_checks(self) -> None:
        """Recalculate overall status based on all individual check results."""
        if not self.checks:
            self.overall_status = HealthStatus.UNKNOWN
            return

        statuses = [check.status for check in self.checks]

        if all(status == HealthStatus.HEALTHY for status in statuses):
            self.overall_status = HealthStatus.HEALTHY
        elif any(status == HealthStatus.UNHEALTHY for status in statuses):
            self.overall_status = HealthStatus.UNHEALTHY
        elif any(status == HealthStatus.DEGRADED for status in statuses):
            self.overall_status = HealthStatus.DEGRADED
        else:
            self.overall_status = HealthStatus.UNKNOWN

    def get_unhealthy_components(self) -> list[HealthCheck]:
        """Get list of unhealthy components."""
        return [
            check
            for check in self.checks
            if check.status in (HealthStatus.UNHEALTHY, HealthStatus.DEGRADED)
        ]

    def to_dict(self) -> dict[str, Any]:
        """Convert system health to dictionary."""
        return {
            "overall_status": self.overall_status.value,
            "checks": [check.to_dict() for check in self.checks],
            "timestamp": self.timestamp,
            "uptime_seconds": self.uptime_seconds,
            "message": self.message,
        }


class HealthChecker:
    """Comprehensive health checking for MetSuperQ components."""

    def __init__(self, influx_config: InfluxConfig | None = None) -> None:
        """Initialize health checker.

        Parameters
        ----------
        influx_config : InfluxConfig | None
            InfluxDB configuration for database health checks
        """
        self._influx_config = influx_config
        self._start_time = time.time()

        logger.info("Initialized HealthChecker")

    def check_database_health(self) -> HealthCheck:
        """Check InfluxDB database health.

        Returns
        -------
        HealthCheck
            Database health check result
        """
        start_time = time.time()

        if not self._influx_config:
            return HealthCheck(
                component=ComponentType.DATABASE,
                status=HealthStatus.UNKNOWN,
                message="No database configuration provided",
                response_time_ms=0.0,
                timestamp=time.time(),
            )

        try:
            # Use context manager to ensure connection is always closed
            with InfluxDBClient(self._influx_config) as client:
                # All database operations happen within connection scope
                health_info = client.health_check()

                response_time = (time.time() - start_time) * MS_PER_SECOND

                if health_info and health_info.get("status") == "pass":
                    return HealthCheck(
                        component=ComponentType.DATABASE,
                        status=HealthStatus.HEALTHY,
                        message="Database connection successful",
                        response_time_ms=response_time,
                        timestamp=time.time(),
                        details=health_info,
                    )
                else:
                    return HealthCheck(
                        component=ComponentType.DATABASE,
                        status=HealthStatus.DEGRADED,
                        message="Database responding but not fully healthy",
                        response_time_ms=response_time,
                        timestamp=time.time(),
                        details=health_info,
                    )

        except InfluxDBConnectionError as e:
            response_time = (time.time() - start_time) * 1000
            return HealthCheck(
                component=ComponentType.DATABASE,
                status=HealthStatus.UNHEALTHY,
                message=f"Database connection failed: {e}",
                response_time_ms=response_time,
                timestamp=time.time(),
                details={"error": str(e)},
            )
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            return HealthCheck(
                component=ComponentType.DATABASE,
                status=HealthStatus.UNHEALTHY,
                message=f"Unexpected database error: {e}",
                response_time_ms=response_time,
                timestamp=time.time(),
                details={"error": str(e)},
            )

    def check_analysis_engine_health(self) -> HealthCheck:
        """Check analysis engine health.

        Returns
        -------
        HealthCheck
            Analysis engine health check result
        """
        start_time = time.time()

        try:
            # Basic functionality test
            _ = BaseAnalyzer()

            response_time = (time.time() - start_time) * 1000

            return HealthCheck(
                component=ComponentType.ANALYSIS_ENGINE,
                status=HealthStatus.HEALTHY,
                message="Analysis engine initialized successfully",
                response_time_ms=response_time,
                timestamp=time.time(),
                details={
                    "numpy_version": np.__version__,
                    "lmfit_version": lmfit.__version__,
                    "h5py_version": h5py.__version__,
                },
            )

        except ImportError as e:
            response_time = (time.time() - start_time) * 1000
            return HealthCheck(
                component=ComponentType.ANALYSIS_ENGINE,
                status=HealthStatus.UNHEALTHY,
                message=f"Missing dependency: {e}",
                response_time_ms=response_time,
                timestamp=time.time(),
                details={"error": str(e)},
            )
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            return HealthCheck(
                component=ComponentType.ANALYSIS_ENGINE,
                status=HealthStatus.DEGRADED,
                message=f"Analysis engine issue: {e}",
                response_time_ms=response_time,
                timestamp=time.time(),
                details={"error": str(e)},
            )

    def check_file_system_health(self) -> HealthCheck:
        """Check file system health for data directories.

        Returns
        -------
        HealthCheck
            File system health check result
        """
        start_time = time.time()

        try:
            # Test write/read in temp directory
            with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
                test_file = Path(f.name)
                f.write("health_check_test")

            # Verify file was written and can be read
            content = test_file.read_text()
            test_file.unlink()  # Clean up

            if content != "health_check_test":
                raise ValueError("File system read/write test failed")

            # Check available disk space
            stat = os.statvfs(tempfile.gettempdir())
            free_space_gb = (stat.f_frsize * stat.f_bavail) / BYTES_PER_GB

            response_time = (time.time() - start_time) * MS_PER_SECOND

            if free_space_gb < LOW_DISK_SPACE_GB:
                status = HealthStatus.DEGRADED
                message = f"Low disk space: {free_space_gb:.1f}GB free"
            else:
                status = HealthStatus.HEALTHY
                message = f"File system healthy: {free_space_gb:.1f}GB free"

            return HealthCheck(
                component=ComponentType.FILE_SYSTEM,
                status=status,
                message=message,
                response_time_ms=response_time,
                timestamp=time.time(),
                details={"free_space_gb": free_space_gb},
            )

        except Exception as e:
            response_time = (time.time() - start_time) * MS_PER_SECOND
            return HealthCheck(
                component=ComponentType.FILE_SYSTEM,
                status=HealthStatus.UNHEALTHY,
                message=f"File system error: {e}",
                response_time_ms=response_time,
                timestamp=time.time(),
                details={"error": str(e)},
            )

    def check_memory_health(self) -> HealthCheck:
        """Check memory usage health.

        Returns
        -------
        HealthCheck
            Memory health check result
        """
        start_time = time.time()

        try:
            if psutil is None:
                raise ImportError("psutil not available")

            memory = psutil.virtual_memory()
            process = psutil.Process()
            process_memory_mb = process.memory_info().rss / BYTES_PER_MB

            response_time = (time.time() - start_time) * MS_PER_SECOND

            # Determine status based on memory usage
            if memory.percent > CRITICAL_MEMORY_PERCENT:
                status = HealthStatus.UNHEALTHY
                message = f"Critical memory usage: {memory.percent:.1f}%"
            elif memory.percent > HIGH_MEMORY_PERCENT:
                status = HealthStatus.DEGRADED
                message = f"High memory usage: {memory.percent:.1f}%"
            else:
                status = HealthStatus.HEALTHY
                message = f"Memory usage normal: {memory.percent:.1f}%"

            return HealthCheck(
                component=ComponentType.MEMORY,
                status=status,
                message=message,
                response_time_ms=response_time,
                timestamp=time.time(),
                details={
                    "system_memory_percent": memory.percent,
                    "system_memory_available_gb": memory.available / BYTES_PER_GB,
                    "process_memory_mb": process_memory_mb,
                },
            )

        except ImportError:
            response_time = (time.time() - start_time) * MS_PER_SECOND
            return HealthCheck(
                component=ComponentType.MEMORY,
                status=HealthStatus.UNKNOWN,
                message="psutil not available for memory monitoring",
                response_time_ms=response_time,
                timestamp=time.time(),
            )
        except Exception as e:
            response_time = (time.time() - start_time) * MS_PER_SECOND
            return HealthCheck(
                component=ComponentType.MEMORY,
                status=HealthStatus.DEGRADED,
                message=f"Memory check error: {e}",
                response_time_ms=response_time,
                timestamp=time.time(),
                details={"error": str(e)},
            )

    def perform_full_health_check(self) -> SystemHealth:
        """Perform comprehensive health check of all components.

        Returns
        -------
        SystemHealth
            Complete system health status
        """
        logger.info("Starting full system health check")

        health = SystemHealth(
            uptime_seconds=time.time() - self._start_time,
            timestamp=time.time(),
            overall_status=HealthStatus.HEALTHY,
            message="System health check completed",
        )

        # Perform all health checks
        checks = [
            self.check_analysis_engine_health(),
            self.check_file_system_health(),
            self.check_memory_health(),
        ]

        # Add database check if configuration is available
        if self._influx_config:
            checks.append(self.check_database_health())

        # Add all checks to system health
        for check in checks:
            health.add_check(check)

        logger.info(
            "Health check completed",
            extra={
                "overall_status": health.overall_status.value,
                "unhealthy_components": len(health.get_unhealthy_components()),
                "total_checks": len(health.checks),
            },
        )

        return health

    def get_health_summary(self) -> dict[str, Any]:
        """Get a quick health summary.

        Returns
        -------
        dict[str, Any]
            Health summary dictionary
        """
        health = self.perform_full_health_check()
        return {
            "status": health.overall_status.value,
            "timestamp": health.timestamp,
            "uptime_seconds": health.uptime_seconds,
            "components_checked": len(health.checks),
            "unhealthy_components": len(health.get_unhealthy_components()),
            "details": health.to_dict(),
        }
