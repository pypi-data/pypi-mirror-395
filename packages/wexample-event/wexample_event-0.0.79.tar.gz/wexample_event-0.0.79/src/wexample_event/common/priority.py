from __future__ import annotations

from enum import IntEnum


class EventPriority(IntEnum):
    """Convenience priorities for event listeners."""

    LOW = -100
    NORMAL = 0
    HIGH = 100


DEFAULT_PRIORITY: EventPriority = EventPriority.NORMAL
