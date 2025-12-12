"""
Local testing utilities for AWS Lambda handlers.

This module provides utilities for testing Lambda handlers locally using Flask,
without needing to deploy to AWS or use serverless-offline.

Key Features:
    - Convert Flask requests to Lambda API Gateway Proxy events
    - Convert Lambda responses to Flask responses
    - Mock Lambda context objects
    - Mock Cognito user authentication
    - Easy integration with Flask development servers

Usage:
    Create a local_server.py in your service:

    ```python
    import os
    from flask import Flask, request
    from flask_cors import CORS
    from agrifrika_shared.local_testing import (
        flask_to_lambda_event,
        lambda_to_flask_response,
        MockLambdaContext,
        inject_mock_auth
    )

    # Set environment for local testing
    os.environ['STAGE'] = 'local'
    os.environ['TABLE_NAME'] = 'my-service-local'

    # Import your handlers
    from handlers.create import handler as create_handler
    from handlers.get import handler as get_handler

    app = Flask(__name__)
    CORS(app)

    @app.route('/', methods=['POST'])
    def create():
        event = flask_to_lambda_event(
            method='POST',
            path='/',
            body=request.get_data(as_text=True)
        )
        event = inject_mock_auth(event)  # Add mock auth
        response = create_handler(event, MockLambdaContext())
        return lambda_to_flask_response(response)

    @app.route('/<item_id>', methods=['GET'])
    def get(item_id):
        event = flask_to_lambda_event(
            method='GET',
            path=f'/{item_id}',
            path_params={'id': item_id}
        )
        event = inject_mock_auth(event)  # Add mock auth
        response = get_handler(event, MockLambdaContext())
        return lambda_to_flask_response(response)

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=3000, debug=True)
    ```

Environment Variables:
    Configure mock user authentication with these optional environment variables:
    - LOCAL_USER_ID: User ID for Cognito claims (default: 'local-test-user-123')
    - LOCAL_USER_EMAIL: Email for Cognito claims (default: 'test@local.dev')
    - LOCAL_AGGREGATOR_ID: Aggregator ID (default: 'local-aggregator-456')
    - LOCAL_USERNAME: Username for Cognito claims (default: 'localuser')
"""

from agrifrika_shared.local_testing.mock_context import MockLambdaContext
from agrifrika_shared.local_testing.event_converter import (
    flask_to_lambda_event,
    lambda_to_flask_response,
    create_lambda_event
)
from agrifrika_shared.local_testing.local_dev_helper import (
    inject_mock_auth,
    get_mock_claims,
    get_test_user_info,
    is_local_mode
)

__all__ = [
    'MockLambdaContext',
    'flask_to_lambda_event',
    'lambda_to_flask_response',
    'create_lambda_event',
    'inject_mock_auth',
    'get_mock_claims',
    'get_test_user_info',
    'is_local_mode',
]
