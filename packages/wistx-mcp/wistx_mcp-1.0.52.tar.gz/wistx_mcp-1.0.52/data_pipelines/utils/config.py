"""Configuration settings for data pipelines."""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def _find_env_file() -> Path | str:
    """Find .env file in project root.
    
    Returns:
        Path to .env file or ".env" if not found
    """
    current = Path(__file__).resolve()
    project_root = current.parent.parent.parent
    env_file = project_root / ".env"
    if env_file.exists():
        return str(env_file)
    return ".env"


class PipelineSettings(BaseSettings):
    """Pipeline configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=_find_env_file(),
        case_sensitive=False,
        extra="ignore",
    )

    mongodb_uri: str = Field(
        ...,
        validation_alias="MONGODB_URI",
        description="MongoDB connection URI",
    )
    mongodb_db_name: str = Field(
        default="wistx-production",
        validation_alias="DATABASE_NAME",
        description="MongoDB database name",
    )

    gemini_api_key: str = Field(
        ...,
        validation_alias="GEMINI_API_KEY",
        description="Gemini API key for embeddings and chat completions",
    )

    pinecone_api_key: str = Field(
        ...,
        validation_alias="PINECONE_API_KEY",
        description="Pinecone API key",
    )

    pinecone_environment: str = Field(
        default="us-east-1-aws",
        validation_alias="PINECONE_ENVIRONMENT",
        description="Pinecone environment/region",
    )

    pinecone_index_name: str = Field(
        default="wistx",
        validation_alias="PINECONE_INDEX_NAME",
        description="Pinecone index name",
    )

    github_token: str | None = Field(
        default=None,
        validation_alias="GITHUB_TOKEN",
        description="GitHub token for API access",
    )
    
    github_internal_token: str | None = Field(
        default=None,
        validation_alias="GITHUB_INTERNAL_TOKEN",
        description="GitHub token for internal code examples collection",
    )
    
    github_min_stars: int = Field(
        default=200,
        validation_alias="GITHUB_MIN_STARS",
        description="Minimum stars for GitHub repositories (default: 200 for quality)",
    )
    
    github_max_repos_per_query: int = Field(
        default=1667,
        validation_alias="GITHUB_MAX_REPOS_PER_QUERY",
        description="Maximum repositories to process per search query (for 100k repos: ~1667 per query with 60 queries)",
    )
    
    github_max_files_per_repo: int = Field(
        default=999999,
        validation_alias="GITHUB_MAX_FILES_PER_REPO",
        description="Maximum files to process per repository (999999 = process all files, set lower to limit)",
    )
    
    github_repo_max_depth: int = Field(
        default=5,
        validation_alias="GITHUB_REPO_MAX_DEPTH",
        description="Maximum directory depth for recursive traversal",
    )
    
    github_enable_structure_extraction: bool = Field(
        default=True,
        validation_alias="GITHUB_ENABLE_STRUCTURE_EXTRACTION",
        description="Enable repository structure extraction during code examples collection (default: True)",
    )
    
    github_enable_quality_evaluation: bool = Field(
        default=True,
        validation_alias="GITHUB_ENABLE_QUALITY_EVALUATION",
        description="Enable quality evaluation and template storage for repositories (default: True)",
    )
    
    github_max_concurrent_repos: int = Field(
        default=5,
        validation_alias="GITHUB_MAX_CONCURRENT_REPOS",
        description="Maximum concurrent repositories to process (default: 5)",
    )
    
    github_collection_batch_size: int = Field(
        default=100,
        validation_alias="GITHUB_COLLECTION_BATCH_SIZE",
        description="Batch size for paginated repository collection (default: 100 repos per batch)",
    )
    
    github_use_paginated_collection: bool = Field(
        default=True,
        validation_alias="GITHUB_USE_PAGINATED_COLLECTION",
        description="Use paginated collection to reduce memory usage (default: True)",
    )
    
    github_use_streaming_pipeline: bool = Field(
        default=True,
        validation_alias="GITHUB_USE_STREAMING_PIPELINE",
        description="Use streaming pipeline to process examples as collected (default: True)",
    )
    
    github_enable_checkpointing: bool = Field(
        default=True,
        validation_alias="GITHUB_ENABLE_CHECKPOINTING",
        description="Enable checkpointing for code examples pipeline resume capability (default: True)",
    )
    
    github_checkpoint_interval: int = Field(
        default=100,
        validation_alias="GITHUB_CHECKPOINT_INTERVAL",
        description="Save checkpoint every N examples processed (default: 100)",
    )

    aws_access_key_id: str | None = Field(
        default=None,
        validation_alias="AWS_ACCESS_KEY_ID",
        description="AWS access key ID for pricing API",
    )
    aws_secret_access_key: str | None = Field(
        default=None,
        validation_alias="AWS_SECRET_ACCESS_KEY",
        description="AWS secret access key",
    )

    gcp_api_key: str | None = Field(
        default=None,
        validation_alias="GCP_API_KEY",
        description="GCP API key for Cloud Billing Catalog API (fallback if service account not available)",
    )
    gcp_service_account_key_path: str | None = Field(
        default=None,
        validation_alias="GCP_SERVICE_ACCOUNT_KEY_PATH",
        description="Path to GCP service account JSON key file",
    )
    gcp_service_account_key_json: str | None = Field(
        default=None,
        validation_alias="GCP_SERVICE_ACCOUNT_KEY_JSON",
        description="GCP service account JSON key content (alternative to key_path)",
    )

    alibaba_access_key_id: str | None = Field(
        default=None,
        validation_alias="ALIBABA_ACCESS_KEY_ID",
        description="Alibaba Cloud access key ID",
    )
    alibaba_access_key_secret: str | None = Field(
        default=None,
        validation_alias="ALIBABA_ACCESS_KEY_SECRET",
        description="Alibaba Cloud access key secret",
    )

    oracle_tenancy_ocid: str | None = Field(
        default=None,
        validation_alias="ORACLE_TENANCY_OCID",
        description="Oracle Cloud tenancy OCID",
    )
    oracle_user_ocid: str | None = Field(
        default=None,
        validation_alias="ORACLE_USER_OCID",
        description="Oracle Cloud user OCID",
    )
    oracle_fingerprint: str | None = Field(
        default=None,
        validation_alias="ORACLE_FINGERPRINT",
        description="Oracle Cloud API key fingerprint",
    )
    oracle_private_key_path: str | None = Field(
        default=None,
        validation_alias="ORACLE_PRIVATE_KEY_PATH",
        description="Path to Oracle Cloud private key file",
    )
    oracle_private_key_content: str | None = Field(
        default=None,
        validation_alias="ORACLE_PRIVATE_KEY_CONTENT",
        description="Oracle Cloud private key content (alternative to path)",
    )

    max_workers: int = Field(
        default=4,
        description="Maximum number of worker threads",
    )
    batch_size: int = Field(
        default=250,
        description="Batch size for MongoDB bulk operations (optimized for reliability)",
    )
    retry_attempts: int = Field(
        default=3,
        description="Number of retry attempts",
    )
    retry_delay: int = Field(
        default=5,
        description="Retry delay in seconds",
    )

    streaming_batch_size: int = Field(
        default=10,
        validation_alias="STREAMING_BATCH_SIZE",
        description="Batch size for streaming saves (progress logging)",
    )

    embedding_batch_size: int = Field(
        default=200,
        validation_alias="EMBEDDING_BATCH_SIZE",
        description="Batch size for embedding generation (default: 200, Gemini allows up to 2048)",
    )

    url_fetch_timeout_seconds: float = Field(
        default=60.0,
        validation_alias="URL_FETCH_TIMEOUT_SECONDS",
        description="Timeout for URL fetching operations (default: 60 seconds, max recommended: 120s for slow sites)",
    )

    url_fetch_max_retries: int = Field(
        default=2,
        validation_alias="URL_FETCH_MAX_RETRIES",
        description="Maximum number of retries for URL fetching on timeout (default: 2)",
    )

    llm_api_timeout_seconds: float = Field(
        default=90.0,
        validation_alias="LLM_API_TIMEOUT_SECONDS",
        description="Timeout for LLM API calls (default: 90 seconds)",
    )

    pdf_processing_timeout_seconds: float = Field(
        default=120.0,
        validation_alias="PDF_PROCESSING_TIMEOUT_SECONDS",
        description="Timeout for PDF processing operations (default: 120 seconds)",
    )

    sitemap_fetch_timeout_seconds: float = Field(
        default=30.0,
        validation_alias="SITEMAP_FETCH_TIMEOUT_SECONDS",
        description="Timeout for sitemap fetching operations (default: 30 seconds)",
    )

    api_rate_limit_max_calls: int = Field(
        default=100,
        validation_alias="API_RATE_LIMIT_MAX_CALLS",
        description="Maximum API calls per period for global rate limiting (default: 100, can be increased to 5000+ for Gemini)",
    )

    api_rate_limit_period_seconds: float = Field(
        default=60.0,
        validation_alias="API_RATE_LIMIT_PERIOD_SECONDS",
        description="Time period in seconds for rate limiting (default: 60 seconds)",
    )

    max_concurrent_urls: int = Field(
        default=10,
        validation_alias="MAX_CONCURRENT_URLS",
        description="Maximum concurrent URL fetches (default: 10, increase for higher throughput)",
    )

    domain_rate_limit_max_calls: int = Field(
        default=10,
        validation_alias="DOMAIN_RATE_LIMIT_MAX_CALLS",
        description="Maximum calls per domain per period (default: 10 calls per minute)",
    )

    domain_rate_limit_period_seconds: float = Field(
        default=60.0,
        validation_alias="DOMAIN_RATE_LIMIT_PERIOD_SECONDS",
        description="Time period in seconds for per-domain rate limiting (default: 60 seconds)",
    )

    use_paginated_collection: bool = Field(
        default=True,
        validation_alias="USE_PAGINATED_COLLECTION",
        description="Use paginated URL processing to reduce memory usage (default: True)",
    )

    collection_batch_size: int = Field(
        default=1000,
        validation_alias="COLLECTION_BATCH_SIZE",
        description="Batch size for paginated URL processing (default: 1000 URLs per batch)",
    )

    use_streaming_pipeline: bool = Field(
        default=True,
        validation_alias="USE_STREAMING_PIPELINE",
        description="Use streaming pipeline to process articles as collected (default: True)",
    )

    enable_checkpointing: bool = Field(
        default=True,
        validation_alias="ENABLE_CHECKPOINTING",
        description="Enable checkpointing for pipeline resume capability (default: True)",
    )

    checkpoint_interval: int = Field(
        default=100,
        validation_alias="CHECKPOINT_INTERVAL",
        description="Save checkpoint every N URLs/articles processed (default: 100)",
    )

    data_dir: Path = Field(
        default_factory=lambda: Path(__file__).parent.parent / "data",
        description="Base directory for data files",
    )


settings = PipelineSettings()

