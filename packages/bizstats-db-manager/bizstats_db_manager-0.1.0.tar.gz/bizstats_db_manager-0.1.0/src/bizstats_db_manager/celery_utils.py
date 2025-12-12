"""
Celery task utilities for async database operations.

Provides utilities for running async database operations within Celery tasks,
which run in a synchronous context.
"""

import asyncio
import concurrent.futures
import logging
import os
from typing import AsyncGenerator, Optional

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from .config import DatabaseConfig

logger = logging.getLogger(__name__)

# Global session factory for Celery tasks
_celery_session_factory: Optional[async_sessionmaker[AsyncSession]] = None


def get_celery_session_factory(
    config: Optional[DatabaseConfig] = None,
) -> async_sessionmaker[AsyncSession]:
    """
    Get async session factory for Celery tasks.

    Creates a new session factory that Celery tasks can use
    independently from the main FastAPI database manager.

    Args:
        config: Optional database configuration. If None, loads from environment.

    Returns:
        Session factory for async database operations

    Usage:
        session_factory = get_celery_session_factory()

        async def my_async_operation():
            async with session_factory() as session:
                result = await session.execute(select(User))
                return result.scalars().all()
    """
    global _celery_session_factory

    if _celery_session_factory is not None:
        return _celery_session_factory

    # Load config from environment if not provided
    if config is None:
        config = DatabaseConfig.from_env()

    # Create engine for Celery tasks with optimized settings
    engine = create_async_engine(
        config.get_sqlalchemy_url(),
        echo=config.echo_sql,
        pool_pre_ping=True,
        pool_recycle=300,  # 5 minutes - shorter for background tasks
        pool_size=5,  # Smaller pool for background tasks
        max_overflow=10,
    )

    _celery_session_factory = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    return _celery_session_factory


async def get_async_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Async generator for database sessions in Celery tasks.

    Usage in Celery tasks:
        async for db in get_async_db_session():
            # Use db session here
            result = await db.execute(select(User))
            return result.scalars().all()

    Or with run_async:
        async def my_operation():
            async for db in get_async_db_session():
                result = await db.execute(select(User))
                return result.scalars().all()

        # In Celery task
        result = run_async(my_operation())
    """
    session_factory = get_celery_session_factory()
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


def run_async(coro):
    """
    Run async coroutine in Celery task (sync context).

    Handles the complexity of running async code from sync Celery tasks,
    including proper event loop management.

    Args:
        coro: Async coroutine to execute

    Returns:
        Result of the coroutine

    Usage:
        @celery_app.task
        def my_celery_task():
            async def async_operation():
                async for db in get_async_db_session():
                    users = await db.execute(select(User))
                    return users.scalars().all()

            return run_async(async_operation())
    """
    try:
        # Try to get existing event loop
        loop = asyncio.get_event_loop()

        if loop.is_running():
            # If loop is running (e.g., in notebook or some async context),
            # we need to use a new thread
            logger.debug("Event loop running, using thread executor")
            return _run_in_new_thread(coro)
        else:
            # Loop exists but not running, use it
            return loop.run_until_complete(coro)

    except RuntimeError:
        # No event loop in current thread, create a new one
        logger.debug("No event loop, using asyncio.run()")
        return asyncio.run(coro)


def _run_in_new_thread(coro):
    """Run coroutine in a new thread with its own event loop."""

    def run_in_new_loop():
        new_loop = asyncio.new_event_loop()
        try:
            asyncio.set_event_loop(new_loop)
            return new_loop.run_until_complete(coro)
        finally:
            new_loop.close()
            asyncio.set_event_loop(None)

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(run_in_new_loop)
        return future.result()


def reset_celery_session_factory() -> None:
    """
    Reset the global Celery session factory.

    Useful for testing or when database configuration changes.
    """
    global _celery_session_factory
    _celery_session_factory = None


class CeleryDatabaseMixin:
    """
    Mixin for Celery tasks that need database access.

    Usage:
        class MyTask(CeleryDatabaseMixin, celery.Task):
            def run(self, user_id: str):
                return self.run_db_operation(self._get_user, user_id)

            async def _get_user(self, session: AsyncSession, user_id: str):
                result = await session.execute(
                    select(User).where(User.id == user_id)
                )
                return result.scalar_one_or_none()
    """

    def run_db_operation(self, async_func, *args, **kwargs):
        """
        Run an async database operation.

        Args:
            async_func: Async function that takes (session, *args, **kwargs)
            *args: Additional arguments for the function
            **kwargs: Additional keyword arguments

        Returns:
            Result of the async function
        """
        async def operation():
            async for session in get_async_db_session():
                return await async_func(session, *args, **kwargs)

        return run_async(operation())
