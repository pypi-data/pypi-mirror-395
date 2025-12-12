"""
Custom exception classes for business logic and validation errors.

These exceptions provide structured error handling across all services.
"""


class AgrifrikaException(Exception):
    """Base exception for all Agrifrika custom exceptions"""

    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class ValidationError(AgrifrikaException):
    """Raised when input validation fails"""

    def __init__(self, message: str, field: str = None):
        super().__init__(message, error_code='VALIDATION_ERROR')
        self.field = field


class BusinessError(AgrifrikaException):
    """Raised when business logic validation fails"""

    def __init__(self, message: str, error_code: str = 'BUSINESS_ERROR'):
        super().__init__(message, error_code=error_code)


class NotFoundError(AgrifrikaException):
    """Raised when a requested resource is not found"""

    def __init__(self, resource: str, identifier: str = None):
        message = f"{resource} not found"
        if identifier:
            message = f"{resource} with identifier '{identifier}' not found"
        super().__init__(message, error_code='NOT_FOUND')
        self.resource = resource
        self.identifier = identifier


class ConflictError(AgrifrikaException):
    """Raised when a resource already exists or conflicts with existing data"""

    def __init__(self, message: str, conflicting_field: str = None):
        super().__init__(message, error_code='CONFLICT')
        self.conflicting_field = conflicting_field


class UnauthorizedError(AgrifrikaException):
    """Raised when authentication is required but not provided or invalid"""

    def __init__(self, message: str = "Unauthorized access"):
        super().__init__(message, error_code='UNAUTHORIZED')


class ForbiddenError(AgrifrikaException):
    """Raised when user doesn't have permission to access a resource"""

    def __init__(self, message: str = "Access forbidden"):
        super().__init__(message, error_code='FORBIDDEN')


class ExternalServiceError(AgrifrikaException):
    """Raised when an external service (AWS, third-party API) fails"""

    def __init__(self, service: str, message: str, original_error: Exception = None):
        super().__init__(f"{service} error: {message}", error_code='EXTERNAL_SERVICE_ERROR')
        self.service = service
        self.original_error = original_error
