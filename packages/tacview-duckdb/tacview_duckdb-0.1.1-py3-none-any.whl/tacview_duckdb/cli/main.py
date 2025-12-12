"""Command-line interface for py-tacview-duckdb."""

import argparse
import sys
from pathlib import Path

from ..api import parse_acmi
from ..storage.duckdb_store import DuckDBStore
from ..__version__ import __version__

# Load .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, env vars must be set manually


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="tacview-parse",
        description="Parse Tacview ACMI files into DuckDB database",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Parse ACMI file (auto-detects product, DCS recordings enable 7 enrichments)
  tacview-parse recording.acmi -o timeline_data/

  # Parse with async enrichments (immediate querying)
  tacview-parse recording.acmi --async

  # Parse with specific enrichments
  tacview-parse recording.acmi --enrich weapons,coalitions,missed_weapons

  # Parse without enrichments (fast)
  tacview-parse recording.acmi --no-enrich

  # Show summary
  tacview-parse recording.acmi --summary

  # Query database
  tacview-parse timeline_data/a3f5d9c2b1e8f4a7.duckdb --query "SELECT COUNT(*) FROM objects"

  # Open interactive shell
  tacview-parse timeline_data/a3f5d9c2b1e8f4a7.duckdb --shell
        """,
    )

    parser.add_argument("input", help="ACMI file or database path")
    parser.add_argument(
        "-o",
        "--output",
        default="timeline_data",
        help="Output directory for database (default: timeline_data)",
    )
    parser.add_argument(
        "--enrich",
        help="Comma-separated list of enrichments (e.g., weapons,containers,ejections,decoys,missed_weapons,coalitions,takeoff_landing). If not specified, uses product-specific defaults (DCS recordings auto-enable all 7 enrichments)",
    )
    parser.add_argument(
        "--no-enrich",
        action="store_true",
        help="Disable all enrichments",
    )
    parser.add_argument(
        "--async",
        "--async-enrichments",
        dest="async_enrichments",
        action="store_true",
        help="Run enrichments in background thread (experimental, allows immediate querying)",
    )
    parser.add_argument(
        "--keep",
        action="store_true",
        help="Keep existing database if it exists (default: drop and recreate)",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Show database summary",
    )
    parser.add_argument(
        "--query",
        help="Execute SQL query on database",
    )
    parser.add_argument(
        "--shell",
        action="store_true",
        help="Open interactive database shell",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show verbose output",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    args = parser.parse_args()

    try:
        # Check if input is a database file
        input_path = Path(args.input)
        is_database = input_path.suffix == ".duckdb"

        if is_database:
            # Working with existing database
            if not input_path.exists():
                print(f"Error: Database not found: {input_path}", file=sys.stderr)
                return 1

            store = DuckDBStore.from_path(input_path)

            if args.summary or (not args.query and not args.shell):
                show_summary(store)

            if args.query:
                execute_query(store, args.query)

            if args.shell:
                open_shell(store)

        else:
            # Parsing ACMI file
            if not input_path.exists():
                print(f"Error: File not found: {input_path}", file=sys.stderr)
                return 1

            # Parse enrichments
            # Default is None = use product-specific defaults (DCS auto-enables 7 enrichments)
            enrichments = None  # default: auto-detect based on product
            
            if args.no_enrich:
                enrichments = []  # Explicitly disable all enrichments
            elif args.enrich:
                enrichments = [e.strip() for e in args.enrich.split(",")]

            # Parse ACMI
            store = parse_acmi(
                input_path,
                output_dir=args.output,
                enrichments=enrichments,
                async_enrichments=args.async_enrichments,
                progress=args.verbose,
                drop_existing=not args.keep,
            )

            # Handle async enrichments - always wait for completion in CLI
            if args.async_enrichments:
                if args.verbose:
                    print("Waiting for background enrichments to complete...")
                store.wait_for_enrichments()
                if args.verbose:
                    print("Enrichments complete!")

            if args.summary or args.verbose:
                show_summary(store)

            if args.query:
                execute_query(store, args.query)

            if args.shell:
                open_shell(store)

            if not args.verbose:
                print(f"Database created: {Path(store.database_path).name}")
                print(f"Full path: {store.database_path}")

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback

            traceback.print_exc()
        return 1


def show_summary(store: DuckDBStore):
    """Show database summary."""
    summary = store.get_summary()

    print("\n=== Database Summary ===")
    print(f"Objects: {summary.get('object_count', 0)}")
    print(f"States: {summary.get('state_count', 0)}")

    if "start_time" in summary:
        print(f"Time Range: {summary['start_time']:.2f}s - {summary['end_time']:.2f}s")
        print(f"Duration: {summary['duration']:.2f}s")

    if "metadata" in summary and summary["metadata"]:
        print("\n=== Metadata ===")
        for key, value in summary["metadata"].items():
            print(f"{key}: {value}")

    print()


def execute_query(store: DuckDBStore, query: str):
    """Execute SQL query and print results."""
    try:
        results = store.query_sql(query)

        if not results:
            print("No results")
            return

        # Print as table
        if results:
            # Get column names
            columns = list(results[0].keys())
            
            # Calculate column widths
            col_widths = {col: len(col) for col in columns}
            for row in results:
                for col in columns:
                    value_str = str(row[col])
                    col_widths[col] = max(col_widths[col], len(value_str))

            # Print header
            header = " | ".join(col.ljust(col_widths[col]) for col in columns)
            print(header)
            print("-" * len(header))

            # Print rows
            for row in results:
                print(" | ".join(str(row[col]).ljust(col_widths[col]) for col in columns))

            print(f"\n{len(results)} row(s)")

    except Exception as e:
        print(f"Query error: {e}", file=sys.stderr)


def open_shell(store: DuckDBStore):
    """Open interactive database shell."""
    try:
        import duckdb
    except ImportError:
        print("Error: duckdb package required for shell", file=sys.stderr)
        return

    print(f"\nOpening interactive shell for: {store.database_path}")
    print("Type SQL queries or .exit to quit\n")

    conn = store.get_query_connection()

    while True:
        try:
            query = input("duckdb> ")
            
            if not query.strip():
                continue
                
            if query.strip() in [".exit", ".quit", "exit", "quit"]:
                break

            # Execute query
            result = conn.execute(query).fetchall()
            
            if result:
                # Get column names
                columns = [desc[0] for desc in conn.description]
                
                # Print header
                print(" | ".join(columns))
                print("-" * (sum(len(col) for col in columns) + 3 * (len(columns) - 1)))
                
                # Print rows
                for row in result:
                    print(" | ".join(str(val) for val in row))
                    
                print(f"\n{len(result)} row(s)\n")
            else:
                print("Query executed successfully\n")

        except KeyboardInterrupt:
            print("\nUse .exit to quit")
        except EOFError:
            break
        except Exception as e:
            print(f"Error: {e}\n")

    conn.close()
    print("Goodbye!")


if __name__ == "__main__":
    sys.exit(main())

