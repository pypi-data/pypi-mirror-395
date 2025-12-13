"""Types used in `click_extended`."""

from typing import Any, Callable

from click_extended.core.other.context import Context

Decorator = Callable[[Callable[..., Any]], Callable[..., Any]]

__all__ = [
    "Context",
    "Decorator",
]
