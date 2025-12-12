from __future__ import annotations

from wexample_helpers.testing.abstract_test_helpers import AbstractTestHelpers


class TestEventBubbling(AbstractTestHelpers):
    def test_bubbling_async(self) -> None:
        """Test that bubbling works with async dispatch."""
        import asyncio

        from wexample_event.common.dispatcher import EventDispatcherMixin
        from wexample_event.dataclass.event import Event

        class Node(EventDispatcherMixin):
            _enable_bubbling = True

            def __init__(self, parent=None) -> None:
                self.parent = parent

            def _get_bubbling_parent(self):
                return self.parent

        parent = Node()
        child = Node(parent=parent)

        parent_events = []

        async def parent_listener(event: Event) -> None:
            parent_events.append(event.name)

        parent.add_event_listener("test", parent_listener)

        async def run_test() -> None:
            await child.dispatch_async("test")

        asyncio.run(run_test())

        assert len(parent_events) == 1
        assert parent_events[0] == "test"

    def test_bubbling_disabled_by_default(self) -> None:
        """Test that bubbling is disabled by default."""
        from wexample_event.common.dispatcher import EventDispatcherMixin
        from wexample_event.dataclass.event import Event

        class Node(EventDispatcherMixin):
            def __init__(self, parent=None) -> None:
                self.parent = parent

            def _get_bubbling_parent(self):
                return self.parent

        parent = Node()
        child = Node(parent=parent)

        parent_events = []

        def parent_listener(event: Event) -> None:
            parent_events.append(event.name)

        parent.add_event_listener("test", parent_listener)

        # Child dispatches, parent should NOT receive (bubbling disabled)
        child.dispatch("test")

        assert len(parent_events) == 0

    def test_bubbling_enabled(self) -> None:
        """Test that bubbling works when enabled."""
        from wexample_event.common.dispatcher import EventDispatcherMixin
        from wexample_event.dataclass.event import Event

        class Node(EventDispatcherMixin):
            _enable_bubbling = True

            def __init__(self, parent=None) -> None:
                self.parent = parent

            def _get_bubbling_parent(self):
                return self.parent

        parent = Node()
        child = Node(parent=parent)

        parent_events = []

        def parent_listener(event: Event) -> None:
            parent_events.append(event.name)

        parent.add_event_listener("test", parent_listener)

        # Child dispatches, parent SHOULD receive (bubbling enabled)
        child.dispatch("test")

        assert len(parent_events) == 1
        assert parent_events[0] == "test"

    def test_bubbling_multi_level(self) -> None:
        """Test that bubbling works through multiple levels."""
        from wexample_event.common.dispatcher import EventDispatcherMixin
        from wexample_event.dataclass.event import Event

        class Node(EventDispatcherMixin):
            _enable_bubbling = True

            def __init__(self, name: str, parent=None) -> None:
                self.name = name
                self.parent = parent
                self.received_events = []

            def _get_bubbling_parent(self):
                return self.parent

        # Create hierarchy: root -> middle -> leaf
        root = Node("root")
        middle = Node("middle", parent=root)
        leaf = Node("leaf", parent=middle)

        def track_event(node: Node):
            def listener(event: Event) -> None:
                node.received_events.append(event.name)

            return listener

        root.add_event_listener("test", track_event(root))
        middle.add_event_listener("test", track_event(middle))
        leaf.add_event_listener("test", track_event(leaf))

        # Leaf dispatches
        leaf.dispatch("test")

        # All levels should receive the event
        assert len(leaf.received_events) == 1
        assert len(middle.received_events) == 1
        assert len(root.received_events) == 1

    def test_bubbling_stops_at_no_parent(self) -> None:
        """Test that bubbling stops when no parent exists."""
        from wexample_event.common.dispatcher import EventDispatcherMixin

        class Node(EventDispatcherMixin):
            _enable_bubbling = True

            def __init__(self, parent=None) -> None:
                self.parent = parent

            def _get_bubbling_parent(self):
                return self.parent

        root = Node()  # No parent
        child = Node(parent=root)

        # Should not raise an error
        child.dispatch("test")
        root.dispatch("test")

    def test_bubbling_with_different_parent_attribute_name(self) -> None:
        """Test that bubbling works with custom parent attribute names."""
        from wexample_event.common.dispatcher import EventDispatcherMixin
        from wexample_event.dataclass.event import Event

        class Node(EventDispatcherMixin):
            _enable_bubbling = True

            def __init__(self, owner=None) -> None:
                self.owner = owner  # Different name

            def _get_bubbling_parent(self):
                return self.owner  # Return custom attribute

        owner = Node()
        child = Node(owner=owner)

        owner_events = []

        def listener(event: Event) -> None:
            owner_events.append(event.name)

        owner.add_event_listener("test", listener)

        child.dispatch("test")

        assert len(owner_events) == 1

    def test_bubbling_with_payload(self) -> None:
        """Test that payload is preserved during bubbling."""
        from wexample_event.common.dispatcher import EventDispatcherMixin
        from wexample_event.dataclass.event import Event

        class Node(EventDispatcherMixin):
            _enable_bubbling = True

            def __init__(self, parent=None) -> None:
                self.parent = parent

            def _get_bubbling_parent(self):
                return self.parent

        parent = Node()
        child = Node(parent=parent)

        received_payloads = []

        def listener(event: Event) -> None:
            received_payloads.append(event.payload)

        parent.add_event_listener("test", listener)

        child.dispatch("test", payload={"key": "value"})

        assert len(received_payloads) == 1
        assert received_payloads[0] == {"key": "value"}
