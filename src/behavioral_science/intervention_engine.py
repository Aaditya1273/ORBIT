"""
ORBIT Behavioral Science Intervention Engine
World-class behavioral science implementation for habit formation and behavior change
"""

import json
import random
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import structlog

logger = structlog.get_logger(__name__)


class BehavioralTechnique(Enum):
    """Behavioral science techniques available in ORBIT"""
    IMPLEMENTATION_INTENTIONS = "implementation_intentions"
    HABIT_STACKING = "habit_stacking"
    TEMPTATION_BUNDLING = "temptation_bundling"
    SOCIAL_PROOF = "social_proof"
    LOSS_AVERSION = "loss_aversion"
    FRESH_START_EFFECT = "fresh_start_effect"
    FRICTION_INJECTION = "friction_injection"
    COMMITMENT_DEVICE = "commitment_device"
    MENTAL_CONTRASTING = "mental_contrasting"
    ENVIRONMENTAL_DESIGN = "environmental_design"


@dataclass
class InterventionContext:
    """Context for behavioral intervention"""
    user_id: str
    goal_domain: str
    current_behavior: str
    desired_behavior: str
    user_patterns: Dict[str, Any]
    environmental_factors: Dict[str, Any]
    historical_compliance: float
    energy_level: float
    time_of_day: int
    day_of_week: int
    streak_count: int
    recent_failures: int


@dataclass
class BehavioralIntervention:
    """Structured behavioral intervention"""
    technique: BehavioralTechnique
    content: str
    implementation_plan: str
    success_metrics: List[str]
    expected_compliance: float
    difficulty_level: int  # 1-5
    time_investment: int  # minutes
    environmental_requirements: List[str]
    fallback_strategy: str
    behavioral_rationale: str


class InterventionEngine:
    """
    Core engine for generating behavioral science-backed interventions
    """
    
    def __init__(self):
        self.technique_library = self._initialize_technique_library()
        self.success_patterns = self._load_success_patterns()
        self.personalization_rules = self._load_personalization_rules()
        
        logger.info("Intervention Engine initialized with behavioral science techniques")
    
    async def generate_intervention(
        self,
        context: InterventionContext,
        preferred_techniques: Optional[List[BehavioralTechnique]] = None
    ) -> BehavioralIntervention:
        """
        Generate a personalized behavioral intervention based on context
        """
        try:
            # Select optimal technique
            technique = await self._select_optimal_technique(context, preferred_techniques)
            
            # Generate intervention content
            intervention = await self._generate_technique_intervention(technique, context)
            
            # Personalize based on user patterns
            personalized_intervention = await self._personalize_intervention(intervention, context)
            
            # Add environmental considerations
            final_intervention = await self._add_environmental_design(personalized_intervention, context)
            
            logger.info(
                "Behavioral intervention generated",
                technique=technique.value,
                expected_compliance=final_intervention.expected_compliance,
                user_id=context.user_id
            )
            
            return final_intervention
            
        except Exception as e:
            logger.error(
                "Failed to generate behavioral intervention",
                error=str(e),
                user_id=context.user_id,
                exc_info=True
            )
            
            # Return fallback intervention
            return await self._generate_fallback_intervention(context)
    
    async def _select_optimal_technique(
        self,
        context: InterventionContext,
        preferred_techniques: Optional[List[BehavioralTechnique]] = None
    ) -> BehavioralTechnique:
        """
        Select the most appropriate behavioral technique based on context
        """
        # Calculate technique scores
        technique_scores = {}
        
        available_techniques = preferred_techniques or list(BehavioralTechnique)
        
        for technique in available_techniques:
            score = await self._calculate_technique_score(technique, context)
            technique_scores[technique] = score
        
        # Select highest scoring technique
        best_technique = max(technique_scores, key=technique_scores.get)
        
        logger.debug(
            "Technique selected",
            technique=best_technique.value,
            score=technique_scores[best_technique],
            all_scores=[(t.value, s) for t, s in technique_scores.items()]
        )
        
        return best_technique
    
    async def _calculate_technique_score(
        self,
        technique: BehavioralTechnique,
        context: InterventionContext
    ) -> float:
        """
        Calculate effectiveness score for a technique given the context
        """
        base_score = 0.5
        
        # Historical compliance factor
        compliance_factor = min(context.historical_compliance * 1.5, 1.0)
        
        # Technique-specific scoring
        if technique == BehavioralTechnique.IMPLEMENTATION_INTENTIONS:
            # Works well for specific, concrete behaviors
            if "specific" in context.desired_behavior.lower():
                base_score += 0.3
            if context.energy_level > 0.7:
            "learning": {
                "primary_techniques": ["habit_stacking", "temptation_bundling", "implementation_intention"],
                "crisis_techniques": ["friction_reduction", "social_proof"],
                "motivation_boosters": ["fresh_start_effect", "commitment_device"],
                "common_barriers": ["time_constraints", "difficulty", "lack_of_progress", "boredom"],
                "success_predictors": ["spaced_repetition", "active_practice", "clear_goals"]
            },
            "social": {
                "primary_techniques": ["implementation_intention", "habit_stacking", "social_proof"],
                "crisis_techniques": ["friction_reduction", "environmental_design"],
                "motivation_boosters": ["commitment_device", "fresh_start_effect"],
                "common_barriers": ["social_anxiety", "time_constraints", "energy_levels"],
                "success_predictors": ["regular_contact", "shared_activities", "mutual_support"]
            }
        }
    
    def _initialize_crisis_protocols(self) -> Dict[str, Dict[str, Any]]:
        """Initialize crisis intervention protocols"""
        return {
            "goal_abandonment_risk": {
                "triggers": ["missed_3_consecutive", "progress_below_20_percent", "negative_feedback_loop"],
                "interventions": [
                    "reduce_difficulty_temporarily",
                    "provide_social_support",
                    "reframe_expectations",
                    "celebrate_small_wins"
                ],
                "techniques": ["friction_reduction", "social_proof", "fresh_start_effect"]
            },
            "motivation_crisis": {
                "triggers": ["low_engagement_score", "skipped_interventions", "negative_self_talk"],
                "interventions": [
                    "reconnect_with_why",
                    "provide_inspiration_stories",
                    "adjust_approach",
                    "offer_alternatives"
                ],
                "techniques": ["loss_aversion", "social_proof", "commitment_device"]
            },
            "overwhelm_state": {
                "triggers": ["too_many_goals", "high_stress_indicators", "decision_fatigue"],
                "interventions": [
                    "simplify_approach",
                    "prioritize_ruthlessly",
                    "provide_structure",
                    "reduce_cognitive_load"
                ],
                "techniques": ["environmental_design", "implementation_intention", "friction_reduction"]
            }
        }
    
    async def enhance_with_behavioral_science(
        self,
        intervention: Dict[str, Any],
        user_patterns: Dict[str, Any],
        domain: str
    ) -> Dict[str, Any]:
        """
        Enhance intervention with appropriate behavioral science techniques
        """
        try:
            # Select appropriate techniques for the domain
            domain_strategy = self.domain_strategies.get(domain, self.domain_strategies["productivity"])
            primary_techniques = domain_strategy["primary_techniques"]
            
            # Analyze user patterns to select best techniques
            selected_techniques = self._select_techniques_for_user(
                primary_techniques, user_patterns, domain
            )
            
            # Apply each selected technique
            enhanced_intervention = intervention.copy()
            applied_techniques = []
            
            for technique_name in selected_techniques:
                if technique_name in self.techniques:
                    technique = self.techniques[technique_name]
                    enhanced_content = await self._apply_technique(
                        enhanced_intervention["content"],
                        technique,
                        user_patterns,
                        domain
                    )
                    
                    if enhanced_content != enhanced_intervention["content"]:
                        enhanced_intervention["content"] = enhanced_content
                        applied_techniques.append({
                            "name": technique.name,
                            "description": technique.description,
                            "effectiveness_score": technique.effectiveness_score
                        })
            
            # Update intervention metadata
            enhanced_intervention["techniques"] = applied_techniques
            enhanced_intervention["behavioral_science_applied"] = True
            enhanced_intervention["expected_compliance"] = self._calculate_expected_compliance(
                applied_techniques, user_patterns, domain
            )
            
            logger.info(
                "Intervention enhanced with behavioral science",
                domain=domain,
                techniques_applied=len(applied_techniques),
                expected_compliance=enhanced_intervention["expected_compliance"]
            )
            
            return enhanced_intervention
            
        except Exception as e:
            logger.error(f"Failed to enhance intervention with behavioral science: {str(e)}")
            return intervention
    
    def _select_techniques_for_user(
        self,
        available_techniques: List[str],
        user_patterns: Dict[str, Any],
        domain: str
    ) -> List[str]:
        """
        Select the most appropriate techniques based on user patterns
        """
        selected = []
        
        # Get user preferences and success patterns
        preferred_styles = user_patterns.get("preferred_intervention_styles", [])
        historical_success = user_patterns.get("technique_success_rates", {})
        personality_traits = user_patterns.get("personality_traits", {})
        
        for technique_name in available_techniques:
            if technique_name not in self.techniques:
                continue
                
            technique = self.techniques[technique_name]
            
            # Score technique based on multiple factors
            score = 0.0
            
            # Base effectiveness
            score += technique.effectiveness_score * 0.4
            
            # Historical success with this user
            if technique_name in historical_success:
                score += historical_success[technique_name] * 0.3
            
            # User preference alignment
            if technique.implementation_difficulty in preferred_styles:
                score += 0.2
            
            # Personality trait alignment
            if self._technique_matches_personality(technique, personality_traits):
                score += 0.1
            
            # Select if score is above threshold
            if score > 0.6:  # Threshold for technique selection
                selected.append(technique_name)
        
        # Limit to top 3 techniques to avoid overwhelming the user
        selected = sorted(selected, key=lambda t: self.techniques[t].effectiveness_score, reverse=True)[:3]
        
        return selected
    
    def _technique_matches_personality(
        self,
        technique: BehavioralTechnique,
        personality_traits: Dict[str, float]
    ) -> bool:
        """
        Check if technique aligns with user's personality traits
        """
        # Simplified personality matching - in production, this would be more sophisticated
        if technique.name == "Social Proof" and personality_traits.get("extraversion", 0.5) > 0.6:
            return True
        if technique.name == "Implementation Intention" and personality_traits.get("conscientiousness", 0.5) > 0.7:
            return True
        if technique.name == "Temptation Bundling" and personality_traits.get("openness", 0.5) > 0.6:
            return True
        
        return False
    
    async def _apply_technique(
        self,
        intervention_content: str,
        technique: BehavioralTechnique,
        user_patterns: Dict[str, Any],
        domain: str
    ) -> str:
        """
        Apply a specific behavioral science technique to intervention content
        """
        if technique.name == "Implementation Intention":
            return self._apply_implementation_intention(intervention_content, user_patterns)
        elif technique.name == "Habit Stacking":
            return self._apply_habit_stacking(intervention_content, user_patterns)
        elif technique.name == "Social Proof":
            return self._apply_social_proof(intervention_content, domain)
        elif technique.name == "Loss Aversion":
            return self._apply_loss_aversion(intervention_content, user_patterns)
        elif technique.name == "Environmental Design":
            return self._apply_environmental_design(intervention_content, domain)
        elif technique.name == "Friction Injection":
            return self._apply_friction_injection(intervention_content, domain)
        else:
            return intervention_content
    
    def _apply_implementation_intention(
        self,
        content: str,
        user_patterns: Dict[str, Any]
    ) -> str:
        """Apply implementation intention technique"""
        # Add if-then planning structure
        schedule = user_patterns.get("typical_schedule", {})
        
        if "morning_routine" in schedule:
            morning_time = schedule["morning_routine"].get("time", "7:00 AM")
            content += f"\n\n🎯 Implementation Plan: If it's {morning_time} and I've finished my morning routine, then I will immediately start this action."
        else:
            content += f"\n\n🎯 Implementation Plan: Choose a specific time and trigger. For example: 'If I finish my morning coffee, then I will immediately do this action.'"
        
        return content
    
    def _apply_habit_stacking(
        self,
        content: str,
        user_patterns: Dict[str, Any]
    ) -> str:
        """Apply habit stacking technique"""
        existing_habits = user_patterns.get("strong_habits", [])
        
        if existing_habits:
            habit = random.choice(existing_habits)
            content += f"\n\n🔗 Habit Stack: After you {habit.lower()}, immediately do this new action. This leverages your existing routine for automatic success."
        else:
            content += f"\n\n🔗 Habit Stack: Attach this new action to something you already do consistently every day (like brushing teeth, having coffee, or checking email)."
        
        return content
    
    def _apply_social_proof(self, content: str, domain: str) -> str:
        """Apply social proof technique"""
        # Domain-specific social proof examples
        social_proof_examples = {
            "health": "83% of people with similar goals who exercise in the morning stick to their routine long-term",
            "finance": "Users who automate their savings are 7x more likely to reach their financial goals",
            "productivity": "People who time-block their calendar are 3x more productive than those who don't",
            "learning": "Learners who practice for 15 minutes daily retain 90% more information than weekend warriors",
            "social": "People who schedule regular check-ins maintain stronger relationships over time"
        }
        
        proof = social_proof_examples.get(domain, "Most successful people in this area follow a similar approach")
        content += f"\n\n👥 Social Proof: {proof}. You're joining a community of successful achievers!"
        
        return content
    
    def _apply_loss_aversion(
        self,
        content: str,
        user_patterns: Dict[str, Any]
    ) -> str:
        """Apply loss aversion technique"""
        goals = user_patterns.get("current_goals", [])
        
        if goals:
            goal = goals[0]  # Use primary goal
            content += f"\n\n⚠️ Consider This: Every day you delay is a day further from achieving {goal.get('title', 'your goal')}. The cost of inaction compounds over time."
        else:
            content += f"\n\n⚠️ Consider This: Each day without action is a missed opportunity that you can't get back. The cost of waiting often exceeds the cost of starting imperfectly."
        
        return content
    
    def _apply_environmental_design(self, content: str, domain: str) -> str:
        """Apply environmental design technique"""
        design_suggestions = {
            "health": "Set out your workout clothes the night before and keep healthy snacks visible",
            "finance": "Use separate savings accounts and hide spending apps in folders on your phone",
            "productivity": "Create a dedicated workspace and remove distracting items from view",
            "learning": "Keep learning materials visible and remove entertainment options from study area",
            "social": "Add social events to your calendar and set reminders to reach out to friends"
        }
        
        suggestion = design_suggestions.get(domain, "Modify your environment to make success easier")
        content += f"\n\n🏗️ Environment Design: {suggestion}. Your environment should work for you, not against you."
        
        return content
    
    def _apply_friction_injection(self, content: str, domain: str) -> str:
        """Apply friction injection technique"""
        friction_examples = {
            "finance": "Add a 24-hour delay before non-essential purchases over $50",
            "health": "Put junk food in hard-to-reach places and healthy food at eye level",
            "productivity": "Use website blockers during focus time and put your phone in another room",
            "learning": "Remove entertainment apps from your phone during study hours",
            "social": "Set specific times for social media and use app timers to enforce limits"
        }
        
        example = friction_examples.get(domain, "Add small barriers to behaviors you want to reduce")
        content += f"\n\n🚧 Smart Friction: {example}. Make bad choices harder and good choices easier."
        
        return content
    
    def _calculate_expected_compliance(
        self,
        applied_techniques: List[Dict[str, Any]],
        user_patterns: Dict[str, Any],
        domain: str
    ) -> float:
        """
        Calculate expected compliance rate based on applied techniques and user patterns
        """
        base_compliance = user_patterns.get("average_compliance_rate", 0.6)
        
        # Boost from behavioral science techniques
        technique_boost = 0.0
        for technique in applied_techniques:
            technique_boost += technique["effectiveness_score"] * 0.1  # Each technique adds up to 10% boost
        
        # Domain-specific adjustments
        domain_multipliers = {
            "health": 0.9,  # Slightly harder
            "finance": 1.1,  # Easier with automation
            "productivity": 1.0,  # Baseline
            "learning": 0.95,  # Slightly harder
            "social": 1.05   # Slightly easier
        }
        
        domain_multiplier = domain_multipliers.get(domain, 1.0)
        
        # Calculate final compliance rate
        expected_compliance = min(0.95, (base_compliance + technique_boost) * domain_multiplier)
        
        return round(expected_compliance, 2)
    
    async def apply_crisis_intervention_techniques(
        self,
        intervention: Dict[str, Any],
        user_patterns: Dict[str, Any],
        context: Any
    ) -> Dict[str, Any]:
        """
        Apply crisis intervention techniques for users in distress
        """
        # Identify crisis type
        crisis_type = self._identify_crisis_type(user_patterns, context)
        
        if crisis_type and crisis_type in self.crisis_protocols:
            protocol = self.crisis_protocols[crisis_type]
            
            # Apply crisis-specific techniques
            crisis_techniques = protocol["techniques"]
            enhanced_intervention = intervention.copy()
            
            # Make intervention more supportive and less demanding
            enhanced_intervention["content"] = self._make_intervention_supportive(
                enhanced_intervention["content"]
            )
            
            # Apply crisis techniques
            for technique_name in crisis_techniques:
                if technique_name in self.techniques:
                    technique = self.techniques[technique_name]
                    enhanced_intervention["content"] = await self._apply_technique(
                        enhanced_intervention["content"],
                        technique,
                        user_patterns,
                        "crisis"
                    )
            
            enhanced_intervention["crisis_intervention"] = True
            enhanced_intervention["crisis_type"] = crisis_type
            
            logger.info(f"Crisis intervention applied: {crisis_type}")
            
            return enhanced_intervention
        
        return intervention
    
    def _identify_crisis_type(self, user_patterns: Dict[str, Any], context: Any) -> Optional[str]:
        """Identify if user is in crisis and what type"""
        # Simplified crisis detection - in production, this would be more sophisticated
        compliance_rate = user_patterns.get("recent_compliance_rate", 1.0)
        engagement_score = user_patterns.get("engagement_score", 1.0)
        goal_count = len(getattr(context, 'current_goals', []))
        
        if compliance_rate < 0.3:
            return "goal_abandonment_risk"
        elif engagement_score < 0.4:
            return "motivation_crisis"
        elif goal_count > 5:
            return "overwhelm_state"
        
        return None
    
    def _make_intervention_supportive(self, content: str) -> str:
        """Make intervention more supportive for crisis situations"""
        supportive_prefix = "I understand you're going through a challenging time. Let's take a gentle, supportive approach:\n\n"
        
        # Add empathy and reduce pressure
        content = content.replace("You must", "When you're ready, you might")
        content = content.replace("You should", "Consider")
        content = content.replace("immediately", "when it feels right")
        
        return supportive_prefix + content
    
    async def apply_failure_prevention_techniques(
        self,
        intervention: Dict[str, Any],
        user_patterns: Dict[str, Any],
        failure_risk: float
    ) -> Dict[str, Any]:
        """
        Apply failure prevention techniques based on risk assessment
        """
        enhanced_intervention = intervention.copy()
        
        # Add failure prevention messaging
        risk_level = "high" if failure_risk > 0.8 else "medium" if failure_risk > 0.6 else "low"
        
        prevention_messages = {
            "high": "🚨 Early Warning: I've detected patterns that suggest you might be at risk of abandoning this goal. Let's take preventive action now.",
            "medium": "⚠️ Heads Up: Some patterns suggest we should adjust our approach to keep you on track.",
            "low": "✅ Looking Good: You're on a positive trajectory. Let's maintain this momentum."
        }
        
        enhanced_intervention["content"] = (
            prevention_messages[risk_level] + "\n\n" + enhanced_intervention["content"]
        )
        
        # Apply specific failure prevention techniques
        if failure_risk > 0.7:
            # High risk - apply multiple prevention techniques
            enhanced_intervention["content"] += "\n\n🛡️ Failure Prevention Plan:"
            enhanced_intervention["content"] += "\n• Reduce difficulty by 30% temporarily"
            enhanced_intervention["content"] += "\n• Set up daily check-ins for accountability"
            enhanced_intervention["content"] += "\n• Identify and remove the biggest obstacle"
            enhanced_intervention["content"] += "\n• Celebrate small wins to rebuild momentum"
        
        enhanced_intervention["failure_prevention_applied"] = True
        enhanced_intervention["failure_risk"] = failure_risk
        
        return enhanced_intervention