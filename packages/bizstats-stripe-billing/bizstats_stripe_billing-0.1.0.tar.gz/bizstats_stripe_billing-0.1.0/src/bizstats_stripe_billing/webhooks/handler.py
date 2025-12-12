"""
Webhook handler for processing Stripe events.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

import logging
from datetime import datetime, timezone
from typing import Dict, Any, Optional, Callable, Awaitable, Set
import stripe

from ..config import get_config, StripeConfig
from ..client import get_client, StripeClient
from ..models import WebhookEvent, WebhookEventType
from ..models.results import WebhookResult
from ..exceptions import WebhookSignatureError, WebhookEventAlreadyProcessedError

logger = logging.getLogger(__name__)

# Type for event handlers
WebhookEventHandler = Callable[[Dict[str, Any], stripe.Event], Awaitable[WebhookResult]]


class WebhookHandler:
    """
    Handler for processing Stripe webhook events.

    Provides:
    - Signature verification
    - Event routing
    - Idempotency handling
    - Error handling and logging

    Example:
        ```python
        handler = WebhookHandler()

        # Register custom handlers
        @handler.on(WebhookEventType.SUBSCRIPTION_CREATED)
        async def handle_subscription(data, event):
            # Process subscription created event
            return WebhookResult.ok(event.id, event.type)

        # Process incoming webhook
        result = await handler.process(payload, signature)
        ```
    """

    def __init__(
        self,
        config: Optional[StripeConfig] = None,
        client: Optional[StripeClient] = None,
    ):
        """
        Initialize webhook handler.

        Args:
            config: Optional Stripe configuration
            client: Optional Stripe client
        """
        self.config = config or get_config()
        self.client = client or get_client(self.config)
        self._handlers: Dict[str, WebhookEventHandler] = {}
        self._processed_events: Set[str] = set()

        # Optional callback for checking if event was processed
        self._check_processed: Optional[Callable[[str], Awaitable[bool]]] = None
        # Optional callback for marking event as processed
        self._mark_processed: Optional[Callable[[str], Awaitable[None]]] = None

    def on(
        self,
        event_type: WebhookEventType,
    ) -> Callable[[WebhookEventHandler], WebhookEventHandler]:
        """
        Decorator to register an event handler.

        Args:
            event_type: The event type to handle

        Returns:
            Decorator function
        """

        def decorator(handler: WebhookEventHandler) -> WebhookEventHandler:
            self._handlers[event_type.value] = handler
            return handler

        return decorator

    def register(
        self,
        event_type: WebhookEventType,
        handler: WebhookEventHandler,
    ) -> None:
        """
        Register an event handler.

        Args:
            event_type: The event type to handle
            handler: The handler function
        """
        self._handlers[event_type.value] = handler

    def set_processed_checker(
        self,
        checker: Callable[[str], Awaitable[bool]],
    ) -> None:
        """Set callback for checking if event was already processed."""
        self._check_processed = checker

    def set_processed_marker(
        self,
        marker: Callable[[str], Awaitable[None]],
    ) -> None:
        """Set callback for marking event as processed."""
        self._mark_processed = marker

    async def process(
        self,
        payload: bytes,
        signature: str,
    ) -> WebhookResult:
        """
        Process a webhook payload.

        Args:
            payload: Raw webhook payload bytes
            signature: Stripe-Signature header value

        Returns:
            WebhookResult indicating success or failure
        """
        try:
            # Verify signature and construct event
            event = self._verify_signature(payload, signature)
            event_id = event.id
            event_type = event.type
            data = event.data.object

            logger.info(f"Processing webhook event: {event_type} (ID: {event_id})")

            # Check if already processed
            if await self._is_already_processed(event_id):
                logger.info(f"Event {event_id} already processed, skipping")
                return WebhookResult.skipped(
                    event_id, event_type, "Already processed"
                )

            # Route to handler
            result = await self._route_event(event_type, data, event)

            # Mark as processed
            await self._mark_as_processed(event_id)

            return result

        except WebhookSignatureError as e:
            logger.error(f"Webhook signature verification failed: {e}")
            return WebhookResult.error(str(e))
        except Exception as e:
            logger.error(f"Error processing webhook: {e}")
            return WebhookResult.error(str(e))

    def _verify_signature(
        self,
        payload: bytes,
        signature: str,
    ) -> stripe.Event:
        """Verify webhook signature and construct event."""
        try:
            return stripe.Webhook.construct_event(
                payload,
                signature,
                self.config.webhook_secret,
                tolerance=self.config.webhook_tolerance,
            )
        except stripe.SignatureVerificationError as e:
            raise WebhookSignatureError(str(e))

    async def _is_already_processed(self, event_id: str) -> bool:
        """Check if event was already processed."""
        # Check in-memory set first
        if event_id in self._processed_events:
            return True

        # Use custom checker if available
        if self._check_processed:
            return await self._check_processed(event_id)

        return False

    async def _mark_as_processed(self, event_id: str) -> None:
        """Mark event as processed."""
        # Add to in-memory set
        self._processed_events.add(event_id)

        # Limit in-memory set size
        if len(self._processed_events) > 10000:
            # Remove oldest entries (approximately)
            to_remove = list(self._processed_events)[:5000]
            for item in to_remove:
                self._processed_events.discard(item)

        # Use custom marker if available
        if self._mark_processed:
            await self._mark_processed(event_id)

    async def _route_event(
        self,
        event_type: str,
        data: Dict[str, Any],
        event: stripe.Event,
    ) -> WebhookResult:
        """Route event to appropriate handler."""
        handler = self._handlers.get(event_type)

        if handler:
            try:
                return await handler(data, event)
            except Exception as e:
                logger.error(f"Error in handler for {event_type}: {e}")
                return WebhookResult.error(
                    str(e), event_id=event.id, event_type=event_type
                )
        else:
            # No handler registered - consider it handled
            logger.info(f"No handler registered for event type: {event_type}")
            return WebhookResult.ok(
                event_id=event.id,
                event_type=event_type,
                actions=["No handler registered"],
            )


# Default handlers that can be registered


def create_default_handler() -> WebhookHandler:
    """Create a WebhookHandler with default handlers registered."""
    from .events import (
        process_checkout_completed,
        process_subscription_created,
        process_subscription_updated,
        process_subscription_deleted,
        process_invoice_paid,
        process_invoice_payment_failed,
        process_customer_created,
        process_customer_updated,
    )

    handler = WebhookHandler()

    # Register default handlers
    handler.register(
        WebhookEventType.CHECKOUT_SESSION_COMPLETED,
        process_checkout_completed,
    )
    handler.register(
        WebhookEventType.SUBSCRIPTION_CREATED,
        process_subscription_created,
    )
    handler.register(
        WebhookEventType.SUBSCRIPTION_UPDATED,
        process_subscription_updated,
    )
    handler.register(
        WebhookEventType.SUBSCRIPTION_DELETED,
        process_subscription_deleted,
    )
    handler.register(
        WebhookEventType.INVOICE_PAID,
        process_invoice_paid,
    )
    handler.register(
        WebhookEventType.INVOICE_PAYMENT_FAILED,
        process_invoice_payment_failed,
    )
    handler.register(
        WebhookEventType.CUSTOMER_CREATED,
        process_customer_created,
    )
    handler.register(
        WebhookEventType.CUSTOMER_UPDATED,
        process_customer_updated,
    )

    return handler
