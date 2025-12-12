# ZENTAXA Python SDK

Framework-agnostic observability SDK for multi-agent workflows.

**🚀 Live Platform:** [https://zentaxaapp.azurewebsites.net](https://zentaxaapp.azurewebsites.net)

## Features

- 🔍 **Universal Telemetry**: Unified API for all major frameworks
- 🤖 **5 Framework Integrations**: LangChain, LangGraph, CrewAI, AutoGen, LlamaIndex
- 📊 **Real-time Tracking**: Agent runs, steps, LLM calls, tools
- 🔄 **Multi-Step Visualization**: Track and visualize complex agent pipelines
- 🚀 **Easy Integration**: Add 2 lines of code to your existing agents
- ⚡ **Async Support**: Non-blocking telemetry capture
- 🛡️ **Error Handling**: Automatic retry logic with exponential backoff

## Installation

```bash
pip install zentaxa
```

### Framework-specific installation

```bash
# LangChain / LangGraph
pip install zentaxa[langchain]

# CrewAI
pip install zentaxa[crewai]

# AutoGen
pip install zentaxa[autogen]

# LlamaIndex
pip install zentaxa[llamaindex]

# All frameworks
pip install zentaxa[all]
```

## Quick Start

### Basic Usage

```python
from zentaxa import ZentaxaClient

# Default: connects to https://zentaxaapp.azurewebsites.net
client = ZentaxaClient()

# Start an agent run
response = client.trace(
    run_id=None,
    agent_id="my-agent",
    framework="custom",
    event_type="agent_start",
    metadata={"input": "Your query here"}
)
run_id = response["run_id"]

# Log steps
client.log(run_id, "info", "Processing step 1")

# End the run with results
client.trace(
    run_id=run_id,
    agent_id="my-agent",
    framework="custom",
    event_type="agent_end",
    metadata={
        "input": "Your query",
        "output": "Agent response",
        "steps": [
            {"step_number": 1, "step_name": "Analyze", "input": "...", "output": "...", "latency_ms": 1500, "status": "completed"}
        ],
        "latency_ms": 1500
    }
)
```

### LangChain

```python
from zentaxa import ZentaxaClient
from zentaxa.integrations.langchain import ZentaxaCallbackHandler
from langchain_openai import ChatOpenAI

# Initialize client (default connects to live platform)
client = ZentaxaClient()

# Create callback handler
handler = ZentaxaCallbackHandler(client=client, agent_id="my-agent")

# Use with LangChain
llm = ChatOpenAI(callbacks=[handler])
result = llm.invoke("What is quantum computing?")
```

### LangGraph

```python
from zentaxa.integrations.langgraph import LangGraphObserver
from langgraph.graph import StateGraph

observer = LangGraphObserver(client=client, agent_id="my-graph")

graph = StateGraph(state_schema)
graph.add_node("research", research_node, callbacks=[observer])
graph.add_node("analyze", analyze_node, callbacks=[observer])
compiled = graph.compile()

result = compiled.invoke({"query": "quantum computing"})
```

### CrewAI

```python
from zentaxa.integrations.crewai import CrewAIObserver
from crewai import Crew

observer = CrewAIObserver(client=client, agent_id="research-crew")

# Context manager automatically tracks execution
with observer:
    result = crew.kickoff()
```

### AutoGen

```python
from zentaxa.integrations.autogen import AutoGenTracer
from autogen import UserProxyAgent, AssistantAgent

tracer = AutoGenTracer(client=client, agent_id="autogen-conversation")

with tracer:
    user_proxy.initiate_chat(assistant, message="Research quantum computing")
```

### LlamaIndex

```python
from zentaxa.integrations.llamaindex import LlamaIndexObserver
from llama_index.core.agent import ReActAgent
from llama_index.core.callbacks import CallbackManager

observer = LlamaIndexObserver(client=client, agent_id="llama-agent")
callback_manager = CallbackManager([observer])

agent = ReActAgent.from_tools(
    tools,
    llm=llm,
    callback_manager=callback_manager
)

response = agent.chat("Research quantum computing")
```

## Configuration

### Client Options

```python
client = ZentaxaClient(
    base_url="https://zentaxaapp.azurewebsites.net",  # Default (live platform)
    timeout=10.0,                                      # Request timeout (seconds)
    max_retries=3,                                     # Retry attempts
    async_mode=False                                   # Enable async operations
)
```

### Async Mode

```python
import asyncio

async def main():
    async with ZentaxaClient(async_mode=True) as client:
        await client.trace_async(
            run_id=None,
            agent_id="async-agent",
            framework="langchain",
            event_type="agent_start"
        )

asyncio.run(main())
```

## Manual Telemetry

### Trace Events

```python
# Start agent run
response = client.trace(
    run_id=None,
    agent_id="research-agent",
    framework="langchain",
    event_type="agent_start",
    metadata={"goal": "Research quantum computing"}
)
run_id = response["run_id"]

# End agent run
client.trace(
    run_id=run_id,
    agent_id="research-agent",
    framework="langchain",
    event_type="agent_end",
    metadata={"output": "Research complete"}
)
```

### Log Events

```python
client.log(
    run_id=run_id,
    message="Executing search tool",
    level="info",
    context={"tool_name": "TavilySearch", "input": "quantum computing"}
)
```

### Metric Events

```python
client.metric(
    run_id=run_id,
    metric_name="llm_latency_ms",
    value=2340.5,
    tags={"provider": "openai", "model": "gpt-4"}
)
```

### Agent Events

```python
client.agent_event(
    run_id=run_id,
    event_type="step_complete",
    step_number=1,
    step_name="Plan Research",
    action_type="plan",
    input_data="Research quantum computing",
    output_data="1. Search papers\n2. Analyze trends",
    latency_ms=150,
    cost_usd=0.0001
)
```

## API Reference

### ZentaxaClient

- `trace(run_id, agent_id, framework, event_type, metadata)` - Send trace event
- `log(run_id, message, level, context)` - Send log event
- `metric(run_id, metric_name, value, tags)` - Send metric event
- `agent_event(run_id, event_type, ...)` - Send agent event
- `bulk(events)` - Send multiple events in batch

### Callback Handlers

- `ZentaxaCallbackHandler` - LangChain/LangGraph callback
- `LangGraphObserver` - LangGraph-specific observer
- `CrewAIObserver` - CrewAI wrapper
- `AutoGenTracer` - AutoGen conversation tracker
- `LlamaIndexObserver` - LlamaIndex event handler

## Development

```bash
# Clone repository
git clone https://github.com/zentaxa/zentaxa-sdk

# Install dependencies
cd zentaxa-sdk/sdk/python
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black zentaxa/
```

## License

MIT License - see LICENSE file for details.

## Support

- Live Platform: [https://zentaxaapp.azurewebsites.net](https://zentaxaapp.azurewebsites.net)
- Dashboard: [https://zentaxaapp.azurewebsites.net/dashboard](https://zentaxaapp.azurewebsites.net/dashboard)
- Pipeline Explorer: [https://zentaxaapp.azurewebsites.net/pipeline](https://zentaxaapp.azurewebsites.net/pipeline)
- Issues: https://github.com/CoderInWaves/Startup-MVP/issues
- Email: support@zentaxa.me

## Version

1.0.1
