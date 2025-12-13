"""
Schema design commands for QueryNL CLI

Handles schema generation, visualization, analysis, modification, and application.
"""

import json
import uuid
from datetime import datetime
from typing import Optional, Dict
import click
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from ..models import SchemaDesign, TableDesign, ColumnDefinition, Relationship
from ..config import load_config
from ..credentials import get_password
from ..database import DatabaseConnection
from ..errors import ConfigError

console = Console()


@click.group()
def schema():
    """Schema design and management"""
    pass


@schema.command("design")
@click.argument("description")
@click.option("--output", "-o", type=click.Path(), help="Output file path (default: schema-{timestamp}.json)")
@click.option("--id", "schema_id", help="Schema identifier (default: auto-generated)")
def design_schema(description, output, schema_id):
    """
    Design database schema from natural language description

    Examples:
        querynl schema design "blog with posts and comments"
        querynl schema design "e-commerce with users, products, and orders" --output my-schema.json
    """
    try:
        console.print(f"\n[bold]Designing schema from:[/bold] {description}")

        # Generate schema using pattern matching (MVP - replace with LLM later)
        schema = _generate_schema_from_description(description, schema_id)

        # Display summary
        _display_schema_summary(schema)

        # Save to file
        if not output:
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            output = f"schema-{timestamp}.json"

        with open(output, 'w') as f:
            json.dump(schema.to_dict(), f, indent=2)

        console.print(f"\n[green]✓[/green] Schema saved to: [bold]{output}[/bold]")
        console.print("\n[dim]Next steps:[/dim]")
        console.print(f"  [cyan]querynl schema visualize {output}[/cyan]  - Generate ER diagram")
        console.print(f"  [cyan]querynl schema analyze {output}[/cyan]   - Analyze for issues")
        console.print(f"  [cyan]querynl schema apply {output}[/cyan]     - Generate SQL")

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise click.Abort()


@schema.command("visualize")
@click.argument("schema_file", type=click.Path(exists=True))
@click.option("--output", "-o", type=click.Path(), help="Output markdown file (default: stdout)")
def visualize_schema(schema_file, output):
    """
    Generate Mermaid ER diagram from schema

    Examples:
        querynl schema visualize schema.json
        querynl schema visualize schema.json --output diagram.md
    """
    try:
        # Load schema
        with open(schema_file, 'r') as f:
            schema_data = json.load(f)

        schema = SchemaDesign.from_dict(schema_data)

        # Generate Mermaid diagram
        mermaid = _generate_mermaid_diagram(schema)

        if output:
            with open(output, 'w') as f:
                f.write(f"# {schema.id} - ER Diagram\n\n")
                f.write(f"**Description**: {schema.description}\n\n")
                f.write(f"```mermaid\n{mermaid}\n```\n")
            console.print(f"[green]✓[/green] Diagram saved to: [bold]{output}[/bold]")
        else:
            console.print(f"\n[bold]{schema.id} - ER Diagram[/bold]")
            console.print(f"[dim]{schema.description}[/dim]\n")
            syntax = Syntax(mermaid, "mermaid", theme="monokai")
            console.print(syntax)

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise click.Abort()


@schema.command("analyze")
@click.argument("schema_file", type=click.Path(exists=True))
def analyze_schema(schema_file):
    """
    Analyze schema for design issues

    Examples:
        querynl schema analyze schema.json
    """
    try:
        # Load schema
        with open(schema_file, 'r') as f:
            schema_data = json.load(f)

        schema = SchemaDesign.from_dict(schema_data)

        console.print(f"\n[bold]Analyzing schema:[/bold] {schema.id}")

        # Run analysis checks
        issues = _analyze_schema_design(schema)

        # Display results
        _display_analysis_results(issues)

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise click.Abort()


@schema.command("modify")
@click.argument("schema_file", type=click.Path(exists=True))
@click.argument("modification")
@click.option("--output", "-o", type=click.Path(), help="Output file (default: overwrite existing)")
def modify_schema(schema_file, modification, output):
    """
    Modify existing schema with natural language changes

    Examples:
        querynl schema modify schema.json "add user_email column to users table"
        querynl schema modify schema.json "add categories table" --output updated-schema.json
    """
    try:
        # Load existing schema
        with open(schema_file, 'r') as f:
            schema_data = json.load(f)

        schema = SchemaDesign.from_dict(schema_data)

        console.print(f"\n[bold]Modifying schema:[/bold] {schema.id}")
        console.print(f"[dim]Change:[/dim] {modification}")

        # Apply modification (MVP - pattern matching)
        modified_schema = _apply_schema_modification(schema, modification)

        # Update metadata
        modified_schema.modified_at = datetime.now()
        modified_schema.version += 1

        # Display changes
        console.print(f"\n[yellow]Version:[/yellow] {schema.version} → {modified_schema.version}")

        # Save
        output_path = output or schema_file
        with open(output_path, 'w') as f:
            json.dump(modified_schema.to_dict(), f, indent=2)

        console.print(f"[green]✓[/green] Schema updated: [bold]{output_path}[/bold]")

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise click.Abort()


@schema.command("apply")
@click.argument("schema_file", type=click.Path(exists=True))
@click.option("--connection", "-c", help="Connection to apply schema to")
@click.option("--execute", is_flag=True, help="Execute SQL on connection")
@click.option("--output", "-o", type=click.Path(), help="Save SQL to file")
def apply_schema(schema_file, connection, execute, output):
    """
    Generate CREATE TABLE SQL from schema

    Examples:
        querynl schema apply schema.json
        querynl schema apply schema.json --execute --connection my-db
        querynl schema apply schema.json --output schema.sql
    """
    try:
        # Load schema
        with open(schema_file, 'r') as f:
            schema_data = json.load(f)

        schema = SchemaDesign.from_dict(schema_data)

        # Determine database type
        db_type = "postgresql"  # Default
        if connection:
            config = load_config()
            if connection not in config.connections:
                raise ConfigError(f"Connection '{connection}' not found")

            from ..models import ConnectionProfile
            profile = ConnectionProfile.from_dict(config.connections[connection])
            db_type = profile.database_type

        # Generate SQL
        sql = _generate_create_table_sql(schema, db_type)

        # Display SQL
        console.print(f"\n[bold]Generated SQL for {db_type}:[/bold]")
        syntax = Syntax(sql, "sql", theme="monokai", line_numbers=True)
        console.print(syntax)

        # Save to file
        if output:
            with open(output, 'w') as f:
                f.write(sql)
            console.print(f"\n[green]✓[/green] SQL saved to: [bold]{output}[/bold]")

        # Execute if requested
        if execute:
            if not connection:
                console.print("[yellow]--execute requires --connection[/yellow]")
                return

            from rich.prompt import Confirm
            if not Confirm.ask("\n[yellow]⚠️  Execute this SQL on the database?[/yellow]"):
                console.print("[dim]Cancelled[/dim]")
                return

            # Execute SQL
            config = load_config()
            profile = ConnectionProfile.from_dict(config.connections[connection])
            password = get_password(connection) if profile.database_type != "sqlite" else None
            conn_config = profile.get_connection_config(password)

            db = DatabaseConnection(conn_config)
            console.print(f"\n[dim]Executing on {connection}...[/dim]")

            # Execute each statement
            statements = [s.strip() for s in sql.split(';') if s.strip()]
            for stmt in statements:
                try:
                    db.execute_query(stmt + ';')
                except Exception as e:
                    console.print(f"[red]Error executing statement:[/red] {e}")
                    db.close()
                    raise

            db.close()
            console.print("[green]✓[/green] Schema applied successfully")

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise click.Abort()


# Helper functions

def _generate_schema_from_description(description: str, schema_id: Optional[str] = None) -> SchemaDesign:
    """Generate schema from natural language (MVP pattern matching)"""

    # Simple pattern matching for MVP
    desc_lower = description.lower()

    tables = []
    relationships = []

    # Blog pattern
    if "blog" in desc_lower:
        tables.append(TableDesign(
            name="posts",
            columns=[
                ColumnDefinition(name="id", type="SERIAL", primary_key=True, nullable=False),
                ColumnDefinition(name="title", type="VARCHAR(200)", nullable=False),
                ColumnDefinition(name="content", type="TEXT", nullable=False),
                ColumnDefinition(name="created_at", type="TIMESTAMP", nullable=False, default_value="CURRENT_TIMESTAMP"),
            ]
        ))
        tables.append(TableDesign(
            name="comments",
            columns=[
                ColumnDefinition(name="id", type="SERIAL", primary_key=True, nullable=False),
                ColumnDefinition(name="post_id", type="INTEGER", nullable=False),
                ColumnDefinition(name="content", type="TEXT", nullable=False),
                ColumnDefinition(name="created_at", type="TIMESTAMP", nullable=False, default_value="CURRENT_TIMESTAMP"),
            ]
        ))
        relationships.append(Relationship(
            from_table="comments",
            from_column="post_id",
            to_table="posts",
            to_column="id",
            on_delete="CASCADE"
        ))

    # E-commerce pattern
    elif "e-commerce" in desc_lower or "ecommerce" in desc_lower or "shop" in desc_lower:
        tables.append(TableDesign(
            name="users",
            columns=[
                ColumnDefinition(name="id", type="SERIAL", primary_key=True, nullable=False),
                ColumnDefinition(name="email", type="VARCHAR(255)", nullable=False, unique=True),
                ColumnDefinition(name="name", type="VARCHAR(100)", nullable=False),
                ColumnDefinition(name="created_at", type="TIMESTAMP", nullable=False, default_value="CURRENT_TIMESTAMP"),
            ]
        ))
        tables.append(TableDesign(
            name="products",
            columns=[
                ColumnDefinition(name="id", type="SERIAL", primary_key=True, nullable=False),
                ColumnDefinition(name="name", type="VARCHAR(200)", nullable=False),
                ColumnDefinition(name="price", type="DECIMAL(10,2)", nullable=False),
                ColumnDefinition(name="stock", type="INTEGER", nullable=False, default_value="0"),
            ]
        ))
        tables.append(TableDesign(
            name="orders",
            columns=[
                ColumnDefinition(name="id", type="SERIAL", primary_key=True, nullable=False),
                ColumnDefinition(name="user_id", type="INTEGER", nullable=False),
                ColumnDefinition(name="total", type="DECIMAL(10,2)", nullable=False),
                ColumnDefinition(name="created_at", type="TIMESTAMP", nullable=False, default_value="CURRENT_TIMESTAMP"),
            ]
        ))
        relationships.extend([
            Relationship(from_table="orders", from_column="user_id", to_table="users", to_column="id", on_delete="CASCADE")
        ])

    # Generic fallback
    else:
        # Extract potential table names from description
        words = desc_lower.replace(",", " ").split()
        table_names = [w for w in words if len(w) > 3 and w not in ["with", "and", "the", "for"]]

        for table_name in table_names[:3]:  # Limit to 3 tables
            tables.append(TableDesign(
                name=table_name,
                columns=[
                    ColumnDefinition(name="id", type="SERIAL", primary_key=True, nullable=False),
                    ColumnDefinition(name="name", type="VARCHAR(100)", nullable=False),
                    ColumnDefinition(name="created_at", type="TIMESTAMP", nullable=False, default_value="CURRENT_TIMESTAMP"),
                ]
            ))

    return SchemaDesign(
        id=schema_id or f"schema-{uuid.uuid4().hex[:8]}",
        description=description,
        tables=tables,
        relationships=relationships
    )


def _display_schema_summary(schema: SchemaDesign):
    """Display schema summary"""
    console.print("\n[bold cyan]Schema Summary[/bold cyan]")
    console.print(f"[dim]ID:[/dim] {schema.id}")
    console.print(f"[dim]Version:[/dim] {schema.version}")
    console.print(f"\n[bold]Tables:[/bold] {len(schema.tables)}")

    for table in schema.tables:
        console.print(f"  • [cyan]{table.name}[/cyan] ({len(table.columns)} columns)")

    if schema.relationships:
        console.print(f"\n[bold]Relationships:[/bold] {len(schema.relationships)}")
        for rel in schema.relationships:
            console.print(f"  • [yellow]{rel.from_table}.{rel.from_column}[/yellow] → [green]{rel.to_table}.{rel.to_column}[/green]")


def _generate_mermaid_diagram(schema: SchemaDesign) -> str:
    """Generate Mermaid ER diagram"""
    lines = ["erDiagram"]

    # Add tables
    for table in schema.tables:
        lines.append(f"    {table.name} {{")
        for col in table.columns:
            col_type = col.type
            constraints = []
            if col.primary_key:
                constraints.append("PK")
            if col.unique:
                constraints.append("UK")
            if not col.nullable:
                constraints.append("NOT NULL")

            constraint_str = f" {','.join(constraints)}" if constraints else ""
            lines.append(f"        {col_type} {col.name}{constraint_str}")
        lines.append("    }")

    # Add relationships
    for rel in schema.relationships:
        # Determine relationship cardinality (simplified)
        lines.append(f"    {rel.to_table} ||--o{{ {rel.from_table} : \"{rel.on_delete}\"")

    return "\n".join(lines)


def _analyze_schema_design(schema: SchemaDesign) -> Dict[str, list]:
    """Analyze schema for issues"""
    issues = {
        "errors": [],
        "warnings": [],
        "suggestions": []
    }

    # Check for tables without primary keys
    for table in schema.tables:
        has_pk = any(col.primary_key for col in table.columns)
        if not has_pk:
            issues["errors"].append(f"Table '{table.name}' has no primary key")

    # Check for foreign keys without indexes
    for rel in schema.relationships:
        from_table = next((t for t in schema.tables if t.name == rel.from_table), None)
        if from_table:
            # Check if from_column has an index
            has_index = any(rel.from_column in idx.get("columns", []) for idx in from_table.indexes)
            if not has_index:
                issues["warnings"].append(f"Foreign key {rel.from_table}.{rel.from_column} should have an index")

    # Check naming conventions
    for table in schema.tables:
        if not table.name.islower():
            issues["suggestions"].append(f"Table '{table.name}' should use lowercase naming")

        for col in table.columns:
            if not col.name.islower():
                issues["suggestions"].append(f"Column '{table.name}.{col.name}' should use lowercase naming")

    # Check for timestamps
    for table in schema.tables:
        has_created_at = any(col.name == "created_at" for col in table.columns)
        if not has_created_at:
            issues["suggestions"].append(f"Table '{table.name}' should have a 'created_at' timestamp column")

    return issues


def _display_analysis_results(issues: Dict[str, list]):
    """Display analysis results"""
    total_issues = sum(len(v) for v in issues.values())

    if total_issues == 0:
        panel = Panel(
            "[green]✓[/green] No issues found!\nSchema follows best practices.",
            title="[bold green]Analysis Complete[/bold green]",
            border_style="green"
        )
        console.print(panel)
        return

    # Display issues by severity
    if issues["errors"]:
        console.print("\n[bold red]Errors:[/bold red]")
        for error in issues["errors"]:
            console.print(f"  [red]✗[/red] {error}")

    if issues["warnings"]:
        console.print("\n[bold yellow]Warnings:[/bold yellow]")
        for warning in issues["warnings"]:
            console.print(f"  [yellow]⚠[/yellow] {warning}")

    if issues["suggestions"]:
        console.print("\n[bold cyan]Suggestions:[/bold cyan]")
        for suggestion in issues["suggestions"]:
            console.print(f"  [cyan]ℹ[/cyan] {suggestion}")

    console.print(f"\n[dim]Total issues: {total_issues}[/dim]")


def _apply_schema_modification(schema: SchemaDesign, modification: str) -> SchemaDesign:
    """Apply modification to schema (MVP - simple pattern matching)"""
    # This is a simplified implementation
    # In production, this would use LLM to understand and apply changes

    console.print("[yellow]Note:[/yellow] Schema modification is simplified in MVP")

    # For now, just return the schema unchanged
    # TODO: Implement actual modification logic
    return schema


def _generate_create_table_sql(schema: SchemaDesign, db_type: str = "postgresql") -> str:
    """Generate CREATE TABLE SQL for schema"""
    statements = []

    # Generate table statements
    for table in schema.tables:
        cols = []
        for col in table.columns:
            col_def = f"{col.name} {col.type}"

            if col.primary_key:
                col_def += " PRIMARY KEY"
            if not col.nullable:
                col_def += " NOT NULL"
            if col.unique and not col.primary_key:
                col_def += " UNIQUE"
            if col.default_value:
                col_def += f" DEFAULT {col.default_value}"

            cols.append(col_def)

        table_sql = f"CREATE TABLE {table.name} (\n    " + ",\n    ".join(cols) + "\n);"
        statements.append(table_sql)

    # Generate foreign key constraints
    for rel in schema.relationships:
        fk_sql = (
            f"ALTER TABLE {rel.from_table} "
            f"ADD CONSTRAINT fk_{rel.from_table}_{rel.from_column} "
            f"FOREIGN KEY ({rel.from_column}) "
            f"REFERENCES {rel.to_table}({rel.to_column}) "
            f"ON DELETE {rel.on_delete} "
            f"ON UPDATE {rel.on_update};"
        )
        statements.append(fk_sql)

    return "\n\n".join(statements)


# ============================================================================
# Schema Introspection Commands (View actual database schema)
# ============================================================================

@schema.command("show")
@click.option("--connection", "-c", help="Connection name to use")
@click.option("--table", "-t", help="Show schema for specific table only")
@click.option("--format", "-f", type=click.Choice(["tree", "table", "detailed", "graph"]), default="tree", help="Output format")
def schema_show(connection, table, format):
    """
    Display database schema information.

    Shows all tables and their columns with data types from your connected database.

    Examples:
        querynl schema show
        querynl schema show --connection my-db
        querynl schema show --table users
        querynl schema show --format table
    """
    from ..schema_introspection import SchemaIntrospector
    from ..models import ConnectionProfile
    from rich.tree import Tree
    from rich.table import Table

    try:
        config = load_config()

        # Determine which connection to use
        connection_name = connection or config.default_connection

        if not connection_name:
            raise ConfigError(
                "No connection specified",
                suggestion="Use --connection or set a default connection with 'querynl connect use'"
            )

        if connection_name not in config.connections:
            raise ConfigError(
                f"Connection '{connection_name}' not found",
                suggestion="Run 'querynl connect list' to see available connections"
            )

        profile = ConnectionProfile.from_dict(config.connections[connection_name])
        password = get_password(connection_name) if profile.database_type != "sqlite" else None

        # Introspect schema
        console.print(f"[dim]Fetching schema from {connection_name}...[/dim]")
        introspector = SchemaIntrospector(profile, password)
        schema_data = introspector.get_schema()

        tables = schema_data.get("tables", {})

        if not tables:
            console.print("[yellow]No tables found in database[/yellow]")
            return

        # Filter to specific table if requested
        if table:
            if table not in tables:
                console.print(f"[red]Table '{table}' not found[/red]")
                console.print(f"\nAvailable tables: {', '.join(sorted(tables.keys()))}")
                return
            tables = {table: tables[table]}

        # Display based on format
        if format == "tree":
            _display_tree_format(tables, connection_name, profile.database_type)
        elif format == "table":
            _display_table_format(tables, connection_name, profile.database_type)
        elif format == "detailed":
            _display_detailed_format(tables, connection_name, profile.database_type)
        elif format == "graph":
            _display_graph_format(schema_data, connection_name, profile.database_type, introspector)

    except ConfigError:
        raise
    except Exception as e:
        raise ConfigError(f"Failed to fetch schema: {e}")


def _display_tree_format(tables, connection_name, db_type):
    """Display schema in tree format."""
    from rich.tree import Tree

    tree = Tree(f"[bold cyan]📊 Database: {connection_name}[/bold cyan] ({db_type})")

    for table_name in sorted(tables.keys()):
        table_info = tables[table_name]
        column_details = table_info.get("column_details", [])

        if column_details:
            table_branch = tree.add(f"[bold yellow]📋 {table_name}[/bold yellow] ({len(column_details)} columns)")

            for col in column_details:
                col_name = col["name"]
                col_type = col["type"]
                nullable = "NULL" if col.get("nullable", True) else "NOT NULL"
                default = col.get("default")

                col_display = f"[green]{col_name}[/green] [dim]({col_type})[/dim] [cyan]{nullable}[/cyan]"
                if default:
                    col_display += f" [dim]default: {default}[/dim]"

                table_branch.add(col_display)
        else:
            tree.add(f"[bold yellow]📋 {table_name}[/bold yellow] (no columns)")

    console.print(tree)
    console.print(f"\n[dim]Total tables: {len(tables)}[/dim]")


def _display_table_format(tables, connection_name, db_type):
    """Display schema in table format."""
    from rich.table import Table as RichTable

    console.print(f"[bold cyan]Database: {connection_name}[/bold cyan] ({db_type})\n")

    for table_name in sorted(tables.keys()):
        table_info = tables[table_name]
        column_details = table_info.get("column_details", [])

        if not column_details:
            console.print(f"[yellow]{table_name}[/yellow]: No columns")
            continue

        table = RichTable(title=f"Table: {table_name}", show_header=True, header_style="bold cyan")
        table.add_column("Column", style="green")
        table.add_column("Type", style="white")
        table.add_column("Nullable", style="cyan")
        table.add_column("Default", style="dim")

        for col in column_details:
            table.add_row(
                col["name"],
                col["type"],
                "YES" if col.get("nullable", True) else "NO",
                str(col.get("default", "")) if col.get("default") is not None else ""
            )

        console.print(table)
        console.print()

    console.print(f"[dim]Total tables: {len(tables)}[/dim]")


def _display_detailed_format(tables, connection_name, db_type):
    """Display schema in detailed format with panels."""
    console.print(f"[bold cyan]Database: {connection_name}[/bold cyan] ({db_type})")
    console.print(f"[dim]Total tables: {len(tables)}[/dim]\n")

    for table_name in sorted(tables.keys()):
        table_info = tables[table_name]
        column_details = table_info.get("column_details", [])

        if not column_details:
            console.print(Panel(f"[yellow]No columns[/yellow]", title=table_name, border_style="yellow"))
            continue

        # Build detailed information
        lines = []
        for i, col in enumerate(column_details, 1):
            col_name = col["name"]
            col_type = col["type"]
            nullable = "NULL" if col.get("nullable", True) else "NOT NULL"
            default = col.get("default")

            line = f"{i}. [green]{col_name}[/green]"
            line += f"\n   Type: [white]{col_type}[/white]"
            line += f"\n   Nullable: [cyan]{nullable}[/cyan]"
            if default:
                line += f"\n   Default: [dim]{default}[/dim]"

            lines.append(line)

        content = "\n\n".join(lines)
        panel = Panel(
            content,
            title=f"[bold yellow]📋 {table_name}[/bold yellow] ({len(column_details)} columns)",
            border_style="cyan",
            expand=False
        )
        console.print(panel)
        console.print()


@schema.command("stats")
@click.option("--connection", "-c", help="Connection name to use")
def schema_stats(connection):
    """
    Display database schema statistics.

    Shows summary statistics about tables and columns.

    Examples:
        querynl schema stats
        querynl schema stats --connection my-db
    """
    from ..schema_introspection import SchemaIntrospector
    from ..models import ConnectionProfile
    from rich.table import Table as RichTable

    try:
        config = load_config()

        # Determine which connection to use
        connection_name = connection or config.default_connection

        if not connection_name:
            raise ConfigError(
                "No connection specified",
                suggestion="Use --connection or set a default connection"
            )

        if connection_name not in config.connections:
            raise ConfigError(
                f"Connection '{connection_name}' not found",
                suggestion="Run 'querynl connect list' to see available connections"
            )

        profile = ConnectionProfile.from_dict(config.connections[connection_name])
        password = get_password(connection_name) if profile.database_type != "sqlite" else None

        # Introspect schema
        console.print(f"[dim]Analyzing schema from {connection_name}...[/dim]")
        introspector = SchemaIntrospector(profile, password)
        schema_data = introspector.get_schema()

        tables = schema_data.get("tables", {})

        if not tables:
            console.print("[yellow]No tables found in database[/yellow]")
            return

        # Calculate statistics
        total_tables = len(tables)
        total_columns = sum(len(t.get("columns", [])) for t in tables.values())
        avg_columns = total_columns / total_tables if total_tables > 0 else 0

        # Find largest table
        largest_table = max(tables.items(), key=lambda x: len(x[1].get("columns", [])))
        largest_table_name = largest_table[0]
        largest_table_cols = len(largest_table[1].get("columns", []))

        # Count data types
        type_counts = {}
        for table_info in tables.values():
            for col in table_info.get("column_details", []):
                col_type = col.get("type", "unknown")
                # Normalize type (e.g., "varchar(255)" -> "varchar")
                base_type = col_type.split("(")[0].lower()
                type_counts[base_type] = type_counts.get(base_type, 0) + 1

        # Display statistics
        stats_table = RichTable(title=f"Schema Statistics: {connection_name}", show_header=True, header_style="bold cyan")
        stats_table.add_column("Metric", style="yellow")
        stats_table.add_column("Value", style="green", justify="right")

        stats_table.add_row("Database Type", profile.database_type)
        stats_table.add_row("Total Tables", str(total_tables))
        stats_table.add_row("Total Columns", str(total_columns))
        stats_table.add_row("Average Columns per Table", f"{avg_columns:.1f}")
        stats_table.add_row("Largest Table", f"{largest_table_name} ({largest_table_cols} columns)")

        console.print(stats_table)
        console.print()

        # Display type distribution
        if type_counts:
            type_table = RichTable(title="Column Type Distribution", show_header=True, header_style="bold cyan")
            type_table.add_column("Data Type", style="yellow")
            type_table.add_column("Count", style="green", justify="right")
            type_table.add_column("Percentage", style="cyan", justify="right")

            for col_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / total_columns * 100) if total_columns > 0 else 0
                type_table.add_row(col_type, str(count), f"{percentage:.1f}%")

            console.print(type_table)

    except ConfigError:
        raise
    except Exception as e:
        raise ConfigError(f"Failed to fetch schema statistics: {e}")


def _display_graph_format(schema_data, connection_name, db_type, introspector):
    """Display schema in graphical ER diagram format with foreign key relationships."""
    from rich.console import Group
    from rich.panel import Panel
    from rich.table import Table as RichTable

    tables = schema_data.get("tables", {})
    sorted_table_names = sorted(tables.keys())

    # Detect foreign key relationships by column naming conventions
    relationships = _detect_relationships(tables)

    console.print(f"\n[bold cyan]📊 Database ER Diagram: {connection_name}[/bold cyan] ({db_type})\n")

    # Create a mapping of table names to their positions in the grid
    table_positions = {table_name: idx for idx, table_name in enumerate(sorted_table_names)}

    # Build table boxes with relationship indicators
    table_boxes = []
    table_names_list = []

    for table_name in sorted_table_names:
        table_info = tables[table_name]
        column_details = table_info.get("column_details", [])

        if not column_details:
            continue

        table_names_list.append(table_name)

        # Build table box content
        lines = []
        lines.append(f"[bold yellow]{table_name.upper()}[/bold yellow]")
        lines.append("─" * (len(table_name) + 2))

        # Find outgoing relationships from this table
        outgoing_rels = [r for r in relationships if r["from_table"] == table_name]
        incoming_rels = [r for r in relationships if r["to_table"] == table_name]

        for col in column_details:
            col_name = col["name"]
            col_type = col["type"]

            # Check if this column is involved in a relationship
            is_fk = any(r["from_column"] == col_name for r in outgoing_rels)
            is_pk_referenced = col_name.lower() == "id" and any(r["to_column"] == col_name for r in incoming_rels)

            # Mark primary keys and foreign keys
            if col_name.lower() == "id":
                prefix = "🔑 "
            elif is_fk:
                prefix = "🔗 "
            else:
                prefix = "   "

            # Truncate long type names
            if len(col_type) > 15:
                col_type = col_type[:12] + "..."

            lines.append(f"{prefix}[green]{col_name}[/green] [dim]{col_type}[/dim]")

        box_content = "\n".join(lines)
        table_boxes.append(Panel(box_content, border_style="cyan", expand=False))

    # Display tables in a grid-like layout (3 per row)
    rows_count = (len(table_boxes) + 2) // 3  # Calculate number of rows

    for i in range(0, len(table_boxes), 3):
        row_tables = table_boxes[i:i+3]
        row_table_names = table_names_list[i:i+3]

        # Create columns side by side
        from rich.columns import Columns
        console.print(Columns(row_tables, equal=True, expand=False))

        # Draw connection lines between tables in this row and previous rows
        if relationships and i > 0:
            # Draw lines for relationships
            connection_lines = []
            for rel in relationships:
                from_table = rel["from_table"]
                to_table = rel["to_table"]

                # Check if we should draw a line
                from_idx = table_names_list.index(from_table) if from_table in table_names_list else -1
                to_idx = table_names_list.index(to_table) if to_table in table_names_list else -1

                # Only draw if from_table is in current or previous rows and to_table is above it
                if from_idx >= 0 and to_idx >= 0 and from_idx > to_idx and from_idx <= i + 2 and from_idx >= i:
                    from_col_in_row = from_idx % 3
                    to_col_in_row = to_idx % 3

                    # Simple visual indicator
                    spaces_before = "    " * from_col_in_row
                    connection_lines.append(f"{spaces_before}[dim cyan]│[/dim cyan]")
                    connection_lines.append(f"{spaces_before}[dim cyan]└──→ {to_table}[/dim cyan]")

            if connection_lines:
                for line in connection_lines[:2]:  # Limit to avoid clutter
                    console.print(line)

        console.print()

    # Display relationships with visual ASCII art connections
    if relationships:
        console.print("\n[bold cyan]🔗 Relationships (Foreign Keys)[/bold cyan]\n")

        for rel in relationships:
            from_table = rel["from_table"]
            from_col = rel["from_column"]
            to_table = rel["to_table"]
            to_col = rel["to_column"]

            # Draw a visual connection line
            console.print(
                f"  [yellow]{from_table}[/yellow].[green]{from_col}[/green] "
                f"[dim cyan]──────→[/dim cyan] "
                f"[yellow]{to_table}[/yellow].[green]{to_col}[/green]"
            )
    else:
        console.print("\n[dim]No foreign key relationships detected[/dim]")

    console.print(f"\n[dim]Total tables: {len(tables)}[/dim]")
    console.print("[dim]Legend: 🔑 Primary Key | 🔗 Foreign Key | [cyan]───→[/cyan] Relationship[/dim]")


def _detect_relationships(tables):
    """
    Detect foreign key relationships by naming conventions.

    Looks for columns ending in _id that match other table names.
    """
    relationships = []

    for table_name, table_info in tables.items():
        column_details = table_info.get("column_details", [])

        for col in column_details:
            col_name = col["name"]

            # Check if column name ends with _id (foreign key convention)
            if col_name.lower().endswith("_id") and col_name.lower() != "id":
                # Extract potential table name
                potential_table = col_name[:-3]  # Remove "_id"

                # Check if it matches any table (singular or plural)
                for other_table in tables.keys():
                    if (other_table.lower() == potential_table.lower() or
                        other_table.lower() == potential_table.lower() + "s" or
                        other_table.lower() + "s" == potential_table.lower()):

                        relationships.append({
                            "from_table": table_name,
                            "from_column": col_name,
                            "to_table": other_table,
                            "to_column": "id"  # Assume primary key is "id"
                        })
                        break

    return relationships
