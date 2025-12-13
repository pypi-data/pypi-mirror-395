---
description: "Task list for QueryNL CLI implementation"
---

# Tasks: Command Line Interface Tool

**Input**: Design documents from `/specs/002-command-line-interface/`
**Prerequisites**: plan.md (complete), spec.md (complete), data-model.md (complete), contracts/ (complete)

**Tests**: Tests are OPTIONAL per spec.md - not included in this task list

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

**Constitution Compliance**: All tasks must align with [QueryNL Constitution v1.0.0](../../.specify/memory/constitution.md). Security-first design, transparency, and fail-safe defaults are non-negotiable.

## Format: `[ID] [P?] [Story] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions
- Single project structure: `src/cli/` for CLI code, `tests/cli/` for tests
- Shared backend: `src/models/`, `src/services/`, `src/lib/` (existing)
- User config: `~/.querynl/` (created at runtime)

---

## Phase 1: Setup & Project Initialization

**Purpose**: Create project structure and initialize dependencies

- [X] T001 Create CLI directory structure (src/cli/, src/cli/commands/, src/cli/formatting/, tests/cli/)
- [X] T002 Update requirements.txt with Click 8.1+, Rich 13.0+, prompt_toolkit 3.0+, keyring 25.0+, keyrings.cryptfile 1.3+, PyYAML 6.0+
- [X] T003 [P] Create src/cli/__init__.py with version export
- [X] T004 [P] Create src/cli/commands/__init__.py
- [X] T005 [P] Create src/cli/formatting/__init__.py
- [X] T006 Create src/cli/main.py with Click app scaffold (empty command groups: query, connect, schema, migrate, config)
- [X] T007 Setup entry point in setup.py or pyproject.toml (console_scripts: querynl = src.cli.main:cli)
- [X] T008 Configure pytest for CLI tests in pytest.ini (testpaths = tests/cli)

**Checkpoint**: Project structure created, dependencies installable, `querynl --version` command works

---

## Phase 2: Foundational Infrastructure (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T009 [P] [Foundation] Create platform-specific config path resolver in src/cli/config.py (XDG_CONFIG_HOME on Linux, ~/Library/Application Support on macOS, %APPDATA% on Windows)
- [X] T010 [P] [Foundation] Implement config file loader/saver in src/cli/config.py (YAML parsing, validation, atomic writes)
- [X] T011 [P] [Foundation] Create CLIConfiguration model class in src/cli/config.py (from data-model.md)
- [X] T012 [P] [Foundation] Implement keyring credential storage wrapper in src/cli/credentials.py (service="querynl", account=connection_name)
- [X] T013 [P] [Foundation] Add keyrings.cryptfile fallback in src/cli/credentials.py (for headless environments with QUERYNL_KEYRING_PASSWORD env var)
- [X] T014 [P] [Foundation] Create error handling framework in src/cli/errors.py (custom exceptions: ConfigError, ConnectionError, QueryError with actionable messages)
- [X] T015 [P] [Foundation] Create logging configuration in src/cli/logging.py (console and file handlers, respect --verbose flag, never log credentials)
- [X] T016 [Foundation] Integrate existing database drivers from src/lib/ into CLI context (reuse connection pooling, driver detection)

**Checkpoint**: Foundation ready - config system works, credentials store/retrieve securely, error handling provides actionable messages, database drivers accessible

---

## Phase 3: User Story 2 - Connection Management (Priority: P1) 🎯 MVP

**Goal**: Users can add/list/test/use/remove database connections with secure credential storage

**Independent Test**: Run `querynl connect add test-db`, verify config written to ~/.querynl/config.yaml, credentials in keychain, then test/list/use/remove

**Why First**: Connection management is prerequisite for all other features (queries, schema, migrations)

### Implementation for User Story 2

- [X] T017 [P] [US2] Create ConnectionProfile model in src/cli/models.py (data class from data-model.md with validation)
- [X] T018 [P] [US2] Create SSHTunnel model in src/cli/models.py (nested in ConnectionProfile)
- [X] T019 [US2] Implement `querynl connect add <name>` command in src/cli/commands/connect.py (interactive prompts for host/port/database/username/password)
- [X] T020 [US2] Add database type detection in connect add (prompt for postgresql/mysql/sqlite/mongodb)
- [X] T021 [US2] Implement password prompt with hidden input in connect add (getpass or Click.prompt with hide_input=True)
- [X] T022 [US2] Store ConnectionProfile in config.yaml (without password) in connect add
- [X] T023 [US2] Store password in system keychain in connect add (keyring.set_password)
- [X] T024 [US2] Implement connection test after add (attempt connection, report success/failure with latency)
- [X] T025 [US2] Set as default_connection if first connection added
- [X] T026 [P] [US2] Implement `querynl connect list` command in src/cli/commands/connect.py (Rich table with name, type, host, port, status - NO credentials)
- [X] T027 [P] [US2] Implement `querynl connect test <name>` command in src/cli/commands/connect.py (verify connectivity, show latency, report detailed errors)
- [X] T028 [P] [US2] Implement `querynl connect use <name>` command in src/cli/commands/connect.py (set as default_connection in config)
- [X] T029 [P] [US2] Implement `querynl connect remove <name>` command in src/cli/commands/connect.py (delete from config + keychain, require --confirm flag)
- [X] T030 [US2] Add environment variable support in src/cli/credentials.py (read QUERYNL_CONNECTION_STRING for CI/CD, parse connection string format)
- [X] T031 [US2] Wire all connect commands to main.py command group (@cli.group('connect'))
- [X] T032 [US2] Add SSL validation toggle (--no-ssl flag, default ssl_enabled=True)
- [X] T033 [US2] Add SSH tunnel support in connect add (optional prompts for ssh_host, ssh_username, ssh_key_path)

**Checkpoint US2**: User can manage connections end-to-end (add/list/test/use/remove), credentials stored securely, environment variables work for automation

---

## Phase 4: User Story 1 - Interactive Natural Language Queries (Priority: P1) 🎯 MVP

**Goal**: Users can execute natural language queries and see formatted results

**Independent Test**: Run `querynl query "count all users"`, verify SQL displayed, confirmation prompted if destructive, results shown in table format

**Why Second**: Core value proposition - natural language queries. Depends on connection management (US2).

### Implementation for User Story 1

- [X] T034 [P] [US1] Create QueryHistory model in src/cli/models.py (data class from data-model.md)
- [X] T035 [P] [US1] Create SQLite schema in src/cli/history.py (query_history table with indexes from data-model.md)
- [X] T036 [P] [US1] Implement history database initialization in src/cli/history.py (create ~/.querynl/history.db on first run)
- [X] T037 [P] [US1] Implement query history storage functions in src/cli/history.py (insert_query, get_session_history, prune_old_entries)
- [X] T038 [US1] Implement table formatter in src/cli/formatting/table.py (Rich table with column alignment, borders, auto-width)
- [X] T039 [US1] Create `querynl query "<natural language>"` command in src/cli/commands/query.py (parse NL input, call LLM service)
- [X] T040 [US1] Integrate LLM query generation service from src/services/ in query command (reuse existing backend service)
- [X] T041 [US1] Display generated SQL to user before execution in query command (Rich syntax highlighting for SQL)
- [X] T042 [US1] Implement destructive operation detection in query command (regex for DELETE, DROP, TRUNCATE, ALTER)
- [X] T043 [US1] Add confirmation prompt for destructive operations in query command (Click.confirm with default=False)
- [X] T044 [US1] Execute SQL query against active connection in query command (use database driver from src/lib/)
- [X] T045 [US1] Format and display results using table formatter in query command
- [X] T046 [US1] Save query to history database after execution (including execution_time_ms, row_count, error if failed)
- [X] T047 [US1] Add --non-interactive flag to query command (skip confirmations, for automation)
- [X] T048 [US1] Add --timeout flag to query command (set query timeout in seconds, default 60)
- [X] T049 [US1] Add --limit flag to query command (limit result rows, default 1000)
- [X] T050 [US1] Add --connection flag to query command (override default connection)
- [X] T051 [US1] Implement Ctrl+C handling in query command (gracefully cancel query, cleanup connection)
- [X] T052 [US1] Add ambiguous query handling (if LLM returns multiple interpretations, prompt user to choose)
- [X] T053 [US1] Wire query command to main.py (@cli.command('query'))

**Checkpoint US1**: User can execute natural language queries end-to-end, see SQL before execution, confirm destructive operations, view results in tables

---

## Phase 5: User Story 7 - Interactive REPL Mode (Priority: P2)

**Goal**: Users can enter interactive mode with persistent context and enhanced UX

**Independent Test**: Run `querynl repl`, execute multiple related queries, verify conversation context maintained, history accessible with up arrow

**Why Third**: REPL enhances query UX significantly but depends on basic query functionality (US1) and connections (US2).

### Implementation for User Story 7

- [X] T054 [P] [US7] Create REPLSession model in src/cli/models.py (session_id, conversation_context, connection_name)
- [X] T055 [P] [US7] Implement REPL session manager in src/cli/repl.py (create session, track context, cleanup on exit)
- [X] T056 [US7] Create `querynl repl` command in src/cli/commands/query.py (initialize prompt_toolkit session)
- [X] T057 [US7] Integrate prompt_toolkit for REPL input in repl command (PromptSession with multiline support)
- [X] T058 [US7] Add command history to REPL (prompt_toolkit FileHistory stored in ~/.querynl/repl_history)
- [X] T059 [US7] Implement tab completion in REPL (CompleteStyle.READLINE, complete table names from schema cache)
- [X] T060 [US7] Add REPL-specific commands in src/cli/repl.py (\help, \connect, \tables, \schema, \history, \exit)
- [X] T061 [US7] Implement \help command (list available REPL commands and shortcuts)
- [X] T062 [US7] Implement \connect <name> command (switch active connection within REPL)
- [X] T063 [US7] Implement \tables command (list tables in current database)
- [X] T064 [US7] Implement \schema <table> command (show table schema with columns/types)
- [X] T065 [US7] Implement \history command (show recent queries from current session)
- [X] T066 [US7] Implement \exit command (gracefully exit REPL, save session)
- [X] T067 [US7] Add multi-line input support (detect unclosed quotes/parentheses, continue prompt on next line)
- [X] T068 [US7] Implement conversation context persistence (append user/assistant messages to REPLSession.conversation_context)
- [X] T069 [US7] Pass conversation context to LLM for follow-up queries (enables "show me the first 10" after initial query)
- [X] T070 [US7] Cache last query results in REPLSession.last_result_rows (for reference by LLM in context)
- [X] T071 [US7] Add REPL welcome message (display version, active connection, \help hint)
- [X] T072 [US7] Wire repl command to main.py (@cli.command('repl'))

**Checkpoint US7**: REPL mode functional with history, tab completion, conversation context, and backslash commands

---

## Phase 6: User Story 6 - Output Format Flexibility (Priority: P3)

**Goal**: Users can output results in JSON/CSV/markdown formats in addition to tables

**Independent Test**: Run same query with --format json, --format csv, --format markdown, verify output correctness

**Why Fourth**: Enhances usability but not critical for MVP. Depends on query execution (US1).

### Implementation for User Story 6

- [X] T073 [P] [US6] Implement JSON formatter in src/cli/formatting/json_formatter.py (output array of objects, comply with contracts/output-formats.json schema)
- [X] T074 [P] [US6] Implement CSV formatter in src/cli/formatting/csv_formatter.py (RFC 4180 compliant, proper escaping, headers)
- [X] T075 [P] [US6] Implement markdown formatter in src/cli/formatting/markdown_formatter.py (GitHub-flavored markdown tables with alignment)
- [X] T076 [US6] Add --format flag to query command (choices: table, json, csv, markdown, default: table)
- [X] T077 [US6] Add format dispatcher in query command (select formatter based on --format flag)
- [X] T078 [US6] Add --output flag to query command (write results to file instead of stdout)
- [X] T079 [US6] Implement file write with atomic operation in query command (write to temp file, rename on success)
- [X] T080 [US6] Add format validation in query command (ensure chosen format compatible with query results)
- [X] T081 [US6] Handle large result sets efficiently (stream to file for JSON/CSV, paginate for table/markdown)

**Checkpoint US6**: Multiple output formats working, file output functional, large results handled efficiently

---

## Phase 7: User Story 3 - Schema Design from CLI (Priority: P2)

**Goal**: Users can design schemas from natural language descriptions and export to files

**Independent Test**: Run `querynl schema design "e-commerce with users, products, orders"`, verify JSON output with normalized schema

**Why Fifth**: Valuable for project initialization but less frequently used than queries. Depends on connections (US2).

### Implementation for User Story 3

- [X] T082 [P] [US3] Create SchemaDesign model in src/cli/models.py (tables, relationships, version from data-model.md)
- [X] T083 [P] [US3] Create TableDesign model in src/cli/models.py (name, columns, indexes, constraints)
- [X] T084 [P] [US3] Create ColumnDefinition model in src/cli/models.py (name, type, nullable, primary_key, unique)
- [X] T085 [P] [US3] Create Relationship model in src/cli/models.py (from_table/column, to_table/column, on_delete/update)
- [X] T086 [US3] Create `querynl schema design "<description>"` command in src/cli/commands/schema.py (call LLM for schema generation)
- [X] T087 [US3] Integrate schema design service from src/services/ (reuse existing backend schema generation)
- [X] T088 [US3] Display generated schema summary in schema design command (table names, relationship count, validation results)
- [X] T089 [US3] Save schema to JSON file in schema design command (default: ./schema-{timestamp}.json, or --output flag)
- [X] T090 [US3] Implement schema JSON serialization (convert SchemaDesign to JSON matching data-model.md format)
- [X] T091 [US3] Create `querynl schema visualize <schema-file>` command in src/cli/commands/schema.py (generate Mermaid ER diagram)
- [X] T092 [US3] Implement Mermaid ER diagram generation in schema visualize (erDiagram syntax with relationships)
- [X] T093 [US3] Add --output flag to schema visualize (save to markdown file, default: stdout)
- [X] T094 [US3] Create `querynl schema analyze <schema-file>` command in src/cli/commands/schema.py (detect design issues)
- [X] T095 [US3] Implement schema analysis checks in schema analyze (missing indexes, normalization issues, naming conventions)
- [X] T096 [US3] Display analysis results with suggestions in schema analyze (Rich panel with warnings/errors/suggestions)
- [X] T097 [US3] Create `querynl schema modify <schema-file> "<description>"` command in src/cli/commands/schema.py (update existing schema)
- [X] T098 [US3] Implement schema modification logic in schema modify (load existing, merge LLM changes, increment version)
- [X] T099 [US3] Create `querynl schema apply <schema-file>` command in src/cli/commands/schema.py (generate CREATE TABLE statements)
- [X] T100 [US3] Implement SQL generation from schema in schema apply (database-specific CREATE TABLE syntax)
- [X] T101 [US3] Add --execute flag to schema apply (optionally run generated SQL on connection)
- [X] T102 [US3] Add confirmation prompt in schema apply --execute (show SQL, require confirmation)
- [X] T103 [US3] Wire all schema commands to main.py command group (@cli.group('schema'))

**Checkpoint US3**: Schema design workflow complete, generate/visualize/analyze/modify/apply all functional

---

## Phase 8: User Story 4 - Migration Generation (Priority: P2)

**Goal**: Users can generate migration files from schema changes with framework support

**Independent Test**: Create two schema versions, run `querynl migrate generate`, verify up/down SQL files created

**Why Sixth**: Essential for production schema evolution but depends on schema design (US3).

### Implementation for User Story 4

- [X] T104 [P] [US4] Create MigrationRecord model in src/cli/models.py (migration_id, status, sql_content, rollback_sql from data-model.md)
- [X] T105 [P] [US4] Create migration tracking database in src/cli/migrations.py (SQLite or target database table)
- [X] T106 [US4] Create `querynl migrate generate` command in src/cli/commands/migrate.py (diff schemas, generate SQL)
- [X] T107 [US4] Add --from flag to migrate generate (source schema file)
- [X] T108 [US4] Add --to flag to migrate generate (target schema file)
- [X] T109 [US4] Add --framework flag to migrate generate (choices: alembic, flyway, raw, default: raw)
- [X] T110 [US4] Add --message flag to migrate generate (migration description)
- [X] T111 [US4] Implement schema diffing logic in migrate generate (detect added/removed/modified tables/columns)
- [X] T112 [US4] Generate up migration SQL (CREATE TABLE, ALTER TABLE, CREATE INDEX statements)
- [X] T113 [US4] Generate down migration SQL (DROP TABLE, DROP INDEX, ALTER TABLE REVERT statements)
- [X] T114 [US4] Format migrations for Alembic framework (Python revision files with upgrade/downgrade functions)
- [X] T115 [US4] Format migrations for Flyway framework (versioned SQL files V{version}__{description}.sql)
- [X] T116 [US4] Format migrations as raw SQL (separate up.sql and down.sql files)
- [X] T117 [US4] Add timestamp-based versioning to generated migrations (YYYYMMDDHHmmss format)
- [X] T118 [US4] Save migration files to project directory (default: ./migrations/, or --output flag)
- [X] T119 [US4] Create `querynl migrate preview <migration-file>` command in src/cli/commands/migrate.py (display SQL with explanation)
- [X] T120 [US4] Implement migration explanation in migrate preview (parse SQL, describe changes in plain English)
- [X] T121 [US4] Create `querynl migrate apply` command in src/cli/commands/migrate.py (apply pending migrations to connection)
- [X] T122 [US4] Implement transaction-wrapped migration application in migrate apply (BEGIN, execute, COMMIT or ROLLBACK on error)
- [X] T123 [US4] Record successful migrations in tracking database in migrate apply (update MigrationRecord status)
- [X] T124 [US4] Add --dry-run flag to migrate apply (show SQL without executing)
- [X] T125 [US4] Create `querynl migrate status` command in src/cli/commands/migrate.py (list applied/pending/failed migrations)
- [X] T126 [US4] Display migration status as Rich table in migrate status (version, description, status, applied_at)
- [X] T127 [US4] Create `querynl migrate rollback` command in src/cli/commands/migrate.py (rollback last migration using down script)
- [X] T128 [US4] Implement rollback logic in migrate rollback (execute down SQL, update tracking database)
- [X] T129 [US4] Add --steps flag to migrate rollback (rollback N migrations, default: 1)
- [X] T130 [US4] Add confirmation prompt to migrate apply and rollback (show affected migrations, require --confirm)
- [X] T131 [US4] Wire all migrate commands to main.py command group (@cli.group('migrate'))

**Checkpoint US4**: Migration workflow complete, generate/preview/apply/status/rollback all functional, framework support working

---

## Phase 9: User Story 5 - Scriptable Commands for Automation (Priority: P2)

**Goal**: CLI works correctly in CI/CD with proper exit codes and JSON output

**Independent Test**: Write shell script using querynl commands, verify exit codes, stderr/stdout separation, non-TTY compatibility

**Why Seventh**: Enables automation but depends on core query/schema/migration features being stable.

### Implementation for User Story 5

- [X] T132 [P] [US5] Define exit code constants in src/cli/errors.py (0=success, 1=general error, 2=invalid args, 3=connection error, 4=query error, 5=config error)
- [X] T133 [P] [US5] Implement exit code mapping in main.py (catch exception types, map to appropriate exit codes)
- [X] T134 [P] [US5] Ensure all error messages go to stderr (use Click.echo with err=True)
- [X] T135 [P] [US5] Ensure all normal output goes to stdout (use Click.echo without err parameter)
- [X] T136 [US5] Test CLI in non-TTY environment (Docker container without terminal)
- [X] T137 [US5] Add TTY detection in formatting modules (disable colors/formatting if not TTY)
- [X] T138 [US5] Test --non-interactive flag in automation scenarios (verify no prompts, exits with error if input needed)
- [X] T139 [US5] Validate JSON output is parseable by jq (run `querynl query ... --format json | jq .`)
- [X] T140 [US5] Validate JSON output is parseable by Python json module (run in test script)
- [X] T141 [US5] Test environment variable configuration in CI/CD (QUERYNL_CONNECTION_STRING, QUERYNL_LLM_API_KEY)
- [X] T142 [US5] Add --quiet flag to all commands (suppress all non-essential output, errors still to stderr)
- [X] T143 [US5] Document exit codes in help text and quickstart.md

**Checkpoint US5**: Automation-friendly CLI verified, exit codes correct, stderr/stdout separation working, non-TTY compatible, JSON parseable

---

## Phase 10: User Story 8 - Configuration Management (Priority: P3)

**Goal**: Users can manage CLI configuration via commands instead of editing YAML manually

**Independent Test**: Run `querynl config set default_format json`, verify config.yaml updated, `querynl config get default_format` returns json

**Why Eighth**: Nice-to-have for power users but not essential. Depends on config system (Foundation).

### Implementation for User Story 8

- [X] T144 [P] [US8] Create `querynl config show` command in src/cli/commands/config.py (display current configuration as YAML)
- [X] T145 [P] [US8] Create `querynl config get <key>` command in src/cli/commands/config.py (retrieve single config value)
- [X] T146 [P] [US8] Create `querynl config set <key> <value>` command in src/cli/commands/config.py (update config value with validation)
- [X] T147 [P] [US8] Create `querynl config reset` command in src/cli/commands/config.py (restore default configuration)
- [X] T148 [US8] Implement config key validation in config set (check valid keys, types, enum values)
- [X] T149 [US8] Display actionable error messages for invalid config in config set (show valid options, examples)
- [X] T150 [US8] Add --confirm flag to config reset (prevent accidental reset)
- [X] T151 [US8] Add tab completion for config keys in config get/set (complete from CLIConfiguration fields)
- [X] T152 [US8] Wire all config commands to main.py command group (@cli.group('config'))

**Checkpoint US8**: Config management complete, get/set/show/reset all working, validation provides clear errors

---

## Phase 11: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final production readiness

### Constitution Compliance Tasks

- [X] T153 [P] [Constitution] Security audit: Verify credential encryption (test keyring storage, no plain text in config)
- [X] T154 [P] [Constitution] Security audit: Verify no credentials in logs/errors (grep codebase for password logging)
- [X] T155 [P] [Constitution] Security audit: SQL injection prevention testing (test with malicious inputs)
- [X] T156 [Constitution] UX validation: First query within 3 minutes test (install CLI, add connection, execute query, time it)
- [X] T157 [Constitution] Transparency: Verify SQL displayed before execution (test all query commands)
- [X] T158 [Constitution] Multi-DB testing: Test with PostgreSQL, MySQL, SQLite, MongoDB (create test matrix)
- [X] T159 [Constitution] Fail-safe: Verify destructive operations require confirmation (test DELETE/DROP/TRUNCATE)
- [X] T160 [Constitution] Fail-safe: Verify rollback migrations generated by default (test migrate generate)

### General Quality Tasks

- [X] T161 [P] [Polish] Add --help text to all commands (docstrings converted to help, examples in extended help)
- [X] T162 [P] [Polish] Add --version command to main CLI (display QueryNL version, Python version, platform)
- [X] T163 [P] [Polish] Implement --verbose logging flag in main.py (debug logging to ~/.querynl/debug.log)
- [X] T164 [P] [Polish] Implement --quiet flag in main.py (suppress all non-essential output)
- [X] T165 [P] [Polish] Add Rich console styling to all output (consistent color scheme, panels for important info)
- [X] T166 [Polish] Optimize startup time (lazy import heavy dependencies, profile with cProfile)
- [X] T167 [Polish] Profile memory usage during query execution (ensure <100MB for typical queries)
- [X] T168 [Polish] Implement result streaming for large queries (avoid loading entire result set into memory)
- [X] T169 [Polish] Configure PyInstaller for binary distribution in pyinstaller.spec (single file, optimized size)
- [X] T170 [Polish] Optimize PyInstaller binary size (exclude unnecessary modules, use UPX compression, target <50MB)
- [X] T171 [Polish] Test binary on macOS Intel and Apple Silicon (ensure both architectures work)
- [X] T172 [Polish] Test binary on Linux (Ubuntu 20.04, Debian, RHEL/CentOS with different glibc versions)
- [X] T173 [Polish] Test binary on Windows 10 and 11 (ensure Windows Credential Manager works)
- [X] T174 [Polish] Add platform-specific keyring fallback messaging (guide users to install keyrings.cryptfile if needed)
- [X] T175 [Polish] Handle terminal resize during output (re-render table on SIGWINCH)
- [X] T176 [Polish] Implement query result pagination (auto-invoke pager for large result sets)
- [X] T177 [Polish] Add color scheme detection (respect terminal light/dark mode)
- [X] T178 [Polish] Update CLAUDE.md with CLI-specific commands (pytest tests/cli, querynl commands)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 2 (Phase 3)**: Depends on Foundational phase - MUST complete first (connections required for all other features)
- **User Story 1 (Phase 4)**: Depends on US2 (connections) - Core query functionality
- **User Story 7 (Phase 5)**: Depends on US1 (query) and US2 (connections) - Enhanced REPL mode
- **User Story 6 (Phase 6)**: Depends on US1 (query) - Output format flexibility
- **User Story 3 (Phase 7)**: Depends on US2 (connections) - Schema design (independent of query)
- **User Story 4 (Phase 8)**: Depends on US3 (schema) - Migration generation
- **User Story 5 (Phase 9)**: Depends on US1, US3, US4 being stable - Automation testing
- **User Story 8 (Phase 10)**: Depends only on Foundational phase - Config management (independent)
- **Polish (Phase 11)**: Depends on all desired user stories being complete

### User Story Dependencies

```
Foundation (T009-T016) → BLOCKS ALL USER STORIES
    ↓
US2: Connection Management (T017-T033) → BLOCKS US1, US7, US3
    ↓
    ├→ US1: Query Execution (T034-T053) → BLOCKS US7, US6
    │   ├→ US7: REPL Mode (T054-T072)
    │   └→ US6: Output Formats (T073-T081)
    │
    └→ US3: Schema Design (T082-T103) → BLOCKS US4
        └→ US4: Migrations (T104-T131)

US8: Config Management (T144-T152) - Independent, only depends on Foundation
US5: Automation (T132-T143) - Cross-cutting, test after US1, US3, US4 stable
```

### Critical Path (MVP - US1 + US2 only)

1. Phase 1: Setup (T001-T008) - 8 tasks
2. Phase 2: Foundation (T009-T016) - 8 tasks
3. Phase 3: US2 Connections (T017-T033) - 17 tasks
4. Phase 4: US1 Queries (T034-T053) - 20 tasks

**Total for MVP**: 53 tasks

### Parallel Opportunities

**Within Setup (Phase 1)**:
- T003, T004, T005 can run in parallel (different __init__.py files)

**Within Foundation (Phase 2)**:
- T009, T010, T011 can run in parallel after setup (config system)
- T012, T013 can run in parallel after setup (credentials system)
- T014, T015 can run in parallel after setup (error/logging)

**Within US2 (Phase 3)**:
- T017, T018 can run in parallel (model classes)
- T026, T027, T028, T029 can run in parallel after T019-T025 (list/test/use/remove commands)

**Within US1 (Phase 4)**:
- T034, T035, T036, T037 can run in parallel (history system)
- After query command created (T039), many flags can be added in parallel: T047, T048, T049, T050

**Within US7 (Phase 5)**:
- T054, T055 can run in parallel (REPL session)
- T061-T066 can run in parallel after T060 (individual backslash commands)

**Within US6 (Phase 6)**:
- T073, T074, T075 can run in parallel (independent formatters)

**Within US3 (Phase 7)**:
- T082, T083, T084, T085 can run in parallel (model classes)

**Within US4 (Phase 8)**:
- T104, T105 can run in parallel (migration models and tracking)

**Within US5 (Phase 9)**:
- T132, T133, T134, T135 can run in parallel (exit codes and stdout/stderr)

**Within US8 (Phase 10)**:
- T144, T145, T146, T147 can run in parallel (independent config commands)

**Within Polish (Phase 11)**:
- T153, T154, T155 can run in parallel (security audits)
- T161, T162, T163, T164, T165 can run in parallel (help/version/logging/quiet/styling)
- T171, T172, T173 can run in parallel (platform testing)

---

## Parallel Example: Foundation Phase

```bash
# Launch all foundation tasks in parallel (after Phase 1 complete):

# Config system (3 tasks in parallel):
Task: "Create platform-specific config path resolver in src/cli/config.py"
Task: "Implement config file loader/saver in src/cli/config.py"
Task: "Create CLIConfiguration model class in src/cli/config.py"

# Credentials system (2 tasks in parallel):
Task: "Implement keyring credential storage wrapper in src/cli/credentials.py"
Task: "Add keyrings.cryptfile fallback in src/cli/credentials.py"

# Error handling and logging (2 tasks in parallel):
Task: "Create error handling framework in src/cli/errors.py"
Task: "Create logging configuration in src/cli/logging.py"

# Then (sequential - depends on above):
Task: "Integrate existing database drivers from src/lib/ into CLI context"
```

---

## Implementation Strategy

### MVP First (US2 + US1 Only)

1. Complete Phase 1: Setup (T001-T008)
2. Complete Phase 2: Foundational (T009-T016) - CRITICAL - blocks all stories
3. Complete Phase 3: US2 Connection Management (T017-T033)
4. Complete Phase 4: US1 Query Execution (T034-T053)
5. **STOP and VALIDATE**: Test connections + queries independently
6. Run constitution compliance checks (T153-T160)
7. Deploy/demo MVP

**MVP Milestone**: Users can manage connections and execute natural language queries from CLI

### Incremental Delivery (After MVP)

1. MVP (US2 + US1) → Test independently → Deploy/Demo
2. Add Phase 5: US7 REPL Mode (T054-T072) → Test independently → Deploy/Demo
3. Add Phase 7: US3 Schema Design (T082-T103) → Test independently → Deploy/Demo
4. Add Phase 8: US4 Migrations (T104-T131) → Test independently → Deploy/Demo
5. Add Phase 6: US6 Output Formats (T073-T081) → Test independently → Deploy/Demo
6. Add Phase 10: US8 Config Management (T144-T152) → Test independently → Deploy/Demo
7. Complete Phase 9: US5 Automation Testing (T132-T143)
8. Complete Phase 11: Polish (T153-T178)

### Parallel Team Strategy

With multiple developers after Foundation phase completes:

**Developer A**: US2 Connection Management (T017-T033)
**Developer B**: US1 Query Execution (T034-T053) - Can start models/history in parallel with US2
**Developer C**: US8 Config Management (T144-T152) - Independent, only needs Foundation

After US2 completes:
**Developer A**: US7 REPL Mode (T054-T072)
**Developer B**: US3 Schema Design (T082-T103)

After US3 completes:
**Developer A or B**: US4 Migrations (T104-T131)

After US1 completes:
**Any Developer**: US6 Output Formats (T073-T081)

---

## Notes

- **[P] tasks**: Different files, no dependencies, can run in parallel
- **[Story] label**: Maps task to specific user story for traceability
- **File paths**: All tasks include exact file paths for implementation
- **Each user story**: Independently completable and testable
- **Commit strategy**: Commit after each task or logical group
- **Checkpoints**: Stop at any checkpoint to validate story independently
- **No tests**: Tests are optional per spec.md, not included in this task list
- **Constitution**: All security, transparency, fail-safe principles must be verified in Phase 11
- **Avoid**: Vague tasks, same file conflicts, cross-story dependencies that break independence

---

**Task List Complete**: 178 tasks across 11 phases
**Estimated MVP**: 53 tasks (Phases 1-4)
**Constitution Compliance**: 8 dedicated verification tasks (T153-T160)
**Parallel Execution**: ~40% of tasks marked [P] for parallel execution
**Ready for**: Implementation via /speckit.implement command
