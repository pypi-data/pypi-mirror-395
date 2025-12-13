"""
Error handling framework for QueryNL CLI

Custom exceptions with actionable error messages and suggestions.
Exit codes follow Unix conventions for automation compatibility.
"""

from typing import Optional


# Exit code constants
EXIT_SUCCESS = 0           # Command completed successfully
EXIT_GENERAL_ERROR = 1     # General/unspecified error
EXIT_INVALID_ARGS = 2      # Invalid command-line arguments
EXIT_CONNECTION_ERROR = 3  # Database connection failed
EXIT_QUERY_ERROR = 4       # Query execution failed
EXIT_CONFIG_ERROR = 5      # Configuration error


class QueryNLError(Exception):
    """Base exception for all QueryNL CLI errors."""

    def __init__(self, message: str, suggestion: Optional[str] = None):
        self.message = message
        self.suggestion = suggestion
        super().__init__(message)

    def __str__(self) -> str:
        if self.suggestion:
            return f"{self.message}\nSuggestion: {self.suggestion}"
        return self.message


class ConfigError(QueryNLError):
    """Configuration-related errors."""

    def __init__(self, message: str, suggestion: Optional[str] = None):
        if suggestion is None:
            suggestion = "Check your configuration file at ~/.querynl/config.yaml"
        super().__init__(message, suggestion)


class ConnectionError(QueryNLError):
    """Database connection errors."""

    def __init__(self, message: str, suggestion: Optional[str] = None):
        if suggestion is None:
            suggestion = "Run 'querynl connect test <name>' to diagnose connection issues"
        super().__init__(message, suggestion)


class QueryError(QueryNLError):
    """Query execution errors."""

    def __init__(self, message: str, suggestion: Optional[str] = None):
        if suggestion is None:
            suggestion = "Check your query syntax and try again, or use --explain to see generated SQL"
        super().__init__(message, suggestion)


class CredentialError(QueryNLError):
    """Credential storage/retrieval errors."""

    def __init__(self, message: str, suggestion: Optional[str] = None):
        if suggestion is None:
            suggestion = "Try re-adding the connection or set QUERYNL_CONNECTION_STRING environment variable"
        super().__init__(message, suggestion)


class SchemaError(QueryNLError):
    """Schema design and validation errors."""

    def __init__(self, message: str, suggestion: Optional[str] = None):
        if suggestion is None:
            suggestion = "Check schema file syntax or try regenerating the schema"
        super().__init__(message, suggestion)


class MigrationError(QueryNLError):
    """Migration generation and application errors."""

    def __init__(self, message: str, suggestion: Optional[str] = None):
        if suggestion is None:
            suggestion = "Use --dry-run to preview migration or check migration file syntax"
        super().__init__(message, suggestion)


def format_error_message(error: Exception) -> str:
    """
    Format error message for display to user.

    Args:
        error: Exception to format

    Returns:
        Formatted error message with suggestion if available
    """
    if isinstance(error, QueryNLError):
        return str(error)

    # Generic error formatting
    error_type = type(error).__name__
    message = str(error)

    return f"{error_type}: {message}"


def get_exit_code(exception: Exception) -> int:
    """
    Map exception types to exit codes for automation compatibility.

    Args:
        exception: The exception that was raised

    Returns:
        Appropriate exit code for the exception type
    """
    # Map custom exceptions to exit codes
    if isinstance(exception, ConfigError):
        return EXIT_CONFIG_ERROR
    elif isinstance(exception, ConnectionError):
        return EXIT_CONNECTION_ERROR
    elif isinstance(exception, (QueryError, SchemaError, MigrationError)):
        return EXIT_QUERY_ERROR
    elif isinstance(exception, (ValueError, TypeError)):
        return EXIT_INVALID_ARGS
    elif isinstance(exception, FileNotFoundError):
        return EXIT_CONFIG_ERROR
    elif isinstance(exception, QueryNLError):
        return EXIT_GENERAL_ERROR
    else:
        return EXIT_GENERAL_ERROR
