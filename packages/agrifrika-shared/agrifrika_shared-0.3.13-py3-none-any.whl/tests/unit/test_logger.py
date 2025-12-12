"""Tests for structured logger."""

import pytest
import json
import logging
from unittest.mock import Mock, MagicMock
from agrifrika_shared.utils.logger import StructuredLogger, get_logger


@pytest.mark.unit
class TestStructuredLogger:
    """Tests for StructuredLogger class."""

    def test_logger_initialization(self):
        """Test that logger is initialized correctly."""
        logger = StructuredLogger('test_logger')

        assert logger.name == 'test_logger'
        assert logger.logger.level == logging.INFO

    def test_logger_with_custom_level(self):
        """Test logger initialization with custom level."""
        logger = StructuredLogger('test_logger', level=logging.DEBUG)

        assert logger.logger.level == logging.DEBUG

    def test_info_logging(self, caplog):
        """Test info level logging."""
        logger = StructuredLogger('test_logger')

        with caplog.at_level(logging.INFO):
            logger.info('test_message', user_id='123', action='created')

        # Check that log was created
        assert len(caplog.records) > 0

        # Parse the JSON log entry
        log_entry = json.loads(caplog.records[0].message)

        assert log_entry['level'] == 'INFO'
        assert log_entry['message'] == 'test_message'
        assert log_entry['user_id'] == '123'
        assert log_entry['action'] == 'created'
        assert 'timestamp' in log_entry
        assert log_entry['logger'] == 'test_logger'

    def test_error_logging(self, caplog):
        """Test error level logging."""
        logger = StructuredLogger('test_logger')

        with caplog.at_level(logging.ERROR):
            logger.error('error_occurred', error_code='ERR_001')

        log_entry = json.loads(caplog.records[0].message)

        assert log_entry['level'] == 'ERROR'
        assert log_entry['message'] == 'error_occurred'
        assert log_entry['error_code'] == 'ERR_001'

    def test_error_logging_with_traceback(self, caplog):
        """Test error logging with exception traceback."""
        logger = StructuredLogger('test_logger')

        try:
            raise ValueError("Test error")
        except ValueError:
            with caplog.at_level(logging.ERROR):
                logger.error('exception_caught', exc_info=True)

        log_entry = json.loads(caplog.records[0].message)

        assert log_entry['level'] == 'ERROR'
        assert 'traceback' in log_entry
        assert 'ValueError: Test error' in log_entry['traceback']

    def test_warning_logging(self, caplog):
        """Test warning level logging."""
        logger = StructuredLogger('test_logger')

        with caplog.at_level(logging.WARNING):
            logger.warning('warning_message', threshold=90)

        log_entry = json.loads(caplog.records[0].message)

        assert log_entry['level'] == 'WARNING'
        assert log_entry['message'] == 'warning_message'
        assert log_entry['threshold'] == 90

    def test_debug_logging(self, caplog):
        """Test debug level logging."""
        logger = StructuredLogger('test_logger', level=logging.DEBUG)

        with caplog.at_level(logging.DEBUG):
            logger.debug('debug_message', cache_key='user:123')

        log_entry = json.loads(caplog.records[0].message)

        assert log_entry['level'] == 'DEBUG'
        assert log_entry['message'] == 'debug_message'
        assert log_entry['cache_key'] == 'user:123'

    def test_timestamp_format(self, caplog):
        """Test that timestamp is in ISO format with Z."""
        logger = StructuredLogger('test_logger')

        with caplog.at_level(logging.INFO):
            logger.info('test')

        log_entry = json.loads(caplog.records[0].message)

        # Check timestamp format (ISO 8601 with Z)
        assert log_entry['timestamp'].endswith('Z')
        assert 'T' in log_entry['timestamp']

    def test_structured_data_serialization(self, caplog):
        """Test that structured data is properly serialized."""
        logger = StructuredLogger('test_logger')

        with caplog.at_level(logging.INFO):
            logger.info(
                'complex_data',
                user={'id': '123', 'name': 'John'},
                tags=['tag1', 'tag2'],
                count=42,
                active=True
            )

        log_entry = json.loads(caplog.records[0].message)

        assert log_entry['user'] == {'id': '123', 'name': 'John'}
        assert log_entry['tags'] == ['tag1', 'tag2']
        assert log_entry['count'] == 42
        assert log_entry['active'] is True


@pytest.mark.unit
class TestLogLambdaEvent:
    """Tests for log_lambda_event method."""

    def test_logs_lambda_event_basic(self, caplog):
        """Test logging Lambda event without context."""
        logger = StructuredLogger('test_logger')

        event = {
            'httpMethod': 'POST',
            'path': '/users',
            'resource': '/users'
        }

        with caplog.at_level(logging.INFO):
            logger.log_lambda_event(event)

        log_entry = json.loads(caplog.records[0].message)

        assert log_entry['message'] == 'lambda_invocation'
        assert log_entry['http_method'] == 'POST'
        assert log_entry['path'] == '/users'
        assert log_entry['resource'] == '/users'

    def test_logs_lambda_event_with_context(self, caplog):
        """Test logging Lambda event with context."""
        logger = StructuredLogger('test_logger')

        event = {
            'httpMethod': 'GET',
            'path': '/users/123',
            'resource': '/users/{id}'
        }

        # Mock Lambda context
        context = Mock()
        context.request_id = 'req-123'
        context.function_name = 'user-service'
        context.memory_limit_in_mb = 512
        context.get_remaining_time_in_millis = Mock(return_value=5000)

        with caplog.at_level(logging.INFO):
            logger.log_lambda_event(event, context)

        log_entry = json.loads(caplog.records[0].message)

        assert log_entry['request_id'] == 'req-123'
        assert log_entry['function_name'] == 'user-service'
        assert log_entry['memory_limit_mb'] == 512
        assert log_entry['remaining_time_ms'] == 5000

    def test_logs_lambda_event_missing_fields(self, caplog):
        """Test logging Lambda event with missing optional fields."""
        logger = StructuredLogger('test_logger')

        event = {}  # Empty event

        with caplog.at_level(logging.INFO):
            logger.log_lambda_event(event)

        log_entry = json.loads(caplog.records[0].message)

        assert log_entry['message'] == 'lambda_invocation'
        assert log_entry['http_method'] is None
        assert log_entry['path'] is None
        assert log_entry['resource'] is None


@pytest.mark.unit
class TestLogExecutionTime:
    """Tests for log_execution_time method."""

    def test_logs_execution_time(self, caplog):
        """Test logging operation execution time."""
        logger = StructuredLogger('test_logger')

        with caplog.at_level(logging.INFO):
            logger.log_execution_time('database_query', 125.5, rows=10)

        log_entry = json.loads(caplog.records[0].message)

        assert log_entry['message'] == 'database_query_completed'
        assert log_entry['duration_ms'] == 125.5
        assert log_entry['rows'] == 10

    def test_logs_execution_time_with_metadata(self, caplog):
        """Test logging execution time with additional metadata."""
        logger = StructuredLogger('test_logger')

        with caplog.at_level(logging.INFO):
            logger.log_execution_time(
                'api_call',
                250.0,
                endpoint='/users',
                status_code=200,
                cache_hit=False
            )

        log_entry = json.loads(caplog.records[0].message)

        assert log_entry['message'] == 'api_call_completed'
        assert log_entry['duration_ms'] == 250.0
        assert log_entry['endpoint'] == '/users'
        assert log_entry['status_code'] == 200
        assert log_entry['cache_hit'] is False


@pytest.mark.unit
class TestGetLogger:
    """Tests for get_logger factory function."""

    def test_creates_logger_instance(self):
        """Test that get_logger creates a StructuredLogger instance."""
        logger = get_logger('my_service')

        assert isinstance(logger, StructuredLogger)
        assert logger.name == 'my_service'

    def test_creates_different_loggers(self):
        """Test that get_logger creates separate instances."""
        logger1 = get_logger('service1')
        logger2 = get_logger('service2')

        assert logger1.name == 'service1'
        assert logger2.name == 'service2'


@pytest.mark.unit
class TestLoggerEdgeCases:
    """Tests for edge cases and special scenarios."""

    def test_logs_empty_message(self, caplog):
        """Test logging with empty message."""
        logger = StructuredLogger('test_logger')

        with caplog.at_level(logging.INFO):
            logger.info('')

        log_entry = json.loads(caplog.records[0].message)

        assert log_entry['message'] == ''
        assert log_entry['level'] == 'INFO'

    def test_logs_with_no_additional_fields(self, caplog):
        """Test logging with just a message, no extra fields."""
        logger = StructuredLogger('test_logger')

        with caplog.at_level(logging.INFO):
            logger.info('simple_message')

        log_entry = json.loads(caplog.records[0].message)

        assert log_entry['message'] == 'simple_message'
        assert 'timestamp' in log_entry
        assert 'level' in log_entry
        assert 'logger' in log_entry

    def test_logs_special_characters(self, caplog):
        """Test logging with special characters."""
        logger = StructuredLogger('test_logger')

        with caplog.at_level(logging.INFO):
            logger.info('message with "quotes" and \\backslashes\\')

        log_entry = json.loads(caplog.records[0].message)

        assert 'quotes' in log_entry['message']
        assert 'backslashes' in log_entry['message']

    def test_logs_unicode_characters(self, caplog):
        """Test logging with unicode characters."""
        logger = StructuredLogger('test_logger')

        with caplog.at_level(logging.INFO):
            logger.info('message with émojis 🎉 and unicode é')

        log_entry = json.loads(caplog.records[0].message)

        assert '🎉' in log_entry['message']
        assert 'é' in log_entry['message']

    def test_multiple_logs_in_sequence(self, caplog):
        """Test that multiple sequential logs are all captured."""
        logger = StructuredLogger('test_logger')

        with caplog.at_level(logging.INFO):
            logger.info('first')
            logger.info('second')
            logger.info('third')

        assert len(caplog.records) == 3

        messages = [json.loads(r.message)['message'] for r in caplog.records]
        assert messages == ['first', 'second', 'third']
