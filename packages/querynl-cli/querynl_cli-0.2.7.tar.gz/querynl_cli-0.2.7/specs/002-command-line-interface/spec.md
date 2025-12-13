# Feature Specification: QueryNL CLI - Command Line Interface Tool

**Feature Branch**: `002-command-line-interface`
**Created**: 2025-10-12
**Status**: Draft
**Input**: User description: "Command Line Interface (CLI) Tool - Provide a standalone command-line interface similar to Claude Code that allows developers to interact with the database agent from the terminal"

**Constitution**: This specification must comply with [QueryNL Constitution v1.0.0](../.specify/memory/constitution.md). All requirements must align with Security-First Design, User Experience Over Technical Purity, Transparency, Multi-Database Parity, and Fail-Safe Defaults principles.

## Executive Summary

The QueryNL CLI provides a standalone command-line interface for developers who work primarily in terminal environments. It delivers full feature parity with IDE extensions, enabling natural language database queries, schema design, and migration generation directly from the command line. The CLI supports both interactive REPL mode for exploratory work and scriptable commands for automation and CI/CD integration.

The CLI targets terminal-focused developers, DevOps engineers, database administrators, and automation scenarios where IDE extensions are impractical. By providing a first-class terminal experience, QueryNL becomes accessible in SSH sessions, containerized environments, CI/CD pipelines, and server administration contexts.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Interactive Natural Language Queries (Priority: P1)

A backend developer working in a terminal session needs to query a database without switching to an IDE. They run `querynl query "show all active users"` and receive formatted results instantly, or enter interactive mode with `querynl repl` for exploratory data analysis with persistent conversation context.

**Why this priority**: This is the core CLI use case—enabling quick database access from the terminal. It provides immediate value and can function independently as a complete tool.

**Independent Test**: Can be fully tested by installing the CLI, connecting to a test database, and executing natural language queries. Verifies basic functionality and delivers value without any other features.

**Acceptance Scenarios**:

1. **Given** the CLI is installed and a database connection configured, **When** the user runs `querynl query "count all users"`, **Then** the CLI generates SQL, displays it for review, executes it, and shows results in a formatted table
2. **Given** an active query session, **When** the user runs `querynl query --format json "select users"`, **Then** results are output as JSON for piping to other tools
3. **Given** the user starts `querynl repl`, **When** they enter multiple related queries, **Then** the system maintains conversation context across queries
4. **Given** a long-running query, **When** the user presses Ctrl+C, **Then** the query is cancelled gracefully and the CLI returns to ready state
5. **Given** an ambiguous query, **When** the CLI detects multiple interpretations, **Then** it prompts the user to choose from clarification options before generating SQL

---

### User Story 2 - Connection Management (Priority: P1)

A developer needs to manage multiple database connections from the command line. They use `querynl connect add` to configure a new connection with secure credential storage, `querynl connect list` to view available connections, and `querynl connect use <name>` to switch active connections.

**Why this priority**: Connection management is essential infrastructure for all CLI features. Without it, no queries can be executed. Must be implemented first.

**Independent Test**: Can be tested by adding, listing, updating, and removing connections, verifying credentials are stored securely and never exposed in plain text.

**Acceptance Scenarios**:

1. **Given** the CLI is installed, **When** the user runs `querynl connect add prod-db`, **Then** the CLI prompts for connection details, stores credentials encrypted in system keychain, and confirms successful setup
2. **Given** multiple connections configured, **When** the user runs `querynl connect list`, **Then** all connections are displayed with name, type, host, and status (not credentials)
3. **Given** a configured connection, **When** the user runs `querynl connect test prod-db`, **Then** the CLI verifies connectivity and reports success or detailed error
4. **Given** stored credentials, **When** the user runs `querynl connect use prod-db`, **Then** the CLI sets this as the active connection for subsequent commands
5. **Given** a connection to remove, **When** the user runs `querynl connect remove dev-db --confirm`, **Then** credentials are securely deleted from keychain and config removed

---

### User Story 3 - Schema Design from CLI (Priority: P2)

A developer wants to design a database schema from the terminal as part of a new project setup. They run `querynl schema design "e-commerce with users, products, orders"` and receive a generated schema with ER diagram exported as text/markdown, which they can review and approve for migration generation.

**Why this priority**: Schema design is valuable for project initialization and planning but less frequently used than queries. It builds on connection management and can be developed after core query functionality.

**Independent Test**: Can be tested by providing schema descriptions and verifying normalized schemas are generated with appropriate relationships and constraints.

**Acceptance Scenarios**:

1. **Given** a connected database, **When** the user runs `querynl schema design "blog with posts and comments"`, **Then** the CLI generates a schema, displays tables/relationships, and saves to a file
2. **Given** a generated schema, **When** the user runs `querynl schema visualize --output schema.md`, **Then** an ER diagram in Mermaid syntax is written to the file
3. **Given** an existing schema file, **When** the user runs `querynl schema modify schema.json "add user profiles"`, **Then** the schema is updated while preserving existing tables and relationships
4. **Given** a schema design, **When** the user runs `querynl schema analyze schema.json`, **Then** design issues (missing indexes, normalization problems) are reported with suggestions
5. **Given** an approved schema, **When** the user runs `querynl schema apply schema.json --connection dev-db`, **Then** CREATE TABLE statements are generated and optionally executed

---

### User Story 4 - Migration Generation (Priority: P2)

A developer has modified their schema and needs to generate migration files compatible with their migration framework. They run `querynl migrate generate --from old-schema.json --to new-schema.json --framework alembic` and receive properly formatted migration files with both up and down scripts.

**Why this priority**: Migration generation is essential for production schema evolution but depends on schema design capability. It's independently valuable for teams using migration frameworks.

**Independent Test**: Can be tested by providing before/after schemas, generating migrations, and verifying they can be applied successfully to a test database.

**Acceptance Scenarios**:

1. **Given** a schema change, **When** the user runs `querynl migrate generate --message "add indexes"`, **Then** migration files are created in the configured framework format with timestamp/version
2. **Given** a migration file, **When** the user runs `querynl migrate preview migration_001.sql`, **Then** the SQL statements are displayed with explanation of changes
3. **Given** pending migrations, **When** the user runs `querynl migrate apply`, **Then** migrations are applied to the active connection with transaction rollback on failure
4. **Given** applied migrations, **When** the user runs `querynl migrate status`, **Then** a list shows which migrations are applied, pending, or failed
5. **Given** a failed migration, **When** the user runs `querynl migrate rollback`, **Then** the last migration is rolled back using the down script

---

### User Story 5 - Scriptable Commands for Automation (Priority: P2)

A DevOps engineer wants to integrate QueryNL into CI/CD pipelines to validate database schemas and run automated queries. They write shell scripts using `querynl` commands with proper exit codes, JSON output, and non-interactive mode to check schema health before deployments.

**Why this priority**: Automation support expands QueryNL's utility beyond interactive use to enable CI/CD integration. This is valuable for teams with mature DevOps practices but not essential for individual developers.

**Independent Test**: Can be tested by writing shell scripts that use QueryNL commands and verifying exit codes, output formats, and error handling work correctly for automation.

**Acceptance Scenarios**:

1. **Given** a shell script, **When** it runs `querynl query "count users" --format json --non-interactive`, **Then** output is machine-readable JSON with no prompts
2. **Given** a CI/CD pipeline, **When** it runs `querynl schema validate schema.json`, **Then** exit code 0 for valid schema, non-zero with error message for issues
3. **Given** automation needs, **When** a script runs `querynl migrate status --format json`, **Then** migration status is output as parseable JSON array
4. **Given** credentials in environment, **When** `querynl` commands run with `QUERYNL_CONNECTION_STRING` set, **Then** connection info is read from env vars instead of keychain
5. **Given** an error condition, **When** any `querynl` command fails, **Then** exit code is non-zero, error message goes to stderr, and normal output to stdout

---

### User Story 6 - Output Format Flexibility (Priority: P3)

A developer wants to process query results in different formats depending on their workflow. They use `--format table` for human-readable output, `--format json` for piping to jq, `--format csv` for spreadsheet import, and `--format markdown` for documentation.

**Why this priority**: Format flexibility enhances usability but is not essential for core functionality. Default table format is sufficient for most use cases. Additional formats improve power user experience.

**Independent Test**: Can be tested by executing the same query with different --format flags and verifying output matches expected format specifications.

**Acceptance Scenarios**:

1. **Given** query results, **When** using `--format table` (default), **Then** results display as an ASCII table with aligned columns and borders
2. **Given** query results, **When** using `--format json`, **Then** results are valid JSON array of objects suitable for programmatic processing
3. **Given** query results, **When** using `--format csv`, **Then** results are RFC 4180 compliant CSV with proper escaping
4. **Given** query results, **When** using `--format markdown`, **Then** results are a markdown table suitable for documentation
5. **Given** any format, **When** results exceed terminal width, **Then** output is paginated or wraps appropriately

---

### User Story 7 - Interactive REPL Mode (Priority: P2)

A data analyst wants to explore a database interactively without typing `querynl` before every command. They run `querynl repl` to enter an interactive shell with command history, tab completion, and persistent context across multiple queries.

**Why this priority**: REPL mode significantly improves user experience for exploratory work but is not essential for basic CLI functionality. It's a quality-of-life enhancement that makes the CLI more pleasant to use.

**Independent Test**: Can be tested by entering REPL mode and verifying interactive features (history, completion, multi-line input) work correctly.

**Acceptance Scenarios**:

1. **Given** REPL mode, **When** the user types partial commands and presses Tab, **Then** available completions are suggested (table names, commands)
2. **Given** REPL history, **When** the user presses Up arrow, **Then** previous commands are recalled for editing and re-execution
3. **Given** a multi-line query, **When** the user enters an opening parenthesis or quote, **Then** the prompt continues on next line until closing character
4. **Given** REPL session, **When** the user types `\help`, **Then** available commands and shortcuts are displayed
5. **Given** REPL mode, **When** the user types `exit` or presses Ctrl+D, **Then** the session ends gracefully with context saved

---

### User Story 8 - Configuration Management (Priority: P3)

A user wants to customize CLI behavior through configuration files. They create a `~/.querynl/config.yaml` file to set default output format, connection, LLM provider, and other preferences that persist across sessions.

**Why this priority**: Configuration enhances power user experience but defaults work well for most users. This is a nice-to-have feature that reduces repetitive flag usage.

**Independent Test**: Can be tested by creating config files with various settings and verifying CLI respects them while allowing command-line flags to override config values.

**Acceptance Scenarios**:

1. **Given** a config file with `default_format: json`, **When** running queries without --format, **Then** output defaults to JSON
2. **Given** a config file with `default_connection: prod`, **When** running commands without --connection, **Then** prod connection is used
3. **Given** conflicting settings, **When** command-line flags are provided, **Then** flags override config file settings
4. **Given** no config file, **When** the CLI runs, **Then** sensible built-in defaults are used without error
5. **Given** invalid config syntax, **When** the CLI starts, **Then** a clear error message is displayed with the syntax error location

---

### Edge Cases

- What happens when the terminal window is resized during output?
- How does the CLI handle piped input from stdin (e.g., `echo "query users" | querynl query -`)?
- What happens when output exceeds terminal buffer size?
- How does the CLI behave when run in non-TTY environments (Docker containers, CI/CD)?
- What happens when keychain access is unavailable (headless servers)?
- How does the CLI handle concurrent executions (multiple terminals)?
- What happens when the config file path is not writable?
- How does the CLI handle very long query results (millions of rows)?
- What happens when network connection is lost mid-query?
- How does the CLI handle timezone differences between client and database?
- What happens when the user's LLM API quota is exceeded?
- How does the CLI behave with no internet connection (offline mode)?

## Requirements *(mandatory)*

### Functional Requirements

#### Core CLI Functionality
- **FR-001**: CLI MUST provide a `querynl` command-line tool installable via package managers (npm, homebrew, apt, or binary download)
- **FR-002**: CLI MUST support natural language query execution with `querynl query "<natural language>"`
- **FR-003**: CLI MUST display generated SQL before execution and require explicit confirmation for destructive operations
- **FR-004**: CLI MUST support interactive REPL mode via `querynl repl` with command history and tab completion
- **FR-005**: CLI MUST provide comprehensive help documentation via `--help` flag for all commands and subcommands
- **FR-006**: CLI MUST return appropriate exit codes (0 for success, non-zero for errors) for scriptability
- **FR-007**: CLI MUST complete query execution in under 3 seconds for 90% of queries (matching VS Code extension performance)

#### Connection Management
- **FR-008**: CLI MUST support adding database connections with `querynl connect add <name>`
- **FR-009**: CLI MUST store credentials encrypted in system keychain (macOS Keychain, Windows Credential Manager, Linux Secret Service)
- **FR-010**: CLI MUST support listing connections with `querynl connect list` (without exposing credentials)
- **FR-011**: CLI MUST support testing connections with `querynl connect test <name>`
- **FR-012**: CLI MUST support switching active connections with `querynl connect use <name>`
- **FR-013**: CLI MUST support removing connections with `querynl connect remove <name>`
- **FR-014**: CLI MUST support reading connection info from environment variables (e.g., `QUERYNL_CONNECTION_STRING`) for containerized environments

#### Schema Design
- **FR-015**: CLI MUST support schema design with `querynl schema design "<description>"`
- **FR-016**: CLI MUST export schemas to JSON format for version control and collaboration
- **FR-017**: CLI MUST generate ER diagrams in Mermaid syntax with `querynl schema visualize`
- **FR-018**: CLI MUST analyze schemas for issues with `querynl schema analyze <file>`
- **FR-019**: CLI MUST support modifying existing schemas with natural language modifications

#### Migration Management
- **FR-020**: CLI MUST generate migration files with `querynl migrate generate`
- **FR-021**: CLI MUST support multiple migration frameworks (Alembic, Flyway at minimum)
- **FR-022**: CLI MUST generate both up and down migration scripts
- **FR-023**: CLI MUST preview migrations with `querynl migrate preview <file>`
- **FR-024**: CLI MUST apply migrations with `querynl migrate apply` and rollback with `querynl migrate rollback`
- **FR-025**: CLI MUST track migration status with `querynl migrate status`

#### Output Formatting
- **FR-026**: CLI MUST support multiple output formats: table (default), JSON, CSV, markdown
- **FR-027**: CLI MUST format table output with proper column alignment and borders
- **FR-028**: CLI MUST support `--format` flag on all commands that produce output
- **FR-029**: CLI MUST paginate large result sets automatically (using less/more on Unix, more on Windows)
- **FR-030**: CLI MUST respect terminal width and adapt output accordingly

#### Configuration & Preferences
- **FR-031**: CLI MUST support configuration file at platform-specific locations (XDG on Linux, ~/Library on macOS, AppData on Windows)
- **FR-032**: CLI MUST allow setting default connection, output format, and LLM provider in config
- **FR-033**: CLI MUST allow command-line flags to override config file settings
- **FR-034**: CLI MUST validate config file syntax and provide clear error messages for invalid configuration

#### Scriptability & Automation
- **FR-035**: CLI MUST support non-interactive mode with `--non-interactive` or `-y` flag
- **FR-036**: CLI MUST output errors to stderr and normal output to stdout for proper piping
- **FR-037**: CLI MUST support piping input from stdin for batch processing
- **FR-038**: CLI MUST support reading queries from files with `querynl query --file queries.sql`
- **FR-039**: CLI MUST provide JSON output format suitable for parsing by CI/CD tools

#### Security & Credentials
- **FR-040**: CLI MUST never display credentials in plain text (logs, output, error messages)
- **FR-041**: CLI MUST support LLM API key configuration for BYOK users
- **FR-042**: CLI MUST validate SSL certificates for database connections by default
- **FR-043**: CLI MUST support SSH tunneling for remote database access
- **FR-044**: CLI MUST sanitize all user inputs to prevent SQL injection

#### Platform Support
- **FR-045**: CLI MUST run on macOS (Intel and Apple Silicon)
- **FR-046**: CLI MUST run on Linux (Ubuntu 20.04+, Debian, RHEL/CentOS)
- **FR-047**: CLI MUST run on Windows 10+
- **FR-048**: CLI MUST provide installation packages for npm, Homebrew, and direct binary download

### Key Entities

- **CLI Session**: Represents an active CLI execution with context (active connection, query history, preferences). Short-lived for single commands, persistent for REPL mode.

- **Connection Profile**: Stored connection configuration including name, database type, host, port, database name, and encrypted credential reference. Persisted in config file with credentials in keychain.

- **Query History**: Record of executed queries in REPL mode, including natural language input, generated SQL, execution time, and results summary. Stored locally for command recall.

- **CLI Configuration**: User preferences stored in config file including default connection, output format, LLM provider, and custom settings. Platform-specific file location.

- **Migration State**: Tracking information for migrations including applied migrations, pending migrations, and failure history. Stored in project directory or database.

## Success Criteria *(mandatory)*

### Measurable Outcomes

#### User Productivity
- **SC-001**: Users can install the CLI and execute their first query within 3 minutes
- **SC-002**: Query execution from CLI completes within 3 seconds for 90% of queries
- **SC-003**: CLI commands have feature parity with VS Code extension for core functionality
- **SC-004**: 80% of users successfully complete connection setup on first attempt

#### Developer Experience
- **SC-005**: CLI help documentation covers 100% of commands with examples
- **SC-006**: Error messages are actionable with suggested remediation in 95% of failure cases
- **SC-007**: REPL mode provides tab completion for table names and common commands
- **SC-008**: CLI respects terminal conventions (colors, width, paging) on all supported platforms

#### Automation & Scripting
- **SC-009**: CLI provides consistent exit codes enabling reliable error detection in scripts
- **SC-010**: JSON output format is parseable by standard tools (jq, Python json module)
- **SC-011**: CLI runs successfully in non-interactive environments (Docker, CI/CD)
- **SC-012**: Environment variable configuration works without requiring keychain access

#### Performance
- **SC-013**: CLI binary size is under 50MB for single-binary distributions
- **SC-014**: CLI startup time (to ready state) is under 500ms
- **SC-015**: Memory usage during query execution stays under 100MB for typical queries
- **SC-016**: Large result sets (10,000+ rows) are streamed efficiently without loading entirely into memory

#### Security & Reliability
- **SC-017**: Zero credential exposure incidents in logs, error messages, or terminal output
- **SC-018**: Credential encryption uses platform-native keychain APIs on all supported OSes
- **SC-019**: CLI handles network failures gracefully with retry logic and clear error messages
- **SC-020**: SQL injection attack attempts are detected and blocked by input validation

#### Platform Support
- **SC-021**: CLI installs successfully on macOS, Linux, and Windows without manual dependencies
- **SC-022**: Installation via package manager (npm, Homebrew) completes in under 2 minutes
- **SC-023**: CLI binary runs without requiring installation on all platforms (portable mode)
- **SC-024**: Platform-specific features (keychain, config paths) work correctly on each OS

## Assumptions

1. **Target Users**: Assumes users are comfortable with command-line interfaces and understand basic SQL concepts
2. **Terminal Environment**: Assumes users have access to a terminal emulator with ANSI color support
3. **Network Access**: Assumes users have internet connectivity for LLM API calls (except offline mode)
4. **Keychain Access**: Assumes system keychain is available and accessible (fallback to encrypted file for headless servers)
5. **Package Managers**: Assumes users can install via npm (Node.js installed) or use binary downloads
6. **Database Permissions**: Assumes users have appropriate database credentials and permissions for their use case
7. **Migration Frameworks**: Assumes teams using migrations already have a framework (Alembic, Flyway) configured
8. **Configuration Files**: Assumes users can read/write to home directory for config storage
9. **LLM Providers**: Assumes major LLM providers (OpenAI, Anthropic) maintain stable APIs
10. **REPL Libraries**: Assumes standard readline/linenoise libraries provide adequate interactive features

## Dependencies

1. **Backend Service**: CLI requires the QueryNL backend service for LLM orchestration and query generation
2. **System Keychain**: Depends on OS-native keychain APIs for secure credential storage
3. **Terminal Libraries**: Depends on terminal handling libraries (readline, termcolor, blessed/ink)
4. **Database Drivers**: Requires same database drivers as VS Code extension
5. **Package Managers**: Distribution depends on npm registry, Homebrew tap, or GitHub releases
6. **Shared Core Logic**: CLI shares query generation, schema design, and migration logic with IDE extensions

## Out of Scope (Initial Release)

1. **GUI Mode**: No graphical interface—pure command-line only
2. **Plugin System**: No extension/plugin architecture for third-party commands
3. **Cloud Sync**: No syncing of configuration or history across devices
4. **Advanced Visualizations**: No charts or graphs—text/table output only
5. **Database Administration**: No backup/restore, user management, or performance monitoring
6. **Real-time Collaboration**: No shared sessions or multi-user REPL
7. **Custom Themes**: No terminal theme customization beyond standard ANSI colors
8. **Windows PowerShell Module**: Only standard CLI, not PowerShell cmdlets
9. **Shell Completions**: No bash/zsh completion scripts (Phase 2 feature)
10. **Alias System**: No custom command aliases or shortcuts

## Non-Functional Requirements

### Performance
- CLI startup time must not exceed 500ms
- Query execution must match IDE extension performance (<3s for 90% of queries)
- Memory footprint must stay under 100MB during normal operation
- Binary size must be under 50MB for single-binary distributions

### Reliability
- CLI must handle network interruptions gracefully with retry logic
- All state changes (connection config, migration status) must be atomic
- CLI must never leave partial/corrupted state files after crashes
- Error recovery must be automatic without requiring manual cleanup

### Usability
- All error messages must be clear, actionable, and include suggested fixes
- Help documentation must be comprehensive with examples for every command
- Terminal output must respect width/height and adapt to window resizing
- Command naming must follow Unix conventions (lowercase, hyphens, clear verbs)

### Security
- Credential encryption must use AES-256 or OS keychain equivalent
- SSL/TLS must be enabled by default for database connections
- No sensitive data (credentials, queries with PII) logged to disk
- API keys must be stored separately from database credentials

### Portability
- CLI must run on macOS (10.15+), Linux (kernel 4.x+), Windows (10+)
- No hard dependencies on specific shell (work in bash, zsh, fish, PowerShell, cmd)
- Binary must be self-contained or clearly document runtime dependencies
- Configuration file format must be portable across platforms

### Maintainability
- Codebase must share logic with IDE extensions (monorepo or shared packages)
- CLI commands must be modular and easily extensible
- Automated tests must cover 80%+ of code paths
- Platform-specific code must be isolated and clearly marked
