"""
Core export service for QueryNL CLI

Main entry point for exporting query results to files.
"""

import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable

from .exceptions import (
    ExportError,
    InvalidPathError,
    UnsupportedFormatError,
    EmptyResultError
)
from .file_utils import (
    validate_export_path,
    resolve_file_conflict,
    ensure_parent_directory,
    get_file_size,
    format_file_size
)


class ExportFormat(Enum):
    """Supported export formats."""
    CSV = "csv"
    JSON = "json"
    SQL = "sql"
    MERMAID = "mermaid"
    TXT = "txt"

    @classmethod
    def from_extension(cls, extension: str) -> "ExportFormat":
        """
        Detect format from file extension.

        Args:
            extension: File extension (with or without leading dot)

        Returns:
            Corresponding ExportFormat

        Raises:
            UnsupportedFormatError: If extension is not recognized
        """
        ext = extension.lower().lstrip(".")

        format_map = {
            "csv": cls.CSV,
            "json": cls.JSON,
            "sql": cls.SQL,
            "mmd": cls.MERMAID,
            "mermaid": cls.MERMAID,
            "txt": cls.TXT,
        }

        if ext not in format_map:
            raise UnsupportedFormatError(ext)

        return format_map[ext]


@dataclass
class ExportConfiguration:
    """Configuration for export operation."""

    file_path: Path
    format: ExportFormat
    source_database_type: str = "postgresql"
    overwrite_behavior: str = "auto_rename"
    include_headers: bool = True
    progress_enabled: bool = True
    progress_interval: int = 10000
    pretty_print: bool = False
    batch_size: int = 1000


@dataclass
class ExportResult:
    """Result of export operation."""

    success: bool
    file_path: Optional[Path] = None
    original_path: Optional[Path] = None
    row_count: int = 0
    file_size_bytes: int = 0
    duration_ms: float = 0.0
    format: Optional[ExportFormat] = None
    warnings: List[str] = field(default_factory=list)
    error: Optional[str] = None

    def __str__(self) -> str:
        """Format result as user-friendly message."""
        if not self.success:
            return f"❌ Export failed: {self.error}"

        message = f"✓ Exported {self.row_count} rows to {self.file_path}"

        if self.original_path and self.original_path != self.file_path:
            message += f"\n  (renamed from {self.original_path.name})"

        if self.file_size_bytes > 0:
            size_str = format_file_size(self.file_size_bytes)
            message += f"\n  File size: {size_str}"

        if self.duration_ms > 0:
            message += f" ({self.duration_ms:.0f}ms)"

        if self.warnings:
            message += "\n⚠️  Warnings:"
            for warning in self.warnings:
                message += f"\n  - {warning}"

        return message


def export_to_file(
    result_data: Dict[str, Any],
    file_path: str | Path,
    *,
    format: Optional[ExportFormat] = None,
    database_type: str = "postgresql",
    config: Optional[ExportConfiguration] = None,
    progress_callback: Optional[Callable[[int], None]] = None
) -> ExportResult:
    """
    Export query results to a file.

    Args:
        result_data: Query result dictionary with 'rows' key
        file_path: Destination file path
        format: Export format (auto-detected from extension if not provided)
        database_type: Source database type (for SQL format)
        config: Optional custom configuration
        progress_callback: Optional callback for progress updates (row_count)

    Returns:
        ExportResult with success status and metadata

    Raises:
        EmptyResultError: If result_data has no rows
        InvalidPathError: If file path is invalid
        UnsupportedFormatError: If format is not supported
        ExportError: For other export failures
    """
    start_time = time.time()

    try:
        # Validate result data
        rows = result_data.get("rows", [])
        if not rows:
            raise EmptyResultError()

        # Validate and resolve file path
        resolved_path = validate_export_path(file_path)
        original_path = resolved_path

        # Detect format if not provided
        if format is None:
            format = ExportFormat.from_extension(resolved_path.suffix)

        # Create configuration if not provided
        if config is None:
            config = ExportConfiguration(
                file_path=resolved_path,
                format=format,
                source_database_type=database_type
            )
        else:
            config.file_path = resolved_path
            config.format = format

        # Ensure parent directory exists
        ensure_parent_directory(resolved_path)

        # Resolve file conflicts (auto-rename)
        if config.overwrite_behavior == "auto_rename":
            resolved_path = resolve_file_conflict(resolved_path)
            config.file_path = resolved_path

        # Perform format-specific export
        from ..formatting import csv_formatter, json_formatter, sql_formatter, mermaid_formatter

        if format == ExportFormat.CSV:
            csv_formatter.save_csv_to_file(
                result=result_data,
                file_path=str(resolved_path),
                include_headers=config.include_headers
            )
        elif format == ExportFormat.JSON:
            json_formatter.save_json_to_file(
                result=result_data,
                file_path=str(resolved_path),
                pretty=config.pretty_print
            )
        elif format == ExportFormat.SQL:
            # Extract table name from result or use default
            table_name = result_data.get("table_name", "exported_data")

            # If no table name in result, try to infer from query
            if table_name == "exported_data" and result_data.get("rows"):
                # Use generic table name - user can modify SQL file
                pass

            sql_formatter.save_sql_to_file(
                result=result_data,
                file_path=str(resolved_path),
                table_name=table_name,
                database_type=database_type,
                batch_size=config.batch_size
            )
        elif format == ExportFormat.MERMAID:
            # For Mermaid, expect schema_data in result
            if "schema_data" not in result_data:
                raise ExportError(
                    "Mermaid format requires schema data",
                    "Use \\schema graph command in REPL, then \\export <file>.mmd"
                )

            mermaid_formatter.save_mermaid_to_file(
                schema_data=result_data["schema_data"],
                file_path=str(resolved_path),
                database_type=database_type
            )
        elif format == ExportFormat.TXT:
            # Plain text export - simple string dump
            with open(resolved_path, 'w', encoding='utf-8') as f:
                if isinstance(result_data, str):
                    f.write(result_data)
                elif "rows" in result_data:
                    # Format as simple text table
                    rows = result_data["rows"]
                    if rows:
                        # Write headers
                        headers = list(rows[0].keys())
                        f.write('\t'.join(headers) + '\n')
                        # Write rows
                        for row in rows:
                            values = [str(row.get(h, '')) for h in headers]
                            f.write('\t'.join(values) + '\n')
                else:
                    f.write(str(result_data))
        else:
            raise UnsupportedFormatError(format.value)

        # Calculate duration and file size
        duration_ms = (time.time() - start_time) * 1000
        file_size = get_file_size(resolved_path)

        return ExportResult(
            success=True,
            file_path=resolved_path,
            original_path=original_path if original_path != resolved_path else None,
            row_count=len(rows),
            file_size_bytes=file_size,
            duration_ms=duration_ms,
            format=format
        )

    except (EmptyResultError, InvalidPathError, UnsupportedFormatError) as e:
        # Re-raise known errors
        raise
    except Exception as e:
        # Wrap unexpected errors
        duration_ms = (time.time() - start_time) * 1000
        return ExportResult(
            success=False,
            error=str(e),
            duration_ms=duration_ms
        )
