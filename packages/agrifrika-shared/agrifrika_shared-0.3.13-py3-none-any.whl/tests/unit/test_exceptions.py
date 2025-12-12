"""Tests for custom exception classes."""

import pytest
from agrifrika_shared.utils.exceptions import (
    AgrifrikaException,
    ValidationError,
    BusinessError,
    NotFoundError,
    ConflictError,
    UnauthorizedError,
    ForbiddenError,
    ExternalServiceError,
)


@pytest.mark.unit
class TestAgrifrikaException:
    """Tests for base AgrifrikaException class."""

    def test_exception_with_message_only(self):
        """Test creating exception with just a message."""
        exc = AgrifrikaException("Test error")
        assert exc.message == "Test error"
        assert exc.error_code is None
        assert str(exc) == "Test error"

    def test_exception_with_message_and_code(self):
        """Test creating exception with message and error code."""
        exc = AgrifrikaException("Test error", error_code="TEST_ERROR")
        assert exc.message == "Test error"
        assert exc.error_code == "TEST_ERROR"

    def test_exception_is_raisable(self):
        """Test that exception can be raised and caught."""
        with pytest.raises(AgrifrikaException) as exc_info:
            raise AgrifrikaException("Test error")

        assert exc_info.value.message == "Test error"


@pytest.mark.unit
class TestValidationError:
    """Tests for ValidationError exception."""

    def test_validation_error_with_message(self):
        """Test validation error with just a message."""
        exc = ValidationError("Invalid input")
        assert exc.message == "Invalid input"
        assert exc.error_code == "VALIDATION_ERROR"
        assert exc.field is None

    def test_validation_error_with_field(self):
        """Test validation error with field specified."""
        exc = ValidationError("Email is invalid", field="email")
        assert exc.message == "Email is invalid"
        assert exc.field == "email"
        assert exc.error_code == "VALIDATION_ERROR"

    def test_validation_error_inheritance(self):
        """Test that ValidationError inherits from AgrifrikaException."""
        exc = ValidationError("Test")
        assert isinstance(exc, AgrifrikaException)
        assert isinstance(exc, Exception)


@pytest.mark.unit
class TestBusinessError:
    """Tests for BusinessError exception."""

    def test_business_error_default_code(self):
        """Test business error with default error code."""
        exc = BusinessError("Business rule violated")
        assert exc.message == "Business rule violated"
        assert exc.error_code == "BUSINESS_ERROR"

    def test_business_error_custom_code(self):
        """Test business error with custom error code."""
        exc = BusinessError("Insufficient balance", error_code="INSUFFICIENT_BALANCE")
        assert exc.message == "Insufficient balance"
        assert exc.error_code == "INSUFFICIENT_BALANCE"


@pytest.mark.unit
class TestNotFoundError:
    """Tests for NotFoundError exception."""

    def test_not_found_error_resource_only(self):
        """Test not found error with just resource name."""
        exc = NotFoundError("User")
        assert exc.message == "User not found"
        assert exc.resource == "User"
        assert exc.identifier is None
        assert exc.error_code == "NOT_FOUND"

    def test_not_found_error_with_identifier(self):
        """Test not found error with resource and identifier."""
        exc = NotFoundError("Product", identifier="prod-123")
        assert exc.message == "Product with identifier 'prod-123' not found"
        assert exc.resource == "Product"
        assert exc.identifier == "prod-123"

    def test_not_found_error_inheritance(self):
        """Test that NotFoundError inherits from AgrifrikaException."""
        exc = NotFoundError("Item")
        assert isinstance(exc, AgrifrikaException)


@pytest.mark.unit
class TestConflictError:
    """Tests for ConflictError exception."""

    def test_conflict_error_basic(self):
        """Test basic conflict error."""
        exc = ConflictError("Resource already exists")
        assert exc.message == "Resource already exists"
        assert exc.error_code == "CONFLICT"
        assert exc.conflicting_field is None

    def test_conflict_error_with_field(self):
        """Test conflict error with conflicting field."""
        exc = ConflictError("Email already exists", conflicting_field="email")
        assert exc.message == "Email already exists"
        assert exc.conflicting_field == "email"


@pytest.mark.unit
class TestUnauthorizedError:
    """Tests for UnauthorizedError exception."""

    def test_unauthorized_error_default_message(self):
        """Test unauthorized error with default message."""
        exc = UnauthorizedError()
        assert exc.message == "Unauthorized access"
        assert exc.error_code == "UNAUTHORIZED"

    def test_unauthorized_error_custom_message(self):
        """Test unauthorized error with custom message."""
        exc = UnauthorizedError("Invalid token")
        assert exc.message == "Invalid token"
        assert exc.error_code == "UNAUTHORIZED"


@pytest.mark.unit
class TestForbiddenError:
    """Tests for ForbiddenError exception."""

    def test_forbidden_error_default_message(self):
        """Test forbidden error with default message."""
        exc = ForbiddenError()
        assert exc.message == "Access forbidden"
        assert exc.error_code == "FORBIDDEN"

    def test_forbidden_error_custom_message(self):
        """Test forbidden error with custom message."""
        exc = ForbiddenError("Insufficient permissions")
        assert exc.message == "Insufficient permissions"
        assert exc.error_code == "FORBIDDEN"


@pytest.mark.unit
class TestExternalServiceError:
    """Tests for ExternalServiceError exception."""

    def test_external_service_error_basic(self):
        """Test external service error without original error."""
        exc = ExternalServiceError("DynamoDB", "Connection timeout")
        assert exc.message == "DynamoDB error: Connection timeout"
        assert exc.service == "DynamoDB"
        assert exc.error_code == "EXTERNAL_SERVICE_ERROR"
        assert exc.original_error is None

    def test_external_service_error_with_original(self):
        """Test external service error with original exception."""
        original = ValueError("Invalid value")
        exc = ExternalServiceError("S3", "Upload failed", original_error=original)

        assert exc.message == "S3 error: Upload failed"
        assert exc.service == "S3"
        assert exc.original_error is original

    def test_external_service_error_inheritance(self):
        """Test that ExternalServiceError inherits from AgrifrikaException."""
        exc = ExternalServiceError("AWS", "Service unavailable")
        assert isinstance(exc, AgrifrikaException)


@pytest.mark.unit
class TestExceptionChaining:
    """Tests for exception chaining and handling."""

    def test_can_catch_specific_exception(self):
        """Test that specific exceptions can be caught."""
        with pytest.raises(NotFoundError):
            raise NotFoundError("User")

    def test_can_catch_base_exception(self):
        """Test that base class can catch derived exceptions."""
        with pytest.raises(AgrifrikaException):
            raise ValidationError("Invalid")

    def test_exception_info_available(self):
        """Test that exception info is accessible in except block."""
        try:
            raise NotFoundError("Product", "123")
        except NotFoundError as e:
            assert e.resource == "Product"
            assert e.identifier == "123"
            assert e.error_code == "NOT_FOUND"
