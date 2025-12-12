"""Tests for the Resolver module."""

import pytest

from pyimport2pkg.resolver import Resolver, ResolveStrategy, resolve_mappings
from pyimport2pkg.models import ImportInfo, MappingResult, PackageCandidate


class TestResolver:
    """Test Resolver class."""

    def test_resolve_single_candidate(self):
        """Test resolving with single candidate."""
        resolver = Resolver()

        result = MappingResult(
            import_info=ImportInfo.from_module_name("numpy"),
            candidates=[PackageCandidate("numpy", is_recommended=True)],
            resolved_package="numpy",
            is_resolved=True,
        )

        resolved = resolver.resolve(result)

        assert resolved.resolved_package == "numpy"

    def test_resolve_most_popular(self):
        """Test resolving with MOST_POPULAR strategy."""
        resolver = Resolver(strategy=ResolveStrategy.MOST_POPULAR)

        result = MappingResult(
            import_info=ImportInfo.from_module_name("cv2"),
            candidates=[
                PackageCandidate("opencv-contrib-python", download_count=5000),
                PackageCandidate("opencv-python", download_count=10000),
                PackageCandidate("opencv-python-headless", download_count=3000),
            ],
            is_resolved=True,
        )

        resolved = resolver.resolve(result)

        assert resolved.resolved_package == "opencv-python"

    def test_resolve_first_strategy(self):
        """Test resolving with FIRST strategy."""
        resolver = Resolver(strategy=ResolveStrategy.FIRST)

        result = MappingResult(
            import_info=ImportInfo.from_module_name("cv2"),
            candidates=[
                PackageCandidate("opencv-contrib-python"),
                PackageCandidate("opencv-python"),
            ],
            is_resolved=True,
        )

        resolved = resolver.resolve(result)

        assert resolved.resolved_package == "opencv-contrib-python"

    def test_resolve_all_strategy(self):
        """Test resolving with ALL strategy."""
        resolver = Resolver(strategy=ResolveStrategy.ALL)

        result = MappingResult(
            import_info=ImportInfo.from_module_name("cv2"),
            candidates=[
                PackageCandidate("opencv-python"),
                PackageCandidate("opencv-contrib-python"),
            ],
            resolved_package="opencv-python",
            is_resolved=True,
        )

        resolved = resolver.resolve(result)

        # Should keep all candidates, resolved package unchanged
        assert len(resolved.candidates) == 2

    def test_resolve_empty_candidates(self):
        """Test resolving with no candidates."""
        resolver = Resolver()

        result = MappingResult(
            import_info=ImportInfo.from_module_name("unknown"),
            candidates=[],
            is_resolved=False,
        )

        resolved = resolver.resolve(result)

        assert resolved.resolved_package is None

    def test_resolve_all(self):
        """Test resolving multiple results."""
        resolver = Resolver(strategy=ResolveStrategy.MOST_POPULAR)

        results = [
            MappingResult(
                import_info=ImportInfo.from_module_name("cv2"),
                candidates=[
                    PackageCandidate("opencv-python", download_count=10000),
                    PackageCandidate("opencv-contrib-python", download_count=5000),
                ],
            ),
            MappingResult(
                import_info=ImportInfo.from_module_name("PIL"),
                candidates=[
                    PackageCandidate("Pillow", download_count=20000),
                ],
            ),
        ]

        resolved = resolver.resolve_all(results)

        assert len(resolved) == 2
        assert resolved[0].resolved_package == "opencv-python"
        assert resolved[1].resolved_package == "Pillow"


class TestResolveMappings:
    """Test resolve_mappings convenience function."""

    def test_resolve_mappings(self):
        """Test the convenience function."""
        results = [
            MappingResult(
                import_info=ImportInfo.from_module_name("numpy"),
                candidates=[PackageCandidate("numpy")],
                resolved_package="numpy",
            ),
        ]

        resolved = resolve_mappings(results)

        assert len(resolved) == 1
        assert resolved[0].resolved_package == "numpy"
