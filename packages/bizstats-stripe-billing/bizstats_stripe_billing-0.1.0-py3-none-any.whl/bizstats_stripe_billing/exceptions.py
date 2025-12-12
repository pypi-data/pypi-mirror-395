"""
Custom exceptions for Stripe billing.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

from typing import Optional, Any
import stripe


class StripeBillingError(Exception):
    """Base exception for all Stripe billing errors."""

    def __init__(
        self,
        message: str,
        code: Optional[str] = None,
        stripe_error: Optional[stripe.StripeError] = None,
    ):
        self.message = message
        self.code = code
        self.stripe_error = stripe_error
        super().__init__(message)

    @property
    def http_status(self) -> Optional[int]:
        """Get HTTP status code from Stripe error."""
        if self.stripe_error:
            return getattr(self.stripe_error, "http_status", None)
        return None

    def to_dict(self) -> dict:
        """Convert exception to dictionary for API responses."""
        return {
            "error": self.__class__.__name__,
            "message": self.message,
            "code": self.code,
            "http_status": self.http_status,
        }


class StripeAPIError(StripeBillingError):
    """Error communicating with Stripe API."""

    pass


class StripeAuthenticationError(StripeBillingError):
    """Invalid or missing Stripe API key."""

    pass


class StripeRateLimitError(StripeBillingError):
    """Stripe rate limit exceeded."""

    def __init__(
        self,
        message: str,
        stripe_error: Optional[stripe.StripeError] = None,
        retry_after: Optional[int] = None,
    ):
        super().__init__(message, "rate_limit_exceeded", stripe_error)
        self.retry_after = retry_after


class StripeValidationError(StripeBillingError):
    """Invalid request parameters."""

    def __init__(
        self,
        message: str,
        stripe_error: Optional[stripe.StripeError] = None,
        param: Optional[str] = None,
        code: Optional[str] = None,
    ):
        super().__init__(message, code, stripe_error)
        self.param = param

    def to_dict(self) -> dict:
        """Convert exception to dictionary for API responses."""
        result = super().to_dict()
        if self.param:
            result["param"] = self.param
        return result


class CustomerNotFoundError(StripeBillingError):
    """Customer not found."""

    def __init__(self, customer_id: str):
        super().__init__(
            f"Customer not found: {customer_id}",
            code="customer_not_found",
        )
        self.customer_id = customer_id


class SubscriptionNotFoundError(StripeBillingError):
    """Subscription not found."""

    def __init__(self, subscription_id: str):
        super().__init__(
            f"Subscription not found: {subscription_id}",
            code="subscription_not_found",
        )
        self.subscription_id = subscription_id


class PlanNotFoundError(StripeBillingError):
    """Plan/Product not found."""

    def __init__(self, plan_id: str):
        super().__init__(
            f"Plan not found: {plan_id}",
            code="plan_not_found",
        )
        self.plan_id = plan_id


class PriceNotFoundError(StripeBillingError):
    """Price not found."""

    def __init__(self, price_id: str):
        super().__init__(
            f"Price not found: {price_id}",
            code="price_not_found",
        )
        self.price_id = price_id


class WebhookSignatureError(StripeBillingError):
    """Invalid webhook signature."""

    def __init__(self, message: str = "Invalid webhook signature"):
        super().__init__(message, code="webhook_signature_invalid")


class WebhookEventAlreadyProcessedError(StripeBillingError):
    """Webhook event was already processed."""

    def __init__(self, event_id: str):
        super().__init__(
            f"Event already processed: {event_id}",
            code="event_already_processed",
        )
        self.event_id = event_id


class PaymentFailedError(StripeBillingError):
    """Payment failed."""

    def __init__(
        self,
        message: str,
        decline_code: Optional[str] = None,
        stripe_error: Optional[stripe.StripeError] = None,
    ):
        super().__init__(message, "payment_failed", stripe_error)
        self.decline_code = decline_code

    def to_dict(self) -> dict:
        """Convert exception to dictionary for API responses."""
        result = super().to_dict()
        if self.decline_code:
            result["decline_code"] = self.decline_code
        return result


class SubscriptionAlreadyExistsError(StripeBillingError):
    """Customer already has an active subscription."""

    def __init__(self, customer_id: str, subscription_id: str):
        super().__init__(
            f"Customer {customer_id} already has active subscription {subscription_id}",
            code="subscription_already_exists",
        )
        self.customer_id = customer_id
        self.subscription_id = subscription_id


class InsufficientPermissionsError(StripeBillingError):
    """User doesn't have permission for this billing operation."""

    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message, code="insufficient_permissions")


class UsageLimitExceededError(StripeBillingError):
    """Usage limit exceeded for the current plan."""

    def __init__(
        self,
        metric: str,
        current_usage: int,
        limit: int,
    ):
        super().__init__(
            f"Usage limit exceeded for {metric}: {current_usage}/{limit}",
            code="usage_limit_exceeded",
        )
        self.metric = metric
        self.current_usage = current_usage
        self.limit = limit

    def to_dict(self) -> dict:
        """Convert exception to dictionary for API responses."""
        result = super().to_dict()
        result.update({
            "metric": self.metric,
            "current_usage": self.current_usage,
            "limit": self.limit,
        })
        return result
