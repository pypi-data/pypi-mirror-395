"""
Local Development Helper - Mock authentication for local testing.

This module provides utilities for simulating Cognito authentication
when running services locally (STAGE=local).
"""

import os
from typing import Dict, Any


def is_local_mode() -> bool:
    """
    Check if running in local development mode.

    Returns:
        True if STAGE=local, False otherwise
    """
    return os.environ.get('STAGE', '').lower() == 'local'


def get_mock_claims() -> Dict[str, str]:
    """
    Get mock Cognito claims for local testing.

    Returns:
        Dictionary of mock Cognito claims

    Environment variables can override defaults:
        - LOCAL_USER_ID: User ID (sub claim)
        - LOCAL_USER_EMAIL: User email
        - LOCAL_AGGREGATOR_ID: Aggregator ID
        - LOCAL_USERNAME: Cognito username
    """
    return {
        'sub': os.environ.get('LOCAL_USER_ID', 'local-test-user-123'),
        'email': os.environ.get('LOCAL_USER_EMAIL', 'test@local.dev'),
        'custom:aggregator_id': os.environ.get('LOCAL_AGGREGATOR_ID', 'local-aggregator-456'),
        'cognito:username': os.environ.get('LOCAL_USERNAME', 'localuser'),
        'email_verified': 'true',
        'given_name': 'Test',
        'family_name': 'User',
    }


def inject_mock_auth(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Inject mock authentication context into Lambda event for local testing.

    This function modifies the event to simulate Cognito authentication
    when running in local mode (STAGE=local).

    Args:
        event: Lambda event dictionary

    Returns:
        Modified event with mock authentication context

    Example:
        >>> event = inject_mock_auth(event)
        >>> user_id = get_user_id(event)  # Returns local-test-user-123
    """
    if not is_local_mode():
        return event

    # Don't override existing auth context
    if event.get('requestContext', {}).get('authorizer', {}).get('claims'):
        return event

    # Inject mock Cognito claims
    if 'requestContext' not in event:
        event['requestContext'] = {}

    if 'authorizer' not in event['requestContext']:
        event['requestContext']['authorizer'] = {}

    event['requestContext']['authorizer']['claims'] = get_mock_claims()

    return event


def get_test_user_info() -> Dict[str, str]:
    """
    Get information about the mock test user for debugging.

    Returns:
        Dictionary with test user information

    Example:
        >>> info = get_test_user_info()
        >>> print(f"Testing as: {info['email']}")
    """
    claims = get_mock_claims()
    return {
        'user_id': claims['sub'],
        'email': claims['email'],
        'aggregator_id': claims.get('custom:aggregator_id', 'N/A'),
        'username': claims['cognito:username'],
    }
