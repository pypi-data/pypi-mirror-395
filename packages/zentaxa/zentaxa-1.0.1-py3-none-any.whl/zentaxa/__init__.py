"""
ZENTAXA Python SDK
==================

Framework-agnostic observability SDK for multi-agent workflows.

Supported Frameworks:
  - LangChain / LangGraph
  - CrewAI
  - AutoGen
  - LlamaIndex

Usage:
    from zentaxa import ZentaxaClient
    from zentaxa.integrations.langchain import ZentaxaCallbackHandler
    
    # Default: connects to https://zentaxaapp.azurewebsites.net
    client = ZentaxaClient()
    handler = ZentaxaCallbackHandler(client=client, agent_id="my-agent")
    
    # Use with LangChain
    llm = ChatOpenAI(callbacks=[handler])

Installation:
    pip install zentaxa

Version: 1.0.1
"""

from .client import ZentaxaClient

__version__ = "1.0.1"
__all__ = ["ZentaxaClient"]

# Lazy loading for framework integrations - import only when needed
def __getattr__(name):
    if name == "ZentaxaCallbackHandler":
        from .integrations.langchain import ZentaxaCallbackHandler
        return ZentaxaCallbackHandler
    elif name == "LangGraphObserver":
        from .integrations.langgraph import LangGraphObserver
        return LangGraphObserver
    elif name == "CrewAIObserver":
        from .integrations.crewai import CrewAIObserver
        return CrewAIObserver
    elif name == "AutoGenTracer":
        from .integrations.autogen import AutoGenTracer
        return AutoGenTracer
    elif name == "LlamaIndexObserver":
        from .integrations.llamaindex import LlamaIndexObserver
        return LlamaIndexObserver
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
