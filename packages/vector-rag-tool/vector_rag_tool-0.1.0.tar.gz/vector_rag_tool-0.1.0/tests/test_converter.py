"""
Tests for the document converter module.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from vector_rag_tool.core.converter import (
    MARKITDOWN_EXTENSIONS,
    OPENAI_ENHANCED_EXTENSIONS,
    OPENAI_REQUIRED_EXTENSIONS,
    benefits_from_openai,
    get_file_category,
    is_markitdown_available,
    requires_markitdown,
    requires_openai,
)


class TestFileTypeDetection:
    """Tests for file type detection functions."""

    def test_requires_markitdown_pdf(self) -> None:
        """PDF files require markitdown."""
        assert requires_markitdown("document.pdf") is True

    def test_requires_markitdown_docx(self) -> None:
        """Word documents require markitdown."""
        assert requires_markitdown("report.docx") is True

    def test_requires_markitdown_xlsx(self) -> None:
        """Excel files require markitdown."""
        assert requires_markitdown("data.xlsx") is True

    def test_requires_markitdown_pptx(self) -> None:
        """PowerPoint files require markitdown."""
        assert requires_markitdown("slides.pptx") is True

    def test_requires_markitdown_python_false(self) -> None:
        """Python files do not require markitdown."""
        assert requires_markitdown("script.py") is False

    def test_requires_markitdown_markdown_false(self) -> None:
        """Markdown files do not require markitdown."""
        assert requires_markitdown("readme.md") is False

    def test_requires_openai_image(self) -> None:
        """Image files require OpenAI for content extraction."""
        assert requires_openai("photo.jpg") is True
        assert requires_openai("screenshot.png") is True
        assert requires_openai("graphic.gif") is True

    def test_requires_openai_document_false(self) -> None:
        """Document files do not require OpenAI."""
        assert requires_openai("document.pdf") is False
        assert requires_openai("report.docx") is False

    def test_benefits_from_openai_pptx(self) -> None:
        """PowerPoint files benefit from OpenAI for embedded images."""
        assert benefits_from_openai("slides.pptx") is True

    def test_benefits_from_openai_pdf_false(self) -> None:
        """PDF files do not benefit from OpenAI (text extraction works)."""
        assert benefits_from_openai("document.pdf") is False


class TestFileCategories:
    """Tests for file category detection."""

    def test_get_file_category_pdf(self) -> None:
        """PDF files are categorized correctly."""
        assert get_file_category("document.pdf") == "pdf"

    def test_get_file_category_docx(self) -> None:
        """Word documents are categorized correctly."""
        assert get_file_category("report.docx") == "word"

    def test_get_file_category_xlsx(self) -> None:
        """Excel files are categorized correctly."""
        assert get_file_category("data.xlsx") == "excel"

    def test_get_file_category_image(self) -> None:
        """Image files are categorized correctly."""
        assert get_file_category("photo.jpg") == "image"
        assert get_file_category("screenshot.png") == "image"

    def test_get_file_category_unsupported(self) -> None:
        """Unsupported files return None."""
        assert get_file_category("script.py") is None
        assert get_file_category("unknown.xyz") is None


class TestExtensionSets:
    """Tests for extension set definitions."""

    def test_markitdown_extensions_include_documents(self) -> None:
        """Markitdown extensions include document formats."""
        assert ".pdf" in MARKITDOWN_EXTENSIONS
        assert ".docx" in MARKITDOWN_EXTENSIONS
        assert ".xlsx" in MARKITDOWN_EXTENSIONS
        assert ".pptx" in MARKITDOWN_EXTENSIONS

    def test_markitdown_extensions_include_images(self) -> None:
        """Markitdown extensions include image formats."""
        assert ".jpg" in MARKITDOWN_EXTENSIONS
        assert ".png" in MARKITDOWN_EXTENSIONS

    def test_openai_required_extensions_are_images(self) -> None:
        """OpenAI required extensions are image formats."""
        assert ".jpg" in OPENAI_REQUIRED_EXTENSIONS
        assert ".jpeg" in OPENAI_REQUIRED_EXTENSIONS
        assert ".png" in OPENAI_REQUIRED_EXTENSIONS
        assert ".gif" in OPENAI_REQUIRED_EXTENSIONS

    def test_openai_enhanced_extensions_are_presentations(self) -> None:
        """OpenAI enhanced extensions are presentation formats."""
        assert ".pptx" in OPENAI_ENHANCED_EXTENSIONS
        assert ".ppt" in OPENAI_ENHANCED_EXTENSIONS


class TestMarkitdownAvailability:
    """Tests for markitdown availability check."""

    def test_is_markitdown_available_returns_bool(self) -> None:
        """Availability check returns boolean."""
        result = is_markitdown_available()
        assert isinstance(result, bool)
