"""
ORBIT API Routes
FastAPI router with all API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.security import HTTPBearer
from typing import List, Dict, Any
import uuid
from datetime import datetime

from .schemas import (
    GoalCreate, GoalResponse, InterventionRequest, InterventionResponse,
    UserCreate, UserResponse, EvaluationResponse
)
from ..agents.worker_agent import WorkerAgent
from ..agents.supervisor_agent import SupervisorAgent
from ..agents.base_agent import AgentContext
from ..core.redis import cache, session_manager
from ..database.models import User, Goal, Intervention

# Create API router
app = APIRouter()

# Security
security = HTTPBearer()

# Initialize agents
worker_agent = WorkerAgent()
supervisor_agent = SupervisorAgent()

@app.get("/")
async def api_root():
    """API root endpoint"""
    return {
        "name": "ORBIT API",
        "version": "1.0.0",
        "description": "Autonomous Life Optimization Platform API",
        "endpoints": {
            "health": "/health",
            "goals": "/goals",
            "interventions": "/interventions",
            "users": "/users"
        }
    }

@app.get("/health")
async def api_health():
    """API health check"""
    try:
        # Test agent health
        worker_health = await worker_agent.health_check()
        supervisor_health = await supervisor_agent.health_check()
        
        return {
            "status": "healthy",
            "agents": {
                "worker": worker_health,
                "supervisor": supervisor_health
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

@app.post("/interventions/generate", response_model=InterventionResponse)
async def generate_intervention(
    request: InterventionRequest,
    background_tasks: BackgroundTasks
):
    """Generate AI intervention for user goal"""
    try:
        # Create agent context
        context = AgentContext(
            user_id=request.user_id,
            session_id=str(uuid.uuid4()),
            current_goals=request.goals,
            user_state=request.user_state or {},
            recent_history=request.recent_history or [],
            external_context=request.external_context or {}
        )
        
        # Generate intervention with Worker Agent
        worker_response = await worker_agent.execute(
            context=context,
            user_input=request.user_input
        )
        
        # Evaluate with Supervisor Agent
        supervisor_response = await supervisor_agent.execute(
            context=context,
            user_input=worker_response.content
        )
        
        # Cache the intervention
        intervention_id = str(uuid.uuid4())
        await cache.set(
            f"intervention:{intervention_id}",
            {
                "worker_response": worker_response.to_dict(),
                "supervisor_response": supervisor_response.to_dict(),
                "context": request.dict(),
                "timestamp": datetime.utcnow().isoformat()
            },
            expire=3600  # 1 hour
        )
        
        return InterventionResponse(
            id=intervention_id,
            content=worker_response.content,
            reasoning=worker_response.reasoning,
            confidence=worker_response.confidence,
            evaluation=EvaluationResponse(
                safety_score=supervisor_response.metadata.get("safety_score", 0.8),
                relevance_score=supervisor_response.metadata.get("relevance_score", 0.8),
                accuracy_score=supervisor_response.metadata.get("accuracy_score", 0.8),
                success_probability=supervisor_response.metadata.get("success_probability", 0.7),
                engagement_quality=supervisor_response.metadata.get("engagement_quality", 0.8),
                overall_score=supervisor_response.confidence,
                reasoning=supervisor_response.reasoning
            ),
            metadata={
                "worker_model": worker_response.model_used,
                "supervisor_model": supervisor_response.model_used,
                "execution_time_ms": worker_response.execution_time_ms + supervisor_response.execution_time_ms,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Intervention generation failed: {str(e)}")

@app.get("/interventions/{intervention_id}")
async def get_intervention(intervention_id: str):
    """Get cached intervention by ID"""
    intervention = await cache.get(f"intervention:{intervention_id}")
    
    if not intervention:
        raise HTTPException(status_code=404, detail="Intervention not found")
    
    return intervention

@app.post("/goals", response_model=GoalResponse)
async def create_goal(goal: GoalCreate):
    """Create a new user goal"""
    try:
        goal_id = str(uuid.uuid4())
        goal_data = {
            "id": goal_id,
            "title": goal.title,
            "description": goal.description,
            "domain": goal.domain,
            "target_value": goal.target_value,
            "current_value": goal.current_value,
            "unit": goal.unit,
            "deadline": goal.deadline.isoformat() if goal.deadline else None,
            "priority": goal.priority,
            "status": "active",
            "created_at": datetime.utcnow().isoformat()
        }
        
        # Cache the goal
        await cache.set(f"goal:{goal_id}", goal_data, expire=86400)  # 24 hours
        
        return GoalResponse(**goal_data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Goal creation failed: {str(e)}")

@app.get("/goals", response_model=List[GoalResponse])
async def list_goals(user_id: str):
    """List all goals for a user"""
    try:
        # In a real implementation, this would query the database
        # For now, return cached goals
        goal_keys = await cache.list_keys(f"goal:*")
        goals = []
        
        for key in goal_keys:
            goal_data = await cache.get(key)
            if goal_data:
                goals.append(GoalResponse(**goal_data))
        
        return goals
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list goals: {str(e)}")

@app.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate):
    """Create a new user"""
    try:
        user_id = str(uuid.uuid4())
        user_data = {
            "id": user_id,
            "email": user.email,
            "name": user.name,
            "preferences": user.preferences or {},
            "created_at": datetime.utcnow().isoformat(),
            "is_active": True
        }
        
        # Cache user data
        await cache.set(f"user:{user_id}", user_data, expire=86400)
        
        # Create session
        session_id = await session_manager.create_session(
            user_id=user_id,
            session_data={"user_id": user_id, "email": user.email}
        )
        
        user_data["session_id"] = session_id
        return UserResponse(**user_data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"User creation failed: {str(e)}")

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    """Get user by ID"""
    user_data = await cache.get(f"user:{user_id}")
    
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(**user_data)

@app.get("/test/openrouter")
async def test_openrouter():
    """Test OpenRouter integration"""
    try:
        # Simple test of both agents
        context = AgentContext(
            user_id="test_user",
            session_id="test_session",
            current_goals=[{
                "title": "Test Goal",
                "domain": "productivity",
                "progress": 0.5
            }],
            user_state={"test": True},
            recent_history=[]
        )
        
        # Test Worker Agent (Gemini)
        worker_response = await worker_agent.execute(
            context=context,
            user_input="Generate a simple productivity tip"
        )
        
        # Test Supervisor Agent (Claude via OpenRouter)
        supervisor_response = await supervisor_agent.execute(
            context=context,
            user_input=worker_response.content
        )
        
        return {
            "status": "success",
            "worker_agent": {
                "model": worker_response.model_used,
                "response": worker_response.content[:100] + "...",
                "confidence": worker_response.confidence,
                "execution_time_ms": worker_response.execution_time_ms
            },
            "supervisor_agent": {
                "model": supervisor_response.model_used,
                "response": supervisor_response.content[:100] + "...",
                "confidence": supervisor_response.confidence,
                "execution_time_ms": supervisor_response.execution_time_ms
            },
            "total_time_ms": worker_response.execution_time_ms + supervisor_response.execution_time_ms
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "OpenRouter integration test failed"
        }

@app.get("/test/redis")
async def test_redis():
    """Test Redis connection and operations"""
    try:
        # Test basic operations
        test_key = f"test:{uuid.uuid4()}"
        test_value = {"message": "Redis test", "timestamp": datetime.utcnow().isoformat()}
        
        # Set value
        await cache.set(test_key, test_value, expire=60)
        
        # Get value
        retrieved_value = await cache.get(test_key)
        
        # Delete value
        await cache.delete(test_key)
        
        return {
            "status": "success",
            "operations": {
                "set": "success",
                "get": "success" if retrieved_value == test_value else "failed",
                "delete": "success"
            },
            "test_data": {
                "original": test_value,
                "retrieved": retrieved_value
            }
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Redis test failed"
        }