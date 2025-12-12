"""
Default webhook event processors.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

import logging
from typing import Dict, Any
import stripe

from ..models.results import WebhookResult

logger = logging.getLogger(__name__)


async def process_checkout_completed(
    data: Dict[str, Any],
    event: stripe.Event,
) -> WebhookResult:
    """
    Process checkout.session.completed event.

    This is called when a customer completes checkout. The subscription
    should be created by Stripe automatically if mode was 'subscription'.
    """
    session_id = data.get("id")
    customer_id = data.get("customer")
    subscription_id = data.get("subscription")
    mode = data.get("mode")
    amount_total = data.get("amount_total", 0)
    currency = data.get("currency", "usd")

    logger.info(
        f"Checkout completed: session={session_id}, "
        f"customer={customer_id}, subscription={subscription_id}, "
        f"mode={mode}"
    )

    actions = [f"Checkout completed for session {session_id}"]

    if subscription_id:
        actions.append(f"Subscription {subscription_id} created")

    return WebhookResult.ok(
        event_id=event.id,
        event_type=event.type,
        actions=actions,
    )


async def process_subscription_created(
    data: Dict[str, Any],
    event: stripe.Event,
) -> WebhookResult:
    """
    Process customer.subscription.created event.

    Called when a new subscription is created.
    """
    subscription_id = data.get("id")
    customer_id = data.get("customer")
    status = data.get("status")
    plan_id = None

    # Get plan info from items
    items = data.get("items", {}).get("data", [])
    if items:
        plan_id = items[0].get("price", {}).get("product")

    logger.info(
        f"Subscription created: {subscription_id}, "
        f"customer={customer_id}, status={status}, plan={plan_id}"
    )

    return WebhookResult.ok(
        event_id=event.id,
        event_type=event.type,
        actions=[f"Subscription {subscription_id} created with status {status}"],
    )


async def process_subscription_updated(
    data: Dict[str, Any],
    event: stripe.Event,
) -> WebhookResult:
    """
    Process customer.subscription.updated event.

    Called when a subscription is modified (plan change, status change, etc.)
    """
    subscription_id = data.get("id")
    customer_id = data.get("customer")
    status = data.get("status")
    cancel_at_period_end = data.get("cancel_at_period_end", False)

    # Check what changed from previous_attributes
    previous = event.data.get("previous_attributes", {})

    logger.info(
        f"Subscription updated: {subscription_id}, "
        f"status={status}, cancel_at_period_end={cancel_at_period_end}"
    )

    actions = [f"Subscription {subscription_id} updated"]

    if "status" in previous:
        old_status = previous["status"]
        actions.append(f"Status changed: {old_status} -> {status}")

    if "cancel_at_period_end" in previous:
        if cancel_at_period_end:
            actions.append("Subscription scheduled for cancellation")
        else:
            actions.append("Subscription cancellation removed")

    if "items" in previous:
        actions.append("Plan changed")

    return WebhookResult.ok(
        event_id=event.id,
        event_type=event.type,
        actions=actions,
    )


async def process_subscription_deleted(
    data: Dict[str, Any],
    event: stripe.Event,
) -> WebhookResult:
    """
    Process customer.subscription.deleted event.

    Called when a subscription is cancelled and the period has ended.
    """
    subscription_id = data.get("id")
    customer_id = data.get("customer")

    logger.info(
        f"Subscription deleted: {subscription_id}, customer={customer_id}"
    )

    return WebhookResult.ok(
        event_id=event.id,
        event_type=event.type,
        actions=[f"Subscription {subscription_id} cancelled/deleted"],
    )


async def process_invoice_paid(
    data: Dict[str, Any],
    event: stripe.Event,
) -> WebhookResult:
    """
    Process invoice.paid event.

    Called when an invoice is successfully paid.
    """
    invoice_id = data.get("id")
    customer_id = data.get("customer")
    subscription_id = data.get("subscription")
    amount_paid = data.get("amount_paid", 0)
    currency = data.get("currency", "usd")

    logger.info(
        f"Invoice paid: {invoice_id}, "
        f"customer={customer_id}, amount={amount_paid} {currency}"
    )

    return WebhookResult.ok(
        event_id=event.id,
        event_type=event.type,
        actions=[
            f"Invoice {invoice_id} paid",
            f"Amount: {amount_paid / 100:.2f} {currency.upper()}",
        ],
    )


async def process_invoice_payment_failed(
    data: Dict[str, Any],
    event: stripe.Event,
) -> WebhookResult:
    """
    Process invoice.payment_failed event.

    Called when payment for an invoice fails.
    """
    invoice_id = data.get("id")
    customer_id = data.get("customer")
    subscription_id = data.get("subscription")
    attempt_count = data.get("attempt_count", 0)
    next_payment_attempt = data.get("next_payment_attempt")

    logger.warning(
        f"Invoice payment failed: {invoice_id}, "
        f"customer={customer_id}, attempt={attempt_count}"
    )

    actions = [f"Payment failed for invoice {invoice_id}"]
    actions.append(f"Attempt count: {attempt_count}")

    if next_payment_attempt:
        actions.append("Will retry automatically")
    else:
        actions.append("No more retries scheduled")

    return WebhookResult.ok(
        event_id=event.id,
        event_type=event.type,
        actions=actions,
    )


async def process_customer_created(
    data: Dict[str, Any],
    event: stripe.Event,
) -> WebhookResult:
    """
    Process customer.created event.

    Called when a new customer is created in Stripe.
    """
    customer_id = data.get("id")
    email = data.get("email")
    name = data.get("name")

    logger.info(f"Customer created: {customer_id}, email={email}")

    return WebhookResult.ok(
        event_id=event.id,
        event_type=event.type,
        actions=[f"Customer {customer_id} created"],
    )


async def process_customer_updated(
    data: Dict[str, Any],
    event: stripe.Event,
) -> WebhookResult:
    """
    Process customer.updated event.

    Called when customer information is updated.
    """
    customer_id = data.get("id")
    previous = event.data.get("previous_attributes", {})

    logger.info(f"Customer updated: {customer_id}")

    actions = [f"Customer {customer_id} updated"]
    for key in previous.keys():
        actions.append(f"Changed: {key}")

    return WebhookResult.ok(
        event_id=event.id,
        event_type=event.type,
        actions=actions,
    )


async def process_payment_method_attached(
    data: Dict[str, Any],
    event: stripe.Event,
) -> WebhookResult:
    """Process payment_method.attached event."""
    pm_id = data.get("id")
    customer_id = data.get("customer")
    pm_type = data.get("type")

    logger.info(
        f"Payment method attached: {pm_id}, "
        f"customer={customer_id}, type={pm_type}"
    )

    return WebhookResult.ok(
        event_id=event.id,
        event_type=event.type,
        actions=[f"Payment method {pm_id} attached to customer {customer_id}"],
    )


async def process_charge_succeeded(
    data: Dict[str, Any],
    event: stripe.Event,
) -> WebhookResult:
    """Process charge.succeeded event."""
    charge_id = data.get("id")
    amount = data.get("amount", 0)
    currency = data.get("currency", "usd")
    customer_id = data.get("customer")

    logger.info(
        f"Charge succeeded: {charge_id}, "
        f"amount={amount} {currency}, customer={customer_id}"
    )

    return WebhookResult.ok(
        event_id=event.id,
        event_type=event.type,
        actions=[f"Charge {charge_id} succeeded: {amount / 100:.2f} {currency.upper()}"],
    )


async def process_charge_failed(
    data: Dict[str, Any],
    event: stripe.Event,
) -> WebhookResult:
    """Process charge.failed event."""
    charge_id = data.get("id")
    failure_code = data.get("failure_code")
    failure_message = data.get("failure_message")
    customer_id = data.get("customer")

    logger.warning(
        f"Charge failed: {charge_id}, "
        f"code={failure_code}, message={failure_message}"
    )

    return WebhookResult.ok(
        event_id=event.id,
        event_type=event.type,
        actions=[f"Charge {charge_id} failed: {failure_message}"],
    )
