"""Billing and subscription models."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class PlanLimits(BaseModel):
    """Usage limits for a plan.

    Use -1 for unlimited limits.
    """

    queries_per_month: int = Field(default=0, ge=-1, description="Queries per month (-1 for unlimited)")
    indexes_per_month: int = Field(default=0, ge=-1, description="Indexes per month (-1 for unlimited)")
    storage_mb: int = Field(default=0, ge=-1, description="Storage limit in MB (-1 for unlimited)")
    requests_per_minute: int = Field(default=60, ge=1, description="Rate limit per minute")
    max_api_keys: int = Field(default=1, ge=1, description="Maximum API keys")
    custom_controls: int = Field(
        default=0,
        ge=-1,
        description="Maximum number of custom compliance controls (-1 for unlimited)",
    )


class PlanFeatures(BaseModel):
    """Features included in a plan."""

    compliance_queries: bool = Field(default=True, description="Access to compliance queries")
    knowledge_queries: bool = Field(default=True, description="Access to knowledge queries")
    repository_indexing: bool = Field(default=False, description="Repository indexing")
    document_indexing: bool = Field(default=False, description="Document indexing")
    custom_indexes: bool = Field(default=False, description="Custom user indexes")
    priority_support: bool = Field(default=False, description="Priority support")
    sso: bool = Field(default=False, description="Single sign-on")
    api_access: bool = Field(default=True, description="API access")


class SubscriptionPlan(BaseModel):
    """Subscription plan definition."""

    plan_id: str = Field(..., description="Plan ID (professional, team, enterprise)")
    name: str = Field(..., description="Plan name")
    description: str = Field(..., description="Plan description")
    monthly_price: float = Field(default=0.0, ge=0.0, description="Monthly price in USD")
    annual_price: float = Field(default=0.0, ge=0.0, description="Annual price in USD")
    stripe_monthly_price_id: str | None = Field(default=None, description="Stripe monthly price ID")
    stripe_annual_price_id: str | None = Field(default=None, description="Stripe annual price ID")
    limits: PlanLimits = Field(..., description="Plan limits")
    features: PlanFeatures = Field(..., description="Plan features")
    popular: bool = Field(default=False, description="Is this a popular plan")
    is_active: bool = Field(default=True, description="Is this plan active and available for new signups")


class SubscriptionStatus(BaseModel):
    """Current subscription status."""

    plan_id: str = Field(..., description="Current plan ID")
    status: str = Field(..., description="Subscription status (active, trialing, past_due, canceled)")
    current_period_start: datetime = Field(..., description="Current period start")
    current_period_end: datetime = Field(..., description="Current period end")
    cancel_at_period_end: bool = Field(default=False, description="Will cancel at period end")
    stripe_subscription_id: str | None = Field(default=None, description="Stripe subscription ID")
    stripe_customer_id: str | None = Field(default=None, description="Stripe customer ID")


class CheckoutSessionRequest(BaseModel):
    """Request to create checkout session."""

    price_id: str = Field(..., description="Stripe price ID")
    success_url: str = Field(..., description="Success redirect URL")
    cancel_url: str = Field(..., description="Cancel redirect URL")


class CheckoutSessionResponse(BaseModel):
    """Checkout session response."""

    session_id: str = Field(..., description="Stripe checkout session ID")
    url: str = Field(..., description="Checkout URL")
    publishable_key: str = Field(..., description="Stripe publishable key")


class CustomerPortalRequest(BaseModel):
    """Request to create customer portal session."""

    return_url: str = Field(..., description="Return URL after portal")


class CustomerPortalResponse(BaseModel):
    """Customer portal session response."""

    url: str = Field(..., description="Portal URL")

