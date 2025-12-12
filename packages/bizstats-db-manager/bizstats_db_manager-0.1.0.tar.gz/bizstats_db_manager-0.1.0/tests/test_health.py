"""Tests for health check utilities."""

import pytest
from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, MagicMock

from bizstats_db_manager.health import (
    HealthStatus,
    HealthCheck,
    check_database_health,
)
from bizstats_db_manager.manager import DatabaseManager


class TestHealthStatus:
    """Tests for HealthStatus enum."""

    def test_status_values(self):
        """Test all status values exist."""
        assert HealthStatus.HEALTHY.value == "healthy"
        assert HealthStatus.DEGRADED.value == "degraded"
        assert HealthStatus.UNHEALTHY.value == "unhealthy"
        assert HealthStatus.UNKNOWN.value == "unknown"


class TestHealthCheck:
    """Tests for HealthCheck."""

    def test_is_healthy_true(self):
        """Test is_healthy when healthy."""
        health = HealthCheck(status=HealthStatus.HEALTHY, connected=True)
        assert health.is_healthy is True

    def test_is_healthy_false(self):
        """Test is_healthy when not healthy."""
        health = HealthCheck(status=HealthStatus.UNHEALTHY, connected=False)
        assert health.is_healthy is False

    def test_is_degraded(self):
        """Test is_degraded property."""
        degraded = HealthCheck(status=HealthStatus.DEGRADED, connected=True)
        healthy = HealthCheck(status=HealthStatus.HEALTHY, connected=True)

        assert degraded.is_degraded is True
        assert healthy.is_degraded is False

    @pytest.mark.asyncio
    async def test_check_not_initialized(self):
        """Test health check when not initialized."""
        manager = DatabaseManager()

        health = await HealthCheck.check(manager)

        assert health.status == HealthStatus.UNHEALTHY
        assert health.connected is False
        assert "not initialized" in health.error

    @pytest.mark.asyncio
    async def test_check_healthy(self, mock_asyncpg_pool):
        """Test health check when healthy."""
        manager = DatabaseManager()
        manager._initialized = True
        manager.pool = mock_asyncpg_pool

        health = await HealthCheck.check(manager)

        assert health.status == HealthStatus.HEALTHY
        assert health.connected is True
        assert health.error is None
        assert health.latency_ms is not None

    @pytest.mark.asyncio
    async def test_check_connection_error(self):
        """Test health check with connection error."""
        # Create a failing pool
        class FailingPool:
            def get_size(self):
                return 10
            def get_min_size(self):
                return 5
            def get_max_size(self):
                return 20
            def get_idle_size(self):
                return 5

            @asynccontextmanager
            async def acquire(self):
                raise Exception("Connection failed")
                yield  # Never reached

        manager = DatabaseManager()
        manager._initialized = True
        manager.pool = FailingPool()

        health = await HealthCheck.check(manager)

        assert health.status == HealthStatus.UNHEALTHY
        assert health.connected is False
        assert "Connection failed" in health.error

    @pytest.mark.asyncio
    async def test_check_includes_pool_stats(self, mock_asyncpg_pool):
        """Test health check includes pool statistics."""
        manager = DatabaseManager()
        manager._initialized = True
        manager.pool = mock_asyncpg_pool

        health = await HealthCheck.check(manager)

        assert "size" in health.pool_stats
        assert "min_size" in health.pool_stats
        assert "max_size" in health.pool_stats
        assert "idle_connections" in health.pool_stats

    def test_to_dict_healthy(self):
        """Test to_dict for healthy status."""
        health = HealthCheck(
            status=HealthStatus.HEALTHY,
            connected=True,
            latency_ms=5.5,
            database_name="test_db",
            database_version="PostgreSQL 15",
            database_size=1024000,
            pool_stats={"size": 10, "idle": 5},
        )

        d = health.to_dict()

        assert d["status"] == "healthy"
        assert d["connected"] is True
        assert d["latency_ms"] == 5.5
        assert d["database"]["name"] == "test_db"
        assert d["database"]["version"] == "PostgreSQL 15"
        assert d["pool"]["size"] == 10
        assert "error" not in d

    def test_to_dict_unhealthy(self):
        """Test to_dict for unhealthy status."""
        health = HealthCheck(
            status=HealthStatus.UNHEALTHY,
            connected=False,
            error="Connection refused",
        )

        d = health.to_dict()

        assert d["status"] == "unhealthy"
        assert d["connected"] is False
        assert d["error"] == "Connection refused"

    def test_to_dict_includes_timestamp(self):
        """Test to_dict includes timestamp."""
        health = HealthCheck(status=HealthStatus.HEALTHY, connected=True)
        d = health.to_dict()

        assert "timestamp" in d


class TestCheckDatabaseHealth:
    """Tests for check_database_health function."""

    @pytest.mark.asyncio
    async def test_returns_dict(self, mock_asyncpg_pool):
        """Test function returns dictionary."""
        manager = DatabaseManager()
        manager._initialized = True
        manager.pool = mock_asyncpg_pool

        result = await check_database_health(manager)

        assert isinstance(result, dict)
        assert "status" in result
        assert "connected" in result
