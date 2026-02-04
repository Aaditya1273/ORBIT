"""
ORBIT Worker Agent - The Primary AI Coach
World-class behavioral intervention generation with cross-domain optimization
"""

import json
import asyncio
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass

from langchain.schema import HumanMessage, SystemMessage
import structlog

from .base_agent import BaseAgent, AgentResponse, AgentContext
from ..core.config import settings, BEHAVIORAL_CONSTANTS, DOMAIN_CONFIGS
from ..behavioral_science.intervention_engine import InterventionEngine
from ..behavioral_science.pattern_analyzer import PatternAnalyzer


logger = structlog.get_logger(__name__)


@dataclass
class InterventionRequest:
    """Structured request for intervention generation"""
    trigger_type: str  # "scheduled", "reactive", "predictive"
    domain: str  # "health", "finance", "productivity", etc.
    urgency: str  # "low", "medium", "high", "critical"
    context_data: Dict[str, Any]
    user_state: Dict[str, Any]
    goal_progress: Dict[str, Any]


class WorkerAgent(BaseAgent):
    """
    The Worker Agent is ORBIT's primary AI coach responsible for:
    1. Generating personalized behavioral interventions
    2. Cross-domain goal optimization
    3. Predictive failure prevention
    4. Adaptive difficulty scaling
    5. Context-aware timing
    """
    
    def __init__(self, **kwargs):
        super().__init__(agent_type="worker", **kwargs)
        
        # Initialize behavioral science engines
        self.intervention_engine = InterventionEngine()
        self.pattern_analyzer = PatternAnalyzer()
        
        # Cache for user patterns and preferences
        self.user_patterns_cache = {}
        self.intervention_history = {}
        
        logger.info("Worker Agent initialized with behavioral science engines")
    
    async def _execute_internal(
        self,
        context: AgentContext,
        user_input: str,
        **kwargs
    ) -> AgentResponse:
        """
        Generate intelligent, personalized interventions based on context
        """
        try:
            # Parse the request type
            request = self._parse_intervention_request(user_input, context)
            
            # Analyze user patterns
            user_patterns = await self._analyze_user_patterns(context)
            
            # Generate intervention based on type
            if request.trigger_type == "scheduled":
                intervention = await self._generate_scheduled_intervention(request, user_patterns, context)
            elif request.trigger_type == "reactive":
                intervention = await self._generate_reactive_intervention(request, user_patterns, context)
            elif request.trigger_type == "predictive":
                intervention = await self._generate_predictive_intervention(request, user_patterns, context)
            else:
                intervention = await self._generate_general_intervention(request, user_patterns, context)
            
            # Apply cross-domain optimization
            if settings.CROSS_DOMAIN_SYNC_ENABLED:
                intervention = await self._apply_cross_domain_optimization(intervention, context)
            
            # Calculate confidence based on multiple factors
            confidence = self._calculate_intervention_confidence(intervention, user_patterns, context)
            
            # Store intervention for learning
            await self._store_intervention_for_learning(intervention, context)
            
            return AgentResponse(
                content=intervention["content"],
                reasoning=intervention["reasoning"],
                confidence=confidence,
                metadata={
                    "intervention_type": request.trigger_type,
                    "domain": request.domain,
                    "urgency": request.urgency,
                    "cross_domain_effects": intervention.get("cross_domain_effects", []),
                    "behavioral_techniques": intervention.get("techniques", []),
                    "expected_compliance_rate": intervention.get("expected_compliance", 0.0)
                }
            )
            
        except Exception as e:
            logger.error(f"Worker agent execution failed: {str(e)}", exc_info=True)
            raise
    
    def _parse_intervention_request(self, user_input: str, context: AgentContext) -> InterventionRequest:
        """
        Parse user input and context to determine intervention type and parameters
        """
        # Default values
        trigger_type = "general"
        domain = "productivity"  # Default domain
        urgency = "medium"
        
        # Extract domain from goals or input
        if context.current_goals:
            # Use the domain of the most recent or highest priority goal
            primary_goal = context.current_goals[0]
            domain = primary_goal.get("domain", "productivity")
        
        # Determine trigger type from context
        if "schedule" in user_input.lower() or "morning" in user_input.lower():
            trigger_type = "scheduled"
        elif "struggling" in user_input.lower() or "help" in user_input.lower():
            trigger_type = "reactive"
            urgency = "high"
        elif "predict" in user_input.lower() or "prevent" in user_input.lower():
            trigger_type = "predictive"
        
        # Extract urgency indicators
        if any(word in user_input.lower() for word in ["urgent", "critical", "emergency"]):
            urgency = "critical"
        elif any(word in user_input.lower() for word in ["struggling", "failing", "behind"]):
            urgency = "high"
        
        return InterventionRequest(
            trigger_type=trigger_type,
            domain=domain,
            urgency=urgency,
            context_data=context.external_context or {},
            user_state=context.user_state,
            goal_progress={goal.get("id"): goal.get("progress", 0) for goal in context.current_goals}
        )
    
    async def _analyze_user_patterns(self, context: AgentContext) -> Dict[str, Any]:
        """
        Analyze user behavioral patterns for personalization
        """
        user_id = context.user_id
        
        # Check cache first
        if user_id in self.user_patterns_cache:
            cached_patterns = self.user_patterns_cache[user_id]
            if (datetime.utcnow() - cached_patterns["last_updated"]).seconds < 3600:  # 1 hour cache
                return cached_patterns["patterns"]
        
        # Analyze patterns from recent history
        patterns = await self.pattern_analyzer.analyze_user_patterns(
            user_id=user_id,
            history=context.recent_history,
            goals=context.current_goals,
            user_state=context.user_state
        )
        
        # Cache the results
        self.user_patterns_cache[user_id] = {
            "patterns": patterns,
            "last_updated": datetime.utcnow()
        }
        
        return patterns
    
    async def _generate_scheduled_intervention(
        self,
        request: InterventionRequest,
        user_patterns: Dict[str, Any],
        context: AgentContext
    ) -> Dict[str, Any]:
        """
        Generate scheduled interventions (morning briefings, evening reviews, etc.)
        """
        current_time = datetime.utcnow()
        
        # Build context-aware prompt
        prompt = self._build_scheduled_intervention_prompt(request, user_patterns, context, current_time)
        
        # Call LLM with structured prompt
        messages = [
            SystemMessage(content=self.model_config["system_prompt"]),
            HumanMessage(content=prompt)
        ]
        
        llm_response = await self._call_llm(messages)
        
        # Parse and structure the response
        intervention = self._parse_llm_intervention_response(llm_response["content"])
        
        # Add behavioral science techniques
        intervention = await self.intervention_engine.enhance_with_behavioral_science(
            intervention, user_patterns, request.domain
        )
        
        return intervention
    
    async def _generate_reactive_intervention(
        self,
        request: InterventionRequest,
        user_patterns: Dict[str, Any],
        context: AgentContext
    ) -> Dict[str, Any]:
        """
        Generate reactive interventions for immediate user needs
        """
        # Build urgent, empathetic prompt
        prompt = self._build_reactive_intervention_prompt(request, user_patterns, context)
        
        messages = [
            SystemMessage(content=self.model_config["system_prompt"] + "\n\nIMPORTANT: The user needs immediate help. Be empathetic, practical, and actionable."),
            HumanMessage(content=prompt)
        ]
        
        llm_response = await self._call_llm(messages)
        intervention = self._parse_llm_intervention_response(llm_response["content"])
        
        # Apply crisis intervention techniques if needed
        if request.urgency in ["high", "critical"]:
            intervention = await self.intervention_engine.apply_crisis_intervention_techniques(
                intervention, user_patterns, context
            )
        
        return intervention
    
    async def _generate_predictive_intervention(
        self,
        request: InterventionRequest,
        user_patterns: Dict[str, Any],
        context: AgentContext
    ) -> Dict[str, Any]:
        """
        Generate predictive interventions to prevent failure before it happens
        """
        # Analyze failure risk
        failure_risk = await self.pattern_analyzer.calculate_failure_risk(
            user_patterns, context.current_goals, context.recent_history
        )
        
        if failure_risk > settings.FAILURE_PREDICTION_THRESHOLD:
            # High risk - generate preventive intervention
            prompt = self._build_predictive_intervention_prompt(
                request, user_patterns, context, failure_risk
            )
            
            messages = [
                SystemMessage(content=self.model_config["system_prompt"] + "\n\nFOCUS: Prevent goal failure through early intervention."),
                HumanMessage(content=prompt)
            ]
            
            llm_response = await self._call_llm(messages)
            intervention = self._parse_llm_intervention_response(llm_response["content"])
            
            # Apply failure prevention techniques
            intervention = await self.intervention_engine.apply_failure_prevention_techniques(
                intervention, user_patterns, failure_risk
            )
            
            return intervention
        else:
            # Low risk - generate supportive intervention
            return await self._generate_general_intervention(request, user_patterns, context)
    
    async def _generate_general_intervention(
        self,
        request: InterventionRequest,
        user_patterns: Dict[str, Any],
        context: AgentContext
    ) -> Dict[str, Any]:
        """
        Generate general-purpose interventions
        """
        prompt = self._build_general_intervention_prompt(request, user_patterns, context)
        
        messages = [
            SystemMessage(content=self.model_config["system_prompt"]),
            HumanMessage(content=prompt)
        ]
        
        llm_response = await self._call_llm(messages)
        intervention = self._parse_llm_intervention_response(llm_response["content"])
        
        # Apply standard behavioral science techniques
        intervention = await self.intervention_engine.enhance_with_behavioral_science(
            intervention, user_patterns, request.domain
        )
        
        return intervention
    
    def _build_scheduled_intervention_prompt(
        self,
        request: InterventionRequest,
        user_patterns: Dict[str, Any],
        context: AgentContext,
        current_time: datetime
    ) -> str:
        """
        Build a comprehensive prompt for scheduled interventions
        """
        time_of_day = "morning" if current_time.hour < 12 else "evening" if current_time.hour > 18 else "afternoon"
        
        prompt_parts = [
            f"Generate a {time_of_day} intervention for the user.",
            f"Current time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"Domain focus: {request.domain}",
            "",
            "USER CONTEXT:",
            self._build_context_prompt(context),
            "",
            "USER PATTERNS:",
            json.dumps(user_patterns, indent=2),
            "",
            "REQUIREMENTS:",
            f"1. Create a personalized {time_of_day} plan",
            "2. Consider user's energy patterns and schedule",
            "3. Prioritize based on goal urgency and progress",
            "4. Include specific, actionable next steps",
            "5. Apply appropriate behavioral science techniques",
            "6. Consider cross-domain goal interactions",
            "",
            "OUTPUT FORMAT:",
            "Provide a structured intervention with:",
            "- Main message/plan",
            "- Specific actions to take",
            "- Reasoning for recommendations",
            "- Expected outcomes"
        ]
        
        return "\n".join(prompt_parts)
    
    def _build_reactive_intervention_prompt(
        self,
        request: InterventionRequest,
        user_patterns: Dict[str, Any],
        context: AgentContext
    ) -> str:
        """
        Build prompt for reactive interventions
        """
        prompt_parts = [
            "The user needs immediate help and support.",
            f"Urgency level: {request.urgency}",
            f"Domain: {request.domain}",
            "",
            "USER CONTEXT:",
            self._build_context_prompt(context),
            "",
            "USER PATTERNS:",
            json.dumps(user_patterns, indent=2),
            "",
            "REQUIREMENTS:",
            "1. Be empathetic and understanding",
            "2. Provide immediate, actionable solutions",
            "3. Address the root cause, not just symptoms",
            "4. Offer alternatives if the primary solution isn't feasible",
            "5. Include emotional support and motivation",
            "6. Use proven behavioral science techniques",
            "",
            "FOCUS ON:",
            "- Immediate relief and support",
            "- Practical next steps",
            "- Building confidence and momentum",
            "- Preventing further setbacks"
        ]
        
        return "\n".join(prompt_parts)
    
    def _build_predictive_intervention_prompt(
        self,
        request: InterventionRequest,
        user_patterns: Dict[str, Any],
        context: AgentContext,
        failure_risk: float
    ) -> str:
        """
        Build prompt for predictive interventions
        """
        prompt_parts = [
            f"PREDICTIVE INTERVENTION NEEDED - Failure risk: {failure_risk:.2f}",
            f"Domain: {request.domain}",
            "",
            "SITUATION:",
            f"Analysis indicates {failure_risk*100:.1f}% chance of goal failure based on current patterns.",
            "Early intervention is needed to prevent setbacks.",
            "",
            "USER CONTEXT:",
            self._build_context_prompt(context),
            "",
            "USER PATTERNS:",
            json.dumps(user_patterns, indent=2),
            "",
            "INTERVENTION STRATEGY:",
            "1. Address the specific risk factors identified",
            "2. Adjust goals/expectations if needed",
            "3. Provide additional support and resources",
            "4. Create accountability mechanisms",
            "5. Build resilience for future challenges",
            "",
            "FOCUS ON PREVENTION:",
            "- Early warning signs mitigation",
            "- Habit modification before failure",
            "- Motivation and confidence building",
            "- Environmental design changes"
        ]
        
        return "\n".join(prompt_parts)
    
    def _build_general_intervention_prompt(
        self,
        request: InterventionRequest,
        user_patterns: Dict[str, Any],
        context: AgentContext
    ) -> str:
        """
        Build prompt for general interventions
        """
        prompt_parts = [
            f"Generate a personalized intervention for the user.",
            f"Domain: {request.domain}",
            f"Urgency: {request.urgency}",
            "",
            "USER CONTEXT:",
            self._build_context_prompt(context),
            "",
            "USER PATTERNS:",
            json.dumps(user_patterns, indent=2),
            "",
            "REQUIREMENTS:",
            "1. Personalize based on user patterns and preferences",
            "2. Apply relevant behavioral science techniques",
            "3. Consider current context and constraints",
            "4. Provide clear, actionable guidance",
            "5. Include reasoning for recommendations",
            "6. Consider cross-domain goal interactions"
        ]
        
        return "\n".join(prompt_parts)
    
    def _parse_llm_intervention_response(self, response_content: str) -> Dict[str, Any]:
        """
        Parse LLM response into structured intervention format
        """
        # Try to extract structured information from the response
        # This is a simplified version - in production, you'd use more sophisticated parsing
        
        lines = response_content.split('\n')
        
        intervention = {
            "content": response_content,
            "reasoning": "",
            "actions": [],
            "techniques": [],
            "expected_compliance": 0.7  # Default
        }
        
        # Extract specific sections if they exist
        current_section = None
        for line in lines:
            line = line.strip()
            if line.lower().startswith("reasoning:"):
                current_section = "reasoning"
                intervention["reasoning"] = line[10:].strip()
            elif line.lower().startswith("actions:"):
                current_section = "actions"
            elif line.lower().startswith("techniques:"):
                current_section = "techniques"
            elif line.startswith("- ") and current_section:
                if current_section == "actions":
                    intervention["actions"].append(line[2:])
                elif current_section == "techniques":
                    intervention["techniques"].append(line[2:])
        
        return intervention
    
    async def _apply_cross_domain_optimization(
        self,
        intervention: Dict[str, Any],
        context: AgentContext
    ) -> Dict[str, Any]:
        """
        Apply cross-domain optimization to consider goal interactions
        """
        if not context.current_goals or len(context.current_goals) < 2:
            return intervention
        
        # Analyze goal interactions
        goal_interactions = await self.pattern_analyzer.analyze_goal_interactions(
            context.current_goals, context.recent_history
        )
        
        # Modify intervention based on interactions
        cross_domain_effects = []
        
        for interaction in goal_interactions:
            if interaction["impact_score"] > 0.5:  # Significant interaction
                effect = {
                    "source_domain": interaction["source_domain"],
                    "target_domain": interaction["target_domain"],
                    "effect_type": interaction["effect_type"],
                    "recommendation": interaction["recommendation"]
                }
                cross_domain_effects.append(effect)
                
                # Modify intervention content to include cross-domain considerations
                intervention["content"] += f"\n\n🔗 Cross-domain insight: {interaction['recommendation']}"
        
        intervention["cross_domain_effects"] = cross_domain_effects
        
        return intervention
    
    def _calculate_intervention_confidence(
        self,
        intervention: Dict[str, Any],
        user_patterns: Dict[str, Any],
        context: AgentContext
    ) -> float:
        """
        Calculate confidence score for the intervention
        """
        confidence_factors = []
        
        # Pattern match confidence
        pattern_confidence = user_patterns.get("confidence", 0.5)
        confidence_factors.append(pattern_confidence * 0.3)
        
        # Historical compliance rate
        historical_compliance = user_patterns.get("average_compliance_rate", 0.7)
        confidence_factors.append(historical_compliance * 0.3)
        
        # Context completeness
        context_completeness = min(1.0, len(context.user_state) / 10)  # Assume 10 is complete
        confidence_factors.append(context_completeness * 0.2)
        
        # Intervention specificity
        specificity = min(1.0, len(intervention.get("actions", [])) / 5)  # 5 actions is very specific
        confidence_factors.append(specificity * 0.2)
        
        return min(1.0, sum(confidence_factors))
    
    async def _store_intervention_for_learning(
        self,
        intervention: Dict[str, Any],
        context: AgentContext
    ):
        """
        Store intervention data for the optimizer agent to learn from
        """
        intervention_record = {
            "user_id": context.user_id,
            "session_id": context.session_id,
            "timestamp": datetime.utcnow().isoformat(),
            "intervention": intervention,
            "context": {
                "goals": context.current_goals,
                "user_state": context.user_state,
                "external_context": context.external_context
            }
        }
        
        # Store in intervention history (in production, this would go to a database)
        if context.user_id not in self.intervention_history:
            self.intervention_history[context.user_id] = []
        
        self.intervention_history[context.user_id].append(intervention_record)
        
        # Keep only last 100 interventions per user
        if len(self.intervention_history[context.user_id]) > 100:
            self.intervention_history[context.user_id] = self.intervention_history[context.user_id][-100:]
        
        logger.info(
            "Intervention stored for learning",
            user_id=context.user_id,
            intervention_type=intervention.get("type", "unknown")
        )