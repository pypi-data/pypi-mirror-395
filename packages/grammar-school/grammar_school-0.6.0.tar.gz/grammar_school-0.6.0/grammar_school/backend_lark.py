"""Lark parser backend for Grammar School."""

from lark import Lark, Transformer, v_args

from grammar_school.ast import Arg, Call, CallChain, Expression, PropertyAccess, Value
from grammar_school.smart_transformer import SmartTransformer

DEFAULT_GRAMMAR = """
start: statement+

// Statement is a call chain (which can be a single call or multiple chained calls)
statement: call_chain

call_chain: call (DOT call)*
call: IDENTIFIER "(" args? ")"
args: arg (COMMA arg)*
arg: IDENTIFIER "=" expression
    | expression

// Expression with operator precedence (lowest to highest)
expression: comparison
comparison: addition (comparison_op addition)*
comparison_op: EQ | NE | LT | GT | LE | GE
addition: multiplication (add_op multiplication)*
add_op: PLUS | MINUS
multiplication: atom (mul_op atom)*
mul_op: MUL | DIV
atom: NUMBER
    | STRING
    | BOOL
    | IDENTIFIER
    | property_access  // Must come after IDENTIFIER - Lark prefers longer matches
    | function_ref
    | "(" expression ")"

// Property access: track.name
property_access: IDENTIFIER (DOT IDENTIFIER)+

// Function reference: @function_name syntax
function_ref: "@" IDENTIFIER

// Operators
PLUS: "+"
MINUS: "-"
MUL: "*"
DIV: "/"
EQ: "=="
NE: "!="
LT: "<"
GT: ">"
LE: "<="
GE: ">="

DOT: "."
COMMA: ","
NUMBER: /-?\\d+(\\.\\d+)?/
STRING: /"([^"\\\\]|\\\\.)*"|'([^'\\\\]|\\\\.)*'/
IDENTIFIER: /[a-zA-Z_][a-zA-Z0-9_]*/
BOOL: "true" | "false"

%import common.WS
%ignore WS
"""


@v_args(inline=True)
class ASTTransformer(Transformer):
    """Transforms Lark parse tree into Grammar School AST."""

    def start(self, *statements):
        # If single statement, return it directly (backward compatibility)
        if len(statements) == 1:
            statement = statements[0]
            # If it's already a CallChain, return it
            if isinstance(statement, CallChain):
                return statement
            # If it's a single Call, wrap it in a CallChain
            if isinstance(statement, Call):
                return CallChain(calls=[statement])
            return statement

        # Multiple statements - combine all calls into one CallChain
        all_calls = []
        for statement in statements:
            if isinstance(statement, CallChain):
                all_calls.extend(statement.calls)
            elif isinstance(statement, Call):
                all_calls.append(statement)
        return CallChain(calls=all_calls)

    def statement(self, call_chain):
        # Statement is always a call_chain (which can contain one or more calls)
        # Just return the call_chain as-is
        return call_chain

    def call_chain(self, *calls):
        # Filter out DOT tokens - only keep Call objects
        filtered_calls = [
            call
            for call in calls
            if not (hasattr(call, "type") and call.type == "DOT") and isinstance(call, Call)
        ]
        return CallChain(calls=filtered_calls)

    def call(self, name, args=None):
        from grammar_school.ast import Expression, PropertyAccess, Value

        args_dict: dict[str, Value | Expression | PropertyAccess] = {}
        positional_index = 0
        if args:
            for arg in args:
                if isinstance(arg, Arg):
                    args_dict[arg.name] = arg.value
                else:
                    # Handle multiple positional arguments
                    # Convert to Value if it's a raw token
                    if isinstance(arg, Value | Expression | PropertyAccess):
                        args_dict[f"_positional_{positional_index}"] = arg
                    else:
                        # Convert token to Value
                        args_dict[f"_positional_{positional_index}"] = self._token_to_value(arg)
                    positional_index += 1
        return Call(name=str(name), args=args_dict)

    def _token_to_value(self, token) -> Value:
        """Convert a token to a Value."""
        token_str = str(token)
        if token.type == "NUMBER":
            try:
                num_val: int | float = int(token_str)
            except ValueError:
                num_val = float(token_str)
            return Value(kind="number", value=num_val)
        elif token.type == "STRING":
            return Value(kind="string", value=token_str.strip('"').strip("'"))
        elif token.type == "BOOL":
            return Value(kind="bool", value=token_str.lower() == "true")
        elif token.type == "IDENTIFIER":
            return Value(kind="identifier", value=token_str)
        else:
            return Value(kind="string", value=token_str)

    def args(self, *arg_list):
        # Filter out comma tokens
        return [arg for arg in arg_list if not (hasattr(arg, "type") and arg.type == "COMMA")]

    def arg(self, *parts):
        # Filter out = tokens
        filtered = [p for p in parts if not (hasattr(p, "type") and p.type == "=")]
        if len(filtered) == 2:
            name, value = filtered
            # Ensure value is Expression, PropertyAccess, or Value
            if not isinstance(value, Value | Expression | PropertyAccess):
                value = (
                    self._token_to_value(value)
                    if hasattr(value, "type")
                    else Value(kind="string", value=str(value))
                )
            return Arg(name=str(name), value=value)
        elif len(filtered) == 1:
            # Positional argument
            value = filtered[0]
            # Keep Expression, PropertyAccess, or Value as-is
            if not isinstance(value, Value | Expression | PropertyAccess):
                value = (
                    self._token_to_value(value)
                    if hasattr(value, "type")
                    else Value(kind="string", value=str(value))
                )
            return value
        else:
            # Fallback: return first part as value
            return parts[0] if parts else Value(kind="string", value="")

    def function_ref(self, identifier):
        """Handle function reference syntax @function_name."""
        # Return a Value with kind="function"
        func_name = str(identifier)
        return Value(kind="function", value=func_name)

    def expression(self, expr):
        """Handle expression - just pass through."""
        return expr

    def comparison(self, *parts):
        """Handle comparison expressions: addition (comparison_op addition)*"""
        if len(parts) == 1:
            return parts[0]
        # Build left-associative expression tree
        result = parts[0]
        for i in range(1, len(parts), 2):
            if i + 1 < len(parts):
                op = str(parts[i])
                right = parts[i + 1]
                result = Expression(operator=op, left=result, right=right)
        return result

    def comparison_op(self, op):
        """Handle comparison operator."""
        return str(op)

    def addition(self, *parts):
        """Handle addition expressions: multiplication (add_op multiplication)*"""
        if len(parts) == 1:
            return parts[0]
        # Build left-associative expression tree
        result = parts[0]
        for i in range(1, len(parts), 2):
            if i + 1 < len(parts):
                op = str(parts[i])
                right = parts[i + 1]
                result = Expression(operator=op, left=result, right=right)
        return result

    def add_op(self, op):
        """Handle addition operator."""
        return str(op)

    def multiplication(self, *parts):
        """Handle multiplication expressions: atom (mul_op atom)*"""
        if len(parts) == 1:
            return parts[0]
        # Build left-associative expression tree
        result = parts[0]
        for i in range(1, len(parts), 2):
            if i + 1 < len(parts):
                op = str(parts[i])
                right = parts[i + 1]
                result = Expression(operator=op, left=result, right=right)
        return result

    def mul_op(self, op):
        """Handle multiplication operator."""
        return str(op)

    def atom(self, atom_value):
        """Handle atom (base value)."""
        # If it's already a Value, Expression, PropertyAccess, or function_ref, return as-is
        if isinstance(atom_value, Value | Expression | PropertyAccess):
            return atom_value
        # Otherwise, convert token to Value
        return self._token_to_value(atom_value)

    def property_access(self, *parts):
        """Handle property access: IDENTIFIER (DOT IDENTIFIER)+"""
        # Filter out DOT tokens
        identifiers = [
            str(part) for part in parts if not (hasattr(part, "type") and part.type == "DOT")
        ]
        if len(identifiers) < 2:
            # Single identifier - return as Value
            return Value(kind="identifier", value=identifiers[0])
        # Multiple identifiers - property access
        return PropertyAccess(object_name=identifiers[0], properties=identifiers[1:])

    def value(self, token):
        # Check if token is already a Value (from function_ref transformation)
        if isinstance(token, Value):
            return token

        token_str = str(token)

        if token.type == "NUMBER":
            try:
                num_val: int | float = int(token_str)
            except ValueError:
                num_val = float(token_str)
            return Value(kind="number", value=num_val)
        elif token.type == "STRING":
            return Value(kind="string", value=token_str.strip('"').strip("'"))
        elif token.type == "BOOL":
            return Value(kind="bool", value=token_str.lower() == "true")
        elif token.type == "IDENTIFIER":
            return Value(kind="identifier", value=token_str)
        else:
            return Value(kind="string", value=token_str)


class LarkBackend:
    """Lark-based parser backend."""

    def __init__(
        self,
        grammar: str = DEFAULT_GRAMMAR,
        transformer: Transformer | None = None,
        use_smart_transformer: bool = True,
    ):
        """
        Initialize with a Lark grammar string.

        Args:
            grammar: Lark grammar string
            transformer: Optional custom transformer (if None, uses SmartTransformer or ASTTransformer)
            use_smart_transformer: If True, use SmartTransformer (adapts to any grammar).
                                 If False, use ASTTransformer (coupled to default grammar).
        """
        self.parser = Lark(grammar, start="start", parser="lalr")
        if transformer is not None:
            self.transformer = transformer
        elif use_smart_transformer:
            # SmartTransformer works with any grammar, including the default
            self.transformer = SmartTransformer()
        else:
            # ASTTransformer is faster for default grammar (backward compatibility)
            self.transformer = ASTTransformer()

    def parse(self, code: str) -> CallChain:
        """Parse code into a CallChain AST."""
        tree = self.parser.parse(code)
        result = self.transformer.transform(tree)
        # Handle case where transformer returns a list (unwrap it)
        if isinstance(result, list):
            if result and isinstance(result[0], CallChain):
                return result[0]
            # If list contains Calls, create a CallChain using iterator
            from grammar_school.ast import Call

            # Use generator expression instead of list comprehension for memory efficiency
            calls_iter = (item for item in result if isinstance(item, Call))
            calls = list(calls_iter)  # Convert to list for CallChain
            if calls:
                return CallChain(calls=calls)
            # Empty list - return empty CallChain
            return CallChain(calls=[])
        # Result should be a CallChain
        if isinstance(result, CallChain):
            return result
        # If it's a single Call, wrap it
        from grammar_school.ast import Call

        if isinstance(result, Call):
            return CallChain(calls=[result])
        # Fallback: return empty CallChain
        return CallChain(calls=[])

    @staticmethod
    def clean_grammar_for_cfg(grammar: str) -> str:
        """
        Clean Lark grammar for use with CFG systems (e.g., GPT-5).

        Removes Lark-specific directives that aren't supported in standard CFG:
        - %import directives
        - %ignore directives
        - Other %-prefixed directives

        Args:
            grammar: Lark grammar string with directives

        Returns:
            Cleaned grammar string suitable for CFG systems

        Example:
            ```python
            cleaned = LarkBackend.clean_grammar_for_cfg(DEFAULT_GRAMMAR)
            # Use cleaned grammar with GPT-5 CFG
            ```
        """
        return "\n".join(line for line in grammar.split("\n") if not line.strip().startswith("%"))
