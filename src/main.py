"""
ORBIT - Autonomous Life Optimization Platform
Main FastAPI application entry point
"""

import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

from src.core.config import settings
from src.database.database import init_db
from src.core.redis import init_redis, health_check_redis
from src.api.main import app as api_app

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize Sentry for error tracking and performance monitoring
if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        # Enable FastAPI integration for automatic request tracking
        integrations=[
            FastApiIntegration(),
            SqlalchemyIntegration(),
        ],
        # Set traces_sample_rate to 1.0 to capture 100% of transactions for performance monitoring
        # In production, reduce this to 0.1 (10%) or lower to reduce volume
        traces_sample_rate=1.0 if settings.ENVIRONMENT == "development" else 0.1,
        
        # Send default PII (Personally Identifiable Information) like user IP, headers
        send_default_pii=True,
        
        # Set environment
        environment=settings.ENVIRONMENT,
        
        # Release tracking (optional)
        release=f"orbit@{settings.APP_VERSION}",
        
        # Enable profiling (optional)
        profiles_sample_rate=0.1,
    )
    logger.info("✅ Sentry error monitoring initialized")
else:
    logger.warning("⚠️  Sentry DSN not configured - error monitoring disabled")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("🚀 Starting ORBIT platform...")
    
    # Initialize database
    try:
        from src.database.database import init_db
        init_db()  # Create all tables
        logger.info("✅ Database initialized")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        if settings.SENTRY_DSN:
            sentry_sdk.capture_exception(e)
    
    # Initialize Redis
    try:
        await init_redis()
        logger.info("✅ Redis initialized")
    except Exception as e:
        logger.error(f"❌ Redis initialization failed: {e}")
        if settings.SENTRY_DSN:
            sentry_sdk.capture_exception(e)
    
    logger.info("🌟 ORBIT platform ready!")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down ORBIT platform...")

# Create FastAPI application
app = FastAPI(
    title="ORBIT API",
    description="Autonomous Life Optimization Platform with Transparent AI",
    version=settings.APP_VERSION,
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"] + settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "0.0.0.0"] + settings.ALLOWED_HOSTS
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions and send to Sentry"""
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    
    # Capture exception in Sentry
    if settings.SENTRY_DSN:
        sentry_sdk.capture_exception(exc)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred",
            "detail": str(exc) if settings.DEBUG else None
        }
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    """Comprehensive health check"""
    try:
        # Check Redis connection
        redis_health = await health_check_redis()
        
        # Check database (basic connection test)
        db_health = {"status": "healthy", "message": "Database connection successful"}
        
        # Overall health status
        overall_status = "healthy" if redis_health["status"] == "healthy" else "degraded"
        
        return {
            "status": overall_status,
            "timestamp": redis_health["timestamp"],
            "services": {
                "redis": redis_health,
                "database": db_health,
                "api": {"status": "healthy", "message": "API operational"},
                "sentry": {
                    "status": "enabled" if settings.SENTRY_DSN else "disabled",
                    "environment": settings.ENVIRONMENT
                }
            },
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        
        # Capture health check failures in Sentry
        if settings.SENTRY_DSN:
            sentry_sdk.capture_exception(e)
        
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": "unknown"
        }

# Sentry debug endpoint (only in development)
@app.get("/sentry-debug")
async def trigger_sentry_error():
    """
    Trigger a test error to verify Sentry integration
    Only available in development mode
    """
    if settings.ENVIRONMENT != "development":
        return JSONResponse(
            status_code=403,
            content={"error": "This endpoint is only available in development mode"}
        )
    
    # This will trigger an error and send it to Sentry
    division_by_zero = 1 / 0
    return {"message": "This should never be reached"}

# Include API routes
from src.api.auth import router as auth_router
app.include_router(auth_router, prefix="/api/v1")
app.include_router(api_app, prefix="/api/v1")

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with platform information"""
    return {
        "name": "ORBIT",
        "description": "Autonomous Life Optimization Platform",
        "version": settings.APP_VERSION,
        "status": "operational",
        "environment": settings.ENVIRONMENT,
        "monitoring": {
            "sentry": "enabled" if settings.SENTRY_DSN else "disabled",
            "opik": "enabled" if settings.OPIK_API_KEY else "disabled"
        },
        "docs": "/docs" if settings.ENVIRONMENT != "production" else None,
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development"
    )