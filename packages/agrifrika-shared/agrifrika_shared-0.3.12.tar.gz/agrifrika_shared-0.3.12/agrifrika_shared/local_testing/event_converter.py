"""
Event conversion utilities for local Lambda testing.

This module provides functions to convert between Flask HTTP requests
and AWS Lambda API Gateway Proxy event format, enabling local testing
of Lambda handlers without deploying to AWS.
"""

from __future__ import annotations

import os
import json
from typing import Dict, Any, Optional, TYPE_CHECKING

# Flask imports are lazy to avoid import errors in Lambda environment
# Flask is only needed for local development, not in Lambda
if TYPE_CHECKING:
    from flask import Response


def flask_to_lambda_event(
    method: str = 'GET',
    path: str = '/',
    path_params: Optional[Dict[str, str]] = None,
    query_params: Optional[Dict[str, str]] = None,
    body: Optional[str] = None,
    include_auth: bool = True
) -> Dict[str, Any]:
    """
    Convert Flask request to AWS Lambda API Gateway Proxy event format.

    This function creates a Lambda event dictionary from Flask request parameters,
    simulating the structure that AWS API Gateway provides to Lambda functions.

    Args:
        method: HTTP method (GET, POST, PUT, DELETE, etc.)
        path: Request path (e.g., '/users/123')
        path_params: Path parameters dictionary (e.g., {'id': '123'})
        query_params: Query string parameters dictionary (e.g., {'page': '1', 'limit': '10'})
        body: Request body as string (usually JSON)
        include_auth: Whether to include mock Cognito authorizer claims (default: True)

    Returns:
        Dict containing Lambda event in API Gateway Proxy format

    Environment Variables (optional):
        LOCAL_USER_ID: User ID for mock Cognito claims (default: 'local-test-user-123')
        LOCAL_USER_EMAIL: Email for mock Cognito claims (default: 'test@local.dev')
        LOCAL_AGGREGATOR_ID: Aggregator ID for mock claims (default: 'local-aggregator-456')
        LOCAL_USERNAME: Username for mock claims (default: 'localuser')

    Example:
        ```python
        from flask import request
        from agrifrika_shared.local_testing import flask_to_lambda_event

        @app.route('/users/<user_id>', methods=['GET'])
        def get_user(user_id):
            event = flask_to_lambda_event(
                method='GET',
                path=f'/users/{user_id}',
                path_params={'id': user_id},
                query_params=request.args.to_dict()
            )
            response = lambda_handler(event, context)
            return lambda_to_flask_response(response)
        ```
    """
    # Lazy import Flask to avoid import errors in Lambda
    try:
        from flask import request as flask_request
    except ImportError:
        flask_request = None

    event = {
        'httpMethod': method,
        'path': path,
        'pathParameters': path_params or {},
        'queryStringParameters': query_params or {},
        'headers': dict(flask_request.headers) if flask_request else {},
        'body': body,
        'requestContext': {
            'requestId': 'local-request',
            'stage': os.environ.get('STAGE', 'local'),
            'identity': {
                'sourceIp': '127.0.0.1',
                'userAgent': 'local-test-client'
            }
        }
    }

    # Add mock Cognito authorizer claims if requested
    if include_auth:
        event['requestContext']['authorizer'] = {
            'claims': {
                'sub': os.environ.get('LOCAL_USER_ID', 'local-test-user-123'),
                'email': os.environ.get('LOCAL_USER_EMAIL', 'test@local.dev'),
                'custom:aggregator_id': os.environ.get('LOCAL_AGGREGATOR_ID', 'local-aggregator-456'),
                'cognito:username': os.environ.get('LOCAL_USERNAME', 'localuser'),
            }
        }

    return event


def lambda_to_flask_response(lambda_response: Dict[str, Any]) -> Response:
    """
    Convert AWS Lambda response to Flask response.

    This function transforms the dictionary response from a Lambda handler
    into a Flask Response object with appropriate status code, body, and headers.

    Args:
        lambda_response: Lambda function response dictionary with keys:
            - statusCode (int): HTTP status code
            - body (str or dict): Response body (JSON string or dict)
            - headers (dict, optional): HTTP headers to include

    Returns:
        Flask Response object

    Example:
        ```python
        from agrifrika_shared.local_testing import lambda_to_flask_response

        lambda_response = {
            'statusCode': 200,
            'body': '{"message": "Success"}',
            'headers': {'Content-Type': 'application/json'}
        }
        return lambda_to_flask_response(lambda_response)
        ```
    """
    # Lazy import Flask to avoid import errors in Lambda
    from flask import Response, jsonify

    status_code = lambda_response.get('statusCode', 200)
    body = lambda_response.get('body', '{}')
    headers = lambda_response.get('headers', {})

    # Parse body if it's a JSON string
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            # If it's not valid JSON, return as-is
            pass

    # Create Flask response
    response = jsonify(body) if isinstance(body, dict) else Response(body)
    response.status_code = status_code

    # Add custom headers from Lambda response
    for key, value in headers.items():
        response.headers[key] = value

    return response


def create_lambda_event(
    http_method: str,
    path: str,
    body: Optional[Dict[str, Any]] = None,
    path_parameters: Optional[Dict[str, str]] = None,
    query_parameters: Optional[Dict[str, str]] = None,
    headers: Optional[Dict[str, str]] = None,
    user_id: Optional[str] = None,
    aggregator_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a complete Lambda API Gateway Proxy event from scratch.

    This is a convenience function for creating Lambda events in tests
    without needing Flask request context.

    Args:
        http_method: HTTP method (GET, POST, PUT, DELETE, etc.)
        path: Request path
        body: Request body as dictionary (will be JSON-encoded)
        path_parameters: Path parameters dictionary
        query_parameters: Query string parameters dictionary
        headers: HTTP headers dictionary
        user_id: User ID for Cognito claims (overrides LOCAL_USER_ID env var)
        aggregator_id: Aggregator ID for Cognito claims (overrides LOCAL_AGGREGATOR_ID env var)

    Returns:
        Dict containing Lambda event in API Gateway Proxy format

    Example:
        ```python
        from agrifrika_shared.local_testing import create_lambda_event, MockLambdaContext

        # In a test
        event = create_lambda_event(
            http_method='POST',
            path='/products',
            body={'name': 'Tomatoes', 'price': 100},
            user_id='test-user-123'
        )
        response = lambda_handler(event, MockLambdaContext())
        ```
    """
    event = {
        'httpMethod': http_method,
        'path': path,
        'pathParameters': path_parameters or {},
        'queryStringParameters': query_parameters or {},
        'headers': headers or {'Content-Type': 'application/json'},
        'body': json.dumps(body) if body else None,
        'requestContext': {
            'requestId': 'test-request-id',
            'stage': os.environ.get('STAGE', 'local'),
            'identity': {
                'sourceIp': '127.0.0.1',
                'userAgent': 'test-client'
            },
            'authorizer': {
                'claims': {
                    'sub': user_id or os.environ.get('LOCAL_USER_ID', 'local-test-user-123'),
                    'email': os.environ.get('LOCAL_USER_EMAIL', 'test@local.dev'),
                    'custom:aggregator_id': aggregator_id or os.environ.get('LOCAL_AGGREGATOR_ID', 'local-aggregator-456'),
                    'cognito:username': os.environ.get('LOCAL_USERNAME', 'localuser'),
                }
            }
        }
    }

    return event
