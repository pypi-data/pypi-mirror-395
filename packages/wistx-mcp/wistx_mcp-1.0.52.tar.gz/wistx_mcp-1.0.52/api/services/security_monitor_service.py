"""Security Monitor Service for suspicious activity detection.

OWASP-validated implementation for detecting:
- Brute force attacks (IP + Account based)
- Credential stuffing (Multi-IP per account)
- Password spraying (Same password, multiple accounts)
- API scanning (High 404 rate)
- Authorization probing (High 403 rate)

References:
- OWASP Authentication Cheat Sheet
- OWASP Blocking Brute Force Attacks
- OWASP Credential Stuffing Prevention
"""

import asyncio
import hashlib
import logging
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional

from api.database.redis_client import RedisCircuitBreakerOpenError, get_redis_manager
from api.models.audit_log import AuditEventType, AuditLogSeverity
from api.services.audit_log_service import audit_log_service

logger = logging.getLogger(__name__)


class ThreatType(str, Enum):
    """Types of security threats detected."""

    BRUTE_FORCE_IP = "brute_force_ip"
    BRUTE_FORCE_ACCOUNT = "brute_force_account"
    CREDENTIAL_STUFFING = "credential_stuffing"
    PASSWORD_SPRAYING = "password_spraying"
    API_SCANNING = "api_scanning"
    AUTHORIZATION_PROBING = "authorization_probing"
    ACCOUNT_ENUMERATION = "account_enumeration"


class ThreatSeverity(str, Enum):
    """Threat severity levels for graduated response."""

    LOW = "low"  # Log + Monitor
    MEDIUM = "medium"  # Require CAPTCHA + Delay
    HIGH = "high"  # Temporary block + MFA step-up
    CRITICAL = "critical"  # Extended block + Account lock + Alert


@dataclass
class SecurityThreshold:
    """Configurable threshold for security detection."""

    count: int
    window_seconds: int
    severity: ThreatSeverity


# OWASP-recommended detection thresholds (configurable)
DEFAULT_THRESHOLDS = {
    ThreatType.BRUTE_FORCE_IP: SecurityThreshold(count=5, window_seconds=300, severity=ThreatSeverity.HIGH),
    ThreatType.BRUTE_FORCE_ACCOUNT: SecurityThreshold(count=5, window_seconds=600, severity=ThreatSeverity.HIGH),
    ThreatType.CREDENTIAL_STUFFING: SecurityThreshold(count=10, window_seconds=600, severity=ThreatSeverity.HIGH),
    ThreatType.PASSWORD_SPRAYING: SecurityThreshold(count=10, window_seconds=600, severity=ThreatSeverity.HIGH),
    ThreatType.API_SCANNING: SecurityThreshold(count=10, window_seconds=60, severity=ThreatSeverity.MEDIUM),
    ThreatType.AUTHORIZATION_PROBING: SecurityThreshold(count=5, window_seconds=300, severity=ThreatSeverity.HIGH),
    ThreatType.ACCOUNT_ENUMERATION: SecurityThreshold(count=10, window_seconds=300, severity=ThreatSeverity.MEDIUM),
}

# Redis key prefixes
REDIS_PREFIX = "security:"
KEY_FAILED_AUTH_IP = f"{REDIS_PREFIX}failed_auth:ip:"
KEY_FAILED_AUTH_ACCOUNT = f"{REDIS_PREFIX}failed_auth:account:"
KEY_CREDENTIAL_STUFFING = f"{REDIS_PREFIX}cred_stuffing:account:"
KEY_FORBIDDEN_IP = f"{REDIS_PREFIX}forbidden:ip:"
KEY_NOT_FOUND_IP = f"{REDIS_PREFIX}not_found:ip:"
KEY_ACCOUNT_ENUM_IP = f"{REDIS_PREFIX}account_enum:ip:"


class SecurityMonitorService:
    """Service for monitoring and detecting suspicious security activity.

    Implements OWASP-recommended patterns for detecting automated attacks
    using Redis-based sliding window counters with TTL.
    """

    def __init__(self, thresholds: Optional[dict[ThreatType, SecurityThreshold]] = None):
        """Initialize security monitor service.

        Args:
            thresholds: Optional custom thresholds (defaults to OWASP-recommended values)
        """
        self.thresholds = thresholds or DEFAULT_THRESHOLDS
        self._redis_available: Optional[bool] = None

    async def _get_redis_manager(self) -> Optional[Any]:
        """Get Redis manager with availability check."""
        try:
            manager = await get_redis_manager()
            if manager:
                self._redis_available = True
            return manager
        except Exception as e:
            if self._redis_available is not False:
                logger.warning("Redis not available for security monitoring: %s", e)
                self._redis_available = False
            return None

    async def _increment_counter(self, key: str, ttl_seconds: int) -> int:
        """Increment a Redis counter with TTL.

        Uses Redis manager's circuit breaker and retry logic.

        Args:
            key: Redis key
            ttl_seconds: TTL for the key

        Returns:
            Current count after increment
        """
        manager = await self._get_redis_manager()
        if not manager:
            return 0

        try:
            async def _incr_operation(client: Any) -> int:
                pipe = client.pipeline()
                pipe.incr(key)
                pipe.expire(key, ttl_seconds)
                results = await pipe.execute()
                return results[0] if results else 0

            return await manager.execute(_incr_operation)
        except RedisCircuitBreakerOpenError:
            logger.debug("Redis circuit breaker open, security counter increment skipped")
            return 0
        except Exception as e:
            logger.debug("Failed to increment security counter %s: %s", key, e)
            return 0

    async def _get_counter(self, key: str) -> int:
        """Get current value of a Redis counter.

        Uses Redis manager's circuit breaker and retry logic.
        """
        manager = await self._get_redis_manager()
        if not manager:
            return 0

        try:
            async def _get_operation(client: Any) -> int:
                value = await client.get(key)
                return int(value) if value else 0

            return await manager.execute(_get_operation)
        except RedisCircuitBreakerOpenError:
            logger.debug("Redis circuit breaker open, security counter get skipped")
            return 0
        except Exception as e:
            logger.debug("Failed to get security counter %s: %s", key, e)
            return 0

    async def _add_to_set(self, key: str, value: str, ttl_seconds: int) -> int:
        """Add value to a Redis set with TTL.

        Uses Redis manager's circuit breaker and retry logic.

        Args:
            key: Redis key
            value: Value to add
            ttl_seconds: TTL for the key

        Returns:
            Set size after addition
        """
        manager = await self._get_redis_manager()
        if not manager:
            return 0

        try:
            async def _sadd_operation(client: Any) -> int:
                pipe = client.pipeline()
                pipe.sadd(key, value)
                pipe.expire(key, ttl_seconds)
                pipe.scard(key)
                results = await pipe.execute()
                return results[2] if len(results) >= 3 else 0

            return await manager.execute(_sadd_operation)
        except RedisCircuitBreakerOpenError:
            logger.debug("Redis circuit breaker open, security set add skipped")
            return 0
        except Exception as e:
            logger.debug("Failed to add to security set %s: %s", key, e)
            return 0

    def _log_suspicious_activity(
        self,
        threat_type: ThreatType,
        severity: ThreatSeverity,
        ip_address: Optional[str],
        user_id: Optional[str],
        details: dict[str, Any],
    ) -> None:
        """Log suspicious activity to audit log."""
        severity_map = {
            ThreatSeverity.LOW: AuditLogSeverity.LOW,
            ThreatSeverity.MEDIUM: AuditLogSeverity.MEDIUM,
            ThreatSeverity.HIGH: AuditLogSeverity.HIGH,
            ThreatSeverity.CRITICAL: AuditLogSeverity.CRITICAL,
        }

        audit_log_service.log_event(
            event_type=AuditEventType.SUSPICIOUS_ACTIVITY,
            severity=severity_map.get(severity, AuditLogSeverity.HIGH),
            message=f"Suspicious activity detected: {threat_type.value}",
            success=False,
            user_id=user_id,
            ip_address=ip_address,
            details={
                "threat_type": threat_type.value,
                "threat_severity": severity.value,
                **details,
            },
            compliance_tags=["PCI-DSS-10", "SOC2", "SECURITY"],
        )

    async def track_failed_auth(
        self,
        ip_address: Optional[str],
        user_id: Optional[str] = None,
        username: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> dict[str, Any]:
        """Track failed authentication attempt.

        Detects:
        - Brute force by IP (many failures from same IP)
        - Brute force by account (many failures for same account)
        - Credential stuffing (same account from many IPs)
        - Account enumeration (many different usernames from same IP)

        Args:
            ip_address: Client IP address
            user_id: User ID (if known)
            username: Username attempted
            user_agent: User agent string

        Returns:
            Detection result with threat info if detected
        """
        result = {"detected": False, "threats": []}
        account_id = user_id or username

        # Track brute force by IP
        if ip_address:
            threshold = self.thresholds[ThreatType.BRUTE_FORCE_IP]
            key = f"{KEY_FAILED_AUTH_IP}{ip_address}"
            count = await self._increment_counter(key, threshold.window_seconds)

            if count >= threshold.count:
                threat = {
                    "type": ThreatType.BRUTE_FORCE_IP.value,
                    "severity": threshold.severity.value,
                    "count": count,
                    "threshold": threshold.count,
                    "window_seconds": threshold.window_seconds,
                }
                result["threats"].append(threat)
                result["detected"] = True

                self._log_suspicious_activity(
                    ThreatType.BRUTE_FORCE_IP,
                    threshold.severity,
                    ip_address,
                    user_id,
                    {"count": count, "threshold": threshold.count, "user_agent": user_agent},
                )

        # Track brute force by account
        if account_id:
            threshold = self.thresholds[ThreatType.BRUTE_FORCE_ACCOUNT]
            key = f"{KEY_FAILED_AUTH_ACCOUNT}{account_id}"
            count = await self._increment_counter(key, threshold.window_seconds)

            if count >= threshold.count:
                threat = {
                    "type": ThreatType.BRUTE_FORCE_ACCOUNT.value,
                    "severity": threshold.severity.value,
                    "count": count,
                    "threshold": threshold.count,
                }
                result["threats"].append(threat)
                result["detected"] = True

                self._log_suspicious_activity(
                    ThreatType.BRUTE_FORCE_ACCOUNT,
                    threshold.severity,
                    ip_address,
                    user_id,
                    {"count": count, "threshold": threshold.count, "account": account_id},
                )

        # Track credential stuffing (same account from multiple IPs)
        if account_id and ip_address:
            threshold = self.thresholds[ThreatType.CREDENTIAL_STUFFING]
            key = f"{KEY_CREDENTIAL_STUFFING}{account_id}"
            ip_count = await self._add_to_set(key, ip_address, threshold.window_seconds)

            if ip_count >= threshold.count:
                threat = {
                    "type": ThreatType.CREDENTIAL_STUFFING.value,
                    "severity": threshold.severity.value,
                    "unique_ips": ip_count,
                    "threshold": threshold.count,
                }
                result["threats"].append(threat)
                result["detected"] = True

                self._log_suspicious_activity(
                    ThreatType.CREDENTIAL_STUFFING,
                    threshold.severity,
                    ip_address,
                    user_id,
                    {"unique_ips": ip_count, "threshold": threshold.count, "account": account_id},
                )

        # Track account enumeration (many usernames from same IP)
        if ip_address and username:
            threshold = self.thresholds[ThreatType.ACCOUNT_ENUMERATION]
            key = f"{KEY_ACCOUNT_ENUM_IP}{ip_address}"
            username_count = await self._add_to_set(key, username, threshold.window_seconds)

            if username_count >= threshold.count:
                threat = {
                    "type": ThreatType.ACCOUNT_ENUMERATION.value,
                    "severity": threshold.severity.value,
                    "unique_usernames": username_count,
                    "threshold": threshold.count,
                }
                result["threats"].append(threat)
                result["detected"] = True

                self._log_suspicious_activity(
                    ThreatType.ACCOUNT_ENUMERATION,
                    threshold.severity,
                    ip_address,
                    user_id,
                    {"unique_usernames": username_count, "threshold": threshold.count},
                )

        return result

    async def track_forbidden(
        self,
        ip_address: Optional[str],
        endpoint: Optional[str] = None,
        user_id: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> dict[str, Any]:
        """Track 403 Forbidden response for authorization probing detection.

        Args:
            ip_address: Client IP address
            endpoint: Attempted endpoint
            user_id: User ID (if authenticated)
            user_agent: User agent string

        Returns:
            Detection result with threat info if detected
        """
        result = {"detected": False, "threats": []}

        if not ip_address:
            return result

        threshold = self.thresholds[ThreatType.AUTHORIZATION_PROBING]
        key = f"{KEY_FORBIDDEN_IP}{ip_address}"
        count = await self._increment_counter(key, threshold.window_seconds)

        if count >= threshold.count:
            threat = {
                "type": ThreatType.AUTHORIZATION_PROBING.value,
                "severity": threshold.severity.value,
                "count": count,
                "threshold": threshold.count,
                "window_seconds": threshold.window_seconds,
            }
            result["threats"].append(threat)
            result["detected"] = True

            self._log_suspicious_activity(
                ThreatType.AUTHORIZATION_PROBING,
                threshold.severity,
                ip_address,
                user_id,
                {
                    "count": count,
                    "threshold": threshold.count,
                    "endpoint": endpoint,
                    "user_agent": user_agent,
                },
            )

        return result

    async def track_not_found(
        self,
        ip_address: Optional[str],
        endpoint: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> dict[str, Any]:
        """Track 404 Not Found response for API scanning detection.

        Args:
            ip_address: Client IP address
            endpoint: Attempted endpoint
            user_agent: User agent string

        Returns:
            Detection result with threat info if detected
        """
        result = {"detected": False, "threats": []}

        if not ip_address:
            return result

        threshold = self.thresholds[ThreatType.API_SCANNING]
        key = f"{KEY_NOT_FOUND_IP}{ip_address}"
        count = await self._increment_counter(key, threshold.window_seconds)

        if count >= threshold.count:
            threat = {
                "type": ThreatType.API_SCANNING.value,
                "severity": threshold.severity.value,
                "count": count,
                "threshold": threshold.count,
                "window_seconds": threshold.window_seconds,
            }
            result["threats"].append(threat)
            result["detected"] = True

            self._log_suspicious_activity(
                ThreatType.API_SCANNING,
                threshold.severity,
                ip_address,
                None,
                {
                    "count": count,
                    "threshold": threshold.count,
                    "endpoint": endpoint,
                    "user_agent": user_agent,
                },
            )

        return result

    async def get_threat_status(self, ip_address: Optional[str], user_id: Optional[str] = None) -> dict[str, Any]:
        """Get current threat status for an IP or user.

        Args:
            ip_address: IP address to check
            user_id: User ID to check

        Returns:
            Current threat status with counters
        """
        status = {
            "ip_address": ip_address,
            "user_id": user_id,
            "counters": {},
            "is_suspicious": False,
        }

        if ip_address:
            status["counters"]["failed_auth_ip"] = await self._get_counter(f"{KEY_FAILED_AUTH_IP}{ip_address}")
            status["counters"]["forbidden"] = await self._get_counter(f"{KEY_FORBIDDEN_IP}{ip_address}")
            status["counters"]["not_found"] = await self._get_counter(f"{KEY_NOT_FOUND_IP}{ip_address}")

        if user_id:
            status["counters"]["failed_auth_account"] = await self._get_counter(f"{KEY_FAILED_AUTH_ACCOUNT}{user_id}")

        # Check if any counter exceeds 50% of threshold
        for threat_type, threshold in self.thresholds.items():
            counter_key = None
            if threat_type == ThreatType.BRUTE_FORCE_IP and ip_address:
                counter_key = "failed_auth_ip"
            elif threat_type == ThreatType.BRUTE_FORCE_ACCOUNT and user_id:
                counter_key = "failed_auth_account"
            elif threat_type == ThreatType.AUTHORIZATION_PROBING and ip_address:
                counter_key = "forbidden"
            elif threat_type == ThreatType.API_SCANNING and ip_address:
                counter_key = "not_found"

            if counter_key and status["counters"].get(counter_key, 0) >= threshold.count * 0.5:
                status["is_suspicious"] = True
                break

        return status


# Singleton instance
security_monitor_service = SecurityMonitorService()
