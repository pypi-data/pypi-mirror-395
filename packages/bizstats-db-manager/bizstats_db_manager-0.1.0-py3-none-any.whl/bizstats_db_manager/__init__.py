"""
BizStats Database Manager - PostgreSQL async database management.

A production-ready PostgreSQL database management library with:
- Async SQLAlchemy 2.0+ support
- asyncpg connection pooling
- Alembic migration utilities
- Celery task support
- Health checks and monitoring

Quick Start:
    from bizstats_db_manager import DatabaseManager, Base

    # Initialize
    db = DatabaseManager()
    await db.initialize("postgresql://user:pass@localhost/db")

    # Use with FastAPI
    @app.get("/users")
    async def get_users(session: AsyncSession = Depends(db.get_session_dependency())):
        result = await session.execute(select(User))
        return result.scalars().all()

    # Health check
    health = await db.health_check()
    print(health)  # {"status": "healthy", "connected": True, ...}
"""

from .config import DatabaseConfig, TimeoutConfig
from .manager import DatabaseManager
from .base import Base, BaseModel
from .service import (
    BaseService,
    SingletonService,
    ServiceResult,
    PaginatedResult,
    PaginationParams,
)
from .celery_utils import (
    get_celery_session_factory,
    get_async_db_session,
    run_async,
)
from .health import HealthCheck, HealthStatus

__version__ = "0.1.0"
__author__ = "Absolut-e Data Com Inc."
__email__ = "account@absolut-e.com"

__all__ = [
    # Core
    "DatabaseManager",
    "DatabaseConfig",
    "TimeoutConfig",
    # Base classes
    "Base",
    "BaseModel",
    # Service patterns
    "BaseService",
    "SingletonService",
    "ServiceResult",
    "PaginatedResult",
    "PaginationParams",
    # Celery support
    "get_celery_session_factory",
    "get_async_db_session",
    "run_async",
    # Health
    "HealthCheck",
    "HealthStatus",
    # Version
    "__version__",
]
