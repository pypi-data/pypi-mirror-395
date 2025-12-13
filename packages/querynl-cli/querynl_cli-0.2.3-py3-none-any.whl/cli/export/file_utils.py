"""
File handling utilities for export functionality

Provides path validation, auto-rename, and directory creation.
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from .exceptions import InvalidPathError, PermissionDeniedError, DiskFullError


def validate_export_path(file_path: str | Path) -> Path:
    """
    Validate export file path for security and accessibility.

    Args:
        file_path: Path to validate

    Returns:
        Resolved absolute Path object

    Raises:
        InvalidPathError: If path contains traversal or is invalid
        PermissionDeniedError: If parent directory is not writable
    """
    try:
        path = Path(file_path).resolve()
    except (ValueError, OSError) as e:
        raise InvalidPathError(str(file_path), f"Cannot resolve path: {e}")

    # Check for path traversal attempts
    # The resolved path should not escape the current working directory
    # unless it's an absolute path explicitly provided by the user
    if ".." in Path(file_path).parts:
        raise InvalidPathError(
            str(file_path),
            "Path contains '..' component (path traversal)"
        )

    # Check if parent directory is writable
    parent_dir = path.parent
    if parent_dir.exists() and not os.access(parent_dir, os.W_OK):
        raise PermissionDeniedError(str(path))

    return path


def resolve_file_conflict(file_path: Path) -> Path:
    """
    Resolve file name conflict by adding timestamp suffix.

    If file already exists, appends timestamp in format: YYYYMMDD_HHMMSS
    Example: results.csv -> results_20251025_143022.csv

    Args:
        file_path: Original file path

    Returns:
        Unique file path (may be same as input if no conflict)
    """
    if not file_path.exists():
        return file_path

    # Generate timestamp suffix
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Split filename and extension
    stem = file_path.stem
    suffix = file_path.suffix

    # Create new filename with timestamp
    new_name = f"{stem}_{timestamp}{suffix}"
    new_path = file_path.parent / new_name

    # If somehow the timestamped file also exists, add a counter
    counter = 1
    while new_path.exists():
        new_name = f"{stem}_{timestamp}_{counter}{suffix}"
        new_path = file_path.parent / new_name
        counter += 1

    return new_path


def ensure_parent_directory(file_path: Path) -> None:
    """
    Create parent directory if it doesn't exist (mkdir -p behavior).

    Args:
        file_path: File path whose parent directory should exist

    Raises:
        PermissionDeniedError: If directory creation fails due to permissions
        DiskFullError: If directory creation fails due to disk full
    """
    parent_dir = file_path.parent

    if parent_dir.exists():
        return

    try:
        parent_dir.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        raise PermissionDeniedError(str(parent_dir))
    except OSError as e:
        # Check for disk full (ENOSPC error)
        if e.errno == 28:  # ENOSPC
            raise DiskFullError(str(parent_dir))
        raise InvalidPathError(str(file_path), f"Cannot create directory: {e}")


def get_file_size(file_path: Path) -> int:
    """
    Get file size in bytes.

    Args:
        file_path: Path to file

    Returns:
        File size in bytes, or 0 if file doesn't exist
    """
    try:
        return file_path.stat().st_size
    except (OSError, FileNotFoundError):
        return 0


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.

    Args:
        size_bytes: File size in bytes

    Returns:
        Formatted string (e.g., "1.23 MB", "456 KB")
    """
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"
