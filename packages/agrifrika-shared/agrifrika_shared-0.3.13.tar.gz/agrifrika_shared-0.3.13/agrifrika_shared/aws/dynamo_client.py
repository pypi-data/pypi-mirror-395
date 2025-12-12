"""
DynamoDB client wrapper with error handling and common operations.

This module provides a high-level interface for DynamoDB operations
with proper error handling and logging.
"""

import os
from typing import Dict, List, Optional, Any
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

from .clients import get_dynamodb_resource
from ..utils.logger import get_logger
from ..utils.exceptions import ExternalServiceError, NotFoundError

logger = get_logger(__name__)


class DynamoDBClient:
    """
    Wrapper for DynamoDB operations with error handling.

    Example:
        >>> client = DynamoDBClient()
        >>> table = client.get_table('users')
        >>> user = client.get_item('users', {'id': '123'})
    """

    def __init__(self):
        self.dynamodb = get_dynamodb_resource()

    def get_table(self, table_name: str):
        """
        Get DynamoDB table resource.

        Args:
            table_name: Name of the DynamoDB table

        Returns:
            DynamoDB Table resource

        Example:
            >>> table = client.get_table('users')
            >>> response = table.get_item(Key={'id': '123'})
        """
        return self.dynamodb.Table(table_name)

    def put_item(self, table_name: str, item: Dict[str, Any]) -> bool:
        """
        Put item into DynamoDB table.

        Args:
            table_name: Name of the table
            item: Item dictionary to insert

        Returns:
            True if successful

        Raises:
            ExternalServiceError: If DynamoDB operation fails

        Example:
            >>> client.put_item('users', {'id': '123', 'name': 'John'})
        """
        try:
            table = self.get_table(table_name)
            table.put_item(Item=item)
            logger.info('dynamodb_put_item_success', table=table_name)
            return True
        except ClientError as e:
            logger.error('dynamodb_put_item_failed', table=table_name, error=str(e))
            raise ExternalServiceError('DynamoDB', f'Failed to put item: {str(e)}', e)

    def get_item(self, table_name: str, key: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Get item from DynamoDB table.

        Args:
            table_name: Name of the table
            key: Primary key dictionary

        Returns:
            Item dictionary or None if not found

        Example:
            >>> item = client.get_item('users', {'id': '123'})
            >>> if item:
            ...     print(item['name'])
        """
        try:
            table = self.get_table(table_name)
            response = table.get_item(Key=key)
            item = response.get('Item')

            if item:
                logger.debug('dynamodb_get_item_success', table=table_name, key=key)
            else:
                logger.debug('dynamodb_get_item_not_found', table=table_name, key=key)

            return item
        except ClientError as e:
            logger.error('dynamodb_get_item_failed', table=table_name, key=key, error=str(e))
            raise ExternalServiceError('DynamoDB', f'Failed to get item: {str(e)}', e)

    def query(
        self,
        table_name: str,
        key_condition_expression,
        index_name: Optional[str] = None,
        filter_expression=None,
        limit: Optional[int] = None,
        exclusive_start_key: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Query DynamoDB table.

        Args:
            table_name: Name of the table
            key_condition_expression: boto3 Key condition (e.g., Key('pk').eq('value'))
            index_name: Optional GSI/LSI name
            filter_expression: Optional filter expression
            limit: Optional limit on number of items
            exclusive_start_key: Optional pagination token

        Returns:
            Dictionary with 'Items' and optional 'LastEvaluatedKey'

        Example:
            >>> from boto3.dynamodb.conditions import Key
            >>> result = client.query(
            ...     'users',
            ...     key_condition_expression=Key('status').eq('active'),
            ...     index_name='StatusIndex'
            ... )
            >>> for item in result['Items']:
            ...     print(item['name'])
        """
        try:
            table = self.get_table(table_name)

            query_kwargs = {
                'KeyConditionExpression': key_condition_expression
            }

            if index_name:
                query_kwargs['IndexName'] = index_name

            if filter_expression is not None:
                query_kwargs['FilterExpression'] = filter_expression

            if limit:
                query_kwargs['Limit'] = limit

            if exclusive_start_key:
                query_kwargs['ExclusiveStartKey'] = exclusive_start_key

            response = table.query(**query_kwargs)

            logger.info(
                'dynamodb_query_success',
                table=table_name,
                index=index_name,
                count=len(response.get('Items', []))
            )

            return {
                'Items': response.get('Items', []),
                'LastEvaluatedKey': response.get('LastEvaluatedKey')
            }
        except ClientError as e:
            logger.error('dynamodb_query_failed', table=table_name, error=str(e))
            raise ExternalServiceError('DynamoDB', f'Failed to query table: {str(e)}', e)

    def scan(
        self,
        table_name: str,
        filter_expression=None,
        limit: Optional[int] = None,
        exclusive_start_key: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Scan DynamoDB table.

        Warning: Scans are expensive operations. Use query when possible.

        Args:
            table_name: Name of the table
            filter_expression: Optional filter expression
            limit: Optional limit on number of items
            exclusive_start_key: Optional pagination token

        Returns:
            Dictionary with 'Items' and optional 'LastEvaluatedKey'

        Example:
            >>> from boto3.dynamodb.conditions import Attr
            >>> result = client.scan(
            ...     'users',
            ...     filter_expression=Attr('status').eq('active')
            ... )
        """
        try:
            table = self.get_table(table_name)

            scan_kwargs = {}

            if filter_expression is not None:
                scan_kwargs['FilterExpression'] = filter_expression

            if limit:
                scan_kwargs['Limit'] = limit

            if exclusive_start_key:
                scan_kwargs['ExclusiveStartKey'] = exclusive_start_key

            response = table.scan(**scan_kwargs)

            logger.warning(
                'dynamodb_scan_executed',
                table=table_name,
                count=len(response.get('Items', []))
            )

            return {
                'Items': response.get('Items', []),
                'LastEvaluatedKey': response.get('LastEvaluatedKey')
            }
        except ClientError as e:
            logger.error('dynamodb_scan_failed', table=table_name, error=str(e))
            raise ExternalServiceError('DynamoDB', f'Failed to scan table: {str(e)}', e)

    def update_item(
        self,
        table_name: str,
        key: Dict[str, Any],
        update_expression: str,
        expression_attribute_values: Dict[str, Any],
        expression_attribute_names: Optional[Dict[str, str]] = None,
        condition_expression=None
    ) -> Dict[str, Any]:
        """
        Update item in DynamoDB table.

        Args:
            table_name: Name of the table
            key: Primary key dictionary
            update_expression: Update expression (e.g., 'SET #name = :name')
            expression_attribute_values: Values map (e.g., {':name': 'John'})
            expression_attribute_names: Optional names map (e.g., {'#name': 'name'})
            condition_expression: Optional condition expression

        Returns:
            Updated item attributes

        Example:
            >>> client.update_item(
            ...     'users',
            ...     {'id': '123'},
            ...     'SET #name = :name, updated_at = :updated',
            ...     {':name': 'John Doe', ':updated': '2025-01-01'},
            ...     {'#name': 'name'}
            ... )
        """
        try:
            table = self.get_table(table_name)

            update_kwargs = {
                'Key': key,
                'UpdateExpression': update_expression,
                'ExpressionAttributeValues': expression_attribute_values,
                'ReturnValues': 'ALL_NEW'
            }

            if expression_attribute_names:
                update_kwargs['ExpressionAttributeNames'] = expression_attribute_names

            if condition_expression is not None:
                update_kwargs['ConditionExpression'] = condition_expression

            response = table.update_item(**update_kwargs)

            logger.info('dynamodb_update_item_success', table=table_name, key=key)

            return response.get('Attributes', {})
        except ClientError as e:
            logger.error('dynamodb_update_item_failed', table=table_name, key=key, error=str(e))
            raise ExternalServiceError('DynamoDB', f'Failed to update item: {str(e)}', e)

    def delete_item(self, table_name: str, key: Dict[str, Any]) -> bool:
        """
        Delete item from DynamoDB table.

        Args:
            table_name: Name of the table
            key: Primary key dictionary

        Returns:
            True if successful

        Example:
            >>> client.delete_item('users', {'id': '123'})
        """
        try:
            table = self.get_table(table_name)
            table.delete_item(Key=key)
            logger.info('dynamodb_delete_item_success', table=table_name, key=key)
            return True
        except ClientError as e:
            logger.error('dynamodb_delete_item_failed', table=table_name, key=key, error=str(e))
            raise ExternalServiceError('DynamoDB', f'Failed to delete item: {str(e)}', e)

    def batch_get_items(self, table_name: str, keys: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Batch get multiple items from DynamoDB table.

        Args:
            table_name: Name of the table
            keys: List of primary key dictionaries

        Returns:
            List of items

        Example:
            >>> keys = [{'id': '123'}, {'id': '456'}]
            >>> items = client.batch_get_items('users', keys)
        """
        try:
            response = self.dynamodb.batch_get_item(
                RequestItems={
                    table_name: {
                        'Keys': keys
                    }
                }
            )

            items = response.get('Responses', {}).get(table_name, [])

            logger.info(
                'dynamodb_batch_get_success',
                table=table_name,
                requested=len(keys),
                retrieved=len(items)
            )

            return items
        except ClientError as e:
            logger.error('dynamodb_batch_get_failed', table=table_name, error=str(e))
            raise ExternalServiceError('DynamoDB', f'Failed to batch get items: {str(e)}', e)

    def batch_write_items(self, table_name: str, items: List[Dict[str, Any]]) -> bool:
        """
        Batch write multiple items to DynamoDB table.

        Args:
            table_name: Name of the table
            items: List of item dictionaries

        Returns:
            True if successful

        Example:
            >>> items = [{'id': '123', 'name': 'John'}, {'id': '456', 'name': 'Jane'}]
            >>> client.batch_write_items('users', items)
        """
        try:
            table = self.get_table(table_name)

            with table.batch_writer() as batch:
                for item in items:
                    batch.put_item(Item=item)

            logger.info('dynamodb_batch_write_success', table=table_name, count=len(items))
            return True
        except ClientError as e:
            logger.error('dynamodb_batch_write_failed', table=table_name, error=str(e))
            raise ExternalServiceError('DynamoDB', f'Failed to batch write items: {str(e)}', e)
