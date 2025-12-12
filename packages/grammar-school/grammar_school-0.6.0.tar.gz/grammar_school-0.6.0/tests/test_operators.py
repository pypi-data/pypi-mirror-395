"""Tests for built-in operators and expressions."""

from grammar_school import Grammar, method
from grammar_school.ast import Expression, PropertyAccess, Value
from grammar_school.backend_lark import LarkBackend


class TestOperators:
    """Test built-in operators."""

    def test_parse_simple_arithmetic(self):
        """Test parsing simple arithmetic expressions."""
        backend = LarkBackend()

        # Test addition with positional argument
        result = backend.parse("add(1 + 2)")
        assert len(result.calls) == 1
        call = result.calls[0]
        assert call.name == "add"
        assert "_positional_0" in call.args
        expr = call.args["_positional_0"]
        assert isinstance(expr, Expression)
        assert expr.operator == "+"
        assert isinstance(expr.left, Value)
        assert expr.left.value == 1
        assert isinstance(expr.right, Value)
        assert expr.right.value == 2

        # Test addition with named argument
        result = backend.parse("add(a=1 + 2)")
        assert len(result.calls) == 1
        call = result.calls[0]
        assert call.name == "add"
        assert "a" in call.args
        expr = call.args["a"]
        assert isinstance(expr, Expression)
        assert expr.operator == "+"
        assert isinstance(expr.left, Value)
        assert expr.left.value == 1
        assert isinstance(expr.right, Value)
        assert expr.right.value == 2

    def test_parse_comparison(self):
        """Test parsing comparison expressions."""
        backend = LarkBackend()

        # Test equality
        result = backend.parse('filter(tracks, track.name == "FX")')
        assert len(result.calls) == 1
        call = result.calls[0]
        assert call.name == "filter"
        # Second argument should be an expression
        assert "_positional_1" in call.args
        expr = call.args["_positional_1"]
        assert isinstance(expr, Expression)
        assert expr.operator == "=="

    def test_parse_property_access(self):
        """Test parsing property access."""
        backend = LarkBackend()

        result = backend.parse("get(track.name)")
        assert len(result.calls) == 1
        call = result.calls[0]
        assert "_positional_0" in call.args
        prop = call.args["_positional_0"]
        assert isinstance(prop, PropertyAccess)
        assert prop.object_name == "track"
        assert prop.properties == ["name"]

    def test_parse_complex_expression(self):
        """Test parsing complex expressions with precedence."""
        backend = LarkBackend()

        # Test: 1 + 2 * 3 (should respect precedence)
        result = backend.parse("calc(value=1 + 2 * 3)")
        assert len(result.calls) == 1
        call = result.calls[0]
        expr = call.args["value"]
        assert isinstance(expr, Expression)
        # Should be: (1 + (2 * 3))
        assert expr.operator == "+"
        assert isinstance(expr.left, Value)
        assert expr.left.value == 1
        assert isinstance(expr.right, Expression)
        assert expr.right.operator == "*"


class TestExpressionEvaluation:
    """Test expression evaluation."""

    def test_evaluate_arithmetic(self):
        """Test evaluating arithmetic expressions."""

        class TestGrammar(Grammar):
            @method
            def add(self, a, b):
                return a + b

        grammar = TestGrammar()
        # This will test that expressions are evaluated
        # For now, just verify parsing works
        result = grammar.parse("add(a=1 + 2, b=3)")
        assert len(result.calls) == 1

    def test_evaluate_comparison(self):
        """Test evaluating comparison expressions."""

        class TestGrammar(Grammar):
            def __init__(self):
                super().__init__()
                self.tracks = [{"name": "FX"}, {"name": "Drums"}]

            @method
            def filter(self, tracks, predicate):
                # predicate should be evaluated to True/False
                return [t for t in tracks if predicate]

        grammar = TestGrammar()
        # This will test expression evaluation in filter
        # For now, just verify parsing works
        result = grammar.parse('filter(tracks, track.name == "FX")')
        assert len(result.calls) == 1
