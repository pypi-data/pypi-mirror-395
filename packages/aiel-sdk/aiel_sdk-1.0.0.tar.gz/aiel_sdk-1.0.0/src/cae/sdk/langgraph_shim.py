from typing import Any, Dict, List, Tuple
# Contract shim — real execution happens server-side.
START = "__start__"
END = "__end__"

class InMemorySaver:
    def __init__(self, *_, **__): ...

class ToolNode:
    def __init__(self, *_, **__): ...

def tools_condition(*args, **kwargs):
    # In real LangGraph this routes tool-calls vs continue.
    # Here we only provide a stable contract surface.
    return "continue"

class CompiledGraph:
    def invoke(self, state, config=None):
        return state

    async def ainvoke(self, state, config=None):
        return state

class StateGraph:
    def __init__(self, state_schema=None):
        self.state_schema = state_schema
        self._nodes: Dict[str, Tuple[Any, Dict[str, Any]]] = {}
        self._edges: List[Tuple[str, str]] = []
        self._conditionals: List[Dict[str, Any]] = []

    def add_node(self, name, node, **kwargs):
        self._nodes[name] = (node, dict(kwargs))
        return self

    def add_edge(self, src, dst):
        self._edges.append((src, dst))
        return self

    def add_conditional_edges(self, source, condition, path_map=None, **kwargs):
        self._conditionals.append(
            {"source": source, "condition": condition, "path_map": path_map, "kwargs": dict(kwargs)}
        )
        return self

    def compile(self, checkpointer=None, **kwargs):
        return CompiledGraph()