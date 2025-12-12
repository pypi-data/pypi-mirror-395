"""
AWS client wrappers with retry logic.
"""

from .clients import (
    get_boto3_config,
    get_region,
    get_dynamodb_client,
    get_dynamodb_resource,
    get_cognito_client,
    get_s3_client,
    get_ses_client,
    get_sns_client,
    get_lambda_client,
    get_secrets_client,
    clear_clients,
)

from .dynamo_client import DynamoDBClient
from .cognito_client import CognitoClient
from .s3_client import (
    generate_presigned_url,
    generate_upload_url,
    delete_file,
    file_exists,
    get_file_info,
)

__all__ = [
    # Client factory
    "get_boto3_config",
    "get_region",
    "get_dynamodb_client",
    "get_dynamodb_resource",
    "get_cognito_client",
    "get_s3_client",
    "get_ses_client",
    "get_sns_client",
    "get_lambda_client",
    "get_secrets_client",
    "clear_clients",
    # Client wrappers
    "DynamoDBClient",
    "CognitoClient",
    # S3 utility functions
    "generate_presigned_url",
    "generate_upload_url",
    "delete_file",
    "file_exists",
    "get_file_info",
]
