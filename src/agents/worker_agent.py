"""
ORBIT Worker Agent
Generates personalized interventions, daily plans, and behavioral nudges
"""

import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from langchain.schema import SystemMessage, HumanMessage

from .base_agent import BaseAgent, AgentResponse, AgentContext
from ..core.config import settings, DOMAIN_CONFIGS
from ..models.intervention import InterventionType
import structlog

logger = structlog.get_logger(__name__)


class WorkerAgent(BaseAgent):
    """
    Worker Agent: The creative force behind ORBIT's interventions
    
    Responsibilities:
    - Generate personalized daily plans
    - Create contextual interventions and nudges
    - Adapt strategies based on user patterns
    - Provide cross-domain optimization suggestions
    """
    
    def __init__(self, model_config: Optional[Dict[str, Any]] = None):
        super().__init__(
            agent_type="worker",
            model_config=model_config or {
                "model": settings.DEFAULT_WORKER_MODEL,
                "temperature": 0.7,
                "max_tokens": 4000,
                "system_prompt": self._build_system_prompt()
            }
        )
    
    def _build_system_prompt(self) -> str:
        """Build the comprehensive system prompt for the Worker Agent"""
        return """You are the Worker Agent in ORBIT, an autonomous life optimization platform.

CORE MISSION:
Generate personalized, actionable interventions that help users achieve their goals through behavioral science-backed strategies.

BEHAVIORAL SCIENCE PRINCIPLES:
1. Implementation Intentions: Create specific "if-then" plans
2. Habit Stacking: Link new behaviors to existing habits
3. Temptation Bundling: Pair desired behaviors with enjoyable activities
4. Social Proof: Reference what similar users have achieved
5. Loss Aversion: Frame in terms of what they might lose
6. Fresh Start Effect: Leverage natural reset points
7. Friction Injection: Make bad habits harder, good habits easier

INTERVENTION TYPES:
- NUDGE: Gentle reminder or suggestion (low friction)
- PLAN: Structured daily/weekly plan with specific actions
- FRICTION: Introduce barriers to unwanted behaviors
- REWARD: Celebrate achievements and milestones
- PIVOT: Adjust strategy when current approach isn't working
- SYNC: Cross-domain optimization suggestions

RESPONSE FORMAT:
Always respond with a JSON object containing:
{
  "intervention_type": "NUDGE|PLAN|FRICTION|REWARD|PIVOT|SYNC",
  "domain": "health|finance|productivity|learning|social",
  "title": "Brief, engaging title",
  "content": "Main intervention content",
  "reasoning": "Why this intervention now",
  "behavioral_principle": "Which principle(s) you're applying",
  "timing": "when|immediate|scheduled",
  "expected_outcome": "What success looks like",
  "fallback_strategy": "What to do if user doesn't engage",
  "cross_domain_effects": ["potential impacts on other goals"],
  "confidence": 0.0-1.0
}

PERSONALIZATION FACTORS:
- User's historical compliance patterns
- Current energy/motivation levels
- Time of day and context
- Recent successes and failures
- Personality indicators (if available)
- External factors (weather, calendar, etc.)

SAFETY GUIDELINES:
- Never suggest anything that could cause physical harm
- Avoid financial advice beyond basic budgeting
- Don't provide medical advice
- Be sensitive to mental health considerations
- Respect user boundaries and preferences

QUALITY STANDARDS:
- Be specific and actionable
- Include clear success metrics
- Provide fallback options
- Consider timing and context
- Explain your reasoning clearly
"""
    
    async def _execute_internal(
        self,
        context: AgentContext,
        user_input: str,
        intervention_type: Optional[str] = None,
        domain: Optional[str] = None,
        **kwargs
    ) -> AgentResponse:
        """
        Generate a personalized intervention based on context and input
        """
        try:
            # Build comprehensive context prompt
            context_prompt = self._build_intervention_context(context, user_input)
            
            # Create messages for LLM
            messages = [
                SystemMessage(content=self.model_config["system_prompt"]),
                HumanMessage(content=context_prompt)
            ]
            
            # Call LLM
            llm_response = await self._call_llm(messages)
            
            # Parse the JSON response
            try:
                intervention_data = json.loads(llm_response["content"])
            except json.JSONDecodeError:
                # Fallback: extract JSON from response if it's embedded in text
                intervention_data = self._extract_json_from_text(llm_response["content"])
            
            # Validate and enhance the intervention
            validated_intervention = self._validate_intervention(intervention_data, context)
            
            # Calculate confidence based on context quality and user history
            confidence = self._calculate_confidence(validated_intervention, context)
            validated_intervention["confidence"] = confidence
            
            return AgentResponse(
                content=json.dumps(validated_intervention, indent=2),
                reasoning=validated_intervention.get("reasoning", "Generated personalized intervention"),
                confidence=confidence,
                metadata={
                    "intervention_type": validated_intervention.get("intervention_type"),
                    "domain": validated_intervention.get("domain"),
                    "behavioral_principle": validated_intervention.get("behavioral_principle"),
                    "token_usage": llm_response.get("token_usage", {})
                },
                token_usage=llm_response.get("token_usage", {})
            )
            
        except Exception as e:
            logger.error(
                "Worker agent execution failed",
                error=str(e),
                user_id=context.user_id,
                exc_info=True
            )
            
            # Return fallback intervention
            fallback = self._generate_fallback_intervention(context, user_input)
            return AgentResponse(
                content=json.dumps(fallback, indent=2),
                reasoning="Generated fallback intervention due to processing error",
                confidence=0.3,
                metadata={"fallback": True, "error": str(e)}
            )
    
    def _build_intervention_context(self, context: AgentContext, user_input: str) -> str:
        """Build comprehensive context for intervention generation"""
        
        context_parts = [
            f"USER REQUEST: {user_input}",
            f"TIMESTAMP: {datetime.utcnow().isoformat()}",
            f"USER ID: {context.user_id}",
        ]
        
        # Current goals analysis
        if context.current_goals:
            context_parts.append("\nCURRENT GOALS:")
            for goal in context.current_goals:
                goal_info = f"- {goal.get('title', 'Untitled')}"
                if goal.get('domain'):
                    goal_info += f" (Domain: {goal['domain']})"
                if goal.get('progress') is not None:
                    goal_info += f" - Progress: {goal['progress']}%"
                if goal.get('deadline'):
                    goal_info += f" - Deadline: {goal['deadline']}"
                if goal.get('status'):
                    goal_info += f" - Status: {goal['status']}"
                context_parts.append(goal_info)
        
        # User state and patterns
        if context.user_state:
            context_parts.append(f"\nUSER STATE:")
            for key, value in context.user_state.items():
                context_parts.append(f"- {key}: {value}")
        
        # Recent activity patterns
        if context.recent_history:
            context_parts.append(f"\nRECENT ACTIVITY (Last {len(context.recent_history)} events):")
            for event in context.recent_history[-10:]:  # Last 10 events
                timestamp = event.get('timestamp', 'Unknown')
                action = event.get('action', 'Unknown action')
                outcome = event.get('outcome', '')
                context_parts.append(f"- {timestamp}: {action} {outcome}")
        
        # External context (calendar, weather, etc.)
        if context.external_context:
            context_parts.append(f"\nEXTERNAL CONTEXT:")
            for key, value in context.external_context.items():
                context_parts.append(f"- {key}: {value}")
        
        # Add behavioral insights if available
        behavioral_insights = self._extract_behavioral_insights(context)
        if behavioral_insights:
            context_parts.append(f"\nBEHAVIORAL INSIGHTS:")
            for insight in behavioral_insights:
                context_parts.append(f"- {insight}")
        
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