"""
LangChain / LangGraph Integration
==================================

ZentaxaCallbackHandler for LangChain and LangGraph agents.
Automatically captures LLM calls, chains, tools, and errors.

Usage (LangChain):
    from zentaxa import ZentaxaClient
    from zentaxa.integrations.langchain import ZentaxaCallbackHandler
    from langchain_openai import ChatOpenAI
    
    client = ZentaxaClient()
    handler = ZentaxaCallbackHandler(client=client, agent_id="my-agent")
    
    llm = ChatOpenAI(callbacks=[handler])
    result = llm.invoke("What is quantum computing?")

Usage (LangGraph):
    from langgraph.graph import StateGraph
    
    graph = StateGraph(state_schema)
    graph.add_node("research", research_node, callbacks=[handler])
    graph.compile()
"""

from typing import Any, Dict, List, Optional
from uuid import uuid4
from datetime import datetime
import time
import logging

try:
    from langchain_core.callbacks.base import BaseCallbackHandler
    from langchain_core.agents import AgentAction, AgentFinish
    from langchain_core.outputs import LLMResult
except ImportError:
    raise ImportError(
        "LangChain not installed. Install with: pip install langchain-core"
    )

from ..client import ZentaxaClient

logger = logging.getLogger(__name__)


class ZentaxaCallbackHandler(BaseCallbackHandler):
    """
    LangChain callback handler for ZENTAXA telemetry.
    
    Captures:
      - LLM calls (prompts, responses, tokens, cost)
      - Chain execution (inputs, outputs, latency)
      - Tool calls (tool name, input, output)
      - Errors and exceptions
    
    Args:
        client: ZentaxaClient instance
        agent_id: Unique identifier for the agent
        framework: Framework name (default: "langchain")
        auto_start: Automatically start agent run (default: True)
    """
    
    def __init__(
        self,
        client: ZentaxaClient,
        agent_id: str,
        framework: str = "langchain",
        auto_start: bool = True
    ):
        super().__init__()
        self.client = client
        self.agent_id = agent_id
        self.framework = framework
        self.run_id: Optional[str] = None
        self.step_counter = 0
        self.step_start_times: Dict[str, float] = {}
        
        # Auto-start agent run
        if auto_start:
            self.start_run()
    
    def start_run(self, metadata: Optional[Dict[str, Any]] = None):
        """Start new agent run"""
        try:
            response = self.client.trace(
                run_id=None,  # Will be generated
                agent_id=self.agent_id,
                framework=self.framework,
                event_type="agent_start",
                metadata=metadata or {}
            )
            self.run_id = response.get("run_id")
            logger.info(f"Started agent run: {self.run_id}")
        except Exception as e:
            logger.error(f"Failed to start run: {e}")
    
    def end_run(self, output: Any = None):
        """End agent run"""
        if not self.run_id:
            return
        
        try:
            self.client.trace(
                run_id=self.run_id,
                agent_id=self.agent_id,
                framework=self.framework,
                event_type="agent_end",
                metadata={"output": str(output) if output else None}
            )
            logger.info(f"Ended agent run: {self.run_id}")
        except Exception as e:
            logger.error(f"Failed to end run: {e}")
    
    # ========================================================================
    # LLM CALLBACKS
    # ========================================================================
    
    def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: List[str],
        **kwargs: Any
    ) -> None:
        """Called when LLM starts"""
        if not self.run_id:
            self.start_run()
        
        try:
            self.step_counter += 1
            step_key = f"llm_{self.step_counter}"
            self.step_start_times[step_key] = time.time()
            
            self.client.agent_event(
                run_id=self.run_id,
                event_type="step_start",
                step_number=self.step_counter,
                step_name=f"LLM Call {self.step_counter}",
                action_type="llm",
                input_data=prompts[0] if prompts else None,
                metadata={
                    "model": serialized.get("name", "unknown"),
                    "prompts_count": len(prompts)
                }
            )
        except Exception as e:
            logger.error(f"on_llm_start error: {e}")
    
    def on_llm_end(
        self,
        response: LLMResult,
        **kwargs: Any
    ) -> None:
        """Called when LLM ends"""
        if not self.run_id:
            return
        
        try:
            step_key = f"llm_{self.step_counter}"
            latency_ms = (time.time() - self.step_start_times.get(step_key, time.time())) * 1000
            
            # Extract tokens and cost
            llm_output = response.llm_output or {}
            tokens_used = llm_output.get("token_usage", {}).get("total_tokens", 0)
            
            # Get first generation text
            output_text = ""
            if response.generations and len(response.generations) > 0:
                output_text = response.generations[0][0].text if response.generations[0] else ""
            
            self.client.agent_event(
                run_id=self.run_id,
                event_type="step_complete",
                step_number=self.step_counter,
                step_name=f"LLM Call {self.step_counter}",
                action_type="llm",
                output_data=output_text,
                latency_ms=latency_ms,
                tokens_used=tokens_used,
                metadata=llm_output
            )
            
            # Send metrics
            self.client.metric(
                run_id=self.run_id,
                metric_name="llm_latency_ms",
                value=latency_ms
            )
            
            if tokens_used:
                self.client.metric(
                    run_id=self.run_id,
                    metric_name="tokens_used",
                    value=float(tokens_used)
                )
        except Exception as e:
            logger.error(f"on_llm_end error: {e}")
    
    def on_llm_error(
        self,
        error: Exception,
        **kwargs: Any
    ) -> None:
        """Called when LLM errors"""
        if not self.run_id:
            return
        
        try:
            self.client.log(
                run_id=self.run_id,
                message=f"LLM error: {str(error)}",
                level="error",
                context={"error_type": type(error).__name__}
            )
        except Exception as e:
            logger.error(f"on_llm_error callback error: {e}")
    
    # ========================================================================
    # CHAIN CALLBACKS
    # ========================================================================
    
    def on_chain_start(
        self,
        serialized: Dict[str, Any],
        inputs: Dict[str, Any],
        **kwargs: Any
    ) -> None:
        """Called when chain starts"""
        if not self.run_id:
            self.start_run(metadata={"input": str(inputs)})
        
        try:
            self.step_counter += 1
            step_key = f"chain_{self.step_counter}"
            self.step_start_times[step_key] = time.time()
            
            chain_name = serialized.get("name", "Unknown Chain")
            
            self.client.agent_event(
                run_id=self.run_id,
                event_type="step_start",
                step_number=self.step_counter,
                step_name=chain_name,
                action_type="plan",
                input_data=str(inputs),
                metadata={"chain_type": serialized.get("_type", "unknown")}
            )
        except Exception as e:
            logger.error(f"on_chain_start error: {e}")
    
    def on_chain_end(
        self,
        outputs: Dict[str, Any],
        **kwargs: Any
    ) -> None:
        """Called when chain ends"""
        if not self.run_id:
            return
        
        try:
            step_key = f"chain_{self.step_counter}"
            latency_ms = (time.time() - self.step_start_times.get(step_key, time.time())) * 1000
            
            self.client.agent_event(
                run_id=self.run_id,
                event_type="step_complete",
                step_number=self.step_counter,
                step_name=f"Chain {self.step_counter}",
                action_type="plan",
                output_data=str(outputs),
                latency_ms=latency_ms
            )
        except Exception as e:
            logger.error(f"on_chain_end error: {e}")
    
    def on_chain_error(
        self,
        error: Exception,
        **kwargs: Any
    ) -> None:
        """Called when chain errors"""
        if not self.run_id:
            return
        
        try:
            self.client.log(
                run_id=self.run_id,
                message=f"Chain error: {str(error)}",
                level="error",
                context={"error_type": type(error).__name__}
            )
        except Exception as e:
            logger.error(f"on_chain_error callback error: {e}")
    
    # ========================================================================
    # TOOL CALLBACKS
    # ========================================================================
    
    def on_tool_start(
        self,
        serialized: Dict[str, Any],
        input_str: str,
        **kwargs: Any
    ) -> None:
        """Called when tool starts"""
        if not self.run_id:
            self.start_run()
        
        try:
            self.step_counter += 1
            step_key = f"tool_{self.step_counter}"
            self.step_start_times[step_key] = time.time()
            
            tool_name = serialized.get("name", "Unknown Tool")
            
            self.client.agent_event(
                run_id=self.run_id,
                event_type="step_start",
                step_number=self.step_counter,
                step_name=tool_name,
                action_type="tool",
                input_data=input_str,
                metadata={"tool_name": tool_name}
            )
        except Exception as e:
            logger.error(f"on_tool_start error: {e}")
    
    def on_tool_end(
        self,
        output: str,
        **kwargs: Any
    ) -> None:
        """Called when tool ends"""
        if not self.run_id:
            return
        
        try:
            step_key = f"tool_{self.step_counter}"
            latency_ms = (time.time() - self.step_start_times.get(step_key, time.time())) * 1000
            
            self.client.agent_event(
                run_id=self.run_id,
                event_type="step_complete",
                step_number=self.step_counter,
                step_name=f"Tool {self.step_counter}",
                action_type="tool",
                output_data=output,
                latency_ms=latency_ms
            )
        except Exception as e:
            logger.error(f"on_tool_end error: {e}")
    
    def on_tool_error(
        self,
        error: Exception,
        **kwargs: Any
    ) -> None:
        """Called when tool errors"""
        if not self.run_id:
            return
        
        try:
            self.client.log(
                run_id=self.run_id,
                message=f"Tool error: {str(error)}",
                level="error",
                context={"error_type": type(error).__name__}
            )
        except Exception as e:
            logger.error(f"on_tool_error callback error: {e}")
    
    # ========================================================================
    # AGENT CALLBACKS
    # ========================================================================
    
    def on_agent_action(
        self,
        action: AgentAction,
        **kwargs: Any
    ) -> None:
        """Called when agent takes action"""
        if not self.run_id:
            return
        
        try:
            self.client.log(
                run_id=self.run_id,
                message=f"Agent action: {action.tool}",
                level="info",
                context={
                    "tool": action.tool,
                    "tool_input": str(action.tool_input),
                    "log": action.log
                }
            )
        except Exception as e:
            logger.error(f"on_agent_action error: {e}")
    
    def on_agent_finish(
        self,
        finish: AgentFinish,
        **kwargs: Any
    ) -> None:
        """Called when agent finishes"""
        if not self.run_id:
            return
        
        try:
            self.end_run(output=finish.return_values)
        except Exception as e:
            logger.error(f"on_agent_finish error: {e}")
