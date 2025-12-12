"""
LlamaIndex Integration
======================

LlamaIndexObserver for tracking LlamaIndex agent workflows.
Captures AgentRunner events, query engine operations, and retrieval.

Usage:
    from zentaxa import ZentaxaClient
    from zentaxa.integrations.llamaindex import LlamaIndexObserver
    from llama_index.core.agent import ReActAgent
    
    client = ZentaxaClient()
    observer = LlamaIndexObserver(client=client, agent_id="llama-agent")
    
    # Add to callback manager
    from llama_index.core.callbacks import CallbackManager
    callback_manager = CallbackManager([observer])
    
    agent = ReActAgent.from_tools(
        tools,
        llm=llm,
        callback_manager=callback_manager
    )
    
    response = agent.chat("Research quantum computing")
"""

from typing import Any, Dict, Optional, List
import time
import logging
from ..client import ZentaxaClient

logger = logging.getLogger(__name__)


class LlamaIndexObserver:
    """
    LlamaIndex observer for ZENTAXA telemetry.
    
    Captures:
      - Agent reasoning loops
      - Tool/function calls
      - Query engine operations
      - Retrieval events (document chunks)
      - Index operations
    
    Args:
        client: ZentaxaClient instance
        agent_id: Unique identifier for the agent
        track_retrievals: Log retrieved document chunks (default: False)
    """
    
    def __init__(
        self,
        client: ZentaxaClient,
        agent_id: str,
        track_retrievals: bool = False
    ):
        self.client = client
        self.agent_id = agent_id
        self.track_retrievals = track_retrievals
        self.run_id: Optional[str] = None
        self.step_counter = 0
        self.query_history: List[str] = []
        self.start_time: Optional[float] = None
        self.event_starts: Dict[str, float] = {}
    
    def start_run(self, query: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None):
        """Start tracking agent run"""
        try:
            self.start_time = time.time()
            response = self.client.trace(
                run_id=None,
                agent_id=self.agent_id,
                framework="llamaindex",
                event_type="agent_start",
                metadata={
                    "query": query,
                    **(metadata or {})
                }
            )
            self.run_id = response.get("run_id")
            
            if query:
                self.query_history.append(query)
            
            logger.info(f"Started LlamaIndex run: {self.run_id}")
        except Exception as e:
            logger.error(f"Failed to start run: {e}")
    
    def end_run(self, response: Any = None):
        """End agent run tracking"""
        if not self.run_id:
            return
        
        try:
            total_latency = (time.time() - self.start_time) * 1000 if self.start_time else 0
            
            self.client.trace(
                run_id=self.run_id,
                agent_id=self.agent_id,
                framework="llamaindex",
                event_type="agent_end",
                metadata={
                    "response": str(response) if response else None,
                    "total_steps": self.step_counter,
                    "queries": self.query_history
                }
            )
            
            self.client.metric(
                run_id=self.run_id,
                metric_name="total_latency_ms",
                value=total_latency
            )
            
            logger.info(f"Ended LlamaIndex run: {self.run_id}")
        except Exception as e:
            logger.error(f"Failed to end run: {e}")
    
    def on_event_start(
        self,
        event_type: str,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = ""
    ):
        """Called when LlamaIndex event starts"""
        if not self.run_id:
            query = None
            if event_type == "query" and payload:
                query = payload.get("query_str")
            self.start_run(query=query)
        
        try:
            self.event_starts[event_id] = time.time()
            
            # Track different event types
            if event_type == "retrieve":
                self._track_retrieval_start(payload, event_id)
            elif event_type == "llm":
                self._track_llm_start(payload, event_id)
            elif event_type == "agent_step":
                self._track_agent_step_start(payload, event_id)
            elif event_type == "function_call":
                self._track_function_call_start(payload, event_id)
            else:
                # Generic event
                self.client.log(
                    run_id=self.run_id,
                    message=f"Event started: {event_type}",
                    level="debug",
                    context={"event_id": event_id, "payload": payload}
                )
        except Exception as e:
            logger.error(f"on_event_start error: {e}")
    
    def on_event_end(
        self,
        event_type: str,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = ""
    ):
        """Called when LlamaIndex event ends"""
        if not self.run_id:
            return
        
        try:
            latency_ms = (time.time() - self.event_starts.get(event_id, time.time())) * 1000
            
            # Track different event types
            if event_type == "retrieve":
                self._track_retrieval_end(payload, event_id, latency_ms)
            elif event_type == "llm":
                self._track_llm_end(payload, event_id, latency_ms)
            elif event_type == "agent_step":
                self._track_agent_step_end(payload, event_id, latency_ms)
            elif event_type == "function_call":
                self._track_function_call_end(payload, event_id, latency_ms)
        except Exception as e:
            logger.error(f"on_event_end error: {e}")
    
    def _track_retrieval_start(self, payload: Optional[Dict[str, Any]], event_id: str):
        """Track retrieval start"""
        query = payload.get("query_str", "") if payload else ""
        
        self.step_counter += 1
        self.client.agent_event(
            run_id=self.run_id,
            event_type="step_start",
            step_number=self.step_counter,
            step_name="Document Retrieval",
            action_type="retrieve",
            input_data=query,
            metadata={"event_id": event_id}
        )
    
    def _track_retrieval_end(self, payload: Optional[Dict[str, Any]], event_id: str, latency_ms: float):
        """Track retrieval end"""
        nodes = payload.get("nodes", []) if payload else []
        node_count = len(nodes)
        
        # Optionally log retrieved chunks
        if self.track_retrievals and nodes:
            for i, node in enumerate(nodes[:3]):  # First 3 nodes only
                self.client.log(
                    run_id=self.run_id,
                    message=f"Retrieved chunk {i+1}/{node_count}",
                    level="debug",
                    context={
                        "score": getattr(node, "score", None),
                        "text_preview": str(node.text)[:100] if hasattr(node, "text") else None
                    }
                )
        
        self.client.agent_event(
            run_id=self.run_id,
            event_type="step_complete",
            step_number=self.step_counter,
            step_name="Document Retrieval",
            action_type="retrieve",
            output_data=f"Retrieved {node_count} chunks",
            latency_ms=latency_ms,
            metadata={"node_count": node_count}
        )
    
    def _track_llm_start(self, payload: Optional[Dict[str, Any]], event_id: str):
        """Track LLM call start"""
        self.step_counter += 1
        
        messages = payload.get("messages", []) if payload else []
        prompt = str(messages) if messages else ""
        
        self.client.agent_event(
            run_id=self.run_id,
            event_type="step_start",
            step_number=self.step_counter,
            step_name="LLM Call",
            action_type="llm",
            input_data=prompt,
            metadata={"event_id": event_id}
        )
    
    def _track_llm_end(self, payload: Optional[Dict[str, Any]], event_id: str, latency_ms: float):
        """Track LLM call end"""
        response = payload.get("response", "") if payload else ""
        
        # Extract token usage if available
        raw = payload.get("raw") if payload else None
        tokens_used = None
        if raw and hasattr(raw, "usage"):
            tokens_used = getattr(raw.usage, "total_tokens", None)
        
        self.client.agent_event(
            run_id=self.run_id,
            event_type="step_complete",
            step_number=self.step_counter,
            step_name="LLM Call",
            action_type="llm",
            output_data=str(response),
            latency_ms=latency_ms,
            tokens_used=tokens_used
        )
        
        self.client.metric(
            run_id=self.run_id,
            metric_name="llm_latency_ms",
            value=latency_ms
        )
    
    def _track_agent_step_start(self, payload: Optional[Dict[str, Any]], event_id: str):
        """Track agent reasoning step start"""
        self.step_counter += 1
        
        thought = payload.get("thought", "") if payload else ""
        
        self.client.agent_event(
            run_id=self.run_id,
            event_type="step_start",
            step_number=self.step_counter,
            step_name=f"Agent Step {self.step_counter}",
            action_type="reason",
            input_data=thought,
            metadata={"event_id": event_id}
        )
    
    def _track_agent_step_end(self, payload: Optional[Dict[str, Any]], event_id: str, latency_ms: float):
        """Track agent reasoning step end"""
        output = payload.get("output", "") if payload else ""
        
        self.client.agent_event(
            run_id=self.run_id,
            event_type="step_complete",
            step_number=self.step_counter,
            step_name=f"Agent Step {self.step_counter}",
            action_type="reason",
            output_data=str(output),
            latency_ms=latency_ms
        )
    
    def _track_function_call_start(self, payload: Optional[Dict[str, Any]], event_id: str):
        """Track function/tool call start"""
        self.step_counter += 1
        
        tool_name = payload.get("tool", {}).get("name", "Unknown") if payload else "Unknown"
        tool_input = payload.get("arguments", {}) if payload else {}
        
        self.client.agent_event(
            run_id=self.run_id,
            event_type="step_start",
            step_number=self.step_counter,
            step_name=f"Tool: {tool_name}",
            action_type="tool",
            input_data=str(tool_input),
            metadata={
                "event_id": event_id,
                "tool_name": tool_name
            }
        )
    
    def _track_function_call_end(self, payload: Optional[Dict[str, Any]], event_id: str, latency_ms: float):
        """Track function/tool call end"""
        output = payload.get("output", "") if payload else ""
        tool_name = payload.get("tool", {}).get("name", "Unknown") if payload else "Unknown"
        
        self.client.agent_event(
            run_id=self.run_id,
            event_type="step_complete",
            step_number=self.step_counter,
            step_name=f"Tool: {tool_name}",
            action_type="tool",
            output_data=str(output),
            latency_ms=latency_ms
        )
    
    # ========================================================================
    # CONTEXT MANAGER
    # ========================================================================
    
    def __enter__(self):
        """Context manager entry"""
        self.start_run()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if exc_type:
            if self.run_id:
                self.client.trace(
                    run_id=self.run_id,
                    agent_id=self.agent_id,
                    framework="llamaindex",
                    event_type="agent_error",
                    metadata={"error": str(exc_val)}
                )
        else:
            self.end_run()
        
        return False
