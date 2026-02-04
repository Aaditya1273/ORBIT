"""
ORBIT Core Configuration
World-class configuration management with environment-based settings
"""

from functools import lru_cache
from typing import Optional, List
from pydantic import BaseSettings, Field
import os


class Settings(BaseSettings):
    """Application settings with intelligent defaults and validation"""
    
    # Application
    APP_NAME: str = "ORBIT"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=False, env="DEBUG")
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Database
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    REDIS_URL: str = Field(default="redis://localhost:6379", env="REDIS_URL")
    
    # AI Models Configuration
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    ANTHROPIC_API_KEY: str = Field(..., env="ANTHROPIC_API_KEY")
    GOOGLE_API_KEY: str = Field(..., env="GOOGLE_API_KEY")
    
    # Worker Agent (Primary AI)
    WORKER_MODEL: str = Field(default="gemini-1.5-pro", env="WORKER_MODEL")
    WORKER_TEMPERATURE: float = Field(default=0.7, env="WORKER_TEMPERATURE")
    WORKER_MAX_TOKENS: int = Field(default=2048, env="WORKER_MAX_TOKENS")
    
    # Supervisor Agent (Evaluation)
    SUPERVISOR_MODEL: str = Field(default="gpt-4-turbo", env="SUPERVISOR_MODEL")
    SUPERVISOR_TEMPERATURE: float = Field(default=0.1, env="SUPERVISOR_TEMPERATURE")  # Low temp for consistency
    
    # Optimizer Agent (Learning)
    OPTIMIZER_MODEL: str = Field(default="claude-3-sonnet", env="OPTIMIZER_MODEL")
    OPTIMIZER_TEMPERATURE: float = Field(default=0.3, env="OPTIMIZER_TEMPERATURE")
    
    # Opik Configuration
    OPIK_API_KEY: str = Field(..., env="OPIK_API_KEY")
    OPIK_PROJECT_NAME: str = Field(default="orbit-production", env="OPIK_PROJECT_NAME")
    OPIK_WORKSPACE: str = Field(default="orbit", env="OPIK_WORKSPACE")
    
    # n8n Configuration
    N8N_API_URL: str = Field(..., env="N8N_API_URL")
    N8N_API_KEY: str = Field(..., env="N8N_API_KEY")
    
    # External Integrations
    GOOGLE_CALENDAR_CREDENTIALS: Optional[str] = Field(None, env="GOOGLE_CALENDAR_CREDENTIALS")
    STRIPE_SECRET_KEY: Optional[str] = Field(None, env="STRIPE_SECRET_KEY")
    TWILIO_ACCOUNT_SID: Optional[str] = Field(None, env="TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN: Optional[str] = Field(None, env="TWILIO_AUTH_TOKEN")
    
    # Performance Settings
    MAX_CONCURRENT_REQUESTS: int = Field(default=100, env="MAX_CONCURRENT_REQUESTS")
    REQUEST_TIMEOUT: int = Field(default=30, env="REQUEST_TIMEOUT")
    RATE_LIMIT_PER_MINUTE: int = Field(default=60, env="RATE_LIMIT_PER_MINUTE")
    
    # Behavioral Science Parameters
    INTERVENTION_COOLDOWN_MINUTES: int = Field(default=30, env="INTERVENTION_COOLDOWN_MINUTES")
    FAILURE_PREDICTION_THRESHOLD: float = Field(default=0.7, env="FAILURE_PREDICTION_THRESHOLD")
    CROSS_DOMAIN_SYNC_ENABLED: bool = Field(default=True, env="CROSS_DOMAIN_SYNC_ENABLED")
    
    # Safety and Reliability
    MIN_SUPERVISOR_SAFETY_SCORE: float = Field(default=0.8, env="MIN_SUPERVISOR_SAFETY_SCORE")
    MIN_SUPERVISOR_RELEVANCE_SCORE: float = Field(default=0.6, env="MIN_SUPERVISOR_RELEVANCE_SCORE")
    ENABLE_SELF_CORRECTION: bool = Field(default=True, env="ENABLE_SELF_CORRECTION")
    
    # Monitoring and Logging
    SENTRY_DSN: Optional[str] = Field(None, env="SENTRY_DSN")
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    ENABLE_METRICS: bool = Field(default=True, env="ENABLE_METRICS")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Global settings instance
settings = get_settings()


# Model configurations for different use cases
MODEL_CONFIGS = {
    "worker": {
        "model": settings.WORKER_MODEL,
        "temperature": settings.WORKER_TEMPERATURE,
        "max_tokens": settings.WORKER_MAX_TOKENS,
        "system_prompt": """You are ORBIT's Worker Agent, the world's most effective AI life coach.

Your role: Generate personalized, actionable interventions that help users achieve their goals.

Core principles:
1. Behavioral science-first: Every suggestion must be grounded in proven psychology
2. Context-aware: Consider user's current state, energy, schedule, and patterns
3. Actionable: Provide specific, measurable next steps
4. Empathetic: Understand human struggles and motivation
5. Adaptive: Adjust based on user feedback and success patterns

You have access to:
- User's goal history and progress
- Current calendar and schedule
- Recent behavioral patterns
- Cross-domain goal interactions
- Behavioral science knowledge base

Always explain your reasoning and provide alternatives when possible."""
    },
    
    "supervisor": {
        "model": settings.SUPERVISOR_MODEL,
        "temperature": settings.SUPERVISOR_TEMPERATURE,
        "max_tokens": 1024,
        "system_prompt": """You are ORBIT's Supervisor Agent, responsible for evaluating AI-generated interventions.

Your role: Ensure every intervention is safe, relevant, accurate, and likely to succeed.

Evaluation dimensions (score 0.0-1.0):

1. SAFETY SCORE: Risk assessment
   - Physical safety (no over-exertion, unsafe advice)
   - Financial safety (no overspending, risky investments)
   - Mental health (no excessive pressure, unrealistic expectations)

2. RELEVANCE SCORE: Context alignment
   - Goal alignment with user's stated objectives
   - Current life context (calendar, mood, energy)
   - Timing appropriateness

3. ACCURACY SCORE: Truthfulness and factual correctness
   - No hallucinations or false claims
   - Fact verification against knowledge base
   - Source credibility

4. SUCCESS PROBABILITY: Likelihood of user compliance
   - Historical compliance rate for similar interventions
   - Behavioral science alignment
   - Personalization quality

5. ENGAGEMENT QUALITY: User experience
   - Appropriate tone and messaging
   - Cognitive load management
   - Motivational impact

Return structured evaluation with scores and reasoning."""
    },
    
    "optimizer": {
        "model": settings.OPTIMIZER_MODEL,
        "temperature": settings.OPTIMIZER_TEMPERATURE,
        "max_tokens": 2048,
        "system_prompt": """You are ORBIT's Optimizer Agent, responsible for continuous system improvement.

Your role: Analyze performance data and optimize the entire ORBIT system.

Key functions:
1. Pattern Analysis: Identify what works and what doesn't from Opik traces
2. A/B Test Design: Create experiments to improve intervention effectiveness
3. Prompt Optimization: Refine Worker and Supervisor agent prompts
4. Strategy Adaptation: Adjust behavioral science approaches based on data
5. Failure Prevention: Identify early warning signs and prevention strategies

You analyze:
- Weekly Opik trace data
- User success/failure patterns
- Intervention effectiveness metrics
- Cross-domain optimization opportunities
- Behavioral science research updates

Output actionable improvements with clear success metrics."""
    }
}


# Behavioral science constants
BEHAVIORAL_CONSTANTS = {
    "habit_formation_days": 66,  # Average days to form a habit
    "decision_fatigue_threshold": 35,  # Max decisions per day before fatigue
    "optimal_goal_count": 3,  # Maximum goals to focus on simultaneously
    "intervention_spacing_hours": 4,  # Minimum hours between interventions
    "streak_motivation_threshold": 7,  # Days when streak becomes motivating
    "failure_recovery_window_hours": 48,  # Window to recover from setbacks
}


# Domain-specific configurations
DOMAIN_CONFIGS = {
    "health": {
        "max_workout_intensity_increase": 0.1,  # 10% max increase per week
        "rest_day_minimum": 1,  # Minimum rest days per week
        "sleep_target_hours": 8,
        "hydration_reminders_per_day": 6,
    },
    "finance": {
        "emergency_fund_months": 6,
        "max_discretionary_spending_pct": 0.3,  # 30% of income
        "investment_risk_tolerance": "moderate",
        "bill_reminder_days_ahead": 3,
    },
    "productivity": {
        "deep_work_block_minutes": 90,
        "break_interval_minutes": 25,  # Pomodoro technique
        "max_meetings_per_day": 6,
        "focus_time_protection_hours": 2,  # Daily protected focus time
    },
    "learning": {
        "spaced_repetition_intervals": [1, 3, 7, 14, 30],  # Days
        "max_learning_minutes_per_day": 120,
        "skill_practice_minimum_minutes": 15,
        "knowledge_retention_target": 0.8,  # 80% retention rate
    },
    "social": {
        "relationship_maintenance_frequency_days": 14,
        "social_energy_recovery_hours": 24,
        "networking_events_per_month": 2,
        "gratitude_practice_frequency_days": 3,
    }
}