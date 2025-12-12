"""
Base Pydantic models for common patterns.

These base models provide common fields and functionality
that can be inherited by domain models.
"""

from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class TimestampedModel(BaseModel):
    """
    Base model with timestamp fields.

    Automatically manages created_at and updated_at fields.

    Example:
        >>> class User(TimestampedModel):
        ...     name: str
        ...     email: str
        >>> user = User(name="John", email="john@example.com")
        >>> print(user.created_at)  # Auto-generated
    """

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        # Allow validation on assignment
        validate_assignment = True
        # Use enum values instead of enum objects
        use_enum_values = True
        # Serialize datetime as ISO format
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class SoftDeleteModel(TimestampedModel):
    """
    Base model with soft delete support.

    Adds is_deleted and deleted_at fields for soft deletion.

    Example:
        >>> class Product(SoftDeleteModel):
        ...     name: str
        ...     price: float
        >>> product = Product(name="Apple", price=1.99)
        >>> product.is_deleted  # False by default
        >>> product.soft_delete()
        >>> product.is_deleted  # True now
    """

    is_deleted: bool = Field(default=False)
    deleted_at: Optional[datetime] = None

    def soft_delete(self):
        """Mark the entity as deleted"""
        self.is_deleted = True
        self.deleted_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    def restore(self):
        """Restore a soft-deleted entity"""
        self.is_deleted = False
        self.deleted_at = None
        self.updated_at = datetime.now(timezone.utc)


class AuditedModel(TimestampedModel):
    """
    Base model with audit fields.

    Tracks who created and last updated the entity.

    Example:
        >>> class Order(AuditedModel):
        ...     amount: float
        ...     status: str
        >>> order = Order(amount=99.99, status="pending", created_by="user_123")
    """

    created_by: str
    updated_by: Optional[str] = None

    def update_audit_fields(self, user_id: str):
        """Update audit fields when entity is modified"""
        self.updated_by = user_id
        self.updated_at = datetime.now(timezone.utc)


class PaginationParams(BaseModel):
    """
    Standard pagination parameters.

    Example:
        >>> params = PaginationParams(page=2, limit=20)
        >>> offset = params.get_offset()  # 20
    """

    page: int = Field(default=1, ge=1, description="Page number (1-indexed)")
    limit: int = Field(default=20, ge=1, le=100, description="Items per page (max 100)")

    def get_offset(self) -> int:
        """Calculate offset for database queries"""
        return (self.page - 1) * self.limit

    @field_validator('page')
    @classmethod
    def validate_page(cls, v):
        if v < 1:
            raise ValueError('Page must be >= 1')
        return v

    @field_validator('limit')
    @classmethod
    def validate_limit(cls, v):
        if v < 1:
            raise ValueError('Limit must be >= 1')
        if v > 100:
            raise ValueError('Limit must be <= 100')
        return v


class PaginatedResponse(BaseModel):
    """
    Standard paginated response wrapper.

    Example:
        >>> items = [{"id": "1", "name": "Item 1"}]
        >>> response = PaginatedResponse(
        ...     items=items,
        ...     total=100,
        ...     page=1,
        ...     limit=20,
        ...     total_pages=5
        ... )
    """

    items: list
    total: int = Field(description="Total number of items")
    page: int = Field(description="Current page number")
    limit: int = Field(description="Items per page")
    total_pages: int = Field(description="Total number of pages")
    has_next: bool = Field(description="Whether there are more pages")
    has_prev: bool = Field(description="Whether there are previous pages")

    @classmethod
    def from_items(cls, items: list, total: int, page: int, limit: int):
        """
        Create paginated response from items and pagination info.

        Args:
            items: List of items for current page
            total: Total number of items across all pages
            page: Current page number
            limit: Items per page

        Returns:
            PaginatedResponse instance
        """
        total_pages = (total + limit - 1) // limit  # Ceiling division

        return cls(
            items=items,
            total=total,
            page=page,
            limit=limit,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_prev=page > 1
        )


class StatusEnum:
    """
    Base class for status enums.

    Provides common status values that can be inherited.
    """
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    DELETED = "deleted"
