"""
LangGraph Integration
=====================

Extended ZentaxaCallbackHandler for LangGraph-specific events.
Captures graph state transitions, node executions, and edges.

Usage:
    from zentaxa import ZentaxaClient
    from zentaxa.integrations.langgraph import LangGraphObserver
    from langgraph.graph import StateGraph
    
    client = ZentaxaClient()
    observer = LangGraphObserver(client=client, agent_id="my-graph")
    
    graph = StateGraph(state_schema)
    graph.add_node("research", research_node, callbacks=[observer])
    graph.add_node("analyze", analyze_node, callbacks=[observer])
    compiled = graph.compile()
    
    result = compiled.invoke({"query": "quantum computing"})
"""

from typing import Any, Dict, Optional
from .langchain import ZentaxaCallbackHandler
from ..client import ZentaxaClient
import logging

logger = logging.getLogger(__name__)


class LangGraphObserver(ZentaxaCallbackHandler):
    """
    LangGraph observer extending LangChain callback handler.
    
    Additional capabilities:
      - Node transition tracking
      - Graph state snapshots
      - Edge execution logging
      - Conditional routing capture
    
    Args:
        client: ZentaxaClient instance
        agent_id: Unique identifier for the graph
        track_state: Capture full state at each node (default: True)
    """
    
    def __init__(
        self,
        client: ZentaxaClient,
        agent_id: str,
        track_state: bool = True,
        **kwargs
    ):
        super().__init__(
            client=client,
            agent_id=agent_id,
            framework="langgraph",
            **kwargs
        )
        self.track_state = track_state
        self.node_sequence: list = []
        self.current_state: Optional[Dict[str, Any]] = None
    
    def on_node_start(
        self,
        node_name: str,
        input_state: Dict[str, Any],
        **kwargs: Any
    ) -> None:
        """Called when graph node starts"""
        if not self.run_id:
            self.start_run(metadata={"initial_state": str(input_state)})
        
        try:
            self.step_counter += 1
            self.node_sequence.append(node_name)
            
            if self.track_state:
                self.current_state = input_state
            
            self.client.agent_event(
                run_id=self.run_id,
                event_type="step_start",
                step_number=self.step_counter,
                step_name=f"Node: {node_name}",
                action_type="plan",
                input_data=str(input_state) if self.track_state else node_name,
                metadata={
                    "node_name": node_name,
                    "node_sequence": self.node_sequence,
                    "graph_type": "langgraph"
                }
            )
            
            self.client.log(
                run_id=self.run_id,
                message=f"Entering node: {node_name}",
                level="info",
                context={"node_sequence": self.node_sequence}
            )
        except Exception as e:
            logger.error(f"on_node_start error: {e}")
    
    def on_node_end(
        self,
        node_name: str,
        output_state: Dict[str, Any],
        **kwargs: Any
    ) -> None:
        """Called when graph node ends"""
        if not self.run_id:
            return
        
        try:
            self.client.agent_event(
                run_id=self.run_id,
                event_type="step_complete",
                step_number=self.step_counter,
                step_name=f"Node: {node_name}",
                action_type="plan",
                output_data=str(output_state) if self.track_state else node_name,
                metadata={
                    "node_name": node_name,
                    "state_changes": self._compare_states(self.current_state, output_state) if self.track_state else None
                }
            )
            
            if self.track_state:
                self.current_state = output_state
        except Exception as e:
            logger.error(f"on_node_end error: {e}")
    
    def on_edge_taken(
        self,
        source_node: str,
        target_node: str,
        condition: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """Called when graph takes an edge"""
        if not self.run_id:
            return
        
        try:
            self.client.log(
                run_id=self.run_id,
                message=f"Edge: {source_node} → {target_node}",
                level="info",
                context={
                    "source": source_node,
                    "target": target_node,
                    "condition": condition,
                    "edge_type": "conditional" if condition else "direct"
                }
            )
        except Exception as e:
            logger.error(f"on_edge_taken error: {e}")
    
    def _compare_states(
        self,
        old_state: Optional[Dict[str, Any]],
        new_state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compare two states and return differences"""
        if not old_state:
            return {"type": "initial_state"}
        
        changes = {}
        for key in new_state.keys():
            if key not in old_state:
                changes[key] = {"action": "added", "value": new_state[key]}
            elif old_state[key] != new_state[key]:
                changes[key] = {
                    "action": "modified",
                    "old": old_state[key],
                    "new": new_state[key]
                }
        
        for key in old_state.keys():
            if key not in new_state:
                changes[key] = {"action": "removed", "old_value": old_state[key]}
        
        return changes
