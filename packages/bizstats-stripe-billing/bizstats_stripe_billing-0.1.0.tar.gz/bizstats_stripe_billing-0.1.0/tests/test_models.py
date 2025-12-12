"""
Tests for models module (enums, schemas, results).

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

import pytest
from datetime import datetime, timezone

from bizstats_stripe_billing import (
    # Enums
    SubscriptionStatus,
    BillingPeriod,
    PaymentStatus,
    InvoiceStatus,
    WebhookEventType,
    # Schemas
    Customer,
    CustomerCreate,
    CustomerUpdate,
    Subscription,
    SubscriptionCreate,
    SubscriptionUpdate,
    Plan,
    PlanPrice,
    PlanLimits,
    Invoice,
    PaymentMethod,
    CheckoutSession,
    CheckoutSessionCreate,
    UsageRecord,
    UsageRecordCreate,
    WebhookEvent,
    BillingPortalSession,
    # Results
    OperationResult,
    CustomerResult,
    SubscriptionResult,
    CheckoutResult,
    PortalResult,
    WebhookResult,
)


class TestEnums:
    """Tests for enum types."""

    def test_subscription_status_values(self):
        """Test SubscriptionStatus enum values."""
        assert SubscriptionStatus.ACTIVE == "active"
        assert SubscriptionStatus.TRIALING == "trialing"
        assert SubscriptionStatus.PAST_DUE == "past_due"
        assert SubscriptionStatus.CANCELED == "canceled"
        assert SubscriptionStatus.UNPAID == "unpaid"
        assert SubscriptionStatus.INCOMPLETE == "incomplete"

    def test_billing_period_values(self):
        """Test BillingPeriod enum values."""
        assert BillingPeriod.DAILY == "day"
        assert BillingPeriod.WEEKLY == "week"
        assert BillingPeriod.MONTHLY == "month"
        assert BillingPeriod.YEARLY == "year"

    def test_webhook_event_type_values(self):
        """Test WebhookEventType enum values."""
        assert WebhookEventType.CHECKOUT_SESSION_COMPLETED == "checkout.session.completed"
        assert WebhookEventType.SUBSCRIPTION_CREATED == "customer.subscription.created"
        assert WebhookEventType.INVOICE_PAID == "invoice.paid"

    def test_payment_status_values(self):
        """Test PaymentStatus enum values."""
        assert PaymentStatus.PENDING == "pending"
        assert PaymentStatus.SUCCEEDED == "succeeded"
        assert PaymentStatus.FAILED == "failed"
        assert PaymentStatus.CANCELED == "canceled"

    def test_invoice_status_values(self):
        """Test InvoiceStatus enum values."""
        assert InvoiceStatus.DRAFT == "draft"
        assert InvoiceStatus.OPEN == "open"
        assert InvoiceStatus.PAID == "paid"
        assert InvoiceStatus.VOID == "void"


class TestCustomerSchemas:
    """Tests for customer-related schemas."""

    def test_customer_create_minimal(self):
        """Test CustomerCreate with minimal fields."""
        customer = CustomerCreate(email="test@example.com")
        assert customer.email == "test@example.com"
        assert customer.name is None
        assert customer.organization_id is None

    def test_customer_create_full(self):
        """Test CustomerCreate with all fields."""
        customer = CustomerCreate(
            email="test@example.com",
            name="Test User",
            organization_id="org_123",
            user_id="user_123",
            metadata={"source": "web"},
        )
        assert customer.email == "test@example.com"
        assert customer.name == "Test User"
        assert customer.organization_id == "org_123"
        assert customer.user_id == "user_123"
        assert customer.metadata == {"source": "web"}

    def test_customer_model(self):
        """Test Customer model."""
        now = datetime.now(timezone.utc)
        customer = Customer(
            id="cus_123",
            email="test@example.com",
            name="Test User",
            stripe_customer_id="cus_stripe_123",
            organization_id="org_123",
            created_at=now,
            updated_at=now,
            metadata={},
        )
        assert customer.id == "cus_123"
        assert customer.stripe_customer_id == "cus_stripe_123"

    def test_customer_update(self):
        """Test CustomerUpdate model."""
        update = CustomerUpdate(
            name="Updated Name",
            metadata={"updated": "true"},
        )
        assert update.name == "Updated Name"
        assert update.email is None  # Optional field


class TestSubscriptionSchemas:
    """Tests for subscription-related schemas."""

    def test_subscription_create(self):
        """Test SubscriptionCreate model."""
        sub = SubscriptionCreate(
            customer_id="cus_123",
            plan_id="plan_123",
            price_id="price_123",
            trial_days=14,
        )
        assert sub.customer_id == "cus_123"
        assert sub.plan_id == "plan_123"
        assert sub.price_id == "price_123"
        assert sub.trial_days == 14

    def test_subscription_model(self):
        """Test Subscription model."""
        now = datetime.now(timezone.utc)
        sub = Subscription(
            id="sub_123",
            stripe_subscription_id="sub_stripe_123",
            customer_id="cus_123",
            plan_id="plan_123",
            plan_name="Pro Plan",
            status=SubscriptionStatus.ACTIVE,
            billing_period=BillingPeriod.MONTHLY,
            current_period_start=now,
            current_period_end=now,
            cancel_at_period_end=False,
            created_at=now,
            updated_at=now,
        )
        assert sub.status == SubscriptionStatus.ACTIVE
        assert sub.cancel_at_period_end is False

    def test_subscription_update(self):
        """Test SubscriptionUpdate model."""
        update = SubscriptionUpdate(
            price_id="price_new_123",
            cancel_at_period_end=True,
        )
        assert update.price_id == "price_new_123"
        assert update.cancel_at_period_end is True


class TestPlanSchemas:
    """Tests for plan-related schemas."""

    def test_plan_price(self):
        """Test PlanPrice model."""
        price = PlanPrice(
            id="price_123",
            amount=2900,
            currency="usd",
            interval=BillingPeriod.MONTHLY,
        )
        assert price.amount == 2900
        assert price.interval == BillingPeriod.MONTHLY

    def test_plan_limits(self):
        """Test PlanLimits model."""
        limits = PlanLimits(
            api_calls=10000,
            storage_gb=50,
            users=10,
            chat_sessions=1000,
        )
        assert limits.api_calls == 10000
        assert limits.storage_gb == 50

    def test_plan_model(self):
        """Test Plan model."""
        plan = Plan(
            id="plan_123",
            stripe_product_id="prod_123",
            name="Pro Plan",
            description="Professional plan",
            prices={"monthly": PlanPrice(
                id="price_monthly",
                amount=2900,
                currency="usd",
                interval=BillingPeriod.MONTHLY,
            )},
            limits=PlanLimits(
                api_calls=10000,
                storage_gb=50,
            ),
            features=["Feature 1", "Feature 2"],
            active=True,
        )
        assert plan.name == "Pro Plan"
        assert len(plan.prices) == 1
        assert len(plan.features) == 2


class TestCheckoutSchemas:
    """Tests for checkout-related schemas."""

    def test_checkout_session_create(self):
        """Test CheckoutSessionCreate model."""
        checkout = CheckoutSessionCreate(
            customer_id="cus_123",
            price_id="price_123",
            success_url="https://example.com/success",
            cancel_url="https://example.com/cancel",
        )
        assert checkout.customer_id == "cus_123"
        assert checkout.mode == "subscription"  # default

    def test_checkout_session_create_with_mode(self):
        """Test CheckoutSessionCreate with payment mode."""
        checkout = CheckoutSessionCreate(
            customer_id="cus_123",
            price_id="price_123",
            success_url="https://example.com/success",
            cancel_url="https://example.com/cancel",
            mode="payment",
        )
        assert checkout.mode == "payment"

    def test_checkout_session_model(self):
        """Test CheckoutSession model."""
        now = datetime.now(timezone.utc)
        session = CheckoutSession(
            id="cs_123",
            url="https://checkout.stripe.com/cs_123",
            customer_id="cus_123",
            subscription_id="sub_123",
            mode="subscription",
            status="complete",
            expires_at=now,
        )
        assert session.url.startswith("https://")
        assert session.status == "complete"


class TestInvoiceSchemas:
    """Tests for invoice-related schemas."""

    def test_invoice_model(self):
        """Test Invoice model."""
        now = datetime.now(timezone.utc)
        invoice = Invoice(
            id="in_123",
            customer_id="cus_123",
            subscription_id="sub_123",
            status=InvoiceStatus.PAID,
            amount_due=2900,
            amount_paid=2900,
            currency="usd",
            created_at=now,
        )
        assert invoice.status == InvoiceStatus.PAID
        assert invoice.amount_due == invoice.amount_paid


class TestUsageSchemas:
    """Tests for usage-related schemas."""

    def test_usage_record_create(self):
        """Test UsageRecordCreate model."""
        record = UsageRecordCreate(
            subscription_item_id="si_123",
            quantity=100,
        )
        assert record.quantity == 100
        assert record.action == "increment"  # default

    def test_usage_record_model(self):
        """Test UsageRecord model."""
        now = datetime.now(timezone.utc)
        record = UsageRecord(
            id="mbur_123",
            subscription_item_id="si_123",
            quantity=100,
            timestamp=now,
            action="increment",
        )
        assert record.quantity == 100


class TestWebhookSchemas:
    """Tests for webhook-related schemas."""

    def test_webhook_event(self):
        """Test WebhookEvent model."""
        now = datetime.now(timezone.utc)
        event = WebhookEvent(
            id="evt_123",
            type="customer.subscription.created",
            data={"id": "sub_123"},
            created_at=now,
        )
        assert event.type == "customer.subscription.created"
        assert event.data["id"] == "sub_123"


class TestResultModels:
    """Tests for operation result models."""

    def test_operation_result_ok(self):
        """Test OperationResult.ok factory."""
        result = OperationResult.ok(data={"key": "value"})
        assert result.success is True
        assert result.data == {"key": "value"}
        assert result.error_message is None

    def test_operation_result_error(self):
        """Test OperationResult.error factory."""
        result = OperationResult.error("Something went wrong", code="ERR_001")
        assert result.success is False
        assert result.error_message == "Something went wrong"
        assert result.error_code == "ERR_001"

    def test_customer_result_ok(self):
        """Test CustomerResult.ok factory."""
        result = CustomerResult.ok(
            customer_id="cus_123",
            stripe_customer_id="cus_stripe_123",
        )
        assert result.success is True
        assert result.customer_id == "cus_123"
        assert result.stripe_customer_id == "cus_stripe_123"

    def test_subscription_result_ok(self):
        """Test SubscriptionResult.ok factory."""
        result = SubscriptionResult.ok(
            subscription_id="sub_123",
            stripe_subscription_id="sub_stripe_123",
        )
        assert result.success is True
        assert result.subscription_id == "sub_123"

    def test_checkout_result_ok(self):
        """Test CheckoutResult.ok factory."""
        result = CheckoutResult.ok(
            session_id="cs_123",
            checkout_url="https://checkout.stripe.com/cs_123",
        )
        assert result.success is True
        assert result.checkout_url.startswith("https://")

    def test_portal_result_ok(self):
        """Test PortalResult.ok factory."""
        result = PortalResult.ok(
            session_id="bps_123",
            portal_url="https://billing.stripe.com/bps_123",
        )
        assert result.success is True
        assert result.portal_url.startswith("https://")

    def test_webhook_result_ok(self):
        """Test WebhookResult.ok factory."""
        result = WebhookResult.ok(
            event_id="evt_123",
            event_type="customer.subscription.created",
            actions=["Created subscription"],
        )
        assert result.success is True
        assert result.event_id == "evt_123"
        assert result.processed is True
        assert len(result.actions) == 1

    def test_webhook_result_skipped(self):
        """Test WebhookResult.skipped factory."""
        result = WebhookResult.skipped(
            event_id="evt_123",
            event_type="test.event",
            reason="Already processed",
        )
        assert result.success is True
        assert result.processed is False
        assert "Already processed" in result.actions[0]

    def test_webhook_result_error(self):
        """Test WebhookResult.error factory."""
        result = WebhookResult.error(
            "Signature verification failed",
            event_id="evt_123",
        )
        assert result.success is False
        assert result.error_message == "Signature verification failed"
