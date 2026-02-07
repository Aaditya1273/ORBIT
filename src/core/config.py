"""
ORBIT Configuration Management
Centralized configuration using Pydantic Settings
"""

import os
from typing import List, Optional, Any, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Application
    APP_NAME: str = "ORBIT"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    SECRET_KEY: str = "orbit-dev-secret-key"
    ALLOWED_HOSTS: Union[List[str], str] = ["localhost", "127.0.0.1", "0.0.0.0"]
    
    # Database
    DATABASE_URL: str = "sqlite:///./orbit_dev.db"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_PASSWORD: Optional[str] = None
    
    # AI Models
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: str = "test-key"  # Gemini API key
    OPEN_ROUTER_API_KEY: str = "test-key"  # OpenRouter for cost-effective model access
    
    # Evaluation & Monitoring
    OPIK_API_KEY: str = "test-key"
    OPIK_PROJECT_NAME: str = "orbit-production"
    OPIK_WORKSPACE: str = "orbit-workspace"
    LANGFUSE_SECRET_KEY: Optional[str] = None
    LANGFUSE_PUBLIC_KEY: Optional[str] = None
    WANDB_API_KEY: Optional[str] = None
    
    # External Services
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    STRIPE_API_KEY: Optional[str] = None
    STRIPE_WEBHOOK_SECRET: Optional[str] = None
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    
    # n8n Integration
    N8N_API_URL: str = "http://localhost:5678"
    N8N_API_KEY: Optional[str] = None
    
    # Security
    JWT_SECRET_KEY: str = "orbit-jwt-secret-dev"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ENCRYPTION_KEY: str = "orbit-encryption-key-dev"  # For encrypting sensitive user data
    
    # Monitoring
    SENTRY_DSN: Optional[str] = None
    PROMETHEUS_PORT: int = 9090
    LOG_LEVEL: str = "INFO"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_BURST: int = 100
    
    # AI Configuration
    DEFAULT_WORKER_MODEL: str = "gemini-1.5-pro"
    DEFAULT_SUPERVISOR_MODEL: str = "claude-3-sonnet-20240229"
    MAX_TOKENS_PER_REQUEST: int = 4000
    AI_TIMEOUT_SECONDS: int = 30
    
    # Intervention Settings
    MIN_INTERVENTION_INTERVAL_HOURS: int = 2
    MAX_DAILY_INTERVENTIONS: int = 10
    INTERVENTION_QUALITY_THRESHOLD: float = 0.7
    
    # User Limits
    MAX_GOALS_PER_USER: int = 20
    MAX_INTEGRATIONS_PER_USER: int = 50
    DATA_RETENTION_DAYS: int = 365
    
    # Email Configuration
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    FROM_EMAIL: str = "noreply@orbit.ai"
    FROM_NAME: str = "ORBIT AI Platform"
    FRONTEND_URL: str = "http://localhost:3000"
    
    @field_validator("ALLOWED_HOSTS", mode="before")
    @classmethod
    def parse_allowed_hosts(cls, v):
        if not v:
            return ["localhost", "127.0.0.1", "0.0.0.0"]
        if isinstance(v, str):
            # Handle standard CSV or bracketed list strings
            v = v.strip()
            if v.startswith("[") and v.endswith("]"):
                v = v[1:-1]
            return [host.strip() for host in v.split(",") if host.strip()]
        if isinstance(v, list):
            return v
        return ["localhost", "127.0.0.1", "0.0.0.0"]
    
    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, v):
        if v not in ["development", "staging", "production"]:
            raise ValueError("ENVIRONMENT must be development, staging, or production")
        return v
    
    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v):
        if v not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            raise ValueError("LOG_LEVEL must be a valid logging level")
        return v
    
    model_config = SettingsConfigDict(
        env_file=(".env", ".env.local"),
        env_file_encoding='utf-8',
        case_sensitive=True,
        extra='ignore'
    )

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()

# Global settings instance
settings = get_settings()

# Model configurations
MODEL_CONFIGS = {
    "worker": {
        "model": "gemini-2.5-flash",  # Using Gemini 2.5 Flash (working model)
        "provider": "google",
        "max_tokens": 8192,
        "temperature": 0.7,
        "top_p": 0.9,
        "system_prompt": ""
    },
    "supervisor": {
        "model": "anthropic/claude-3-haiku",  # Using Claude Haiku via OpenRouter (working model)
        "provider": "openrouter",
        "max_tokens": 4096,
        "temperature": 0.3,
        "top_p": 0.9,
        "system_prompt": ""
    },
    "optimizer": {
        "model": "openai/gpt-3.5-turbo",  # Using GPT-3.5 via OpenRouter (working model)
        "provider": "openrouter",
        "max_tokens": 4096,
        "temperature": 0.5,
        "top_p": 0.9,
        "system_prompt": ""
    },
    "fallback": {
        "model": "meta-llama/llama-3-8b-instruct",  # Working free model
        "provider": "openrouter",
        "max_tokens": 2048,
        "temperature": 0.7,
        "top_p": 0.9,
        "system_prompt": ""
    }
}

# Evaluation thresholds
EVALUATION_THRESHOLDS = {
    "safety_score": 0.8,
    "relevance_score": 0.7,
    "accuracy_score": 0.8,
    "adherence_probability": 0.6,
    "engagement_quality": 0.7,
    "overall_score": 0.7
}

# Domain configurations
DOMAIN_CONFIGS = {
    "health": {
        "color": "#4CAF50",
        "icon": "💪",
        "default_metrics": ["steps", "calories", "sleep_hours", "workouts"],
        "intervention_types": ["workout_reminder", "nutrition_nudge", "sleep_optimization"]
    },
    "finance": {
        "color": "#2196F3",
        "icon": "💰",
        "default_metrics": ["spending", "savings", "budget_adherence", "investment_growth"],
        "intervention_types": ["spending_alert", "savings_reminder", "budget_check"]
    },
    "productivity": {
        "color": "#FF9800",
        "icon": "📈",
        "default_metrics": ["focus_time", "tasks_completed", "meetings_attended", "goals_achieved"],
        "intervention_types": ["focus_reminder", "break_suggestion", "priority_adjustment"]
    },
    "learning": {
        "color": "#9C27B0",
        "icon": "📚",
        "default_metrics": ["study_time", "courses_completed", "skills_acquired", "practice_sessions"],
        "intervention_types": ["study_reminder", "skill_practice", "learning_path_adjustment"]
    },
    "social": {
        "color": "#E91E63",
        "icon": "🤝",
        "default_metrics": ["social_interactions", "relationships_maintained", "community_engagement", "networking_events"],
        "intervention_types": ["relationship_reminder", "social_activity_suggestion", "networking_opportunity"]
    }
}