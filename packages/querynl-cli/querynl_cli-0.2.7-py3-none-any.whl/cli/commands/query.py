"""
Query execution commands for QueryNL CLI

Handles natural language query execution with SQL generation and result formatting.
"""

import sys
import click
from rich.console import Console
from rich.prompt import Confirm
from rich.syntax import Syntax

from ..config import load_config
from ..credentials import get_password
from ..models import ConnectionProfile
from ..database import DatabaseConnection
from ..llm import LLMService
from ..history import save_query_history, generate_session_id
from ..formatting.table import print_results
from ..errors import ConfigError, QueryError

console = Console()


@click.group()
def query():
    """Execute natural language database queries"""
    pass


@query.command("exec")
@click.argument("query_text", required=False)
@click.option("--format", "-f", "output_format", type=click.Choice(["table", "json", "csv", "markdown"]), default="table", help="Output format")
@click.option("--non-interactive", "-y", is_flag=True, help="Skip confirmation prompts")
@click.option("--output", "-o", type=click.Path(), help="Write output to file")
@click.option("--export", type=click.Path(), help="Export results to file (CSV, JSON, SQL, Mermaid)")
@click.option("--explain", "-e", is_flag=True, help="Show SQL without executing")
@click.option("--timeout", "-t", type=int, default=30, help="Query timeout in seconds")
@click.option("--limit", "-l", type=int, help="Limit result rows")
@click.option("--connection", "-c", help="Connection to use (overrides default)")
@click.option("--file", type=click.Path(exists=True), help="Read query from file")
def exec_query(
    query_text,
    output_format,
    non_interactive,
    output,
    export,
    explain,
    timeout,
    limit,
    connection,
    file,
):
    """
    Execute a natural language database query

    Examples:
        querynl query exec "count all users"
        querynl query exec --format json "show active users"
        querynl query exec --file queries.txt
        echo "list tables" | querynl query exec -
    """
    try:
        # Get query text from various sources
        if file:
            with open(file, "r") as f:
                query_text = f.read().strip()
        elif query_text == "-":
            query_text = sys.stdin.read().strip()
        elif not query_text:
            raise click.UsageError("Query text required. Use '-' to read from stdin or --file to read from file")

        # Load config and get connection
        config = load_config()

        connection_name = connection or config.default_connection
        if not connection_name:
            raise ConfigError(
                "No default connection set",
                suggestion="Run 'querynl connect add' to create a connection"
            )

        if connection_name not in config.connections:
            raise ConfigError(
                f"Connection '{connection_name}' not found",
                suggestion="Run 'querynl connect list' to see available connections"
            )

        profile = ConnectionProfile.from_dict(config.connections[connection_name])
        password = get_password(connection_name) if profile.database_type != "sqlite" else None

        # Introspect database schema for intelligent query generation
        from ..schema_introspection import SchemaIntrospector

        console.print("[dim]Analyzing database schema...[/dim]")
        introspector = SchemaIntrospector(profile, password)
        schema = introspector.get_schema()

        # Generate SQL from natural language
        # Get LLM API key from keychain
        import keyring
        import os

        provider = config.llm_provider
        keyring_service = f"querynl-{provider}"

        # Try keychain first, then environment variable
        api_key = None
        try:
            api_key = keyring.get_password(keyring_service, "api_key")
        except Exception:
            pass

        if not api_key:
            env_var = "OPENAI_API_KEY" if provider == "openai" else "ANTHROPIC_API_KEY"
            api_key = os.getenv(env_var)

        llm = LLMService(api_key=api_key, provider=provider)
        result = llm.generate_sql(query_text, profile.database_type, schema=schema)

        sql = result.get("sql", "")
        explanation = result.get("explanation", "")
        is_destructive = result.get("destructive", False)

        # Display generated SQL
        console.print("\n[bold]Generated SQL:[/bold]")
        syntax = Syntax(sql, "sql", theme="monokai", line_numbers=False)
        console.print(syntax)

        if explanation:
            console.print(f"\n[dim]{explanation}[/dim]")

        # Check for errors in generation
        if result.get("error"):
            console.print(f"\n[yellow]Warning: {result['error']}[/yellow]")
            if result.get("confidence", 0) < 0.5:
                console.print("[yellow]Low confidence - consider rephrasing your query[/yellow]")

        # Explain mode - don't execute
        if explain:
            console.print("\n[dim]Explanation mode - query not executed[/dim]")
            return

        # Confirmation for destructive operations
        if is_destructive and not non_interactive:
            console.print("\n[yellow]⚠️  Warning: This query will modify data[/yellow]")
            if result.get("warning"):
                console.print(f"[yellow]{result['warning']}[/yellow]")

            if not Confirm.ask("\nExecute this query?", default=False):
                console.print("[yellow]Query cancelled[/yellow]")
                return

        # Execute query
        console.print("\n[dim]Executing query...[/dim]")

        conn_config = profile.get_connection_config(password)
        db = DatabaseConnection(conn_config)

        try:
            # Apply limit if specified
            if limit and "SELECT" in sql.upper():
                if "LIMIT" not in sql.upper():
                    sql = sql.rstrip(";") + f" LIMIT {limit};"

            query_result = db.execute_query(sql)

            # Save to history
            session_id = generate_session_id()
            save_query_history(
                session_id=session_id,
                connection_name=connection_name,
                natural_language_input=query_text,
                generated_sql=sql,
                executed=True,
                execution_time_ms=query_result.get("execution_time_ms"),
                row_count=query_result.get("row_count"),
            )

            # Display results
            if output:
                # Write to file
                import json
                with open(output, "w") as f:
                    if output_format == "json":
                        json.dump(query_result, f, indent=2)
                    elif output_format == "csv":
                        import csv
                        if query_result.get("rows"):
                            writer = csv.DictWriter(f, fieldnames=query_result["rows"][0].keys())
                            writer.writeheader()
                            writer.writerows(query_result["rows"])
                    else:
                        # For table/markdown, capture console output
                        # Simplified: just write JSON for now
                        json.dump(query_result, f, indent=2)

                console.print(f"\n[green]✓[/green] Results written to {output}")
            else:
                # Print to console
                print_results(query_result, output_format)

            # Export results if --export flag provided
            if export:
                from ..export import export_to_file, ExportError

                try:
                    export_result = export_to_file(
                        result_data=query_result,
                        file_path=export,
                        database_type=profile.database_type
                    )
                    console.print(f"\n{export_result}")
                except ExportError as e:
                    console.print(f"\n[red]Export failed:[/red] {e}")

        except Exception as e:
            # Save failed query to history
            session_id = generate_session_id()
            save_query_history(
                session_id=session_id,
                connection_name=connection_name,
                natural_language_input=query_text,
                generated_sql=sql,
                executed=False,
                error_message=str(e),
            )

            raise QueryError(f"Query execution failed: {e}")

        finally:
            db.close()

    except Exception as e:
        console.print(f"\n[red]Error:[/red] {e}")
        raise click.Abort()


@query.command("history")
@click.option("--limit", "-n", type=int, default=20, help="Number of entries to show")
@click.option("--connection", "-c", help="Filter by connection")
@click.option("--format", "-f", "output_format", type=click.Choice(["table", "json"]), default="table", help="Output format")
def show_history(limit, connection, output_format):
    """
    Show query history

    Examples:
        querynl query history
        querynl query history --limit 50
        querynl query history --connection prod-db
    """
    try:
        from ..history import get_query_history
        from rich.table import Table

        history = get_query_history(limit=limit, connection_name=connection)

        if not history:
            console.print("[yellow]No query history found[/yellow]")
            return

        if output_format == "json":
            console.print_json(data={"history": history})
            return

        # Table format
        table = Table(title="Query History")
        table.add_column("TIMESTAMP", style="cyan")
        table.add_column("CONNECTION", style="magenta")
        table.add_column("QUERY", style="white", max_width=50)
        table.add_column("ROWS", style="green")
        table.add_column("TIME", style="yellow")

        for entry in history:
            timestamp = entry["timestamp"].split("T")[0] if "T" in entry["timestamp"] else entry["timestamp"]
            query = entry["natural_language_input"][:47] + "..." if len(entry["natural_language_input"]) > 50 else entry["natural_language_input"]
            rows = str(entry["row_count"]) if entry["row_count"] is not None else "-"
            time = f"{entry['execution_time_ms']}ms" if entry["execution_time_ms"] else "-"

            table.add_row(timestamp, entry["connection_name"], query, rows, time)

        console.print(table)

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise click.Abort()
