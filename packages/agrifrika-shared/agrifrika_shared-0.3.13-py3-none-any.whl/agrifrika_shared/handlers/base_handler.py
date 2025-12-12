"""
Base handler for Lambda functions with common patterns abstracted.

This module provides a base class that handles common Lambda handler concerns:
- Authentication and user extraction
- Parameter parsing (path, query, body)
- Error handling and logging
- Response formatting
- Extension hooks

Example:
    ```python
    from agrifrika_shared.handlers import BaseHandler
    from services.goods_service import GoodsService
    from models.goods import GoodsCreate

    class CreateHandler(BaseHandler):
        requires_auth = True
        parse_body = True

        def __init__(self):
            super().__init__()
            self.service = GoodsService()

        def handle(self, event, context):
            goods = GoodsCreate(**self.body)
            result = self.service.create_goods(self.user_id, goods, event)
            return result, 'Created successfully', 201

    # Lambda entry point
    handler = CreateHandler()
    ```
"""

from typing import Any, Dict, Optional, Tuple, Union
from agrifrika_shared.utils import (
    parse_lambda_body,
    get_user_id,
    success_response,
    error_response,
    get_logger
)
from agrifrika_shared.utils.exceptions import (
    NotFoundError,
    ForbiddenError,
    ValidationError,
    BusinessError,
    UnauthorizedError
)
# Lazy import inject_mock_auth to avoid importing flask in Lambda environment


class BaseHandler:
    """
    Base handler for Lambda functions with common patterns abstracted.

    Subclasses should:
    1. Set class attributes: requires_auth, parse_body
    2. Initialize service in __init__ (call super().__init__())
    3. Implement handle() method with business logic

    Attributes:
        requires_auth (bool): Whether authentication is required (default: True)
        parse_body (bool): Whether to parse request body (default: False)
        user_id (str): Authenticated user ID (available after auth)
        path_params (dict): Path parameters from API Gateway
        query_params (dict): Query string parameters from API Gateway
        body (dict): Parsed request body (if parse_body=True)
        event (dict): Original Lambda event
        context: Original Lambda context
        logger: Logger instance for this handler
    """

    # Configuration options (override in subclass)
    requires_auth: bool = True
    parse_body: bool = False

    def __init__(self):
        """Initialize handler. Override to set up services."""
        self.logger = get_logger(self.__class__.__name__)
        self.user_id: Optional[str] = None
        self.path_params: Dict[str, Any] = {}
        self.query_params: Dict[str, Any] = {}
        self.body: Optional[Dict[str, Any]] = None
        self.event: Optional[Dict[str, Any]] = None
        self.context: Optional[Any] = None

    def __call__(self, event: Dict[str, Any], context: Any) -> Dict[str, Any]:
        """
        Lambda entry point. Handles full request lifecycle.

        Args:
            event: Lambda event dictionary
            context: Lambda context object

        Returns:
            API Gateway response dictionary
        """
        try:
            # 1. Extract user ID if auth required
            if self.requires_auth:
                self.user_id = get_user_id(event)
                if self.user_id is None:
                    raise UnauthorizedError("Authentication required")
            else:
                self.user_id = None

            # 2. Extract parameters
            self.path_params = event.get('pathParameters') or {}
            self.query_params = event.get('queryStringParameters') or {}
            self.event = event
            self.context = context

            # 3. Parse body if configured
            if self.parse_body:
                self.body = parse_lambda_body(event)
            else:
                self.body = None

            # 4. Call before hook
            self.before_handle(event, context)

            # 5. Call handler logic
            result = self.handle(event, context)

            # 6. Call after hook
            result = self.after_handle(result)

            # 7. Format response
            return self._format_success(result)

        except UnauthorizedError as e:
            self.logger.warning("unauthorized_request", error=str(e))
            return error_response(str(e), 401)
        except ValidationError as e:
            self.logger.warning("validation_error", error=str(e), field=getattr(e, 'field', None))
            return error_response(str(e), 400)
        except Exception as e:
            # Check if it's a Pydantic ValidationError
            if e.__class__.__name__ == 'ValidationError' and hasattr(e, 'errors'):
                # Pydantic validation error
                errors = e.errors() if callable(getattr(e, 'errors', None)) else []
                error_msg = f"Validation failed: {len(errors)} error(s)"
                if errors:
                    # Format first error for user-friendly message
                    first_error = errors[0]
                    field = first_error.get('loc', ['unknown'])[-1]
                    msg = first_error.get('msg', 'validation error')
                    error_msg = f"Field '{field}': {msg}"
                self.logger.warning("pydantic_validation_error", error=str(e), errors=errors)
                return error_response(error_msg, 400)
            raise  # Re-raise to continue to other handlers
        except NotFoundError as e:
            self.logger.warning("resource_not_found", error=str(e))
            return error_response(str(e), 404)
        except ForbiddenError as e:
            self.logger.warning("forbidden_access", error=str(e))
            return error_response(str(e), 403)
        except BusinessError as e:
            self.logger.warning("business_rule_violation", error=str(e))
            return error_response(str(e), 400)
        except Exception as e:
            self.logger.error("handler_error", error=str(e), exc_info=True)
            return error_response('Internal server error', 500)

    def handle(self, event: Dict[str, Any], context: Any) -> Union[Any, Tuple[Any, str], Tuple[Any, str, int]]:
        """
        Handler logic - override this in subclasses.

        Args:
            event: Lambda event dictionary
            context: Lambda context object

        Returns:
            One of:
            - data (returns 200 with default message)
            - (data, message) (returns 200 with custom message)
            - (data, message, status_code) (returns custom status)

        Raises:
            Any exception will be caught and converted to appropriate error response
        """
        raise NotImplementedError("Subclasses must implement handle()")

    def before_handle(self, event: Dict[str, Any], context: Any) -> None:
        """
        Hook called before handle(). Override for custom pre-processing.

        Use cases:
        - Permission checks
        - Rate limiting
        - Custom logging
        - Request enrichment

        Args:
            event: Lambda event dictionary
            context: Lambda context object
        """
        pass

    def after_handle(self, result: Any) -> Any:
        """
        Hook called after handle(). Override for custom post-processing.

        Use cases:
        - Metrics collection
        - Response enrichment
        - Custom logging

        Args:
            result: Return value from handle()

        Returns:
            Modified result (or same result if no modification)
        """
        return result

    def _format_success(self, result: Any) -> Dict[str, Any]:
        """
        Format successful response.

        Args:
            result: Return value from handle()

        Returns:
            API Gateway response dictionary
        """
        # Handle different return formats
        if isinstance(result, tuple):
            if len(result) == 3:
                data, message, status_code = result
                return success_response(data, message, status_code)
            elif len(result) == 2:
                data, message = result
                return success_response(data, message)
            else:
                # Single item tuple - unwrap it
                return success_response(result[0])
        else:
            # Just data, use default message
            return success_response(result)
