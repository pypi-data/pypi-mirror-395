"""
Text chunking strategies for different content types.

This module provides flexible chunking strategies using LangChain text splitters
to optimally segment content for embedding and retrieval operations.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import os
from abc import ABC, abstractmethod
from enum import Enum
from hashlib import sha256
from pathlib import Path
from typing import Any

# Disable LangChain/LangSmith telemetry before importing
os.environ.setdefault("LANGCHAIN_TRACING_V2", "false")
os.environ.setdefault("LANGSMITH_TRACING", "false")

from langchain_text_splitters import (
    Language,
    MarkdownTextSplitter,
    RecursiveCharacterTextSplitter,
)

from vector_rag_tool.core.models import Chunk, ChunkMetadata


class SupportedLanguage(str, Enum):
    """Supported programming languages for code chunking."""

    PYTHON = "python"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    GO = "go"
    KOTLIN = "kotlin"
    JAVASCRIPT = "javascript"
    TSX = "tsx"
    JSX = "jsx"
    HTML = "html"
    CSS = "css"
    SQL = "sql"
    RUST = "rust"
    CPP = "cpp"
    CSHARP = "csharp"
    PHP = "php"
    RUBY = "ruby"
    SCALA = "scala"
    SWIFT = "swift"
    SHELL = "shell"
    JSON = "json"
    XML = "xml"
    YAML = "yaml"
    TOML = "toml"
    MARKDOWN = "markdown"

    @classmethod
    def from_extension(cls, extension: str) -> "SupportedLanguage | None":
        """Map file extension to supported language."""
        mapping = {
            ".py": cls.PYTHON,
            ".ts": cls.TYPESCRIPT,
            ".tsx": cls.TSX,
            ".js": cls.JAVASCRIPT,
            ".jsx": cls.JSX,
            ".java": cls.JAVA,
            ".go": cls.GO,
            ".kt": cls.KOTLIN,
            ".html": cls.HTML,
            ".htm": cls.HTML,
            ".css": cls.CSS,
            ".sql": cls.SQL,
            ".rs": cls.RUST,
            ".cpp": cls.CPP,
            ".cc": cls.CPP,
            ".cxx": cls.CPP,
            ".cs": cls.CSHARP,
            ".php": cls.PHP,
            ".rb": cls.RUBY,
            ".scala": cls.SCALA,
            ".swift": cls.SWIFT,
            ".sh": cls.SHELL,
            ".bash": cls.SHELL,
            ".zsh": cls.SHELL,
            ".fish": cls.SHELL,
            ".json": cls.JSON,
            ".jsonl": cls.JSON,
            ".xml": cls.XML,
            ".yaml": cls.YAML,
            ".yml": cls.YAML,
            ".toml": cls.TOML,
            ".md": cls.MARKDOWN,
            ".markdown": cls.MARKDOWN,
        }
        return mapping.get(extension.lower())

    @property
    def langchain_language(self) -> Language | None:
        """Map to LangChain Language enum."""
        mapping = {
            SupportedLanguage.PYTHON: Language.PYTHON,
            SupportedLanguage.TYPESCRIPT: Language.TS,
            # TSX uses TypeScript splitter
            SupportedLanguage.TSX: Language.TS,
            SupportedLanguage.JAVASCRIPT: Language.JS,
            # JSX uses JavaScript splitter
            SupportedLanguage.JSX: Language.JS,
            SupportedLanguage.JAVA: Language.JAVA,
            SupportedLanguage.GO: Language.GO,
            SupportedLanguage.KOTLIN: Language.KOTLIN,
            SupportedLanguage.HTML: Language.HTML,
            # CSS not in LangChain, will use None
            SupportedLanguage.CSS: None,
            # SQL not in LangChain, will use None
            SupportedLanguage.SQL: None,
            SupportedLanguage.RUST: Language.RUST,
            SupportedLanguage.CPP: Language.CPP,
            SupportedLanguage.CSHARP: Language.CSHARP,
            SupportedLanguage.PHP: Language.PHP,
            SupportedLanguage.RUBY: Language.RUBY,
            SupportedLanguage.SCALA: Language.SCALA,
            SupportedLanguage.SWIFT: Language.SWIFT,
            # Shell not in LangChain, will use None
            SupportedLanguage.SHELL: None,
            SupportedLanguage.JSON: None,  # JSON not in LangChain
            SupportedLanguage.XML: None,  # XML not in LangChain
            SupportedLanguage.YAML: None,  # YAML not in LangChain
            SupportedLanguage.TOML: None,  # TOML not in LangChain
            SupportedLanguage.MARKDOWN: Language.MARKDOWN,
        }
        return mapping.get(self)


class ChunkingStrategy(ABC):
    """
    Abstract base class for text chunking strategies.

    Provides a common interface for different chunking approaches
    while allowing customization for specific content types.
    """

    def __init__(self, **kwargs: Any) -> None:
        """Initialize chunking strategy with configuration."""
        self.config = kwargs

    @abstractmethod
    def chunk(self, content: str, source_file: Path) -> list[Chunk]:
        """
        Split content into chunks.

        Args:
            content: The text content to chunk
            source_file: Path to the source file

        Returns:
            List of chunks with metadata
        """
        pass


class MarkdownChunkingStrategy(ChunkingStrategy):
    """Chunking strategy optimized for Markdown content."""

    def __init__(
        self,
        chunk_size: int = 1500,
        chunk_overlap: int = 200,
        **kwargs: Any,
    ) -> None:
        """
        Initialize Markdown chunking strategy.

        Args:
            chunk_size: Target chunk size in characters
            chunk_overlap: Number of characters to overlap between chunks
            **kwargs: Additional configuration options
        """
        # Ensure chunk_overlap is not larger than chunk_size
        if chunk_overlap >= chunk_size:
            chunk_overlap = max(0, chunk_size - 50)

        super().__init__(**kwargs)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        # Use MarkdownTextSplitter for better handling of structure
        self.splitter = MarkdownTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            **kwargs,
        )

    def chunk(self, content: str, source_file: Path) -> list[Chunk]:
        """Split Markdown content into chunks."""
        docs = self.splitter.create_documents([content])
        chunks = []

        for i, doc in enumerate(docs):
            # Generate chunk ID based on content hash and file
            content_hash = sha256(doc.page_content.encode()).hexdigest()[:16]
            chunk_id = f"{source_file.stem}_{content_hash}_{i}"

            # Extract line numbers if possible
            lines = doc.page_content.split("\n")
            line_start = 1  # Could be enhanced with better line tracking
            line_end = line_start + len(lines) - 1

            metadata = ChunkMetadata(
                source_file=source_file,
                line_start=line_start,
                line_end=line_end,
                chunk_index=i,
                total_chunks=len(docs),
            )

            chunk = Chunk(id=chunk_id, content=doc.page_content, metadata=metadata)
            chunks.append(chunk)

        return chunks


class CodeChunkingStrategy(ChunkingStrategy):
    """Chunking strategy for code files with language-specific handling."""

    def __init__(
        self,
        language: SupportedLanguage,
        chunk_size: int = 1500,
        chunk_overlap: int = 200,
        **kwargs: Any,
    ) -> None:
        """
        Initialize code chunking strategy.

        Args:
            language: Programming language for specialized chunking
            chunk_size: Target chunk size in characters
            chunk_overlap: Number of characters to overlap between chunks
            **kwargs: Additional configuration options
        """
        # Ensure chunk_overlap is not larger than chunk_size
        if chunk_overlap >= chunk_size:
            chunk_overlap = max(0, chunk_size - 50)

        super().__init__(**kwargs)
        self.language = language
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        # Use RecursiveCharacterTextSplitter with language-specific separators
        lc_lang = language.langchain_language
        if lc_lang:
            self.splitter = RecursiveCharacterTextSplitter.from_language(
                language=lc_lang,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                **kwargs,
            )
        else:
            # Fallback to generic splitter
            self.splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                separators=["\n\n", "\n", " ", ""],
                **kwargs,
            )

    def chunk(self, content: str, source_file: Path) -> list[Chunk]:
        """Split code content into chunks."""
        docs = self.splitter.create_documents([content])
        chunks = []

        for i, doc in enumerate(docs):
            # Generate chunk ID
            content_hash = sha256(doc.page_content.encode()).hexdigest()[:16]
            chunk_id = f"{source_file.stem}_{self.language.value}_{content_hash}_{i}"

            # Calculate line numbers
            lines = doc.page_content.split("\n")
            line_start = 1  # Could be enhanced with better tracking
            line_end = line_start + len(lines) - 1

            metadata = ChunkMetadata(
                source_file=source_file,
                line_start=line_start,
                line_end=line_end,
                chunk_index=i,
                total_chunks=len(docs),
                tags=[self.language.value],  # Tag with language
            )

            chunk = Chunk(id=chunk_id, content=doc.page_content, metadata=metadata)
            chunks.append(chunk)

        return chunks


class YAMLChunkingStrategy(ChunkingStrategy):
    """Chunking strategy optimized for YAML configuration files."""

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        **kwargs: Any,
    ) -> None:
        """
        Initialize YAML chunking strategy.

        Args:
            chunk_size: Target chunk size in characters (smaller for YAML)
            chunk_overlap: Minimal overlap for structured data
            **kwargs: Additional configuration options
        """
        # Ensure chunk_overlap is not larger than chunk_size
        if chunk_overlap >= chunk_size:
            chunk_overlap = max(0, chunk_size - 50)

        super().__init__(**kwargs)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        # Use YAML-specific separators for better structure preservation
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""],
            is_separator_regex=False,
            **kwargs,
        )

    def chunk(self, content: str, source_file: Path) -> list[Chunk]:
        """Split YAML content into chunks."""
        docs = self.splitter.create_documents([content])
        chunks = []

        for i, doc in enumerate(docs):
            # Generate chunk ID
            content_hash = sha256(doc.page_content.encode()).hexdigest()[:16]
            chunk_id = f"{source_file.stem}_yaml_{content_hash}_{i}"

            # Calculate line numbers
            lines = doc.page_content.split("\n")
            line_start = 1
            line_end = line_start + len(lines) - 1

            metadata = ChunkMetadata(
                source_file=source_file,
                line_start=line_start,
                line_end=line_end,
                chunk_index=i,
                total_chunks=len(docs),
                tags=["yaml", "config"],
            )

            chunk = Chunk(id=chunk_id, content=doc.page_content, metadata=metadata)
            chunks.append(chunk)

        return chunks


class GenericChunkingStrategy(ChunkingStrategy):
    """Generic chunking strategy for unknown or plain text content."""

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 100,
        **kwargs: Any,
    ) -> None:
        """
        Initialize generic chunking strategy.

        Args:
            chunk_size: Target chunk size in characters
            chunk_overlap: Number of characters to overlap between chunks
            **kwargs: Additional configuration options
        """
        # Ensure chunk_overlap is not larger than chunk_size
        if chunk_overlap >= chunk_size:
            chunk_overlap = max(0, chunk_size - 50)

        super().__init__(**kwargs)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""],
            **kwargs,
        )

    def chunk(self, content: str, source_file: Path) -> list[Chunk]:
        """Split generic content into chunks."""
        docs = self.splitter.create_documents([content])
        chunks = []

        for i, doc in enumerate(docs):
            # Generate chunk ID
            content_hash = sha256(doc.page_content.encode()).hexdigest()[:16]
            chunk_id = f"{source_file.stem}_generic_{content_hash}_{i}"

            # Calculate line numbers
            lines = doc.page_content.split("\n")
            line_start = 1
            line_end = line_start + len(lines) - 1

            metadata = ChunkMetadata(
                source_file=source_file,
                line_start=line_start,
                line_end=line_end,
                chunk_index=i,
                total_chunks=len(docs),
                tags=["text"],
            )

            chunk = Chunk(id=chunk_id, content=doc.page_content, metadata=metadata)
            chunks.append(chunk)

        return chunks


class ChunkerFactory:
    """Factory for creating appropriate chunking strategies based on content type."""

    @staticmethod
    def create_strategy(
        file_path: Path,
        content: str | None = None,
        **kwargs: Any,
    ) -> ChunkingStrategy:
        """
        Create the appropriate chunking strategy for a file.

        Args:
            file_path: Path to the file to be chunked
            content: Optional file content (can be used for content-based detection)
            **kwargs: Additional configuration for the strategy

        Returns:
            Appropriate ChunkingStrategy instance
        """
        # Determine by file extension
        extension = file_path.suffix.lower()

        # Check for specific content types
        if extension in [".md", ".markdown"]:
            return MarkdownChunkingStrategy(**kwargs)
        elif extension in [".yaml", ".yml"]:
            return YAMLChunkingStrategy(**kwargs)
        else:
            # Check for programming languages
            language = SupportedLanguage.from_extension(extension)
            if language:
                return CodeChunkingStrategy(language=language, **kwargs)

        # Default to generic strategy
        return GenericChunkingStrategy(**kwargs)

    @staticmethod
    def chunk_file(file_path: Path, **kwargs: Any) -> list[Chunk]:
        """
        Convenience method to chunk a file directly.

        Args:
            file_path: Path to the file to chunk
            **kwargs: Additional configuration for the strategy

        Returns:
            List of chunks
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        content = file_path.read_text(encoding="utf-8")
        strategy = ChunkerFactory.create_strategy(file_path, content, **kwargs)
        return strategy.chunk(content, file_path)

    @staticmethod
    def chunk_text(
        content: str,
        source_file: Path,
        file_type: str = "markdown",
        **kwargs: Any,
    ) -> list[Chunk]:
        """
        Convenience method to chunk text content directly.

        Useful for content that has been converted from other formats
        (e.g., PDF to Markdown via markitdown).

        Args:
            content: Text content to chunk
            source_file: Original source file path (for metadata)
            file_type: Type of content (markdown, text, etc.)
            **kwargs: Additional configuration for the strategy

        Returns:
            List of chunks
        """
        # Create a virtual path with the appropriate extension for strategy selection
        if file_type == "markdown":
            virtual_path = source_file.with_suffix(".md")
        else:
            virtual_path = source_file

        strategy = ChunkerFactory.create_strategy(virtual_path, content, **kwargs)
        chunks = strategy.chunk(content, source_file)

        # Update chunks to reference the original source file
        for chunk in chunks:
            chunk.metadata.source_file = source_file

        return chunks
