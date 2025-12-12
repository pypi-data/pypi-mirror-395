"""
Main billing service providing high-level billing operations.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

import logging
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List, Callable, Awaitable
import stripe

from .config import get_config, StripeConfig
from .client import StripeClient, get_client
from .models import (
    Customer,
    CustomerCreate,
    CustomerUpdate,
    Subscription,
    SubscriptionCreate,
    SubscriptionUpdate,
    Plan,
    PlanPrice,
    PlanLimits,
    CheckoutSession,
    CheckoutSessionCreate,
    Invoice,
    PaymentMethod,
    BillingPortalSession,
    SubscriptionStatus,
    BillingPeriod,
)
from .models.results import (
    CustomerResult,
    SubscriptionResult,
    CheckoutResult,
    PortalResult,
)
from .exceptions import (
    CustomerNotFoundError,
    SubscriptionNotFoundError,
    PlanNotFoundError,
)

logger = logging.getLogger(__name__)


# Type for storage callbacks
CustomerStorageCallback = Callable[[Customer], Awaitable[Customer]]
SubscriptionStorageCallback = Callable[[Subscription], Awaitable[Subscription]]


class BillingService:
    """
    High-level billing service.

    Provides a clean API for common billing operations with optional
    database integration via callbacks.

    Example:
        ```python
        from bizstats_stripe_billing import BillingService

        billing = BillingService()

        # Create customer
        result = billing.create_customer(
            CustomerCreate(email="user@example.com", name="John Doe")
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
        ```
    """

    def __init__(
        self,
        config: Optional[StripeConfig] = None,
        client: Optional[StripeClient] = None,
    ):
        """
        Initialize billing service.

        Args:
            config: Optional Stripe configuration
            client: Optional Stripe client (creates new if not provided)
        """
        self.config = config or get_config()
        self.client = client or get_client(self.config)

        # Optional storage callbacks
        self._on_customer_created: Optional[CustomerStorageCallback] = None
        self._on_subscription_created: Optional[SubscriptionStorageCallback] = None
        self._on_subscription_updated: Optional[SubscriptionStorageCallback] = None

    def on_customer_created(self, callback: CustomerStorageCallback) -> None:
        """Register callback for customer creation."""
        self._on_customer_created = callback

    def on_subscription_created(self, callback: SubscriptionStorageCallback) -> None:
        """Register callback for subscription creation."""
        self._on_subscription_created = callback

    def on_subscription_updated(self, callback: SubscriptionStorageCallback) -> None:
        """Register callback for subscription updates."""
        self._on_subscription_updated = callback

    # Customer Operations

    def create_customer(
        self,
        data: CustomerCreate,
        id_generator: Optional[Callable[[], str]] = None,
    ) -> CustomerResult:
        """
        Create a new customer in Stripe.

        Args:
            data: Customer creation data
            id_generator: Optional function to generate internal customer ID

        Returns:
            CustomerResult with customer IDs
        """
        try:
            # Prepare metadata
            metadata = dict(data.metadata)
            if data.organization_id:
                metadata["organization_id"] = data.organization_id
            if data.user_id:
                metadata["user_id"] = data.user_id

            # Create in Stripe
            stripe_customer = self.client.create_customer(
                email=data.email,
                name=data.name,
                metadata=metadata,
            )

            # Generate internal ID
            internal_id = id_generator() if id_generator else stripe_customer.id

            logger.info(
                f"Created customer: internal_id={internal_id}, "
                f"stripe_id={stripe_customer.id}"
            )

            return CustomerResult.ok(
                customer_id=internal_id,
                stripe_customer_id=stripe_customer.id,
            )

        except Exception as e:
            logger.error(f"Error creating customer: {e}")
            return CustomerResult.error(str(e))

    def get_customer(self, stripe_customer_id: str) -> Customer:
        """
        Retrieve a customer from Stripe.

        Args:
            stripe_customer_id: Stripe customer ID

        Returns:
            Customer model

        Raises:
            CustomerNotFoundError: If customer not found
        """
        try:
            stripe_customer = self.client.get_customer(stripe_customer_id)
            return self._stripe_customer_to_model(stripe_customer)
        except Exception as e:
            if "No such customer" in str(e):
                raise CustomerNotFoundError(stripe_customer_id)
            raise

    def update_customer(
        self,
        stripe_customer_id: str,
        data: CustomerUpdate,
    ) -> Customer:
        """
        Update a customer in Stripe.

        Args:
            stripe_customer_id: Stripe customer ID
            data: Update data

        Returns:
            Updated Customer model
        """
        update_params = {}
        if data.email is not None:
            update_params["email"] = data.email
        if data.name is not None:
            update_params["name"] = data.name
        if data.phone is not None:
            update_params["phone"] = data.phone
        if data.metadata is not None:
            update_params["metadata"] = data.metadata

        stripe_customer = self.client.update_customer(
            stripe_customer_id,
            **update_params,
        )
        return self._stripe_customer_to_model(stripe_customer)

    # Subscription Operations

    def create_subscription(
        self,
        data: SubscriptionCreate,
    ) -> SubscriptionResult:
        """
        Create a new subscription.

        Args:
            data: Subscription creation data

        Returns:
            SubscriptionResult with subscription IDs
        """
        try:
            # Create in Stripe
            stripe_subscription = self.client.create_subscription(
                customer_id=data.customer_id,
                price_id=data.price_id,
                trial_days=data.trial_days,
                metadata=data.metadata,
            )

            # Get client secret if payment is required
            client_secret = None
            if hasattr(stripe_subscription, "latest_invoice"):
                invoice = stripe_subscription.latest_invoice
                if hasattr(invoice, "payment_intent") and invoice.payment_intent:
                    client_secret = invoice.payment_intent.client_secret

            # Get trial end
            trial_end = None
            if stripe_subscription.trial_end:
                trial_end = datetime.fromtimestamp(
                    stripe_subscription.trial_end, tz=timezone.utc
                )

            logger.info(f"Created subscription: {stripe_subscription.id}")

            return SubscriptionResult.ok(
                subscription_id=stripe_subscription.id,
                stripe_subscription_id=stripe_subscription.id,
                client_secret=client_secret,
                trial_end=trial_end,
            )

        except Exception as e:
            logger.error(f"Error creating subscription: {e}")
            return SubscriptionResult.error(str(e))

    def get_subscription(self, stripe_subscription_id: str) -> Subscription:
        """
        Retrieve a subscription from Stripe.

        Args:
            stripe_subscription_id: Stripe subscription ID

        Returns:
            Subscription model

        Raises:
            SubscriptionNotFoundError: If subscription not found
        """
        try:
            stripe_subscription = self.client.get_subscription(stripe_subscription_id)
            return self._stripe_subscription_to_model(stripe_subscription)
        except Exception as e:
            if "No such subscription" in str(e):
                raise SubscriptionNotFoundError(stripe_subscription_id)
            raise

    def update_subscription(
        self,
        stripe_subscription_id: str,
        data: SubscriptionUpdate,
    ) -> SubscriptionResult:
        """
        Update a subscription.

        Args:
            stripe_subscription_id: Stripe subscription ID
            data: Update data

        Returns:
            SubscriptionResult
        """
        try:
            update_params = {
                "proration_behavior": data.proration_behavior,
            }

            if data.price_id:
                # Get current subscription to find item ID
                current = self.client.get_subscription(stripe_subscription_id)
                item_id = current.items.data[0].id
                update_params["items"] = [{"id": item_id, "price": data.price_id}]

            if data.cancel_at_period_end is not None:
                update_params["cancel_at_period_end"] = data.cancel_at_period_end

            if data.metadata:
                update_params["metadata"] = data.metadata

            stripe_subscription = self.client.update_subscription(
                stripe_subscription_id,
                **update_params,
            )

            logger.info(f"Updated subscription: {stripe_subscription_id}")

            return SubscriptionResult.ok(
                subscription_id=stripe_subscription.id,
                stripe_subscription_id=stripe_subscription.id,
            )

        except Exception as e:
            logger.error(f"Error updating subscription: {e}")
            return SubscriptionResult.error(str(e))

    def cancel_subscription(
        self,
        stripe_subscription_id: str,
        at_period_end: bool = True,
    ) -> SubscriptionResult:
        """
        Cancel a subscription.

        Args:
            stripe_subscription_id: Stripe subscription ID
            at_period_end: Whether to cancel at end of billing period

        Returns:
            SubscriptionResult
        """
        try:
            stripe_subscription = self.client.cancel_subscription(
                stripe_subscription_id,
                at_period_end=at_period_end,
            )

            logger.info(
                f"Cancelled subscription: {stripe_subscription_id} "
                f"(at_period_end={at_period_end})"
            )

            return SubscriptionResult.ok(
                subscription_id=stripe_subscription.id,
                stripe_subscription_id=stripe_subscription.id,
            )

        except Exception as e:
            logger.error(f"Error cancelling subscription: {e}")
            return SubscriptionResult.error(str(e))

    def resume_subscription(
        self,
        stripe_subscription_id: str,
    ) -> SubscriptionResult:
        """
        Resume a cancelled subscription (before period end).

        Args:
            stripe_subscription_id: Stripe subscription ID

        Returns:
            SubscriptionResult
        """
        try:
            stripe_subscription = self.client.resume_subscription(
                stripe_subscription_id,
            )

            logger.info(f"Resumed subscription: {stripe_subscription_id}")

            return SubscriptionResult.ok(
                subscription_id=stripe_subscription.id,
                stripe_subscription_id=stripe_subscription.id,
            )

        except Exception as e:
            logger.error(f"Error resuming subscription: {e}")
            return SubscriptionResult.error(str(e))

    # Checkout Operations

    def create_checkout_session(
        self,
        data: CheckoutSessionCreate,
    ) -> CheckoutResult:
        """
        Create a Stripe Checkout session.

        Args:
            data: Checkout session creation data

        Returns:
            CheckoutResult with session URL
        """
        try:
            # Use configured URLs if not provided
            success_url = data.success_url or self.config.success_url
            cancel_url = data.cancel_url or self.config.cancel_url

            session = self.client.create_checkout_session(
                price_id=data.price_id,
                success_url=success_url,
                cancel_url=cancel_url,
                mode=data.mode,
                customer_id=data.customer_id,
                customer_email=data.customer_email,
                trial_days=data.trial_days,
                metadata=data.metadata,
                allow_promotion_codes=data.allow_promotion_codes,
                billing_address_collection=data.billing_address_collection,
                automatic_tax={"enabled": data.automatic_tax}
                if data.automatic_tax
                else None,
            )

            logger.info(f"Created checkout session: {session.id}")

            return CheckoutResult.ok(
                session_id=session.id,
                checkout_url=session.url,
            )

        except Exception as e:
            logger.error(f"Error creating checkout session: {e}")
            return CheckoutResult.error(str(e))

    # Billing Portal Operations

    def create_portal_session(
        self,
        stripe_customer_id: str,
        return_url: Optional[str] = None,
    ) -> PortalResult:
        """
        Create a billing portal session.

        Args:
            stripe_customer_id: Stripe customer ID
            return_url: URL to return to after portal session

        Returns:
            PortalResult with portal URL
        """
        try:
            url = return_url or self.config.portal_return_url

            session = self.client.create_portal_session(
                customer_id=stripe_customer_id,
                return_url=url,
            )

            logger.info(
                f"Created portal session for customer: {stripe_customer_id}"
            )

            return PortalResult.ok(
                session_id=session.id,
                portal_url=session.url,
            )

        except Exception as e:
            logger.error(f"Error creating portal session: {e}")
            return PortalResult.error(str(e))

    # Plan Operations

    def list_plans(
        self,
        active_only: bool = True,
    ) -> List[Plan]:
        """
        List all available plans.

        Args:
            active_only: Only return active plans

        Returns:
            List of Plan models
        """
        products = self.client.list_products(active=active_only)
        plans = []

        for product in products:
            # Get prices for this product
            prices = self.client.list_prices(
                product_id=product.id,
                active=active_only,
            )
            plan = self._stripe_product_to_plan(product, prices)
            plans.append(plan)

        return plans

    def get_plan(self, product_id: str) -> Plan:
        """
        Get a specific plan by product ID.

        Args:
            product_id: Stripe product ID

        Returns:
            Plan model

        Raises:
            PlanNotFoundError: If plan not found
        """
        try:
            product = self.client.get_product(product_id)
            prices = self.client.list_prices(product_id=product_id)
            return self._stripe_product_to_plan(product, prices)
        except Exception as e:
            if "No such product" in str(e):
                raise PlanNotFoundError(product_id)
            raise

    # Invoice Operations

    def list_invoices(
        self,
        stripe_customer_id: str,
        limit: int = 10,
    ) -> List[Invoice]:
        """
        List invoices for a customer.

        Args:
            stripe_customer_id: Stripe customer ID
            limit: Maximum number of invoices to return

        Returns:
            List of Invoice models
        """
        stripe_invoices = self.client.list_invoices(
            customer_id=stripe_customer_id,
            limit=limit,
        )
        return [self._stripe_invoice_to_model(inv) for inv in stripe_invoices]

    # Payment Method Operations

    def list_payment_methods(
        self,
        stripe_customer_id: str,
    ) -> List[PaymentMethod]:
        """
        List payment methods for a customer.

        Args:
            stripe_customer_id: Stripe customer ID

        Returns:
            List of PaymentMethod models
        """
        methods = self.client.list_payment_methods(
            customer_id=stripe_customer_id,
        )
        return [self._stripe_payment_method_to_model(m) for m in methods]

    def set_default_payment_method(
        self,
        stripe_customer_id: str,
        payment_method_id: str,
    ) -> Customer:
        """
        Set default payment method for a customer.

        Args:
            stripe_customer_id: Stripe customer ID
            payment_method_id: Payment method ID to set as default

        Returns:
            Updated Customer model
        """
        stripe_customer = self.client.set_default_payment_method(
            customer_id=stripe_customer_id,
            payment_method_id=payment_method_id,
        )
        return self._stripe_customer_to_model(stripe_customer)

    # Helper Methods

    def _stripe_customer_to_model(
        self,
        stripe_customer: stripe.Customer,
    ) -> Customer:
        """Convert Stripe customer to our model."""
        return Customer(
            id=stripe_customer.id,
            stripe_customer_id=stripe_customer.id,
            email=stripe_customer.email or "",
            name=stripe_customer.name,
            phone=stripe_customer.phone,
            default_currency=stripe_customer.currency or "usd",
            metadata=dict(stripe_customer.metadata or {}),
            organization_id=stripe_customer.metadata.get("organization_id")
            if stripe_customer.metadata
            else None,
            created_at=datetime.fromtimestamp(
                stripe_customer.created, tz=timezone.utc
            ),
            updated_at=datetime.now(timezone.utc),
        )

    def _stripe_subscription_to_model(
        self,
        stripe_sub: stripe.Subscription,
    ) -> Subscription:
        """Convert Stripe subscription to our model."""
        # Get billing period from price
        billing_period = BillingPeriod.MONTHLY
        if stripe_sub.items.data:
            interval = stripe_sub.items.data[0].price.recurring.interval
            billing_period = BillingPeriod(interval)

        return Subscription(
            id=stripe_sub.id,
            stripe_subscription_id=stripe_sub.id,
            customer_id=stripe_sub.customer,
            plan_id=stripe_sub.items.data[0].price.product
            if stripe_sub.items.data
            else "",
            plan_name=stripe_sub.items.data[0].price.nickname or "Unknown"
            if stripe_sub.items.data
            else "Unknown",
            status=SubscriptionStatus(stripe_sub.status),
            billing_period=billing_period,
            amount=stripe_sub.items.data[0].price.unit_amount or 0
            if stripe_sub.items.data
            else 0,
            currency=stripe_sub.currency or "usd",
            current_period_start=datetime.fromtimestamp(
                stripe_sub.current_period_start, tz=timezone.utc
            )
            if stripe_sub.current_period_start
            else None,
            current_period_end=datetime.fromtimestamp(
                stripe_sub.current_period_end, tz=timezone.utc
            )
            if stripe_sub.current_period_end
            else None,
            trial_start=datetime.fromtimestamp(
                stripe_sub.trial_start, tz=timezone.utc
            )
            if stripe_sub.trial_start
            else None,
            trial_end=datetime.fromtimestamp(stripe_sub.trial_end, tz=timezone.utc)
            if stripe_sub.trial_end
            else None,
            cancel_at_period_end=stripe_sub.cancel_at_period_end,
            canceled_at=datetime.fromtimestamp(
                stripe_sub.canceled_at, tz=timezone.utc
            )
            if stripe_sub.canceled_at
            else None,
            ended_at=datetime.fromtimestamp(stripe_sub.ended_at, tz=timezone.utc)
            if stripe_sub.ended_at
            else None,
            metadata=dict(stripe_sub.metadata or {}),
            created_at=datetime.fromtimestamp(stripe_sub.created, tz=timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

    def _stripe_product_to_plan(
        self,
        product: stripe.Product,
        prices: List[stripe.Price],
    ) -> Plan:
        """Convert Stripe product and prices to Plan model."""
        price_dict = {}
        monthly_price = 0
        yearly_price = 0

        for price in prices:
            if price.recurring:
                interval = price.recurring.interval
                price_model = PlanPrice(
                    id=price.id,
                    amount=price.unit_amount or 0,
                    currency=price.currency,
                    interval=BillingPeriod(interval),
                    interval_count=price.recurring.interval_count or 1,
                )
                if interval == "month":
                    price_dict["monthly"] = price_model
                    monthly_price = price.unit_amount or 0
                elif interval == "year":
                    price_dict["yearly"] = price_model
                    yearly_price = price.unit_amount or 0

        # Parse features from metadata or marketing_features
        features = []
        if hasattr(product, "marketing_features"):
            features = [f.name for f in product.marketing_features]

        return Plan(
            id=product.metadata.get("plan_id", product.id)
            if product.metadata
            else product.id,
            stripe_product_id=product.id,
            name=product.name,
            description=product.description,
            active=product.active,
            prices=price_dict,
            monthly_price=monthly_price,
            yearly_price=yearly_price,
            features=features,
            is_popular=product.metadata.get("is_popular", "false").lower() == "true"
            if product.metadata
            else False,
            is_recommended=product.metadata.get("is_recommended", "false").lower()
            == "true"
            if product.metadata
            else False,
            badge=product.metadata.get("badge") if product.metadata else None,
            color=product.metadata.get("color") if product.metadata else None,
            metadata=dict(product.metadata or {}),
            created_at=datetime.fromtimestamp(product.created, tz=timezone.utc)
            if product.created
            else None,
            updated_at=datetime.fromtimestamp(product.updated, tz=timezone.utc)
            if product.updated
            else None,
        )

    def _stripe_invoice_to_model(
        self,
        invoice: stripe.Invoice,
    ) -> Invoice:
        """Convert Stripe invoice to our model."""
        from .models.enums import InvoiceStatus

        return Invoice(
            id=invoice.id,
            customer_id=invoice.customer,
            subscription_id=invoice.subscription,
            status=InvoiceStatus(invoice.status) if invoice.status else InvoiceStatus.DRAFT,
            amount_due=invoice.amount_due or 0,
            amount_paid=invoice.amount_paid or 0,
            amount_remaining=invoice.amount_remaining or 0,
            subtotal=invoice.subtotal or 0,
            tax=invoice.tax or 0,
            total=invoice.total or 0,
            currency=invoice.currency or "usd",
            hosted_invoice_url=invoice.hosted_invoice_url,
            invoice_pdf=invoice.invoice_pdf,
            due_date=datetime.fromtimestamp(invoice.due_date, tz=timezone.utc)
            if invoice.due_date
            else None,
            paid_at=datetime.fromtimestamp(
                invoice.status_transitions.paid_at, tz=timezone.utc
            )
            if invoice.status_transitions and invoice.status_transitions.paid_at
            else None,
            period_start=datetime.fromtimestamp(invoice.period_start, tz=timezone.utc)
            if invoice.period_start
            else None,
            period_end=datetime.fromtimestamp(invoice.period_end, tz=timezone.utc)
            if invoice.period_end
            else None,
            created_at=datetime.fromtimestamp(invoice.created, tz=timezone.utc),
        )

    def _stripe_payment_method_to_model(
        self,
        method: stripe.PaymentMethod,
    ) -> PaymentMethod:
        """Convert Stripe payment method to our model."""
        card_details = {}
        if method.card:
            card_details = {
                "card_brand": method.card.brand,
                "card_last4": method.card.last4,
                "card_exp_month": method.card.exp_month,
                "card_exp_year": method.card.exp_year,
            }

        return PaymentMethod(
            id=method.id,
            type=method.type,
            **card_details,
            is_default=False,  # Need to check against customer default
            created_at=datetime.fromtimestamp(method.created, tz=timezone.utc),
        )


# Convenience function
def create_billing_service(
    config: Optional[StripeConfig] = None,
) -> BillingService:
    """Create a new BillingService instance."""
    return BillingService(config)
