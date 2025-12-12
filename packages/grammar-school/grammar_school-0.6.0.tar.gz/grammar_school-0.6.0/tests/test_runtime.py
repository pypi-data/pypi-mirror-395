"""Tests for runtime types."""

from grammar_school.runtime import Action, Runtime


class TestAction:
    """Test Action type."""

    def test_action_creation(self):
        """Test action creation."""
        action = Action(kind="greet", payload={"name": "World"})
        assert action.kind == "greet"
        assert action.payload == {"name": "World"}

    def test_action_empty_payload(self):
        """Test action with empty payload."""
        action = Action(kind="noop", payload={})
        assert action.kind == "noop"
        assert len(action.payload) == 0


class TestRuntime:
    """Test Runtime protocol."""

    def test_runtime_implementation(self):
        """Test that a class can implement Runtime."""

        class MyRuntime(Runtime):
            def __init__(self):
                self.actions = []

            def execute(self, action: Action) -> None:
                self.actions.append(action)

        runtime = MyRuntime()
        action = Action(kind="test", payload={})
        runtime.execute(action)
        assert len(runtime.actions) == 1
        assert runtime.actions[0] == action
