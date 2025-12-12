"""
BizStats Stripe Billing - Comprehensive Stripe billing integration.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.

Features:
- Customer management
- Subscription management
- Checkout sessions
- Billing portal
- Webhook handling
- Usage-based billing
- Invoice management

Example:
    ```python
    from bizstats_stripe_billing import BillingService, CustomerCreate

    billing = BillingService()

    # Create a customer
    result = billing.create_customer(
        CustomerCreate(email="user@example.com")
    )

    # Create checkout session
    checkout = billing.create_checkout_session(
        CheckoutSessionCreate(
            customer_id=result.stripe_customer_id,
            price_id="price_xxx",
            success_url="https://example.com/success",
            cancel_url="https://example.com/cancel",
        )
    )
    print(f"Checkout URL: {checkout.checkout_url}")
    ```
"""

__version__ = "0.1.0"
__author__ = "Absolut-e Data Com Inc."
__email__ = "account@absolut-e.com"

# Configuration
from .config import (
    StripeConfig,
    get_config,
    configure,
    get_test_card,
    TEST_CARDS,
)

# Client
from .client import (
    StripeClient,
    get_client,
)

# Main Service
from .billing import (
    BillingService,
    create_billing_service,
)

# Models
from .models import (
    # Enums
    SubscriptionStatus,
    BillingPeriod,
    SubscriptionPlan,
    UsageMetric,
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

# Exceptions
from .exceptions import (
    StripeBillingError,
    StripeAPIError,
    StripeAuthenticationError,
    StripeRateLimitError,
    StripeValidationError,
    CustomerNotFoundError,
    SubscriptionNotFoundError,
    PlanNotFoundError,
    PriceNotFoundError,
    WebhookSignatureError,
    WebhookEventAlreadyProcessedError,
    PaymentFailedError,
    SubscriptionAlreadyExistsError,
    InsufficientPermissionsError,
    UsageLimitExceededError,
)

# Webhooks
from .webhooks import (
    WebhookHandler,
    WebhookEventHandler,
)

__all__ = [
    # Version
    "__version__",
    # Configuration
    "StripeConfig",
    "get_config",
    "configure",
    "get_test_card",
    "TEST_CARDS",
    # Client
    "StripeClient",
    "get_client",
    # Service
    "BillingService",
    "create_billing_service",
    # Enums
    "SubscriptionStatus",
    "BillingPeriod",
    "SubscriptionPlan",
    "UsageMetric",
    "PaymentStatus",
    "InvoiceStatus",
    "WebhookEventType",
    # Models
    "Customer",
    "CustomerCreate",
    "CustomerUpdate",
    "Subscription",
    "SubscriptionCreate",
    "SubscriptionUpdate",
    "Plan",
    "PlanPrice",
    "PlanLimits",
    "Invoice",
    "PaymentMethod",
    "CheckoutSession",
    "CheckoutSessionCreate",
    "UsageRecord",
    "UsageRecordCreate",
    "WebhookEvent",
    "BillingPortalSession",
    # Results
    "OperationResult",
    "CustomerResult",
    "SubscriptionResult",
    "CheckoutResult",
    "PortalResult",
    "WebhookResult",
    # Exceptions
    "StripeBillingError",
    "StripeAPIError",
    "StripeAuthenticationError",
    "StripeRateLimitError",
    "StripeValidationError",
    "CustomerNotFoundError",
    "SubscriptionNotFoundError",
    "PlanNotFoundError",
    "PriceNotFoundError",
    "WebhookSignatureError",
    "WebhookEventAlreadyProcessedError",
    "PaymentFailedError",
    "SubscriptionAlreadyExistsError",
    "InsufficientPermissionsError",
    "UsageLimitExceededError",
    # Webhooks
    "WebhookHandler",
    "WebhookEventHandler",
]
