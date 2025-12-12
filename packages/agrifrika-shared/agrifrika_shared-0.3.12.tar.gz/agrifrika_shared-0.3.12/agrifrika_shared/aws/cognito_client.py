"""
Cognito client wrapper for user management operations.

This module provides a high-level interface for AWS Cognito operations
with proper error handling and logging.
"""

import os
from typing import Dict, List, Optional, Any
from botocore.exceptions import ClientError

from .clients import get_cognito_client
from ..utils.logger import get_logger
from ..utils.exceptions import ExternalServiceError, NotFoundError, ConflictError

logger = get_logger(__name__)


class CognitoClient:
    """
    Wrapper for Cognito Identity Provider operations.

    Example:
        >>> client = CognitoClient()
        >>> user = client.create_user('test@example.com', 'TempPass123!')
        >>> client.add_user_to_group('test@example.com', 'Admins')
    """

    def __init__(self, user_pool_id: Optional[str] = None):
        """
        Initialize Cognito client.

        Args:
            user_pool_id: Optional user pool ID. Defaults to COGNITO_USER_POOL_ID env var
        """
        self.client = get_cognito_client()
        self.user_pool_id = user_pool_id or os.environ.get('COGNITO_USER_POOL_ID')

        if not self.user_pool_id:
            raise ValueError('COGNITO_USER_POOL_ID environment variable is required')

    def create_user(
        self,
        email: str,
        temp_password: str,
        attributes: Optional[Dict[str, str]] = None,
        send_invitation: bool = True
    ) -> Dict[str, Any]:
        """
        Create a new user in Cognito user pool.

        Args:
            email: User email address (will be username)
            temp_password: Temporary password
            attributes: Optional user attributes (e.g., {'given_name': 'John', 'family_name': 'Doe'})
            send_invitation: Whether to send email invitation

        Returns:
            Created user information

        Raises:
            ConflictError: If user already exists
            ExternalServiceError: If Cognito operation fails

        Example:
            >>> user = client.create_user(
            ...     'test@example.com',
            ...     'TempPass123!',
            ...     {'given_name': 'John', 'family_name': 'Doe', 'custom:user_type': 'aggregator'}
            ... )
        """
        try:
            user_attributes = [
                {'Name': 'email', 'Value': email},
                {'Name': 'email_verified', 'Value': 'true'}
            ]

            if attributes:
                for key, value in attributes.items():
                    user_attributes.append({'Name': key, 'Value': value})

            response = self.client.admin_create_user(
                UserPoolId=self.user_pool_id,
                Username=email,
                UserAttributes=user_attributes,
                TemporaryPassword=temp_password,
                MessageAction='SUPPRESS' if not send_invitation else 'RESEND',
                DesiredDeliveryMediums=['EMAIL']
            )

            logger.info('cognito_user_created', email=email, username=response['User']['Username'])

            return response['User']
        except ClientError as e:
            error_code = e.response['Error']['Code']

            if error_code == 'UsernameExistsException':
                logger.warning('cognito_user_exists', email=email)
                raise ConflictError(f'User with email {email} already exists', 'email')
            else:
                logger.error('cognito_create_user_failed', email=email, error=str(e))
                raise ExternalServiceError('Cognito', f'Failed to create user: {str(e)}', e)

    def get_user(self, username: str) -> Dict[str, Any]:
        """
        Get user details from Cognito.

        Args:
            username: Username (typically email)

        Returns:
            User information

        Raises:
            NotFoundError: If user not found
            ExternalServiceError: If Cognito operation fails

        Example:
            >>> user = client.get_user('test@example.com')
            >>> print(user['Username'])
        """
        try:
            response = self.client.admin_get_user(
                UserPoolId=self.user_pool_id,
                Username=username
            )

            logger.debug('cognito_get_user_success', username=username)

            return response
        except ClientError as e:
            error_code = e.response['Error']['Code']

            if error_code == 'UserNotFoundException':
                logger.warning('cognito_user_not_found', username=username)
                raise NotFoundError('User', username)
            else:
                logger.error('cognito_get_user_failed', username=username, error=str(e))
                raise ExternalServiceError('Cognito', f'Failed to get user: {str(e)}', e)

    def update_user_attributes(self, username: str, attributes: Dict[str, str]) -> bool:
        """
        Update user attributes in Cognito.

        Args:
            username: Username (typically email)
            attributes: Dictionary of attributes to update

        Returns:
            True if successful

        Example:
            >>> client.update_user_attributes(
            ...     'test@example.com',
            ...     {'given_name': 'Jane', 'phone_number': '+237612345678'}
            ... )
        """
        try:
            user_attributes = [
                {'Name': key, 'Value': value}
                for key, value in attributes.items()
            ]

            self.client.admin_update_user_attributes(
                UserPoolId=self.user_pool_id,
                Username=username,
                UserAttributes=user_attributes
            )

            logger.info('cognito_user_attributes_updated', username=username)

            return True
        except ClientError as e:
            logger.error('cognito_update_attributes_failed', username=username, error=str(e))
            raise ExternalServiceError('Cognito', f'Failed to update user attributes: {str(e)}', e)

    def set_permanent_password(self, username: str, password: str) -> bool:
        """
        Set a permanent password for a user.

        Args:
            username: Username (typically email)
            password: New permanent password

        Returns:
            True if successful

        Example:
            >>> client.set_permanent_password('test@example.com', 'SecurePass123!')
        """
        try:
            self.client.admin_set_user_password(
                UserPoolId=self.user_pool_id,
                Username=username,
                Password=password,
                Permanent=True
            )

            logger.info('cognito_password_set', username=username)

            return True
        except ClientError as e:
            logger.error('cognito_set_password_failed', username=username, error=str(e))
            raise ExternalServiceError('Cognito', f'Failed to set password: {str(e)}', e)

    def disable_user(self, username: str) -> bool:
        """
        Disable a user in Cognito.

        Args:
            username: Username (typically email)

        Returns:
            True if successful

        Example:
            >>> client.disable_user('test@example.com')
        """
        try:
            self.client.admin_disable_user(
                UserPoolId=self.user_pool_id,
                Username=username
            )

            logger.info('cognito_user_disabled', username=username)

            return True
        except ClientError as e:
            logger.error('cognito_disable_user_failed', username=username, error=str(e))
            raise ExternalServiceError('Cognito', f'Failed to disable user: {str(e)}', e)

    def enable_user(self, username: str) -> bool:
        """
        Enable a user in Cognito.

        Args:
            username: Username (typically email)

        Returns:
            True if successful

        Example:
            >>> client.enable_user('test@example.com')
        """
        try:
            self.client.admin_enable_user(
                UserPoolId=self.user_pool_id,
                Username=username
            )

            logger.info('cognito_user_enabled', username=username)

            return True
        except ClientError as e:
            logger.error('cognito_enable_user_failed', username=username, error=str(e))
            raise ExternalServiceError('Cognito', f'Failed to enable user: {str(e)}', e)

    def delete_user(self, username: str) -> bool:
        """
        Delete a user from Cognito.

        Args:
            username: Username (typically email)

        Returns:
            True if successful

        Example:
            >>> client.delete_user('test@example.com')
        """
        try:
            self.client.admin_delete_user(
                UserPoolId=self.user_pool_id,
                Username=username
            )

            logger.info('cognito_user_deleted', username=username)

            return True
        except ClientError as e:
            logger.error('cognito_delete_user_failed', username=username, error=str(e))
            raise ExternalServiceError('Cognito', f'Failed to delete user: {str(e)}', e)

    def add_user_to_group(self, username: str, group_name: str) -> bool:
        """
        Add a user to a Cognito group.

        Args:
            username: Username (typically email)
            group_name: Name of the group

        Returns:
            True if successful

        Example:
            >>> client.add_user_to_group('test@example.com', 'Admins')
        """
        try:
            self.client.admin_add_user_to_group(
                UserPoolId=self.user_pool_id,
                Username=username,
                GroupName=group_name
            )

            logger.info('cognito_user_added_to_group', username=username, group=group_name)

            return True
        except ClientError as e:
            logger.error('cognito_add_to_group_failed', username=username, group=group_name, error=str(e))
            raise ExternalServiceError('Cognito', f'Failed to add user to group: {str(e)}', e)

    def remove_user_from_group(self, username: str, group_name: str) -> bool:
        """
        Remove a user from a Cognito group.

        Args:
            username: Username (typically email)
            group_name: Name of the group

        Returns:
            True if successful

        Example:
            >>> client.remove_user_from_group('test@example.com', 'Admins')
        """
        try:
            self.client.admin_remove_user_from_group(
                UserPoolId=self.user_pool_id,
                Username=username,
                GroupName=group_name
            )

            logger.info('cognito_user_removed_from_group', username=username, group=group_name)

            return True
        except ClientError as e:
            logger.error('cognito_remove_from_group_failed', username=username, group=group_name, error=str(e))
            raise ExternalServiceError('Cognito', f'Failed to remove user from group: {str(e)}', e)

    def list_users(self, limit: int = 60, pagination_token: Optional[str] = None) -> Dict[str, Any]:
        """
        List users in the Cognito user pool.

        Args:
            limit: Maximum number of users to return (1-60)
            pagination_token: Token for pagination

        Returns:
            Dictionary with 'Users' list and optional 'PaginationToken'

        Example:
            >>> result = client.list_users(limit=20)
            >>> for user in result['Users']:
            ...     print(user['Username'])
        """
        try:
            list_kwargs = {
                'UserPoolId': self.user_pool_id,
                'Limit': min(limit, 60)  # Max 60 per AWS limits
            }

            if pagination_token:
                list_kwargs['PaginationToken'] = pagination_token

            response = self.client.list_users(**list_kwargs)

            logger.info('cognito_list_users_success', count=len(response['Users']))

            return {
                'Users': response['Users'],
                'PaginationToken': response.get('PaginationToken')
            }
        except ClientError as e:
            logger.error('cognito_list_users_failed', error=str(e))
            raise ExternalServiceError('Cognito', f'Failed to list users: {str(e)}', e)

    def resend_invitation(self, username: str) -> bool:
        """
        Resend invitation email to a user.

        Args:
            username: Username (typically email)

        Returns:
            True if successful

        Example:
            >>> client.resend_invitation('test@example.com')
        """
        try:
            self.client.admin_create_user(
                UserPoolId=self.user_pool_id,
                Username=username,
                MessageAction='RESEND',
                DesiredDeliveryMediums=['EMAIL']
            )

            logger.info('cognito_invitation_resent', username=username)

            return True
        except ClientError as e:
            logger.error('cognito_resend_invitation_failed', username=username, error=str(e))
            raise ExternalServiceError('Cognito', f'Failed to resend invitation: {str(e)}', e)
