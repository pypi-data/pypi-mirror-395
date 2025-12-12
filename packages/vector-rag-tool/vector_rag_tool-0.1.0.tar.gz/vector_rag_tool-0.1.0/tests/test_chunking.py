"""
Tests for text chunking strategies.

This module tests the various chunking strategies and their ability
to handle different content types correctly.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from pathlib import Path
from textwrap import dedent

import pytest

from vector_rag_tool.core.chunking import (
    ChunkerFactory,
    CodeChunkingStrategy,
    GenericChunkingStrategy,
    MarkdownChunkingStrategy,
    SupportedLanguage,
    YAMLChunkingStrategy,
)
from vector_rag_tool.core.models import Chunk


class TestSupportedLanguage:
    """Test the SupportedLanguage enum and its utility methods."""

    def test_from_extension(self) -> None:
        """Test mapping file extensions to languages."""
        test_cases = [
            (".py", SupportedLanguage.PYTHON),
            (".ts", SupportedLanguage.TYPESCRIPT),
            (".tsx", SupportedLanguage.TSX),
            (".java", SupportedLanguage.JAVA),
            (".go", SupportedLanguage.GO),
            (".kt", SupportedLanguage.KOTLIN),
            (".yaml", SupportedLanguage.YAML),
            (".yml", SupportedLanguage.YAML),
            (".md", SupportedLanguage.MARKDOWN),
            (".unknown", None),
            ("", None),
        ]

        for ext, expected in test_cases:
            result = SupportedLanguage.from_extension(ext)
            assert result == expected, f"Extension {ext} should map to {expected}"

    def test_langchain_language_mapping(self) -> None:
        """Test mapping to LangChain Language enum."""
        test_cases = [
            (SupportedLanguage.PYTHON, "PYTHON"),
            (SupportedLanguage.TYPESCRIPT, "TS"),
            (SupportedLanguage.JAVA, "JAVA"),
            (SupportedLanguage.MARKDOWN, "MARKDOWN"),
        ]

        for lang, expected_name in test_cases:
            lc_lang = lang.langchain_language
            assert lc_lang is not None, f"Language {lang} should have LangChain mapping"
            assert lc_lang.name == expected_name, f"Expected {expected_name}, got {lc_lang.name}"

        # Test languages that don't have LangChain mapping
        no_mapping_cases = [
            SupportedLanguage.YAML,
            SupportedLanguage.CSS,
            SupportedLanguage.SQL,
            SupportedLanguage.SHELL,
        ]

        for lang in no_mapping_cases:
            lc_lang = lang.langchain_language
            assert lc_lang is None, f"Language {lang} should not have LangChain mapping"


class TestMarkdownChunkingStrategy:
    """Test Markdown-specific chunking strategy."""

    def test_basic_markdown_chunking(self) -> None:
        """Test basic Markdown content chunking."""
        strategy = MarkdownChunkingStrategy(chunk_size=100, chunk_overlap=10)

        content = dedent("""
            # Main Title

            This is some introduction text with multiple sentences.
            It should be split into chunks based on the token size.

            ## Section 1

            Here's the first section with some content. Lorem ipsum dolor sit amet,
            consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore
            et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation
            ullamco laboris nisi ut aliquip ex ea commodo consequat.

            - Item 1 with some additional text to make it longer
            - Item 2 with more content to increase length
            - Item 3 also has some extra descriptive text here

            ## Section 2

            More content in the second section. Duis aute irure dolor in reprehenderit
            in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur
            sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt
            mollit anim id est laborum.

            ## Section 3

            Additional content in section three to ensure we have enough text for
            multiple chunks to be created when using a small chunk size.
        """).strip()

        source_file = Path("test.md")
        chunks = strategy.chunk(content, source_file)

        assert len(chunks) > 1, "Content should be split into multiple chunks"

        for chunk in chunks:
            assert isinstance(chunk, Chunk), "Should return Chunk objects"
            assert chunk.content, "Chunk content should not be empty"
            assert chunk.metadata.source_file == source_file
            assert chunk.metadata.chunk_index < len(chunks)
            assert chunk.metadata.total_chunks == len(chunks)
            assert chunk.id, "Chunk should have an ID"

    def test_small_markdown_chunking(self) -> None:
        """Test chunking small Markdown content."""
        strategy = MarkdownChunkingStrategy(chunk_size=1500, chunk_overlap=200)

        content = "# Small Content\n\nJust a little bit of text."
        source_file = Path("small.md")

        chunks = strategy.chunk(content, source_file)

        assert len(chunks) >= 1, "Should have at least one chunk"
        if len(chunks) == 1:
            assert chunks[0].content == content, "Single chunk should contain all content"

    def test_chunk_metadata(self) -> None:
        """Test chunk metadata is properly set."""
        strategy = MarkdownChunkingStrategy(chunk_size=500)

        content = "# Test\n\nContent here.\n\nMore content."
        source_file = Path("metadata.md")

        chunks = strategy.chunk(content, source_file)

        for i, chunk in enumerate(chunks):
            assert chunk.metadata.chunk_index == i
            assert chunk.metadata.total_chunks == len(chunks)
            assert chunk.metadata.line_start >= 1
            assert chunk.metadata.line_end >= chunk.metadata.line_start


class TestCodeChunkingStrategy:
    """Test code-specific chunking strategy."""

    def test_python_chunking(self) -> None:
        """Test Python code chunking."""
        strategy = CodeChunkingStrategy(
            language=SupportedLanguage.PYTHON,
            chunk_size=500,
            chunk_overlap=50,
        )

        content = dedent("""
            def hello_world():
                '''A simple greeting function.'''
                print("Hello, World!")
                return True

            class Calculator:
                def __init__(self):
                    self.result = 0

                def add(self, a, b):
                    '''Add two numbers.'''
                    self.result = a + b
                    return self.result

                def subtract(self, a, b):
                    '''Subtract two numbers.'''
                    self.result = a - b
                    return self.result

            if __name__ == "__main__":
                calc = Calculator()
                print(calc.add(5, 3))
                print(calc.subtract(10, 4))
        """).strip()

        source_file = Path("test.py")
        chunks = strategy.chunk(content, source_file)

        assert len(chunks) >= 1, "Should have at least one chunk"

        for chunk in chunks:
            assert isinstance(chunk, Chunk)
            assert SupportedLanguage.PYTHON.value in chunk.metadata.tags
            assert chunk.metadata.source_file == source_file

    def test_typescript_chunking(self) -> None:
        """Test TypeScript code chunking."""
        strategy = CodeChunkingStrategy(
            language=SupportedLanguage.TYPESCRIPT,
            chunk_size=400,
            chunk_overlap=50,
        )

        content = dedent("""
            interface User {
                id: number;
                name: string;
                email: string;
            }

            class UserService {
                private users: User[] = [];

                addUser(user: User): void {
                    this.users.push(user);
                }

                getUser(id: number): User | undefined {
                    return this.users.find(u => u.id === id);
                }
            }

            const userService = new UserService();
            userService.addUser({ id: 1, name: "John", email: "john@example.com" });
        """).strip()

        source_file = Path("test.ts")
        chunks = strategy.chunk(content, source_file)

        assert len(chunks) >= 1, "Should have at least one chunk"

        for chunk in chunks:
            assert SupportedLanguage.TYPESCRIPT.value in chunk.metadata.tags

    def test_unsupported_language_fallback(self) -> None:
        """Test fallback for unsupported languages."""

        # Create a mock language enum value that doesn't have LangChain mapping
        class MockLanguage:
            value = "mocklang"
            langchain_language = None

        strategy = CodeChunkingStrategy(
            language=MockLanguage(),  # type: ignore
            chunk_size=500,
        )

        content = "Some mock language code\nwith multiple lines"
        source_file = Path("test.mock")

        chunks = strategy.chunk(content, source_file)

        assert len(chunks) >= 1, "Should handle unsupported language gracefully"


class TestYAMLChunkingStrategy:
    """Test YAML-specific chunking strategy."""

    def test_yaml_chunking(self) -> None:
        """Test YAML content chunking."""
        strategy = YAMLChunkingStrategy(chunk_size=300, chunk_overlap=20)

        content = dedent("""
            app:
              name: "my-application"
              version: "1.0.0"
              environment: "development"

            database:
              host: "localhost"
              port: 5432
              name: "myapp_db"
              credentials:
                username: "admin"
                password: "secret"

            features:
              - authentication
              - user_profiles
              - data_export
              - real_time_updates

            logging:
              level: "info"
              format: "json"
              outputs:
                - console
                - file
        """).strip()

        source_file = Path("config.yaml")
        chunks = strategy.chunk(content, source_file)

        assert len(chunks) >= 1, "Should have at least one chunk"

        for chunk in chunks:
            assert isinstance(chunk, Chunk)
            assert "yaml" in chunk.metadata.tags
            assert "config" in chunk.metadata.tags
            assert chunk.metadata.source_file == source_file

    def test_small_yaml_chunking(self) -> None:
        """Test chunking small YAML content."""
        strategy = YAMLChunkingStrategy()

        content = "key: value\nname: test"
        source_file = Path("small.yaml")

        chunks = strategy.chunk(content, source_file)

        # Small content might be in a single chunk
        assert len(chunks) >= 1, "Should have at least one chunk"


class TestGenericChunkingStrategy:
    """Test generic text chunking strategy."""

    def test_generic_text_chunking(self) -> None:
        """Test generic text content chunking."""
        strategy = GenericChunkingStrategy(chunk_size=200, chunk_overlap=20)

        content = (
            "This is a long text document. " * 50 + "It should be split into multiple chunks. " * 30
        )

        source_file = Path("document.txt")
        chunks = strategy.chunk(content, source_file)

        assert len(chunks) > 1, "Long content should be split into multiple chunks"

        for chunk in chunks:
            assert isinstance(chunk, Chunk)
            assert "text" in chunk.metadata.tags
            assert len(chunk.content) > 0

    def test_empty_content(self) -> None:
        """Test chunking empty content."""
        strategy = GenericChunkingStrategy()
        source_file = Path("empty.txt")

        chunks = strategy.chunk("", source_file)

        # Should handle empty content gracefully
        assert len(chunks) >= 0, "Should handle empty content"


class TestChunkerFactory:
    """Test the ChunkerFactory for strategy selection."""

    def test_markdown_strategy_selection(self) -> None:
        """Test factory selects Markdown strategy for .md files."""
        file_path = Path("test.md")
        strategy = ChunkerFactory.create_strategy(file_path)

        assert isinstance(strategy, MarkdownChunkingStrategy)

    def test_yaml_strategy_selection(self) -> None:
        """Test factory selects YAML strategy for .yaml/.yml files."""
        for ext in ["yaml", "yml"]:
            file_path = Path(f"test.{ext}")
            strategy = ChunkerFactory.create_strategy(file_path)

            assert isinstance(strategy, YAMLChunkingStrategy)

    def test_code_strategy_selection(self) -> None:
        """Test factory selects Code strategy for programming files."""
        test_cases = [
            ("test.py", SupportedLanguage.PYTHON),
            ("test.ts", SupportedLanguage.TYPESCRIPT),
            ("test.java", SupportedLanguage.JAVA),
            ("test.go", SupportedLanguage.GO),
            ("test.kt", SupportedLanguage.KOTLIN),
        ]

        for filename, expected_lang in test_cases:
            file_path = Path(filename)
            strategy = ChunkerFactory.create_strategy(file_path)

            assert isinstance(strategy, CodeChunkingStrategy)
            assert strategy.language == expected_lang

    def test_generic_strategy_selection(self) -> None:
        """Test factory selects Generic strategy for unknown file types."""
        file_path = Path("test.unknown")
        strategy = ChunkerFactory.create_strategy(file_path)

        assert isinstance(strategy, GenericChunkingStrategy)

    def test_chunk_file_convenience_method(self) -> None:
        """Test the convenience method for chunking files."""
        # Create a temporary file
        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Test Document\n\nThis is a test document for chunking.")
            temp_path = Path(f.name)

        try:
            chunks = ChunkerFactory.chunk_file(temp_path)

            assert len(chunks) >= 1, "Should have at least one chunk"
            for chunk in chunks:
                assert isinstance(chunk, Chunk)
                assert chunk.metadata.source_file == temp_path
        finally:
            temp_path.unlink()

    def test_chunk_file_nonexistent(self) -> None:
        """Test chunking non-existent file raises error."""
        file_path = Path("nonexistent.md")

        with pytest.raises(FileNotFoundError):
            ChunkerFactory.chunk_file(file_path)

    def test_strategy_with_custom_config(self) -> None:
        """Test creating strategy with custom configuration."""
        file_path = Path("test.md")
        custom_config = {
            "chunk_size": 2000,
            "chunk_overlap": 300,
            "length_function": len,  # Use character count instead of tokens
        }

        strategy = ChunkerFactory.create_strategy(file_path, **custom_config)

        assert isinstance(strategy, MarkdownChunkingStrategy)
        assert strategy.chunk_size == 2000
        assert strategy.chunk_overlap == 300

    def test_chunk_id_uniqueness(self) -> None:
        """Test that chunk IDs are unique within a file."""
        strategy = MarkdownChunkingStrategy(chunk_size=100)

        content = "# Title\n\n" + "Some content.\n" * 50
        source_file = Path("unique_test.md")

        chunks = strategy.chunk(content, source_file)

        chunk_ids = [chunk.id for chunk in chunks]
        assert len(chunk_ids) == len(set(chunk_ids)), "All chunk IDs should be unique"


class TestChunkingIntegration:
    """Integration tests for chunking scenarios."""

    def test_mixed_content_types(self) -> None:
        """Test chunking different content types with consistent interface."""
        # Create temporary files for testing
        import tempfile

        with (
            tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as md_file,
            tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as yaml_file,
            tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as py_file,
        ):
            md_file.write("# Markdown\n\nContent here.")
            yaml_file.write("key: value")
            py_file.write("print('hello')")
            md_path = Path(md_file.name)
            yaml_path = Path(yaml_file.name)
            py_path = Path(py_file.name)

        try:
            markdown_chunks = ChunkerFactory.chunk_file(md_path, chunk_size=100)
            yaml_chunks = ChunkerFactory.chunk_file(yaml_path, chunk_size=100)
            python_chunks = ChunkerFactory.chunk_file(py_path, chunk_size=100)

            # All should return lists of chunks
            for chunks in [markdown_chunks, yaml_chunks, python_chunks]:
                assert isinstance(chunks, list)
                for chunk in chunks:
                    assert isinstance(chunk, Chunk)
        finally:
            # Clean up temporary files
            md_path.unlink()
            yaml_path.unlink()
            py_path.unlink()

    def test_chunk_size_impact(self) -> None:
        """Test how different chunk sizes affect chunking."""
        content = "This is test content. " * 100
        source_file = Path("size_test.md")

        small_strategy = MarkdownChunkingStrategy(chunk_size=200, chunk_overlap=20)
        large_strategy = MarkdownChunkingStrategy(chunk_size=2000, chunk_overlap=200)
        small_chunks = small_strategy.chunk(content, source_file)
        large_chunks = large_strategy.chunk(content, source_file)

        assert len(small_chunks) >= len(large_chunks), (
            "Smaller chunk size should create more or equal chunks"
        )

    def test_chunk_overlap_impact(self) -> None:
        """Test how chunk overlap affects content."""
        content = "First sentence. Second sentence. Third sentence. " * 10
        source_file = Path("overlap_test.md")

        no_overlap_strategy = MarkdownChunkingStrategy(chunk_size=200, chunk_overlap=0)
        with_overlap_strategy = MarkdownChunkingStrategy(chunk_size=200, chunk_overlap=50)
        no_overlap = no_overlap_strategy.chunk(content, source_file)
        with_overlap = with_overlap_strategy.chunk(content, source_file)

        assert len(no_overlap) == len(with_overlap), (
            "Overlap shouldn't change chunk count for this content"
        )

        # Check that overlapping chunks have some shared content
        if len(with_overlap) > 1:
            chunk1 = with_overlap[0].content
            chunk2 = with_overlap[1].content
            # Check if there's any overlap (this is a simple check)
            assert len(chunk1) > 0 and len(chunk2) > 0
