"""
ZENTAXA Framework Integrations
===============================

Auto-instrumentation for popular agent frameworks:
  - LangChain / LangGraph
  - CrewAI
  - AutoGen
  - LlamaIndex

Note: Each integration is imported lazily to avoid requiring all frameworks.
Import only the integrations you need:

    from zentaxa.integrations.langchain import ZentaxaCallbackHandler
    from zentaxa.integrations.crewai import CrewAIObserver
    from zentaxa.integrations.autogen import AutoGenTracer
    from zentaxa.integrations.llamaindex import LlamaIndexObserver
"""

__all__ = [
    "ZentaxaCallbackHandler",
    "CrewAIObserver", 
    "AutoGenTracer",
    "LlamaIndexObserver"
]
