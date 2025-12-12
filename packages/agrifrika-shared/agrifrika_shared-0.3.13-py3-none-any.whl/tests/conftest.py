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
    os.environ['AWS_REGION'] = 'us-east-1'
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
def dynamodb_client(aws_mock):
    """Mock DynamoDB client for testing."""
    return boto3.client('dynamodb', region_name='us-east-1')


@pytest.fixture(scope='function')
def s3_client(aws_mock):
    """Mock S3 client for testing."""
    return boto3.client('s3', region_name='us-east-1')


@pytest.fixture(scope='function')
def s3_bucket(s3_client):
    """Create a mock S3 bucket for testing."""
    bucket_name = 'test-bucket'
    s3_client.create_bucket(Bucket=bucket_name)
    return bucket_name


@pytest.fixture(scope='function')
def sqs_client(aws_mock):
    """Mock SQS client for testing."""
    return boto3.client('sqs', region_name='us-east-1')


@pytest.fixture(scope='function')
def events_client(aws_mock):
    """Mock EventBridge client for testing."""
    return boto3.client('events', region_name='us-east-1')


@pytest.fixture(scope='function')
def cognito_client(aws_mock):
    """Mock Cognito client for testing."""
    return boto3.client('cognito-idp', region_name='us-east-1')


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


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        'id': 'user-123',
        'email': 'test@example.com',
        'name': 'Test User',
        'user_type': 'client',
        'status': 'active'
    }


@pytest.fixture(autouse=True)
def reset_clients_cache():
    """Reset AWS clients cache before each test."""
    try:
        from agrifrika_shared.aws.clients import clear_clients
        clear_clients()
        yield
        clear_clients()
    except ImportError:
        # If function doesn't exist, just yield
        yield
