"""
ORBIT Supervisor Agent - AI Safety and Quality Guardian
World-class intervention evaluation with 5-dimensional scoring
"""

import json
import asyncio
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

from langchain.schema import HumanMessage, SystemMessage
import structlog

from .base_agent import BaseAgent, AgentResponse, AgentContext
from ..core.config import settings


logger = structlog.get_logger(__name__)


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class EvaluationScore:
    """Individual evaluation dimension score"""
    dimension: str
    score: float  # 0.0 to 1.0
    reasoning: str
    risk_factors: List[str]
    confidence: float


@dataclass
class SupervisorEvaluation:
    """Complete supervisor evaluation of an intervention"""
    safety_score: EvaluationScore
    relevance_score: EvaluationScore
    accuracy_score: EvaluationScore
    success_probability: EvaluationScore
    engagement_quality: EvaluationScore
    
    overall_score: float
    risk_level: RiskLevel
    approved: bool
    recommendations: List[str]
    required_modifications: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "safety_score": {
                "score": self.safety_score.score,
                "reasoning": self.safety_score.reasoning,
                "risk_factors": self.safety_score.risk_factors,
                "confidence": self.safety_score.confidence
            },
            "relevance_score": {
                "score": self.relevance_score.score,
                "reasoning": self.relevance_score.reasoning,
                "risk_factors": self.relevance_score.risk_factors,
                "confidence": self.relevance_score.confidence
            },
            "accuracy_score": {
                "score": self.accuracy_score.score,
                "reasoning": self.accuracy_score.reasoning,
                "risk_factors": self.accuracy_score.risk_factors,
                "confidence": self.accuracy_score.confidence
            },
            "success_probability": {
                "score": self.success_probability.score,
                "reasoning": self.success_probability.reasoning,
                "risk_factors": self.success_probability.risk_factors,
                "confidence": self.success_probability.confidence
            },
            "engagement_quality": {
                "score": self.engagement_quality.score,
                "reasoning": self.engagement_quality.reasoning,
                "risk_factors": self.engagement_quality.risk_factors,
                "confidence": self.engagement_quality.confidence
            },
            "overall_score": self.overall_score,
            "risk_level": self.risk_level.value,
            "approved": self.approved,
            "recommendations": self.recommendations,
            "required_modifications": self.required_modifications
        }


class SupervisorAgent(BaseAgent):
    """
    The Supervisor Agent is ORBIT's AI safety and quality guardian responsible for:
    1. Real-time intervention evaluation across 5 dimensions
    2. Risk assessment and safety checks
    3. Quality control and accuracy verification
    4. Success probability prediction
    5. User experience optimization
    """
    
    def __init__(self, **kwargs):
        super().__init__(agent_type="supervisor", **kwargs)
        
        # Evaluation thresholds
        self.safety_threshold = settings.MIN_SUPERVISOR_SAFETY_SCORE
        self.relevance_thresh
                