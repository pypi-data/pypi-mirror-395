"""
Mapper module: Maps import module names to pip package names.

Uses multiple data sources in priority order:
1. Hardcoded mappings (highest priority)
2. Namespace package mappings
3. Database lookup (if available)
4. Direct mapping guess (module name == package name)
"""

from pathlib import Path
from typing import Protocol, runtime_checkable

from .models import ImportInfo, PackageCandidate, MappingResult
from .mappings import (
    get_hardcoded_mapping,
    resolve_namespace_package,
    is_namespace_package,
)


@runtime_checkable
class DatabaseProtocol(Protocol):
    """Protocol for database lookup."""

    def lookup(self, module_name: str) -> list[tuple[str, int]] | None:
        """
        Look up a module name in the database.

        Args:
            module_name: The top-level module name

        Returns:
            List of (package_name, download_count) tuples, or None if not found
        """
        ...


class Mapper:
    """
    Maps import module names to pip package names.

    Uses multiple data sources in priority order.
    """

    def __init__(self, database: DatabaseProtocol | None = None):
        """
        Initialize the mapper.

        Args:
            database: Optional database for additional lookups
        """
        self.database = database

    def _create_candidates(
        self,
        package_names: list[str],
        source: str,
    ) -> list[PackageCandidate]:
        """Create PackageCandidate objects from package names."""
        candidates = []
        for i, name in enumerate(package_names):
            candidates.append(PackageCandidate(
                package_name=name,
                is_recommended=(i == 0),  # First one is recommended
            ))
        return candidates

    def map_import(self, import_info: ImportInfo) -> MappingResult:
        """
        Map a single import to its package name(s).

        Args:
            import_info: The import information

        Returns:
            MappingResult with candidates and resolution status
        """
        result = MappingResult(import_info=import_info)
        top_level = import_info.top_level
        sub_modules = import_info.sub_modules

        # 1. Check namespace packages FIRST if there are submodules
        # This takes priority because namespace packages like google.cloud.*
        # have specific package mappings that shouldn't be overridden
        if sub_modules and is_namespace_package(import_info.module_name):
            namespace_result = resolve_namespace_package(top_level, sub_modules)
            if namespace_result:
                result.candidates = self._create_candidates(namespace_result, "namespace")
                result.source = "namespace"
                result.resolved_package = namespace_result[0]
                result.is_resolved = True
                return result

        # 2. Check hardcoded mappings (for non-namespace or top-level only imports)
        hardcoded = get_hardcoded_mapping(top_level)
        if hardcoded:
            result.candidates = self._create_candidates(hardcoded, "hardcoded")
            result.source = "hardcoded"
            result.resolved_package = hardcoded[0]
            result.is_resolved = True
            return result

        # 3. Check namespace packages for top-level only imports
        # (e.g., just "import google" without submodules)
        if is_namespace_package(import_info.module_name):
            namespace_result = resolve_namespace_package(top_level, sub_modules)
            if namespace_result:
                result.candidates = self._create_candidates(namespace_result, "namespace")
                result.source = "namespace"
                result.resolved_package = namespace_result[0]
                result.is_resolved = True
                return result

        # 3. Check database if available
        if self.database is not None:
            db_result = self.database.lookup(top_level)
            if db_result:
                # db_result is list of (package_name, download_count)
                candidates = []
                for pkg_name, downloads in db_result:
                    candidates.append(PackageCandidate(
                        package_name=pkg_name,
                        download_count=downloads,
                        is_recommended=(len(candidates) == 0),
                    ))
                result.candidates = candidates
                result.source = "database"
                result.resolved_package = candidates[0].package_name
                result.is_resolved = True
                return result

        # 4. Guess: assume module name equals package name
        # This is a fallback and may not always be correct
        result.candidates = [PackageCandidate(
            package_name=top_level,
            is_recommended=True,
            note="Guessed: module name assumed to equal package name",
        )]
        result.source = "guessed"
        result.resolved_package = top_level
        result.is_resolved = True
        import_info.warnings.append(
            f"Package name '{top_level}' was guessed. Please verify it's correct."
        )

        return result

    def map_imports(self, imports: list[ImportInfo]) -> list[MappingResult]:
        """
        Map multiple imports to their package names.

        Args:
            imports: List of ImportInfo objects

        Returns:
            List of MappingResult objects
        """
        return [self.map_import(imp) for imp in imports]


def map_imports(
    imports: list[ImportInfo],
    database: DatabaseProtocol | None = None,
) -> list[MappingResult]:
    """
    Convenience function to map imports to packages.

    Args:
        imports: List of ImportInfo objects
        database: Optional database for additional lookups

    Returns:
        List of MappingResult objects
    """
    mapper = Mapper(database=database)
    return mapper.map_imports(imports)
