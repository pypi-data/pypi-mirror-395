"""Tests for service patterns."""

import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

from bizstats_db_manager.service import (
    ServiceResult,
    PaginatedResult,
    PaginationParams,
    BaseService,
    SingletonService,
)


class TestServiceResult:
    """Tests for ServiceResult."""

    def test_ok_result(self):
        """Test creating successful result."""
        result = ServiceResult.ok(data={"id": 123})

        assert result.success is True
        assert result.data == {"id": 123}
        assert result.error_message is None
        assert result.error_code is None

    def test_ok_result_with_details(self):
        """Test successful result with additional details."""
        result = ServiceResult.ok(data="test", extra="value")

        assert result.success is True
        assert result.data == "test"
        assert result.details == {"extra": "value"}

    def test_error_result(self):
        """Test creating error result."""
        result = ServiceResult.fail("Something went wrong", code="ERR_001")

        assert result.success is False
        assert result.error_message == "Something went wrong"
        assert result.error_code == "ERR_001"
        assert result.data is None

    def test_error_result_with_details(self):
        """Test error result with additional details."""
        result = ServiceResult.fail("Error", field="email")

        assert result.success is False
        assert result.details == {"field": "email"}

    def test_to_dict_success(self):
        """Test converting successful result to dict."""
        result = ServiceResult.ok(data={"name": "test"})
        d = result.to_dict()

        assert d["success"] is True
        assert d["data"] == {"name": "test"}
        assert "timestamp" in d
        assert "error" not in d

    def test_to_dict_error(self):
        """Test converting error result to dict."""
        result = ServiceResult.fail("Failed", code="ERR")
        d = result.to_dict()

        assert d["success"] is False
        assert d["error"] == "Failed"
        assert d["error_code"] == "ERR"
        assert "data" not in d

    def test_bool_conversion(self):
        """Test boolean conversion."""
        success = ServiceResult.ok(data="test")
        failure = ServiceResult.fail("error")

        assert bool(success) is True
        assert bool(failure) is False

    def test_timestamp_auto_set(self):
        """Test timestamp is automatically set."""
        result = ServiceResult.ok()
        assert isinstance(result.timestamp, datetime)


class TestPaginatedResult:
    """Tests for PaginatedResult."""

    def test_basic_pagination(self):
        """Test basic pagination result."""
        result = PaginatedResult(
            items=[1, 2, 3],
            total=100,
            page=1,
            page_size=20,
        )

        assert len(result.items) == 3
        assert result.total == 100
        assert result.page == 1
        assert result.page_size == 20

    def test_total_pages(self):
        """Test total pages calculation."""
        result = PaginatedResult(items=[], total=100, page=1, page_size=20)
        assert result.total_pages == 5

        result2 = PaginatedResult(items=[], total=101, page=1, page_size=20)
        assert result2.total_pages == 6

        result3 = PaginatedResult(items=[], total=0, page=1, page_size=20)
        assert result3.total_pages == 0

    def test_total_pages_zero_page_size(self):
        """Test total pages with zero page size."""
        result = PaginatedResult(items=[], total=100, page=1, page_size=0)
        assert result.total_pages == 0

    def test_has_previous(self):
        """Test has_previous property."""
        first_page = PaginatedResult(items=[], total=100, page=1, page_size=20)
        second_page = PaginatedResult(items=[], total=100, page=2, page_size=20)

        assert first_page.has_previous is False
        assert second_page.has_previous is True

    def test_has_next(self):
        """Test has_next property."""
        middle_page = PaginatedResult(items=[], total=100, page=3, page_size=20)
        last_page = PaginatedResult(items=[], total=100, page=5, page_size=20)

        assert middle_page.has_next is True
        assert last_page.has_next is False

    def test_to_dict(self):
        """Test to_dict conversion."""
        result = PaginatedResult(
            items=[{"id": 1}, {"id": 2}],
            total=50,
            page=2,
            page_size=10,
            has_more=True,
        )
        d = result.to_dict()

        assert d["items"] == [{"id": 1}, {"id": 2}]
        assert d["pagination"]["total"] == 50
        assert d["pagination"]["page"] == 2
        assert d["pagination"]["page_size"] == 10
        assert d["pagination"]["total_pages"] == 5
        assert d["pagination"]["has_more"] is True
        assert d["pagination"]["has_previous"] is True
        assert d["pagination"]["has_next"] is True


class TestPaginationParams:
    """Tests for PaginationParams."""

    def test_default_values(self):
        """Test default pagination values."""
        params = PaginationParams()
        assert params.page == 1
        assert params.page_size == 20

    def test_offset_calculation(self):
        """Test offset calculation."""
        params1 = PaginationParams(page=1, page_size=20)
        assert params1.offset == 0

        params2 = PaginationParams(page=3, page_size=20)
        assert params2.offset == 40

        params3 = PaginationParams(page=5, page_size=10)
        assert params3.offset == 40

    def test_limit_property(self):
        """Test limit property."""
        params = PaginationParams(page=1, page_size=25)
        assert params.limit == 25

    def test_validate(self):
        """Test validation and clamping."""
        params = PaginationParams(page=-1, page_size=200)
        validated = params.validate(max_page_size=100)

        assert validated.page == 1
        assert validated.page_size == 100

    def test_validate_zero_values(self):
        """Test validation with zero values."""
        params = PaginationParams(page=0, page_size=0)
        validated = params.validate()

        assert validated.page == 1
        assert validated.page_size == 1


class TestBaseService:
    """Tests for BaseService."""

    @pytest.fixture
    def mock_db(self):
        """Create mock database session."""
        db = AsyncMock()
        db.execute = AsyncMock()
        db.commit = AsyncMock()
        db.rollback = AsyncMock()
        db.refresh = AsyncMock()
        return db

    @pytest.fixture
    def service(self, mock_db):
        """Create test service."""
        class TestService(BaseService):
            pass
        return TestService(mock_db)

    def test_init(self, service, mock_db):
        """Test service initialization."""
        assert service.db == mock_db
        assert service.logger is not None

    @pytest.mark.asyncio
    async def test_execute_query(self, service, mock_db):
        """Test query execution."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = {"id": 1}
        mock_db.execute.return_value = mock_result

        result = await service._execute_query("SELECT 1")
        assert result == {"id": 1}

    @pytest.mark.asyncio
    async def test_execute_query_all(self, service, mock_db):
        """Test query execution returning all results."""
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [1, 2, 3]
        mock_db.execute.return_value = mock_result

        result = await service._execute_query_all("SELECT *")
        assert result == [1, 2, 3]

    @pytest.mark.asyncio
    async def test_execute_query_first(self, service, mock_db):
        """Test query execution returning first result."""
        mock_result = MagicMock()
        mock_result.scalars.return_value.first.return_value = {"id": 1}
        mock_db.execute.return_value = mock_result

        result = await service._execute_query_first("SELECT *")
        assert result == {"id": 1}

    @pytest.mark.asyncio
    async def test_commit_success(self, service, mock_db):
        """Test successful commit."""
        result = await service._commit()
        assert result is True
        mock_db.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_commit_failure(self, service, mock_db):
        """Test commit failure with rollback."""
        mock_db.commit.side_effect = Exception("DB error")

        result = await service._commit()
        assert result is False
        mock_db.rollback.assert_called_once()

    @pytest.mark.asyncio
    async def test_refresh(self, service, mock_db):
        """Test instance refresh."""
        instance = MagicMock()
        await service._refresh(instance)
        mock_db.refresh.assert_called_once_with(instance)


class TestSingletonService:
    """Tests for SingletonService."""

    def test_singleton_pattern(self):
        """Test singleton pattern."""
        class MySingleton(SingletonService):
            _instance = None

        instance1 = MySingleton()
        instance2 = MySingleton()

        assert instance1 is instance2

    def test_get_instance(self):
        """Test get_instance class method."""
        class MySingleton(SingletonService):
            _instance = None

        instance1 = MySingleton.get_instance()
        instance2 = MySingleton.get_instance()

        assert instance1 is instance2

    def test_reset_instance(self):
        """Test reset_instance class method."""
        class MySingleton(SingletonService):
            _instance = None

        instance1 = MySingleton()
        MySingleton.reset_instance()
        instance2 = MySingleton()

        assert instance1 is not instance2
