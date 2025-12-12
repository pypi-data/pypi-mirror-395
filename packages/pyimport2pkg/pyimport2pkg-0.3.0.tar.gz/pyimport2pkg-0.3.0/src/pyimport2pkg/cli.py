"""
CLI module: Command-line interface for pyimport2pkg.

Provides commands for analyzing projects and managing the mapping database.
"""

import argparse
import asyncio
import sys
from pathlib import Path

from . import __version__
from .scanner import scan_project
from .parser import Parser
from .filter import Filter, detect_python_version
from .mapper import Mapper
from .resolver import Resolver, ResolveStrategy
from .exporter import Exporter
from .database import MappingDatabase, build_database, DEFAULT_DB_PATH


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog="pyimport2pkg",
        description="Reverse mapping from Python imports to pip package names",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # analyze command
    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze Python files/project and output required packages",
    )
    analyze_parser.add_argument(
        "path",
        type=Path,
        help="Path to Python file or project directory",
    )
    analyze_parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Output file path (default: stdout)",
    )
    analyze_parser.add_argument(
        "-f", "--format",
        choices=["requirements", "json", "simple"],
        default="requirements",
        help="Output format (default: requirements)",
    )
    analyze_parser.add_argument(
        "--exclude",
        type=str,
        help="Comma-separated list of directories to exclude",
    )
    analyze_parser.add_argument(
        "--exclude-optional",
        action="store_true",
        help="Exclude optional packages (from conditional/try-except imports)",
    )
    analyze_parser.add_argument(
        "--python-version",
        type=str,
        help="Target Python version (e.g., 3.8)",
    )
    analyze_parser.add_argument(
        "--no-comments",
        action="store_true",
        help="Don't include comments in output",
    )
    analyze_parser.add_argument(
        "--use-database",
        action="store_true",
        help="Use the mapping database for lookups",
    )

    # build-db command
    builddb_parser = subparsers.add_parser(
        "build-db",
        help="Build/update the mapping database from PyPI",
        description="""
Build or expand the mapping database from PyPI.

Default behavior (smart incremental):
  - If database has 500 packages and you request --max-packages 1000,
    it adds the 500 new packages automatically.
  - No need for special flags to expand an existing database.

Examples:
  pyimport2pkg build-db                    # Build with 5000 packages
  pyimport2pkg build-db --max-packages 10000  # Expand to 10000 packages
  pyimport2pkg build-db --resume           # Continue interrupted build
  pyimport2pkg build-db --retry-failed     # Retry failed packages
  pyimport2pkg build-db --rebuild          # Force rebuild from scratch
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    builddb_parser.add_argument(
        "--max-packages",
        type=int,
        default=5000,
        help="Target number of packages (default: 5000)",
    )
    builddb_parser.add_argument(
        "--concurrency",
        type=int,
        default=50,
        help="Concurrent requests (default: 50)",
    )
    builddb_parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume from last interrupted build",
    )
    builddb_parser.add_argument(
        "--retry-failed",
        action="store_true",
        help="Retry packages that failed in the last build",
    )
    builddb_parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Force rebuild: delete existing database and start fresh",
    )
    builddb_parser.add_argument(
        "--db-path",
        type=Path,
        help="Database file path",
    )

    # db-info command
    subparsers.add_parser(
        "db-info",
        help="Show database information",
    )

    # build-status command
    subparsers.add_parser(
        "build-status",
        help="Show current build progress status",
    )

    # query command
    query_parser = subparsers.add_parser(
        "query",
        help="Query module-to-package mapping",
    )
    query_parser.add_argument(
        "module",
        type=str,
        help="Module name to query",
    )

    return parser


def parse_python_version(version_str: str | None) -> tuple[int, int] | None:
    """Parse Python version string to tuple."""
    if not version_str:
        return None

    try:
        parts = version_str.split(".")
        return (int(parts[0]), int(parts[1]))
    except (ValueError, IndexError):
        return None


def analyze_project(args: argparse.Namespace) -> int:
    """Run the analyze command."""
    path = args.path.resolve()

    if not path.exists():
        print(f"Error: Path '{path}' does not exist", file=sys.stderr)
        return 1

    # Parse exclusions
    exclude_dirs = set()
    if args.exclude:
        exclude_dirs = set(args.exclude.split(","))

    # Scan for Python files
    print(f"Scanning {path}...", file=sys.stderr)
    files = scan_project(path, exclude_dirs=exclude_dirs)

    if not files:
        print("No Python files found", file=sys.stderr)
        return 0

    print(f"Found {len(files)} Python files", file=sys.stderr)

    # Parse imports
    parser = Parser()
    all_imports = []
    for file in files:
        imports = parser.parse_file(file)
        all_imports.extend(imports)

    print(f"Found {len(all_imports)} import statements", file=sys.stderr)

    # Filter imports
    python_version = parse_python_version(args.python_version)
    project_root = path if path.is_dir() else path.parent

    # Auto-detect Python version if not specified
    if python_version is None:
        detected_version = detect_python_version(project_root)
        if detected_version:
            python_version = detected_version
            print(f"Detected Python version: {python_version[0]}.{python_version[1]}", file=sys.stderr)

    filter_ = Filter(
        project_root=project_root,
        python_version=python_version,
    )
    third_party, filtered = filter_.filter_imports(all_imports)

    # Collect error imports from filtered list (syntax errors, read errors, dynamic imports)
    error_imports = [imp for imp in filtered if imp.module_name.startswith("<")]

    print(f"Identified {len(third_party)} third-party imports", file=sys.stderr)

    # Map imports to packages
    database = None
    if args.use_database:
        db = MappingDatabase()
        if db.exists():
            database = db
        else:
            print("Warning: Database not found. Run 'build-db' first.", file=sys.stderr)

    mapper = Mapper(database=database)
    results = mapper.map_imports(third_party)

    # Resolve conflicts
    resolver = Resolver(strategy=ResolveStrategy.MOST_POPULAR)
    results = resolver.resolve_all(results)

    # Split by optional status
    required = [r for r in results if not r.import_info.is_optional]
    optional = [r for r in results if r.import_info.is_optional]

    # Collect warnings only from packages that will be included
    warnings = []
    for result in required:
        warnings.extend(result.import_info.warnings)
    if not args.exclude_optional:
        for result in optional:
            warnings.extend(result.import_info.warnings)

    # Export
    exporter = Exporter(
        include_optional=not args.exclude_optional,
        include_comments=not args.no_comments,
    )

    if args.format == "requirements":
        content = exporter.export_requirements_txt(
            required, optional, warnings,
            errors=error_imports,
            output=args.output,
        )
    elif args.format == "json":
        content = exporter.export_json(
            required, optional, warnings=warnings,
            output=args.output,
        )
    else:  # simple
        packages = exporter.export_simple_list(required)
        content = "\n".join(packages)
        if args.output:
            args.output.write_text(content)

    if not args.output:
        print(content)

    # Summary
    unique_packages = len(exporter._get_unique_packages(required))
    print(f"\nIdentified {unique_packages} unique packages", file=sys.stderr)

    if database:
        database.close()

    return 0


def build_db_command(args: argparse.Namespace) -> int:
    """Run the build-db command."""
    from .database import get_build_progress, MappingDatabase

    db_path = args.db_path or DEFAULT_DB_PATH
    progress = get_build_progress()

    # Validate conflicting options
    if args.resume and args.rebuild:
        print("错误: --resume 和 --rebuild 不能同时使用", file=sys.stderr)
        return 1

    # Handle --resume: check if there's something to resume
    if args.resume:
        if not progress.has_incomplete_build():
            print("没有中断的构建可以恢复。", file=sys.stderr)
            print("提示: 直接运行 build-db --max-packages N 即可扩展数据库", file=sys.stderr)
            return 1
        status = progress.get_status()
        print(f"恢复中断的构建...")
        print(f"  上次进度: {status['processed']}/{status['total']} 已处理")
        print(f"  失败数: {status['failed']}")

    # Handle --retry-failed
    elif args.retry_failed:
        failed_list = progress.get_failed()
        if not failed_list:
            print("没有失败的包需要重试。", file=sys.stderr)
            return 1
        print(f"进度文件中有 {len(failed_list)} 个失败记录")

    # Handle --rebuild
    elif args.rebuild:
        print(f"强制重建数据库...")

    # Default: smart incremental
    else:
        db = MappingDatabase(db_path)
        if db.exists():
            existing_count = db.get_stats()["packages"]
            print(f"数据库已有 {existing_count} 个包")
            print(f"目标: top {args.max_packages} 个包")
            db.close()
        else:
            print(f"创建新数据库: {db_path}")
            print(f"目标: top {args.max_packages} 个包")

    async def run():
        return await build_database(
            db_path=db_path,
            max_packages=args.max_packages,
            concurrency=args.concurrency,
            resume=args.resume,
            retry_failed=args.retry_failed,
            rebuild=args.rebuild,
        )

    stats = asyncio.run(run())

    # Check for special messages
    if stats.get('message'):
        print(stats['message'])
        return 0

    # Check if interrupted
    if stats.get('interrupted'):
        print(f"\n构建被中断。")
        print(f"  已处理: {stats['success'] + stats['failed']}")
        print(f"  成功: {stats['success']}")
        print(f"  失败: {stats['failed']}")
        print("\n可以使用以下命令继续:")
        print("  pyimport2pkg build-db --resume        # 继续处理剩余的包")
        print("  pyimport2pkg build-db --retry-failed  # 只重试失败的包")
        return 1

    print(f"\n构建完成!")
    print(f"  本次处理: {stats['total']}")
    print(f"  成功: {stats['success']}")
    print(f"  失败: {stats['failed']}")
    if stats.get('skipped', 0) > 0:
        print(f"  跳过 (已存在): {stats['skipped']}")

    # Show error breakdown if there were failures
    if stats.get('error_breakdown'):
        print(f"\n错误类型统计:")
        for error_type, count in stats['error_breakdown'].items():
            print(f"  - {error_type}: {count}")

    if stats.get('error_log_path'):
        print(f"\n详细错误日志: {stats['error_log_path']}")

    # Show final database stats
    db = MappingDatabase(db_path)
    if db.exists():
        final_stats = db.get_stats()
        print(f"\n数据库统计:")
        print(f"  总包数: {final_stats['packages']}")
        print(f"  模块映射数: {final_stats['mappings']}")
        db.close()

    return 0


def db_info_command(args: argparse.Namespace) -> int:
    """Run the db-info command."""
    db = MappingDatabase()

    if not db.exists():
        print("Database not found. Run 'build-db' to create it.")
        return 1

    stats = db.get_stats()
    db.close()

    print("Database Information:")
    print(f"  Path: {stats['db_path']}")
    print(f"  Packages: {stats['packages']}")
    print(f"  Module mappings: {stats['mappings']}")
    print(f"  Unique modules: {stats['unique_modules']}")
    print(f"  Last updated: {stats['last_updated'] or 'Unknown'}")

    return 0


def build_status_command(args: argparse.Namespace) -> int:
    """Run the build-status command."""
    from .database import get_build_progress

    progress = get_build_progress()
    status = progress.get_status()

    if status['status'] == 'none':
        print("没有构建记录。")
        return 0

    print("构建状态:")
    print(f"  状态: {status['status']}")
    print(f"  总包数: {status['total']}")
    print(f"  已处理: {status['processed']}")
    print(f"  失败数: {status['failed']}")
    print(f"  开始时间: {status['started_at']}")
    print(f"  最后更新: {status['last_updated']}")

    if status['status'] == 'interrupted':
        remaining = status['total'] - status['processed']
        print(f"\n未处理: {remaining} 个包")
        print("\n可用命令:")
        print("  pyimport2pkg build-db --resume        # 继续处理")
        print("  pyimport2pkg build-db --retry-failed  # 重试失败的包")

    if status['failed'] > 0:
        failed_list = progress.get_failed()
        print(f"\n失败的包 (前10个):")
        for pkg in failed_list[:10]:
            print(f"  - {pkg}")
        if len(failed_list) > 10:
            print(f"  ... 还有 {len(failed_list) - 10} 个")

    return 0


def query_command(args: argparse.Namespace) -> int:
    """Run the query command."""
    from .models import ImportInfo

    module_name = args.module

    # First check hardcoded mappings
    mapper = Mapper()
    imp = ImportInfo.from_module_name(module_name)
    result = mapper.map_import(imp)

    print(f"Module: {module_name}")
    print(f"Source: {result.source}")

    if result.candidates:
        print("Candidates:")
        for i, candidate in enumerate(result.candidates):
            marker = " (recommended)" if candidate.is_recommended else ""
            downloads = f" [{candidate.download_count:,} downloads]" if candidate.download_count else ""
            print(f"  {i+1}. {candidate.package_name}{marker}{downloads}")
    else:
        print("No mapping found")

    return 0


def main(argv: list[str] | None = None) -> int:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 0

    if args.command == "analyze":
        return analyze_project(args)
    elif args.command == "build-db":
        return build_db_command(args)
    elif args.command == "db-info":
        return db_info_command(args)
    elif args.command == "build-status":
        return build_status_command(args)
    elif args.command == "query":
        return query_command(args)

    return 0


if __name__ == "__main__":
    sys.exit(main())
