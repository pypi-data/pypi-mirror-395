"""
Billing enumerations.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

from enum import Enum


class SubscriptionStatus(str, Enum):
    """Subscription status enumeration (mirrors Stripe statuses)."""

    INCOMPLETE = "incomplete"
    INCOMPLETE_EXPIRED = "incomplete_expired"
    TRIALING = "trialing"
    ACTIVE = "active"
    PAST_DUE = "past_due"
    CANCELED = "canceled"
    UNPAID = "unpaid"
    PAUSED = "paused"

    @classmethod
    def is_active_status(cls, status: "SubscriptionStatus") -> bool:
        """Check if status represents an active subscription."""
        return status in (cls.ACTIVE, cls.TRIALING)

    @classmethod
    def is_problem_status(cls, status: "SubscriptionStatus") -> bool:
        """Check if status indicates a billing problem."""
        return status in (cls.PAST_DUE, cls.UNPAID, cls.INCOMPLETE)


class BillingPeriod(str, Enum):
    """Billing period enumeration."""

    DAILY = "day"
    WEEKLY = "week"
    MONTHLY = "month"
    YEARLY = "year"

    @property
    def display_name(self) -> str:
        """Get display name for the billing period."""
        return {
            self.DAILY: "Daily",
            self.WEEKLY: "Weekly",
            self.MONTHLY: "Monthly",
            self.YEARLY: "Yearly",
        }.get(self, self.value.capitalize())


class SubscriptionPlan(str, Enum):
    """Subscription plan tiers."""

    FREE = "free"
    STARTER = "starter"
    PROFESSIONAL = "professional"
    BUSINESS = "business"
    ENTERPRISE = "enterprise"

    # Alternative naming convention
    COMPLIMENTARY = "complimentary"
    FOUNDATION = "foundation"
    PRESTIGE = "prestige"
    SIGNATURE = "signature"


class UsageMetric(str, Enum):
    """Usage metric types for metered billing."""

    API_CALLS = "api_calls"
    STORAGE_GB = "storage_gb"
    COMPUTE_HOURS = "compute_hours"
    TOKENS = "tokens"
    MESSAGES = "messages"
    CHAT_SESSIONS = "chat_sessions"
    KB_TOKENS = "kb_tokens"
    USERS = "users"
    INTEGRATIONS = "integrations"
    WEBSITES = "websites"


class PaymentStatus(str, Enum):
    """Payment status enumeration."""

    PENDING = "pending"
    PROCESSING = "processing"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELED = "canceled"
    REFUNDED = "refunded"
    DISPUTED = "disputed"


class InvoiceStatus(str, Enum):
    """Invoice status enumeration."""

    DRAFT = "draft"
    OPEN = "open"
    PAID = "paid"
    VOID = "void"
    UNCOLLECTIBLE = "uncollectible"


class WebhookEventType(str, Enum):
    """Stripe webhook event types we handle."""

    # Checkout
    CHECKOUT_SESSION_COMPLETED = "checkout.session.completed"
    CHECKOUT_SESSION_EXPIRED = "checkout.session.expired"
    CHECKOUT_SESSION_ASYNC_PAYMENT_SUCCEEDED = "checkout.session.async_payment_succeeded"
    CHECKOUT_SESSION_ASYNC_PAYMENT_FAILED = "checkout.session.async_payment_failed"

    # Customer
    CUSTOMER_CREATED = "customer.created"
    CUSTOMER_UPDATED = "customer.updated"
    CUSTOMER_DELETED = "customer.deleted"

    # Subscription
    SUBSCRIPTION_CREATED = "customer.subscription.created"
    SUBSCRIPTION_UPDATED = "customer.subscription.updated"
    SUBSCRIPTION_DELETED = "customer.subscription.deleted"
    SUBSCRIPTION_PAUSED = "customer.subscription.paused"
    SUBSCRIPTION_RESUMED = "customer.subscription.resumed"
    SUBSCRIPTION_TRIAL_WILL_END = "customer.subscription.trial_will_end"

    # Invoice
    INVOICE_CREATED = "invoice.created"
    INVOICE_FINALIZED = "invoice.finalized"
    INVOICE_PAID = "invoice.paid"
    INVOICE_PAYMENT_SUCCEEDED = "invoice.payment_succeeded"
    INVOICE_PAYMENT_FAILED = "invoice.payment_failed"
    INVOICE_PAYMENT_ACTION_REQUIRED = "invoice.payment_action_required"
    INVOICE_UPCOMING = "invoice.upcoming"
    INVOICE_OVERDUE = "invoice.overdue"
    INVOICE_MARKED_UNCOLLECTIBLE = "invoice.marked_uncollectible"

    # Payment Method
    PAYMENT_METHOD_ATTACHED = "payment_method.attached"
    PAYMENT_METHOD_DETACHED = "payment_method.detached"
    PAYMENT_METHOD_UPDATED = "payment_method.updated"

    # Charge
    CHARGE_SUCCEEDED = "charge.succeeded"
    CHARGE_FAILED = "charge.failed"
    CHARGE_REFUNDED = "charge.refunded"
    CHARGE_DISPUTE_CREATED = "charge.dispute.created"

    # Product/Price
    PRODUCT_CREATED = "product.created"
    PRODUCT_UPDATED = "product.updated"
    PRICE_CREATED = "price.created"
    PRICE_UPDATED = "price.updated"

    @classmethod
    def from_string(cls, event_type: str) -> "WebhookEventType":
        """Get enum from string, returns None if not found."""
        for member in cls:
            if member.value == event_type:
                return member
        raise ValueError(f"Unknown webhook event type: {event_type}")
