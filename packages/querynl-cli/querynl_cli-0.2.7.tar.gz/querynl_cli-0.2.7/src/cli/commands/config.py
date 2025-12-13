"""
Configuration management commands for QueryNL CLI.

Provides commands to view, modify, and reset CLI configuration.
"""

import os
import click
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
import yaml

from ..config import load_config, get_config_dir
from ..errors import ConfigError

console = Console()


@click.group()
def config():
    """
    Configuration management commands.

    Manage QueryNL CLI settings including default connection,
    output formats, and behavior preferences.
    """
    pass


@config.command("show")
@click.option("--format", "-f", type=click.Choice(["yaml", "table"]), default="yaml", help="Output format")
def config_show(format):
    """
    Display current configuration.

    Shows all configuration settings from ~/.querynl/config.yaml
    in a human-readable format.

    Examples:
        querynl config show
        querynl config show --format table
    """
    try:
        config_data = load_config()
        config_file = get_config_dir() / "config.yaml"

        if format == "yaml":
            # Display as syntax-highlighted YAML
            with open(config_file, 'r') as f:
                yaml_content = f.read()

            syntax = Syntax(yaml_content, "yaml", theme="monokai", line_numbers=True)
            panel = Panel(
                syntax,
                title=f"Configuration: {config_file}",
                border_style="cyan"
            )
            console.print(panel)

        elif format == "table":
            # Display as table
            table = Table(title="QueryNL Configuration", show_header=True, header_style="bold cyan")
            table.add_column("Setting", style="yellow")
            table.add_column("Value", style="white")

            # Flatten config for table display
            def flatten_dict(d, parent_key=''):
                items = []
                for k, v in d.items():
                    new_key = f"{parent_key}.{k}" if parent_key else k
                    if isinstance(v, dict):
                        items.extend(flatten_dict(v, new_key))
                    else:
                        items.append((new_key, str(v)))
                return items

            for key, value in flatten_dict(config_data):
                table.add_row(key, value)

            console.print(table)

    except FileNotFoundError:
        raise ConfigError(
            "Configuration file not found",
            "Run 'querynl connect add' to initialize configuration"
        )
    except Exception as e:
        raise ConfigError(f"Failed to load configuration: {e}")


@config.command("get")
@click.argument("key")
def config_get(key):
    """
    Get a specific configuration value.

    Args:
        key: Configuration key (e.g., 'default_connection', 'default_format')

    Examples:
        querynl config get default_connection
        querynl config get default_format
    """
    try:
        config_data = load_config()

        # Handle nested keys (e.g., 'connections.mydb.host')
        value = config_data
        for part in key.split('.'):
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                console.print(f"[yellow]Configuration key '{key}' not found[/yellow]")
                return

        console.print(f"[cyan]{key}:[/cyan] {value}")

    except Exception as e:
        raise ConfigError(f"Failed to get configuration: {e}")


@config.command("set")
@click.argument("key")
@click.argument("value")
def config_set(key, value):
    """
    Set a configuration value.

    Args:
        key: Configuration key (e.g., 'default_connection', 'default_format')
        value: New value for the configuration key

    Examples:
        querynl config set default_connection my-db
        querynl config set default_format json
        querynl config set prompt_format verbose

    Valid settings:
        - default_connection: Name of connection to use by default
        - default_format: Output format (table, json, csv, markdown)
        - prompt_format: REPL prompt style (minimal, verbose)
        - log_level: Logging level (debug, info, warning, error)
    """
    try:
        config_data = load_config()
        config_file = get_config_dir() / "config.yaml"

        # Validate common keys
        valid_formats = ["table", "json", "csv", "tsv", "markdown"]
        valid_log_levels = ["debug", "info", "warning", "error"]

        if key == "default_format" and value not in valid_formats:
            raise ConfigError(
                f"Invalid format '{value}'",
                f"Valid formats: {', '.join(valid_formats)}"
            )

        if key == "log_level" and value not in valid_log_levels:
            raise ConfigError(
                f"Invalid log level '{value}'",
                f"Valid levels: {', '.join(valid_log_levels)}"
            )

        # Set the value (handle nested keys)
        parts = key.split('.')
        target = config_data
        for part in parts[:-1]:
            if part not in target:
                target[part] = {}
            target = target[part]

        # Type conversion for common settings
        if value.lower() in ('true', 'false'):
            value = value.lower() == 'true'
        elif value.isdigit():
            value = int(value)
        elif '.' in value and value.replace('.', '').isdigit():
            value = float(value)

        target[parts[-1]] = value

        # Save configuration
        with open(config_file, 'w') as f:
            yaml.dump(config_data, f, default_flow_style=False, sort_keys=False)

        console.print(f"[green]✓[/green] Configuration updated: [cyan]{key}[/cyan] = {value}")

    except ConfigError:
        raise
    except Exception as e:
        raise ConfigError(f"Failed to set configuration: {e}")


@config.command("reset")
@click.option("--confirm", is_flag=True, help="Skip confirmation prompt")
def config_reset(confirm):
    """
    Reset configuration to defaults.

    Restores the default CLI configuration, preserving saved connections.
    This cannot be undone.

    Examples:
        querynl config reset --confirm
    """
    if not confirm:
        console.print("[yellow]Warning:[/yellow] This will reset all configuration to defaults.")
        console.print("Saved connections will be preserved.")
        if not click.confirm("Continue?"):
            console.print("[dim]Reset cancelled[/dim]")
            return

    try:
        config_file = get_config_dir() / "config.yaml"

        # Load current config to preserve connections
        try:
            current_config = load_config()
            connections = current_config.get("connections", {})
        except Exception:
            connections = {}

        # Create default configuration
        default_config = {
            "default_connection": None,
            "default_format": "table",
            "prompt_format": "minimal",
            "log_level": "info",
            "connections": connections  # Preserve connections
        }

        # Save default configuration
        with open(config_file, 'w') as f:
            yaml.dump(default_config, f, default_flow_style=False, sort_keys=False)

        console.print("[green]✓[/green] Configuration reset to defaults")
        console.print(f"[dim]Config file: {config_file}[/dim]")

    except Exception as e:
        raise ConfigError(f"Failed to reset configuration: {e}")


@config.command("path")
def config_path():
    """
    Show configuration file path.

    Displays the location of the config.yaml file.

    Examples:
        querynl config path
    """
    config_file = get_config_dir() / "config.yaml"
    console.print(f"[cyan]Configuration file:[/cyan] {config_file}")

    if config_file.exists():
        console.print("[green]✓[/green] File exists")
    else:
        console.print("[yellow]![/yellow] File not found (will be created on first use)")


@config.command("llm")
@click.option("--provider", "-p", type=click.Choice(["openai", "anthropic"]), default="openai", help="LLM provider")
@click.option("--api-key", "-k", prompt="API Key", hide_input=True, help="API key for LLM provider")
@click.option("--test", is_flag=True, help="Test the API key after setting")
def config_llm(provider, api_key, test):
    """
    Configure LLM API credentials.

    Sets up API keys for natural language to SQL query generation.
    API keys are stored securely in your system's keychain.

    Supported providers:
        - openai: OpenAI GPT-4 (https://platform.openai.com/api-keys)
        - anthropic: Anthropic Claude (https://console.anthropic.com/)

    Examples:
        querynl config llm --provider openai
        querynl config llm --provider anthropic --test
    """
    import keyring

    try:
        # Store API key in system keychain
        keyring_service = f"querynl-{provider}"
        keyring.set_password(keyring_service, "api_key", api_key)

        # Update provider in config
        config_data = load_config()
        config_data.llm_provider = provider

        from ..config import save_config
        save_config(config_data)

        console.print(f"[green]✓[/green] {provider.capitalize()} API key saved securely in keychain")
        console.print(f"[dim]Service: {keyring_service}[/dim]")

        # Optionally set environment variable for current session
        env_var = "OPENAI_API_KEY" if provider == "openai" else "ANTHROPIC_API_KEY"
        console.print(f"\n[cyan]Tip:[/cyan] You can also set {env_var} environment variable:")
        console.print(f"[dim]export {env_var}=your-api-key[/dim]")

        if test:
            console.print("\n[cyan]Testing API key...[/cyan]")
            from ..llm import LLMService

            llm_service = LLMService(api_key=api_key, provider=provider)

            if llm_service.llm is None:
                console.print("[red]✗[/red] Failed to initialize LLM service")
                return

            # Test with a simple query
            result = llm_service.generate_sql(
                natural_language="count all users",
                database_type="postgresql"
            )

            if result.get("confidence", 0) > 0.5 and not result.get("error"):
                console.print("[green]✓[/green] API key is valid and working!")
                console.print(f"[dim]Test query generated successfully (confidence: {result['confidence']:.0%})[/dim]")
            else:
                console.print("[yellow]![/yellow] API key set but test query failed")
                console.print(f"[dim]{result.get('explanation', 'Unknown error')}[/dim]")

    except Exception as e:
        raise ConfigError(f"Failed to configure LLM: {e}")


@config.command("llm-show")
def config_llm_show():
    """
    Show current LLM configuration.

    Displays the configured LLM provider and whether an API key is set.

    Examples:
        querynl config llm-show
    """
    import keyring

    try:
        config_data = load_config()
        provider = config_data.llm_provider

        console.print(f"[cyan]LLM Provider:[/cyan] {provider}")

        # Check if API key is set in keychain
        keyring_service = f"querynl-{provider}"
        try:
            api_key = keyring.get_password(keyring_service, "api_key")
            if api_key:
                # Show masked API key
                masked = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
                console.print(f"[cyan]API Key:[/cyan] {masked} [green](set)[/green]")
            else:
                console.print(f"[cyan]API Key:[/cyan] [yellow](not set)[/yellow]")
        except Exception:
            console.print(f"[cyan]API Key:[/cyan] [yellow](not set)[/yellow]")

        # Check environment variable
        env_var = "OPENAI_API_KEY" if provider == "openai" else "ANTHROPIC_API_KEY"
        env_value = os.environ.get(env_var)
        if env_value:
            masked_env = env_value[:8] + "..." + env_value[-4:] if len(env_value) > 12 else "***"
            console.print(f"[cyan]Environment Variable ({env_var}):[/cyan] {masked_env} [green](set)[/green]")
        else:
            console.print(f"[cyan]Environment Variable ({env_var}):[/cyan] [dim](not set)[/dim]")

        console.print(f"\n[dim]To configure: querynl config llm --provider {provider}[/dim]")

    except Exception as e:
        raise ConfigError(f"Failed to show LLM configuration: {e}")
