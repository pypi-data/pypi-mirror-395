"""
Base service patterns for database-bound operations.

Provides:
- ServiceResult: Standard result wrapper
- PaginatedResult: Paginated list wrapper
- BaseService: Abstract base for DB services
- SingletonService: Base for infrastructure services
"""

import logging
from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


@dataclass
class ServiceResult(Generic[T]):
    """
    Standard result wrapper for service operations.

    Provides consistent success/error handling across all services.

    Usage:
        # Success case
        return ServiceResult.ok(data={"user_id": 123})

        # Error case
        return ServiceResult.fail("User not found", code="USER_NOT_FOUND")

        # Check result
        if result.success:
            process(result.data)
        else:
            handle_error(result.error_message, result.error_code)
    """

    success: bool
    data: Optional[T] = None
    error_message: Optional[str] = None
    error_code: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

    @classmethod
    def ok(cls, data: T = None, **details) -> "ServiceResult[T]":
        """Create a successful result."""
        return cls(success=True, data=data, details=details)

    @classmethod
    def fail(
        cls,
        message: str,
        code: Optional[str] = None,
        **details
    ) -> "ServiceResult[T]":
        """Create an error result."""
        return cls(
            success=False,
            error_message=message,
            error_code=code,
            details=details
        )

    # Alias for backwards compatibility
    error = fail

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary for API responses."""
        result = {
            "success": self.success,
            "timestamp": self.timestamp.isoformat(),
        }

        if self.success:
            result["data"] = self.data
        else:
            result["error"] = self.error_message
            if self.error_code:
                result["error_code"] = self.error_code

        if self.details:
            result["details"] = self.details

        return result

    def __bool__(self) -> bool:
        """Allow using result in boolean context."""
        return self.success


@dataclass
class PaginatedResult(Generic[T]):
    """
    Result wrapper for paginated list operations.

    Usage:
        return PaginatedResult(
            items=users,
            total=100,
            page=1,
            page_size=20,
            has_more=True
        )
    """

    items: List[T]
    total: int
    page: int
    page_size: int
    has_more: bool = False

    @property
    def total_pages(self) -> int:
        """Calculate total number of pages."""
        if self.page_size <= 0:
            return 0
        return (self.total + self.page_size - 1) // self.page_size

    @property
    def has_previous(self) -> bool:
        """Check if there is a previous page."""
        return self.page > 1

    @property
    def has_next(self) -> bool:
        """Check if there is a next page."""
        return self.page < self.total_pages

    def to_dict(self) -> Dict[str, Any]:
        """Convert to API response format."""
        return {
            "items": self.items,
            "pagination": {
                "total": self.total,
                "page": self.page,
                "page_size": self.page_size,
                "total_pages": self.total_pages,
                "has_more": self.has_more,
                "has_previous": self.has_previous,
                "has_next": self.has_next,
            }
        }


@dataclass
class PaginationParams:
    """
    Standard pagination parameters for list endpoints.

    Usage in routers:
        @router.get("/items")
        async def list_items(
            page: int = Query(1, ge=1),
            page_size: int = Query(20, ge=1, le=100),
        ):
            params = PaginationParams(page=page, page_size=page_size)
            return await service.list_items(params)
    """

    page: int = 1
    page_size: int = 20

    @property
    def offset(self) -> int:
        """Calculate SQL offset from page number."""
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        """Get limit (same as page_size for clarity)."""
        return self.page_size

    def validate(self, max_page_size: int = 100) -> "PaginationParams":
        """Validate and clamp pagination parameters."""
        self.page = max(1, self.page)
        self.page_size = max(1, min(self.page_size, max_page_size))
        return self


class BaseService(ABC):
    """
    Abstract base class for database-bound services.

    Provides:
    - Standard database session management
    - Logging setup
    - Common utility methods

    Usage:
        class UserService(BaseService):
            async def get_user(self, user_id: uuid.UUID) -> ServiceResult[User]:
                try:
                    user = await self._execute_query(
                        select(User).where(User.id == user_id)
                    )
                    if not user:
                        return ServiceResult.error("User not found", "NOT_FOUND")
                    return ServiceResult.ok(user)
                except Exception as e:
                    self._log_error("get_user", e, user_id=str(user_id))
                    return ServiceResult.error(str(e), "DB_ERROR")
    """

    def __init__(self, db: AsyncSession):
        """Initialize service with database session."""
        self.db = db
        self.logger = logging.getLogger(self.__class__.__name__)

    async def _execute_query(self, query):
        """Execute a SQLAlchemy query and return scalar result."""
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def _execute_query_all(self, query):
        """Execute a SQLAlchemy query and return all results."""
        result = await self.db.execute(query)
        return result.scalars().all()

    async def _execute_query_first(self, query):
        """Execute a SQLAlchemy query and return first result."""
        result = await self.db.execute(query)
        return result.scalars().first()

    async def _commit(self) -> bool:
        """Commit the current transaction."""
        try:
            await self.db.commit()
            return True
        except Exception as e:
            await self.db.rollback()
            self.logger.error(f"Transaction commit failed: {e}")
            return False

    async def _refresh(self, instance) -> None:
        """Refresh instance from database."""
        await self.db.refresh(instance)

    def _log_info(self, operation: str, **context):
        """Log info message with context."""
        self.logger.info(f"{operation}", extra=context)

    def _log_error(self, operation: str, error: Exception, **context):
        """Log error with context."""
        self.logger.error(f"{operation} failed: {error}", exc_info=True, extra=context)

    def _log_warning(self, operation: str, message: str, **context):
        """Log warning with context."""
        self.logger.warning(f"{operation}: {message}", extra=context)


class SingletonService:
    """
    Base class for singleton infrastructure services.

    Usage:
        class MyCacheService(SingletonService):
            _instance = None

            def __init__(self):
                if not hasattr(self, "initialized"):
                    self.initialized = True
                    # Initialize service
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls):
        """Get or create singleton instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def reset_instance(cls):
        """Reset singleton instance (for testing)."""
        cls._instance = None
