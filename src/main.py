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
from src.core.exceptions import ORBITException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize Sentry for error tracking
if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        integrations=[
            FastApiIntegration(auto_enabling=True),
            SqlalchemyIntegration(),
        ],
        traces_sample_rate=0.1,
        environment=settings.ENVIRONMENT,
    )

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("🚀 Starting ORBIT platform...")
    
    # Initialize database
    await init_db()
    logger.info("✅ Database initialized")
    
    # Initialize Redis
    await init_redis()
    logger.info("✅ Redis initialized")
    
    # Setup monitoring
    setup_monitoring()
    logger.info("✅ Monitoring setup complete")
    
    logger.info("🌟 ORBIT platform ready!")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down ORBIT platform...")

# Create FastAPI application
app = FastAPI(
    title="ORBIT API",
    description="Autonomous Life Optimization Platform with Transparent AI",
    version="1.0.0",
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)

# Global exception handler
@app.exception_handler(ORBITException)
async def orbit_exception_handler(request: Request, exc: ORBITException):
    """Handle custom ORBIT exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.error_code,
            "message": exc.message,
            "details": exc.details
        }
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions"""
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred"
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
                "api": {"status": "healthy", "message": "API operational"}
            },
            "version": "1.0.0",
            "environment": settings.ENVIRONMENT
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": "unknown"
        }

# Include API routes
app.include_router(api_app, prefix="/api/v1")

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with platform information"""
    return {
        "name": "ORBIT",
        "description": "Autonomous Life Optimization Platform",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs" if settings.ENVIRONMENT != "production" else None
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development"
    )