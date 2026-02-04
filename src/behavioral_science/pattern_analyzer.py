"""
ORBIT Pattern Analyzer
Advanced behavioral pattern analysis and failure prediction
"""

import json
import statistics
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from collections import defaultdict, Counter

import structlog

logger = structlog.get_logger(__name__)


@dataclass
class BehavioralPattern:
    """Identified behavioral pattern"""
    pattern_type: str
    confidence: float
    description: str
    frequency: int
    last_occurrence: datetime
    impact_score: float  # -1.0 to 1.0 (negative = harmful, positive = helpful)
    recommendations: List[str]


@dataclass
class GoalInteraction:
    """Cross-domain goal interaction analysis"""
    source_domain: str
    target_domain: str
    interaction_type: str  # "synergistic", "competing", "neutral"
    impact_score: float  # -1.0 to 1.0
    effect_type: str  # "positive", "negative", "neutral"
    recommendation: str
    evidence: List[str]


class PatternAnalyzer:
    """
    Advanced behavioral pattern analysis engine for ORBIT
    """
    
    def __init__(self):
        self.pattern_cache = {}
        self.interaction_cache = {}
        
        # Pattern recognition thresholds
        self.min_pattern_occurrences = 3
        self.pattern_confidence_threshold = 0.6
        self.interaction_significance_threshold = 0.4
        
        logger.info("Pattern Analyzer initialized")
    
    async def analyze_user_patterns(
        self,
        user_id: str,
        history: List[Dict[str, Any]],
        goals: List[Dict[str, Any]],
        user_state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Comprehensive analysis of user behavioral patterns
        """
        try:
            # Analyze different types of patterns
            temporal_patterns = self._analyze_temporal_patterns(history)
            compliance_patterns = self._analyze_compliance_patterns(history)
            energy_patterns = self._analyze_energy_patterns(history, user_state)
            context_patterns = self._analyze_context_patterns(history)
            goal_patterns = self._analyze_goal_patterns(goals, history)
            
            # Calculate overall pattern confidence
            pattern_confidence = self._calculate_pattern_confidence([
                temporal_patterns, compliance_patterns, energy_patterns,
                context_patterns, goal_patterns
            ])
            
            # Generate insights and recommendations
            insights = self._generate_pattern_insights(
                temporal_patterns, compliance_patterns, energy_patterns,
                context_patterns, goal_patterns
            )
            
            patterns = {
                "user_id": user_id,
                "analysis_timestamp": datetime.utcnow().isoformat(),
                "confidence": pattern_confidence,
                "temporal_patterns": temporal_patterns,
                "compliance_patterns": compliance_patterns,
                "energy_patterns": energy_patterns,
                "context_patterns": context_patterns,
                "goal_patterns": goal_patterns,
                "insights": insights,
                "recommendations": self._generate_pattern_recommendations(insights)
            }
            
            # Cache results
            self.pattern_cache[user_id] = {
                "patterns": patterns,
                "timestamp": datetime.utcnow()
            }
            
            logger.info(
                "User patterns analyzed",
                user_id=user_id,
                confidence=pattern_confidence,
                insights_count=len(insights)
            )
            
            return patterns
            
        except Exception as e:
            logger.error(f"Pattern analysis failed for user {user_id}: {str(e)}")
            return self._get_default_patterns(user_id)
    
    def _analyze_temporal_patterns(self, history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze time-based behavioral patterns"""
        if not history:
            return {"confidence": 0.0, "patterns": []}
        
        # Group activities by time of day
        hourly_activity = defaultdict(list)
        daily_activity = defaultdict(list)
        weekly_activity = defaultdict(list)
        
        for event in history:
            if "timestamp" in event:
                try:
                    timestamp = datetime.fromisoformat(event["timestamp"].replace("Z", "+00:00"))
                    hour = timestamp.hour
                    day = timestamp.strftime("%A")
                    week = timestamp.isocalendar()[1]
                    
                    activity_type = event.get("action", "unknown")
                    
                    hourly_activity[hour].append(activity_type)
                    daily_activity[day].append(activity_type)
                    weekly_activity[week].append(activity_type)
                except:
                    continue
        
        patterns = []
        
        # Find peak activity hours
        if hourly_activity:
            peak_hours = sorted(hourly_activity.keys(), key=lambda h: len(hourly_activity[h]), reverse=True)[:3]
            patterns.append({
                "type": "peak_activity_hours",
                "data": peak_hours,
                "confidence": min(1.0, len(history) / 50),  # More data = higher confidence
                "description": f"Most active during hours: {', '.join(map(str, peak_hours))}"
            })
        
        # Find preferred days
        if daily_activity:
            preferred_days = sorted(daily_activity.keys(), key=lambda d: len(daily_activity[d]), reverse=True)[:3]
            patterns.append({
                "type": "preferred_days",
                "data": preferred_days,
                "confidence": min(1.0, len(set(daily_activity.keys())) / 7),
                "description": f"Most active on: {', '.join(preferred_days)}"
            })
        
        return {
            "confidence": self._calculate_temporal_confidence(patterns),
            "patterns": patterns,
            "hourly_distribution": dict(hourly_activity),
            "daily_distribution": dict(daily_activity)
        }
    
    def _analyze_compliance_patterns(self, history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze compliance and success patterns"""
        if not history:
            return {"confidence": 0.0, "average_compliance_rate": 0.5}
        
        # Extract compliance events
        compliance_events = []
        for event in history:
            if event.get("type") == "intervention_response":
                compliance_events.append({
                    "timestamp": event.get("timestamp"),
                    "complied": event.get("complied", False),
                    "intervention_type": event.get("intervention_type", "unknown"),
                    "domain": event.get("domain", "unknown")
                })
        
        if not compliance_events:
            return {"confidence": 0.0, "average_compliance_rate": 0.5}
        
        # Calculate overall compliance rate
        total_complied = sum(1 for event in compliance_events if event["complied"])
        compliance_rate = total_complied / len(compliance_events)
        
        # Analyze compliance by domain
        domain_compliance = defaultdict(list)
        for event in compliance_events:
            domain_compliance[event["domain"]].append(event["complied"])
        
        domain_rates = {}
        for domain, compliances in domain_compliance.items():
            domain_rates[domain] = sum(compliances) / len(compliances)
        
        # Analyze compliance by intervention type
        type_compliance = defaultdict(list)
        for event in compliance_events:
            type_compliance[event["intervention_type"]].append(event["complied"])
        
        type_rates = {}
        for int_type, compliances in type_compliance.items():
            type_rates[int_type] = sum(compliances) / len(compliances)
        
        # Find patterns in compliance timing
        compliance_trends = self._analyze_compliance_trends(compliance_events)
        
        return {
            "confidence": min(1.0, len(compliance_events) / 20),
            "average_compliance_rate": compliance_rate,
            "domain_compliance_rates": domain_rates,
            "intervention_type_rates": type_rates,
            "trends": compliance_trends,
            "total_interventions": len(compliance_events),
            "successful_interventions": total_complied
        }
    
    def _analyze_energy_patterns(
        self,
        history: List[Dict[str, Any]],
        user_state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze energy level patterns and optimal timing"""
        energy_data = []
        
        # Extract energy-related events from history
        for event in history:
            if "energy_level" in event:
                energy_data.append({
                    "timestamp": event.get("timestamp"),
                    "energy_level": event["energy_level"],
                    "activity": event.get("action", "unknown")
                })
        
        # Include current energy state
        current_energy = user_state.get("energy_level")
        if current_energy:
            energy_data.append({
                "timestamp": datetime.utcnow().isoformat(),
                "energy_level": current_energy,
                "activity": "current_state"
            })
        
        if not energy_data:
            return {"confidence": 0.0, "patterns": []}
        
        # Analyze energy by time of day
        hourly_energy = defaultdict(list)
        for data in energy_data:
            try:
                timestamp = datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
                hour = timestamp.hour
                hourly_energy[hour].append(data["energy_level"])
            except:
                continue
        
        # Calculate average energy by hour
        hourly_averages = {}
        for hour, energies in hourly_energy.items():
            if isinstance(energies[0], (int, float)):
                hourly_averages[hour] = statistics.mean(energies)
            else:
                # Handle string energy levels
                energy_map = {"low": 1, "medium": 2, "high": 3}
                numeric_energies = [energy_map.get(e.lower(), 2) for e in energies]
                hourly_averages[hour] = statistics.mean(numeric_energies)
        
        # Find peak energy hours
        peak_hours = []
        if hourly_averages:
            max_energy = max(hourly_averages.values())
            peak_hours = [hour for hour, energy in hourly_averages.items() if energy >= max_energy * 0.9]
        
        patterns = []
        if peak_hours:
            patterns.append({
                "type": "peak_energy_hours",
                "data": sorted(peak_hours),
                "confidence": min(1.0, len(energy_data) / 10),
                "description": f"Highest energy during hours: {', '.join(map(str, sorted(peak_hours)))}"
            })
        
        return {
            "confidence": min(1.0, len(energy_data) / 10),
            "patterns": patterns,
            "hourly_averages": hourly_averages,
            "peak_energy_hours": sorted(peak_hours) if peak_hours else [],
            "current_energy": current_energy
        }
    
    def _analyze_context_patterns(self, history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze contextual patterns (location, weather, social, etc.)"""
        context_data = defaultdict(list)
        
        for event in history:
            context = event.get("context", {})
            for key, value in context.items():
                if value:  # Only include non-empty values
                    context_data[key].append({
                        "value": value,
                        "success": event.get("success", False),
                        "timestamp": event.get("timestamp")
                    })
        
        patterns = []
        
        # Analyze each context dimension
        for context_type, data in context_data.items():
            if len(data) >= self.min_pattern_occurrences:
                # Find most common values
                value_counts = Counter(item["value"] for item in data)
                most_common = value_counts.most_common(3)
                
                # Calculate success rates by context value
                success_rates = defaultdict(list)
                for item in data:
                    success_rates[item["value"]].append(item["success"])
                
                context_success_rates = {}
                for value, successes in success_rates.items():
                    context_success_rates[value] = sum(successes) / len(successes)
                
                patterns.append({
                    "type": f"{context_type}_pattern",
                    "most_common_values": most_common,
                    "success_rates": context_success_rates,
                    "confidence": min(1.0, len(data) / 10),
                    "description": f"Context pattern for {context_type}"
                })
        
        return {
            "confidence": min(1.0, len(patterns) / 5) if patterns else 0.0,
            "patterns": patterns,
            "context_dimensions": list(context_data.keys())
        }
    
    def _analyze_goal_patterns(
        self,
        goals: List[Dict[str, Any]],
        history: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze goal-related patterns and preferences"""
        if not goals:
            return {"confidence": 0.0, "patterns": []}
        
        # Analyze goal domains
        domains = [goal.get("domain", "unknown") for goal in goals]
        domain_counts = Counter(domains)
        
        # Analyze goal progress patterns
        progress_data = []
        for goal in goals:
            if "progress" in goal:
                progress_data.append({
                    "domain": goal.get("domain", "unknown"),
                    "progress": goal["progress"],
                    "created_date": goal.get("created_date"),
                    "target_date": goal.get("target_date")
                })
        
        # Calculate average progress by domain
        domain_progress = defaultdict(list)
        for data in progress_data:
            domain_progress[data["domain"]].append(data["progress"])
        
        domain_avg_progress = {}
        for domain, progresses in domain_progress.items():
            domain_avg_progress[domain] = statistics.mean(progresses)
        
        patterns = []
        
        # Domain preference pattern
        if domain_counts:
            preferred_domains = [domain for domain, count in domain_counts.most_common(3)]
            patterns.append({
                "type": "domain_preferences",
                "data": preferred_domains,
                "confidence": min(1.0, len(goals) / 5),
                "description": f"Preferred goal domains: {', '.join(preferred_domains)}"
            })
        
        # Progress pattern
        if domain_avg_progress:
            best_performing_domains = sorted(
                domain_avg_progress.items(),
                key=lambda x: x[1],
                reverse=True
            )[:3]
            
            patterns.append({
                "type": "progress_performance",
                "data": best_performing_domains,
                "confidence": min(1.0, len(progress_data) / 5),
                "description": f"Best performing domains: {', '.join([d[0] for d in best_performing_domains])}"
            })
        
        return {
            "confidence": min(1.0, len(patterns) / 2) if patterns else 0.0,
            "patterns": patterns,
            "domain_distribution": dict(domain_counts),
            "domain_avg_progress": domain_avg_progress,
            "total_goals": len(goals),
            "active_goals": len([g for g in goals if g.get("status") == "active"])
        }
    
    def _calculate_pattern_confidence(self, pattern_groups: List[Dict[str, Any]]) -> float:
        """Calculate overall confidence in pattern analysis"""
        confidences = [group.get("confidence", 0.0) for group in pattern_groups]
        if not confidences:
            return 0.0
        
        # Weighted average with more weight on compliance and temporal patterns
        weights = [0.3, 0.3, 0.2, 0.1, 0.1]  # temporal, compliance, energy, context, goal
        weighted_sum = sum(conf * weight for conf, weight in zip(confidences, weights))
        
        return min(1.0, weighted_sum)
    
    def _calculate_temporal_confidence(self, patterns: List[Dict[str, Any]]) -> float:
        """Calculate confidence in temporal patterns"""
        if not patterns:
            return 0.0
        
        avg_confidence = statistics.mean(pattern.get("confidence", 0.0) for pattern in patterns)
        return avg_confidence
    
    def _analyze_compliance_trends(self, compliance_events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze trends in compliance over time"""
        if len(compliance_events) < 5:
            return {"trend": "insufficient_data"}
        
        # Sort by timestamp
        sorted_events = sorted(
            compliance_events,
            key=lambda x: x.get("timestamp", "")
        )
        
        # Calculate rolling compliance rate
        window_size = min(5, len(sorted_events) // 2)
        rolling_rates = []
        
        for i in range(len(sorted_events) - window_size + 1):
            window = sorted_events[i:i + window_size]
            rate = sum(1 for event in window if event["complied"]) / len(window)
            rolling_rates.append(rate)
        
        if len(rolling_rates) < 2:
            return {"trend": "insufficient_data"}
        
        # Determine trend
        first_half = rolling_rates[:len(rolling_rates)//2]
        second_half = rolling_rates[len(rolling_rates)//2:]
        
        first_avg = statistics.mean(first_half)
        second_avg = statistics.mean(second_half)
        
        if second_avg > first_avg + 0.1:
            trend = "improving"
        elif second_avg < first_avg - 0.1:
            trend = "declining"
        else:
            trend = "stable"
        
        return {
            "trend": trend,
            "first_half_avg": first_avg,
            "second_half_avg": second_avg,
            "change": second_avg - first_avg,
            "rolling_rates": rolling_rates
        }
    
    def _generate_pattern_insights(self, *pattern_groups) -> List[Dict[str, Any]]:
        """Generate actionable insights from pattern analysis"""
        insights = []
        
        temporal, compliance, energy, context, goal = pattern_groups
        
        # Temporal insights
        if temporal.get("confidence", 0) > 0.6:
            peak_hours = None
            for pattern in temporal.get("patterns", []):
                if pattern["type"] == "peak_activity_hours":
                    peak_hours = pattern["data"]
                    break
            
            if peak_hours:
                insights.append({
                    "type": "optimal_timing",
                    "insight": f"You're most active during hours {peak_hours}. Schedule important tasks during these times.",
                    "confidence": temporal["confidence"],
                    "actionable": True
                })
        
        # Compliance insights
        if compliance.get("confidence", 0) > 0.6:
            avg_rate = compliance.get("average_compliance_rate", 0.5)
            if avg_rate < 0.6:
                insights.append({
                    "type": "compliance_improvement",
                    "insight": f"Your compliance rate is {avg_rate:.1%}. Consider reducing intervention difficulty or frequency.",
                    "confidence": compliance["confidence"],
                    "actionable": True
                })
            elif avg_rate > 0.8:
                insights.append({
                    "type": "compliance_success",
                    "insight": f"Excellent compliance rate of {avg_rate:.1%}! You might be ready for more challenging goals.",
                    "confidence": compliance["confidence"],
                    "actionable": True
                })
        
        # Energy insights
        if energy.get("confidence", 0) > 0.6:
            peak_energy_hours = energy.get("peak_energy_hours", [])
            if peak_energy_hours:
                insights.append({
                    "type": "energy_optimization",
                    "insight": f"Your energy peaks during hours {peak_energy_hours}. Schedule demanding tasks then.",
                    "confidence": energy["confidence"],
                    "actionable": True
                })
        
        # Goal insights
        if goal.get("confidence", 0) > 0.6:
            domain_progress = goal.get("domain_avg_progress", {})
            if domain_progress:
                best_domain = max(domain_progress.items(), key=lambda x: x[1])
                worst_domain = min(domain_progress.items(), key=lambda x: x[1])
                
                if best_domain[1] - worst_domain[1] > 0.3:  # Significant difference
                    insights.append({
                        "type": "domain_performance",
                        "insight": f"You excel in {best_domain[0]} ({best_domain[1]:.1%}) but struggle with {worst_domain[0]} ({worst_domain[1]:.1%}). Consider applying successful strategies across domains.",
                        "confidence": goal["confidence"],
                        "actionable": True
                    })
        
        return insights
    
    def _generate_pattern_recommendations(self, insights: List[Dict[str, Any]]) -> List[str]:
        """Generate specific recommendations based on insights"""
        recommendations = []
        
        for insight in insights:
            if insight["type"] == "optimal_timing":
                recommendations.append("Schedule your most important goals during your peak activity hours")
            elif insight["type"] == "compliance_improvement":
                recommendations.append("Reduce intervention difficulty by 20% to improve compliance")
                recommendations.append("Increase intervention spacing to reduce overwhelm")
            elif insight["type"] == "energy_optimization":
                recommendations.append("Align demanding tasks with your natural energy peaks")
            elif insight["type"] == "domain_performance":
                recommendations.append("Apply successful strategies from your best-performing domain to struggling areas")
        
        return recommendations
    
    def _get_default_patterns(self, user_id: str) -> Dict[str, Any]:
        """Return default patterns when analysis fails"""
        return {
            "user_id": user_id,
            "analysis_timestamp": datetime.utcnow().isoformat(),
            "confidence": 0.0,
            "temporal_patterns": {"confidence": 0.0, "patterns": []},
            "compliance_patterns": {"confidence": 0.0, "average_compliance_rate": 0.6},
            "energy_patterns": {"confidence": 0.0, "patterns": []},
            "context_patterns": {"confidence": 0.0, "patterns": []},
            "goal_patterns": {"confidence": 0.0, "patterns": []},
            "insights": [],
            "recommendations": ["Start with simple, consistent actions", "Track your progress daily"]
        }
    
    async def calculate_failure_risk(
        self,
        user_patterns: Dict[str, Any],
        current_goals: List[Dict[str, Any]],
        recent_history: List[Dict[str, Any]]
    ) -> float:
        """
        Calculate the probability of goal failure based on patterns and current state
        """
        try:
            risk_factors = []
            
            # Compliance risk
            compliance_rate = user_patterns.get("compliance_patterns", {}).get("average_compliance_rate", 0.6)
            if compliance_rate < 0.4:
                risk_factors.append(0.4)  # High risk
            elif compliance_rate < 0.6:
                risk_factors.append(0.2)  # Medium risk
            
            # Goal overload risk
            active_goals = len([g for g in current_goals if g.get("status") == "active"])
            if active_goals > 5:
                risk_factors.append(0.3)
            elif active_goals > 3:
                risk_factors.append(0.1)
            
            # Progress stagnation risk
            stagnant_goals = 0
            for goal in current_goals:
                progress = goal.get("progress", 0)
                if progress < 0.2 and self._goal_age_days(goal) > 30:
                    stagnant_goals += 1
            
            if stagnant_goals > 0:
                risk_factors.append(min(0.4, stagnant_goals * 0.15))
            
            # Recent activity decline
            if len(recent_history) < 5:  # Very little recent activity
                risk_factors.append(0.25)
            
            # Energy pattern mismatch
            energy_patterns = user_patterns.get("energy_patterns", {})
            if energy_patterns.get("confidence", 0) > 0.6:
                current_energy = energy_patterns.get("current_energy")
                if current_energy and isinstance(current_energy, str):
                    if current_energy.lower() == "low":
                        risk_factors.append(0.15)
            
            # Calculate overall risk
            if not risk_factors:
                return 0.2  # Base risk
            
            # Combine risk factors (not simply additive to avoid over-penalization)
            combined_risk = 1 - (1 - sum(risk_factors)) ** 0.5
            return min(0.95, max(0.05, combined_risk))
            
        except Exception as e:
            logger.error(f"Failure risk calculation failed: {str(e)}")
            return 0.5  # Default medium risk
    
    def _goal_age_days(self, goal: Dict[str, Any]) -> int:
        """Calculate how many days old a goal is"""
        try:
            created_date = goal.get("created_date")
            if created_date:
                created = datetime.fromisoformat(created_date.replace("Z", "+00:00"))
                return (datetime.utcnow() - created).days
        except:
            pass
        return 0
    
    async def analyze_goal_interactions(
        self,
        goals: List[Dict[str, Any]],
        history: List[Dict[str, Any]]
    ) -> List[GoalInteraction]:
        """
        Analyze how goals interact with each other across domains
        """
        if len(goals) < 2:
            return []
        
        interactions = []
        
        # Analyze each pair of goals
        for i, goal1 in enumerate(goals):
            for j, goal2 in enumerate(goals[i+1:], i+1):
                interaction = await self._analyze_goal_pair_interaction(goal1, goal2, history)
                if interaction and interaction.impact_score > self.interaction_significance_threshold:
                    interactions.append(interaction)
        
        return interactions
    
    async def _analyze_goal_pair_interaction(
        self,
        goal1: Dict[str, Any],
        goal2: Dict[str, Any],
        history: List[Dict[str, Any]]
    ) -> Optional[GoalInteraction]:
        """
        Analyze interaction between two specific goals
        """
        domain1 = goal1.get("domain", "unknown")
        domain2 = goal2.get("domain", "unknown")
        
        if domain1 == domain2:
            return None  # Same domain interactions are handled elsewhere
        
        # Known domain interactions
        interaction_matrix = {
            ("health", "productivity"): {
                "type": "synergistic",
                "impact": 0.7,
                "effect": "positive",
                "recommendation": "Exercise boosts cognitive performance. Schedule workouts before important work."
            },
            ("health", "finance"): {
                "type": "competing",
                "impact": 0.4,
                "effect": "negative",
                "recommendation": "Gym memberships and healthy food cost money. Budget for health investments."
            },
            ("productivity", "learning"): {
                "type": "synergistic",
                "impact": 0.8,
                "effect": "positive",
                "recommendation": "Learning new skills enhances productivity. Combine learning with work projects."
            },
            ("finance", "social"): {
                "type": "competing",
                "impact": 0.5,
                "effect": "negative",
                "recommendation": "Social activities often involve spending. Plan budget-friendly social activities."
            },
            ("health", "social"): {
                "type": "synergistic",
                "impact": 0.6,
                "effect": "positive",
                "recommendation": "Social fitness activities combine both goals. Join group fitness classes."
            }
        }
        
        # Check both directions
        key1 = (domain1, domain2)
        key2 = (domain2, domain1)
        
        interaction_data = interaction_matrix.get(key1) or interaction_matrix.get(key2)
        
        if interaction_data:
            return GoalInteraction(
                source_domain=domain1,
                target_domain=domain2,
                interaction_type=interaction_data["type"],
                impact_score=interaction_data["impact"],
                effect_type=interaction_data["effect"],
                recommendation=interaction_data["recommendation"],
                evidence=["domain_interaction_matrix"]
            )
        
        # Default neutral interaction
        return GoalInteraction(
            source_domain=domain1,
            target_domain=domain2,
            interaction_type="neutral",
            impact_score=0.1,
            effect_type="neutral",
            recommendation=f"Monitor how {domain1} and {domain2} goals affect each other.",
            evidence=["default_analysis"]
        )