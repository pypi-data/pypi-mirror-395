"""Tests for OpenAI CFG utility functions."""

from grammar_school.backend_lark import LarkBackend
from grammar_school.openai_utils import OpenAICFG


class TestOpenAICFG:
    """Test OpenAICFG class."""

    def test_cfg_creation(self):
        """Test creating an OpenAICFG instance."""
        cfg = OpenAICFG(
            tool_name="test_tool",
            description="Test tool description",
            grammar="start: test",
            syntax="lark",
        )

        assert cfg.tool_name == "test_tool"
        assert cfg.description == "Test tool description"
        assert cfg.grammar == "start: test"
        assert cfg.syntax == "lark"

    def test_cfg_default_syntax(self):
        """Test OpenAICFG defaults to 'lark' syntax."""
        cfg = OpenAICFG(
            tool_name="test_tool",
            description="Test tool description",
            grammar="start: test",
        )

        assert cfg.syntax == "lark"

    def test_build_tool_structure(self):
        """Test that the returned dictionary has the correct structure."""
        cfg = OpenAICFG(
            tool_name="magda_dsl",
            description="Generates MAGDA DSL code",
            grammar="start: track",
            syntax="lark",
        )

        tool = cfg.build_tool()

        assert tool["type"] == "custom"
        assert tool["name"] == "magda_dsl"
        assert tool["description"] == "Generates MAGDA DSL code"
        assert "format" in tool
        assert tool["format"]["type"] == "grammar"
        assert tool["format"]["syntax"] == "lark"
        assert "definition" in tool["format"]

    def test_grammar_cleaning(self):
        """Test that grammar is cleaned using clean_grammar_for_cfg."""
        # Grammar with Lark directives that should be removed
        grammar_with_directives = """%import common
start: track
track: "track"
"""
        cfg = OpenAICFG(
            tool_name="test_tool",
            description="Test tool",
            grammar=grammar_with_directives,
            syntax="lark",
        )

        tool = cfg.build_tool()
        cleaned_grammar = tool["format"]["definition"]

        # Verify %import directive was removed
        assert "%import" not in cleaned_grammar
        # Verify the actual grammar content is still there
        assert "start: track" in cleaned_grammar
        assert 'track: "track"' in cleaned_grammar

        # Verify it matches what clean_grammar_for_cfg would produce
        expected_cleaned = LarkBackend.clean_grammar_for_cfg(grammar_with_directives)
        assert cleaned_grammar == expected_cleaned

    def test_default_syntax_handling(self):
        """Test that syntax defaults to 'lark' when not specified."""
        cfg = OpenAICFG(
            tool_name="test_tool",
            description="Test tool",
            grammar="start: test",
            syntax="",  # Empty string should default to "lark"
        )

        tool = cfg.build_tool()
        assert tool["format"]["syntax"] == "lark"

    def test_regex_syntax(self):
        """Test that regex syntax is preserved."""
        cfg = OpenAICFG(
            tool_name="test_tool",
            description="Test tool",
            grammar="^\\d+$",
            syntax="regex",
        )

        tool = cfg.build_tool()
        assert tool["format"]["syntax"] == "regex"

    def test_all_config_fields_used(self):
        """Test that all config fields are properly used in the tool."""
        cfg = OpenAICFG(
            tool_name="custom_tool",
            description="Custom description with special chars: !@#$",
            grammar='start: custom_rule\ncustom_rule: "value"',
            syntax="lark",
        )

        tool = cfg.build_tool()

        assert tool["name"] == "custom_tool"
        assert tool["description"] == "Custom description with special chars: !@#$"
        assert tool["format"]["syntax"] == "lark"
        assert "custom_rule" in tool["format"]["definition"]

    def test_text_format_structure(self):
        """Test that the returned dictionary has the correct structure."""
        cfg = OpenAICFG(tool_name="test", description="test", grammar="start: test")
        text_format = cfg.get_text_format()

        assert isinstance(text_format, dict)
        assert "format" in text_format
        assert isinstance(text_format["format"], dict)
        assert text_format["format"]["type"] == "text"

    def test_text_format_consistency(self):
        """Test that the function returns the same structure on multiple calls."""
        cfg = OpenAICFG(tool_name="test", description="test", grammar="start: test")
        format1 = cfg.get_text_format()
        format2 = cfg.get_text_format()

        assert format1 == format2
        assert format1["format"]["type"] == "text"
        assert format2["format"]["type"] == "text"
