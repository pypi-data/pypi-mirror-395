"""Tests for the Filter module - v0.2.0 comprehensive tests."""

import pytest
from pathlib import Path

from pyimport2pkg.filter import (
    Filter, filter_imports, get_stdlib_modules, detect_python_version, BACKPORTS
)
from pyimport2pkg.models import ImportInfo


class TestGetStdlibModules:
    """Test stdlib module detection."""

    def test_common_stdlib_modules(self):
        """Test that common stdlib modules are recognized."""
        stdlib = get_stdlib_modules()

        common_modules = ["os", "sys", "json", "pathlib", "typing", "collections",
                         "itertools", "functools", "re", "datetime", "math"]

        for mod in common_modules:
            assert mod in stdlib, f"{mod} should be in stdlib"

    def test_internal_modules(self):
        """Test that internal modules are included."""
        stdlib = get_stdlib_modules()

        assert "_thread" in stdlib
        assert "_collections" in stdlib or "collections" in stdlib

    def test_version_specific_311(self):
        """Test version-specific modules for 3.11."""
        stdlib_311 = get_stdlib_modules((3, 11))
        assert "tomllib" in stdlib_311

    def test_version_specific_39(self):
        """Test version-specific modules for 3.9."""
        stdlib_39 = get_stdlib_modules((3, 9))
        assert "zoneinfo" in stdlib_39
        assert "graphlib" in stdlib_39

    def test_old_version_lacks_new_modules(self):
        """Test that old Python versions don't have new modules."""
        stdlib_36 = get_stdlib_modules((3, 6))
        assert "dataclasses" not in stdlib_36
        assert "zoneinfo" not in stdlib_36
        assert "tomllib" not in stdlib_36


class TestDetectPythonVersion:
    """Test Python version auto-detection."""

    def test_detect_from_python_version_file(self, tmp_path: Path):
        """Test detection from .python-version file (pyenv)."""
        (tmp_path / ".python-version").write_text("3.8.10\n")

        version = detect_python_version(tmp_path)

        assert version == (3, 8)

    def test_detect_from_python_version_short(self, tmp_path: Path):
        """Test detection from .python-version with short format."""
        (tmp_path / ".python-version").write_text("3.9\n")

        version = detect_python_version(tmp_path)

        assert version == (3, 9)

    def test_detect_from_pyproject_toml(self, tmp_path: Path):
        """Test detection from pyproject.toml."""
        pyproject_content = '''
[project]
name = "myproject"
requires-python = ">=3.8"
'''
        (tmp_path / "pyproject.toml").write_text(pyproject_content)

        version = detect_python_version(tmp_path)

        assert version == (3, 8)

    def test_detect_from_pyproject_toml_exact(self, tmp_path: Path):
        """Test detection from pyproject.toml with exact version."""
        pyproject_content = '''
[project]
name = "myproject"
requires-python = "==3.10.*"
'''
        (tmp_path / "pyproject.toml").write_text(pyproject_content)

        version = detect_python_version(tmp_path)

        assert version == (3, 10)

    def test_detect_from_setup_cfg(self, tmp_path: Path):
        """Test detection from setup.cfg."""
        setup_content = '''
[options]
python_requires = >=3.7
'''
        (tmp_path / "setup.cfg").write_text(setup_content)

        version = detect_python_version(tmp_path)

        assert version == (3, 7)

    def test_detect_from_venv_pyvenv_cfg(self, tmp_path: Path):
        """Test detection from virtual environment's pyvenv.cfg."""
        venv_dir = tmp_path / ".venv"
        venv_dir.mkdir()
        pyvenv_cfg_content = '''
home = /usr/bin
version = 3.11.5
'''
        (venv_dir / "pyvenv.cfg").write_text(pyvenv_cfg_content)

        version = detect_python_version(tmp_path)

        assert version == (3, 11)

    def test_detect_priority_python_version_first(self, tmp_path: Path):
        """Test that .python-version takes priority over pyproject.toml."""
        (tmp_path / ".python-version").write_text("3.8\n")
        (tmp_path / "pyproject.toml").write_text('requires-python = ">=3.10"')

        version = detect_python_version(tmp_path)

        # .python-version should win
        assert version == (3, 8)

    def test_detect_returns_none_when_not_found(self, tmp_path: Path):
        """Test that detection returns None when no version info found."""
        version = detect_python_version(tmp_path)

        assert version is None

    def test_detect_handles_invalid_python_version_file(self, tmp_path: Path):
        """Test that detection handles invalid .python-version gracefully."""
        (tmp_path / ".python-version").write_text("invalid\n")

        version = detect_python_version(tmp_path)

        assert version is None


class TestFilterStdlib:
    """Test stdlib filtering."""

    def test_filters_stdlib(self):
        """Test that stdlib imports are filtered."""
        f = Filter()

        stdlib_imports = [
            ImportInfo.from_module_name("os"),
            ImportInfo.from_module_name("sys"),
            ImportInfo.from_module_name("json"),
            ImportInfo.from_module_name("pathlib"),
        ]

        third_party, filtered = f.filter_imports(stdlib_imports)

        assert len(third_party) == 0
        assert len(filtered) == 4

    def test_keeps_third_party(self):
        """Test that third-party imports are kept."""
        f = Filter()

        imports = [
            ImportInfo.from_module_name("numpy"),
            ImportInfo.from_module_name("pandas"),
            ImportInfo.from_module_name("requests"),
        ]

        third_party, filtered = f.filter_imports(imports)

        assert len(third_party) == 3
        assert len(filtered) == 0

        modules = {i.module_name for i in third_party}
        assert modules == {"numpy", "pandas", "requests"}

    def test_mixed_imports(self):
        """Test filtering mixed imports."""
        f = Filter()

        imports = [
            ImportInfo.from_module_name("os"),       # stdlib
            ImportInfo.from_module_name("numpy"),    # third-party
            ImportInfo.from_module_name("json"),     # stdlib
            ImportInfo.from_module_name("pandas"),   # third-party
        ]

        third_party, filtered = f.filter_imports(imports)

        assert len(third_party) == 2
        assert len(filtered) == 2

        third_party_names = {i.module_name for i in third_party}
        assert third_party_names == {"numpy", "pandas"}

    def test_stdlib_submodule(self):
        """Test that stdlib submodules are filtered."""
        f = Filter()

        imports = [
            ImportInfo.from_module_name("os.path"),
            ImportInfo.from_module_name("collections.abc"),
            ImportInfo.from_module_name("urllib.parse"),
        ]

        third_party, filtered = f.filter_imports(imports)

        assert len(third_party) == 0
        assert len(filtered) == 3


class TestFilterRelativeImports:
    """Test relative import filtering."""

    def test_filters_relative_imports(self):
        """Test that relative imports are filtered."""
        f = Filter()

        imports = [
            ImportInfo(module_name="utils", top_level="utils", is_relative=True),
            ImportInfo(module_name="", top_level="", is_relative=True),
        ]

        third_party, filtered = f.filter_imports(imports)

        assert len(third_party) == 0
        assert len(filtered) == 2


class TestFilterLocalModules:
    """Test local module filtering."""

    def test_filters_local_modules(self, tmp_path: Path):
        """Test that local project modules are filtered."""
        # Create a simple project structure
        (tmp_path / "mymodule.py").write_text("")
        (tmp_path / "mypackage").mkdir()
        (tmp_path / "mypackage" / "__init__.py").write_text("")

        f = Filter(project_root=tmp_path)

        imports = [
            ImportInfo.from_module_name("mymodule"),
            ImportInfo.from_module_name("mypackage"),
            ImportInfo.from_module_name("mypackage.submodule"),
            ImportInfo.from_module_name("numpy"),  # third-party
        ]

        third_party, filtered = f.filter_imports(imports)

        assert len(third_party) == 1
        assert third_party[0].module_name == "numpy"

    def test_no_project_root(self):
        """Test behavior when no project root is set."""
        f = Filter()

        imports = [
            ImportInfo.from_module_name("somemodule"),
        ]

        # Without project root, no local filtering happens
        third_party, filtered = f.filter_imports(imports)

        assert len(third_party) == 1

    def test_src_directory(self, tmp_path: Path):
        """Test that packages in src/ directory are detected."""
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "mylib").mkdir()
        (tmp_path / "src" / "mylib" / "__init__.py").write_text("")

        f = Filter(project_root=tmp_path)

        imports = [
            ImportInfo.from_module_name("mylib"),
            ImportInfo.from_module_name("mylib.utils"),
        ]

        third_party, filtered = f.filter_imports(imports)

        assert len(third_party) == 0
        assert len(filtered) == 2


class TestFilterErrorMarkers:
    """Test error marker filtering."""

    def test_filters_syntax_error_marker(self):
        """Test that syntax error markers are filtered."""
        f = Filter()

        imports = [
            ImportInfo(module_name="<syntax_error>", top_level="<syntax_error>"),
        ]

        third_party, filtered = f.filter_imports(imports)

        assert len(third_party) == 0
        assert len(filtered) == 1

    def test_filters_read_error_marker(self):
        """Test that read error markers are filtered."""
        f = Filter()

        imports = [
            ImportInfo(module_name="<read_error>", top_level="<read_error>"),
        ]

        third_party, filtered = f.filter_imports(imports)

        assert len(third_party) == 0
        assert len(filtered) == 1

    def test_filters_dynamic_import_marker(self):
        """Test that dynamic import markers are filtered."""
        f = Filter()

        imports = [
            ImportInfo(module_name="<dynamic>", top_level="<dynamic>"),
        ]

        third_party, filtered = f.filter_imports(imports)

        assert len(third_party) == 0
        assert len(filtered) == 1


class TestBackports:
    """Test backport detection."""

    def test_dataclasses_backport_python36(self):
        """Test dataclasses backport detection for Python 3.6."""
        f = Filter(python_version=(3, 6))

        imports = [ImportInfo.from_module_name("dataclasses")]
        third_party, _ = f.filter_imports(imports)

        assert len(third_party) == 1
        assert any("backport" in w.lower() or "dataclasses" in w for w in third_party[0].warnings)

    def test_dataclasses_stdlib_python37(self):
        """Test dataclasses is stdlib in Python 3.7+."""
        f = Filter(python_version=(3, 7))

        imports = [ImportInfo.from_module_name("dataclasses")]
        third_party, filtered = f.filter_imports(imports)

        assert len(third_party) == 0
        assert len(filtered) == 1

    def test_tomllib_backport_python310(self):
        """Test tomllib backport for Python < 3.11."""
        f = Filter(python_version=(3, 10))

        imports = [ImportInfo.from_module_name("tomllib")]
        third_party, _ = f.filter_imports(imports)

        assert len(third_party) == 1
        assert any("tomli" in w for w in third_party[0].warnings)

    def test_tomllib_stdlib_python311(self):
        """Test tomllib is stdlib in Python 3.11+."""
        f = Filter(python_version=(3, 11))

        imports = [ImportInfo.from_module_name("tomllib")]
        third_party, filtered = f.filter_imports(imports)

        assert len(third_party) == 0
        assert len(filtered) == 1

    def test_zoneinfo_backport_python38(self):
        """Test zoneinfo backport for Python < 3.9."""
        f = Filter(python_version=(3, 8))

        imports = [ImportInfo.from_module_name("zoneinfo")]
        third_party, _ = f.filter_imports(imports)

        assert len(third_party) == 1
        assert any("backport" in w.lower() or "zoneinfo" in w for w in third_party[0].warnings)

    def test_zoneinfo_stdlib_python39(self):
        """Test zoneinfo is stdlib in Python 3.9+."""
        f = Filter(python_version=(3, 9))

        imports = [ImportInfo.from_module_name("zoneinfo")]
        third_party, filtered = f.filter_imports(imports)

        assert len(third_party) == 0
        assert len(filtered) == 1

    def test_backports_data_structure(self):
        """Test BACKPORTS has correct structure."""
        for module_name, info in BACKPORTS.items():
            assert "min_version" in info, f"{module_name} missing min_version"
            assert "package" in info, f"{module_name} missing package"
            assert isinstance(info["min_version"], tuple), f"{module_name} min_version should be tuple"
            assert len(info["min_version"]) == 2, f"{module_name} min_version should have 2 elements"


class TestFilterConvenience:
    """Test convenience function."""

    def test_filter_imports_function(self):
        """Test the filter_imports convenience function."""
        imports = [
            ImportInfo.from_module_name("os"),
            ImportInfo.from_module_name("numpy"),
        ]

        result = filter_imports(imports)

        assert len(result) == 1
        assert result[0].module_name == "numpy"


class TestFilterMethods:
    """Test individual filter methods."""

    def test_is_stdlib(self):
        """Test is_stdlib method."""
        f = Filter()

        assert f.is_stdlib("os") is True
        assert f.is_stdlib("os.path") is True
        assert f.is_stdlib("numpy") is False
        assert f.is_stdlib("pandas") is False

    def test_is_local_module(self, tmp_path: Path):
        """Test is_local_module method."""
        (tmp_path / "mymodule.py").write_text("")

        f = Filter(project_root=tmp_path)

        assert f.is_local_module("mymodule") is True
        assert f.is_local_module("mymodule.sub") is True
        assert f.is_local_module("othermodule") is False

    def test_should_filter(self):
        """Test should_filter method."""
        f = Filter()

        # Should filter stdlib
        assert f.should_filter(ImportInfo.from_module_name("os")) is True

        # Should filter relative
        assert f.should_filter(ImportInfo(
            module_name="utils", top_level="utils", is_relative=True
        )) is True

        # Should filter errors
        assert f.should_filter(ImportInfo(
            module_name="<error>", top_level="<error>"
        )) is True

        # Should not filter third-party
        assert f.should_filter(ImportInfo.from_module_name("numpy")) is False

    def test_needs_backport(self):
        """Test needs_backport method."""
        # Old Python needs backport
        f_old = Filter(python_version=(3, 6))
        assert f_old.needs_backport("dataclasses") == "dataclasses"

        # New Python doesn't need backport
        f_new = Filter(python_version=(3, 11))
        assert f_new.needs_backport("dataclasses") is None


class TestFilterWithAutoDetection:
    """Test filter with Python version auto-detection."""

    def test_filter_uses_detected_version(self, tmp_path: Path):
        """Test that filter can use auto-detected version."""
        (tmp_path / ".python-version").write_text("3.8\n")

        detected = detect_python_version(tmp_path)
        f = Filter(project_root=tmp_path, python_version=detected)

        # zoneinfo is not stdlib in 3.8
        imports = [ImportInfo.from_module_name("zoneinfo")]
        third_party, _ = f.filter_imports(imports)

        assert len(third_party) == 1  # Needs backport warning

    def test_filter_explicit_version_overrides(self, tmp_path: Path):
        """Test that explicit version overrides detection."""
        (tmp_path / ".python-version").write_text("3.8\n")

        # Use explicit version 3.11 instead of detected 3.8
        f = Filter(project_root=tmp_path, python_version=(3, 11))

        # zoneinfo is stdlib in 3.11
        imports = [ImportInfo.from_module_name("zoneinfo")]
        third_party, filtered = f.filter_imports(imports)

        assert len(third_party) == 0
        assert len(filtered) == 1

