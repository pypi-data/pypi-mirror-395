"""
Convenience functions for emitting domain events.

These are high-level functions that wrap emit_event with domain-specific details.
"""

from typing import Optional
from .emitter import emit_event, EventSource


def emit_order_created(
    order_id: str,
    aggregator_id: Optional[str],
    status: str,
    total_amount: float
) -> None:
    """
    Emit OrderCreated event for metrics tracking.

    Args:
        order_id: Order ID
        aggregator_id: Aggregator ID (if any)
        status: Order status
        total_amount: Order total amount
    """
    emit_event(
        source=EventSource.ORDER_SERVICE.value,
        detail_type='OrderCreated',
        detail={
            'order_id': order_id,
            'aggregator_id': aggregator_id,
            'status': status,
            'total_amount': total_amount
        }
    )


def emit_order_updated(
    order_id: str,
    aggregator_id: Optional[str],
    old_status: str,
    status: str,
    total_amount: float
) -> None:
    """
    Emit OrderUpdated event for metrics tracking.

    Args:
        order_id: Order ID
        aggregator_id: Aggregator ID (if any)
        old_status: Previous order status
        status: New order status
        total_amount: Order total amount
    """
    emit_event(
        source=EventSource.ORDER_SERVICE.value,
        detail_type='OrderUpdated',
        detail={
            'order_id': order_id,
            'aggregator_id': aggregator_id,
            'old_status': old_status,
            'status': status,
            'total_amount': total_amount
        }
    )


def emit_product_created(
    product_id: str,
    aggregator_id: Optional[str],
    status: str,
    quantity: float
) -> None:
    """
    Emit ProductCreated event for metrics tracking.

    Args:
        product_id: Product request ID
        aggregator_id: Aggregator ID (if any)
        status: Product request status
        quantity: Requested quantity
    """
    emit_event(
        source=EventSource.PRODUCT_SERVICE.value,
        detail_type='ProductCreated',
        detail={
            'product_id': product_id,
            'aggregator_id': aggregator_id,
            'status': status,
            'quantity': quantity
        }
    )


def emit_product_updated(
    product_id: str,
    aggregator_id: Optional[str],
    old_status: str,
    status: str,
    quantity: float
) -> None:
    """
    Emit ProductUpdated event for metrics tracking.

    Args:
        product_id: Product request ID
        aggregator_id: Aggregator ID (if any)
        old_status: Previous status
        status: New status
        quantity: Requested quantity
    """
    emit_event(
        source=EventSource.PRODUCT_SERVICE.value,
        detail_type='ProductUpdated',
        detail={
            'product_id': product_id,
            'aggregator_id': aggregator_id,
            'old_status': old_status,
            'status': status,
            'quantity': quantity
        }
    )
