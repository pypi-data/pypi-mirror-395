"""
Filter module: Filters out standard library and local modules.

Identifies which imports are from the standard library, local project modules,
or third-party packages that need to be installed.
"""

import sys
import re
from pathlib import Path
from typing import Iterator

from .models import ImportInfo


# Python 3.10+ has sys.stdlib_module_names
# For earlier versions, we maintain a list
STDLIB_MODULES_FALLBACK: set[str] = {
    # Core modules (always present)
    "__future__", "__main__", "_thread", "abc", "aifc", "argparse", "array",
    "ast", "asynchat", "asyncio", "asyncore", "atexit", "audioop", "base64",
    "bdb", "binascii", "binhex", "bisect", "builtins", "bz2", "calendar",
    "cgi", "cgitb", "chunk", "cmath", "cmd", "code", "codecs", "codeop",
    "collections", "colorsys", "compileall", "concurrent", "configparser",
    "contextlib", "contextvars", "copy", "copyreg", "cProfile", "crypt",
    "csv", "ctypes", "curses", "dataclasses", "datetime", "dbm", "decimal",
    "difflib", "dis", "distutils", "doctest", "email", "encodings", "enum",
    "errno", "faulthandler", "fcntl", "filecmp", "fileinput", "fnmatch",
    "fractions", "ftplib", "functools", "gc", "getopt", "getpass", "gettext",
    "glob", "graphlib", "grp", "gzip", "hashlib", "heapq", "hmac", "html",
    "http", "idlelib", "imaplib", "imghdr", "imp", "importlib", "inspect",
    "io", "ipaddress", "itertools", "json", "keyword", "lib2to3", "linecache",
    "locale", "logging", "lzma", "mailbox", "mailcap", "marshal", "math",
    "mimetypes", "mmap", "modulefinder", "multiprocessing", "netrc", "nis",
    "nntplib", "numbers", "operator", "optparse", "os", "ossaudiodev",
    "pathlib", "pdb", "pickle", "pickletools", "pipes", "pkgutil", "platform",
    "plistlib", "poplib", "posix", "posixpath", "pprint", "profile", "pstats",
    "pty", "pwd", "py_compile", "pyclbr", "pydoc", "queue", "quopri",
    "random", "re", "readline", "reprlib", "resource", "rlcompleter", "runpy",
    "sched", "secrets", "select", "selectors", "shelve", "shlex", "shutil",
    "signal", "site", "smtpd", "smtplib", "sndhdr", "socket", "socketserver",
    "spwd", "sqlite3", "ssl", "stat", "statistics", "string", "stringprep",
    "struct", "subprocess", "sunau", "symtable", "sys", "sysconfig", "syslog",
    "tabnanny", "tarfile", "telnetlib", "tempfile", "termios", "test",
    "textwrap", "threading", "time", "timeit", "tkinter", "token", "tokenize",
    "tomllib", "trace", "traceback", "tracemalloc", "tty", "turtle",
    "turtledemo", "types", "typing", "unicodedata", "unittest", "urllib",
    "uu", "uuid", "venv", "warnings", "wave", "weakref", "webbrowser",
    "winreg", "winsound", "wsgiref", "xdrlib", "xml", "xmlrpc", "zipapp",
    "zipfile", "zipimport", "zlib", "zoneinfo",
    # Internal modules (underscore prefix)
    "_abc", "_ast", "_bisect", "_blake2", "_bootlocale", "_bz2", "_codecs",
    "_codecs_cn", "_codecs_hk", "_codecs_iso2022", "_codecs_jp", "_codecs_kr",
    "_codecs_tw", "_collections", "_collections_abc", "_compat_pickle",
    "_compression", "_contextvars", "_crypt", "_csv", "_ctypes", "_curses",
    "_curses_panel", "_datetime", "_dbm", "_decimal", "_elementtree",
    "_frozen_importlib", "_frozen_importlib_external", "_functools", "_gdbm",
    "_hashlib", "_heapq", "_imp", "_io", "_json", "_locale", "_lsprof",
    "_lzma", "_markupbase", "_md5", "_msi", "_multibytecodec",
    "_multiprocessing", "_opcode", "_operator", "_osx_support", "_pickle",
    "_posixshmem", "_posixsubprocess", "_py_abc", "_pydecimal", "_pyio",
    "_queue", "_random", "_sha1", "_sha256", "_sha3", "_sha512", "_signal",
    "_sitebuiltins", "_socket", "_sqlite3", "_sre", "_ssl", "_stat",
    "_statistics", "_string", "_strptime", "_struct", "_symtable", "_thread",
    "_threading_local", "_tkinter", "_tracemalloc", "_uuid", "_warnings",
    "_weakref", "_weakrefset", "_winapi", "_xxsubinterpreters", "_xxtestfuzz",
    "_zoneinfo",
}

# Backports: modules that are in stdlib for newer Python versions
# but may need to be installed for older versions
BACKPORTS: dict[str, dict] = {
    # Core Python modules
    "dataclasses": {"min_version": (3, 7), "package": "dataclasses"},
    "typing": {"min_version": (3, 5), "package": "typing"},
    "enum": {"min_version": (3, 4), "package": "enum34"},
    "asyncio": {"min_version": (3, 4), "package": "asyncio"},
    "pathlib": {"min_version": (3, 4), "package": "pathlib2"},
    "functools": {"min_version": (3, 2), "package": "functools32"},
    "contextlib": {"min_version": (3, 2), "package": "contextlib2"},
    "importlib": {"min_version": (3, 1), "package": "importlib"},

    # Python 3.11+ modules
    "tomllib": {"min_version": (3, 11), "package": "tomli"},
    "exceptiongroup": {"min_version": (3, 11), "package": "exceptiongroup"},

    # Python 3.9+ modules
    "zoneinfo": {"min_version": (3, 9), "package": "backports.zoneinfo"},
    "graphlib": {"min_version": (3, 9), "package": "graphlib-backport"},

    # Python 3.8+ modules
    "importlib.metadata": {"min_version": (3, 8), "package": "importlib-metadata"},
    "importlib.resources": {"min_version": (3, 9), "package": "importlib-resources"},
    "typing_extensions": {"min_version": (3, 8), "package": "typing-extensions"},
    "cached_property": {"min_version": (3, 8), "package": "backports.cached-property"},

    # Python 3.7+ modules
    "contextvars": {"min_version": (3, 7), "package": "contextvars"},
}


def detect_python_version(project_root: Path) -> tuple[int, int] | None:
    """
    Auto-detect the target Python version for a project.

    Detection priority:
    1. .python-version file (pyenv)
    2. pyproject.toml requires-python
    3. setup.cfg python_requires
    4. Virtual environment's Python version
    5. Returns None if not detected (will use current Python version)

    Args:
        project_root: The project root directory

    Returns:
        Python version as (major, minor) tuple, or None if not detected
    """
    project_root = Path(project_root)

    # 1. Check .python-version (pyenv)
    pyenv_file = project_root / ".python-version"
    if pyenv_file.exists():
        try:
            version_str = pyenv_file.read_text().strip()
            # Parse "3.8.10" or "3.8" -> (3, 8)
            match = re.match(r"^(\d+)\.(\d+)", version_str)
            if match:
                return (int(match.group(1)), int(match.group(2)))
        except Exception:
            pass

    # 2. Check pyproject.toml
    pyproject = project_root / "pyproject.toml"
    if pyproject.exists():
        try:
            content = pyproject.read_text()
            # Look for requires-python = ">=3.8" or similar
            match = re.search(r'requires-python\s*=\s*["\']([^"\']+)["\']', content)
            if match:
                version_spec = match.group(1)
                # Extract version number from spec like ">=3.8", "~=3.9", "==3.10.*"
                version_match = re.search(r'(\d+)\.(\d+)', version_spec)
                if version_match:
                    return (int(version_match.group(1)), int(version_match.group(2)))
        except Exception:
            pass

    # 3. Check setup.cfg
    setup_cfg = project_root / "setup.cfg"
    if setup_cfg.exists():
        try:
            content = setup_cfg.read_text()
            match = re.search(r'python_requires\s*=\s*([^\n]+)', content)
            if match:
                version_spec = match.group(1).strip()
                version_match = re.search(r'(\d+)\.(\d+)', version_spec)
                if version_match:
                    return (int(version_match.group(1)), int(version_match.group(2)))
        except Exception:
            pass

    # 4. Check virtual environment's pyvenv.cfg
    for venv_dir in [".venv", "venv", "env", ".env"]:
        venv_path = project_root / venv_dir
        pyvenv_cfg = venv_path / "pyvenv.cfg"
        if pyvenv_cfg.exists():
            try:
                content = pyvenv_cfg.read_text()
                # Look for version = 3.10.5 or version_info = 3.10.5
                match = re.search(r'version\s*=\s*(\d+)\.(\d+)', content)
                if match:
                    return (int(match.group(1)), int(match.group(2)))
            except Exception:
                pass

    return None


def get_stdlib_modules(python_version: tuple[int, int] | None = None) -> set[str]:
    """
    Get the set of standard library module names.

    Args:
        python_version: Target Python version as (major, minor).
                       If None, uses the current Python version.

    Returns:
        Set of standard library module names
    """
    if python_version is None:
        python_version = (sys.version_info.major, sys.version_info.minor)

    # Python 3.10+ has sys.stdlib_module_names
    # Only use it if targeting the CURRENT Python version
    current_version = (sys.version_info.major, sys.version_info.minor)
    if (
        hasattr(sys, "stdlib_module_names")
        and python_version == current_version
    ):
        return set(sys.stdlib_module_names)

    # Use fallback list
    stdlib = STDLIB_MODULES_FALLBACK.copy()

    # Remove modules that don't exist in older Python versions
    # (they need to be installed as backports)
    if python_version < (3, 11):
        stdlib.discard("tomllib")
    if python_version < (3, 9):
        stdlib.discard("zoneinfo")
        stdlib.discard("graphlib")
    if python_version < (3, 7):
        stdlib.discard("dataclasses")
        stdlib.discard("contextvars")
    if python_version < (3, 6):
        stdlib.discard("secrets")
    if python_version < (3, 5):
        stdlib.discard("typing")
        stdlib.discard("zipapp")
    if python_version < (3, 4):
        stdlib.discard("asyncio")
        stdlib.discard("enum")
        stdlib.discard("pathlib")
        stdlib.discard("statistics")
        stdlib.discard("tracemalloc")

    # Add version-specific modules (for completeness when targeting newer versions)
    if python_version >= (3, 11):
        stdlib.add("tomllib")
    if python_version >= (3, 9):
        stdlib.add("zoneinfo")
        stdlib.add("graphlib")
    if python_version >= (3, 8):
        stdlib.add("importlib.metadata")

    # Remove deprecated/removed modules for newer versions
    if python_version >= (3, 12):
        stdlib.discard("distutils")
        stdlib.discard("asynchat")
        stdlib.discard("asyncore")
        stdlib.discard("smtpd")
    if python_version >= (3, 11):
        stdlib.discard("binhex")
    if python_version >= (3, 13):
        stdlib.discard("aifc")
        stdlib.discard("audioop")
        stdlib.discard("chunk")
        stdlib.discard("cgi")
        stdlib.discard("cgitb")
        stdlib.discard("crypt")
        stdlib.discard("imghdr")
        stdlib.discard("mailcap")
        stdlib.discard("msilib")
        stdlib.discard("nis")
        stdlib.discard("nntplib")
        stdlib.discard("ossaudiodev")
        stdlib.discard("pipes")
        stdlib.discard("sndhdr")
        stdlib.discard("spwd")
        stdlib.discard("sunau")
        stdlib.discard("telnetlib")
        stdlib.discard("uu")
        stdlib.discard("xdrlib")

    return stdlib


class Filter:
    """
    Filters imports to identify third-party packages.

    Removes standard library modules, relative imports, and local project modules.
    """

    def __init__(
        self,
        project_root: Path | None = None,
        python_version: tuple[int, int] | None = None,
    ):
        """
        Initialize the filter.

        Args:
            project_root: Root directory of the project (for local module detection)
            python_version: Target Python version as (major, minor)
        """
        self.project_root = Path(project_root) if project_root else None
        self.python_version = python_version or (
            sys.version_info.major,
            sys.version_info.minor,
        )
        self.stdlib_modules = get_stdlib_modules(self.python_version)

        # Collect local module names from project
        self.local_modules: set[str] = set()
        if self.project_root:
            self._scan_local_modules()

    def _scan_local_modules(self) -> None:
        """Scan project root to identify local module names."""
        if not self.project_root or not self.project_root.exists():
            return

        # Check for Python files and packages in root
        for item in self.project_root.iterdir():
            if item.is_file() and item.suffix == ".py":
                # Single module file (e.g., utils.py -> utils)
                self.local_modules.add(item.stem)
            elif item.is_dir():
                # Check if it's a Python package
                if (item / "__init__.py").exists():
                    self.local_modules.add(item.name)
                # Also check common source directories
                elif item.name in ("src", "lib", "source"):
                    self._scan_src_dir(item)

    def _scan_src_dir(self, src_dir: Path) -> None:
        """Scan a source directory for packages."""
        for item in src_dir.iterdir():
            if item.is_dir() and (item / "__init__.py").exists():
                self.local_modules.add(item.name)

    def is_stdlib(self, module_name: str) -> bool:
        """Check if a module is from the standard library."""
        top_level = module_name.split(".")[0]
        return top_level in self.stdlib_modules

    def is_local_module(self, module_name: str) -> bool:
        """Check if a module is a local project module."""
        top_level = module_name.split(".")[0]
        return top_level in self.local_modules

    def needs_backport(self, module_name: str) -> str | None:
        """
        Check if a module needs a backport package for the target Python version.

        Returns:
            The backport package name if needed, None otherwise.
        """
        top_level = module_name.split(".")[0]

        if top_level in BACKPORTS:
            backport_info = BACKPORTS[top_level]
            min_version = backport_info["min_version"]

            if self.python_version < min_version:
                return backport_info["package"]

        return None

    def should_filter(self, import_info: ImportInfo) -> bool:
        """
        Check if an import should be filtered out.

        Returns True if the import should be excluded (stdlib, relative, local).
        """
        # Filter relative imports
        if import_info.is_relative:
            return True

        # Filter error markers
        if import_info.module_name.startswith("<"):
            return True

        # Filter standard library
        if self.is_stdlib(import_info.module_name):
            return True

        # Filter local modules
        if self.is_local_module(import_info.module_name):
            return True

        return False

    def filter_imports(
        self,
        imports: list[ImportInfo],
    ) -> tuple[list[ImportInfo], list[ImportInfo]]:
        """
        Filter a list of imports.

        Args:
            imports: List of ImportInfo objects to filter

        Returns:
            Tuple of (third_party_imports, filtered_imports)
        """
        third_party = []
        filtered = []

        for imp in imports:
            if self.should_filter(imp):
                filtered.append(imp)
            else:
                # Check for backport
                backport = self.needs_backport(imp.module_name)
                if backport:
                    imp.warnings.append(
                        f"Module '{imp.module_name}' may need backport package "
                        f"'{backport}' for Python {self.python_version[0]}.{self.python_version[1]}"
                    )
                third_party.append(imp)

        return third_party, filtered


def filter_imports(
    imports: list[ImportInfo],
    project_root: Path | None = None,
    python_version: tuple[int, int] | None = None,
) -> list[ImportInfo]:
    """
    Convenience function to filter imports.

    Args:
        imports: List of ImportInfo objects
        project_root: Project root directory
        python_version: Target Python version

    Returns:
        List of third-party imports (stdlib and local filtered out)
    """
    f = Filter(project_root=project_root, python_version=python_version)
    third_party, _ = f.filter_imports(imports)
    return third_party
