"""Smart AST transformer that adapts to any grammar structure."""

from typing import Any

from lark import Transformer, v_args

from grammar_school.ast import Arg, Call, CallChain, Expression, PropertyAccess, Value


@v_args(inline=True)
class SmartTransformer(Transformer):
    """
    A smart transformer that adapts to any grammar structure.

    This transformer automatically handles:
    - Any grammar that produces call chains (default behavior)
    - Custom grammar structures via configuration
    - Fallback to generic tree transformation

    Usage:
        ```python
        # Default: works with standard Grammar School grammar
        transformer = SmartTransformer()

        # Custom: configure for specific grammar structure
        transformer = SmartTransformer(
            start_rule="statement",
            call_rule="function_call",
            chain_rule="statement_list"
        )
        ```
    """

    def __init__(
        self,
        start_rule: str = "start",
        call_rule: str = "call",
        chain_rule: str = "call_chain",
        args_rule: str = "args",
        arg_rule: str = "arg",
        value_rule: str = "value",
        function_ref_rule: str = "function_ref",
    ):
        """
        Initialize smart transformer with grammar rule names.

        Args:
            start_rule: Name of the start rule in the grammar
            call_rule: Name of the rule that represents a function call
            chain_rule: Name of the rule that represents a chain of calls
            args_rule: Name of the rule that represents arguments
            arg_rule: Name of the rule that represents a single argument
            value_rule: Name of the rule that represents a value
            function_ref_rule: Name of the rule that represents a function reference
        """
        super().__init__()
        self.start_rule = start_rule
        self.call_rule = call_rule
        self.chain_rule = chain_rule
        self.args_rule = args_rule
        self.arg_rule = arg_rule
        self.value_rule = value_rule
        self.function_ref_rule = function_ref_rule

    def _get_method_name(self, rule_name: str) -> str:
        """Convert rule name to transformer method name."""
        # Replace hyphens/underscores and convert to snake_case
        return rule_name.replace("-", "_").replace(".", "_")

    def __default__(self, data: str, children: list, meta: Any) -> Any:
        """
        Default transformer method that handles any rule not explicitly defined.

        This allows the transformer to work with any grammar structure by:
        1. Trying to match known patterns (call, chain, etc.)
        2. Falling back to generic tree transformation
        """
        rule_name = data

        # Handle start rule - expect it to contain a call chain
        if rule_name == self.start_rule:
            if len(children) == 1:
                result = children[0]
                # Ensure we return a CallChain
                if isinstance(result, CallChain):
                    return result
                elif isinstance(result, Call):
                    return CallChain(calls=[result])
                elif isinstance(result, list):
                    # If it's a list, extract the CallChain or create one
                    if result and isinstance(result[0], CallChain):
                        return result[0]
                    chain = self._create_call_chain(result)
                    return chain if isinstance(chain, CallChain) else CallChain(calls=[])
                else:
                    # Unknown type - return empty chain
                    return CallChain(calls=[])
            # If start rule has multiple children, try to create a chain
            return self._create_call_chain(children)

        # Handle call chain - collect all calls
        if rule_name == self.chain_rule or "chain" in rule_name.lower() or rule_name == "expr":
            # If it's a single call, wrap it in a CallChain
            if len(children) == 1 and isinstance(children[0], Call):
                return CallChain(calls=[children[0]])
            return self._create_call_chain(children)

        # Handle function call
        if (
            rule_name == self.call_rule
            or "call" in rule_name.lower()
            or rule_name.endswith("_call")
        ):
            return self._create_call(children)

        # Handle arguments
        if rule_name == self.args_rule or rule_name.endswith("args") or rule_name == "params":
            return self._create_args(children)

        # Handle single argument
        if rule_name == self.arg_rule or rule_name.endswith("arg") or rule_name == "param":
            return self._create_arg(children)

        # Handle value
        if rule_name == self.value_rule or rule_name == "value":
            if children:
                return self._create_value(children[0])
            return None

        # Handle function reference
        if rule_name == self.function_ref_rule or "function_ref" in rule_name.lower():
            return self._create_function_ref(children)

        # Generic fallback: return the first child or the tree itself
        if len(children) == 1:
            return children[0]
        return children

    def _create_call_chain(self, children: list) -> CallChain:
        """Create a CallChain from children, filtering out non-Call objects."""

        def _iter_calls():
            """Generator that yields Call objects from children."""
            for child in children:
                # Filter out tokens (DOT, COMMA, etc.)
                if hasattr(child, "type") and child.type in ("DOT", "COMMA"):
                    continue
                # Only include Call objects
                if isinstance(child, Call):
                    yield child
                # If child is a CallChain, extract its calls
                elif isinstance(child, CallChain):
                    yield from child.calls

        # Convert iterator to list for CallChain (dataclass requires concrete list)
        calls = list(_iter_calls())
        return CallChain(calls=calls)

    def _create_call(self, children: list) -> Call:
        """Create a Call from children."""
        if not children:
            raise ValueError("Call must have at least a name")

        # First child is the function name (IDENTIFIER token)
        name = str(children[0])

        # Remaining children are arguments
        args_dict = {}
        positional_index = 0

        for child in children[1:]:
            # Filter out tokens
            if hasattr(child, "type") and child.type in ("COMMA", "LPAR", "RPAR", "(", ")"):
                continue

            if isinstance(child, Arg):
                args_dict[child.name] = child.value
            elif isinstance(child, list):
                # Handle list of args
                for arg in child:
                    if isinstance(arg, Arg):
                        args_dict[arg.name] = arg.value
                    else:
                        # Keep Expression, PropertyAccess, or Value as-is
                        if not isinstance(arg, Value | Expression | PropertyAccess):
                            arg = self._create_value(arg)
                        args_dict[f"_positional_{positional_index}"] = arg
                        positional_index += 1
            else:
                # Positional argument - keep Expression, PropertyAccess, or Value as-is
                if not isinstance(child, Value | Expression | PropertyAccess):
                    child = self._create_value(child)
                args_dict[f"_positional_{positional_index}"] = child
                positional_index += 1

        return Call(name=name, args=args_dict)

    def _create_args(self, children: list) -> list:
        """Create a list of arguments, filtering out comma tokens."""

        def _iter_args():
            """Generator that yields arguments, filtering out comma tokens."""
            for child in children:
                if hasattr(child, "type") and child.type == "COMMA":
                    continue
                yield child

        # Return as list for compatibility, but could be made lazy
        return list(_iter_args())

    def _create_arg(self, children: list) -> Arg | Value | Expression | PropertyAccess:
        """Create an Arg (named) or return Value/Expression/PropertyAccess (positional)."""
        # Filter out = tokens
        filtered = [c for c in children if not (hasattr(c, "type") and c.type in ("=", "EQ"))]

        if len(filtered) == 2:
            # Named argument: IDENTIFIER = value
            name = str(filtered[0])
            value = filtered[1]
            # Keep Expression, PropertyAccess, or Value as-is
            if not isinstance(value, Value | Expression | PropertyAccess):
                value = self._create_value(value)
            return Arg(name=name, value=value)
        elif len(filtered) == 1:
            # Positional argument: just the value
            value = filtered[0]
            # Keep Expression, PropertyAccess, or Value as-is
            if not isinstance(value, Value | Expression | PropertyAccess):
                value = self._create_value(value)
            return value
        else:
            # Empty argument - return empty string value as fallback
            return Value(kind="string", value="")

    def _create_value(self, token: Any) -> Value:
        """Create a Value from a token."""
        if isinstance(token, Value):
            return token

        if not hasattr(token, "type"):
            # If it's already a string/number, wrap it
            if isinstance(token, int | float):
                return Value(kind="number", value=token)
            if isinstance(token, str):
                return Value(kind="string", value=token)
            return Value(kind="string", value=str(token))

        token_str = str(token)
        token_type = token.type

        if token_type == "NUMBER":
            try:
                num_val: int | float = int(token_str)
            except ValueError:
                num_val = float(token_str)
            return Value(kind="number", value=num_val)
        elif token_type == "STRING":
            return Value(kind="string", value=token_str.strip('"').strip("'"))
        elif token_type == "BOOL":
            return Value(kind="bool", value=token_str.lower() == "true")
        elif token_type == "IDENTIFIER":
            return Value(kind="identifier", value=token_str)
        else:
            return Value(kind="string", value=token_str)

    def _create_function_ref(self, children: list) -> Value:
        """Create a function reference Value."""
        if not children:
            raise ValueError("Function reference must have an identifier")
        func_name = str(children[-1])  # Last child is the identifier (after @)
        return Value(kind="function", value=func_name)

    # Explicit methods for default grammar (for backward compatibility and performance)
    def start(self, *statements):
        """
        Handle start rule with multiple statements.

        Combines all statements into a single CallChain.
        """
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

    def call_chain(self, *calls):
        """Handle call_chain rule - default grammar."""
        return self._create_call_chain(list(calls))

    def call(self, name, args=None):
        """Handle call rule - default grammar."""
        children = [name]
        if args:
            children.append(args)
        return self._create_call(children)

    def args(self, *arg_list):
        """Handle args rule - default grammar."""
        return self._create_args(list(arg_list))

    def arg(self, *parts):
        """Handle arg rule - default grammar."""
        return self._create_arg(list(parts))

    def value(self, token):
        """Handle value rule - default grammar."""
        return self._create_value(token)

    def function_ref(self, identifier):
        """Handle function_ref rule - default grammar."""
        return self._create_function_ref([identifier])

    # Expression handling methods
    def expression(self, expr):
        """Handle expression - pass through."""
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
        # If it's already a Value, Expression, PropertyAccess, return as-is
        if isinstance(atom_value, Value | Expression | PropertyAccess):
            return atom_value
        # Otherwise, convert token to Value using the generic method
        return self._create_value(atom_value)

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
