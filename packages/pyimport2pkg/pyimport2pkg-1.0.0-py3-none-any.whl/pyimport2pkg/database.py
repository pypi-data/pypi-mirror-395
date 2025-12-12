"""
Database module: Builds and queries the module-to-package mapping database.

Fetches popular packages from PyPI, extracts top_level.txt from wheel files,
and builds a SQLite database for fast lookups.

Features:
- Smart incremental updates (default behavior)
- True async parallelism with batched DB writes
- Progress tracking with resume capability
- Graceful interrupt handling (Ctrl+C)
"""

import asyncio
import signal
import sqlite3
import tempfile
import zipfile
from pathlib import Path
from typing import Callable
from datetime import datetime
import json
import sys
import threading

import httpx


# Default database location
DEFAULT_DB_PATH = Path(__file__).parent / "data" / "mapping.db"

# Progress file location
DEFAULT_PROGRESS_PATH = Path(__file__).parent / "data" / "build_progress.json"

# PyPI top packages data source
TOP_PACKAGES_URL = "https://hugovk.github.io/top-pypi-packages/top-pypi-packages-30-days.min.json"

# PyPI JSON API
PYPI_JSON_URL = "https://pypi.org/pypi/{package}/json"


class MappingDatabase:
    """
    SQLite database for module-to-package mappings.

    Schema:
    - packages: package_name, download_count, last_updated
    - mappings: module_name -> package_name (many-to-many)
    """

    def __init__(self, db_path: Path | str | None = None):
        self.db_path = Path(db_path) if db_path else DEFAULT_DB_PATH
        self._connection: sqlite3.Connection | None = None
        self._lock = threading.Lock()

    def _ensure_dir(self) -> None:
        """Ensure the database directory exists."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def _get_connection(self) -> sqlite3.Connection:
        """Get or create database connection."""
        if self._connection is None:
            self._ensure_dir()
            self._connection = sqlite3.connect(str(self.db_path), check_same_thread=False)
            self._connection.row_factory = sqlite3.Row
            # Performance optimizations
            self._connection.execute("PRAGMA journal_mode=WAL")
            self._connection.execute("PRAGMA synchronous=NORMAL")
            self._connection.execute("PRAGMA cache_size=10000")
        return self._connection

    def close(self) -> None:
        """Close the database connection."""
        if self._connection:
            self._connection.close()
            self._connection = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def init_schema(self) -> None:
        """Initialize the database schema."""
        conn = self._get_connection()
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS packages (
                package_name TEXT PRIMARY KEY,
                download_count INTEGER DEFAULT 0,
                last_updated TEXT
            );

            CREATE TABLE IF NOT EXISTS mappings (
                module_name TEXT NOT NULL,
                package_name TEXT NOT NULL,
                PRIMARY KEY (module_name, package_name),
                FOREIGN KEY (package_name) REFERENCES packages(package_name)
            );

            CREATE INDEX IF NOT EXISTS idx_mappings_module
                ON mappings(module_name);

            CREATE TABLE IF NOT EXISTS metadata (
                key TEXT PRIMARY KEY,
                value TEXT
            );
        """)
        conn.commit()

    def lookup(self, module_name: str) -> list[tuple[str, int]] | None:
        """Look up a module name in the database."""
        conn = self._get_connection()
        cursor = conn.execute("""
            SELECT m.package_name, p.download_count
            FROM mappings m
            JOIN packages p ON m.package_name = p.package_name
            WHERE m.module_name = ?
            ORDER BY p.download_count DESC
        """, (module_name,))

        results = cursor.fetchall()
        if not results:
            return None

        return [(row["package_name"], row["download_count"]) for row in results]

    def add_package(
        self,
        package_name: str,
        top_level_modules: list[str],
        download_count: int = 0,
    ) -> None:
        """Add a package and its module mappings to the database."""
        with self._lock:
            conn = self._get_connection()
            conn.execute("""
                INSERT OR REPLACE INTO packages (package_name, download_count, last_updated)
                VALUES (?, ?, ?)
            """, (package_name, download_count, datetime.now().isoformat()))

            for module in top_level_modules:
                if module and not module.startswith("_"):
                    conn.execute("""
                        INSERT OR IGNORE INTO mappings (module_name, package_name)
                        VALUES (?, ?)
                    """, (module, package_name))
            conn.commit()

    def add_packages_batch(
        self,
        packages: list[tuple[str, list[str], int]],
    ) -> None:
        """
        Add multiple packages in a single transaction.

        Args:
            packages: List of (package_name, top_level_modules, download_count)
        """
        if not packages:
            return

        with self._lock:
            conn = self._get_connection()
            now = datetime.now().isoformat()

            # Batch insert packages
            conn.executemany("""
                INSERT OR REPLACE INTO packages (package_name, download_count, last_updated)
                VALUES (?, ?, ?)
            """, [(name, count, now) for name, _, count in packages])

            # Batch insert mappings
            mappings = []
            for name, modules, _ in packages:
                for module in modules:
                    if module and not module.startswith("_"):
                        mappings.append((module, name))

            if mappings:
                conn.executemany("""
                    INSERT OR IGNORE INTO mappings (module_name, package_name)
                    VALUES (?, ?)
                """, mappings)

            conn.commit()

    def get_stats(self) -> dict:
        """Get database statistics."""
        conn = self._get_connection()

        package_count = conn.execute(
            "SELECT COUNT(*) FROM packages"
        ).fetchone()[0]

        mapping_count = conn.execute(
            "SELECT COUNT(*) FROM mappings"
        ).fetchone()[0]

        unique_modules = conn.execute(
            "SELECT COUNT(DISTINCT module_name) FROM mappings"
        ).fetchone()[0]

        last_updated = conn.execute(
            "SELECT value FROM metadata WHERE key = 'last_build'"
        ).fetchone()

        return {
            "packages": package_count,
            "mappings": mapping_count,
            "unique_modules": unique_modules,
            "last_updated": last_updated[0] if last_updated else None,
            "db_path": str(self.db_path),
        }

    def set_metadata(self, key: str, value: str) -> None:
        """Set a metadata value."""
        conn = self._get_connection()
        conn.execute("""
            INSERT OR REPLACE INTO metadata (key, value) VALUES (?, ?)
        """, (key, value))
        conn.commit()

    def exists(self) -> bool:
        """Check if the database file exists and has data."""
        if not self.db_path.exists():
            return False
        try:
            stats = self.get_stats()
            return stats["packages"] > 0
        except Exception:
            return False

    def get_existing_packages(self) -> set[str]:
        """Get set of all package names in the database."""
        conn = self._get_connection()
        cursor = conn.execute("SELECT package_name FROM packages")
        return {row[0] for row in cursor.fetchall()}


class BuildProgress:
    """
    Tracks build progress for resume capability.

    Now with batched saves for better performance.
    """

    def __init__(self, progress_path: Path | str | None = None):
        self.progress_path = Path(progress_path) if progress_path else DEFAULT_PROGRESS_PATH
        self._data: dict = {}
        self._dirty = False
        self._lock = threading.Lock()
        self._load()

    def _load(self) -> None:
        """Load progress from file."""
        if self.progress_path.exists():
            try:
                self._data = json.loads(self.progress_path.read_text(encoding="utf-8"))
            except Exception:
                self._data = {}
        else:
            self._data = {}

    def save(self) -> None:
        """Save progress to file (only if dirty)."""
        with self._lock:
            if not self._dirty:
                return
            # Convert sets to lists for JSON
            save_data = self._data.copy()
            if isinstance(save_data.get("processed"), set):
                save_data["processed"] = list(save_data["processed"])
            if isinstance(save_data.get("failed"), set):
                save_data["failed"] = list(save_data["failed"])

            self.progress_path.parent.mkdir(parents=True, exist_ok=True)
            self.progress_path.write_text(
                json.dumps(save_data, indent=2, ensure_ascii=False),
                encoding="utf-8"
            )
            self._dirty = False

    def force_save(self) -> None:
        """Force save progress to file."""
        with self._lock:
            self._dirty = True
        self.save()

    def start_build(self, total_packages: int, package_list: list[str], max_packages: int = 0) -> None:
        """Start a new build session."""
        with self._lock:
            self._data = {
                "started_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "total_packages": total_packages,
                "max_packages": max_packages,  # Save for resume
                "package_list": package_list,
                "processed": set(),
                "failed": set(),
                "status": "in_progress",
            }
            # Convert sets to lists for JSON serialization
            self._dirty = True
        self.force_save()

    def mark_processed(self, package_name: str, success: bool) -> None:
        """Mark a package as processed (does NOT save immediately)."""
        with self._lock:
            if "processed" not in self._data:
                self._data["processed"] = set()
            elif isinstance(self._data["processed"], list):
                self._data["processed"] = set(self._data["processed"])

            self._data["processed"].add(package_name)

            if not success:
                if "failed" not in self._data:
                    self._data["failed"] = set()
                elif isinstance(self._data["failed"], list):
                    self._data["failed"] = set(self._data["failed"])
                self._data["failed"].add(package_name)
            else:
                # Remove from failed if it was previously failed (retry success)
                if "failed" in self._data:
                    if isinstance(self._data["failed"], list):
                        self._data["failed"] = set(self._data["failed"])
                    self._data["failed"].discard(package_name)

            self._data["last_updated"] = datetime.now().isoformat()
            self._dirty = True

    def mark_completed(self) -> None:
        """Mark build as completed."""
        with self._lock:
            self._data["status"] = "completed"
            self._data["completed_at"] = datetime.now().isoformat()
            self._dirty = True
        self.force_save()

    def mark_interrupted(self) -> None:
        """Mark build as interrupted."""
        with self._lock:
            self._data["status"] = "interrupted"
            self._data["interrupted_at"] = datetime.now().isoformat()
            self._dirty = True
        self.force_save()

    def get_unprocessed(self) -> list[str]:
        """Get list of packages not yet processed."""
        all_packages = set(self._data.get("package_list", []))
        processed = self._data.get("processed", [])
        if isinstance(processed, list):
            processed = set(processed)
        return list(all_packages - processed)

    def get_failed(self) -> list[str]:
        """Get list of failed packages."""
        failed = self._data.get("failed", [])
        if isinstance(failed, set):
            return list(failed)
        return failed

    def has_incomplete_build(self) -> bool:
        """Check if there's an incomplete build to resume."""
        status = self._data.get("status")
        return status in ("in_progress", "interrupted")

    def get_status(self) -> dict:
        """Get current build status."""
        processed = self._data.get("processed", [])
        if isinstance(processed, set):
            processed_count = len(processed)
        else:
            processed_count = len(processed)

        failed = self._data.get("failed", [])
        if isinstance(failed, set):
            failed_count = len(failed)
        else:
            failed_count = len(failed)

        return {
            "status": self._data.get("status", "none"),
            "total": self._data.get("total_packages", 0),
            "processed": processed_count,
            "failed": failed_count,
            "started_at": self._data.get("started_at"),
            "last_updated": self._data.get("last_updated"),
        }

    def get_max_packages(self) -> int:
        """Get the max_packages value from the build session."""
        return self._data.get("max_packages", 0)

    def clear(self) -> None:
        """Clear progress data."""
        self._data = {}
        self._dirty = False
        if self.progress_path.exists():
            self.progress_path.unlink()


class DatabaseBuilder:
    """
    Builds the mapping database by fetching data from PyPI.

    Optimized for performance with:
    - True async parallelism
    - Batched database writes
    - Chunked task creation (memory efficient)
    - Rate limit detection and auto-retry
    """

    # How often to save progress and flush DB (in packages)
    SAVE_INTERVAL = 100

    # How often to print progress
    PRINT_INTERVAL = 100

    # Chunk size for task creation (memory optimization)
    CHUNK_SIZE = 500

    # Rate limit detection
    CONSECUTIVE_FAIL_THRESHOLD = 20  # Pause if this many consecutive failures
    PAUSE_DURATION = 30  # Seconds to pause when rate limited
    MAX_PAUSE_COUNT = 5  # Max pauses before giving up

    def __init__(
        self,
        db: MappingDatabase,
        max_packages: int = 5000,
        concurrency: int = 50,
        progress: BuildProgress | None = None,
    ):
        self.db = db
        self.max_packages = max_packages
        self.concurrency = concurrency
        self.progress = progress or BuildProgress()
        self._client: httpx.AsyncClient | None = None

        # Pending packages to write to DB (batched)
        self._pending_packages: list[tuple[str, list[str], int]] = []
        self._pending_lock = asyncio.Lock()

        # Error tracking
        self.failed_packages: list[dict] = []

        # Interrupt flag
        self._interrupted = False
        self._original_sigint_handler = None

        # Counters
        self._success_count = 0
        self._fail_count = 0
        self._processed_count = 0

        # Rate limit detection
        self._consecutive_failures = 0
        self._pause_count = 0

    def _setup_signal_handlers(self) -> None:
        """Setup signal handlers for graceful interrupt."""
        def signal_handler(signum, frame):
            if self._interrupted:
                print("\nForce quitting...", file=sys.stderr)
                sys.exit(1)
            print("\nSaving progress, please wait... (Press Ctrl+C again to force quit)", file=sys.stderr)
            self._interrupted = True

        self._original_sigint_handler = signal.signal(signal.SIGINT, signal_handler)

    def _restore_signal_handlers(self) -> None:
        """Restore original signal handlers."""
        if self._original_sigint_handler is not None:
            signal.signal(signal.SIGINT, self._original_sigint_handler)

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=30.0,
                follow_redirects=True,
                limits=httpx.Limits(
                    max_keepalive_connections=self.concurrency,
                    max_connections=self.concurrency * 2,
                ),
            )
        return self._client

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None

    async def fetch_top_packages(self) -> list[dict]:
        """Fetch the list of top PyPI packages."""
        client = await self._get_client()
        response = await client.get(TOP_PACKAGES_URL)
        response.raise_for_status()
        data = response.json()
        return data.get("rows", [])[:self.max_packages]

    async def fetch_package_info(self, package_name: str) -> dict | None:
        """Fetch package info from PyPI JSON API."""
        client = await self._get_client()
        try:
            url = PYPI_JSON_URL.format(package=package_name)
            response = await client.get(url)
            if response.status_code == 404:
                return None
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

    def extract_top_level_from_wheel(self, wheel_content: bytes) -> list[str]:
        """Extract top_level.txt from wheel file content."""
        try:
            with tempfile.NamedTemporaryFile(suffix=".whl", delete=False) as f:
                f.write(wheel_content)
                temp_path = f.name

            try:
                with zipfile.ZipFile(temp_path, "r") as zf:
                    for name in zf.namelist():
                        if name.endswith("top_level.txt"):
                            content = zf.read(name).decode("utf-8")
                            return [line.strip() for line in content.splitlines() if line.strip()]
                    return self._infer_top_level_from_wheel(zf)
            finally:
                Path(temp_path).unlink(missing_ok=True)
        except Exception:
            return []

    def _infer_top_level_from_wheel(self, zf: zipfile.ZipFile) -> list[str]:
        """Infer top-level modules from wheel contents."""
        top_level = set()
        for name in zf.namelist():
            if ".dist-info/" in name or ".data/" in name:
                continue
            parts = name.split("/")
            if parts[0] and not parts[0].startswith("_"):
                module = parts[0]
                if module.endswith(".py"):
                    module = module[:-3]
                top_level.add(module)
        return list(top_level)

    async def _flush_pending(self) -> None:
        """Flush pending packages to database."""
        async with self._pending_lock:
            if self._pending_packages:
                self.db.add_packages_batch(self._pending_packages)
                self._pending_packages = []

    async def _add_pending(self, package_name: str, modules: list[str], download_count: int) -> None:
        """Add a package to pending list for batch write."""
        async with self._pending_lock:
            self._pending_packages.append((package_name, modules, download_count))

            # Flush if batch is large enough
            if len(self._pending_packages) >= self.SAVE_INTERVAL:
                self.db.add_packages_batch(self._pending_packages)
                self._pending_packages = []

    async def fetch_and_process_package(
        self,
        package_name: str,
        download_count: int,
    ) -> bool:
        """Fetch and process a single package."""
        try:
            info = await self.fetch_package_info(package_name)
            if not info:
                self.failed_packages.append({
                    "package": package_name,
                    "error": "not_found",
                    "timestamp": datetime.now().isoformat(),
                })
                return False

            # Find a suitable wheel URL
            urls = info.get("urls", [])
            wheel_url = None

            for url_info in urls:
                if url_info.get("packagetype") == "bdist_wheel":
                    filename = url_info.get("filename", "")
                    if "py3-none-any" in filename or "py2.py3-none-any" in filename:
                        wheel_url = url_info.get("url")
                        break
                    elif not wheel_url:
                        wheel_url = url_info.get("url")

            if not wheel_url:
                # No wheel, guess module name
                modules = [package_name.replace("-", "_").lower()]
                await self._add_pending(package_name, modules, download_count)
                return True

            # Download and extract wheel
            client = await self._get_client()
            response = await client.get(wheel_url)
            response.raise_for_status()

            top_level = self.extract_top_level_from_wheel(response.content)
            if not top_level:
                top_level = [package_name.replace("-", "_").lower()]

            await self._add_pending(package_name, top_level, download_count)
            return True

        except httpx.TimeoutException:
            self.failed_packages.append({
                "package": package_name,
                "error": "timeout",
                "timestamp": datetime.now().isoformat(),
            })
            return False
        except httpx.HTTPStatusError as e:
            self.failed_packages.append({
                "package": package_name,
                "error": f"http_{e.response.status_code}",
                "timestamp": datetime.now().isoformat(),
            })
            return False
        except Exception as e:
            self.failed_packages.append({
                "package": package_name,
                "error": str(type(e).__name__),
                "timestamp": datetime.now().isoformat(),
            })
            return False

    async def build(
        self,
        progress_callback: Callable | None = None,
        resume: bool = False,
        retry_failed: bool = False,
    ) -> dict:
        """
        Build the database from PyPI data.

        Default behavior: Smart incremental update
        - Fetches top N packages from PyPI
        - Skips packages already in the database
        - Only processes new packages

        Args:
            progress_callback: Optional callback(current, total, package_name)
            resume: Resume from last interrupted build
            retry_failed: Only retry packages that failed last time

        Returns:
            Build statistics
        """
        self._setup_signal_handlers()

        try:
            # Initialize database
            self.db.init_schema()

            # Get existing packages
            existing_packages = self.db.get_existing_packages()

            # Determine which packages to process
            if retry_failed:
                # Only retry failed packages
                failed_list = self.progress.get_failed()
                if not failed_list:
                    return {"message": "No failed packages to retry", "total": 0, "success": 0, "failed": 0, "skipped": 0}

                # Use saved max_packages if available, otherwise use current setting
                saved_max = self.progress.get_max_packages()
                if saved_max > 0:
                    original_max = self.max_packages
                    self.max_packages = saved_max
                    all_packages = await self.fetch_top_packages()
                    self.max_packages = original_max
                else:
                    all_packages = await self.fetch_top_packages()

                package_map = {p["project"]: p for p in all_packages}
                packages = [package_map[name] for name in failed_list if name in package_map]
                print(f"Retrying {len(packages)} failed packages...", file=sys.stderr)

            elif resume and self.progress.has_incomplete_build():
                # Resume interrupted build
                unprocessed = self.progress.get_unprocessed()
                if not unprocessed:
                    return {"message": "No unprocessed packages", "total": 0, "success": 0, "failed": 0, "skipped": 0}

                # Use saved max_packages if available, otherwise use current setting
                saved_max = self.progress.get_max_packages()
                if saved_max > 0:
                    original_max = self.max_packages
                    self.max_packages = saved_max
                    print(f"Using saved max_packages from last build: {saved_max}", file=sys.stderr)
                    all_packages = await self.fetch_top_packages()
                    self.max_packages = original_max
                else:
                    all_packages = await self.fetch_top_packages()

                package_map = {p["project"]: p for p in all_packages}
                packages = [package_map[name] for name in unprocessed if name in package_map]
                print(f"Resuming build: {len(packages)} packages to process", file=sys.stderr)

            else:
                # Default: smart incremental update
                all_packages = await self.fetch_top_packages()

                # Filter out existing packages
                packages = [p for p in all_packages if p["project"] not in existing_packages]

                if existing_packages:
                    print(f"Database has {len(existing_packages)} packages", file=sys.stderr)

                if not packages:
                    return {
                        "message": f"Database already contains top {len(existing_packages)} packages, no update needed",
                        "total": 0,
                        "success": 0,
                        "failed": 0,
                        "skipped": len(existing_packages),
                    }

                print(f"Will process {len(packages)} new packages", file=sys.stderr)

                # Start new build tracking (save max_packages for resume)
                package_names = [p["project"] for p in packages]
                self.progress.start_build(len(packages), package_names, self.max_packages)

            total = len(packages)
            if total == 0:
                return {"message": "No packages to process", "total": 0, "success": 0, "failed": 0, "skipped": len(existing_packages)}

            # Process packages with semaphore for concurrency control
            semaphore = asyncio.Semaphore(self.concurrency)

            async def process_one(pkg: dict) -> bool:
                """Process one package, return True if should continue, False to pause."""
                if self._interrupted:
                    return True

                async with semaphore:
                    if self._interrupted:
                        return True

                    package_name = pkg.get("project", "")
                    download_count = pkg.get("download_count", 0)

                    result = await self.fetch_and_process_package(package_name, download_count)

                    self._processed_count += 1
                    if result:
                        self._success_count += 1
                        self._consecutive_failures = 0  # Reset on success
                    else:
                        self._fail_count += 1
                        self._consecutive_failures += 1

                    # Update progress tracker (but don't save yet)
                    self.progress.mark_processed(package_name, result)

                    # Periodic progress save and callback
                    if self._processed_count % self.SAVE_INTERVAL == 0:
                        await self._flush_pending()
                        self.progress.save()

                    if self._processed_count % self.PRINT_INTERVAL == 0 or self._processed_count == total:
                        print(f"  [{self._processed_count}/{total}] Success: {self._success_count}, Failed: {self._fail_count}", file=sys.stderr)

                    if progress_callback:
                        progress_callback(self._processed_count, total, package_name)

                    return True

            async def check_rate_limit() -> bool:
                """Check if rate limited, pause if needed. Returns False if should stop."""
                if self._consecutive_failures >= self.CONSECUTIVE_FAIL_THRESHOLD:
                    self._pause_count += 1
                    if self._pause_count > self.MAX_PAUSE_COUNT:
                        print(f"\nToo many consecutive failures, reached max pause count ({self.MAX_PAUSE_COUNT}), stopping build.", file=sys.stderr)
                        return False

                    print(f"\nDetected {self._consecutive_failures} consecutive failures, possible rate limiting.", file=sys.stderr)
                    print(f"Pausing {self.PAUSE_DURATION} seconds before retry (pause {self._pause_count}/{self.MAX_PAUSE_COUNT})...", file=sys.stderr)

                    await asyncio.sleep(self.PAUSE_DURATION)
                    self._consecutive_failures = 0  # Reset after pause
                    print("Resuming...", file=sys.stderr)

                return True

            # Process packages in chunks for memory efficiency
            print(f"Starting processing (concurrency: {self.concurrency}, chunk size: {self.CHUNK_SIZE})...", file=sys.stderr)

            for chunk_start in range(0, len(packages), self.CHUNK_SIZE):
                if self._interrupted:
                    break

                chunk_end = min(chunk_start + self.CHUNK_SIZE, len(packages))
                chunk = packages[chunk_start:chunk_end]

                # Check rate limit before processing each chunk
                if not await check_rate_limit():
                    self._interrupted = True
                    break

                # Process this chunk
                tasks = [process_one(pkg) for pkg in chunk]
                await asyncio.gather(*tasks, return_exceptions=True)

                # Flush after each chunk
                await self._flush_pending()

            # Final flush
            await self._flush_pending()

            # Handle completion
            if self._interrupted:
                self.progress.mark_interrupted()
                print(f"\nBuild interrupted. Processed {self._processed_count}/{total} packages.", file=sys.stderr)
            else:
                self.db.set_metadata("last_build", datetime.now().isoformat())
                self.db.set_metadata("source", TOP_PACKAGES_URL)
                self.progress.mark_completed()

            # Save error log if needed
            error_log_path = None
            if self.failed_packages:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                error_log_path = self.db.db_path.parent / f"build_errors_{timestamp}.json"
                error_log_path.write_text(
                    json.dumps(self.failed_packages, indent=2, ensure_ascii=False),
                    encoding="utf-8"
                )

            await self.close()

            # Error breakdown
            error_breakdown = {}
            for err in self.failed_packages:
                error_type = err.get("error", "unknown")
                error_breakdown[error_type] = error_breakdown.get(error_type, 0) + 1

            return {
                "total": total,
                "success": self._success_count,
                "failed": self._fail_count,
                "skipped": len(existing_packages),
                "error_breakdown": error_breakdown,
                "error_log_path": str(error_log_path) if error_log_path else None,
                "interrupted": self._interrupted,
            }

        finally:
            self._restore_signal_handlers()


async def build_database(
    db_path: Path | str | None = None,
    max_packages: int = 5000,
    concurrency: int = 50,
    progress_callback: Callable | None = None,
    resume: bool = False,
    retry_failed: bool = False,
    incremental: bool = False,  # Kept for backward compatibility, but now default behavior
    rebuild: bool = False,
) -> dict:
    """
    Build the database.

    Default behavior is smart incremental:
    - If database has 500 packages and you request 1000, it adds 500 new ones
    - Use --resume to continue an interrupted build
    - Use --retry-failed to retry failed packages
    - Use --rebuild to force rebuild from scratch

    Args:
        db_path: Path to database file
        max_packages: Target number of packages
        concurrency: Concurrent requests (default: 50)
        progress_callback: Progress callback
        resume: Resume interrupted build
        retry_failed: Retry failed packages
        incremental: (deprecated, always True now)
        rebuild: Force rebuild from scratch

    Returns:
        Build statistics
    """
    db = MappingDatabase(db_path)
    progress = BuildProgress()

    # Handle rebuild
    if rebuild:
        if db.db_path.exists():
            db.db_path.unlink()
        progress.clear()
        print("Force rebuild: cleared old database", file=sys.stderr)

    builder = DatabaseBuilder(db, max_packages, concurrency, progress)

    try:
        return await builder.build(
            progress_callback,
            resume=resume,
            retry_failed=retry_failed,
        )
    finally:
        db.close()


def get_database(db_path: Path | str | None = None) -> MappingDatabase:
    """Get a database instance."""
    return MappingDatabase(db_path)


def get_build_progress() -> BuildProgress:
    """Get the build progress tracker."""
    return BuildProgress()
