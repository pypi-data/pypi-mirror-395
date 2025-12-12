"""Tests for the Database module."""

import pytest
from pathlib import Path
import sqlite3
import json
from datetime import datetime

from pyimport2pkg.database import (
    MappingDatabase,
    DatabaseBuilder,
    BuildProgress,
    get_build_progress,
)


class TestMappingDatabase:
    """Test MappingDatabase class."""

    def test_init_schema(self, tmp_path: Path):
        """Test database schema initialization."""
        db_path = tmp_path / "test.db"
        db = MappingDatabase(db_path)

        db.init_schema()

        # Verify tables exist
        conn = sqlite3.connect(str(db_path))
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
        tables = {row[0] for row in cursor.fetchall()}

        assert "packages" in tables
        assert "mappings" in tables
        assert "metadata" in tables

        conn.close()
        db.close()

    def test_add_package(self, tmp_path: Path):
        """Test adding a package."""
        db = MappingDatabase(tmp_path / "test.db")
        db.init_schema()

        db.add_package(
            package_name="numpy",
            top_level_modules=["numpy"],
            download_count=100000,
        )

        result = db.lookup("numpy")
        assert result is not None
        assert len(result) == 1
        assert result[0][0] == "numpy"
        assert result[0][1] == 100000

        db.close()

    def test_add_package_multiple_modules(self, tmp_path: Path):
        """Test adding a package with multiple top-level modules."""
        db = MappingDatabase(tmp_path / "test.db")
        db.init_schema()

        db.add_package(
            package_name="mypackage",
            top_level_modules=["module1", "module2"],
            download_count=5000,
        )

        result1 = db.lookup("module1")
        result2 = db.lookup("module2")

        assert result1 is not None
        assert result2 is not None
        assert result1[0][0] == "mypackage"
        assert result2[0][0] == "mypackage"

        db.close()

    def test_lookup_nonexistent(self, tmp_path: Path):
        """Test looking up a non-existent module."""
        db = MappingDatabase(tmp_path / "test.db")
        db.init_schema()

        result = db.lookup("nonexistent_module")
        assert result is None

        db.close()

    def test_lookup_multiple_packages(self, tmp_path: Path):
        """Test looking up a module that maps to multiple packages."""
        db = MappingDatabase(tmp_path / "test.db")
        db.init_schema()

        # Add two packages with the same module name
        db.add_package("package-a", ["sharedmodule"], 10000)
        db.add_package("package-b", ["sharedmodule"], 5000)

        result = db.lookup("sharedmodule")
        assert result is not None
        assert len(result) == 2

        # Should be sorted by download count (descending)
        assert result[0][0] == "package-a"
        assert result[1][0] == "package-b"

        db.close()

    def test_get_stats(self, tmp_path: Path):
        """Test getting database statistics."""
        db = MappingDatabase(tmp_path / "test.db")
        db.init_schema()

        db.add_package("pkg1", ["mod1", "mod2"], 1000)
        db.add_package("pkg2", ["mod3"], 2000)

        stats = db.get_stats()

        assert stats["packages"] == 2
        assert stats["mappings"] == 3
        assert stats["unique_modules"] == 3

        db.close()

    def test_set_metadata(self, tmp_path: Path):
        """Test setting metadata."""
        db = MappingDatabase(tmp_path / "test.db")
        db.init_schema()

        db.set_metadata("test_key", "test_value")

        conn = sqlite3.connect(str(tmp_path / "test.db"))
        result = conn.execute(
            "SELECT value FROM metadata WHERE key = ?", ("test_key",)
        ).fetchone()

        assert result[0] == "test_value"

        conn.close()
        db.close()

    def test_exists(self, tmp_path: Path):
        """Test checking if database exists."""
        db_path = tmp_path / "test.db"
        db = MappingDatabase(db_path)

        # Should not exist initially
        assert db.exists() is False

        # Create and populate
        db.init_schema()
        db.add_package("test", ["test"], 100)

        # Should exist now
        assert db.exists() is True

        db.close()

    def test_context_manager(self, tmp_path: Path):
        """Test using database as context manager."""
        db_path = tmp_path / "test.db"

        with MappingDatabase(db_path) as db:
            db.init_schema()
            db.add_package("test", ["test"], 100)

        # Connection should be closed
        # Verify by opening a new connection
        with MappingDatabase(db_path) as db:
            result = db.lookup("test")
            assert result is not None

    def test_skips_private_modules(self, tmp_path: Path):
        """Test that private modules (starting with _) are skipped."""
        db = MappingDatabase(tmp_path / "test.db")
        db.init_schema()

        db.add_package("mypackage", ["public", "_private", "__dunder"], 1000)

        # Public module should be found
        assert db.lookup("public") is not None

        # Private modules should not be found
        assert db.lookup("_private") is None
        assert db.lookup("__dunder") is None

        db.close()


class TestDatabaseBuilder:
    """Test DatabaseBuilder class."""

    def test_extract_top_level_from_wheel(self, tmp_path: Path):
        """Test extracting top_level.txt from a wheel."""
        import zipfile

        # Create a fake wheel
        wheel_path = tmp_path / "test-1.0-py3-none-any.whl"
        with zipfile.ZipFile(wheel_path, "w") as zf:
            zf.writestr("test/__init__.py", "")
            zf.writestr("test/module.py", "")
            zf.writestr("test-1.0.dist-info/WHEEL", "")
            zf.writestr("test-1.0.dist-info/METADATA", "")
            zf.writestr("test-1.0.dist-info/top_level.txt", "test\n")

        # Read wheel content
        wheel_content = wheel_path.read_bytes()

        db = MappingDatabase(tmp_path / "test.db")
        builder = DatabaseBuilder(db)

        modules = builder.extract_top_level_from_wheel(wheel_content)

        assert "test" in modules

        db.close()

    def test_infer_top_level_from_wheel(self, tmp_path: Path):
        """Test inferring top-level modules when top_level.txt is missing."""
        import zipfile

        # Create a wheel without top_level.txt
        wheel_path = tmp_path / "mylib-1.0-py3-none-any.whl"
        with zipfile.ZipFile(wheel_path, "w") as zf:
            zf.writestr("mylib/__init__.py", "")
            zf.writestr("mylib/utils.py", "")
            zf.writestr("mylib-1.0.dist-info/WHEEL", "")
            zf.writestr("mylib-1.0.dist-info/METADATA", "")
            # No top_level.txt

        wheel_content = wheel_path.read_bytes()

        db = MappingDatabase(tmp_path / "test.db")
        builder = DatabaseBuilder(db)

        modules = builder.extract_top_level_from_wheel(wheel_content)

        assert "mylib" in modules

        db.close()


class TestDatabaseIntegration:
    """Integration tests for database functionality."""

    def test_database_with_mapper(self, tmp_path: Path):
        """Test using database with Mapper."""
        from pyimport2pkg.mapper import Mapper
        from pyimport2pkg.models import ImportInfo

        # Create and populate database
        db = MappingDatabase(tmp_path / "test.db")
        db.init_schema()
        db.add_package("custom-package", ["customlib"], 50000)

        # Use with mapper
        mapper = Mapper(database=db)
        imp = ImportInfo.from_module_name("customlib")

        result = mapper.map_import(imp)

        assert result.is_resolved
        assert result.source == "database"
        assert result.resolved_package == "custom-package"

        db.close()


class TestBuildProgress:
    """Test BuildProgress class for tracking build state."""

    def test_init_creates_empty_data(self, tmp_path: Path):
        """Test initialization with no existing progress file."""
        progress_path = tmp_path / "progress.json"
        progress = BuildProgress(progress_path)

        assert progress.get_status()["status"] == "none"
        assert not progress.has_incomplete_build()

    def test_start_build(self, tmp_path: Path):
        """Test starting a new build."""
        progress_path = tmp_path / "progress.json"
        progress = BuildProgress(progress_path)

        packages = ["numpy", "pandas", "requests"]
        progress.start_build(3, packages)

        assert progress_path.exists()
        status = progress.get_status()
        assert status["status"] == "in_progress"
        assert status["total"] == 3
        assert status["processed"] == 0
        assert status["failed"] == 0

    def test_mark_processed_success(self, tmp_path: Path):
        """Test marking a package as successfully processed."""
        progress_path = tmp_path / "progress.json"
        progress = BuildProgress(progress_path)

        progress.start_build(3, ["numpy", "pandas", "requests"])
        progress.mark_processed("numpy", success=True)

        status = progress.get_status()
        assert status["processed"] == 1
        assert status["failed"] == 0
        assert "numpy" not in progress.get_failed()

    def test_mark_processed_failure(self, tmp_path: Path):
        """Test marking a package as failed."""
        progress_path = tmp_path / "progress.json"
        progress = BuildProgress(progress_path)

        progress.start_build(3, ["numpy", "pandas", "requests"])
        progress.mark_processed("numpy", success=False)

        status = progress.get_status()
        assert status["processed"] == 1
        assert status["failed"] == 1
        assert "numpy" in progress.get_failed()

    def test_retry_success_removes_from_failed(self, tmp_path: Path):
        """Test that successful retry removes package from failed set."""
        progress_path = tmp_path / "progress.json"
        progress = BuildProgress(progress_path)

        progress.start_build(3, ["numpy", "pandas", "requests"])
        # First mark as failed
        progress.mark_processed("numpy", success=False)
        assert "numpy" in progress.get_failed()

        # Then mark as success (retry succeeded)
        progress.mark_processed("numpy", success=True)
        assert "numpy" not in progress.get_failed()

    def test_get_max_packages(self, tmp_path: Path):
        """Test getting max_packages from build session."""
        progress_path = tmp_path / "progress.json"
        progress = BuildProgress(progress_path)

        # Default is 0 when no build started
        assert progress.get_max_packages() == 0

        # Start build with max_packages
        progress.start_build(100, ["pkg1", "pkg2"], max_packages=5000)
        assert progress.get_max_packages() == 5000

    def test_mark_completed(self, tmp_path: Path):
        """Test marking build as completed."""
        progress_path = tmp_path / "progress.json"
        progress = BuildProgress(progress_path)

        progress.start_build(2, ["numpy", "pandas"])
        progress.mark_processed("numpy", success=True)
        progress.mark_processed("pandas", success=True)
        progress.mark_completed()

        status = progress.get_status()
        assert status["status"] == "completed"
        assert not progress.has_incomplete_build()

    def test_mark_interrupted(self, tmp_path: Path):
        """Test marking build as interrupted."""
        progress_path = tmp_path / "progress.json"
        progress = BuildProgress(progress_path)

        progress.start_build(3, ["numpy", "pandas", "requests"])
        progress.mark_processed("numpy", success=True)
        progress.mark_interrupted()

        status = progress.get_status()
        assert status["status"] == "interrupted"
        assert progress.has_incomplete_build()

    def test_get_unprocessed(self, tmp_path: Path):
        """Test getting list of unprocessed packages."""
        progress_path = tmp_path / "progress.json"
        progress = BuildProgress(progress_path)

        progress.start_build(3, ["numpy", "pandas", "requests"])
        progress.mark_processed("numpy", success=True)

        unprocessed = progress.get_unprocessed()
        assert "numpy" not in unprocessed
        assert "pandas" in unprocessed
        assert "requests" in unprocessed

    def test_get_failed(self, tmp_path: Path):
        """Test getting list of failed packages."""
        progress_path = tmp_path / "progress.json"
        progress = BuildProgress(progress_path)

        progress.start_build(3, ["numpy", "pandas", "requests"])
        progress.mark_processed("numpy", success=True)
        progress.mark_processed("pandas", success=False)
        progress.mark_processed("requests", success=False)

        failed = progress.get_failed()
        assert "numpy" not in failed
        assert "pandas" in failed
        assert "requests" in failed

    def test_has_incomplete_build_in_progress(self, tmp_path: Path):
        """Test detecting in-progress build."""
        progress_path = tmp_path / "progress.json"
        progress = BuildProgress(progress_path)

        progress.start_build(3, ["numpy", "pandas", "requests"])

        assert progress.has_incomplete_build()

    def test_has_incomplete_build_interrupted(self, tmp_path: Path):
        """Test detecting interrupted build."""
        progress_path = tmp_path / "progress.json"
        progress = BuildProgress(progress_path)

        progress.start_build(3, ["numpy", "pandas", "requests"])
        progress.mark_interrupted()

        assert progress.has_incomplete_build()

    def test_clear_progress(self, tmp_path: Path):
        """Test clearing progress data."""
        progress_path = tmp_path / "progress.json"
        progress = BuildProgress(progress_path)

        progress.start_build(3, ["numpy", "pandas", "requests"])
        progress.clear()

        assert not progress_path.exists()
        assert progress.get_status()["status"] == "none"

    def test_load_existing_progress(self, tmp_path: Path):
        """Test loading existing progress file."""
        progress_path = tmp_path / "progress.json"

        # Create progress file manually
        data = {
            "started_at": "2025-12-05T10:00:00",
            "total_packages": 100,
            "package_list": ["pkg1", "pkg2"],
            "processed": ["pkg1"],
            "failed": [],
            "status": "interrupted",
        }
        progress_path.write_text(json.dumps(data))

        # Load it
        progress = BuildProgress(progress_path)

        assert progress.has_incomplete_build()
        assert progress.get_status()["total"] == 100
        assert progress.get_status()["processed"] == 1


class TestDatedErrorLogs:
    """Test dated error log functionality."""

    def test_error_log_filename_format(self):
        """Test that error log filename follows expected format."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Verify format: YYYYMMDD_HHMMSS = 15 characters
        assert len(timestamp) == 15
        assert "_" in timestamp

    def test_multiple_error_logs_coexist(self, tmp_path: Path):
        """Test that multiple error logs can exist."""
        import time

        # Create first log
        log1 = tmp_path / "build_errors_20251205_100000.json"
        log1.write_text(json.dumps([{"error": "test1"}]))

        # Create second log with different timestamp
        log2 = tmp_path / "build_errors_20251205_100001.json"
        log2.write_text(json.dumps([{"error": "test2"}]))

        # Both should exist independently
        assert log1.exists()
        assert log2.exists()
        assert json.loads(log1.read_text())[0]["error"] == "test1"
        assert json.loads(log2.read_text())[0]["error"] == "test2"


class TestErrorDetailCapture:
    """Test improved error detail capture."""

    def test_error_includes_timestamp(self):
        """Test that error records include timestamp."""
        error = {
            "package": "test-pkg",
            "error": "timeout",
            "detail": "Request timed out",
            "timestamp": datetime.now().isoformat(),
        }

        assert "timestamp" in error
        # Verify it's a valid ISO format
        parsed = datetime.fromisoformat(error["timestamp"])
        assert isinstance(parsed, datetime)

    def test_error_detail_captures_exception_type(self):
        """Test that exception type is captured in detail."""
        try:
            raise ValueError("Test error message")
        except Exception as e:
            error_detail = f"{type(e).__name__}: {str(e)}" if str(e) else type(e).__name__

        assert "ValueError" in error_detail
        assert "Test error message" in error_detail

    def test_error_detail_fallback_for_empty_message(self):
        """Test fallback when exception message is empty."""
        class EmptyException(Exception):
            def __str__(self):
                return ""

        try:
            raise EmptyException()
        except Exception as e:
            error_detail = f"{type(e).__name__}: {str(e)}" if str(e) else type(e).__name__

        assert error_detail == "EmptyException"


class TestCLIBuildOptions:
    """Test CLI build-db command options."""

    def test_parser_has_resume_option(self):
        """Test that build-db parser has --resume option."""
        from pyimport2pkg.cli import create_parser

        parser = create_parser()
        args = parser.parse_args(["build-db", "--resume"])

        assert args.resume is True
        assert args.retry_failed is False

    def test_parser_has_retry_failed_option(self):
        """Test that build-db parser has --retry-failed option."""
        from pyimport2pkg.cli import create_parser

        parser = create_parser()
        args = parser.parse_args(["build-db", "--retry-failed"])

        assert args.retry_failed is True
        assert args.resume is False

    def test_build_status_command_exists(self):
        """Test that build-status command exists."""
        from pyimport2pkg.cli import create_parser

        parser = create_parser()
        args = parser.parse_args(["build-status"])

        assert args.command == "build-status"

    def test_default_options(self):
        """Test default values for build-db options."""
        from pyimport2pkg.cli import create_parser

        parser = create_parser()
        args = parser.parse_args(["build-db"])

        assert args.resume is False
        assert args.retry_failed is False
        assert args.max_packages == 5000
        assert args.concurrency == 50  # Updated: default is now 50


class TestGetBuildProgress:
    """Test get_build_progress helper function."""

    def test_returns_build_progress_instance(self):
        """Test that function returns BuildProgress instance."""
        progress = get_build_progress()

        assert isinstance(progress, BuildProgress)

    def test_uses_default_path(self):
        """Test that default path is used."""
        from pyimport2pkg.database import DEFAULT_PROGRESS_PATH

        progress = get_build_progress()

        assert progress.progress_path == DEFAULT_PROGRESS_PATH


class TestDatabaseBuilderWithProgress:
    """Test DatabaseBuilder with progress tracking."""

    def test_builder_accepts_progress(self, tmp_path: Path):
        """Test that builder accepts progress parameter."""
        db_path = tmp_path / "test.db"
        db = MappingDatabase(db_path)
        progress = BuildProgress(tmp_path / "progress.json")

        builder = DatabaseBuilder(db, progress=progress)

        assert builder.progress is progress
        db.close()

    def test_builder_creates_default_progress(self, tmp_path: Path):
        """Test that builder creates default progress if not provided."""
        db_path = tmp_path / "test.db"
        db = MappingDatabase(db_path)

        builder = DatabaseBuilder(db)

        assert builder.progress is not None
        assert isinstance(builder.progress, BuildProgress)
        db.close()

    def test_builder_tracks_failed_packages(self, tmp_path: Path):
        """Test that builder tracks failed packages."""
        db_path = tmp_path / "test.db"
        db = MappingDatabase(db_path)

        builder = DatabaseBuilder(db)

        # Manually add a failed package record
        builder.failed_packages.append({
            "package": "test-pkg",
            "error": "not_found",
            "detail": "Package not found",
            "timestamp": datetime.now().isoformat(),
        })

        assert len(builder.failed_packages) == 1
        assert builder.failed_packages[0]["error"] == "not_found"
        db.close()


class TestIncrementalUpdate:
    """Test incremental update functionality (now default behavior)."""

    def test_get_existing_packages_empty(self, tmp_path: Path):
        """Test getting existing packages from empty database."""
        db = MappingDatabase(tmp_path / "test.db")
        db.init_schema()

        # Empty initially
        assert db.get_existing_packages() == set()

        db.close()

    def test_get_existing_packages(self, tmp_path: Path):
        """Test getting set of existing packages."""
        db = MappingDatabase(tmp_path / "test.db")
        db.init_schema()

        # Add some packages
        db.add_package("numpy", ["numpy"], 100000)
        db.add_package("pandas", ["pandas"], 80000)
        db.add_package("requests", ["requests"], 60000)

        existing = db.get_existing_packages()
        assert existing == {"numpy", "pandas", "requests"}

        db.close()

    def test_rebuild_cli_option(self):
        """Test that CLI parser has --rebuild option."""
        from pyimport2pkg.cli import create_parser

        parser = create_parser()
        args = parser.parse_args(["build-db", "--rebuild"])

        assert args.rebuild is True

    def test_rebuild_with_max_packages(self):
        """Test --rebuild with --max-packages."""
        from pyimport2pkg.cli import create_parser

        parser = create_parser()
        args = parser.parse_args(["build-db", "--rebuild", "--max-packages", "10000"])

        assert args.rebuild is True
        assert args.max_packages == 10000


class TestBatchProcessing:
    """Test batch processing functionality."""

    def test_builder_has_save_interval(self, tmp_path: Path):
        """Test builder has SAVE_INTERVAL constant."""
        db = MappingDatabase(tmp_path / "test.db")
        builder = DatabaseBuilder(db)

        assert hasattr(builder, 'SAVE_INTERVAL')
        assert builder.SAVE_INTERVAL == 100  # Updated for better performance

        db.close()

    def test_builder_has_chunk_size(self, tmp_path: Path):
        """Test builder has CHUNK_SIZE constant for memory efficiency."""
        db = MappingDatabase(tmp_path / "test.db")
        builder = DatabaseBuilder(db)

        assert hasattr(builder, 'CHUNK_SIZE')
        assert builder.CHUNK_SIZE == 500

        db.close()

    def test_builder_has_rate_limit_settings(self, tmp_path: Path):
        """Test builder has rate limit detection constants."""
        db = MappingDatabase(tmp_path / "test.db")
        builder = DatabaseBuilder(db)

        assert hasattr(builder, 'CONSECUTIVE_FAIL_THRESHOLD')
        assert hasattr(builder, 'PAUSE_DURATION')
        assert hasattr(builder, 'MAX_PAUSE_COUNT')
        assert builder.CONSECUTIVE_FAIL_THRESHOLD == 20
        assert builder.PAUSE_DURATION == 30
        assert builder.MAX_PAUSE_COUNT == 5

        db.close()

    def test_builder_tracks_consecutive_failures(self, tmp_path: Path):
        """Test builder has consecutive failure tracking."""
        db = MappingDatabase(tmp_path / "test.db")
        builder = DatabaseBuilder(db)

        assert hasattr(builder, '_consecutive_failures')
        assert hasattr(builder, '_pause_count')
        assert builder._consecutive_failures == 0
        assert builder._pause_count == 0

        db.close()

    def test_add_packages_batch(self, tmp_path: Path):
        """Test batch adding packages."""
        db = MappingDatabase(tmp_path / "test.db")
        db.init_schema()

        packages = [
            ("numpy", ["numpy"], 100000),
            ("pandas", ["pandas"], 80000),
            ("requests", ["requests"], 60000),
        ]

        db.add_packages_batch(packages)

        # Verify all packages were added
        assert db.lookup("numpy") is not None
        assert db.lookup("pandas") is not None
        assert db.lookup("requests") is not None

        stats = db.get_stats()
        assert stats["packages"] == 3

        db.close()


class TestProgressSaveFrequency:
    """Test progress save behavior (now batched for performance)."""

    def test_mark_processed_marks_dirty(self, tmp_path: Path):
        """Test that mark_processed sets dirty flag."""
        progress_path = tmp_path / "progress.json"
        progress = BuildProgress(progress_path)

        progress.start_build(3, ["pkg1", "pkg2", "pkg3"])

        # Mark first package (doesn't save immediately)
        progress.mark_processed("pkg1", success=True)

        # Dirty flag should be set
        assert progress._dirty is True

    def test_force_save_persists_data(self, tmp_path: Path):
        """Test that force_save writes to disk."""
        progress_path = tmp_path / "progress.json"
        progress = BuildProgress(progress_path)

        progress.start_build(3, ["pkg1", "pkg2", "pkg3"])
        progress.mark_processed("pkg1", success=True)
        progress.force_save()  # Explicitly save

        # Check file was updated (reload from disk)
        progress2 = BuildProgress(progress_path)
        assert "pkg1" in progress2._data.get("processed", [])

    def test_progress_survives_crash_with_save(self, tmp_path: Path):
        """Test that progress survives crash when save is called."""
        progress_path = tmp_path / "progress.json"

        # Simulate first run
        progress1 = BuildProgress(progress_path)
        progress1.start_build(5, ["a", "b", "c", "d", "e"])
        progress1.mark_processed("a", success=True)
        progress1.mark_processed("b", success=True)
        progress1.mark_processed("c", success=False)
        progress1.save()  # Explicit save before "crash"

        # Simulate restart - create new instance
        progress2 = BuildProgress(progress_path)

        # Check state was preserved
        assert progress2.has_incomplete_build()
        status = progress2.get_status()
        assert status["processed"] == 3
        assert status["failed"] == 1

        # Check unprocessed list
        unprocessed = progress2.get_unprocessed()
        assert "d" in unprocessed
        assert "e" in unprocessed
        assert "a" not in unprocessed

    def test_mark_interrupted_saves_immediately(self, tmp_path: Path):
        """Test that mark_interrupted saves immediately."""
        progress_path = tmp_path / "progress.json"
        progress = BuildProgress(progress_path)

        progress.start_build(3, ["pkg1", "pkg2", "pkg3"])
        progress.mark_processed("pkg1", success=True)
        progress.mark_interrupted()  # Should save immediately

        # Check file was updated
        progress2 = BuildProgress(progress_path)
        assert progress2.get_status()["status"] == "interrupted"
