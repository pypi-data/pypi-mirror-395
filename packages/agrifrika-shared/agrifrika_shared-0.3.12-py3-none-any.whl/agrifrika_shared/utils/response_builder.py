"""
Standard response builders for Lambda API Gateway handlers.

This module provides a consistent interface for building HTTP responses
with proper CORS headers, error handling, and JSON encoding.
"""

import json
import hashlib
from decimal import Decimal
from typing import Any, Dict, Optional, Union
from datetime import datetime


class DecimalEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles Decimal and datetime types"""

    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        elif isinstance(obj, datetime):
            return obj.isoformat()
        return super(DecimalEncoder, self).default(obj)


class ResponseBuilder:
    """Utility class for building standardized API responses"""

    @staticmethod
    def _build_response(
        status_code: int,
        body: Union[Dict, str],
        headers: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Build a standardized response with common headers"""
        default_headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Amz-Date, X-Api-Key, X-Amz-Security-Token'
        }

        if headers:
            default_headers.update(headers)

        return {
            'statusCode': status_code,
            'body': json.dumps(body, cls=DecimalEncoder) if isinstance(body, dict) else body,
            'headers': default_headers
        }

    @staticmethod
    def success(data: Any = None, message: str = "Success", status_code: int = 200) -> Dict[str, Any]:
        """Build a success response"""
        body = {'message': message}
        if data is not None:
            body['data'] = data
        return ResponseBuilder._build_response(status_code, body)

    @staticmethod
    def created(data: Any = None, message: str = "Created successfully") -> Dict[str, Any]:
        """Build a 201 Created response"""
        return ResponseBuilder.success(data, message, 201)

    @staticmethod
    def error(message: str, status_code: int = 400, error_code: Optional[str] = None, details: Optional[Dict] = None) -> Dict[str, Any]:
        """Build an error response"""
        body = {'message': message}
        if error_code:
            body['error_code'] = error_code
        if details:
            body['details'] = details
        return ResponseBuilder._build_response(status_code, body)

    @staticmethod
    def bad_request(message: str, error_code: Optional[str] = None) -> Dict[str, Any]:
        """Build a 400 Bad Request response"""
        return ResponseBuilder.error(message, 400, error_code)

    @staticmethod
    def unauthorized(message: str = "Unauthorized") -> Dict[str, Any]:
        """Build a 401 Unauthorized response"""
        return ResponseBuilder.error(message, 401)

    @staticmethod
    def forbidden(message: str = "Forbidden") -> Dict[str, Any]:
        """Build a 403 Forbidden response"""
        return ResponseBuilder.error(message, 403)

    @staticmethod
    def not_found(message: str = "Resource not found") -> Dict[str, Any]:
        """Build a 404 Not Found response"""
        return ResponseBuilder.error(message, 404)

    @staticmethod
    def conflict(message: str = "Conflict") -> Dict[str, Any]:
        """Build a 409 Conflict response"""
        return ResponseBuilder.error(message, 409)

    @staticmethod
    def internal_error(message: str = "Internal server error", error_details: Optional[str] = None) -> Dict[str, Any]:
        """Build a 500 Internal Server Error response"""
        body = {'message': message}
        if error_details:
            body['error_details'] = error_details
        return ResponseBuilder._build_response(500, body)

    @staticmethod
    def validation_error(field: str, message: str) -> Dict[str, Any]:
        """Build a validation error response"""
        return ResponseBuilder.bad_request(f"Validation error for field '{field}': {message}")

    @staticmethod
    def missing_field(field: str) -> Dict[str, Any]:
        """Build a missing field error response"""
        return ResponseBuilder.bad_request(f"Missing required field: {field}")

    @staticmethod
    def list_response(items: list, count: Optional[int] = None, pagination: Optional[Dict] = None) -> Dict[str, Any]:
        """Build a list response with optional pagination"""
        data = {'items': items}
        if count is not None:
            data['count'] = count
        if pagination:
            data['pagination'] = pagination
        return ResponseBuilder.success(data, "Retrieved successfully")

    @staticmethod
    def cors_response() -> Dict[str, Any]:
        """Build a CORS preflight response"""
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Amz-Date, X-Api-Key, X-Amz-Security-Token',
                'Access-Control-Max-Age': '86400'
            },
            'body': ''
        }

    @staticmethod
    def generate_etag(data: Any) -> str:
        """Generate an ETag from response data using MD5 hash"""
        json_string = json.dumps(data, sort_keys=True, cls=DecimalEncoder)
        etag = hashlib.md5(json_string.encode('utf-8')).hexdigest()
        return f'"{etag}"'

    @staticmethod
    def extract_if_none_match(event: Dict) -> Optional[str]:
        """Extract If-None-Match header from Lambda event"""
        headers = event.get('headers', {}) or {}
        return headers.get('If-None-Match') or headers.get('if-none-match')

    @staticmethod
    def not_modified(etag: str) -> Dict[str, Any]:
        """Build a 304 Not Modified response"""
        return {
            'statusCode': 304,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Amz-Date, X-Api-Key, X-Amz-Security-Token',
                'ETag': etag,
                'Cache-Control': 'no-cache'
            },
            'body': ''
        }

    @staticmethod
    def success_with_etag(data: Any, event: Dict, message: str = "Success") -> Dict[str, Any]:
        """Build a success response with ETag support"""
        etag = ResponseBuilder.generate_etag(data)
        client_etag = ResponseBuilder.extract_if_none_match(event)
        if client_etag and client_etag == etag:
            return ResponseBuilder.not_modified(etag)

        body = {'message': message, 'data': data}
        headers = {'ETag': etag, 'Cache-Control': 'no-cache'}
        return ResponseBuilder._build_response(200, body, headers)

    @staticmethod
    def list_response_with_etag(items: list, event: Dict, count: Optional[int] = None, pagination: Optional[Dict] = None) -> Dict[str, Any]:
        """Build a list response with ETag support"""
        data = {'items': items}
        if count is not None:
            data['count'] = count
        if pagination:
            data['pagination'] = pagination

        etag = ResponseBuilder.generate_etag(data)
        client_etag = ResponseBuilder.extract_if_none_match(event)
        if client_etag and client_etag == etag:
            return ResponseBuilder.not_modified(etag)

        body = {'message': 'Retrieved successfully', 'data': data}
        headers = {'ETag': etag, 'Cache-Control': 'no-cache'}
        return ResponseBuilder._build_response(200, body, headers)


# Convenience functions for backward compatibility
def success_response(data: Any = None, message: str = "Success", status_code: int = 200) -> Dict[str, Any]:
    """Convenience function for success responses"""
    return ResponseBuilder.success(data, message, status_code)


def error_response(message: str, status_code: int = 400, error_code: Optional[str] = None, details: Optional[Dict] = None) -> Dict[str, Any]:
    """Convenience function for error responses"""
    return ResponseBuilder.error(message, status_code, error_code, details)


def unauthorized_response(message: str = "Unauthorized") -> Dict[str, Any]:
    """Convenience function for unauthorized responses"""
    return ResponseBuilder.unauthorized(message)


def not_found_response(message: str = "Resource not found") -> Dict[str, Any]:
    """Convenience function for not found responses"""
    return ResponseBuilder.not_found(message)


def success_with_etag(data: Any, event: Dict, message: str = "Success") -> Dict[str, Any]:
    """Convenience function for success responses with ETag support"""
    return ResponseBuilder.success_with_etag(data, event, message)


def list_response_with_etag(items: list, event: Dict, count: Optional[int] = None, pagination: Optional[Dict] = None) -> Dict[str, Any]:
    """Convenience function for list responses with ETag support"""
    return ResponseBuilder.list_response_with_etag(items, event, count, pagination)


def internal_error_response(message: str = "Internal server error", error_details: Optional[str] = None) -> Dict[str, Any]:
    """Convenience function for internal error responses"""
    return ResponseBuilder.internal_error(message, error_details)


def validation_error_response(errors: list) -> Dict[str, Any]:
    """Convenience function for validation error responses"""
    return ResponseBuilder._build_response(400, {
        'message': 'Validation failed',
        'errors': errors
    })


def cors_response() -> Dict[str, Any]:
    """Convenience function for CORS preflight responses"""
    return ResponseBuilder.cors_response()
