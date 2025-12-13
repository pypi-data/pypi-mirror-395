"""
Streaming export coordinator for large datasets

Provides base interface for format writers and coordinates streaming exports.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, TextIO, Optional, Callable
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.console import Console

console = Console(stderr=True)


class FormatWriter(ABC):
    """Abstract base class for format-specific export writers."""

    @abstractmethod
    def begin(self, file_handle: TextIO, columns: List[str]) -> None:
        """
        Initialize writer and write any headers/preamble.

        Args:
            file_handle: Open file handle for writing
            columns: List of column names
        """
        pass

    @abstractmethod
    def write_row(self, row: Dict[str, Any]) -> None:
        """
        Write a single data row.

        Args:
            row: Dictionary of column_name -> value
        """
        pass

    @abstractmethod
    def end(self) -> None:
        """Finalize export and write any footers."""
        pass


class StreamingExporter:
    """
    Coordinates streaming export of large result sets.

    Chooses between in-memory and streaming approaches based on row count,
    provides progress indicators for long-running exports.
    """

    def __init__(
        self,
        writer: FormatWriter,
        progress_enabled: bool = True,
        progress_interval: int = 10000,
        streaming_threshold: int = 10000
    ):
        """
        Initialize streaming exporter.

        Args:
            writer: Format-specific writer instance
            progress_enabled: Show progress indicators
            progress_interval: Rows between progress updates
            streaming_threshold: Row count threshold for streaming
        """
        self.writer = writer
        self.progress_enabled = progress_enabled
        self.progress_interval = progress_interval
        self.streaming_threshold = streaming_threshold

    def export(
        self,
        rows: List[Dict[str, Any]],
        file_handle: TextIO,
        progress_callback: Optional[Callable[[int], None]] = None
    ) -> int:
        """
        Export rows to file using configured writer.

        Args:
            rows: List of row dictionaries
            file_handle: Open file handle
            progress_callback: Optional callback for progress updates

        Returns:
            Number of rows exported
        """
        if not rows:
            # Write empty file with just headers
            columns = []
            self.writer.begin(file_handle, columns)
            self.writer.end()
            return 0

        # Get column names from first row
        columns = list(rows[0].keys())

        # Initialize writer
        self.writer.begin(file_handle, columns)

        # Determine export approach
        row_count = len(rows)
        use_streaming = row_count >= self.streaming_threshold

        if use_streaming and self.progress_enabled:
            # Stream with progress indicators
            rows_exported = self._export_with_progress(
                rows,
                progress_callback
            )
        else:
            # Simple in-memory export
            rows_exported = self._export_simple(rows)

        # Finalize export
        self.writer.end()

        return rows_exported

    def _export_simple(self, rows: List[Dict[str, Any]]) -> int:
        """
        Export rows without progress tracking.

        Args:
            rows: List of row dictionaries

        Returns:
            Number of rows exported
        """
        for row in rows:
            self.writer.write_row(row)
        return len(rows)

    def _export_with_progress(
        self,
        rows: List[Dict[str, Any]],
        progress_callback: Optional[Callable[[int], None]] = None
    ) -> int:
        """
        Export rows with progress indicators.

        Args:
            rows: List of row dictionaries
            progress_callback: Optional callback for progress updates

        Returns:
            Number of rows exported
        """
        total_rows = len(rows)

        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]Exporting..."),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TextColumn("[green]{task.fields[rows]:,} rows"),
            console=console,
        ) as progress:
            task = progress.add_task(
                "export",
                total=total_rows,
                rows=0
            )

            rows_exported = 0

            for row in rows:
                self.writer.write_row(row)
                rows_exported += 1

                # Update progress every interval
                if rows_exported % self.progress_interval == 0:
                    progress.update(task, completed=rows_exported, rows=rows_exported)

                    # Call custom progress callback if provided
                    if progress_callback:
                        progress_callback(rows_exported)

            # Final progress update
            progress.update(task, completed=rows_exported, rows=rows_exported)

        return rows_exported
