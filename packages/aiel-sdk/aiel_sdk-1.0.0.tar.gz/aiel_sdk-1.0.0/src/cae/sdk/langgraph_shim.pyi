from __future__ import annotations
from typing import Any, Callable, Dict, Mapping, Optional, Protocol, Sequence, Tuple, TypedDict, TypeVar, Union

START: str
END: str

# A practical "messages state" contract that works across IDEs.
class Message(TypedDict, total=False):
    role: str
    content: str
    name: str
    tool_call_id: str

class MessagesState(TypedDict, total=False):
    messages: list[Message]
    # allow extra keys in runtime
    __extra__: Dict[str, Any]

State = Mapping[str, Any]
NodeFn = Callable[[State], Mapping[str, Any]]

class InMemorySaver: ...
class RetryPolicy: ...
class CachePolicy: ...

class ToolNode:
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

def tools_condition(*args: Any, **kwargs: Any) -> str: ...

class CompiledGraph(Protocol):
    def invoke(self, state: State, config: Optional[dict] = ...) -> Dict[str, Any]: ...
    async def ainvoke(self, state: State, config: Optional[dict] = ...) -> Dict[str, Any]: ...

ConditionFn = Callable[[State], str]

class StateGraph:
    def __init__(self, state_schema: Any = ...) -> None: ...

    def add_node(
        self,
        name: str,
        node: NodeFn,
        *,
        defer: bool = ...,
        metadata: Optional[dict[str, Any]] = ...,
        input_schema: Any = ...,
        retry_policy: RetryPolicy | Sequence[RetryPolicy] | None = ...,
        cache_policy: CachePolicy | None = ...,
        destinations: dict[str, str] | Tuple[str, ...] | None = ...,
        **kwargs: Any,
    ) -> StateGraph: ...

    def add_edge(self, src: str, dst: str) -> StateGraph: ...

    def add_conditional_edges(
        self,
        source: str,
        condition: Callable[[State], str],
        path_map: Optional[dict[str, str]] = ...,
        **kwargs: Any,
    ) -> StateGraph: ...

    def compile(self, checkpointer: Any = ..., **kwargs: Any) -> CompiledGraph: ...