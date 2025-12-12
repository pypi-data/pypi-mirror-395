"""
Pydantic schemas for billing models.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict

from .enums import (
    SubscriptionStatus,
    BillingPeriod,
    PaymentStatus,
    InvoiceStatus,
)


# Customer Models


class CustomerCreate(BaseModel):
    """Schema for creating a new customer."""

    email: str
    name: Optional[str] = None
    phone: Optional[str] = None
    metadata: Dict[str, str] = Field(default_factory=dict)
    # Reference IDs for your application
    organization_id: Optional[str] = None
    user_id: Optional[str] = None


class CustomerUpdate(BaseModel):
    """Schema for updating a customer."""

    email: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None


class Customer(BaseModel):
    """Customer model."""

    model_config = ConfigDict(from_attributes=True)

    id: str  # Your internal ID
    stripe_customer_id: str
    email: str
    name: Optional[str] = None
    phone: Optional[str] = None
    default_currency: str = "usd"
    metadata: Dict[str, Any] = Field(default_factory=dict)
    organization_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime


# Plan Models


class PlanPrice(BaseModel):
    """Price information for a plan."""

    id: str  # Stripe price ID
    amount: int  # Amount in cents
    currency: str = "usd"
    interval: BillingPeriod = BillingPeriod.MONTHLY
    interval_count: int = 1


class PlanLimits(BaseModel):
    """Usage limits for a plan."""

    api_calls: Optional[int] = None
    storage_gb: Optional[int] = None
    users: Optional[int] = None
    chat_sessions: Optional[int] = None
    kb_tokens: Optional[int] = None
    tokens_per_session: Optional[int] = None
    integrations: Optional[int] = None
    websites: Optional[int] = None


class Plan(BaseModel):
    """Plan/Product model."""

    model_config = ConfigDict(from_attributes=True)

    id: str  # Your internal plan ID (e.g., "professional")
    stripe_product_id: str
    name: str
    description: Optional[str] = None
    active: bool = True
    # Pricing
    prices: Dict[str, PlanPrice] = Field(default_factory=dict)  # monthly, yearly
    monthly_price: int = 0  # In cents
    yearly_price: int = 0  # In cents
    # Features and limits
    features: List[str] = Field(default_factory=list)
    limits: Optional[PlanLimits] = None
    # Display
    is_popular: bool = False
    is_recommended: bool = False
    badge: Optional[str] = None
    color: Optional[str] = None
    cta: str = "Get Started"
    # Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# Subscription Models


class SubscriptionCreate(BaseModel):
    """Schema for creating a subscription."""

    customer_id: str
    plan_id: str
    price_id: Optional[str] = None  # If not provided, uses default monthly
    billing_period: BillingPeriod = BillingPeriod.MONTHLY
    trial_days: Optional[int] = None
    payment_method_id: Optional[str] = None
    metadata: Dict[str, str] = Field(default_factory=dict)
    # Proration behavior
    proration_behavior: str = "create_prorations"


class SubscriptionUpdate(BaseModel):
    """Schema for updating a subscription."""

    plan_id: Optional[str] = None
    price_id: Optional[str] = None
    billing_period: Optional[BillingPeriod] = None
    cancel_at_period_end: Optional[bool] = None
    metadata: Optional[Dict[str, str]] = None
    proration_behavior: str = "create_prorations"


class Subscription(BaseModel):
    """Subscription model."""

    model_config = ConfigDict(from_attributes=True)

    id: str  # Your internal ID
    stripe_subscription_id: str
    customer_id: str
    plan_id: str
    plan_name: str
    status: SubscriptionStatus
    billing_period: BillingPeriod
    # Pricing
    amount: int = 0  # In cents
    currency: str = "usd"
    # Period
    current_period_start: Optional[datetime] = None
    current_period_end: Optional[datetime] = None
    # Trial
    trial_start: Optional[datetime] = None
    trial_end: Optional[datetime] = None
    # Cancellation
    cancel_at_period_end: bool = False
    canceled_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    # Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime

    @property
    def is_active(self) -> bool:
        """Check if subscription is active."""
        return SubscriptionStatus.is_active_status(self.status)

    @property
    def has_billing_problem(self) -> bool:
        """Check if subscription has billing issues."""
        return SubscriptionStatus.is_problem_status(self.status)


# Checkout Models


class CheckoutSessionCreate(BaseModel):
    """Schema for creating a checkout session."""

    customer_id: Optional[str] = None  # Stripe customer ID
    customer_email: Optional[str] = None  # If no existing customer
    price_id: str
    success_url: str
    cancel_url: str
    mode: str = "subscription"  # subscription, payment, setup
    trial_days: Optional[int] = None
    metadata: Dict[str, str] = Field(default_factory=dict)
    # Allow promotion codes
    allow_promotion_codes: bool = False
    # Collect billing address
    billing_address_collection: str = "auto"  # auto, required
    # Tax settings
    automatic_tax: bool = False


class CheckoutSession(BaseModel):
    """Checkout session model."""

    id: str  # Stripe checkout session ID
    url: str
    status: str  # open, complete, expired
    mode: str
    customer_id: Optional[str] = None
    subscription_id: Optional[str] = None
    payment_intent_id: Optional[str] = None
    amount_total: Optional[int] = None
    currency: Optional[str] = None
    expires_at: datetime
    metadata: Dict[str, Any] = Field(default_factory=dict)


# Invoice Models


class Invoice(BaseModel):
    """Invoice model."""

    model_config = ConfigDict(from_attributes=True)

    id: str  # Stripe invoice ID
    customer_id: str
    subscription_id: Optional[str] = None
    status: InvoiceStatus
    # Amounts in cents
    amount_due: int = 0
    amount_paid: int = 0
    amount_remaining: int = 0
    subtotal: int = 0
    tax: int = 0
    total: int = 0
    currency: str = "usd"
    # URLs
    hosted_invoice_url: Optional[str] = None
    invoice_pdf: Optional[str] = None
    # Dates
    due_date: Optional[datetime] = None
    paid_at: Optional[datetime] = None
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None
    created_at: datetime


# Payment Method Models


class PaymentMethod(BaseModel):
    """Payment method model."""

    id: str  # Stripe payment method ID
    type: str  # card, bank_account, etc.
    # Card details (if type is card)
    card_brand: Optional[str] = None  # visa, mastercard, etc.
    card_last4: Optional[str] = None
    card_exp_month: Optional[int] = None
    card_exp_year: Optional[int] = None
    # Status
    is_default: bool = False
    created_at: datetime


# Usage Models


class UsageRecordCreate(BaseModel):
    """Schema for creating a usage record."""

    subscription_item_id: str
    quantity: int
    timestamp: Optional[datetime] = None
    action: str = "increment"  # increment, set


class UsageRecord(BaseModel):
    """Usage record model."""

    id: str
    subscription_item_id: str
    quantity: int
    timestamp: datetime
    action: str


# Webhook Models


class WebhookEvent(BaseModel):
    """Webhook event model."""

    id: str  # Stripe event ID
    type: str  # Event type (e.g., customer.subscription.created)
    api_version: Optional[str] = None
    data: Dict[str, Any]  # Event data object
    created_at: datetime
    # Processing status
    processed: bool = False
    processed_at: Optional[datetime] = None
    error: Optional[str] = None


# Billing Portal Models


class BillingPortalSession(BaseModel):
    """Billing portal session model."""

    id: str  # Stripe portal session ID
    url: str
    return_url: str
    customer_id: str
    created_at: datetime
