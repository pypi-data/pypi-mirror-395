"""
S3 utility functions using agrifrika_shared S3 client.

No module-level instantiation - safe for testing.
"""

import os
import logging
from typing import Optional, Dict, Any
from botocore.exceptions import ClientError
from agrifrika_shared.aws.clients import get_s3_client

logger = logging.getLogger(__name__)


def _get_bucket_name() -> str:
    """
    Get S3 bucket name from environment.

    Returns:
        S3 bucket name

    Raises:
        ValueError: If S3_BUCKET_NAME is not set
    """
    bucket_name = os.environ.get('S3_BUCKET_NAME')
    if not bucket_name:
        raise ValueError("S3_BUCKET_NAME environment variable is required")
    return bucket_name


def generate_presigned_url(
    file_key: str,
    operation: str = 'get_object',
    expires_in: int = 3600,
    bucket_name: Optional[str] = None
) -> Optional[str]:
    """
    Generate a presigned URL for S3 operations using agrifrika_shared client.

    Args:
        file_key: S3 key of the file
        operation: S3 operation ('get_object', 'put_object', etc.)
        expires_in: URL expiration time in seconds
        bucket_name: Optional bucket name (uses S3_BUCKET_NAME env if not provided)

    Returns:
        Presigned URL or None if error
    """
    try:
        bucket = bucket_name or _get_bucket_name()
        s3_client = get_s3_client()

        presigned_url = s3_client.generate_presigned_url(
            operation,
            Params={
                'Bucket': bucket,
                'Key': file_key
            },
            ExpiresIn=expires_in
        )
        return presigned_url
    except ClientError as e:
        logger.error(f"Error generating presigned URL for {file_key}: {e}")
        return None
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return None


def generate_upload_url(
    file_key: str,
    content_type: str,
    expires_in: int = 3600,
    bucket_name: Optional[str] = None
) -> Optional[str]:
    """
    Generate a presigned URL for file upload using agrifrika_shared client.

    Args:
        file_key: S3 key where file will be uploaded
        content_type: MIME type of the file
        expires_in: URL expiration time in seconds
        bucket_name: Optional bucket name (uses S3_BUCKET_NAME env if not provided)

    Returns:
        Presigned upload URL or None if error
    """
    try:
        bucket = bucket_name or _get_bucket_name()
        s3_client = get_s3_client()

        presigned_url = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': bucket,
                'Key': file_key,
                'ContentType': content_type
            },
            ExpiresIn=expires_in
        )
        return presigned_url
    except ClientError as e:
        logger.error(f"Error generating upload URL for {file_key}: {e}")
        return None
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return None


def delete_file(file_key: str, bucket_name: Optional[str] = None) -> bool:
    """
    Delete a file from S3 using agrifrika_shared client.

    Args:
        file_key: S3 key of the file to delete
        bucket_name: Optional bucket name (uses S3_BUCKET_NAME env if not provided)

    Returns:
        True if successful, False otherwise
    """
    try:
        bucket = bucket_name or _get_bucket_name()
        s3_client = get_s3_client()

        s3_client.delete_object(
            Bucket=bucket,
            Key=file_key
        )
        logger.info(f"Successfully deleted file: {file_key}")
        return True
    except ClientError as e:
        logger.error(f"Error deleting file {file_key}: {e}")
        return False
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return False


def file_exists(file_key: str, bucket_name: Optional[str] = None) -> bool:
    """
    Check if a file exists in S3 using agrifrika_shared client.

    Args:
        file_key: S3 key of the file
        bucket_name: Optional bucket name (uses S3_BUCKET_NAME env if not provided)

    Returns:
        True if file exists, False otherwise
    """
    try:
        bucket = bucket_name or _get_bucket_name()
        s3_client = get_s3_client()

        s3_client.head_object(
            Bucket=bucket,
            Key=file_key
        )
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            return False
        logger.error(f"Error checking file existence {file_key}: {e}")
        return False
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return False


def get_file_info(file_key: str, bucket_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Get file metadata from S3 using agrifrika_shared client.

    Args:
        file_key: S3 key of the file
        bucket_name: Optional bucket name (uses S3_BUCKET_NAME env if not provided)

    Returns:
        File metadata dictionary or None if error
    """
    try:
        bucket = bucket_name or _get_bucket_name()
        s3_client = get_s3_client()

        response = s3_client.head_object(
            Bucket=bucket,
            Key=file_key
        )
        return {
            'file_key': file_key,
            'file_size': response['ContentLength'],
            'content_type': response.get('ContentType'),
            'last_modified': response.get('LastModified'),
            'etag': response.get('ETag', '').strip('"')
        }
    except ClientError as e:
        logger.error(f"Error getting file info for {file_key}: {e}")
        return None
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return None
