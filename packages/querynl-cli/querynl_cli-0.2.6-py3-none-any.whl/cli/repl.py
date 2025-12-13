"""
REPL (Read-Eval-Print Loop) mode for QueryNL CLI

Provides interactive query session with conversation context, history, and tab completion.
"""

import uuid
from typing import Optional, Dict
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.completion import Completer, Completion
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax

from .models import REPLSession
from .config import load_config, get_config_dir
from .credentials import get_password
from .database import DatabaseConnection
from .llm import LLMService
from .history import save_query_history, get_query_history
from .formatting.table import print_results
from .errors import ConfigError

console = Console()


class TableNameCompleter(Completer):
    """
    Tab completion for table names in REPL.

    Fetches table names from current database connection.
    """

    def __init__(self, session: REPLSession):
        self.session = session
        self.table_cache: list[str] = []

    def update_cache(self, tables: list[str]):
        """Update cached table names"""
        self.table_cache = tables

    def get_completions(self, document, complete_event):
        """Provide completions for current input (T025-T026)"""
        word = document.get_word_before_cursor()
        text = document.text_before_cursor

        # Complete REPL commands
        repl_commands = ["\\help", "\\connect", "\\tables", "\\schema", "\\history", "\\export", "\\exit", "\\quit"]

        # Schema design subcommands (T026, T035, T043-T049, T062-T067)
        schema_subcommands = ["\\schema design", "\\schema show", "\\schema save", "\\schema load", "\\schema list", "\\schema upload", "\\schema history", "\\schema finalize", "\\schema reset", "\\schema export", "\\schema execute", "\\schema validate", "\\schema help"]

        # If user typed "\schema " suggest subcommands
        if text.startswith("\\schema "):
            for subcmd in schema_subcommands:
                if subcmd.startswith(text.rstrip()):
                    yield Completion(subcmd[len(text):], start_position=0)
        else:
            # Complete main commands
            for cmd in repl_commands:
                if cmd.startswith(word):
                    yield Completion(cmd, start_position=-len(word))

        # Complete table names
        for table in self.table_cache:
            if table.startswith(word.lower()):
                yield Completion(table, start_position=-len(word))


class REPLManager:
    """
    Manages REPL session state and command execution.
    """

    def __init__(self, connection_name: Optional[str] = None):
        """
        Initialize REPL manager.

        Args:
            connection_name: Optional connection to use (defaults to default_connection)
        """
        self.config = load_config()
        self.session = REPLSession(
            session_id=str(uuid.uuid4()),
            connection_name=connection_name or self.config.default_connection
        )

        # Initialize LLM with API key from keychain or environment
        import keyring
        import os

        provider = self.config.llm_provider
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

        self.llm = LLMService(api_key=api_key, provider=provider)
        self.running = True
        self.last_result = None  # Store most recent query result for export

        # Initialize prompt_toolkit session
        config_dir = get_config_dir()
        history_file = config_dir / "repl_history"
        self.completer = TableNameCompleter(self.session)
        self.prompt_session = PromptSession(
            history=FileHistory(str(history_file)),
            completer=self.completer,
            complete_while_typing=True,
        )

        # Load table names for completion
        self._refresh_table_cache()

    def _refresh_table_cache(self):
        """Refresh cached table names for tab completion"""
        if not self.session.connection_name:
            return

        try:
            profile = self._get_active_profile()
            password = get_password(self.session.connection_name) if profile.database_type != "sqlite" else None
            conn_config = profile.get_connection_config(password)

            db = DatabaseConnection(conn_config)
            db.connect()

            # Query for table names
            sql = None
            if profile.database_type == "postgresql":
                sql = "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public';"
            elif profile.database_type == "mysql":
                sql = "SHOW TABLES;"
            elif profile.database_type == "sqlite":
                sql = "SELECT name FROM sqlite_master WHERE type='table';"

            if sql:
                result = db.execute_query(sql)
                if profile.database_type == "mysql":
                    # MySQL returns tables with key like 'Tables_in_dbname'
                    tables = [list(row.values())[0] for row in result.get("rows", [])]
                else:
                    # PostgreSQL and SQLite
                    column_name = "tablename" if profile.database_type == "postgresql" else "name"
                    tables = [row.get(column_name) for row in result.get("rows", []) if row.get(column_name)]
                self.completer.update_cache(tables)
            else:
                self.completer.update_cache([])

            db.close()

        except Exception as e:
            # Silently fail - tab completion just won't have table names
            # Log error for debugging but don't show to user
            import logging
            logging.debug(f"Failed to load table names for completion: {e}")
            pass

    def _get_active_profile(self):
        """Get active connection profile"""
        if not self.session.connection_name:
            raise ConfigError(
                "No active connection",
                suggestion="Use \\connect <name> to set a connection"
            )

        if self.session.connection_name not in self.config.connections:
            raise ConfigError(
                f"Connection '{self.session.connection_name}' not found",
                suggestion="Use \\connect <name> with a valid connection"
            )

        from .models import ConnectionProfile
        return ConnectionProfile.from_dict(self.config.connections[self.session.connection_name])

    def show_welcome(self):
        """Display welcome message"""
        from . import __version__

        welcome_text = f"""
[bold cyan]QueryNL REPL v{__version__}[/bold cyan]

Connected to: [green]{self.session.connection_name or 'None'}[/green]
Session ID: [dim]{self.session.session_id[:8]}[/dim]

Type your queries in natural language or use these commands:
  [cyan]\\help[/cyan]           - Show this help message
  [cyan]\\connect[/cyan]        - Switch database connection
  [cyan]\\tables[/cyan]         - List all tables
  [cyan]\\schema[/cyan]         - Show complete database schema
  [cyan]\\schema design[/cyan]  - Design schemas with AI (NEW!)
  [cyan]\\history[/cyan]        - Show query history
  [cyan]\\export[/cyan]         - Export last query result to file
  [cyan]\\exit[/cyan]           - Exit REPL

Press [bold]Ctrl+C[/bold] or type [bold]\\exit[/bold] to quit.
"""
        console.print(Panel(welcome_text, border_style="cyan"))

    def handle_command(self, command: str) -> bool:
        """
        Handle REPL-specific commands (starting with backslash).

        Args:
            command: Command string (e.g., "\\help", "\\connect my-db")

        Returns:
            True if command was handled, False otherwise
        """
        parts = command.strip().split(maxsplit=1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        if cmd in ["\\exit", "\\quit"]:
            self.running = False
            console.print("[dim]Goodbye![/dim]")
            return True

        elif cmd == "\\help":
            self._cmd_help()
            return True

        elif cmd == "\\connect":
            self._cmd_connect(args)
            return True

        elif cmd == "\\tables":
            self._cmd_tables()
            return True

        elif cmd == "\\schema":
            self._cmd_schema(args)
            return True

        elif cmd == "\\history":
            self._cmd_history()
            return True

        elif cmd == "\\export":
            self._cmd_export(args)
            return True

        else:
            console.print(f"[yellow]Unknown command: {cmd}[/yellow]")
            console.print("Type [bold]\\help[/bold] for available commands")
            return True

    def _cmd_help(self):
        """Display help for REPL commands"""
        table = Table(title="REPL Commands", show_header=True, header_style="bold cyan")
        table.add_column("Command", style="cyan")
        table.add_column("Description", style="white")

        table.add_row("\\help", "Show this help message")
        table.add_row("\\connect <name>", "Switch to different database connection")
        table.add_row("\\tables", "List all tables in current database")
        table.add_row("\\schema", "Show complete database schema (tree format)")
        table.add_row("\\schema graph", "Show graphical ER diagram with relationships")
        table.add_row("\\schema table", "Show schema in table format")
        table.add_row("\\schema detailed", "Show schema in detailed panel format")
        table.add_row("\\schema <table>", "Show schema for a specific table")
        table.add_row("", "")
        table.add_row("[bold cyan]\\schema design[/bold cyan]", "[bold]Design schemas with AI conversation[/bold]")
        table.add_row("\\schema show", "Show current schema design")
        table.add_row("\\schema save <name>", "Save schema design session")
        table.add_row("\\schema help", "Show schema design help")
        table.add_row("", "")
        table.add_row("\\history", "Show recent query history")
        table.add_row("\\export <file>", "Export last query result to file (CSV, JSON, SQL)")
        table.add_row("\\exit, \\quit", "Exit REPL mode")

        console.print(table)
        console.print("\n[dim]You can also type natural language queries directly.[/dim]")
        console.print("[dim]New: Use [cyan]\\schema design[/cyan] to design database schemas with AI![/dim]")
        console.print("[dim]Tip: Type 'add sample data' to populate your schema with test data![/dim]")

    def _cmd_connect(self, connection_name: str):
        """Switch active connection"""
        if not connection_name:
            console.print("[yellow]Usage: \\connect <name>[/yellow]")
            console.print("\nAvailable connections:")
            for name in self.config.connections.keys():
                marker = "● " if name == self.session.connection_name else "○ "
                console.print(f"  {marker}{name}")
            return

        if connection_name not in self.config.connections:
            console.print(f"[red]Connection '{connection_name}' not found[/red]")
            return

        self.session.connection_name = connection_name
        self._refresh_table_cache()
        console.print(f"[green]✓[/green] Switched to connection: [bold]{connection_name}[/bold]")

    def _cmd_tables(self):
        """List all tables in current database"""
        try:
            profile = self._get_active_profile()
            password = get_password(self.session.connection_name) if profile.database_type != "sqlite" else None
            conn_config = profile.get_connection_config(password)

            db = DatabaseConnection(conn_config)

            # Generate appropriate SQL for listing tables
            if profile.database_type == "postgresql":
                sql = "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public';"
            elif profile.database_type == "mysql":
                sql = "SHOW TABLES;"
            elif profile.database_type == "sqlite":
                sql = "SELECT name FROM sqlite_master WHERE type='table';"
            else:
                console.print(f"[yellow]Table listing not supported for {profile.database_type}[/yellow]")
                return

            result = db.execute_query(sql)
            print_results(result, "table")
            db.close()

        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")

    def _cmd_schema(self, args: str):
        """
        Handle schema commands - both introspection and design.

        Schema Design Commands (T018-T024):
            \\schema design [description] - Start/continue schema design conversation
            \\schema show [view]          - Show current schema design (text/erd/ddl)
            \\schema save <name>          - Save current schema design session
            \\schema load <name>          - Load named schema design session
            \\schema help                 - Show schema design help

        Schema Introspection Commands (existing):
            \\schema                      - Show all tables (tree format)
            \\schema graph                - Show ER diagram of existing database
            \\schema table                - Show tables in table format
        """
        # Parse first argument to determine command type
        if args:
            parts = args.split(maxsplit=1)
            subcommand = parts[0].lower()
            remaining_args = parts[1] if len(parts) > 1 else ""

            # Route to schema DESIGN commands (T018-T024, T035-T038, T043-T049, T062-T067)
            design_commands = ["design", "show", "save", "load", "list", "upload", "history", "finalize", "reset", "export", "execute", "validate", "help"]
            if subcommand in design_commands:
                return self._cmd_schema_design(subcommand, remaining_args)

        # Otherwise, handle as schema INTROSPECTION (existing functionality)
        try:
            profile = self._get_active_profile()
            password = get_password(self.session.connection_name) if profile.database_type != "sqlite" else None

            # Parse arguments to check for format option
            format_type = "tree"  # Default format
            table_name = ""

            if args:
                parts = args.split()

                # Check if first argument is a format type (simpler syntax: \schema graph)
                valid_formats = ["tree", "table", "detailed", "graph"]
                if parts and parts[0].lower() in valid_formats:
                    format_type = parts[0].lower()
                    parts = parts[1:]  # Remove format from parts
                # Otherwise check for --format option
                elif "--format" in parts or "-f" in parts:
                    format_idx = parts.index("--format") if "--format" in parts else parts.index("-f")
                    if format_idx + 1 < len(parts):
                        format_type = parts[format_idx + 1]
                        # Remove format args from parts
                        parts = [p for i, p in enumerate(parts) if i not in (format_idx, format_idx + 1)]

                # Remaining parts are table name
                table_name = " ".join(parts).strip()

            # If no table specified, show all tables
            if not table_name:
                from .schema_introspection import SchemaIntrospector
                from rich.tree import Tree

                console.print("[dim]Fetching database schema...[/dim]")
                introspector = SchemaIntrospector(profile, password)
                schema_data = introspector.get_schema()

                tables = schema_data.get("tables", {})

                if not tables:
                    console.print("[yellow]No tables found in database[/yellow]")
                    return

                # Display based on format type
                if format_type == "graph":
                    # Import the graph display function from schema command
                    from .commands.schema import _display_graph_format
                    _display_graph_format(schema_data, self.session.connection_name, profile.database_type, introspector)
                    return
                elif format_type == "table":
                    # Display in table format
                    from rich.table import Table as RichTable
                    for tbl_name in sorted(tables.keys()):
                        table_info = tables[tbl_name]
                        column_details = table_info.get("column_details", [])

                        if not column_details:
                            continue

                        display_table = RichTable(title=f"Table: {tbl_name}", show_header=True, header_style="bold cyan")
                        display_table.add_column("Column", style="green")
                        display_table.add_column("Type", style="cyan")
                        display_table.add_column("Nullable", style="yellow")
                        display_table.add_column("Default", style="dim")

                        for col in column_details:
                            col_name = col["name"]
                            col_type = col["type"]
                            nullable = "YES" if col.get("nullable", True) else "NO"
                            default = col.get("default", "")

                            display_table.add_row(col_name, col_type, nullable, default)

                        console.print(display_table)
                        console.print()

                    console.print(f"[dim]Total tables: {len(tables)}[/dim]")
                    return
                elif format_type == "detailed":
                    # Display in detailed panel format
                    from rich.panel import Panel
                    for tbl_name in sorted(tables.keys()):
                        table_info = tables[tbl_name]
                        column_details = table_info.get("column_details", [])

                        if not column_details:
                            continue

                        lines = []
                        for idx, col in enumerate(column_details, 1):
                            col_name = col["name"]
                            col_type = col["type"]
                            nullable = "NULL" if col.get("nullable", True) else "NOT NULL"
                            default = col.get("default", "")

                            lines.append(f"{idx}. [green]{col_name}[/green]")
                            lines.append(f"   Type: {col_type}")
                            lines.append(f"   Nullable: {nullable}")
                            if default:
                                lines.append(f"   Default: {default}")
                            lines.append("")

                        panel_content = "\n".join(lines)
                        console.print(Panel(panel_content, title=f"📋 {tbl_name} ({len(column_details)} columns)", border_style="cyan"))
                        console.print()

                    console.print(f"[dim]Total tables: {len(tables)}[/dim]")
                    return

                # Display in tree format (default)
                tree = Tree(f"[bold cyan]📊 Database Schema[/bold cyan]")

                for tbl_name in sorted(tables.keys()):
                    table_info = tables[tbl_name]
                    column_details = table_info.get("column_details", [])

                    if column_details:
                        table_branch = tree.add(f"[bold yellow]📋 {tbl_name}[/bold yellow] ({len(column_details)} columns)")

                        for col in column_details:
                            col_name = col["name"]
                            col_type = col["type"]
                            nullable = "NULL" if col.get("nullable", True) else "NOT NULL"

                            col_display = f"[green]{col_name}[/green] [dim]({col_type})[/dim] [cyan]{nullable}[/cyan]"
                            table_branch.add(col_display)
                    else:
                        tree.add(f"[bold yellow]📋 {tbl_name}[/bold yellow] (no columns)")

                console.print(tree)
                console.print(f"\n[dim]Total tables: {len(tables)}[/dim]")
                console.print("[dim]Tip: Use \\schema <table_name> to see details for a specific table[/dim]")
                console.print("[dim]     Use \\schema graph, \\schema table, or \\schema detailed for different views[/dim]")
                return

            # Show specific table schema
            conn_config = profile.get_connection_config(password)
            db = DatabaseConnection(conn_config)

            # Generate appropriate SQL for schema inspection
            if profile.database_type == "postgresql":
                sql = f"""
                    SELECT column_name, data_type, is_nullable, column_default
                    FROM information_schema.columns
                    WHERE table_name = '{table_name}' AND table_schema = 'public'
                    ORDER BY ordinal_position;
                """
            elif profile.database_type == "mysql":
                sql = f"DESCRIBE {table_name};"
            elif profile.database_type == "sqlite":
                sql = f"PRAGMA table_info({table_name});"
            else:
                console.print(f"[yellow]Schema inspection not supported for {profile.database_type}[/yellow]")
                return

            result = db.execute_query(sql)

            if result.get("row_count", 0) == 0:
                console.print(f"[yellow]Table '{table_name}' not found or has no columns[/yellow]")
            else:
                print_results(result, "table")

            db.close()

        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")

    def _cmd_history(self):
        """Show recent query history"""
        try:
            history = get_query_history(limit=10, connection_name=self.session.connection_name)

            if not history:
                console.print("[yellow]No query history found[/yellow]")
                return

            table = Table(title="Recent Queries", show_header=True, header_style="bold cyan")
            table.add_column("Time", style="dim")
            table.add_column("Query", style="white", max_width=60)
            table.add_column("Rows", style="green", justify="right")

            for entry in history:
                timestamp = entry["timestamp"].split("T")[1][:8] if "T" in entry["timestamp"] else entry["timestamp"]
                query = entry["natural_language_input"][:57] + "..." if len(entry["natural_language_input"]) > 60 else entry["natural_language_input"]
                rows = str(entry["row_count"]) if entry["row_count"] is not None else "-"

                table.add_row(timestamp, query, rows)

            console.print(table)

        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")

    def _cmd_export(self, file_path: str):
        """Export the most recent query result to a file"""
        if not file_path:
            console.print("[yellow]Usage: \\export <filepath>[/yellow]")
            console.print("\nExamples:")
            console.print("  \\export results.csv")
            console.print("  \\export output/data.json")
            console.print("  \\export backup.sql")
            console.print("\n[dim]Supported formats: csv, json, sql, mermaid, txt[/dim]")
            return

        if not self.last_result:
            console.print("[yellow]No query results to export[/yellow]")
            console.print("[dim]Execute a query first, then use \\export[/dim]")
            return

        try:
            from .export import export_to_file, ExportError

            profile = self._get_active_profile()

            export_result = export_to_file(
                result_data=self.last_result,
                file_path=file_path,
                database_type=profile.database_type
            )

            console.print(f"\n{export_result}")

        except ExportError as e:
            console.print(f"[red]Export failed:[/red] {e}")
        except Exception as e:
            console.print(f"[red]Unexpected error during export:[/red] {e}")

    def execute_query(self, query_text: str):
        """
        Execute natural language query with conversation context.

        Args:
            query_text: User's natural language query
        """
        try:
            # Check for test data generation intent (T024)
            if self._detect_test_data_intent(query_text):
                self._handle_test_data_generation(query_text)
                return

            profile = self._get_active_profile()
            password = get_password(self.session.connection_name) if profile.database_type != "sqlite" else None

            # Introspect database schema for intelligent query generation
            from .schema_introspection import SchemaIntrospector

            introspector = SchemaIntrospector(profile, password)
            schema = introspector.get_schema()

            # Add user message to context
            self.session.add_message("user", query_text)

            # Generate SQL with schema information
            result = self.llm.generate_sql(
                query_text,
                profile.database_type,
                schema=schema
            )

            sql = result.get("sql", "")
            explanation = result.get("explanation", "")

            # Display generated SQL
            console.print("\n[bold]Generated SQL:[/bold]")
            syntax = Syntax(sql, "sql", theme="monokai", line_numbers=False)
            console.print(syntax)

            if explanation:
                console.print(f"[dim]{explanation}[/dim]")

            # Execute query
            conn_config = profile.get_connection_config(password)
            db = DatabaseConnection(conn_config)

            query_result = db.execute_query(sql)

            # Store result for export
            self.last_result = query_result

            # Update session context
            self.session.update_results(query_result.get("rows", []))
            self.session.add_message("assistant", f"Query executed: {sql}")

            # Display results
            print_results(query_result, "table")

            # Save to history
            save_query_history(
                session_id=self.session.session_id,
                connection_name=self.session.connection_name,
                natural_language_input=query_text,
                generated_sql=sql,
                executed=True,
                execution_time_ms=query_result.get("execution_time_ms"),
                row_count=query_result.get("row_count"),
            )

            db.close()

        except Exception as e:
            console.print(f"\n[red]Error:[/red] {e}")
            self.session.add_message("assistant", f"Error: {e}")

    def _cmd_schema_design(self, subcommand: str, args: str):
        """
        Handle schema design commands (T018-T024).

        Args:
            subcommand: design, show, save, load, or help
            args: Remaining arguments
        """
        from .schema_design.session import SchemaSessionManager
        from .schema_design.conversation import SchemaConversation
        from .schema_design.schema_generator import SchemaGenerator
        from .schema_design.visualizer import MermaidERDGenerator
        from rich.table import Table as RichTable
        from rich.markdown import Markdown

        # Initialize schema session manager
        session_mgr = SchemaSessionManager()

        try:
            if subcommand == "help":
                # T024: Display schema design help
                self._schema_design_help()

            elif subcommand == "design":
                # T019: Start or continue schema design conversation
                self._schema_design_interactive(session_mgr, args)

            elif subcommand == "show":
                # T020-T022: Show current schema design
                view = args.strip() or "text"
                self._schema_show_design(session_mgr, view)

            elif subcommand == "save":
                # T023: Save current session with a name
                if not args.strip():
                    console.print("[yellow]Usage: \\schema save <name>[/yellow]")
                    return
                self._schema_save_session(session_mgr, args.strip())

            elif subcommand == "load":
                # Load a named session
                if not args.strip():
                    console.print("[yellow]Usage: \\schema load <name>[/yellow]")
                    return
                self._schema_load_session(session_mgr, args.strip())

            elif subcommand == "list":
                # List all sessions
                self._schema_list_sessions(session_mgr, args.strip())

            elif subcommand == "upload":
                # T035-T038: Upload and analyze data file
                if not args.strip():
                    console.print("[yellow]Usage: \\schema upload <file_path>[/yellow]")
                    return
                self._schema_upload_file(session_mgr, args.strip())

            elif subcommand == "history":
                # T043-T044: Show schema version history
                self._schema_show_history(session_mgr, args.strip())

            elif subcommand == "finalize":
                # T046-T047: Finalize schema design
                self._schema_finalize(session_mgr)

            elif subcommand == "reset":
                # T049: Reset session
                self._schema_reset(session_mgr)

            elif subcommand == "export":
                # T067: Export schema to file
                if not args.strip():
                    console.print("[yellow]Usage: \\schema export <filename>[/yellow]")
                    console.print("[dim]Supported formats: .json, .sql, .md[/dim]")
                    return
                self._schema_export(session_mgr, args.strip())

            elif subcommand == "execute":
                # T062-T064: Execute DDL in database
                self._schema_execute(session_mgr)

            elif subcommand == "validate":
                # T065-T066: Validate implemented schema
                self._schema_validate(session_mgr)

            else:
                console.print(f"[yellow]Unknown schema design command: {subcommand}[/yellow]")
                console.print("Type [cyan]\\schema help[/cyan] for available commands")

        except Exception as e:
            console.print(f"[red]Schema design error:[/red] {e}")
            import logging
            logging.error(f"Schema design command failed: {e}", exc_info=True)

    def _schema_design_help(self):
        """Display schema design help (T024)"""
        help_text = """
[bold cyan]Schema Design Commands[/bold cyan]

Design database schemas through natural language conversation:

  [cyan]\\schema design[/cyan]              Start/continue schema design conversation
  [cyan]\\schema design <description>[/cyan] Start with initial description
  [cyan]\\schema upload <file>[/cyan]       Upload and analyze CSV/Excel/JSON file
  [cyan]\\schema show [view][/cyan]         Show current schema (text/erd/ddl/mapping)
  [cyan]\\schema history [version][/cyan]   Show version history or specific version
  [cyan]\\schema finalize[/cyan]            Finalize schema design with validation
  [cyan]\\schema export <file>[/cyan]       Export schema (.json/.sql/.md)
  [cyan]\\schema execute[/cyan]             Execute DDL in connected database
  [cyan]\\schema validate[/cyan]            Validate implemented schema vs design
  [cyan]\\schema save <name>[/cyan]         Save current session
  [cyan]\\schema load <name>[/cyan]         Load saved session
  [cyan]\\schema list [status][/cyan]       List all sessions (filter: active/finalized/implemented)
  [cyan]\\schema reset[/cyan]               Reset session (requires confirmation)
  [cyan]\\schema help[/cyan]                Show this help

[bold]Views for \\schema show:[/bold]
  [cyan]text[/cyan]    - Tables and columns in text format (default)
  [cyan]erd[/cyan]     - Mermaid ER diagram
  [cyan]ddl[/cyan]     - SQL CREATE TABLE statements
  [cyan]mapping[/cyan] - File-to-table column mapping (after file upload)

[bold]Example Workflow:[/bold]
  1. [dim]\\schema design "I need to track customers and orders"[/dim]
  2. [dim]Conversation with AI about requirements...[/dim]
  3. [dim]\\schema show erd[/dim]
  4. [dim]\\schema save ecommerce[/dim]

[dim]Note: Schema design requires an active LLM service (OpenAI or Anthropic).[/dim]
"""
        console.print(Markdown(help_text))

    def _schema_design_interactive(self, session_mgr: 'SchemaSessionManager', initial_description: str):
        """
        Start interactive schema design conversation (T019).

        Args:
            session_mgr: Session manager instance
            initial_description: Optional initial description to start with
        """
        from .schema_design.conversation import SchemaConversation
        from .schema_design.schema_generator import SchemaGenerator

        # Get or create active session
        active_session = session_mgr.get_active_session()
        if not active_session:
            # Determine database type from active connection
            db_type = None
            if self.session.connection_name:
                try:
                    profile = self._get_active_profile()
                    db_type = profile.database_type
                except:
                    pass

            active_session = session_mgr.create_session(database_type=db_type)
            console.print(f"[green]✓[/green] Started new schema design session")
            console.print(f"[dim]Session ID: {active_session.id[:8]}...[/dim]")
            if db_type:
                console.print(f"[dim]Target database: {db_type}[/dim]")
        else:
            console.print(f"[green]✓[/green] Resuming schema design session")
            console.print(f"[dim]Session ID: {active_session.id[:8]}...[/dim]")
            if active_session.current_schema:
                console.print(f"[dim]Current schema has {len(active_session.current_schema.tables)} tables[/dim]")

        # Initialize conversation and generator
        conversation = SchemaConversation(self.llm, active_session)
        generator = SchemaGenerator(self.llm)

        # If initial description provided, process it
        if initial_description:
            console.print(f"\n[bold]You:[/bold] {initial_description}\n")
            try:
                response = conversation.process_user_input(initial_description)
                console.print(f"[bold cyan]Assistant:[/bold cyan] {response}\n")
                session_mgr.save_session(active_session)
            except Exception as e:
                console.print(f"[red]Error:[/red] {e}")
                return

        # Enter conversation mode
        console.print("[dim]Entering schema design mode. Type 'done' to exit, 'generate' to create schema.[/dim]\n")

        while True:
            try:
                user_input = self.prompt_session.prompt("You: ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ["done", "exit", "quit"]:
                    console.print("[dim]Exiting schema design mode.[/dim]")
                    break

                if user_input.lower() == "generate":
                    # Generate schema from conversation
                    console.print("\n[dim]Generating schema from conversation...[/dim]")
                    try:
                        # Build context from conversation
                        context = "\n".join([
                            f"{turn.role}: {turn.content}"
                            for turn in active_session.conversation_history[-10:]
                        ])

                        schema_proposal = generator.generate_from_description(
                            description=context,
                            database_type=active_session.database_type or "postgresql"
                        )

                        # Add to session
                        active_session.add_schema_version(schema_proposal)
                        session_mgr.save_session(active_session)

                        console.print(f"[green]✓[/green] Generated schema with {len(schema_proposal.tables)} tables")
                        console.print(f"[dim]Version: {schema_proposal.version}[/dim]")
                        console.print("\nUse [cyan]\\schema show[/cyan] to view the schema")
                        break

                    except Exception as e:
                        console.print(f"[red]Schema generation failed:[/red] {e}")
                        continue

                # Process user input through conversation
                response = conversation.process_user_input(user_input)
                console.print(f"\n[bold cyan]Assistant:[/bold cyan] {response}\n")

                # Save session after each turn
                session_mgr.save_session(active_session)

            except KeyboardInterrupt:
                console.print("\n[dim]Exiting schema design mode.[/dim]")
                break
            except EOFError:
                console.print("\n[dim]Exiting schema design mode.[/dim]")
                break

    def _schema_show_design(self, session_mgr: 'SchemaSessionManager', view: str):
        """
        Show current schema design in specified view (T020-T022, T037).

        Args:
            session_mgr: Session manager instance
            view: View type (text, erd, ddl, mapping)
        """
        from .schema_design.visualizer import MermaidERDGenerator
        from rich.table import Table as RichTable

        active_session = session_mgr.get_active_session()
        if not active_session or not active_session.current_schema:
            console.print("[yellow]No active schema design session.[/yellow]")
            console.print("Use [cyan]\\schema design[/cyan] to start designing a schema")
            return

        schema = active_session.current_schema

        if view == "text":
            # T021: Text view with Rich tables
            console.print(f"\n[bold cyan]Schema Design - Version {schema.version}[/bold cyan]")
            console.print(f"[dim]Database: {schema.database_type} | Normalization: {schema.normalization_level}[/dim]\n")

            for table in schema.tables:
                table_display = RichTable(title=f"Table: {table.name}", show_header=True, header_style="bold cyan")
                table_display.add_column("Column", style="green")
                table_display.add_column("Type", style="cyan")
                table_display.add_column("Constraints", style="yellow")

                for col in table.columns:
                    constraints = ", ".join(col.constraints) if col.constraints else ""
                    table_display.add_row(col.name, col.data_type, constraints)

                console.print(table_display)
                if table.description:
                    console.print(f"[dim]{table.description}[/dim]")
                console.print()

            if schema.rationale:
                console.print(f"[bold]Design Rationale:[/bold]\n{schema.rationale}\n")

        elif view == "erd":
            # T022: Mermaid ER diagram view
            mermaid_diagram = MermaidERDGenerator.generate(schema)
            console.print(f"\n[bold cyan]Schema ER Diagram - Version {schema.version}[/bold cyan]\n")
            syntax = Syntax(mermaid_diagram, "mermaid", theme="monokai", word_wrap=True)
            console.print(syntax)
            console.print("\n[dim]Copy this diagram to view in GitHub, VS Code, or any Mermaid viewer[/dim]")

        elif view == "ddl":
            # T062: DDL view with syntax highlighting
            from .schema_design.ddl_generator import DDLGenerator

            console.print(f"\n[bold cyan]Schema DDL - Version {schema.version}[/bold cyan]")
            console.print(f"[dim]Database: {schema.database_type}[/dim]\n")

            try:
                ddl = DDLGenerator.generate(schema)

                # Determine syntax highlighting language
                syntax_lang = "sql"
                if schema.database_type == "mongodb":
                    syntax_lang = "javascript"

                syntax = Syntax(ddl, syntax_lang, theme="monokai", line_numbers=True, word_wrap=True)
                console.print(syntax)

                console.print("\n[dim]Copy this DDL to execute in your database[/dim]")
                console.print("[dim]Use [cyan]\\schema execute[/cyan] to run these statements directly (coming soon)[/dim]")

            except Exception as e:
                console.print(f"[red]Failed to generate DDL:[/red] {e}")

        elif view == "mapping":
            # T037: File-to-table column mapping view
            if not active_session.uploaded_files:
                console.print("[yellow]No files uploaded in this session.[/yellow]")
                console.print("Use [cyan]\\schema upload <file>[/cyan] to upload data files")
                return

            console.print(f"\n[bold cyan]File-to-Schema Mapping[/bold cyan]\n")

            for uploaded_file in active_session.uploaded_files:
                analysis = uploaded_file.analysis

                # File header
                console.print(f"[bold]File:[/bold] {uploaded_file.file_name}")
                console.print(f"[dim]Detected entities: {', '.join(analysis.detected_entities)}[/dim]\n")

                # Column mapping table
                mapping_table = RichTable(title=f"Column Mapping: {uploaded_file.file_name}", show_header=True)
                mapping_table.add_column("File Column", style="cyan")
                mapping_table.add_column("Inferred Type", style="green")
                mapping_table.add_column("Suggested Table", style="yellow")
                mapping_table.add_column("Notes", style="dim")

                for col in analysis.columns:
                    # Determine suggested table based on column name and detected entities
                    suggested_table = "unknown"
                    notes = ""

                    # Check if column name matches an entity
                    col_lower = col.name.lower()
                    for entity in analysis.detected_entities:
                        if entity.lower() in col_lower or col_lower.startswith(entity.lower().rstrip('s')):
                            suggested_table = entity
                            break

                    # Check if it's a foreign key
                    if col_lower.endswith('_id'):
                        fk_entity = col_lower[:-3]
                        suggested_table = f"{fk_entity}s"  # Plural form
                        notes = "Foreign key candidate"

                    # Check if it's a primary key
                    if col_lower == 'id' or col.unique_values == analysis.row_count:
                        notes = "Primary key candidate"

                    mapping_table.add_row(
                        col.name,
                        col.inferred_type,
                        suggested_table,
                        notes
                    )

                console.print(mapping_table)
                console.print()

            # Show current schema mapping if exists
            if schema and schema.tables:
                console.print(f"[bold]Current Schema Tables:[/bold]")
                for table in schema.tables:
                    col_count = len(table.columns)
                    console.print(f"  • {table.name} ({col_count} columns)")
                console.print()

            console.print("[dim]Use [cyan]\\schema design[/cyan] to refine the schema based on this mapping[/dim]")

        else:
            console.print(f"[yellow]Unknown view: {view}[/yellow]")
            console.print("Valid views: [cyan]text[/cyan], [cyan]erd[/cyan], [cyan]ddl[/cyan], [cyan]mapping[/cyan]")

    def _schema_save_session(self, session_mgr: 'SchemaSessionManager', name: str):
        """
        Save current schema design session with a name (T023).

        Args:
            session_mgr: Session manager instance
            name: Session name
        """
        active_session = session_mgr.get_active_session()
        if not active_session:
            console.print("[yellow]No active schema design session to save.[/yellow]")
            return

        active_session.name = name
        session_mgr.save_session(active_session)
        console.print(f"[green]✓[/green] Saved schema design session as '[bold]{name}[/bold]'")
        console.print(f"[dim]Use '\\schema load {name}' to restore this session later[/dim]")

    def _schema_load_session(self, session_mgr: 'SchemaSessionManager', name: str):
        """
        Load a named schema design session.

        Args:
            session_mgr: Session manager instance
            name: Session name
        """
        try:
            loaded_session = session_mgr.load_session(name=name)
            console.print(f"[green]✓[/green] Loaded schema design session '[bold]{name}[/bold]'")
            console.print(f"[dim]Session ID: {loaded_session.id[:8]}...[/dim]")
            if loaded_session.current_schema:
                console.print(f"[dim]Current schema has {len(loaded_session.current_schema.tables)} tables (version {loaded_session.current_schema.version})[/dim]")
            console.print("\nUse [cyan]\\schema design[/cyan] to continue or [cyan]\\schema show[/cyan] to view")
        except Exception as e:
            console.print(f"[red]Failed to load session:[/red] {e}")

    def _schema_list_sessions(self, session_mgr: 'SchemaSessionManager', status_filter: str):
        """
        List all schema design sessions.

        Args:
            session_mgr: Session manager instance
            status_filter: Optional status filter (active/finalized/implemented)
        """
        from rich.table import Table as RichTable
        from datetime import datetime

        try:
            # Parse status filter if provided
            filter_status = None
            if status_filter:
                status_filter = status_filter.lower()
                if status_filter in ['active', 'finalized', 'implemented']:
                    filter_status = status_filter
                else:
                    console.print(f"[yellow]Invalid status filter: {status_filter}[/yellow]")
                    console.print("[dim]Valid options: active, finalized, implemented[/dim]")
                    return

            # Get sessions
            sessions = session_mgr.list_sessions(status=filter_status, limit=50)

            if not sessions:
                if filter_status:
                    console.print(f"[yellow]No {filter_status} sessions found.[/yellow]")
                else:
                    console.print("[yellow]No schema design sessions found.[/yellow]")
                console.print("\nUse [cyan]\\schema design[/cyan] to start a new session")
                return

            # Create rich table
            table = RichTable(title=f"Schema Design Sessions ({len(sessions)})")
            table.add_column("Name", style="cyan", no_wrap=True)
            table.add_column("Session ID", style="dim", no_wrap=True)
            table.add_column("Status", style="bold")
            table.add_column("Tables", justify="right")
            table.add_column("Database", style="dim")
            table.add_column("Updated", style="dim")

            for session in sessions:
                # Format session data
                name = session.name or "[dim]<unnamed>[/dim]"
                session_id = session.id[:8] + "..."

                # Status with color
                status_color = {
                    "active": "yellow",
                    "finalized": "blue",
                    "implemented": "green"
                }.get(session.status, "white")
                status_display = f"[{status_color}]{session.status}[/{status_color}]"

                # Table count
                table_count = str(len(session.current_schema.tables)) if session.current_schema else "0"

                # Database type
                db_type = session.database_type or "-"

                # Updated time (relative)
                try:
                    # session.updated_at could be datetime object or string
                    if isinstance(session.updated_at, str):
                        updated = datetime.fromisoformat(session.updated_at)
                    else:
                        updated = session.updated_at

                    now = datetime.now()
                    delta = now - updated

                    if delta.days > 0:
                        time_str = f"{delta.days}d ago"
                    elif delta.seconds > 3600:
                        time_str = f"{delta.seconds // 3600}h ago"
                    elif delta.seconds > 60:
                        time_str = f"{delta.seconds // 60}m ago"
                    else:
                        time_str = "just now"
                except Exception as e:
                    # Fallback to string representation
                    time_str = str(session.updated_at)[:19] if session.updated_at else "unknown"

                table.add_row(name, session_id, status_display, table_count, db_type, time_str)

            console.print()
            console.print(table)
            console.print()
            console.print("[bold]Commands:[/bold]")
            console.print("  [cyan]\\schema load <name>[/cyan]   - Load a saved session")
            console.print("  [cyan]\\schema list <status>[/cyan] - Filter by status (active/finalized/implemented)")
            console.print()

        except Exception as e:
            console.print(f"[red]Failed to list sessions:[/red] {e}")
            import logging
            logging.error(f"Schema list failed: {e}", exc_info=True)

    def _schema_upload_file(self, session_mgr: 'SchemaSessionManager', file_path: str):
        """
        Upload and analyze a data file (T035-T038).

        Args:
            session_mgr: Session manager instance
            file_path: Path to file to upload
        """
        from .schema_design.file_analyzer import FileAnalyzer
        from .schema_design import (
            FileTooLargeError,
            UnsupportedFileTypeError,
            FileParseError
        )
        from rich.table import Table as RichTable
        from pathlib import Path

        try:
            # T038: Error handling for file upload
            file_path_obj = Path(file_path).expanduser().resolve()

            if not file_path_obj.exists():
                console.print(f"[red]File not found:[/red] {file_path}")
                console.print(f"[dim]Checked path: {file_path_obj}[/dim]")
                return

            # Get or create active session
            active_session = session_mgr.get_active_session()
            if not active_session:
                # Determine database type from active connection
                db_type = None
                if self.session.connection_name:
                    try:
                        profile = self._get_active_profile()
                        db_type = profile.database_type
                    except:
                        pass

                active_session = session_mgr.create_session(database_type=db_type)
                console.print(f"[green]✓[/green] Started new schema design session")

            # T035: Analyze file
            console.print(f"\n[bold]Analyzing file:[/bold] {file_path_obj.name}")
            console.print(f"[dim]Path: {file_path_obj}[/dim]\n")

            analyzer = FileAnalyzer()
            uploaded_file = analyzer.analyze_file(str(file_path_obj))

            # Add to session
            active_session.uploaded_files.append(uploaded_file)
            session_mgr.save_session(active_session)

            # T036: Display file analysis with Rich tables
            console.print(f"[green]✓[/green] File analyzed successfully\n")

            # File summary
            analysis = uploaded_file.analysis
            summary_table = RichTable(title=f"File Summary: {uploaded_file.file_name}", show_header=False)
            summary_table.add_column("Property", style="cyan")
            summary_table.add_column("Value")

            size_mb = uploaded_file.file_size_bytes / (1024 * 1024)
            summary_table.add_row("File Type", uploaded_file.file_type.upper())
            summary_table.add_row("File Size", f"{size_mb:.2f} MB")
            summary_table.add_row("Rows", str(analysis.row_count))
            summary_table.add_row("Columns", str(analysis.column_count))
            summary_table.add_row("Detected Entities", ", ".join(analysis.detected_entities))

            console.print(summary_table)
            console.print()

            # Column details
            columns_table = RichTable(title="Column Analysis", show_header=True)
            columns_table.add_column("Column Name", style="cyan")
            columns_table.add_column("Type", style="green")
            columns_table.add_column("Nullable", style="yellow")
            columns_table.add_column("Unique Values", justify="right")
            columns_table.add_column("Sample Values", style="dim")

            for col in analysis.columns:
                nullable = "✓" if col.nullable else "✗"
                samples = ", ".join(str(v) for v in col.sample_values[:3])
                columns_table.add_row(
                    col.name,
                    col.inferred_type,
                    nullable,
                    str(col.unique_values),
                    samples
                )

            console.print(columns_table)

            # Show relationships if detected
            if analysis.potential_relationships:
                console.print()
                rel_table = RichTable(title="Detected Relationships", show_header=True)
                rel_table.add_column("From Column", style="cyan")
                rel_table.add_column("To File", style="green")
                rel_table.add_column("To Column", style="green")
                rel_table.add_column("Confidence", justify="right")

                for rel in analysis.potential_relationships:
                    conf_color = "green" if rel.confidence >= 0.8 else "yellow" if rel.confidence >= 0.6 else "red"
                    rel_table.add_row(
                        rel.from_column,
                        rel.to_file,
                        rel.to_column,
                        f"[{conf_color}]{rel.confidence:.0%}[/{conf_color}]"
                    )

                console.print(rel_table)

            # Next steps
            console.print()
            console.print("[bold]Next steps:[/bold]")
            console.print("  [cyan]\\schema design[/cyan]  - Start conversation to refine schema")
            console.print("  [cyan]\\schema show mapping[/cyan]  - View file-to-table mapping")
            console.print("  [dim]Or continue uploading more files to detect cross-file relationships[/dim]")

        except FileTooLargeError as e:
            console.print(f"[red]File too large:[/red] {e}")
            console.print("[dim]Maximum file size is 100MB[/dim]")

        except UnsupportedFileTypeError as e:
            console.print(f"[red]Unsupported file type:[/red] {e}")
            console.print("[dim]Supported formats: CSV (.csv), Excel (.xlsx, .xls), JSON (.json)[/dim]")

        except FileParseError as e:
            console.print(f"[red]File parsing error:[/red] {e}")
            console.print("[dim]Ensure the file is properly formatted and not corrupted[/dim]")

        except Exception as e:
            console.print(f"[red]Upload failed:[/red] {e}")
            import logging
            logging.error(f"File upload failed: {e}", exc_info=True)

    def _schema_show_history(self, session_mgr: 'SchemaSessionManager', version_arg: str):
        """
        Show schema version history (T043-T044).

        Args:
            session_mgr: Session manager instance
            version_arg: Optional version number to show specific version
        """
        from rich.table import Table as RichTable
        from rich.panel import Panel

        active_session = session_mgr.get_active_session()
        if not active_session:
            console.print("[yellow]No active schema design session.[/yellow]")
            console.print("Use [cyan]\\schema design[/cyan] to start designing a schema")
            return

        if not active_session.schema_versions:
            console.print("[yellow]No schema versions in this session.[/yellow]")
            console.print("Use [cyan]\\schema design[/cyan] and type 'generate' to create a schema")
            return

        # Show specific version if requested
        if version_arg:
            try:
                version_num = int(version_arg)
                if version_num < 1 or version_num > len(active_session.schema_versions):
                    console.print(f"[red]Invalid version number.[/red] Valid range: 1-{len(active_session.schema_versions)}")
                    return

                # Show specific version details
                schema = active_session.schema_versions[version_num - 1]
                console.print(f"\n[bold cyan]Schema Version {schema.version}[/bold cyan]")
                console.print(f"[dim]Created: {schema.created_at}[/dim]")
                console.print(f"[dim]Database: {schema.database_type} | Normalization: {schema.normalization_level}[/dim]\n")

                # Tables summary
                for table in schema.tables:
                    table_display = RichTable(title=f"Table: {table.name}", show_header=True, header_style="bold cyan")
                    table_display.add_column("Column", style="green")
                    table_display.add_column("Type", style="cyan")
                    table_display.add_column("Constraints", style="yellow")

                    for col in table.columns:
                        constraints = ", ".join(col.constraints) if col.constraints else ""
                        table_display.add_row(col.name, col.data_type, constraints)

                    console.print(table_display)
                    if table.description:
                        console.print(f"[dim]{table.description}[/dim]")
                    console.print()

                if schema.rationale:
                    console.print(Panel(schema.rationale, title="Design Rationale", border_style="dim"))

            except ValueError:
                console.print(f"[red]Invalid version number:[/red] {version_arg}")
                console.print("Usage: [cyan]\\schema history <version_number>[/cyan]")
            return

        # Show version history list
        console.print(f"\n[bold cyan]Schema Version History[/bold cyan]")
        console.print(f"[dim]Session: {active_session.id[:8]}...[/dim]\n")

        history_table = RichTable(show_header=True, header_style="bold cyan")
        history_table.add_column("Version", justify="right", style="cyan")
        history_table.add_column("Created", style="dim")
        history_table.add_column("Tables", justify="right")
        history_table.add_column("Database", style="green")
        history_table.add_column("Changes", style="yellow")

        for i, schema in enumerate(active_session.schema_versions):
            # Determine what changed from previous version
            changes = "Initial design"
            if i > 0:
                prev_schema = active_session.schema_versions[i - 1]
                prev_tables = {t.name for t in prev_schema.tables}
                curr_tables = {t.name for t in schema.tables}

                added = curr_tables - prev_tables
                removed = prev_tables - curr_tables

                change_parts = []
                if added:
                    change_parts.append(f"+{len(added)} tables")
                if removed:
                    change_parts.append(f"-{len(removed)} tables")
                if not added and not removed:
                    change_parts.append("Modified")

                changes = ", ".join(change_parts) if change_parts else "No changes"

            # Mark current version
            version_str = f"{schema.version}"
            if i == len(active_session.schema_versions) - 1:
                version_str = f"[bold]{schema.version} (current)[/bold]"

            history_table.add_row(
                version_str,
                schema.created_at.strftime("%Y-%m-%d %H:%M") if hasattr(schema.created_at, 'strftime') else str(schema.created_at),
                str(len(schema.tables)),
                schema.database_type,
                changes
            )

        console.print(history_table)
        console.print()
        console.print("[dim]Use [cyan]\\schema history <version>[/cyan] to view details of a specific version[/dim]")

    def _schema_finalize(self, session_mgr: 'SchemaSessionManager'):
        """
        Finalize schema design with validation (T046-T047).

        Args:
            session_mgr: Session manager instance
        """
        from .schema_design.schema_generator import SchemaGenerator

        active_session = session_mgr.get_active_session()
        if not active_session:
            console.print("[yellow]No active schema design session.[/yellow]")
            console.print("Use [cyan]\\schema design[/cyan] to start designing a schema")
            return

        if not active_session.current_schema:
            console.print("[yellow]No schema to finalize.[/yellow]")
            console.print("Use [cyan]\\schema design[/cyan] and type 'generate' to create a schema first")
            return

        if active_session.status == "finalized":
            console.print("[yellow]Schema is already finalized.[/yellow]")
            console.print("Use [cyan]\\schema reset[/cyan] to start over or [cyan]\\schema design[/cyan] to refine")
            return

        # T047: Run validation checks
        console.print("\n[bold]Validating schema design...[/bold]\n")

        generator = SchemaGenerator(self.llm)
        validation_result = generator.validate_schema(active_session.current_schema)

        # Display validation results
        if validation_result["errors"]:
            console.print("[red]✗ Validation failed with errors:[/red]\n")
            for error in validation_result["errors"]:
                console.print(f"  [red]•[/red] {error}")
            console.print("\n[yellow]Please fix these errors before finalizing.[/yellow]")
            console.print("Use [cyan]\\schema design[/cyan] to refine the schema")
            return

        if validation_result["warnings"]:
            console.print("[yellow]⚠ Validation passed with warnings:[/yellow]\n")
            for warning in validation_result["warnings"]:
                console.print(f"  [yellow]•[/yellow] {warning}")
            console.print()

            # Ask for confirmation
            try:
                confirmation = input("Proceed with finalization despite warnings? (yes/no): ").strip().lower()
                if confirmation not in ["yes", "y"]:
                    console.print("[dim]Finalization cancelled.[/dim]")
                    return
            except (KeyboardInterrupt, EOFError):
                console.print("\n[dim]Finalization cancelled.[/dim]")
                return
        else:
            console.print("[green]✓ Validation passed with no errors or warnings[/green]\n")

        # Update session status to finalized
        active_session.status = "finalized"
        session_mgr.save_session(active_session)

        console.print("[green]✓ Schema design finalized[/green]")
        console.print(f"[dim]Session: {active_session.id[:8]}...[/dim]")
        console.print(f"[dim]Version: {active_session.current_schema.version}[/dim]")
        console.print(f"[dim]Tables: {len(active_session.current_schema.tables)}[/dim]\n")

        console.print("[bold]Next steps:[/bold]")
        console.print("  [cyan]\\schema show ddl[/cyan]      - View DDL statements")
        console.print("  [cyan]\\schema export <file>[/cyan] - Export to .sql, .json, or .md")
        console.print("  [cyan]\\schema execute[/cyan]       - Execute DDL in connected database")
        console.print("  [cyan]\\schema save <name>[/cyan]   - Save this session for later")

    def _schema_reset(self, session_mgr: 'SchemaSessionManager'):
        """
        Reset current session (T049).

        Args:
            session_mgr: Session manager instance
        """
        active_session = session_mgr.get_active_session()
        if not active_session:
            console.print("[yellow]No active schema design session to reset.[/yellow]")
            return

        # Show what will be lost
        console.print("\n[bold yellow]⚠ Warning: This will delete the current session[/bold yellow]\n")
        console.print(f"Session ID: {active_session.id[:8]}...")
        if active_session.name:
            console.print(f"Session Name: {active_session.name}")
        console.print(f"Schema Versions: {len(active_session.schema_versions)}")
        console.print(f"Uploaded Files: {len(active_session.uploaded_files)}")
        console.print(f"Conversation Turns: {len(active_session.conversation_history)}")
        console.print()

        # Confirmation prompt
        try:
            confirmation = input("Type 'reset' to confirm deletion: ").strip()
            if confirmation != "reset":
                console.print("[dim]Reset cancelled.[/dim]")
                return
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Reset cancelled.[/dim]")
            return

        # Delete the session
        try:
            session_mgr.delete_session(active_session.id)
            console.print("[green]✓ Session deleted successfully[/green]")
            console.print("\nUse [cyan]\\schema design[/cyan] to start a new session")
        except Exception as e:
            console.print(f"[red]Failed to delete session:[/red] {e}")

    def _schema_export(self, session_mgr: 'SchemaSessionManager', file_path: str):
        """
        Export schema to file (T067).

        Supports .json, .sql, and .md formats.

        Args:
            session_mgr: Session manager instance
            file_path: Path to export file
        """
        from pathlib import Path
        import json

        active_session = session_mgr.get_active_session()
        if not active_session:
            console.print("[yellow]No active schema design session.[/yellow]")
            console.print("Use [cyan]\\schema design[/cyan] to start designing a schema")
            return

        if not active_session.current_schema:
            console.print("[yellow]No schema to export.[/yellow]")
            console.print("Use [cyan]\\schema design[/cyan] and type 'generate' to create a schema first")
            return

        schema = active_session.current_schema
        path = Path(file_path).expanduser()
        extension = path.suffix.lower()

        try:
            if extension == '.json':
                # Export as JSON
                schema_dict = {
                    "version": schema.version,
                    "database_type": schema.database_type,
                    "normalization_level": schema.normalization_level,
                    "created_at": schema.created_at.isoformat() if hasattr(schema.created_at, 'isoformat') else str(schema.created_at),
                    "tables": [
                        {
                            "name": table.name,
                            "description": table.description,
                            "columns": [
                                {
                                    "name": col.name,
                                    "data_type": col.data_type,
                                    "constraints": col.constraints,
                                    "default_value": col.default_value,
                                    "description": col.description
                                }
                                for col in table.columns
                            ],
                            "indexes": [
                                {
                                    "name": idx.name,
                                    "columns": idx.columns,
                                    "unique": idx.unique,
                                    "type": idx.type
                                }
                                for idx in table.indexes
                            ] if table.indexes else []
                        }
                        for table in schema.tables
                    ],
                    "relationships": [
                        {
                            "from_table": rel.from_table,
                            "to_table": rel.to_table,
                            "type": rel.type,
                            "foreign_key": rel.foreign_key,
                            "description": rel.description
                        }
                        for rel in schema.relationships
                    ] if schema.relationships else [],
                    "rationale": schema.rationale
                }

                with open(path, 'w') as f:
                    json.dump(schema_dict, f, indent=2)

                console.print(f"[green]✓[/green] Exported schema to JSON: [bold]{path}[/bold]")

            elif extension == '.sql':
                # Export as SQL DDL
                from .schema_design.ddl_generator import DDLGenerator

                ddl = DDLGenerator.generate(schema)

                with open(path, 'w') as f:
                    f.write(ddl)

                console.print(f"[green]✓[/green] Exported schema to SQL: [bold]{path}[/bold]")
                console.print(f"[dim]Database: {schema.database_type}[/dim]")

            elif extension == '.md':
                # Export as Markdown
                from .schema_design.visualizer import MermaidERDGenerator

                md_parts = [
                    f"# Schema: {active_session.name or 'Untitled'}",
                    f"",
                    f"**Version**: {schema.version}",
                    f"**Database**: {schema.database_type}",
                    f"**Normalization**: {schema.normalization_level}",
                    f"**Created**: {schema.created_at}",
                    f"",
                    f"## Design Rationale",
                    f"",
                    schema.rationale or "No rationale provided",
                    f"",
                    f"## ER Diagram",
                    f"",
                    f"```mermaid",
                    MermaidERDGenerator.generate(schema),
                    f"```",
                    f"",
                    f"## Tables",
                    f""
                ]

                for table in schema.tables:
                    md_parts.append(f"### {table.name}")
                    if table.description:
                        md_parts.append(f"*{table.description}*")
                    md_parts.append("")
                    md_parts.append("| Column | Type | Constraints |")
                    md_parts.append("|--------|------|-------------|")

                    for col in table.columns:
                        constraints = ", ".join(col.constraints) if col.constraints else ""
                        md_parts.append(f"| {col.name} | {col.data_type} | {constraints} |")

                    md_parts.append("")

                    if table.indexes:
                        md_parts.append("**Indexes**:")
                        for idx in table.indexes:
                            unique_str = "UNIQUE " if idx.unique else ""
                            md_parts.append(f"- {unique_str}{idx.name} on ({', '.join(idx.columns)})")
                        md_parts.append("")

                markdown = "\n".join(md_parts)

                with open(path, 'w') as f:
                    f.write(markdown)

                console.print(f"[green]✓[/green] Exported schema to Markdown: [bold]{path}[/bold]")

            else:
                console.print(f"[red]Unsupported file format:[/red] {extension}")
                console.print("[dim]Supported formats: .json, .sql, .md[/dim]")
                return

            console.print(f"[dim]Exported {len(schema.tables)} tables[/dim]")

        except Exception as e:
            console.print(f"[red]Export failed:[/red] {e}")
            import logging
            logging.error(f"Schema export failed: {e}", exc_info=True)

    def _schema_execute(self, session_mgr: 'SchemaSessionManager'):
        """
        Execute DDL in connected database (T062-T064).

        Requires active database connection.
        Executes with confirmation and rollback on errors.

        Args:
            session_mgr: Session manager instance
        """
        active_session = session_mgr.get_active_session()
        if not active_session:
            console.print("[yellow]No active schema design session.[/yellow]")
            console.print("Use [cyan]\\schema design[/cyan] to start designing a schema")
            return

        if not active_session.current_schema:
            console.print("[yellow]No schema to execute.[/yellow]")
            console.print("Use [cyan]\\schema design[/cyan] and type 'generate' to create a schema first")
            return

        if active_session.status != "finalized":
            console.print("[yellow]Schema must be finalized before execution.[/yellow]")
            console.print("Use [cyan]\\schema finalize[/cyan] to validate and finalize the schema")
            return

        # T063: Pre-execution validation checks
        if not self.session.connection_name:
            console.print("[red]No database connection active.[/red]")
            console.print("Use [cyan]\\connect add <name>[/cyan] to add a connection")
            console.print("Use [cyan]\\connect use <name>[/cyan] to activate a connection")
            return

        schema = active_session.current_schema

        # Check database type matches
        try:
            profile = self._get_active_profile()
            if profile.database_type != schema.database_type:
                console.print(f"[yellow]⚠ Warning: Schema is designed for {schema.database_type}, but connected to {profile.database_type}[/yellow]")
                try:
                    confirmation = input("Continue anyway? (yes/no): ").strip().lower()
                    if confirmation not in ["yes", "y"]:
                        console.print("[dim]Execution cancelled.[/dim]")
                        return
                except (KeyboardInterrupt, EOFError):
                    console.print("\n[dim]Execution cancelled.[/dim]")
                    return
        except Exception as e:
            console.print(f"[red]Could not verify database connection:[/red] {e}")
            return

        # Generate DDL
        from .schema_design.ddl_generator import DDLGenerator

        try:
            ddl = DDLGenerator.generate(schema)
        except Exception as e:
            console.print(f"[red]Failed to generate DDL:[/red] {e}")
            return

        # Display DDL
        console.print(f"\n[bold cyan]Generated DDL for {schema.database_type}[/bold cyan]\n")

        syntax_lang = "sql" if schema.database_type != "mongodb" else "javascript"
        syntax = Syntax(ddl, syntax_lang, theme="monokai", line_numbers=True)
        console.print(syntax)

        console.print(f"\n[bold]This will execute {len(schema.tables)} CREATE TABLE statements[/bold]")

        # Confirmation prompt
        console.print("\n[yellow]⚠ Warning: This will modify your database[/yellow]")
        try:
            confirmation = input("Type 'EXECUTE' to confirm: ").strip()
            if confirmation != "EXECUTE":
                console.print("[dim]Execution cancelled.[/dim]")
                return
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Execution cancelled.[/dim]")
            return

        # T064: Execute with transaction and rollback on errors
        from .credentials import get_password
        from .database import DatabaseConnection

        console.print("\n[bold]Executing DDL...[/bold]\n")

        try:
            password = get_password(self.session.connection_name) if profile.database_type != "sqlite" else None
            conn_config = profile.get_connection_config(password)
            db = DatabaseConnection(conn_config)

            # Split DDL into individual statements and filter out comments
            raw_statements = ddl.split(';')
            statements = []

            for stmt in raw_statements:
                # Remove comment lines but keep the SQL
                lines = stmt.strip().split('\n')
                sql_lines = [line for line in lines if line.strip() and not line.strip().startswith('--')]

                if sql_lines:
                    clean_stmt = '\n'.join(sql_lines).strip()
                    if clean_stmt:
                        statements.append(clean_stmt)

            if not statements:
                console.print("[yellow]No DDL statements to execute.[/yellow]")
                return

            # Execute with progress
            from rich.progress import Progress, SpinnerColumn, TextColumn

            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task(f"Executing {len(statements)} statements...", total=len(statements))

                for i, statement in enumerate(statements, 1):
                    # Skip comments
                    if statement.startswith('--') or statement.startswith('//'):
                        continue

                    try:
                        # Execute statement
                        db.execute_query(statement)
                        progress.update(task, advance=1, description=f"Executed statement {i}/{len(statements)}")

                    except Exception as e:
                        console.print(f"\n[red]✗ Execution failed on statement {i}:[/red]")
                        console.print(f"[red]{str(e)}[/red]")
                        console.print(f"\n[yellow]Rolling back changes...[/yellow]")

                        # Note: Actual rollback depends on database support
                        # PostgreSQL/MySQL support transactions, SQLite may have limitations
                        db.close()
                        console.print("[yellow]Some changes may have been committed before the error.[/yellow]")
                        console.print("[dim]Manual cleanup may be required.[/dim]")
                        return

            db.close()

            # T068: Update session status
            active_session.status = "implemented"
            session_mgr.save_session(active_session)

            console.print(f"\n[green]✓ Schema successfully implemented in database[/green]")
            console.print(f"[dim]Connection: {self.session.connection_name}[/dim]")
            console.print(f"[dim]Tables created: {len(schema.tables)}[/dim]")

            console.print("\n[bold]Next steps:[/bold]")
            console.print("  [cyan]\\tables[/cyan]           - View created tables")
            console.print("  [cyan]\\schema validate[/cyan]  - Validate implementation matches design")

        except Exception as e:
            console.print(f"[red]Execution failed:[/red] {e}")
            import logging
            logging.error(f"DDL execution failed: {e}", exc_info=True)

    def _schema_validate(self, session_mgr: 'SchemaSessionManager'):
        """
        Validate implemented schema matches design (T065-T066).

        Compares designed schema with actual database structure.

        Args:
            session_mgr: Session manager instance
        """
        active_session = session_mgr.get_active_session()
        if not active_session:
            console.print("[yellow]No active schema design session.[/yellow]")
            console.print("Use [cyan]\\schema design[/cyan] to start designing a schema")
            return

        if not active_session.current_schema:
            console.print("[yellow]No schema design to validate.[/yellow]")
            return

        if not self.session.connection_name:
            console.print("[red]No database connection active.[/red]")
            console.print("Use [cyan]\\connect use <name>[/cyan] to connect to a database")
            return

        schema = active_session.current_schema

        console.print(f"\n[bold]Validating schema implementation...[/bold]\n")
        console.print(f"Design: {len(schema.tables)} tables (version {schema.version})")
        console.print(f"Connection: {self.session.connection_name}\n")

        # Get actual database schema
        from .credentials import get_password
        from .schema_introspection import SchemaIntrospector

        try:
            profile = self._get_active_profile()
            password = get_password(self.session.connection_name) if profile.database_type != "sqlite" else None

            console.print("[dim][INFO] Introspecting database schema...[/dim]")
            introspector = SchemaIntrospector(profile, password)
            actual_schema = introspector.get_schema()

        except Exception as e:
            console.print(f"[red][ERROR] Schema introspection failed:[/red] {e}")
            import logging
            logging.error(f"Schema validation failed: {e}", exc_info=True)

        # T066: Compare and display discrepancies
        from rich.table import Table as RichTable

        validation_table = RichTable(title="Validation Results", show_header=True)
        validation_table.add_column("Table", style="cyan")
        validation_table.add_column("Status", style="bold")
        validation_table.add_column("Notes")

        discrepancies = []
        all_valid = True

        # Check each designed table
        for designed_table in schema.tables:
            table_name = designed_table.name
            actual_table = actual_schema.get("tables", {}).get(table_name)

            if not actual_table:
                validation_table.add_row(
                    table_name,
                    "[red]✗ MISSING[/red]",
                    "Table does not exist in database"
                )
                discrepancies.append(f"Table {table_name} is missing")
                all_valid = False
                continue

            # Check columns
            designed_cols = {col.name for col in designed_table.columns}
            actual_cols = set(actual_table.get("columns", []))

            missing_cols = designed_cols - actual_cols
            extra_cols = actual_cols - designed_cols

            if missing_cols or extra_cols:
                notes = []
                if missing_cols:
                    notes.append(f"Missing columns: {', '.join(missing_cols)}")
                    discrepancies.append(f"Table {table_name}: missing columns {', '.join(missing_cols)}")
                if extra_cols:
                    notes.append(f"Extra columns: {', '.join(extra_cols)}")

                validation_table.add_row(
                    table_name,
                    "[yellow]⚠ PARTIAL[/yellow]",
                    "; ".join(notes)
                )
                all_valid = False
            else:
                validation_table.add_row(
                    table_name,
                    "[green]✓ VALID[/green]",
                    f"{len(designed_cols)} columns match"
                )

        # Check for extra tables in database
        designed_table_names = {t.name for t in schema.tables}
        actual_table_names = set(actual_schema.get("tables", {}).keys())
        extra_tables = actual_table_names - designed_table_names

        for extra_table in extra_tables:
            validation_table.add_row(
                extra_table,
                "[yellow]⚠ EXTRA[/yellow]",
                "Table exists but not in design"
            )

        console.print(validation_table)
        console.print()

        if all_valid and not extra_tables:
            console.print("[green]✓ Schema implementation matches design perfectly[/green]")
            console.print(f"[dim]All {len(schema.tables)} tables validated successfully[/dim]")
        else:
            console.print("[yellow]⚠ Schema implementation has discrepancies[/yellow]")
            if discrepancies:
                console.print("\n[bold]Issues found:[/bold]")
                for issue in discrepancies:
                    console.print(f"  [red]•[/red] {issue}")

            console.print("\n[bold]Recommendations:[/bold]")
            console.print("  1. Review the differences above")
            console.print("  2. Use [cyan]\\schema show ddl[/cyan] to see the designed schema")
            console.print("  3. Manually adjust the database or regenerate the schema")

    def _detect_test_data_intent(self, query_text: str) -> bool:
        """Detect if user is requesting test data generation (T024).

        Args:
            query_text: User's natural language query

        Returns:
            True if test data intent detected
        """
        query_lower = query_text.lower()

        # Keywords that indicate test data generation
        test_data_keywords = [
            'add sample data',
            'add test data',
            'generate sample data',
            'generate test data',
            'populate',
            'insert sample',
            'insert test',
            'create sample data',
            'create test data',
            'fill with data',
            'add some data',
            'add data to',
        ]

        return any(keyword in query_lower for keyword in test_data_keywords)

    def _parse_record_counts(self, query_text: str) -> Optional[Dict[str, int]]:
        """Parse record count specifications from user query (T029).

        Extracts patterns like:
        - "add 100 users"
        - "add 50 customers and 200 orders"
        - "generate 1000 records"

        Args:
            query_text: User's natural language query

        Returns:
            Dictionary mapping table names to counts, or None if no counts specified
        """
        import re

        record_counts = {}

        # Pattern 1: "N <table_name>" or "N <table_name>s"
        # e.g., "add 100 users", "generate 50 customers"
        pattern1 = r'\b(\d+)\s+([a-zA-Z_][a-zA-Z0-9_]*?)s?\b'
        matches = re.findall(pattern1, query_text.lower())

        for count_str, table_name in matches:
            count = int(count_str)
            # Remove common words that aren't table names
            if table_name not in ['sample', 'test', 'fake', 'some', 'data', 'records', 'rows']:
                record_counts[table_name] = count

        # Pattern 2: "N records per table"
        pattern2 = r'(\d+)\s+records?\s+per\s+table'
        match = re.search(pattern2, query_text.lower())
        if match:
            # This means all tables get the same count - we'll handle this in the generator
            # Return a special marker
            return {'__all__': int(match.group(1))}

        return record_counts if record_counts else None

    def _parse_domain_context(self, query_text: str) -> Optional[str]:
        """Parse domain context from user query (T033).

        Detects domain-specific keywords like:
        - "e-commerce"
        - "blog"
        - "social media"
        - "medical"

        Args:
            query_text: User's natural language query

        Returns:
            Domain context string or None
        """
        query_lower = query_text.lower()

        # Domain context keywords
        domain_keywords = {
            'e-commerce': ['e-commerce', 'ecommerce', 'store', 'shop', 'product', 'cart', 'checkout'],
            'blog': ['blog', 'post', 'article', 'comment'],
            'social media': ['social media', 'social', 'twitter', 'facebook', 'instagram', 'feed', 'follower'],
            'medical': ['medical', 'health', 'patient', 'doctor', 'hospital', 'clinic'],
            'financial': ['financial', 'finance', 'banking', 'transaction', 'account', 'payment'],
            'inventory': ['inventory', 'warehouse', 'stock', 'supplier'],
            'education': ['education', 'school', 'student', 'course', 'grade'],
            'real estate': ['real estate', 'property', 'listing', 'rental']
        }

        for domain, keywords in domain_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                return domain

        return None

    def _handle_test_data_generation(self, query_text: str):
        """Handle test data generation request (T025-T028).

        Args:
            query_text: User's natural language query
        """
        try:
            from .models import TestDataRequest, CancellationToken
            from .schema_design.test_data_generator import TestDataGenerator
            from .schema_design.data_synthesizer import FakerDataSynthesizer
            from .schema_design.insertion_executor import (
                MySQLInsertionExecutor,
                PostgreSQLInsertionExecutor,
                SQLiteInsertionExecutor
            )

            console.print("\n[bold cyan]Test Data Generation[/bold cyan]\n")

            # Get database connection info
            profile = self._get_active_profile()
            password = get_password(self.session.connection_name) if profile.database_type != "sqlite" else None

            # Validate schema exists
            from .schema_introspection import SchemaIntrospector
            introspector = SchemaIntrospector(profile, password)
            schema = introspector.get_schema()

            if not schema.get("tables"):
                console.print("[red]Error:[/red] No tables found in database")
                console.print("[dim]Create a schema first using [cyan]\\schema design[/cyan][/dim]")
                return

            # Parse quantity specifications (T029)
            record_counts = self._parse_record_counts(query_text)

            # Parse domain context (T033)
            domain_context = self._parse_domain_context(query_text)

            # Create request
            request = TestDataRequest(
                user_query=query_text,
                database_type=profile.database_type,
                target_tables=None,  # Generate for all tables
                record_counts=record_counts,
                domain_context=domain_context
            )

            # Initialize components
            data_synthesizer = FakerDataSynthesizer()

            # Select appropriate insertion executor
            if profile.database_type == 'mysql':
                insertion_executor = MySQLInsertionExecutor()
            elif profile.database_type == 'postgresql':
                insertion_executor = PostgreSQLInsertionExecutor()
            elif profile.database_type == 'sqlite':
                insertion_executor = SQLiteInsertionExecutor()
            else:
                raise ValueError(f"Unsupported database type: {profile.database_type}")

            # Initialize generator
            generator = TestDataGenerator(
                llm_service=self.llm,
                data_synthesizer=data_synthesizer,
                insertion_executor=insertion_executor
            )

            # Get database connection - create SQLAlchemy engine
            from sqlalchemy import create_engine

            conn_config = profile.get_connection_config(password)

            # Build SQLAlchemy connection string
            if profile.database_type == "mysql":
                connection_string = f"mysql+pymysql://{conn_config['username']}:{conn_config['password']}@{conn_config['host']}:{conn_config.get('port', 3306)}/{conn_config['database_name']}"
            elif profile.database_type == "postgresql":
                connection_string = f"postgresql+psycopg2://{conn_config['username']}:{conn_config['password']}@{conn_config['host']}:{conn_config.get('port', 5432)}/{conn_config['database_name']}"
            elif profile.database_type == "sqlite":
                connection_string = f"sqlite:///{conn_config['database_name']}"
            else:
                raise ValueError(f"Unsupported database type: {profile.database_type}")

            # Create SQLAlchemy engine
            engine = create_engine(connection_string)
            # Pass the engine - the generator will use it for introspection
            # and get raw connection for insertions
            connection = engine
            db = None

            # Estimate total records and warn for large datasets (T031)
            estimated_total = 0
            if record_counts:
                if '__all__' in record_counts:
                    # All tables get same count
                    num_tables = len(schema.get("tables", []))
                    estimated_total = record_counts['__all__'] * num_tables
                else:
                    estimated_total = sum(record_counts.values())
            else:
                # Default: ~15 records per table
                estimated_total = len(schema.get("tables", [])) * 15

            # Warn for large datasets (> 10,000 records)
            if estimated_total > 10000:
                console.print(f"\n[yellow]⚠ Large Dataset Warning[/yellow]")
                console.print(f"This will generate approximately [bold]{estimated_total:,}[/bold] records")

                # Estimate time based on database type
                speed_estimates = {
                    'mysql': 500,
                    'postgresql': 600,
                    'sqlite': 1000
                }
                speed = speed_estimates.get(profile.database_type, 500)
                estimated_seconds = estimated_total / speed
                estimated_minutes = estimated_seconds / 60

                if estimated_minutes < 1:
                    time_str = f"{estimated_seconds:.0f} seconds"
                else:
                    time_str = f"{estimated_minutes:.1f} minutes"

                console.print(f"Estimated time: [cyan]{time_str}[/cyan]")

                # Prompt for confirmation
                from prompt_toolkit import prompt as pt_prompt
                response = pt_prompt("\nContinue? (y/N): ")
                if response.lower() not in ['y', 'yes']:
                    console.print("[dim]Operation cancelled[/dim]")
                    if connection:
                        connection.dispose()
                    return

            # Progress callback
            from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

            cancellation_token = CancellationToken()

            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                console=console
            ) as progress:
                task = progress.add_task("Generating test data plan...", total=None)

                def progress_callback(update):
                    progress.update(
                        task,
                        description=f"Inserting into {update.current_table} ({update.table_number}/{update.total_tables})",
                        completed=update.records_completed,
                        total=update.records_total
                    )

                # Execute test data generation
                result = generator.generate_test_data(
                    request=request,
                    connection=connection,
                    progress_callback=progress_callback,
                    cancellation_token=cancellation_token
                )

            # Display results (T027)
            console.print("\n[bold green]✓ Test Data Generation Complete[/bold green]\n")

            # Summary table
            summary_table = Table(title="Insertion Summary", show_header=True, header_style="bold cyan")
            summary_table.add_column("Table", style="cyan")
            summary_table.add_column("Inserted", justify="right", style="green")
            summary_table.add_column("Failed", justify="right", style="red")
            summary_table.add_column("Duration", justify="right", style="yellow")

            for table_name, table_result in result.table_results.items():
                summary_table.add_row(
                    table_name,
                    str(table_result.records_inserted),
                    str(table_result.records_failed),
                    f"{table_result.insertion_duration_seconds:.2f}s"
                )

            console.print(summary_table)

            # Overall stats
            console.print(f"\n[bold]Total Records:[/bold] {result.total_records_inserted}/{result.total_records_requested}")
            console.print(f"[bold]Duration:[/bold] {result.duration_seconds:.2f} seconds")

            if result.total_records_failed > 0:
                console.print(f"\n[yellow]⚠ {result.total_records_failed} records failed to insert[/yellow]")
                if result.errors and len(result.errors) <= 10:
                    console.print("\n[bold]Errors:[/bold]")
                    for error in result.errors[:10]:
                        console.print(f"  [red]•[/red] {error.table_name}: {error.error_message}")

            # Clean up SQLAlchemy engine
            if connection:
                connection.dispose()

            # Add to session context
            self.session.add_message("user", query_text)
            self.session.add_message(
                "assistant",
                f"Generated {result.total_records_inserted} test records across {len(result.table_results)} tables"
            )

        except ValueError as e:
            console.print(f"\n[red]Error:[/red] {e}")
            self.session.add_message("assistant", f"Error: {e}")
        except Exception as e:
            console.print(f"\n[red]Unexpected error during test data generation:[/red] {e}")
            import traceback
            console.print(f"[dim]{traceback.format_exc()}[/dim]")
            self.session.add_message("assistant", f"Error: {e}")

    def run(self):
        """Run the REPL loop"""
        self.show_welcome()

        while self.running:
            try:
                # Show prompt
                connection_display = self.session.connection_name or "no-connection"
                user_input = self.prompt_session.prompt(f"querynl ({connection_display})> ")

                # Skip empty input
                if not user_input.strip():
                    continue

                # Handle REPL commands
                if user_input.strip().startswith("\\"):
                    self.handle_command(user_input.strip())
                else:
                    # Execute as natural language query
                    self.execute_query(user_input.strip())

            except KeyboardInterrupt:
                console.print("\n[dim]Use \\exit to quit[/dim]")
                continue
            except EOFError:
                self.running = False
                console.print("\n[dim]Goodbye![/dim]")
                break
            except Exception as e:
                console.print(f"\n[red]Unexpected error:[/red] {e}")
                continue


def start_repl(connection_name: Optional[str] = None):
    """
    Start interactive REPL session.

    Args:
        connection_name: Optional connection to use
    """
    manager = REPLManager(connection_name=connection_name)
    manager.run()
