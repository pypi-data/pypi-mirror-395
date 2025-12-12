"""
Document converter using markitdown for converting various file formats to Markdown.

This module provides functionality to convert documents (PDF, DOCX, XLSX, PPTX,
images, etc.) to Markdown format for indexing. It supports optional OpenAI
integration for image descriptions, which must be explicitly enabled.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import os
from pathlib import Path
from typing import Any

from vector_rag_tool.logging_config import get_logger

logger = get_logger(__name__)

# File extensions that require markitdown conversion
MARKITDOWN_EXTENSIONS: dict[str, str] = {
    # Documents
    ".pdf": "pdf",
    ".docx": "word",
    ".doc": "word",
    ".pptx": "powerpoint",
    ".ppt": "powerpoint",
    ".xlsx": "excel",
    ".xls": "excel",
    # Data formats
    ".csv": "csv",
    ".json": "json",
    ".xml": "xml",
    # Web/ebook
    ".html": "html",
    ".htm": "html",
    ".epub": "epub",
    # Images (require OpenAI for descriptions)
    ".jpg": "image",
    ".jpeg": "image",
    ".png": "image",
    ".gif": "image",
    ".webp": "image",
    ".bmp": "image",
    # Audio (require transcription)
    ".mp3": "audio",
    ".wav": "audio",
    ".m4a": "audio",
    # Archives
    ".zip": "archive",
}

# Extensions that require OpenAI for meaningful content extraction
OPENAI_REQUIRED_EXTENSIONS: set[str] = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".webp",
    ".bmp",
}

# Extensions where OpenAI enhances but isn't required (e.g., PPTX with embedded images)
OPENAI_ENHANCED_EXTENSIONS: set[str] = {
    ".pptx",
    ".ppt",
}


class MarkitdownNotAvailableError(ImportError):
    """Raised when markitdown is not installed."""

    pass


class OpenAIRequiredError(ValueError):
    """Raised when OpenAI is required but not enabled."""

    pass


def is_markitdown_available() -> bool:
    """
    Check if markitdown is installed and available.

    Returns:
        True if markitdown is available, False otherwise.
    """
    try:
        from markitdown import MarkItDown  # noqa: F401

        return True
    except ImportError:
        return False


def requires_markitdown(file_path: str) -> bool:
    """
    Check if a file requires markitdown for conversion.

    Args:
        file_path: Path to the file.

    Returns:
        True if the file requires markitdown conversion.
    """
    extension = Path(file_path).suffix.lower()
    return extension in MARKITDOWN_EXTENSIONS


def requires_openai(file_path: str) -> bool:
    """
    Check if a file requires OpenAI for meaningful content extraction.

    Args:
        file_path: Path to the file.

    Returns:
        True if the file requires OpenAI for content extraction.
    """
    extension = Path(file_path).suffix.lower()
    return extension in OPENAI_REQUIRED_EXTENSIONS


def benefits_from_openai(file_path: str) -> bool:
    """
    Check if a file would benefit from OpenAI (enhanced but not required).

    Args:
        file_path: Path to the file.

    Returns:
        True if the file would benefit from OpenAI integration.
    """
    extension = Path(file_path).suffix.lower()
    return extension in OPENAI_ENHANCED_EXTENSIONS


def get_file_category(file_path: str) -> str | None:
    """
    Get the category of a file based on its extension.

    Args:
        file_path: Path to the file.

    Returns:
        File category string if supported by markitdown, None otherwise.
    """
    extension = Path(file_path).suffix.lower()
    return MARKITDOWN_EXTENSIONS.get(extension)


class DocumentConverter:
    """
    Converts documents to Markdown using markitdown.

    Supports various file formats including PDF, Word, Excel, PowerPoint,
    images, and more. OpenAI integration for image descriptions must be
    explicitly enabled via the enable_openai parameter.
    """

    def __init__(
        self,
        enable_openai: bool = False,
        openai_model: str = "gpt-4o",
        openai_prompt: str | None = None,
    ) -> None:
        """
        Initialize the document converter.

        Args:
            enable_openai: Whether to enable OpenAI for image descriptions.
            openai_model: OpenAI model to use for image descriptions.
            openai_prompt: Custom prompt for image descriptions.

        Raises:
            MarkitdownNotAvailableError: If markitdown is not installed.
        """
        if not is_markitdown_available():
            raise MarkitdownNotAvailableError(
                "markitdown is not installed. Install with: "
                "uv add 'vector-rag-tool[documents]' or uv add markitdown[all]"
            )

        self.enable_openai = enable_openai
        self.openai_model = openai_model
        self.openai_prompt = openai_prompt
        self._markitdown = self._create_markitdown()

        logger.info(
            "DocumentConverter initialized (openai_enabled=%s, model=%s)",
            enable_openai,
            openai_model if enable_openai else "N/A",
        )

    def _create_markitdown(self) -> Any:
        """Create and configure the MarkItDown instance."""
        from markitdown import MarkItDown

        if self.enable_openai:
            try:
                from openai import OpenAI

                # Use environment variable for API key
                api_key = os.environ.get("OPENAI_API_KEY")
                if not api_key:
                    raise OpenAIRequiredError(
                        "OPENAI_API_KEY environment variable not set. "
                        "Set it or disable --enable-openai flag."
                    )

                client = OpenAI(api_key=api_key)
                logger.debug("OpenAI client initialized for image descriptions")

                kwargs: dict[str, object] = {
                    "llm_client": client,
                    "llm_model": self.openai_model,
                }
                if self.openai_prompt:
                    kwargs["llm_prompt"] = self.openai_prompt

                return MarkItDown(**kwargs)

            except ImportError:
                raise MarkitdownNotAvailableError(
                    "openai package not installed. Install with: "
                    "uv add 'vector-rag-tool[documents]' or uv add openai"
                )
        else:
            return MarkItDown(enable_plugins=False)

    def convert(self, file_path: str) -> str:
        """
        Convert a document to Markdown.

        Args:
            file_path: Path to the file to convert.

        Returns:
            Markdown content as string.

        Raises:
            OpenAIRequiredError: If file requires OpenAI but it's not enabled.
            FileNotFoundError: If the file doesn't exist.
            ValueError: If conversion fails.
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Check if OpenAI is required but not enabled
        if requires_openai(file_path) and not self.enable_openai:
            extension = path.suffix.lower()
            raise OpenAIRequiredError(
                f"File type '{extension}' requires OpenAI for content extraction. "
                f"Use --enable-openai flag to enable OpenAI integration."
            )

        # Log warning if file would benefit from OpenAI
        if benefits_from_openai(file_path) and not self.enable_openai:
            logger.warning(
                "File '%s' may have embedded images. "
                "Use --enable-openai for better image descriptions.",
                path.name,
            )

        logger.debug("Converting file: %s", file_path)

        try:
            result = self._markitdown.convert(str(path))
            content: str = str(result.text_content)

            if not content or not content.strip():
                logger.warning("Empty content extracted from: %s", file_path)
                return f"# {path.name}\n\n*No extractable content*"

            logger.debug(
                "Converted %s: %d characters extracted",
                path.name,
                len(content),
            )
            return content

        except Exception as e:
            logger.error("Failed to convert %s: %s", file_path, e)
            raise ValueError(f"Failed to convert {file_path}: {e}")

    def can_convert(self, file_path: str) -> bool:
        """
        Check if a file can be converted.

        Args:
            file_path: Path to the file.

        Returns:
            True if the file can be converted (considering OpenAI requirements).
        """
        if not requires_markitdown(file_path):
            return False

        # If OpenAI is required but not enabled, cannot convert
        if requires_openai(file_path) and not self.enable_openai:
            return False

        return True

    def get_supported_extensions(self) -> set[str]:
        """
        Get set of supported file extensions.

        Returns:
            Set of supported extensions (including the dot).
        """
        if self.enable_openai:
            return set(MARKITDOWN_EXTENSIONS.keys())
        else:
            # Exclude extensions that require OpenAI
            return set(MARKITDOWN_EXTENSIONS.keys()) - OPENAI_REQUIRED_EXTENSIONS


def convert_file_to_markdown(
    file_path: str,
    enable_openai: bool = False,
    openai_model: str = "gpt-4o",
) -> str:
    """
    Convenience function to convert a single file to Markdown.

    Args:
        file_path: Path to the file to convert.
        enable_openai: Whether to enable OpenAI for image descriptions.
        openai_model: OpenAI model to use.

    Returns:
        Markdown content as string.

    Raises:
        OpenAIRequiredError: If file requires OpenAI but it's not enabled.
        MarkitdownNotAvailableError: If markitdown is not installed.
    """
    converter = DocumentConverter(
        enable_openai=enable_openai,
        openai_model=openai_model,
    )
    return converter.convert(file_path)
