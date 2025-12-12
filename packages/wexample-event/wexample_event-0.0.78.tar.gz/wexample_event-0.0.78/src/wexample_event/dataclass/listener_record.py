from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from .event import Event

EventCallback = Callable[[Event], Awaitable[None] | None]


@dataclass(slots=True)
class ListenerRecord:
    callback: EventCallback
    once: bool
    order: int
    priority: int
