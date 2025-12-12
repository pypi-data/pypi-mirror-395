"""
Database health check utilities.

Provides comprehensive health monitoring for database connections.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .manager import DatabaseManager

logger = logging.getLogger(__name__)


class HealthStatus(str, Enum):
    """Health check status values."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass
class HealthCheck:
    """
    Database health check result.

    Usage:
        health = await HealthCheck.check(db_manager)
        if health.is_healthy:
            print("Database is healthy")
        else:
            print(f"Database issues: {health.error}")
    """

    status: HealthStatus
    connected: bool
    latency_ms: Optional[float] = None
    database_name: Optional[str] = None
    database_version: Optional[str] = None
    database_size: Optional[int] = None
    pool_stats: Dict[str, int] = field(default_factory=dict)
    error: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)

    @property
    def is_healthy(self) -> bool:
        """Check if database is healthy."""
        return self.status == HealthStatus.HEALTHY

    @property
    def is_degraded(self) -> bool:
        """Check if database is degraded."""
        return self.status == HealthStatus.DEGRADED

    @classmethod
    async def check(cls, manager: "DatabaseManager") -> "HealthCheck":
        """
        Perform comprehensive health check.

        Args:
            manager: DatabaseManager instance to check

        Returns:
            HealthCheck result
        """
        import time

        if not manager.is_initialized:
            return cls(
                status=HealthStatus.UNHEALTHY,
                connected=False,
                error="Database not initialized",
            )

        try:
            start_time = time.perf_counter()

            async with manager.get_connection() as conn:
                # Test basic connectivity
                result = await conn.fetchval("SELECT 1")

                # Calculate latency
                latency_ms = (time.perf_counter() - start_time) * 1000

                # Get database info
                db_info = await conn.fetchrow(
                    """
                    SELECT
                        current_database() as database_name,
                        version() as version,
                        pg_database_size(current_database()) as database_size
                    """
                )

                # Get pool stats
                pool_stats = {}
                if manager.pool:
                    pool_stats = {
                        "size": manager.pool.get_size(),
                        "min_size": manager.pool.get_min_size(),
                        "max_size": manager.pool.get_max_size(),
                        "idle_connections": manager.pool.get_idle_size(),
                        "free_connections": manager.pool.get_size()
                        - (manager.pool.get_size() - manager.pool.get_idle_size()),
                    }

                # Determine status based on latency
                if latency_ms > 1000:
                    status = HealthStatus.DEGRADED
                elif latency_ms > 5000:
                    status = HealthStatus.UNHEALTHY
                else:
                    status = HealthStatus.HEALTHY

                return cls(
                    status=status,
                    connected=result == 1,
                    latency_ms=round(latency_ms, 2),
                    database_name=db_info["database_name"],
                    database_version=db_info["version"],
                    database_size=db_info["database_size"],
                    pool_stats=pool_stats,
                )

        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return cls(
                status=HealthStatus.UNHEALTHY,
                connected=False,
                error=str(e),
            )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses."""
        result = {
            "status": self.status.value,
            "connected": self.connected,
            "timestamp": self.timestamp.isoformat(),
        }

        if self.latency_ms is not None:
            result["latency_ms"] = self.latency_ms

        if self.database_name:
            result["database"] = {
                "name": self.database_name,
                "version": self.database_version,
                "size_bytes": self.database_size,
            }

        if self.pool_stats:
            result["pool"] = self.pool_stats

        if self.error:
            result["error"] = self.error

        return result


async def check_database_health(manager: "DatabaseManager") -> Dict[str, Any]:
    """
    Convenience function to check database health.

    Args:
        manager: DatabaseManager instance

    Returns:
        Health check result as dictionary
    """
    health = await HealthCheck.check(manager)
    return health.to_dict()
