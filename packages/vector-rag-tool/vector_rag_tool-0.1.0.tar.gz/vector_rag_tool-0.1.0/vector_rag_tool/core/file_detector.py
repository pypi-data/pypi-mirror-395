"""
File type detection and glob pattern expansion utilities.

This module provides functionality to detect file types by their extensions
and expand glob patterns while handling various path formats including
tilde expansion, environment variables, and relative paths.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import glob
import os
from pathlib import Path

# Native text file extensions (read directly)
NATIVE_TEXT_EXTENSIONS: dict[str, str] = {
    ".md": "markdown",
    ".py": "python",
    ".ts": "typescript",
    ".tsx": "typescript-react",
    ".js": "javascript",
    ".jsx": "javascript-react",
    ".java": "java",
    ".go": "go",
    ".kt": "kotlin",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".txt": "text",
    ".rst": "restructuredtext",
    ".toml": "toml",
    ".ini": "ini",
    ".cfg": "config",
    ".sh": "shell",
    ".bash": "shell",
    ".zsh": "shell",
    ".fish": "shell",
    ".sql": "sql",
    ".r": "r",
    ".rb": "ruby",
    ".php": "php",
    ".swift": "swift",
    ".c": "c",
    ".cpp": "cpp",
    ".h": "header",
    ".hpp": "header",
    ".cs": "csharp",
    ".rs": "rust",
    ".scala": "scala",
    ".lua": "lua",
    ".pl": "perl",
    ".ex": "elixir",
    ".exs": "elixir",
    ".clj": "clojure",
    ".hs": "haskell",
    ".erl": "erlang",
    ".tf": "terraform",
    ".hcl": "hcl",
}

# Markitdown-convertible extensions (require conversion to markdown)
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
    # Images (require OpenAI)
    ".jpg": "image",
    ".jpeg": "image",
    ".png": "image",
    ".gif": "image",
    ".webp": "image",
    ".bmp": "image",
    # Audio
    ".mp3": "audio",
    ".wav": "audio",
    ".m4a": "audio",
    # Archives
    ".zip": "archive",
}

# Combined supported extensions (native + markitdown)
SUPPORTED_EXTENSIONS: dict[str, str] = {**NATIVE_TEXT_EXTENSIONS, **MARKITDOWN_EXTENSIONS}

# Set of supported extensions for quick lookup
SUPPORTED_EXTENSIONS_SET: set[str] = set(SUPPORTED_EXTENSIONS.keys())

# Set of native text extensions
NATIVE_TEXT_EXTENSIONS_SET: set[str] = set(NATIVE_TEXT_EXTENSIONS.keys())

# Set of markitdown extensions
MARKITDOWN_EXTENSIONS_SET: set[str] = set(MARKITDOWN_EXTENSIONS.keys())


def expand_glob_pattern(pattern: str) -> list[str]:
    """
    Expand a glob pattern with support for tilde, environment variables, and relative paths.

    Args:
        pattern: The glob pattern to expand (may contain ~, $VAR, *, etc.)

    Returns:
        List of expanded file paths matching the pattern

    Examples:
        >>> expand_glob_pattern("*.py")
        ['file1.py', 'file2.py']

        >>> expand_glob_pattern("~/Documents/*.md")
        ['/Users/user/Documents/file1.md', '/Users/user/Documents/file2.md']

        >>> expand_glob_pattern("$HOME/*.yaml")
        ['/Users/user/config.yaml']
    """
    # Expand tilde (~) to user home directory
    expanded_pattern = os.path.expanduser(pattern)

    # Expand environment variables
    expanded_pattern = os.path.expandvars(expanded_pattern)

    # Convert to absolute path if relative
    if not os.path.isabs(expanded_pattern):
        expanded_pattern = os.path.abspath(expanded_pattern)

    # Use glob to find matching files
    try:
        # Use recursive glob for ** patterns
        if "**" in expanded_pattern:
            # For Python 3.14, glob can handle recursive patterns directly
            matches = glob.glob(expanded_pattern, recursive=True)
        else:
            matches = glob.glob(expanded_pattern)

        # Filter to only include files (not directories)
        file_matches = [match for match in matches if os.path.isfile(match)]

        # Normalize paths to handle /private on macOS and other path variations
        normalized_matches = [os.path.normpath(os.path.realpath(match)) for match in file_matches]

        # Remove duplicates and sort for consistent results
        unique_matches = sorted(list(set(normalized_matches)))

        return unique_matches

    except Exception:
        # If glob fails, return empty list
        return []


def detect_file_type(file_path: str) -> str | None:
    """
    Detect the file type based on its extension.

    Args:
        file_path: Path to the file

    Returns:
        File type string if supported, None otherwise

    Examples:
        >>> detect_file_type("example.py")
        'python'

        >>> detect_file_type("config.yaml")
        'yaml'

        >>> detect_file_type("unsupported.xyz")
        None
    """
    # Get the file extension (lowercase)
    extension = Path(file_path).suffix.lower()

    # Return the corresponding file type if supported
    return SUPPORTED_EXTENSIONS.get(extension)


def detect_files_from_patterns(patterns: list[str]) -> list[tuple[str, str]]:
    """
    Expand multiple glob patterns and detect file types for all matched files.

    Args:
        patterns: List of glob patterns to expand and process

    Returns:
        List of tuples containing (file_path, file_type) for all supported files

    Examples:
        >>> detect_files_from_patterns(["*.py", "docs/*.md"])
        [('main.py', 'python'), ('docs/readme.md', 'markdown')]
    """
    # Collect all files from all patterns
    all_files = set()

    for pattern in patterns:
        expanded_files = expand_glob_pattern(pattern)
        all_files.update(expanded_files)

    # Convert to sorted list for consistent results
    sorted_files = sorted(all_files)

    # Detect file types and filter for supported types
    result: list[tuple[str, str]] = []
    for file_path in sorted_files:
        file_type = detect_file_type(file_path)
        if file_type is not None:
            result.append((file_path, file_type))

    return result


def get_supported_extensions() -> set[str]:
    """
    Get the set of supported file extensions.

    Returns:
        Set of supported file extensions (including the dot)

    Examples:
        >>> get_supported_extensions()
        {'.md', '.py', '.ts', '.tsx', '.js', '.jsx', '.java', '.go', '.kt', '.yaml', '.yml'}
    """
    return SUPPORTED_EXTENSIONS_SET.copy()


def is_supported_file(file_path: str) -> bool:
    """
    Check if a file is supported based on its extension.

    Args:
        file_path: Path to the file to check

    Returns:
        True if the file type is supported, False otherwise

    Examples:
        >>> is_supported_file("example.py")
        True

        >>> is_supported_file("unsupported.xyz")
        False
    """
    extension = Path(file_path).suffix.lower()
    return extension in SUPPORTED_EXTENSIONS_SET


def is_native_text_file(file_path: str) -> bool:
    """
    Check if a file is a native text file that can be read directly.

    Args:
        file_path: Path to the file to check

    Returns:
        True if the file is a native text file, False otherwise

    Examples:
        >>> is_native_text_file("example.py")
        True

        >>> is_native_text_file("document.pdf")
        False
    """
    extension = Path(file_path).suffix.lower()
    return extension in NATIVE_TEXT_EXTENSIONS_SET


def requires_markitdown(file_path: str) -> bool:
    """
    Check if a file requires markitdown conversion.

    Args:
        file_path: Path to the file to check

    Returns:
        True if the file requires markitdown conversion, False otherwise

    Examples:
        >>> requires_markitdown("document.pdf")
        True

        >>> requires_markitdown("example.py")
        False
    """
    extension = Path(file_path).suffix.lower()
    return extension in MARKITDOWN_EXTENSIONS_SET


def group_files_by_type(file_paths: list[str]) -> dict[str, list[str]]:
    """
    Group files by their detected types.

    Args:
        file_paths: List of file paths to group

    Returns:
        Dictionary mapping file types to lists of file paths

    Examples:
        >>> group_files_by_type(["file1.py", "file2.py", "doc.md"])
        {'python': ['file1.py', 'file2.py'], 'markdown': ['doc.md']}
    """
    grouped: dict[str, list[str]] = {}

    for file_path in file_paths:
        file_type = detect_file_type(file_path)
        if file_type is not None:
            if file_type not in grouped:
                grouped[file_type] = []
            grouped[file_type].append(file_path)

    # Sort files within each group for consistent results
    for file_type in grouped:
        grouped[file_type].sort()

    return grouped
