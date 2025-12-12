"""Secure token encryption with unique salts per token."""

import base64
import hashlib
import logging
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from api.config import settings

logger = logging.getLogger(__name__)


class TokenEncryptionService:
    """Service for encrypting/decrypting tokens with unique salts."""

    @staticmethod
    def _derive_key(salt: bytes) -> bytes:
        """Derive encryption key from salt.

        Args:
            salt: Unique salt for this token

        Returns:
            Fernet key
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(
            kdf.derive(settings.secret_key.encode())
        )
        return key

    @staticmethod
    def encrypt_token(token: str, resource_id: str) -> str:
        """Encrypt token with resource-specific salt.

        Args:
            token: Plain token to encrypt
            resource_id: Resource ID used to generate unique salt

        Returns:
            Encrypted token with salt prefix
        """
        salt = hashlib.sha256(
            f"{resource_id}:{settings.secret_key}".encode()
        ).digest()[:16]

        key = TokenEncryptionService._derive_key(salt)
        fernet = Fernet(key)
        encrypted = fernet.encrypt(token.encode())

        salt_b64 = base64.urlsafe_b64encode(salt).decode()
        encrypted_b64 = base64.urlsafe_b64encode(encrypted).decode()

        return f"{salt_b64}:{encrypted_b64}"

    @staticmethod
    def decrypt_token(encrypted_token: str, resource_id: str) -> str:
        """Decrypt token.

        Args:
            encrypted_token: Encrypted token with salt prefix
            resource_id: Resource ID used to verify salt

        Returns:
            Plain token

        Raises:
            ValueError: If decryption fails or salt mismatch
        """
        try:
            parts = encrypted_token.split(":", 1)
            if len(parts) != 2:
                raise ValueError("Invalid encrypted token format")

            salt_b64, encrypted_b64 = parts
            salt = base64.urlsafe_b64decode(salt_b64)
            encrypted = base64.urlsafe_b64decode(encrypted_b64)

            expected_salt = hashlib.sha256(
                f"{resource_id}:{settings.secret_key}".encode()
            ).digest()[:16]

            if salt != expected_salt:
                raise ValueError("Salt mismatch - token may be corrupted")

            key = TokenEncryptionService._derive_key(salt)
            fernet = Fernet(key)
            return fernet.decrypt(encrypted).decode()

        except Exception as e:
            logger.error("Token decryption failed: %s", e)
            raise ValueError(f"Failed to decrypt token: {e}") from e

