"""
Table formatter for QueryNL CLI

Uses Rich to create beautiful ASCII tables with proper column alignment.
Automatically detects TTY and disables colors/formatting when piping output.
"""

import sys
from typing import List, Dict, Any
from rich.console import Console
from rich.table import Table

# Auto-detect TTY for proper automation support
console = Console(force_terminal=sys.stdout.isatty() if hasattr(sys.stdout, 'isatty') else False)


def format_table(rows: List[Dict[str, Any]], title: str = None) -> Table:
    """
    Format query results as a Rich table.

    Args:
        rows: List of row dictionaries (column_name -> value)
        title: Optional table title

    Returns:
        Rich Table object
    """
    if not rows:
        table = Table(title=title or "Query Results")
        table.add_column("(no results)", style="dim")
        return table

    # Create table with automatic column detection
    table = Table(title=title, show_header=True, header_style="bold cyan")

    # Add columns from first row
    first_row = rows[0]
    for column_name in first_row.keys():
        table.add_column(str(column_name), style="white")

    # Add rows
    for row in rows:
        values = [str(value) if value is not None else "[dim]NULL[/dim]" for value in row.values()]
        table.add_row(*values)

    return table


def print_table(rows: List[Dict[str, Any]], title: str = None, show_metadata: bool = True) -> None:
    """
    Print formatted table to console.

    Args:
        rows: List of row dictionaries
        title: Optional table title
        show_metadata: Whether to show row count and execution time
    """
    table = format_table(rows, title)
    console.print(table)

    if show_metadata:
        console.print(f"\n[dim]{len(rows)} row{'s' if len(rows) != 1 else ''} returned[/dim]")


def print_results(result: Dict[str, Any], format_type: str = "table") -> None:
    """
    Print query results in specified format.

    Args:
        result: Query result dictionary with rows, row_count, execution_time_ms
        format_type: Output format (table, json, csv, markdown, tsv)
    """
    rows = result.get("rows", [])
    row_count = result.get("row_count", len(rows))
    execution_time = result.get("execution_time_ms", 0)

    if format_type == "table":
        print_table(rows, show_metadata=False)
        console.print(f"\n[dim]{row_count} row{'s' if row_count != 1 else ''} returned ({execution_time}ms)[/dim]")

    elif format_type == "json":
        from .json_formatter import print_json
        print_json(result, include_metadata=True)

    elif format_type == "csv":
        from .csv_formatter import print_csv
        print_csv(result, include_headers=True, show_metadata=True)

    elif format_type == "tsv":
        from .csv_formatter import print_tsv
        print_tsv(result, include_headers=True)

    elif format_type == "markdown":
        from .markdown_formatter import print_markdown
        print_markdown(result, alignment="left", show_metadata=True)

    else:
        console.print(f"[yellow]Unknown format: {format_type}[/yellow]")
        console.print("Supported formats: table, json, csv, tsv, markdown")
