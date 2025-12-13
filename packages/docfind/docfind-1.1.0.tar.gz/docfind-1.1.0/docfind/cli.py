"""
Command-line interface for docfind.

Provides commands for indexing, searching, and managing the document index.
"""

import argparse
import sys
import json
import logging
from pathlib import Path
from typing import Optional

from . import __version__
from .db import DatabaseManager
from .indexer import DocumentIndexer
from .search import SearchEngine
from .utils import (
    Config,
    get_default_db_path,
    setup_logging,
    get_data_dir,
    format_size,
    check_ripgrep_version,
    is_system_path,
)

logger = logging.getLogger(__name__)


def cmd_index(args):
    """Index command handler."""
    root_path = Path(args.path).resolve()

    if not root_path.exists():
        print(f"Error: Path does not exist: {root_path}", file=sys.stderr)
        return 1

    # Check for system paths
    if is_system_path(root_path) and not args.force:
        print(f"Warning: {root_path} appears to be a system path.", file=sys.stderr)
        response = input("Are you sure you want to index this path? [y/N]: ")
        if response.lower() != "y":
            print("Indexing cancelled.")
            return 0

    # Load config
    config = Config()

    # Get database path
    db_path = Path(args.database) if args.database else Path(config["db_path"])

    # Initialize database
    db = DatabaseManager(db_path)

    # Create indexer
    indexer = DocumentIndexer(
        db=db,
        max_file_size=args.max_size or config["max_file_size"],
        trust_external_tools=args.trust_external_tools
        or config["trust_external_tools"],
        ignore_patterns=config["ignore_globs"],
    )

    # Progress callback
    def progress_callback(progress):
        if args.verbose or args.progress:
            stats = progress.get_stats()
            print(
                f"\rProgress: {stats['processed_files']}/{stats['total_files']} files "
                f"({stats['successful']} ok, {stats['failed']} errors) - {stats['current_file'][:60]}",
                end="",
                flush=True,
            )

    try:
        # Run indexing
        print(f"Indexing: {root_path}")
        progress = indexer.index_directory(
            root_path=root_path,
            reindex=args.reindex,
            threads=args.threads or config["threads"],
            progress_callback=progress_callback,
        )

        if args.progress:
            print()  # New line after progress

        # Print results
        stats = progress.get_stats()
        print(f"\nIndexing complete:")
        print(f"  Total files: {stats['total_files']}")
        print(f"  Successful: {stats['successful']}")
        print(f"  Failed: {stats['failed']}")
        print(f"  Skipped: {stats['skipped']}")
        print(f"  Data processed: {format_size(stats['bytes_processed'])}")
        print(
            f"  Time: {stats['elapsed_seconds']:.1f}s ({stats['files_per_second']:.1f} files/s)"
        )

        if stats["errors"] and args.verbose:
            print(f"\nRecent errors:")
            for error in stats["errors"][-5:]:
                print(f"  {error['file']}: {error['error']}")

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback

            traceback.print_exc()
        return 1


def cmd_search(args):
    """Search command handler."""
    # Load config
    config = Config()

    # Get database path
    db_path = Path(args.database) if args.database else Path(config["db_path"])

    if not db_path.exists():
        print(f"Error: Database not found: {db_path}", file=sys.stderr)
        print("Run 'docfind index' first to create an index.", file=sys.stderr)
        return 1

    # Initialize database and search engine
    db = DatabaseManager(db_path)
    search = SearchEngine(db)

    # Run search
    try:
        results = search.search(
            query=args.query,
            use_ripgrep=args.use_ripgrep,
            case_sensitive=args.case_sensitive,
            regex=args.regex,
            whole_word=args.whole_word,
            root_path=args.root,
            limit=args.limit,
            offset=args.offset,
        )

        # Output results
        if args.json:
            # JSON output
            for result in results:
                print(json.dumps(result))
        else:
            # Human-readable output
            if not results:
                print("No results found.")
                return 0

            print(f"Found {len(results)} results:\n")

            for i, result in enumerate(results, 1):
                path = result.get("path", "unknown")
                source_type = result.get("source_type", "unknown")
                snippet = result.get("snippet", "")
                line = result.get("line", "")

                print(f"{i}. {path} ({source_type})")

                if line:
                    print(f"   Line {line}: {snippet[:100]}")
                else:
                    print(f"   {snippet[:100]}")

                print()

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback

            traceback.print_exc()
        return 1


def cmd_list(args):
    """List indexed roots command handler."""
    # Load config
    config = Config()

    # Get database path
    db_path = Path(args.database) if args.database else Path(config["db_path"])

    if not db_path.exists():
        print(f"Error: Database not found: {db_path}", file=sys.stderr)
        return 1

    db = DatabaseManager(db_path)

    roots = db.get_roots()

    if not roots:
        print("No indexed paths.")
        return 0

    if args.json:
        data = [{"root": r[0], "count": r[1], "last_indexed": r[2]} for r in roots]
        print(json.dumps(data, indent=2))
    else:
        print("Indexed paths:\n")
        for root, count, last_indexed in roots:
            from datetime import datetime

            dt = datetime.fromtimestamp(last_indexed)
            print(f"  {root}")
            print(f"    Documents: {count}")
            print(f"    Last indexed: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
            print()

    return 0


def cmd_stats(args):
    """Statistics command handler."""
    # Load config
    config = Config()

    # Get database path
    db_path = Path(args.database) if args.database else Path(config["db_path"])

    if not db_path.exists():
        print(f"Error: Database not found: {db_path}", file=sys.stderr)
        return 1

    db = DatabaseManager(db_path)
    stats = db.get_stats()

    if args.json:
        print(json.dumps(stats, indent=2))
    else:
        print("Database Statistics:\n")
        print(f"  Total documents: {stats.get('total_docs', 0)}")
        print(f"  Total size: {format_size(stats.get('total_size', 0) or 0)}")
        print(f"  Indexed roots: {stats.get('root_count', 0)}")
        print(f"  Errors: {stats.get('error_count', 0)}")

        by_type = stats.get("by_type", {})
        if by_type:
            print(f"\n  By file type:")
            for file_type, count in sorted(
                by_type.items(), key=lambda x: x[1], reverse=True
            ):
                print(f"    {file_type}: {count}")

    return 0


def cmd_explain(args):
    """Explain command handler."""
    # Load config
    config = Config()

    # Get database path
    db_path = Path(args.database) if args.database else Path(config["db_path"])

    if not db_path.exists():
        print(f"Error: Database not found: {db_path}", file=sys.stderr)
        return 1

    db = DatabaseManager(db_path)

    if args.query:
        # Explain query
        search = SearchEngine(db)
        explanation = search.explain_search(args.query)

        print(json.dumps(explanation, indent=2))

    else:
        # Explain document
        doc = db.get_document_by_path(args.path)

        if not doc:
            print(f"Error: Document not found: {args.path}", file=sys.stderr)
            return 1

        # Remove large text field for display
        display_doc = {k: v for k, v in doc.items() if k != "extracted_text"}

        if args.show_text:
            display_doc["extracted_text_preview"] = doc.get("extracted_text", "")[:500]

        print(json.dumps(display_doc, indent=2))

    return 0


def cmd_remove(args):
    """Remove command handler."""
    # Load config
    config = Config()

    # Get database path
    db_path = Path(args.database) if args.database else Path(config["db_path"])

    if not db_path.exists():
        print(f"Error: Database not found: {db_path}", file=sys.stderr)
        return 1

    db = DatabaseManager(db_path)

    if args.all:
        if not args.force:
            response = input("Remove all indexed documents? [y/N]: ")
            if response.lower() != "y":
                print("Cancelled.")
                return 0

        # Delete database file
        db.close()
        db_path.unlink()
        print(f"Removed database: {db_path}")

    else:
        # Remove specific root
        db.delete_by_root(args.path)
        print(f"Removed index for: {args.path}")

    return 0


def cmd_optimize(args):
    """Optimize command handler."""
    # Load config
    config = Config()

    # Get database path
    db_path = Path(args.database) if args.database else Path(config["db_path"])

    if not db_path.exists():
        print(f"Error: Database not found: {db_path}", file=sys.stderr)
        return 1

    db = DatabaseManager(db_path)

    print("Optimizing database...")
    db.optimize()
    print("Optimization complete.")

    return 0


def cmd_doctor(args):
    """Doctor command handler - check system configuration."""
    print("DocFind System Check\n")

    # Python version
    print(f"Python version: {sys.version.split()[0]}")

    # Config
    config = Config()
    print(f"Config file: {config.config_path}")
    print(f"Database: {config['db_path']}")

    # Check database
    db_path = Path(config["db_path"])
    if db_path.exists():
        print(f"Database size: {format_size(db_path.stat().st_size)}")

        db = DatabaseManager(db_path)
        stats = db.get_stats()
        print(f"Documents indexed: {stats.get('total_docs', 0)}")
    else:
        print("Database: Not created yet")

    # Check ripgrep
    print()
    rg_version = check_ripgrep_version()
    if rg_version:
        print(f"ripgrep: {rg_version}")
    else:
        print("ripgrep: Not found (optional)")

    # Check dependencies
    print("\nDependencies:")

    deps = [
        ("pdfminer", "pdfminer.six", "PDF extraction"),
        ("docx", "python-docx", "DOCX extraction"),
        ("openpyxl", "openpyxl", "XLSX extraction"),
        ("pptx", "python-pptx", "PPTX extraction"),
        ("bs4", "beautifulsoup4", "HTML/XML extraction"),
        ("lxml", "lxml", "XML parsing"),
    ]

    for module_name, package_name, purpose in deps:
        try:
            __import__(module_name)
            print(f"  {package_name}: OK ({purpose})")
        except ImportError:
            print(f"  {package_name}: MISSING ({purpose})")

    print("\nAll checks complete.")

    return 0


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="DocFind - Document indexing and search tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("--version", action="version", version=f"docfind {__version__}")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("-d", "--database", help="Database file path")

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Index command
    parser_index = subparsers.add_parser("index", help="Index documents")
    parser_index.add_argument("path", help="Directory to index")
    parser_index.add_argument(
        "-r", "--reindex", action="store_true", help="Reindex existing files"
    )
    parser_index.add_argument("-t", "--threads", type=int, help="Number of threads")
    parser_index.add_argument("--max-size", type=int, help="Maximum file size (bytes)")
    parser_index.add_argument(
        "--trust-external-tools", action="store_true", help="Trust external converters"
    )
    parser_index.add_argument("--progress", action="store_true", help="Show progress")
    parser_index.add_argument("--force", action="store_true", help="Skip confirmations")
    parser_index.set_defaults(func=cmd_index)

    # Search command
    parser_search = subparsers.add_parser("search", help="Search documents")
    parser_search.add_argument("query", help="Search query")
    parser_search.add_argument(
        "-i", "--case-sensitive", action="store_true", help="Case-sensitive search"
    )
    parser_search.add_argument(
        "-e", "--regex", action="store_true", help="Regex search"
    )
    parser_search.add_argument(
        "-w", "--whole-word", action="store_true", help="Whole word search"
    )
    parser_search.add_argument(
        "-g", "--use-ripgrep", action="store_true", help="Use ripgrep"
    )
    parser_search.add_argument("-r", "--root", help="Filter by root path")
    parser_search.add_argument(
        "-l", "--limit", type=int, default=100, help="Result limit"
    )
    parser_search.add_argument(
        "-o", "--offset", type=int, default=0, help="Result offset"
    )
    parser_search.add_argument("-j", "--json", action="store_true", help="JSON output")
    parser_search.set_defaults(func=cmd_search)

    # List command
    parser_list = subparsers.add_parser("list", help="List indexed paths")
    parser_list.add_argument("-j", "--json", action="store_true", help="JSON output")
    parser_list.set_defaults(func=cmd_list)

    # Stats command
    parser_stats = subparsers.add_parser("stats", help="Show statistics")
    parser_stats.add_argument("-j", "--json", action="store_true", help="JSON output")
    parser_stats.set_defaults(func=cmd_stats)

    # Explain command
    parser_explain = subparsers.add_parser("explain", help="Explain query or document")
    group = parser_explain.add_mutually_exclusive_group(required=True)
    group.add_argument("-q", "--query", help="Explain query")
    group.add_argument("-p", "--path", help="Explain document")
    parser_explain.add_argument(
        "--show-text", action="store_true", help="Show extracted text preview"
    )
    parser_explain.set_defaults(func=cmd_explain)

    # Remove command
    parser_remove = subparsers.add_parser("remove", help="Remove indexed data")
    group = parser_remove.add_mutually_exclusive_group(required=True)
    group.add_argument("-p", "--path", help="Root path to remove")
    group.add_argument("-a", "--all", action="store_true", help="Remove all data")
    parser_remove.add_argument("--force", action="store_true", help="Skip confirmation")
    parser_remove.set_defaults(func=cmd_remove)

    # Optimize command
    parser_optimize = subparsers.add_parser("optimize", help="Optimize database")
    parser_optimize.set_defaults(func=cmd_optimize)

    # Doctor command
    parser_doctor = subparsers.add_parser("doctor", help="Check system configuration")
    parser_doctor.set_defaults(func=cmd_doctor)

    # Parse arguments
    args = parser.parse_args()

    # Setup logging
    log_file = get_data_dir() / "docfind.log"
    setup_logging(log_file=log_file, verbose=args.verbose)

    # Execute command
    if not args.command:
        parser.print_help()
        return 0

    try:
        return args.func(args)
    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback

            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
