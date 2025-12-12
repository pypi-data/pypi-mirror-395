"""Tests for DatabaseManager."""

import pytest
from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, MagicMock, patch

from bizstats_db_manager.manager import (
    DatabaseManager,
    get_default_manager,
    init_database,
    close_database,
)
from bizstats_db_manager.config import DatabaseConfig


class TestDatabaseManager:
    """Tests for DatabaseManager."""

    @pytest.fixture
    def manager(self):
        """Create fresh manager instance."""
        return DatabaseManager()

    def test_init(self, manager):
        """Test manager initialization state."""
        assert manager.pool is None
        assert manager.engine is None
        assert manager.session_factory is None
        assert manager.config is None
        assert manager._initialized is False

    def test_is_initialized_false(self, manager):
        """Test is_initialized when not initialized."""
        assert manager.is_initialized is False

    @pytest.mark.asyncio
    async def test_initialize_with_config(self, manager, database_config):
        """Test initialization with config object."""
        with patch.object(manager, "_create_pool", new_callable=AsyncMock) as mock_pool, \
             patch.object(manager, "_create_engine", new_callable=AsyncMock) as mock_engine:

            await manager.initialize(database_config)

            assert manager.config == database_config
            mock_pool.assert_called_once()
            mock_engine.assert_called_once()
            assert manager._initialized is True

    @pytest.mark.asyncio
    async def test_initialize_with_url(self, manager):
        """Test initialization with URL string."""
        url = "postgresql://user:pass@localhost/db"

        with patch.object(manager, "_create_pool", new_callable=AsyncMock), \
             patch.object(manager, "_create_engine", new_callable=AsyncMock):

            await manager.initialize(url)

            assert manager.config is not None
            assert manager.config.host == "localhost"
            assert manager.config.user == "user"

    @pytest.mark.asyncio
    async def test_initialize_from_env(self, manager, monkeypatch):
        """Test initialization from environment."""
        monkeypatch.setenv("POSTGRES_HOST", "envhost")
        monkeypatch.setenv("POSTGRES_DB", "envdb")

        with patch.object(manager, "_create_pool", new_callable=AsyncMock), \
             patch.object(manager, "_create_engine", new_callable=AsyncMock):

            await manager.initialize(None)

            assert manager.config.host == "envhost"
            assert manager.config.database == "envdb"

    @pytest.mark.asyncio
    async def test_initialize_idempotent(self, manager, database_config):
        """Test that multiple initialize calls are safe."""
        with patch.object(manager, "_create_pool", new_callable=AsyncMock) as mock_pool, \
             patch.object(manager, "_create_engine", new_callable=AsyncMock):

            await manager.initialize(database_config)
            await manager.initialize(database_config)

            # Should only be called once
            assert mock_pool.call_count == 1

    @pytest.mark.asyncio
    async def test_close(self, manager, mock_asyncpg_pool):
        """Test closing connections."""
        manager.pool = mock_asyncpg_pool

        # Create a mock engine with async dispose
        mock_engine = MagicMock()
        mock_engine.dispose = AsyncMock()
        manager.engine = mock_engine

        manager.session_factory = MagicMock()
        manager._initialized = True

        await manager.close()

        # MockPool.close is async
        assert manager.pool is None
        assert manager.engine is None
        assert manager.session_factory is None
        assert manager._initialized is False

    @pytest.mark.asyncio
    async def test_get_connection_not_initialized(self, manager):
        """Test get_connection raises when not initialized."""
        with pytest.raises(RuntimeError, match="not initialized"):
            async with manager.get_connection():
                pass

    @pytest.mark.asyncio
    async def test_get_connection(self, manager, mock_asyncpg_pool):
        """Test getting a connection."""
        manager.pool = mock_asyncpg_pool
        manager._initialized = True

        async with manager.get_connection() as conn:
            result = await conn.fetchval("SELECT 1")
            assert result == 1

    @pytest.mark.asyncio
    async def test_get_session_not_initialized(self, manager):
        """Test get_session raises when not initialized."""
        with pytest.raises(RuntimeError, match="not initialized"):
            async with manager.get_session():
                pass

    @pytest.mark.asyncio
    async def test_get_session(self, manager, mock_session_factory, mock_async_session):
        """Test getting a session."""
        manager.session_factory = mock_session_factory
        manager._initialized = True

        async with manager.get_session() as session:
            assert session is mock_async_session

    @pytest.mark.asyncio
    async def test_get_session_commits_on_success(self, manager, mock_session_factory, mock_async_session):
        """Test session commits on successful exit."""
        manager.session_factory = mock_session_factory
        manager._initialized = True

        async with manager.get_session():
            pass

        mock_async_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_session_rollback_on_error(self, manager, mock_session_factory, mock_async_session):
        """Test session rolls back on error."""
        manager.session_factory = mock_session_factory
        manager._initialized = True

        with pytest.raises(ValueError):
            async with manager.get_session():
                raise ValueError("Test error")

        mock_async_session.rollback.assert_called_once()

    def test_get_session_dependency(self, manager):
        """Test getting FastAPI dependency."""
        manager._initialized = True
        manager.session_factory = MagicMock()

        dep = manager.get_session_dependency()
        assert callable(dep)

    def test_get_connection_dependency(self, manager):
        """Test getting FastAPI connection dependency."""
        manager._initialized = True
        manager.pool = MagicMock()

        dep = manager.get_connection_dependency()
        assert callable(dep)

    @pytest.mark.asyncio
    async def test_execute_raw(self, manager, mock_asyncpg_pool):
        """Test raw query execution."""
        manager.pool = mock_asyncpg_pool
        manager._initialized = True

        result = await manager.execute_raw("SELECT * FROM users")
        assert result == []

    @pytest.mark.asyncio
    async def test_execute_raw_one(self, manager, mock_asyncpg_pool):
        """Test single row raw query."""
        manager.pool = mock_asyncpg_pool
        manager._initialized = True

        result = await manager.execute_raw_one("SELECT * FROM users WHERE id = $1", 1)
        assert result is not None

    @pytest.mark.asyncio
    async def test_execute_raw_val(self, manager, mock_asyncpg_pool):
        """Test single value raw query."""
        manager.pool = mock_asyncpg_pool
        manager._initialized = True

        result = await manager.execute_raw_val("SELECT 1")
        assert result == 1


class TestDatabaseManagerInternals:
    """Tests for internal manager methods."""

    @pytest.fixture
    def manager(self):
        """Create fresh manager instance."""
        return DatabaseManager()

    @pytest.mark.asyncio
    async def test_initialize_failure_cleans_up(self, manager, database_config):
        """Test that failed initialization cleans up properly."""
        with patch.object(manager, "_create_pool", new_callable=AsyncMock) as mock_pool, \
             patch.object(manager, "_create_engine", new_callable=AsyncMock) as mock_engine, \
             patch.object(manager, "close", new_callable=AsyncMock) as mock_close:

            mock_engine.side_effect = Exception("Engine creation failed")

            with pytest.raises(Exception, match="Engine creation failed"):
                await manager.initialize(database_config)

            mock_close.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_pool_success(self, manager, database_config):
        """Test successful pool creation."""
        manager.config = database_config

        # Create a proper async context manager for acquire
        mock_connection = AsyncMock()
        mock_connection.fetchval = AsyncMock(return_value=1)

        @asynccontextmanager
        async def mock_acquire():
            yield mock_connection

        mock_pool = MagicMock()
        mock_pool.acquire = mock_acquire

        with patch("bizstats_db_manager.manager.asyncpg.create_pool", new_callable=AsyncMock) as mock_create:
            mock_create.return_value = mock_pool

            await manager._create_pool()

            assert manager.pool is mock_pool
            mock_create.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_pool_retry_on_failure(self, manager, database_config):
        """Test pool creation retries on failure."""
        manager.config = database_config

        # Create a proper async context manager for acquire
        mock_connection = AsyncMock()
        mock_connection.fetchval = AsyncMock(return_value=1)

        @asynccontextmanager
        async def mock_acquire():
            yield mock_connection

        mock_pool = MagicMock()
        mock_pool.acquire = mock_acquire

        call_count = 0

        async def create_pool_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise Exception("Connection failed")
            return mock_pool

        with patch("bizstats_db_manager.manager.asyncpg.create_pool", side_effect=create_pool_effect), \
             patch("asyncio.sleep", new_callable=AsyncMock):
            await manager._create_pool()

        assert call_count == 2
        assert manager.pool is mock_pool

    @pytest.mark.asyncio
    async def test_create_pool_exhausts_retries(self, manager, database_config):
        """Test pool creation raises after exhausting retries."""
        manager.config = database_config

        with patch("bizstats_db_manager.manager.asyncpg.create_pool", side_effect=Exception("Connection failed")), \
             patch("asyncio.sleep", new_callable=AsyncMock):

            with pytest.raises(RuntimeError, match="Failed to create connection pool"):
                await manager._create_pool()

    @pytest.mark.asyncio
    async def test_create_engine_success(self, manager, database_config):
        """Test successful engine creation."""
        manager.config = database_config

        mock_engine = MagicMock()

        with patch("bizstats_db_manager.manager.create_async_engine", return_value=mock_engine):
            await manager._create_engine()

            assert manager.engine is mock_engine
            assert manager.session_factory is not None

    @pytest.mark.asyncio
    async def test_close_with_none_pool_and_engine(self, manager):
        """Test close when pool and engine are None."""
        manager.pool = None
        manager.engine = None
        manager._initialized = True

        await manager.close()

        assert manager._initialized is False


class TestModuleFunctions:
    """Tests for module-level functions."""

    def test_get_default_manager(self):
        """Test getting default manager."""
        manager1 = get_default_manager()
        manager2 = get_default_manager()

        assert manager1 is manager2
        assert isinstance(manager1, DatabaseManager)

    @pytest.mark.asyncio
    async def test_init_database(self):
        """Test init_database function."""
        with patch.object(DatabaseManager, "initialize", new_callable=AsyncMock):
            manager = await init_database("postgresql://localhost/test")
            assert manager is not None

    @pytest.mark.asyncio
    async def test_close_database(self):
        """Test close_database function."""
        # Get the default manager first
        manager = get_default_manager()
        manager._initialized = True
        manager.pool = AsyncMock()
        manager.engine = AsyncMock()

        await close_database()

        # After close, getting default should create new
        # (we reset the global in close_database)
