"""
QueryNL CLI - Main entry point

Provides command groups for database query, connection management, schema design,
migrations, and configuration.
"""

import sys
import click
from rich.console import Console

from . import __version__
from .logging import setup_logging
from .errors import get_exit_code, format_error_message
from .commands.connect import connect
from .commands.query import query as query_group
from .commands.schema import schema
from .commands.migrate import migrate
from .commands.config import config

# Auto-detect TTY for proper automation support (disable colors when piping)
console = Console(force_terminal=sys.stdout.isatty() if hasattr(sys.stdout, 'isatty') else False)
error_console = Console(stderr=True, force_terminal=sys.stderr.isatty() if hasattr(sys.stderr, 'isatty') else False)


@click.group()
@click.version_option(version=__version__, prog_name="QueryNL CLI")
@click.option("--verbose", is_flag=True, help="Enable verbose output")
@click.option("--quiet", "-q", is_flag=True, help="Suppress non-essential output")
@click.pass_context
def cli(ctx, verbose, quiet):
    """
    QueryNL - Natural Language Database Queries from the Terminal

    A powerful CLI tool for executing database queries using natural language,
    managing connections, designing schemas, and generating migrations.

    Examples:
      querynl query "count all users"
      querynl connect add my-db
      querynl repl
    """
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["quiet"] = quiet

    # Setup logging
    setup_logging(verbose=verbose)


# Register command groups
cli.add_command(connect)
cli.add_command(query_group, name="query")
cli.add_command(schema)
cli.add_command(migrate)
cli.add_command(config)


@cli.command()
@click.option("--connection", "-c", help="Connection to use (overrides default)")
@click.pass_context
def repl(ctx, connection):
    """
    Start interactive REPL mode

    Provides an interactive session with conversation context, command history,
    and tab completion for enhanced query experience.

    Examples:
        querynl repl
        querynl repl --connection my-db
    """
    from .repl import start_repl

    try:
        start_repl(connection_name=connection)
    except KeyboardInterrupt:
        console.print("\n[dim]REPL interrupted[/dim]")
    except Exception as e:
        console.print(f"[red]Error starting REPL:[/red] {e}")
        raise click.Abort()


def main():
    """
    Main entry point with exit code handling for automation.

    Catches exceptions and maps them to appropriate exit codes:
    - 0: Success
    - 1: General error
    - 2: Invalid arguments
    - 3: Connection error
    - 4: Query/schema/migration error
    - 5: Configuration error
    """
    try:
        cli()
        sys.exit(0)
    except click.ClickException as e:
        # Click handles its own error display
        e.show()
        sys.exit(e.exit_code if hasattr(e, 'exit_code') else 1)
    except click.Abort:
        # User cancelled operation
        sys.exit(1)
    except Exception as e:
        # Map exception to exit code
        exit_code = get_exit_code(e)
        error_msg = format_error_message(e)
        error_console.print(f"[red]Error:[/red] {error_msg}")
        sys.exit(exit_code)


if __name__ == "__main__":
    main()
