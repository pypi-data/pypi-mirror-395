"""Tests for the Mapper module."""

import pytest

from pyimport2pkg.mapper import Mapper, map_imports
from pyimport2pkg.models import ImportInfo


class MockDatabase:
    """Mock database for testing."""

    def __init__(self, data: dict[str, list[tuple[str, int]]]):
        self.data = data

    def lookup(self, module_name: str) -> list[tuple[str, int]] | None:
        return self.data.get(module_name)


class TestMapperHardcoded:
    """Test hardcoded mapping resolution."""

    def test_maps_cv2_to_opencv(self):
        """Test cv2 -> opencv-python mapping."""
        mapper = Mapper()
        imp = ImportInfo.from_module_name("cv2")

        result = mapper.map_import(imp)

        assert result.is_resolved
        assert result.source == "hardcoded"
        assert result.resolved_package == "opencv-python"
        assert len(result.candidates) >= 2

    def test_maps_pil_to_pillow(self):
        """Test PIL -> Pillow mapping."""
        mapper = Mapper()
        imp = ImportInfo.from_module_name("PIL")

        result = mapper.map_import(imp)

        assert result.is_resolved
        assert result.resolved_package == "Pillow"

    def test_maps_sklearn_to_scikit_learn(self):
        """Test sklearn -> scikit-learn mapping."""
        mapper = Mapper()
        imp = ImportInfo.from_module_name("sklearn")

        result = mapper.map_import(imp)

        assert result.is_resolved
        assert result.resolved_package == "scikit-learn"

    def test_maps_win32api_to_pywin32(self):
        """Test win32api -> pywin32 mapping."""
        mapper = Mapper()
        imp = ImportInfo.from_module_name("win32api")

        result = mapper.map_import(imp)

        assert result.is_resolved
        assert result.resolved_package == "pywin32"


class TestMapperNamespace:
    """Test namespace package mapping resolution."""

    def test_maps_google_cloud_storage(self):
        """Test google.cloud.storage mapping."""
        mapper = Mapper()
        imp = ImportInfo.from_module_name("google.cloud.storage")

        result = mapper.map_import(imp)

        assert result.is_resolved
        assert result.source == "namespace"
        assert result.resolved_package == "google-cloud-storage"

    def test_maps_azure_storage_blob(self):
        """Test azure.storage.blob mapping."""
        mapper = Mapper()
        imp = ImportInfo.from_module_name("azure.storage.blob")

        result = mapper.map_import(imp)

        assert result.is_resolved
        assert result.resolved_package == "azure-storage-blob"

    def test_maps_google_auth(self):
        """Test google.auth mapping."""
        mapper = Mapper()
        imp = ImportInfo.from_module_name("google.auth")

        result = mapper.map_import(imp)

        assert result.is_resolved
        assert result.resolved_package == "google-auth"


class TestMapperDatabase:
    """Test database lookup resolution."""

    def test_uses_database_when_available(self):
        """Test that database is used when mapping not in hardcoded."""
        db = MockDatabase({
            "mypackage": [("my-package", 10000), ("mypackage-alt", 5000)]
        })
        mapper = Mapper(database=db)
        imp = ImportInfo.from_module_name("mypackage")

        result = mapper.map_import(imp)

        assert result.is_resolved
        assert result.source == "database"
        assert result.resolved_package == "my-package"
        assert len(result.candidates) == 2

    def test_hardcoded_takes_priority_over_database(self):
        """Test that hardcoded mappings take priority over database."""
        db = MockDatabase({
            "cv2": [("wrong-opencv", 10000)]
        })
        mapper = Mapper(database=db)
        imp = ImportInfo.from_module_name("cv2")

        result = mapper.map_import(imp)

        # Should use hardcoded, not database
        assert result.source == "hardcoded"
        assert result.resolved_package == "opencv-python"

    def test_database_returns_download_counts(self):
        """Test that database results include download counts."""
        db = MockDatabase({
            "somelib": [("some-lib", 50000), ("somelib", 1000)]
        })
        mapper = Mapper(database=db)
        imp = ImportInfo.from_module_name("somelib")

        result = mapper.map_import(imp)

        assert result.candidates[0].download_count == 50000
        assert result.candidates[1].download_count == 1000


class TestMapperGuess:
    """Test guess fallback resolution."""

    def test_guesses_unknown_module(self):
        """Test that unknown modules are guessed."""
        mapper = Mapper()
        imp = ImportInfo.from_module_name("some_random_module")

        result = mapper.map_import(imp)

        assert result.is_resolved
        assert result.source == "guessed"
        assert result.resolved_package == "some_random_module"
        assert any("guessed" in w.lower() for w in imp.warnings)

    def test_guess_uses_top_level(self):
        """Test that guess uses top-level module name."""
        mapper = Mapper()
        imp = ImportInfo.from_module_name("mylib.submodule.utils")

        result = mapper.map_import(imp)

        assert result.resolved_package == "mylib"


class TestMapperMultiple:
    """Test mapping multiple imports."""

    def test_maps_multiple_imports(self):
        """Test mapping a list of imports."""
        mapper = Mapper()
        imports = [
            ImportInfo.from_module_name("cv2"),
            ImportInfo.from_module_name("PIL"),
            ImportInfo.from_module_name("requests"),
        ]

        results = mapper.map_imports(imports)

        assert len(results) == 3
        assert all(r.is_resolved for r in results)


class TestMapperCandidates:
    """Test candidate handling."""

    def test_first_candidate_is_recommended(self):
        """Test that first candidate is marked as recommended."""
        mapper = Mapper()
        imp = ImportInfo.from_module_name("cv2")

        result = mapper.map_import(imp)

        assert result.candidates[0].is_recommended is True
        if len(result.candidates) > 1:
            assert result.candidates[1].is_recommended is False

    def test_candidates_preserve_order(self):
        """Test that candidates preserve order from mappings."""
        mapper = Mapper()
        imp = ImportInfo.from_module_name("cv2")

        result = mapper.map_import(imp)

        # opencv-python should be first (recommended)
        assert result.candidates[0].package_name == "opencv-python"


class TestMapImportsFunction:
    """Test the convenience function."""

    def test_map_imports_function(self):
        """Test the map_imports convenience function."""
        imports = [
            ImportInfo.from_module_name("cv2"),
            ImportInfo.from_module_name("numpy"),
        ]

        results = map_imports(imports)

        assert len(results) == 2
        assert results[0].resolved_package == "opencv-python"

    def test_map_imports_with_database(self):
        """Test map_imports with database."""
        db = MockDatabase({
            "customlib": [("custom-lib", 10000)]
        })
        imports = [
            ImportInfo.from_module_name("customlib"),
        ]

        results = map_imports(imports, database=db)

        assert results[0].resolved_package == "custom-lib"
