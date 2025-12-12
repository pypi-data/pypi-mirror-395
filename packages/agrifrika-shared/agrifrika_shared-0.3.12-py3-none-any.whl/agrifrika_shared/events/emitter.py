"""
EventBridge event emitter for async communication between services.

Replaces synchronous Lambda invocations with async event-driven patterns.
"""

import json
import os
from typing import Dict, Any, Optional, List
from enum import Enum
from datetime import datetime, timezone
from ..utils.logger import get_logger
from ..aws.clients import get_events_client

logger = get_logger(__name__)


class EventSource(str, Enum):
    """Standard event sources."""
    ORDER_SERVICE = "order.service"
    PRODUCT_SERVICE = "product.service"
    AGGREGATOR_SERVICE = "aggregator.service"
    USER_SERVICE = "user.service"
    CLIENT_SERVICE = "client.service"
    NOTIFICATION_SERVICE = "notification.service"


class NotificationEventType(str, Enum):
    """Notification event types."""
    USER_INVITATION_REQUESTED = "UserInvitationRequested"
    CLIENT_INVITATION_REQUESTED = "ClientInvitationRequested"
    PASSWORD_RESET_REQUESTED = "PasswordResetRequested"
    ORDER_CONFIRMATION_REQUESTED = "OrderConfirmationRequested"
    WELCOME_EMAIL_REQUESTED = "WelcomeEmailRequested"


def _get_eventbridge_client():
    """Get EventBridge client."""
    return get_events_client()


def emit_event(
    source: str,
    detail_type: str,
    detail: Dict[str, Any],
    event_bus_name: str = 'default',
    resources: Optional[List[str]] = None
) -> bool:
    """
    Emit an event to EventBridge.

    Args:
        source: Event source (e.g., 'order.service')
        detail_type: Type of event (e.g., 'OrderCreated')
        detail: Event payload (will be JSON serialized)
        event_bus_name: EventBridge bus name (default: 'default')
        resources: Optional list of resource ARNs

    Returns:
        bool: True if event was successfully emitted

    Example:
        emit_event(
            source=EventSource.ORDER_SERVICE,
            detail_type='OrderCreated',
            detail={
                'order_id': 'ord-123',
                'aggregator_id': 'agg-456',
                'total_amount': 150.00
            }
        )
    """
    try:
        client = _get_eventbridge_client()

        # Ensure detail has required metadata
        enriched_detail = {
            **detail,
            '_emitted_at': datetime.now(timezone.utc).isoformat(),
            '_source': source,
            '_detail_type': detail_type
        }

        entry = {
            'Time': datetime.now(timezone.utc),
            'Source': source,
            'DetailType': detail_type,
            'Detail': json.dumps(enriched_detail, default=str),
            'EventBusName': event_bus_name
        }

        if resources:
            entry['Resources'] = resources

        response = client.put_events(Entries=[entry])

        # Check for failures
        if response.get('FailedEntryCount', 0) > 0:
            failed_entries = response.get('Entries', [])
            logger.error(
                "event_emission_failed",
                source=source,
                detail_type=detail_type,
                failed_entries=failed_entries
            )
            return False

        logger.info(
            "event_emitted",
            source=source,
            detail_type=detail_type,
            event_id=response['Entries'][0]['EventId']
        )
        return True

    except Exception as e:
        logger.error(
            "event_emission_error",
            source=source,
            detail_type=detail_type,
            error=str(e),
            exc_info=True
        )
        return False


def emit_notification_event(
    notification_type: NotificationEventType,
    recipient_email: str,
    payload: Dict[str, Any],
    source: str = EventSource.AGGREGATOR_SERVICE
) -> bool:
    """
    Emit a notification event for async delivery.

    This replaces synchronous invoke_notification_service() calls.
    Notification service listens to these events and sends emails/SMS.

    Args:
        notification_type: Type of notification
        recipient_email: Email address of recipient
        payload: Notification payload (template data)
        source: Service emitting the notification (default: aggregator.service)

    Returns:
        bool: True if event was successfully emitted

    Example:
        emit_notification_event(
            notification_type=NotificationEventType.USER_INVITATION_REQUESTED,
            recipient_email='user@example.com',
            payload={
                'first_name': 'John',
                'last_name': 'Doe',
                'temporary_password': 'TempPass123!',
                'aggregator_name': 'My Company',
                'login_url': 'https://app.agrifrika.com'
            }
        )
    """
    detail = {
        'notification_type': notification_type.value,
        'recipient_email': recipient_email,
        'payload': payload,
        'requested_at': datetime.now(timezone.utc).isoformat()
    }

    return emit_event(
        source=source,
        detail_type=notification_type.value,
        detail=detail
    )


def emit_user_invitation(
    user_email: str,
    first_name: str,
    last_name: str,
    temporary_password: str,
    aggregator_name: str,
    aggregator_email: str,
    user_id: str
) -> bool:
    """
    Emit user invitation notification event.

    Convenience wrapper for emitting user invitations.

    Args:
        user_email: User's email address
        first_name: User's first name
        last_name: User's last name
        temporary_password: Temporary password
        aggregator_name: Name of the aggregator
        aggregator_email: Aggregator contact email
        user_id: ID of the created user

    Returns:
        bool: True if event was successfully emitted
    """
    return emit_notification_event(
        notification_type=NotificationEventType.USER_INVITATION_REQUESTED,
        recipient_email=user_email,
        payload={
            'first_name': first_name,
            'last_name': last_name,
            'temporary_password': temporary_password,
            'aggregator_name': aggregator_name,
            'aggregator_email': aggregator_email,
            'user_id': user_id,
            'login_url': os.environ.get('APP_URL', 'https://app.agrifrika.com')
        }
    )


def emit_client_invitation(
    client_email: str,
    first_name: str,
    last_name: str,
    temporary_password: str,
    aggregator_name: str,
    aggregator_email: str,
    client_id: str,
    business_address: Optional[Dict[str, Any]] = None
) -> bool:
    """
    Emit client invitation notification event.

    Convenience wrapper for emitting client invitations.

    Args:
        client_email: Client's email address
        first_name: Client's first name
        last_name: Client's last name
        temporary_password: Temporary password
        aggregator_name: Name of the aggregator
        aggregator_email: Aggregator contact email
        client_id: ID of the created client
        business_address: Optional business address

    Returns:
        bool: True if event was successfully emitted
    """
    payload = {
        'first_name': first_name,
        'last_name': last_name,
        'temporary_password': temporary_password,
        'aggregator_name': aggregator_name,
        'aggregator_email': aggregator_email,
        'client_id': client_id,
        'login_url': os.environ.get('APP_URL', 'https://app.agrifrika.com')
    }

    if business_address:
        payload['business_address'] = business_address

    return emit_notification_event(
        notification_type=NotificationEventType.CLIENT_INVITATION_REQUESTED,
        recipient_email=client_email,
        payload=payload
    )


def emit_order_created(
    order_id: str,
    aggregator_id: str,
    status: str,
    total_amount: float,
    customer_id: Optional[str] = None,
    **additional_fields
) -> bool:
    """
    Emit OrderCreated event for metrics tracking.

    Args:
        order_id: ID of the created order
        aggregator_id: ID of the aggregator
        status: Order status (pending, completed, etc.)
        total_amount: Total order amount
        customer_id: Optional customer ID
        **additional_fields: Any additional order fields

    Returns:
        bool: True if event was successfully emitted
    """
    detail = {
        'order_id': order_id,
        'aggregator_id': aggregator_id,
        'status': status,
        'total_amount': total_amount,
        'created_at': datetime.now(timezone.utc).isoformat(),
        **additional_fields
    }

    if customer_id:
        detail['customer_id'] = customer_id

    return emit_event(
        source=EventSource.ORDER_SERVICE,
        detail_type='OrderCreated',
        detail=detail
    )


def emit_order_updated(
    order_id: str,
    aggregator_id: str,
    status: str,
    old_status: str,
    total_amount: float,
    changes: Optional[Dict[str, Any]] = None,
    **additional_fields
) -> bool:
    """
    Emit OrderUpdated event for metrics tracking.

    Args:
        order_id: ID of the updated order
        aggregator_id: ID of the aggregator
        status: New order status
        old_status: Previous order status
        total_amount: Total order amount
        changes: Dict of what changed (for delta calculations)
        **additional_fields: Any additional order fields

    Returns:
        bool: True if event was successfully emitted
    """
    detail = {
        'order_id': order_id,
        'aggregator_id': aggregator_id,
        'status': status,
        'old_status': old_status,
        'total_amount': total_amount,
        'updated_at': datetime.now(timezone.utc).isoformat(),
        **additional_fields
    }

    if changes:
        detail['changes'] = changes

    return emit_event(
        source=EventSource.ORDER_SERVICE,
        detail_type='OrderUpdated',
        detail=detail
    )


def emit_product_created(
    product_id: str,
    aggregator_id: str,
    status: str,
    stock: int,
    price: float,
    **additional_fields
) -> bool:
    """
    Emit ProductCreated event for metrics tracking.

    Args:
        product_id: ID of the created product
        aggregator_id: ID of the aggregator
        status: Product status (active, inactive)
        stock: Current stock level
        price: Product price
        **additional_fields: Any additional product fields

    Returns:
        bool: True if event was successfully emitted
    """
    detail = {
        'product_id': product_id,
        'aggregator_id': aggregator_id,
        'status': status,
        'stock': stock,
        'price': price,
        'created_at': datetime.now(timezone.utc).isoformat(),
        **additional_fields
    }

    return emit_event(
        source=EventSource.PRODUCT_SERVICE,
        detail_type='ProductCreated',
        detail=detail
    )


def emit_product_updated(
    product_id: str,
    aggregator_id: str,
    status: str,
    stock: int,
    old_stock: Optional[int] = None,
    changes: Optional[Dict[str, Any]] = None,
    **additional_fields
) -> bool:
    """
    Emit ProductUpdated event for metrics tracking.

    Args:
        product_id: ID of the updated product
        aggregator_id: ID of the aggregator
        status: Product status
        stock: New stock level
        old_stock: Previous stock level (for delta calculations)
        changes: Dict of what changed
        **additional_fields: Any additional product fields

    Returns:
        bool: True if event was successfully emitted
    """
    detail = {
        'product_id': product_id,
        'aggregator_id': aggregator_id,
        'status': status,
        'stock': stock,
        'updated_at': datetime.now(timezone.utc).isoformat(),
        **additional_fields
    }

    if old_stock is not None:
        detail['old_stock'] = old_stock

    if changes:
        detail['changes'] = changes

    return emit_event(
        source=EventSource.PRODUCT_SERVICE,
        detail_type='ProductUpdated',
        detail=detail
    )


def emit_user_logged_in(
    user_id: str,
    login_timestamp: datetime,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    login_method: str = 'password',
    **additional_fields
) -> bool:
    """
    Emit UserLoggedIn event for metrics tracking and analytics.

    Args:
        user_id: ID of the user who logged in
        login_timestamp: Timestamp of login
        ip_address: Optional IP address of the login
        user_agent: Optional user agent string
        login_method: Login method (password, passwordless, oauth, etc.)
        **additional_fields: Any additional login fields

    Returns:
        bool: True if event was successfully emitted
    """
    detail = {
        'user_id': user_id,
        'login_timestamp': login_timestamp.isoformat() if isinstance(login_timestamp, datetime) else login_timestamp,
        'login_method': login_method,
        **additional_fields
    }

    if ip_address:
        detail['ip_address'] = ip_address

    if user_agent:
        detail['user_agent'] = user_agent

    return emit_event(
        source=EventSource.USER_SERVICE,
        detail_type='UserLoggedIn',
        detail=detail
    )
