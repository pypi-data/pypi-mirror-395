"""
Structured JSON logging for Lambda functions.

This module provides a structured logger that outputs JSON-formatted logs
compatible with CloudWatch Logs Insights queries.
"""

import logging
import json
import sys
from typing import Any, Dict, Optional
from datetime import datetime
import traceback


class StructuredLogger:
    """
    JSON structured logger for Lambda.

    Outputs logs in JSON format for easy parsing in CloudWatch Logs Insights.

    Example:
        >>> logger = StructuredLogger(__name__)
        >>> logger.info("user_created", user_id="123", email="test@example.com")
        # Output: {"timestamp": "2025-01-15T10:30:00", "level": "INFO", ...}
    """

    def __init__(self, name: str, level: int = logging.INFO):
        """
        Initialize the structured logger.

        Args:
            name: Logger name (typically __name__)
            level: Logging level (default: INFO)
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Remove existing handlers to avoid duplicates
        self.logger.handlers = []

        # Create console handler with JSON formatter
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        self.logger.addHandler(handler)

        self.name = name

    def _log(self, level: str, message: str, **kwargs):
        """
        Internal method to log structured data.

        Args:
            level: Log level (INFO, ERROR, WARNING, DEBUG)
            message: Log message
            **kwargs: Additional structured data fields
        """
        log_entry = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': level,
            'logger': self.name,
            'message': message,
            **kwargs
        }

        # Output as JSON
        log_line = json.dumps(log_entry)
        getattr(self.logger, level.lower())(log_line)

    def info(self, message: str, **kwargs):
        """
        Log an info message.

        Args:
            message: Log message
            **kwargs: Additional structured fields

        Example:
            >>> logger.info("order_created", order_id="123", amount=99.99)
        """
        self._log('INFO', message, **kwargs)

    def error(self, message: str, exc_info: bool = False, **kwargs):
        """
        Log an error message.

        Args:
            message: Error message
            exc_info: If True, include exception traceback
            **kwargs: Additional structured fields

        Example:
            >>> try:
            ...     risky_operation()
            ... except Exception as e:
            ...     logger.error("operation_failed", exc_info=True, error=str(e))
        """
        if exc_info:
            kwargs['traceback'] = traceback.format_exc()
        self._log('ERROR', message, **kwargs)

    def warning(self, message: str, **kwargs):
        """
        Log a warning message.

        Args:
            message: Warning message
            **kwargs: Additional structured fields

        Example:
            >>> logger.warning("rate_limit_approaching", current=950, limit=1000)
        """
        self._log('WARNING', message, **kwargs)

    def debug(self, message: str, **kwargs):
        """
        Log a debug message.

        Args:
            message: Debug message
            **kwargs: Additional structured fields

        Example:
            >>> logger.debug("cache_hit", key="user:123", ttl=3600)
        """
        self._log('DEBUG', message, **kwargs)

    def log_lambda_event(self, event: Dict[str, Any], context: Optional[Any] = None):
        """
        Log Lambda invocation details.

        Args:
            event: Lambda event dictionary
            context: Lambda context object (optional)

        Example:
            >>> def handler(event, context):
            ...     logger.log_lambda_event(event, context)
        """
        log_data = {
            'http_method': event.get('httpMethod'),
            'path': event.get('path'),
            'resource': event.get('resource'),
        }

        if context:
            log_data.update({
                'request_id': context.request_id,
                'function_name': context.function_name,
                'memory_limit_mb': context.memory_limit_in_mb,
                'remaining_time_ms': context.get_remaining_time_in_millis()
            })

        self.info('lambda_invocation', **log_data)

    def log_execution_time(self, operation: str, duration_ms: float, **kwargs):
        """
        Log operation execution time.

        Args:
            operation: Operation name
            duration_ms: Duration in milliseconds
            **kwargs: Additional context

        Example:
            >>> import time
            >>> start = time.time()
            >>> result = expensive_operation()
            >>> duration = (time.time() - start) * 1000
            >>> logger.log_execution_time("expensive_operation", duration, result_count=len(result))
        """
        self.info(
            f'{operation}_completed',
            duration_ms=duration_ms,
            **kwargs
        )


# Global logger instance
logger = StructuredLogger(__name__)


def get_logger(name: str) -> StructuredLogger:
    """
    Factory function to create a logger instance.

    Args:
        name: Logger name (typically __name__)

    Returns:
        StructuredLogger instance

    Example:
        >>> from agrifrika_shared.utils.logger import get_logger
        >>> logger = get_logger(__name__)
        >>> logger.info("service_started")
    """
    return StructuredLogger(name)
