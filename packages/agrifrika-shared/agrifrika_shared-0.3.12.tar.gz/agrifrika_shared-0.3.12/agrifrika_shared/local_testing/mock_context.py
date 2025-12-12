"""
Mock AWS Lambda context for local testing.

This module provides a mock Lambda context object that simulates
the context parameter passed to Lambda handlers during local development.
"""


class MockLambdaContext:
    """
    Mock AWS Lambda context for local testing.

    This class simulates the context object that AWS Lambda provides
    to handler functions. Use this when testing Lambda handlers locally
    to avoid runtime errors from missing context attributes.

    Attributes:
        function_name (str): Name of the Lambda function
        function_version (str): Version of the Lambda function
        invoked_function_arn (str): ARN of the invoked function
        memory_limit_in_mb (str): Memory limit configured for the function
        aws_request_id (str): AWS request ID for this invocation
        log_group_name (str): CloudWatch log group name
        log_stream_name (str): CloudWatch log stream name

    Example:
        ```python
        from agrifrika_shared.local_testing import MockLambdaContext

        context = MockLambdaContext()
        response = lambda_handler(event, context)
        ```
    """

    def __init__(
        self,
        function_name: str = 'local-function',
        function_version: str = '$LATEST',
        memory_limit_in_mb: str = '128'
    ):
        """
        Initialize mock Lambda context.

        Args:
            function_name: Name of the Lambda function (default: 'local-function')
            function_version: Function version (default: '$LATEST')
            memory_limit_in_mb: Memory limit in MB (default: '128')
        """
        self.function_name = function_name
        self.function_version = function_version
        self.invoked_function_arn = f'arn:aws:lambda:us-east-1:000000000000:function:{function_name}'
        self.memory_limit_in_mb = memory_limit_in_mb
        self.aws_request_id = 'local-request-id'
        self.log_group_name = f'/aws/lambda/{function_name}'
        self.log_stream_name = 'local'

    def get_remaining_time_in_millis(self) -> int:
        """
        Get remaining execution time in milliseconds.

        Returns:
            int: Remaining time in milliseconds (always returns 300000 for local testing)
        """
        return 300000  # 5 minutes for local testing
