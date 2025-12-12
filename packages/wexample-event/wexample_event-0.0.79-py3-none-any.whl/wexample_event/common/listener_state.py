from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wexample_event.dataclass.listener_record import EventCallback


class ListenerState:
    bindings: list[tuple[str, EventCallback]]
    dispatcher: EventDispatcherMixin | None  # type: ignore[name-defined]

    def __init__(self) -> None:
        self.dispatcher = None
        self.bindings = []
