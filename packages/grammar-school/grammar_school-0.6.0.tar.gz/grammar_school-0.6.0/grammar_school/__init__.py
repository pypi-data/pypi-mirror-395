"""Grammar School - A lightweight framework for building tiny LLM-friendly DSLs."""

from grammar_school.ast import Arg, Call, CallChain, Expression, PropertyAccess, Value
from grammar_school.backend_lark import DEFAULT_GRAMMAR, LarkBackend
from grammar_school.cfg_vendor import (
    CFGProvider,
    CFGVendor,  # Backward compatibility
    OpenAICFGProvider,
    OpenAICFGVendor,  # Backward compatibility
)
from grammar_school.grammar import Grammar, method, rule
from grammar_school.grammar_builder import GrammarBuilder
from grammar_school.grammar_config import (
    load_grammar_from_config,
    load_grammar_from_toml,
    load_grammar_from_yaml,
)
from grammar_school.interpreter import Interpreter
from grammar_school.openai_utils import OpenAICFG
from grammar_school.runtime import Action, Runtime
from grammar_school.version import __version__

__all__ = [
    "Action",
    "Arg",
    "Call",
    "CallChain",
    "Expression",
    "CFGProvider",
    "CFGVendor",  # Backward compatibility
    "DEFAULT_GRAMMAR",
    "Grammar",
    "GrammarBuilder",
    "Interpreter",
    "OpenAICFGProvider",
    "OpenAICFGVendor",  # Backward compatibility
    "LarkBackend",
    "OpenAICFG",
    "PropertyAccess",
    "Runtime",
    "Value",
    "__version__",
    "load_grammar_from_config",
    "load_grammar_from_toml",
    "load_grammar_from_yaml",
    "method",
    "rule",
]
