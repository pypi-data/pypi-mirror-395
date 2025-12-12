"""Tests for Grammar class."""

from grammar_school import Grammar, method

# For backward compatibility in tests - will be updated later
verb = method  # type: ignore[misc]


class TestGrammar:
    """Test Grammar class."""

    def test_grammar_with_default_runtime(self):
        """Test grammar with default runtime."""

        class TestGrammar(Grammar):
            def __init__(self):
                super().__init__()
                self.greeted = []

            @verb
            def greet(self, name):
                self.greeted.append(name)

        grammar = TestGrammar()
        grammar.execute('greet(name="World")')
        assert "World" in grammar.greeted

    def test_grammar_with_custom_runtime(self):
        """Test grammar with custom runtime - now methods execute directly."""

        class TestGrammar(Grammar):
            def __init__(self):
                super().__init__()
                self.greeted = []

            @verb
            def greet(self, name):
                self.greeted.append(name)

        grammar = TestGrammar()
        grammar.execute('greet(name="World")')

        assert len(grammar.greeted) == 1
        assert grammar.greeted[0] == "World"

    def test_grammar_parse(self):
        """Test grammar parse method."""

        class TestGrammar(Grammar):
            def __init__(self):
                super().__init__()
                self.greeted = []

            @verb
            def greet(self, name):
                self.greeted.append(name)

        grammar = TestGrammar()
        call_chain = grammar.parse('greet(name="World")')

        assert call_chain is not None
        assert len(call_chain.calls) == 1
        assert call_chain.calls[0].name == "greet"

    def test_grammar_compile(self):
        """Test grammar compile method - now just execute directly."""

        class TestGrammar(Grammar):
            def __init__(self):
                super().__init__()
                self.greeted = []

            @verb
            def greet(self, name):
                self.greeted.append(name)

        grammar = TestGrammar()
        grammar.execute('greet(name="World")')

        assert len(grammar.greeted) == 1
        assert grammar.greeted[0] == "World"

    def test_grammar_stream(self):
        """Test grammar stream method."""

        class TestGrammar(Grammar):
            def __init__(self):
                super().__init__()
                self.tracks = []

            @verb
            def track(self, name):
                self.tracks.append(name)

        grammar = TestGrammar()
        # Stream yields None, but methods execute
        results = list(grammar.stream('track(name="A").track(name="B")'))

        assert len(results) == 2  # Two None values
        assert len(grammar.tracks) == 2
        assert grammar.tracks[0] == "A"
        assert grammar.tracks[1] == "B"

    def test_grammar_execute_with_string(self):
        """Test grammar execute with string code."""

        class TestGrammar(Grammar):
            def __init__(self):
                super().__init__()
                self.greeted = []

            @verb
            def greet(self, name):
                self.greeted.append(name)

        grammar = TestGrammar()
        grammar.execute('greet(name="World")')

        assert len(grammar.greeted) == 1
        assert grammar.greeted[0] == "World"

    def test_grammar_execute_with_action_list(self):
        """Test grammar execute - now methods execute directly, no action list."""

        class TestGrammar(Grammar):
            def __init__(self):
                super().__init__()
                self.greeted = []

            @verb
            def greet(self, name):
                self.greeted.append(name)

        grammar = TestGrammar()
        grammar.execute('greet(name="World").greet(name="Universe")')

        assert len(grammar.greeted) == 2
        assert grammar.greeted[0] == "World"
        assert grammar.greeted[1] == "Universe"

    def test_grammar_multiple_verbs(self):
        """Test grammar with multiple verbs."""

        class TestGrammar(Grammar):
            def __init__(self):
                super().__init__()
                self.messages = []

            @verb
            def greet(self, name):
                self.messages.append(f"greet:{name}")

            @verb
            def farewell(self, name):
                self.messages.append(f"farewell:{name}")

        grammar = TestGrammar()
        grammar.execute('greet(name="Hello").farewell(name="Goodbye")')

        assert len(grammar.messages) == 2
        assert grammar.messages[0] == "greet:Hello"
        assert grammar.messages[1] == "farewell:Goodbye"

    def test_grammar_chained_calls(self):
        """Test grammar with chained method calls."""

        class TestGrammar(Grammar):
            def __init__(self):
                super().__init__()
                self.tracks = []
                self.clips = []

            @verb
            def track(self, name):
                self.tracks.append(name)

            @verb
            def add_clip(self, start, end):
                self.clips.append({"start": start, "end": end})

        grammar = TestGrammar()
        grammar.execute('track(name="A").add_clip(start=0, end=10)')

        assert len(grammar.tracks) == 1
        assert grammar.tracks[0] == "A"
        assert len(grammar.clips) == 1
        assert grammar.clips[0]["start"] == 0
        assert grammar.clips[0]["end"] == 10

    def test_grammar_multiline_statements(self):
        """Test grammar with multiline statements."""

        class TestGrammar(Grammar):
            def __init__(self):
                super().__init__()
                self.tracks = []
                self.clips = []

            @verb
            def track(self, name):
                self.tracks.append(name)

            @verb
            def add_clip(self, start, length):
                self.clips.append({"start": start, "length": length})

        grammar = TestGrammar()
        # Multiline DSL code
        code = """track(name="Drums")
add_clip(start=0, length=8)
add_clip(start=8, length=8)"""
        grammar.execute(code)

        assert len(grammar.tracks) == 1
        assert grammar.tracks[0] == "Drums"
        assert len(grammar.clips) == 2
        assert grammar.clips[0]["start"] == 0
        assert grammar.clips[0]["length"] == 8
        assert grammar.clips[1]["start"] == 8
        assert grammar.clips[1]["length"] == 8

    def test_grammar_multiline_backward_compatibility(self):
        """Test that single-line call chains still work (backward compatibility)."""

        class TestGrammar(Grammar):
            def __init__(self):
                super().__init__()
                self.messages = []

            @verb
            def greet(self, name):
                self.messages.append(f"greet:{name}")

        grammar = TestGrammar()
        # Single line should still work
        grammar.execute('greet(name="World")')

        assert len(grammar.messages) == 1
        assert grammar.messages[0] == "greet:World"
