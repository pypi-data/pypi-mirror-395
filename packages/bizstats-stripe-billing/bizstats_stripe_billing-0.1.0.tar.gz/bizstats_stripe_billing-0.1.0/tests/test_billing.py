"""
Tests for BillingService module.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime, timezone

from bizstats_stripe_billing import (
    BillingService,
    create_billing_service,
    StripeConfig,
    CustomerCreate,
    CustomerUpdate,
    SubscriptionCreate,
    SubscriptionUpdate,
    CheckoutSessionCreate,
    SubscriptionStatus,
    BillingPeriod,
    SubscriptionPlan,
)
from bizstats_stripe_billing.exceptions import (
    CustomerNotFoundError,
    SubscriptionNotFoundError,
)


class TestBillingServiceInitialization:
    """Tests for BillingService initialization."""

    def test_service_initialization(self, test_config):
        """Test service initializes with config."""
        with patch("stripe.api_key"):
            with patch("stripe.api_version"):
                service = BillingService(test_config)
                assert service.config == test_config

    def test_service_has_client(self, billing_service):
        """Test service has a Stripe client."""
        assert billing_service.client is not None


class TestCustomerOperations:
    """Tests for customer operations in BillingService."""

    def test_create_customer(self, billing_service, mock_stripe_customer):
        """Test creating a customer."""
        with patch.object(billing_service.client, "create_customer", return_value=mock_stripe_customer):
            create_data = CustomerCreate(
                email="test@example.com",
                name="Test User",
            )
            result = billing_service.create_customer(create_data)
            assert result.success is True
            assert result.stripe_customer_id == "cus_test123"

    def test_create_customer_failure(self, billing_service):
        """Test customer creation failure."""
        with patch.object(billing_service.client, "create_customer", side_effect=Exception("API Error")):
            create_data = CustomerCreate(email="test@example.com")
            result = billing_service.create_customer(create_data)
            assert result.success is False
            assert "API Error" in result.error_message

    def test_get_customer(self, billing_service, mock_stripe_customer):
        """Test retrieving a customer."""
        # Add required attributes for conversion
        mock_stripe_customer.phone = None
        mock_stripe_customer.currency = "usd"

        with patch.object(billing_service.client, "get_customer", return_value=mock_stripe_customer):
            customer = billing_service.get_customer("cus_test123")
            assert customer.stripe_customer_id == "cus_test123"
            assert customer.email == "test@example.com"

    def test_get_customer_not_found(self, billing_service):
        """Test customer not found."""
        with patch.object(billing_service.client, "get_customer", side_effect=Exception("No such customer")):
            with pytest.raises(CustomerNotFoundError):
                billing_service.get_customer("cus_123")

    def test_update_customer(self, billing_service, mock_stripe_customer):
        """Test updating a customer."""
        mock_stripe_customer.name = "Updated Name"
        mock_stripe_customer.phone = None
        mock_stripe_customer.currency = "usd"

        with patch.object(billing_service.client, "update_customer", return_value=mock_stripe_customer):
            update = CustomerUpdate(name="Updated Name")
            customer = billing_service.update_customer("cus_test123", update)
            assert customer.name == "Updated Name"


class TestSubscriptionOperations:
    """Tests for subscription operations in BillingService."""

    def test_create_subscription(self, billing_service, mock_stripe_subscription):
        """Test creating a subscription."""
        mock_stripe_subscription.trial_end = None

        with patch.object(billing_service.client, "create_subscription", return_value=mock_stripe_subscription):
            create_data = SubscriptionCreate(
                customer_id="cus_test123",
                plan_id="plan_test123",
                price_id="price_test123",
            )
            result = billing_service.create_subscription(create_data)
            assert result.success is True
            assert result.subscription_id == "sub_test123"

    def test_create_subscription_failure(self, billing_service):
        """Test subscription creation failure."""
        with patch.object(billing_service.client, "create_subscription", side_effect=Exception("Error")):
            create_data = SubscriptionCreate(
                customer_id="cus_test123",
                plan_id="plan_test123",
                price_id="price_test123",
            )
            result = billing_service.create_subscription(create_data)
            assert result.success is False

    def test_get_subscription(self, billing_service, mock_stripe_subscription):
        """Test retrieving a subscription."""
        # Add additional attributes needed for conversion
        mock_stripe_subscription.currency = "usd"
        mock_stripe_subscription.created = int(datetime.now(timezone.utc).timestamp())
        mock_stripe_subscription.ended_at = None

        with patch.object(billing_service.client, "get_subscription", return_value=mock_stripe_subscription):
            subscription = billing_service.get_subscription("sub_test123")
            assert subscription.stripe_subscription_id == "sub_test123"
            assert subscription.status == SubscriptionStatus.ACTIVE

    def test_get_subscription_not_found(self, billing_service):
        """Test subscription not found."""
        with patch.object(billing_service.client, "get_subscription", side_effect=Exception("No such subscription")):
            with pytest.raises(SubscriptionNotFoundError):
                billing_service.get_subscription("sub_123")

    def test_cancel_subscription(self, billing_service, mock_stripe_subscription):
        """Test canceling a subscription."""
        mock_stripe_subscription.cancel_at_period_end = True

        with patch.object(billing_service.client, "cancel_subscription", return_value=mock_stripe_subscription):
            result = billing_service.cancel_subscription("sub_test123")
            assert result.success is True

    def test_cancel_subscription_immediate(self, billing_service, mock_stripe_subscription):
        """Test immediate subscription cancellation."""
        mock_stripe_subscription.status = "canceled"

        with patch.object(billing_service.client, "cancel_subscription", return_value=mock_stripe_subscription):
            result = billing_service.cancel_subscription("sub_test123", at_period_end=False)
            assert result.success is True

    def test_resume_subscription(self, billing_service, mock_stripe_subscription):
        """Test resuming a canceled subscription."""
        mock_stripe_subscription.cancel_at_period_end = False

        with patch.object(billing_service.client, "resume_subscription", return_value=mock_stripe_subscription):
            result = billing_service.resume_subscription("sub_test123")
            assert result.success is True


class TestCheckoutOperations:
    """Tests for checkout operations in BillingService."""

    def test_create_checkout_session(self, billing_service, mock_stripe_checkout_session):
        """Test creating a checkout session."""
        with patch.object(billing_service.client, "create_checkout_session", return_value=mock_stripe_checkout_session):
            create_data = CheckoutSessionCreate(
                customer_id="cus_test123",
                price_id="price_test123",
                success_url="https://example.com/success",
                cancel_url="https://example.com/cancel",
            )
            result = billing_service.create_checkout_session(create_data)
            assert result.success is True
            assert result.session_id == "cs_test123"
            assert result.checkout_url is not None

    def test_create_checkout_session_failure(self, billing_service):
        """Test checkout session creation failure."""
        with patch.object(billing_service.client, "create_checkout_session", side_effect=Exception("Error")):
            create_data = CheckoutSessionCreate(
                customer_id="cus_test123",
                price_id="price_test123",
                success_url="https://example.com/success",
                cancel_url="https://example.com/cancel",
            )
            result = billing_service.create_checkout_session(create_data)
            assert result.success is False


class TestBillingPortalOperations:
    """Tests for billing portal operations in BillingService."""

    def test_create_portal_session(self, billing_service, mock_stripe_portal_session):
        """Test creating a billing portal session."""
        with patch.object(billing_service.client, "create_portal_session", return_value=mock_stripe_portal_session):
            result = billing_service.create_portal_session(
                stripe_customer_id="cus_test123",
                return_url="https://example.com/account",
            )
            assert result.success is True
            assert result.session_id == "bps_test123"
            assert result.portal_url is not None

    def test_create_portal_session_failure(self, billing_service):
        """Test portal session creation failure."""
        with patch.object(billing_service.client, "create_portal_session", side_effect=Exception("Error")):
            result = billing_service.create_portal_session(
                stripe_customer_id="cus_test123",
                return_url="https://example.com/account",
            )
            assert result.success is False


class TestPlanOperations:
    """Tests for plan operations in BillingService."""

    def test_list_plans(self, billing_service, mock_stripe_product, mock_stripe_price):
        """Test listing plans."""
        mock_stripe_product.created = int(datetime.now(timezone.utc).timestamp())
        mock_stripe_product.updated = int(datetime.now(timezone.utc).timestamp())

        with patch.object(billing_service.client, "list_products", return_value=[mock_stripe_product]):
            with patch.object(billing_service.client, "list_prices", return_value=[mock_stripe_price]):
                plans = billing_service.list_plans()
                assert len(plans) >= 1


class TestInvoiceOperations:
    """Tests for invoice operations in BillingService."""

    def test_list_invoices(self, billing_service, mock_stripe_invoice):
        """Test listing invoices."""
        # Add required attributes
        mock_stripe_invoice.amount_remaining = 0
        mock_stripe_invoice.subtotal = 2900
        mock_stripe_invoice.tax = 0
        mock_stripe_invoice.total = 2900
        mock_stripe_invoice.period_start = int(datetime.now(timezone.utc).timestamp())
        mock_stripe_invoice.period_end = int(datetime.now(timezone.utc).timestamp())
        mock_stripe_invoice.status_transitions = Mock()
        mock_stripe_invoice.status_transitions.paid_at = int(datetime.now(timezone.utc).timestamp())

        with patch.object(billing_service.client, "list_invoices", return_value=[mock_stripe_invoice]):
            invoices = billing_service.list_invoices(stripe_customer_id="cus_test123")
            assert len(invoices) == 1


class TestPaymentMethodOperations:
    """Tests for payment method operations in BillingService."""

    def test_list_payment_methods(self, billing_service):
        """Test listing payment methods."""
        mock_method = Mock()
        mock_method.id = "pm_test123"
        mock_method.type = "card"
        mock_method.card = Mock()
        mock_method.card.brand = "visa"
        mock_method.card.last4 = "4242"
        mock_method.card.exp_month = 12
        mock_method.card.exp_year = 2025
        mock_method.created = int(datetime.now(timezone.utc).timestamp())

        with patch.object(billing_service.client, "list_payment_methods", return_value=[mock_method]):
            methods = billing_service.list_payment_methods(stripe_customer_id="cus_test123")
            assert len(methods) == 1
            assert methods[0].id == "pm_test123"


class TestCallbackRegistration:
    """Tests for callback registration."""

    def test_register_customer_created_callback(self, billing_service):
        """Test registering customer created callback."""
        async def callback(customer):
            return customer

        billing_service.on_customer_created(callback)
        assert billing_service._on_customer_created is not None

    def test_register_subscription_created_callback(self, billing_service):
        """Test registering subscription created callback."""
        async def callback(subscription):
            return subscription

        billing_service.on_subscription_created(callback)
        assert billing_service._on_subscription_created is not None

    def test_register_subscription_updated_callback(self, billing_service):
        """Test registering subscription updated callback."""
        async def callback(subscription):
            return subscription

        billing_service.on_subscription_updated(callback)
        assert billing_service._on_subscription_updated is not None


class TestCreateBillingService:
    """Tests for create_billing_service factory function."""

    def test_create_billing_service_with_config(self, test_config):
        """Test creating billing service with config."""
        with patch("stripe.api_key"):
            with patch("stripe.api_version"):
                service = create_billing_service(test_config)
                assert isinstance(service, BillingService)


class TestCustomerMetadata:
    """Tests for customer metadata handling."""

    def test_create_customer_with_organization_id(self, billing_service, mock_stripe_customer):
        """Test creating customer with organization_id in metadata."""
        with patch.object(billing_service.client, "create_customer", return_value=mock_stripe_customer) as mock_create:
            create_data = CustomerCreate(
                email="test@example.com",
                name="Test User",
                organization_id="org_123",
            )
            result = billing_service.create_customer(create_data)
            assert result.success is True
            # Verify organization_id was added to metadata
            call_args = mock_create.call_args
            assert call_args.kwargs["metadata"]["organization_id"] == "org_123"

    def test_create_customer_with_user_id(self, billing_service, mock_stripe_customer):
        """Test creating customer with user_id in metadata."""
        with patch.object(billing_service.client, "create_customer", return_value=mock_stripe_customer) as mock_create:
            create_data = CustomerCreate(
                email="test@example.com",
                user_id="user_456",
            )
            result = billing_service.create_customer(create_data)
            assert result.success is True
            # Verify user_id was added to metadata
            call_args = mock_create.call_args
            assert call_args.kwargs["metadata"]["user_id"] == "user_456"

    def test_create_customer_with_id_generator(self, billing_service, mock_stripe_customer):
        """Test creating customer with custom ID generator."""
        with patch.object(billing_service.client, "create_customer", return_value=mock_stripe_customer):
            create_data = CustomerCreate(email="test@example.com")
            result = billing_service.create_customer(
                create_data,
                id_generator=lambda: "custom_id_123"
            )
            assert result.success is True
            assert result.customer_id == "custom_id_123"


class TestCustomerUpdateFields:
    """Tests for customer update fields."""

    def test_update_customer_with_phone(self, billing_service, mock_stripe_customer):
        """Test updating customer with phone."""
        mock_stripe_customer.phone = "+1234567890"
        mock_stripe_customer.currency = "usd"

        with patch.object(billing_service.client, "update_customer", return_value=mock_stripe_customer) as mock_update:
            update = CustomerUpdate(phone="+1234567890")
            billing_service.update_customer("cus_test123", update)
            call_args = mock_update.call_args
            assert call_args.kwargs["phone"] == "+1234567890"

    def test_update_customer_with_metadata(self, billing_service, mock_stripe_customer):
        """Test updating customer with metadata."""
        mock_stripe_customer.phone = None
        mock_stripe_customer.currency = "usd"
        mock_stripe_customer.metadata = {"key": "value"}

        with patch.object(billing_service.client, "update_customer", return_value=mock_stripe_customer) as mock_update:
            update = CustomerUpdate(metadata={"key": "value"})
            billing_service.update_customer("cus_test123", update)
            call_args = mock_update.call_args
            assert call_args.kwargs["metadata"] == {"key": "value"}

    def test_update_customer_with_all_fields(self, billing_service, mock_stripe_customer):
        """Test updating customer with all fields."""
        mock_stripe_customer.name = "New Name"
        mock_stripe_customer.email = "new@example.com"
        mock_stripe_customer.phone = "+1234567890"
        mock_stripe_customer.currency = "usd"

        with patch.object(billing_service.client, "update_customer", return_value=mock_stripe_customer) as mock_update:
            update = CustomerUpdate(
                email="new@example.com",
                name="New Name",
                phone="+1234567890",
                metadata={"plan": "premium"}
            )
            billing_service.update_customer("cus_test123", update)
            call_args = mock_update.call_args
            assert call_args.kwargs["email"] == "new@example.com"
            assert call_args.kwargs["name"] == "New Name"
            assert call_args.kwargs["phone"] == "+1234567890"


class TestCustomerErrorPaths:
    """Tests for customer error handling paths."""

    def test_get_customer_other_error(self, billing_service):
        """Test get_customer re-raises non-NotFound errors."""
        with patch.object(billing_service.client, "get_customer", side_effect=Exception("Network error")):
            with pytest.raises(Exception, match="Network error"):
                billing_service.get_customer("cus_123")


class TestSubscriptionWithPayment:
    """Tests for subscription with payment intent."""

    def test_create_subscription_with_payment_intent(self, billing_service, mock_stripe_subscription):
        """Test creating subscription that requires payment."""
        mock_stripe_subscription.trial_end = None

        # Add mock for latest_invoice with payment_intent
        mock_payment_intent = Mock()
        mock_payment_intent.client_secret = "pi_secret_123"

        mock_invoice = Mock()
        mock_invoice.payment_intent = mock_payment_intent

        mock_stripe_subscription.latest_invoice = mock_invoice

        with patch.object(billing_service.client, "create_subscription", return_value=mock_stripe_subscription):
            create_data = SubscriptionCreate(
                customer_id="cus_test123",
                plan_id="plan_test123",
                price_id="price_test123",
            )
            result = billing_service.create_subscription(create_data)
            assert result.success is True
            assert result.client_secret == "pi_secret_123"

    def test_create_subscription_with_trial(self, billing_service, mock_stripe_subscription):
        """Test creating subscription with trial period."""
        import time
        trial_timestamp = int(time.time()) + 86400 * 14  # 14 days from now

        mock_stripe_subscription.trial_end = trial_timestamp

        with patch.object(billing_service.client, "create_subscription", return_value=mock_stripe_subscription):
            create_data = SubscriptionCreate(
                customer_id="cus_test123",
                plan_id="plan_test123",
                price_id="price_test123",
                trial_days=14,
            )
            result = billing_service.create_subscription(create_data)
            assert result.success is True
            assert result.trial_end is not None


class TestSubscriptionUpdate:
    """Tests for subscription update operations."""

    def test_update_subscription_price(self, billing_service, mock_stripe_subscription):
        """Test updating subscription price."""
        # Setup mock subscription with items
        mock_item = Mock()
        mock_item.id = "si_test123"
        mock_stripe_subscription.items = Mock()
        mock_stripe_subscription.items.data = [mock_item]

        with patch.object(billing_service.client, "get_subscription", return_value=mock_stripe_subscription):
            with patch.object(billing_service.client, "update_subscription", return_value=mock_stripe_subscription):
                update_data = SubscriptionUpdate(
                    price_id="price_new123",
                    proration_behavior="create_prorations",
                )
                result = billing_service.update_subscription("sub_test123", update_data)
                assert result.success is True

    def test_update_subscription_cancel_at_period_end(self, billing_service, mock_stripe_subscription):
        """Test updating subscription to cancel at period end."""
        with patch.object(billing_service.client, "update_subscription", return_value=mock_stripe_subscription):
            update_data = SubscriptionUpdate(
                cancel_at_period_end=True,
                proration_behavior="none",
            )
            result = billing_service.update_subscription("sub_test123", update_data)
            assert result.success is True

    def test_update_subscription_with_metadata(self, billing_service, mock_stripe_subscription):
        """Test updating subscription metadata."""
        with patch.object(billing_service.client, "update_subscription", return_value=mock_stripe_subscription):
            update_data = SubscriptionUpdate(
                metadata={"key": "value"},
                proration_behavior="none",
            )
            result = billing_service.update_subscription("sub_test123", update_data)
            assert result.success is True

    def test_update_subscription_failure(self, billing_service):
        """Test subscription update failure."""
        with patch.object(billing_service.client, "update_subscription", side_effect=Exception("Update failed")):
            update_data = SubscriptionUpdate(proration_behavior="none")
            result = billing_service.update_subscription("sub_test123", update_data)
            assert result.success is False
            assert "Update failed" in result.error_message


class TestSubscriptionErrorPaths:
    """Tests for subscription error handling paths."""

    def test_get_subscription_other_error(self, billing_service):
        """Test get_subscription re-raises non-NotFound errors."""
        with patch.object(billing_service.client, "get_subscription", side_effect=Exception("Network error")):
            with pytest.raises(Exception, match="Network error"):
                billing_service.get_subscription("sub_123")

    def test_cancel_subscription_failure(self, billing_service):
        """Test cancel subscription failure."""
        with patch.object(billing_service.client, "cancel_subscription", side_effect=Exception("Cancel failed")):
            result = billing_service.cancel_subscription("sub_test123")
            assert result.success is False
            assert "Cancel failed" in result.error_message

    def test_resume_subscription_failure(self, billing_service):
        """Test resume subscription failure."""
        with patch.object(billing_service.client, "resume_subscription", side_effect=Exception("Resume failed")):
            result = billing_service.resume_subscription("sub_test123")
            assert result.success is False
            assert "Resume failed" in result.error_message


class TestGetPlanOperations:
    """Tests for get_plan operation."""

    def test_get_plan_success(self, billing_service, mock_stripe_product, mock_stripe_price):
        """Test getting a specific plan."""
        mock_stripe_product.created = int(datetime.now(timezone.utc).timestamp())
        mock_stripe_product.updated = int(datetime.now(timezone.utc).timestamp())

        with patch.object(billing_service.client, "get_product", return_value=mock_stripe_product):
            with patch.object(billing_service.client, "list_prices", return_value=[mock_stripe_price]):
                plan = billing_service.get_plan("prod_test123")
                assert plan is not None
                assert plan.stripe_product_id == "prod_test123"

    def test_get_plan_not_found(self, billing_service):
        """Test get_plan raises PlanNotFoundError."""
        from bizstats_stripe_billing.exceptions import PlanNotFoundError

        with patch.object(billing_service.client, "get_product", side_effect=Exception("No such product")):
            with pytest.raises(PlanNotFoundError):
                billing_service.get_plan("prod_123")

    def test_get_plan_other_error(self, billing_service):
        """Test get_plan re-raises non-NotFound errors."""
        with patch.object(billing_service.client, "get_product", side_effect=Exception("Network error")):
            with pytest.raises(Exception, match="Network error"):
                billing_service.get_plan("prod_123")


class TestSetDefaultPaymentMethod:
    """Tests for set_default_payment_method operation."""

    def test_set_default_payment_method_success(self, billing_service, mock_stripe_customer):
        """Test setting default payment method."""
        mock_stripe_customer.phone = None
        mock_stripe_customer.currency = "usd"

        with patch.object(billing_service.client, "set_default_payment_method", return_value=mock_stripe_customer):
            customer = billing_service.set_default_payment_method(
                stripe_customer_id="cus_test123",
                payment_method_id="pm_test123",
            )
            assert customer.stripe_customer_id == "cus_test123"


class TestSubscriptionHelperMethods:
    """Tests for subscription helper conversion methods."""

    def test_stripe_subscription_to_model_yearly(self, billing_service):
        """Test converting yearly subscription."""
        mock_sub = Mock()
        mock_sub.id = "sub_test123"
        mock_sub.customer = "cus_test123"
        mock_sub.status = "active"
        mock_sub.currency = "usd"
        mock_sub.current_period_start = int(datetime.now(timezone.utc).timestamp())
        mock_sub.current_period_end = int(datetime.now(timezone.utc).timestamp())
        mock_sub.trial_start = None
        mock_sub.trial_end = None
        mock_sub.cancel_at_period_end = False
        mock_sub.canceled_at = None
        mock_sub.ended_at = None
        mock_sub.metadata = {}
        mock_sub.created = int(datetime.now(timezone.utc).timestamp())

        # Setup yearly price
        mock_price = Mock()
        mock_price.recurring = Mock()
        mock_price.recurring.interval = "year"
        mock_price.unit_amount = 29900
        mock_price.product = "prod_test123"
        mock_price.nickname = "Yearly Plan"

        mock_item = Mock()
        mock_item.price = mock_price

        mock_sub.items = Mock()
        mock_sub.items.data = [mock_item]

        subscription = billing_service._stripe_subscription_to_model(mock_sub)
        assert subscription.billing_period == BillingPeriod.YEARLY

    def test_stripe_subscription_to_model_empty_items(self, billing_service):
        """Test converting subscription with empty items."""
        mock_sub = Mock()
        mock_sub.id = "sub_test123"
        mock_sub.customer = "cus_test123"
        mock_sub.status = "active"
        mock_sub.currency = "usd"
        mock_sub.current_period_start = None
        mock_sub.current_period_end = None
        mock_sub.trial_start = None
        mock_sub.trial_end = None
        mock_sub.cancel_at_period_end = False
        mock_sub.canceled_at = None
        mock_sub.ended_at = None
        mock_sub.metadata = {}
        mock_sub.created = int(datetime.now(timezone.utc).timestamp())

        # Empty items
        mock_sub.items = Mock()
        mock_sub.items.data = []

        subscription = billing_service._stripe_subscription_to_model(mock_sub)
        assert subscription.plan_id == ""
        assert subscription.plan_name == "Unknown"


class TestPlanPriceConversion:
    """Tests for plan price conversion."""

    def test_stripe_product_to_plan_yearly_price(self, billing_service, mock_stripe_product):
        """Test converting product with yearly price."""
        mock_stripe_product.created = int(datetime.now(timezone.utc).timestamp())
        mock_stripe_product.updated = int(datetime.now(timezone.utc).timestamp())

        # Create yearly price
        mock_price = Mock()
        mock_price.id = "price_yearly"
        mock_price.unit_amount = 29900
        mock_price.currency = "usd"
        mock_price.recurring = Mock()
        mock_price.recurring.interval = "year"
        mock_price.recurring.interval_count = 1

        plan = billing_service._stripe_product_to_plan(mock_stripe_product, [mock_price])
        assert plan.yearly_price == 29900

    def test_stripe_product_to_plan_no_metadata(self, billing_service):
        """Test converting product without metadata."""
        mock_product = Mock()
        mock_product.id = "prod_test123"
        mock_product.name = "Test Plan"
        mock_product.description = "Test description"
        mock_product.active = True
        mock_product.metadata = None
        mock_product.created = int(datetime.now(timezone.utc).timestamp())
        mock_product.updated = int(datetime.now(timezone.utc).timestamp())
        mock_product.marketing_features = []

        plan = billing_service._stripe_product_to_plan(mock_product, [])
        assert plan.id == "prod_test123"
        assert plan.is_popular is False


class TestPaymentMethodConversion:
    """Tests for payment method conversion."""

    def test_payment_method_without_card(self, billing_service):
        """Test converting payment method without card details."""
        mock_method = Mock()
        mock_method.id = "pm_test123"
        mock_method.type = "sepa_debit"
        mock_method.card = None
        mock_method.created = int(datetime.now(timezone.utc).timestamp())

        payment_method = billing_service._stripe_payment_method_to_model(mock_method)
        assert payment_method.id == "pm_test123"
        assert payment_method.type == "sepa_debit"
