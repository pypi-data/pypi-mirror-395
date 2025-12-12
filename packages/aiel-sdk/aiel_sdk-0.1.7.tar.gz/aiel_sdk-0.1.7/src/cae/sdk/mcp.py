from __future__ import annotations
from typing import Any, Callable, List

from .registry import ExportRegistry
from .exports import McpServerExport

class CaeMcpServer:
    def __init__(self, name: str):
        self.name = name
        server = ExportRegistry.mcp_servers.get(name)
        if server is None:
            server = McpServerExport(name=name, tools=[])
            ExportRegistry.mcp_servers[name] = server

    @property
    def _server_export(self) -> McpServerExport:
        return ExportRegistry.mcp_servers[self.name]

    def tool(self, name: str | None = None):
        def decorator(fn: Callable[..., Any]):
            tool_name = name or fn.__name__

            if tool_name not in self._server_export.tools:
                self._server_export.tools.append(tool_name)

            ExportRegistry.mcp_tool_fns[(self.name, tool_name)] = fn
            return fn
        return decorator

def mcp_server(name: str, tools: List[str] | None = None) -> CaeMcpServer:
    server = ExportRegistry.mcp_servers.get(name)
    if server is None:
        server = McpServerExport(name=name, tools=[])
        ExportRegistry.mcp_servers[name] = server

    if tools:
        for t in tools:
            if t not in server.tools:
                server.tools.append(t)

    return CaeMcpServer(name)
