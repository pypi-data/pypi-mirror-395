"""
AutoGen Integration
===================

AutoGenTracer for Microsoft AutoGen multi-agent conversations.
Tracks message exchanges, tool calls, and agent interactions.

Usage:
    from zentaxa import ZentaxaClient
    from zentaxa.integrations.autogen import AutoGenTracer
    from autogen import UserProxyAgent, AssistantAgent
    
    client = ZentaxaClient()
    tracer = AutoGenTracer(client=client, agent_id="autogen-conversation")
    
    # Wrap agents with tracer
    user_proxy = UserProxyAgent("user", tracer=tracer)
    assistant = AssistantAgent("assistant", llm_config=config, tracer=tracer)
    
    # Start conversation
    with tracer:
        user_proxy.initiate_chat(assistant, message="Research quantum computing")
"""

from typing import Any, Dict, Optional, List
import time
import logging
from ..client import ZentaxaClient

logger = logging.getLogger(__name__)


class AutoGenTracer:
    """
    AutoGen tracer for ZENTAXA telemetry.
    
    Captures:
      - Agent-to-agent messages
      - Tool/function calls
      - Code execution
      - Conversation flow
      - Human-in-the-loop interactions
    
    Args:
        client: ZentaxaClient instance
        agent_id: Unique identifier for the conversation
        track_messages: Store full message content (default: True)
    """
    
    def __init__(
        self,
        client: ZentaxaClient,
        agent_id: str,
        track_messages: bool = True
    ):
        self.client = client
        self.agent_id = agent_id
        self.track_messages = track_messages
        self.run_id: Optional[str] = None
        self.message_count = 0
        self.agents_involved: set = set()
        self.start_time: Optional[float] = None
    
    def start_conversation(self, metadata: Optional[Dict[str, Any]] = None):
        """Start tracking conversation"""
        try:
            self.start_time = time.time()
            response = self.client.trace(
                run_id=None,
                agent_id=self.agent_id,
                framework="autogen",
                event_type="agent_start",
                metadata=metadata or {}
            )
            self.run_id = response.get("run_id")
            logger.info(f"Started AutoGen conversation: {self.run_id}")
        except Exception as e:
            logger.error(f"Failed to start conversation: {e}")
    
    def end_conversation(self, final_response: Any = None):
        """End conversation tracking"""
        if not self.run_id:
            return
        
        try:
            total_latency = (time.time() - self.start_time) * 1000 if self.start_time else 0
            
            self.client.trace(
                run_id=self.run_id,
                agent_id=self.agent_id,
                framework="autogen",
                event_type="agent_end",
                metadata={
                    "final_response": str(final_response) if final_response else None,
                    "total_messages": self.message_count,
                    "agents_involved": list(self.agents_involved)
                }
            )
            
            self.client.metric(
                run_id=self.run_id,
                metric_name="total_latency_ms",
                value=total_latency
            )
            
            logger.info(f"Ended AutoGen conversation: {self.run_id}")
        except Exception as e:
            logger.error(f"Failed to end conversation: {e}")
    
    def track_message(
        self,
        from_agent: str,
        to_agent: str,
        message: Dict[str, Any],
        message_type: str = "chat"
    ):
        """
        Track message exchange between agents.
        
        Args:
            from_agent: Sender agent name
            to_agent: Receiver agent name
            message: Message content (typically {"role": "...", "content": "..."})
            message_type: Type of message (chat, function_call, code_execution)
        """
        if not self.run_id:
            self.start_conversation()
        
        try:
            self.message_count += 1
            self.agents_involved.add(from_agent)
            self.agents_involved.add(to_agent)
            
            message_content = message.get("content", "") if isinstance(message, dict) else str(message)
            
            self.client.agent_event(
                run_id=self.run_id,
                event_type="step_complete",
                step_number=self.message_count,
                step_name=f"Message: {from_agent} → {to_agent}",
                action_type="reason",
                input_data=from_agent,
                output_data=message_content if self.track_messages else f"[Message {self.message_count}]",
                metadata={
                    "from": from_agent,
                    "to": to_agent,
                    "message_type": message_type,
                    "role": message.get("role") if isinstance(message, dict) else None
                }
            )
            
            self.client.log(
                run_id=self.run_id,
                message=f"Message {self.message_count}: {from_agent} → {to_agent}",
                level="info",
                context={
                    "from": from_agent,
                    "to": to_agent,
                    "type": message_type
                }
            )
        except Exception as e:
            logger.error(f"track_message error: {e}")
    
    def track_function_call(
        self,
        agent_name: str,
        function_name: str,
        arguments: Dict[str, Any],
        result: Any = None,
        latency_ms: Optional[float] = None
    ):
        """Track function/tool call by agent"""
        if not self.run_id:
            return
        
        try:
            self.message_count += 1
            
            self.client.agent_event(
                run_id=self.run_id,
                event_type="step_complete",
                step_number=self.message_count,
                step_name=f"{agent_name} - {function_name}",
                action_type="tool",
                input_data=str(arguments),
                output_data=str(result) if result else None,
                latency_ms=latency_ms,
                metadata={
                    "agent_name": agent_name,
                    "function_name": function_name
                }
            )
        except Exception as e:
            logger.error(f"track_function_call error: {e}")
    
    def track_code_execution(
        self,
        agent_name: str,
        code: str,
        output: str,
        success: bool = True,
        latency_ms: Optional[float] = None
    ):
        """Track code execution by agent"""
        if not self.run_id:
            return
        
        try:
            self.message_count += 1
            
            self.client.agent_event(
                run_id=self.run_id,
                event_type="step_complete",
                step_number=self.message_count,
                step_name=f"{agent_name} - Code Execution",
                action_type="code",
                input_data=code,
                output_data=output,
                latency_ms=latency_ms,
                metadata={
                    "agent_name": agent_name,
                    "success": success,
                    "code_length": len(code)
                }
            )
            
            self.client.log(
                run_id=self.run_id,
                message=f"Code execution by {agent_name}: {'success' if success else 'failed'}",
                level="info" if success else "warning",
                context={
                    "agent": agent_name,
                    "output_length": len(output)
                }
            )
        except Exception as e:
            logger.error(f"track_code_execution error: {e}")
    
    def track_llm_call(
        self,
        agent_name: str,
        model: str,
        prompt: str,
        response: str,
        tokens_used: Optional[int] = None,
        cost_usd: Optional[float] = None,
        latency_ms: Optional[float] = None
    ):
        """Track LLM call by agent"""
        if not self.run_id:
            return
        
        try:
            self.message_count += 1
            
            self.client.agent_event(
                run_id=self.run_id,
                event_type="step_complete",
                step_number=self.message_count,
                step_name=f"{agent_name} - LLM Call",
                action_type="llm",
                input_data=prompt,
                output_data=response,
                latency_ms=latency_ms,
                cost_usd=cost_usd,
                tokens_used=tokens_used,
                metadata={
                    "agent_name": agent_name,
                    "model": model
                }
            )
            
            if latency_ms:
                self.client.metric(
                    run_id=self.run_id,
                    metric_name="llm_latency_ms",
                    value=latency_ms,
                    tags={"agent": agent_name, "model": model}
                )
            
            if tokens_used:
                self.client.metric(
                    run_id=self.run_id,
                    metric_name="tokens_used",
                    value=float(tokens_used),
                    tags={"agent": agent_name, "model": model}
                )
        except Exception as e:
            logger.error(f"track_llm_call error: {e}")
    
    def track_human_input(
        self,
        prompt: str,
        response: str
    ):
        """Track human-in-the-loop interaction"""
        if not self.run_id:
            return
        
        try:
            self.message_count += 1
            
            self.client.log(
                run_id=self.run_id,
                message="Human input requested",
                level="info",
                context={
                    "prompt": prompt,
                    "response": response[:100]  # Truncate
                }
            )
        except Exception as e:
            logger.error(f"track_human_input error: {e}")
    
    # ========================================================================
    # CONTEXT MANAGER
    # ========================================================================
    
    def __enter__(self):
        """Context manager entry"""
        self.start_conversation()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if exc_type:
            if self.run_id:
                self.client.trace(
                    run_id=self.run_id,
                    agent_id=self.agent_id,
                    framework="autogen",
                    event_type="agent_error",
                    metadata={"error": str(exc_val)}
                )
        else:
            self.end_conversation()
        
        return False
