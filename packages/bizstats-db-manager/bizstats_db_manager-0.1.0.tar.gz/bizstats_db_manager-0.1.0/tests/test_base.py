"""Tests for base model classes."""

import uuid
from datetime import datetime

import pytest
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from bizstats_db_manager.base import (
    Base,
    BaseModel,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
    SoftDeleteMixin,
    NAMING_CONVENTION,
)


class TestNamingConvention:
    """Tests for naming convention."""

    def test_naming_convention_keys(self):
        """Test all required keys are present."""
        assert "ix" in NAMING_CONVENTION  # index
        assert "uq" in NAMING_CONVENTION  # unique
        assert "ck" in NAMING_CONVENTION  # check
        assert "fk" in NAMING_CONVENTION  # foreign key
        assert "pk" in NAMING_CONVENTION  # primary key


class TestBase:
    """Tests for Base declarative class."""

    def test_metadata_naming_convention(self):
        """Test metadata has naming convention set."""
        assert Base.metadata.naming_convention == NAMING_CONVENTION


class TestTimestampMixin:
    """Tests for TimestampMixin."""

    def test_mixin_has_created_at(self):
        """Test mixin has created_at field."""
        assert hasattr(TimestampMixin, "created_at")

    def test_mixin_has_updated_at(self):
        """Test mixin has updated_at field."""
        assert hasattr(TimestampMixin, "updated_at")


class TestUUIDPrimaryKeyMixin:
    """Tests for UUIDPrimaryKeyMixin."""

    def test_mixin_has_id(self):
        """Test mixin has id field."""
        assert hasattr(UUIDPrimaryKeyMixin, "id")


class TestSoftDeleteMixin:
    """Tests for SoftDeleteMixin."""

    def test_mixin_has_is_deleted(self):
        """Test mixin has is_deleted field."""
        assert hasattr(SoftDeleteMixin, "is_deleted")

    def test_mixin_has_deleted_at(self):
        """Test mixin has deleted_at field."""
        assert hasattr(SoftDeleteMixin, "deleted_at")


class TestBaseModel:
    """Tests for BaseModel."""

    def test_model_is_abstract(self):
        """Test BaseModel is abstract."""
        assert BaseModel.__abstract__ is True

    def test_model_has_id(self):
        """Test model has UUID id field."""
        assert hasattr(BaseModel, "id")

    def test_model_has_timestamps(self):
        """Test model has timestamp fields."""
        assert hasattr(BaseModel, "created_at")
        assert hasattr(BaseModel, "updated_at")

    def test_to_dict(self):
        """Test to_dict method."""
        # Create a unique model class for this test
        class TestUserToDict(BaseModel):
            __tablename__ = "test_users_to_dict"
            __table_args__ = {"extend_existing": True}
            name: Mapped[str] = mapped_column(String(255))

        user = TestUserToDict()
        user.id = uuid.uuid4()
        user.name = "Test User"
        user.created_at = datetime(2024, 1, 1, 12, 0, 0)
        user.updated_at = datetime(2024, 1, 2, 12, 0, 0)

        d = user.to_dict()

        assert "id" in d
        assert d["name"] == "Test User"
        assert isinstance(d["id"], str)  # UUID converted to string
        assert "created_at" in d
        assert "updated_at" in d

    def test_to_dict_with_exclude(self):
        """Test to_dict with exclusions."""
        class TestUserExclude(BaseModel):
            __tablename__ = "test_users_exclude"
            __table_args__ = {"extend_existing": True}
            name: Mapped[str] = mapped_column(String(255))

        user = TestUserExclude()
        user.id = uuid.uuid4()
        user.name = "Test User"
        user.created_at = datetime(2024, 1, 1, 12, 0, 0)
        user.updated_at = datetime(2024, 1, 2, 12, 0, 0)

        d = user.to_dict(exclude={"created_at", "updated_at"})

        assert "created_at" not in d
        assert "updated_at" not in d
        assert "name" in d

    def test_update_from_dict(self):
        """Test update_from_dict method."""
        class TestUserUpdate(BaseModel):
            __tablename__ = "test_users_update"
            __table_args__ = {"extend_existing": True}
            name: Mapped[str] = mapped_column(String(255))

        user = TestUserUpdate()
        user.name = "Original"

        user.update_from_dict({"name": "Updated"})
        assert user.name == "Updated"

    def test_update_from_dict_excludes_id(self):
        """Test update_from_dict excludes id by default."""
        class TestUserExcludeId(BaseModel):
            __tablename__ = "test_users_exclude_id"
            __table_args__ = {"extend_existing": True}
            name: Mapped[str] = mapped_column(String(255))

        user = TestUserExcludeId()
        original_id = uuid.uuid4()
        user.id = original_id

        user.update_from_dict({"id": uuid.uuid4(), "name": "Test"})
        assert user.id == original_id

    def test_update_from_dict_excludes_created_at(self):
        """Test update_from_dict excludes created_at by default."""
        class TestUserExcludeCreated(BaseModel):
            __tablename__ = "test_users_exclude_created"
            __table_args__ = {"extend_existing": True}
            name: Mapped[str] = mapped_column(String(255))

        user = TestUserExcludeCreated()
        original_time = datetime(2024, 1, 1)
        user.created_at = original_time

        user.update_from_dict({"created_at": datetime(2025, 1, 1)})
        assert user.created_at == original_time

    def test_update_from_dict_ignores_unknown_fields(self):
        """Test update_from_dict ignores unknown fields."""
        class TestUserUnknown(BaseModel):
            __tablename__ = "test_users_unknown"
            __table_args__ = {"extend_existing": True}
            name: Mapped[str] = mapped_column(String(255))

        user = TestUserUnknown()
        user.name = "Original"

        # Should not raise
        user.update_from_dict({"unknown_field": "value", "name": "Updated"})
        assert user.name == "Updated"

    def test_repr(self):
        """Test __repr__ method."""
        class TestUserRepr(BaseModel):
            __tablename__ = "test_users_repr"
            __table_args__ = {"extend_existing": True}
            name: Mapped[str] = mapped_column(String(255))

        user = TestUserRepr()
        user.id = uuid.UUID("12345678-1234-5678-1234-567812345678")

        repr_str = repr(user)
        assert "TestUserRepr" in repr_str
        assert "12345678-1234-5678-1234-567812345678" in repr_str
