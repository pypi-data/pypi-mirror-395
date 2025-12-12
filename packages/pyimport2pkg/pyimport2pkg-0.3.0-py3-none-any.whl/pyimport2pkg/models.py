"""
Core data models for pyimport2pkg.

Defines the data structures used throughout the application.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path


class ImportType(Enum):
    """Type of import statement."""
    STANDARD = auto()      # import xxx
    FROM = auto()          # from xxx import yyy
    DYNAMIC = auto()       # importlib.import_module('xxx')


class ImportContext(Enum):
    """Context in which the import appears."""
    TOP_LEVEL = auto()     # Module level import
    CONDITIONAL = auto()   # Inside if/elif/else block
    TRY_EXCEPT = auto()    # Inside try/except block
    FUNCTION = auto()      # Inside function/method
    CLASS = auto()         # Inside class body


@dataclass
class ImportInfo:
    """
    Complete information about a single import statement.

    Attributes:
        module_name: Full module path, e.g., "google.cloud.storage"
        top_level: Top-level module name, e.g., "google"
        sub_modules: List of submodule names, e.g., ["cloud", "storage"]
        file_path: Path to the source file
        line_number: Line number in the source file
        import_statement: Original import statement text
        import_type: Type of import (STANDARD, FROM, DYNAMIC)
        context: Context where import appears
        is_optional: Whether this is an optional import (try-except, conditional)
        is_relative: Whether this is a relative import
        is_dynamic: Whether this is a dynamic import
        warnings: List of warning messages
    """
    module_name: str
    top_level: str
    sub_modules: list[str] = field(default_factory=list)

    file_path: Path | None = None
    line_number: int = 0
    import_statement: str = ""

    import_type: ImportType = ImportType.STANDARD
    context: ImportContext = ImportContext.TOP_LEVEL

    is_optional: bool = False
    is_relative: bool = False
    is_dynamic: bool = False

    warnings: list[str] = field(default_factory=list)

    @classmethod
    def from_module_name(cls, module_name: str, **kwargs) -> "ImportInfo":
        """Create ImportInfo from a module name string."""
        parts = module_name.split(".")
        return cls(
            module_name=module_name,
            top_level=parts[0],
            sub_modules=parts[1:] if len(parts) > 1 else [],
            **kwargs
        )


@dataclass
class PackageCandidate:
    """
    A candidate pip package for an import.

    Attributes:
        package_name: The pip package name
        download_count: Monthly download count (for popularity ranking)
        is_recommended: Whether this is the recommended choice
        note: Additional information about this candidate
    """
    package_name: str
    download_count: int = 0
    is_recommended: bool = False
    note: str = ""


@dataclass
class MappingResult:
    """
    Result of mapping an import to package(s).

    Attributes:
        import_info: The original import information
        candidates: List of candidate packages
        resolved_package: The final resolved package name (after conflict resolution)
        source: Where the mapping came from (hardcoded, database, guessed)
        is_resolved: Whether a package was successfully resolved
    """
    import_info: ImportInfo
    candidates: list[PackageCandidate] = field(default_factory=list)
    resolved_package: str | None = None
    source: str = "unknown"  # "hardcoded", "namespace", "database", "guessed"
    is_resolved: bool = False

    def resolve(self, package_name: str) -> None:
        """Mark this mapping as resolved with the given package."""
        self.resolved_package = package_name
        self.is_resolved = True


@dataclass
class AnalysisResult:
    """
    Complete result of analyzing a project or file.

    Attributes:
        required_packages: Packages that must be installed
        optional_packages: Packages from conditional/try-except imports
        unresolved_imports: Imports that couldn't be mapped
        warnings: General warnings from the analysis
        stats: Statistics about the analysis
    """
    required_packages: list[MappingResult] = field(default_factory=list)
    optional_packages: list[MappingResult] = field(default_factory=list)
    unresolved_imports: list[ImportInfo] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    stats: dict = field(default_factory=dict)

    def add_required(self, result: MappingResult) -> None:
        """Add a required package mapping."""
        self.required_packages.append(result)

    def add_optional(self, result: MappingResult) -> None:
        """Add an optional package mapping."""
        self.optional_packages.append(result)

    def add_unresolved(self, import_info: ImportInfo) -> None:
        """Add an unresolved import."""
        self.unresolved_imports.append(import_info)

    def get_unique_packages(self) -> set[str]:
        """Get all unique resolved package names."""
        packages = set()
        for result in self.required_packages + self.optional_packages:
            if result.resolved_package:
                packages.add(result.resolved_package)
        return packages
