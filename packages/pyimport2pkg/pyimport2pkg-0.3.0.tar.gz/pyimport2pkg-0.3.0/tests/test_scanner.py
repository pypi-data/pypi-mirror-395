"""Tests for the Scanner module."""

import pytest
from pathlib import Path
import tempfile
import os

from pyimport2pkg.scanner import Scanner, scan_project


class TestScanner:
    """Tests for Scanner class."""

    def test_scan_single_file(self, tmp_path: Path):
        """Test scanning a single Python file."""
        py_file = tmp_path / "test.py"
        py_file.write_text("import os")

        scanner = Scanner()
        result = scanner.scan(py_file)

        assert len(result) == 1
        assert result[0] == py_file

    def test_scan_ignores_non_python_files(self, tmp_path: Path):
        """Test that non-Python files are ignored."""
        py_file = tmp_path / "test.py"
        py_file.write_text("import os")

        txt_file = tmp_path / "readme.txt"
        txt_file.write_text("readme content")

        js_file = tmp_path / "script.js"
        js_file.write_text("console.log('hello')")

        scanner = Scanner()
        result = scanner.scan(tmp_path)

        assert len(result) == 1
        assert result[0] == py_file

    def test_scan_directory_recursive(self, tmp_path: Path):
        """Test recursive directory scanning."""
        # Create nested structure
        (tmp_path / "module1.py").write_text("import os")
        (tmp_path / "subdir").mkdir()
        (tmp_path / "subdir" / "module2.py").write_text("import sys")
        (tmp_path / "subdir" / "nested").mkdir()
        (tmp_path / "subdir" / "nested" / "module3.py").write_text("import json")

        scanner = Scanner()
        result = scanner.scan(tmp_path)

        assert len(result) == 3

    def test_excludes_venv_directory(self, tmp_path: Path):
        """Test that .venv directory is excluded."""
        (tmp_path / "main.py").write_text("import os")
        (tmp_path / ".venv").mkdir()
        (tmp_path / ".venv" / "lib.py").write_text("import sys")

        scanner = Scanner()
        result = scanner.scan(tmp_path)

        assert len(result) == 1
        assert result[0].name == "main.py"

    def test_excludes_pycache(self, tmp_path: Path):
        """Test that __pycache__ is excluded."""
        (tmp_path / "main.py").write_text("import os")
        (tmp_path / "__pycache__").mkdir()
        (tmp_path / "__pycache__" / "main.cpython-311.pyc").write_text("")

        scanner = Scanner()
        result = scanner.scan(tmp_path)

        assert len(result) == 1

    def test_excludes_git_directory(self, tmp_path: Path):
        """Test that .git directory is excluded."""
        (tmp_path / "main.py").write_text("import os")
        (tmp_path / ".git").mkdir()
        (tmp_path / ".git" / "hooks" ).mkdir(parents=True)
        (tmp_path / ".git" / "hooks" / "pre-commit.py").write_text("#!/usr/bin/env python")

        scanner = Scanner()
        result = scanner.scan(tmp_path)

        assert len(result) == 1

    def test_excludes_hidden_files_by_default(self, tmp_path: Path):
        """Test that hidden files are excluded by default."""
        (tmp_path / "main.py").write_text("import os")
        (tmp_path / ".hidden.py").write_text("import sys")

        scanner = Scanner()
        result = scanner.scan(tmp_path)

        assert len(result) == 1
        assert result[0].name == "main.py"

    def test_includes_hidden_files_when_enabled(self, tmp_path: Path):
        """Test including hidden files when option is enabled."""
        (tmp_path / "main.py").write_text("import os")
        (tmp_path / ".hidden.py").write_text("import sys")

        scanner = Scanner(include_hidden=True)
        result = scanner.scan(tmp_path)

        assert len(result) == 2

    def test_custom_exclude_dirs(self, tmp_path: Path):
        """Test custom directory exclusion."""
        (tmp_path / "main.py").write_text("import os")
        (tmp_path / "vendor").mkdir()
        (tmp_path / "vendor" / "lib.py").write_text("import sys")

        # Without custom exclude
        scanner1 = Scanner()
        result1 = scanner1.scan(tmp_path)
        assert len(result1) == 2

        # With custom exclude
        scanner2 = Scanner(exclude_dirs={"vendor"})
        result2 = scanner2.scan(tmp_path)
        assert len(result2) == 1

    def test_custom_exclude_files(self, tmp_path: Path):
        """Test custom file exclusion."""
        (tmp_path / "main.py").write_text("import os")
        (tmp_path / "conftest.py").write_text("import pytest")

        # Without custom exclude
        scanner1 = Scanner()
        result1 = scanner1.scan(tmp_path)
        assert len(result1) == 2

        # With custom exclude
        scanner2 = Scanner(exclude_files={"conftest.py"})
        result2 = scanner2.scan(tmp_path)
        assert len(result2) == 1

    def test_excludes_setup_py_by_default(self, tmp_path: Path):
        """Test that setup.py is excluded by default."""
        (tmp_path / "main.py").write_text("import os")
        (tmp_path / "setup.py").write_text("from setuptools import setup")

        scanner = Scanner()
        result = scanner.scan(tmp_path)

        assert len(result) == 1
        assert result[0].name == "main.py"

    def test_empty_directory(self, tmp_path: Path):
        """Test scanning an empty directory."""
        scanner = Scanner()
        result = scanner.scan(tmp_path)

        assert len(result) == 0

    def test_nonexistent_path(self, tmp_path: Path):
        """Test scanning a non-existent path."""
        scanner = Scanner()
        result = scanner.scan(tmp_path / "nonexistent")

        assert len(result) == 0

    def test_excludes_egg_info(self, tmp_path: Path):
        """Test that .egg-info directories are excluded."""
        (tmp_path / "main.py").write_text("import os")
        (tmp_path / "mypackage.egg-info").mkdir()
        (tmp_path / "mypackage.egg-info" / "PKG-INFO.py").write_text("")

        scanner = Scanner()
        result = scanner.scan(tmp_path)

        assert len(result) == 1


class TestScanProject:
    """Tests for scan_project convenience function."""

    def test_basic_scan(self, tmp_path: Path):
        """Test basic project scanning."""
        (tmp_path / "main.py").write_text("import os")

        result = scan_project(tmp_path)

        assert len(result) == 1

    def test_with_options(self, tmp_path: Path):
        """Test scanning with custom options."""
        (tmp_path / "main.py").write_text("import os")
        (tmp_path / "tests").mkdir()
        (tmp_path / "tests" / "test_main.py").write_text("import pytest")

        result = scan_project(tmp_path, exclude_dirs={"tests"})

        assert len(result) == 1
        assert result[0].name == "main.py"


class TestSampleProject:
    """Tests using the sample project fixture."""

    def test_scan_sample_project(self, sample_project_dir: Path):
        """Test scanning the sample project."""
        scanner = Scanner()
        result = scanner.scan(sample_project_dir)

        # Should find main.py, utils.py, and subdir/nested.py
        assert len(result) == 3
        names = {f.name for f in result}
        assert "main.py" in names
        assert "utils.py" in names
        assert "nested.py" in names
