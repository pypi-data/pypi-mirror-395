"""
Test fixtures for stripe-billing tests.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

import pytest
from datetime import datetime, timezone
from unittest.mock import Mock, AsyncMock, MagicMock, patch
import stripe

from bizstats_stripe_billing import (
    StripeConfig,
    StripeClient,
    BillingService,
    WebhookHandler,
    Customer,
    CustomerCreate,
    Subscription,
    SubscriptionCreate,
    Plan,
    PlanPrice,
    PlanLimits,
    CheckoutSession,
    Invoice,
    SubscriptionStatus,
    BillingPeriod,
    SubscriptionPlan,
    WebhookEventType,
)


@pytest.fixture
def test_config():
    """Create test Stripe configuration."""
    return StripeConfig(
        secret_key="sk_test_123456789",
        webhook_secret="whsec_test_secret_123",
        publishable_key="pk_test_123456789",
        max_retries=3,
        retry_delay=0.1,
        webhook_tolerance=300,
    )


@pytest.fixture
def mock_stripe_customer():
    """Create mock Stripe customer object."""
    customer = Mock(spec=stripe.Customer)
    customer.id = "cus_test123"
    customer.email = "test@example.com"
    customer.name = "Test User"
    customer.metadata = {"org_id": "org_123"}
    customer.created = int(datetime.now(timezone.utc).timestamp())
    customer.default_source = None
    customer.invoice_settings = Mock()
    customer.invoice_settings.default_payment_method = "pm_test123"
    return customer


@pytest.fixture
def mock_stripe_subscription():
    """Create mock Stripe subscription object."""
    subscription = Mock(spec=stripe.Subscription)
    subscription.id = "sub_test123"
    subscription.customer = "cus_test123"
    subscription.status = "active"
    subscription.current_period_start = int(datetime.now(timezone.utc).timestamp())
    subscription.current_period_end = int(datetime.now(timezone.utc).timestamp()) + 2592000
    subscription.cancel_at_period_end = False
    subscription.canceled_at = None
    subscription.trial_start = None
    subscription.trial_end = None
    subscription.metadata = {}

    # Mock items
    item = Mock()
    item.id = "si_test123"
    item.price = Mock()
    item.price.id = "price_test123"
    item.price.product = "prod_test123"
    item.price.unit_amount = 2900
    item.price.currency = "usd"
    item.price.nickname = "Pro Plan Monthly"  # Required for plan_name
    item.price.recurring = Mock()
    item.price.recurring.interval = "month"
    item.quantity = 1

    items_list = Mock()
    items_list.data = [item]
    subscription.items = items_list

    return subscription


@pytest.fixture
def mock_stripe_checkout_session():
    """Create mock Stripe checkout session."""
    session = Mock(spec=stripe.checkout.Session)
    session.id = "cs_test123"
    session.url = "https://checkout.stripe.com/pay/cs_test123"
    session.customer = "cus_test123"
    session.subscription = "sub_test123"
    session.payment_intent = "pi_test123"
    session.mode = "subscription"
    session.status = "complete"
    session.success_url = "https://example.com/success"
    session.cancel_url = "https://example.com/cancel"
    session.metadata = {}
    return session


@pytest.fixture
def mock_stripe_invoice():
    """Create mock Stripe invoice."""
    invoice = Mock(spec=stripe.Invoice)
    invoice.id = "in_test123"
    invoice.customer = "cus_test123"
    invoice.subscription = "sub_test123"
    invoice.status = "paid"
    invoice.amount_due = 2900
    invoice.amount_paid = 2900
    invoice.currency = "usd"
    invoice.created = int(datetime.now(timezone.utc).timestamp())
    invoice.due_date = int(datetime.now(timezone.utc).timestamp()) + 604800
    invoice.paid_at = int(datetime.now(timezone.utc).timestamp())
    invoice.hosted_invoice_url = "https://invoice.stripe.com/i/in_test123"
    invoice.invoice_pdf = "https://invoice.stripe.com/i/in_test123/pdf"
    invoice.number = "INV-0001"

    # Mock lines
    line = Mock()
    line.description = "Pro Plan - Monthly"
    line.amount = 2900
    invoice.lines = Mock()
    invoice.lines.data = [line]

    return invoice


@pytest.fixture
def mock_stripe_portal_session():
    """Create mock Stripe billing portal session."""
    session = Mock()
    session.id = "bps_test123"
    session.url = "https://billing.stripe.com/session/bps_test123"
    session.customer = "cus_test123"
    session.return_url = "https://example.com/account"
    session.created = int(datetime.now(timezone.utc).timestamp())
    return session


@pytest.fixture
def mock_stripe_product():
    """Create mock Stripe product."""
    product = Mock(spec=stripe.Product)
    product.id = "prod_test123"
    product.name = "Pro Plan"
    product.description = "Professional plan with advanced features"
    product.active = True
    product.metadata = {
        "plan_type": "pro",
        "max_chatbots": "10",
        "max_messages": "50000",
    }
    return product


@pytest.fixture
def mock_stripe_price():
    """Create mock Stripe price."""
    price = Mock(spec=stripe.Price)
    price.id = "price_test123"
    price.product = "prod_test123"
    price.unit_amount = 2900
    price.currency = "usd"
    price.active = True
    price.type = "recurring"
    price.recurring = Mock()
    price.recurring.interval = "month"
    price.recurring.interval_count = 1
    price.metadata = {}
    return price


@pytest.fixture
def mock_stripe_event():
    """Create mock Stripe webhook event."""
    event = Mock(spec=stripe.Event)
    event.id = "evt_test123"
    event.type = "customer.subscription.created"
    event.created = int(datetime.now(timezone.utc).timestamp())
    event.livemode = False
    event.api_version = "2024-11-20"

    # Event data
    event.data = Mock()
    event.data.object = {
        "id": "sub_test123",
        "customer": "cus_test123",
        "status": "active",
        "items": {"data": [{"price": {"product": "prod_test123"}}]},
    }
    event.data.previous_attributes = {}

    # Make get() work on event.data
    event.data.get = lambda key, default=None: getattr(event.data, key, default) if hasattr(event.data, key) else default

    return event


@pytest.fixture
def sample_customer_create():
    """Create sample customer creation request."""
    return CustomerCreate(
        email="test@example.com",
        name="Test User",
        organization_id="org_123",
        metadata={"source": "web"},
    )


@pytest.fixture
def sample_subscription_create():
    """Create sample subscription creation request."""
    return SubscriptionCreate(
        customer_id="cus_test123",
        plan_id="plan_test123",
        price_id="price_test123",
        trial_days=14,
        metadata={"org_id": "org_123"},
    )


@pytest.fixture
def sample_plan():
    """Create sample plan."""
    return Plan(
        id="prod_test123",
        name="Pro Plan",
        description="Professional plan with advanced features",
        plan_type=SubscriptionPlan.PRO,
        prices=[
            PlanPrice(
                id="price_monthly",
                amount=2900,
                currency="usd",
                interval=BillingPeriod.MONTHLY,
            ),
            PlanPrice(
                id="price_yearly",
                amount=29000,
                currency="usd",
                interval=BillingPeriod.YEARLY,
            ),
        ],
        limits=PlanLimits(
            max_chatbots=10,
            max_messages_per_month=50000,
            max_documents=1000,
            max_storage_mb=10240,
        ),
        features=["Advanced analytics", "Priority support", "Custom branding"],
        is_active=True,
    )


@pytest.fixture
def stripe_client(test_config):
    """Create Stripe client with test config."""
    with patch("stripe.api_key"):
        with patch("stripe.api_version"):
            client = StripeClient(test_config)
            return client


@pytest.fixture
def billing_service(test_config):
    """Create billing service with test config."""
    with patch("stripe.api_key"):
        with patch("stripe.api_version"):
            service = BillingService(test_config)
            return service


@pytest.fixture
def webhook_handler(test_config):
    """Create webhook handler with test config."""
    with patch("stripe.api_key"):
        with patch("stripe.api_version"):
            return WebhookHandler(test_config)
