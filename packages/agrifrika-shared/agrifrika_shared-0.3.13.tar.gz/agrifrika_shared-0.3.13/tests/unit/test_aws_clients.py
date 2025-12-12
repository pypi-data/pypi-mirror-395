"""Tests for AWS client factory functions."""

import pytest
import os
from unittest.mock import patch
import boto3
from moto import mock_aws
from agrifrika_shared.aws.clients import (
    get_boto3_config,
    get_region,
    is_local_mode,
    get_local_endpoint,
    get_dynamodb_client,
    get_dynamodb_resource,
    get_cognito_client,
    get_s3_client,
    get_events_client,
    clear_clients,
)


@pytest.mark.unit
class TestGetBoto3Config:
    """Tests for boto3 configuration."""

    def test_returns_config_object(self):
        """Test that get_boto3_config returns a Config object."""
        config = get_boto3_config()

        assert config is not None
        assert hasattr(config, 'retries')

    def test_config_has_retries(self):
        """Test that config includes retry configuration."""
        config = get_boto3_config()

        assert config.retries is not None
        assert config.retries['max_attempts'] == 3
        assert config.retries['mode'] == 'adaptive'


@pytest.mark.unit
class TestGetRegion:
    """Tests for get_region function."""

    def test_returns_default_region(self):
        """Test that default region is us-east-1."""
        with patch.dict(os.environ, {}, clear=True):
            region = get_region()
            assert region == 'us-east-1'

    def test_returns_environment_region(self):
        """Test that environment variable overrides default."""
        with patch.dict(os.environ, {'AWS_REGION': 'eu-west-1'}):
            region = get_region()
            assert region == 'eu-west-1'


@pytest.mark.unit
class TestIsLocalMode:
    """Tests for is_local_mode function."""

    def test_returns_false_by_default(self):
        """Test that local mode is false by default."""
        with patch.dict(os.environ, {}, clear=True):
            assert is_local_mode() is False

    def test_returns_true_when_stage_is_local(self):
        """Test that local mode is true when STAGE=local."""
        with patch.dict(os.environ, {'STAGE': 'local'}):
            assert is_local_mode() is True

    def test_case_insensitive_local_check(self):
        """Test that local mode check is case-insensitive."""
        with patch.dict(os.environ, {'STAGE': 'LOCAL'}):
            assert is_local_mode() is True

        with patch.dict(os.environ, {'STAGE': 'Local'}):
            assert is_local_mode() is True

    def test_returns_false_for_other_stages(self):
        """Test that local mode is false for other stages."""
        with patch.dict(os.environ, {'STAGE': 'dev'}):
            assert is_local_mode() is False

        with patch.dict(os.environ, {'STAGE': 'prod'}):
            assert is_local_mode() is False


@pytest.mark.unit
class TestGetLocalEndpoint:
    """Tests for get_local_endpoint function."""

    def test_returns_none_when_not_local(self):
        """Test that None is returned when not in local mode."""
        with patch.dict(os.environ, {'STAGE': 'dev'}):
            endpoint = get_local_endpoint('dynamodb')
            assert endpoint is None

    def test_returns_dynamodb_endpoint(self):
        """Test that DynamoDB endpoint is returned in local mode."""
        with patch.dict(os.environ, {'STAGE': 'local'}):
            endpoint = get_local_endpoint('dynamodb')
            assert endpoint == 'http://localhost:8000'

    def test_returns_s3_endpoint(self):
        """Test that S3 endpoint is returned in local mode."""
        with patch.dict(os.environ, {'STAGE': 'local'}):
            endpoint = get_local_endpoint('s3')
            assert endpoint == 'http://localhost:4566'

    def test_returns_custom_endpoint_from_env(self):
        """Test that custom endpoints from environment are used."""
        with patch.dict(os.environ, {
            'STAGE': 'local',
            'DYNAMODB_ENDPOINT': 'http://custom:9000'
        }):
            endpoint = get_local_endpoint('dynamodb')
            assert endpoint == 'http://custom:9000'

    def test_returns_none_for_unknown_service(self):
        """Test that None is returned for unknown services."""
        with patch.dict(os.environ, {'STAGE': 'local'}):
            endpoint = get_local_endpoint('unknown_service')
            assert endpoint is None


@pytest.mark.unit
class TestClientSingletons:
    """Tests for client singleton pattern."""

    def setup_method(self):
        """Clear client cache before each test."""
        clear_clients()

    @mock_aws
    def test_dynamodb_client_is_singleton(self):
        """Test that DynamoDB client is cached and reused."""
        client1 = get_dynamodb_client()
        client2 = get_dynamodb_client()

        assert client1 is client2

    @mock_aws
    def test_dynamodb_resource_is_singleton(self):
        """Test that DynamoDB resource is cached and reused."""
        resource1 = get_dynamodb_resource()
        resource2 = get_dynamodb_resource()

        assert resource1 is resource2

    @mock_aws
    def test_different_clients_are_separate(self):
        """Test that different client types are stored separately."""
        dynamodb = get_dynamodb_client()
        s3 = get_s3_client()

        assert dynamodb is not s3

    @mock_aws
    def test_clear_cache_creates_new_clients(self):
        """Test that clearing cache creates new client instances."""
        client1 = get_dynamodb_client()

        clear_clients()

        client2 = get_dynamodb_client()

        # Should be different instances after cache clear
        assert client1 is not client2


@pytest.mark.unit
class TestGetDynamoDBClient:
    """Tests for get_dynamodb_client function."""

    def setup_method(self):
        """Clear client cache before each test."""
        clear_clients()

    @mock_aws
    def test_creates_dynamodb_client(self):
        """Test that DynamoDB client is created."""
        client = get_dynamodb_client()

        assert client is not None
        assert hasattr(client, 'get_item')
        assert hasattr(client, 'put_item')

    @mock_aws
    def test_uses_correct_region(self):
        """Test that client uses correct region."""
        with patch.dict(os.environ, {'AWS_REGION': 'eu-west-1'}):
            clear_clients()
            client = get_dynamodb_client()

            assert client.meta.region_name == 'eu-west-1'


@pytest.mark.unit
class TestGetDynamoDBResource:
    """Tests for get_dynamodb_resource function."""

    def setup_method(self):
        """Clear client cache before each test."""
        clear_clients()

    @mock_aws
    def test_creates_dynamodb_resource(self):
        """Test that DynamoDB resource is created."""
        resource = get_dynamodb_resource()

        assert resource is not None
        assert hasattr(resource, 'Table')


@pytest.mark.unit
class TestGetCognitoClient:
    """Tests for get_cognito_client function."""

    def setup_method(self):
        """Clear client cache before each test."""
        clear_clients()

    @mock_aws
    def test_creates_cognito_client(self):
        """Test that Cognito client is created."""
        client = get_cognito_client()

        assert client is not None
        assert hasattr(client, 'admin_get_user')
        assert hasattr(client, 'admin_create_user')


@pytest.mark.unit
class TestGetS3Client:
    """Tests for get_s3_client function."""

    def setup_method(self):
        """Clear client cache before each test."""
        clear_clients()

    @mock_aws
    def test_creates_s3_client(self):
        """Test that S3 client is created."""
        client = get_s3_client()

        assert client is not None
        assert hasattr(client, 'get_object')
        assert hasattr(client, 'put_object')


@pytest.mark.unit
class TestGetEventsClient:
    """Tests for get_events_client function."""

    def setup_method(self):
        """Clear client cache before each test."""
        clear_clients()

    @mock_aws
    def test_creates_events_client(self):
        """Test that EventBridge client is created."""
        client = get_events_client()

        assert client is not None
        assert hasattr(client, 'put_events')
