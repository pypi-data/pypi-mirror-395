from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Tuple

from .exports import ToolExport, AgentExport, FlowExport, HttpHandlerExport, McpServerExport

@dataclass
class ExportRegistry:
    tools: Dict[str, ToolExport] = field(default_factory=dict)
    agents: Dict[str, AgentExport] = field(default_factory=dict)
    flows: Dict[str, FlowExport] = field(default_factory=dict)
    http_handlers: List[HttpHandlerExport] = field(default_factory=list)
    mcp_servers: Dict[str, McpServerExport] = field(default_factory=dict)
    mcp_tool_fns: Dict[Tuple[str, str], Callable[..., Any]] = field(default_factory=dict)
