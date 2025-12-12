"""
Tests for webhook handling module.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime, timezone
import stripe

from bizstats_stripe_billing import (
    WebhookHandler,
    WebhookEventHandler,
    WebhookEventType,
    StripeConfig,
)
from bizstats_stripe_billing.webhooks.handler import create_default_handler
from bizstats_stripe_billing.webhooks.events import (
    process_checkout_completed,
    process_subscription_created,
    process_subscription_updated,
    process_subscription_deleted,
    process_invoice_paid,
    process_invoice_payment_failed,
    process_customer_created,
    process_customer_updated,
)
from bizstats_stripe_billing.models.results import WebhookResult
from bizstats_stripe_billing.exceptions import WebhookSignatureError


class TestWebhookHandler:
    """Tests for WebhookHandler class."""

    def test_handler_initialization(self, test_config):
        """Test handler initializes with config."""
        handler = WebhookHandler(test_config)
        assert handler.config == test_config
        assert handler._handlers == {}

    def test_register_handler(self, webhook_handler):
        """Test registering an event handler."""
        async def custom_handler(data, event):
            return WebhookResult.ok(event.id, event.type)

        webhook_handler.register(
            WebhookEventType.SUBSCRIPTION_CREATED,
            custom_handler,
        )
        assert WebhookEventType.SUBSCRIPTION_CREATED.value in webhook_handler._handlers

    def test_register_handler_decorator(self, webhook_handler):
        """Test registering handler with decorator."""
        @webhook_handler.on(WebhookEventType.INVOICE_PAID)
        async def handle_invoice(data, event):
            return WebhookResult.ok(event.id, event.type)

        assert WebhookEventType.INVOICE_PAID.value in webhook_handler._handlers

    def test_set_processed_checker(self, webhook_handler):
        """Test setting custom processed checker."""
        async def check_processed(event_id):
            return event_id == "already_processed"

        webhook_handler.set_processed_checker(check_processed)
        assert webhook_handler._check_processed is not None

    def test_set_processed_marker(self, webhook_handler):
        """Test setting custom processed marker."""
        async def mark_processed(event_id):
            pass

        webhook_handler.set_processed_marker(mark_processed)
        assert webhook_handler._mark_processed is not None


class TestWebhookProcessing:
    """Tests for webhook event processing."""

    @pytest.mark.asyncio
    async def test_process_valid_event(self, webhook_handler, mock_stripe_event):
        """Test processing a valid webhook event."""
        # Register a handler
        @webhook_handler.on(WebhookEventType.SUBSCRIPTION_CREATED)
        async def handle_subscription(data, event):
            return WebhookResult.ok(event.id, event.type, ["Processed"])

        with patch.object(webhook_handler, "_verify_signature", return_value=mock_stripe_event):
            result = await webhook_handler.process(
                payload=b'{"test": "data"}',
                signature="t=123,v1=abc",
            )
            assert result.success is True
            assert result.event_id == "evt_test123"

    @pytest.mark.asyncio
    async def test_process_invalid_signature(self, webhook_handler):
        """Test processing event with invalid signature."""
        with patch.object(
            webhook_handler,
            "_verify_signature",
            side_effect=WebhookSignatureError("Invalid signature"),
        ):
            result = await webhook_handler.process(
                payload=b'{"test": "data"}',
                signature="invalid",
            )
            assert result.success is False
            assert "Invalid signature" in result.error_message

    @pytest.mark.asyncio
    async def test_process_already_processed_event(self, webhook_handler, mock_stripe_event):
        """Test processing an already processed event."""
        # Add event to processed set
        webhook_handler._processed_events.add("evt_test123")

        with patch.object(webhook_handler, "_verify_signature", return_value=mock_stripe_event):
            result = await webhook_handler.process(
                payload=b'{"test": "data"}',
                signature="t=123,v1=abc",
            )
            assert result.success is True
            assert result.processed is False  # skipped events have processed=False

    @pytest.mark.asyncio
    async def test_process_unhandled_event(self, webhook_handler, mock_stripe_event):
        """Test processing event with no registered handler."""
        # Change event type to something unhandled
        mock_stripe_event.type = "unhandled.event.type"

        with patch.object(webhook_handler, "_verify_signature", return_value=mock_stripe_event):
            result = await webhook_handler.process(
                payload=b'{"test": "data"}',
                signature="t=123,v1=abc",
            )
            # Should still succeed but indicate no handler
            assert result.success is True
            assert "No handler registered" in result.actions[0]

    @pytest.mark.asyncio
    async def test_process_handler_error(self, webhook_handler, mock_stripe_event):
        """Test processing when handler raises an error."""
        @webhook_handler.on(WebhookEventType.SUBSCRIPTION_CREATED)
        async def failing_handler(data, event):
            raise ValueError("Handler error")

        with patch.object(webhook_handler, "_verify_signature", return_value=mock_stripe_event):
            result = await webhook_handler.process(
                payload=b'{"test": "data"}',
                signature="t=123,v1=abc",
            )
            assert result.success is False
            assert "Handler error" in result.error_message

    @pytest.mark.asyncio
    async def test_custom_processed_checker(self, webhook_handler, mock_stripe_event):
        """Test using custom processed checker."""
        async def check_processed(event_id):
            return event_id == "evt_test123"

        webhook_handler.set_processed_checker(check_processed)

        with patch.object(webhook_handler, "_verify_signature", return_value=mock_stripe_event):
            result = await webhook_handler.process(
                payload=b'{"test": "data"}',
                signature="t=123,v1=abc",
            )
            assert result.processed is False  # skipped events have processed=False

    @pytest.mark.asyncio
    async def test_custom_processed_marker(self, webhook_handler, mock_stripe_event):
        """Test using custom processed marker."""
        marked_events = []

        async def mark_processed(event_id):
            marked_events.append(event_id)

        webhook_handler.set_processed_marker(mark_processed)

        @webhook_handler.on(WebhookEventType.SUBSCRIPTION_CREATED)
        async def handle_subscription(data, event):
            return WebhookResult.ok(event.id, event.type)

        with patch.object(webhook_handler, "_verify_signature", return_value=mock_stripe_event):
            await webhook_handler.process(
                payload=b'{"test": "data"}',
                signature="t=123,v1=abc",
            )
            assert "evt_test123" in marked_events


class TestSignatureVerification:
    """Tests for webhook signature verification."""

    def test_verify_signature_success(self, webhook_handler, mock_stripe_event):
        """Test successful signature verification."""
        with patch.object(stripe.Webhook, "construct_event", return_value=mock_stripe_event):
            event = webhook_handler._verify_signature(
                payload=b'{"test": "data"}',
                signature="t=123,v1=abc",
            )
            assert event.id == "evt_test123"

    def test_verify_signature_failure(self, webhook_handler):
        """Test signature verification failure."""
        error = stripe.SignatureVerificationError("Bad signature", "sig")
        with patch.object(stripe.Webhook, "construct_event", side_effect=error):
            with pytest.raises(WebhookSignatureError):
                webhook_handler._verify_signature(
                    payload=b'{"test": "data"}',
                    signature="invalid",
                )


class TestIdempotencyHandling:
    """Tests for idempotency handling."""

    @pytest.mark.asyncio
    async def test_in_memory_idempotency(self, webhook_handler):
        """Test in-memory idempotency check."""
        # Not processed
        result = await webhook_handler._is_already_processed("evt_new")
        assert result is False

        # Add to processed
        webhook_handler._processed_events.add("evt_new")

        # Now processed
        result = await webhook_handler._is_already_processed("evt_new")
        assert result is True

    @pytest.mark.asyncio
    async def test_mark_as_processed(self, webhook_handler):
        """Test marking event as processed."""
        await webhook_handler._mark_as_processed("evt_mark")
        assert "evt_mark" in webhook_handler._processed_events

    @pytest.mark.asyncio
    async def test_processed_set_size_limit(self, webhook_handler):
        """Test that processed set size is limited."""
        # Add many events
        for i in range(11000):
            webhook_handler._processed_events.add(f"evt_{i}")

        # Mark another as processed (triggers cleanup)
        await webhook_handler._mark_as_processed("evt_trigger")

        # Set should be reduced
        assert len(webhook_handler._processed_events) <= 6001


class TestDefaultEventProcessors:
    """Tests for default event processors."""

    @pytest.mark.asyncio
    async def test_process_checkout_completed(self, mock_stripe_event):
        """Test checkout completed processor."""
        mock_stripe_event.type = "checkout.session.completed"
        data = {
            "id": "cs_test123",
            "customer": "cus_test123",
            "subscription": "sub_test123",
            "mode": "subscription",
            "amount_total": 2900,
            "currency": "usd",
        }

        result = await process_checkout_completed(data, mock_stripe_event)
        assert result.success is True
        assert "Checkout completed" in result.actions[0]

    @pytest.mark.asyncio
    async def test_process_subscription_created(self, mock_stripe_event):
        """Test subscription created processor."""
        mock_stripe_event.type = "customer.subscription.created"
        data = {
            "id": "sub_test123",
            "customer": "cus_test123",
            "status": "active",
            "items": {"data": [{"price": {"product": "prod_test123"}}]},
        }

        result = await process_subscription_created(data, mock_stripe_event)
        assert result.success is True
        assert "created" in result.actions[0].lower()

    @pytest.mark.asyncio
    async def test_process_subscription_updated(self, mock_stripe_event):
        """Test subscription updated processor."""
        mock_stripe_event.type = "customer.subscription.updated"
        mock_stripe_event.data.previous_attributes = {"status": "trialing"}
        data = {
            "id": "sub_test123",
            "customer": "cus_test123",
            "status": "active",
            "cancel_at_period_end": False,
        }

        result = await process_subscription_updated(data, mock_stripe_event)
        assert result.success is True
        assert any("updated" in action.lower() for action in result.actions)

    @pytest.mark.asyncio
    async def test_process_subscription_updated_with_cancellation(self, mock_stripe_event):
        """Test subscription updated with cancellation scheduled."""
        mock_stripe_event.type = "customer.subscription.updated"
        mock_stripe_event.data.previous_attributes = {"cancel_at_period_end": False}
        data = {
            "id": "sub_test123",
            "customer": "cus_test123",
            "status": "active",
            "cancel_at_period_end": True,
        }

        result = await process_subscription_updated(data, mock_stripe_event)
        assert result.success is True
        assert any("cancellation" in action.lower() for action in result.actions)

    @pytest.mark.asyncio
    async def test_process_subscription_deleted(self, mock_stripe_event):
        """Test subscription deleted processor."""
        mock_stripe_event.type = "customer.subscription.deleted"
        data = {
            "id": "sub_test123",
            "customer": "cus_test123",
        }

        result = await process_subscription_deleted(data, mock_stripe_event)
        assert result.success is True
        assert any("cancelled" in action.lower() or "deleted" in action.lower() for action in result.actions)

    @pytest.mark.asyncio
    async def test_process_invoice_paid(self, mock_stripe_event):
        """Test invoice paid processor."""
        mock_stripe_event.type = "invoice.paid"
        data = {
            "id": "in_test123",
            "customer": "cus_test123",
            "subscription": "sub_test123",
            "amount_paid": 2900,
            "currency": "usd",
        }

        result = await process_invoice_paid(data, mock_stripe_event)
        assert result.success is True
        assert any("paid" in action.lower() for action in result.actions)

    @pytest.mark.asyncio
    async def test_process_invoice_payment_failed(self, mock_stripe_event):
        """Test invoice payment failed processor."""
        mock_stripe_event.type = "invoice.payment_failed"
        data = {
            "id": "in_test123",
            "customer": "cus_test123",
            "subscription": "sub_test123",
            "attempt_count": 2,
            "next_payment_attempt": int(datetime.now(timezone.utc).timestamp()) + 86400,
        }

        result = await process_invoice_payment_failed(data, mock_stripe_event)
        assert result.success is True
        assert any("failed" in action.lower() for action in result.actions)

    @pytest.mark.asyncio
    async def test_process_invoice_payment_failed_no_retry(self, mock_stripe_event):
        """Test invoice payment failed with no more retries."""
        mock_stripe_event.type = "invoice.payment_failed"
        data = {
            "id": "in_test123",
            "customer": "cus_test123",
            "attempt_count": 4,
            "next_payment_attempt": None,
        }

        result = await process_invoice_payment_failed(data, mock_stripe_event)
        assert result.success is True
        assert any("no more retries" in action.lower() for action in result.actions)

    @pytest.mark.asyncio
    async def test_process_customer_created(self, mock_stripe_event):
        """Test customer created processor."""
        mock_stripe_event.type = "customer.created"
        data = {
            "id": "cus_test123",
            "email": "test@example.com",
            "name": "Test User",
        }

        result = await process_customer_created(data, mock_stripe_event)
        assert result.success is True
        assert any("created" in action.lower() for action in result.actions)

    @pytest.mark.asyncio
    async def test_process_customer_updated(self, mock_stripe_event):
        """Test customer updated processor."""
        mock_stripe_event.type = "customer.updated"
        mock_stripe_event.data.previous_attributes = {"email": "old@example.com"}
        data = {
            "id": "cus_test123",
            "email": "new@example.com",
        }

        result = await process_customer_updated(data, mock_stripe_event)
        assert result.success is True
        assert any("updated" in action.lower() for action in result.actions)


class TestCreateDefaultHandler:
    """Tests for create_default_handler function."""

    def test_create_default_handler(self, test_config):
        """Test creating handler with default processors."""
        # Clear module-level config
        import bizstats_stripe_billing.config as config_module
        config_module._config = test_config

        handler = create_default_handler()
        assert isinstance(handler, WebhookHandler)

        # Check that default handlers are registered
        assert "checkout.session.completed" in handler._handlers
        assert "customer.subscription.created" in handler._handlers
        assert "customer.subscription.updated" in handler._handlers
        assert "customer.subscription.deleted" in handler._handlers
        assert "invoice.paid" in handler._handlers
        assert "invoice.payment_failed" in handler._handlers
        assert "customer.created" in handler._handlers
        assert "customer.updated" in handler._handlers
