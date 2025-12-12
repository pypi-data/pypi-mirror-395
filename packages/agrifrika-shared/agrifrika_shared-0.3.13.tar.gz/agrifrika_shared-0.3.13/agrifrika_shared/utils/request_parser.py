"""
Lambda event parsing utilities.

This module provides utilities for parsing API Gateway Lambda proxy events
into structured Python objects using Pydantic models.
"""

from typing import TypeVar, Type, Dict, Any, Optional
from pydantic import BaseModel, ValidationError
import json


T = TypeVar('T', bound=BaseModel)


def parse_lambda_event(event: Dict[str, Any], model: Type[T]) -> T:
    """
    Parse Lambda API Gateway event into Pydantic model.

    Handles:
    - Body parsing (JSON string or dict)
    - Path/query parameters merging
    - Cognito authorizer context

    Args:
        event: Lambda event dictionary
        model: Pydantic model class to parse into

    Returns:
        Parsed and validated model instance

    Raises:
        ValidationError: If payload doesn't match model schema
        json.JSONDecodeError: If body is not valid JSON

    Example:
        >>> from pydantic import BaseModel
        >>> class CreateUserRequest(BaseModel):
        ...     email: str
        ...     name: str
        >>> event = {'body': '{"email": "test@example.com", "name": "Test"}'}
        >>> request = parse_lambda_event(event, CreateUserRequest)
        >>> print(request.email)
        test@example.com
    """
    # Extract body
    body = event.get('body', {})
    if isinstance(body, str):
        body = json.loads(body) if body else {}
    elif body is None:
        body = {}

    # Merge path parameters (e.g., /users/{userId} -> {userId: '123'})
    path_params = event.get('pathParameters') or {}
    body.update(path_params)

    # Merge query string parameters
    query_params = event.get('queryStringParameters') or {}
    body.update(query_params)

    # Parse into model with validation
    return model(**body)


def parse_lambda_body(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse Lambda event body into a dictionary.

    Args:
        event: Lambda event dictionary

    Returns:
        Parsed body as dictionary

    Example:
        >>> event = {'body': '{"key": "value"}'}
        >>> body = parse_lambda_body(event)
        >>> print(body)
        {'key': 'value'}
    """
    body = event.get('body', {})
    if isinstance(body, str):
        return json.loads(body) if body else {}
    return body or {}


def get_auth_context(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract Cognito claims from Lambda authorizer context.

    Args:
        event: Lambda event dictionary

    Returns:
        Dictionary of Cognito claims (empty dict if not present)

    Example:
        >>> context = get_auth_context(event)
        >>> user_id = context.get('sub')
        >>> email = context.get('email')
    """
    return event.get('requestContext', {}).get('authorizer', {}).get('claims', {})


def get_user_id(event: Dict[str, Any]) -> Optional[str]:
    """
    Extract user ID (sub claim) from Cognito context.

    Args:
        event: Lambda event dictionary

    Returns:
        User ID string or None if not present
    """
    context = get_auth_context(event)
    return context.get('sub')


def get_path_parameter(event: Dict[str, Any], parameter: str) -> Optional[str]:
    """
    Extract a specific path parameter from the event.

    Args:
        event: Lambda event dictionary
        parameter: Name of the path parameter

    Returns:
        Parameter value or None if not present

    Example:
        >>> user_id = get_path_parameter(event, 'userId')
    """
    path_params = event.get('pathParameters') or {}
    return path_params.get(parameter)


def get_query_parameter(event: Dict[str, Any], parameter: str, default: Optional[str] = None) -> Optional[str]:
    """
    Extract a specific query string parameter from the event.

    Args:
        event: Lambda event dictionary
        parameter: Name of the query parameter
        default: Default value if parameter not present

    Returns:
        Parameter value or default

    Example:
        >>> page = get_query_parameter(event, 'page', '1')
        >>> limit = get_query_parameter(event, 'limit', '10')
    """
    query_params = event.get('queryStringParameters') or {}
    return query_params.get(parameter, default)


def get_header(event: Dict[str, Any], header: str, case_sensitive: bool = False) -> Optional[str]:
    """
    Extract a header value from the event.

    Args:
        event: Lambda event dictionary
        header: Header name
        case_sensitive: If False, performs case-insensitive lookup

    Returns:
        Header value or None if not present

    Example:
        >>> content_type = get_header(event, 'Content-Type')
        >>> auth_token = get_header(event, 'Authorization')
    """
    headers = event.get('headers', {}) or {}

    if case_sensitive:
        return headers.get(header)

    # Case-insensitive lookup
    header_lower = header.lower()
    for key, value in headers.items():
        if key.lower() == header_lower:
            return value
    return None


def extract_pagination(event: Dict[str, Any]) -> Dict[str, int]:
    """
    Extract pagination parameters from query string.

    Args:
        event: Lambda event dictionary

    Returns:
        Dictionary with 'page' and 'limit' keys

    Example:
        >>> pagination = extract_pagination(event)
        >>> page = pagination['page']  # defaults to 1
        >>> limit = pagination['limit']  # defaults to 20
    """
    page = int(get_query_parameter(event, 'page', '1'))
    limit = int(get_query_parameter(event, 'limit', '20'))

    # Enforce reasonable limits
    page = max(1, page)
    limit = max(1, min(limit, 100))  # Max 100 items per page

    return {
        'page': page,
        'limit': limit
    }
