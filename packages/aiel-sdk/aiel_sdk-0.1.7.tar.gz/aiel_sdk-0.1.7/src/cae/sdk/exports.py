from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, List, Optional

@dataclass
class ToolExport:
    name: str
    fn: Callable[..., Any]

@dataclass
class AgentExport:
    name: str
    fn: Callable[..., Any]

@dataclass
class FlowExport:
    name: str
    fn: Optional[Callable[..., Any]]
    graph_builder: Optional[Callable[..., Any]]

@dataclass
class HttpHandlerExport:
    method: str
    path: str
    fn: Callable[..., Any]

@dataclass
class McpServerExport:
    name: str
    tools: List[str]
