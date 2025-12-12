"""Tests for common models and enums."""

import pytest
from pydantic import ValidationError
from agrifrika_shared.models.common import (
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


@pytest.mark.unit
class TestEnums:
    """Tests for enumeration types."""

    def test_user_type_values(self):
        """Test UserType enum values."""
        assert UserType.AGGREGATOR_ADMIN == "aggregator_admin"
        assert UserType.AGGREGATOR_USER == "aggregator_user"
        assert UserType.FARMER == "farmer"
        assert UserType.BUYER == "buyer"
        assert UserType.PLATFORM_ADMIN == "platform_admin"

    def test_user_status_values(self):
        """Test UserStatus enum values."""
        assert UserStatus.ACTIVE == "active"
        assert UserStatus.INACTIVE == "inactive"
        assert UserStatus.PENDING == "pending"
        assert UserStatus.SUSPENDED == "suspended"

    def test_order_status_values(self):
        """Test OrderStatus enum values."""
        assert OrderStatus.PENDING == "pending"
        assert OrderStatus.CONFIRMED == "confirmed"
        assert OrderStatus.PROCESSING == "processing"
        assert OrderStatus.SHIPPED == "shipped"
        assert OrderStatus.DELIVERED == "delivered"
        assert OrderStatus.CANCELLED == "cancelled"
        assert OrderStatus.REFUNDED == "refunded"

    def test_payment_status_values(self):
        """Test PaymentStatus enum values."""
        assert PaymentStatus.PENDING == "pending"
        assert PaymentStatus.PROCESSING == "processing"
        assert PaymentStatus.COMPLETED == "completed"
        assert PaymentStatus.FAILED == "failed"
        assert PaymentStatus.REFUNDED == "refunded"

    def test_currency_values(self):
        """Test Currency enum values."""
        assert Currency.XAF == "XAF"
        assert Currency.USD == "USD"
        assert Currency.EUR == "EUR"

    def test_country_values(self):
        """Test Country enum values."""
        assert Country.CAMEROON == "CM"


@pytest.mark.unit
class TestAddress:
    """Tests for Address model."""

    def test_create_minimal_address(self):
        """Test creating address with minimal required fields."""
        address = Address(city="Douala")

        assert address.city == "Douala"
        assert address.country == Country.CAMEROON
        assert address.street is None
        assert address.region is None
        assert address.postal_code is None
        assert address.coordinates is None

    def test_create_complete_address(self):
        """Test creating address with all fields."""
        address = Address(
            street="123 Main St",
            city="Yaoundé",
            region="Centre",
            postal_code="1234",
            country=Country.CAMEROON,
            coordinates={'lat': 3.848, 'lng': 11.502}
        )

        assert address.street == "123 Main St"
        assert address.city == "Yaoundé"
        assert address.region == "Centre"
        assert address.postal_code == "1234"
        assert address.country == Country.CAMEROON
        assert address.coordinates == {'lat': 3.848, 'lng': 11.502}

    def test_address_uses_enum_values(self):
        """Test that address serializes enum as value."""
        address = Address(city="Douala", country=Country.CAMEROON)

        # When dumped to dict, enum should be value not object
        data = address.model_dump()
        assert data['country'] == "CM"

    def test_address_missing_city(self):
        """Test that city is required."""
        with pytest.raises(ValidationError):
            Address()


@pytest.mark.unit
class TestContactInfo:
    """Tests for ContactInfo model."""

    def test_create_with_valid_email(self):
        """Test creating contact info with valid email."""
        contact = ContactInfo(email="test@example.com")

        assert contact.email == "test@example.com"

    def test_create_with_valid_phone(self):
        """Test creating contact info with valid phone."""
        contact = ContactInfo(phone="+237612345678")

        assert contact.phone == "+237612345678"

    def test_create_with_all_fields(self):
        """Test creating contact info with all fields."""
        contact = ContactInfo(
            email="test@example.com",
            phone="+237612345678",
            whatsapp="+237622345678",
            alternate_phone="+237699999999"
        )

        assert contact.email == "test@example.com"
        assert contact.phone == "+237612345678"
        assert contact.whatsapp == "+237622345678"
        assert contact.alternate_phone == "+237699999999"

    def test_validates_email_format(self):
        """Test that invalid email format is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            ContactInfo(email="invalid-email")

        assert "Invalid email format" in str(exc_info.value)

    def test_validates_phone_format(self):
        """Test that invalid phone format is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            ContactInfo(phone="invalid")

        assert "Invalid phone number format" in str(exc_info.value)

    def test_validates_whatsapp_format(self):
        """Test that invalid whatsapp format is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            ContactInfo(whatsapp="1")  # Too short - single digit

        assert "Invalid phone number format" in str(exc_info.value)

    def test_allows_none_values(self):
        """Test that None values are allowed for all fields."""
        contact = ContactInfo()

        assert contact.email is None
        assert contact.phone is None
        assert contact.whatsapp is None
        assert contact.alternate_phone is None


@pytest.mark.unit
class TestMoney:
    """Tests for Money model."""

    def test_create_money_with_xaf(self):
        """Test creating money with XAF currency."""
        money = Money(amount=1500.00, currency=Currency.XAF)

        assert money.amount == 1500.00
        assert money.currency == Currency.XAF

    def test_default_currency_is_xaf(self):
        """Test that default currency is XAF."""
        money = Money(amount=100.00)

        assert money.currency == Currency.XAF

    def test_create_money_with_usd(self):
        """Test creating money with USD currency."""
        money = Money(amount=50.00, currency=Currency.USD)

        assert money.amount == 50.00
        assert money.currency == Currency.USD

    def test_validates_non_negative_amount(self):
        """Test that negative amounts are rejected."""
        with pytest.raises(ValidationError):
            Money(amount=-10.00)

    def test_zero_amount_is_valid(self):
        """Test that zero amount is valid."""
        money = Money(amount=0.00)

        assert money.amount == 0.00

    def test_to_dict(self):
        """Test converting money to dictionary."""
        money = Money(amount=100.00, currency=Currency.USD)
        data = money.to_dict()

        assert data == {
            'amount': 100.00,
            'currency': Currency.USD
        }

    def test_uses_enum_values(self):
        """Test that currency is serialized as value."""
        money = Money(amount=100.00, currency=Currency.EUR)
        data = money.model_dump()

        assert data['currency'] == "EUR"


@pytest.mark.unit
class TestImageInfo:
    """Tests for ImageInfo model."""

    def test_create_minimal_image_info(self):
        """Test creating image info with minimal required fields."""
        image = ImageInfo(url="https://example.com/image.jpg")

        assert image.url == "https://example.com/image.jpg"
        assert image.thumbnail_url is None
        assert image.width is None
        assert image.height is None
        assert image.size_bytes is None
        assert image.alt_text is None

    def test_create_complete_image_info(self):
        """Test creating image info with all fields."""
        image = ImageInfo(
            url="https://example.com/image.jpg",
            thumbnail_url="https://example.com/thumb.jpg",
            width=1920,
            height=1080,
            size_bytes=524288,
            alt_text="Product image"
        )

        assert image.url == "https://example.com/image.jpg"
        assert image.thumbnail_url == "https://example.com/thumb.jpg"
        assert image.width == 1920
        assert image.height == 1080
        assert image.size_bytes == 524288
        assert image.alt_text == "Product image"

    def test_url_is_required(self):
        """Test that URL is required."""
        with pytest.raises(ValidationError):
            ImageInfo()


@pytest.mark.unit
class TestCoordinates:
    """Tests for Coordinates model."""

    def test_create_valid_coordinates(self):
        """Test creating valid GPS coordinates."""
        coords = Coordinates(lat=4.0511, lng=9.7679)

        assert coords.lat == 4.0511
        assert coords.lng == 9.7679

    def test_validates_latitude_range(self):
        """Test that latitude must be between -90 and 90."""
        # Valid edge cases
        Coordinates(lat=90, lng=0)
        Coordinates(lat=-90, lng=0)

        # Invalid cases
        with pytest.raises(ValidationError):
            Coordinates(lat=91, lng=0)

        with pytest.raises(ValidationError):
            Coordinates(lat=-91, lng=0)

    def test_validates_longitude_range(self):
        """Test that longitude must be between -180 and 180."""
        # Valid edge cases
        Coordinates(lat=0, lng=180)
        Coordinates(lat=0, lng=-180)

        # Invalid cases
        with pytest.raises(ValidationError):
            Coordinates(lat=0, lng=181)

        with pytest.raises(ValidationError):
            Coordinates(lat=0, lng=-181)

    def test_coordinates_are_required(self):
        """Test that both coordinates are required."""
        with pytest.raises(ValidationError):
            Coordinates(lat=4.0511)

        with pytest.raises(ValidationError):
            Coordinates(lng=9.7679)


@pytest.mark.unit
class TestErrorDetail:
    """Tests for ErrorDetail model."""

    def test_create_minimal_error_detail(self):
        """Test creating error detail with minimal fields."""
        error = ErrorDetail(
            code="VALIDATION_ERROR",
            message="Invalid input"
        )

        assert error.code == "VALIDATION_ERROR"
        assert error.message == "Invalid input"
        assert error.field is None
        assert error.details is None

    def test_create_error_with_field(self):
        """Test creating error detail with field."""
        error = ErrorDetail(
            code="VALIDATION_ERROR",
            message="Invalid email format",
            field="email"
        )

        assert error.code == "VALIDATION_ERROR"
        assert error.message == "Invalid email format"
        assert error.field == "email"

    def test_create_error_with_details(self):
        """Test creating error detail with additional details."""
        error = ErrorDetail(
            code="VALIDATION_ERROR",
            message="Multiple validation errors",
            details={
                'errors': [
                    {'field': 'email', 'reason': 'Invalid format'},
                    {'field': 'phone', 'reason': 'Too short'}
                ]
            }
        )

        assert error.code == "VALIDATION_ERROR"
        assert error.message == "Multiple validation errors"
        assert 'errors' in error.details
        assert len(error.details['errors']) == 2

    def test_code_and_message_are_required(self):
        """Test that code and message are required."""
        with pytest.raises(ValidationError):
            ErrorDetail(code="ERROR")

        with pytest.raises(ValidationError):
            ErrorDetail(message="Error message")


@pytest.mark.unit
class TestModelsIntegration:
    """Tests for integration between models."""

    def test_address_with_coordinates_object(self):
        """Test that Address can use Coordinates model."""
        coords = Coordinates(lat=4.0511, lng=9.7679)

        # Address accepts dict, so convert coordinates
        address = Address(
            city="Douala",
            coordinates=coords.model_dump()
        )

        assert address.coordinates['lat'] == 4.0511
        assert address.coordinates['lng'] == 9.7679

    def test_money_in_complex_model(self):
        """Test using Money model in complex scenarios."""
        from pydantic import BaseModel

        class Product(BaseModel):
            name: str
            price: Money

        product = Product(
            name="Banana",
            price=Money(amount=500.00, currency=Currency.XAF)
        )

        assert product.price.amount == 500.00
        assert product.price.currency == Currency.XAF
