"""Tests for AST types."""

from grammar_school.ast import Arg, Call, CallChain, Value


class TestValue:
    """Test Value AST node."""

    def test_value_number(self):
        """Test number value."""
        value = Value(kind="number", value=42)
        assert value.kind == "number"
        assert value.value == 42

    def test_value_string(self):
        """Test string value."""
        value = Value(kind="string", value="hello")
        assert value.kind == "string"
        assert value.value == "hello"

    def test_value_identifier(self):
        """Test identifier value."""
        value = Value(kind="identifier", value="my_var")
        assert value.kind == "identifier"
        assert value.value == "my_var"


class TestArg:
    """Test Arg AST node."""

    def test_arg_with_name(self):
        """Test arg with name."""
        value = Value(kind="string", value="test")
        arg = Arg(name="name", value=value)
        assert arg.name == "name"
        assert arg.value == value


class TestCall:
    """Test Call AST node."""

    def test_call_with_args(self):
        """Test call with arguments."""
        value1 = Value(kind="string", value="test")
        value2 = Value(kind="number", value=42)
        call = Call(name="greet", args={"name": value1, "count": value2})
        assert call.name == "greet"
        assert len(call.args) == 2
        assert call.args["name"] == value1
        assert call.args["count"] == value2

    def test_call_without_args(self):
        """Test call without arguments."""
        call = Call(name="hello", args={})
        assert call.name == "hello"
        assert len(call.args) == 0


class TestCallChain:
    """Test CallChain AST node."""

    def test_call_chain_single(self):
        """Test call chain with single call."""
        call = Call(name="greet", args={})
        chain = CallChain(calls=[call])
        assert len(chain.calls) == 1
        assert chain.calls[0] == call

    def test_call_chain_multiple(self):
        """Test call chain with multiple calls."""
        call1 = Call(name="track", args={})
        call2 = Call(name="add_clip", args={})
        chain = CallChain(calls=[call1, call2])
        assert len(chain.calls) == 2
        assert chain.calls[0] == call1
        assert chain.calls[1] == call2
