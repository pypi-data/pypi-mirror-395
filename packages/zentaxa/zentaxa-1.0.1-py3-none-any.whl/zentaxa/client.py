"""
ZENTAXA HTTP Client
===================

Core HTTP client for telemetry ingestion.
Handles async/sync requests with retry logic and error handling.

OPTIMIZED: Pre-compiled serialization, connection pooling, reduced allocations.
"""

import httpx
import asyncio
import uuid
from typing import Optional, Dict, Any, List, Union
from datetime import datetime, timezone
from enum import Enum
import logging

logger = logging.getLogger(__name__)


# Pre-compiled datetime type for O(1) isinstance check
_DATETIME_TYPE = datetime


def _serialize_value(obj: Any) -> Any:
    """Optimized serialization with type-based dispatch"""
    obj_type = type(obj)
    
    if obj_type is _DATETIME_TYPE:
        return obj.isoformat()
    elif obj_type is dict:
        return {k: _serialize_value(v) for k, v in obj.items()}
    elif obj_type is list:
        return [_serialize_value(item) for item in obj]
    return obj


class EventType(str, Enum):
    """Telemetry event types"""
    TRACE = "trace"
    LOG = "log"
    METRIC = "metric"
    AGENT_EVENT = "agent_event"


class ZentaxaClient:
    """
    HTTP client for ZENTAXA telemetry ingestion.
    
    Supports both sync and async operations with automatic retry logic.
    
    Args:
        base_url: ZENTAXA backend URL (default: https://zentaxaapp.azurewebsites.net)
        timeout: Request timeout in seconds (default: 10)
        max_retries: Maximum retry attempts (default: 3)
        async_mode: Enable async operations (default: False)
    
    Example:
        client = ZentaxaClient()
        client.trace(
            run_id=None,
            agent_id="research-agent",
            framework="langchain",
            event_type="agent_start"
        )
    """
    
    def __init__(
        self,
        base_url: str = "https://zentaxaapp.azurewebsites.net",
        api_key: Optional[str] = None,
        timeout: float = 10.0,
        max_retries: int = 3,
        async_mode: bool = False
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.async_mode = async_mode
        
        # Initialize sync HTTP client with auth header
        headers = {"X-API-Key": api_key} if api_key else {}
        self._client = httpx.Client(timeout=timeout, headers=headers)
        # Async client created lazily on first async call
        self._async_client = None
        
        logger.info(f"ZentaxaClient initialized: {base_url}")
    
    def __del__(self):
        """Cleanup HTTP client"""
        if hasattr(self, "_client") and self._client:
            try:
                self._client.close()
            except:
                pass
        # Async client cleanup handled by context manager
    
    # ========================================================================
    # TRACE EVENTS
    # ========================================================================
    
    def trace(
        self,
        run_id: Optional[str],
        agent_id: str,
        framework: str,
        event_type: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Send trace event (agent lifecycle).
        
        Args:
            run_id: Agent run ID (None for new runs)
            agent_id: Unique agent identifier
            framework: Framework name (langchain, crewai, etc.)
            event_type: agent_start, agent_end, agent_error
            metadata: Additional context
        
        Returns:
            Response with run_id and status
        """
        payload = {
            "run_id": run_id,
            "agent_id": agent_id,
            "framework": framework,
            "event_type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "metadata": metadata or {}
        }
        
        return self._post("/v1/trace", payload)
    
    async def trace_async(
        self,
        run_id: Optional[str],
        agent_id: str,
        framework: str,
        event_type: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Async version of trace()"""
        payload = {
            "run_id": run_id,
            "agent_id": agent_id,
            "framework": framework,
            "event_type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "metadata": metadata or {}
        }
        
        return await self._post_async("/v1/trace", payload)
    
    # ========================================================================
    # LOG EVENTS
    # ========================================================================
    
    def log(
        self,
        run_id: str,
        message: str,
        level: str = "info",
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Send log event.
        
        Args:
            run_id: Agent run ID
            message: Log message
            level: Log level (debug, info, warning, error)
            context: Additional context
        
        Returns:
            Response with status
        """
        payload = {
            "run_id": run_id,
            "level": level,
            "message": message,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "context": context or {}
        }
        
        return self._post("/v1/log", payload)
    
    async def log_async(
        self,
        run_id: str,
        message: str,
        level: str = "info",
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Async version of log()"""
        payload = {
            "run_id": run_id,
            "level": level,
            "message": message,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "context": context or {}
        }
        
        return await self._post_async("/v1/log", payload)
    
    # ========================================================================
    # METRIC EVENTS
    # ========================================================================
    
    def metric(
        self,
        run_id: str,
        metric_name: str,
        value: float,
        tags: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Send metric event.
        
        Args:
            run_id: Agent run ID
            metric_name: Metric name (llm_latency_ms, cost_usd, etc.)
            value: Metric value
            tags: Tags for categorization
        
        Returns:
            Response with status
        """
        payload = {
            "run_id": run_id,
            "metric_name": metric_name,
            "value": value,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tags": tags or {}
        }
        
        return self._post("/v1/metrics", payload)
    
    async def metric_async(
        self,
        run_id: str,
        metric_name: str,
        value: float,
        tags: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Async version of metric()"""
        payload = {
            "run_id": run_id,
            "metric_name": metric_name,
            "value": value,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tags": tags or {}
        }
        
        return await self._post_async("/v1/metrics", payload)
    
    # ========================================================================
    # AGENT EVENTS
    # ========================================================================
    
    def agent_event(
        self,
        run_id: str,
        event_type: str,
        step_number: Optional[int] = None,
        step_name: Optional[str] = None,
        action_type: str = "tool",
        input_data: Any = None,
        output_data: Any = None,
        latency_ms: Optional[float] = None,
        cost_usd: Optional[float] = None,
        tokens_used: Optional[int] = None,
        related_llm_call_ids: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Send agent event (steps, state changes).
        
        Args:
            run_id: Agent run ID
            event_type: step_start, step_complete, state_change
            step_number: Step index
            step_name: Human-readable step name
            action_type: tool, llm, plan, reason, retrieve, search, code
            input_data: Step input
            output_data: Step output
            latency_ms: Step latency
            cost_usd: Step cost
            tokens_used: Tokens consumed
            related_llm_call_ids: Associated LLM call IDs
            metadata: Additional context
        
        Returns:
            Response with status and step_id
        """
        payload = {
            "run_id": run_id,
            "event_type": event_type,
            "step_number": step_number,
            "step_name": step_name,
            "action_type": action_type,
            "input_data": input_data,
            "output_data": output_data,
            "latency_ms": latency_ms,
            "cost": cost_usd,  # Backend expects 'cost' not 'cost_usd'
            "tokens_used": tokens_used,
            "related_llm_call_ids": related_llm_call_ids or [],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "metadata": metadata or {}
        }
        
        return self._post("/v1/agent-event", payload)
    
    async def agent_event_async(
        self,
        run_id: str,
        event_type: str,
        step_number: Optional[int] = None,
        step_name: Optional[str] = None,
        action_type: str = "tool",
        input_data: Any = None,
        output_data: Any = None,
        latency_ms: Optional[float] = None,
        cost_usd: Optional[float] = None,
        tokens_used: Optional[int] = None,
        related_llm_call_ids: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Async version of agent_event()"""
        payload = {
            "run_id": run_id,
            "event_type": event_type,
            "step_number": step_number,
            "step_name": step_name,
            "action_type": action_type,
            "input_data": input_data,
            "output_data": output_data,
            "latency_ms": latency_ms,
            "cost": cost_usd,  # Backend expects 'cost' not 'cost_usd'
            "tokens_used": tokens_used,
            "related_llm_call_ids": related_llm_call_ids or [],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "metadata": metadata or {}
        }
        
        return await self._post_async("/v1/agent-event", payload)
    
    # ========================================================================
    # BULK OPERATIONS
    # ========================================================================
    
    def bulk(self, events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Send multiple events in bulk.
        
        Args:
            events: List of events with 'type' and 'data' keys
        
        Returns:
            Response with batch status
        """
        payload = {"events": events}
        return self._post("/v1/bulk", payload)
    
    async def bulk_async(self, events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Async version of bulk()"""
        payload = {"events": events}
        return await self._post_async("/v1/bulk", payload)
    
    # ========================================================================
    # INTERNAL HELPERS - OPTIMIZED
    # ========================================================================
    
    def _post(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Sync POST with retry logic - optimized serialization"""
        url = f"{self.base_url}{endpoint}"
        
        # Optimized datetime serialization
        serialized_payload = _serialize_value(payload)
        
        last_exception = None
        for attempt in range(self.max_retries):
            try:
                response = self._client.post(url, json=serialized_payload)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    logger.warning(f"Request failed (attempt {attempt + 1}/{self.max_retries}): {e}")
                else:
                    logger.error(f"Failed to send telemetry after {self.max_retries} attempts")
                    raise
        
        raise last_exception or httpx.RequestError("Max retries exceeded")
    
    async def _post_async(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Async POST with retry logic - lazy client initialization"""
        # Lazy async client creation
        if self._async_client is None:
            headers = {"X-API-Key": self.api_key} if self.api_key else {}
            self._async_client = httpx.AsyncClient(timeout=self.timeout, headers=headers)
        
        url = f"{self.base_url}{endpoint}"
        serialized_payload = _serialize_value(payload)
        
        last_exception = None
        for attempt in range(self.max_retries):
            try:
                response = await self._async_client.post(url, json=serialized_payload)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    logger.warning(f"Request failed (attempt {attempt + 1}/{self.max_retries}): {e}")
                else:
                    logger.error(f"Failed to send telemetry after {self.max_retries} attempts")
                    raise
        
        raise last_exception or httpx.RequestError("Max retries exceeded")
    
    # ========================================================================
    # CONTEXT MANAGER
    # ========================================================================
    
    def __enter__(self):
        """Sync context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Sync context manager exit"""
        self._client.close()
    
    async def __aenter__(self):
        """Async context manager entry"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self._async_client:
            await self._async_client.aclose()
            self._async_client = None
