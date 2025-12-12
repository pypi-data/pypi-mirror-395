"""
Shared test fixtures for agrifrika-shared package tests.
"""

import pytest
import boto3
from moto import mock_aws
import os


@pytest.fixture(scope='function')
def aws_credentials():
    """Mock AWS credentials for moto."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
    os.environ['REGION'] = 'us-east-1'


@pytest.fixture(scope='function')
def aws_mock(aws_credentials):
    """Mock AWS services for testing."""
    with mock_aws():
        yield


@pytest.fixture(scope='function')
def dynamodb_resource(aws_mock):
    """Mock DynamoDB resource for testing."""
    return boto3.resource('dynamodb', region_name='us-east-1')


@pytest.fixture(scope='function')
def sqs_client(aws_mock):
    """Mock SQS client for testing."""
    return boto3.client('sqs', region_name='us-east-1')


@pytest.fixture(scope='function')
def events_client(aws_mock):
    """Mock EventBridge client for testing."""
    return boto3.client('events', region_name='us-east-1')


@pytest.fixture
def sample_lambda_event():
    """Sample API Gateway Lambda event."""
    return {
        'httpMethod': 'POST',
        'path': '/test',
        'headers': {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer test-token'
        },
        'queryStringParameters': {'param1': 'value1'},
        'pathParameters': {'id': 'test-id'},
        'body': '{"key": "value"}',
        'requestContext': {
            'authorizer': {
                'claims': {
                    'sub': 'user-123',
                    'email': 'test@example.com',
                    'custom:user_type': 'client'
                }
            }
        }
    }
