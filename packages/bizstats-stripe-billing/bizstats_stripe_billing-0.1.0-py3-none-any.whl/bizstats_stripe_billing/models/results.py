"""
Operation result models.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

from datetime import datetime
from typing import Optional, Generic, TypeVar, Any, Dict
from pydantic import BaseModel, Field

T = TypeVar("T")


class OperationResult(BaseModel, Generic[T]):
    """Generic operation result."""

    success: bool
    data: Optional[T] = None
    error_message: Optional[str] = None
    error_code: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def ok(cls, data: T = None, **metadata) -> "OperationResult[T]":
        """Create a successful result."""
        return cls(success=True, data=data, metadata=metadata)

    @classmethod
    def error(
        cls, message: str, code: Optional[str] = None, **metadata
    ) -> "OperationResult[T]":
        """Create an error result."""
        return cls(
            success=False,
            error_message=message,
            error_code=code,
            metadata=metadata,
        )


class CustomerResult(BaseModel):
    """Result of customer operations."""

    success: bool
    customer_id: Optional[str] = None
    stripe_customer_id: Optional[str] = None
    error_message: Optional[str] = None

    @classmethod
    def ok(cls, customer_id: str, stripe_customer_id: str) -> "CustomerResult":
        """Create a successful result."""
        return cls(
            success=True,
            customer_id=customer_id,
            stripe_customer_id=stripe_customer_id,
        )

    @classmethod
    def error(cls, message: str) -> "CustomerResult":
        """Create an error result."""
        return cls(success=False, error_message=message)


class SubscriptionResult(BaseModel):
    """Result of subscription operations."""

    success: bool
    subscription_id: Optional[str] = None
    stripe_subscription_id: Optional[str] = None
    client_secret: Optional[str] = None
    error_message: Optional[str] = None
    trial_end: Optional[datetime] = None
    # For upgrades/downgrades
    proration_amount: Optional[int] = None

    @classmethod
    def ok(
        cls,
        subscription_id: str,
        stripe_subscription_id: str,
        client_secret: Optional[str] = None,
        trial_end: Optional[datetime] = None,
    ) -> "SubscriptionResult":
        """Create a successful result."""
        return cls(
            success=True,
            subscription_id=subscription_id,
            stripe_subscription_id=stripe_subscription_id,
            client_secret=client_secret,
            trial_end=trial_end,
        )

    @classmethod
    def error(cls, message: str) -> "SubscriptionResult":
        """Create an error result."""
        return cls(success=False, error_message=message)


class CheckoutResult(BaseModel):
    """Result of checkout session creation."""

    success: bool
    session_id: Optional[str] = None
    checkout_url: Optional[str] = None
    error_message: Optional[str] = None

    @classmethod
    def ok(cls, session_id: str, checkout_url: str) -> "CheckoutResult":
        """Create a successful result."""
        return cls(
            success=True,
            session_id=session_id,
            checkout_url=checkout_url,
        )

    @classmethod
    def error(cls, message: str) -> "CheckoutResult":
        """Create an error result."""
        return cls(success=False, error_message=message)


class PortalResult(BaseModel):
    """Result of billing portal session creation."""

    success: bool
    session_id: Optional[str] = None
    portal_url: Optional[str] = None
    error_message: Optional[str] = None

    @classmethod
    def ok(cls, session_id: str, portal_url: str) -> "PortalResult":
        """Create a successful result."""
        return cls(
            success=True,
            session_id=session_id,
            portal_url=portal_url,
        )

    @classmethod
    def error(cls, message: str) -> "PortalResult":
        """Create an error result."""
        return cls(success=False, error_message=message)


class WebhookResult(BaseModel):
    """Result of webhook processing."""

    success: bool
    event_id: Optional[str] = None
    event_type: Optional[str] = None
    processed: bool = False
    error_message: Optional[str] = None
    # Actions taken
    actions: list[str] = Field(default_factory=list)

    @classmethod
    def ok(
        cls,
        event_id: str,
        event_type: str,
        actions: Optional[list[str]] = None,
    ) -> "WebhookResult":
        """Create a successful result."""
        return cls(
            success=True,
            event_id=event_id,
            event_type=event_type,
            processed=True,
            actions=actions or [],
        )

    @classmethod
    def error(
        cls,
        message: str,
        event_id: Optional[str] = None,
        event_type: Optional[str] = None,
    ) -> "WebhookResult":
        """Create an error result."""
        return cls(
            success=False,
            error_message=message,
            event_id=event_id,
            event_type=event_type,
        )

    @classmethod
    def skipped(
        cls, event_id: str, event_type: str, reason: str
    ) -> "WebhookResult":
        """Create a skipped result (event already processed)."""
        return cls(
            success=True,
            event_id=event_id,
            event_type=event_type,
            processed=False,
            actions=[f"Skipped: {reason}"],
        )
