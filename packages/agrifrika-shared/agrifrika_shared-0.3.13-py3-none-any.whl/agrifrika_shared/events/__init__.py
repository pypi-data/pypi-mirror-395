"""
Event utilities for EventBridge-based async communication.

Provides a unified way to emit events for:
- Domain events (OrderCreated, ProductUpdated, etc.)
- Notification events (UserInvitationRequested, etc.)
- Metrics events (trigger pre-computation)
"""

from .emitter import (
    emit_event,
    emit_notification_event,
    emit_user_invitation,
    emit_client_invitation,
    EventSource,
    NotificationEventType
)
from .domain_events import (
    emit_order_created,
    emit_order_updated,
    emit_product_created,
    emit_product_updated
)

__all__ = [
    'emit_event',
    'emit_notification_event',
    'emit_user_invitation',
    'emit_client_invitation',
    'EventSource',
    'NotificationEventType',
    'emit_order_created',
    'emit_order_updated',
    'emit_product_created',
    'emit_product_updated'
]
