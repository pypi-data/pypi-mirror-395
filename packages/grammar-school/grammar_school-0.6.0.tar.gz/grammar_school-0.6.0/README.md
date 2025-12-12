# Grammar School - Python Implementation

A lightweight framework for building tiny LLM-friendly DSLs in Python.

## Installation

```bash
pip install grammar-school
```

For development:

```bash
pip install -e ".[dev]"
```

## Quick Start

```python
from grammar_school import Grammar, method

class MyGrammar(Grammar):
    @method
    def greet(self, name):
        # @method contains the actual implementation
        # You can do anything here - side effects, state changes, etc.
        print(f"Hello, {name}!")

# No runtime needed - methods execute directly!
grammar = MyGrammar()
grammar.execute('greet(name="World")')

# Methods can maintain state using self
class MyGrammarWithState(Grammar):
    def __init__(self):
        super().__init__()
        self.greetings = []  # State managed in the grammar instance

    @method
    def greet(self, name):
        self.greetings.append(name)
        print(f"Hello, {name}!")

grammar = MyGrammarWithState()
grammar.execute('greet(name="World")')
print(grammar.greetings)  # ['World']
```

## Understanding the Architecture

Grammar School provides a **unified interface**:

1. **Grammar + @method**: Methods contain their implementation directly
2. **Framework handles the rest**: Parsing, interpretation, and execution happen automatically

**Benefits:**
- Simple and intuitive - just write methods with your logic
- No need to separate concerns - methods can do anything
- State management via `self` attributes
- The Grammar/Runtime split is handled internally but hidden from you

## Streaming Execution

For large DSL programs or real-time processing, you can stream method executions:

```python
grammar = MyGrammar()

# Stream method executions one at a time (memory efficient)
for _ in grammar.stream('greet(name="A").greet(name="B").greet(name="C")'):
    # Methods execute as they're called
    pass
```

This is useful for:
- **Large programs**: Don't load all method calls into memory at once
- **Real-time processing**: Start executing methods before parsing completes
- **Memory efficiency**: Process methods incrementally

## Functional Programming Support

Grammar School allows you to implement functional programming patterns by defining your own methods:

```python
from grammar_school import Grammar, method

class MyGrammar(Grammar):
    @method
    def square(self, x):
        return x * x

    @method
    def is_even(self, x):
        return x % 2 == 0

    @method
    def map(self, func, data):
        # Implement your own map logic
        return [func(x) for x in data]

    @method
    def filter(self, predicate, data):
        # Implement your own filter logic
        return [x for x in data if predicate(x)]

grammar = MyGrammar()
# Use functional operations - you provide the implementation
grammar.execute('map(@square, data)')
grammar.execute('filter(@is_even, data)')
grammar.execute('map(@square, data).filter(@is_even, data)')
```

**Available functional operations:**
- `map(@function, data)` - Map a function over data
- `filter(@predicate, data)` - Filter data using a predicate
- `reduce(@function, data, initial)` - Reduce data using a function
- `compose(@f, @g, @h)` - Compose multiple functions
- `pipe(data, @f, @g, @h)` - Pipe data through functions

**Function references:** Use `@function_name` syntax to pass functions as arguments.

## Examples

See the `examples/` directory for complete DSL implementations.

## API Reference

### Core Types

- `Value`: AST value node (number, string, identifier, bool)
- `Arg`: Named argument
- `Call`: Function call with arguments
- `CallChain`: Chain of calls (method chaining)
### Decorators

- `@method`: Mark a method as a DSL handler (contains implementation)
- `@rule`: Define grammar rules (for custom grammars)

### Classes

- `Grammar`: Main grammar class that orchestrates parsing and interpretation
- `Interpreter`: Interprets CallChain AST into Actions
- `LarkBackend`: Lark-based parser backend
