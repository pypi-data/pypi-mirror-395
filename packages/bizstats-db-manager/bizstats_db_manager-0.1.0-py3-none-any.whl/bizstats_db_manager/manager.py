"""
Core database manager with async support and connection pooling.

Features:
- Async SQLAlchemy 2.0+ engine
- asyncpg connection pool for raw queries
- Automatic reconnection with exponential backoff
- Health checks and monitoring
- FastAPI dependency injection support
"""

import asyncio
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Callable, Optional, Union

import asyncpg
from asyncpg import Connection, Pool
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from .config import DatabaseConfig

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Manages database connections and operations.

    Provides:
    - asyncpg pool for high-performance raw queries
    - SQLAlchemy async engine for ORM operations
    - Session factory for request-scoped sessions
    - Health check and monitoring

    Usage:
        # Initialize
        db = DatabaseManager()
        await db.initialize(config)

        # Or with URL
        await db.initialize("postgresql://user:pass@localhost/db")

        # Get session (context manager)
        async with db.get_session() as session:
            result = await session.execute(select(User))

        # Raw query
        async with db.get_connection() as conn:
            rows = await conn.fetch("SELECT * FROM users")

        # FastAPI dependency
        app.dependency_overrides[get_db] = db.get_session_dependency()

        # Cleanup
        await db.close()
    """

    def __init__(self):
        self.pool: Optional[Pool] = None
        self.engine: Optional[AsyncEngine] = None
        self.session_factory: Optional[async_sessionmaker[AsyncSession]] = None
        self.config: Optional[DatabaseConfig] = None
        self._initialized = False
        self._lock = asyncio.Lock()

    @property
    def is_initialized(self) -> bool:
        """Check if database is initialized."""
        return self._initialized

    async def initialize(
        self,
        config: Union[DatabaseConfig, str, None] = None,
    ) -> None:
        """
        Initialize database connections.

        Args:
            config: DatabaseConfig instance, URL string, or None to use environment

        Raises:
            RuntimeError: If initialization fails after all retries
        """
        async with self._lock:
            if self._initialized:
                logger.debug("Database already initialized, skipping")
                return

            # Parse config
            if config is None:
                self.config = DatabaseConfig.from_env()
            elif isinstance(config, str):
                self.config = DatabaseConfig.from_url(config)
            else:
                self.config = config

            logger.info(f"Initializing database: {self.config.get_masked_url()}")

            try:
                await self._create_pool()
                await self._create_engine()
                self._initialized = True
                logger.info("Database initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize database: {e}")
                await self.close()
                raise

    async def _create_pool(self) -> None:
        """Create asyncpg connection pool with retry logic."""
        url = self.config.get_asyncpg_url()
        last_error = None

        for attempt in range(self.config.max_retries):
            try:
                logger.info(f"Creating connection pool (attempt {attempt + 1})")

                self.pool = await asyncpg.create_pool(
                    url,
                    min_size=self.config.pool.min_size,
                    max_size=self.config.pool.max_size,
                    command_timeout=self.config.timeouts.command_timeout,
                    server_settings=self.config.get_server_settings(),
                )

                # Test connection
                async with self.pool.acquire() as conn:
                    await conn.fetchval("SELECT 1")

                logger.info("Connection pool created successfully")
                return

            except Exception as e:
                last_error = e
                if attempt < self.config.max_retries - 1:
                    wait_time = self.config.retry_backoff_base ** attempt
                    logger.warning(
                        f"Pool creation failed (attempt {attempt + 1}), "
                        f"retrying in {wait_time}s: {e}"
                    )
                    await asyncio.sleep(wait_time)

        raise RuntimeError(
            f"Failed to create connection pool after {self.config.max_retries} attempts: {last_error}"
        )

    async def _create_engine(self) -> None:
        """Create SQLAlchemy async engine."""
        url = self.config.get_sqlalchemy_url()

        self.engine = create_async_engine(
            url,
            echo=self.config.echo_sql,
            pool_size=self.config.pool.min_size,
            max_overflow=self.config.pool.max_overflow,
            pool_timeout=self.config.timeouts.pool_timeout,
            pool_recycle=self.config.pool.pool_recycle,
            pool_pre_ping=self.config.pool.pool_pre_ping,
            connect_args={
                "command_timeout": self.config.timeouts.command_timeout,
                "server_settings": self.config.get_server_settings(),
            },
        )

        self.session_factory = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

        logger.info("SQLAlchemy engine created successfully")

    async def close(self) -> None:
        """Close all database connections."""
        if self.pool:
            await self.pool.close()
            self.pool = None

        if self.engine:
            await self.engine.dispose()
            self.engine = None

        self.session_factory = None
        self._initialized = False
        logger.info("Database connections closed")

    @asynccontextmanager
    async def get_connection(self) -> AsyncGenerator[Connection, None]:
        """
        Get a raw asyncpg connection from the pool.

        Usage:
            async with db.get_connection() as conn:
                rows = await conn.fetch("SELECT * FROM users WHERE id = $1", user_id)
        """
        if not self.pool:
            raise RuntimeError("Database not initialized. Call initialize() first.")

        async with self.pool.acquire() as connection:
            yield connection

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Get a SQLAlchemy async session.

        Automatically commits on success, rolls back on error.

        Usage:
            async with db.get_session() as session:
                user = User(name="John")
                session.add(user)
                # Auto-commits on exit
        """
        if not self.session_factory:
            raise RuntimeError("Database not initialized. Call initialize() first.")

        async with self.session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    def get_session_dependency(self) -> Callable:
        """
        Get a FastAPI dependency for database sessions.

        Usage:
            from fastapi import Depends

            db = DatabaseManager()

            @app.get("/users")
            async def get_users(
                session: AsyncSession = Depends(db.get_session_dependency())
            ):
                result = await session.execute(select(User))
                return result.scalars().all()
        """
        async def dependency() -> AsyncGenerator[AsyncSession, None]:
            async with self.get_session() as session:
                yield session

        return dependency

    def get_connection_dependency(self) -> Callable:
        """
        Get a FastAPI dependency for raw database connections.

        Usage:
            @app.get("/raw")
            async def raw_query(
                conn: Connection = Depends(db.get_connection_dependency())
            ):
                return await conn.fetch("SELECT * FROM users")
        """
        async def dependency() -> AsyncGenerator[Connection, None]:
            async with self.get_connection() as conn:
                yield conn

        return dependency

    async def execute_raw(self, query: str, *args) -> list:
        """
        Execute a raw SQL query and return all results.

        Args:
            query: SQL query with $1, $2 placeholders
            *args: Query parameters

        Returns:
            List of result rows
        """
        async with self.get_connection() as conn:
            return await conn.fetch(query, *args)

    async def execute_raw_one(self, query: str, *args):
        """
        Execute a raw SQL query and return single result.

        Args:
            query: SQL query with $1, $2 placeholders
            *args: Query parameters

        Returns:
            Single result row or None
        """
        async with self.get_connection() as conn:
            return await conn.fetchrow(query, *args)

    async def execute_raw_val(self, query: str, *args):
        """
        Execute a raw SQL query and return single value.

        Args:
            query: SQL query with $1, $2 placeholders
            *args: Query parameters

        Returns:
            Single value or None
        """
        async with self.get_connection() as conn:
            return await conn.fetchval(query, *args)


# Global instance for convenience
_default_manager: Optional[DatabaseManager] = None


def get_default_manager() -> DatabaseManager:
    """Get or create the default database manager instance."""
    global _default_manager
    if _default_manager is None:
        _default_manager = DatabaseManager()
    return _default_manager


async def init_database(config: Union[DatabaseConfig, str, None] = None) -> DatabaseManager:
    """
    Initialize the default database manager.

    Args:
        config: Database configuration

    Returns:
        Initialized DatabaseManager instance
    """
    manager = get_default_manager()
    await manager.initialize(config)
    return manager


async def close_database() -> None:
    """Close the default database manager."""
    global _default_manager
    if _default_manager:
        await _default_manager.close()
        _default_manager = None
