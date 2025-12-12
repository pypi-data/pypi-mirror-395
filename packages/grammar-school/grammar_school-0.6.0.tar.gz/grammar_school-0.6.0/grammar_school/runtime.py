"""Runtime types for Grammar School."""

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass
class Action:
    """
    A runtime action produced by the interpreter.

    Actions are data structures that represent "what to do" but not "how to do it".
    They are produced by @verb methods in your Grammar subclass and then executed
    by the Runtime.

    Example:
        Action(kind="create_track", payload={"name": "Drums", "color": "blue"})
    """

    kind: str
    payload: dict[str, Any]


class Runtime(Protocol):
    """
    Protocol for runtime implementations that execute actions.

    The Runtime is responsible for taking Actions (produced by @verb methods) and
    performing the actual side effects - printing, database operations, API calls,
    file I/O, etc.

    This separation allows:
    - @verb methods to be pure (just return Action data structures)
    - Runtime to handle all side effects and state management
    - Same Grammar can work with different Runtimes (testing, production, etc.)

    Example:
        ```python
        class MyRuntime(Runtime):
            def __init__(self):
                self.tasks = {}  # Runtime manages state

            def execute(self, action: Action) -> None:
                if action.kind == "create_task":
                    # Perform actual side effect
                    self.tasks[action.payload["name"]] = action.payload
                    print(f"Created: {action.payload['name']}")
        ```
    """

    def execute(self, action: Action) -> None:
        """
        Execute a single action.

        This is where the actual work happens - side effects, state changes,
        I/O operations, etc. The action contains the "what" (kind and payload),
        and this method defines the "how".

        Args:
            action: The action to execute
        """
        ...
