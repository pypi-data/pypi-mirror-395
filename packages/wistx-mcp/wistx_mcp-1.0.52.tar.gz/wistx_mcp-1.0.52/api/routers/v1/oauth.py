"""OAuth callback handlers for GitHub integration."""

import base64
import hashlib
import hmac
import logging
import time
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import RedirectResponse
from starlette.requests import Request

from api.auth.oauth import github_oauth_client, get_oauth_backend_callback_url, get_oauth_frontend_redirect_url
from api.dependencies import get_current_user
from api.services.oauth_service import oauth_service
from api.config import settings
from api.models.v1_requests import SelectGitHubOrganizationsRequest

logger = logging.getLogger(__name__)

router = APIRouter()


def encode_user_state(user_id: str, signup: bool = False) -> str:
    """Encode user ID in OAuth state parameter with expiration.
    
    Args:
        user_id: User ID to encode
        signup: Whether this is during signup flow
        
    Returns:
        Encoded state string with timestamp
    """
    timestamp = int(time.time())
    state_data = f"{user_id}:{'signup' if signup else 'connect'}:{timestamp}"
    signature = hmac.new(
        settings.secret_key.encode(),
        state_data.encode(),
        hashlib.sha256
    ).hexdigest()
    encoded = base64.urlsafe_b64encode(f"{state_data}:{signature}".encode()).decode()
    return encoded


def decode_user_state(state: str, max_age_seconds: int = 600) -> tuple[str | None, bool]:
    """Decode user ID from OAuth state parameter with expiration check.
    
    Args:
        state: Encoded state string
        max_age_seconds: Maximum age of state token in seconds (default 10 minutes)
        
    Returns:
        Tuple of (user_id, is_signup) or (None, False) if invalid/expired
    """
    try:
        decoded = base64.urlsafe_b64decode(state.encode()).decode()
        parts = decoded.rsplit(":", 3)
        
        if len(parts) == 3:
            state_data, signature = ":".join(parts[:2]), parts[2]
            expected_signature = hmac.new(
                settings.secret_key.encode(),
                state_data.encode(),
                hashlib.sha256
            ).hexdigest()
            
            if not hmac.compare_digest(signature, expected_signature):
                logger.warning("OAuth state signature validation failed")
                return None, False
            
            user_id, flow_type = state_data.split(":", 1)
            return user_id, flow_type == "signup"
        
        if len(parts) == 4:
            state_data, signature = ":".join(parts[:3]), parts[3]
            expected_signature = hmac.new(
                settings.secret_key.encode(),
                state_data.encode(),
                hashlib.sha256
            ).hexdigest()
            
            if not hmac.compare_digest(signature, expected_signature):
                logger.warning("OAuth state signature validation failed")
                return None, False
            
            state_parts = state_data.split(":", 2)
            if len(state_parts) != 3:
                return None, False
            
            user_id, flow_type, timestamp_str = state_parts
            
            try:
                timestamp = int(timestamp_str)
                age = int(time.time()) - timestamp
                
                if age < 0:
                    logger.warning("OAuth state token has future timestamp (clock skew?)")
                    return None, False
                
                if age > max_age_seconds:
                    logger.warning("OAuth state token expired (age: %d seconds, max: %d)", age, max_age_seconds)
                    return None, False
            except ValueError:
                logger.warning("OAuth state token has invalid timestamp format")
                return None, False
            
            return user_id, flow_type == "signup"
        
        logger.warning("OAuth state token has invalid format (expected 3 or 4 parts, got %d)", len(parts))
        return None, False
    except Exception as e:
        logger.error("Failed to decode state: %s", e, exc_info=True)
        return None, False


def get_v1_oauth_callback_url(provider: str) -> str:
    """Get v1 OAuth callback URL for provider.
    
    This is used for connecting OAuth accounts to existing authenticated users.
    Different from the generic OAuth callback which creates/logs in users.
    
    NOTE: We use the same callback URL as the main OAuth flow (/auth/{provider}/callback)
    and distinguish between flows using the state parameter. This avoids needing to
    register a separate callback URL in GitHub OAuth App settings.
    
    Args:
        provider: OAuth provider name (github)
        
    Returns:
        OAuth callback URL (same as main OAuth flow)
    """
    from api.auth.oauth import get_oauth_backend_callback_url
    
    callback_url = get_oauth_backend_callback_url(provider)
    logger.info(
        "Using OAuth callback URL for v1 flow (same as main OAuth): %s (debug=%s)",
        callback_url,
        settings.debug,
    )
    return callback_url


@router.get("/github/callback")
async def github_oauth_callback(
    code: str = Query(...),
    state: str = Query(None),
    request: Request = None,
) -> RedirectResponse:
    """Handle GitHub OAuth callback.

    This endpoint handles the OAuth callback from GitHub and stores the token
    with the user's account. This is a REQUIRED step in the signup flow.
    Users must connect GitHub to complete signup and enable repository indexing.

    Signup flow order:
    1. OAuth Authentication (Google/GitHub) - creates account
    2. Profile Completion - required
    3. GitHub Repository Connection - required, last step

    Args:
        code: OAuth authorization code
        state: OAuth state (contains encoded user ID and signup flag)

    Returns:
        Redirect response to frontend (onboarding complete or settings)
    """
    if not state:
        logger.warning(
            "SECURITY: GitHub OAuth callback missing state parameter",
            extra={"event": "oauth_state_missing", "provider": "github"},
        )
        frontend_url = get_oauth_frontend_redirect_url("github", request)
        error_url = f"{frontend_url}?error=invalid_state&message=Missing%20state%20parameter"
        return RedirectResponse(url=error_url)

    user_id, is_signup = decode_user_state(state)
    if not user_id:
        logger.warning(
            "SECURITY: GitHub OAuth callback with invalid/expired state",
            extra={"event": "oauth_state_invalid", "provider": "github", "has_state": bool(state)},
        )
        frontend_url = get_oauth_frontend_redirect_url("github", request)
        error_url = f"{frontend_url}?error=invalid_state&message=Invalid%20or%20expired%20state%20parameter"
        return RedirectResponse(url=error_url)
    
    logger.info(
        "GitHub OAuth callback processing for user: %s (signup: %s)",
        user_id,
        is_signup,
        extra={"event": "oauth_callback_start", "provider": "github", "user_id": str(user_id), "is_signup": is_signup},
    )

    try:
        redirect_uri = get_v1_oauth_callback_url("github")
        access_token_response = await github_oauth_client.get_access_token(code, redirect_uri)

        access_token = access_token_response["access_token"]
        refresh_token = access_token_response.get("refresh_token")
        expires_in = access_token_response.get("expires_in")
        scope = access_token_response.get("scope", "repo")

        await oauth_service.store_github_token(
            user_id=str(user_id),
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=expires_in,
            scope=scope,
        )

        try:
            from api.services.github_service import github_service
            organizations = await github_service.list_user_organizations(user_id=str(user_id))
            if organizations:
                await oauth_service.update_github_organizations(
                    user_id=str(user_id),
                    organizations=organizations,
                )
        except Exception as e:
            logger.warning(
                "Failed to fetch organizations after OAuth callback: %s",
                e,
                exc_info=True,
            )

        from api.database.mongodb import mongodb_manager
        from bson import ObjectId
        from datetime import datetime

        db = mongodb_manager.get_database()
        user_doc = db.users.find_one({"_id": ObjectId(user_id)})
        if user_doc and user_doc.get("profile_completed", False):
            db.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"onboarding_completed": True, "updated_at": datetime.utcnow()}},
            )

        logger.info(
            "SECURITY: GitHub OAuth token stored successfully for user: %s",
            user_id,
            extra={"event": "oauth_token_stored", "provider": "github", "user_id": str(user_id), "is_signup": is_signup},
        )
        
        frontend_url = get_oauth_frontend_redirect_url("github", request)
        
        if is_signup:
            redirect_url = f"{frontend_url}?onboarding=true"
        else:
            redirect_url = f"{frontend_url}?connected=true"
        
        return RedirectResponse(url=redirect_url)

    except Exception as e:
        logger.error(
            "SECURITY: GitHub OAuth callback error: %s",
            e,
            exc_info=True,
            extra={"event": "oauth_callback_error", "provider": "github", "user_id": str(user_id) if user_id else None},
        )
        
        frontend_url = get_oauth_frontend_redirect_url("github", request)
        if "?" in frontend_url:
            frontend_url += "&github=error"
        else:
            frontend_url += "?github=error"
        return RedirectResponse(url=frontend_url)


@router.get("/github/authorize")
async def github_oauth_authorize(
    signup: bool = Query(default=False, description="True if this is during signup flow"),
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """Get GitHub OAuth authorization URL.

    This is a REQUIRED step in the signup flow. Users must connect GitHub
    to complete signup and enable repository indexing.

    Signup flow order:
    1. OAuth Authentication (Google/GitHub) - creates account
    2. Profile Completion - required
    3. GitHub Repository Connection - required, last step

    Args:
        signup: True if this is during signup flow (sets state for callback)
        current_user: Current authenticated user

    Returns:
        Authorization URL with appropriate state
    """
    user_id = current_user.get("user_id")
    if not user_id:
        logger.warning(
            "SECURITY: GitHub OAuth authorize attempt without authentication",
            extra={"event": "oauth_authorize_unauthorized", "provider": "github"},
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated",
        )
    
    logger.info(
        "GitHub OAuth authorization requested for user: %s (signup: %s)",
        user_id,
        signup,
        extra={"event": "oauth_authorize", "provider": "github", "user_id": str(user_id), "is_signup": signup},
    )
    
    oauth_state = encode_user_state(str(user_id), signup=signup)
    
    redirect_uri = get_v1_oauth_callback_url("github")
    
    authorization_url = await github_oauth_client.get_authorization_url(
        redirect_uri=redirect_uri,
        scope=["repo", "read:org"],
        state=oauth_state,
    )

    return {
        "authorization_url": authorization_url,
        "message": "Connect GitHub to complete signup and enable repository indexing" if signup else "Visit this URL to authorize GitHub access",
        "required": True,
        "step": "last" if signup else None,
    }


@router.get("/github/status")
async def github_oauth_status(
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """Check GitHub OAuth connection status.

    Args:
        current_user: Current authenticated user

    Returns:
        Connection status
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated",
        )

    has_token = await oauth_service.has_github_token(str(user_id))

    return {
        "connected": has_token,
        "required": True,
        "message": "GitHub connected" if has_token else "GitHub connection required to complete signup",
        "authorization_url": "/v1/oauth/github/authorize" if not has_token else None,
    }


@router.get("/github/repositories")
async def list_user_repositories(
    include_private: bool = Query(default=True, description="Include private repositories"),
    limit: int = Query(default=100, ge=1, le=500, description="Maximum number of repositories"),
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """List user's GitHub repositories.

    Uses the user's GitHub OAuth token to fetch their repositories from GitHub API.
    This allows users to discover and select repositories to index.

    Args:
        include_private: Include private repositories
        limit: Maximum number of repositories to return
        current_user: Current authenticated user

    Returns:
        Dictionary with list of repositories and metadata
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated",
        )

    from api.services.github_service import github_service

    try:
        repos = await github_service.list_user_repositories(
            user_id=str(user_id),
            include_private=include_private,
            limit=limit,
        )

        return {
            "repositories": repos,
            "total": len(repos),
            "include_private": include_private,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "GITHUB_OAUTH_REQUIRED",
                "message": str(e),
                "authorization_url": "/v1/oauth/github/authorize",
            },
        ) from e
    except Exception as e:
        logger.error("Error listing repositories: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve repositories",
        ) from e


@router.delete("/github/disconnect")
async def github_oauth_disconnect(
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """Disconnect GitHub OAuth.

    Args:
        current_user: Current authenticated user

    Returns:
        Success message
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated",
        )

    await oauth_service.revoke_github_token(str(user_id))

    return {
        "message": "GitHub disconnected successfully",
    }


@router.get("/github/organizations")
async def list_github_organizations(
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """List user's GitHub organizations.

    Uses the user's GitHub OAuth token to fetch their organizations from GitHub API.

    Args:
        current_user: Current authenticated user

    Returns:
        Dictionary with list of organizations and metadata
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated",
        )

    from api.services.github_service import github_service
    from api.services.oauth_service import oauth_service

    try:
        orgs = await github_service.list_user_organizations(user_id=str(user_id))
        selected_orgs = await oauth_service.get_selected_organizations(user_id=str(user_id))

        return {
            "organizations": orgs,
            "total": len(orgs),
            "selected_organizations": selected_orgs,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "GITHUB_OAUTH_REQUIRED",
                "message": str(e),
                "authorization_url": "/v1/oauth/github/authorize",
            },
        ) from e
    except Exception as e:
        logger.error("Error listing organizations: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve organizations",
        ) from e


@router.post("/github/organizations/select")
async def select_github_organizations(
    request: SelectGitHubOrganizationsRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """Select which GitHub organizations to grant access.

    Args:
        request: Request containing list of organization login names to select
        current_user: Current authenticated user

    Returns:
        Success message
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated",
        )

    organization_logins = request.organization_logins

    if not organization_logins:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one organization must be selected",
        )

    try:
        await oauth_service.select_github_organizations(
            user_id=str(user_id),
            organization_logins=organization_logins,
        )

        return {
            "message": f"Selected {len(organization_logins)} organization(s)",
            "selected_organizations": organization_logins,
        }

    except Exception as e:
        logger.error("Error selecting organizations: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to select organizations",
        ) from e


@router.get("/github/organizations/{org_login}/repositories")
async def list_organization_repositories(
    org_login: str,
    include_private: bool = Query(default=True, description="Include private repositories"),
    limit: int = Query(default=100, ge=1, le=500, description="Maximum number of repositories"),
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """List repositories for a specific GitHub organization.

    Args:
        org_login: Organization login name
        include_private: Include private repositories
        limit: Maximum number of repositories to return
        current_user: Current authenticated user

    Returns:
        Dictionary with list of repositories and metadata
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated",
        )

    from api.services.github_service import github_service

    try:
        repos = await github_service.list_organization_repositories(
            user_id=str(user_id),
            org_login=org_login,
            include_private=include_private,
            limit=limit,
        )

        return {
            "repositories": repos,
            "organization": org_login,
            "total": len(repos),
            "include_private": include_private,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "GITHUB_OAUTH_REQUIRED",
                "message": str(e),
                "authorization_url": "/v1/oauth/github/authorize",
            },
        ) from e
    except Exception as e:
        logger.error("Error listing organization repositories: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve organization repositories",
        ) from e


@router.post("/github/refresh-permissions")
async def refresh_github_permissions(
    current_user: dict[str, Any] = Depends(get_current_user),
    request: Request = None,
) -> dict[str, Any]:
    """Refresh GitHub OAuth permissions.

    Generates a new authorization URL to re-authorize with updated scopes.
    This allows users to grant access to additional organizations.

    Args:
        current_user: Current authenticated user

    Returns:
        Authorization URL for permission refresh
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated",
        )

    oauth_state = encode_user_state(str(user_id), signup=False)
    redirect_uri = get_v1_oauth_callback_url("github")

    authorization_url = await github_oauth_client.get_authorization_url(
        redirect_uri=redirect_uri,
        scope=["repo", "read:org"],
        state=oauth_state,
    )

    frontend_url = get_oauth_frontend_redirect_url("github", request)
    if "?" in frontend_url:
        callback_url = f"{frontend_url}&refresh=organizations"
    else:
        callback_url = f"{frontend_url}?refresh=organizations"

    return {
        "authorization_url": authorization_url,
        "callback_url": callback_url,
        "message": "Visit this URL to refresh GitHub permissions and grant access to additional organizations",
        "scopes": ["repo", "read:org"],
    }

