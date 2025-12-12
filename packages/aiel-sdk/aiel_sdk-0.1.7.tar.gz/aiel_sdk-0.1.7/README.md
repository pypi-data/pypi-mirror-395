# aiel-sdk

Local contract SDK for AI Execution Layer.

This package is intentionally lightweight: it provides importable contracts and typing
for code that executes on the AI Execution Layer runtime (server-side).

Example:

```py
from cae.sdk import (
  StateGraph, START, END, InMemorySaver,
  tools_condition, ToolNode,
  ChatPromptTemplate, PromptTemplate, Runnable, RunnableConfig,
  tool, agent, flow, flow_graph, http, mcp_server
)
```

## Status
![PyPI](https://img.shields.io/pypi/v/aiel-cli)
Backend integration: not implemented yet (planned per sprint output)