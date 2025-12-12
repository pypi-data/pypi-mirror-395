"""
Shared Pydantic models for all domains.
"""

from .base import (
    TimestampedModel,
    SoftDeleteModel,
    AuditedModel,
    PaginationParams,
    PaginatedResponse,
    StatusEnum,
)

from .common import (
    UserType,
    UserStatus,
    OrderStatus,
    PaymentStatus,
    Currency,
    Country,
    Address,
    ContactInfo,
    Money,
    ImageInfo,
    Coordinates,
    ErrorDetail,
)

__all__ = [
    # Base models
    "TimestampedModel",
    "SoftDeleteModel",
    "AuditedModel",
    "PaginationParams",
    "PaginatedResponse",
    "StatusEnum",
    # Common models
    "UserType",
    "UserStatus",
    "OrderStatus",
    "PaymentStatus",
    "Currency",
    "Country",
    "Address",
    "ContactInfo",
    "Money",
    "ImageInfo",
    "Coordinates",
    "ErrorDetail",
]
