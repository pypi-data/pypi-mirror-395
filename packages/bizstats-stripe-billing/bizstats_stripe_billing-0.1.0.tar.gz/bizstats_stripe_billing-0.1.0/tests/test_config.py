"""
Tests for configuration module.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

import os
import pytest
from unittest.mock import patch

from bizstats_stripe_billing import (
    StripeConfig,
    get_config,
    configure,
    get_test_card,
    TEST_CARDS,
)


class TestStripeConfig:
    """Tests for StripeConfig class."""

    def test_create_config_with_defaults(self):
        """Test creating config uses default values."""
        # StripeConfig has defaults for all fields
        config = StripeConfig()
        assert config.api_version == "2024-11-20"
        assert config.max_retries == 3
        assert config.retry_delay == 1.0
        assert config.webhook_tolerance == 300
        assert config.default_currency == "usd"

    def test_create_config_from_env(self):
        """Test creating config from environment variables."""
        env_vars = {
            "STRIPE_SECRET_KEY": "sk_test_custom_123",
            "STRIPE_WEBHOOK_SECRET": "whsec_custom_test",
            "STRIPE_PUBLISHABLE_KEY": "pk_test_custom_123",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            config = StripeConfig()
            assert config.secret_key == "sk_test_custom_123"
            assert config.webhook_secret == "whsec_custom_test"
            assert config.publishable_key == "pk_test_custom_123"

    def test_config_test_mode_detection(self):
        """Test detection of test mode from secret key."""
        env_vars = {
            "STRIPE_SECRET_KEY": "sk_test_123",
            "STRIPE_WEBHOOK_SECRET": "whsec_test",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            config = StripeConfig()
            assert config.is_test_mode is True

        env_vars_live = {
            "STRIPE_SECRET_KEY": "sk_live_123",
            "STRIPE_WEBHOOK_SECRET": "whsec_live",
        }
        with patch.dict(os.environ, env_vars_live, clear=False):
            live_config = StripeConfig()
            assert live_config.is_test_mode is False

    def test_config_api_version_property(self):
        """Test api_version is a property."""
        config = StripeConfig()
        assert config.api_version == "2024-11-20"

    def test_config_default_currency(self):
        """Test default currency configuration."""
        config = StripeConfig()
        assert config.default_currency == "usd"

    def test_config_supported_currencies(self):
        """Test supported currencies list."""
        config = StripeConfig()
        assert "usd" in config.supported_currencies
        assert "eur" in config.supported_currencies

    def test_config_parse_currencies_from_string(self):
        """Test parsing currencies from comma-separated string."""
        env_vars = {
            "STRIPE_SECRET_KEY": "sk_test_123",
            "STRIPE_WEBHOOK_SECRET": "whsec_test",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            config = StripeConfig(
                supported_currencies="USD, EUR, GBP",
            )
            assert config.supported_currencies == ["usd", "eur", "gbp"]

    def test_config_urls_have_defaults(self):
        """Test URL configurations have sensible defaults."""
        config = StripeConfig()
        assert "success" in config.success_url
        assert "cancel" in config.cancel_url
        assert "billing" in config.portal_return_url


class TestGetConfig:
    """Tests for get_config function."""

    def test_get_config_returns_singleton(self):
        """Test that get_config returns cached config."""
        env_vars = {
            "STRIPE_SECRET_KEY": "sk_test_singleton",
            "STRIPE_WEBHOOK_SECRET": "whsec_singleton",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            # Clear any cached config first
            import bizstats_stripe_billing.config as config_module
            config_module._config = None

            config1 = get_config()
            config2 = get_config()
            assert config1 is config2


class TestConfigure:
    """Tests for configure function."""

    def test_configure_sets_global_config(self):
        """Test that configure sets the global config."""
        import bizstats_stripe_billing.config as config_module

        custom_config = StripeConfig()
        configure(custom_config)

        assert config_module._config is custom_config
        assert get_config() is custom_config


class TestTestCards:
    """Tests for test card constants."""

    def test_test_cards_exist(self):
        """Test that TEST_CARDS dictionary has expected cards."""
        assert "visa_success" in TEST_CARDS
        assert "visa_declined" in TEST_CARDS
        assert "insufficient_funds" in TEST_CARDS
        assert "3d_secure_required" in TEST_CARDS

    def test_get_test_card(self):
        """Test get_test_card function."""
        success_card = get_test_card("visa_success")
        assert success_card == "4242424242424242"

        decline_card = get_test_card("visa_declined")
        assert decline_card == "4000000000000002"

    def test_get_test_card_default(self):
        """Test get_test_card returns default for unknown type."""
        card = get_test_card("nonexistent")
        assert card == TEST_CARDS["visa_success"]

    def test_test_cards_are_strings(self):
        """Test that all test cards are string values."""
        for name, number in TEST_CARDS.items():
            assert isinstance(number, str)
            assert len(number) >= 15  # Cards can be 15-16 digits
            assert number.isdigit()

    def test_all_test_card_types(self):
        """Test all available test card types."""
        expected_cards = [
            "visa_success",
            "visa_declined",
            "mastercard_success",
            "amex_success",
            "3d_secure_required",
            "insufficient_funds",
            "expired_card",
            "processing_error",
        ]
        for card_type in expected_cards:
            assert card_type in TEST_CARDS
            assert len(TEST_CARDS[card_type]) >= 15
