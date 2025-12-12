"""
Tests for exceptions module.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

import pytest
from unittest.mock import MagicMock

from bizstats_stripe_billing.exceptions import (
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


class TestStripeBillingError:
    """Tests for base StripeBillingError."""

    def test_basic_creation(self):
        """Test basic exception creation."""
        error = StripeBillingError("Test error")
        assert str(error) == "Test error"
        assert error.message == "Test error"
        assert error.code is None
        assert error.stripe_error is None

    def test_with_code(self):
        """Test exception with error code."""
        error = StripeBillingError("Test error", code="test_code")
        assert error.code == "test_code"

    def test_with_stripe_error(self):
        """Test exception with Stripe error."""
        mock_stripe_error = MagicMock()
        mock_stripe_error.http_status = 400
        error = StripeBillingError("Test error", stripe_error=mock_stripe_error)
        assert error.stripe_error is mock_stripe_error

    def test_http_status_property(self):
        """Test http_status property with Stripe error."""
        mock_stripe_error = MagicMock()
        mock_stripe_error.http_status = 401
        error = StripeBillingError("Auth error", stripe_error=mock_stripe_error)
        assert error.http_status == 401

    def test_http_status_none_without_stripe_error(self):
        """Test http_status is None without Stripe error."""
        error = StripeBillingError("Test error")
        assert error.http_status is None

    def test_to_dict(self):
        """Test to_dict method."""
        mock_stripe_error = MagicMock()
        mock_stripe_error.http_status = 500
        error = StripeBillingError("Server error", code="server_error", stripe_error=mock_stripe_error)
        result = error.to_dict()
        assert result["error"] == "StripeBillingError"
        assert result["message"] == "Server error"
        assert result["code"] == "server_error"
        assert result["http_status"] == 500


class TestStripeAPIError:
    """Tests for StripeAPIError."""

    def test_creation(self):
        """Test API error creation."""
        error = StripeAPIError("API communication failed")
        assert isinstance(error, StripeBillingError)
        assert error.message == "API communication failed"


class TestStripeAuthenticationError:
    """Tests for StripeAuthenticationError."""

    def test_creation(self):
        """Test authentication error creation."""
        error = StripeAuthenticationError("Invalid API key")
        assert isinstance(error, StripeBillingError)
        assert error.message == "Invalid API key"


class TestStripeRateLimitError:
    """Tests for StripeRateLimitError."""

    def test_creation(self):
        """Test rate limit error creation."""
        error = StripeRateLimitError("Rate limit exceeded")
        assert error.code == "rate_limit_exceeded"
        assert error.retry_after is None

    def test_with_retry_after(self):
        """Test rate limit error with retry_after."""
        error = StripeRateLimitError("Rate limit exceeded", retry_after=30)
        assert error.retry_after == 30


class TestStripeValidationError:
    """Tests for StripeValidationError."""

    def test_creation(self):
        """Test validation error creation."""
        error = StripeValidationError("Invalid email format")
        assert error.message == "Invalid email format"
        assert error.param is None

    def test_with_param(self):
        """Test validation error with parameter."""
        error = StripeValidationError("Invalid email format", param="email", code="invalid_email")
        assert error.param == "email"
        assert error.code == "invalid_email"

    def test_to_dict_with_param(self):
        """Test to_dict includes param field."""
        error = StripeValidationError("Invalid email", param="email")
        result = error.to_dict()
        assert result["param"] == "email"

    def test_to_dict_without_param(self):
        """Test to_dict without param field."""
        error = StripeValidationError("Invalid request")
        result = error.to_dict()
        assert "param" not in result


class TestCustomerNotFoundError:
    """Tests for CustomerNotFoundError."""

    def test_creation(self):
        """Test customer not found error creation."""
        error = CustomerNotFoundError("cus_123")
        assert error.customer_id == "cus_123"
        assert error.code == "customer_not_found"
        assert "cus_123" in error.message


class TestSubscriptionNotFoundError:
    """Tests for SubscriptionNotFoundError."""

    def test_creation(self):
        """Test subscription not found error creation."""
        error = SubscriptionNotFoundError("sub_123")
        assert error.subscription_id == "sub_123"
        assert error.code == "subscription_not_found"
        assert "sub_123" in error.message


class TestPlanNotFoundError:
    """Tests for PlanNotFoundError."""

    def test_creation(self):
        """Test plan not found error creation."""
        error = PlanNotFoundError("plan_123")
        assert error.plan_id == "plan_123"
        assert error.code == "plan_not_found"
        assert "plan_123" in error.message


class TestPriceNotFoundError:
    """Tests for PriceNotFoundError."""

    def test_creation(self):
        """Test price not found error creation."""
        error = PriceNotFoundError("price_123")
        assert error.price_id == "price_123"
        assert error.code == "price_not_found"
        assert "price_123" in error.message


class TestWebhookSignatureError:
    """Tests for WebhookSignatureError."""

    def test_creation(self):
        """Test webhook signature error creation."""
        error = WebhookSignatureError()
        assert error.code == "webhook_signature_invalid"
        assert "Invalid webhook signature" in error.message

    def test_with_custom_message(self):
        """Test webhook signature error with custom message."""
        error = WebhookSignatureError("Signature mismatch")
        assert error.message == "Signature mismatch"


class TestWebhookEventAlreadyProcessedError:
    """Tests for WebhookEventAlreadyProcessedError."""

    def test_creation(self):
        """Test webhook event already processed error creation."""
        error = WebhookEventAlreadyProcessedError("evt_123")
        assert error.event_id == "evt_123"
        assert error.code == "event_already_processed"
        assert "evt_123" in error.message


class TestPaymentFailedError:
    """Tests for PaymentFailedError."""

    def test_creation(self):
        """Test payment failed error creation."""
        error = PaymentFailedError("Payment declined")
        assert error.code == "payment_failed"
        assert error.decline_code is None

    def test_with_decline_code(self):
        """Test payment failed error with decline code."""
        error = PaymentFailedError("Card declined", decline_code="card_declined")
        assert error.decline_code == "card_declined"

    def test_to_dict_with_decline_code(self):
        """Test to_dict includes decline code."""
        error = PaymentFailedError("Card declined", decline_code="insufficient_funds")
        result = error.to_dict()
        assert result["decline_code"] == "insufficient_funds"

    def test_to_dict_without_decline_code(self):
        """Test to_dict without decline code."""
        error = PaymentFailedError("Payment failed")
        result = error.to_dict()
        assert "decline_code" not in result


class TestSubscriptionAlreadyExistsError:
    """Tests for SubscriptionAlreadyExistsError."""

    def test_creation(self):
        """Test subscription already exists error creation."""
        error = SubscriptionAlreadyExistsError("cus_123", "sub_456")
        assert error.customer_id == "cus_123"
        assert error.subscription_id == "sub_456"
        assert error.code == "subscription_already_exists"
        assert "cus_123" in error.message
        assert "sub_456" in error.message


class TestInsufficientPermissionsError:
    """Tests for InsufficientPermissionsError."""

    def test_creation(self):
        """Test insufficient permissions error creation."""
        error = InsufficientPermissionsError()
        assert error.code == "insufficient_permissions"
        assert "Insufficient permissions" in error.message

    def test_with_custom_message(self):
        """Test insufficient permissions error with custom message."""
        error = InsufficientPermissionsError("Cannot modify subscription")
        assert error.message == "Cannot modify subscription"


class TestUsageLimitExceededError:
    """Tests for UsageLimitExceededError."""

    def test_creation(self):
        """Test usage limit exceeded error creation."""
        error = UsageLimitExceededError(
            metric="api_calls",
            current_usage=1500,
            limit=1000,
        )
        assert error.metric == "api_calls"
        assert error.current_usage == 1500
        assert error.limit == 1000
        assert error.code == "usage_limit_exceeded"
        assert "api_calls" in error.message
        assert "1500" in error.message
        assert "1000" in error.message

    def test_to_dict(self):
        """Test to_dict includes usage details."""
        error = UsageLimitExceededError(
            metric="storage_gb",
            current_usage=60,
            limit=50,
        )
        result = error.to_dict()
        assert result["metric"] == "storage_gb"
        assert result["current_usage"] == 60
        assert result["limit"] == 50
