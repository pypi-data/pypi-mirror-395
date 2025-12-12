from __future__ import annotations
from typing import Any, List, Optional

class ChatPromptTemplate:
    @classmethod
    def from_messages(cls, messages: List[Any]):
        return cls()
    def format_messages(self, **kwargs: Any) -> List[Any]:
        return []

class PromptTemplate:
    def __init__(self, template: str = "", **kwargs: Any):
        self.template = template
    def format(self, **kwargs: Any) -> str:
        return self.template

class RunnableConfig:
    def __init__(self, **kwargs: Any):
        self.metadata = kwargs

class Runnable:
    def invoke(self, input: Any, config: Optional[RunnableConfig] = None) -> Any:
        raise RuntimeError("Runnable is a contract shim. Execution happens server-side.")
