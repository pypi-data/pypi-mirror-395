"""
Connection management commands for QueryNL CLI

Handles add/list/test/use/remove database connections with secure credential storage.
"""

import os
import click
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from typing import Optional

from ..config import load_config, save_config
from ..credentials import (
    store_password,
    get_password,
    delete_password,
    parse_connection_string,
)
from ..models import ConnectionProfile, SSHTunnel
from ..database import DatabaseConnection
from ..errors import ConfigError, ConnectionError as ConnError, CredentialError

console = Console()


@click.group()
def connect():
    """Manage database connections"""
    pass


@connect.command("add")
@click.argument("name")
@click.option("--type", "db_type", type=click.Choice(["postgresql", "mysql", "sqlite", "mongodb"]), help="Database type")
@click.option("--host", help="Database host")
@click.option("--port", type=int, help="Database port")
@click.option("--database", help="Database name")
@click.option("--username", help="Database username")
@click.option("--ssl/--no-ssl", default=True, help="Enable/disable SSL")
@click.option("--ssh-tunnel", is_flag=True, help="Configure SSH tunnel")
@click.option("--set-default", is_flag=True, help="Set as default connection")
def add_connection(name, db_type, host, port, database, username, ssl, ssh_tunnel, set_default):
    """
    Add a new database connection

    Examples:
        querynl connect add my-db
        querynl connect add prod --type postgresql --host localhost
    """
    try:
        config = load_config()

        # Check if connection already exists
        if name in config.connections:
            if not Confirm.ask(f"Connection '{name}' already exists. Overwrite?"):
                console.print("[yellow]Cancelled[/yellow]")
                return

        # Check for environment variable connection string
        connection_string = os.environ.get("QUERYNL_CONNECTION_STRING")
        if connection_string and not db_type:
            console.print("[dim]Using QUERYNL_CONNECTION_STRING from environment[/dim]")
            try:
                parsed = parse_connection_string(connection_string)
                db_type = parsed.get("database_type")
                host = parsed.get("host")
                port = parsed.get("port")
                database = parsed.get("database_name")
                username = parsed.get("username")
                password = parsed.get("password")
            except ValueError as e:
                raise ConfigError(f"Invalid connection string: {e}")
        else:
            password = None

        # Interactive prompts for missing values
        if not db_type:
            db_type = Prompt.ask(
                "Database type",
                choices=["postgresql", "mysql", "sqlite", "mongodb"],
                default="postgresql"
            )

        # SQLite doesn't need host/port/username
        if db_type != "sqlite":
            if not host:
                host = Prompt.ask("Host", default="localhost")

            if not port:
                default_ports = {
                    "postgresql": 5432,
                    "mysql": 3306,
                    "mongodb": 27017,
                }
                port = int(Prompt.ask("Port", default=str(default_ports.get(db_type, 5432))))

            if not username:
                username = Prompt.ask("Username")

            if not password:
                password = Prompt.ask("Password", password=True)

        if not database:
            if db_type == "sqlite":
                database = Prompt.ask("Database file path", default="./database.db")
            else:
                database = Prompt.ask("Database name")

        # SSH tunnel configuration
        ssh_tunnel_config = None
        if ssh_tunnel:
            console.print("\n[bold]SSH Tunnel Configuration[/bold]")
            ssh_host = Prompt.ask("SSH host")
            ssh_port = int(Prompt.ask("SSH port", default="22"))
            ssh_username = Prompt.ask("SSH username")
            ssh_key_path = Prompt.ask("SSH key path", default=f"{os.path.expanduser('~')}/.ssh/id_rsa")
            remote_port = port or 5432

            ssh_tunnel_config = SSHTunnel(
                ssh_host=ssh_host,
                ssh_port=ssh_port,
                ssh_username=ssh_username,
                ssh_key_path=ssh_key_path,
                remote_bind_host=host or "localhost",
                remote_bind_port=remote_port,
            )

        # Create connection profile
        profile = ConnectionProfile(
            name=name,
            database_type=db_type,
            host=host,
            port=port,
            database_name=database,
            username=username,
            ssl_enabled=ssl,
            ssh_tunnel=ssh_tunnel_config,
        )

        # Store password in keychain (if not SQLite)
        if db_type != "sqlite" and password:
            try:
                store_password(name, password)
                console.print("[green]✓[/green] Credentials stored securely in keychain")
            except Exception as e:
                raise CredentialError(f"Failed to store credentials: {e}")

        # Test connection
        console.print("\n[dim]Testing connection...[/dim]")
        test_result = _test_connection(profile, password)

        if test_result["status"] == "success":
            # Save to config
            config.connections[name] = profile.to_dict()

            # Set as default if first connection or explicitly requested
            if set_default or not config.default_connection:
                config.default_connection = name
                console.print("[green]✓[/green] Set as default connection")

            save_config(config)

            console.print(f"\n[green]✓[/green] Connection '{name}' added successfully")
            console.print(f"[dim]  Type: {db_type}[/dim]")
            if host:
                console.print(f"[dim]  Host: {host}:{port}[/dim]")
            console.print(f"[dim]  Database: {database}[/dim]")
            console.print(f"[dim]  Latency: {test_result.get('latency_ms')}ms[/dim]")

        else:
            console.print(f"\n[red]✗[/red] Connection test failed: {test_result.get('error')}")
            if not Confirm.ask("Save connection anyway?"):
                console.print("[yellow]Cancelled[/yellow]")
                return

            # Save even if test failed
            config.connections[name] = profile.to_dict()
            save_config(config)
            console.print(f"[yellow]Connection '{name}' saved (test failed)[/yellow]")

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise click.Abort()


@connect.command("list")
@click.option("--format", "output_format", type=click.Choice(["table", "json"]), default="table", help="Output format")
def list_connections(output_format):
    """List all configured connections"""
    try:
        config = load_config()

        if not config.connections:
            console.print("[yellow]No connections configured[/yellow]")
            console.print("Add a connection with: [bold]querynl connect add <name>[/bold]")
            return

        if output_format == "json":
            # Remove sensitive data
            safe_connections = {
                name: {k: v for k, v in conn.items() if k not in ["password"]}
                for name, conn in config.connections.items()
            }
            console.print_json(data={"connections": safe_connections})
            return

        # Table format
        table = Table(title="Database Connections")
        table.add_column("NAME", style="cyan")
        table.add_column("TYPE", style="magenta")
        table.add_column("HOST", style="white")
        table.add_column("DATABASE", style="green")
        table.add_column("STATUS", style="yellow")

        for name, conn_data in config.connections.items():
            is_default = "● " if name == config.default_connection else "○ "
            status = f"{is_default}{'Default' if name == config.default_connection else 'Active'}"

            host_display = conn_data.get("host", "local")
            if conn_data.get("port"):
                host_display += f":{conn_data['port']}"

            table.add_row(
                name,
                conn_data.get("database_type", "unknown"),
                host_display,
                conn_data.get("database_name", ""),
                status
            )

        console.print(table)

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise click.Abort()


@connect.command("test")
@click.argument("name")
def test_connection(name):
    """Test database connection"""
    try:
        config = load_config()

        if name not in config.connections:
            raise ConfigError(
                f"Connection '{name}' not found",
                suggestion="Run 'querynl connect list' to see available connections"
            )

        profile = ConnectionProfile.from_dict(config.connections[name])
        password = get_password(name) if profile.database_type != "sqlite" else None

        console.print(f"Testing connection '{name}'...")

        result = _test_connection(profile, password)

        if result["status"] == "success":
            console.print("\n[green]✓ Connection successful[/green]")
            console.print(f"  Database: {result.get('version', 'Unknown')}")
            console.print(f"  Latency: {result.get('latency_ms')}ms")
        else:
            console.print("\n[red]✗ Connection failed[/red]")
            console.print(f"  Error: {result.get('error')}")
            raise ConnError(result.get("error"))

    except Exception as e:
        if not isinstance(e, ConnError):
            console.print(f"[red]Error:[/red] {e}")
        raise click.Abort()


@connect.command("use")
@click.argument("name")
def use_connection(name):
    """Set default connection"""
    try:
        config = load_config()

        if name not in config.connections:
            raise ConfigError(
                f"Connection '{name}' not found",
                suggestion="Run 'querynl connect list' to see available connections"
            )

        config.default_connection = name
        save_config(config)

        console.print(f"[green]✓[/green] Default connection set to '{name}'")

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise click.Abort()


@connect.command("remove")
@click.argument("name")
@click.option("--confirm", is_flag=True, help="Skip confirmation prompt")
def remove_connection(name, confirm):
    """Remove a database connection"""
    try:
        config = load_config()

        if name not in config.connections:
            raise ConfigError(
                f"Connection '{name}' not found",
                suggestion="Run 'querynl connect list' to see available connections"
            )

        # Confirmation prompt
        if not confirm:
            if not Confirm.ask(f"Remove connection '{name}'?"):
                console.print("[yellow]Cancelled[/yellow]")
                return

        # Remove from config
        del config.connections[name]

        # Clear default if this was default connection
        if config.default_connection == name:
            # Set to first remaining connection, if any
            remaining = list(config.connections.keys())
            config.default_connection = remaining[0] if remaining else None

        save_config(config)

        # Delete credentials from keychain
        try:
            delete_password(name)
            console.print("[green]✓[/green] Credentials deleted from keychain")
        except Exception:
            pass  # Ignore if credentials don't exist

        console.print(f"[green]✓[/green] Connection '{name}' removed")

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise click.Abort()


def _test_connection(profile: ConnectionProfile, password: Optional[str]) -> dict:
    """
    Internal helper to test a connection.

    Args:
        profile: Connection profile to test
        password: Database password

    Returns:
        Test result dictionary
    """
    try:
        conn_config = profile.get_connection_config(password)
        db = DatabaseConnection(conn_config)
        return db.test_connection()
    except Exception as e:
        return {
            "status": "failed",
            "error": str(e),
        }
