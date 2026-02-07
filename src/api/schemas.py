"""
ORBIT API Schemas
Pydantic models for request/response validation
"""

from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, validator
from enum import Enum


# User Schemas
class UserCreate(BaseModel):
    """Schema for creating a new user"""
    email: EmailStr
    name: str = Field(..., min_length=2, max_length=100)
    password: str = Field(..., min_length=8)


class UserResponse(BaseModel):
    """Schema for user response"""
    id: int
    email: str
    name: str
    created_at: datetime
    
    model_config = {
        "from_attributes": True
    }


class DomainType(str, Enum):
    HEALTH = "health"
    FINANCE = "finance"
    PRODUCTIVITY = "productivity"
    LEARNING = "learning"
    SOCIAL = "social"


class UrgencyLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TriggerType(str, Enum):
    SCHEDULED = "scheduled"
    REACTIVE = "reactive"
    PREDICTIVE = "predictive"
    GENERAL = "general"


# Request Schemas
class InterventionRequest(BaseModel):
    """Request for generating an intervention"""
    user_input: str = Field(..., description="User's input or situation description")
    session_id: str = Field(..., description="Session identifier")
    trigger_type: TriggerType = Field(default=TriggerType.GENERAL, description="Type of intervention trigger")
    domain: DomainType = Field(default=DomainType.PRODUCTIVITY, description="Primary domain for intervention")
    urgency: UrgencyLevel = Field(default=UrgencyLevel.MEDIUM, description="Urgency level")
    
    current_goals: List[Dict[str, Any]] = Field(default=[], description="User's current goals")
    user_state: Dict[str, Any] = Field(default={}, description="Current user state")
    recent_history: List[Dict[str, Any]] = Field(default=[], description="Recent user activity")
    external_context: Optional[Dict[str, Any]] = Field(default=None, description="External context data")
    
    @validator('user_input')
    def validate_user_input(cls, v):
        if not v or len(v.strip()) < 3:
            raise ValueError('User input must be at least 3 characters long')
        return v.strip()


class InterventionFeedback(BaseModel):
    """Feedback on an intervention"""
    complied: bool = Field(..., description="Whether user complied with intervention")
    rating: int = Field(..., ge=1, le=5, description="Rating from 1-5")
    feedback_text: Optional[str] = Field(None, description="Optional text feedback")
    completion_time_minutes: Optional[int] = Field(None, description="Time taken to complete")
    difficulty_rating: Optional[int] = Field(None, ge=1, le=5, description="Difficulty rating 1-5")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "complied": True,
                "rating": 4,
                "feedback_text": "This was helpful and well-timed",
                "completion_time_minutes": 15,
                "difficulty_rating": 2
            }
        }
    }


class GoalCreate(BaseModel):
    """Schema for creating a new goal"""
    title: str = Field(..., min_length=3, max_length=200, description="Goal title")
    description: Optional[str] = Field(None, max_length=1000, description="Goal description")
    domain: DomainType = Field(..., description="Goal domain")
    target_date: Optional[datetime] = Field(None, description="Target completion date")
    priority: int = Field(default=3, ge=1, le=5, description="Priority level 1-5")
    
    # Goal-specific metadata
    target_value: Optional[Union[int, float, str]] = Field(None, description="Target value (e.g., weight, amount)")
    current_value: Optional[Union[int, float, str]] = Field(None, description="Current value")
    unit: Optional[str] = Field(None, description="Unit of measurement")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Exercise 3 times per week",
                "description": "Build a consistent exercise habit",
                "domain": "health",
                "target_date": "2024-06-30T00:00:00Z",
                "priority": 4,
                "target_value": 3,
                "current_value": 1,
                "unit": "times per week"
            }
        }
    }


class GoalUpdate(BaseModel):
    """Schema for updating a goal"""
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    target_date: Optional[datetime] = None
    priority: Optional[int] = Field(None, ge=1, le=5)
    status: Optional[str] = Field(None, pattern="^(active|paused|completed|abandoned)$")
    current_value: Optional[Union[int, float, str]] = None


# Response Schemas
class EvaluationResponse(BaseModel):
    """Response containing AI evaluation metrics"""
    safety_score: float = Field(..., ge=0.0, le=1.0)
    relevance_score: float = Field(..., ge=0.0, le=1.0)
    accuracy_score: float = Field(..., ge=0.0, le=1.0)
    adherence_probability: float = Field(..., ge=0.0, le=1.0)
    engagement_quality: float = Field(..., ge=0.0, le=1.0)
    overall_score: float = Field(..., ge=0.0, le=1.0)
    feedback: Optional[str] = None
    
    model_config = {
        'from_attributes': True
    }


class InterventionResponse(BaseModel):
    """Response containing generated intervention"""
    intervention_id: str = Field(..., description="Unique intervention identifier")
    content: str = Field(..., description="Intervention content/message")
    reasoning: Optional[str] = Field(None, description="AI reasoning for the intervention")
    confidence: float = Field(..., ge=0.0, le=1.0, description="AI confidence score")
    
    supervisor_evaluation: Optional[Dict[str, Any]] = Field(None, description="Supervisor agent evaluation")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    execution_time_ms: int = Field(..., description="Execution time in milliseconds")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "intervention_id": "int_1640995200",
                "content": "Based on your energy patterns, now is a great time to tackle that important project. Start with just 25 minutes of focused work.",
                "reasoning": "User shows peak productivity at this time based on historical patterns",
                "confidence": 0.85,
                "supervisor_evaluation": {
                    "safety_score": {"score": 0.95, "reasoning": "Low risk intervention"},
                    "relevance_score": {"score": 0.88, "reasoning": "Well-aligned with user goals"},
                    "overall_score": 0.87,
                    "approved": True
                },
                "execution_time_ms": 1250
            }
        }
    }


class GoalResponse(BaseModel):
    """Response schema for goal data"""
    id: str = Field(..., description="Goal identifier")
    title: str = Field(..., description="Goal title")
    description: Optional[str] = Field(None, description="Goal description")
    domain: DomainType = Field(..., description="Goal domain")
    status: str = Field(..., description="Goal status")
    progress: float = Field(..., ge=0.0, le=1.0, description="Progress percentage (0-1)")
    
    created_date: datetime = Field(..., description="Creation date")
    target_date: Optional[datetime] = Field(None, description="Target completion date")
    last_updated: datetime = Field(..., description="Last update date")
    
    priority: int = Field(..., description="Priority level")
    target_value: Optional[Union[int, float, str]] = None
    current_value: Optional[Union[int, float, str]] = None
    unit: Optional[str] = None
    
    # AI insights
    ai_insights: Optional[List[str]] = Field(default=[], description="AI-generated insights")
    next_actions: Optional[List[str]] = Field(default=[], description="Suggested next actions")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "goal_123",
                "title": "Exercise 3 times per week",
                "description": "Build a consistent exercise habit",
                "domain": "health",
                "status": "active",
                "progress": 0.65,
                "created_date": "2024-01-01T00:00:00Z",
                "target_date": "2024-06-30T00:00:00Z",
                "last_updated": "2024-01-15T10:30:00Z",
                "priority": 4,
                "target_value": 3,
                "current_value": 2,
                "unit": "times per week",
                "ai_insights": ["You exercise best in the mornings", "Consistency is improving"],
                "next_actions": ["Schedule tomorrow's workout", "Prepare gym clothes tonight"]
            }
        }
    }


class UserPatterns(BaseModel):
    """User behavioral patterns response"""
    user_id: str = Field(..., description="User identifier")
    analysis_timestamp: datetime = Field(..., description="When analysis was performed")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Overall pattern confidence")
    
    insights: List[Dict[str, Any]] = Field(default=[], description="Behavioral insights")
    recommendations: List[str] = Field(default=[], description="Personalized recommendations")
    
    # Pattern categories
    temporal_patterns: Dict[str, Any] = Field(default={}, description="Time-based patterns")
    compliance_patterns: Dict[str, Any] = Field(default={}, description="Compliance patterns")
    energy_patterns: Dict[str, Any] = Field(default={}, description="Energy level patterns")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": "user_123",
                "analysis_timestamp": "2024-01-15T10:30:00Z",
                "confidence": 0.85,
                "insights": [
                    {
                        "type": "optimal_timing",
                        "insight": "You're most productive between 9-11 AM",
                        "confidence": 0.9,
                        "actionable": True
                    }
                ],
                "recommendations": [
                    "Schedule important tasks during peak hours",
                    "Take breaks when energy is low"
                ]
            }
        }
    }


class DashboardData(BaseModel):
    """Dashboard data response"""
    user: Dict[str, Any] = Field(..., description="User information")
    today_focus: str = Field(..., description="Today's main focus area")
    energy_level: str = Field(..., description="Current energy level")
    
    ai_reliability: Dict[str, Any] = Field(..., description="AI performance metrics")
    goals: List[Dict[str, Any]] = Field(default=[], description="Active goals summary")
    todays_plan: List[Dict[str, Any]] = Field(default=[], description="Today's planned activities")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "user": {
                    "id": "user_123",
                    "name": "Alex Johnson",
                    "streak_days": 14,
                    "total_goals": 5,
                    "active_goals": 3
                },
                "today_focus": "Financial discipline",
                "energy_level": "7/10",
                "ai_reliability": {
                    "interventions_this_week": 47,
                    "helpful_percentage": 89,
                    "safety_score": 0.97
                },
                "goals": [
                    {
                        "id": "goal_1",
                        "title": "Exercise 3x/week",
                        "progress": 78,
                        "next_action": "Tomorrow 7 AM workout"
                    }
                ]
            }
        }
    }


# Integration Schemas
class IntegrationConnect(BaseModel):
    """Schema for connecting external integrations"""
    integration_type: str = Field(..., description="Type of integration (google_calendar, fitbit, etc.)")
    credentials: Dict[str, Any] = Field(..., description="Integration credentials")
    settings: Optional[Dict[str, Any]] = Field(default={}, description="Integration settings")


class IntegrationStatus(BaseModel):
    """Integration status response"""
    integration_type: str = Field(..., description="Integration type")
    status: str = Field(..., description="Connection status")
    last_sync: Optional[datetime] = Field(None, description="Last successful sync")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "integration_type": "google_calendar",
                "status": "connected",
                "last_sync": "2024-01-15T10:30:00Z",
                "error_message": None
            }
        }
    }


# Analytics Schemas
class AnalyticsRequest(BaseModel):
    """Request for analytics data"""
    start_date: datetime = Field(..., description="Start date for analytics")
    end_date: datetime = Field(..., description="End date for analytics")
    metrics: List[str] = Field(default=[], description="Specific metrics to include")
    granularity: str = Field(default="daily", pattern="^(hourly|daily|weekly|monthly)$")


class AnalyticsResponse(BaseModel):
    """Analytics data response"""
    period: Dict[str, datetime] = Field(..., description="Analysis period")
    metrics: Dict[str, Any] = Field(..., description="Calculated metrics")
    trends: Dict[str, Any] = Field(default={}, description="Trend analysis")
    insights: List[str] = Field(default=[], description="Key insights")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "period": {
                    "start_date": "2024-01-01T00:00:00Z",
                    "end_date": "2024-01-15T23:59:59Z"
                },
                "metrics": {
                    "goal_completion_rate": 0.78,
                    "intervention_compliance": 0.85,
                    "average_daily_progress": 0.12
                },
                "trends": {
                    "goal_completion": "improving",
                    "engagement": "stable"
                },
                "insights": [
                    "Your morning productivity has increased 23%",
                    "Health goals show strongest progress"
                ]
            }
        }
    }


# Error Schemas
class ErrorResponse(BaseModel):
    """Standard error response"""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Error timestamp")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "error": "ValidationError",
                "message": "Invalid input data",
                "details": {"field": "user_input", "issue": "too short"},
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }
    }


# Health Check Schema
class HealthCheck(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Overall health status")
    timestamp: float = Field(..., description="Check timestamp")
    version: str = Field(..., description="API version")
    agents: Dict[str, Dict[str, Any]] = Field(default={}, description="Agent health status")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "healthy",
                "timestamp": 1640995200.0,
                "version": "1.0.0",
                "agents": {
                    "worker": {"status": "healthy", "response_time_ms": 150},
                    "supervisor": {"status": "healthy", "response_time_ms": 95}
                }
            }
        }
    }