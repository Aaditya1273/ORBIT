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
        # Use the supervisor model configuration from settings
        supervisor_config = MODEL_CONFIGS.get("supervisor", {
            "model": "anthropic/claude-3-sonnet-20240229",
            "provider": "openrouter",
            "temperature": 0.3,
            "max_tokens": 4096,
            "system_prompt": ""
        })
        
        super().__init__(agent_type="supervisor", model_config=supervisor_config, **kwargs)
        
        # Evaluation thresholds
        self.safety_threshold = getattr(settings, 'MIN_SUPERVISOR_SAFETY_SCORE', 0.8)
        self.relevance_threshold = getattr(settings, 'MIN_SUPERVISOR_RELEVANCE_SCORE', 0.7)
        self.accuracy_threshold = 0.8
        self.success_threshold = 0.6
        self.engagement_threshold = 0.7
        self.overall_threshold = 0.7
        
        # Risk assessment components
        self.safety_checker = SafetyChecker()
        self.fact_checker = FactChecker()
        self.relevance_analyzer = RelevanceAnalyzer()
        
        logger.info("Supervisor Agent initialized with evaluation thresholds")
    
    async def _execute_internal(
        self,
        context: AgentContext,
        user_input: str,
        intervention_to_evaluate: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> AgentResponse:
        """
        Evaluate an intervention across all dimensions
        """
        try:
            if not intervention_to_evaluate:
                # Parse intervention from user_input if not provided directly
                intervention_to_evaluate = self._parse_intervention_from_input(user_input)
            
            # Perform comprehensive evaluation
            evaluation = await self._evaluate_intervention(intervention_to_evaluate, context)
            
            # Log evaluation to Opik
            await self._log_evaluation_to_opik(intervention_to_evaluate, evaluation, context)
            
            # Generate response
            response_content = self._format_evaluation_response(evaluation)
            
            return AgentResponse(
                content=response_content,
                reasoning=f"Completed 5-dimensional evaluation with overall score {evaluation.overall_score:.2f}",
                confidence=min([
                    evaluation.safety_score.confidence,
                    evaluation.relevance_score.confidence,
                    evaluation.accuracy_score.confidence,
                    evaluation.success_probability.confidence,
                    evaluation.engagement_quality.confidence
                ]),
                metadata={
                    "evaluation": evaluation.to_dict(),
                    "approved": evaluation.approved,
                    "risk_level": evaluation.risk_level.value
                }
            )
            
        except Exception as e:
            logger.error(
                "Supervisor evaluation failed",
                error=str(e),
                user_id=context.user_id,
                exc_info=True
            )
            
            # Return conservative evaluation on error
            return AgentResponse(
                content="Evaluation failed - intervention rejected for safety",
                reasoning=f"Error during evaluation: {str(e)}",
                confidence=0.0,
                metadata={
                    "error": True,
                    "approved": False,
                    "risk_level": "critical"
                }
            )
    
    async def _evaluate_intervention(
        self,
        intervention: Dict[str, Any],
        context: AgentContext
    ) -> SupervisorEvaluation:
        """
        Perform comprehensive 5-dimensional evaluation
        """
        # Run all evaluations in parallel for efficiency
        evaluation_tasks = [
            self._evaluate_safety(intervention, context),
            self._evaluate_relevance(intervention, context),
            self._evaluate_accuracy(intervention, context),
            self._evaluate_success_probability(intervention, context),
            self._evaluate_engagement_quality(intervention, context)
        ]
        
        results = await asyncio.gather(*evaluation_tasks)
        
        safety_score, relevance_score, accuracy_score, success_probability, engagement_quality = results
        
        # Calculate overall score (weighted average)
        overall_score = self._calculate_overall_score([
            (safety_score.score, 0.25),      # Safety is critical
            (relevance_score.score, 0.20),   # Relevance is important
            (accuracy_score.score, 0.20),    # Accuracy matters
            (success_probability.score, 0.20), # Success prediction
            (engagement_quality.score, 0.15)  # User experience
        ])
        
        # Determine risk level and approval
        risk_level = self._determine_risk_level(safety_score.score, overall_score)
        approved = self._determine_approval(safety_score.score, overall_score, risk_level)
        
        # Generate recommendations
        recommendations = self._generate_recommendations([
            safety_score, relevance_score, accuracy_score, success_probability, engagement_quality
        ])
        
        # Generate required modifications if not approved
        required_modifications = []
        if not approved:
            required_modifications = self._generate_required_modifications([
                safety_score, relevance_score, accuracy_score, success_probability, engagement_quality
            ])
        
        return SupervisorEvaluation(
            safety_score=safety_score,
            relevance_score=relevance_score,
            accuracy_score=accuracy_score,
            success_probability=success_probability,
            engagement_quality=engagement_quality,
            overall_score=overall_score,
            risk_level=risk_level,
            approved=approved,
            recommendations=recommendations,
            required_modifications=required_modifications
        )
    
    async def _evaluate_safety(
        self,
        intervention: Dict[str, Any],
        context: AgentContext
    ) -> EvaluationScore:
        """
        Evaluate intervention safety across multiple dimensions
        """
        content = intervention.get('content', '')
        domain = intervention.get('domain', 'general')
        
        # Build safety evaluation prompt
        safety_prompt = f"""
        Evaluate the safety of this intervention on a scale of 0.0 to 1.0:
        
        INTERVENTION:
        Domain: {domain}
        Content: {content}
        
        USER CONTEXT:
        {self._build_context_prompt(context)}
        
        SAFETY CRITERIA:
        1. Physical Safety: Could this cause physical harm?
        2. Mental Health: Could this negatively impact mental wellbeing?
        3. Financial Safety: Could this cause financial harm?
        4. Privacy: Does this respect user privacy?
        5. Ethical Considerations: Is this ethically appropriate?
        
        Provide your evaluation as JSON:
        {{
            "safety_score": 0.0-1.0,
            "reasoning": "detailed explanation",
            "risk_factors": ["list", "of", "identified", "risks"],
            "confidence": 0.0-1.0
        }}
        """
        
        # Call LLM for safety evaluation
        messages = [
            SystemMessage(content="You are a safety evaluation expert. Be thorough and conservative in your assessment."),
            HumanMessage(content=safety_prompt)
        ]
        
        response = await self._call_llm(messages)
        
        try:
            safety_data = json.loads(response["content"])
            
            # Additional automated safety checks
            automated_checks = await self.safety_checker.run_automated_checks(content, domain)
            
            # Combine LLM evaluation with automated checks
            final_score = min(safety_data["safety_score"], automated_checks["safety_score"])
            
            return EvaluationScore(
                dimension="safety",
                score=final_score,
                reasoning=safety_data["reasoning"],
                risk_factors=safety_data.get("risk_factors", []) + automated_checks.get("risk_factors", []),
                confidence=min(safety_data["confidence"], automated_checks["confidence"])
            )
            
        except (json.JSONDecodeError, KeyError) as e:
            logger.warning(f"Failed to parse safety evaluation: {e}")
            # Conservative fallback
            return EvaluationScore(
                dimension="safety",
                score=0.5,
                reasoning="Failed to parse safety evaluation - using conservative score",
                risk_factors=["evaluation_parsing_failed"],
                confidence=0.3
            )
    
    async def _evaluate_relevance(
        self,
        intervention: Dict[str, Any],
        context: AgentContext
    ) -> EvaluationScore:
        """
        Evaluate how relevant the intervention is to the user's current situation
        """
        content = intervention.get('content', '')
        domain = intervention.get('domain', 'general')
        
        relevance_prompt = f"""
        Evaluate how relevant this intervention is to the user's current situation:
        
        INTERVENTION:
        Domain: {domain}
        Content: {content}
        
        USER CONTEXT:
        {self._build_context_prompt(context)}
        
        RELEVANCE CRITERIA:
        1. Goal Alignment: How well does this align with user's goals?
        2. Timing: Is this appropriately timed?
        3. Context Awareness: Does this consider user's current situation?
        4. Personalization: Is this personalized to the user?
        5. Priority: Is this addressing the right priority level?
        
        Provide evaluation as JSON:
        {{
            "relevance_score": 0.0-1.0,
            "reasoning": "detailed explanation",
            "alignment_factors": ["factors", "supporting", "relevance"],
            "misalignment_factors": ["factors", "reducing", "relevance"],
            "confidence": 0.0-1.0
        }}
        """
        
        messages = [
            SystemMessage(content="You are a relevance evaluation expert. Consider context, timing, and personalization."),
            HumanMessage(content=relevance_prompt)
        ]
        
        response = await self._call_llm(messages)
        
        try:
            relevance_data = json.loads(response["content"])
            
            # Additional relevance checks
            context_relevance = await self.relevance_analyzer.analyze_context_relevance(
                intervention, context
            )
            
            # Combine scores
            final_score = (relevance_data["relevance_score"] + context_relevance["score"]) / 2
            
            return EvaluationScore(
                dimension="relevance",
                score=final_score,
                reasoning=relevance_data["reasoning"],
                risk_factors=relevance_data.get("misalignment_factors", []),
                confidence=relevance_data["confidence"]
            )
            
        except (json.JSONDecodeError, KeyError) as e:
            logger.warning(f"Failed to parse relevance evaluation: {e}")
            return EvaluationScore(
                dimension="relevance",
                score=0.5,
                reasoning="Failed to parse relevance evaluation",
                risk_factors=["evaluation_parsing_failed"],
                confidence=0.3
            )
    
    async def _evaluate_accuracy(
        self,
        intervention: Dict[str, Any],
        context: AgentContext
    ) -> EvaluationScore:
        """
        Evaluate the factual accuracy and truthfulness of the intervention
        """
        content = intervention.get('content', '')
        
        # Check for factual claims that can be verified
        fact_check_results = await self.fact_checker.check_claims(content)
        
        accuracy_prompt = f"""
        Evaluate the accuracy and truthfulness of this intervention:
        
        INTERVENTION CONTENT:
        {content}
        
        FACT CHECK RESULTS:
        {json.dumps(fact_check_results, indent=2)}
        
        ACCURACY CRITERIA:
        1. Factual Correctness: Are any factual claims accurate?
        2. No Hallucinations: Is the information made up or speculative?
        3. Source Reliability: Are any referenced sources credible?
        4. Consistency: Is the information internally consistent?
        5. Currency: Is the information up-to-date?
        
        Provide evaluation as JSON:
        {{
            "accuracy_score": 0.0-1.0,
            "reasoning": "detailed explanation",
            "verified_claims": ["list", "of", "verified", "claims"],
            "questionable_claims": ["list", "of", "questionable", "claims"],
            "confidence": 0.0-1.0
        }}
        """
        
        messages = [
            SystemMessage(content="You are a fact-checking expert. Be rigorous about accuracy and truthfulness."),
            HumanMessage(content=accuracy_prompt)
        ]
        
        response = await self._call_llm(messages)
        
        try:
            accuracy_data = json.loads(response["content"])
            
            # Combine LLM evaluation with automated fact checking
            automated_score = fact_check_results.get("overall_accuracy", 0.8)
            final_score = (accuracy_data["accuracy_score"] + automated_score) / 2
            
            return EvaluationScore(
                dimension="accuracy",
                score=final_score,
                reasoning=accuracy_data["reasoning"],
                risk_factors=accuracy_data.get("questionable_claims", []),
                confidence=accuracy_data["confidence"]
            )
            
        except (json.JSONDecodeError, KeyError) as e:
            logger.warning(f"Failed to parse accuracy evaluation: {e}")
            return EvaluationScore(
                dimension="accuracy",
                score=0.7,  # Neutral score
                reasoning="Failed to parse accuracy evaluation",
                risk_factors=["evaluation_parsing_failed"],
                confidence=0.3
            )
    
    async def _evaluate_success_probability(
        self,
        intervention: Dict[str, Any],
        context: AgentContext
    ) -> EvaluationScore:
        """
        Predict the probability that the user will successfully follow through
        """
        content = intervention.get('content', '')
        domain = intervention.get('domain', 'general')
        
        success_prompt = f"""
        Predict the probability that the user will successfully follow this intervention:
        
        INTERVENTION:
        Domain: {domain}
        Content: {content}
        
        USER CONTEXT:
        {self._build_context_prompt(context)}
        
        SUCCESS FACTORS TO CONSIDER:
        1. Behavioral Science: Does this use proven behavior change techniques?
        2. User History: How has the user responded to similar interventions?
        3. Difficulty Level: Is this appropriately challenging but achievable?
        4. Motivation Alignment: Does this align with user's intrinsic motivation?
        5. Environmental Factors: Are there barriers or enablers in the environment?
        
        Provide evaluation as JSON:
        {{
            "success_probability": 0.0-1.0,
            "reasoning": "detailed explanation",
            "success_factors": ["factors", "supporting", "success"],
            "barrier_factors": ["factors", "hindering", "success"],
            "confidence": 0.0-1.0
        }}
        """
        
        messages = [
            SystemMessage(content="You are a behavioral prediction expert. Consider psychology and past patterns."),
            HumanMessage(content=success_prompt)
        ]
        
        response = await self._call_llm(messages)
        
        try:
            success_data = json.loads(response["content"])
            
            return EvaluationScore(
                dimension="success_probability",
                score=success_data["success_probability"],
                reasoning=success_data["reasoning"],
                risk_factors=success_data.get("barrier_factors", []),
                confidence=success_data["confidence"]
            )
            
        except (json.JSONDecodeError, KeyError) as e:
            logger.warning(f"Failed to parse success probability evaluation: {e}")
            return EvaluationScore(
                dimension="success_probability",
                score=0.6,  # Neutral probability
                reasoning="Failed to parse success probability evaluation",
                risk_factors=["evaluation_parsing_failed"],
                confidence=0.3
            )
    
    async def _evaluate_engagement_quality(
        self,
        intervention: Dict[str, Any],
        context: AgentContext
    ) -> EvaluationScore:
        """
        Evaluate the quality of user engagement and experience
        """
        content = intervention.get('content', '')
        
        engagement_prompt = f"""
        Evaluate the engagement quality and user experience of this intervention:
        
        INTERVENTION CONTENT:
        {content}
        
        USER CONTEXT:
        {self._build_context_prompt(context)}
        
        ENGAGEMENT CRITERIA:
        1. Tone Appropriateness: Is the tone suitable for the user and situation?
        2. Clarity: Is the message clear and easy to understand?
        3. Motivation: Is this motivating and inspiring?
        4. Cognitive Load: Is this easy to process mentally?
        5. Emotional Impact: Will this create positive emotional response?
        
        Provide evaluation as JSON:
        {{
            "engagement_score": 0.0-1.0,
            "reasoning": "detailed explanation",
            "positive_factors": ["factors", "enhancing", "engagement"],
            "negative_factors": ["factors", "reducing", "engagement"],
            "confidence": 0.0-1.0
        }}
        """
        
        messages = [
            SystemMessage(content="You are a user experience expert. Focus on engagement and emotional impact."),
            HumanMessage(content=engagement_prompt)
        ]
        
        response = await self._call_llm(messages)
        
        try:
            engagement_data = json.loads(response["content"])
            
            return EvaluationScore(
                dimension="engagement_quality",
                score=engagement_data["engagement_score"],
                reasoning=engagement_data["reasoning"],
                risk_factors=engagement_data.get("negative_factors", []),
                confidence=engagement_data["confidence"]
            )
            
        except (json.JSONDecodeError, KeyError) as e:
            logger.warning(f"Failed to parse engagement evaluation: {e}")
            return EvaluationScore(
                dimension="engagement_quality",
                score=0.6,  # Neutral score
                reasoning="Failed to parse engagement evaluation",
                risk_factors=["evaluation_parsing_failed"],
                confidence=0.3
            )
    
    def _calculate_overall_score(self, weighted_scores: List[Tuple[float, float]]) -> float:
        """
        Calculate weighted overall score
        """
        total_weighted = sum(score * weight for score, weight in weighted_scores)
        total_weight = sum(weight for _, weight in weighted_scores)
        return total_weighted / total_weight if total_weight > 0 else 0.0
    
    def _determine_risk_level(self, safety_score: float, overall_score: float) -> RiskLevel:
        """
        Determine risk level based on scores
        """
        if safety_score < 0.6 or overall_score < 0.4:
            return RiskLevel.CRITICAL
        elif safety_score < 0.8 or overall_score < 0.6:
            return RiskLevel.HIGH
        elif safety_score < 0.9 or overall_score < 0.8:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
    
    def _determine_approval(
        self,
        safety_score: float,
        overall_score: float,
        risk_level: RiskLevel
    ) -> bool:
        """
        Determine if intervention should be approved
        """
        # Safety is non-negotiable
        if safety_score < self.safety_threshold:
            return False
        
        # Overall quality threshold
        if overall_score < self.overall_threshold:
            return False
        
        # Critical risk interventions are never approved
        if risk_level == RiskLevel.CRITICAL:
            return False
        
        return True
    
    def _generate_recommendations(self, scores: List[EvaluationScore]) -> List[str]:
        """
        Generate recommendations based on evaluation scores
        """
        recommendations = []
        
        for score in scores:
            if score.score < 0.8:  # Room for improvement
                if score.dimension == "safety":
                    recommendations.append(f"Improve safety by addressing: {', '.join(score.risk_factors[:2])}")
                elif score.dimension == "relevance":
                    recommendations.append("Enhance personalization and context awareness")
                elif score.dimension == "accuracy":
                    recommendations.append("Verify factual claims and add credible sources")
                elif score.dimension == "success_probability":
                    recommendations.append("Apply stronger behavioral science techniques")
                elif score.dimension == "engagement_quality":
                    recommendations.append("Improve tone and emotional appeal")
        
        return recommendations[:5]  # Limit to top 5
    
    def _generate_required_modifications(self, scores: List[EvaluationScore]) -> List[str]:
        """
        Generate required modifications for rejected interventions
        """
        modifications = []
        
        for score in scores:
            if score.score < 0.6:  # Requires modification
                if score.dimension == "safety":
                    modifications.append("CRITICAL: Remove all safety risks before resubmission")
                elif score.dimension == "relevance":
                    modifications.append("REQUIRED: Improve alignment with user goals and context")
                elif score.dimension == "accuracy":
                    modifications.append("REQUIRED: Verify and correct all factual claims")
        
        return modifications
    
    def _parse_intervention_from_input(self, user_input: str) -> Dict[str, Any]:
        """
        Parse intervention data from user input
        """
        try:
            # Try to parse as JSON first
            return json.loads(user_input)
        except json.JSONDecodeError:
            # Fallback: treat as plain text intervention
            return {
                "content": user_input,
                "domain": "general",
                "type": "general"
            }
    
    def _format_evaluation_response(self, evaluation: SupervisorEvaluation) -> str:
        """
        Format evaluation results into readable response
        """
        status_emoji = "✅" if evaluation.approved else "❌"
        risk_emoji = {
            RiskLevel.LOW: "🟢",
            RiskLevel.MEDIUM: "🟡", 
            RiskLevel.HIGH: "🟠",
            RiskLevel.CRITICAL: "🔴"
        }
        
        response_parts = [
            f"{status_emoji} SUPERVISOR EVALUATION COMPLETE",
            f"Overall Score: {evaluation.overall_score:.2f}/1.0",
            f"Risk Level: {risk_emoji[evaluation.risk_level]} {evaluation.risk_level.value.upper()}",
            f"Status: {'APPROVED' if evaluation.approved else 'REJECTED'}",
            "",
            "📊 DIMENSION SCORES:",
            f"🛡️  Safety: {evaluation.safety_score.score:.2f}",
            f"🎯 Relevance: {evaluation.relevance_score.score:.2f}",
            f"✅ Accuracy: {evaluation.accuracy_score.score:.2f}",
            f"📈 Success Probability: {evaluation.success_probability.score:.2f}",
            f"💫 Engagement Quality: {evaluation.engagement_quality.score:.2f}",
        ]
        
        if evaluation.recommendations:
            response_parts.extend([
                "",
                "💡 RECOMMENDATIONS:",
                *[f"• {rec}" for rec in evaluation.recommendations[:3]]
            ])
        
        if evaluation.required_modifications:
            response_parts.extend([
                "",
                "⚠️  REQUIRED MODIFICATIONS:",
                *[f"• {mod}" for mod in evaluation.required_modifications]
            ])
        
        return "\n".join(response_parts)
    
    async def _log_evaluation_to_opik(
        self,
        intervention: Dict[str, Any],
        evaluation: SupervisorEvaluation,
        context: AgentContext
    ):
        """
        Log evaluation results to Opik for analysis
        """
        try:
            if self.enable_opik:
                opik_context.update_current_trace(
                    name="supervisor_evaluation",
                    input={
                        "intervention": intervention,
                        "context": context.user_id
                    },
                    output=evaluation.to_dict(),
                    metadata={
                        "approved": evaluation.approved,
                        "risk_level": evaluation.risk_level.value,
                        "overall_score": evaluation.overall_score
                    }
                )
        except Exception as e:
            logger.warning(f"Failed to log evaluation to Opik: {e}")


# Helper classes for specialized evaluation tasks

class SafetyChecker:
    """Automated safety checking utilities"""
    
    async def run_automated_checks(self, content: str, domain: str) -> Dict[str, Any]:
        """Run automated safety checks"""
        risk_factors = []
        safety_score = 1.0
        
        # Check for harmful keywords
        harmful_keywords = [
            "dangerous", "risky", "unsafe", "harmful", "illegal",
            "overdose", "extreme", "radical", "aggressive"
        ]
        
        content_lower = content.lower()
        for keyword in harmful_keywords:
            if keyword in content_lower:
                risk_factors.append(f"contains_keyword_{keyword}")
                safety_score -= 0.1
        
        # Domain-specific checks
        if domain == "health":
            health_risks = ["medication", "supplement", "diet", "exercise"]
            for risk in health_risks:
                if risk in content_lower and "consult" not in content_lower:
                    risk_factors.append(f"health_advice_without_disclaimer")
                    safety_score -= 0.2
        
        return {
            "safety_score": max(0.0, safety_score),
            "risk_factors": risk_factors,
            "confidence": 0.8
        }


class FactChecker:
    """Automated fact checking utilities"""
    
    async def check_claims(self, content: str) -> Dict[str, Any]:
        """Check factual claims in content"""
        # This would integrate with fact-checking APIs
        # For now, return mock results
        return {
            "overall_accuracy": 0.9,
            "verified_claims": [],
            "questionable_claims": [],
            "confidence": 0.7
        }


class RelevanceAnalyzer:
    """Analyze relevance to user context"""
    
    async def analyze_context_relevance(
        self,
        intervention: Dict[str, Any],
        context: AgentContext
    ) -> Dict[str, Any]:
        """Analyze how well intervention matches user context"""
        relevance_score = 0.8  # Base score
        
        # Check goal alignment
        intervention_domain = intervention.get('domain', '')
        user_domains = [goal.get('domain', '') for goal in context.current_goals]
        
        if intervention_domain in user_domains:
            relevance_score += 0.1
        
        return {
            "score": min(1.0, relevance_score),
            "confidence": 0.7
        }
                