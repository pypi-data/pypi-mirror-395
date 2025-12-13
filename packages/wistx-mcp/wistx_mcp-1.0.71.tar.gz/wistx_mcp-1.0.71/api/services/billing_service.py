"""Billing service with Stripe integration."""

import logging
from typing import Any, Optional

import stripe
from stripe import _error as stripe_error
from bson import ObjectId

from api.config import settings
from api.database.mongodb import mongodb_manager
from api.exceptions import ValidationError, ExternalServiceError
from api.models.billing import CheckoutSessionResult, CustomerResult, PortalSessionResult

logger = logging.getLogger(__name__)

stripe.api_key = getattr(settings, "stripe_secret_key", None) or ""


class BillingService:
    """Stripe billing integration service."""

    def __init__(self):
        """Initialize billing service."""
        if not stripe.api_key:
            logger.warning("Stripe API key not configured. Billing features will be disabled.")

    async def find_customer_by_email(
        self,
        email: str,
    ) -> Optional[CustomerResult]:
        """Find existing Stripe customer by email.

        Args:
            email: Customer email

        Returns:
            CustomerResult if found, None otherwise
        """
        if not stripe.api_key:
            return None

        try:
            customers = stripe.Customer.list(
                email=email,
                limit=1,
            )
            if customers.data:
                customer = customers.data[0]
                return CustomerResult(
                    customer_id=customer.id,
                    email=customer.email or email,
                )
            return None
        except (stripe_error.StripeError, ValueError, RuntimeError, ConnectionError) as e:
            logger.warning("Failed to search for existing customer by email: %s", e)
            return None
        except Exception as e:
            logger.warning("Unexpected error searching for customer: %s", e)
            return None

    async def get_or_create_customer(
        self,
        user_id: str,
        email: str,
        name: Optional[str] = None,
    ) -> CustomerResult:
        """Get existing Stripe customer or create new one.

        Checks database first, then Stripe by email, then creates new customer.
        This prevents duplicate customer creation.

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

        db = mongodb_manager.get_database()
        user = db.users.find_one({"_id": ObjectId(user_id)})
        
        if user and user.get("stripe_customer_id"):
            existing_customer_id = user.get("stripe_customer_id")
            try:
                customer = stripe.Customer.retrieve(existing_customer_id)
                logger.info("Using existing Stripe customer from database: %s", existing_customer_id)
                return CustomerResult(
                    customer_id=customer.id,
                    email=customer.email or email,
                )
            except stripe_error.StripeError:
                logger.warning("Stripe customer %s not found in Stripe, will create new one", existing_customer_id)
                db.users.update_one(
                    {"_id": ObjectId(user_id)},
                    {"$unset": {"stripe_customer_id": ""}},
                )

        existing_customer = await self.find_customer_by_email(email)
        if existing_customer:
            logger.info("Found existing Stripe customer by email: %s", existing_customer.customer_id)
            db.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"stripe_customer_id": existing_customer.customer_id}},
            )
            return existing_customer

        try:
            customer = stripe.Customer.create(
                email=email,
                name=name,
                metadata={
                    "user_id": user_id,
                },
            )

            db.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"stripe_customer_id": customer.id}},
            )

            logger.info("Created new Stripe customer: %s for user: %s", customer.id, user_id)
            return CustomerResult(
                customer_id=customer.id,
                email=customer.email or email,
            )
        except (stripe_error.StripeError, ValueError, RuntimeError, ConnectionError) as e:
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

    async def create_customer(
        self,
        user_id: str,
        email: str,
        name: Optional[str] = None,
    ) -> CustomerResult:
        """Create Stripe customer for user.

        DEPRECATED: Use get_or_create_customer instead to prevent duplicates.

        Args:
            user_id: User ID
            email: User email
            name: User name (optional)

        Returns:
            Stripe customer object
        """
        return await self.get_or_create_customer(user_id, email, name)

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
        except (stripe_error.StripeError, ValueError, RuntimeError, ConnectionError) as e:
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
        except (stripe_error.StripeError, ValueError, RuntimeError, ConnectionError) as e:
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
        except (stripe_error.StripeError, ValueError, RuntimeError, ConnectionError) as e:
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
        except (stripe_error.StripeError, ValueError, RuntimeError, ConnectionError) as e:
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
        except (stripe_error.StripeError, ValueError, RuntimeError, ConnectionError) as e:
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
    ) -> CheckoutSessionResult:
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

            return CheckoutSessionResult(
                session_id=session.id,
                url=session.url or "",
                publishable_key=settings.stripe_publishable_key or "",
            )
        except stripe_error.InvalidRequestError as e:
            error_message = str(e)
            if "No such price" in error_message:
                api_key_prefix = stripe.api_key[:7] if stripe.api_key else "none"
                is_test_mode = api_key_prefix.startswith("sk_test")
                is_live_mode = api_key_prefix.startswith("sk_live")
                mode = "test" if is_test_mode else ("live" if is_live_mode else "unknown")
                
                logger.error(
                    "Stripe price ID not found: %s | Stripe mode: %s | API key prefix: %s | Error: %s. "
                    "Check if price exists in Stripe dashboard and matches test/live mode.",
                    price_id,
                    mode,
                    api_key_prefix,
                    error_message,
                    exc_info=True,
                )
                raise ExternalServiceError(
                    message=f"Stripe price ID not found: {price_id} (mode: {mode})",
                    user_message="The selected plan is not available. Please contact support or try again later.",
                    error_code="STRIPE_PRICE_NOT_FOUND",
                    details={
                        "price_id": price_id,
                        "stripe_mode": mode,
                        "stripe_error": error_message,
                    },
                ) from e
            if "No such customer" in error_message:
                logger.warning(
                    "Stripe customer ID not found: %s. Customer may have been deleted or is from different Stripe account/mode.",
                    customer_id,
                    exc_info=True,
                )
                raise ExternalServiceError(
                    message=f"Stripe customer not found: {customer_id}",
                    user_message="Billing account issue detected. Please try again.",
                    error_code="STRIPE_CUSTOMER_NOT_FOUND",
                    details={"customer_id": customer_id, "stripe_error": error_message},
                ) from e
            logger.error("Stripe invalid request error: %s", e, exc_info=True)
            raise ExternalServiceError(
                message=f"Stripe request error: {error_message}",
                user_message="Failed to create checkout session. Please try again later.",
                error_code="STRIPE_INVALID_REQUEST",
                details={"price_id": price_id, "customer_id": customer_id, "stripe_error": error_message},
            ) from e
        except (stripe_error.StripeError, ValueError, RuntimeError, ConnectionError) as e:
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

    async def get_checkout_session(
        self,
        session_id: str,
    ) -> dict[str, Any]:
        """Retrieve Stripe checkout session.

        Args:
            session_id: Stripe checkout session ID

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
            session = stripe.checkout.Session.retrieve(session_id)
            return {
                "id": session.id,
                "customer": session.customer,
                "subscription": session.subscription,
                "status": session.payment_status,
                "metadata": session.metadata or {},
            }
        except (stripe_error.StripeError, ValueError, RuntimeError, ConnectionError) as e:
            logger.error("Failed to retrieve checkout session: %s", e, exc_info=True)
            raise
        except Exception as e:
            logger.error("Unexpected error retrieving checkout session: %s", e, exc_info=True)
            raise ExternalServiceError(
                message=f"Unexpected error retrieving checkout session: {e}",
                user_message="Failed to retrieve checkout session. Please try again later.",
                error_code="STRIPE_CHECKOUT_SESSION_ERROR",
                details={"session_id": session_id, "error": str(e)}
            ) from e

    async def create_portal_session(
        self,
        customer_id: str,
        return_url: str,
    ) -> PortalSessionResult:
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

            return PortalSessionResult(
                url=session.url or "",
            )
        except (stripe_error.StripeError, ValueError, RuntimeError, ConnectionError) as e:
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

            current_period_start = getattr(subscription, "current_period_start", None)
            current_period_end = getattr(subscription, "current_period_end", None)

            items = getattr(subscription, "items", None)
            items_data = getattr(items, "data", []) if items else []

            if not current_period_start and items_data:
                first_item = items_data[0]
                current_period_start = getattr(first_item, "current_period_start", None)
                current_period_end = getattr(first_item, "current_period_end", None)

            # Extract price_id - try subscription.plan.id first (most reliable)
            price_id = None
            if hasattr(subscription, "plan") and subscription.plan:
                price_id = getattr(subscription.plan, "id", None)
                logger.debug("get_subscription: Got price_id from subscription.plan: %s", price_id)

            # Fallback to items if plan not available
            if not price_id and items_data and len(items_data) > 0:
                price = getattr(items_data[0], "price", None)
                if price:
                    price_id = getattr(price, "id", None)
                    logger.debug("get_subscription: Got price_id from items: %s", price_id)

            return {
                "subscription_id": subscription.id,
                "status": subscription.status,
                "current_period_start": current_period_start,
                "current_period_end": current_period_end,
                "cancel_at_period_end": getattr(subscription, "cancel_at_period_end", False),
                "customer_id": subscription.customer,
                "price_id": price_id,
            }
        except (stripe_error.StripeError, ValueError, RuntimeError, ConnectionError) as e:
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

    async def get_customer_subscriptions(
        self,
        customer_id: str,
    ) -> list[dict[str, Any]]:
        """Get all active subscriptions for a customer.

        Args:
            customer_id: Stripe customer ID

        Returns:
            List of subscription objects
        """
        if not stripe.api_key:
            raise ValidationError(
                message="Stripe API key not configured",
                user_message="Billing service is not configured. Please contact support.",
                error_code="STRIPE_NOT_CONFIGURED",
                details={"service": "billing"}
            )

        try:
            subscriptions = stripe.Subscription.list(
                customer=customer_id,
                status="all",
                limit=10,
                expand=["data.items.data.price"],
            )

            result = []
            for subscription in subscriptions.data:
                current_period_start = getattr(subscription, "current_period_start", None)
                current_period_end = getattr(subscription, "current_period_end", None)

                # Extract price_id - try multiple approaches
                price_id = None
                items_count = 0

                # Method 1: Try subscription.plan.id directly (top-level plan)
                if hasattr(subscription, "plan") and subscription.plan:
                    if hasattr(subscription.plan, "id"):
                        price_id = subscription.plan.id
                    elif isinstance(subscription.plan, dict):
                        price_id = subscription.plan.get("id")
                    logger.debug("Got price_id from subscription.plan: %s", price_id)

                # Method 2: Try subscription["items"]["data"][0]["price"]["id"] via dict access
                if not price_id:
                    try:
                        # Convert to dict if it's a Stripe object
                        sub_dict = subscription.to_dict() if hasattr(subscription, "to_dict") else dict(subscription)
                        items = sub_dict.get("items", {})
                        items_data = items.get("data", []) if isinstance(items, dict) else []
                        items_count = len(items_data)
                        if items_data:
                            first_item = items_data[0]
                            # Try price first
                            price = first_item.get("price", {})
                            if price:
                                price_id = price.get("id")
                            # Fallback to plan
                            if not price_id:
                                plan = first_item.get("plan", {})
                                if plan:
                                    price_id = plan.get("id")
                            logger.debug("Got price_id from items via dict: %s", price_id)
                    except Exception as e:
                        logger.warning("Failed to extract price_id via dict for %s: %s", subscription.id, e)

                # Method 3: Try direct attribute access on items
                if not price_id and hasattr(subscription, "items") and subscription.items:
                    try:
                        items_obj = subscription.items
                        if hasattr(items_obj, "data") and items_obj.data:
                            items_count = len(items_obj.data)
                            first_item = items_obj.data[0]
                            if hasattr(first_item, "price") and first_item.price:
                                price_id = getattr(first_item.price, "id", None)
                            if not price_id and hasattr(first_item, "plan") and first_item.plan:
                                price_id = getattr(first_item.plan, "id", None)
                            logger.debug("Got price_id from items via attr: %s", price_id)
                    except Exception as e:
                        logger.warning("Failed to extract price_id via attr for %s: %s", subscription.id, e)

                logger.debug(
                    "Extracted subscription data: id=%s, status=%s, price_id=%s, items_count=%d",
                    subscription.id, subscription.status, price_id, items_count
                )
                
                result.append({
                    "subscription_id": subscription.id,
                    "status": subscription.status,
                    "current_period_start": current_period_start,
                    "current_period_end": current_period_end,
                    "cancel_at_period_end": getattr(subscription, "cancel_at_period_end", False),
                    "customer_id": subscription.customer,
                    "price_id": price_id,
                })

            return result
        except (stripe_error.StripeError, ValueError, RuntimeError, ConnectionError) as e:
            logger.error("Failed to get customer subscriptions: %s", e, exc_info=True)
            raise
        except Exception as e:
            logger.error("Unexpected error getting customer subscriptions: %s", e, exc_info=True)
            raise ExternalServiceError(
                message=f"Unexpected error getting customer subscriptions: {e}",
                user_message="Failed to retrieve subscriptions. Please try again later.",
                error_code="STRIPE_SUBSCRIPTION_LIST_ERROR",
                details={"customer_id": customer_id, "error": str(e)}
            ) from e

    async def create_organization_customer(
        self,
        organization_id: str,
        email: str,
        name: str,
    ) -> CustomerResult:
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

            return CustomerResult(
                customer_id=customer.id,
                email=customer.email or email,
            )
        except (stripe_error.StripeError, ValueError, RuntimeError, ConnectionError) as e:
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
        except (stripe_error.StripeError, ValueError, RuntimeError, ConnectionError) as e:
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
    ) -> CheckoutSessionResult:
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

            return CheckoutSessionResult(
                session_id=session.id,
                url=session.url or "",
                publishable_key=settings.stripe_publishable_key or "",
            )
        except (stripe_error.StripeError, ValueError, RuntimeError, ConnectionError) as e:
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
    ) -> PortalSessionResult:
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

            return PortalSessionResult(
                url=session.url or "",
            )
        except (stripe_error.StripeError, ValueError, RuntimeError, ConnectionError) as e:
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
        except (stripe_error.StripeError, ValueError, RuntimeError, ConnectionError) as e:
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
        except stripe_error.InvalidRequestError:
            return None
        except (stripe_error.StripeError, ValueError, RuntimeError, ConnectionError) as e:
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
        except (stripe_error.StripeError, ValueError, RuntimeError, ConnectionError) as e:
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
        except stripe_error.InvalidRequestError as e:
            logger.warning("Coupon not found or already deleted: %s", coupon_id)
            return False
        except (stripe_error.StripeError, ValueError, RuntimeError, ConnectionError) as e:
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
