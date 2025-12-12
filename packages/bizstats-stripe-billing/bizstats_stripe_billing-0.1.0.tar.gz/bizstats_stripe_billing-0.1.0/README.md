# @bizstats/stripe-billing

Comprehensive Stripe billing integration for BizStats applications.

## Features

- Customer management (create, update, delete)
- Subscription lifecycle (create, cancel, resume, update)
- Checkout sessions for payment flow
- Billing portal integration
- Webhook handling with signature verification
- Usage-based/metered billing
- Invoice management
- Payment method management

## Installation

```bash
pip install bizstats-stripe-billing
```

## Quick Start

```python
from bizstats_stripe_billing import (
    BillingService,
    CustomerCreate,
    CheckoutSessionCreate,
)

# Initialize the service
billing = BillingService()

# Create a customer
result = billing.create_customer(
    CustomerCreate(
        email="user@example.com",
        name="John Doe",
    )
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

## Configuration

Set environment variables:

```bash
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_PUBLISHABLE_KEY=pk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
```

Or configure programmatically:

```python
from bizstats_stripe_billing import StripeConfig, configure

config = StripeConfig(
    secret_key="sk_test_xxx",
    webhook_secret="whsec_xxx",
)
configure(config)
```

## Webhook Handling

```python
from bizstats_stripe_billing import (
    WebhookHandler,
    WebhookEventType,
    WebhookResult,
)

handler = WebhookHandler()

@handler.on(WebhookEventType.SUBSCRIPTION_CREATED)
async def handle_subscription(data, event):
    # Process subscription created event
    return WebhookResult.ok(event.id, event.type)

# Process incoming webhook
result = await handler.process(payload, signature)
```

## License

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
