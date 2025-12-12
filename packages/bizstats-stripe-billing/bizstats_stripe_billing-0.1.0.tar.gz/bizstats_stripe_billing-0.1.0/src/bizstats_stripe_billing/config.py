"""
Stripe configuration settings.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

import os
from typing import List, Optional, Dict, Any
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class StripeConfig(BaseSettings):
    """Stripe configuration settings."""

    # API Keys
    publishable_key: str = Field(
        default="pk_test_default",
        alias="STRIPE_PUBLISHABLE_KEY",
        description="Stripe publishable key for frontend",
    )
    secret_key: str = Field(
        default="sk_test_default",
        alias="STRIPE_SECRET_KEY",
        description="Stripe secret key for backend operations",
    )

    # Webhook Configuration
    webhook_secret: str = Field(
        default="whsec_test_default",
        alias="STRIPE_WEBHOOK_SECRET",
        description="Stripe webhook endpoint secret for signature verification",
    )
    webhook_tolerance: int = Field(
        default=300,
        alias="STRIPE_WEBHOOK_TOLERANCE",
        description="Webhook signature tolerance in seconds",
    )

    # Currency and Locale
    default_currency: str = Field(
        default="usd",
        alias="STRIPE_DEFAULT_CURRENCY",
        description="Default currency for payments",
    )
    supported_currencies: List[str] = Field(
        default=["usd", "eur", "gbp", "cad", "aud"],
        description="List of supported currencies",
    )

    # Payment Configuration
    success_url: str = Field(
        default="http://localhost:3000/billing/success",
        alias="STRIPE_SUCCESS_URL",
        description="URL to redirect after successful payment",
    )
    cancel_url: str = Field(
        default="http://localhost:3000/billing/cancel",
        alias="STRIPE_CANCEL_URL",
        description="URL to redirect after cancelled payment",
    )

    # Billing Portal
    portal_return_url: str = Field(
        default="http://localhost:3000/billing",
        alias="STRIPE_PORTAL_RETURN_URL",
        description="URL to redirect after billing portal",
    )

    # Development/Testing
    test_mode: bool = Field(
        default=True,
        alias="STRIPE_TEST_MODE",
        description="Enable test mode for development",
    )

    # Security Settings
    require_3d_secure: bool = Field(
        default=True,
        alias="STRIPE_REQUIRE_3D_SECURE",
        description="Require 3D Secure authentication",
    )
    automatic_tax: bool = Field(
        default=False,
        alias="STRIPE_AUTOMATIC_TAX",
        description="Enable automatic tax calculation",
    )

    # Retry Configuration
    max_retries: int = Field(
        default=3,
        alias="STRIPE_MAX_RETRIES",
        description="Maximum retry attempts for API calls",
    )
    retry_delay: float = Field(
        default=1.0,
        alias="STRIPE_RETRY_DELAY",
        description="Base delay between retries in seconds",
    )

    # Business Information
    business_name: str = Field(
        default="BizStats",
        alias="STRIPE_BUSINESS_NAME",
        description="Business name for invoices",
    )
    support_email: str = Field(
        default="support@bizstats.ai",
        alias="STRIPE_SUPPORT_EMAIL",
        description="Support email for customers",
    )

    @field_validator("supported_currencies", mode="before")
    @classmethod
    def parse_currencies(cls, v):
        """Parse currencies from string or list."""
        if isinstance(v, str):
            return [c.strip().lower() for c in v.split(",")]
        return [c.lower() for c in v]

    @field_validator("default_currency")
    @classmethod
    def validate_currency(cls, v):
        """Validate currency code."""
        return v.lower()

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

    @property
    def is_test_mode(self) -> bool:
        """Check if using test keys."""
        return self.secret_key.startswith("sk_test_")

    @property
    def api_version(self) -> str:
        """Get recommended Stripe API version."""
        return "2024-11-20"


# Singleton instance
_config: Optional[StripeConfig] = None


def get_config() -> StripeConfig:
    """Get the global Stripe configuration instance."""
    global _config
    if _config is None:
        _config = StripeConfig()
    return _config


def configure(config: StripeConfig) -> None:
    """Set the global Stripe configuration."""
    global _config
    _config = config


# Test card numbers for development
TEST_CARDS = {
    "visa_success": "4242424242424242",
    "visa_declined": "4000000000000002",
    "mastercard_success": "5555555555554444",
    "amex_success": "378282246310005",
    "3d_secure_required": "4000002500003155",
    "insufficient_funds": "4000000000009995",
    "expired_card": "4000000000000069",
    "processing_error": "4000000000000119",
}


def get_test_card(card_type: str = "visa_success") -> str:
    """Get a test card number for development."""
    return TEST_CARDS.get(card_type, TEST_CARDS["visa_success"])
