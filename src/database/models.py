"""
ORBIT Database Models
SQLAlchemy models for the ORBIT platform
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
import json

from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()


class User(Base):
    """User model with comprehensive profile data"""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    
    # Profile information
    timezone = Column(String(50), default="UTC")
    language = Column(String(10), default="en")
    onboarding_completed = Column(Boolean, default=False)
    
    # Subscription and billing
    subscription_tier = Column(String(50), default="starter")  # starter, pro, elite
    subscription_status = Column(String(50), default="active")
    billing_customer_id = Column(String(255), nullable=True)
    
    # User preferences and settings
    preferences = Column(JSON, default=dict)
    notification_settings = Column(JSON, default=dict)
    privacy_settings = Column(JSON, default=dict)
    
    # Behavioral data
    personality_traits = Column(JSON, default=dict)  # Big 5 personality scores
    behavioral_patterns = Column(JSON, default=dict)  # Cached pattern analysis
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    goals = relationship("Goal", back_populates="user", cascade="all, delete-orphan")
    interventions = relationship("Intervention", back_populates="user", cascade="all, delete-orphan")
    user_sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    integrations = relationship("Integration", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, name={self.name})>"
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "email": self.email,
            "name": self.name,
            "timezone": self.timezone,
            "subscription_tier": self.subscription_tier,
            "onboarding_completed": self.onboarding_completed,
            "created_at": self.created_at.isoformat(),
            "last_active": self.last_active.isoformat()
        }


class Goal(Base):
    """Goal model with comprehensive tracking"""
    __tablename__ = "goals"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Basic goal information
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    domain = Column(String(50), nullable=False)  # health, finance, productivity, learning, social
    
    # Goal specifics
    target_value = Column(String(255), nullable=True)  # Flexible target (number, text, etc.)
    current_value = Column(String(255), nullable=True)
    unit = Column(String(100), nullable=True)
    
    # Progress and status
    progress = Column(Float, default=0.0)  # 0.0 to 1.0
    status = Column(String(50), default="active")  # active, paused, completed, abandoned
    priority = Column(Integer, default=3)  # 1-5 priority scale
    
    # Dates
    created_date = Column(DateTime, default=datetime.utcnow)
    target_date = Column(DateTime, nullable=True)
    completed_date = Column(DateTime, nullable=True)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # AI and behavioral data
    ai_insights = Column(JSON, default=list)  # AI-generated insights
    behavioral_data = Column(JSON, default=dict)  # Behavioral patterns for this goal
    success_predictors = Column(JSON, default=dict)  # Factors that predict success
    
    # Goal relationships and dependencies
    parent_goal_id = Column(UUID(as_uuid=True), ForeignKey("goals.id"), nullable=True)
    goal_interactions = Column(JSON, default=list)  # Cross-domain interactions
    
    # Timestamps
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="goals")
    interventions = relationship("Intervention", back_populates="goal")
    progress_logs = relationship("ProgressLog", back_populates="goal", cascade="all, delete-orphan")
    parent_goal = relationship("Goal", remote_side=[id])
    
    def __repr__(self):
        return f"<Goal(id={self.id}, title={self.title}, domain={self.domain}, progress={self.progress})>"
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
            "domain": self.domain,
            "target_value": self.target_value,
            "current_value": self.current_value,
            "unit": self.unit,
            "progress": self.progress,
            "status": self.status,
            "priority": self.priority,
            "created_date": self.created_date.isoformat(),
            "target_date": self.target_date.isoformat() if self.target_date else None,
            "ai_insights": self.ai_insights,
            "last_updated": self.last_updated.isoformat()
        }


class Intervention(Base):
    """Intervention model for tracking AI-generated interventions"""
    __tablename__ = "interventions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    goal_id = Column(UUID(as_uuid=True), ForeignKey("goals.id"), nullable=True)
    session_id = Column(String(255), nullable=False)
    
    # Intervention details
    intervention_type = Column(String(50), nullable=False)  # scheduled, reactive, predictive
    domain = Column(String(50), nullable=False)
    urgency = Column(String(50), default="medium")
    
    # Content and AI data
    content = Column(Text, nullable=False)
    reasoning = Column(Text, nullable=True)
    confidence = Column(Float, nullable=False)
    
    # Agent execution data
    worker_response = Column(JSON, default=dict)
    supervisor_evaluation = Column(JSON, default=dict)
    execution_metadata = Column(JSON, default=dict)
    execution_time_ms = Column(Integer, nullable=False)
    
    # User interaction
    delivered_at = Column(DateTime, default=datetime.utcnow)
    viewed_at = Column(DateTime, nullable=True)
    responded_at = Column(DateTime, nullable=True)
    
    # Feedback and outcomes
    user_complied = Column(Boolean, nullable=True)
    user_rating = Column(Integer, nullable=True)  # 1-5 rating
    user_feedback = Column(Text, nullable=True)
    completion_time_minutes = Column(Integer, nullable=True)
    difficulty_rating = Column(Integer, nullable=True)  # 1-5 difficulty
    
    # Context data
    user_context = Column(JSON, default=dict)  # User state at time of intervention
    external_context = Column(JSON, default=dict)  # External factors
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="interventions")
    goal = relationship("Goal", back_populates="interventions")
    
    def __repr__(self):
        return f"<Intervention(id={self.id}, type={self.intervention_type}, domain={self.domain})>"
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "intervention_type": self.intervention_type,
            "domain": self.domain,
            "content": self.content,
            "confidence": self.confidence,
            "delivered_at": self.delivered_at.isoformat(),
            "user_complied": self.user_complied,
            "user_rating": self.user_rating,
            "execution_time_ms": self.execution_time_ms
        }


class ProgressLog(Base):
    """Progress tracking for goals"""
    __tablename__ = "progress_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    goal_id = Column(UUID(as_uuid=True), ForeignKey("goals.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Progress data
    previous_value = Column(String(255), nullable=True)
    new_value = Column(String(255), nullable=False)
    progress_delta = Column(Float, nullable=False)  # Change in progress
    
    # Context
    log_type = Column(String(50), default="manual")  # manual, automatic, intervention_result
    notes = Column(Text, nullable=True)
    context_data = Column(JSON, default=dict)
    
    # Timestamps
    logged_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    goal = relationship("Goal", back_populates="progress_logs")
    
    def __repr__(self):
        return f"<ProgressLog(id={self.id}, goal_id={self.goal_id}, delta={self.progress_delta})>"


class UserSession(Base):
    """User session tracking for analytics"""
    __tablename__ = "user_sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Session data
    session_token = Column(String(255), unique=True, nullable=False)
    device_info = Column(JSON, default=dict)
    ip_address = Column(String(45), nullable=True)  # IPv6 compatible
    user_agent = Column(Text, nullable=True)
    
    # Session activity
    started_at = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    
    # Activity tracking
    page_views = Column(Integer, default=0)
    interventions_received = Column(Integer, default=0)
    goals_updated = Column(Integer, default=0)
    
    # Relationships
    user = relationship("User", back_populates="user_sessions")
    
    def __repr__(self):
        return f"<UserSession(id={self.id}, user_id={self.user_id}, started={self.started_at})>"


class Integration(Base):
    """External service integrations"""
    __tablename__ = "integrations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Integration details
    integration_type = Column(String(100), nullable=False)  # google_calendar, fitbit, etc.
    integration_name = Column(String(255), nullable=False)
    status = Column(String(50), default="connected")  # connected, disconnected, error
    
    # Credentials and settings (encrypted)
    encrypted_credentials = Column(Text, nullable=True)
    settings = Column(JSON, default=dict)
    
    # Sync information
    last_sync_at = Column(DateTime, nullable=True)
    next_sync_at = Column(DateTime, nullable=True)
    sync_frequency_minutes = Column(Integer, default=60)
    
    # Error tracking
    error_count = Column(Integer, default=0)
    last_error = Column(Text, nullable=True)
    last_error_at = Column(DateTime, nullable=True)
    
    # Data tracking
    total_records_synced = Column(Integer, default=0)
    last_sync_record_count = Column(Integer, default=0)
    
    # Timestamps
    connected_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="integrations")
    
    def __repr__(self):
        return f"<Integration(id={self.id}, type={self.integration_type}, status={self.status})>"
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "integration_type": self.integration_type,
            "integration_name": self.integration_name,
            "status": self.status,
            "last_sync_at": self.last_sync_at.isoformat() if self.last_sync_at else None,
            "connected_at": self.connected_at.isoformat()
        }


class OpikTrace(Base):
    """Store Opik traces for analysis and optimization"""
    __tablename__ = "opik_traces"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    # Opik trace data
    trace_id = Column(String(255), unique=True, nullable=False)
    span_id = Column(String(255), nullable=True)
    operation_name = Column(String(255), nullable=False)
    
    # Agent execution data
    agent_type = Column(String(50), nullable=False)
    model_used = Column(String(100), nullable=False)
    
    # Input/Output
    input_data = Column(JSON, nullable=False)
    output_data = Column(JSON, nullable=False)
    
    # Evaluation scores
    safety_score = Column(Float, nullable=True)
    relevance_score = Column(Float, nullable=True)
    accuracy_score = Column(Float, nullable=True)
    success_probability = Column(Float, nullable=True)
    engagement_quality = Column(Float, nullable=True)
    overall_score = Column(Float, nullable=True)
    
    # Performance metrics
    execution_time_ms = Column(Integer, nullable=False)
    token_usage = Column(JSON, default=dict)
    cost_estimate = Column(Float, nullable=True)
    
    # Context and metadata
    context_data = Column(JSON, default=dict)
    metadata = Column(JSON, default=dict)
    
    # Success tracking
    user_feedback_received = Column(Boolean, default=False)
    user_complied = Column(Boolean, nullable=True)
    user_rating = Column(Integer, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<OpikTrace(id={self.id}, agent={self.agent_type}, score={self.overall_score})>"


class SystemMetrics(Base):
    """System-wide metrics and analytics"""
    __tablename__ = "system_metrics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Metric identification
    metric_name = Column(String(255), nullable=False)
    metric_type = Column(String(50), nullable=False)  # counter, gauge, histogram
    
    # Metric data
    value = Column(Float, nullable=False)
    labels = Column(JSON, default=dict)  # Additional labels/dimensions
    
    # Aggregation period
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    granularity = Column(String(20), nullable=False)  # minute, hour, day, week, month
    
    # Timestamps
    recorded_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<SystemMetrics(name={self.metric_name}, value={self.value}, period={self.granularity})>"


# Database utility functions
def create_tables(engine):
    """Create all tables"""
    Base.metadata.create_all(bind=engine)


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()


def get_user_goals(db: Session, user_id: str, status: str = "active") -> List[Goal]:
    """Get user's goals by status"""
    query = db.query(Goal).filter(Goal.user_id == user_id)
    if status:
        query = query.filter(Goal.status == status)
    return query.all()


def get_recent_interventions(db: Session, user_id: str, limit: int = 10) -> List[Intervention]:
    """Get user's recent interventions"""
    return db.query(Intervention).filter(
        Intervention.user_id == user_id
    ).order_by(
        Intervention.delivered_at.desc()
    ).limit(limit).all()


def create_intervention(db: Session, intervention_data: Dict[str, Any]) -> Intervention:
    """Create a new intervention record"""
    intervention = Intervention(**intervention_data)
    db.add(intervention)
    db.commit()
    db.refresh(intervention)
    return intervention


def update_goal_progress(db: Session, goal_id: str, new_progress: float, notes: str = None) -> Goal:
    """Update goal progress and create progress log"""
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        return None
    
    # Create progress log
    progress_log = ProgressLog(
        goal_id=goal_id,
        user_id=goal.user_id,
        previous_value=str(goal.progress),
        new_value=str(new_progress),
        progress_delta=new_progress - goal.progress,
        notes=notes
    )
    
    # Update goal
    goal.progress = new_progress
    goal.last_updated = datetime.utcnow()
    
    if new_progress >= 1.0:
        goal.status = "completed"
        goal.completed_date = datetime.utcnow()
    
    db.add(progress_log)
    db.commit()
    db.refresh(goal)
    
    return goal