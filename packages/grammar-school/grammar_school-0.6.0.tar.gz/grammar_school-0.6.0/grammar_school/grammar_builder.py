"""Programmatic grammar builder for Grammar School."""


class Rule:
    """Represents a grammar rule."""

    def __init__(self, name: str, definition: str, description: str | None = None):
        """
        Initialize a grammar rule.

        Args:
            name: Rule name (e.g., "call_chain")
            definition: Rule definition in Lark syntax (e.g., "call (DOT call)*")
            description: Optional human-readable description
        """
        self.name = name
        self.definition = definition
        self.description = description

    def __str__(self) -> str:
        """Convert rule to Lark grammar string."""
        result = []
        if self.description:
            result.append(f"// {self.description}")
        result.append(f"{self.name}: {self.definition}")
        return "\n".join(result)


class Terminal:
    """Represents a terminal (token) in the grammar."""

    def __init__(self, name: str, pattern: str, description: str | None = None):
        """
        Initialize a terminal.

        Args:
            name: Terminal name (e.g., "DOT")
            pattern: Regex pattern or literal string (e.g., '"\\.\"' or '/[a-zA-Z_][a-zA-Z0-9_]*/')
            description: Optional human-readable description
        """
        self.name = name
        self.pattern = pattern
        self.description = description

    def __str__(self) -> str:
        """Convert terminal to Lark grammar string."""
        result = []
        if self.description:
            result.append(f"// {self.description}")
        # If pattern doesn't start with /, it's a literal
        if not self.pattern.startswith("/"):
            result.append(f'{self.name}: "{self.pattern}"')
        else:
            result.append(f"{self.name}: {self.pattern}")
        return "\n".join(result)


class GrammarBuilder:
    """Builder for creating grammars programmatically."""

    def __init__(self):
        """Initialize an empty grammar builder."""
        self.rules: list[Rule] = []
        self.terminals: list[Terminal] = []
        self.start_rule: str = "start"
        self.directives: list[str] = []

    def rule(self, name: str, definition: str, description: str | None = None) -> "GrammarBuilder":
        """
        Add a grammar rule.

        Args:
            name: Rule name
            definition: Rule definition in Lark syntax
            description: Optional description

        Returns:
            Self for method chaining

        Example:
            ```python
            builder.rule("call_chain", "call (DOT call)*", "Chain of calls")
            ```
        """
        self.rules.append(Rule(name, definition, description))
        return self

    def terminal(self, name: str, pattern: str, description: str | None = None) -> "GrammarBuilder":
        """
        Add a terminal (token).

        Args:
            name: Terminal name
            pattern: Regex pattern or literal string
            description: Optional description

        Returns:
            Self for method chaining

        Example:
            ```python
            builder.terminal("DOT", ".", "Dot separator")
            builder.terminal("IDENTIFIER", "/[a-zA-Z_][a-zA-Z0-9_]*/", "Identifier pattern")
            ```
        """
        self.terminals.append(Terminal(name, pattern, description))
        return self

    def start(self, rule_name: str) -> "GrammarBuilder":
        """
        Set the start rule.

        Args:
            rule_name: Name of the start rule

        Returns:
            Self for method chaining
        """
        self.start_rule = rule_name
        return self

    def directive(self, directive: str) -> "GrammarBuilder":
        """
        Add a Lark directive (e.g., %import, %ignore).

        Args:
            directive: Directive string (e.g., "%import common.WS")

        Returns:
            Self for method chaining
        """
        self.directives.append(directive)
        return self

    def build(self) -> str:
        """
        Build the complete Lark grammar string.

        Returns:
            Complete grammar string ready for Lark parser
        """
        lines = []

        # Find the target for the start rule
        start_target = None
        start_rule_obj = None

        for rule in self.rules:
            if rule.name == self.start_rule:
                start_rule_obj = rule
                # If start rule exists, use its definition directly
                start_target = rule.definition
                break

        if start_target is None:
            # No rule named after start_rule, use first rule's name
            start_target = self.rules[0].name if self.rules else "call_chain"

        # Add start rule (only if it's different from a rule we'll add later)
        if start_rule_obj is None:
            # Start rule doesn't exist as a regular rule, add it
            lines.append(f"{self.start_rule}: {start_target}")
            lines.append("")

        # Add all rules (if start rule exists as a rule, it will be included here)
        for rule in self.rules:
            lines.append(str(rule))
            lines.append("")

        # Add terminals
        for terminal in self.terminals:
            lines.append(str(terminal))
            lines.append("")

        # Add directives
        for directive in self.directives:
            lines.append(directive)

        return "\n".join(lines)

    @classmethod
    def default(cls) -> "GrammarBuilder":
        """
        Create the default Grammar School grammar.

        Returns:
            GrammarBuilder with default grammar rules
        """
        builder = cls()
        builder.rule("start", "call_chain", "Entry point: a chain of function calls")
        builder.start("start")
        builder.rule("call_chain", "call (DOT call)*", "Chain of calls connected with dots")
        builder.rule("call", 'IDENTIFIER "(" args? ")"', "Single function call")
        builder.rule("args", "arg (COMMA arg)*", "Comma-separated list of arguments")
        builder.rule("arg", 'IDENTIFIER "=" value | value', "Single argument: named or positional")
        builder.rule(
            "value",
            "NUMBER | STRING | BOOL | IDENTIFIER | function_ref",
            "A value can be a number, string, identifier, boolean, or function reference",
        )
        builder.rule("function_ref", '"@" IDENTIFIER', "Function reference using @ syntax")
        builder.terminal("DOT", ".", "Dot separator for method chaining")
        builder.terminal("COMMA", ",", "Comma separator for arguments")
        builder.terminal("NUMBER", "/-?\\d+(\\.\\d+)?/", "Numeric value (integer or float)")
        builder.terminal("STRING", "/\"([^\"\\\\]|\\\\.)*\"|'([^'\\\\]|\\\\.)*'/", "String literal")
        builder.terminal("IDENTIFIER", "/[a-zA-Z_][a-zA-Z0-9_]*/", "Identifier name")
        # BOOL needs to be defined as a rule, not a terminal, because it uses alternation
        builder.rule("BOOL", '"true" | "false"', "Boolean literal")
        builder.directive("%import common.WS")
        builder.directive("%ignore WS")
        return builder
