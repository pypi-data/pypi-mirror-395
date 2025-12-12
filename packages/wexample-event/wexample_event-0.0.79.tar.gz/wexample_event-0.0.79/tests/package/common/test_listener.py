from __future__ import annotations

import pytest
from wexample_helpers.testing.abstract_test_helpers import AbstractTestHelpers


class TestEventListenerMixin(AbstractTestHelpers):
    def test_listener_bind_none_raises(self) -> None:
        """Test that binding to None raises ValueError."""
        from wexample_event.common.listener import EventListenerMixin
        from wexample_event.dataclass.event import Event

        class TestListener(EventListenerMixin):
            @EventListenerMixin.on("test")
            def handle_test(self, event: Event) -> None:
                pass

        listener = TestListener()

        with pytest.raises(ValueError):
            listener.bind_to_dispatcher(None)  # type: ignore

    def test_listener_bind_same_dispatcher_twice(self) -> None:
        """Test binding to the same dispatcher twice does nothing."""
        from wexample_event.common.dispatcher import EventDispatcherMixin
        from wexample_event.common.listener import EventListenerMixin
        from wexample_event.dataclass.event import Event

        class TestDispatcher(EventDispatcherMixin):
            pass

        class TestListener(EventListenerMixin):
            def __init__(self) -> None:
                self.call_count = 0

            @EventListenerMixin.on("test")
            def handle_test(self, event: Event) -> None:
                self.call_count += 1

        dispatcher = TestDispatcher()
        listener = TestListener()

        listener.bind_to_dispatcher(dispatcher)
        listener.bind_to_dispatcher(dispatcher)  # Should be idempotent

        dispatcher.dispatch("test")
        assert listener.call_count == 1  # Not 2

    def test_listener_bind_to_dispatcher(self) -> None:
        """Test binding listener to dispatcher."""
        from wexample_event.common.dispatcher import EventDispatcherMixin
        from wexample_event.common.listener import EventListenerMixin
        from wexample_event.dataclass.event import Event

        class TestDispatcher(EventDispatcherMixin):
            pass

        class TestListener(EventListenerMixin):
            def __init__(self) -> None:
                self.events_received: list[Event] = []

            @EventListenerMixin.on("test_event")
            def handle_test(self, event: Event) -> None:
                self.events_received.append(event)

        dispatcher = TestDispatcher()
        listener = TestListener()

        listener.bind_to_dispatcher(dispatcher)
        dispatcher.dispatch("test_event")

        assert len(listener.events_received) == 1
        assert listener.events_received[0].name == "test_event"

    def test_listener_decorator(self) -> None:
        """Test @on decorator marks methods as listeners."""
        from wexample_event.common.listener import EventListenerMixin
        from wexample_event.dataclass.event import Event

        class TestListener(EventListenerMixin):
            def __init__(self) -> None:
                self.events_received: list[Event] = []

            @EventListenerMixin.on("test_event")
            def handle_test(self, event: Event) -> None:
                self.events_received.append(event)

        listener = TestListener()
        assert hasattr(listener.handle_test, "__event_listener_specs__")

    def test_listener_get_bound_dispatcher(self) -> None:
        """Test getting the bound dispatcher."""
        from wexample_event.common.dispatcher import EventDispatcherMixin
        from wexample_event.common.listener import EventListenerMixin
        from wexample_event.dataclass.event import Event

        class TestDispatcher(EventDispatcherMixin):
            pass

        class TestListener(EventListenerMixin):
            @EventListenerMixin.on("test")
            def handle_test(self, event: Event) -> None:
                pass

        dispatcher = TestDispatcher()
        listener = TestListener()

        assert listener.get_bound_dispatcher() is None

        listener.bind_to_dispatcher(dispatcher)
        assert listener.get_bound_dispatcher() is dispatcher

        listener.unbind_from_dispatcher()
        assert listener.get_bound_dispatcher() is None

    def test_listener_inheritance(self) -> None:
        """Test that listener methods are inherited."""
        from wexample_event.common.dispatcher import EventDispatcherMixin
        from wexample_event.common.listener import EventListenerMixin
        from wexample_event.dataclass.event import Event

        class TestDispatcher(EventDispatcherMixin):
            pass

        class BaseListener(EventListenerMixin):
            def __init__(self) -> None:
                self.base_count = 0

            @EventListenerMixin.on("base_event")
            def handle_base(self, event: Event) -> None:
                self.base_count += 1

        class DerivedListener(BaseListener):
            def __init__(self) -> None:
                super().__init__()
                self.derived_count = 0

            @EventListenerMixin.on("derived_event")
            def handle_derived(self, event: Event) -> None:
                self.derived_count += 1

        dispatcher = TestDispatcher()
        listener = DerivedListener()

        listener.bind_to_dispatcher(dispatcher)
        dispatcher.dispatch("base_event")
        dispatcher.dispatch("derived_event")

        assert listener.base_count == 1
        assert listener.derived_count == 1

    def test_listener_multiple_decorators_same_method(self) -> None:
        """Test multiple @on decorators on the same method."""
        from wexample_event.common.dispatcher import EventDispatcherMixin
        from wexample_event.common.listener import EventListenerMixin
        from wexample_event.dataclass.event import Event

        class TestDispatcher(EventDispatcherMixin):
            pass

        class TestListener(EventListenerMixin):
            def __init__(self) -> None:
                self.call_count = 0

            @EventListenerMixin.on("event1")
            @EventListenerMixin.on("event2")
            def handle_both(self, event: Event) -> None:
                self.call_count += 1

        dispatcher = TestDispatcher()
        listener = TestListener()

        listener.bind_to_dispatcher(dispatcher)
        dispatcher.dispatch("event1")
        dispatcher.dispatch("event2")

        assert listener.call_count == 2

    def test_listener_multiple_events(self) -> None:
        """Test listener handling multiple event types."""
        from wexample_event.common.dispatcher import EventDispatcherMixin
        from wexample_event.common.listener import EventListenerMixin
        from wexample_event.dataclass.event import Event

        class TestDispatcher(EventDispatcherMixin):
            pass

        class TestListener(EventListenerMixin):
            def __init__(self) -> None:
                self.event1_count = 0
                self.event2_count = 0

            @EventListenerMixin.on("event1")
            def handle_event1(self, event: Event) -> None:
                self.event1_count += 1

            @EventListenerMixin.on("event2")
            def handle_event2(self, event: Event) -> None:
                self.event2_count += 1

        dispatcher = TestDispatcher()
        listener = TestListener()

        listener.bind_to_dispatcher(dispatcher)
        dispatcher.dispatch("event1")
        dispatcher.dispatch("event2")
        dispatcher.dispatch("event1")

        assert listener.event1_count == 2
        assert listener.event2_count == 1

    def test_listener_multiple_instances(self) -> None:
        """Test multiple listener instances work independently."""
        from wexample_event.common.dispatcher import EventDispatcherMixin
        from wexample_event.common.listener import EventListenerMixin
        from wexample_event.dataclass.event import Event

        class TestDispatcher(EventDispatcherMixin):
            pass

        class TestListener(EventListenerMixin):
            def __init__(self) -> None:
                self.call_count = 0

            @EventListenerMixin.on("test")
            def handle_test(self, event: Event) -> None:
                self.call_count += 1

        dispatcher = TestDispatcher()
        listener1 = TestListener()
        listener2 = TestListener()

        listener1.bind_to_dispatcher(dispatcher)
        listener2.bind_to_dispatcher(dispatcher)

        dispatcher.dispatch("test")

        assert listener1.call_count == 1
        assert listener2.call_count == 1

    def test_listener_once(self) -> None:
        """Test listener with once=True."""
        from wexample_event.common.dispatcher import EventDispatcherMixin
        from wexample_event.common.listener import EventListenerMixin
        from wexample_event.dataclass.event import Event

        class TestDispatcher(EventDispatcherMixin):
            pass

        class TestListener(EventListenerMixin):
            def __init__(self) -> None:
                self.call_count = 0

            @EventListenerMixin.on("test", once=True)
            def handle_once(self, event: Event) -> None:
                self.call_count += 1

        dispatcher = TestDispatcher()
        listener = TestListener()

        listener.bind_to_dispatcher(dispatcher)
        dispatcher.dispatch("test")
        dispatcher.dispatch("test")

        assert listener.call_count == 1

    def test_listener_rebind_to_different_dispatcher(self) -> None:
        """Test rebinding listener to a different dispatcher."""
        from wexample_event.common.dispatcher import EventDispatcherMixin
        from wexample_event.common.listener import EventListenerMixin
        from wexample_event.dataclass.event import Event

        class TestDispatcher(EventDispatcherMixin):
            pass

        class TestListener(EventListenerMixin):
            def __init__(self) -> None:
                self.events_received: list[Event] = []

            @EventListenerMixin.on("test")
            def handle_test(self, event: Event) -> None:
                self.events_received.append(event)

        dispatcher1 = TestDispatcher()
        dispatcher2 = TestDispatcher()
        listener = TestListener()

        listener.bind_to_dispatcher(dispatcher1)
        dispatcher1.dispatch("test")
        assert len(listener.events_received) == 1

        # Rebind to different dispatcher
        listener.bind_to_dispatcher(dispatcher2)
        dispatcher1.dispatch("test")  # Should not trigger
        dispatcher2.dispatch("test")  # Should trigger

        assert len(listener.events_received) == 2

    def test_listener_unbind(self) -> None:
        """Test unbinding listener from dispatcher."""
        from wexample_event.common.dispatcher import EventDispatcherMixin
        from wexample_event.common.listener import EventListenerMixin
        from wexample_event.dataclass.event import Event

        class TestDispatcher(EventDispatcherMixin):
            pass

        class TestListener(EventListenerMixin):
            def __init__(self) -> None:
                self.call_count = 0

            @EventListenerMixin.on("test")
            def handle_test(self, event: Event) -> None:
                self.call_count += 1

        dispatcher = TestDispatcher()
        listener = TestListener()

        listener.bind_to_dispatcher(dispatcher)
        dispatcher.dispatch("test")
        assert listener.call_count == 1

        listener.unbind_from_dispatcher()
        dispatcher.dispatch("test")
        assert listener.call_count == 1  # Should not increase

    def test_listener_unbind_without_bind(self) -> None:
        """Test that unbinding without binding doesn't raise error."""
        from wexample_event.common.listener import EventListenerMixin
        from wexample_event.dataclass.event import Event

        class TestListener(EventListenerMixin):
            @EventListenerMixin.on("test")
            def handle_test(self, event: Event) -> None:
                pass

        listener = TestListener()
        listener.unbind_from_dispatcher()  # Should not raise

    def test_listener_with_payload(self) -> None:
        """Test listener receiving event with payload."""
        from wexample_event.common.dispatcher import EventDispatcherMixin
        from wexample_event.common.listener import EventListenerMixin
        from wexample_event.dataclass.event import Event

        class TestDispatcher(EventDispatcherMixin):
            pass

        class TestListener(EventListenerMixin):
            def __init__(self) -> None:
                self.received_payload = None

            @EventListenerMixin.on("test")
            def handle_test(self, event: Event) -> None:
                self.received_payload = event.payload

        dispatcher = TestDispatcher()
        listener = TestListener()

        listener.bind_to_dispatcher(dispatcher)
        dispatcher.dispatch("test", payload={"key": "value"})

        assert listener.received_payload == {"key": "value"}

    def test_listener_with_priority(self) -> None:
        """Test listener with custom priority."""
        from wexample_event.common.dispatcher import EventDispatcherMixin
        from wexample_event.common.listener import EventListenerMixin, EventPriority
        from wexample_event.dataclass.event import Event

        class TestDispatcher(EventDispatcherMixin):
            pass

        class TestListener(EventListenerMixin):
            def __init__(self) -> None:
                self.call_order: list[str] = []

            @EventListenerMixin.on("test", priority=EventPriority.HIGH)
            def high_priority_handler(self, event: Event) -> None:
                self.call_order.append("high")

            @EventListenerMixin.on("test", priority=EventPriority.LOW)
            def low_priority_handler(self, event: Event) -> None:
                self.call_order.append("low")

        dispatcher = TestDispatcher()
        listener = TestListener()

        listener.bind_to_dispatcher(dispatcher)
        dispatcher.dispatch("test")

        assert listener.call_order == ["high", "low"]

    def test_types(self) -> None:
        """Test type validation for EventListenerMixin."""
        from wexample_event.common.listener import EventListenerMixin
        from wexample_event.dataclass.event import Event

        class TestListener(EventListenerMixin):
            @EventListenerMixin.on("test")
            def handle_test(self, event: Event) -> None:
                pass

        listener = TestListener()

        self._test_type_validate_or_fail(
            success_cases=[
                (listener, TestListener),
                (listener, EventListenerMixin),
            ]
        )
