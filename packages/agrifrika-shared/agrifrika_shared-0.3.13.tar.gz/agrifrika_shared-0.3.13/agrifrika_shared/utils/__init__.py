"""
Shared utility functions.
"""

from .request_parser import (
    parse_lambda_event,
    parse_lambda_body,
    get_auth_context,
    get_user_id,
    get_path_parameter,
    get_query_parameter,
    get_header,
    extract_pagination,
)

from .response_builder import (
    ResponseBuilder,
    success_response,
    error_response,
    unauthorized_response,
    not_found_response,
    internal_error_response,
    validation_error_response,
    success_with_etag,
    list_response_with_etag,
    cors_response,
)

from .logger import (
    StructuredLogger,
    logger,
    get_logger,
)

from .exceptions import (
    AgrifrikaException,
    ValidationError,
    BusinessError,
    NotFoundError,
    ConflictError,
    UnauthorizedError,
    ForbiddenError,
    ExternalServiceError,
)

from .validators import (
    validate_email,
    validate_phone,
    validate_url,
    validate_uuid,
    sanitize_string,
    validate_password_strength,
)

__all__ = [
    # Request parser
    "parse_lambda_event",
    "parse_lambda_body",
    "get_auth_context",
    "get_user_id",
    "get_path_parameter",
    "get_query_parameter",
    "get_header",
    "extract_pagination",
    # Response builder
    "ResponseBuilder",
    "success_response",
    "error_response",
    "unauthorized_response",
    "not_found_response",
    "internal_error_response",
    "validation_error_response",
    "success_with_etag",
    "list_response_with_etag",
    "cors_response",
    # Logger
    "StructuredLogger",
    "logger",
    "get_logger",
    # Exceptions
    "AgrifrikaException",
    "ValidationError",
    "BusinessError",
    "NotFoundError",
    "ConflictError",
    "UnauthorizedError",
    "ForbiddenError",
    "ExternalServiceError",
    # Validators
    "validate_email",
    "validate_phone",
    "validate_url",
    "validate_uuid",
    "sanitize_string",
    "validate_password_strength",
]
