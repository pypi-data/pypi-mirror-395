"""
Tests for Stripe client module.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import stripe

from bizstats_stripe_billing import (
    StripeClient,
    get_client,
    StripeConfig,
)
from bizstats_stripe_billing.exceptions import (
    StripeAPIError,
    StripeAuthenticationError,
    StripeRateLimitError,
    StripeValidationError,
)


class TestStripeClient:
    """Tests for StripeClient class."""

    def test_client_initialization(self, test_config):
        """Test client initializes with config."""
        with patch("stripe.api_key"):
            with patch("stripe.api_version"):
                client = StripeClient(test_config)
                assert client.config == test_config

    def test_client_sets_api_key(self, test_config):
        """Test client sets Stripe API key."""
        with patch("stripe.api_key"):
            with patch("stripe.api_version"):
                client = StripeClient(test_config)
                assert stripe.api_key == test_config.secret_key


class TestCustomerOperations:
    """Tests for customer operations."""

    def test_create_customer(self, stripe_client, mock_stripe_customer):
        """Test creating a customer."""
        with patch.object(stripe.Customer, "create", return_value=mock_stripe_customer):
            result = stripe_client.create_customer(
                email="test@example.com",
                name="Test User",
                metadata={"org_id": "org_123"},
            )
            assert result.id == "cus_test123"
            assert result.email == "test@example.com"

    def test_create_customer_api_error(self, stripe_client):
        """Test customer creation handles API errors."""
        error = stripe.APIError("API Error", http_status=500)
        with patch.object(stripe.Customer, "create", side_effect=error):
            with pytest.raises(StripeAPIError):
                stripe_client.create_customer(email="test@example.com")

    def test_get_customer(self, stripe_client, mock_stripe_customer):
        """Test retrieving a customer."""
        with patch.object(stripe.Customer, "retrieve", return_value=mock_stripe_customer):
            result = stripe_client.get_customer("cus_test123")
            assert result.id == "cus_test123"

    def test_get_customer_not_found(self, stripe_client):
        """Test customer not found error."""
        error = stripe.InvalidRequestError(
            "No such customer",
            param="customer",
            http_status=404,
        )
        with patch.object(stripe.Customer, "retrieve", side_effect=error):
            with pytest.raises(StripeValidationError):
                stripe_client.get_customer("cus_nonexistent")

    def test_update_customer(self, stripe_client, mock_stripe_customer):
        """Test updating a customer."""
        mock_stripe_customer.name = "Updated Name"
        with patch.object(stripe.Customer, "modify", return_value=mock_stripe_customer):
            result = stripe_client.update_customer(
                "cus_test123",
                name="Updated Name",
            )
            assert result.name == "Updated Name"

    def test_delete_customer(self, stripe_client):
        """Test deleting a customer."""
        with patch.object(stripe.Customer, "delete", return_value=None):
            result = stripe_client.delete_customer("cus_test123")
            assert result is True


class TestSubscriptionOperations:
    """Tests for subscription operations."""

    def test_create_subscription(self, stripe_client, mock_stripe_subscription):
        """Test creating a subscription."""
        with patch.object(stripe.Subscription, "create", return_value=mock_stripe_subscription):
            result = stripe_client.create_subscription(
                customer_id="cus_test123",
                price_id="price_test123",
            )
            assert result.id == "sub_test123"
            assert result.status == "active"

    def test_create_subscription_with_trial(self, stripe_client, mock_stripe_subscription):
        """Test creating subscription with trial."""
        with patch.object(stripe.Subscription, "create", return_value=mock_stripe_subscription):
            result = stripe_client.create_subscription(
                customer_id="cus_test123",
                price_id="price_test123",
                trial_days=14,
            )
            assert result is not None

    def test_get_subscription(self, stripe_client, mock_stripe_subscription):
        """Test retrieving a subscription."""
        with patch.object(stripe.Subscription, "retrieve", return_value=mock_stripe_subscription):
            result = stripe_client.get_subscription("sub_test123")
            assert result.id == "sub_test123"

    def test_get_subscription_not_found(self, stripe_client):
        """Test subscription not found error."""
        error = stripe.InvalidRequestError(
            "No such subscription",
            param="subscription",
            http_status=404,
        )
        with patch.object(stripe.Subscription, "retrieve", side_effect=error):
            with pytest.raises(StripeValidationError):
                stripe_client.get_subscription("sub_nonexistent")

    def test_update_subscription(self, stripe_client, mock_stripe_subscription):
        """Test updating a subscription."""
        with patch.object(stripe.Subscription, "modify", return_value=mock_stripe_subscription):
            result = stripe_client.update_subscription(
                "sub_test123",
                cancel_at_period_end=True,
            )
            assert result is not None

    def test_cancel_subscription_at_period_end(self, stripe_client, mock_stripe_subscription):
        """Test canceling a subscription at period end."""
        mock_stripe_subscription.cancel_at_period_end = True
        with patch.object(stripe.Subscription, "modify", return_value=mock_stripe_subscription):
            result = stripe_client.cancel_subscription("sub_test123", at_period_end=True)
            assert result.cancel_at_period_end is True

    def test_cancel_subscription_immediate(self, stripe_client, mock_stripe_subscription):
        """Test immediate subscription cancellation."""
        mock_stripe_subscription.status = "canceled"
        with patch.object(stripe.Subscription, "cancel", return_value=mock_stripe_subscription):
            result = stripe_client.cancel_subscription("sub_test123", at_period_end=False)
            assert result.status == "canceled"

    def test_resume_subscription(self, stripe_client, mock_stripe_subscription):
        """Test resuming a canceled subscription."""
        mock_stripe_subscription.cancel_at_period_end = False
        with patch.object(stripe.Subscription, "modify", return_value=mock_stripe_subscription):
            result = stripe_client.resume_subscription("sub_test123")
            assert result.cancel_at_period_end is False


class TestCheckoutOperations:
    """Tests for checkout operations."""

    def test_create_checkout_session(self, stripe_client, mock_stripe_checkout_session):
        """Test creating a checkout session."""
        with patch.object(stripe.checkout.Session, "create", return_value=mock_stripe_checkout_session):
            result = stripe_client.create_checkout_session(
                price_id="price_test123",
                success_url="https://example.com/success",
                cancel_url="https://example.com/cancel",
                customer_id="cus_test123",
            )
            assert result.id == "cs_test123"
            assert result.url is not None

    def test_create_checkout_session_payment_mode(self, stripe_client, mock_stripe_checkout_session):
        """Test creating checkout session in payment mode."""
        mock_stripe_checkout_session.mode = "payment"
        with patch.object(stripe.checkout.Session, "create", return_value=mock_stripe_checkout_session):
            result = stripe_client.create_checkout_session(
                price_id="price_test123",
                success_url="https://example.com/success",
                cancel_url="https://example.com/cancel",
                mode="payment",
            )
            assert result is not None

    def test_get_checkout_session(self, stripe_client, mock_stripe_checkout_session):
        """Test retrieving a checkout session."""
        with patch.object(stripe.checkout.Session, "retrieve", return_value=mock_stripe_checkout_session):
            result = stripe_client.get_checkout_session("cs_test123")
            assert result.id == "cs_test123"


class TestBillingPortalOperations:
    """Tests for billing portal operations."""

    def test_create_portal_session(self, stripe_client, mock_stripe_portal_session):
        """Test creating a billing portal session."""
        with patch.object(stripe.billing_portal.Session, "create", return_value=mock_stripe_portal_session):
            result = stripe_client.create_portal_session(
                customer_id="cus_test123",
                return_url="https://example.com/account",
            )
            assert result.id == "bps_test123"
            assert result.url is not None


class TestProductOperations:
    """Tests for product/price operations."""

    def test_get_product(self, stripe_client, mock_stripe_product):
        """Test retrieving a product."""
        with patch.object(stripe.Product, "retrieve", return_value=mock_stripe_product):
            result = stripe_client.get_product("prod_test123")
            assert result.id == "prod_test123"
            assert result.name == "Pro Plan"

    def test_list_products(self, stripe_client, mock_stripe_product):
        """Test listing products."""
        mock_list = Mock()
        mock_list.auto_paging_iter = Mock(return_value=iter([mock_stripe_product]))
        with patch.object(stripe.Product, "list", return_value=mock_list):
            result = stripe_client.list_products(active=True)
            assert len(result) == 1

    def test_get_price(self, stripe_client, mock_stripe_price):
        """Test retrieving a price."""
        with patch.object(stripe.Price, "retrieve", return_value=mock_stripe_price):
            result = stripe_client.get_price("price_test123")
            assert result.id == "price_test123"
            assert result.unit_amount == 2900

    def test_list_prices(self, stripe_client, mock_stripe_price):
        """Test listing prices."""
        mock_list = Mock()
        mock_list.auto_paging_iter = Mock(return_value=iter([mock_stripe_price]))
        with patch.object(stripe.Price, "list", return_value=mock_list):
            result = stripe_client.list_prices(product_id="prod_test123")
            assert len(result) == 1


class TestInvoiceOperations:
    """Tests for invoice operations."""

    def test_get_invoice(self, stripe_client, mock_stripe_invoice):
        """Test retrieving an invoice."""
        with patch.object(stripe.Invoice, "retrieve", return_value=mock_stripe_invoice):
            result = stripe_client.get_invoice("in_test123")
            assert result.id == "in_test123"

    def test_list_invoices(self, stripe_client, mock_stripe_invoice):
        """Test listing invoices."""
        mock_list = Mock()
        mock_list.data = [mock_stripe_invoice]
        with patch.object(stripe.Invoice, "list", return_value=mock_list):
            result = stripe_client.list_invoices(customer_id="cus_test123")
            assert len(result) == 1


class TestWebhookOperations:
    """Tests for webhook operations."""

    def test_verify_webhook_signature(self, stripe_client, mock_stripe_event):
        """Test verifying webhook signature."""
        with patch.object(stripe.Webhook, "construct_event", return_value=mock_stripe_event):
            result = stripe_client.verify_webhook_signature(
                payload=b'{"test": "data"}',
                signature="t=123,v1=abc",
            )
            assert result.id == "evt_test123"

    def test_verify_webhook_signature_invalid(self, stripe_client):
        """Test webhook signature verification failure."""
        error = stripe.SignatureVerificationError(
            "Invalid signature",
            sig_header="invalid",
        )
        with patch.object(stripe.Webhook, "construct_event", side_effect=error):
            with pytest.raises(StripeValidationError):
                stripe_client.verify_webhook_signature(
                    payload=b'{"test": "data"}',
                    signature="invalid",
                )


class TestUsageOperations:
    """Tests for usage-based billing operations."""

    def test_create_usage_record(self, stripe_client):
        """Test creating a usage record."""
        mock_record = Mock()
        mock_record.id = "mbur_test123"
        mock_record.quantity = 100
        mock_record.subscription_item = "si_test123"

        # Stripe SDK 7.0+ changed how usage records are created
        # Mock the internal method that calls the API
        with patch(
            "bizstats_stripe_billing.client.stripe.SubscriptionItem.create_usage_record",
            return_value=mock_record,
            create=True,
        ):
            result = stripe_client.create_usage_record(
                subscription_item_id="si_test123",
                quantity=100,
            )
            assert result.quantity == 100


class TestPaymentMethodOperations:
    """Tests for payment method operations."""

    def test_list_payment_methods(self, stripe_client):
        """Test listing payment methods."""
        mock_method = Mock()
        mock_method.id = "pm_test123"
        mock_method.type = "card"

        mock_list = Mock()
        mock_list.data = [mock_method]

        with patch.object(stripe.PaymentMethod, "list", return_value=mock_list):
            result = stripe_client.list_payment_methods(
                customer_id="cus_test123",
            )
            assert len(result) == 1
            assert result[0].id == "pm_test123"

    def test_attach_payment_method(self, stripe_client):
        """Test attaching a payment method."""
        mock_method = Mock()
        mock_method.id = "pm_test123"
        mock_method.customer = "cus_test123"

        with patch.object(stripe.PaymentMethod, "attach", return_value=mock_method):
            result = stripe_client.attach_payment_method(
                payment_method_id="pm_test123",
                customer_id="cus_test123",
            )
            assert result.id == "pm_test123"

    def test_set_default_payment_method(self, stripe_client, mock_stripe_customer):
        """Test setting default payment method."""
        with patch.object(stripe.Customer, "modify", return_value=mock_stripe_customer):
            result = stripe_client.set_default_payment_method(
                customer_id="cus_test123",
                payment_method_id="pm_test123",
            )
            assert result is not None


class TestErrorHandling:
    """Tests for error handling."""

    def test_authentication_error(self, stripe_client):
        """Test handling authentication errors."""
        error = stripe.AuthenticationError("Invalid API key")
        with patch.object(stripe.Customer, "create", side_effect=error):
            with pytest.raises(StripeAuthenticationError):
                stripe_client.create_customer(email="test@example.com")

    def test_rate_limit_error(self, stripe_client):
        """Test handling rate limit errors."""
        error = stripe.RateLimitError("Too many requests")
        with patch.object(stripe.Customer, "create", side_effect=error):
            with pytest.raises(StripeRateLimitError):
                stripe_client.create_customer(email="test@example.com")

    def test_generic_stripe_error(self, stripe_client):
        """Test handling generic Stripe errors."""
        error = stripe.StripeError("Generic error")
        with patch.object(stripe.Customer, "create", side_effect=error):
            with pytest.raises(StripeAPIError):
                stripe_client.create_customer(email="test@example.com")

    def test_card_error(self, stripe_client):
        """Test handling card errors."""
        error = stripe.CardError(
            message="Card declined",
            param="card",
            code="card_declined",
        )
        with patch.object(stripe.Customer, "create", side_effect=error):
            with pytest.raises(StripeValidationError):
                stripe_client.create_customer(email="test@example.com")


class TestGetClient:
    """Tests for get_client function."""

    def test_get_client_with_config(self, test_config):
        """Test getting client with config."""
        with patch("stripe.api_key"):
            with patch("stripe.api_version"):
                client = get_client(test_config)
                assert isinstance(client, StripeClient)

    def test_get_client_singleton(self, test_config):
        """Test client singleton behavior."""
        with patch("stripe.api_key"):
            with patch("stripe.api_version"):
                # Clear cached client
                import bizstats_stripe_billing.client as client_module
                client_module._client = None

                client1 = get_client(test_config)
                client2 = get_client()
                assert client1 is client2
