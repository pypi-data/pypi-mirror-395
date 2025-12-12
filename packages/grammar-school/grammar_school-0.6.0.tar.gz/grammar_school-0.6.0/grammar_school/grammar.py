"""Grammar definition system for Grammar School."""

from collections.abc import Callable
from pathlib import Path
from typing import Any, TypeVar

from grammar_school.ast import CallChain
from grammar_school.backend_lark import DEFAULT_GRAMMAR, LarkBackend
from grammar_school.grammar_builder import GrammarBuilder
from grammar_school.grammar_config import (
    load_grammar_from_config,
    load_grammar_from_toml,
    load_grammar_from_yaml,
)
from grammar_school.interpreter import Interpreter

T = TypeVar("T")


def rule(
    grammar: str | None = None,
    **kwargs: str | Any,
) -> Callable[[type[T]], type[T]]:
    """
    Decorator to define grammar rules.

    Supports three forms:
    1. @rule("call_chain: call ('.' call)*")
    2. @rule(call_chain="call ('.' call)*")
    3. @rule(call_chain = sym("call") + many(lit(".") + sym("call")))
    """
    if grammar is not None:

        def decorator_with_grammar(cls: type[T]) -> type[T]:
            if not hasattr(cls, "_grammar_rules"):
                cls._grammar_rules = {}  # type: ignore[attr-defined]
            cls._grammar_rules["_default"] = grammar  # type: ignore[attr-defined]
            return cls

        return decorator_with_grammar

    def decorator_with_kwargs(cls: type[T]) -> type[T]:
        if not hasattr(cls, "_grammar_rules"):
            cls._grammar_rules = {}  # type: ignore[attr-defined]
        for key, value in kwargs.items():
            cls._grammar_rules[key] = value  # type: ignore[attr-defined]
        return cls

    return decorator_with_kwargs


def method(func: Callable) -> Callable:
    """
    Decorator to mark a method as a direct implementation handler.

    Methods decorated with @method contain the actual implementation.
    The framework handles the Grammar/Runtime split internally.

    Example:
        @method
        def greet(self, name):
            print(f"Hello, {name}!")
            # Can do anything here - side effects, state changes, etc.
    """
    func._is_method = True  # type: ignore[attr-defined]
    return func


class Grammar:
    """
    Main Grammar class for Grammar School.

    Subclass this and define @verb methods to create your DSL handlers.
    Then use parse(), compile(), or execute() to process DSL scripts.

    **The Two-Layer Architecture:**

    1. **@verb methods** (in Grammar subclass):
       - Transform DSL syntax into Action data structures
       - Pure functions - no side effects, just return Actions
       - Example: `track(name="Drums")` → `Action(kind="create_track", payload={...})`

    2. **Runtime** (separate class):
       - Takes Actions and performs actual side effects
       - Handles state management, I/O, database operations, etc.
       - Example: Receives `Action(kind="create_track", ...)` → creates actual track in system

    This separation allows:
    - Same Grammar to work with different Runtimes (testing vs production)
    - @verb methods to be testable without side effects
    - Runtime to manage state independently of Grammar logic

    Example:
        ```python
        from grammar_school import Grammar, verb, Action

        class MyGrammar(Grammar):
            @verb
            def greet(self, name, _context=None):
                # Pure function - just returns Action, no side effects
                return Action(kind="greet", payload={"name": name})

        # Default runtime prints actions - no need to import Runtime!
        grammar = MyGrammar()
        grammar.execute('greet(name="World")')

        # Or provide a custom runtime for actual behavior
        from grammar_school import Runtime

        class MyRuntime(Runtime):
            def __init__(self):
                self.greetings = []  # Runtime manages state

            def execute(self, action: Action) -> None:
                # This is where side effects happen
                if action.kind == "greet":
                    name = action.payload["name"]
                    self.greetings.append(name)
                    print(f"Hello, {name}!")

        grammar = MyGrammar(runtime=MyRuntime())
        grammar.execute('greet(name="World")')
        ```
    """

    def __init__(
        self,
        grammar: str | GrammarBuilder | dict[str, Any] | Path | None = None,
        grammar_file: str | Path | None = None,
    ):
        """
        Initialize grammar with optional custom grammar definition.

        Args:
            grammar: Optional custom grammar. Can be:
                    - String (Lark grammar definition)
                    - GrammarBuilder instance
                    - Dict (grammar config - will be loaded via load_grammar_from_config)
                    - Path (to YAML/TOML grammar config file)
                    - None (uses Grammar School's default)
            grammar_file: Optional path to YAML/TOML grammar config file (alternative to grammar)

        Example:
            ```python
            # Using @method handlers - simple and direct
            class MyDSL(Grammar):
                @method
                def greet(self, name):
                    print(f"Hello, {name}!")

            dsl = MyDSL()  # No runtime needed
            dsl.execute('greet(name="World")')

            # Using string
            grammar = MyGrammar(grammar="start: call_chain\ncall_chain: call (DOT call)*")

            # Using GrammarBuilder
            from grammar_school import GrammarBuilder
            builder = GrammarBuilder.default()
            grammar = MyGrammar(grammar=builder)

            # Using config dict
            config = {
                "start": "start",
                "rules": [
                    {"name": "start", "definition": "call_chain"},
                    {"name": "call_chain", "definition": "call (DOT call)*"}
                ]
            }
            grammar = MyGrammar(grammar=config)

            # Using config file
            grammar = MyGrammar(grammar_file="grammar.yaml")
            # or
            grammar = MyGrammar(grammar="grammar.toml")  # Path as string
            ```
        """

        # Handle grammar parameter
        if grammar is None:
            if grammar_file is not None:
                # Load from file
                grammar_str = self._load_grammar_from_file(grammar_file)
            else:
                # Use default
                grammar_str = DEFAULT_GRAMMAR
        elif isinstance(grammar, dict):
            # Config dict - load it
            grammar_str = load_grammar_from_config(grammar)
        elif isinstance(grammar, str | Path) and (
            str(grammar).endswith(".yaml")
            or str(grammar).endswith(".yml")
            or str(grammar).endswith(".toml")
        ):
            # Path to config file
            grammar_str = self._load_grammar_from_file(grammar)
        elif isinstance(grammar, GrammarBuilder):
            # GrammarBuilder - convert to string
            grammar_str = grammar.build()
        else:
            # String (Lark grammar definition)
            grammar_str = str(grammar)

        self.backend = LarkBackend(grammar_str)
        self.interpreter = Interpreter(self)

    def _load_grammar_from_file(self, path: str | Path) -> str:
        """Load grammar from YAML or TOML config file."""
        path = Path(path)
        if path.suffix in (".yaml", ".yml"):
            return load_grammar_from_yaml(path)
        elif path.suffix == ".toml":
            return load_grammar_from_toml(path)
        else:
            raise ValueError(
                f"Unsupported grammar config file format: {path.suffix}. Use .yaml, .yml, or .toml"
            )

    def parse(self, code: str) -> CallChain:
        """Parse DSL code into a CallChain AST."""
        return self.backend.parse(code)

    def compile(self, code: str) -> list[None]:
        """
        Compile DSL code by executing methods.

        Note: Methods execute directly during compilation.
        Returns a list of None values (one per method call).
        """
        call_chain = self.parse(code)
        return self.interpreter.interpret(call_chain)

    def stream(self, code: str):
        """
        Stream method executions from DSL code.

        This is a generator that executes methods one at a time, allowing
        for memory-efficient processing and real-time execution of large DSL programs.

        Args:
            code: DSL code string to execute and stream

        Yields:
            None: One None per method executed (methods execute during iteration)

        Example:
            ```python
            grammar = MyGrammar()
            for _ in grammar.stream('greet(name="A").greet(name="B").greet(name="C")'):
                # Methods execute as they're called
                pass
            ```
        """
        call_chain = self.parse(code)
        yield from self.interpreter.interpret_stream(call_chain)

    def execute(self, code: str) -> None:
        """
        Execute DSL code by calling methods directly.

        Methods decorated with @method are executed immediately when called.
        No runtime is needed - methods contain their own implementation.

        Args:
            code: DSL code string to execute

        Example:
            ```python
            class MyDSL(Grammar):
                @method
                def greet(self, name):
                    print(f"Hello, {name}!")

            dsl = MyDSL()
            dsl.execute('greet(name="World")')  # Prints: Hello, World!
            ```
        """
        call_chain = self.parse(code)
        # Execute methods directly - they run during interpretation
        for _ in self.interpreter.interpret_stream(call_chain):
            pass  # Methods execute during interpretation


def sym(name: str) -> Any:
    """Create a nonterminal symbol."""
    return {"type": "sym", "name": name}


def lit(text: str) -> Any:
    """Create a literal terminal."""
    return {"type": "lit", "text": text}


def many(expr: Any) -> Any:
    """Create a many (zero or more) combinator."""
    return {"type": "many", "expr": expr}


class _Optional:
    """Helper for optional combinators."""

    def __init__(self, expr: Any):
        self.expr = expr

    def optional(self) -> Any:
        """Make an expression optional."""
        return {"type": "optional", "expr": self.expr}


def optional(expr: Any) -> Any:
    """Create an optional combinator."""
    return _Optional(expr).optional()
