"""
Base Agent Architecture for ORBIT
World-class AI agent foundation with Opik integration
"""

import asyncio
import json
import time
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass, asdict
from datetime import datetime
import uuid

from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
import opik
from opik import track, opik_context
import structlog
import httpx
import json

from ..core.config import settings, MODEL_CONFIGS


logger = structlog.get_logger(__name__)


@dataclass
class AgentResponse:
    """Standardized agent response format"""
    content: str
    reasoning: Optional[str] = None
    confidence: float = 0.0
    metadata: Dict[str, Any] = None
    execution_time_ms: int = 0
    model_used: str = ""
    token_usage: Dict[str, int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AgentContext:
    """Context passed to agents for decision making"""
    user_id: str
    session_id: str
    current_goals: List[Dict[str, Any]]
    user_state: Dict[str, Any]
    recent_history: List[Dict[str, Any]]
    external_context: Dict[str, Any] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


class BaseAgent(ABC):
    """
    Base class for all ORBIT agents with built-in Opik tracking,
    error handling, and performance monitoring
    """
    
    def __init__(
        self,
        agent_type: str,
        model_config: Optional[Dict[str, Any]] = None,
        enable_opik: bool = True
    ):
        self.agent_type = agent_type
        self.enable_opik = enable_opik
        self.model_config = model_config or MODEL_CONFIGS.get(agent_type, {})
        
        # Initialize LLM based on model configuration
        self.llm = self._initialize_llm()
        
        # Initialize Opik client if enabled
        if self.enable_opik:
            self.opik_client = opik.Opik(
                api_key=settings.OPIK_API_KEY,
                project_name=settings.OPIK_PROJECT_NAME,
                workspace=settings.OPIK_WORKSPACE
            )
        
        logger.info(
            "Agent initialized",
            agent_type=agent_type,
            model=self.model_config.get("model"),
            opik_enabled=enable_opik
        )
    
    def _initialize_llm(self):
        """Initialize the appropriate LLM based on model configuration"""
        model_config = self.model_config
        provider = model_config.get("provider", "openrouter")
        model_name = model_config.get("model", "meta-llama/llama-3.1-8b-instruct:free")
        
        if provider == "google":
            # Use Google Gemini directly
            return ChatGoogleGenerativeAI(
                model=model_name.split("/")[-1],  # Extract model name
                temperature=model_config.get("temperature", 0.7),
                max_output_tokens=model_config.get("max_tokens", 2048),
                google_api_key=settings.GOOGLE_API_KEY,
            )
        elif provider == "openrouter":
            # Use OpenRouter for cost-effective access to multiple models
            return OpenRouterLLM(
                model=model_name,
                temperature=model_config.get("temperature", 0.7),
                max_tokens=model_config.get("max_tokens", 2048),
                api_key=settings.OPEN_ROUTER_API_KEY,
            )
        else:
            # Fallback to OpenRouter with free model
            logger.warning(f"Unknown provider {provider}, falling back to OpenRouter")
            return OpenRouterLLM(
                model="meta-llama/llama-3.1-8b-instruct:free",
                temperature=0.7,
                max_tokens=2048,
                api_key=settings.OPEN_ROUTER_API_KEY,
            )
    
    @track(name="agent_execution")
    async def execute(
        self,
        context: AgentContext,
        user_input: str,
        **kwargs
    ) -> AgentResponse:
        """
        Main execution method with comprehensive tracking and error handling
        """
        start_time = time.time()
        execution_id = str(uuid.uuid4())
        
        try:
            # Log execution start
            logger.info(
                "Agent execution started",
                agent_type=self.agent_type,
                execution_id=execution_id,
                user_id=context.user_id,
                session_id=context.session_id
            )
            
            # Add Opik context
            if self.enable_opik:
                opik_context.update_current_trace(
                    name=f"{self.agent_type}_execution",
                    input={
                        "user_input": user_input,
                        "context": context.to_dict() if hasattr(context, 'to_dict') else str(context),
                        "agent_type": self.agent_type,
                        "model": self.model_config.get("model")
                    },
                    metadata={
                        "execution_id": execution_id,
                        "user_id": context.user_id,
                        "session_id": context.session_id,
                        "timestamp": datetime.utcnow().isoformat()
                    }
                )
            
            # Execute the agent-specific logic
            response = await self._execute_internal(context, user_input, **kwargs)
            
            # Calculate execution time
            execution_time_ms = int((time.time() - start_time) * 1000)
            response.execution_time_ms = execution_time_ms
            response.model_used = self.model_config.get("model", "unknown")
            
            # Update Opik trace with output
            if self.enable_opik:
                opik_context.update_current_trace(
                    output={
                        "content": response.content,
                        "reasoning": response.reasoning,
                        "confidence": response.confidence,
                        "execution_time_ms": execution_time_ms
                    },
                    metadata={
                        "success": True,
                        "token_usage": response.token_usage or {}
                    }
                )
            
            logger.info(
                "Agent execution completed",
                agent_type=self.agent_type,
                execution_id=execution_id,
                execution_time_ms=execution_time_ms,
                confidence=response.confidence
            )
            
            return response
            
        except Exception as e:
            execution_time_ms = int((time.time() - start_time) * 1000)
            
            # Log error
            logger.error(
                "Agent execution failed",
                agent_type=self.agent_type,
                execution_id=execution_id,
                error=str(e),
                execution_time_ms=execution_time_ms,
                exc_info=True
            )
            
            # Update Opik trace with error
            if self.enable_opik:
                opik_context.update_current_trace(
                    output={"error": str(e)},
                    metadata={
                        "success": False,
                        "error_type": type(e).__name__,
                        "execution_time_ms": execution_time_ms
                    }
                )
            
            # Return error response
            return AgentResponse(
                content=f"I encountered an error: {str(e)}",
                reasoning="Error occurred during execution",
                confidence=0.0,
                execution_time_ms=execution_time_ms,
                model_used=self.model_config.get("model", "unknown"),
                metadata={"error": True, "error_message": str(e)}
            )
    
    @abstractmethod
    async def _execute_internal(
        self,
        context: AgentContext,
        user_input: str,
        **kwargs
    ) -> AgentResponse:
        """
        Internal execution method to be implemented by subclasses
        """
        pass
    
    async def _call_llm(
        self,
        messages: List[BaseMessage],
        **kwargs
    ) -> Dict[str, Any]:
        """
        Call the LLM with proper error handling and token tracking
        """
        try:
            # Add system message if not present
            if not any(isinstance(msg, SystemMessage) for msg in messages):
                system_prompt = self.model_config.get("system_prompt", "")
                if system_prompt:
                    messages = [SystemMessage(content=system_prompt)] + messages
            
            # Call the LLM
            response = await self.llm.ainvoke(messages, **kwargs)
            
            # Extract token usage if available
            token_usage = {}
            if hasattr(response, 'response_metadata'):
                usage = response.response_metadata.get('usage', {})
                token_usage = {
                    "prompt_tokens": usage.get('prompt_tokens', 0),
                    "completion_tokens": usage.get('completion_tokens', 0),
                    "total_tokens": usage.get('total_tokens', 0)
                }
            
            return {
                "content": response.content,
                "token_usage": token_usage,
                "model": self.model_config.get("model")
            }
            
        except Exception as e:
            logger.error(
                "LLM call failed",
                agent_type=self.agent_type,
                model=self.model_config.get("model"),
                error=str(e),
                exc_info=True
            )
            raise
    
    def _build_context_prompt(self, context: AgentContext) -> str:
        """
        Build a comprehensive context prompt from the AgentContext
        """
        prompt_parts = []
        
        # User information
        prompt_parts.append(f"User ID: {context.user_id}")
        prompt_parts.append(f"Session ID: {context.session_id}")
        prompt_parts.append(f"Current Time: {context.timestamp.isoformat()}")
        
        # Current goals
        if context.current_goals:
            prompt_parts.append("\nCurrent Goals:")
            for i, goal in enumerate(context.current_goals, 1):
                goal_info = f"{i}. {goal.get('title', 'Untitled Goal')}"
                if goal.get('domain'):
                    goal_info += f" (Domain: {goal['domain']})"
                if goal.get('progress'):
                    goal_info += f" - Progress: {goal['progress']}%"
                prompt_parts.append(goal_info)
        
        # User state
        if context.user_state:
            prompt_parts.append(f"\nUser State: {json.dumps(context.user_state, indent=2)}")
        
        # Recent history
        if context.recent_history:
            prompt_parts.append("\nRecent History:")
            for event in context.recent_history[-5:]:  # Last 5 events
                timestamp = event.get('timestamp', 'Unknown time')
                action = event.get('action', 'Unknown action')
                prompt_parts.append(f"- {timestamp}: {action}")
        
        # External context
        if context.external_context:
            prompt_parts.append(f"\nExternal Context: {json.dumps(context.external_context, indent=2)}")
        
        return "\n".join(prompt_parts)
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Perform a health check on the agent
        """
        try:
            # Simple test call
            test_messages = [
                SystemMessage(content="You are a test agent."),
                HumanMessage(content="Respond with 'OK' if you're working correctly.")
            ]
            
            start_time = time.time()
            response = await self._call_llm(test_messages)
            response_time = int((time.time() - start_time) * 1000)
            
            return {
                "status": "healthy",
                "agent_type": self.agent_type,
                "model": self.model_config.get("model"),
                "response_time_ms": response_time,
                "opik_enabled": self.enable_opik,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "agent_type": self.agent_type,
                "model": self.model_config.get("model"),
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }


class AgentOrchestrator:
    """
    Orchestrates multiple agents and manages their interactions
    """
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.execution_history: List[Dict[str, Any]] = []
    
    def register_agent(self, agent_type: str, agent: BaseAgent):
        """Register an agent with the orchestrator"""
        self.agents[agent_type] = agent
        logger.info(f"Agent registered: {agent_type}")
    
    async def execute_workflow(
        self,
        workflow_name: str,
        context: AgentContext,
        user_input: str,
        **kwargs
    ) -> Dict[str, AgentResponse]:
        """
        Execute a multi-agent workflow
        """
        workflow_id = str(uuid.uuid4())
        start_time = time.time()
        
        logger.info(
            "Workflow execution started",
            workflow_name=workflow_name,
            workflow_id=workflow_id,
            user_id=context.user_id
        )
        
        results = {}
        
        try:
            if workflow_name == "intervention_pipeline":
                # Standard intervention pipeline: Worker -> Supervisor -> (Optional) Optimizer
                
                # Step 1: Worker generates intervention
                if "worker" in self.agents:
                    worker_response = await self.agents["worker"].execute(
                        context, user_input, **kwargs
                    )
                    results["worker"] = worker_response
                
                # Step 2: Supervisor evaluates intervention
                if "supervisor" in self.agents and "worker" in results:
                    supervisor_input = f"Evaluate this intervention: {results['worker'].content}"
                    supervisor_response = await self.agents["supervisor"].execute(
                        context, supervisor_input, **kwargs
                    )
                    results["supervisor"] = supervisor_response
                
                # Step 3: Optional optimizer feedback (async)
                if "optimizer" in self.agents:
                    # This could be done asynchronously for performance
                    asyncio.create_task(
                        self._log_for_optimization(workflow_id, context, results)
                    )
            
            execution_time_ms = int((time.time() - start_time) * 1000)
            
            # Log workflow completion
            self.execution_history.append({
                "workflow_id": workflow_id,
                "workflow_name": workflow_name,
                "user_id": context.user_id,
                "execution_time_ms": execution_time_ms,
                "results": {k: v.to_dict() for k, v in results.items()},
                "timestamp": datetime.utcnow().isoformat()
            })
            
            logger.info(
                "Workflow execution completed",
                workflow_name=workflow_name,
                workflow_id=workflow_id,
                execution_time_ms=execution_time_ms,
                agents_executed=list(results.keys())
            )
            
            return results
            
        except Exception as e:
            logger.error(
                "Workflow execution failed",
                workflow_name=workflow_name,
                workflow_id=workflow_id,
                error=str(e),
                exc_info=True
            )
            raise
    
    async def _log_for_optimization(
        self,
        workflow_id: str,
        context: AgentContext,
        results: Dict[str, AgentResponse]
    ):
        """
        Log execution data for the optimizer agent to analyze later
        """
        try:
            # This would typically write to a database or queue for batch processing
            optimization_data = {
                "workflow_id": workflow_id,
                "context": context,
                "results": results,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # For now, just log it
            logger.info(
                "Optimization data logged",
                workflow_id=workflow_id,
                data_size=len(str(optimization_data))
            )
            
        except Exception as e:
            logger.error(
                "Failed to log optimization data",
                workflow_id=workflow_id,
                error=str(e)
            )
    
    async def health_check_all(self) -> Dict[str, Dict[str, Any]]:
        """
        Perform health checks on all registered agents
        """
        health_results = {}
        
        for agent_type, agent in self.agents.items():
            health_results[agent_type] = await agent.health_check()
        
        return health_results


class OpenRouterLLM:
    """
    Custom LLM wrapper for OpenRouter API
    Provides cost-effective access to multiple AI models
    """
    
    def __init__(self, model: str, temperature: float = 0.7, max_tokens: int = 2048, api_key: str = None):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.api_key = api_key or settings.OPEN_ROUTER_API_KEY
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        
        if not self.api_key:
            raise ValueError("OpenRouter API key is required")
    
    async def ainvoke(self, messages: List[BaseMessage], **kwargs) -> Any:
        """
        Async invoke method compatible with LangChain interface
        """
        # Convert LangChain messages to OpenRouter format
        openrouter_messages = []
        
        for message in messages:
            if isinstance(message, SystemMessage):
                openrouter_messages.append({
                    "role": "system",
                    "content": message.content
                })
            elif isinstance(message, HumanMessage):
                openrouter_messages.append({
                    "role": "user", 
                    "content": message.content
                })
            elif isinstance(message, AIMessage):
                openrouter_messages.append({
                    "role": "assistant",
                    "content": message.content
                })
        
        # Prepare request payload
        payload = {
            "model": self.model,
            "messages": openrouter_messages,
            "temperature": kwargs.get("temperature", self.temperature),
            "max_tokens": kwargs.get("max_tokens", self.max_tokens),
            "top_p": kwargs.get("top_p", 0.9),
            "stream": False
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://orbit.ai",  # Optional: for analytics
            "X-Title": "ORBIT AI Platform"  # Optional: for analytics
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.base_url,
                    json=payload,
                    headers=headers
                )
                response.raise_for_status()
                
                result = response.json()
                
                # Extract response content
                content = result["choices"][0]["message"]["content"]
                
                # Extract usage information
                usage = result.get("usage", {})
                
                # Create response object compatible with LangChain
                class OpenRouterResponse:
                    def __init__(self, content: str, usage: dict):
                        self.content = content
                        self.response_metadata = {
                            "usage": {
                                "prompt_tokens": usage.get("prompt_tokens", 0),
                                "completion_tokens": usage.get("completion_tokens", 0),
                                "total_tokens": usage.get("total_tokens", 0)
                            },
                            "model": self.model,
                            "provider": "openrouter"
                        }
                
                return OpenRouterResponse(content, usage)
                
        except httpx.HTTPStatusError as e:
            logger.error(f"OpenRouter API error: {e.response.status_code} - {e.response.text}")
            
            # Fallback to free model if paid model fails
            if self.model != "meta-llama/llama-3.1-8b-instruct:free":
                logger.info("Falling back to free model")
                fallback_llm = OpenRouterLLM(
                    model="meta-llama/llama-3.1-8b-instruct:free",
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                    api_key=self.api_key
                )
                return await fallback_llm.ainvoke(messages, **kwargs)
            
            raise Exception(f"OpenRouter API error: {e.response.status_code}")
            
        except Exception as e:
            logger.error(f"OpenRouter request failed: {str(e)}")
            raise Exception(f"OpenRouter request failed: {str(e)}")
    
    def invoke(self, messages: List[BaseMessage], **kwargs) -> Any:
        """
        Sync invoke method (wrapper around async)
        """
        import asyncio
        return asyncio.run(self.ainvoke(messages, **kwargs))