"""Interpreter for Grammar School."""

from typing import Any

from grammar_school.ast import CallChain, Expression, PropertyAccess, Value


class Interpreter:
    """Interprets CallChain AST and executes methods directly."""

    def __init__(self, dsl_instance: Any):
        """Initialize interpreter with a DSL instance containing method handlers."""
        self.dsl = dsl_instance
        self._method_handlers = self._collect_methods()

    def _collect_methods(self) -> dict[str, Any]:
        """Collect all methods marked with @method decorator."""
        methods = {}
        for name in dir(self.dsl):
            attr = getattr(self.dsl, name)
            if callable(attr) and getattr(attr, "_is_method", False):
                methods[name] = attr
        return methods

    def interpret(self, call_chain: CallChain) -> list[None]:
        """
        Interpret a CallChain by executing methods directly.

        Note: This method exists for compatibility but methods execute directly
        during interpret_stream. The returned list will contain None values
        (one per method call executed).
        """
        return list(self.interpret_stream(call_chain))

    def interpret_stream(self, call_chain: CallChain):
        """
        Interpret a CallChain by executing methods directly (streaming).

        This is a generator that executes methods one at a time, allowing
        for memory-efficient processing of large DSL programs.

        Yields:
            None: One None per method executed (for compatibility with Action-based interface)
        """
        for call in call_chain.calls:
            if call.name not in self._method_handlers:
                raise ValueError(f"Unknown method: {call.name}")

            handler = self._method_handlers[call.name]
            args = self._coerce_args(call.args)
            # Remove _context from args if present (methods don't need it)
            args.pop("_context", None)
            # Call method directly - it executes immediately
            handler(**args)
            # Yield None to indicate execution (for compatibility)
            yield None

    def _coerce_args(self, args: dict[str, Value | Expression | PropertyAccess]) -> dict[str, Any]:
        """
        Coerce Value, Expression, or PropertyAccess objects to native Python types.

        Function references (kind="function") are resolved to actual function handlers
        if they exist in the method handlers, otherwise passed as string identifiers.

        Expressions are evaluated to their result values.
        PropertyAccess is resolved to the actual property value.
        """
        coerced = {}
        positional_args = []

        # Collect positional arguments in order
        for name, value in sorted(args.items()):
            if name.startswith("_positional_"):
                try:
                    index = int(name.split("_")[-1])
                    positional_args.append((index, value))
                except ValueError:
                    # Argument name does not match expected '_positional_N' pattern; skip it.
                    pass

        # Sort by index and extract values
        positional_values = [v for _, v in sorted(positional_args)]

        # Process all named arguments (non-positional)
        for name, value in args.items():
            if name.startswith("_positional_"):
                continue  # Already handled above

            coerced[name] = self._evaluate_value(value)

        # Handle positional arguments - pass as *args if multiple, or single value if one
        if positional_values:
            # Coerce each positional value
            coerced_positionals = []
            for value in positional_values:
                coerced_positionals.append(self._evaluate_value(value))

            # If handler accepts *args, we need to pass them separately
            # For now, pass as _positional_0, _positional_1, etc. for backward compat
            # But also support passing as a list if handler expects it
            if len(coerced_positionals) == 1:
                coerced["_positional"] = coerced_positionals[0]
            else:
                # Multiple positionals - pass as list
                coerced["_positional"] = coerced_positionals

        return coerced

    def _evaluate_value(self, value: Value | Expression | PropertyAccess) -> Any:
        """
        Evaluate a Value, Expression, or PropertyAccess to a Python value.

        Args:
            value: Value, Expression, or PropertyAccess to evaluate

        Returns:
            Python value (int, float, str, bool, etc.)
        """
        if isinstance(value, Expression):
            return self._evaluate_expression(value)
        elif isinstance(value, PropertyAccess):
            return self._evaluate_property_access(value)
        elif isinstance(value, Value):
            if value.kind == "function":
                # Function reference - try to resolve to handler, otherwise pass as string
                func_name = value.value
                return self._method_handlers.get(func_name, func_name)
            else:
                return value.value
        else:
            # Fallback for unknown types
            return value

    def _evaluate_expression(self, expr: Expression) -> Any:
        """
        Evaluate an expression to a Python value.

        Args:
            expr: Expression to evaluate

        Returns:
            Python value result of the expression
        """
        if expr.operator is None:
            # Single value expression
            return self._evaluate_value(expr.left)

        # Binary operator expression
        left_val = self._evaluate_value(expr.left)
        right_val = self._evaluate_value(expr.right) if expr.right else None

        # Evaluate based on operator
        if expr.operator == "+":
            return left_val + right_val
        elif expr.operator == "-":
            return left_val - right_val
        elif expr.operator == "*":
            return left_val * right_val
        elif expr.operator == "/":
            if right_val == 0:
                raise ValueError("Division by zero is not allowed in Grammar School expressions.")
            return left_val / right_val
        elif expr.operator == "==":
            return left_val == right_val
        elif expr.operator == "!=":
            return left_val != right_val
        elif expr.operator == "<":
            return left_val < right_val
        elif expr.operator == ">":
            return left_val > right_val
        elif expr.operator == "<=":
            return left_val <= right_val
        elif expr.operator == ">=":
            return left_val >= right_val
        else:
            raise ValueError(f"Unknown operator: {expr.operator}")

    def _evaluate_property_access(self, prop: PropertyAccess) -> Any:
        """
        Evaluate property access like track.name.

        Args:
            prop: PropertyAccess to evaluate

        Returns:
            Python value of the property
        """
        # Get the object from DSL context
        # For now, we'll look for it in the DSL instance attributes
        # This is a simple implementation - users can override for more complex cases
        obj = getattr(self.dsl, prop.object_name, None)
        if obj is None:
            # Try as a variable in a context dict if DSL has one
            if hasattr(self.dsl, "_context") and isinstance(self.dsl._context, dict):
                obj = self.dsl._context.get(prop.object_name)
            if obj is None:
                raise ValueError(f"Unknown object: {prop.object_name}")

        # Navigate through properties
        result = obj
        for prop_name in prop.properties:
            if hasattr(result, prop_name):
                result = getattr(result, prop_name)
            elif isinstance(result, dict):
                result = result.get(prop_name)
                if result is None:
                    raise ValueError(f"Property '{prop_name}' not found in dict")
            else:
                raise ValueError(f"Property '{prop_name}' not found on {type(result).__name__}")

        return result
