"""
ORBIT Optimizer Agent - Continuous Learning and Improvement
Analyzes patterns, optimizes strategies, and improves system performance
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import structlog

from .base_agent import BaseAgent, AgentResponse, AgentContext
from ..core.config import settings
from ..database.models import OpikTrace, Intervention, User, Goal

logger = structlog.get_logger(__name__)


@dataclass
class OptimizationInsight:
    """Individual optimization insight"""
    insight_type: str  # pattern, failure_mode, improvement_opportunity
    description: str
    confidence: float
    impact_score: float  # Estimated impact on user success
    actionable_steps: List[str]
    affected_users: int
    supporting_data: Dict[str, Any]


@dataclass
class OptimizationReport:
    """Complete optimization analysis report"""
    analysis_period: Tuple[datetime, datetime]
    total_traces_analyzed: int
    insights: List[OptimizationInsight]
    performance_trends: Dict[str, Any]
    recommended_actions: List[str]
    a_b_test_results: List[Dict[str, Any]]
    model_performance: Dict[str, Any]
    user_satisfaction_trends: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "analysis_period": {
                "start": self.analysis_period[0].isoformat(),
                "end": self.analysis_period[1].isoformat()
            },
            "total_traces_analyzed": self.total_traces_analyzed,
            "insights": [
                {
                    "type": insight.insight_type,
                    "description": insight.description,
                    "confidence": insight.confidence,
                    "impact_score": insight.impact_score,
                    "actionable_steps": insight.actionable_steps,
                    "affected_users": insight.affected_users
                }
                for insight in self.insights
            ],
            "performance_trends": self.performance_trends,
            "recommended_actions": self.recommended_actions,
            "a_b_test_results": self.a_b_test_results,
            "model_performance": self.model_performance,
            "user_satisfaction_trends": self.user_satisfaction_trends
        }


class OptimizerAgent(BaseAgent):
    """
    The Optimizer Agent continuously learns from system performance and user feedback
    to improve intervention quality, timing, and effectiveness.
    
    Key Responsibilities:
    1. Analyze Opik traces for patterns and insights
    2. Identify failure modes and improvement opportunities
    3. Run A/B tests on intervention strategies
    4. Optimize model prompts and parameters
    5. Generate actionable recommendations for system improvement
    """
    
    def __init__(self, **kwargs):
        super().__init__(agent_type="optimizer", **kwargs)
        
        # Analysis components
        self.pattern_analyzer = PatternAnalyzer()
        self.ab_tester = ABTester()
        self.prompt_optimizer = PromptOptimizer()
        
        # Optimization history
        self.optimization_history: List[OptimizationReport] = []
        
        # Performance tracking
        self.baseline_metrics = {}
        self.current_metrics = {}
        
        logger.info("Optimizer Agent initialized")
    
    async def _execute_internal(
        self,
        context: AgentContext,
        user_input: str,
        analysis_type: str = "weekly",
        **kwargs
    ) -> AgentResponse:
        """
        Execute optimization analysis based on the requested type
        """
        try:
            if analysis_type == "weekly":
                report = await self.weekly_optimization_analysis()
            elif analysis_type == "monthly":
                report = await self.monthly_deep_analysis()
            elif analysis_type == "real_time":
                report = await self.real_time_optimization()
            elif analysis_type == "ab_test":
                report = await self.analyze_ab_test_results()
            else:
                report = await self.custom_analysis(user_input, **kwargs)
            
            # Store optimization report
            self.optimization_history.append(report)
            
            # Generate response
            response_content = self._format_optimization_response(report)
            
            return AgentResponse(
                content=response_content,
                reasoning=f"Completed {analysis_type} optimization analysis",
                confidence=0.9,
                metadata={
                    "analysis_type": analysis_type,
                    "insights_count": len(report.insights),
                    "traces_analyzed": report.total_traces_analyzed,
                    "report": report.to_dict()
                }
            )
            
        except Exception as e:
            logger.error(
                "Optimizer agent execution failed",
                error=str(e),
                analysis_type=analysis_type,
                exc_info=True
            )
            
            return AgentResponse(
                content=f"Optimization analysis failed: {str(e)}",
                reasoning="Error occurred during optimization analysis",
                confidence=0.0,
                metadata={"error": True, "error_message": str(e)}
            )
    
    async def weekly_optimization_analysis(self) -> OptimizationReport:
        """
        Comprehensive weekly analysis of system performance and optimization opportunities
        """
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=7)
        
        logger.info(
            "Starting weekly optimization analysis",
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat()
        )
        
        # Fetch data for analysis
        traces = await self._fetch_opik_traces(start_date, end_date)
        interventions = await self._fetch_interventions(start_date, end_date)
        user_feedback = await self._fetch_user_feedback(start_date, end_date)
        
        # Perform various analyses
        insights = []
        
        # 1. Pattern Analysis
        pattern_insights = await self.pattern_analyzer.analyze_intervention_patterns(
            traces, interventions, user_feedback
        )
        insights.extend(pattern_insights)
        
        # 2. Failure Mode Analysis
        failure_insights = await self._analyze_failure_modes(traces, interventions)
        insights.extend(failure_insights)
        
        # 3. Performance Trend Analysis
        performance_trends = await self._analyze_performance_trends(traces)
        
        # 4. User Satisfaction Analysis
        satisfaction_trends = await self._analyze_user_satisfaction(user_feedback)
        
        # 5. Model Performance Analysis
        model_performance = await self._analyze_model_performance(traces)
        
        # 6. A/B Test Results
        ab_test_results = await self.ab_tester.get_recent_results()
        
        # Generate recommendations
        recommended_actions = await self._generate_recommendations(
            insights, performance_trends, satisfaction_trends
        )
        
        report = OptimizationReport(
            analysis_period=(start_date, end_date),
            total_traces_analyzed=len(traces),
            insights=insights,
            performance_trends=performance_trends,
            recommended_actions=recommended_actions,
            a_b_test_results=ab_test_results,
            model_performance=model_performance,
            user_satisfaction_trends=satisfaction_trends
        )
        
        logger.info(
            "Weekly optimization analysis completed",
            insights_count=len(insights),
            traces_analyzed=len(traces),
            recommendations_count=len(recommended_actions)
        )
        
        return report
    
    async def _analyze_failure_modes(
        self,
        traces: List[OpikTrace],
        interventions: List[Intervention]
    ) -> List[OptimizationInsight]:
        """
        Analyze common failure modes and their root causes
        """
        insights = []
        
        # Group traces by failure type
        low_safety_traces = [t for t in traces if t.safety_score and t.safety_score < 0.8]
        low_relevance_traces = [t for t in traces if t.relevance_score and t.relevance_score < 0.7]
        low_compliance_interventions = [i for i in interventions if i.user_complied is False]
        
        # Analyze low safety scores
        if len(low_safety_traces) > len(traces) * 0.05:  # More than 5% have safety issues
            safety_insight = await self._analyze_safety_failures(low_safety_traces)
            insights.append(safety_insight)
        
        # Analyze low relevance scores
        if len(low_relevance_traces) > len(traces) * 0.1:  # More than 10% have relevance issues
            relevance_insight = await self._analyze_relevance_failures(low_relevance_traces)
            insights.append(relevance_insight)
        
        # Analyze low compliance rates
        if len(low_compliance_interventions) > len(interventions) * 0.3:  # More than 30% non-compliance
            compliance_insight = await self._analyze_compliance_failures(low_compliance_interventions)
            insights.append(compliance_insight)
        
        return insights
    
    async def _analyze_safety_failures(self, low_safety_traces: List[OpikTrace]) -> OptimizationInsight:
        """
        Analyze patterns in safety failures
        """
        # Analyze common patterns in low safety traces
        domains = [trace.input_data.get('domain', 'unknown') for trace in low_safety_traces]
        domain_counts = defaultdict(int)
        for domain in domains:
            domain_counts[domain] += 1
        
        most_problematic_domain = max(domain_counts, key=domain_counts.get)
        
        return OptimizationInsight(
            insight_type="failure_mode",
            description=f"Safety issues concentrated in {most_problematic_domain} domain ({domain_counts[most_problematic_domain]} incidents)",
            confidence=0.85,
            impact_score=0.9,  # High impact - safety is critical
            actionable_steps=[
                f"Review and strengthen safety guidelines for {most_problematic_domain} interventions",
                "Add domain-specific safety checks to Supervisor Agent",
                "Implement additional human review for high-risk interventions",
                "Update training data to include more safety examples"
            ],
            affected_users=len(set(trace.user_id for trace in low_safety_traces if trace.user_id)),
            supporting_data={
                "domain_breakdown": dict(domain_counts),
                "total_incidents": len(low_safety_traces),
                "average_safety_score": np.mean([t.safety_score for t in low_safety_traces])
            }
        )
    
    async def _analyze_performance_trends(self, traces: List[OpikTrace]) -> Dict[str, Any]:
        """
        Analyze performance trends over time
        """
        # Group traces by day
        daily_metrics = defaultdict(list)
        
        for trace in traces:
            day = trace.created_at.date()
            daily_metrics[day].append({
                'safety_score': trace.safety_score or 0,
                'relevance_score': trace.relevance_score or 0,
                'accuracy_score': trace.accuracy_score or 0,
                'overall_score': trace.overall_score or 0,
                'execution_time_ms': trace.execution_time_ms,
                'user_complied': trace.user_complied
            })
        
        # Calculate daily averages
        trends = {}
        for day, day_traces in daily_metrics.items():
            trends[day.isoformat()] = {
                'avg_safety_score': np.mean([t['safety_score'] for t in day_traces]),
                'avg_relevance_score': np.mean([t['relevance_score'] for t in day_traces]),
                'avg_accuracy_score': np.mean([t['accuracy_score'] for t in day_traces]),
                'avg_overall_score': np.mean([t['overall_score'] for t in day_traces]),
                'avg_execution_time': np.mean([t['execution_time_ms'] for t in day_traces]),
                'compliance_rate': np.mean([1 if t['user_complied'] else 0 for t in day_traces if t['user_complied'] is not None]),
                'total_interventions': len(day_traces)
            }
        
        # Calculate week-over-week changes
        sorted_days = sorted(trends.keys())
        if len(sorted_days) >= 7:
            recent_avg = np.mean([trends[day]['avg_overall_score'] for day in sorted_days[-3:]])
            previous_avg = np.mean([trends[day]['avg_overall_score'] for day in sorted_days[-7:-4]])
            week_over_week_change = (recent_avg - previous_avg) / previous_avg if previous_avg > 0 else 0
        else:
            week_over_week_change = 0
        
        return {
            'daily_trends': trends,
            'week_over_week_change': week_over_week_change,
            'trend_direction': 'improving' if week_over_week_change > 0.02 else 'declining' if week_over_week_change < -0.02 else 'stable'
        }
    
    async def _generate_recommendations(
        self,
        insights: List[OptimizationInsight],
        performance_trends: Dict[str, Any],
        satisfaction_trends: Dict[str, Any]
    ) -> List[str]:
        """
        Generate actionable recommendations based on analysis
        """
        recommendations = []
        
        # High-impact insights first
        high_impact_insights = [i for i in insights if i.impact_score > 0.7]
        for insight in high_impact_insights:
            recommendations.extend(insight.actionable_steps[:2])  # Top 2 actions per insight
        
        # Performance-based recommendations
        if performance_trends.get('trend_direction') == 'declining':
            recommendations.append("Investigate recent changes that may have caused performance decline")
            recommendations.append("Consider rolling back recent model updates if performance continues to decline")
        
        # Satisfaction-based recommendations
        if satisfaction_trends.get('average_rating', 3.5) < 3.5:
            recommendations.append("Focus on improving user experience and intervention relevance")
            recommendations.append("Conduct user interviews to understand satisfaction issues")
        
        # Remove duplicates and limit to top 10
        unique_recommendations = list(dict.fromkeys(recommendations))
        return unique_recommendations[:10]
    
    async def _fetch_opik_traces(self, start_date: datetime, end_date: datetime) -> List[OpikTrace]:
        """
        Fetch Opik traces for the specified time period
        """
        # This would typically query the database
        # For now, return mock data
        return []
    
    async def _fetch_interventions(self, start_date: datetime, end_date: datetime) -> List[Intervention]:
        """
        Fetch interventions for the specified time period
        """
        # This would typically query the database
        return []
    
    async def _fetch_user_feedback(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """
        Fetch user feedback for the specified time period
        """
        # This would typically query the database
        return []
    
    def _format_optimization_response(self, report: OptimizationReport) -> str:
        """
        Format the optimization report into a readable response
        """
        response_parts = [
            f"🔧 ORBIT Optimization Report",
            f"📅 Analysis Period: {report.analysis_period[0].strftime('%Y-%m-%d')} to {report.analysis_period[1].strftime('%Y-%m-%d')}",
            f"📊 Traces Analyzed: {report.total_traces_analyzed:,}",
            "",
            "🎯 Key Insights:",
        ]
        
        for i, insight in enumerate(report.insights[:5], 1):  # Top 5 insights
            response_parts.append(
                f"{i}. {insight.description} (Impact: {insight.impact_score:.1f}, Confidence: {insight.confidence:.1f})"
            )
        
        response_parts.extend([
            "",
            "📈 Performance Trends:",
            f"- Overall trend: {report.performance_trends.get('trend_direction', 'stable').title()}",
            f"- Week-over-week change: {report.performance_trends.get('week_over_week_change', 0):.1%}",
            "",
            "🎯 Top Recommendations:",
        ])
        
        for i, rec in enumerate(report.recommended_actions[:5], 1):
            response_parts.append(f"{i}. {rec}")
        
        if report.a_b_test_results:
            response_parts.extend([
                "",
                "🧪 A/B Test Results:",
                f"- Active tests: {len(report.a_b_test_results)}",
                "- See detailed results in metadata"
            ])
        
        return "\n".join(response_parts)


class PatternAnalyzer:
    """
    Analyzes patterns in user behavior and intervention effectiveness
    """
    
    async def analyze_intervention_patterns(
        self,
        traces: List[OpikTrace],
        interventions: List[Intervention],
        feedback: List[Dict[str, Any]]
    ) -> List[OptimizationInsight]:
        """
        Analyze patterns in intervention effectiveness
        """
        insights = []
        
        # Temporal patterns
        temporal_insight = await self._analyze_temporal_patterns(interventions)
        if temporal_insight:
            insights.append(temporal_insight)
        
        # Domain-specific patterns
        domain_insight = await self._analyze_domain_patterns(interventions, feedback)
        if domain_insight:
            insights.append(domain_insight)
        
        # User segment patterns
        segment_insight = await self._analyze_user_segment_patterns(interventions, feedback)
        if segment_insight:
            insights.append(segment_insight)
        
        return insights
    
    async def _analyze_temporal_patterns(self, interventions: List[Intervention]) -> Optional[OptimizationInsight]:
        """
        Analyze temporal patterns in intervention effectiveness
        """
        if not interventions:
            return None
        
        # Group by hour of day
        hourly_effectiveness = defaultdict(list)
        
        for intervention in interventions:
            if intervention.delivered_at and intervention.user_rating:
                hour = intervention.delivered_at.hour
                hourly_effectiveness[hour].append(intervention.user_rating)
        
        # Find best and worst hours
        hourly_averages = {
            hour: np.mean(ratings) 
            for hour, ratings in hourly_effectiveness.items() 
            if len(ratings) >= 5  # Minimum sample size
        }
        
        if not hourly_averages:
            return None
        
        best_hour = max(hourly_averages, key=hourly_averages.get)
        worst_hour = min(hourly_averages, key=hourly_averages.get)
        
        if hourly_averages[best_hour] - hourly_averages[worst_hour] > 0.5:  # Significant difference
            return OptimizationInsight(
                insight_type="pattern",
                description=f"Interventions at {best_hour}:00 are {hourly_averages[best_hour]:.1f}/5 vs {hourly_averages[worst_hour]:.1f}/5 at {worst_hour}:00",
                confidence=0.8,
                impact_score=0.6,
                actionable_steps=[
                    f"Schedule more interventions around {best_hour}:00",
                    f"Reduce or modify interventions around {worst_hour}:00",
                    "Implement time-based intervention scheduling"
                ],
                affected_users=len(set(i.user_id for i in interventions)),
                supporting_data={
                    "hourly_averages": hourly_averages,
                    "best_hour": best_hour,
                    "worst_hour": worst_hour
                }
            )
        
        return None


class ABTester:
    """
    Manages A/B tests for intervention strategies
    """
    
    def __init__(self):
        self.active_tests = {}
        self.completed_tests = []
    
    async def get_recent_results(self) -> List[Dict[str, Any]]:
        """
        Get recent A/B test results
        """
        # Mock A/B test results
        return [
            {
                "test_name": "intervention_tone_test",
                "status": "completed",
                "variant_a": {"name": "motivational", "conversion_rate": 0.72, "sample_size": 1000},
                "variant_b": {"name": "practical", "conversion_rate": 0.78, "sample_size": 1000},
                "winner": "variant_b",
                "confidence": 0.95,
                "lift": 0.083
            }
        ]


class PromptOptimizer:
    """
    Optimizes AI model prompts based on performance data
    """
    
    async def optimize_prompts(self, performance_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Generate optimized prompts based on performance analysis
        """
        # This would use techniques like:
        # - Genetic algorithms for prompt evolution
        # - Reinforcement learning from human feedback
        # - A/B testing of prompt variations
        
        return {
            "worker_prompt_v2": "Enhanced prompt with better behavioral science integration...",
            "supervisor_prompt_v2": "Improved evaluation criteria based on user feedback..."
        }