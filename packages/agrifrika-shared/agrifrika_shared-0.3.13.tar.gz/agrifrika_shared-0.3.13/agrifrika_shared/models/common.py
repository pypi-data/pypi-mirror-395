"""
Common models and enums shared across all domains.
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from agrifrika_shared.utils.validators import validate_email, validate_phone


class UserType(str, Enum):
    """User type enumeration"""
    AGGREGATOR_ADMIN = "aggregator_admin"
    AGGREGATOR_USER = "aggregator_user"
    FARMER = "farmer"
    BUYER = "buyer"
    PLATFORM_ADMIN = "platform_admin"


class UserStatus(str, Enum):
    """User status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    SUSPENDED = "suspended"


class OrderStatus(str, Enum):
    """Order status enumeration"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class PaymentStatus(str, Enum):
    """Payment status enumeration"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class Currency(str, Enum):
    """Supported currencies"""
    XAF = "XAF"  # Central African CFA franc
    USD = "USD"
    EUR = "EUR"


class Country(str, Enum):
    """Supported countries"""
    CAMEROON = "CM"
    # Add more as needed


class Address(BaseModel):
    """
    Standard address model.

    Example:
        >>> address = Address(
        ...     street="123 Main St",
        ...     city="Douala",
        ...     region="Littoral",
        ...     country=Country.CAMEROON
        ... )
    """
    street: Optional[str] = None
    city: str
    region: Optional[str] = None
    postal_code: Optional[str] = None
    country: Country = Country.CAMEROON
    coordinates: Optional[dict] = Field(
        None,
        description="GPS coordinates {lat: float, lng: float}"
    )

    class Config:
        use_enum_values = True


class ContactInfo(BaseModel):
    """
    Standard contact information model.

    Example:
        >>> contact = ContactInfo(
        ...     email="test@example.com",
        ...     phone="+237612345678",
        ...     whatsapp="+237612345678"
        ... )
    """
    email: Optional[str] = None
    phone: Optional[str] = None
    whatsapp: Optional[str] = None
    alternate_phone: Optional[str] = None

    @field_validator('email')
    @classmethod
    def validate_email_field(cls, v):
        if v and not validate_email(v):
            raise ValueError('Invalid email format')
        return v

    @field_validator('phone', 'whatsapp', 'alternate_phone')
    @classmethod
    def validate_phone_field(cls, v):
        if v and not validate_phone(v):
            raise ValueError('Invalid phone number format')
        return v


class Money(BaseModel):
    """
    Money value with currency.

    Example:
        >>> price = Money(amount=1500.00, currency=Currency.XAF)
        >>> print(f"{price.amount} {price.currency}")
    """
    amount: float = Field(..., ge=0, description="Amount (must be non-negative)")
    currency: Currency = Currency.XAF

    class Config:
        use_enum_values = True

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'amount': self.amount,
            'currency': self.currency
        }


class ImageInfo(BaseModel):
    """
    Image metadata model.

    Example:
        >>> image = ImageInfo(
        ...     url="https://s3.amazonaws.com/bucket/image.jpg",
        ...     thumbnail_url="https://s3.amazonaws.com/bucket/thumb.jpg",
        ...     width=1920,
        ...     height=1080
        ... )
    """
    url: str
    thumbnail_url: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    size_bytes: Optional[int] = None
    alt_text: Optional[str] = None


class Coordinates(BaseModel):
    """
    GPS coordinates model.

    Example:
        >>> coords = Coordinates(lat=4.0511, lng=9.7679)  # Douala
    """
    lat: float = Field(..., ge=-90, le=90, description="Latitude")
    lng: float = Field(..., ge=-180, le=180, description="Longitude")

    class Config:
        json_schema_extra = {
            "example": {
                "lat": 4.0511,
                "lng": 9.7679
            }
        }


class ErrorDetail(BaseModel):
    """
    Standard error detail model for API responses.

    Example:
        >>> error = ErrorDetail(
        ...     code="VALIDATION_ERROR",
        ...     message="Invalid email format",
        ...     field="email"
        ... )
    """
    code: str
    message: str
    field: Optional[str] = None
    details: Optional[dict] = None
