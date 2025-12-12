"""Integration tests for AWS client wrappers with moto."""

import pytest
import boto3
from moto import mock_aws
from botocore.exceptions import ClientError


@pytest.mark.integration
@mock_aws
class TestDynamoDBIntegration:
    """Integration tests for DynamoDB client wrapper."""

    def test_table_operations(self, dynamodb_resource):
        """Test basic DynamoDB table operations."""
        # Create table
        table = dynamodb_resource.create_table(
            TableName='test_table',
            KeySchema=[
                {'AttributeName': 'id', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'id', 'AttributeType': 'S'}
            ],
            BillingMode='PAY_PER_REQUEST'
        )

        # Put item
        table.put_item(Item={'id': '123', 'name': 'Test'})

        # Get item
        response = table.get_item(Key={'id': '123'})

        assert response['Item']['id'] == '123'
        assert response['Item']['name'] == 'Test'

    def test_query_operations(self, dynamodb_resource):
        """Test DynamoDB query operations."""
        table = dynamodb_resource.create_table(
            TableName='test_table',
            KeySchema=[
                {'AttributeName': 'pk', 'KeyType': 'HASH'},
                {'AttributeName': 'sk', 'KeyType': 'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'pk', 'AttributeType': 'S'},
                {'AttributeName': 'sk', 'AttributeType': 'S'}
            ],
            BillingMode='PAY_PER_REQUEST'
        )

        # Put multiple items
        table.put_item(Item={'pk': 'USER#123', 'sk': 'ORDER#1', 'amount': 100})
        table.put_item(Item={'pk': 'USER#123', 'sk': 'ORDER#2', 'amount': 200})

        # Query
        response = table.query(
            KeyConditionExpression='pk = :pk',
            ExpressionAttributeValues={':pk': 'USER#123'}
        )

        assert response['Count'] == 2


@pytest.mark.integration
@mock_aws
class TestS3Integration:
    """Integration tests for S3 client."""

    def test_bucket_and_object_operations(self, s3_client, s3_bucket):
        """Test S3 bucket and object operations."""
        # Put object
        s3_client.put_object(
            Bucket=s3_bucket,
            Key='test.txt',
            Body=b'Hello, World!'
        )

        # Get object
        response = s3_client.get_object(Bucket=s3_bucket, Key='test.txt')
        content = response['Body'].read()

        assert content == b'Hello, World!'

    def test_list_objects(self, s3_client, s3_bucket):
        """Test listing S3 objects."""
        # Put multiple objects
        s3_client.put_object(Bucket=s3_bucket, Key='file1.txt', Body=b'Content 1')
        s3_client.put_object(Bucket=s3_bucket, Key='file2.txt', Body=b'Content 2')

        # List objects
        response = s3_client.list_objects_v2(Bucket=s3_bucket)

        assert response['KeyCount'] == 2

    def test_delete_object(self, s3_client, s3_bucket):
        """Test deleting S3 objects."""
        # Put object
        s3_client.put_object(Bucket=s3_bucket, Key='test.txt', Body=b'Content')

        # Delete object
        s3_client.delete_object(Bucket=s3_bucket, Key='test.txt')

        # Verify deletion
        response = s3_client.list_objects_v2(Bucket=s3_bucket)

        assert response.get('KeyCount', 0) == 0


@pytest.mark.integration
@mock_aws
class TestEventBridgeIntegration:
    """Integration tests for EventBridge client."""

    def test_put_events(self, events_client):
        """Test putting events to EventBridge."""
        response = events_client.put_events(
            Entries=[
                {
                    'Source': 'agrifrika.test',
                    'DetailType': 'TestEvent',
                    'Detail': '{"test": "data"}'
                }
            ]
        )

        assert response['FailedEntryCount'] == 0
        assert len(response['Entries']) == 1


@pytest.mark.integration
@mock_aws
class TestMultiServiceIntegration:
    """Integration tests across multiple AWS services."""

    def test_dynamodb_and_s3_together(self, dynamodb_resource, s3_client, s3_bucket):
        """Test using DynamoDB and S3 together."""
        # Create DynamoDB table
        table = dynamodb_resource.create_table(
            TableName='files',
            KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
            BillingMode='PAY_PER_REQUEST'
        )

        # Upload file to S3
        file_id = 'file-123'
        s3_key = f'{file_id}.txt'
        s3_client.put_object(Bucket=s3_bucket, Key=s3_key, Body=b'File content')

        # Store metadata in DynamoDB
        table.put_item(Item={
            'id': file_id,
            's3_bucket': s3_bucket,
            's3_key': s3_key,
            'size': 12
        })

        # Retrieve metadata from DynamoDB
        db_response = table.get_item(Key={'id': file_id})

        # Verify we can get the file from S3
        s3_response = s3_client.get_object(
            Bucket=db_response['Item']['s3_bucket'],
            Key=db_response['Item']['s3_key']
        )

        assert s3_response['Body'].read() == b'File content'
