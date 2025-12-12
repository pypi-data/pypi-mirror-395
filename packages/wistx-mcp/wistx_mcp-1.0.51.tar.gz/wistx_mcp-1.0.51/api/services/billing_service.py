"""Billing service with Stripe integration."""

import logging
from typing import Any, Optional

import stripe
from bson import ObjectId

from api.config import settings
from api.database.mongodb import mongodb_manager
from api.exceptions import ValidationError, ExternalServiceError

logger = logging.getLogger(__name__)

stripe.api_key = getattr(settings, "stripe_secret_key", None) or ""


class BillingService:
    """Stripe billing integration service."""

    def __init__(self):
        """Initialize billing service."""
        if not stripe.api_key:
            logger.warning("Stripe API key not configured. Billing features will be disabled.")

    async def create_customer(
        self,
        user_id: str,
        email: str,
        name: Optional[str] = None,
    ) -> dict[str, Any]:
        """Create Stripe customer for user.

        Args:
            user_id: User ID
            email: User email
            name: User name (optional)

        Returns:
            Stripe customer object
        """
        if not stripe.api_key:
            raise ValidationError(
                message="Stripe API key not configured",
                user_message="Billing service is not configured. Please contact support.",
                error_code="STRIPE_NOT_CONFIGURED",
                details={"service": "billing"}
            )

        try:
            customer = stripe.Customer.create(
                email=email,
                name=name,
                metadata={
                    "user_id": user_id,
                },
            )

            db = mongodb_manager.get_database()
            db.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"stripe_customer_id": customer.id}},
            )

            return {
                "customer_id": customer.id,
                "email": customer.email,
            }
        except (stripe.error.StripeError, ValueError, RuntimeError, ConnectionError) as e:
            logger.error("Failed to create Stripe customer: %s", e, exc_info=True)
            raise
        except Exception as e:
            logger.error("Unexpected error creating Stripe customer: %s", e, exc_info=True)
            raise ExternalServiceError(
                message=f"Unexpected error creating Stripe customer: {e}",
                user_message="Failed to create billing account. Please try again later.",
                error_code="STRIPE_CUSTOMER_CREATION_ERROR",
                details={"user_id": user_id, "error": str(e)}
            ) from e

    async def create_subscription(
        self,
        customer_id: str,
        price_id: str,
    ) -> dict[str, Any]:
        """Create subscription for customer.

        Args:
            customer_id: Stripe customer ID
            price_id: Stripe price ID

        Returns:
            Subscription object
        """
        if not stripe.api_key:
            raise ValidationError(
                message="Stripe API key not configured",
                user_message="Billing service is not configured. Please contact support.",
                error_code="STRIPE_NOT_CONFIGURED",
                details={"service": "billing"}
            )

        try:
            subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[{"price": price_id}],
            )

            return {
                "subscription_id": subscription.id,
                "status": subscription.status,
                "current_period_end": subscription.current_period_end,
            }
        except (stripe.error.StripeError, ValueError, RuntimeError, ConnectionError) as e:
            logger.error("Failed to create subscription: %s", e, exc_info=True)
            raise
        except Exception as e:
            logger.error("Unexpected error creating subscription: %s", e, exc_info=True)
            raise ExternalServiceError(
                message=f"Unexpected error creating subscription: {e}",
                user_message="Failed to create subscription. Please try again later.",
                error_code="STRIPE_SUBSCRIPTION_CREATION_ERROR",
                details={"customer_id": customer_id, "error": str(e)}
            ) from e

    async def update_subscription(
        self,
        subscription_id: str,
        price_id: str,
    ) -> dict[str, Any]:
        """Update subscription to new plan.

        Args:
            subscription_id: Stripe subscription ID
            price_id: New Stripe price ID

        Returns:
            Updated subscription object
        """
        if not stripe.api_key:
            raise ValidationError(
                message="Stripe API key not configured",
                user_message="Billing service is not configured. Please contact support.",
                error_code="STRIPE_NOT_CONFIGURED",
                details={"service": "billing"}
            )

        try:
            subscription = stripe.Subscription.retrieve(subscription_id)
            subscription = stripe.Subscription.modify(
                subscription_id,
                items=[{
                    "id": subscription["items"]["data"][0].id,
                    "price": price_id,
                }],
                proration_behavior="always_invoice",
            )

            return {
                "subscription_id": subscription.id,
                "status": subscription.status,
            }
        except (stripe.error.StripeError, ValueError, RuntimeError, ConnectionError) as e:
            logger.error("Failed to update subscription: %s", e, exc_info=True)
            raise
        except Exception as e:
            logger.error("Unexpected error updating subscription: %s", e, exc_info=True)
            raise ExternalServiceError(
                message=f"Unexpected error updating subscription: {e}",
                user_message="Failed to update subscription. Please try again later.",
                error_code="STRIPE_SUBSCRIPTION_UPDATE_ERROR",
                details={"subscription_id": subscription_id, "error": str(e)}
            ) from e

    async def cancel_subscription(
        self,
        subscription_id: str,
        immediately: bool = False,
    ) -> dict[str, Any]:
        """Cancel subscription.

        Args:
            subscription_id: Stripe subscription ID
            immediately: Cancel immediately or at period end

        Returns:
            Cancelled subscription object
        """
        if not stripe.api_key:
            raise ValidationError(
                message="Stripe API key not configured",
                user_message="Billing service is not configured. Please contact support.",
                error_code="STRIPE_NOT_CONFIGURED",
                details={"service": "billing"}
            )

        try:
            if immediately:
                subscription = stripe.Subscription.delete(subscription_id)
            else:
                subscription = stripe.Subscription.modify(
                    subscription_id,
                    cancel_at_period_end=True,
                )

            return {
                "subscription_id": subscription.id,
                "status": subscription.status,
                "cancel_at_period_end": subscription.cancel_at_period_end if hasattr(subscription, "cancel_at_period_end") else True,
            }
        except (stripe.error.StripeError, ValueError, RuntimeError, ConnectionError) as e:
            logger.error("Failed to cancel subscription: %s", e, exc_info=True)
            raise
        except Exception as e:
            logger.error("Unexpected error canceling subscription: %s", e, exc_info=True)
            raise ExternalServiceError(
                message=f"Unexpected error canceling subscription: {e}",
                user_message="Failed to cancel subscription. Please try again later.",
                error_code="STRIPE_SUBSCRIPTION_CANCEL_ERROR",
                details={"subscription_id": subscription_id, "error": str(e)}
            ) from e

    async def create_usage_record(
        self,
        subscription_item_id: str,
        quantity: int,
        timestamp: Optional[int] = None,
    ) -> dict[str, Any]:
        """Record usage for metered billing.

        Args:
            subscription_item_id: Stripe subscription item ID
            quantity: Usage quantity
            timestamp: Unix timestamp (defaults to now)

        Returns:
            Usage record object
        """
        if not stripe.api_key:
            raise ValidationError(
                message="Stripe API key not configured",
                user_message="Billing service is not configured. Please contact support.",
                error_code="STRIPE_NOT_CONFIGURED",
                details={"service": "billing"}
            )

        try:
            usage_record = stripe.UsageRecord.create(
                subscription_item=subscription_item_id,
                quantity=quantity,
                timestamp=timestamp,
            )

            return {
                "id": usage_record.id,
                "quantity": usage_record.quantity,
            }
        except (stripe.error.StripeError, ValueError, RuntimeError, ConnectionError) as e:
            logger.error("Failed to create usage record: %s", e, exc_info=True)
            raise
        except Exception as e:
            logger.error("Unexpected error creating usage record: %s", e, exc_info=True)
            raise ExternalServiceError(
                message=f"Unexpected error creating usage record: {e}",
                user_message="Failed to record usage. Please try again later.",
                error_code="STRIPE_USAGE_RECORD_ERROR",
                details={"subscription_item_id": subscription_item_id, "error": str(e)}
            ) from e

    async def get_invoices(
        self,
        customer_id: str,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """Get invoices for customer.

        Args:
            customer_id: Stripe customer ID
            limit: Maximum number of invoices

        Returns:
            List of invoice objects
        """
        if not stripe.api_key:
            raise ValidationError(
                message="Stripe API key not configured",
                user_message="Billing service is not configured. Please contact support.",
                error_code="STRIPE_NOT_CONFIGURED",
                details={"service": "billing"}
            )

        try:
            invoices = stripe.Invoice.list(
                customer=customer_id,
                limit=limit,
            )

            return [
                {
                    "id": invoice.id,
                    "amount_due": invoice.amount_due / 100,
                    "currency": invoice.currency,
                    "status": invoice.status,
                    "created": invoice.created,
                    "pdf": invoice.invoice_pdf,
                }
                for invoice in invoices.data
            ]
        except (stripe.error.StripeError, ValueError, RuntimeError, ConnectionError) as e:
            logger.error("Failed to get invoices: %s", e, exc_info=True)
            raise
        except Exception as e:
            logger.error("Unexpected error getting invoices: %s", e, exc_info=True)
            raise ExternalServiceError(
                message=f"Unexpected error getting invoices: {e}",
                user_message="Failed to retrieve invoices. Please try again later.",
                error_code="STRIPE_INVOICES_ERROR",
                details={"customer_id": customer_id, "error": str(e)}
            ) from e

    async def create_checkout_session(
        self,
        customer_id: str,
        price_id: str,
        success_url: str,
        cancel_url: str,
        metadata: Optional[dict[str, str]] = None,
    ) -> dict[str, Any]:
        """Create Stripe Checkout Session (like Cursor).

        Args:
            customer_id: Stripe customer ID
            price_id: Stripe price ID
            success_url: Success redirect URL
            cancel_url: Cancel redirect URL
            metadata: Additional metadata

        Returns:
            Checkout session object
        """
        if not stripe.api_key:
            raise ValidationError(
                message="Stripe API key not configured",
                user_message="Billing service is not configured. Please contact support.",
                error_code="STRIPE_NOT_CONFIGURED",
                details={"service": "billing"}
            )

        try:
            session_params: dict[str, Any] = {
                "customer": customer_id,
                "payment_method_types": ["card"],
                "line_items": [{"price": price_id, "quantity": 1}],
                "mode": "subscription",
                "success_url": success_url,
                "cancel_url": cancel_url,
                "allow_promotion_codes": True,
            }

            if metadata:
                session_params["metadata"] = metadata

            session = stripe.checkout.Session.create(**session_params)

            return {
                "session_id": session.id,
                "url": session.url,
                "publishable_key": settings.stripe_publishable_key or "",
            }
        except (stripe.error.StripeError, ValueError, RuntimeError, ConnectionError) as e:
            logger.error("Failed to create checkout session: %s", e, exc_info=True)
            raise
        except Exception as e:
            logger.error("Unexpected error creating checkout session: %s", e, exc_info=True)
            raise ExternalServiceError(
                message=f"Unexpected error creating checkout session: {e}",
                user_message="Failed to create checkout session. Please try again later.",
                error_code="STRIPE_CHECKOUT_ERROR",
                details={"customer_id": customer_id, "error": str(e)}
            ) from e

    async def create_portal_session(
        self,
        customer_id: str,
        return_url: str,
    ) -> dict[str, Any]:
        """Create Stripe Customer Portal session (like Cursor).

        Args:
            customer_id: Stripe customer ID
            return_url: Return URL after portal

        Returns:
            Portal session object
        """
        if not stripe.api_key:
            raise ValidationError(
                message="Stripe API key not configured",
                user_message="Billing service is not configured. Please contact support.",
                error_code="STRIPE_NOT_CONFIGURED",
                details={"service": "billing"}
            )

        try:
            session = stripe.billing_portal.Session.create(
                customer=customer_id,
                return_url=return_url,
            )

            return {
                "url": session.url,
            }
        except (stripe.error.StripeError, ValueError, RuntimeError, ConnectionError) as e:
            logger.error("Failed to create portal session: %s", e, exc_info=True)
            raise
        except Exception as e:
            logger.error("Unexpected error creating portal session: %s", e, exc_info=True)
            raise ExternalServiceError(
                message=f"Unexpected error creating portal session: {e}",
                user_message="Failed to create billing portal session. Please try again later.",
                error_code="STRIPE_PORTAL_ERROR",
                details={"customer_id": customer_id, "error": str(e)}
            ) from e

    async def get_subscription(
        self,
        subscription_id: str,
    ) -> dict[str, Any]:
        """Get subscription details.

        Args:
            subscription_id: Stripe subscription ID

        Returns:
            Subscription object
        """
        if not stripe.api_key:
            raise ValidationError(
                message="Stripe API key not configured",
                user_message="Billing service is not configured. Please contact support.",
                error_code="STRIPE_NOT_CONFIGURED",
                details={"service": "billing"}
            )

        try:
            subscription = stripe.Subscription.retrieve(subscription_id)

            return {
                "subscription_id": subscription.id,
                "status": subscription.status,
                "current_period_start": subscription.current_period_start,
                "current_period_end": subscription.current_period_end,
                "cancel_at_period_end": subscription.cancel_at_period_end,
                "customer_id": subscription.customer,
                "price_id": subscription.items.data[0].price.id if subscription.items.data else None,
            }
        except (stripe.error.StripeError, ValueError, RuntimeError, ConnectionError) as e:
            logger.error("Failed to get subscription: %s", e, exc_info=True)
            raise
        except Exception as e:
            logger.error("Unexpected error getting subscription: %s", e, exc_info=True)
            raise ExternalServiceError(
                message=f"Unexpected error getting subscription: {e}",
                user_message="Failed to retrieve subscription. Please try again later.",
                error_code="STRIPE_SUBSCRIPTION_GET_ERROR",
                details={"subscription_id": subscription_id, "error": str(e)}
            ) from e

    async def create_organization_customer(
        self,
        organization_id: str,
        email: str,
        name: str,
    ) -> dict[str, Any]:
        """Create Stripe customer for organization.

        Args:
            organization_id: Organization ID
            email: Organization billing email
            name: Organization name

        Returns:
            Stripe customer object
        """
        if not stripe.api_key:
            raise ValidationError(
                message="Stripe API key not configured",
                user_message="Billing service is not configured. Please contact support.",
                error_code="STRIPE_NOT_CONFIGURED",
                details={"service": "billing"}
            )

        try:
            customer = stripe.Customer.create(
                email=email,
                name=name,
                metadata={
                    "organization_id": organization_id,
                    "type": "organization",
                },
            )

            db = mongodb_manager.get_database()
            db.organizations.update_one(
                {"_id": ObjectId(organization_id)},
                {"$set": {"stripe_customer_id": customer.id}},
            )

            return {
                "customer_id": customer.id,
                "email": customer.email,
            }
        except (stripe.error.StripeError, ValueError, RuntimeError, ConnectionError) as e:
            logger.error("Failed to create organization Stripe customer: %s", e, exc_info=True)
            raise
        except Exception as e:
            logger.error("Unexpected error creating organization Stripe customer: %s", e, exc_info=True)
            raise ExternalServiceError(
                message=f"Unexpected error creating organization Stripe customer: {e}",
                user_message="Failed to create billing account. Please try again later.",
                error_code="STRIPE_ORG_CUSTOMER_ERROR",
                details={"organization_id": organization_id, "error": str(e)}
            ) from e

    async def create_organization_subscription(
        self,
        customer_id: str,
        price_id: str,
    ) -> dict[str, Any]:
        """Create subscription for organization.

        Args:
            customer_id: Stripe customer ID
            price_id: Stripe price ID

        Returns:
            Subscription object
        """
        if not stripe.api_key:
            raise ValidationError(
                message="Stripe API key not configured",
                user_message="Billing service is not configured. Please contact support.",
                error_code="STRIPE_NOT_CONFIGURED",
                details={"service": "billing"}
            )

        try:
            subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[{"price": price_id}],
            )

            return {
                "subscription_id": subscription.id,
                "status": subscription.status,
                "current_period_end": subscription.current_period_end,
            }
        except (stripe.error.StripeError, ValueError, RuntimeError, ConnectionError) as e:
            logger.error("Failed to create organization subscription: %s", e, exc_info=True)
            raise
        except Exception as e:
            logger.error("Unexpected error creating organization subscription: %s", e, exc_info=True)
            raise ExternalServiceError(
                message=f"Unexpected error creating organization subscription: {e}",
                user_message="Failed to create subscription. Please try again later.",
                error_code="STRIPE_ORG_SUBSCRIPTION_ERROR",
                details={"organization_id": organization_id, "error": str(e)}
            ) from e

    async def create_organization_checkout_session(
        self,
        customer_id: str,
        price_id: str,
        success_url: str,
        cancel_url: str,
        organization_id: str,
        metadata: Optional[dict[str, str]] = None,
    ) -> dict[str, Any]:
        """Create Stripe Checkout Session for organization.

        Args:
            customer_id: Stripe customer ID
            price_id: Stripe price ID
            success_url: Success redirect URL
            cancel_url: Cancel redirect URL
            organization_id: Organization ID
            metadata: Additional metadata

        Returns:
            Checkout session object
        """
        if not stripe.api_key:
            raise ValidationError(
                message="Stripe API key not configured",
                user_message="Billing service is not configured. Please contact support.",
                error_code="STRIPE_NOT_CONFIGURED",
                details={"service": "billing"}
            )

        try:
            session_metadata = metadata or {}
            session_metadata["organization_id"] = organization_id
            session_metadata["type"] = "organization"

            session_params: dict[str, Any] = {
                "customer": customer_id,
                "payment_method_types": ["card"],
                "line_items": [{"price": price_id, "quantity": 1}],
                "mode": "subscription",
                "success_url": success_url,
                "cancel_url": cancel_url,
                "allow_promotion_codes": True,
                "metadata": session_metadata,
            }

            session = stripe.checkout.Session.create(**session_params)

            return {
                "session_id": session.id,
                "url": session.url,
                "publishable_key": settings.stripe_publishable_key or "",
            }
        except (stripe.error.StripeError, ValueError, RuntimeError, ConnectionError) as e:
            logger.error("Failed to create organization checkout session: %s", e, exc_info=True)
            raise
        except Exception as e:
            logger.error("Unexpected error creating organization checkout session: %s", e, exc_info=True)
            raise ExternalServiceError(
                message=f"Unexpected error creating organization checkout session: {e}",
                user_message="Failed to create checkout session. Please try again later.",
                error_code="STRIPE_ORG_CHECKOUT_ERROR",
                details={"organization_id": organization_id, "error": str(e)}
            ) from e

    async def create_organization_portal_session(
        self,
        customer_id: str,
        return_url: str,
    ) -> dict[str, Any]:
        """Create Stripe Customer Portal session for organization.

        Args:
            customer_id: Stripe customer ID
            return_url: Return URL after portal

        Returns:
            Portal session object
        """
        if not stripe.api_key:
            raise ValidationError(
                message="Stripe API key not configured",
                user_message="Billing service is not configured. Please contact support.",
                error_code="STRIPE_NOT_CONFIGURED",
                details={"service": "billing"}
            )

        try:
            session = stripe.billing_portal.Session.create(
                customer=customer_id,
                return_url=return_url,
            )

            return {
                "url": session.url,
            }
        except (stripe.error.StripeError, ValueError, RuntimeError, ConnectionError) as e:
            logger.error("Failed to create organization portal session: %s", e, exc_info=True)
            raise
        except Exception as e:
            logger.error("Unexpected error creating organization portal session: %s", e, exc_info=True)
            raise ExternalServiceError(
                message=f"Unexpected error creating organization portal session: {e}",
                user_message="Failed to create billing portal session. Please try again later.",
                error_code="STRIPE_ORG_PORTAL_ERROR",
                details={"organization_id": organization_id, "error": str(e)}
            ) from e

    async def create_coupon(
        self,
        code: str,
        percent_off: float = 100.0,
        duration: str = "once",
        duration_in_months: Optional[int] = None,
        max_redemptions: Optional[int] = None,
        expires_at: Optional[int] = None,
        metadata: Optional[dict[str, str]] = None,
    ) -> dict[str, Any]:
        """Create Stripe coupon for beta users or promotions.

        Args:
            code: Coupon code (e.g., "BETA100")
            percent_off: Percentage discount (default: 100.0 for free)
            duration: "once", "repeating", or "forever"
            duration_in_months: Number of months if duration is "repeating"
            max_redemptions: Maximum number of times coupon can be used
            expires_at: Unix timestamp when coupon expires
            metadata: Additional metadata (e.g., {"type": "beta", "plan": "professional"})

        Returns:
            Coupon object with code and details
        """
        if not stripe.api_key:
            raise ValidationError(
                message="Stripe API key not configured",
                user_message="Billing service is not configured. Please contact support.",
                error_code="STRIPE_NOT_CONFIGURED",
                details={"service": "billing"}
            )

        try:
            coupon_params: dict[str, Any] = {
                "id": code.upper(),
                "percent_off": percent_off,
                "duration": duration,
            }

            if duration == "repeating" and duration_in_months:
                coupon_params["duration_in_months"] = duration_in_months

            if max_redemptions:
                coupon_params["max_redemptions"] = max_redemptions

            if expires_at:
                coupon_params["redeem_by"] = expires_at

            if metadata:
                coupon_params["metadata"] = metadata

            coupon = stripe.Coupon.create(**coupon_params)

            logger.info("Created Stripe coupon: %s (%.1f%% off, duration: %s)", code, percent_off, duration)

            return {
                "id": coupon.id,
                "code": code.upper(),
                "percent_off": coupon.percent_off,
                "duration": coupon.duration,
                "duration_in_months": getattr(coupon, "duration_in_months", None),
                "max_redemptions": coupon.max_redemptions,
                "times_redeemed": coupon.times_redeemed,
                "valid": coupon.valid,
            }
        except (stripe.error.StripeError, ValueError, RuntimeError, ConnectionError) as e:
            logger.error("Failed to create Stripe coupon: %s", e, exc_info=True)
            raise
        except Exception as e:
            logger.error("Unexpected error creating Stripe coupon: %s", e, exc_info=True)
            raise ExternalServiceError(
                message=f"Unexpected error creating Stripe coupon: {e}",
                user_message="Failed to create coupon. Please try again later.",
                error_code="STRIPE_COUPON_CREATION_ERROR",
                details={"code": code, "error": str(e)}
            ) from e

    async def get_coupon(self, coupon_id: str) -> dict[str, Any] | None:
        """Get Stripe coupon details.

        Args:
            coupon_id: Coupon ID or code

        Returns:
            Coupon object or None if not found
        """
        if not stripe.api_key:
            raise ValidationError(
                message="Stripe API key not configured",
                user_message="Billing service is not configured. Please contact support.",
                error_code="STRIPE_NOT_CONFIGURED",
                details={"service": "billing"}
            )

        try:
            coupon = stripe.Coupon.retrieve(coupon_id)
            return {
                "id": coupon.id,
                "code": coupon.id,
                "percent_off": coupon.percent_off,
                "duration": coupon.duration,
                "duration_in_months": getattr(coupon, "duration_in_months", None),
                "max_redemptions": coupon.max_redemptions,
                "times_redeemed": coupon.times_redeemed,
                "valid": coupon.valid,
                "metadata": coupon.metadata,
            }
        except stripe.error.InvalidRequestError:
            return None
        except (stripe.error.StripeError, ValueError, RuntimeError, ConnectionError) as e:
            logger.error("Failed to get Stripe coupon: %s", e, exc_info=True)
            raise
        except Exception as e:
            logger.error("Unexpected error getting Stripe coupon: %s", e, exc_info=True)
            raise ExternalServiceError(
                message=f"Unexpected error getting Stripe coupon: {e}",
                user_message="Failed to retrieve coupon. Please try again later.",
                error_code="STRIPE_COUPON_GET_ERROR",
                details={"coupon_id": coupon_id, "error": str(e)}
            ) from e

    async def list_coupons(
        self,
        limit: int = 100,
        active_only: bool = True,
    ) -> list[dict[str, Any]]:
        """List Stripe coupons.

        Args:
            limit: Maximum number of coupons to return
            active_only: If True, return only valid coupons

        Returns:
            List of coupon objects
        """
        if not stripe.api_key:
            raise ValidationError(
                message="Stripe API key not configured",
                user_message="Billing service is not configured. Please contact support.",
                error_code="STRIPE_NOT_CONFIGURED",
                details={"service": "billing"}
            )

        try:
            params: dict[str, Any] = {"limit": limit}
            if active_only:
                params["active"] = True

            coupons = stripe.Coupon.list(**params)

            return [
                {
                    "id": coupon.id,
                    "code": coupon.id,
                    "percent_off": coupon.percent_off,
                    "duration": coupon.duration,
                    "duration_in_months": getattr(coupon, "duration_in_months", None),
                    "max_redemptions": coupon.max_redemptions,
                    "times_redeemed": coupon.times_redeemed,
                    "valid": coupon.valid,
                    "metadata": coupon.metadata,
                }
                for coupon in coupons.data
            ]
        except (stripe.error.StripeError, ValueError, RuntimeError, ConnectionError) as e:
            logger.error("Failed to list Stripe coupons: %s", e, exc_info=True)
            raise
        except Exception as e:
            logger.error("Unexpected error listing Stripe coupons: %s", e, exc_info=True)
            raise ExternalServiceError(
                message=f"Unexpected error listing Stripe coupons: {e}",
                user_message="Failed to list coupons. Please try again later.",
                error_code="STRIPE_COUPON_LIST_ERROR",
                details={"error": str(e)}
            ) from e

    async def delete_coupon(self, coupon_id: str) -> bool:
        """Delete Stripe coupon.

        Args:
            coupon_id: Coupon ID or code

        Returns:
            True if deleted, False otherwise
        """
        if not stripe.api_key:
            raise ValidationError(
                message="Stripe API key not configured",
                user_message="Billing service is not configured. Please contact support.",
                error_code="STRIPE_NOT_CONFIGURED",
                details={"service": "billing"}
            )

        try:
            deleted = stripe.Coupon.delete(coupon_id)
            logger.info("Deleted Stripe coupon: %s", coupon_id)
            return deleted.deleted
        except stripe.error.InvalidRequestError as e:
            logger.warning("Coupon not found or already deleted: %s", coupon_id)
            return False
        except (stripe.error.StripeError, ValueError, RuntimeError, ConnectionError) as e:
            logger.error("Failed to delete Stripe coupon: %s", e, exc_info=True)
            raise
        except Exception as e:
            logger.error("Unexpected error deleting Stripe coupon: %s", e, exc_info=True)
            raise ExternalServiceError(
                message=f"Unexpected error deleting Stripe coupon: {e}",
                user_message="Failed to delete coupon. Please try again later.",
                error_code="STRIPE_COUPON_DELETE_ERROR",
                details={"coupon_id": coupon_id, "error": str(e)}
            ) from e


billing_service = BillingService()
