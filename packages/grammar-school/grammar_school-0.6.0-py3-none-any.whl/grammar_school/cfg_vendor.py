"""
CFG provider interface for Grammar School.

This module defines the interface that LLM providers must implement
to support Context-Free Grammar (CFG) constraints with Grammar School.
"""

from abc import ABC, abstractmethod
from typing import Any


class CFGProvider(ABC):
    """
    Abstract interface for LLM providers that support CFG constraints.

    This interface allows Grammar School to work with different LLM providers
    (OpenAI, Anthropic, Google, etc.) that implement CFG in their own way.

    Example:
        ```python
        class MyProvider(CFGProvider):
            def build_tool(self, tool_name, description, grammar, syntax):
                # Provider-specific tool building logic
                return {...}

            def get_text_format(self):
                # Provider-specific text format
                return {...}

            def generate(self, prompt, model, tools, text_format, **kwargs):
                # Provider-specific API call
                return response

            def extract_dsl_code(self, response):
                # Provider-specific response parsing
                return dsl_code
        ```
    """

    @abstractmethod
    def build_tool(
        self,
        tool_name: str,
        description: str,
        grammar: str,
        syntax: str = "lark",
    ) -> dict[str, Any]:
        """
        Build the CFG tool payload for this provider.

        Args:
            tool_name: Name of the tool
            description: Description of what the tool does
            grammar: Grammar definition string
            syntax: "lark" or "regex" (default: "lark")

        Returns:
            dict: Provider-specific tool structure
        """
        pass

    @abstractmethod
    def get_text_format(self) -> dict[str, Any]:
        """
        Get the text format configuration for this provider.

        Returns:
            dict: Provider-specific text format configuration
        """
        pass

    @abstractmethod
    def generate(
        self,
        prompt: str,
        model: str,
        tools: list[dict[str, Any]],
        text_format: dict[str, Any],
        client: Any | None = None,
        **kwargs: Any,
    ) -> Any:
        """
        Generate a response from the provider's API.

        Args:
            prompt: The prompt to send
            model: Model name to use
            tools: List of tool definitions
            text_format: Text format configuration
            client: Optional provider client instance
            **kwargs: Additional provider-specific arguments

        Returns:
            Provider-specific response object
        """
        pass

    @abstractmethod
    def extract_dsl_code(self, response: Any) -> str | None:
        """
        Extract DSL code from the provider's response.

        Args:
            response: Provider-specific response object

        Returns:
            str: The generated DSL code, or None if not found
        """
        pass


class OpenAICFGProvider(CFGProvider):
    """
    OpenAI implementation of the CFG provider interface.
    """

    def build_tool(
        self,
        tool_name: str,
        description: str,
        grammar: str,
        syntax: str = "lark",
    ) -> dict[str, Any]:
        """Build OpenAI CFG tool payload."""
        from grammar_school.openai_utils import OpenAICFG

        cfg = OpenAICFG(
            tool_name=tool_name,
            description=description,
            grammar=grammar,
            syntax=syntax,
        )
        return cfg.build_tool()

    def get_text_format(self) -> dict[str, Any]:
        """Get OpenAI text format configuration."""
        from grammar_school.openai_utils import OpenAICFG

        # Create a temporary instance just to get the text format
        cfg = OpenAICFG(tool_name="", description="", grammar="")
        return cfg.get_text_format()

    def generate(
        self,
        prompt: str,
        model: str,
        tools: list[dict[str, Any]],
        text_format: dict[str, Any],
        client: Any | None = None,
        **kwargs: Any,
    ) -> Any:
        """Generate response from OpenAI API."""
        try:
            from openai import OpenAI
        except ImportError as err:
            raise ImportError(
                "OpenAI SDK is required. Install it with: pip install openai"
            ) from err

        if client is None:
            client = OpenAI()

        return client.responses.create(  # type: ignore[call-overload]
            model=model,
            input=prompt,
            text=text_format,
            tools=tools,
            **kwargs,
        )

    def extract_dsl_code(self, response: Any) -> str | None:
        """Extract DSL code from OpenAI response."""
        for item in response.output:
            if hasattr(item, "type") and item.type == "custom_tool_call":
                return item.input  # type: ignore[no-any-return]
        return None


# Backward compatibility aliases
CFGVendor = CFGProvider
OpenAICFGVendor = OpenAICFGProvider
