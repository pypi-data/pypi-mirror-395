"""
QueryNL Schema Design Module

This module provides conversational schema design capabilities through natural language.
Users can design database schemas, upload data files for analysis, iterate on designs,
and implement finalized schemas across multiple database types.
"""

__version__ = "1.0.0"


# Exception Classes (T008)


class SchemaDesignError(Exception):
    """Base exception for schema design errors."""
    pass


class SessionNotFoundError(SchemaDesignError):
    """Raised when a requested schema design session cannot be found."""
    pass


class FileTooLargeError(SchemaDesignError):
    """Raised when uploaded file exceeds size limit (100MB)."""
    pass


class UnsupportedFileTypeError(SchemaDesignError):
    """Raised when file type is not supported (must be csv, xlsx, or json)."""
    pass


class FileParseError(SchemaDesignError):
    """Raised when file cannot be parsed or has invalid format."""
    pass


class UnsupportedDatabaseError(SchemaDesignError):
    """Raised when database type is not supported."""
    pass


class ValidationError(SchemaDesignError):
    """Raised when schema validation fails."""
    pass


__all__ = [
    'SchemaDesignError',
    'SessionNotFoundError',
    'FileTooLargeError',
    'UnsupportedFileTypeError',
    'FileParseError',
    'UnsupportedDatabaseError',
    'ValidationError',
]
