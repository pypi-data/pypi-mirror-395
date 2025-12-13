"""
Adapter utilities for NyxBox.

Adapters provide a common interface so that different kinds of models
(local functions, remote APIs, or custom logic) can be used with the
same experiment runner.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable


class BaseAdapter(ABC):
    """
    Base class for model adapters.

    Subclasses should implement __call__ and return the model output
    as a string.
    """

    def __init__(self, name: str | None = None) -> None:
        self.name: str = name or self.__class__.__name__

    @abstractmethod
    def __call__(self, prompt: str) -> str:
        """
        Run the adapter on a single prompt and return the output text.
        """
        raise NotImplementedError


class FunctionAdapter(BaseAdapter):
    """
    Adapter that wraps a simple callable.

    This allows any function that takes a prompt string and returns
    a string to be used as an adapter.
    """

    def __init__(
        self,
        fn: Callable[[str], str],
        name: str | None = None,
    ) -> None:
        adapter_name = name or getattr(fn, "__name__", "function_adapter")
        super().__init__(name=adapter_name)
        self._fn: Callable[[str], str] = fn

    def __call__(self, prompt: str) -> str:
        return self._fn(prompt)
