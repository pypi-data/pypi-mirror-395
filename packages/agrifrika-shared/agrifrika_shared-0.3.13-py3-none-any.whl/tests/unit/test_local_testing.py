"""Tests for local testing utilities."""

import pytest
from agrifrika_shared.local_testing.mock_context import MockLambdaContext


@pytest.mark.unit
class TestMockLambdaContext:
    """Tests for MockLambdaContext class."""

    def test_creates_with_defaults(self):
        """Test creating mock context with default values."""
        context = MockLambdaContext()

        assert context.function_name == 'local-function'
        assert context.function_version == '$LATEST'
        assert context.memory_limit_in_mb == '128'
        assert context.aws_request_id == 'local-request-id'
        assert context.log_stream_name == 'local'

    def test_creates_with_custom_values(self):
        """Test creating mock context with custom values."""
        context = MockLambdaContext(
            function_name='my-function',
            function_version='1',
            memory_limit_in_mb='512'
        )

        assert context.function_name == 'my-function'
        assert context.function_version == '1'
        assert context.memory_limit_in_mb == '512'

    def test_generates_function_arn(self):
        """Test that function ARN is generated correctly."""
        context = MockLambdaContext(function_name='test-function')

        assert context.invoked_function_arn.startswith('arn:aws:lambda:')
        assert 'test-function' in context.invoked_function_arn

    def test_generates_log_group_name(self):
        """Test that log group name is generated correctly."""
        context = MockLambdaContext(function_name='test-function')

        assert context.log_group_name == '/aws/lambda/test-function'

    def test_get_remaining_time_in_millis(self):
        """Test that remaining time is returned."""
        context = MockLambdaContext()

        time_remaining = context.get_remaining_time_in_millis()

        assert isinstance(time_remaining, int)
        assert time_remaining > 0
        assert time_remaining == 300000  # 5 minutes

    def test_has_all_required_attributes(self):
        """Test that mock context has all attributes of real Lambda context."""
        context = MockLambdaContext()

        # Check all standard Lambda context attributes
        required_attributes = [
            'function_name',
            'function_version',
            'invoked_function_arn',
            'memory_limit_in_mb',
            'aws_request_id',
            'log_group_name',
            'log_stream_name'
        ]

        for attr in required_attributes:
            assert hasattr(context, attr), f"Missing attribute: {attr}"

    def test_can_be_used_as_context_parameter(self):
        """Test that mock context can be used like real Lambda context."""
        context = MockLambdaContext(function_name='my-lambda')

        # Simulate common context usage patterns
        function_info = {
            'name': context.function_name,
            'version': context.function_version,
            'memory': context.memory_limit_in_mb,
            'request_id': context.aws_request_id,
            'time_remaining': context.get_remaining_time_in_millis()
        }

        assert function_info['name'] == 'my-lambda'
        assert function_info['version'] == '$LATEST'
        assert function_info['memory'] == '128'
        assert function_info['time_remaining'] == 300000


@pytest.mark.unit
class TestMockLambdaContextIntegration:
    """Integration tests for MockLambdaContext with handlers."""

    def test_works_with_lambda_handler(self):
        """Test that mock context works with a Lambda handler function."""
        def simple_handler(event, context):
            """Simple Lambda handler for testing."""
            return {
                'statusCode': 200,
                'body': {
                    'function': context.function_name,
                    'request_id': context.aws_request_id,
                    'remaining_time': context.get_remaining_time_in_millis()
                }
            }

        # Create mock event and context
        event = {'test': 'data'}
        context = MockLambdaContext(function_name='test-handler')

        # Call handler
        response = simple_handler(event, context)

        assert response['statusCode'] == 200
        assert response['body']['function'] == 'test-handler'
        assert response['body']['request_id'] == 'local-request-id'
        assert response['body']['remaining_time'] == 300000

    def test_context_attributes_are_strings_or_callable(self):
        """Test that context attributes have correct types."""
        context = MockLambdaContext()

        # String attributes
        assert isinstance(context.function_name, str)
        assert isinstance(context.function_version, str)
        assert isinstance(context.invoked_function_arn, str)
        assert isinstance(context.memory_limit_in_mb, str)
        assert isinstance(context.aws_request_id, str)
        assert isinstance(context.log_group_name, str)
        assert isinstance(context.log_stream_name, str)

        # Callable method
        assert callable(context.get_remaining_time_in_millis)

    def test_multiple_instances_are_independent(self):
        """Test that multiple mock contexts are independent."""
        context1 = MockLambdaContext(function_name='function-1')
        context2 = MockLambdaContext(function_name='function-2')

        assert context1.function_name != context2.function_name
        assert context1.log_group_name != context2.log_group_name
        assert context1.invoked_function_arn != context2.invoked_function_arn
