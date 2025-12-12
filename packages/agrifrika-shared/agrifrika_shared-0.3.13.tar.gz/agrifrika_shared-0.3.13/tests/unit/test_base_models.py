"""Tests for base Pydantic models."""

import pytest
from datetime import datetime, timezone, timedelta
from pydantic import ValidationError
from agrifrika_shared.models.base import (
    TimestampedModel,
    SoftDeleteModel,
    AuditedModel,
    PaginationParams,
    PaginatedResponse,
    StatusEnum,
)


@pytest.mark.unit
class TestTimestampedModel:
    """Tests for TimestampedModel base class."""

    def test_auto_generates_timestamps(self):
        """Test that timestamps are automatically generated."""
        class TestModel(TimestampedModel):
            name: str

        model = TestModel(name="test")

        assert model.created_at is not None
        assert model.updated_at is not None
        assert isinstance(model.created_at, datetime)
        assert isinstance(model.updated_at, datetime)

    def test_timestamps_are_utc(self):
        """Test that timestamps are in UTC timezone."""
        class TestModel(TimestampedModel):
            name: str

        model = TestModel(name="test")

        assert model.created_at.tzinfo is not None
        assert model.updated_at.tzinfo is not None

    def test_timestamps_can_be_provided(self):
        """Test that custom timestamps can be provided."""
        custom_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

        class TestModel(TimestampedModel):
            name: str

        model = TestModel(name="test", created_at=custom_time, updated_at=custom_time)

        assert model.created_at == custom_time
        assert model.updated_at == custom_time

    def test_json_serialization(self):
        """Test that model can be serialized to JSON."""
        class TestModel(TimestampedModel):
            name: str

        model = TestModel(name="test")
        json_data = model.model_dump()

        assert 'created_at' in json_data
        assert 'updated_at' in json_data
        assert json_data['name'] == 'test'


@pytest.mark.unit
class TestSoftDeleteModel:
    """Tests for SoftDeleteModel base class."""

    def test_not_deleted_by_default(self):
        """Test that models are not deleted by default."""
        class TestModel(SoftDeleteModel):
            name: str

        model = TestModel(name="test")

        assert model.is_deleted is False
        assert model.deleted_at is None

    def test_soft_delete(self):
        """Test soft delete functionality."""
        class TestModel(SoftDeleteModel):
            name: str

        model = TestModel(name="test")
        original_updated = model.updated_at

        # Small delay to ensure different timestamps
        import time
        time.sleep(0.01)

        model.soft_delete()

        assert model.is_deleted is True
        assert model.deleted_at is not None
        assert isinstance(model.deleted_at, datetime)
        assert model.updated_at > original_updated

    def test_restore(self):
        """Test restoring a soft-deleted model."""
        class TestModel(SoftDeleteModel):
            name: str

        model = TestModel(name="test")
        model.soft_delete()

        assert model.is_deleted is True
        assert model.deleted_at is not None

        model.restore()

        assert model.is_deleted is False
        assert model.deleted_at is None

    def test_restore_updates_timestamp(self):
        """Test that restore updates the updated_at timestamp."""
        class TestModel(SoftDeleteModel):
            name: str

        model = TestModel(name="test")
        model.soft_delete()
        updated_before_restore = model.updated_at

        import time
        time.sleep(0.01)

        model.restore()

        assert model.updated_at > updated_before_restore


@pytest.mark.unit
class TestAuditedModel:
    """Tests for AuditedModel base class."""

    def test_requires_created_by(self):
        """Test that created_by is required."""
        class TestModel(AuditedModel):
            name: str

        # Should fail without created_by
        with pytest.raises(ValidationError):
            TestModel(name="test")

    def test_created_by_is_set(self):
        """Test that created_by is properly set."""
        class TestModel(AuditedModel):
            name: str

        model = TestModel(name="test", created_by="user_123")

        assert model.created_by == "user_123"
        assert model.updated_by is None

    def test_update_audit_fields(self):
        """Test updating audit fields."""
        class TestModel(AuditedModel):
            name: str

        model = TestModel(name="test", created_by="user_123")
        original_updated = model.updated_at

        import time
        time.sleep(0.01)

        model.update_audit_fields("user_456")

        assert model.updated_by == "user_456"
        assert model.updated_at > original_updated

    def test_inherits_timestamps(self):
        """Test that AuditedModel inherits timestamp fields."""
        class TestModel(AuditedModel):
            name: str

        model = TestModel(name="test", created_by="user_123")

        assert model.created_at is not None
        assert model.updated_at is not None


@pytest.mark.unit
class TestPaginationParams:
    """Tests for PaginationParams model."""

    def test_default_values(self):
        """Test default pagination values."""
        params = PaginationParams()

        assert params.page == 1
        assert params.limit == 20

    def test_custom_values(self):
        """Test custom pagination values."""
        params = PaginationParams(page=3, limit=50)

        assert params.page == 3
        assert params.limit == 50

    def test_get_offset(self):
        """Test offset calculation."""
        params1 = PaginationParams(page=1, limit=20)
        assert params1.get_offset() == 0

        params2 = PaginationParams(page=2, limit=20)
        assert params2.get_offset() == 20

        params3 = PaginationParams(page=3, limit=10)
        assert params3.get_offset() == 20

    def test_validates_page_minimum(self):
        """Test that page must be at least 1."""
        with pytest.raises(ValidationError):
            PaginationParams(page=0)

        with pytest.raises(ValidationError):
            PaginationParams(page=-1)

    def test_validates_limit_minimum(self):
        """Test that limit must be at least 1."""
        with pytest.raises(ValidationError):
            PaginationParams(limit=0)

        with pytest.raises(ValidationError):
            PaginationParams(limit=-1)

    def test_validates_limit_maximum(self):
        """Test that limit cannot exceed 100."""
        with pytest.raises(ValidationError):
            PaginationParams(limit=101)

        with pytest.raises(ValidationError):
            PaginationParams(limit=200)

    def test_limit_100_is_valid(self):
        """Test that limit of 100 is valid (edge case)."""
        params = PaginationParams(limit=100)
        assert params.limit == 100


@pytest.mark.unit
class TestPaginatedResponse:
    """Tests for PaginatedResponse model."""

    def test_creates_from_items(self):
        """Test creating paginated response from items."""
        items = [{'id': '1'}, {'id': '2'}]

        response = PaginatedResponse.from_items(
            items=items,
            total=50,
            page=1,
            limit=20
        )

        assert response.items == items
        assert response.total == 50
        assert response.page == 1
        assert response.limit == 20
        assert response.total_pages == 3  # 50 items / 20 per page = 3 pages
        assert response.has_next is True
        assert response.has_prev is False

    def test_pagination_flags_first_page(self):
        """Test pagination flags on first page."""
        response = PaginatedResponse.from_items(
            items=[],
            total=100,
            page=1,
            limit=20
        )

        assert response.has_next is True
        assert response.has_prev is False

    def test_pagination_flags_middle_page(self):
        """Test pagination flags on middle page."""
        response = PaginatedResponse.from_items(
            items=[],
            total=100,
            page=3,
            limit=20
        )

        assert response.has_next is True
        assert response.has_prev is True

    def test_pagination_flags_last_page(self):
        """Test pagination flags on last page."""
        response = PaginatedResponse.from_items(
            items=[],
            total=100,
            page=5,
            limit=20
        )

        assert response.has_next is False
        assert response.has_prev is True

    def test_total_pages_calculation(self):
        """Test total pages calculation."""
        # 100 items, 20 per page = 5 pages
        response1 = PaginatedResponse.from_items([], 100, 1, 20)
        assert response1.total_pages == 5

        # 101 items, 20 per page = 6 pages (ceiling)
        response2 = PaginatedResponse.from_items([], 101, 1, 20)
        assert response2.total_pages == 6

        # 99 items, 20 per page = 5 pages (ceiling)
        response3 = PaginatedResponse.from_items([], 99, 1, 20)
        assert response3.total_pages == 5

    def test_empty_results(self):
        """Test paginated response with no items."""
        response = PaginatedResponse.from_items(
            items=[],
            total=0,
            page=1,
            limit=20
        )

        assert response.items == []
        assert response.total == 0
        assert response.total_pages == 0
        assert response.has_next is False
        assert response.has_prev is False

    def test_single_page_results(self):
        """Test paginated response with single page of results."""
        response = PaginatedResponse.from_items(
            items=[{'id': '1'}],
            total=10,
            page=1,
            limit=20
        )

        assert response.total_pages == 1
        assert response.has_next is False
        assert response.has_prev is False


@pytest.mark.unit
class TestStatusEnum:
    """Tests for StatusEnum base class."""

    def test_has_standard_statuses(self):
        """Test that StatusEnum has standard status values."""
        assert StatusEnum.ACTIVE == "active"
        assert StatusEnum.INACTIVE == "inactive"
        assert StatusEnum.PENDING == "pending"
        assert StatusEnum.DELETED == "deleted"

    def test_can_be_extended(self):
        """Test that StatusEnum can be extended by custom classes."""
        class CustomStatus(StatusEnum):
            ARCHIVED = "archived"
            DRAFT = "draft"

        assert CustomStatus.ACTIVE == "active"  # Inherited
        assert CustomStatus.ARCHIVED == "archived"  # Custom
        assert CustomStatus.DRAFT == "draft"  # Custom
