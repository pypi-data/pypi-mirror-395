from __future__ import annotations

import inspect
import threading
from collections.abc import Mapping
from itertools import count
from typing import Any, ClassVar

from wexample_event.common.priority import DEFAULT_PRIORITY, EventPriority
from wexample_event.dataclass.event import Event
from wexample_event.dataclass.listener_record import EventCallback, ListenerRecord


class EventDispatcherMixin:
    """Mixin providing a lightweight observer pattern implementation."""

    _LISTENERS_ATTR: ClassVar[str] = "_event_listeners"
    _LOCK_ATTR: ClassVar[str] = "_event_listener_lock"
    _ORDER_ATTR: ClassVar[str] = "_event_listener_order"
    _UNSET: ClassVar[object] = object()
    _enable_bubbling: ClassVar[bool] = False

    def add_event_listener(
        self,
        name: str,
        callback: EventCallback,
        *,
        once: bool = False,
        priority: int | EventPriority = DEFAULT_PRIORITY,
    ) -> None:
        """Register a callback for the given event name."""
        if not callable(callback):
            raise TypeError("callback must be callable")

        listeners, lock, order_seq = self._ensure_dispatcher_state()
        record = ListenerRecord(
            callback=callback,
            once=once,
            priority=int(priority),
            order=next(order_seq),
        )

        with lock:
            bucket = listeners.setdefault(name, [])
            bucket.append(record)
            bucket.sort(key=lambda item: (-item.priority, item.order))

    def clear_event_listeners(self, name: str | None = None) -> None:
        """Remove all listeners. When name is provided, only that event is cleared."""
        listeners, lock, _ = self._ensure_dispatcher_state()

        with lock:
            if name is None:
                listeners.clear()
            else:
                listeners.pop(name, None)

    def dispatch(
        self,
        event: Event | str,
        *,
        payload: Mapping[str, Any] | None = None,
        metadata: Mapping[str, Any] | None = None,
        source: Any | object = _UNSET,
    ) -> Event:
        """Synchronously dispatch an event to all registered listeners."""
        listeners = self._snapshot_listeners(
            event, payload=payload, metadata=metadata, source=source
        )
        dispatched_event, records = listeners

        callbacks_to_remove: list[tuple[str, EventCallback]] = []
        for name, record in records:
            result = record.callback(dispatched_event)
            if inspect.isawaitable(result):
                raise RuntimeError(
                    "Listener returned an awaitable; use dispatch_async for async listeners"
                )
            if record.once:
                callbacks_to_remove.append((name, record.callback))

        for name, callback in callbacks_to_remove:
            self.remove_event_listener(name, callback)

        # Bubble event to parent if enabled
        if self._enable_bubbling:
            parent = self._get_bubbling_parent()
            if parent:
                parent.dispatch(dispatched_event)

        return dispatched_event

    async def dispatch_async(
        self,
        event: Event | str,
        *,
        payload: Mapping[str, Any] | None = None,
        metadata: Mapping[str, Any] | None = None,
        source: Any | object = _UNSET,
    ) -> Event:
        """Asynchronously dispatch an event, awaiting coroutine listeners."""
        listeners = self._snapshot_listeners(
            event, payload=payload, metadata=metadata, source=source
        )
        dispatched_event, records = listeners

        callbacks_to_remove: list[tuple[str, EventCallback]] = []
        for name, record in records:
            result = record.callback(dispatched_event)
            if inspect.isawaitable(result):
                await result
            if record.once:
                callbacks_to_remove.append((name, record.callback))

        for name, callback in callbacks_to_remove:
            self.remove_event_listener(name, callback)

        # Bubble event to parent if enabled
        if self._enable_bubbling:
            parent = self._get_bubbling_parent()
            if parent:
                await parent.dispatch_async(dispatched_event)

        return dispatched_event

    def dispatch_event(
        self,
        event: Event | str,
        *,
        payload: Mapping[str, Any] | None = None,
        metadata: Mapping[str, Any] | None = None,
        source: Any | object = _UNSET,
    ) -> Event:
        """Alias for dispatch to mirror other frameworks' APIs."""
        return self.dispatch(event, payload=payload, metadata=metadata, source=source)

    async def dispatch_event_async(
        self,
        event: Event | str,
        *,
        payload: Mapping[str, Any] | None = None,
        metadata: Mapping[str, Any] | None = None,
        source: Any | object = _UNSET,
    ) -> Event:
        """Alias for dispatch_async for readability."""
        return await self.dispatch_async(
            event, payload=payload, metadata=metadata, source=source
        )

    def has_event_listeners(self, name: str) -> bool:
        listeners, lock, _ = self._ensure_dispatcher_state()
        with lock:
            return bool(listeners.get(name))

    def remove_event_listener(
        self,
        name: str,
        callback: EventCallback,
    ) -> bool:
        """Remove a previously registered callback. Returns True if removed."""
        listeners, lock, _ = self._ensure_dispatcher_state()

        with lock:
            bucket = listeners.get(name)
            if not bucket:
                return False

            initial_length = len(bucket)
            bucket[:] = [
                record
                for record in bucket
                if not (record.callback is callback or record.callback == callback)
            ]
            if not bucket:
                listeners.pop(name, None)
            return len(bucket) != initial_length

    def _coerce_event(
        self,
        event: Event | str,
        *,
        payload: Mapping[str, Any] | None,
        metadata: Mapping[str, Any] | None,
        source: Any | object,
    ) -> Event:
        if isinstance(event, Event):
            if payload is not None or metadata is not None or source is not self._UNSET:
                raise ValueError(
                    "Event instance cannot be combined with payload/metadata/source overrides"
                )
            return event

        resolved_source = self if source is self._UNSET else source
        return Event(
            name=event, payload=payload, metadata=metadata, source=resolved_source
        )

    def _ensure_dispatcher_state(
        self,
    ) -> tuple[dict[str, list[ListenerRecord]], threading.RLock, count]:
        if not hasattr(self, self._LISTENERS_ATTR):
            setattr(self, self._LISTENERS_ATTR, {})
            setattr(self, self._LOCK_ATTR, threading.RLock())
            setattr(self, self._ORDER_ATTR, count())
        return (
            getattr(self, self._LISTENERS_ATTR),
            getattr(self, self._LOCK_ATTR),
            getattr(self, self._ORDER_ATTR),
        )

    def _get_bubbling_parent(self) -> EventDispatcherMixin | None:
        """Override this method to return the parent dispatcher for event bubbling.

        Returns:
            The parent dispatcher to bubble events to, or None if no parent exists.

        Example:
            class FileNode(EventDispatcherMixin):
                _enable_bubbling = True

                def _get_bubbling_parent(self):
                    return self.parent  # or self.owner, self.container, etc.
        """
        return None

    def _snapshot_listeners(
        self,
        event: Event | str,
        *,
        payload: Mapping[str, Any] | None,
        metadata: Mapping[str, Any] | None,
        source: Any | object,
    ) -> tuple[Event, list[tuple[str, ListenerRecord]]]:
        listeners, lock, _ = self._ensure_dispatcher_state()
        dispatched_event = self._coerce_event(
            event, payload=payload, metadata=metadata, source=source
        )

        with lock:
            bucket = listeners.get(dispatched_event.name, [])
            copied = [(dispatched_event.name, record) for record in list(bucket)]
        return dispatched_event, copied
