"""
Export functionality for QueryNL CLI

Provides file export capabilities for query results in multiple formats:
- CSV (RFC 4180 compliant)
- JSON (streaming support)
- SQL INSERT statements
- Mermaid ER diagrams
- Plain text

Supports both CLI mode (--export flag) and REPL mode (\export command).
"""

from .exporter import export_to_file, ExportFormat, ExportConfiguration, ExportResult
from .exceptions import (
    ExportError,
    InvalidPathError,
    PermissionDeniedError,
    DiskFullError,
    UnsupportedFormatError
)

__all__ = [
    'export_to_file',
    'ExportFormat',
    'ExportConfiguration',
    'ExportResult',
    'ExportError',
    'InvalidPathError',
    'PermissionDeniedError',
    'DiskFullError',
    'UnsupportedFormatError',
]
