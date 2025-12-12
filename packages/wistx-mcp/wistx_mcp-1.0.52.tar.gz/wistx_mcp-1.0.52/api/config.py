"""Configuration settings.

All settings are loaded from environment variables (.env file).
Required variables must be set in .env file.

Example .env file:
    MONGODB_URL=mongodb+srv://user:pass@cluster.mongodb.net/
    MONGODB_DATABASE=wistx-production

DEPLOYMENT CONSTANTS:
    WAITLIST_ENABLED: Set to True to enable waitlist mode (blocks /auth routes).
                      Set to False to allow normal signup flow.
                      Change this constant and redeploy to toggle waitlist mode.
"""

from typing import Any

from pydantic import Field, ValidationError, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

WAITLIST_ENABLED = False


class Settings(BaseSettings):
    """Application settings.

    All settings are loaded from environment variables (.env file).
    The .env file should be in the project root directory.
    """

    api_title: str = "WISTX API"
    api_version: str = "1.0.52"
    debug: bool = Field(
        default=False,
        validation_alias="DEBUG",
        description="Debug mode. When True, uses development OAuth redirect URLs (localhost). Set DEBUG=true in .env for local development.",
    )

    mongodb_url: str = Field(
        ...,
        validation_alias="MONGODB_URI",
        description="MongoDB connection URL. Must be set in .env file as MONGODB_URI.",
        examples=[
            "mongodb+srv://user:pass@cluster.mongodb.net/",
            "mongodb://localhost:27017",
        ],
    )
    mongodb_database: str = Field(
        default="wistx",
        validation_alias="DATABASE_NAME",
        description="MongoDB database name",
    )

    mongodb_max_pool_size: int = 50
    mongodb_min_pool_size: int = 10
    mongodb_max_idle_time_ms: int = 30000
    mongodb_server_selection_timeout_ms: int = 60000
    mongodb_connect_timeout_ms: int = 30000
    mongodb_socket_timeout_ms: int = 120000
    mongodb_heartbeat_frequency_ms: int = 10000
    mongodb_wait_queue_timeout_ms: int = 5000
    mongodb_max_connecting: int = 10
    mongodb_retry_writes: bool = True
    mongodb_read_preference: str = "secondaryPreferred"

    mongodb_circuit_breaker_failure_threshold: int = 5
    mongodb_circuit_breaker_recovery_timeout: int = 60

    mongodb_retry_max_attempts: int = 3
    mongodb_retry_initial_delay: float = 1.0
    mongodb_retry_max_delay: float = 10.0

    secret_key: str = Field(
        ...,
        validation_alias="SECRET_KEY",
        description="Secret key for JWT tokens and HMAC signatures. REQUIRED - Must be at least 32 characters. Generate with: python -c 'import secrets; print(secrets.token_urlsafe(32))'",
    )

    api_key_pepper: str = Field(
        ...,
        validation_alias="API_KEY_PEPPER",
        description="Secret pepper for API key hashing. REQUIRED - Must be at least 32 characters. Generate with: python -c 'import secrets; print(secrets.token_urlsafe(32))'",
    )

    jwt_refresh_window_days: int = Field(
        default=7,
        validation_alias="JWT_REFRESH_WINDOW_DAYS",
        description="Maximum days after expiration that a token can be refreshed (default: 7 days)",
    )
    algorithm: str = "HS256"
    access_token_expire_minutes: int = Field(
        default=4320,
        validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES",
        description="Access token expiration time in minutes (default: 4320 = 3 days)",
    )

    model_server_url: str = "http://localhost:8001"

    disable_rate_limit: bool = Field(
        default=False,
        validation_alias="DISABLE_RATE_LIMIT",
        description="Explicitly disable rate limiting. Use only for local development/testing. Never disable in production.",
    )
    disable_csrf_protection: bool = Field(
        default=False,
        validation_alias="DISABLE_CSRF_PROTECTION",
        description="Explicitly disable CSRF protection. Use only for local development/testing. Never disable in production.",
    )

    rate_limit_requests_per_minute: int = 60
    rate_limit_tokens_per_day: int = 1000000

    redis_url: str | None = Field(
        default=None,
        validation_alias="REDIS_URL",
        description="Redis URL for distributed rate limiting (optional, defaults to in-memory if not set)",
        examples=["redis://localhost:6379", "redis://user:pass@localhost:6379/0"],
    )

    memorystore_host: str | None = Field(
        default=None,
        validation_alias="MEMORYSTORE_HOST",
        description="Google Memorystore (Redis) host (optional, for caching)",
    )
    memorystore_port: int = Field(
        default=6379,
        validation_alias="MEMORYSTORE_PORT",
        description="Google Memorystore (Redis) port",
    )
    memorystore_enabled: bool = Field(
        default=False,
        validation_alias="MEMORYSTORE_ENABLED",
        description="Enable Google Memorystore caching",
    )
    redis_password: str | None = Field(
        default=None,
        validation_alias="REDIS_PASSWORD",
        description="Redis password/AUTH string (optional, used when MEMORYSTORE_HOST is set without REDIS_URL)",
    )

    redis_circuit_breaker_failure_threshold: int = Field(
        default=5,
        validation_alias="REDIS_CIRCUIT_BREAKER_FAILURE_THRESHOLD",
        description="Number of failures before opening Redis circuit breaker",
    )
    redis_circuit_breaker_recovery_timeout: int = Field(
        default=60,
        validation_alias="REDIS_CIRCUIT_BREAKER_RECOVERY_TIMEOUT",
        description="Seconds to wait before attempting Redis recovery",
    )
    redis_health_check_interval: int = Field(
        default=30,
        validation_alias="REDIS_HEALTH_CHECK_INTERVAL",
        description="Seconds between Redis health checks",
    )
    redis_max_retries: int = Field(
        default=3,
        validation_alias="REDIS_MAX_RETRIES",
        description="Maximum retry attempts for Redis operations",
    )
    redis_retry_initial_delay: float = Field(
        default=1.0,
        validation_alias="REDIS_RETRY_INITIAL_DELAY",
        description="Initial delay between Redis retries in seconds",
    )
    redis_retry_max_delay: float = Field(
        default=10.0,
        validation_alias="REDIS_RETRY_MAX_DELAY",
        description="Maximum delay between Redis retries in seconds",
    )
    redis_connection_pool_size: int = Field(
        default=50,
        validation_alias="REDIS_CONNECTION_POOL_SIZE",
        description="Maximum Redis connection pool size",
    )
    redis_socket_connect_timeout: int = Field(
        default=5,
        validation_alias="REDIS_SOCKET_CONNECT_TIMEOUT",
        description="Redis socket connection timeout in seconds",
    )
    redis_socket_timeout: int = Field(
        default=5,
        validation_alias="REDIS_SOCKET_TIMEOUT",
        description="Redis socket timeout in seconds",
    )

    otlp_endpoint: str | None = Field(
        default=None,
        validation_alias="OTLP_ENDPOINT",
        description="OpenTelemetry OTLP endpoint for distributed tracing (optional)",
        examples=["http://localhost:4317"],
    )
    tracing_enabled: bool = Field(
        default=False,
        validation_alias="TRACING_ENABLED",
        description="Enable distributed tracing",
    )

    alert_webhook_url: str | None = Field(
        default=None,
        validation_alias="ALERT_WEBHOOK_URL",
        description="Webhook URL for critical alerts (optional)",
    )

    pinecone_api_key: str | None = Field(
        default=None,
        validation_alias="PINECONE_API_KEY",
        description="Pinecone API key (optional, required for vector search)",
    )
    pinecone_environment: str | None = Field(
        default=None,
        validation_alias="PINECONE_ENVIRONMENT",
        description="Pinecone environment/region (optional)",
    )
    pinecone_index_name: str = Field(
        default="wistx",
        validation_alias="PINECONE_INDEX_NAME",
        description="Pinecone index name",
    )
    pinecone_index_dimension: int = Field(
        default=1536,
        validation_alias="PINECONE_INDEX_DIMENSION",
        description="Pinecone index dimension (1536 for Gemini gemini-embedding-001)",
    )
    pinecone_index_region: str = Field(
        default="us-east-1",
        validation_alias="PINECONE_INDEX_REGION",
        description="Pinecone index region (for serverless indexes)",
    )

    gemini_api_key: str = Field(
        ...,
        validation_alias="GEMINI_API_KEY",
        description="Gemini API key for embeddings and chat completions",
    )

    anthropic_api_key: str | None = Field(
        default=None,
        validation_alias="ANTHROPIC_API_KEY",
        description="Anthropic API key for Claude (required for code analysis)",
    )

    enable_waitlist: bool = Field(
        default=WAITLIST_ENABLED,
        validation_alias="ENABLE_WAITLIST",
        description="Enable waitlist mode. When True, blocks access to auth page and requires waitlist signup. Can be overridden by ENABLE_WAITLIST env var.",
    )

    google_oauth_client_id: str = Field(
        ...,
        validation_alias="GOOGLE_OAUTH_CLIENT_ID",
        description="Google OAuth 2.0 client ID",
    )
    google_oauth_client_secret: str = Field(
        ...,
        validation_alias="GOOGLE_OAUTH_CLIENT_SECRET",
        description="Google OAuth 2.0 client secret",
    )
    github_oauth_client_id: str = Field(
        ...,
        validation_alias="GITHUB_OAUTH_CLIENT_ID",
        description="GitHub OAuth app client ID",
    )
    github_oauth_client_secret: str = Field(
        ...,
        validation_alias="GITHUB_OAUTH_CLIENT_SECRET",
        description="GitHub OAuth app client secret",
    )
    github_internal_token: str | None = Field(
        default=None,
        validation_alias="GITHUB_INTERNAL_TOKEN",
        description="Internal GitHub token for public repository access (WISTX service account)",
    )
    oauth_backend_callback_url_dev: str = Field(
        default="http://localhost:8000/auth/{provider}/callback",
        validation_alias="OAUTH_BACKEND_CALLBACK_URL_DEV",
        description="Backend OAuth callback URL for development (where OAuth provider redirects to)",
    )
    oauth_backend_callback_url_prod: str = Field(
        default="https://api.wistx.ai/auth/{provider}/callback",
        validation_alias="OAUTH_BACKEND_CALLBACK_URL_PROD",
        description="Backend OAuth callback URL for production (where OAuth provider redirects to)",
    )
    oauth_frontend_redirect_url_dev: str = Field(
        default="http://localhost:3000/auth/callback/{provider}",
        validation_alias="OAUTH_FRONTEND_REDIRECT_URL_DEV",
        description="Frontend redirect URL for development (where backend redirects after OAuth)",
    )
    oauth_frontend_redirect_url_prod: str = Field(
        default="https://wistx.ai/auth/callback/{provider}",
        validation_alias="OAUTH_FRONTEND_REDIRECT_URL_PROD",
        description="Frontend redirect URL for production (where backend redirects after OAuth). Frontend is on wistx.ai, backend is on api.wistx.ai",
    )

    stripe_secret_key: str | None = Field(
        default=None,
        validation_alias="STRIPE_SECRET_KEY",
        description="Stripe secret key for billing",
    )
    stripe_publishable_key: str | None = Field(
        default=None,
        validation_alias="STRIPE_PUBLISHABLE_KEY",
        description="Stripe publishable key for frontend",
    )
    stripe_webhook_secret: str | None = Field(
        default=None,
        validation_alias="STRIPE_WEBHOOK_SECRET",
        description="Stripe webhook secret for verifying webhooks",
    )

    github_webhook_secret: str | None = Field(
        default=None,
        validation_alias="GITHUB_WEBHOOK_SECRET",
        description="GitHub webhook secret for verifying webhooks",
    )

    email_provider: str = Field(
        default="resend",
        validation_alias="EMAIL_PROVIDER",
        description="Email provider: 'resend', 'sendgrid', or 'ses'",
    )
    email_from_address: str = Field(
        default="noreply@wistx.ai",
        validation_alias="EMAIL_FROM_ADDRESS",
        description="Default sender email address",
    )
    email_from_name: str = Field(
        default="WISTX",
        validation_alias="EMAIL_FROM_NAME",
        description="Default sender name",
    )

    resend_api_key: str | None = Field(
        default=None,
        validation_alias="RESEND_API_KEY",
        description="Resend API key (required if EMAIL_PROVIDER=resend)",
    )

    sendgrid_api_key: str | None = Field(
        default=None,
        validation_alias="SENDGRID_API_KEY",
        description="SendGrid API key (required if EMAIL_PROVIDER=sendgrid)",
    )

    aws_access_key_id: str | None = Field(
        default=None,
        validation_alias="AWS_ACCESS_KEY_ID",
        description="AWS access key ID (required if EMAIL_PROVIDER=ses)",
    )
    aws_secret_access_key: str | None = Field(
        default=None,
        validation_alias="AWS_SECRET_ACCESS_KEY",
        description="AWS secret access key (required if EMAIL_PROVIDER=ses)",
    )
    aws_region: str = Field(
        default="us-east-1",
        validation_alias="AWS_REGION",
        description="AWS region for SES (default: us-east-1)",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("mongodb_url")
    @classmethod
    def validate_mongodb_url(cls, v: str) -> str:
        """Validate MongoDB URL is set and not using default localhost in production."""
        if not v or v.strip() == "":
            raise ValueError(
                "MONGODB_URL is required. Please set it in your .env file.\n"
                "Example: MONGODB_URL=mongodb+srv://user:pass@cluster.mongodb.net/"
            )

        if v == "mongodb://localhost:27017":
            import warnings

            warnings.warn(
                "Using default MongoDB URL (localhost). "
                "Make sure MONGODB_URL is set in your .env file.",
                UserWarning,
            )

        return v.strip()

    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        """Validate secret key strength.

        Args:
            v: Secret key value

        Returns:
            Validated secret key

        Raises:
            ValueError: If secret key is too weak
        """
        v = v.strip()

        if len(v) < 32:
            raise ValueError(
                f"SECRET_KEY must be at least 32 characters long (got {len(v)}). "
                "Generate a secure key with: python -c 'import secrets; print(secrets.token_urlsafe(32))'"
            )

        return v

    @field_validator("api_key_pepper")
    @classmethod
    def validate_api_key_pepper(cls, v: str) -> str:
        """Validate API key pepper strength.

        Args:
            v: API key pepper value

        Returns:
            Validated pepper

        Raises:
            ValueError: If pepper is too weak
        """
        v = v.strip()

        if len(v) < 32:
            raise ValueError(
                f"API_KEY_PEPPER must be at least 32 characters long (got {len(v)}). "
                "Generate a secure pepper with: python -c 'import secrets; print(secrets.token_urlsafe(32))'"
            )

        return v



    def get_mongodb_connection_options(self) -> dict[str, Any]:
        """Get MongoDB connection options as dictionary.

        Returns:
            Dictionary of MongoDB connection options
        """
        mongodb_url_str = str(self.mongodb_url)
        is_atlas = mongodb_url_str.startswith("mongodb+srv://")

        read_pref_map = {
            "primary": "primary",
            "primarypreferred": "primaryPreferred",
            "secondary": "secondary",
            "secondarypreferred": "secondaryPreferred",
            "nearest": "nearest",
        }

        read_pref_str = self.mongodb_read_preference.lower()
        read_preference = read_pref_map.get(read_pref_str, "secondaryPreferred")

        options = {
            "maxPoolSize": self.mongodb_max_pool_size,
            "minPoolSize": self.mongodb_min_pool_size,
            "maxIdleTimeMS": self.mongodb_max_idle_time_ms,
            "serverSelectionTimeoutMS": max(self.mongodb_server_selection_timeout_ms, 30000),
            "connectTimeoutMS": self.mongodb_connect_timeout_ms,
            "socketTimeoutMS": self.mongodb_socket_timeout_ms,
            "heartbeatFrequencyMS": self.mongodb_heartbeat_frequency_ms,
            "waitQueueTimeoutMS": self.mongodb_wait_queue_timeout_ms,
            "maxConnecting": self.mongodb_max_connecting,
            "retryWrites": self.mongodb_retry_writes,
            "readPreference": read_preference,
            "appName": "wistx-api",
            "compressors": ["zlib"],
        }

        if is_atlas:
            options["tls"] = True
            options["tlsAllowInvalidCertificates"] = False

        return options


try:
    settings = Settings()
except ValidationError as e:
    import logging

    logging.basicConfig(level=logging.ERROR)
    logger = logging.getLogger(__name__)
    logger.error("Failed to initialize Settings: %s", e)
    logger.error("This usually means a required environment variable is missing.")
    logger.error("Required variables: MONGODB_URI")
    logger.error("Check your environment variables and Secret Manager configuration.")

    raise SystemExit(1) from e
