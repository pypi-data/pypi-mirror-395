"""
Notification helper utilities to invoke the centralized notification service.
"""

from typing import Dict, Any, Optional, Tuple
from agrifrika_shared.utils.logger import get_logger
from agrifrika_shared.aws.clients import get_lambda_client
import json
import os


logger = get_logger(__name__)

_REGION = os.environ.get('REGION', 'us-east-1')
_DEFAULT_FUNCTION = os.environ.get('NOTIFICATION_SERVICE_FUNCTION_NAME')


def _get_lambda_client():
    return get_lambda_client()


def invoke_notification_service(
    *,
    payload: Dict[str, Any],
    path: str,
    http_method: str = 'POST',
    function_name: Optional[str] = None
) -> Tuple[bool, str]:
    """
    Call the shared notification service Lambda/API and return (success, message).
    """
    target_function = function_name or _DEFAULT_FUNCTION
    if not target_function:
        logger.warning("notification_service_not_configured")
        return False, "Notification service not configured"

    client = _get_lambda_client()

    try:
        response = client.invoke(
            FunctionName=target_function,
            InvocationType='RequestResponse',
            Payload=json.dumps({
                "httpMethod": http_method,
                "path": path,
                "body": json.dumps(payload)
            })
        )

        response_payload = json.loads(response['Payload'].read())
        status_code = response_payload.get('statusCode', 500)
        logger.info("notification_service_response", status_code=status_code)

        if status_code in (200, 202, 207):
            body = json.loads(response_payload.get('body', '{}'))
            data = body.get('data', {})
            summary = data.get('summary', {})

            if status_code == 202:
                return True, body.get('message', 'Invitation queued for delivery')

            if summary.get('any_succeeded'):
                success_channels = [ch['channel'] for ch in summary.get('successful_channels', [])]
                return True, f"Invitation sent via: {', '.join(success_channels)}"

            return False, "Failed to send invitation on all channels"

        error_body = json.loads(response_payload.get('body', '{}'))
        return False, error_body.get('message', 'Unknown notification error')

    except Exception as exc:  # pragma: no cover - defensive
        logger.error(
            "notification_service_invocation_failed",
            error=str(exc),
            exc_info=True
        )
        return False, f"Notification service error: {str(exc)}"
