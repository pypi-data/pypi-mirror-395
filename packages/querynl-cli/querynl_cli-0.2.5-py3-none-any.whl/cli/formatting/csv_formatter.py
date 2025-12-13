"""
CSV formatter for QueryNL CLI

Provides RFC 4180 compliant CSV output with proper escaping.
"""

import csv
import io
from typing import Dict, Any, List
from rich.console import Console

console = Console()


def format_csv(rows: List[Dict[str, Any]], include_headers: bool = True) -> str:
    """
    Format query results as CSV according to RFC 4180.

    Args:
        rows: List of row dictionaries (column_name -> value)
        include_headers: Include header row with column names

    Returns:
        CSV string with proper escaping
    """
    if not rows:
        return ""

    output = io.StringIO()

    # Get column names from first row
    fieldnames = list(rows[0].keys())

    writer = csv.DictWriter(
        output,
        fieldnames=fieldnames,
        quoting=csv.QUOTE_MINIMAL,
        lineterminator='\n'
    )

    if include_headers:
        writer.writeheader()

    # Write rows, converting None to empty string
    for row in rows:
        clean_row = {
            key: (value if value is not None else "")
            for key, value in row.items()
        }
        writer.writerow(clean_row)

    return output.getvalue()


def print_csv(
    result: Dict[str, Any],
    include_headers: bool = True,
    show_metadata: bool = False
) -> None:
    """
    Print query results as CSV to console.

    Args:
        result: Query result dictionary with rows
        include_headers: Include header row
        show_metadata: Show row count and execution time as comment
    """
    rows = result.get("rows", [])

    if not rows:
        console.print("[dim]# No rows returned[/dim]")
        return

    # Print metadata as CSV comment
    if show_metadata:
        row_count = result.get("row_count", len(rows))
        execution_time = result.get("execution_time_ms", 0)
        console.print(f"# Rows: {row_count}, Execution time: {execution_time}ms")

    # Print CSV
    csv_output = format_csv(rows, include_headers=include_headers)
    console.print(csv_output, end="")


def save_csv_to_file(
    result: Dict[str, Any],
    file_path: str,
    include_headers: bool = True
) -> None:
    """
    Save query results as CSV to file.

    Args:
        result: Query result dictionary
        file_path: Path to output file
        include_headers: Include header row
    """
    rows = result.get("rows", [])

    if not rows:
        # Write empty file with just headers if no rows
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            if include_headers and result.get("rows") == []:
                # Try to get column names from result metadata
                f.write("")
        return

    csv_content = format_csv(rows, include_headers=include_headers)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(csv_content)


def format_tsv(rows: List[Dict[str, Any]], include_headers: bool = True) -> str:
    """
    Format query results as TSV (Tab-Separated Values).

    Args:
        rows: List of row dictionaries
        include_headers: Include header row

    Returns:
        TSV string
    """
    if not rows:
        return ""

    output = io.StringIO()
    fieldnames = list(rows[0].keys())

    writer = csv.DictWriter(
        output,
        fieldnames=fieldnames,
        delimiter='\t',
        quoting=csv.QUOTE_MINIMAL,
        lineterminator='\n'
    )

    if include_headers:
        writer.writeheader()

    for row in rows:
        clean_row = {
            key: (value if value is not None else "")
            for key, value in row.items()
        }
        writer.writerow(clean_row)

    return output.getvalue()


def print_tsv(result: Dict[str, Any], include_headers: bool = True) -> None:
    """
    Print query results as TSV to console.

    Args:
        result: Query result dictionary
        include_headers: Include header row
    """
    rows = result.get("rows", [])

    if not rows:
        console.print("[dim]# No rows returned[/dim]")
        return

    tsv_output = format_tsv(rows, include_headers=include_headers)
    console.print(tsv_output, end="")
