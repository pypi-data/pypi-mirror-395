from __future__ import annotations

import pytest
from wexample_helpers.testing.abstract_test_helpers import AbstractTestHelpers


class TestListenerSpec(AbstractTestHelpers):
    def test_listener_spec_creation(self) -> None:
        """Test creating a ListenerSpec."""
        from wexample_event.dataclass.listener_spec import ListenerSpec

        spec = ListenerSpec(name="test_event", priority=100, once=False)

        assert spec.name == "test_event"
        assert spec.priority == 100
        assert spec.once is False

    def test_listener_spec_equality(self) -> None:
        """Test ListenerSpec equality."""
        from wexample_event.dataclass.listener_spec import ListenerSpec

        spec1 = ListenerSpec(name="test", priority=100, once=False)
        spec2 = ListenerSpec(name="test", priority=100, once=False)

        assert spec1 == spec2

    def test_listener_spec_immutable(self) -> None:
        """Test that ListenerSpec is immutable (frozen)."""
        from wexample_event.dataclass.listener_spec import ListenerSpec

        spec = ListenerSpec(name="test", priority=0, once=False)

        with pytest.raises(Exception):  # FrozenInstanceError
            spec.name = "modified"  # type: ignore

    def test_listener_spec_inequality(self) -> None:
        """Test ListenerSpec inequality."""
        from wexample_event.dataclass.listener_spec import ListenerSpec

        spec1 = ListenerSpec(name="test1", priority=100, once=False)
        spec2 = ListenerSpec(name="test2", priority=100, once=False)

        assert spec1 != spec2

    def test_listener_spec_with_negative_priority(self) -> None:
        """Test ListenerSpec with negative priority."""
        from wexample_event.dataclass.listener_spec import ListenerSpec

        spec = ListenerSpec(name="test", priority=-100, once=False)

        assert spec.priority == -100

    def test_listener_spec_with_once(self) -> None:
        """Test ListenerSpec with once=True."""
        from wexample_event.dataclass.listener_spec import ListenerSpec

        spec = ListenerSpec(name="once_event", priority=0, once=True)

        assert spec.name == "once_event"
        assert spec.once is True

    def test_types(self) -> None:
        """Test type validation for ListenerSpec."""
        from wexample_event.dataclass.listener_spec import ListenerSpec

        spec = ListenerSpec(name="test", priority=0, once=False)

        self._test_type_validate_or_fail(success_cases=[(spec, ListenerSpec)])
