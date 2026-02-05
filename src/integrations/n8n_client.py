"""
ORBIT n8n Integration Client
Manages workflow automation and external service orchestration
"""

import asyncio
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import httpx
import structlog

from ..core.config import settings

logger = structlog.get_logger(__name__)


class N8NClient:
    """
    Client for interacting with n8n workflow automation platform
    """
    
    def __init__(self):
        self.base_url = settings.N8N_API_URL.rstrip('/')
        self.api_key = settings.N8N_API_KEY
        self.client = httpx.AsyncClient(
            timeout=30.0,
            headers={
                "X-N8N-API-KEY": self.api_key,
                "Content-Type": "application/json"
            }
        )
        
        # Workflow IDs for different automation types
        self.workflows = {
            "morning_orchestrator": None,
            "intervention_monitor": None,
            "weekly_reflection": None,
            "emergency_pivot": None,
            "cross_domain_sync": None
        }
        
        logger.info("N8N client initialized", base_url=self.base_url)
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    async def trigger_workflow(
        self,
        workflow_name: str,
        data: Dict[str, Any],
        wait_for_completion: bool = False
    ) -> Dict[str, Any]:
        """
        Trigger an n8n workflow with data
        """
        try:
            workflow_id = self.workflows.get(workflow_name)
            if not workflow_id:
                # Try to find workflow by name
                workflow_id = await self._find_workflow_by_name(workflow_name)
                if workflow_id:
                    self.workflows[workflow_name] = workflow_id
                else:
                    raise ValueError(f"Workflow '{workflow_name}' not found")
            
            # Trigger workflow
            url = f"{self.base_url}/webhooks/{workflow_id}"
            
            logger.info(
                "Triggering n8n workflow",
                workflow_name=workflow_name,
                workflow_id=workflow_id,
                data_keys=list(data.keys())
            )
            
            response = await self.client.post(url, json=data)
            response.raise_for_status()
            
            result = response.json()
            
            if wait_for_completion:
                # Poll for completion if requested
                execution_id = result.get("executionId")
                if execution_id:
                    result = await self._wait_for_execution(execution_id)
            
            logger.info(
                "Workflow triggered successfully",
                workflow_name=workflow_name,
                execution_id=result.get("executionId")
            )
            
            return result
            
        except Exception as e:
            logger.error(
                "Failed to trigger workflow",
                workflow_name=workflow_name,
                error=str(e),
                exc_info=True
            )
            raise
    
    async def _find_workflow_by_name(self, workflow_name: str) -> Optional[str]:
        """Find workflow ID by name"""
        try:
            response = await self.client.get(f"{self.base_url}/workflows")
            response.raise_for_status()
            
            workflows = response.json()
            for workflow in workflows:
                if workflow.get("name", "").lower() == workflow_name.lower():
                    return workflow.get("id")
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to find workflow by name: {str(e)}")
            return None
    
    async def _wait_for_execution(self, execution_id: str, timeout: int = 300) -> Dict[str, Any]:
        """Wait for workflow execution to complete"""
        start_time = datetime.utcnow()
        
        while (datetime.utcnow() - start_time).seconds < timeout:
            try:
                response = await self.client.get(f"{self.base_url}/executions/{execution_id}")
                response.raise_for_status()
                
                execution = response.json()
                status = execution.get("status")
                
                if status in ["success", "error", "canceled"]:
                    return execution
                
                # Wait before polling again
                await asyncio.sleep(2)
                
            except Exception as e:
                logger.error(f"Error polling execution status: {str(e)}")
                break
        
        raise TimeoutError(f"Workflow execution {execution_id} timed out")
    
    async def trigger_morning_orchestrator(
        self,
        user_id: str,
        user_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Trigger the morning orchestrator workflow
        """
        workflow_data = {
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat(),
            "user_data": user_data,
            "workflow_type": "morning_orchestrator"
        }
        
        return await self.trigger_workflow("morning_orchestrator", workflow_data)
    
    async def trigger_intervention_monitor(
        self,
        user_id: str,
        trigger_event: str,
        context_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Trigger real-time intervention monitoring
        """
        workflow_data = {
            "user_id": user_id,
            "trigger_event": trigger_event,
            "context_data": context_data,
            "timestamp": datetime.utcnow().isoformat(),
            "workflow_type": "intervention_monitor"
        }
        
        return await self.trigger_workflow("intervention_monitor", workflow_data)
    
    async def trigger_weekly_reflection(
        self,
        user_id: str,
        week_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Trigger weekly reflection and optimization workflow
        """
        workflow_data = {
            "user_id": user_id,
            "week_data": week_data,
            "timestamp": datetime.utcnow().isoformat(),
            "workflow_type": "weekly_reflection"
        }
        
        return await self.trigger_workflow("weekly_reflection", workflow_data, wait_for_completion=True)
    
    async def trigger_emergency_pivot(
        self,
        user_id: str,
        crisis_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Trigger emergency pivot workflow for crisis situations
        """
        workflow_data = {
            "user_id": user_id,
            "crisis_data": crisis_data,
            "timestamp": datetime.utcnow().isoformat(),
            "workflow_type": "emergency_pivot",
            "priority": "high"
        }
        
        return await self.trigger_workflow("emergency_pivot", workflow_data)
    
    async def trigger_cross_domain_sync(
        self,
        user_id: str,
        goal_changes: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Trigger cross-domain goal synchronization
        """
        workflow_data = {
            "user_id": user_id,
            "goal_changes": goal_changes,
            "timestamp": datetime.utcnow().isoformat(),
            "workflow_type": "cross_domain_sync"
        }
        
        return await self.trigger_workflow("cross_domain_sync", workflow_data)
    
    async def get_workflow_status(self, execution_id: str) -> Dict[str, Any]:
        """
        Get the status of a workflow execution
        """
        try:
            response = await self.client.get(f"{self.base_url}/executions/{execution_id}")
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            logger.error(f"Failed to get workflow status: {str(e)}")
            raise
    
    async def list_active_workflows(self) -> List[Dict[str, Any]]:
        """
        List all active workflows
        """
        try:
            response = await self.client.get(f"{self.base_url}/workflows?active=true")
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            logger.error(f"Failed to list workflows: {str(e)}")
            raise
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Check n8n service health
        """
        try:
            response = await self.client.get(f"{self.base_url}/healthz")
            response.raise_for_status()
            
            return {
                "status": "healthy",
                "service": "n8n",
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"N8N health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "service": "n8n",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }


class WorkflowOrchestrator:
    """
    High-level orchestrator for managing n8n workflows
    """
    
    def __init__(self):
        self.n8n_client = N8NClient()
        self.active_executions = {}
        
    async def schedule_morning_briefing(self, user_id: str, user_data: Dict[str, Any]):
        """
        Schedule and execute morning briefing workflow
        """
        try:
            # Gather context data
            context = await self._gather_morning_context(user_id, user_data)
            
            # Trigger morning orchestrator
            result = await self.n8n_client.trigger_morning_orchestrator(user_id, context)
            
            # Track execution
            execution_id = result.get("executionId")
            if execution_id:
                self.active_executions[execution_id] = {
                    "user_id": user_id,
                    "workflow_type": "morning_orchestrator",
                    "started_at": datetime.utcnow()
                }
            
            logger.info(
                "Morning briefing scheduled",
                user_id=user_id,
                execution_id=execution_id
            )
            
            return result
            
        except Exception as e:
            logger.error(
                "Failed to schedule morning briefing",
                user_id=user_id,
                error=str(e)
            )
            raise
    
    async def handle_user_activity(
        self,
        user_id: str,
        activity_type: str,
        activity_data: Dict[str, Any]
    ):
        """
        Handle user activity and trigger appropriate workflows
        """
        try:
            # Determine if intervention is needed
            intervention_needed = await self._assess_intervention_need(
                user_id, activity_type, activity_data
            )
            
            if intervention_needed:
                # Trigger intervention monitor
                await self.n8n_client.trigger_intervention_monitor(
                    user_id=user_id,
                    trigger_event=activity_type,
                    context_data=activity_data
                )
                
                logger.info(
                    "Intervention monitoring triggered",
                    user_id=user_id,
                    activity_type=activity_type
                )
            
        except Exception as e:
            logger.error(
                "Failed to handle user activity",
                user_id=user_id,
                activity_type=activity_type,
                error=str(e)
            )
    
    async def process_weekly_optimization(self, user_id: str):
        """
        Process weekly reflection and optimization
        """
        try:
            # Gather week's data
            week_data = await self._gather_weekly_data(user_id)
            
            # Trigger weekly reflection workflow
            result = await self.n8n_client.trigger_weekly_reflection(user_id, week_data)
            
            logger.info(
                "Weekly optimization processed",
                user_id=user_id,
                execution_id=result.get("executionId")
            )
            
            return result
            
        except Exception as e:
            logger.error(
                "Failed to process weekly optimization",
                user_id=user_id,
                error=str(e)
            )
            raise
    
    async def handle_goal_update(
        self,
        user_id: str,
        goal_changes: List[Dict[str, Any]]
    ):
        """
        Handle goal updates and trigger cross-domain synchronization
        """
        try:
            # Check if cross-domain sync is needed
            sync_needed = await self._assess_cross_domain_impact(goal_changes)
            
            if sync_needed:
                await self.n8n_client.trigger_cross_domain_sync(user_id, goal_changes)
                
                logger.info(
                    "Cross-domain sync triggered",
                    user_id=user_id,
                    changes_count=len(goal_changes)
                )
            
        except Exception as e:
            logger.error(
                "Failed to handle goal update",
                user_id=user_id,
                error=str(e)
            )
    
    async def _gather_morning_context(
        self,
        user_id: str,
        user_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Gather context data for morning briefing
        """
        # This would integrate with various APIs to gather:
        # - Calendar events
        # - Weather data
        # - Sleep data
        # - Goal progress
        # - Recent activity
        
        return {
            "user_data": user_data,
            "calendar_events": [],  # Would fetch from Google Calendar
            "weather": {},  # Would fetch from weather API
            "sleep_data": {},  # Would fetch from wearable APIs
            "goal_progress": {},  # Would fetch from database
            "recent_activity": []  # Would fetch from database
        }
    
    async def _assess_intervention_need(
        self,
        user_id: str,
        activity_type: str,
        activity_data: Dict[str, Any]
    ) -> bool:
        """
        Assess if user activity requires intervention
        """
        # Simplified logic - in production, this would be more sophisticated
        intervention_triggers = [
            "goal_missed",
            "negative_pattern_detected",
            "user_struggling",
            "opportunity_detected"
        ]
        
        return activity_type in intervention_triggers
    
    async def _gather_weekly_data(self, user_id: str) -> Dict[str, Any]:
        """
        Gather data for weekly reflection
        """
        # This would aggregate data from the past week
        return {
            "goal_progress": {},
            "intervention_compliance": {},
            "behavioral_patterns": {},
            "success_metrics": {},
            "challenges_identified": []
        }
    
    async def _assess_cross_domain_impact(
        self,
        goal_changes: List[Dict[str, Any]]
    ) -> bool:
        """
        Assess if goal changes require cross-domain synchronization
        """
        # Check if changes affect multiple domains
        domains = set()
        for change in goal_changes:
            domains.add(change.get("domain"))
        
        return len(domains) > 1 or any(
            change.get("impact_level") == "high" for change in goal_changes
        )


# Global orchestrator instance
workflow_orchestrator = WorkflowOrchestrator()