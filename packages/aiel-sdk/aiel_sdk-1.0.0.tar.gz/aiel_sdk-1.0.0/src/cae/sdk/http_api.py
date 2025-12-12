from __future__ import annotations
from typing import Callable

from .registry import ExportRegistry
from .exports import HttpHandlerExport

class http:
    @staticmethod
    def get(path: str):
        def decorator(fn: Callable):
            ExportRegistry.http_handlers.append(HttpHandlerExport(method="GET", path=path, fn=fn))
            return fn
        return decorator

    @staticmethod
    def post(path: str):
        def decorator(fn: Callable):
            ExportRegistry.http_handlers.append(HttpHandlerExport(method="POST", path=path, fn=fn))
            return fn
        return decorator
