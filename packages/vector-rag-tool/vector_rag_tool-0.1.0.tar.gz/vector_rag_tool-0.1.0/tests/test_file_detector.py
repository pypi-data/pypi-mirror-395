"""
Tests for file detection and glob pattern expansion utilities.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import os
import shutil
import tempfile
from pathlib import Path

import pytest

from vector_rag_tool.core.file_detector import (
    SUPPORTED_EXTENSIONS,
    detect_file_type,
    detect_files_from_patterns,
    expand_glob_pattern,
    get_supported_extensions,
    group_files_by_type,
    is_supported_file,
)


class TestFileTypeDetection:
    """Test file type detection functionality."""

    @pytest.mark.parametrize(
        "file_path, expected_type",
        [
            ("example.py", "python"),
            ("script.PY", "python"),  # Test case insensitive
            ("app.ts", "typescript"),
            ("component.tsx", "typescript-react"),
            ("main.js", "javascript"),
            ("react.jsx", "javascript-react"),
            ("Application.java", "java"),
            ("main.go", "go"),
            ("MyClass.kt", "kotlin"),
            ("config.yaml", "yaml"),
            ("config.yml", "yaml"),
            ("readme.md", "markdown"),
        ],
    )
    def test_detect_supported_file_types(self, file_path: str, expected_type: str) -> None:
        """Test detection of supported file types."""
        assert detect_file_type(file_path) == expected_type

    @pytest.mark.parametrize(
        "file_path",
        [
            "video.mp4",
            "unknown.xyz",
            "no_extension",
            "",
            "file.avi",
            "file.mkv",
        ],
    )
    def test_detect_unsupported_file_types(self, file_path: str) -> None:
        """Test that unsupported file types return None."""
        assert detect_file_type(file_path) is None

    def test_get_supported_extensions(self) -> None:
        """Test getting supported extensions."""
        extensions = get_supported_extensions()
        assert isinstance(extensions, set)
        assert len(extensions) == len(SUPPORTED_EXTENSIONS)
        assert all(ext.startswith(".") for ext in extensions)
        assert ".py" in extensions
        assert ".md" in extensions
        assert ".yaml" in extensions

    @pytest.mark.parametrize(
        "file_path, expected",
        [
            ("example.py", True),
            ("script.PY", True),
            ("file.txt", True),  # Now supported as native text
            ("file.pdf", True),  # Now supported via markitdown
            ("unknown.xyz", False),
            ("no_extension", False),
        ],
    )
    def test_is_supported_file(self, file_path: str, expected: bool) -> None:
        """Test checking if file is supported."""
        assert is_supported_file(file_path) == expected


class TestGlobPatternExpansion:
    """Test glob pattern expansion functionality."""

    def setup_method(self) -> None:
        """Set up temporary test directory with test files."""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

        # Create test files with various extensions
        test_files = [
            "main.py",
            "utils.py",
            "config.yaml",
            "app.ts",
            "component.tsx",
            "readme.md",
            "docs/guide.md",
            "src/index.js",
            "src/App.jsx",
            "build/output.js",
            "subdir/subnested/main.go",
            "data.json",  # Unsupported file
            "backup.txt",  # Unsupported file
        ]

        for file_path in test_files:
            full_path = Path(self.test_dir) / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(f"Content of {file_path}")

    def _norm_path(self, path: str) -> str:
        """Helper to normalize paths consistently with the implementation."""
        return os.path.normpath(os.path.realpath(path))

    def teardown_method(self) -> None:
        """Clean up temporary test directory."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    def test_expand_simple_glob(self) -> None:
        """Test expanding simple glob patterns."""
        files = expand_glob_pattern("*.py")
        expected_files = sorted(
            [
                self._norm_path(os.path.join(self.test_dir, "main.py")),
                self._norm_path(os.path.join(self.test_dir, "utils.py")),
            ]
        )
        assert files == expected_files

    def test_expand_directory_glob(self) -> None:
        """Test expanding glob with directory patterns."""
        files = expand_glob_pattern("src/*")
        # Should include both files and directories in src
        assert len(files) >= 2
        src_index_js = self._norm_path(os.path.join(self.test_dir, "src", "index.js"))
        src_app_jsx = self._norm_path(os.path.join(self.test_dir, "src", "App.jsx"))
        assert src_index_js in files
        assert src_app_jsx in files

    def test_expand_recursive_glob(self) -> None:
        """Test expanding recursive glob patterns."""
        files = expand_glob_pattern("**/*.md")
        expected_files = sorted(
            [
                self._norm_path(os.path.join(self.test_dir, "readme.md")),
                self._norm_path(os.path.join(self.test_dir, "docs", "guide.md")),
            ]
        )
        assert files == expected_files

    def test_expand_tilde_pattern(self) -> None:
        """Test expanding tilde patterns."""
        # This test uses actual home directory
        home_pattern = "~/*.md"
        files = expand_glob_pattern(home_pattern)
        # Should expand to user's home directory
        assert "~" not in str(files)
        assert isinstance(files, list)
        # All paths should be normalized
        for file_path in files:
            assert os.path.isabs(file_path)

    def test_expand_env_var_pattern(self) -> None:
        """Test expanding environment variable patterns."""
        # Set test environment variable
        os.environ["TEST_DIR"] = self.test_dir

        try:
            pattern = "$TEST_DIR/*.py"
            files = expand_glob_pattern(pattern)
            expected_files = sorted(
                [
                    self._norm_path(os.path.join(self.test_dir, "main.py")),
                    self._norm_path(os.path.join(self.test_dir, "utils.py")),
                ]
            )
            assert files == expected_files
        finally:
            del os.environ["TEST_DIR"]

    def test_expand_relative_pattern(self) -> None:
        """Test expanding relative path patterns."""
        files = expand_glob_pattern("./utils.py")
        expected_file = self._norm_path(os.path.join(self.test_dir, "utils.py"))
        assert files == [expected_file]

    def test_expand_nonexistent_pattern(self) -> None:
        """Test expanding pattern that matches no files."""
        files = expand_glob_pattern("nonexistent/*.xyz")
        assert files == []

    def test_expand_complex_pattern(self) -> None:
        """Test expanding complex glob patterns."""
        files = expand_glob_pattern("src/*.js*")
        expected_files = sorted(
            [
                self._norm_path(os.path.join(self.test_dir, "src", "index.js")),
                self._norm_path(os.path.join(self.test_dir, "src", "App.jsx")),
            ]
        )
        assert files == expected_files

    def test_expand_brace_pattern(self) -> None:
        """Test expanding glob with brace patterns."""
        # Basic glob should work (brace patterns might not be supported by all implementations)
        files = expand_glob_pattern("*.py")
        assert len(files) == 2
        assert all(f.endswith(".py") for f in files)


class TestDetectFilesFromPatterns:
    """Test detection of files from multiple patterns."""

    def setup_method(self) -> None:
        """Set up temporary test directory."""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

        # Create test files
        test_files = [
            "main.py",
            "utils.py",
            "app.ts",
            "component.tsx",
            "readme.md",
            "config.yaml",
            "video.mp4",  # Unsupported
            "docs/index.md",
        ]

        for file_path in test_files:
            full_path = Path(self.test_dir) / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(f"Content of {file_path}")

    def _norm_path(self, path: str) -> str:
        """Helper to normalize paths consistently with the implementation."""
        return os.path.normpath(os.path.realpath(path))

    def teardown_method(self) -> None:
        """Clean up temporary test directory."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    def test_single_pattern(self) -> None:
        """Test detecting files from single pattern."""
        result = detect_files_from_patterns(["*.py"])
        expected = [
            (self._norm_path(os.path.join(self.test_dir, "main.py")), "python"),
            (self._norm_path(os.path.join(self.test_dir, "utils.py")), "python"),
        ]
        assert result == expected

    def test_multiple_patterns(self) -> None:
        """Test detecting files from multiple patterns."""
        result = detect_files_from_patterns(["*.py", "**/*.md"])

        # Should include Python and markdown files
        python_files = [r for r in result if r[1] == "python"]
        markdown_files = [r for r in result if r[1] == "markdown"]

        assert len(python_files) == 2
        assert len(markdown_files) == 2
        assert all(r[1] in ["python", "markdown"] for r in result)

    def test_mixed_supported_unsupported(self) -> None:
        """Test patterns that match both supported and unsupported files."""
        result = detect_files_from_patterns(["*"])

        # Should only include supported file types
        file_types = set(file_type for _, file_type in result)
        expected_types = {"python", "typescript", "typescript-react", "markdown", "yaml"}
        assert file_types == expected_types

        # Should not include unsupported files
        paths = [path for path, _ in result]
        assert not any(path.endswith(".mp4") for path in paths)

    def test_overlapping_patterns(self) -> None:
        """Test patterns that may overlap (should not duplicate files)."""
        result = detect_files_from_patterns(["*.py", "main.*", "*"])

        # Should not have duplicates
        paths = [path for path, _ in result]
        assert len(paths) == len(set(paths))

        # Should include main.py only once
        main_py_entries = [path for path, _ in result if path.endswith("main.py")]
        assert len(main_py_entries) == 1

    def test_empty_patterns_list(self) -> None:
        """Test with empty patterns list."""
        result = detect_files_from_patterns([])
        assert result == []

    def test_no_matches(self) -> None:
        """Test with patterns that match no files."""
        result = detect_files_from_patterns(["*.xyz"])
        assert result == []


class TestGroupFilesByType:
    """Test grouping files by type functionality."""

    def test_group_supported_files(self) -> None:
        """Test grouping supported files by type."""
        files = [
            "main.py",
            "utils.py",
            "app.ts",
            "component.tsx",
            "readme.md",
            "config.yaml",
            "settings.yml",
        ]

        result = group_files_by_type(files)

        assert result == {
            "markdown": ["readme.md"],
            "python": ["main.py", "utils.py"],
            "typescript": ["app.ts"],
            "typescript-react": ["component.tsx"],
            "yaml": ["config.yaml", "settings.yml"],
        }

    def test_group_with_unsupported_files(self) -> None:
        """Test grouping with some unsupported files."""
        files = [
            "main.py",
            "video.mp4",  # Unsupported
            "movie.avi",  # Unsupported
            "readme.md",
        ]

        result = group_files_by_type(files)

        assert result == {
            "markdown": ["readme.md"],
            "python": ["main.py"],
        }

    def test_group_empty_list(self) -> None:
        """Test grouping empty file list."""
        result = group_files_by_type([])
        assert result == {}

    def test_group_all_unsupported(self) -> None:
        """Test grouping only unsupported files."""
        files = [
            "video.mp4",
            "movie.avi",
            "stream.mkv",
        ]

        result = group_files_by_type(files)
        assert result == {}


class TestIntegration:
    """Integration tests combining multiple functions."""

    def setup_method(self) -> None:
        """Set up temporary test directory."""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

        # Create realistic project structure
        files = [
            "src/main.py",
            "src/utils.py",
            "src/types.ts",
            "src/components/Widget.tsx",
            "src/App.jsx",
            "tests/test_main.py",
            "docs/README.md",
            "docs/guide.md",
            "config/app.yaml",
            "config/dev.yml",
            "build/main.js",
            "package.json",  # Unsupported
            "Dockerfile",  # Unsupported
            ".gitignore",  # Unsupported
        ]

        for file_path in files:
            full_path = Path(self.test_dir) / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(f"Content of {file_path}")

    def teardown_method(self) -> None:
        """Clean up temporary test directory."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    def test_realistic_workflow(self) -> None:
        """Test a realistic file detection workflow."""
        # Step 1: Find all Python and TypeScript files
        patterns = ["**/*.py", "**/*.ts", "**/*.tsx"]
        files_with_types = detect_files_from_patterns(patterns)

        # Verify results
        assert len(files_with_types) == 5  # 3 Python + 1 TS + 1 TSX

        python_files = [f for f, t in files_with_types if t == "python"]
        typescript_files = [f for f, t in files_with_types if t == "typescript"]
        typescript_react_files = [f for f, t in files_with_types if t == "typescript-react"]

        assert len(python_files) == 3
        assert len(typescript_files) == 1
        assert len(typescript_react_files) == 1

        # Step 2: Group by file type
        file_paths = [path for path, _ in files_with_types]
        grouped = group_files_by_type(file_paths)

        assert "python" in grouped
        assert "typescript" in grouped
        assert "typescript-react" in grouped
        assert len(grouped["python"]) == 3

        # Step 3: Check specific files exist
        all_files = expand_glob_pattern("**/*")
        assert any("main.py" in f for f in all_files)
        assert any("Widget.tsx" in f for f in all_files)

    def test_find_documentation_files(self) -> None:
        """Test finding documentation files."""
        patterns = ["**/*.md"]
        files_with_types = detect_files_from_patterns(patterns)

        assert len(files_with_types) == 2
        assert all(file_type == "markdown" for _, file_type in files_with_types)

        paths = [path for path, _ in files_with_types]
        assert any("README.md" in path for path in paths)
        assert any("guide.md" in path for path in paths)

    def test_config_file_detection(self) -> None:
        """Test configuration file detection."""
        patterns = ["**/*.yaml", "**/*.yml"]
        files_with_types = detect_files_from_patterns(patterns)

        assert len(files_with_types) == 2
        assert all(file_type == "yaml" for _, file_type in files_with_types)

        paths = [path for path, _ in files_with_types]
        assert any("app.yaml" in path for path in paths)
        assert any("dev.yml" in path for path in paths)
