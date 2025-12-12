"""
Stripe API client wrapper with retry logic and error handling.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

import stripe
from typing import Optional, Dict, Any, TypeVar, Callable, Awaitable
from functools import wraps
import asyncio
import logging

from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

from .config import get_config, StripeConfig
from .exceptions import (
    StripeBillingError,
    StripeAPIError,
    StripeAuthenticationError,
    StripeRateLimitError,
    StripeValidationError,
)

logger = logging.getLogger(__name__)

T = TypeVar("T")


def _is_retryable_error(exception: Exception) -> bool:
    """Check if an exception is retryable."""
    if isinstance(exception, stripe.RateLimitError):
        return True
    if isinstance(exception, stripe.APIConnectionError):
        return True
    if isinstance(exception, stripe.APIError):
        # Retry on 5xx errors
        return exception.http_status and exception.http_status >= 500
    return False


def with_retry(func: Callable[..., T]) -> Callable[..., T]:
    """Decorator to add retry logic to Stripe API calls."""
    config = get_config()

    @retry(
        stop=stop_after_attempt(config.max_retries),
        wait=wait_exponential(multiplier=config.retry_delay, min=1, max=10),
        retry=retry_if_exception_type(
            (stripe.RateLimitError, stripe.APIConnectionError)
        ),
        reraise=True,
    )
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


class StripeClient:
    """
    Stripe API client wrapper.

    Provides a clean interface for Stripe API operations with:
    - Automatic retry on transient failures
    - Consistent error handling
    - Request logging
    - API version management
    """

    def __init__(self, config: Optional[StripeConfig] = None):
        """
        Initialize Stripe client.

        Args:
            config: Optional Stripe configuration. Uses global config if not provided.
        """
        self.config = config or get_config()
        self._configure_stripe()

    def _configure_stripe(self) -> None:
        """Configure Stripe SDK."""
        stripe.api_key = self.config.secret_key
        stripe.api_version = self.config.api_version

        # Configure logging level based on test mode
        if self.config.test_mode:
            stripe.log = "debug"

    def _handle_stripe_error(self, error: stripe.StripeError) -> None:
        """Convert Stripe errors to our exception types."""
        if isinstance(error, stripe.AuthenticationError):
            raise StripeAuthenticationError(
                message="Invalid Stripe API key",
                stripe_error=error,
            )
        elif isinstance(error, stripe.RateLimitError):
            raise StripeRateLimitError(
                message="Stripe rate limit exceeded",
                stripe_error=error,
                retry_after=getattr(error, "retry_after", None),
            )
        elif isinstance(error, stripe.InvalidRequestError):
            raise StripeValidationError(
                message=str(error.user_message or error),
                stripe_error=error,
                param=error.param,
            )
        elif isinstance(error, stripe.CardError):
            raise StripeValidationError(
                message=str(error.user_message or error),
                stripe_error=error,
                code=error.code,
            )
        else:
            raise StripeAPIError(
                message=str(error),
                stripe_error=error,
            )

    # Customer Operations

    @with_retry
    def create_customer(
        self,
        email: str,
        name: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> stripe.Customer:
        """Create a new Stripe customer."""
        try:
            params = {
                "email": email,
                "metadata": metadata or {},
            }
            if name:
                params["name"] = name
            params.update(kwargs)

            customer = stripe.Customer.create(**params)
            logger.info(f"Created Stripe customer: {customer.id}")
            return customer
        except stripe.StripeError as e:
            logger.error(f"Error creating customer: {e}")
            self._handle_stripe_error(e)

    @with_retry
    def get_customer(self, customer_id: str) -> stripe.Customer:
        """Retrieve a Stripe customer."""
        try:
            return stripe.Customer.retrieve(customer_id)
        except stripe.StripeError as e:
            logger.error(f"Error retrieving customer {customer_id}: {e}")
            self._handle_stripe_error(e)

    @with_retry
    def update_customer(
        self, customer_id: str, **kwargs
    ) -> stripe.Customer:
        """Update a Stripe customer."""
        try:
            customer = stripe.Customer.modify(customer_id, **kwargs)
            logger.info(f"Updated Stripe customer: {customer_id}")
            return customer
        except stripe.StripeError as e:
            logger.error(f"Error updating customer {customer_id}: {e}")
            self._handle_stripe_error(e)

    @with_retry
    def delete_customer(self, customer_id: str) -> bool:
        """Delete a Stripe customer."""
        try:
            stripe.Customer.delete(customer_id)
            logger.info(f"Deleted Stripe customer: {customer_id}")
            return True
        except stripe.StripeError as e:
            logger.error(f"Error deleting customer {customer_id}: {e}")
            self._handle_stripe_error(e)

    # Subscription Operations

    @with_retry
    def create_subscription(
        self,
        customer_id: str,
        price_id: str,
        trial_days: Optional[int] = None,
        metadata: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> stripe.Subscription:
        """Create a new subscription."""
        try:
            params = {
                "customer": customer_id,
                "items": [{"price": price_id}],
                "metadata": metadata or {},
                "expand": ["latest_invoice.payment_intent"],
            }
            if trial_days:
                params["trial_period_days"] = trial_days
            params.update(kwargs)

            subscription = stripe.Subscription.create(**params)
            logger.info(f"Created subscription: {subscription.id}")
            return subscription
        except stripe.StripeError as e:
            logger.error(f"Error creating subscription: {e}")
            self._handle_stripe_error(e)

    @with_retry
    def get_subscription(self, subscription_id: str) -> stripe.Subscription:
        """Retrieve a subscription."""
        try:
            return stripe.Subscription.retrieve(
                subscription_id,
                expand=["latest_invoice", "default_payment_method"],
            )
        except stripe.StripeError as e:
            logger.error(f"Error retrieving subscription {subscription_id}: {e}")
            self._handle_stripe_error(e)

    @with_retry
    def update_subscription(
        self, subscription_id: str, **kwargs
    ) -> stripe.Subscription:
        """Update a subscription."""
        try:
            subscription = stripe.Subscription.modify(subscription_id, **kwargs)
            logger.info(f"Updated subscription: {subscription_id}")
            return subscription
        except stripe.StripeError as e:
            logger.error(f"Error updating subscription {subscription_id}: {e}")
            self._handle_stripe_error(e)

    @with_retry
    def cancel_subscription(
        self,
        subscription_id: str,
        at_period_end: bool = True,
    ) -> stripe.Subscription:
        """Cancel a subscription."""
        try:
            if at_period_end:
                subscription = stripe.Subscription.modify(
                    subscription_id,
                    cancel_at_period_end=True,
                )
            else:
                subscription = stripe.Subscription.cancel(subscription_id)
            logger.info(
                f"Cancelled subscription: {subscription_id} "
                f"(at_period_end={at_period_end})"
            )
            return subscription
        except stripe.StripeError as e:
            logger.error(f"Error cancelling subscription {subscription_id}: {e}")
            self._handle_stripe_error(e)

    @with_retry
    def resume_subscription(self, subscription_id: str) -> stripe.Subscription:
        """Resume a cancelled subscription."""
        try:
            subscription = stripe.Subscription.modify(
                subscription_id,
                cancel_at_period_end=False,
            )
            logger.info(f"Resumed subscription: {subscription_id}")
            return subscription
        except stripe.StripeError as e:
            logger.error(f"Error resuming subscription {subscription_id}: {e}")
            self._handle_stripe_error(e)

    # Checkout Session Operations

    @with_retry
    def create_checkout_session(
        self,
        price_id: str,
        success_url: str,
        cancel_url: str,
        mode: str = "subscription",
        customer_id: Optional[str] = None,
        customer_email: Optional[str] = None,
        trial_days: Optional[int] = None,
        metadata: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> stripe.checkout.Session:
        """Create a checkout session."""
        try:
            params = {
                "mode": mode,
                "success_url": success_url,
                "cancel_url": cancel_url,
                "line_items": [{"price": price_id, "quantity": 1}],
                "metadata": metadata or {},
            }

            if customer_id:
                params["customer"] = customer_id
            elif customer_email:
                params["customer_email"] = customer_email

            if trial_days and mode == "subscription":
                params["subscription_data"] = {
                    "trial_period_days": trial_days,
                }

            params.update(kwargs)

            session = stripe.checkout.Session.create(**params)
            logger.info(f"Created checkout session: {session.id}")
            return session
        except stripe.StripeError as e:
            logger.error(f"Error creating checkout session: {e}")
            self._handle_stripe_error(e)

    @with_retry
    def get_checkout_session(self, session_id: str) -> stripe.checkout.Session:
        """Retrieve a checkout session."""
        try:
            return stripe.checkout.Session.retrieve(
                session_id,
                expand=["subscription", "customer"],
            )
        except stripe.StripeError as e:
            logger.error(f"Error retrieving checkout session {session_id}: {e}")
            self._handle_stripe_error(e)

    # Billing Portal Operations

    @with_retry
    def create_portal_session(
        self,
        customer_id: str,
        return_url: str,
    ) -> stripe.billing_portal.Session:
        """Create a billing portal session."""
        try:
            session = stripe.billing_portal.Session.create(
                customer=customer_id,
                return_url=return_url,
            )
            logger.info(f"Created portal session for customer: {customer_id}")
            return session
        except stripe.StripeError as e:
            logger.error(f"Error creating portal session: {e}")
            self._handle_stripe_error(e)

    # Product and Price Operations

    @with_retry
    def list_products(
        self,
        active: bool = True,
        limit: int = 100,
        **kwargs,
    ) -> list[stripe.Product]:
        """List all products."""
        try:
            products = stripe.Product.list(
                active=active,
                limit=limit,
                **kwargs,
            )
            return list(products.auto_paging_iter())
        except stripe.StripeError as e:
            logger.error(f"Error listing products: {e}")
            self._handle_stripe_error(e)

    @with_retry
    def get_product(self, product_id: str) -> stripe.Product:
        """Retrieve a product."""
        try:
            return stripe.Product.retrieve(product_id)
        except stripe.StripeError as e:
            logger.error(f"Error retrieving product {product_id}: {e}")
            self._handle_stripe_error(e)

    @with_retry
    def list_prices(
        self,
        product_id: Optional[str] = None,
        active: bool = True,
        limit: int = 100,
        **kwargs,
    ) -> list[stripe.Price]:
        """List prices for a product."""
        try:
            params = {"active": active, "limit": limit}
            if product_id:
                params["product"] = product_id
            params.update(kwargs)

            prices = stripe.Price.list(**params)
            return list(prices.auto_paging_iter())
        except stripe.StripeError as e:
            logger.error(f"Error listing prices: {e}")
            self._handle_stripe_error(e)

    @with_retry
    def get_price(self, price_id: str) -> stripe.Price:
        """Retrieve a price."""
        try:
            return stripe.Price.retrieve(price_id)
        except stripe.StripeError as e:
            logger.error(f"Error retrieving price {price_id}: {e}")
            self._handle_stripe_error(e)

    # Invoice Operations

    @with_retry
    def list_invoices(
        self,
        customer_id: Optional[str] = None,
        subscription_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 10,
    ) -> list[stripe.Invoice]:
        """List invoices."""
        try:
            params = {"limit": limit}
            if customer_id:
                params["customer"] = customer_id
            if subscription_id:
                params["subscription"] = subscription_id
            if status:
                params["status"] = status

            invoices = stripe.Invoice.list(**params)
            return list(invoices.data)
        except stripe.StripeError as e:
            logger.error(f"Error listing invoices: {e}")
            self._handle_stripe_error(e)

    @with_retry
    def get_invoice(self, invoice_id: str) -> stripe.Invoice:
        """Retrieve an invoice."""
        try:
            return stripe.Invoice.retrieve(invoice_id)
        except stripe.StripeError as e:
            logger.error(f"Error retrieving invoice {invoice_id}: {e}")
            self._handle_stripe_error(e)

    # Payment Method Operations

    @with_retry
    def list_payment_methods(
        self,
        customer_id: str,
        type: str = "card",
    ) -> list[stripe.PaymentMethod]:
        """List payment methods for a customer."""
        try:
            methods = stripe.PaymentMethod.list(
                customer=customer_id,
                type=type,
            )
            return list(methods.data)
        except stripe.StripeError as e:
            logger.error(f"Error listing payment methods: {e}")
            self._handle_stripe_error(e)

    @with_retry
    def attach_payment_method(
        self,
        payment_method_id: str,
        customer_id: str,
    ) -> stripe.PaymentMethod:
        """Attach a payment method to a customer."""
        try:
            method = stripe.PaymentMethod.attach(
                payment_method_id,
                customer=customer_id,
            )
            logger.info(
                f"Attached payment method {payment_method_id} "
                f"to customer {customer_id}"
            )
            return method
        except stripe.StripeError as e:
            logger.error(f"Error attaching payment method: {e}")
            self._handle_stripe_error(e)

    @with_retry
    def set_default_payment_method(
        self,
        customer_id: str,
        payment_method_id: str,
    ) -> stripe.Customer:
        """Set default payment method for a customer."""
        try:
            customer = stripe.Customer.modify(
                customer_id,
                invoice_settings={"default_payment_method": payment_method_id},
            )
            logger.info(
                f"Set default payment method for customer {customer_id}"
            )
            return customer
        except stripe.StripeError as e:
            logger.error(f"Error setting default payment method: {e}")
            self._handle_stripe_error(e)

    # Webhook Signature Verification

    def verify_webhook_signature(
        self,
        payload: bytes,
        signature: str,
    ) -> stripe.Event:
        """
        Verify webhook signature and construct event.

        Args:
            payload: Raw webhook payload bytes
            signature: Stripe-Signature header value

        Returns:
            Verified Stripe event

        Raises:
            StripeValidationError: If signature is invalid
        """
        try:
            event = stripe.Webhook.construct_event(
                payload,
                signature,
                self.config.webhook_secret,
                tolerance=self.config.webhook_tolerance,
            )
            return event
        except stripe.SignatureVerificationError as e:
            logger.error(f"Webhook signature verification failed: {e}")
            raise StripeValidationError(
                message="Invalid webhook signature",
                stripe_error=e,
            )

    # Usage Records

    @with_retry
    def create_usage_record(
        self,
        subscription_item_id: str,
        quantity: int,
        timestamp: Optional[int] = None,
        action: str = "increment",
    ) -> stripe.SubscriptionItem:
        """Create a usage record for metered billing."""
        try:
            params = {
                "quantity": quantity,
                "action": action,
            }
            if timestamp:
                params["timestamp"] = timestamp

            record = stripe.SubscriptionItem.create_usage_record(
                subscription_item_id,
                **params,
            )
            logger.info(
                f"Created usage record for subscription item "
                f"{subscription_item_id}: {quantity}"
            )
            return record
        except stripe.StripeError as e:
            logger.error(f"Error creating usage record: {e}")
            self._handle_stripe_error(e)


# Singleton instance
_client: Optional[StripeClient] = None


def get_client(config: Optional[StripeConfig] = None) -> StripeClient:
    """Get or create the Stripe client singleton."""
    global _client
    if _client is None or config is not None:
        _client = StripeClient(config)
    return _client
