"""Tests for the CLI module and end-to-end integration tests - v0.2.0 comprehensive tests."""

import pytest
from pathlib import Path
import json

from pyimport2pkg.cli import main, create_parser, parse_python_version


class TestCLIParser:
    """Test CLI argument parsing."""

    def test_create_parser(self):
        """Test parser creation."""
        parser = create_parser()
        assert parser is not None

    def test_analyze_command_basic(self):
        """Test analyze command parsing."""
        parser = create_parser()
        args = parser.parse_args(["analyze", "."])

        assert args.command == "analyze"
        assert args.path == Path(".")

    def test_analyze_with_all_options(self):
        """Test analyze with various options."""
        parser = create_parser()
        args = parser.parse_args([
            "analyze", ".",
            "-o", "requirements.txt",
            "-f", "json",
            "--exclude", "tests,docs",
            "--exclude-optional",
            "--python-version", "3.8",
            "--no-comments",
            "--use-database",
        ])

        assert args.output == Path("requirements.txt")
        assert args.format == "json"
        assert args.exclude == "tests,docs"
        assert args.exclude_optional is True
        assert args.python_version == "3.8"
        assert args.no_comments is True
        assert args.use_database is True

    def test_analyze_format_choices(self):
        """Test that format only accepts valid choices."""
        parser = create_parser()

        # Valid formats
        for fmt in ["requirements", "json", "simple"]:
            args = parser.parse_args(["analyze", ".", "-f", fmt])
            assert args.format == fmt

    def test_builddb_command(self):
        """Test build-db command parsing."""
        parser = create_parser()
        args = parser.parse_args(["build-db", "--max-packages", "100", "--concurrency", "10"])

        assert args.command == "build-db"
        assert args.max_packages == 100
        assert args.concurrency == 10

    def test_dbinfo_command(self):
        """Test db-info command parsing."""
        parser = create_parser()
        args = parser.parse_args(["db-info"])

        assert args.command == "db-info"

    def test_query_command(self):
        """Test query command parsing."""
        parser = create_parser()
        args = parser.parse_args(["query", "numpy"])

        assert args.command == "query"
        assert args.module == "numpy"

    def test_no_command_shows_help(self, capsys):
        """Test that no command shows help."""
        result = main([])
        assert result == 0


class TestParsePythonVersion:
    """Test Python version parsing."""

    def test_parse_valid_version(self):
        """Test parsing valid version strings."""
        assert parse_python_version("3.8") == (3, 8)
        assert parse_python_version("3.11") == (3, 11)
        assert parse_python_version("3.6") == (3, 6)

    def test_parse_none(self):
        """Test parsing None returns None."""
        assert parse_python_version(None) is None

    def test_parse_invalid_version(self):
        """Test parsing invalid version returns None."""
        assert parse_python_version("invalid") is None
        assert parse_python_version("3") is None
        assert parse_python_version("") is None
        assert parse_python_version("abc.def") is None


class TestCLIQuery:
    """Test CLI query command."""

    def test_query_hardcoded_module_cv2(self, capsys):
        """Test querying cv2 returns opencv-python."""
        result = main(["query", "cv2"])

        assert result == 0
        captured = capsys.readouterr()
        assert "opencv-python" in captured.out
        assert "hardcoded" in captured.out.lower()

    def test_query_hardcoded_module_PIL(self, capsys):
        """Test querying PIL returns Pillow."""
        result = main(["query", "PIL"])

        assert result == 0
        captured = capsys.readouterr()
        assert "Pillow" in captured.out

    def test_query_namespace_module(self, capsys):
        """Test querying a namespace module."""
        result = main(["query", "google.cloud.storage"])

        assert result == 0
        captured = capsys.readouterr()
        assert "google-cloud-storage" in captured.out

    def test_query_guessed_module(self, capsys):
        """Test querying a module that gets guessed."""
        result = main(["query", "numpy"])

        assert result == 0
        captured = capsys.readouterr()
        assert "numpy" in captured.out


class TestCLIAnalyze:
    """Test CLI analyze command."""

    def test_analyze_nonexistent_path(self, capsys):
        """Test analyzing a non-existent path."""
        result = main(["analyze", "/nonexistent/path/that/does/not/exist"])

        assert result == 1
        captured = capsys.readouterr()
        assert "does not exist" in captured.err

    def test_analyze_sample_project_requirements_format(self, sample_project_dir: Path, capsys):
        """Test analyzing sample project with requirements format."""
        result = main(["analyze", str(sample_project_dir)])

        assert result == 0
        captured = capsys.readouterr()

        # Should find expected packages
        output = captured.out.lower()
        assert "numpy" in output or "pandas" in output

    def test_analyze_json_format_structure(self, sample_project_dir: Path, capsys):
        """Test JSON output has correct structure."""
        result = main(["analyze", str(sample_project_dir), "-f", "json"])

        assert result == 0
        captured = capsys.readouterr()

        # Should be valid JSON
        data = json.loads(captured.out)

        # Check required structure
        assert "meta" in data
        assert "required" in data
        assert "optional" in data
        assert "unresolved" in data
        assert "warnings" in data

        # Check meta
        assert data["meta"]["tool"] == "pyimport2pkg"
        assert data["meta"]["version"] == "0.2.0"
        assert "generated_at" in data["meta"]

    def test_analyze_simple_format(self, sample_project_dir: Path, capsys):
        """Test simple output format."""
        result = main(["analyze", str(sample_project_dir), "-f", "simple"])

        assert result == 0
        captured = capsys.readouterr()

        # Should be a simple list, one package per line
        lines = [l for l in captured.out.strip().split("\n") if l]
        assert len(lines) > 0

        # No comments in simple format
        for line in lines:
            assert not line.startswith("#")

    def test_analyze_to_file(self, sample_project_dir: Path, tmp_path: Path):
        """Test writing output to file."""
        output_file = tmp_path / "requirements.txt"
        result = main([
            "analyze",
            str(sample_project_dir),
            "-o", str(output_file),
        ])

        assert result == 0
        assert output_file.exists()
        content = output_file.read_text()
        assert len(content) > 0

    def test_analyze_with_exclude(self, tmp_path: Path, capsys):
        """Test analyzing with exclusions."""
        # Create test files
        (tmp_path / "main.py").write_text("import numpy")
        (tmp_path / "tests").mkdir()
        (tmp_path / "tests" / "test_main.py").write_text("import pytest")

        result = main([
            "analyze",
            str(tmp_path),
            "--exclude", "tests",
            "-f", "simple",
        ])

        assert result == 0
        captured = capsys.readouterr()

        # Should have numpy but not pytest
        assert "numpy" in captured.out
        assert "pytest" not in captured.out

    def test_analyze_exclude_optional(self, tmp_path: Path, capsys):
        """Test --exclude-optional flag."""
        (tmp_path / "app.py").write_text("""
import numpy

try:
    import ujson
except ImportError:
    pass
""")

        # Default behavior (includes optional in requirements format)
        result = main(["analyze", str(tmp_path)])
        assert result == 0
        captured = capsys.readouterr()
        with_optional = captured.out

        # With --exclude-optional flag
        result = main(["analyze", str(tmp_path), "--exclude-optional"])
        assert result == 0
        captured = capsys.readouterr()
        without_optional = captured.out

        # numpy should be in both
        assert "numpy" in with_optional
        assert "numpy" in without_optional

        # ujson should only be in with_optional (in the Try-except section)
        assert "ujson" in with_optional
        assert "ujson" not in without_optional

    def test_analyze_no_comments_flag(self, tmp_path: Path, capsys):
        """Test --no-comments flag."""
        (tmp_path / "app.py").write_text("import numpy")

        result = main(["analyze", str(tmp_path), "--no-comments"])
        assert result == 0
        captured = capsys.readouterr()

        # Should not have header comments
        assert "# Auto-generated" not in captured.out
        assert "# Generated at" not in captured.out

    def test_analyze_python_version_flag(self, tmp_path: Path, capsys):
        """Test --python-version flag affects backport detection."""
        (tmp_path / "app.py").write_text("import dataclasses")

        # Python 3.6 - dataclasses needs backport
        result = main(["analyze", str(tmp_path), "-f", "simple", "--python-version", "3.6"])
        assert result == 0
        captured = capsys.readouterr()
        assert "dataclasses" in captured.out  # Needs the backport package

        # Python 3.7+ - dataclasses is stdlib
        result = main(["analyze", str(tmp_path), "-f", "simple", "--python-version", "3.7"])
        assert result == 0
        captured = capsys.readouterr()
        # dataclasses is stdlib in 3.7+, should not appear
        assert "dataclasses" not in captured.out


class TestIntegration:
    """End-to-end integration tests."""

    def test_full_pipeline_output_format(self, tmp_path: Path):
        """Test the complete analysis pipeline produces correct output."""
        # Create a test project
        (tmp_path / "myproject").mkdir()
        (tmp_path / "myproject" / "__init__.py").write_text("")
        (tmp_path / "myproject" / "main.py").write_text("""
import os
import json

import numpy as np
import pandas as pd
from PIL import Image
from sklearn.model_selection import train_test_split

try:
    import ujson as json_lib
except ImportError:
    import json as json_lib

from .utils import helper
""")
        (tmp_path / "myproject" / "utils.py").write_text("""
import requests
from bs4 import BeautifulSoup
""")

        # Run analysis
        from pyimport2pkg.scanner import scan_project
        from pyimport2pkg.parser import Parser
        from pyimport2pkg.filter import Filter
        from pyimport2pkg.mapper import Mapper
        from pyimport2pkg.resolver import Resolver, ResolveStrategy
        from pyimport2pkg.exporter import Exporter

        # Scan
        files = scan_project(tmp_path)
        assert len(files) == 3  # __init__.py, main.py, utils.py

        # Parse
        parser = Parser()
        all_imports = []
        for f in files:
            all_imports.extend(parser.parse_file(f))

        # Verify parsing captured all imports
        module_names = {i.module_name for i in all_imports}
        assert "numpy" in module_names
        assert "pandas" in module_names
        assert "PIL" in module_names
        assert "sklearn.model_selection" in module_names
        assert "requests" in module_names
        assert "bs4" in module_names
        assert "ujson" in module_names

        # Filter
        filter_ = Filter(project_root=tmp_path)
        third_party, filtered = filter_.filter_imports(all_imports)

        # Verify filtering
        third_party_modules = {i.top_level for i in third_party}
        assert "numpy" in third_party_modules
        assert "pandas" in third_party_modules
        assert "PIL" in third_party_modules
        assert "sklearn" in third_party_modules
        assert "requests" in third_party_modules
        assert "bs4" in third_party_modules
        assert "ujson" in third_party_modules

        # Relative imports should be filtered
        assert "utils" not in third_party_modules

        # Standard library should be filtered
        filtered_modules = {i.top_level for i in filtered if not i.is_relative}
        assert "os" in filtered_modules
        assert "json" in filtered_modules

        # Map
        mapper = Mapper()
        results = mapper.map_imports(third_party)

        # Resolve
        resolver = Resolver(strategy=ResolveStrategy.MOST_POPULAR)
        results = resolver.resolve_all(results)

        # Verify mappings
        package_map = {r.import_info.top_level: r.resolved_package for r in results}
        assert package_map["PIL"] == "Pillow"
        assert package_map["sklearn"] == "scikit-learn"
        assert package_map["bs4"] == "beautifulsoup4"

        # Export
        exporter = Exporter(include_optional=True, include_comments=True)
        required = [r for r in results if not r.import_info.is_optional]
        optional = [r for r in results if r.import_info.is_optional]

        content = exporter.export_requirements_txt(required, optional)

        # Verify output contains correct packages
        assert "numpy" in content
        assert "pandas" in content
        assert "Pillow" in content  # PIL -> Pillow
        assert "scikit-learn" in content  # sklearn -> scikit-learn
        assert "requests" in content
        assert "beautifulsoup4" in content  # bs4 -> beautifulsoup4

        # Verify try-except section exists with ujson
        assert "# === Try-except imports" in content
        assert "ujson" in content

    def test_namespace_package_handling(self, tmp_path: Path):
        """Test handling of namespace packages."""
        (tmp_path / "cloud_app.py").write_text("""
import google.cloud.storage
import google.cloud.bigquery
import azure.storage.blob
""")

        from pyimport2pkg.scanner import scan_project
        from pyimport2pkg.parser import Parser
        from pyimport2pkg.filter import Filter
        from pyimport2pkg.mapper import Mapper

        files = scan_project(tmp_path)
        parser = Parser()
        imports = parser.parse_file(files[0])

        filter_ = Filter()
        third_party, _ = filter_.filter_imports(imports)

        mapper = Mapper()
        results = mapper.map_imports(third_party)

        packages = {r.resolved_package for r in results}

        assert "google-cloud-storage" in packages
        assert "google-cloud-bigquery" in packages
        assert "azure-storage-blob" in packages

    def test_hardcoded_mapping_handling(self, tmp_path: Path):
        """Test handling of classic module-package mismatches."""
        (tmp_path / "cv_app.py").write_text("""
import cv2
from PIL import Image
import yaml
from sklearn.ensemble import RandomForestClassifier
import dateutil
""")

        from pyimport2pkg.scanner import scan_project
        from pyimport2pkg.parser import Parser
        from pyimport2pkg.filter import Filter
        from pyimport2pkg.mapper import Mapper

        files = scan_project(tmp_path)
        parser = Parser()
        imports = parser.parse_file(files[0])

        filter_ = Filter()
        third_party, _ = filter_.filter_imports(imports)

        mapper = Mapper()
        results = mapper.map_imports(third_party)

        packages = {r.resolved_package for r in results}

        assert "opencv-python" in packages  # cv2 -> opencv-python
        assert "Pillow" in packages  # PIL -> Pillow
        assert "PyYAML" in packages  # yaml -> PyYAML
        assert "scikit-learn" in packages  # sklearn -> scikit-learn
        assert "python-dateutil" in packages  # dateutil -> python-dateutil

    def test_conditional_import_detection(self, tmp_path: Path):
        """Test detection of platform-conditional imports."""
        (tmp_path / "platform_app.py").write_text("""
import sys

if sys.platform == "win32":
    import winreg

if sys.platform == "darwin":
    import objc
""")

        from pyimport2pkg.scanner import scan_project
        from pyimport2pkg.parser import Parser
        from pyimport2pkg.filter import Filter

        files = scan_project(tmp_path)
        parser = Parser()
        imports = parser.parse_file(files[0])

        # winreg and objc should be marked as conditional/optional
        optional_imports = [i for i in imports if i.is_optional]
        optional_modules = {i.module_name for i in optional_imports}

        # These platform-specific imports should be optional
        assert "winreg" in optional_modules or "objc" in optional_modules

    def test_try_except_import_detection(self, tmp_path: Path):
        """Test detection of try-except imports."""
        (tmp_path / "fallback_app.py").write_text("""
try:
    import ujson as json
except ImportError:
    import json

try:
    from lxml import etree
except ImportError:
    from xml.etree import ElementTree as etree
""")

        from pyimport2pkg.scanner import scan_project
        from pyimport2pkg.parser import Parser

        files = scan_project(tmp_path)
        parser = Parser()
        imports = parser.parse_file(files[0])

        # Find try-except imports
        from pyimport2pkg.models import ImportContext
        try_except_imports = [i for i in imports if i.context == ImportContext.TRY_EXCEPT]
        try_except_modules = {i.module_name for i in try_except_imports}

        assert "ujson" in try_except_modules
        assert "lxml" in try_except_modules

    def test_json_export_complete_structure(self, tmp_path: Path):
        """Test JSON export has complete and correct structure."""
        (tmp_path / "app.py").write_text("""
import numpy
import pandas

try:
    import ujson
except ImportError:
    pass
""")

        from pyimport2pkg.scanner import scan_project
        from pyimport2pkg.parser import Parser
        from pyimport2pkg.filter import Filter
        from pyimport2pkg.mapper import Mapper
        from pyimport2pkg.resolver import Resolver
        from pyimport2pkg.exporter import Exporter

        files = scan_project(tmp_path)
        parser = Parser()
        imports = parser.parse_file(files[0])

        filter_ = Filter()
        third_party, _ = filter_.filter_imports(imports)

        mapper = Mapper()
        results = mapper.map_imports(third_party)

        resolver = Resolver()
        results = resolver.resolve_all(results)

        required = [r for r in results if not r.import_info.is_optional]
        optional = [r for r in results if r.import_info.is_optional]

        exporter = Exporter()
        content = exporter.export_json(required, optional)
        data = json.loads(content)

        # Check structure
        assert data["meta"]["tool"] == "pyimport2pkg"
        assert data["meta"]["version"] == "0.2.0"
        assert "generated_at" in data["meta"]

        # Check required packages
        required_packages = {r["package"] for r in data["required"]}
        assert "numpy" in required_packages
        assert "pandas" in required_packages

        # Check optional packages
        if data["optional"]:
            optional_packages = {r["package"] for r in data["optional"]}
            assert "ujson" in optional_packages

    def test_requirements_sections_order(self, tmp_path: Path):
        """Test that requirements.txt sections are in correct order."""
        (tmp_path / "app.py").write_text("""
import numpy

if sys.platform == "win32":
    import pywin32

try:
    import ujson
except ImportError:
    pass
""")

        from pyimport2pkg.scanner import scan_project
        from pyimport2pkg.parser import Parser
        from pyimport2pkg.filter import Filter
        from pyimport2pkg.mapper import Mapper
        from pyimport2pkg.resolver import Resolver
        from pyimport2pkg.exporter import Exporter

        files = scan_project(tmp_path)
        parser = Parser()
        imports = parser.parse_file(files[0])

        filter_ = Filter()
        third_party, _ = filter_.filter_imports(imports)

        mapper = Mapper()
        results = mapper.map_imports(third_party)

        resolver = Resolver()
        results = resolver.resolve_all(results)

        from pyimport2pkg.models import ImportContext
        required = [r for r in results if not r.import_info.is_optional]
        conditional = [r for r in results if r.import_info.context == ImportContext.CONDITIONAL]
        try_except = [r for r in results if r.import_info.context == ImportContext.TRY_EXCEPT]

        exporter = Exporter(include_optional=True, include_comments=True)
        content = exporter.export_requirements_txt(required, conditional + try_except)

        # Verify section order: Required -> Conditional -> Try-except
        req_pos = content.find("# === Required")
        if req_pos >= 0:
            # If we have conditional or try-except sections, they should come after required
            cond_pos = content.find("# === Conditional")
            try_pos = content.find("# === Try-except")

            if cond_pos >= 0 and try_pos >= 0:
                assert req_pos < cond_pos < try_pos
            elif cond_pos >= 0:
                assert req_pos < cond_pos
            elif try_pos >= 0:
                assert req_pos < try_pos

    def test_python_version_auto_detection_integration(self, tmp_path: Path, capsys):
        """Test that Python version is auto-detected during analyze."""
        # Create .python-version file
        (tmp_path / ".python-version").write_text("3.8\n")
        (tmp_path / "app.py").write_text("import zoneinfo")

        result = main(["analyze", str(tmp_path), "-f", "simple"])
        assert result == 0

        captured = capsys.readouterr()
        # zoneinfo is not stdlib in 3.8, should be in output
        # (as a backport suggestion)
        # The stderr should show detected version
        assert "3.8" in captured.err


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_project(self, tmp_path: Path, capsys):
        """Test analyzing an empty project."""
        result = main(["analyze", str(tmp_path)])

        assert result == 0
        captured = capsys.readouterr()
        assert "No Python files found" in captured.err

    def test_single_file_analysis(self, tmp_path: Path, capsys):
        """Test analyzing a single file directly."""
        test_file = tmp_path / "single.py"
        test_file.write_text("import numpy\nimport pandas")

        result = main(["analyze", str(test_file), "-f", "simple"])

        assert result == 0
        captured = capsys.readouterr()
        assert "numpy" in captured.out
        assert "pandas" in captured.out

    def test_syntax_error_file(self, tmp_path: Path, capsys):
        """Test handling of files with syntax errors."""
        (tmp_path / "broken.py").write_text("import numpy\ndef foo(\n")
        (tmp_path / "good.py").write_text("import pandas")

        result = main(["analyze", str(tmp_path), "-f", "simple"])

        # Should still succeed
        assert result == 0
        captured = capsys.readouterr()
        # Should have pandas from good.py
        assert "pandas" in captured.out

    def test_no_third_party_imports(self, tmp_path: Path, capsys):
        """Test project with only stdlib imports."""
        (tmp_path / "stdlib_only.py").write_text("""
import os
import sys
import json
from pathlib import Path
""")

        result = main(["analyze", str(tmp_path), "-f", "simple"])

        assert result == 0
        captured = capsys.readouterr()
        # Output should be empty or minimal
        lines = [l for l in captured.out.strip().split("\n") if l and not l.startswith("#")]
        assert len(lines) == 0

    def test_relative_imports_only(self, tmp_path: Path, capsys):
        """Test project with only relative imports."""
        (tmp_path / "pkg").mkdir()
        (tmp_path / "pkg" / "__init__.py").write_text("")
        (tmp_path / "pkg" / "main.py").write_text("""
from . import utils
from .helpers import foo
from ..other import bar
""")

        result = main(["analyze", str(tmp_path), "-f", "simple"])

        assert result == 0
        captured = capsys.readouterr()
        # All relative imports should be filtered
        lines = [l for l in captured.out.strip().split("\n") if l and not l.startswith("#")]
        assert len(lines) == 0
