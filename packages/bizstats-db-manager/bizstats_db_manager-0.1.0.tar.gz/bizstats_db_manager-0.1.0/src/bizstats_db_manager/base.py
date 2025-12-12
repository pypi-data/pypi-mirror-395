"""
SQLAlchemy base classes and model utilities.

Provides:
- Base declarative class with naming conventions
- BaseModel with common fields (id, created_at, updated_at)
- Mixin classes for common patterns
"""

import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import MetaData, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# Standard naming conventions for constraints
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    """
    Base class for all database models.

    Features:
    - Standard naming conventions for indexes, constraints, and keys
    - Automatic table name generation from class name

    Usage:
        class User(Base):
            __tablename__ = "users"

            id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
            name: Mapped[str] = mapped_column(String(255))
    """

    metadata = MetaData(naming_convention=NAMING_CONVENTION)


class TimestampMixin:
    """
    Mixin that adds created_at and updated_at timestamps.

    Usage:
        class User(Base, TimestampMixin):
            __tablename__ = "users"
            id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class UUIDPrimaryKeyMixin:
    """
    Mixin that adds UUID primary key.

    Usage:
        class User(Base, UUIDPrimaryKeyMixin):
            __tablename__ = "users"
            name: Mapped[str] = mapped_column(String(255))
    """

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )


class SoftDeleteMixin:
    """
    Mixin for soft delete functionality.

    Usage:
        class User(Base, SoftDeleteMixin):
            __tablename__ = "users"

        # Soft delete
        user.deleted_at = datetime.utcnow()
        user.is_deleted = True
    """

    is_deleted: Mapped[bool] = mapped_column(default=False, nullable=False)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


class BaseModel(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """
    Abstract base model with common fields.

    Includes:
    - UUID primary key
    - created_at timestamp
    - updated_at timestamp (auto-updates)

    Usage:
        class User(BaseModel):
            __tablename__ = "users"

            name: Mapped[str] = mapped_column(String(255))
            email: Mapped[str] = mapped_column(String(255), unique=True)
    """

    __abstract__ = True

    def to_dict(self, exclude: set = None) -> Dict[str, Any]:
        """
        Convert model to dictionary.

        Args:
            exclude: Set of field names to exclude

        Returns:
            Dictionary representation of the model
        """
        exclude = exclude or set()
        result = {}

        for column in self.__table__.columns:
            if column.name in exclude:
                continue

            value = getattr(self, column.name)

            # Handle special types
            if isinstance(value, uuid.UUID):
                value = str(value)
            elif isinstance(value, datetime):
                value = value.isoformat()

            result[column.name] = value

        return result

    def update_from_dict(self, data: Dict[str, Any], exclude: set = None) -> None:
        """
        Update model from dictionary.

        Args:
            data: Dictionary with field values
            exclude: Set of field names to exclude from update
        """
        exclude = exclude or {"id", "created_at"}

        for key, value in data.items():
            if key in exclude:
                continue
            if hasattr(self, key):
                setattr(self, key, value)

    def __repr__(self) -> str:
        """Generate string representation."""
        class_name = self.__class__.__name__
        pk = getattr(self, "id", None)
        return f"<{class_name}(id={pk})>"
