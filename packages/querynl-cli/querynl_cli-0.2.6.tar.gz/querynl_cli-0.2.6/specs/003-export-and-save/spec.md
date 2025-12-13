# Feature Specification: Export and Save Query Results

**Feature Branch**: `003-export-and-save`
**Created**: 2025-10-25
**Status**: Draft
**Input**: User description: "Export and save query results to files with support for multiple formats (CSV, JSON, SQL) in both CLI and REPL modes"

**Constitution**: This specification must comply with [QueryNL Constitution v1.0.0](../.specify/memory/constitution.md). All requirements must align with Security-First Design, User Experience Over Technical Purity, Transparency, Multi-Database Parity, and Fail-Safe Defaults principles.

## Clarifications

### Session 2025-10-25

- Q: What exactly does `\export` save in REPL mode when multiple queries have been executed? → A: Always exports only the most recent query result (last executed query's data)
- Q: When a file already exists, should the system prompt for confirmation or auto-rename? → A: Auto-rename with timestamp suffix (e.g., results_20251025_143022.csv) - no prompts
- Q: What constitutes "large" for progress indicators and what type of progress should be shown? → A: Show progress every 10,000 rows (e.g., "Exported 10,000 rows...", "20,000 rows...")
- Q: Should directories be created automatically for nested paths or require user confirmation? → A: Always create directories automatically (mkdir -p behavior)
- Q: What format should non-query commands (schema, tables, etc.) use when exported? → A: Plain text (.txt) for lists, Mermaid diagram format (.mmd) for schema diagrams

## User Scenarios & Testing

### User Story 1 - Basic CSV Export in CLI Mode (Priority: P1)

As a database administrator, I want to export query results to a CSV file from the command line so that I can analyze data in spreadsheet applications or share results with non-technical team members.

**Why this priority**: This is the most common use case - CSV is universally compatible with spreadsheet tools (Excel, Google Sheets) and is the expected baseline functionality for any query tool. This alone provides immediate value.

**Independent Test**: Can be fully tested by running `querynl query "SELECT * FROM users" --export results.csv` and verifying that a valid CSV file is created with proper headers and data.

**Acceptance Scenarios**:

1. **Given** I have query results from a CLI command, **When** I specify `--export output.csv`, **Then** the results are saved to a CSV file with column headers and properly escaped values
2. **Given** the export file already exists, **When** I run an export command, **Then** the file is automatically renamed with a timestamp suffix (e.g., output_20251025_143022.csv) and I see a message indicating the new filename
3. **Given** I run a query that returns no results, **When** I export to CSV, **Then** a CSV file is created with only headers
4. **Given** the query results contain special characters (commas, quotes, newlines), **When** exported to CSV, **Then** all values are properly escaped according to CSV standards

---

### User Story 2 - Export in REPL Mode (Priority: P2)

As a data analyst working in REPL mode, I want to export my current query results without leaving the interactive session so that I can save interesting findings while continuing my exploratory analysis.

**Why this priority**: REPL mode is for interactive exploration, and being able to save results mid-session without interrupting workflow is critical for data analysts who discover unexpected insights.

**Independent Test**: Can be tested by starting REPL, running a query, then executing `\export results.csv` and verifying the last query results are saved.

**Acceptance Scenarios**:

1. **Given** I just executed a query in REPL mode, **When** I type `\export filename.csv`, **Then** the results from my most recent query are saved to the specified file
2. **Given** I execute multiple queries in succession (Query A, then Query B, then Query C), **When** I type `\export filename.csv`, **Then** only Query C's results are exported (most recent query only)
3. **Given** I'm in REPL mode with no previous query executed, **When** I try to export, **Then** I receive a helpful error message stating no results are available to export
4. **Given** I want to export in a different format, **When** I type `\export filename.json`, **Then** the system detects the file extension and exports in JSON format automatically
5. **Given** I want to specify the export path, **When** I type `\export /path/to/folder/results.csv`, **Then** the file is saved to the specified absolute or relative path

---

### User Story 3 - Multiple Format Support (Priority: P3)

As a developer integrating QueryNL output with other tools, I want to export results in JSON and SQL INSERT formats, plus Mermaid diagrams for schema visualizations, so that I can pipe data into APIs, scripts, documentation tools, or replicate data to other databases.

**Why this priority**: While CSV covers most use cases, developers need structured data formats (JSON), database migration formats (SQL INSERT statements), and diagram formats (Mermaid) for documentation. This expands QueryNL's utility for automation, integration, and documentation scenarios.

**Independent Test**: Can be tested by exporting the same query results to CSV, JSON, and SQL formats, plus exporting schema visualization to Mermaid format, and verifying each format is valid.

**Acceptance Scenarios**:

1. **Given** I want JSON output, **When** I use `--export output.json` or `--format json --export output.json`, **Then** results are saved as a JSON array of objects with proper escaping
2. **Given** I want SQL INSERT statements, **When** I use `--export output.sql` or `--format sql --export output.sql`, **Then** a SQL file is created with INSERT statements that can be executed on the same database type
3. **Given** I want to export schema as a diagram, **When** I run `\schema graph` and then `\export schema.mmd`, **Then** a Mermaid ER diagram file is created with valid syntax that can be rendered in GitHub, GitLab, or Notion
4. **Given** I specify a format flag, **When** it conflicts with file extension (e.g., `--format json --export output.csv`), **Then** the format flag takes precedence and I receive a warning about the mismatch
5. **Given** I export to JSON, **When** results contain NULL values or special data types (timestamps, JSON columns), **Then** these are properly serialized according to JSON standards

---

### User Story 4 - Auto-Export Mode (Priority: P4)

As a data engineer running regular reports, I want to automatically export query results without manually specifying the export flag each time so that I can script scheduled data extracts more efficiently.

**Why this priority**: This is a convenience feature for automation scenarios. It's useful but not critical - users can already achieve this with the export flag in scripts.

**Independent Test**: Can be tested by enabling auto-export mode in config and verifying all subsequent queries automatically save to files with timestamp-based names.

**Acceptance Scenarios**:

1. **Given** I enable auto-export in my configuration file, **When** I run any query, **Then** results are automatically saved to a default export directory with timestamp-based filenames
2. **Given** auto-export is enabled, **When** I want to disable it for a single query, **Then** I can use a `--no-export` flag to skip exporting
3. **Given** auto-export is enabled, **When** I specify an explicit export path, **Then** the explicit path takes precedence over the auto-export settings

---

### Edge Cases

- What happens when the export directory doesn't exist? (Should automatically create all parent directories, similar to mkdir -p behavior)
- What happens when disk space is full during export? (Should fail gracefully with clear error message)
- What happens when the user lacks write permissions to the target directory? (Should fail with permission error before executing query)
- What happens with very large result sets (millions of rows)? (Should stream to file rather than loading all into memory, with progress messages every 10,000 rows exported)
- What happens when result contains binary data (BLOB columns)? (Should handle gracefully - base64 encode for JSON, skip with warning for CSV, or allow user to exclude columns)
- What happens when column names contain special characters or spaces? (Should quote/escape properly in CSV headers, sanitize for SQL)
- What happens when exporting schema visualization or REPL help output? (Should export schema diagrams as Mermaid format (.mmd) for ER diagrams, and other meta-command outputs as plain text (.txt))

## Requirements

### Functional Requirements

- **FR-001**: System MUST support exporting query results to CSV format with proper header row and escaped values
- **FR-002**: System MUST support exporting query results to JSON format as an array of objects
- **FR-003**: System MUST support exporting query results to SQL INSERT statement format
- **FR-003a**: System MUST support exporting schema diagrams to Mermaid ER diagram format (.mmd)
- **FR-004**: System MUST allow users to specify export file path via `--export <filepath>` flag in CLI mode
- **FR-005**: System MUST provide a `\export <filepath>` command in REPL mode to save only the most recent query's results (not all queries from the session)
- **FR-006**: System MUST auto-detect export format from file extension (.csv, .json, .sql, .mmd, .txt)
- **FR-007**: System MUST allow explicit format specification via `--format <csv|json|sql>` flag that overrides file extension
- **FR-008**: System MUST handle file naming conflicts by automatically renaming with timestamp suffix (format: YYYYMMDD_HHMMSS) and informing the user of the new filename
- **FR-009**: System MUST automatically create all parent directories (mkdir -p behavior) when exporting to nested paths that don't exist
- **FR-010**: System MUST provide clear error messages for permission errors, disk full errors, and invalid paths
- **FR-011**: System MUST properly escape special characters in CSV exports (commas, quotes, newlines, NULL values)
- **FR-012**: System MUST properly serialize data types in JSON exports (NULL, timestamps, nested JSON, numeric types)
- **FR-013**: System MUST generate valid SQL INSERT statements with proper escaping for the target database type
- **FR-014**: System MUST support exporting results from all query types (SELECT, DESCRIBE, SHOW, etc.)
- **FR-015**: System MUST stream large result sets to file incrementally rather than loading entirely into memory, displaying progress messages every 10,000 rows
- **FR-016**: System MUST display export success message with file path and row count
- **FR-017**: System MUST support both absolute and relative file paths for exports
- **FR-018**: System MUST work consistently across all supported database types (PostgreSQL, MySQL, SQLite, MongoDB)
- **FR-019**: System MUST allow exporting output from non-query commands: schema diagrams as Mermaid format (.mmd), other meta-command outputs as plain text (.txt)
- **FR-021**: System MUST generate valid Mermaid ER diagram syntax when exporting schema visualizations to .mmd files
- **FR-020**: System MUST preserve column order from query results in exported files

### Key Entities

- **Export Configuration**: Represents export settings including format, file path, overwrite behavior, and whether auto-export is enabled
- **Export Result**: Represents the outcome of an export operation including success/failure status, file path, row count, and any warnings or errors
- **Format Converter**: Represents the logic for transforming query results into specific file formats with appropriate escaping and serialization

## Success Criteria

### Measurable Outcomes

- **SC-001**: Users can export query results to CSV, JSON, or SQL format in under 3 seconds for result sets up to 10,000 rows
- **SC-002**: Exported CSV files can be opened in Excel, Google Sheets, and other spreadsheet applications without formatting errors
- **SC-003**: Exported JSON files are valid JSON and can be parsed by standard JSON parsers without errors
- **SC-004**: Exported SQL INSERT statements can be executed on the target database without syntax errors
- **SC-004a**: Exported Mermaid diagrams render correctly in GitHub, GitLab, Notion, and other Mermaid-compatible tools
- **SC-005**: System handles result sets of up to 1 million rows without running out of memory (using streaming)
- **SC-006**: Export operations fail gracefully with clear error messages for 100% of error scenarios (permissions, disk space, invalid paths)
- **SC-007**: File naming conflicts are resolved without data loss in 100% of cases through automatic timestamp-based renaming
- **SC-008**: Users can successfully export results from both CLI and REPL modes with the same features available in both interfaces
- **SC-009**: 95% of users can successfully export their first query results without consulting documentation
- **SC-010**: Export feature works identically across PostgreSQL, MySQL, SQLite, and MongoDB databases

## Assumptions

- Users have basic familiarity with file system paths and common file formats (CSV, JSON, SQL)
- Default export behavior is to auto-rename with timestamp when file exists (never overwrites, never prompts)
- Auto-export mode (Priority P4) is disabled by default and must be explicitly enabled
- Large file exports are streamed incrementally with progress messages displayed every 10,000 rows to provide transparency
- Binary/BLOB data will be handled with sensible defaults (base64 for JSON, exclusion for CSV with warning)
- SQL INSERT format generates statements compatible with the source database type only (not cross-database)
- Export paths are relative to the current working directory unless absolute path is specified
- REPL `\export` command applies to the most recent query result in the session
- Schema visualization exports (from `\schema graph`, etc.) export as Mermaid ER diagram format (.mmd) for rendering in documentation tools

## Out of Scope

- Exporting to proprietary formats (Excel .xlsx, Parquet, Avro) - only open formats in MVP
- Automated scheduled exports with cron-like scheduling - use external task schedulers
- Cloud storage destinations (S3, GCS, Azure Blob) - local filesystem only
- Export transformations or filtering (e.g., export only certain columns) - use SQL for this
- Compression of export files (.gz, .zip) - users can compress manually if needed
- Email or Slack integration for sending exported files - out of scope for CLI tool
- Incremental/differential exports that track what was previously exported
- Export templates or custom export formatting beyond standard CSV/JSON/SQL
