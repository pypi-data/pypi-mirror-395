from __future__ import annotations
from typing import Any, Callable

from .registry import ExportRegistry
from .exports import ToolExport, AgentExport, FlowExport

def tool(name: str):
    def decorator(fn: Callable[..., Any]):
        ExportRegistry.tools[name] = ToolExport(name=name, fn=fn)
        return fn
    return decorator

def agent(name: str):
    def decorator(fn: Callable[..., Any]):
        ExportRegistry.agents[name] = AgentExport(name=name, fn=fn)
        return fn
    return decorator

def flow(name: str):
    def decorator(fn: Callable[..., Any]):
        ExportRegistry.flows[name] = FlowExport(name=name, fn=fn, graph_builder=None)
        return fn
    return decorator

def flow_graph(name: str, builder: Callable[..., Any]):
    ExportRegistry.flows[name] = FlowExport(name=name, fn=None, graph_builder=builder)
    return builder
