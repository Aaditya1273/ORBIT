"""
ORBIT Pattern Analyzer
Advanced behavioral pattern analysis for personalized interventions
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import structlog

logger = structlog.get_logger(__name__)


@dataclass
class BehavioralPattern:
    """Identified behavioral pattern"""
    pattern_type: str  # temporal, compliance, energy, failure, success
    description: str
    confidence: float  # 0.0 to 1.0
    frequency: float  # How often this pattern occurs
    impact_score: float  # Impact on goal achievement
    supporting_data: Dict[str, Any]
    actionable_insights: List[str]


@dataclass
class UserInsight:
    """Actionable insight about user behavior"""
    insight_type: str  # optimization, warning, opportunity
    title: str
    description: str
    confidence: float
    potential_impact: float
    recommended_actions: List[str]
    supporting_patterns: List[BehavioralPattern]


class PatternAnalyzer:
    """
    Advanced pattern analysis engine that identifies behavioral patterns
    and generates actionable insights for intervention optimization
    """
    
    def __init__(self):
        self.pattern_cache = {}
        self.insight_cache = {}
        
        logger.info("Pattern Analyzer initialized")
    
    async def analyze_user_patterns(
        self,
        user_id: str,
        interventions: List[Dict[str, Any]],
        goals: List[Dict[str, Any]],
        context_history: List[Dict[str, Any]],
        time_window_days: int = 30
    ) -> Dict[str, Any]:
        """
        Comprehensive analysis of user behavioral patterns
        """
        logger.info(
            "Starting pattern analysis",
            user_id=user_id,
            interventions_count=len(interventions),
            goals_count=len(goals),
            time_window_days=time_window_days
        )
        
        # Convert data to analysis format
        df_interventions = self._prepare_intervention_data(interventions)
        df_goals = self._prepare_goal_data(goals)
        df_context = self._prepare_context_data(context_history)
        
        # Analyze different pattern types
        patterns = []
        
        # 1. Temporal patterns
        temporal_patterns = await self._analyze_temporal_patterns(df_interventions, df_context)
        patterns.extend(temporal_patterns)
        
        # 2. Compliance patterns
        compliance_patterns = await self._analyze_compliance_patterns(df_interventions, df_goals)
        patterns.extend(compliance_patterns)
        
        # 3. Energy and mood patterns
        energy_patterns = await self._analyze_energy_patterns(df_interventions, df_context)
        patterns.extend(energy_patterns)
        
        # 4. Success and failure patterns
        success_patterns = await self._analyze_success_failure_patterns(df_interventions, df_goals)
        patterns.extend(success_patterns)
        
        # 5. Cross-domain patterns
        crosn_patterns(df_interventions, df_goals)
        patterns.extend(cross_domain_patterns)
        
        # Generate actionable insights
        insights = await self._generate_insights(patterns, user_id)
        
        # Calculate overall behavioral profile
        behavioral_profile = await self._create_behavioral_profile(patterns, insights)
        
        analysis_result = {
            "user_id": user_id,
            "analysis_timestamp": datetime.utcnow().isoformat(),
            "ndow_days,
            "patterns": [pattern.__dict__ for pattern in patterns],
            "insights": [insight.__dict__ for insight in insights],
            "behavioral_profile": behavioral_profile,
            "recommendations": await self._generate_recommendations(insights),
            "confidence_score": np.mean([pattern.confidence for pattern in patterns]) if patterns else 0.5
        }
        
        # Cache results
        self.pattern_cache[user_id] = analysis_result
        
        logger.info(
            "Pattern analysis completed",
            user_id=user_id,
            patterns_found=len(patterns),
            insights_generated=len(insights),
            confidence_score=analysis_result["confidence_score"]
        )
        
        return analysis_result
    
    async def _analyze_temporal_patterns(
        self,
        df_interventions: pd.DataFrame,
        df_context: pd.DataFrame
    ) -> List[BehavioralPattern]:
        """
        Analyze temporal patterns in user behavior
        """
        patterns = []
        
        if df_interventions.empty:
            return patterns
        
        # Hour of day patterns
        hourly_compliance = df_interventions.groupby('hour')['complied'].mean()
        
        # Find peak performance hours
        if len(hourly_compliance) > 0:
            peak_hours = hourly_compliance.nlargest(3).index.tolist()
            low_hours = hourly_compliance.nsmallest(3).index.tolist()
            
            if hourly_compliance.max() - hourly_compliance.min() > 0.2:  # Significant difference
                patterns.append(BehavioralPattern(
                    pattern_type="temporal",
                    description=f"Peak performance hours: {peak_hours}, Low performance: {low_hours}",
                    confidence=0.8,
                    frequency=1.0,  # Daily pattern
                    impact_score=0.7,
                    supporting_data={
                        "peak_hours": peak_hours,
                        "low_hours": low_hours,
                        "hourly_compliance": hourly_compliance.to_dict()
                    },
                    actionable_insights=[
                        f"Schedule important interventions during {peak_hours}",
                        f"Avoid or modify interventions during {low_hours}",
                        "Use time-based intervention scheduling"
                    ]
                ))
        
        # Day of week patterns
        if 'day_of_week' in df_interventions.columns:
            weekly_compliance = df_interventions.groupby('day_of_week')['complied'].mean()
            
            if len(weekly_compliance) > 0:
                best_days = weekly_compliance.nlargest(2).index.tolist()
                worst_days = weekly_compliance.nsmallest(2).index.tolist()
                
                if weekly_compliance.max() - weekly_compliance.min() > 0.15:
                    patterns.append(BehavioralPattern(
                        pattern_type="temporal",
                        description=f"Bestng days: {worst_days}",
                        confidence=0.7,
                        frequency=1.0,  # Weekly pattern
                        impact_score=0.6,
                        supporting_data={
                            "best_days": best_days,
                            "worst_days": worst_days,
                            "weekly_compliance": weekly_compliance.to_dict()
                        },
                        actionable_insights=[
                            f"Focus on builtum on {best_days}",
                            f"Provide extra support on {worst_days}",
                            "Adjust intervention frequency based on day of week"
                        ]
                    ))
        
        return patterns
    
    async def _analyze_compliance_patterns(
        self,
        df_interventions: pd.DataFrame,
        df_goals: pd.DataFrame
    ) -> List[BehavioralPattern]:
        """
        Analyze compliance patterns across different dimensions
        """
        patterns = []
        
        if df_interventions.empty:
            return patterns
        
        # Domain-specific compliance
        if 'domain' in df_interventions.columns:
            domain_compliance = df_interventions.groupby('domain')['complied'].agg(['mean', 'count'])
            domain_compliance = domain_compliance[domain_compliance['count'] >= 3]  # Minimum sample size
            
            if not domain_compliance.empty:
                best_domain = domain_compliance['mean']()
                worst_domain = domain_compliance['mean'].idxmin()
                
                if domain_compliance['mean'].max() - domain_compliance['mean'].min() > 0.2:
                    patterns.append(BehavioralPattern(
                        pattern_type="compliance",
                        description=f"Highest compliance in {best_domain} ({domain_compliance.loc[best_domain, 'mean']:.1%}), lowest in {worst_domain} ({domain_compliance.loc[worst_domain, 'mean']:.1%})",
    onfidence=0.8,
                        frequency=0.8,
                        impact_score=0.8,
                        supporting_data={
                            "domain_compliance": domain_compliance.to_dict(),
                            "best_domain": best_domain,
                            "worst_domain": worst_domain
                        },
                        actionable_insights=[
                            f"Leverage success strategies from {best_domain} for other domains",
                            f"Investigate barriers in {worst_domain}",
                            "Consider domain-specific intervention approaches"
                        ]
                    ))
        
        # Intervention type compliance
        if 'intervention_type' in df_interventions.columns:
            type_compliance = df_interventions.groupby('intervention_type')['complied'].agg(['mean', 'count'])
            type_compliance = type_compliance[type_compliance['count'] >= 3]
            
            if not type_copliance.empty:
                best_type = type_compliance['mean'].idxmax()
                worst_type = type_compliance['mean'].idxmin()
                
                patterns.append(BehavioralPattern(
                    pattern_type="compliance",
                    description=f"Most effective intervention type: {best_type}, least effective: {worst_type}",
                    confidence=0.7,
                    frequency=0.6,
                    impact_score=0.7,
                    supporting_data={
                        "type_compliance": type_compliance.to_dict(),
                        "best_type": best_type,
                        "worst_type": worst_type
                    },
                    actionable_insights=[
                        f"Increase use of {best_type} interventions",
                        f"Modify or reduce {worst_type} interventions",
                        "Personalize intervention types based on effectiveness"
                    ]
                ))
        
        return patterns
    
    async def _analyze_energy_patterns(
        self,
        df_interventions: pd.DataFrame,
        df_context: pd.DataFrame
    ) -> List[BehavioralPattern]:
        """
        Analyze energy and mood patterns
        """
        patterns = []
        
        # This would analyze energy levels, stress indicators, etc.
        # For now, create a sample pattern
        if not df_interventions.empty:
            # Analyze compliance vs time since last intervention
            df_intervens['hours_since_last'] = df_interventions['timestamp'].diff().dt.total_seconds() / 3600
            
            # Find optimal intervention frequency
            if 'hours_since_last' in df_interventions.columns:
                # Group by intervention frequency and analyze compliance
                df_interventions['frequency_bucket'] = pd.cut(
                    df_interventions['hours_since_last'].fillna(24), 
                    bins=[0, 2, 6, 12, 24, 48, float('inf')],
                h', '2-6h', '6-12h', '12-24h', '24-48h', '>48h']
                )
                
                frequency_compliance = df_interventions.groupby('frequency_bucket')['complied'].mean()
                
                if len(frequency_compliance) > 0:
                    optimal_frequency = frequency_compliance.idxmax()
                    
                    patterns.append(BehavioralPattern(
                        pattern_type="energy",
                        description=f"Op{optimal_frequency}",
                        confidence=0.6,
                        frequency=0.7,
                        impact_score=0.5,
                        supporting_data={
                            "frequency_compliance": frequency_compliance.to_dict(),
                            "optimal_frequency": optimal_frequency
                        },
                        actionable_insights=[
                            f"Space interventions approximately {optimal_frequency} apart",
                            "Avoid intervention fatigue with appropriate timing",
                            "Monitor user energy levels for optimal timing"
                        ]
                    ))
        
        return patterns
    
    async def _analyze_success_failure_patterns(
        self,
        df_interventions: pd.DataFrame,
        df_goals: pd.DataFrame
    ) -> List[BehavioralPattern]:
        """
        Analyze patterns in success and failure
        """
        patterns = []
        
        if df_interventions.empty:
            return patterns
        
        # Analyze streaks
        df_interventions = df_interventions.sort_values('timestamp')
        df_interventions['compliance_streak'] = (
            df_interventions['complied'] != df_interventions['complied'].shift()
        ).cumsum()
        
        # Calculate streak lengths
        streak_lengths = df_interventions.groupby(['compliance_streak', 'complied']).size()
        
        if len(streak_lengths) > 0:
            success_streaks = strlengths[streak_lengths.index.get_level_values(1) == True]
            failure_streaks = streak_lengths[streak_lengths.index.get_level_values(1) == False]
            
            if len(success_streaks) > 0:
                avg_success_streak = success_streaks.mean()
                max_success_streak = success_streaks.max()
                
                patterns.append(BehavioralPattern(
                    pattern_type="success",
                    description=f"Average success streak: {k:.1f}, Maximum: {max_success_streak}",
                    confidence=0.7,
                    frequency=0.5,
                    impact_score=0.8,
                    supporting_data={
                        "avg_success_streak": avg_success_streak,
                        "max_success_streak": max_success_streak,
                        "success_streaks": success_streaks.tolist()
                    },
                    actionable_insights=[
                        "Celebrate and reinforce success streaks",
                        "Identify factors that contribute to longer streaks",
                        "Use streak momentum for challenging goals"
                    ]
                ))
            
            if len(failure_streaks) > 0:
                avg_failure_streak = failure_streaks.mean()
                
                if avg_failure_streak > 2:  # Concerning pattern
                    patterns.append(BehavioralPattern(
                        pattern_type="failure",
                        description=f"Average failure streak: {avg_failure_streak:.1f} - needs intervention",
                        confidence=0.8,
                        frequency=0.4,
                        impact_score=0.9,
                        supporting_data={
                            "avg_failure_streak": avg_failure_streak,
                            "failure_streaks": failure_streaks.tolist()
                        },
                        actionable_insights=[
                          strategies",
                            "Reduce intervention difficulty during failure streaks",
                            "Provide additional support and motivation"
                        ]
                    ))
        
        return patterns
    
    async def _analyze_cross_domain_patterns(
        self,
        df_interventions: pd.DataFrame,
        df_goals: pd.DataFrame
    ) -> List[BehavioralPattern]:
        """
        Analyze patterns across different goal domains
        """
        patterns = []
        
        if df_interventions.empty or 'domain' not in df_interventions.columns:
            return patterns
        
        # Analyze domain interaction effects
        domains = df_interventions['domain'].unique()
        
        if len(domains) > 1:
            # Calculate correlation between domain compliance rates
            domain_daily_compliance = df_interventions.groupby(['date', 'domain'])['complied'].mean().unstack(fill_value=0)
            
            if len(domain_daily_compliance) > 5:  # Need sufficient data
                correlation_matrix = domain_daily_compliance.corr()
                
                # Find strong correlations
                strong_correlations = []
                for i in range(len(correlation_matrix.columns)):
                    for j in range(i+1, len(correlation_matrix.columns)):
                        corr = correlation_matrix.iloc[i, j]
                        if abs(corr) > 0.5:  # Strong correlation
                      tion_matrix.columns[i]
                            domain2 = correlation_matrix.columns[j]
                            strong_correlations.append((domain1, domain2, corr))
                
                if strong_correlations:
                    for domain1, domain2, corr in strong_correlations:
                        correlation_type = "positive" if corr > 0 else "negative"
                        
                        patterns.append(BehavioralPattern(
                            pattern_type="cross_domain",
                            description=f"{correlation_type.title()} correlation between {domain1} and {domain2} ({corr:.2f})",
                            confidence=0.6,
                            frequency=0.8,
                            impact_score=0.6,
                            supporting_data={
                                "domain1": domain1,
                                "domain2": domain2,
                                "correlation": corr,
                                "corretype": correlation_type
                            },
                            actionable_insights=[
                                f"Success in {domain1} {'supports' if corr > 0 else 'may interfere with'} {domain2}",
                                "Consider cross-domain intervention strategies",
                                "Optimize goal scheduling based on domain interactions"
                            ]
                        ))
        
        return patterns
    
    async def _generate_ins(
        self,
        patterns: List[BehavioralPattern],
        user_id: str
    ) -> List[UserInsight]:
        """
        Generate actionable insights from identified patterns
        """
        insights = []
        
        # Group patterns by type for insight generation
        pattern_groups = defaultdict(list)
        for pattern in patterns:
            pattern_groups[pattern.pattern_type].append(pattern)
        
        # Generate insights for each pattern type
        atterns in pattern_groups.items():
            if pattern_type == "temporal":
                insights.extend(await self._generate_temporal_insights(type_patterns))
            elif pattern_type == "compliance":
                insights.extend(await self._generate_compliance_insights(type_patterns))
            elif pattern_type == "success":
                insights.extend(await self._generate_success_insights(type_patterns))
            elif pattern_type == "failure":
                f._generate_failure_insights(type_patterns))
            elif pattern_type == "cross_domain":
                insights.extend(await self._generate_cross_domain_insights(type_patterns))
        
        # Generate meta-insights from pattern combinations
        meta_insights = await self._generate_meta_insights(patterns)
        insights.extend(meta_insights)
        
        return insights
    
    async def _generate_temporal_insights(self, patterns: List[BehavioralPattern]) -> List[UserInsight]:
        """Generate insights from temporal patterns"""
        insights = []
        
        for pattern in patterns:
            if "Peak performance hours" in pattern.description:
                peak_hours = pattern.supporting_data.get("peak_hours", [])
                
                insights.append(UserInsight(
                    insight_type="optimization",
                    title="Optimize Intervention Timing",
            . Scheduling important tasks during these hours could improve success rates by up to 30%.",
                    confidence=pattern.confidence,
                    potential_impact=0.8,
                    recommended_actions=[
                        f"Schedule high-priority interventions during {peak_hours}",
                        "Set up automatic intervention scheduling",
                        "Use calendar blocking for peak performance hours"
                    ],
        s=[pattern]
                ))
        
        return insights
    
    async def _generate_compliance_insights(self, patterns: List[BehavioralPattern]) -> List[UserInsight]:
        """Generate insights from compliance patterns"""
        insights = []
        
        for pattern in patterns:
            if "Highest compliance" in pattern.description:
                best_domain = pattern.supporting_data.get("best_domain")
                worst_domain = pattern.supporting_data.get("worst_domain")
                
                insights.append(UserInsight(
                    insight_type="optimization",
                    title="Leverage Domain Strengths",
                    description=f"Your success in {best_domain} can be applied to improve {worst_domain} performance. Cross-domain strategy transfer could boost overall success rates.",
                    confidence=pattern.confidence,
                    potential_impact=0.7,
                    recommended_actions=[
                        f"Apply successful {best_domain} strategies to {worst_domain}",
                        "Identify specific success factors for replication",
                        "Create cross-domain goal connections"
                    ],
                    supporting_patterns=[pattern]
                ))
        
        return insights
    
    async def _generate_failure_insights(self, patterns: List[BehavioralPattern]) -> List[UserInsight]:
        """Generate insights from failure patterns"""
        insights = []
        
        for pattern in patterns:
            if "failure streak" in pattern.description:
                avg_failure_streak = pattern.supporting_data.get("avg_failure_streak", 0)
                
                if avg_failure_streak > 2:
                    insights.append(UserInsight(
                        insight_type="warning",
                        title="Failure Recovery Strategy Needed",
                        description=f"Yourer recovery strategies. Early intervention during setbacks could prevent longer failure periods.",
                        confidence=pattern.confidence,
                        potential_impact=0.9,
                        recommended_actions=[
                            "Implement immediate failure recovery protocols",
                            "Reduce intervention difficulty after failures",
                            "Add motivational support during challenging periods",
                            "Create accountability partnerships"
                        ],
                        supporting_patterns=[pattern]
                    ))
        
        return insights
    
    async def _generate_success_insights(self, patterns: List[BehavioralPattern]) -> List[UserInsight]:
        """Generate insights from success patterns"""
        insights = []
        
        for pattern in patterns:
            if "success streak" in pattern.description:
                max_streak = px_success_streak", 0)
                
                insights.append(UserInsight(
                    insight_type="opportunity",
                    title="Build on Success Momentum",
                    description=f"Your maximum success streak of {max_streak} shows you can maintain consistency. Identifying and replicating the conditions that led to this streak could significantly improve your overall performance.",
                    confidence=pattern.confidence,
                    potential_impact=0.8,
                    recommended_actions=[
                        "Analyze factors contributing to your longest success streak",
                        "Create conditions that support sustained success",
                        "Use streak momentum to tackle challenging goals",
                        "Celebrate and reinforce successful patterns"
                    ],
                    supporting_patterns=[pattern]
                ))
        
        return insights
    
    async def _generate_cross_domain_insights(self, patterns: List[BehavioralPattern]) -> List[UserInsight]:
        """Generate insights from cross-domain patterns"""
        insights = []
        
        for pattern in patterns:
            if "correlation between" in pattern.description:
                domain1 = pattern.supporting_data.get("domain1")
                domain2 = pattern.supporting_data.get("domain2")
                correlation = pattern.supporting_data.get("correlation", 0)
                
                if correlatio5:
                    insights.append(UserInsight(
                        insight_type="optimization",
                        title="Leverage Domain Synergies",
                        description=f"Strong positive correlation between {domain1} and {domain2} suggests these goals support each other. Coordinating efforts in these domains could amplify your success.",
                        confidence=pattern.confidence,
                        potential_impact=0.7,
                        recommended_actions=[
                            f"Schedule {domain1} and {domain2} activities together",
                            "Create combined interventions for both domains",
                            "Use success in one domain to motivate the other"
                        ],
                        supporting_patterns=[pattern]
                    ))
                elif correlation < -0.5:
                    insights.append(UserInsight(
                        insight_type="warning",
                        title="Manage Domain Conflicts",
                        description=f"Negative correlation between {domain1} and {domain2} suggests potential conflict. Better scheduling and resource allocation could prevent interference between these goals.",
                        confidence=pattern.confidence,
                        potential_impact=0.6,
                        recommended_actions=[
                            f"Separate {domain1} and {domain2} activities in time",
            resources for each domain",
                            "Monitor for signs of goal conflict"
                        ],
                        supporting_patterns=[pattern]
                    ))
        
        return insights
    
    async def _generate_meta_insights(self, patterns: List[BehavioralPattern]) -> List[UserInsight]:
        """Generate meta-insights from pattern combinations"""
        insights = []
        
        # Overall pattern confidence
        avg_confidence = np.mean([p.r p in patterns]) if patterns else 0.5
        
        if avg_confidence > 0.8:
            insights.append(UserInsight(
                insight_type="optimization",
                title="Strong Behavioral Patterns Identified",
                description=f"Your behavioral patterns are highly predictable (confidence: {avg_confidence:.1%}). This enables precise intervention timing and personalization for maximum effectiveness.",
                confidence=avg_confidence,
                potential_impa,
                recommended_actions=[
                    "Enable advanced personalization features",
                    "Use predictive intervention scheduling",
                    "Implement pattern-based goal recommendations"
                ],
                supporting_patterns=patterns
            ))
        elif avg_confidence < 0.4:
            insights.append(UserInsight(
                insight_type="warning",
                title="Inconsistent Behavioral Patterns",
                f"Your behavioral patterns show high variability (confidence: {avg_confidence:.1%}). More data collection and flexible intervention strategies may be needed.",
                confidence=avg_confidence,
                potential_impact=0.6,
                recommended_actions=[
                    "Increase intervention frequency for better data",
                    "Use adaptive intervention strategies",
                    "Focus on building consistent routines"
                ],
           g_patterns=patterns
            ))
        
        return insights
    
    async def _create_behavioral_profile(
        self,
        patterns: List[BehavioralPattern],
        insights: List[UserInsight]
    ) -> Dict[str, Any]:
        """
        Create comprehensive behavioral profile
        """
        profile = {
            "pattern_strength": np.mean([p.confidence for p in patterns]) if patterns else 0.5,
            "behavioral_consistency": self._calculate_consistency_score(patterns),
    optimization_potential": np.mean([i.potential_impact for i in insights]) if insights else 0.5,
            "primary_success_factors": self._extract_success_factors(patterns),
            "primary_challenges": self._extract_challenges(patterns),
            "recommended_intervention_style": self._recommend_intervention_style(patterns, insights),
            "optimal_intervention_frequency": self._recommend_intervention_frequency(patterns),
            "personalization_level": medium" if len(patterns) > 2 else "low"
        }
        
        return profile
    
    def _calculate_consistency_score(self, patterns: List[BehavioralPattern]) -> float:
        """Calculate behavioral consistency score"""
        if not patterns:
            return 0.5
        
        # Higher frequency patterns indicate more consistent behavior
        frequency_scores = [p.frequency for p in patterns]
        return np.mean(frequency_scores)
    
    def _extract_success_factors(self,havioralPattern]) -> List[str]:
        """Extract key success factors from patterns"""
        success_factors = []
        
        for pattern in patterns:
            if pattern.pattern_type == "success" or pattern.impact_score > 0.7:
                success_factors.extend(pattern.actionable_insights[:2])
        
        return list(set(success_factors))[:5]  # Top 5 unique factors
    
    def _extract_challenges(self, patterns: List[BehavioralPattern]) -> List[str]:
        """Extract key challenges from patterns"""
        challenges = []
        
        for pattern in patterns:
            if pattern.pattern_type == "failure" or "low" in pattern.description.lower():
                challenges.append(pattern.description)
        
        return challenges[:3]  # Top 3 challenges
    
    def _recommend_intervention_style(
        self,
        patterns: List[BehavioralPattern],
        insights: List[UserInsight]
    ) -> str:
        """Recommend intervention style based on patterns"""
        
        # Count pattern types
        pattern_types = [p.pattern_type for p in patterns]
        
        if pattern_types.count("failure") > pattern_types.count("success"):
            return "supportive"  # More support needed
        elif pattern_types.count("temporal") > 2:
            return "scheduled"  # Time-based interventions work well
        elif any("compliance" in p.pattern_type for p in patterns):
            return "adaptive"  # Need flexible approaches
        else:
            return "motivati  # Standard motivational approach
    
    def _recommend_intervention_frequency(self, patterns: List[BehavioralPattern]) -> str:
        """Recommend intervention frequency based on patterns"""
        
        # Look for energy/frequency patterns
        for pattern in patterns:
            if "frequency" in pattern.description.lower():
                optimal_freq = pattern.supporting_data.get("optimal_frequency", "12-24h")
                return optimal_freq
        
        # Default based on pattern stngth
        avg_confidence = np.mean([p.confidence for p in patterns]) if patterns else 0.5
        
        if avg_confidence > 0.8:
            return "12-24h"  # Can handle regular interventions
        elif avg_confidence > 0.6:
            return "24-48h"  # Moderate frequency
        else:
            return "48h+"  # Lower frequency to avoid overwhelm
          = pd.DataFrame(context_history)
        
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        return df       df['complied'] = False
        
        return df
    
    def _prepare_goal_data(self, goals: List[Dict[str, Any]]) -> pd.DataFrame:
        """Prepare goal data for analysis"""
        if not goals:
            return pd.DataFrame()
        
        return pd.DataFrame(goals)
    
    def _prepare_context_data(self, context_history: List[Dict[str, Any]]) -> pd.DataFrame:
        """Prepare context data for analysis"""
        if not context_history:
            return pd.DataFrame()
        
        dfions)
        
        # Ensure required columns exist
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['hour'] = df['timestamp'].dt.hour
            df['day_of_week'] = df['timestamp'].dt.day_name()
            df['date'] = df['timestamp'].dt.date
        
        # Ensure compliance column exists
        if 'user_complied' in df.columns:
            df['complied'] = df['user_complied'].fillna(False)
        elif 'complied' not in df.columns:
     []
        seen = set()
        for rec in recommendations:
            if rec not in seen:
                unique_recommendations.append(rec)
                seen.add(rec)
        
        return unique_recommendations[:10]  # Top 10 recommendations
    
    def _prepare_intervention_data(self, interventions: List[Dict[str, Any]]) -> pd.DataFrame:
        """Prepare intervention data for analysis"""
        if not interventions:
            return pd.DataFrame()
        
        df = pd.DataFrame(intervent
        # Prioritize by potential impact and confidence
        prioritized_insights = sorted(
            insights,
            key=lambda x: x.potential_impact * x.confidence,
            reverse=True
        )
        
        recommendations = []
        for insight in prioritized_insights[:5]:  # Top 5 insights
            recommendations.extend(insight.recommended_actions[:2])  # Top 2 actions per insight
        
        # Remove duplicates while preserving order
        unique_recommendations =
    async def _generate_recommendations(self, insights: List[UserInsight]) -> List[str]:
        """Generate top recommendations from insights"""
    