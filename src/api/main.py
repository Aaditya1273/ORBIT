"""
ORBIT FastAPI Application
World-class API for the autonomous life optimization platform
"""

import asyncio
import time
from contextlib import asynccontextmanager
from typing import Dict, Any, List, Optional

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import structlog
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

from ..core.config import settings
from ..agents.base_agent import AgentOrchestrator, AgentContext
from ..agents.worker_agent import WorkerAgent
from ..agents.supervisor_agent import SupervisorAgent
from ..database.models import User, Goal, Intervention
from ..database.database import get_db
from .routers import auth, goals, interventions, analytics, integrations
from .middleware import RateLimitMiddleware, AuthenticationMiddleware
from .schemas import *

# Configure logging
logger = structlog.get_logger(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter('orbit_requests_total', 'Total requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('orbit_request_duration_seconds', 'Request duration')
INTERVENTION_COUNT = Counter('orbit_interventions_total', 'Total interventions', ['type', 'domain'])
AGENT_EXECUTION_TIME = Histogram('orbit_agent_execution_seconds', 'Agent execution time', ['agent_type'])

# Global agent orchestrator
orchestrator = AgentOrchestrator()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    logger.info("Starting ORBIT API server", version=settings.APP_VERSION)
    
    # Initialize agents
    worker_agent = WorkerAgent()
    supervisor_agent = SupervisorAgent()
    
    orchestrator.register_agent("worker", worker_agent)
    orchestrator.register_agent("supervisor", supervisor_agent)
    
    # Health check all agents
    health_results = await orchestrator.health_check_all()
    logger.info("Agent health check completed", results=health_results)
    
    yield
    
    # Shutdown
    logger.info("Shutting down ORBIT API server")


# Create FastAPI app
app = FastAPI(
    title="ORBIT API",
    description="Autonomous Life Optimization Platform",
    version=settings.APP_VERSION,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.DEBUG else ["https://orbit.ai", "https://app.orbit.ai"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"] if settings.DEBUG else ["orbit.ai", "api.orbit.ai", "localhost"]
)

app.add_middleware(RateLimitMiddleware)
app.add_middleware(AuthenticationMiddleware)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(goals.router, prefix="/api/v1/goals", tags=["goals"])
app.include_router(interventions.router, prefix="/api/v1/interventions", tags=["interventions"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])
app.include_router(integrations.router, prefix="/api/v1/integrations", tags=["integrations"])


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    """Collect metrics for all requests"""
    start_time = time.time()
    
    response = await call_next(request)
    
    # Record metrics
    duration = time.time() - start_time
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    REQUEST_DURATION.observe(duration)
    
    return response


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "ORBIT API",
        "version": settings.APP_VERSION,
        "description": "Autonomous Life Optimization Platform",
        "status": "operational",
        "docs": "/docs" if settings.DEBUG else None
    }


@app.get("/health")
async def health_check():
    """Comprehensive health check endpoint"""
    try:
        # Check agent health
        agent_health = await orchestrator.health_check_all()
        
        # Check database connectivity
        # db_health = await check_database_health()
        
        # Check external services
        # external_health = await check_external_services()
        
        health_status = {
            "status": "healthy",
            "timestamp": time.time(),
            "version": settings.APP_VERSION,
            "agents": agent_health,
            # "database": db_health,
            # "external_services": external_health
        }
        
        return health_status
        
    except Exception as e:
        logger.error("Health check failed", error=str(e))
        raise HTTPException(status_code=503, detail="Service unhealthy")


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/api/v1/interventions/generate")
async def generate_intervention(
    request: InterventionRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user)
):
    """
    Generate a personalized intervention using the agent orchestrator
    """
    try:
        start_time = time.time()
        
        # Build agent context
        context = AgentContext(
            user_id=str(current_user.id),
            session_id=request.session_id,
            current_goals=request.current_goals,
            user_state=request.user_state,
            recent_history=request.recent_history,
            external_context=request.external_context
        )
        
        # Execute intervention pipeline
        results = await orchestrator.execute_workflow(
            workflow_name="intervention_pipeline",
            context=context,
            user_input=request.user_input,
            urgency=request.urgency,
            domain=request.domain
        )
        
        # Extract results
        worker_response = results.get("worker")
        supervisor_evaluation = results.get("supervisor")
        
        if not worker_response:
            raise HTTPException(status_code=500, detail="Worker agent failed to generate intervention")
        
        # Record metrics
        execution_time = time.time() - start_time
        AGENT_EXECUTION_TIME.labels(agent_type="intervention_pipeline").observe(execution_time)
        INTERVENTION_COUNT.labels(
            type=request.trigger_type,
            domain=request.domain
        ).inc()
        
        # Store intervention in database (background task)
        background_tasks.add_task(
            store_intervention,
            current_user.id,
            worker_response,
            supervisor_evaluation
        )
        
        # Return response
        response = InterventionResponse(
            intervention_id=f"int_{int(time.time())}",
            content=worker_response.content,
            reasoning=worker_response.reasoning,
            confidence=worker_response.confidence,
            supervisor_evaluation=supervisor_evaluation.to_dict() if supervisor_evaluation else None,
            metadata=worker_response.metadata,
            execution_time_ms=worker_response.execution_time_ms
        )
        
        logger.info(
            "Intervention generated successfully",
            user_id=current_user.id,
            domain=request.domain,
            confidence=worker_response.confidence,
            execution_time_ms=worker_response.execution_time_ms
        )
        
        return response
        
    except Exception as e:
        logger.error(
            "Intervention generation failed",
            user_id=current_user.id,
            error=str(e),
            exc_info=True
        )
        raise HTTPException(status_code=500, detail=f"Failed to generate intervention: {str(e)}")


@app.post("/api/v1/interventions/{intervention_id}/feedback")
async def submit_intervention_feedback(
    intervention_id: str,
    feedback: InterventionFeedback,
    current_user: User = Depends(get_current_user)
):
    """
    Submit feedback on an intervention for learning
    """
    try:
        # Store feedback for optimizer agent
        await store_intervention_feedback(
            intervention_id=intervention_id,
            user_id=current_user.id,
            feedback=feedback
        )
        
        logger.info(
            "Intervention feedback received",
            intervention_id=intervention_id,
            user_id=current_user.id,
            complied=feedback.complied,
            rating=feedback.rating
        )
        
        return {"status": "success", "message": "Feedback recorded"}
        
    except Exception as e:
        logger.error(
            "Failed to store intervention feedback",
            intervention_id=intervention_id,
            error=str(e)
        )
        raise HTTPException(status_code=500, detail="Failed to record feedback")


@app.get("/api/v1/users/me/patterns")
async def get_user_patterns(
    current_user: User = Depends(get_current_user)
):
    """
    Get user's behavioral patterns and insights
    """
    try:
        # This would typically fetch from cache or database
        # For now, return mock data
        patterns = {
            "user_id": str(current_user.id),
            "analysis_timestamp": time.time(),
            "confidence": 0.85,
            "insights": [
                {
                    "type": "optimal_timing",
                    "insight": "You're most productive between 9-11 AM and 2-4 PM",
                    "confidence": 0.9,
                    "actionable": True
                },
                {
                    "type": "compliance_success",
                    "insight": "Your compliance rate is 78% - excellent progress!",
                    "confidence": 0.85,
                    "actionable": True
                }
            ],
            "recommendations": [
                "Schedule important tasks during your peak hours",
                "Continue your current approach - it's working well"
            ]
        }
        
        return patterns
        
    except Exception as e:
        logger.error(
            "Failed to get user patterns",
            user_id=current_user.id,
            error=str(e)
        )
        raise HTTPException(status_code=500, detail="Failed to retrieve patterns")


@app.get("/api/v1/dashboard")
async def get_dashboard_data(
    current_user: User = Depends(get_current_user)
):
    """
    Get comprehensive dashboard data for the user
    """
    try:
        # This would aggregate data from multiple sources
        dashboard_data = {
            "user": {
                "id": str(current_user.id),
                "name": current_user.name,
                "streak_days": 14,
                "total_goals": 5,
                "active_goals": 3
            },
            "today_focus": "Financial discipline",
            "energy_level": "7/10",
            "ai_reliability": {
                "interventions_this_week": 47,
                "helpful_percentage": 89,
                "safety_score": 0.97,
                "relevance_score": 0.89,
                "accuracy_score": 0.82
            },
            "goals": [
                {
                    "id": "goal_1",
                    "title": "Exercise 3x/week",
                    "domain": "health",
                    "progress": 78,
                    "next_action": "Tomorrow 7 AM workout",
                    "ai_insight": "You exercise best in mornings ☀️"
                },
                {
                    "id": "goal_2",
                    "title": "Save $500/month",
                    "domain": "finance",
                    "progress": 82,
                    "next_action": "Review budget",
                    "ai_insight": "Big purchase temptation detected ⚠️"
                }
            ],
            "todays_plan": [
                {"time": "7:00 AM", "action": "☕ Review budget before coffee shop"},
                {"time": "9:30 AM", "action": "💼 Deep work block (3 hrs)"},
                {"time": "12:30 PM", "action": "🥗 Meal prep reminder"},
                {"time": "3:00 PM", "action": "🧘 Meditation break"},
                {"time": "6:00 PM", "action": "🏃 Workout: 30-min run"},
                {"time": "10:00 PM", "action": "🌙 Wind-down routine"}
            ]
        }
        
        return dashboard_data
        
    except Exception as e:
        logger.error(
            "Failed to get dashboard data",
            user_id=current_user.id,
            error=str(e)
        )
        raise HTTPException(status_code=500, detail="Failed to retrieve dashboard data")


# Background tasks
async def store_intervention(
    user_id: int,
    worker_response: Any,
    supervisor_evaluation: Any
):
    """Store intervention in database"""
    try:
        # This would store in the database
        logger.info(
            "Intervention stored",
            user_id=user_id,
            confidence=worker_response.confidence
        )
    except Exception as e:
        logger.error(f"Failed to store intervention: {str(e)}")


async def store_intervention_feedback(
    intervention_id: str,
    user_id: int,
    feedback: Any
):
    """Store intervention feedback for learning"""
    try:
        # This would store feedback in database for optimizer agent
        logger.info(
            "Feedback stored",
            intervention_id=intervention_id,
            user_id=user_id
        )
    except Exception as e:
        logger.error(f"Failed to store feedback: {str(e)}")


# Dependency functions
async def get_current_user() -> User:
    """Get current authenticated user"""
    # Mock user for now
    return User(
        id=1,
        name="Alex Johnson",
        email="alex@example.com"
    )


if __name__ == "__main__":
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )