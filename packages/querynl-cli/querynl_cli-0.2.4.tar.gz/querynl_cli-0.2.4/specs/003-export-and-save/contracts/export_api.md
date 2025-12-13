# Export API Contract

**Feature**: Export and Save Query Results
**Version**: 1.0.0
**Date**: 2025-10-25

## Overview

This document defines the internal API contract for the export functionality. This is not a REST API, but rather the Python API contract between modules (CLI commands, REPL, export service).

## Core API: Exporter Service

### Module: `src/cli/export/exporter.py`

#### `export_to_file()`

**Purpose**: Main entry point for exporting query results to a file.

**Signature**:
```python
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
    Export query results to a file in the specified format.

    Args:
        result_data: Query result dictionary with 'rows' and metadata
        file_path: Destination file path (str or pathlib.Path)
        format: Export format (auto-detected from extension if None)
        database_type: Source database type for SQL format
        config: Export configuration (uses defaults if None)
        progress_callback: Optional callback for progress updates

    Returns:
        ExportResult with success status, actual file path, row count

    Raises:
        FilePermissionError: Cannot write to specified path
        DiskFullError: Insufficient disk space
        InvalidPathError: Invalid or unsafe file path
        UnsupportedFormatError: Format not supported for data type
    """
```

**Example Usage**:
```python
from cli.export import export_to_file, ExportFormat

# Auto-detect format from extension
result = export_to_file(
    result_data=query_result,
    file_path="./exports/users.csv",
    database_type="postgresql"
)

# Explicit format specification
result = export_to_file(
    result_data=query_result,
    file_path="./exports/users.txt",
    format=ExportFormat.JSON,  # Override extension
    database_type="postgresql"
)

# With progress callback
def show_progress(rows_exported: int):
    print(f"Exported {rows_exported} rows...")

result = export_to_file(
    result_data=large_query_result,
    file_path="./exports/big_table.csv",
    progress_callback=show_progress
)
```

**Behavior**:
1. Validate file path (no traversal, check permissions)
2. Detect format from extension if not specified
3. Check if file exists → auto-rename with timestamp if needed
4. Create parent directories if they don't exist (mkdir -p)
5. Choose streaming vs in-memory based on row count
6. Write data with appropriate format writer
7. Return ExportResult with actual path and metadata

**Error Handling**:
- Pre-flight validation catches most errors before writing
- Atomic writes (temp file → rename) prevent partial files
- Cleanup on error removes temp files
- Clear error messages with actionable suggestions

---

#### `detect_format()`

**Purpose**: Auto-detect export format from file extension.

**Signature**:
```python
def detect_format(file_path: str | Path) -> ExportFormat:
    """
    Detect export format from file extension.

    Args:
        file_path: File path to inspect

    Returns:
        ExportFormat enum value

    Raises:
        UnsupportedFormatError: Unknown file extension
    """
```

**Extension Mapping**:
- `.csv` → `ExportFormat.CSV`
- `.json` → `ExportFormat.JSON`
- `.sql` → `ExportFormat.SQL`
- `.mmd` → `ExportFormat.MERMAID`
- `.txt` → `ExportFormat.TXT`
- Unknown → raises `UnsupportedFormatError`

---

#### `validate_export_path()`

**Purpose**: Validate file path for security and feasibility.

**Signature**:
```python
def validate_export_path(file_path: str | Path) -> Path:
    """
    Validate export file path for security and OS compatibility.

    Args:
        file_path: Path to validate

    Returns:
        Resolved absolute Path object

    Raises:
        InvalidPathError: Path contains traversal or invalid characters
        FilePermissionError: Parent directory not writable
    """
```

**Validation Steps**:
1. Convert to `pathlib.Path` and resolve to absolute path
2. Check for path traversal (`../`, `..\`)
3. Check OS-specific invalid characters (Windows: `<>:"|?*`)
4. Verify parent directory exists or can be created
5. Check write permissions on parent directory
6. Check path length limits (Windows: 260 chars)

---

## Format Writers API

### Base Interface: `FormatWriter`

**Module**: `src/cli/export/streaming.py`

```python
class FormatWriter(ABC):
    """Abstract base class for format-specific export writers."""

    @abstractmethod
    def begin(self, file_handle: TextIO, columns: List[str]) -> None:
        """Initialize writer and write any headers/preamble."""
        pass

    @abstractmethod
    def write_row(self, row: Dict[str, Any]) -> None:
        """Write a single data row."""
        pass

    @abstractmethod
    def end(self) -> None:
        """Finalize export and write any footers."""
        pass
```

### CSV Writer

```python
class CSVWriter(FormatWriter):
    """RFC 4180 compliant CSV writer with streaming support."""

    def __init__(self, include_headers: bool = True):
        self.include_headers = include_headers
        self.csv_writer = None

    def begin(self, file_handle: TextIO, columns: List[str]) -> None:
        self.csv_writer = csv.DictWriter(
            file_handle,
            fieldnames=columns,
            quoting=csv.QUOTE_MINIMAL,
            lineterminator='\n'
        )
        if self.include_headers:
            self.csv_writer.writeheader()

    def write_row(self, row: Dict[str, Any]) -> None:
        # Convert None to empty string, handle special types
        clean_row = {
            k: ("" if v is None else str(v))
            for k, v in row.items()
        }
        self.csv_writer.writerow(clean_row)

    def end(self) -> None:
        pass  # CSV has no footer
```

### JSON Writer

```python
class JSONWriter(FormatWriter):
    """Streaming JSON array writer."""

    def __init__(self, pretty_print: bool = False):
        self.pretty_print = pretty_print
        self.first_row = True
        self.file_handle = None

    def begin(self, file_handle: TextIO, columns: List[str]) -> None:
        self.file_handle = file_handle
        file_handle.write("[\n" if self.pretty_print else "[")

    def write_row(self, row: Dict[str, Any]) -> None:
        if not self.first_row:
            self.file_handle.write(",\n" if self.pretty_print else ",")

        json_row = json.dumps(row, cls=CustomJSONEncoder, indent=2 if self.pretty_print else None)
        self.file_handle.write(json_row)
        self.first_row = False

    def end(self) -> None:
        self.file_handle.write("\n]" if self.pretty_print else "]")
```

### SQL Writer

```python
class SQLWriter(FormatWriter):
    """SQL INSERT statement writer with database-specific escaping."""

    def __init__(self, table_name: str, database_type: str, batch_size: int = 1000):
        self.table_name = table_name
        self.database_type = database_type
        self.batch_size = batch_size
        self.batch_buffer = []
        self.file_handle = None
        self.columns = None

    def begin(self, file_handle: TextIO, columns: List[str]) -> None:
        self.file_handle = file_handle
        self.columns = columns

        # Write header comment
        file_handle.write(f"-- Table: {self.table_name}\n")
        file_handle.write(f"-- Database: {self.database_type}\n")
        file_handle.write(f"-- Exported: {datetime.now().isoformat()}\n\n")

    def write_row(self, row: Dict[str, Any]) -> None:
        self.batch_buffer.append(row)

        if len(self.batch_buffer) >= self.batch_size:
            self._flush_batch()

    def end(self) -> None:
        if self.batch_buffer:
            self._flush_batch()

    def _flush_batch(self) -> None:
        # Database-specific INSERT generation
        if self.database_type == "postgresql":
            self._write_postgres_insert()
        elif self.database_type == "mysql":
            self._write_mysql_insert()
        # ... etc

        self.batch_buffer.clear()
```

### Mermaid Writer

```python
class MermaidWriter(FormatWriter):
    """Mermaid ER diagram writer for schema exports."""

    def __init__(self, schema_data: Dict, relationships: List[Dict]):
        self.schema_data = schema_data
        self.relationships = relationships

    def begin(self, file_handle: TextIO, columns: List[str]) -> None:
        file_handle.write("erDiagram\n")

    def write_entity(self, entity_name: str, columns: List[Dict]) -> None:
        """Write a single entity (table) definition."""
        self.file_handle.write(f"  {entity_name.upper()} {{\n")
        for col in columns:
            col_type = self._map_type(col["type"])
            pk_marker = " PK" if col["name"] == "id" else ""
            fk_marker = " FK" if col["name"].endswith("_id") and col["name"] != "id" else ""
            self.file_handle.write(f"    {col_type} {col['name']}{pk_marker}{fk_marker}\n")
        self.file_handle.write("  }\n\n")

    def write_relationships(self) -> None:
        """Write relationship connections between entities."""
        for rel in self.relationships:
            # Determine cardinality notation
            notation = "||--o{"  # one-to-many (default)
            self.file_handle.write(
                f"  {rel['from_table'].upper()} {notation} "
                f"{rel['to_table'].upper()} : \"{rel['relationship_name']}\"\n"
            )
```

---

## CLI Integration Contracts

### Query Command Extension

**Module**: `src/cli/commands/query.py`

**New Parameter**:
```python
@click.option(
    "--export",
    "-e",
    type=click.Path(),
    help="Export results to file (format auto-detected from extension)"
)
@click.option(
    "--format",
    "-f",
    type=click.Choice(["csv", "json", "sql"], case_sensitive=False),
    help="Override export format (takes precedence over file extension)"
)
```

**Integration Point**:
```python
def execute_query(..., export: Optional[str], format: Optional[str]):
    # ... existing query execution ...

    # After displaying results to console:
    if export:
        from cli.export import export_to_file, ExportFormat

        format_enum = ExportFormat[format.upper()] if format else None

        export_result = export_to_file(
            result_data=result,
            file_path=export,
            format=format_enum,
            database_type=profile.database_type
        )

        if export_result.success:
            console.print(f"[green]✓[/green] Exported {export_result.row_count} rows to {export_result.file_path}")
        else:
            console.print(f"[red]✗[/red] Export failed: {export_result.error}")
```

---

### REPL Command Extension

**Module**: `src/cli/repl.py`

**New Command**: `\export <filepath>`

```python
def _cmd_export(self, filepath: str):
    """Export the most recent query result to a file."""

    if not self.last_result:
        console.print("[yellow]No query results to export. Run a query first.[/yellow]")
        return

    if not filepath:
        console.print("[yellow]Usage: \\export <filepath>[/yellow]")
        console.print("Example: \\export results.csv")
        return

    from cli.export import export_to_file

    try:
        export_result = export_to_file(
            result_data=self.last_result,
            file_path=filepath,
            database_type=self.profile.database_type
        )

        if export_result.success:
            if export_result.file_path != Path(filepath):
                console.print(f"[dim]File existed, renamed to: {export_result.file_path.name}[/dim]")
            console.print(f"[green]✓[/green] Exported {export_result.row_count} rows to {export_result.file_path}")
        else:
            console.print(f"[red]✗[/red] Export failed: {export_result.error}")

    except Exception as e:
        console.print(f"[red]Export error:[/red] {str(e)}")
```

**State Management**:
```python
class REPLSession:
    def __init__(self):
        self.last_result: Optional[Dict[str, Any]] = None
        # ... existing attributes ...

    def execute_query(self, query: str):
        result = # ... execute query ...

        # Cache result for potential export
        self.last_result = result

        return result
```

---

## Error Response Format

All export errors return consistent `ExportResult` objects:

```python
@dataclass
class ExportResult:
    success: bool
    file_path: Optional[Path] = None
    original_path: Optional[Path] = None
    row_count: int = 0
    file_size_bytes: int = 0
    duration_ms: float = 0.0
    format: Optional[ExportFormat] = None
    warnings: List[str] = field(default_factory=list)
    error: Optional[str] = None
```

**Success Example**:
```python
ExportResult(
    success=True,
    file_path=Path("/path/to/exports/users_20251025_143000.csv"),
    original_path=Path("/path/to/exports/users.csv"),
    row_count=1523,
    file_size_bytes=245680,
    duration_ms=342.5,
    format=ExportFormat.CSV,
    warnings=["Binary column 'avatar' skipped in CSV export"]
)
```

**Error Example**:
```python
ExportResult(
    success=False,
    error="Permission denied: Cannot write to /protected/path/users.csv. Check directory permissions."
)
```

---

## Progress Callback Contract

**Signature**:
```python
Callable[[int], None]
```

**Behavior**:
- Called every `progress_interval` rows (default: 10,000)
- Receives total row count exported so far
- Should not block or raise exceptions
- Used by CLI/REPL to display progress indicators

**Example Implementation** (REPL):
```python
from rich.progress import Progress

with Progress() as progress:
    task = progress.add_task("Exporting...", total=estimated_rows)

    def update_progress(rows_exported: int):
        progress.update(task, completed=rows_exported)

    export_result = export_to_file(
        result_data=large_result,
        file_path="big_export.csv",
        progress_callback=update_progress
    )
```

---

## Testing Contract

### Unit Test Requirements

**Test Coverage** (minimum 80%):
- `exporter.py`: All public functions, error paths
- Format writers: All formats, edge cases (NULL, special chars, large values)
- File utilities: Path validation, auto-rename, directory creation
- Streaming: Progress tracking, memory efficiency

**Test Data**:
- Small datasets (10 rows) - basic functionality
- Medium datasets (1,000 rows) - format correctness
- Large datasets (100,000 rows) - streaming, memory
- Edge case data (NULL, empty strings, special characters, binary)

### Integration Test Requirements

**Test Scenarios**:
1. CLI export from query command (all formats)
2. REPL export from cached result (all formats)
3. Cross-database exports (PostgreSQL, MySQL, SQLite, MongoDB)
4. File conflict scenarios (auto-rename)
5. Permission error scenarios
6. Large dataset streaming (memory monitoring)

---

## API Stability Guarantee

**Version**: 1.0.0 (Initial)

**Stability**:
- **Public API** (`export_to_file`, `ExportFormat`, `ExportResult`): Stable, semantic versioning
- **Format Writers**: Internal API, may change in minor versions
- **File utilities**: Internal API, may change in minor versions

**Breaking Changes** (require major version bump):
- Change `export_to_file()` signature
- Remove supported export format
- Change `ExportResult` structure (remove fields)

**Non-Breaking Changes** (minor version bump):
- Add new export format
- Add optional parameters to `export_to_file()`
- Add fields to `ExportResult`
- Performance improvements
