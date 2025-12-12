from __future__ import annotations

import asyncio

import pytest
from wexample_helpers.testing.abstract_test_helpers import AbstractTestHelpers


class TestEventDispatcherMixin(AbstractTestHelpers):
    def test_dispatcher_async(self) -> None:
        """Test async event dispatching."""
        from wexample_event.common.dispatcher import EventDispatcherMixin
        from wexample_event.dataclass.event import Event

        class TestDispatcher(EventDispatcherMixin):
            pass

        dispatcher = TestDispatcher()
        call_order = []

        async def async_listener(event: Event) -> None:
            await asyncio.sleep(0.01)
            call_order.append("async")

        def sync_listener(event: Event) -> None:
            call_order.append("sync")

        dispatcher.add_event_listener("test", async_listener)
        dispatcher.add_event_listener("test", sync_listener)

        async def run_test() -> None:
            await dispatcher.dispatch_async("test")

        asyncio.run(run_test())

        assert len(call_order) == 2
        assert "async" in call_order
        assert "sync" in call_order

    def test_dispatcher_async_once(self) -> None:
        """Test async dispatch with once=True."""
        from wexample_event.common.dispatcher import EventDispatcherMixin
        from wexample_event.dataclass.event import Event

        class TestDispatcher(EventDispatcherMixin):
            pass

        dispatcher = TestDispatcher()
        call_count = []

        async def listener(event: Event) -> None:
            call_count.append(1)

        dispatcher.add_event_listener("test", listener, once=True)

        async def run_test() -> None:
            await dispatcher.dispatch_async("test")
            await dispatcher.dispatch_async("test")

        asyncio.run(run_test())

        assert len(call_count) == 1

    def test_dispatcher_basic_dispatch(self) -> None:
        """Test basic event dispatching."""
        from wexample_event.common.dispatcher import EventDispatcherMixin
        from wexample_event.dataclass.event import Event

        class TestDispatcher(EventDispatcherMixin):
            pass

        dispatcher = TestDispatcher()
        events_received = []

        def listener(event: Event) -> None:
            events_received.append(event)

        dispatcher.add_event_listener("test_event", listener)
        event = dispatcher.dispatch("test_event")

        assert len(events_received) == 1
        assert events_received[0].name == "test_event"
        assert event.name == "test_event"

    def test_dispatcher_clear_listeners(self) -> None:
        """Test clearing all listeners."""
        from wexample_event.common.dispatcher import EventDispatcherMixin
        from wexample_event.dataclass.event import Event

        class TestDispatcher(EventDispatcherMixin):
            pass

        dispatcher = TestDispatcher()
        call_count = []

        def listener(event: Event) -> None:
            call_count.append(1)

        dispatcher.add_event_listener("test1", listener)
        dispatcher.add_event_listener("test2", listener)

        dispatcher.clear_event_listeners()

        dispatcher.dispatch("test1")
        dispatcher.dispatch("test2")

        assert len(call_count) == 0

    def test_dispatcher_clear_specific_event(self) -> None:
        """Test clearing listeners for a specific event."""
        from wexample_event.common.dispatcher import EventDispatcherMixin
        from wexample_event.dataclass.event import Event

        class TestDispatcher(EventDispatcherMixin):
            pass

        dispatcher = TestDispatcher()
        call_count = []

        def listener(event: Event) -> None:
            call_count.append(event.name)

        dispatcher.add_event_listener("test1", listener)
        dispatcher.add_event_listener("test2", listener)

        dispatcher.clear_event_listeners("test1")

        dispatcher.dispatch("test1")
        dispatcher.dispatch("test2")

        assert len(call_count) == 1
        assert call_count[0] == "test2"

    def test_dispatcher_default_source_is_dispatcher(self) -> None:
        """Test that default source is the dispatcher itself."""
        from wexample_event.common.dispatcher import EventDispatcherMixin
        from wexample_event.dataclass.event import Event

        class TestDispatcher(EventDispatcherMixin):
            pass

        dispatcher = TestDispatcher()
        received_sources = []

        def listener(event: Event) -> None:
            received_sources.append(event.source)

        dispatcher.add_event_listener("test", listener)
        dispatcher.dispatch("test")

        assert len(received_sources) == 1
        assert received_sources[0] is dispatcher

    def test_dispatcher_event_alias(self) -> None:
        """Test dispatch_event alias."""
        from wexample_event.common.dispatcher import EventDispatcherMixin
        from wexample_event.dataclass.event import Event

        class TestDispatcher(EventDispatcherMixin):
            pass

        dispatcher = TestDispatcher()
        call_count = []

        def listener(event: Event) -> None:
            call_count.append(1)

        dispatcher.add_event_listener("test", listener)
        dispatcher.dispatch_event("test")

        assert len(call_count) == 1

    def test_dispatcher_event_alias_async(self) -> None:
        """Test dispatch_event_async alias."""
        from wexample_event.common.dispatcher import EventDispatcherMixin
        from wexample_event.dataclass.event import Event

        class TestDispatcher(EventDispatcherMixin):
            pass

        dispatcher = TestDispatcher()
        call_count = []

        async def listener(event: Event) -> None:
            call_count.append(1)

        dispatcher.add_event_listener("test", listener)

        async def run_test() -> None:
            await dispatcher.dispatch_event_async("test")

        asyncio.run(run_test())

        assert len(call_count) == 1

    def test_dispatcher_event_with_metadata(self) -> None:
        """Test dispatching with metadata."""
        from wexample_event.common.dispatcher import EventDispatcherMixin
        from wexample_event.dataclass.event import Event

        class TestDispatcher(EventDispatcherMixin):
            pass

        dispatcher = TestDispatcher()
        received_metadata = []

        def listener(event: Event) -> None:
            received_metadata.append(event.metadata)

        dispatcher.add_event_listener("test", listener)
        dispatcher.dispatch("test", metadata={"user": "test_user"})

        assert len(received_metadata) == 1
        assert received_metadata[0] == {"user": "test_user"}

    def test_dispatcher_event_with_source(self) -> None:
        """Test dispatching with custom source."""
        from wexample_event.common.dispatcher import EventDispatcherMixin
        from wexample_event.dataclass.event import Event

        class TestDispatcher(EventDispatcherMixin):
            pass

        dispatcher = TestDispatcher()
        received_sources = []

        def listener(event: Event) -> None:
            received_sources.append(event.source)

        dispatcher.add_event_listener("test", listener)

        custom_source = {"component": "test"}
        dispatcher.dispatch("test", source=custom_source)

        assert len(received_sources) == 1
        assert received_sources[0] == custom_source

    def test_dispatcher_has_listeners(self) -> None:
        """Test has_event_listeners method."""
        from wexample_event.common.dispatcher import EventDispatcherMixin
        from wexample_event.dataclass.event import Event

        class TestDispatcher(EventDispatcherMixin):
            pass

        dispatcher = TestDispatcher()

        def listener(event: Event) -> None:
            pass

        assert dispatcher.has_event_listeners("test") is False

        dispatcher.add_event_listener("test", listener)
        assert dispatcher.has_event_listeners("test") is True

        dispatcher.remove_event_listener("test", listener)
        assert dispatcher.has_event_listeners("test") is False

    def test_dispatcher_invalid_callback(self) -> None:
        """Test that non-callable raises TypeError."""
        from wexample_event.common.dispatcher import EventDispatcherMixin

        class TestDispatcher(EventDispatcherMixin):
            pass

        dispatcher = TestDispatcher()

        with pytest.raises(TypeError):
            dispatcher.add_event_listener("test", "not_callable")  # type: ignore

    def test_dispatcher_multiple_listeners(self) -> None:
        """Test multiple listeners for the same event."""
        from wexample_event.common.dispatcher import EventDispatcherMixin
        from wexample_event.dataclass.event import Event

        class TestDispatcher(EventDispatcherMixin):
            pass

        dispatcher = TestDispatcher()
        call_order = []

        def listener1(event: Event) -> None:
            call_order.append("listener1")

        def listener2(event: Event) -> None:
            call_order.append("listener2")

        dispatcher.add_event_listener("test", listener1)
        dispatcher.add_event_listener("test", listener2)
        dispatcher.dispatch("test")

        assert len(call_order) == 2
        assert "listener1" in call_order
        assert "listener2" in call_order

    def test_dispatcher_once_listener(self) -> None:
        """Test once=True listener is called only once."""
        from wexample_event.common.dispatcher import EventDispatcherMixin
        from wexample_event.dataclass.event import Event

        class TestDispatcher(EventDispatcherMixin):
            pass

        dispatcher = TestDispatcher()
        call_count = []

        def listener(event: Event) -> None:
            call_count.append(1)

        dispatcher.add_event_listener("test", listener, once=True)

        dispatcher.dispatch("test")
        assert len(call_count) == 1

        dispatcher.dispatch("test")
        assert len(call_count) == 1  # Should not increase

    def test_dispatcher_priority_ordering(self) -> None:
        """Test that listeners are called in priority order."""
        from wexample_event.common.dispatcher import EventDispatcherMixin
        from wexample_event.common.priority import EventPriority
        from wexample_event.dataclass.event import Event

        class TestDispatcher(EventDispatcherMixin):
            pass

        dispatcher = TestDispatcher()
        call_order = []

        def low_priority(event: Event) -> None:
            call_order.append("low")

        def high_priority(event: Event) -> None:
            call_order.append("high")

        def normal_priority(event: Event) -> None:
            call_order.append("normal")

        dispatcher.add_event_listener("test", low_priority, priority=EventPriority.LOW)
        dispatcher.add_event_listener(
            "test", high_priority, priority=EventPriority.HIGH
        )
        dispatcher.add_event_listener(
            "test", normal_priority, priority=EventPriority.NORMAL
        )
        dispatcher.dispatch("test")

        assert call_order == ["high", "normal", "low"]

    def test_dispatcher_remove_listener(self) -> None:
        """Test removing an event listener."""
        from wexample_event.common.dispatcher import EventDispatcherMixin
        from wexample_event.dataclass.event import Event

        class TestDispatcher(EventDispatcherMixin):
            pass

        dispatcher = TestDispatcher()
        call_count = []

        def listener(event: Event) -> None:
            call_count.append(1)

        dispatcher.add_event_listener("test", listener)
        dispatcher.dispatch("test")
        assert len(call_count) == 1

        removed = dispatcher.remove_event_listener("test", listener)
        assert removed is True

        dispatcher.dispatch("test")
        assert len(call_count) == 1  # Should not increase

    def test_dispatcher_remove_nonexistent_listener(self) -> None:
        """Test removing a listener that doesn't exist."""
        from wexample_event.common.dispatcher import EventDispatcherMixin
        from wexample_event.dataclass.event import Event

        class TestDispatcher(EventDispatcherMixin):
            pass

        dispatcher = TestDispatcher()

        def listener(event: Event) -> None:
            pass

        removed = dispatcher.remove_event_listener("test", listener)
        assert removed is False

    def test_dispatcher_sync_with_async_listener_raises(self) -> None:
        """Test that sync dispatch with async listener raises error."""
        from wexample_event.common.dispatcher import EventDispatcherMixin
        from wexample_event.dataclass.event import Event

        class TestDispatcher(EventDispatcherMixin):
            pass

        dispatcher = TestDispatcher()

        async def async_listener(event: Event) -> None:
            pass

        dispatcher.add_event_listener("test", async_listener)

        with pytest.raises(RuntimeError):
            dispatcher.dispatch("test")

    def test_dispatcher_thread_safety(self) -> None:
        """Test that dispatcher is thread-safe."""
        import threading

        from wexample_event.common.dispatcher import EventDispatcherMixin
        from wexample_event.dataclass.event import Event

        class TestDispatcher(EventDispatcherMixin):
            pass

        dispatcher = TestDispatcher()
        call_count = []

        def listener(event: Event) -> None:
            call_count.append(1)

        dispatcher.add_event_listener("test", listener)

        def dispatch_in_thread() -> None:
            for _ in range(10):
                dispatcher.dispatch("test")

        threads = [threading.Thread(target=dispatch_in_thread) for _ in range(5)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        assert len(call_count) == 50

    def test_dispatcher_with_event_object(self) -> None:
        """Test dispatching with an Event object."""
        from wexample_event.common.dispatcher import EventDispatcherMixin
        from wexample_event.dataclass.event import Event

        class TestDispatcher(EventDispatcherMixin):
            pass

        dispatcher = TestDispatcher()
        received_events = []

        def listener(event: Event) -> None:
            received_events.append(event)

        dispatcher.add_event_listener("test", listener)

        original_event = Event(name="test", payload={"key": "value"})
        returned_event = dispatcher.dispatch(original_event)

        assert len(received_events) == 1
        assert received_events[0] is original_event
        assert returned_event is original_event

    def test_dispatcher_with_payload(self) -> None:
        """Test dispatching with payload."""
        from wexample_event.common.dispatcher import EventDispatcherMixin
        from wexample_event.dataclass.event import Event

        class TestDispatcher(EventDispatcherMixin):
            pass

        dispatcher = TestDispatcher()
        received_payload = []

        def listener(event: Event) -> None:
            received_payload.append(event.payload)

        dispatcher.add_event_listener("test", listener)
        dispatcher.dispatch("test", payload={"key": "value"})

        assert len(received_payload) == 1
        assert received_payload[0] == {"key": "value"}

    def test_types(self) -> None:
        """Test type validation for EventDispatcherMixin."""
        from wexample_event.common.dispatcher import EventDispatcherMixin

        class TestDispatcher(EventDispatcherMixin):
            pass

        dispatcher = TestDispatcher()

        self._test_type_validate_or_fail(
            success_cases=[
                (dispatcher, TestDispatcher),
                (dispatcher, EventDispatcherMixin),
            ]
        )
