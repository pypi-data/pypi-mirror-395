from __future__ import annotations

from wexample_helpers.testing.abstract_test_helpers import AbstractTestHelpers


class TestListenerState(AbstractTestHelpers):
    def test_listener_state_add_bindings(self) -> None:
        """Test adding bindings to ListenerState."""
        from wexample_event.common.listener_state import ListenerState
        from wexample_event.dataclass.event import Event

        def callback(event: Event) -> None:
            pass

        state = ListenerState()
        state.bindings.append(("test_event", callback))

        assert len(state.bindings) == 1
        assert state.bindings[0][0] == "test_event"
        assert state.bindings[0][1] is callback

    def test_listener_state_clear_bindings(self) -> None:
        """Test clearing bindings from ListenerState."""
        from wexample_event.common.listener_state import ListenerState
        from wexample_event.dataclass.event import Event

        def callback(event: Event) -> None:
            pass

        state = ListenerState()
        state.bindings.append(("test", callback))
        assert len(state.bindings) == 1

        state.bindings = []
        assert len(state.bindings) == 0

    def test_listener_state_creation(self) -> None:
        """Test creating a ListenerState."""
        from wexample_event.common.listener_state import ListenerState

        state = ListenerState()

        assert state.dispatcher is None
        assert state.bindings == []

    def test_listener_state_mutable(self) -> None:
        """Test that ListenerState is mutable."""
        from wexample_event.common.dispatcher import EventDispatcherMixin
        from wexample_event.common.listener_state import ListenerState

        class TestDispatcher(EventDispatcherMixin):
            pass

        state = ListenerState()
        dispatcher1 = TestDispatcher()
        dispatcher2 = TestDispatcher()

        state.dispatcher = dispatcher1
        assert state.dispatcher is dispatcher1

        state.dispatcher = dispatcher2
        assert state.dispatcher is dispatcher2

    def test_listener_state_set_dispatcher(self) -> None:
        """Test setting dispatcher on ListenerState."""
        from wexample_event.common.dispatcher import EventDispatcherMixin
        from wexample_event.common.listener_state import ListenerState

        class TestDispatcher(EventDispatcherMixin):
            pass

        state = ListenerState()
        dispatcher = TestDispatcher()

        state.dispatcher = dispatcher
        assert state.dispatcher is dispatcher

    def test_types(self) -> None:
        """Test type validation for ListenerState."""
        from wexample_event.common.listener_state import ListenerState

        state = ListenerState()

        self._test_type_validate_or_fail(success_cases=[(state, ListenerState)])
