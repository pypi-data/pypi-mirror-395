"""FastAPI main application."""

import logging
from typing import Any

from fastapi import FastAPI

from api.config import settings
from api.middleware.logging import setup_logging_middleware
from api.middleware.rate_limit import RateLimitMiddleware
from api.middleware.token_tracking import UsageTrackingMiddleware
from api.middleware.cors import setup_cors_middleware
from api.middleware.request_size_limit import RequestSizeLimitMiddleware
from api.middleware.auth import AuthenticationMiddleware
from api.middleware.csrf import CSRFProtectionMiddleware
from api.middleware.audit_logging import AuditLoggingMiddleware
from api.middleware.early_logging import EarlyLoggingMiddleware
from api.middleware.security_headers import SecurityHeadersMiddleware

logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

class MongoDBBackgroundTaskFilter(logging.Filter):
    """Filter to suppress non-critical MongoDB background task errors."""

    def filter(self, record: logging.LogRecord) -> bool:
        """Filter out non-critical MongoDB background task errors."""
        if record.name == "pymongo.client":
            message = record.getMessage()
            error_text = str(record.exc_info) if record.exc_info else ""
            full_message = f"{message} {error_text}".lower()
            
            if "_operationcancelled" in full_message or "operation cancelled" in full_message:
                return False
            
            if "background task" in full_message and "encountered an error" in full_message:
                if "_operationcancelled" in full_message or "autoreconnect" in full_message:
                    return False
            
            if "nodename nor servname" in full_message or "gaierror" in full_message:
                return False
            
            if record.exc_info and record.exc_info[0]:
                exc_type_name = record.exc_info[0].__name__
                if exc_type_name in ("_OperationCancelled", "OperationCancelled", "AutoReconnect", "gaierror"):
                    return False
        
        return True


pymongo_client_logger = logging.getLogger("pymongo.client")
pymongo_client_logger.addFilter(MongoDBBackgroundTaskFilter())

logging.getLogger("pymongo").setLevel(logging.WARNING)
logging.getLogger("pymongo.connection").setLevel(logging.WARNING)
logging.getLogger("pymongo.topology").setLevel(logging.WARNING)
logging.getLogger("pymongo.serverSelection").setLevel(logging.WARNING)
logging.getLogger("pymongo.client").setLevel(logging.ERROR)
logging.getLogger("pymongo.pool").setLevel(logging.WARNING)

logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.api_title,
    description="WISTX API - REST endpoints for compliance, pricing, and code examples context",
    version=settings.api_version,
    docs_url="/docs",
    redoc_url="/redoc",
    debug=settings.debug,
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Local development server",
        },
        {
            "url": "https://api.wistx.ai",
            "description": "Production API",
        },
    ],
)

app.add_middleware(EarlyLoggingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
setup_cors_middleware(app)
setup_logging_middleware(app)
app.add_middleware(RequestSizeLimitMiddleware, max_request_size_mb=getattr(settings, "max_request_size_mb", 10))
app.add_middleware(AuthenticationMiddleware)
app.add_middleware(CSRFProtectionMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(UsageTrackingMiddleware)

from api.middleware.auth_rate_limit import AuthRateLimitMiddleware

app.add_middleware(AuthRateLimitMiddleware, max_attempts=5, window_minutes=15)

from api.middleware.error_alerting import ErrorAlertingMiddleware
from api.middleware.versioning import VersioningMiddleware
from api.middleware.exception_handler import ExceptionHandlerMiddleware

app.add_middleware(ExceptionHandlerMiddleware)
app.add_middleware(AuditLoggingMiddleware)
app.add_middleware(ErrorAlertingMiddleware)
app.add_middleware(VersioningMiddleware)

logger.info("Starting WISTX API v%s", settings.api_version)


@app.on_event("startup")
async def startup_event() -> None:
    """Initialize services on startup."""
    from api.auth.oauth import _validate_oauth_config
    
    _validate_oauth_config()
    
    from api.utils.tracing import initialize_tracing

    if settings.tracing_enabled:
        initialize_tracing(
            service_name="wistx-api",
            otlp_endpoint=settings.otlp_endpoint,
            enabled=settings.tracing_enabled,
        )

    from api.database.mongodb import mongodb_manager
    from api.database.exceptions import MongoDBConnectionError
    from api.services.job_worker import job_worker
    from api.services.job_queue_service import job_queue_service
    from api.scheduler import setup_scheduler
    from pymongo.errors import (
        ServerSelectionTimeoutError,
        NetworkTimeout,
        ConnectionFailure,
        OperationFailure,
    )

    try:
        logger.info("Connecting to MongoDB...")
        mongodb_manager.connect()
        logger.info("MongoDB connection established")

        logger.info("Running database migrations...")
        try:
            from api.database.migrations.migration_manager import MigrationManager
            from api.database.migrations import Migration0001InitialSchema
            from api.database.migrations.migrations_0002_add_custom_compliance_fields import (
                Migration0002AddCustomComplianceFields,
            )
            from api.database.migrations.migrations_0003_resource_deduplication_and_checkpoints import (
                Migration0003ResourceDeduplicationAndCheckpoints,
            )
            from api.database.migrations.migrations_0004_virtual_filesystem import (
                Migration0004VirtualFilesystem,
            )
            from api.database.migrations.migrations_0005_intelligent_context import (
                Migration0005IntelligentContext,
            )
            from api.database.migrations.migrations_0006_predictive_cache import (
                Migration0006PredictiveCache,
            )
            from api.database.migrations.migrations_0007_hybrid_retrieval_indexes import (
                Migration0007HybridRetrievalIndexes,
            )

            migration_manager = MigrationManager()
            migrations = [
                Migration0001InitialSchema(),
                Migration0002AddCustomComplianceFields(),
                Migration0003ResourceDeduplicationAndCheckpoints(),
                Migration0004VirtualFilesystem(),
                Migration0005IntelligentContext(),
                Migration0006PredictiveCache(),
                Migration0007HybridRetrievalIndexes(),
            ]
            await migration_manager.migrate(migrations)

            current_version = await migration_manager.get_current_version()
            logger.info("Database migrations complete. Current version: %d", current_version)
        except Exception as migration_error:
            logger.warning("Migration failed, falling back to manual collection creation: %s", migration_error)
            logger.info("Initializing MongoDB collections...")
            db = mongodb_manager.get_database()

            collections = [
                "compliance_controls",
                "pricing_data",
                "code_examples",
                "best_practices",
                "knowledge_articles",
                "users",
                "api_keys",
                "api_usage",
                "user_usage_summary",
                "indexed_resources",
                "indexed_files",
                "indexing_jobs",
                "reports",
                "quality_templates",
                "infrastructure_budgets",
                "infrastructure_spending",
                "budget_status",
                "budget_alerts",
                "alert_preferences",
                "user_notifications",
                "architecture_design_cache",
            ]

            created_count = 0
            for collection_name in collections:
                try:
                    if collection_name not in db.list_collection_names():
                        db.create_collection(collection_name)
                        logger.info("Created collection: %s", collection_name)
                        created_count += 1
                except OperationFailure as e:
                    if "already exists" in str(e).lower() or "namespace exists" in str(e).lower():
                        logger.debug("Collection %s already exists (race condition)", collection_name)
                    else:
                        logger.warning("Failed to create collection %s: %s", collection_name, e)

            if created_count > 0:
                logger.info("Created %d new MongoDB collections", created_count)
            else:
                logger.info("All MongoDB collections already exist")

            logger.info("Note: Run 'python scripts/run_migrations.py' to apply migrations")

        logger.info("Recovering stale jobs...")
        recovered = await job_queue_service.recover_stale_jobs(stale_threshold_minutes=30)
        if recovered > 0:
            logger.info("Recovered %d stale jobs", recovered)

        logger.info("Recovering stale pipelines...")
        from api.services.pipeline_execution_service import pipeline_execution_service
        recovered_pipelines = await pipeline_execution_service.recover_stale_pipelines(stale_threshold_minutes=5)
        if recovered_pipelines > 0:
            logger.info("Recovered %d stale pipelines", recovered_pipelines)

        logger.info("Starting job worker...")
        await job_worker.start()
        logger.info("Job worker started successfully")
    except (
        MongoDBConnectionError,
        ServerSelectionTimeoutError,
        NetworkTimeout,
        ConnectionFailure,
        ConnectionError,
        TimeoutError,
        ValueError,
    ) as e:
        logger.warning("Failed to initialize MongoDB collections: %s", e)
        logger.warning("Collections may need to be created manually via: python scripts/setup_mongodb.py")
        logger.warning("API will continue to start, but database operations may fail")

    try:
        logger.info("Initializing Redis/Memorystore connection...")
        from api.database.redis_client import get_redis_manager

        redis_manager = await get_redis_manager()
        if redis_manager:
            redis_client = await redis_manager.get_client()
            if redis_client:
                redis_health = redis_manager.get_health_status()
                if redis_health.get("healthy"):
                    logger.info("Redis/Memorystore connection established successfully")
                else:
                    circuit_state = redis_health.get("circuit_state", "unknown")
                    logger.warning(
                        "Redis/Memorystore client initialized but connection failed. "
                        "Circuit state: %s. Falling back to in-memory mode.",
                        circuit_state,
                    )
            else:
                logger.info(
                    "Redis/Memorystore connection failed (network unreachable or not configured). "
                    "Falling back to in-memory mode."
                )
        else:
            logger.info("Redis/Memorystore not configured (skipping initialization)")
    except Exception as e:
        logger.warning("Failed to initialize Redis/Memorystore: %s", e)
        logger.warning("Redis operations will fall back to in-memory mode")

    try:
        scheduler = setup_scheduler()
        if scheduler:
            scheduler.start()
            logger.info("Scheduler started successfully")
    except Exception as e:
        logger.warning("Failed to start scheduler: %s", e)
        logger.warning("Scheduled tasks will not run")

    logger.info("Cache service uses Redis (initialized above)")

    if settings.pinecone_api_key:
        logger.info("Initializing Pinecone connection...")
        try:
            from pinecone import Pinecone  # type: ignore[import-untyped]
            from pinecone.exceptions import NotFoundException  # type: ignore[import-untyped]
        except (ImportError, ModuleNotFoundError) as import_error:
            error_msg = str(import_error)
            if "pinecone-client" in error_msg.lower() or "renamed" in error_msg.lower():
                logger.warning(
                    "Pinecone package conflict detected. Please uninstall 'pinecone-client' "
                    "and install 'pinecone' instead: pip uninstall pinecone-client && pip install pinecone"
                )
            else:
                logger.warning("Pinecone client not installed. Install with: pip install pinecone")
            logger.warning("Vector search features will not be available")
        else:
            try:
                pc = Pinecone(api_key=settings.pinecone_api_key)
                index_name = settings.pinecone_index_name

                try:
                    existing_indexes = pc.list_indexes().names()
                    if index_name not in existing_indexes:
                        logger.info("Creating Pinecone index '%s'...", index_name)
                        try:
                            pc.create_index(
                                name=index_name,
                                dimension=settings.pinecone_index_dimension,
                                metric="cosine",
                                spec={
                                    "serverless": {
                                        "cloud": "aws",
                                        "region": settings.pinecone_index_region,
                                    }
                                },
                            )
                            logger.info("Successfully created Pinecone index '%s'", index_name)
                            logger.info("Note: Index creation may take a few minutes to complete")
                        except (ValueError, RuntimeError, ConnectionError) as create_error:
                            error_msg = str(create_error)
                            if "already exists" in error_msg.lower() or "already exist" in error_msg.lower():
                                logger.info("Pinecone index '%s' already exists (created concurrently)", index_name)
                            else:
                                logger.warning("Failed to create Pinecone index '%s': %s", index_name, create_error)
                                raise
                    else:
                        logger.info("Pinecone index '%s' already exists", index_name)

                    index = pc.Index(index_name)
                    stats = index.describe_index_stats()
                    logger.info(
                        "Successfully connected to Pinecone: index '%s' (%d vectors)",
                        index_name,
                        stats.get("total_vector_count", 0),
                    )
                    
                    try:
                        from api.services.custom_compliance_service import custom_compliance_service
                        
                        if custom_compliance_service.pinecone_loader:
                            try:
                                custom_compliance_service.pinecone_loader.reset_index()
                                logger.debug("Reset PineconeLoader cache - index is now available")
                            except (AttributeError, ValueError) as e:
                                logger.debug("Could not reset PineconeLoader cache: %s", e)
                    except ImportError:
                        pass
                except NotFoundException:
                    logger.warning(
                        "Pinecone index '%s' not found after creation attempt",
                        index_name,
                    )
                    logger.warning("Vector search features will not be available until index is ready")
                except (ConnectionError, TimeoutError, ValueError, AttributeError) as index_error:
                    logger.warning(
                        "Pinecone index '%s' not accessible: %s",
                        index_name,
                        index_error,
                    )
                    logger.warning("Vector search features will not be available")
            except (ValueError, RuntimeError, ConnectionError, TimeoutError) as e:
                logger.warning("Failed to initialize Pinecone: %s", e)
                logger.warning("Vector search features will not be available")
    else:
        logger.info("Pinecone not configured (PINECONE_API_KEY not set)")


@app.get("/health")
async def health_check() -> dict[str, Any]:
    """Health check endpoint."""
    from api.database.mongodb import mongodb_manager
    from api.database.redis_client import get_redis_manager

    health_status = {
        "status": "healthy",
        "api": {
            "version": settings.api_version,
            "title": settings.api_title,
        },
    }

    try:
        db_health = mongodb_manager.health_check()
        health_status["database"] = {
            "status": db_health.get("status", "unknown"),
            "latency_ms": db_health.get("latency_ms"),
            "connections": db_health.get("connections", {}),
        }
    except (ConnectionError, TimeoutError, ValueError) as e:
        health_status["database"] = {
            "status": "unhealthy",
            "error": str(e),
        }
        health_status["status"] = "degraded"

    try:
        redis_manager = await get_redis_manager()
        if redis_manager:
            redis_health = redis_manager.get_health_status()
            health_status["redis"] = {
                "status": "healthy" if redis_health.get("healthy") else "unhealthy",
                "circuit_state": redis_health.get("circuit_state"),
            }
            if not redis_health.get("healthy"):
                health_status["status"] = "degraded"
        else:
            health_status["redis"] = {
                "status": "not_configured",
            }
    except Exception as e:
        health_status["redis"] = {
            "status": "unhealthy",
            "error": str(e),
        }
        health_status["status"] = "degraded"

    if settings.pinecone_api_key:
        try:
            try:
                from pinecone import Pinecone 
                from pinecone.exceptions import NotFoundException 
            except (ImportError, ModuleNotFoundError) as import_error:
                error_msg = str(import_error)
                if "pinecone-client" in error_msg.lower() or "renamed" in error_msg.lower():
                    health_status["pinecone"] = {
                        "status": "unavailable",
                        "error": "Package conflict: uninstall 'pinecone-client' and install 'pinecone'",
                    }
                else:
                    health_status["pinecone"] = {
                        "status": "unavailable",
                        "error": f"Import error: {import_error}",
                    }
            else:
                try:
                    pc = Pinecone(api_key=settings.pinecone_api_key)
                    index = pc.Index(settings.pinecone_index_name)
                    stats = index.describe_index_stats()
                    health_status["pinecone"] = {
                        "status": "healthy",
                        "index": settings.pinecone_index_name,
                        "vector_count": stats.get("total_vector_count", 0),
                    }
                except NotFoundException:
                    health_status["pinecone"] = {
                        "status": "index_not_found",
                        "error": f"Index '{settings.pinecone_index_name}' does not exist. Run 'python scripts/setup_pinecone.py' to create it",
                    }
                    if health_status["status"] == "healthy":
                        health_status["status"] = "degraded"
                except (ConnectionError, TimeoutError, ValueError, AttributeError) as e:
                    health_status["pinecone"] = {
                        "status": "unhealthy",
                        "error": str(e),
                    }
                    if health_status["status"] == "healthy":
                        health_status["status"] = "degraded"
        except (ValueError, RuntimeError, ConnectionError, TimeoutError) as e:
            health_status["pinecone"] = {
                "status": "unhealthy",
                "error": str(e),
            }
            if health_status["status"] == "healthy":
                health_status["status"] = "degraded"
    else:
        health_status["pinecone"] = {
            "status": "not_configured",
        }

    return health_status


from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from api.routers.v1 import router as v1_router
from api.routers.internal import admin, webhooks, github_webhooks
from api.auth.oauth import google_oauth_router, github_oauth_router
from api.auth.users import fastapi_users, jwt_authentication


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """Handle HTTP exceptions and ensure CORS headers are present.
    
    Args:
        request: FastAPI request object
        exc: HTTP exception
        
    Returns:
        JSON response with CORS headers
    """
    origin = request.headers.get("origin")
    if origin:
        allowed_origins = [
            "http://localhost:3000",
            "http://localhost:3001",
            "http://localhost:8000",
            "https://app.wistx.ai",
            "https://wistx.ai",
        ]
        if settings.debug:
            allowed_origins.extend([
                "http://127.0.0.1:3000",
                "http://127.0.0.1:3001",
                "http://127.0.0.1:8000",
            ])
        
        if origin in allowed_origins:
            headers = dict(exc.headers) if exc.headers else {}
            headers["Access-Control-Allow-Origin"] = origin
            headers["Access-Control-Allow-Credentials"] = "true"
            headers["Access-Control-Expose-Headers"] = "X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Window"
            
            content = {"detail": exc.detail}
            if exc.status_code == 422:
                content = {"detail": exc.detail, "body": getattr(exc, "body", None)}
            
            return JSONResponse(
                status_code=exc.status_code,
                content=content,
                headers=headers,
            )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=dict(exc.headers) if exc.headers else {},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle validation errors and ensure CORS headers are present.
    
    Args:
        request: FastAPI request object
        exc: Validation exception
        
    Returns:
        JSON response with CORS headers
    """
    origin = request.headers.get("origin")
    if origin:
        allowed_origins = [
            "http://localhost:3000",
            "http://localhost:3001",
            "https://app.wistx.ai",
            "https://wistx.ai",
        ]
        if settings.debug:
            allowed_origins.extend([
                "http://127.0.0.1:3000",
                "http://127.0.0.1:3001",
                "http://127.0.0.1:8000",
            ])
        
        if origin in allowed_origins:
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={"detail": exc.errors(), "body": exc.body},
                headers={
                    "Access-Control-Allow-Origin": origin,
                    "Access-Control-Allow-Credentials": "true",
                    "Access-Control-Expose-Headers": "X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Window",
                },
            )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors(), "body": exc.body},
    )


app.include_router(v1_router, prefix="/v1", tags=["v1"])
app.include_router(webhooks.router, prefix="/internal", tags=["internal"])
app.include_router(github_webhooks.router, prefix="/internal", tags=["internal"])
app.include_router(admin.router, prefix="/internal", tags=["internal"])

app.include_router(
    google_oauth_router,
    prefix="/auth/google",
    tags=["auth"],
)

app.include_router(
    github_oauth_router,
    prefix="/auth/github",
    tags=["auth"],
)

@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Shutdown scheduler and cleanup on shutdown."""
    from api.database.redis_client import get_redis_manager

    logger.info("Shutting down application...")
    
    try:
        redis_manager = await get_redis_manager()
        if redis_manager:
            await redis_manager.close()
            logger.info("Redis connections closed")
    except Exception as e:
        logger.warning("Error closing Redis connections: %s", e)
    try:
        from api.scheduler import setup_scheduler
        
        scheduler = setup_scheduler()
        if scheduler and hasattr(scheduler, "running") and scheduler.running:
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully")
    except Exception as e:
        logger.warning("Error shutting down scheduler: %s", e)
    
    logger.info("Cancelling running pipelines...")
    try:
        from api.services.pipeline_execution_service import pipeline_execution_service
        cancelled = await pipeline_execution_service.cleanup_on_shutdown()
        if cancelled > 0:
            logger.info("Cancelled %d pipelines on shutdown", cancelled)
    except Exception as e:
        logger.warning("Error cancelling pipelines: %s", e)
    
    from api.services.job_worker import job_worker

    logger.info("Shutting down job worker...")
    await job_worker.stop()
    logger.info("Job worker stopped")


app.include_router(
    fastapi_users.get_auth_router(jwt_authentication),
    prefix="/auth/jwt",
    tags=["auth"],
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)

