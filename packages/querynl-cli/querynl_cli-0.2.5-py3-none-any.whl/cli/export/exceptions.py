"""
Custom exceptions for export functionality

Provides user-friendly error messages for common export failures.
"""


class ExportError(Exception):
    """Base exception for all export-related errors."""

    def __init__(self, message: str, suggestion: str = ""):
        self.message = message
        self.suggestion = suggestion
        super().__init__(message)

    def __str__(self):
        if self.suggestion:
            return f"{self.message}\n💡 Suggestion: {self.suggestion}"
        return self.message


class InvalidPathError(ExportError):
    """Raised when export path is invalid or contains path traversal."""

    def __init__(self, path: str, reason: str = ""):
        message = f"Invalid export path: {path}"
        if reason:
            message += f" ({reason})"
        suggestion = "Use absolute or relative paths without '..' components"
        super().__init__(message, suggestion)


class PermissionDeniedError(ExportError):
    """Raised when user lacks permission to write to export path."""

    def __init__(self, path: str):
        message = f"Permission denied: Cannot write to {path}"
        suggestion = "Check file permissions or choose a different directory"
        super().__init__(message, suggestion)


class DiskFullError(ExportError):
    """Raised when disk is full during export."""

    def __init__(self, path: str):
        message = f"Disk full: Cannot write to {path}"
        suggestion = "Free up disk space or choose a different location"
        super().__init__(message, suggestion)


class UnsupportedFormatError(ExportError):
    """Raised when export format is not supported."""

    def __init__(self, format_name: str):
        message = f"Unsupported export format: {format_name}"
        suggestion = "Supported formats: csv, json, sql, mermaid, txt"
        super().__init__(message, suggestion)


class EmptyResultError(ExportError):
    """Raised when attempting to export empty result set."""

    def __init__(self):
        message = "Cannot export: No query results available"
        suggestion = "Execute a query first, then export the results"
        super().__init__(message, suggestion)
