"""
Markdown formatter for QueryNL CLI

Provides GitHub-flavored markdown table output with column alignment.
"""

from typing import Dict, Any, List, Literal
from rich.console import Console

console = Console()


def format_markdown_table(
    rows: List[Dict[str, Any]],
    alignment: Literal["left", "right", "center"] = "left",
    max_column_width: int = 50
) -> str:
    """
    Format query results as GitHub-flavored markdown table.

    Args:
        rows: List of row dictionaries (column_name -> value)
        alignment: Column alignment (left, right, center)
        max_column_width: Maximum column width (truncate if longer)

    Returns:
        Markdown table string
    """
    if not rows:
        return "_No rows returned_\n"

    # Get column names from first row
    headers = list(rows[0].keys())

    # Calculate column widths
    col_widths = {}
    for header in headers:
        col_widths[header] = min(
            max(len(str(header)), max(len(str(row.get(header, ""))) for row in rows)),
            max_column_width
        )

    lines = []

    # Header row
    header_cells = []
    for header in headers:
        cell = str(header)[:max_column_width]
        header_cells.append(cell)

    lines.append("| " + " | ".join(header_cells) + " |")

    # Separator row with alignment
    separator_cells = []
    for header in headers:
        if alignment == "left":
            sep = ":---"
        elif alignment == "right":
            sep = "---:"
        elif alignment == "center":
            sep = ":---:"
        else:
            sep = "---"

        # Pad separator to column width
        width = col_widths[header]
        if len(sep) < width:
            if alignment == "center":
                sep = ":" + "-" * (width - 2) + ":"
            elif alignment == "right":
                sep = "-" * (width - 1) + ":"
            else:
                sep = ":" + "-" * (width - 1)

        separator_cells.append(sep)

    lines.append("| " + " | ".join(separator_cells) + " |")

    # Data rows
    for row in rows:
        row_cells = []
        for header in headers:
            value = row.get(header)
            cell = str(value) if value is not None else ""

            # Truncate if too long
            if len(cell) > max_column_width:
                cell = cell[:max_column_width - 3] + "..."

            # Escape markdown special characters
            cell = cell.replace("|", "\\|").replace("\n", " ")

            row_cells.append(cell)

        lines.append("| " + " | ".join(row_cells) + " |")

    return "\n".join(lines) + "\n"


def print_markdown(
    result: Dict[str, Any],
    alignment: Literal["left", "right", "center"] = "left",
    show_metadata: bool = True,
    max_column_width: int = 50
) -> None:
    """
    Print query results as markdown table to console.

    Args:
        result: Query result dictionary with rows
        alignment: Column alignment
        show_metadata: Show row count and execution time
        max_column_width: Maximum column width
    """
    rows = result.get("rows", [])

    if not rows:
        console.print("_No rows returned_")
        return

    markdown = format_markdown_table(rows, alignment, max_column_width)
    console.print(markdown)

    if show_metadata:
        row_count = result.get("row_count", len(rows))
        execution_time = result.get("execution_time_ms", 0)
        console.print(f"\n_Rows: {row_count}, Execution time: {execution_time}ms_")


def save_markdown_to_file(
    result: Dict[str, Any],
    file_path: str,
    alignment: Literal["left", "right", "center"] = "left",
    include_metadata: bool = True,
    max_column_width: int = 50
) -> None:
    """
    Save query results as markdown table to file.

    Args:
        result: Query result dictionary
        file_path: Path to output file
        alignment: Column alignment
        include_metadata: Include row count and execution time
        max_column_width: Maximum column width
    """
    rows = result.get("rows", [])

    markdown = format_markdown_table(rows, alignment, max_column_width)

    if include_metadata:
        row_count = result.get("row_count", len(rows))
        execution_time = result.get("execution_time_ms", 0)
        markdown += f"\n_Rows: {row_count}, Execution time: {execution_time}ms_\n"

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(markdown)


def format_markdown_code_block(
    content: str,
    language: str = "sql"
) -> str:
    """
    Format content as markdown code block.

    Args:
        content: Code content
        language: Language for syntax highlighting

    Returns:
        Markdown code block string
    """
    return f"```{language}\n{content}\n```\n"


def format_markdown_list(
    items: List[str],
    ordered: bool = False
) -> str:
    """
    Format list as markdown.

    Args:
        items: List items
        ordered: Use ordered list (1. 2. 3.) vs unordered (- - -)

    Returns:
        Markdown list string
    """
    lines = []
    for i, item in enumerate(items, start=1):
        if ordered:
            lines.append(f"{i}. {item}")
        else:
            lines.append(f"- {item}")

    return "\n".join(lines) + "\n"


def format_markdown_heading(
    text: str,
    level: int = 1
) -> str:
    """
    Format text as markdown heading.

    Args:
        text: Heading text
        level: Heading level (1-6)

    Returns:
        Markdown heading string
    """
    level = max(1, min(6, level))  # Clamp to 1-6
    return f"{'#' * level} {text}\n"


def format_markdown_link(
    text: str,
    url: str,
    title: str = None
) -> str:
    """
    Format markdown link.

    Args:
        text: Link text
        url: URL
        title: Optional title attribute

    Returns:
        Markdown link string
    """
    if title:
        return f'[{text}]({url} "{title}")'
    return f"[{text}]({url})"
