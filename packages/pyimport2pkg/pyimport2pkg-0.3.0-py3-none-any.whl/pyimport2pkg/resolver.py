"""
Resolver module: Handles conflict resolution and final package selection.

When multiple package candidates are available for a module,
the resolver selects the best one based on various strategies.
"""

import platform
from enum import Enum, auto

from .models import MappingResult, PackageCandidate, AnalysisResult, ImportInfo
from .mappings.hardcoded import PLATFORM_SPECIFIC


class ResolveStrategy(Enum):
    """Strategy for resolving multiple candidates."""
    MOST_POPULAR = auto()  # Choose the most downloaded package
    FIRST = auto()         # Choose the first candidate (recommended)
    ALL = auto()           # Keep all candidates


class Resolver:
    """
    Resolves package conflicts and makes final selections.
    """

    def __init__(
        self,
        strategy: ResolveStrategy = ResolveStrategy.MOST_POPULAR,
        target_platform: str | None = None,
    ):
        """
        Initialize the resolver.

        Args:
            strategy: How to resolve multiple candidates
            target_platform: Target platform (default: current platform)
        """
        self.strategy = strategy
        self.target_platform = target_platform or self._get_platform()

    def _get_platform(self) -> str:
        """Get current platform identifier."""
        system = platform.system().lower()
        machine = platform.machine().lower()

        if system == "darwin":
            if "arm" in machine:
                return "darwin_arm64"
            return "darwin_x86_64"
        elif system == "linux":
            return "linux"
        elif system == "windows":
            return "win32"
        return "unknown"

    def _get_platform_recommendation(self, module_name: str) -> str | None:
        """Get platform-specific package recommendation."""
        if module_name not in PLATFORM_SPECIFIC:
            return None

        platform_map = PLATFORM_SPECIFIC[module_name]
        return platform_map.get(
            self.target_platform,
            platform_map.get("default")
        )

    def resolve(self, result: MappingResult) -> MappingResult:
        """
        Resolve a single mapping result.

        Args:
            result: The mapping result to resolve

        Returns:
            The resolved mapping result
        """
        if not result.candidates:
            return result

        # Check for platform-specific recommendation
        platform_rec = self._get_platform_recommendation(result.import_info.top_level)
        if platform_rec:
            # Find matching candidate or add it
            for candidate in result.candidates:
                if candidate.package_name == platform_rec:
                    result.resolved_package = platform_rec
                    candidate.is_recommended = True
                    candidate.note = f"Recommended for {self.target_platform}"
                    return result

        # Apply resolution strategy
        if self.strategy == ResolveStrategy.MOST_POPULAR:
            # Sort by download count and pick the highest
            sorted_candidates = sorted(
                result.candidates,
                key=lambda c: c.download_count,
                reverse=True,
            )
            result.resolved_package = sorted_candidates[0].package_name

        elif self.strategy == ResolveStrategy.FIRST:
            # Just use the first (should already be set)
            result.resolved_package = result.candidates[0].package_name

        elif self.strategy == ResolveStrategy.ALL:
            # Don't change - keep all candidates
            pass

        return result

    def resolve_all(self, results: list[MappingResult]) -> list[MappingResult]:
        """
        Resolve all mapping results.

        Args:
            results: List of mapping results

        Returns:
            List of resolved mapping results
        """
        return [self.resolve(r) for r in results]


def resolve_mappings(
    results: list[MappingResult],
    strategy: ResolveStrategy = ResolveStrategy.MOST_POPULAR,
) -> list[MappingResult]:
    """
    Convenience function to resolve mappings.

    Args:
        results: List of mapping results
        strategy: Resolution strategy

    Returns:
        List of resolved mapping results
    """
    resolver = Resolver(strategy=strategy)
    return resolver.resolve_all(results)
