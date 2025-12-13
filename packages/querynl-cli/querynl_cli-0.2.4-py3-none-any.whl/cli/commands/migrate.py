"""
Migration commands for QueryNL CLI

Handles database migration generation, preview, apply, status, and rollback.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import click
from rich.console import Console
from rich.table import Table
from rich.syntax import Syntax
from rich.prompt import Confirm

from ..models import SchemaDesign, MigrationRecord
from ..migrations import (
    save_migration_record,
    get_migrations,
    update_migration_status
)
from ..config import load_config
from ..credentials import get_password
from ..database import DatabaseConnection
from ..errors import ConfigError

console = Console()


@click.group()
def migrate():
    """Database migration management"""
    pass


@migrate.command("generate")
@click.option("--from", "from_schema", type=click.Path(exists=True), help="Source schema file")
@click.option("--to", "to_schema", type=click.Path(exists=True), help="Target schema file")
@click.option("--framework", type=click.Choice(["alembic", "flyway", "raw"]), default="raw", help="Migration framework")
@click.option("--message", "-m", help="Migration description")
@click.option("--output", "-o", type=click.Path(), help="Output directory (default: ./migrations)")
@click.option("--connection", "-c", help="Target connection (for database-specific SQL)")
def generate_migration(from_schema, to_schema, framework, message, output, connection):
    """
    Generate migration files from schema changes

    Examples:
        querynl migrate generate --from old.json --to new.json --message "add users table"
        querynl migrate generate --from old.json --to new.json --framework alembic
    """
    try:
        if not from_schema or not to_schema:
            raise click.UsageError("Both --from and --to schema files are required")

        # Load schemas
        with open(from_schema, 'r') as f:
            old_schema = SchemaDesign.from_dict(json.load(f))

        with open(to_schema, 'r') as f:
            new_schema = SchemaDesign.from_dict(json.load(f))

        console.print("\n[bold]Generating migration:[/bold]")
        console.print(f"[dim]From:[/dim] {old_schema.id} (v{old_schema.version})")
        console.print(f"[dim]To:[/dim] {new_schema.id} (v{new_schema.version})")

        # Determine database type
        db_type = "postgresql"
        if connection:
            config = load_config()
            if connection in config.connections:
                from ..models import ConnectionProfile
                profile = ConnectionProfile.from_dict(config.connections[connection])
                db_type = profile.database_type

        # Generate migration SQL
        changes = _diff_schemas(old_schema, new_schema)
        up_sql = _generate_up_migration(changes, db_type)
        down_sql = _generate_down_migration(changes, db_type)

        # Generate migration ID
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        migration_id = f"{timestamp}_{message.replace(' ', '_')}" if message else timestamp

        # Display changes
        _display_migration_changes(changes)

        # Set output directory
        output_dir = Path(output) if output else Path("./migrations")
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save migration files based on framework
        if framework == "alembic":
            _save_alembic_migration(output_dir, migration_id, message or "migration", up_sql, down_sql)
        elif framework == "flyway":
            _save_flyway_migration(output_dir, migration_id, message or "migration", up_sql, down_sql)
        else:  # raw
            _save_raw_migration(output_dir, migration_id, up_sql, down_sql)

        # Save migration record
        if connection:
            migration_record = MigrationRecord(
                migration_id=migration_id,
                connection_name=connection,
                framework=framework,
                direction="up",
                sql_content=up_sql,
                rollback_sql=down_sql,
                description=message or "Generated migration",
                status="pending"
            )
            save_migration_record(migration_record)

        console.print(f"\n[green]✓[/green] Migration generated: [bold]{migration_id}[/bold]")
        console.print(f"[dim]Output:[/dim] {output_dir}")

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise click.Abort()


@migrate.command("preview")
@click.argument("migration_file", type=click.Path(exists=True))
def preview_migration(migration_file):
    """
    Preview migration SQL with explanation

    Examples:
        querynl migrate preview migrations/20251015_add_users.sql
    """
    try:
        # Read migration file
        with open(migration_file, 'r') as f:
            sql = f.read()

        console.print(f"\n[bold]Migration Preview:[/bold] {Path(migration_file).name}\n")

        # Display SQL with syntax highlighting
        syntax = Syntax(sql, "sql", theme="monokai", line_numbers=True)
        console.print(syntax)

        # Explain changes (simple parsing for MVP)
        explanation = _explain_migration_sql(sql)
        if explanation:
            console.print("\n[bold cyan]Changes:[/bold cyan]")
            for change in explanation:
                console.print(f"  • {change}")

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise click.Abort()


@migrate.command("apply")
@click.option("--connection", "-c", help="Connection to apply migrations to")
@click.option("--dry-run", is_flag=True, help="Show SQL without executing")
@click.option("--confirm", is_flag=True, help="Skip confirmation prompt")
def apply_migrations(connection, dry_run, confirm):
    """
    Apply pending migrations to database

    Examples:
        querynl migrate apply --connection my-db
        querynl migrate apply --connection my-db --dry-run
    """
    try:
        if not connection:
            config = load_config()
            connection = config.default_connection
            if not connection:
                raise ConfigError("No connection specified and no default connection set")

        # Get pending migrations
        migrations = get_migrations(connection_name=connection, status="pending")

        if not migrations:
            console.print("[yellow]No pending migrations[/yellow]")
            return

        console.print(f"\n[bold]Pending migrations for '{connection}':[/bold]")
        for mig in migrations:
            console.print(f"  • {mig.migration_id} - {mig.description}")

        if dry_run:
            console.print("\n[yellow]Dry run - showing SQL without executing:[/yellow]")
            for mig in migrations:
                console.print(f"\n[bold]{mig.migration_id}:[/bold]")
                syntax = Syntax(mig.sql_content, "sql", theme="monokai")
                console.print(syntax)
            return

        # Confirmation
        if not confirm:
            if not Confirm.ask(f"\n[yellow]Apply {len(migrations)} migration(s)?[/yellow]"):
                console.print("[dim]Cancelled[/dim]")
                return

        # Apply migrations
        config = load_config()
        from ..models import ConnectionProfile
        profile = ConnectionProfile.from_dict(config.connections[connection])
        password = get_password(connection) if profile.database_type != "sqlite" else None
        conn_config = profile.get_connection_config(password)

        db = DatabaseConnection(conn_config)

        for mig in migrations:
            console.print(f"\n[dim]Applying {mig.migration_id}...[/dim]")

            try:
                # Execute in transaction
                db.connect()
                statements = [s.strip() for s in mig.sql_content.split(';') if s.strip()]

                for stmt in statements:
                    db.execute_query(stmt + ';')

                # Mark as applied
                update_migration_status(
                    mig.migration_id,
                    status="applied",
                    applied_at=datetime.now()
                )

                console.print(f"[green]✓[/green] Applied {mig.migration_id}")

            except Exception as e:
                # Mark as failed
                update_migration_status(
                    mig.migration_id,
                    status="failed",
                    error_message=str(e)
                )

                console.print(f"[red]✗[/red] Failed {mig.migration_id}: {e}")
                break

            finally:
                db.close()

        console.print("\n[green]✓[/green] Migration apply complete")

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise click.Abort()


@migrate.command("status")
@click.option("--connection", "-c", help="Filter by connection")
def migration_status(connection):
    """
    Show migration status

    Examples:
        querynl migrate status
        querynl migrate status --connection my-db
    """
    try:
        migrations = get_migrations(connection_name=connection)

        if not migrations:
            console.print("[yellow]No migrations found[/yellow]")
            return

        # Display as table
        table = Table(title="Migration Status")
        table.add_column("Migration ID", style="cyan")
        table.add_column("Connection", style="magenta")
        table.add_column("Description", style="white", max_width=40)
        table.add_column("Status", style="yellow")
        table.add_column("Applied", style="dim")

        for mig in migrations:
            status_color = {
                "pending": "[yellow]PENDING[/yellow]",
                "applied": "[green]APPLIED[/green]",
                "failed": "[red]FAILED[/red]"
            }.get(mig.status, mig.status)

            applied_str = ""
            if mig.applied_at:
                applied_str = mig.applied_at.strftime("%Y-%m-%d %H:%M")

            table.add_row(
                mig.migration_id,
                mig.connection_name,
                mig.description[:37] + "..." if len(mig.description) > 40 else mig.description,
                status_color,
                applied_str
            )

        console.print(table)

        # Summary
        pending = sum(1 for m in migrations if m.status == "pending")
        applied = sum(1 for m in migrations if m.status == "applied")
        failed = sum(1 for m in migrations if m.status == "failed")

        console.print(f"\n[dim]Total: {len(migrations)} | " +
                     f"Applied: {applied} | Pending: {pending} | Failed: {failed}[/dim]")

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise click.Abort()


@migrate.command("rollback")
@click.option("--connection", "-c", help="Connection to rollback")
@click.option("--steps", type=int, default=1, help="Number of migrations to rollback")
@click.option("--confirm", is_flag=True, help="Skip confirmation prompt")
def rollback_migrations(connection, steps, confirm):
    """
    Rollback applied migrations

    Examples:
        querynl migrate rollback --connection my-db
        querynl migrate rollback --connection my-db --steps 2
    """
    try:
        if not connection:
            config = load_config()
            connection = config.default_connection
            if not connection:
                raise ConfigError("No connection specified and no default connection set")

        # Get applied migrations (most recent first)
        migrations = get_migrations(connection_name=connection, status="applied", limit=steps)

        if not migrations:
            console.print("[yellow]No applied migrations to rollback[/yellow]")
            return

        console.print("\n[bold]Migrations to rollback:[/bold]")
        for mig in migrations:
            console.print(f"  • {mig.migration_id} - {mig.description}")

        # Confirmation
        if not confirm:
            if not Confirm.ask(f"\n[yellow]⚠️  Rollback {len(migrations)} migration(s)?[/yellow]"):
                console.print("[dim]Cancelled[/dim]")
                return

        # Rollback migrations
        config = load_config()
        from ..models import ConnectionProfile
        profile = ConnectionProfile.from_dict(config.connections[connection])
        password = get_password(connection) if profile.database_type != "sqlite" else None
        conn_config = profile.get_connection_config(password)

        db = DatabaseConnection(conn_config)

        for mig in migrations:
            if not mig.rollback_sql:
                console.print(f"[yellow]⚠[/yellow] No rollback SQL for {mig.migration_id}, skipping")
                continue

            console.print(f"\n[dim]Rolling back {mig.migration_id}...[/dim]")

            try:
                db.connect()
                statements = [s.strip() for s in mig.rollback_sql.split(';') if s.strip()]

                for stmt in statements:
                    db.execute_query(stmt + ';')

                # Mark as pending (rolled back)
                update_migration_status(
                    mig.migration_id,
                    status="pending",
                    applied_at=None
                )

                console.print(f"[green]✓[/green] Rolled back {mig.migration_id}")

            except Exception as e:
                console.print(f"[red]✗[/red] Failed to rollback {mig.migration_id}: {e}")
                break

            finally:
                db.close()

        console.print("\n[green]✓[/green] Rollback complete")

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise click.Abort()


# Helper functions

def _diff_schemas(old: SchemaDesign, new: SchemaDesign) -> Dict[str, Any]:
    """Diff two schemas to detect changes"""
    changes = {
        "added_tables": [],
        "removed_tables": [],
        "modified_tables": [],
        "added_relationships": [],
        "removed_relationships": []
    }

    old_table_names = {t.name for t in old.tables}
    new_table_names = {t.name for t in new.tables}

    # Detect added/removed tables
    changes["added_tables"] = [t for t in new.tables if t.name not in old_table_names]
    changes["removed_tables"] = [t for t in old.tables if t.name not in new_table_names]

    # Detect modified tables
    common_tables = old_table_names & new_table_names
    for table_name in common_tables:
        old_table = next(t for t in old.tables if t.name == table_name)
        new_table = next(t for t in new.tables if t.name == table_name)

        old_cols = {c.name: c for c in old_table.columns}
        new_cols = {c.name: c for c in new_table.columns}

        if old_cols != new_cols:
            changes["modified_tables"].append({
                "table": table_name,
                "added_columns": [c for c in new_table.columns if c.name not in old_cols],
                "removed_columns": [c for c in old_table.columns if c.name not in new_cols]
            })

    # Detect relationship changes (simplified)
    old_rels = {(r.from_table, r.from_column, r.to_table) for r in old.relationships}
    new_rels = {(r.from_table, r.from_column, r.to_table) for r in new.relationships}

    changes["added_relationships"] = [r for r in new.relationships
                                     if (r.from_table, r.from_column, r.to_table) not in old_rels]
    changes["removed_relationships"] = [r for r in old.relationships
                                       if (r.from_table, r.from_column, r.to_table) not in new_rels]

    return changes


def _generate_up_migration(changes: Dict[str, Any], db_type: str) -> str:
    """Generate up migration SQL"""
    statements = []

    # Create new tables
    for table in changes["added_tables"]:
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

        stmt = f"CREATE TABLE {table.name} (\n    " + ",\n    ".join(cols) + "\n);"
        statements.append(stmt)

    # Modify existing tables
    for modification in changes["modified_tables"]:
        table_name = modification["table"]

        # Add columns
        for col in modification["added_columns"]:
            col_def = f"{col.type}"
            if not col.nullable:
                col_def += " NOT NULL"
            if col.default_value:
                col_def += f" DEFAULT {col.default_value}"

            stmt = f"ALTER TABLE {table_name} ADD COLUMN {col.name} {col_def};"
            statements.append(stmt)

        # Drop columns (not supported in all databases)
        for col in modification["removed_columns"]:
            stmt = f"ALTER TABLE {table_name} DROP COLUMN {col.name};"
            statements.append(stmt)

    # Add foreign keys
    for rel in changes["added_relationships"]:
        stmt = (f"ALTER TABLE {rel.from_table} "
               f"ADD CONSTRAINT fk_{rel.from_table}_{rel.from_column} "
               f"FOREIGN KEY ({rel.from_column}) REFERENCES {rel.to_table}({rel.to_column}) "
               f"ON DELETE {rel.on_delete} ON UPDATE {rel.on_update};")
        statements.append(stmt)

    return "\n\n".join(statements)


def _generate_down_migration(changes: Dict[str, Any], db_type: str) -> str:
    """Generate down migration SQL (reverse changes)"""
    statements = []

    # Drop added tables
    for table in changes["added_tables"]:
        statements.append(f"DROP TABLE {table.name};")

    # Reverse table modifications
    for modification in changes["modified_tables"]:
        table_name = modification["table"]

        # Drop added columns
        for col in modification["added_columns"]:
            statements.append(f"ALTER TABLE {table_name} DROP COLUMN {col.name};")

        # Re-add removed columns (best effort)
        for col in modification["removed_columns"]:
            col_def = f"{col.type}"
            if col.default_value:
                col_def += f" DEFAULT {col.default_value}"
            statements.append(f"ALTER TABLE {table_name} ADD COLUMN {col.name} {col_def};")

    # Drop added foreign keys
    for rel in changes["added_relationships"]:
        statements.append(f"ALTER TABLE {rel.from_table} DROP CONSTRAINT fk_{rel.from_table}_{rel.from_column};")

    # Recreate removed tables
    for table in changes["removed_tables"]:
        cols = []
        for col in table.columns:
            col_def = f"{col.name} {col.type}"
            if col.primary_key:
                col_def += " PRIMARY KEY"
            cols.append(col_def)

        stmt = f"CREATE TABLE {table.name} (\n    " + ",\n    ".join(cols) + "\n);"
        statements.append(stmt)

    return "\n\n".join(statements)


def _display_migration_changes(changes: Dict[str, Any]):
    """Display migration changes"""
    total_changes = (len(changes["added_tables"]) + len(changes["removed_tables"]) +
                    len(changes["modified_tables"]) + len(changes["added_relationships"]) +
                    len(changes["removed_relationships"]))

    if total_changes == 0:
        console.print("\n[yellow]No schema changes detected[/yellow]")
        return

    console.print("\n[bold cyan]Schema Changes:[/bold cyan]")

    if changes["added_tables"]:
        console.print(f"\n[green]Added Tables ({len(changes['added_tables'])}):[/green]")
        for table in changes["added_tables"]:
            console.print(f"  + {table.name} ({len(table.columns)} columns)")

    if changes["removed_tables"]:
        console.print(f"\n[red]Removed Tables ({len(changes['removed_tables'])}):[/red]")
        for table in changes["removed_tables"]:
            console.print(f"  - {table.name}")

    if changes["modified_tables"]:
        console.print(f"\n[yellow]Modified Tables ({len(changes['modified_tables'])}):[/yellow]")
        for mod in changes["modified_tables"]:
            console.print(f"  ~ {mod['table']}")
            for col in mod["added_columns"]:
                console.print(f"      + column: {col.name} ({col.type})")
            for col in mod["removed_columns"]:
                console.print(f"      - column: {col.name}")


def _save_raw_migration(output_dir: Path, migration_id: str, up_sql: str, down_sql: str):
    """Save raw SQL migration files"""
    up_file = output_dir / f"{migration_id}_up.sql"
    down_file = output_dir / f"{migration_id}_down.sql"

    with open(up_file, 'w') as f:
        f.write(up_sql)

    with open(down_file, 'w') as f:
        f.write(down_sql)


def _save_alembic_migration(output_dir: Path, migration_id: str, message: str, up_sql: str, down_sql: str):
    """Save Alembic-format migration"""
    # Build upgrade statements
    up_statements = []
    for stmt in up_sql.split(';'):
        if stmt.strip():
            up_statements.append(f"    op.execute('''{stmt.strip()}''')")
    upgrade_body = "\n".join(up_statements)

    # Build downgrade statements
    down_statements = []
    for stmt in down_sql.split(';'):
        if stmt.strip():
            down_statements.append(f"    op.execute('''{stmt.strip()}''')")
    downgrade_body = "\n".join(down_statements)

    content = f'''"""
{message}

Revision ID: {migration_id}
Created: {datetime.now().isoformat()}
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '{migration_id}'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated ###
{upgrade_body}
    # ### end commands ###


def downgrade():
    # ### commands auto generated ###
{downgrade_body}
    # ### end commands ###
'''

    file_path = output_dir / f"{migration_id}_{message.replace(' ', '_')}.py"
    with open(file_path, 'w') as f:
        f.write(content)


def _save_flyway_migration(output_dir: Path, migration_id: str, message: str, up_sql: str, down_sql: str):
    """Save Flyway-format migration"""
    up_file = output_dir / f"V{migration_id}__{message.replace(' ', '_')}.sql"
    down_file = output_dir / f"U{migration_id}__{message.replace(' ', '_')}.sql"

    with open(up_file, 'w') as f:
        f.write(f"-- Flyway migration: {message}\n")
        f.write(f"-- Created: {datetime.now().isoformat()}\n\n")
        f.write(up_sql)

    with open(down_file, 'w') as f:
        f.write(f"-- Flyway undo migration: {message}\n")
        f.write(f"-- Created: {datetime.now().isoformat()}\n\n")
        f.write(down_sql)


def _explain_migration_sql(sql: str) -> List[str]:
    """Explain migration SQL (simple parsing for MVP)"""
    explanations = []

    if "CREATE TABLE" in sql:
        explanations.append("Creates new table(s)")
    if "DROP TABLE" in sql:
        explanations.append("Drops existing table(s)")
    if "ALTER TABLE" in sql and "ADD COLUMN" in sql:
        explanations.append("Adds new column(s)")
    if "ALTER TABLE" in sql and "DROP COLUMN" in sql:
        explanations.append("Removes column(s)")
    if "ADD CONSTRAINT" in sql:
        explanations.append("Adds foreign key constraint(s)")
    if "CREATE INDEX" in sql:
        explanations.append("Creates index(es)")

    return explanations
