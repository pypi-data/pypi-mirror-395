"""AST types for Grammar School."""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Value:
    """A value in the AST (number, string, identifier, etc.)."""

    kind: str
    value: Any


@dataclass
class PropertyAccess:
    """Property access expression like track.name."""

    object_name: str
    properties: list[str]  # List of property names (e.g., ["name"] for track.name)


@dataclass
class Expression:
    """An expression with operators."""

    operator: str | None  # None for single value, operator string for binary ops
    left: Expression | Value | PropertyAccess
    right: Expression | Value | PropertyAccess | None  # None for unary ops or single values


@dataclass
class Arg:
    """A named argument to a call."""

    name: str
    value: Value | Expression | PropertyAccess


@dataclass
class Call:
    """A single function call with named arguments."""

    name: str
    args: dict[str, Value | Expression | PropertyAccess]


@dataclass
class CallChain:
    """
    A chain of calls connected by dots (method chaining).

    Can be initialized with a list, iterator, or any iterable of Call objects.
    """

    calls: list[Call] = field(default_factory=list)

    def __init__(self, calls: list[Call] | Iterator[Call] | Iterable[Call] | None = None):
        """
        Initialize CallChain with calls.

        Args:
            calls: List, iterator, or iterable of Call objects. If None, creates empty chain.
        """
        if calls is None:
            object.__setattr__(self, "calls", [])
        elif isinstance(calls, list):
            object.__setattr__(self, "calls", calls)
        else:
            # Convert iterator/iterable to list
            object.__setattr__(self, "calls", list(calls))

    def __iter__(self) -> Iterator[Call]:
        """Make CallChain iterable."""
        return iter(self.calls)
