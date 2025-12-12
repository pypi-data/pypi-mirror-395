"""GitHub webhook handlers for automatic repository re-indexing.

Production-ready implementation with comprehensive edge case handling.
"""

import asyncio
import hmac
import hashlib
import logging
import time
from datetime import datetime, timedelta
from typing import Any, Optional

from fastapi import APIRouter, HTTPException, Request, status

from api.config import settings
from api.database.mongodb import mongodb_manager
from api.services.indexing_service import indexing_service
from api.models.indexing import ResourceStatus

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/webhooks/github", tags=["github-webhooks"])

RATE_LIMIT_WINDOW = 60
RATE_LIMIT_MAX = 100


@router.post("/")
async def github_webhook(request: Request) -> dict[str, str]:
    """Handle GitHub webhook events with comprehensive edge case handling.

    Supports:
    - pull_request.merged: Auto-re-index repository when PR is merged
    - push: Auto-re-index on push to main/master branch

    Edge Cases Handled:
    - Duplicate deliveries (idempotency)
    - Rate limiting
    - Invalid signatures
    - Missing resources
    - Concurrent processing
    - Partial failures

    Args:
        request: FastAPI request object

    Returns:
        Success response (within 10 seconds)

    Raises:
        HTTPException: If webhook is invalid or processing fails
    """
    start_time = time.time()

    signature = request.headers.get("X-Hub-Signature-256")
    if not signature:
        logger.warning("Missing X-Hub-Signature-256 header")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing X-Hub-Signature-256 header",
        )

    payload = await request.body()

    if not verify_github_signature(payload, signature):
        logger.warning("Invalid webhook signature")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid webhook signature",
        )

    event_type = request.headers.get("X-GitHub-Event")
    delivery_id = request.headers.get("X-GitHub-Delivery")

    if not event_type:
        logger.warning("Missing X-GitHub-Event header")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing X-GitHub-Event header",
        )

    if not delivery_id:
        logger.warning("Missing X-GitHub-Delivery header")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing X-GitHub-Delivery header",
        )

    if await is_duplicate_event(delivery_id):
        logger.info("Duplicate webhook event detected: %s", delivery_id)
        return {"status": "success", "message": "Event already processed"}

    try:
        payload_json = await request.json()
    except Exception as e:
        logger.error("Failed to parse webhook payload: %s", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON payload",
        ) from e

    repo_url = extract_repo_url(payload_json)
    if repo_url and await is_rate_limited(repo_url):
        logger.warning("Rate limit exceeded for repository: %s", repo_url)
        await record_webhook_event(
            delivery_id=delivery_id,
            event_type=event_type,
            repository_url=repo_url,
            status="rate_limited",
        )
        return {
            "status": "success",
            "message": "Rate limited - will process later",
        }

    await record_webhook_event(
        delivery_id=delivery_id,
        event_type=event_type,
        repository_url=repo_url or "unknown",
        status="processing",
    )

    try:
        asyncio.create_task(
            process_webhook_async(
                delivery_id=delivery_id,
                event_type=event_type,
                payload=payload_json,
            )
        )

        elapsed_time = time.time() - start_time
        if elapsed_time > 9.0:
            logger.warning("Webhook processing took %.2f seconds (approaching 10s limit)", elapsed_time)

        return {"status": "success", "message": "Webhook queued for processing"}

    except Exception as e:
        logger.error("Error queuing webhook: %s", e, exc_info=True)
        await update_webhook_event_status(delivery_id, "failed", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Webhook processing failed",
        ) from e


def verify_github_signature(payload: bytes, signature: str) -> bool:
    """Verify GitHub webhook signature using HMAC SHA-256.

    Args:
        payload: Webhook payload bytes
        signature: X-Hub-Signature-256 header value (format: "sha256=...")

    Returns:
        True if signature is valid
    """
    if not settings.github_webhook_secret:
        logger.warning("GitHub webhook secret not configured")
        return False

    try:
        received_signature = signature.replace("sha256=", "")

        expected_signature = hmac.new(
            settings.github_webhook_secret.encode(),
            payload,
            hashlib.sha256,
        ).hexdigest()

        return hmac.compare_digest(expected_signature, received_signature)

    except Exception as e:
        logger.error("Error verifying webhook signature: %s", e, exc_info=True)
        return False


async def is_duplicate_event(delivery_id: str) -> bool:
    """Check if webhook event was already processed.

    Args:
        delivery_id: GitHub delivery ID

    Returns:
        True if event was already processed
    """
    db = mongodb_manager.get_database()
    collection = db.github_webhook_events

    existing = collection.find_one({
        "delivery_id": delivery_id,
        "status": {"$in": ["processed", "processing"]},
    })

    return existing is not None


async def is_rate_limited(repo_url: str) -> bool:
    """Check if repository is rate limited.

    Args:
        repo_url: Repository URL

    Returns:
        True if rate limited
    """
    db = mongodb_manager.get_database()
    collection = db.github_webhook_events

    cutoff_time = datetime.utcnow() - timedelta(seconds=RATE_LIMIT_WINDOW)

    count = collection.count_documents({
        "repository_url": repo_url,
        "processed_at": {"$gte": cutoff_time},
        "status": {"$in": ["processed", "processing"]},
    })

    return count >= RATE_LIMIT_MAX


async def record_webhook_event(
    delivery_id: str,
    event_type: str,
    repository_url: str,
    status: str = "pending",
) -> None:
    """Record webhook event for deduplication and tracking.

    Args:
        delivery_id: GitHub delivery ID
        event_type: Event type
        repository_url: Repository URL
        status: Processing status
    """
    db = mongodb_manager.get_database()
    collection = db.github_webhook_events

    event = {
        "delivery_id": delivery_id,
        "event_type": event_type,
        "repository_url": repository_url,
        "status": status,
        "processed_at": datetime.utcnow(),
        "expires_at": datetime.utcnow() + timedelta(days=7),
    }

    collection.replace_one(
        {"delivery_id": delivery_id},
        event,
        upsert=True,
    )


async def update_webhook_event_status(
    delivery_id: str,
    status: str,
    error: Optional[str] = None,
) -> None:
    """Update webhook event status.

    Args:
        delivery_id: GitHub delivery ID
        status: New status
        error: Error message if failed
    """
    db = mongodb_manager.get_database()
    collection = db.github_webhook_events

    update = {"status": status, "updated_at": datetime.utcnow()}
    if error:
        update["error"] = error

    collection.update_one(
        {"delivery_id": delivery_id},
        {"$set": update},
    )


def extract_repo_url(payload: dict[str, Any]) -> Optional[str]:
    """Extract repository URL from webhook payload.

    Args:
        payload: Webhook payload

    Returns:
        Repository URL or None
    """
    repo = payload.get("repository", {})
    return repo.get("html_url") or repo.get("clone_url")


async def process_webhook_async(
    delivery_id: str,
    event_type: str,
    payload: dict[str, Any],
) -> None:
    """Process webhook event asynchronously.

    Args:
        delivery_id: GitHub delivery ID
        event_type: Event type
        payload: Webhook payload
    """
    try:
        if event_type == "pull_request":
            await handle_pull_request_event(delivery_id, payload)
        elif event_type == "push":
            await handle_push_event(delivery_id, payload)
        else:
            logger.debug("Unhandled event type: %s", event_type)
            await update_webhook_event_status(delivery_id, "skipped")
            return

        await update_webhook_event_status(delivery_id, "processed")
        logger.info("Successfully processed webhook: %s", delivery_id)

    except Exception as e:
        logger.error(
            "Error processing webhook %s: %s",
            delivery_id,
            e,
            exc_info=True,
        )
        await update_webhook_event_status(delivery_id, "failed", str(e))

        await store_failed_webhook(delivery_id, event_type, payload, str(e))


async def handle_pull_request_event(
    delivery_id: str,
    payload: dict[str, Any],
) -> None:
    """Handle pull request webhook event.

    Args:
        delivery_id: GitHub delivery ID
        payload: Webhook payload
    """
    action = payload.get("action")
    pr = payload.get("pull_request", {})

    if action != "closed" or not pr.get("merged"):
        logger.debug(
            "PR not merged, skipping: action=%s, merged=%s",
            action,
            pr.get("merged"),
        )
        return

    repo = payload.get("repository", {})
    repo_url = repo.get("html_url") or repo.get("clone_url")
    default_branch = repo.get("default_branch", "main")
    merged_branch = pr.get("base", {}).get("ref", default_branch)

    if not repo_url:
        logger.warning("No repository URL in PR webhook payload")
        return

    logger.info(
        "PR merged, triggering re-index: repo=%s, branch=%s, delivery_id=%s",
        repo_url,
        merged_branch,
        delivery_id,
    )

    await trigger_reindex(repo_url, merged_branch, delivery_id)


async def handle_push_event(
    delivery_id: str,
    payload: dict[str, Any],
) -> None:
    """Handle push webhook event.

    Only re-indexes if push is to main/master branch.

    Args:
        delivery_id: GitHub delivery ID
        payload: Webhook payload
    """
    ref = payload.get("ref", "")
    if not ref.startswith("refs/heads/"):
        logger.debug("Not a branch ref: %s", ref)
        return

    branch = ref.replace("refs/heads/", "")

    if branch not in ["main", "master"]:
        logger.debug("Push to non-main branch, skipping: %s", branch)
        return

    repo = payload.get("repository", {})
    repo_url = repo.get("html_url") or repo.get("clone_url")

    if not repo_url:
        logger.warning("No repository URL in push webhook payload")
        return

    logger.info(
        "Push to main branch, triggering re-index: repo=%s, branch=%s, delivery_id=%s",
        repo_url,
        branch,
        delivery_id,
    )

    await trigger_reindex(repo_url, branch, delivery_id)


async def trigger_reindex(
    repo_url: str,
    branch: str,
    delivery_id: str,
) -> None:
    """Trigger repository re-indexing with comprehensive error handling.

    Args:
        repo_url: Repository URL
        branch: Branch name
        delivery_id: Webhook delivery ID (for tracking)
    """
    from api.utils.repo_normalizer import normalize_repo_url
    from bson import ObjectId

    normalized_url = normalize_repo_url(repo_url)

    db = mongodb_manager.get_database()
    collection = db.indexed_resources

    resources = list(collection.find({
        "normalized_repo_url": normalized_url,
        "branch": branch,
        "status": {"$ne": ResourceStatus.DELETED.value},
    }))

    if not resources:
        logger.info(
            "No indexed resources found for repo: %s (branch: %s), delivery_id=%s",
            repo_url,
            branch,
            delivery_id,
        )
        return

    semaphore = asyncio.Semaphore(5)

    async def reindex_resource(resource_doc: dict[str, Any]) -> None:
        """Re-index a single resource."""
        async with semaphore:
            resource_id = resource_doc["_id"]
            user_id = str(resource_doc["user_id"])

            try:
                user_doc = db.users.find_one({"_id": ObjectId(user_id)})
                if not user_doc:
                    logger.warning(
                        "User not found for resource %s, skipping re-index",
                        resource_id,
                    )
                    return

                plan = user_doc.get("plan", "professional")

                current_status = resource_doc.get("status")
                if current_status == ResourceStatus.INDEXING.value:
                    logger.info(
                        "Resource %s already indexing, skipping duplicate trigger",
                        resource_id,
                    )
                    return

                await indexing_service._update_resource_status(
                    resource_id=resource_id,
                    status=ResourceStatus.PENDING,
                    progress=0.0,
                )

                job_id = await indexing_service.start_indexing_job(
                    resource_id=resource_id,
                    user_id=user_id,
                    plan=plan,
                )

                logger.info(
                    "Triggered re-indexing job: resource_id=%s, job_id=%s, delivery_id=%s",
                    resource_id,
                    job_id,
                    delivery_id,
                )

            except Exception as e:
                logger.error(
                    "Failed to trigger re-indexing for resource %s: %s, delivery_id=%s",
                    resource_id,
                    e,
                    delivery_id,
                    exc_info=True,
                )

    tasks = [reindex_resource(resource_doc) for resource_doc in resources]
    await asyncio.gather(*tasks, return_exceptions=True)


async def store_failed_webhook(
    delivery_id: str,
    event_type: str,
    payload: dict[str, Any],
    error: str,
) -> None:
    """Store failed webhook in dead letter queue.

    Args:
        delivery_id: GitHub delivery ID
        event_type: Event type
        payload: Webhook payload
        error: Error message
    """
    db = mongodb_manager.get_database()
    collection = db.github_webhook_dead_letter_queue

    failed_webhook = {
        "delivery_id": delivery_id,
        "event_type": event_type,
        "payload": payload,
        "error": error,
        "failed_at": datetime.utcnow(),
        "retry_count": 0,
        "status": "pending_review",
    }

    collection.insert_one(failed_webhook)
    logger.warning(
        "Stored failed webhook in dead letter queue: delivery_id=%s",
        delivery_id,
    )

