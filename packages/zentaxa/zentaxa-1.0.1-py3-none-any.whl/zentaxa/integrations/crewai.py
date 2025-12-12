"""
CrewAI Integration
==================

CrewAIObserver for tracking CrewAI agent workflows.
Captures agent reasoning, task execution, and crew orchestration.

Usage:
    from zentaxa import ZentaxaClient
    from zentaxa.integrations.crewai import CrewAIObserver
    from crewai import Agent, Task, Crew
    
    client = ZentaxaClient()
    observer = CrewAIObserver(client=client, agent_id="research-crew")
    
    # Wrap crew execution
    with observer:
        result = crew.kickoff()

Alternative (manual):
    observer = CrewAIObserver(client=client, agent_id="research-crew")
    observer.start_crew(crew_name="Research Crew")
    
    # Your crew logic
    result = crew.kickoff()
    
    observer.end_crew(result=result)
"""

from typing import Any, Dict, Optional, List
from datetime import datetime
import time
import logging
from ..client import ZentaxaClient

logger = logging.getLogger(__name__)


class CrewAIObserver:
    """
    CrewAI observer for ZENTAXA telemetry.
    
    Captures:
      - Crew kickoff and completion
      - Agent task assignments
      - Task execution (input, output, duration)
      - Agent reasoning and decisions
      - Inter-agent communication
    
    Args:
        client: ZentaxaClient instance
        agent_id: Unique identifier for the crew
        auto_track: Automatically track all events (default: True)
    """
    
    def __init__(
        self,
        client: ZentaxaClient,
        agent_id: str,
        auto_track: bool = True
    ):
        self.client = client
        self.agent_id = agent_id
        self.auto_track = auto_track
        self.run_id: Optional[str] = None
        self.step_counter = 0
        self.agent_tasks: Dict[str, int] = {}  # agent_name -> task_count
        self.start_time: Optional[float] = None
    
    def start_crew(self, crew_name: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None):
        """Start tracking crew execution"""
        try:
            self.start_time = time.time()
            response = self.client.trace(
                run_id=None,
                agent_id=self.agent_id,
                framework="crewai",
                event_type="agent_start",
                metadata={
                    "crew_name": crew_name or self.agent_id,
                    **(metadata or {})
                }
            )
            self.run_id = response.get("run_id")
            logger.info(f"Started CrewAI run: {self.run_id}")
        except Exception as e:
            logger.error(f"Failed to start crew: {e}")
    
    def end_crew(self, result: Any = None, metadata: Optional[Dict[str, Any]] = None):
        """End crew tracking"""
        if not self.run_id:
            return
        
        try:
            total_latency = (time.time() - self.start_time) * 1000 if self.start_time else 0
            
            self.client.trace(
                run_id=self.run_id,
                agent_id=self.agent_id,
                framework="crewai",
                event_type="agent_end",
                metadata={
                    "result": str(result) if result else None,
                    "total_tasks": self.step_counter,
                    "agents_used": len(self.agent_tasks),
                    **(metadata or {})
                }
            )
            
            self.client.metric(
                run_id=self.run_id,
                metric_name="total_latency_ms",
                value=total_latency
            )
            
            logger.info(f"Ended CrewAI run: {self.run_id}")
        except Exception as e:
            logger.error(f"Failed to end crew: {e}")
    
    def track_task_start(
        self,
        task_description: str,
        agent_name: str,
        task_metadata: Optional[Dict[str, Any]] = None
    ):
        """Track task assignment to agent"""
        if not self.run_id:
            self.start_crew()
        
        try:
            self.step_counter += 1
            
            # Track agent task count
            self.agent_tasks[agent_name] = self.agent_tasks.get(agent_name, 0) + 1
            
            self.client.agent_event(
                run_id=self.run_id,
                event_type="step_start",
                step_number=self.step_counter,
                step_name=f"{agent_name} - Task {self.agent_tasks[agent_name]}",
                action_type="plan",
                input_data=task_description,
                metadata={
                    "agent_name": agent_name,
                    "task_type": "crew_task",
                    **(task_metadata or {})
                }
            )
            
            self.client.log(
                run_id=self.run_id,
                message=f"Task assigned to {agent_name}",
                level="info",
                context={
                    "agent": agent_name,
                    "task": task_description[:100]  # Truncate long tasks
                }
            )
        except Exception as e:
            logger.error(f"track_task_start error: {e}")
    
    def track_task_complete(
        self,
        agent_name: str,
        output: Any,
        latency_ms: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Track task completion"""
        if not self.run_id:
            return
        
        try:
            self.client.agent_event(
                run_id=self.run_id,
                event_type="step_complete",
                step_number=self.step_counter,
                step_name=f"{agent_name} - Task {self.agent_tasks.get(agent_name, 0)}",
                action_type="plan",
                output_data=str(output),
                latency_ms=latency_ms,
                metadata={
                    "agent_name": agent_name,
                    **(metadata or {})
                }
            )
        except Exception as e:
            logger.error(f"track_task_complete error: {e}")
    
    def track_reasoning(
        self,
        agent_name: str,
        thought: str,
        action: Optional[str] = None
    ):
        """Track agent reasoning"""
        if not self.run_id:
            return
        
        try:
            self.client.log(
                run_id=self.run_id,
                message=f"{agent_name} reasoning: {thought}",
                level="info",
                context={
                    "agent": agent_name,
                    "thought": thought,
                    "action": action
                }
            )
        except Exception as e:
            logger.error(f"track_reasoning error: {e}")
    
    def track_tool_use(
        self,
        agent_name: str,
        tool_name: str,
        tool_input: Any,
        tool_output: Any,
        latency_ms: Optional[float] = None
    ):
        """Track tool usage by agent"""
        if not self.run_id:
            return
        
        try:
            self.step_counter += 1
            
            self.client.agent_event(
                run_id=self.run_id,
                event_type="step_complete",
                step_number=self.step_counter,
                step_name=f"{agent_name} - {tool_name}",
                action_type="tool",
                input_data=str(tool_input),
                output_data=str(tool_output),
                latency_ms=latency_ms,
                metadata={
                    "agent_name": agent_name,
                    "tool_name": tool_name
                }
            )
        except Exception as e:
            logger.error(f"track_tool_use error: {e}")
    
    def track_agent_communication(
        self,
        from_agent: str,
        to_agent: str,
        message: str
    ):
        """Track communication between agents"""
        if not self.run_id:
            return
        
        try:
            self.client.log(
                run_id=self.run_id,
                message=f"Agent communication: {from_agent} → {to_agent}",
                level="info",
                context={
                    "from": from_agent,
                    "to": to_agent,
                    "message": message
                }
            )
        except Exception as e:
            logger.error(f"track_agent_communication error: {e}")
    
    # ========================================================================
    # CONTEXT MANAGER
    # ========================================================================
    
    def __enter__(self):
        """Context manager entry"""
        self.start_crew()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if exc_type:
            # Error occurred
            if self.run_id:
                self.client.trace(
                    run_id=self.run_id,
                    agent_id=self.agent_id,
                    framework="crewai",
                    event_type="agent_error",
                    metadata={"error": str(exc_val)}
                )
        else:
            self.end_crew()
        
        return False  # Don't suppress exceptions
