from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence
from typing import Any

from wexample_event.common.dispatcher import EventDispatcherMixin
from wexample_event.common.listener_state import ListenerState
from wexample_event.common.priority import DEFAULT_PRIORITY, EventPriority
from wexample_event.dataclass.listener_record import EventCallback
from wexample_event.dataclass.listener_spec import ListenerSpec


class EventListenerMixin:
    """Mixin that simplifies binding methods to an EventDispatcherMixin."""

    _LISTENER_MARK_ATTR = "__event_listener_specs__"
    _BOUND_STATE_ATTR = "_event_listener_state"

    @classmethod
    def on(
        cls,
        event_name: str,
        *,
        priority: int | EventPriority = DEFAULT_PRIORITY,
        once: bool = False,
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """Decorator to declare a method as an event listener."""

        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            specs = list(getattr(func, cls._LISTENER_MARK_ATTR, ()))
            specs.append(
                ListenerSpec(name=event_name, priority=int(priority), once=once)
            )
            setattr(func, cls._LISTENER_MARK_ATTR, tuple(specs))
            return func

        return decorator

    def bind_to_dispatcher(self, dispatcher: EventDispatcherMixin) -> None:
        """Register all declared listeners on the provided dispatcher."""
        if dispatcher is None:
            raise ValueError("dispatcher must not be None")

        state = self._ensure_listener_state()

        if state.dispatcher is dispatcher:
            return

        if state.dispatcher is not None:
            self.unbind_from_dispatcher()
            state = self._ensure_listener_state()

        bindings: list[tuple[str, EventCallback]] = []
        for method_name, specs in self._iter_declared_listener_specs():
            bound_callback = getattr(self, method_name)
            for spec in specs:
                dispatcher.add_event_listener(
                    spec.name,
                    bound_callback,
                    once=spec.once,
                    priority=spec.priority,
                )
                bindings.append((spec.name, bound_callback))

        state.dispatcher = dispatcher
        state.bindings = bindings

    def get_bound_dispatcher(self) -> EventDispatcherMixin | None:
        """Return the dispatcher this listener is currently bound to."""
        state = self._ensure_listener_state()
        return state.dispatcher

    def unbind_from_dispatcher(self) -> None:
        """Remove all listeners previously bound via bind_to_dispatcher."""
        state = self._ensure_listener_state()
        dispatcher = state.dispatcher
        if dispatcher is None:
            return

        for name, callback in state.bindings:
            dispatcher.remove_event_listener(name, callback)

        state.dispatcher = None
        state.bindings = []

    def _ensure_listener_state(self) -> ListenerState:
        state = getattr(self, self._BOUND_STATE_ATTR, None)
        if state is None:
            state = ListenerState()
            setattr(self, self._BOUND_STATE_ATTR, state)
        return state

    def _iter_declared_listener_specs(
        self,
    ) -> Iterable[tuple[str, Sequence[ListenerSpec]]]:
        for cls in type(self).__mro__:
            for attr_name, value in cls.__dict__.items():
                specs = getattr(value, self._LISTENER_MARK_ATTR, None)
                if specs:
                    yield attr_name, specs
