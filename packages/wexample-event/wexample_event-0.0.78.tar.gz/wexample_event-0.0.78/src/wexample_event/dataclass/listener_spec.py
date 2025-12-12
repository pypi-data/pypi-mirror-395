from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ListenerSpec:
    name: str
    once: bool
    priority: int
