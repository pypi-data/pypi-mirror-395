"""Config-based grammar loader for Grammar School."""

from pathlib import Path
from typing import Any

from grammar_school.grammar_builder import GrammarBuilder


def load_grammar_from_config(config: dict[str, Any]) -> str:
    """
    Load grammar from a config dictionary.

    Config format:
        ```yaml
        start: start
        rules:
          - name: start
            definition: call_chain
            description: Entry point
          - name: call_chain
            definition: call (DOT call)*
            description: Chain of calls
        terminals:
          - name: DOT
            pattern: "."
            description: Dot separator
        directives:
          - "%import common.WS"
          - "%ignore WS"
        ```

    Args:
        config: Dictionary containing grammar configuration

    Returns:
        Lark grammar string
    """
    builder = GrammarBuilder()

    # Set start rule
    if "start" in config:
        builder.start(config["start"])

    # Add rules
    if "rules" in config:
        for rule_config in config["rules"]:
            builder.rule(
                name=rule_config["name"],
                definition=rule_config["definition"],
                description=rule_config.get("description"),
            )

    # Add terminals
    if "terminals" in config:
        for terminal_config in config["terminals"]:
            builder.terminal(
                name=terminal_config["name"],
                pattern=terminal_config["pattern"],
                description=terminal_config.get("description"),
            )

    # Add directives
    if "directives" in config:
        for directive in config["directives"]:
            builder.directive(directive)

    return builder.build()


def load_grammar_from_yaml(path: str | Path) -> str:
    """
    Load grammar from a YAML file.

    Args:
        path: Path to YAML file

    Returns:
        Lark grammar string

    Raises:
        ImportError: If PyYAML is not installed
        FileNotFoundError: If file doesn't exist
    """
    try:
        import yaml  # type: ignore[import-untyped]
    except ImportError as err:
        raise ImportError("PyYAML is required. Install with: pip install pyyaml") from err

    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Grammar config file not found: {path}")

    with path.open() as f:
        config = yaml.safe_load(f)

    return load_grammar_from_config(config)


def load_grammar_from_toml(path: str | Path) -> str:
    """
    Load grammar from a TOML file.

    Args:
        path: Path to TOML file

    Returns:
        Lark grammar string

    Raises:
        ImportError: If tomli/tomllib is not installed
        FileNotFoundError: If file doesn't exist
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Grammar config file not found: {path}")

    # Try tomllib (Python 3.11+)
    try:
        import tomllib

        with path.open("rb") as f:
            config = tomllib.load(f)
    except ImportError:
        # Fall back to tomli
        try:
            import tomli

            with path.open("rb") as f:
                config = tomli.load(f)
        except ImportError as err:
            raise ImportError("tomli is required. Install with: pip install tomli") from err

    return load_grammar_from_config(config)
