from __future__ import annotations

from datetime import datetime, timezone

import pytest
from wexample_helpers.testing.abstract_test_helpers import AbstractTestHelpers


class TestEvent(AbstractTestHelpers):
    def test_event_creation(self) -> None:
        """Test basic event creation with required fields."""
        from wexample_event.dataclass.event import Event

        event = Event(name="test_event")

        assert event.name == "test_event"
        assert event.payload is None
        assert event.metadata is None
        assert event.source is None
        assert isinstance(event.timestamp, datetime)

    def test_event_custom_timestamp(self) -> None:
        """Test event with custom timestamp."""
        from wexample_event.dataclass.event import Event

        custom_time = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        event = Event(name="test", timestamp=custom_time)

        assert event.timestamp == custom_time

    def test_event_derive(self) -> None:
        """Test derive method creates a copy with optional name change."""
        from wexample_event.dataclass.event import Event

        original = Event(
            name="original",
            payload={"key": "value"},
            metadata={"meta": "data"},
        )
        derived = original.derive(name="derived")

        assert derived.name == "derived"
        assert derived.payload == original.payload
        assert derived.metadata == original.metadata
        assert derived is not original

    def test_event_derive_with_changes(self) -> None:
        """Test derive with additional field changes."""
        from wexample_event.dataclass.event import Event

        original = Event(name="test", payload={"a": 1})
        derived = original.derive(name="derived", payload={"b": 2})

        assert derived.name == "derived"
        assert derived.payload == {"b": 2}

    def test_event_derive_without_name(self) -> None:
        """Test derive without name parameter."""
        from wexample_event.dataclass.event import Event

        original = Event(name="test", payload={"key": "value"})
        derived = original.derive(metadata={"new": "meta"})

        assert derived.name == "test"
        assert derived.payload == {"key": "value"}
        assert derived.metadata == {"new": "meta"}

    def test_event_equality(self) -> None:
        """Test event equality comparison."""
        from wexample_event.dataclass.event import Event

        timestamp = datetime.now(timezone.utc)
        event1 = Event(name="test", payload={"key": "value"}, timestamp=timestamp)
        event2 = Event(name="test", payload={"key": "value"}, timestamp=timestamp)

        assert event1 == event2

    def test_event_immutability(self) -> None:
        """Test that Event is immutable (frozen dataclass)."""
        from wexample_event.dataclass.event import Event

        event = Event(name="test_event")

        # Attempting to modify should raise an error
        with pytest.raises(Exception):  # FrozenInstanceError
            event.name = "modified_name"  # type: ignore

    def test_event_inequality(self) -> None:
        """Test event inequality when fields differ."""
        from wexample_event.dataclass.event import Event

        event1 = Event(name="test1")
        event2 = Event(name="test2")

        assert event1 != event2

    def test_event_timestamp_is_utc(self) -> None:
        """Test that timestamp is in UTC timezone."""
        from wexample_event.dataclass.event import Event

        event = Event(name="test")

        assert event.timestamp.tzinfo == timezone.utc

    def test_event_with_metadata(self) -> None:
        """Test event creation with metadata."""
        from wexample_event.dataclass.event import Event

        metadata = {"user_id": "123", "session": "abc"}
        event = Event(name="test_event", metadata=metadata)

        assert event.name == "test_event"
        assert event.metadata == metadata
        assert event.metadata["user_id"] == "123"

    def test_event_with_payload(self) -> None:
        """Test event creation with payload."""
        from wexample_event.dataclass.event import Event

        payload = {"key": "value", "number": 42}
        event = Event(name="test_event", payload=payload)

        assert event.name == "test_event"
        assert event.payload == payload
        assert event.payload["key"] == "value"
        assert event.payload["number"] == 42

    def test_event_with_source(self) -> None:
        """Test event creation with source."""
        from wexample_event.dataclass.event import Event

        source = {"component": "test_component"}
        event = Event(name="test_event", source=source)

        assert event.name == "test_event"
        assert event.source == source

    def test_event_with_update(self) -> None:
        """Test with_update method creates a new event with changes."""
        from wexample_event.dataclass.event import Event

        original = Event(name="original", payload={"key": "value"})
        updated = original.with_update(name="updated")

        assert original.name == "original"
        assert updated.name == "updated"
        assert updated.payload == {"key": "value"}
        assert original is not updated

    def test_event_with_update_multiple_fields(self) -> None:
        """Test with_update with multiple field changes."""
        from wexample_event.dataclass.event import Event

        original = Event(name="test", payload={"a": 1})
        updated = original.with_update(payload={"b": 2}, metadata={"meta": "data"})

        assert original.payload == {"a": 1}
        assert original.metadata is None
        assert updated.payload == {"b": 2}
        assert updated.metadata == {"meta": "data"}

    def test_types(self) -> None:
        """Test type validation for Event class."""
        from wexample_event.dataclass.event import Event

        self._test_type_validate_or_fail(
            success_cases=[
                (Event(name="test"), Event),
                (Event(name="test", payload={"key": "value"}), Event),
            ]
        )
