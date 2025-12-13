"""
Logging configuration for QueryNL CLI

Provides console and file logging with credential protection.
"""

import logging
import re
from pathlib import Path
from typing import Optional

from .config import get_config_dir


class CredentialFilter(logging.Filter):
    """
    Filter to remove credentials from log messages.

    Prevents accidental logging of passwords, API keys, and connection strings.
    """

    # Patterns to detect and redact credentials
    PATTERNS = [
        (re.compile(r"password['\"]?\s*[:=]\s*['\"]?([^'\"&\s]+)", re.I), "password=***"),
        (re.compile(r"api[_-]?key['\"]?\s*[:=]\s*['\"]?([^'\"&\s]+)", re.I), "api_key=***"),
        (re.compile(r"://([^:]+):([^@]+)@", re.I), r"://\1:***@"),  # Connection strings
        (re.compile(r"token['\"]?\s*[:=]\s*['\"]?([^'\"&\s]+)", re.I), "token=***"),
    ]

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Redact credentials from log record.

        Args:
            record: Log record to filter

        Returns:
            True (always allow log, but with redacted message)
        """
        message = record.getMessage()

        for pattern, replacement in self.PATTERNS:
            message = pattern.sub(replacement, message)

        record.msg = message
        record.args = ()

        return True


def setup_logging(verbose: bool = False, log_file: Optional[Path] = None) -> None:
    """
    Setup logging configuration.

    Args:
        verbose: Enable debug-level logging
        log_file: Path to log file (optional, defaults to ~/.querynl/querynl.log)
    """
    log_level = logging.DEBUG if verbose else logging.INFO

    # Create formatters
    console_formatter = logging.Formatter(
        "[%(levelname)s] %(message)s"
    )

    file_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(console_formatter)
    console_handler.addFilter(CredentialFilter())
    root_logger.addHandler(console_handler)

    # File handler (if enabled)
    if log_file or verbose:
        if log_file is None:
            log_file = get_config_dir() / "querynl.log"

        # Ensure log directory exists
        log_file.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)  # Always debug in file
        file_handler.setFormatter(file_formatter)
        file_handler.addFilter(CredentialFilter())
        root_logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)
