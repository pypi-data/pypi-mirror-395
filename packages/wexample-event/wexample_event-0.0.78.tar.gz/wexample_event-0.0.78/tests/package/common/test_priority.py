from __future__ import annotations

from wexample_helpers.testing.abstract_test_helpers import AbstractTestHelpers


class TestEventPriority(AbstractTestHelpers):
    def test_default_priority(self) -> None:
        """Test DEFAULT_PRIORITY constant."""
        from wexample_event.common.priority import DEFAULT_PRIORITY, EventPriority

        assert DEFAULT_PRIORITY == EventPriority.NORMAL
        assert DEFAULT_PRIORITY == 0

    def test_priority_arithmetic(self) -> None:
        """Test arithmetic operations with priorities."""
        from wexample_event.common.priority import EventPriority

        result = EventPriority.NORMAL + 50
        assert result == 50

        result = EventPriority.HIGH - 50
        assert result == 50

    def test_priority_as_int(self) -> None:
        """Test that priorities can be used as integers."""
        from wexample_event.common.priority import EventPriority

        assert int(EventPriority.LOW) == -100
        assert int(EventPriority.NORMAL) == 0
        assert int(EventPriority.HIGH) == 100

    def test_priority_comparison(self) -> None:
        """Test that priorities can be compared."""
        from wexample_event.common.priority import EventPriority

        assert EventPriority.LOW < EventPriority.NORMAL
        assert EventPriority.NORMAL < EventPriority.HIGH
        assert EventPriority.HIGH > EventPriority.LOW

    def test_priority_in_dict(self) -> None:
        """Test using priorities as dictionary keys."""
        from wexample_event.common.priority import EventPriority

        priority_map = {
            EventPriority.LOW: "low",
            EventPriority.NORMAL: "normal",
            EventPriority.HIGH: "high",
        }

        assert priority_map[EventPriority.LOW] == "low"
        assert priority_map[EventPriority.NORMAL] == "normal"
        assert priority_map[EventPriority.HIGH] == "high"

    def test_priority_ordering(self) -> None:
        """Test that priorities maintain correct ordering."""
        from wexample_event.common.priority import EventPriority

        priorities = [EventPriority.HIGH, EventPriority.LOW, EventPriority.NORMAL]
        sorted_priorities = sorted(priorities)

        assert sorted_priorities == [
            EventPriority.LOW,
            EventPriority.NORMAL,
            EventPriority.HIGH,
        ]

    def test_priority_values(self) -> None:
        """Test EventPriority enum values."""
        from wexample_event.common.priority import EventPriority

        assert EventPriority.LOW == -100
        assert EventPriority.NORMAL == 0
        assert EventPriority.HIGH == 100

    def test_types(self) -> None:
        """Test type validation for EventPriority."""
        from wexample_event.common.priority import DEFAULT_PRIORITY, EventPriority

        self._test_type_validate_or_fail(
            success_cases=[
                (EventPriority.LOW, EventPriority),
                (EventPriority.NORMAL, EventPriority),
                (EventPriority.HIGH, EventPriority),
                (DEFAULT_PRIORITY, EventPriority),
            ]
        )
