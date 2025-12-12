"""Pytest configuration and fixtures."""

import os
import pytest
from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, MagicMock, patch

# Set test environment
os.environ.setdefault("POSTGRES_HOST", "localhost")
os.environ.setdefault("POSTGRES_PORT", "5432")
os.environ.setdefault("POSTGRES_USER", "postgres")
os.environ.setdefault("POSTGRES_PASSWORD", "postgres")
os.environ.setdefault("POSTGRES_DB", "test_db")


class MockConnection:
    """Mock asyncpg connection."""

    async def fetch(self, query, *args):
        return []

    async def fetchrow(self, query, *args):
        return {
            "database_name": "test_db",
            "version": "PostgreSQL 15.0",
            "database_size": 1024000,
        }

    async def fetchval(self, query, *args):
        return 1


class MockPool:
    """Mock asyncpg pool with proper async context manager."""

    def __init__(self):
        self._conn = MockConnection()

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
        yield self._conn

    async def close(self):
        pass


@pytest.fixture
def mock_asyncpg_pool():
    """Mock asyncpg pool."""
    return MockPool()


@pytest.fixture
def mock_async_session():
    """Mock SQLAlchemy async session."""
    session = AsyncMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.close = AsyncMock()
    session.execute = AsyncMock()
    session.refresh = AsyncMock()
    return session


@pytest.fixture
def mock_session_factory(mock_async_session):
    """Mock session factory."""
    factory = MagicMock()
    factory.return_value.__aenter__ = AsyncMock(return_value=mock_async_session)
    factory.return_value.__aexit__ = AsyncMock(return_value=None)
    return factory


@pytest.fixture
def database_config():
    """Create test database config."""
    from bizstats_db_manager import DatabaseConfig

    return DatabaseConfig(
        host="localhost",
        port=5432,
        user="postgres",
        password="postgres",
        database="test_db",
    )
