"""
Configuration management for QueryNL CLI

Handles platform-specific config paths, YAML loading/saving, and configuration models.
"""

import os
import platform
from pathlib import Path
from typing import Optional, Dict, Any
import yaml
from pydantic import BaseModel, Field, field_validator
from rich.console import Console

console = Console()


def get_config_dir() -> Path:
    """
    Get platform-specific configuration directory.

    Returns:
        Path to config directory:
        - Linux: ~/.config/querynl (XDG_CONFIG_HOME)
        - macOS: ~/Library/Application Support/querynl
        - Windows: %APPDATA%\\querynl
    """
    system = platform.system()

    if system == "Linux":
        # Use XDG_CONFIG_HOME if set, otherwise ~/.config
        xdg_config = os.environ.get("XDG_CONFIG_HOME")
        if xdg_config:
            return Path(xdg_config) / "querynl"
        return Path.home() / ".config" / "querynl"

    elif system == "Darwin":  # macOS
        return Path.home() / "Library" / "Application Support" / "querynl"

    elif system == "Windows":
        appdata = os.environ.get("APPDATA")
        if appdata:
            return Path(appdata) / "querynl"
        return Path.home() / "AppData" / "Roaming" / "querynl"

    else:
        # Fallback for unknown systems
        return Path.home() / ".querynl"


def get_config_path() -> Path:
    """Get path to the configuration file."""
    return get_config_dir() / "config.yaml"


def get_history_db_path() -> Path:
    """Get path to the query history database."""
    return get_config_dir() / "history.db"


class CLIConfiguration(BaseModel):
    """
    CLI configuration model.

    Stores user preferences and default settings that persist across sessions.
    """
    version: str = "1.0"

    # Default settings
    default_connection: Optional[str] = None
    default_output_format: str = "table"
    llm_provider: str = "openai"

    # Preferences
    enable_telemetry: bool = False
    repl_history_size: int = 1000
    pager: Optional[str] = None  # None = auto-detect (less/more)
    confirm_destructive: bool = True
    color_output: str = "auto"  # auto, always, never

    # Connections storage (credentials stored separately in keychain)
    connections: Dict[str, Dict[str, Any]] = Field(default_factory=dict)

    @field_validator("default_output_format")
    @classmethod
    def validate_output_format(cls, v):
        valid_formats = ["table", "json", "csv", "markdown"]
        if v not in valid_formats:
            raise ValueError(f"Invalid output format. Must be one of: {', '.join(valid_formats)}")
        return v

    @field_validator("color_output")
    @classmethod
    def validate_color_output(cls, v):
        valid_options = ["auto", "always", "never"]
        if v not in valid_options:
            raise ValueError(f"Invalid color option. Must be one of: {', '.join(valid_options)}")
        return v

    @field_validator("repl_history_size")
    @classmethod
    def validate_history_size(cls, v):
        if not 100 <= v <= 10000:
            raise ValueError("REPL history size must be between 100 and 10000")
        return v


def ensure_config_dir() -> None:
    """Create config directory if it doesn't exist."""
    config_dir = get_config_dir()
    config_dir.mkdir(parents=True, exist_ok=True)


def load_config() -> CLIConfiguration:
    """
    Load configuration from file.

    Returns:
        CLIConfiguration object with loaded or default values
    """
    config_path = get_config_path()

    if not config_path.exists():
        # Return default configuration
        return CLIConfiguration()

    try:
        with open(config_path, "r") as f:
            data = yaml.safe_load(f) or {}

        return CLIConfiguration(**data)

    except Exception as e:
        console.print(f"[yellow]Warning: Failed to load config from {config_path}[/yellow]")
        console.print(f"[yellow]Error: {e}[/yellow]")
        console.print("[yellow]Using default configuration[/yellow]")
        return CLIConfiguration()


def save_config(config: CLIConfiguration) -> None:
    """
    Save configuration to file with atomic write.

    Args:
        config: Configuration object to save
    """
    ensure_config_dir()
    config_path = get_config_path()
    temp_path = config_path.with_suffix(".tmp")

    try:
        # Write to temporary file first (atomic write)
        with open(temp_path, "w") as f:
            yaml.safe_dump(
                config.model_dump(),
                f,
                default_flow_style=False,
                sort_keys=False
            )

        # Rename temp file to actual config (atomic operation)
        temp_path.replace(config_path)

    except Exception as e:
        # Clean up temp file if it exists
        if temp_path.exists():
            temp_path.unlink()
        raise Exception(f"Failed to save configuration: {e}")


def update_config(updates: Dict[str, Any]) -> CLIConfiguration:
    """
    Update configuration with new values.

    Args:
        updates: Dictionary of keys to update

    Returns:
        Updated configuration object
    """
    config = load_config()

    for key, value in updates.items():
        if hasattr(config, key):
            setattr(config, key, value)

    save_config(config)
    return config
