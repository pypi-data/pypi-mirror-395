# Contract shim — real execution happens server-side.
START = "__start__"
END = "__end__"

class InMemorySaver:
    def __init__(self, *_, **__): ...

class ToolNode:
    def __init__(self, *_, **__): ...

def tools_condition(*args, **kwargs):
    return "continue"

class CompiledGraph:
    def invoke(self, state, config=None):
        return state

    async def ainvoke(self, state, config=None):
        return state

class StateGraph:
    def __init__(self, state_type=None): ...
    def add_node(self, name, node): return self
    def add_edge(self, src, dst): return self
    def add_conditional_edges(self, source, condition, path_map=None): return self
    def compile(self, checkpointer=None): return CompiledGraph()
