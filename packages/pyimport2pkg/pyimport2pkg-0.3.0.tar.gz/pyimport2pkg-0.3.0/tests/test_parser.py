"""Tests for the Parser module."""

import pytest
from pathlib import Path

from pyimport2pkg.parser import Parser, parse_source, parse_file
from pyimport2pkg.models import ImportType, ImportContext


class TestParserBasicImports:
    """Test basic import statement parsing."""

    def test_simple_import(self):
        """Test: import os"""
        source = "import os"
        result = parse_source(source)

        assert len(result) == 1
        assert result[0].module_name == "os"
        assert result[0].top_level == "os"
        assert result[0].sub_modules == []
        assert result[0].import_type == ImportType.STANDARD

    def test_import_with_alias(self):
        """Test: import numpy as np"""
        source = "import numpy as np"
        result = parse_source(source)

        assert len(result) == 1
        assert result[0].module_name == "numpy"
        assert result[0].top_level == "numpy"

    def test_multi_import(self):
        """Test: import os, sys, json"""
        source = "import os, sys, json"
        result = parse_source(source)

        assert len(result) == 3
        names = {r.module_name for r in result}
        assert names == {"os", "sys", "json"}

    def test_dotted_import(self):
        """Test: import os.path"""
        source = "import os.path"
        result = parse_source(source)

        assert len(result) == 1
        assert result[0].module_name == "os.path"
        assert result[0].top_level == "os"
        assert result[0].sub_modules == ["path"]

    def test_deeply_nested_import(self):
        """Test: import google.cloud.storage.blob"""
        source = "import google.cloud.storage.blob"
        result = parse_source(source)

        assert len(result) == 1
        assert result[0].module_name == "google.cloud.storage.blob"
        assert result[0].top_level == "google"
        assert result[0].sub_modules == ["cloud", "storage", "blob"]


class TestParserFromImports:
    """Test from...import statement parsing."""

    def test_from_import(self):
        """Test: from os import path"""
        source = "from os import path"
        result = parse_source(source)

        assert len(result) == 1
        assert result[0].module_name == "os"
        assert result[0].top_level == "os"
        assert result[0].import_type == ImportType.FROM

    def test_from_import_multiple(self):
        """Test: from os import path, getcwd, listdir"""
        source = "from os import path, getcwd, listdir"
        result = parse_source(source)

        # Should only record the module, not the imported names
        assert len(result) == 1
        assert result[0].module_name == "os"

    def test_from_dotted_import(self):
        """Test: from google.cloud import storage"""
        source = "from google.cloud import storage"
        result = parse_source(source)

        assert len(result) == 1
        assert result[0].module_name == "google.cloud"
        assert result[0].top_level == "google"
        assert result[0].sub_modules == ["cloud"]

    def test_from_import_star(self):
        """Test: from os import *"""
        source = "from os import *"
        result = parse_source(source)

        assert len(result) == 1
        assert result[0].module_name == "os"


class TestParserRelativeImports:
    """Test relative import detection."""

    def test_relative_import_dot(self):
        """Test: from . import utils"""
        source = "from . import utils"
        result = parse_source(source)

        assert len(result) == 1
        assert result[0].is_relative is True

    def test_relative_import_dotdot(self):
        """Test: from .. import parent"""
        source = "from .. import parent"
        result = parse_source(source)

        assert len(result) == 1
        assert result[0].is_relative is True

    def test_relative_import_with_module(self):
        """Test: from .utils import helper"""
        source = "from .utils import helper"
        result = parse_source(source)

        assert len(result) == 1
        assert result[0].is_relative is True
        assert result[0].module_name == "utils"

    def test_absolute_import_not_relative(self):
        """Test that absolute imports are not marked as relative."""
        source = "from os import path"
        result = parse_source(source)

        assert len(result) == 1
        assert result[0].is_relative is False


class TestParserContextDetection:
    """Test import context detection."""

    def test_top_level_context(self):
        """Test top-level imports."""
        source = """
import os
import sys
"""
        result = parse_source(source)

        for r in result:
            assert r.context == ImportContext.TOP_LEVEL
            assert r.is_optional is False

    def test_conditional_import(self):
        """Test imports inside if blocks."""
        source = """
if True:
    import optional_module
"""
        result = parse_source(source)

        assert len(result) == 1
        assert result[0].context == ImportContext.CONDITIONAL
        assert result[0].is_optional is True

    def test_try_except_import(self):
        """Test imports inside try-except blocks."""
        source = """
try:
    import ujson as json
except ImportError:
    import json
"""
        result = parse_source(source)

        assert len(result) == 2
        for r in result:
            assert r.context == ImportContext.TRY_EXCEPT
            assert r.is_optional is True

    def test_function_import(self):
        """Test imports inside functions."""
        source = """
def foo():
    import lazy_module
    return lazy_module.do_something()
"""
        result = parse_source(source)

        assert len(result) == 1
        assert result[0].context == ImportContext.FUNCTION
        assert result[0].is_optional is False  # Function imports aren't optional

    def test_class_import(self):
        """Test imports inside class body."""
        source = """
class MyClass:
    import class_level_import
"""
        result = parse_source(source)

        assert len(result) == 1
        assert result[0].context == ImportContext.CLASS

    def test_nested_context(self):
        """Test nested contexts (function inside class)."""
        source = """
class MyClass:
    def method(self):
        import nested_import
"""
        result = parse_source(source)

        assert len(result) == 1
        # Should be FUNCTION context (innermost)
        assert result[0].context == ImportContext.FUNCTION


class TestParserDynamicImports:
    """Test dynamic import detection."""

    def test_importlib_import_module_literal(self):
        """Test: importlib.import_module('numpy')"""
        source = """
import importlib
mod = importlib.import_module('numpy')
"""
        result = parse_source(source)

        # Should find both the static import and the dynamic one
        assert len(result) == 2

        dynamic = [r for r in result if r.is_dynamic]
        assert len(dynamic) == 1
        assert dynamic[0].module_name == "numpy"
        assert dynamic[0].import_type == ImportType.DYNAMIC

    def test_importlib_import_module_variable(self):
        """Test: importlib.import_module(variable)"""
        source = """
import importlib
name = "numpy"
mod = importlib.import_module(name)
"""
        result = parse_source(source)

        dynamic = [r for r in result if r.is_dynamic]
        assert len(dynamic) == 1
        assert dynamic[0].module_name == "<dynamic>"
        assert len(dynamic[0].warnings) > 0

    def test_dunder_import(self):
        """Test: __import__('numpy')"""
        source = """
mod = __import__('numpy')
"""
        result = parse_source(source)

        assert len(result) == 1
        assert result[0].is_dynamic is True
        assert result[0].module_name == "numpy"


class TestParserLineInfo:
    """Test line number and statement tracking."""

    def test_line_numbers(self):
        """Test that line numbers are correctly recorded."""
        source = """import os

import sys

import json
"""
        result = parse_source(source)

        assert len(result) == 3
        # Line 1 is import os, line 3 is import sys, line 5 is import json
        lines = sorted(r.line_number for r in result)
        assert lines == [1, 3, 5]

    def test_import_statement_text(self):
        """Test that the original statement is captured."""
        source = "import numpy as np"
        result = parse_source(source)

        assert result[0].import_statement == "import numpy as np"


class TestParserErrorHandling:
    """Test error handling."""

    def test_syntax_error(self):
        """Test handling of syntax errors."""
        source = "import os\nthis is not valid python"
        result = parse_source(source)

        # Should return an error marker
        assert len(result) == 1
        assert result[0].module_name == "<syntax_error>"
        assert len(result[0].warnings) > 0

    def test_empty_source(self):
        """Test handling of empty source."""
        source = ""
        result = parse_source(source)

        assert len(result) == 0

    def test_no_imports(self):
        """Test source with no imports."""
        source = """
def foo():
    return 42

print(foo())
"""
        result = parse_source(source)

        assert len(result) == 0


class TestParserFile:
    """Test file parsing."""

    def test_parse_file(self, tmp_path: Path):
        """Test parsing a file."""
        py_file = tmp_path / "test.py"
        py_file.write_text("import os\nimport sys")

        result = parse_file(py_file)

        assert len(result) == 2
        assert all(r.file_path == py_file for r in result)

    def test_parse_nonexistent_file(self, tmp_path: Path):
        """Test parsing a non-existent file."""
        result = parse_file(tmp_path / "nonexistent.py")

        assert len(result) == 1
        assert result[0].module_name == "<read_error>"


class TestParserSampleProject:
    """Test parsing the sample project."""

    def test_parse_sample_main(self, sample_project_dir: Path):
        """Test parsing sample_project/main.py."""
        main_file = sample_project_dir / "main.py"
        result = parse_file(main_file)

        # Check we found the expected imports
        modules = {r.module_name for r in result if not r.is_relative}
        assert "os" in modules
        assert "json" in modules
        assert "numpy" in modules
        assert "pandas" in modules
        assert "PIL" in modules

        # Check relative imports are detected
        relative = [r for r in result if r.is_relative]
        assert len(relative) == 2  # from . import and from .. import


class TestParserComplexCases:
    """Test complex and edge cases."""

    def test_mixed_imports(self):
        """Test file with various import types."""
        source = """
import os
import sys
from pathlib import Path
from typing import List, Dict

import numpy as np
from PIL import Image

try:
    import ujson as json
except ImportError:
    import json

if sys.platform == 'win32':
    import winreg

def lazy_load():
    import pandas as pd
    return pd

class DataProcessor:
    from dataclasses import dataclass
"""
        result = parse_source(source)

        # Count by context
        top_level = [r for r in result if r.context == ImportContext.TOP_LEVEL]
        try_except = [r for r in result if r.context == ImportContext.TRY_EXCEPT]
        conditional = [r for r in result if r.context == ImportContext.CONDITIONAL]
        function = [r for r in result if r.context == ImportContext.FUNCTION]
        class_level = [r for r in result if r.context == ImportContext.CLASS]

        assert len(top_level) >= 6  # os, sys, pathlib, typing, numpy, PIL
        assert len(try_except) == 2  # ujson and json
        assert len(conditional) == 1  # winreg
        assert len(function) == 1  # pandas
        assert len(class_level) == 1  # dataclasses

    def test_async_function_import(self):
        """Test import inside async function."""
        source = """
async def fetch_data():
    import aiohttp
    async with aiohttp.ClientSession() as session:
        pass
"""
        result = parse_source(source)

        assert len(result) == 1
        assert result[0].context == ImportContext.FUNCTION
        assert result[0].module_name == "aiohttp"
