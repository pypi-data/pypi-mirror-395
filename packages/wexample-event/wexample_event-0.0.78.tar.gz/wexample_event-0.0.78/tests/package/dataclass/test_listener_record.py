from __future__ import annotations

from wexample_helpers.testing.abstract_test_helpers import AbstractTestHelpers


class TestListenerRecord(AbstractTestHelpers):
    def test_listener_record_async_callback(self) -> None:
        """Test ListenerRecord with async callback."""
        from wexample_event.dataclass.event import Event
        from wexample_event.dataclass.listener_record import ListenerRecord

        async def async_callback(event: Event) -> None:
            pass

        record = ListenerRecord(
            callback=async_callback, once=False, priority=0, order=1
        )

        assert record.callback is async_callback

    def test_listener_record_creation(self) -> None:
        """Test creating a ListenerRecord."""
        from wexample_event.dataclass.event import Event
        from wexample_event.dataclass.listener_record import ListenerRecord

        def callback(event: Event) -> None:
            pass

        record = ListenerRecord(callback=callback, once=False, priority=0, order=1)

        assert record.callback is callback
        assert record.once is False
        assert record.priority == 0
        assert record.order == 1

    def test_listener_record_mutable(self) -> None:
        """Test that ListenerRecord is mutable (not frozen)."""
        from wexample_event.dataclass.event import Event
        from wexample_event.dataclass.listener_record import ListenerRecord

        def callback(event: Event) -> None:
            pass

        record = ListenerRecord(callback=callback, once=False, priority=0, order=1)

        # Should be able to modify
        record.priority = 100
        assert record.priority == 100

    def test_listener_record_with_once(self) -> None:
        """Test ListenerRecord with once=True."""
        from wexample_event.dataclass.event import Event
        from wexample_event.dataclass.listener_record import ListenerRecord

        def callback(event: Event) -> None:
            pass

        record = ListenerRecord(callback=callback, once=True, priority=100, order=5)

        assert record.once is True
        assert record.priority == 100
        assert record.order == 5

    def test_types(self) -> None:
        """Test type validation for ListenerRecord."""
        from wexample_event.dataclass.event import Event
        from wexample_event.dataclass.listener_record import ListenerRecord

        def callback(event: Event) -> None:
            pass

        record = ListenerRecord(callback=callback, once=False, priority=0, order=1)

        self._test_type_validate_or_fail(success_cases=[(record, ListenerRecord)])
