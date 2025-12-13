"""End-to-end validation script for authentication and onboarding flow.

This script validates:
1. OAuth authentication flow (Google/GitHub)
2. Profile completion flow
3. GitHub connection flow
4. State management and transitions
5. Security validations
6. Error handling
"""

import asyncio
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from bson import ObjectId

from api.auth.database import MongoDBUserDatabase
from api.auth.users import UserManager
from api.config import settings
from api.database.async_mongodb import async_mongodb_adapter
from api.models.user_profile import ProfileCompletionRequest
from api.routers.v1.oauth import decode_user_state, encode_user_state
from api.services.oauth_service import oauth_service
from api.services.user_profile_service import user_profile_service

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class ValidationResult:
    """Validation result container."""

    def __init__(self, name: str):
        self.name = name
        self.passed = True
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.info: list[str] = []

    def fail(self, message: str):
        """Mark validation as failed."""
        self.passed = False
        self.errors.append(message)
        logger.error("❌ %s: %s", self.name, message)

    def warn(self, message: str):
        """Add warning."""
        self.warnings.append(message)
        logger.warning("⚠️  %s: %s", self.name, message)

    def info_msg(self, message: str):
        """Add info message."""
        self.info.append(message)
        logger.info("ℹ️  %s: %s", self.name, message)

    def success(self, message: str):
        """Mark validation as successful."""
        self.info.append(message)
        logger.info("✅ %s: %s", self.name, message)


async def validate_secret_key():
    """Validate secret key configuration."""
    result = ValidationResult("Secret Key Validation")

    secret_key_value = settings.secret_key
    secret_key_length = len(secret_key_value)
    
    if secret_key_value == "your-secret-key-change-in-production":
        result.fail("SECRET_KEY is still using default value. Please update SECRET_KEY in .env file.")
        result.info_msg("Generate a secure key with: python -c 'import secrets; print(secrets.token_urlsafe(32))'")
    elif secret_key_length < 32:
        result.fail(f"SECRET_KEY is too short ({secret_key_length} chars, need 32+). Please update SECRET_KEY in .env file.")
    else:
        result.success(f"SECRET_KEY is properly configured ({secret_key_length} chars)")
        result.info_msg(f"SECRET_KEY starts with: {secret_key_value[:8]}...")

    return result


async def validate_oauth_state_encoding():
    """Validate OAuth state token encoding/decoding."""
    result = ValidationResult("OAuth State Encoding")

    test_user_id = "507f1f77bcf86cd799439011"
    test_signup = True

    try:
        encoded = encode_user_state(test_user_id, signup=test_signup)
        result.info_msg(f"Encoded state: {encoded[:50]}...")

        user_id, is_signup = decode_user_state(encoded)

        if user_id != test_user_id:
            result.fail(f"User ID mismatch: expected {test_user_id}, got {user_id}")
        elif is_signup != test_signup:
            result.fail(f"Signup flag mismatch: expected {test_signup}, got {is_signup}")
        else:
            result.success("State encoding/decoding works correctly")

        invalid_state = "invalid_state_token"
        user_id_invalid, _ = decode_user_state(invalid_state)
        if user_id_invalid is not None:
            result.fail("Invalid state token was accepted (should return None)")
        else:
            result.success("Invalid state tokens are properly rejected")

    except Exception as e:
        result.fail(f"State encoding/decoding failed: {e}")

    return result


async def validate_oauth_state_expiration():
    """Validate OAuth state token expiration."""
    result = ValidationResult("OAuth State Expiration")

    test_user_id = "507f1f77bcf86cd799439011"

    try:
        encoded = encode_user_state(test_user_id, signup=False)
        user_id, _ = decode_user_state(encoded, max_age_seconds=600)

        if user_id != test_user_id:
            result.fail(f"Fresh state token failed: expected {test_user_id}, got {user_id}")
        else:
            result.success("Fresh state tokens are accepted")

        import time
        import base64
        import hashlib
        import hmac

        old_timestamp = int(time.time()) - 700
        old_state_data = f"{test_user_id}:connect:{old_timestamp}"
        old_signature = hmac.new(
            settings.secret_key.encode(),
            old_state_data.encode(),
            hashlib.sha256
        ).hexdigest()
        old_encoded = base64.urlsafe_b64encode(f"{old_state_data}:{old_signature}".encode()).decode()

        user_id_old, _ = decode_user_state(old_encoded, max_age_seconds=600)
        if user_id_old is not None:
            result.fail("Expired state token was accepted (should return None)")
        else:
            result.success("Expired state tokens are properly rejected")

    except Exception as e:
        result.fail(f"State expiration validation failed: {e}")

    return result


async def validate_profile_completion():
    """Validate profile completion flow."""
    result = ValidationResult("Profile Completion Flow")

    await async_mongodb_adapter.connect()
    db = async_mongodb_adapter.get_database()
    collection = db.users

    test_user_id = None
    try:
        test_user = await collection.find_one({"email": "test-validation@example.com"})
        if test_user:
            test_user_id = str(test_user["_id"])
        else:
            result.warn("No test user found, creating one...")
            test_user_doc = {
                "_id": ObjectId(),
                "email": "test-validation@example.com",
                "is_active": True,
                "is_verified": False,
                "is_superuser": False,
                "plan": "free",
                "profile_completed": False,
                "oauth_accounts": [],
            }
            await collection.insert_one(test_user_doc)
            test_user_id = str(test_user_doc["_id"])

        user_db = MongoDBUserDatabase(collection)
        user_manager = UserManager(user_db)
        user = await user_manager.get(ObjectId(test_user_id))

        if not user:
            result.fail(f"Test user not found: {test_user_id}")
            return result

        status_before = await user_profile_service.check_completion_status(test_user_id)
        if status_before.profile_completed:
            result.warn("Test user already has completed profile, resetting...")
            await collection.update_one(
                {"_id": ObjectId(test_user_id)},
                {"$set": {"profile_completed": False, "full_name": None, "role": None, "referral_source": None}}
            )

        profile_data = ProfileCompletionRequest(
            full_name="Test User",
            role="DevOps Engineer",
            organization_name="Test Org",
            referral_source="Google Search",
        )

        try:
            completed_profile = await user_profile_service.complete_profile(test_user_id, profile_data)
            if not completed_profile.profile_completed:
                result.fail("Profile completion did not set profile_completed flag")
            elif completed_profile.full_name != "Test User":
                result.fail(f"Profile name mismatch: expected 'Test User', got '{completed_profile.full_name}'")
            else:
                result.success("Profile completion works correctly")

            status_after = await user_profile_service.check_completion_status(test_user_id)
            if not status_after.profile_completed:
                result.fail("Profile status check shows incomplete after completion")
            elif len(status_after.missing_fields) > 0:
                result.fail(f"Profile status shows missing fields after completion: {status_after.missing_fields}")
            else:
                result.success("Profile status check works correctly")

            try:
                await user_profile_service.complete_profile(test_user_id, profile_data)
                result.fail("Profile completion allowed duplicate completion")
            except ValueError as e:
                if "already completed" in str(e).lower():
                    result.success("Duplicate profile completion is properly prevented")
                else:
                    result.fail(f"Unexpected error on duplicate completion: {e}")

        except Exception as e:
            result.fail(f"Profile completion failed: {e}")

    except Exception as e:
        result.fail(f"Profile completion validation failed: {e}")

    return result


async def validate_signup_next_step():
    """Validate signup next step logic."""
    result = ValidationResult("Signup Next Step Logic")

    await async_mongodb_adapter.connect()
    db = async_mongodb_adapter.get_database()
    collection = db.users

    try:
        test_user = await collection.find_one({"email": "test-nextstep@example.com"})
        if not test_user:
            test_user_doc = {
                "_id": ObjectId(),
                "email": "test-nextstep@example.com",
                "is_active": True,
                "is_verified": False,
                "is_superuser": False,
                "plan": "free",
                "profile_completed": False,
                "oauth_accounts": [],
            }
            await collection.insert_one(test_user_doc)
            test_user_id = str(test_user_doc["_id"])
        else:
            test_user_id = str(test_user["_id"])

        await collection.update_one(
            {"_id": ObjectId(test_user_id)},
            {"$set": {"profile_completed": False}, "$unset": {"github_oauth_token": ""}}
        )

        status = await user_profile_service.check_completion_status(test_user_id)
        has_github = await oauth_service.has_github_token(test_user_id)

        if status.profile_completed:
            result.fail("User should not have completed profile")
        elif has_github:
            result.fail("User should not have GitHub token")
        else:
            result.success("Test user state initialized correctly")

        if not status.profile_completed:
            result.info_msg("Next step should be 'profile'")
        elif not has_github:
            result.info_msg("Next step should be 'github'")
        else:
            result.info_msg("Next step should be 'complete'")

    except Exception as e:
        result.fail(f"Signup next step validation failed: {e}")

    return result


async def validate_github_oauth_flow():
    """Validate GitHub OAuth flow logic."""
    result = ValidationResult("GitHub OAuth Flow")

    try:
        test_user_id = "507f1f77bcf86cd799439011"

        state = encode_user_state(test_user_id, signup=True)
        decoded_user_id, is_signup = decode_user_state(state)

        if decoded_user_id != test_user_id:
            result.fail(f"State decode failed: expected {test_user_id}, got {decoded_user_id}")
        elif not is_signup:
            result.fail("Signup flag not set correctly")
        else:
            result.success("GitHub OAuth state encoding works correctly")

        state_connect = encode_user_state(test_user_id, signup=False)
        decoded_user_id_connect, is_signup_connect = decode_user_state(state_connect)

        if decoded_user_id_connect != test_user_id:
            result.fail(f"Connect state decode failed: expected {test_user_id}, got {decoded_user_id_connect}")
        elif is_signup_connect:
            result.fail("Connect flow incorrectly marked as signup")
        else:
            result.success("GitHub OAuth connect state encoding works correctly")

    except Exception as e:
        result.fail(f"GitHub OAuth flow validation failed: {e}")

    return result


async def validate_error_handling():
    """Validate error handling in auth flow."""
    result = ValidationResult("Error Handling")

    try:
        invalid_user_id = "invalid_user_id_format"
        try:
            await async_mongodb_adapter.connect()
            db = async_mongodb_adapter.get_database()
            collection = db.users
            user_db = MongoDBUserDatabase(collection)
            user_manager = UserManager(user_db)

            user = await user_manager.get(invalid_user_id)
            if user is not None:
                result.warn("Invalid user ID format was accepted")
            else:
                result.success("Invalid user ID format is properly rejected")
        except ValueError:
            result.success("Invalid user ID format raises ValueError")
        except Exception as e:
            result.warn(f"Unexpected error handling for invalid user ID: {e}")

        from pydantic import ValidationError

        try:
            ProfileCompletionRequest(
                full_name="A",
                role="Invalid Role",
                referral_source="Invalid Source",
            )
            result.fail("Invalid profile data was accepted (should raise ValidationError)")
        except ValidationError:
            result.success("Invalid profile data is properly rejected by Pydantic")
        except Exception as e:
            result.warn(f"Unexpected error handling for invalid profile: {e}")

    except Exception as e:
        result.fail(f"Error handling validation failed: {e}")

    return result


async def validate_security_logging():
    """Validate security event logging."""
    result = ValidationResult("Security Logging")

    try:
        oauth_logger = logging.getLogger("api.routers.v1.oauth")
        log_handlers = oauth_logger.handlers
        if not log_handlers:
            result.warn("No log handlers configured for OAuth router")
        else:
            result.success("Log handlers are configured")

        log_level = logging.getLogger("api.routers.v1.oauth").level
        if log_level > logging.INFO:
            result.warn(f"OAuth router log level is {log_level}, may miss security events")
        else:
            result.success(f"OAuth router log level is appropriate ({log_level})")

    except Exception as e:
        result.fail(f"Security logging validation failed: {e}")

    return result


async def validate_database_operations():
    """Validate database operations."""
    result = ValidationResult("Database Operations")

    try:
        await async_mongodb_adapter.connect()
        db = async_mongodb_adapter.get_database()

        if db is None:
            result.fail("Database connection failed")
            return result

        result.success("Database connection successful")

        collection = db.users
        user_count = await collection.count_documents({})
        result.info_msg(f"Found {user_count} users in database")

        test_user = await collection.find_one({"email": "test-validation@example.com"})
        if test_user:
            result.info_msg("Test user exists in database")
        else:
            result.warn("Test user not found (may need to be created)")

    except Exception as e:
        result.fail(f"Database operations validation failed: {e}")

    return result


async def run_all_validations():
    """Run all validation tests."""
    logger.info("=" * 80)
    logger.info("Starting End-to-End Authentication & Onboarding Validation")
    logger.info("=" * 80)

    validations = [
        validate_secret_key(),
        validate_oauth_state_encoding(),
        validate_oauth_state_expiration(),
        validate_profile_completion(),
        validate_signup_next_step(),
        validate_github_oauth_flow(),
        validate_error_handling(),
        validate_security_logging(),
        validate_database_operations(),
    ]

    results = await asyncio.gather(*validations)

    logger.info("")
    logger.info("=" * 80)
    logger.info("Validation Summary")
    logger.info("=" * 80)

    passed = 0
    failed = 0
    warnings_count = 0

    for result in results:
        if result.passed:
            passed += 1
        else:
            failed += 1
        warnings_count += len(result.warnings)

        logger.info("")
        logger.info(f"📋 {result.name}: {'✅ PASSED' if result.passed else '❌ FAILED'}")
        if result.errors:
            for error in result.errors:
                logger.error(f"   ❌ {error}")
        if result.warnings:
            for warning in result.warnings:
                logger.warning(f"   ⚠️  {warning}")
        if result.info:
            for info in result.info[:3]:
                logger.info(f"   ℹ️  {info}")

    logger.info("")
    logger.info("=" * 80)
    logger.info(f"Total: {len(results)} validations")
    logger.info(f"✅ Passed: {passed}")
    logger.info(f"❌ Failed: {failed}")
    logger.info(f"⚠️  Warnings: {warnings_count}")
    logger.info("=" * 80)

    if failed > 0:
        logger.error("")
        logger.error("❌ VALIDATION FAILED - Please review errors above")
        return False
    elif warnings_count > 0:
        logger.warning("")
        logger.warning("⚠️  VALIDATION PASSED WITH WARNINGS - Please review warnings above")
        return True
    else:
        logger.info("")
        logger.info("✅ ALL VALIDATIONS PASSED")
        return True


if __name__ == "__main__":
    success = asyncio.run(run_all_validations())
    exit(0 if success else 1)

