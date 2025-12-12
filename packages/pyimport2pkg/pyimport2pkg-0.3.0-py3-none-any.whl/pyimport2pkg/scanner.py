"""
Scanner module: Scans project directories and collects Python files.

Handles directory traversal with configurable exclusion rules.
"""

from pathlib import Path
from typing import Iterator


# Default directories to exclude
DEFAULT_EXCLUDE_DIRS: set[str] = {
    # Virtual environments
    ".venv", "venv", "env", ".env", "virtualenv",
    # Version control
    ".git", ".svn", ".hg", ".bzr",
    # Cache directories
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    ".hypothesis", ".tox", ".nox",
    # Build artifacts
    "build", "dist", "eggs", "*.egg-info",
    ".eggs", "sdist", "wheels",
    # IDE and editor
    ".idea", ".vscode", ".vs",
    # Node.js (for mixed projects)
    "node_modules",
    # Site packages
    "site-packages", "lib", "lib64",
}

# Default file patterns to exclude
DEFAULT_EXCLUDE_FILES: set[str] = {
    "setup.py",  # Often contains meta-dependencies
}


class Scanner:
    """
    Scans directories for Python files.

    Args:
        exclude_dirs: Additional directory names to exclude
        exclude_files: Additional file names to exclude
        include_hidden: Whether to include hidden files/directories
    """

    def __init__(
        self,
        exclude_dirs: set[str] | None = None,
        exclude_files: set[str] | None = None,
        include_hidden: bool = False,
    ):
        self.exclude_dirs = DEFAULT_EXCLUDE_DIRS.copy()
        if exclude_dirs:
            self.exclude_dirs.update(exclude_dirs)

        self.exclude_files = DEFAULT_EXCLUDE_FILES.copy()
        if exclude_files:
            self.exclude_files.update(exclude_files)

        self.include_hidden = include_hidden

    def _should_exclude_dir(self, dir_path: Path) -> bool:
        """Check if a directory should be excluded."""
        name = dir_path.name

        # Check if hidden (starts with .)
        if not self.include_hidden and name.startswith("."):
            return True

        # Check against exclude patterns
        if name in self.exclude_dirs:
            return True

        # Check for .egg-info suffix
        if name.endswith(".egg-info"):
            return True

        return False

    def _should_exclude_file(self, file_path: Path) -> bool:
        """Check if a file should be excluded."""
        name = file_path.name

        # Check if hidden
        if not self.include_hidden and name.startswith("."):
            return True

        # Check against exclude patterns
        if name in self.exclude_files:
            return True

        return False

    def _is_python_file(self, file_path: Path) -> bool:
        """Check if a file is a Python file."""
        return file_path.suffix == ".py"

    def scan_directory(self, root: Path) -> Iterator[Path]:
        """
        Recursively scan a directory for Python files.

        Args:
            root: The root directory to scan

        Yields:
            Paths to Python files found
        """
        root = Path(root).resolve()

        if not root.exists():
            return

        if not root.is_dir():
            # Single file provided
            if self._is_python_file(root) and not self._should_exclude_file(root):
                yield root
            return

        # Use a stack for iterative traversal (avoids recursion limits)
        dirs_to_process = [root]

        while dirs_to_process:
            current_dir = dirs_to_process.pop()

            try:
                entries = list(current_dir.iterdir())
            except PermissionError:
                continue

            # Sort for consistent ordering
            entries.sort(key=lambda x: x.name)

            for entry in entries:
                if entry.is_dir():
                    if not self._should_exclude_dir(entry):
                        dirs_to_process.append(entry)
                elif entry.is_file():
                    if self._is_python_file(entry) and not self._should_exclude_file(entry):
                        yield entry

    def scan(self, path: Path | str) -> list[Path]:
        """
        Scan a path (file or directory) for Python files.

        Args:
            path: Path to scan (file or directory)

        Returns:
            List of paths to Python files
        """
        return list(self.scan_directory(Path(path)))


def scan_project(
    path: Path | str,
    exclude_dirs: set[str] | None = None,
    exclude_files: set[str] | None = None,
    include_hidden: bool = False,
) -> list[Path]:
    """
    Convenience function to scan a project for Python files.

    Args:
        path: Path to scan
        exclude_dirs: Additional directories to exclude
        exclude_files: Additional files to exclude
        include_hidden: Whether to include hidden files

    Returns:
        List of Python file paths
    """
    scanner = Scanner(
        exclude_dirs=exclude_dirs,
        exclude_files=exclude_files,
        include_hidden=include_hidden,
    )
    return scanner.scan(path)
