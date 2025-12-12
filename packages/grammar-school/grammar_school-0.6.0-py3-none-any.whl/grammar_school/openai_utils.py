"""
Utilities for integrating Grammar School with OpenAI's CFG (Context-Free Grammar) tools.

This module provides helper functions and a convenient class to build OpenAI CFG tool payloads
that use Grammar School grammars as constraints.
"""

from dataclasses import dataclass
from typing import Any

from grammar_school.backend_lark import DEFAULT_GRAMMAR, LarkBackend


@dataclass
class _CFGConfig:
    """Internal configuration for building an OpenAI CFG tool."""

    tool_name: str
    description: str
    grammar: str
    syntax: str = "lark"


def _build_openai_cfg_tool(config: _CFGConfig) -> dict[str, Any]:
    """
    Build an OpenAI CFG tool payload from a CFGConfig.

    This function:
    - Cleans the grammar using clean_grammar_for_cfg()
    - Returns the properly formatted OpenAI tool structure
    - Ensures the syntax defaults to "lark" if not specified

    Args:
        config: CFGConfig containing tool name, description, grammar, and syntax

    Returns:
        dict: OpenAI tool structure ready to be added to the tools array

    Example:
        ```python
        from grammar_school.openai_utils import CFGConfig, build_openai_cfg_tool

        tool = build_openai_cfg_tool(CFGConfig(
            tool_name="magda_dsl",
            description="Generates MAGDA DSL code for REAPER automation",
            grammar=grammar_string,
            syntax="lark",
        ))
        # Add tool to OpenAI request: tools = [tool]
        ```
    """
    # Clean the grammar for CFG
    cleaned_grammar = LarkBackend.clean_grammar_for_cfg(config.grammar)

    # Default to "lark" if syntax is not specified
    syntax = config.syntax or "lark"

    # Build the OpenAI CFG tool structure
    return {
        "type": "custom",
        "name": config.tool_name,
        "description": config.description,
        "format": {
            "type": "grammar",
            "syntax": syntax,
            "definition": cleaned_grammar,
        },
    }


def _get_openai_text_format_for_cfg() -> dict[str, Any]:
    """
    Get the text format configuration that should be used when making OpenAI requests with CFG tools.

    When using CFG, the text format must be set to "text" (not JSON schema) because
    the output is DSL code, not JSON.

    Returns:
        dict: Text format config: {"format": {"type": "text"}}

    Example:
        ```python
        from grammar_school.openai_utils import get_openai_text_format_for_cfg

        params["text"] = get_openai_text_format_for_cfg()
        ```
    """
    return {
        "format": {
            "type": "text",
        },
    }


class OpenAICFG:
    """
    Convenient class for building OpenAI CFG tool configurations.

    This class encapsulates all the functionality needed to create OpenAI CFG tools
    from Grammar School grammars, eliminating the need to import and compose
    multiple utilities.

    Example:
        ```python
        from grammar_school.openai_utils import OpenAICFG

        # Use default Grammar School grammar
        cfg = OpenAICFG(
            tool_name="task_dsl",
            description="Executes task management operations using Grammar School DSL.",
        )

        # Build the tool and get text format in one go
        tool = cfg.build_tool()
        text_format = cfg.get_text_format()

        # Or use custom grammar
        cfg = OpenAICFG(
            tool_name="custom_dsl",
            description="Custom DSL tool",
            grammar="start: custom_rule\ncustom_rule: \"value\"",
        )
        ```
    """

    def __init__(
        self,
        tool_name: str,
        description: str,
        grammar: str | None = None,
        syntax: str = "lark",
    ):
        """
        Initialize OpenAI CFG configuration.

        Args:
            tool_name: Name of the tool that will receive the DSL output
            description: Description of what the tool does
            grammar: Lark or regex grammar definition. If None, uses Grammar School's DEFAULT_GRAMMAR
            syntax: "lark" or "regex" (default: "lark")
        """
        self.tool_name = tool_name
        self.description = description
        self.grammar = grammar if grammar is not None else DEFAULT_GRAMMAR
        self.syntax = syntax

    def build_tool(self) -> dict[str, Any]:
        """
        Build the OpenAI CFG tool payload.

        Returns:
            dict: OpenAI tool structure ready to be added to the tools array

        Example:
            ```python
            cfg = OpenAICFG(tool_name="my_tool", description="My tool")
            tool = cfg.build_tool()
            # Use in OpenAI request: tools = [tool]
            ```
        """
        return _build_openai_cfg_tool(
            _CFGConfig(
                tool_name=self.tool_name,
                description=self.description,
                grammar=self.grammar,
                syntax=self.syntax,
            )
        )

    def get_text_format(self) -> dict[str, Any]:
        """
        Get the text format configuration for OpenAI requests with CFG.

        Returns:
            dict: Text format config: {"format": {"type": "text"}}

        Example:
            ```python
            cfg = OpenAICFG(tool_name="my_tool", description="My tool")
            text_format = cfg.get_text_format()
            # Use in OpenAI request: text=text_format
            ```
        """
        return _get_openai_text_format_for_cfg()

    def build_request_config(self) -> dict[str, Any]:
        """
        Build a complete request configuration dict with both tool and text format.

        This is a convenience method that returns both the tool and text format
        in a single dict structure that can be easily merged into OpenAI request params.

        Returns:
            dict: Dict with "tool" and "text" keys ready for OpenAI request

        Example:
            ```python
            cfg = OpenAICFG(tool_name="my_tool", description="My tool")
            config = cfg.build_request_config()
            # Use in OpenAI request:
            # tools = [config["tool"]]
            # text = config["text"]
            ```
        """
        return {
            "tool": self.build_tool(),
            "text": self.get_text_format(),
        }
