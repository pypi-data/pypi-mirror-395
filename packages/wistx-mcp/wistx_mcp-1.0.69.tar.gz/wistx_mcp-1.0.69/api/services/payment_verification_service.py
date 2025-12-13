"""Service for verifying payment and subscription status."""

import logging
from typing import Optional

import stripe
from stripe import _error as stripe_error

from api.services.billing_service import billing_service

logger = logging.getLogger(__name__)


class PaymentVerificationService:
    """Service for verifying payment success."""

    @staticmethod
    async def verify_checkout_session(session_id: str) -> dict:
        """Verify checkout session completion.

        Args:
            session_id: Stripe checkout session ID

        Returns:
            Verification result with subscription status
        """
        try:
            session = stripe.checkout.Session.retrieve(
                session_id, expand=["subscription", "customer"]
            )

            if session.payment_status != "paid":
                return {
                    "verified": False,
                    "status": "payment_pending",
                    "message": "Payment not yet completed",
                }

            if not session.subscription:
                return {
                    "verified": False,
                    "status": "no_subscription",
                    "message": "No subscription found",
                }

            subscription_id = (
                session.subscription.id
                if hasattr(session.subscription, "id")
                else str(session.subscription)
            )

            subscription_data = await billing_service.get_subscription(subscription_id)

            if not subscription_data:
                return {
                    "verified": False,
                    "status": "subscription_not_found",
                    "message": "Subscription not found",
                }

            return {
                "verified": True,
                "status": "success",
                "subscription_id": subscription_id,
                "subscription_status": subscription_data.get("status"),
                "plan_id": subscription_data.get("plan_id"),
            }

        except stripe_error.StripeError as e:
            logger.error("Stripe error verifying checkout: %s", e)
            return {
                "verified": False,
                "status": "stripe_error",
                "message": str(e),
            }
        except Exception as e:
            logger.error("Error verifying checkout: %s", e, exc_info=True)
            return {
                "verified": False,
                "status": "error",
                "message": str(e),
            }

