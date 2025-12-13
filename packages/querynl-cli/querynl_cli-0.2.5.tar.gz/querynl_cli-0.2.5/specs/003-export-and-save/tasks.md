# Tasks: Export and Save Query Results

**Input**: Design documents from `/specs/003-export-and-save/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/export_api.md, quickstart.md

**Tests**: Tests are NOT explicitly requested in the specification. Focus on implementation with manual testing via quickstart.md examples.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

**Constitution Compliance**: All tasks must align with [QueryNL Constitution v1.0.0](../../.specify/memory/constitution.md). Security-first design, transparency, and fail-safe defaults are non-negotiable.

## Format: `[ID] [P?] [Story] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions
- Single project structure: `src/cli/`, `tests/` at repository root
- Paths are relative to `/Users/marcus/Developer/QueryNLAgent/QueryNL/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create export module structure and base utilities

- [x] T001 [P] [SETUP] Create export module directory structure: `src/cli/export/__init__.py`
- [x] T002 [P] [SETUP] Create file utilities module: `src/cli/export/file_utils.py` with path validation and mkdir -p functions
- [x] T003 [P] [SETUP] Create export configuration dataclass in `src/cli/export/__init__.py` (ExportConfiguration, ExportResult, ExportFormat enum)
- [x] T004 [P] [SETUP] Create base format writer interface in `src/cli/export/streaming.py` (FormatWriter abstract base class)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core export infrastructure that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 [FOUNDATION] Implement path validation in `src/cli/export/file_utils.py`:
  - `validate_export_path()` function
  - Check for path traversal (../, ..\)
  - Verify parent directory writable
  - OS-specific invalid character checks (Windows: `<>:"|?*`)
  - Path length validation (Windows 260 char limit)

- [x] T006 [FOUNDATION] Implement auto-rename with timestamp in `src/cli/export/file_utils.py`:
  - `resolve_file_conflict()` function
  - Check if file exists
  - Generate timestamp suffix (YYYYMMDD_HHMMSS format)
  - Insert before file extension (e.g., `file_20251025_143000.csv`)
  - Return actual path used

- [x] T007 [FOUNDATION] Implement directory creation in `src/cli/export/file_utils.py`:
  - `ensure_parent_directories()` function
  - Use `pathlib.Path.mkdir(parents=True, exist_ok=True)`
  - Handle permission errors with clear messages

- [x] T008 [FOUNDATION] Implement format detection in `src/cli/export/exporter.py`:
  - `detect_format()` function
  - Map file extensions (.csv, .json, .sql, .mmd, .txt) to ExportFormat enum
  - Raise UnsupportedFormatError for unknown extensions

- [x] T009 [FOUNDATION] Create custom exception hierarchy in `src/cli/export/__init__.py`:
  - `ExportError` base class
  - `FilePermissionError`, `DiskFullError`, `InvalidPathError`, `UnsupportedFormatError`, `StreamingError`
  - Each with user-friendly error messages and actionable suggestions

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Basic CSV Export in CLI Mode (Priority: P1) 🎯 MVP

**Goal**: Enable users to export query results to CSV files from the command line with automatic format detection, file conflict handling, and proper CSV escaping.

**Independent Test**: Run `querynl query "SELECT * FROM users" --export users.csv` and verify valid CSV file created with headers and data, can be opened in Excel/Google Sheets.

### Implementation for User Story 1

- [x] T010 [P] [US1] Extend existing CSV formatter in `src/cli/formatting/csv_formatter.py`:
  - Add `export_csv_to_file()` function that uses existing `format_csv()`
  - Implement streaming CSV writer for large datasets (write row-by-row)
  - Handle NULL values → empty string
  - Ensure RFC 4180 compliance (existing formatter already does this)
  - Use UTF-8-sig encoding for Excel compatibility

- [x] T011 [US1] Implement core export service in `src/cli/export/exporter.py`:
  - `export_to_file()` main function
  - Validate file path (call `validate_export_path()` from T005)
  - Detect format (call `detect_format()` from T008)
  - Resolve conflicts (call `resolve_file_conflict()` from T006)
  - Create directories (call `ensure_parent_directories()` from T007)
  - Delegate to format-specific writers
  - Return ExportResult with success status, actual path, row count

- [x] T012 [US1] Implement streaming export coordinator in `src/cli/export/streaming.py`:
  - `StreamingExporter` class
  - Choose streaming vs in-memory based on row count (<10,000 = in-memory, ≥10,000 = streaming)
  - Progress callback support (call every 10,000 rows)
  - Use Rich progress bars for visual feedback
  - Memory-efficient row-by-row writing

- [x] T013 [US1] Add --export flag to query command in `src/cli/commands/query.py`:
  - Add `@click.option("--export", "-e", type=click.Path())`
  - Add `@click.option("--format", "-f", type=click.Choice(["csv", "json", "sql"]))`
  - After query execution and result display, check if export flag provided
  - Call `export_to_file()` from T011
  - Display success message with file path and row count
  - Display renamed filename message if conflict occurred

- [x] T014 [US1] Add user-friendly error handling in `src/cli/commands/query.py`:
  - Catch ExportError exceptions
  - Display actionable error messages (from T009)
  - Examples: "Permission denied: Check directory permissions", "Disk full: Free up space"

**Checkpoint**: User Story 1 complete - users can export query results to CSV from CLI. Test independently per quickstart.md examples 1.1-1.5.

---

## Phase 4: User Story 2 - Export in REPL Mode (Priority: P2)

**Goal**: Enable users to export their most recent query result from REPL mode without leaving the interactive session using `\export <filepath>` command.

**Independent Test**: Start REPL, run a query, execute `\export results.csv`, verify last query results saved to file. Run another query, export again, verify only the new query results exported (not cumulative).

### Implementation for User Story 2

- [x] T015 [US2] Add last result caching to REPL session in `src/cli/repl.py`:
  - Add `self.last_result: Optional[Dict[str, Any]] = None` attribute to REPLSession class
  - Update query execution methods to cache result data after each query
  - Include query metadata (database_type, timestamp, command_type)
  - Cap cache at 100MB to prevent memory issues (check result size)

- [x] T016 [US2] Implement `\export` REPL command in `src/cli/repl.py`:
  - Add `_cmd_export(self, filepath: str)` method
  - Check if `self.last_result` exists, show error if no previous query
  - Parse filepath argument, show usage if missing
  - Call `export_to_file()` with cached result data
  - Display success message with row count and file path
  - Show renamed filename message if conflict occurred
  - Handle export errors with user-friendly messages

- [x] T017 [US2] Update REPL command parser in `src/cli/repl.py`:
  - Add `"\\export"` to repl_commands list for tab completion
  - Add elif branch for `cmd == "\\export"` in `handle_command()`
  - Call `_cmd_export(args)` with filename argument

- [x] T018 [US2] Update REPL help command in `src/cli/repl.py`:
  - Add row to help table: `\\export <filepath>` - Export most recent query result to file
  - Add tip about format auto-detection from file extension
  - Update welcome message with `\\export` command

**Checkpoint**: User Story 2 complete - users can export from REPL mode. Test independently per quickstart.md examples 2.1-2.4.

---

## Phase 5: User Story 3 - Multiple Format Support (Priority: P3)

**Goal**: Enable users to export results in JSON, SQL INSERT, and Mermaid diagram formats in addition to CSV, with automatic format detection from file extensions.

**Independent Test**: Export same query to `.csv`, `.json`, `.sql`, and export schema to `.mmd`. Verify each format is valid (CSV opens in Excel, JSON parses, SQL executes, Mermaid renders on GitHub).

### Implementation for User Story 3

- [x] T019 [P] [US3] Extend JSON formatter in `src/cli/formatting/json_formatter.py`:
  - Add `export_json_to_file()` function
  - Implement streaming JSON array writer (write opening `[`, then rows with commas, then closing `]`)
  - Create custom JSON encoder for datetime → ISO 8601, Decimal → float, bytes → base64
  - Handle NULL → `null`, bool → `true`/`false`
  - Optional pretty-print parameter (default: False for streaming efficiency)

- [x] T020 [P] [US3] Create SQL formatter in `src/cli/formatting/sql_formatter.py`:
  - Implement `SQLWriter` class extending `FormatWriter` base
  - Database-specific escaping for PostgreSQL, MySQL, SQLite
  - Generate INSERT statements with batch size (default 1000 rows per INSERT)
  - Write header comments (table name, database type, timestamp, row count)
  - Escape single quotes (PostgreSQL/SQLite: `''`, MySQL: `\'`)
  - Handle NULL values, boolean values per database type
  - MongoDB: Show error message suggesting JSON format instead

- [x] T021 [P] [US3] Create Mermaid formatter in `src/cli/formatting/mermaid_formatter.py`:
  - Implement `MermaidWriter` class for ER diagrams
  - Generate `erDiagram` syntax
  - Map database types to Mermaid types (varchar, int, timestamp, boolean, json)
  - Mark primary keys (PK), foreign keys (FK)
  - Generate relationship notation (`||--o{` = one-to-many, `||--||` = one-to-one, `}o--o{` = many-to-many)
  - Detect relationships from foreign key naming conventions (column ending in `_id`)
  - Work with schema introspection data from existing `schema_introspection.py`

- [x] T022 [US3] Create plain text formatter in `src/cli/formatting/__init__.py`:
  - Simple text export for non-tabular outputs (schema lists, help text, etc.)
  - Preserve formatting from Rich console output
  - Use for `\tables`, `\help`, and other meta-commands

- [x] T023 [US3] Update format detection in `src/cli/export/exporter.py`:
  - Add `.json` → ExportFormat.JSON mapping
  - Add `.sql` → ExportFormat.SQL mapping
  - Add `.mmd` → ExportFormat.MERMAID mapping
  - Add `.txt` → ExportFormat.TXT mapping

- [x] T024 [US3] Update main exporter to route to format writers in `src/cli/export/exporter.py`:
  - In `export_to_file()`, add switch/match on format type
  - Route CSV → csv_formatter.export_csv_to_file()
  - Route JSON → json_formatter.export_json_to_file()
  - Route SQL → sql_formatter.SQLWriter
  - Route MERMAID → mermaid_formatter.MermaidWriter
  - Route TXT → plain text formatter
  - Pass database_type for SQL format generation

- [x] T025 [US3] Add format override support in `src/cli/commands/query.py`:
  - Allow `--format` flag to override file extension
  - Show warning if format conflicts with extension (e.g., `--format json --export data.csv`)
  - Pass explicit format to `export_to_file()` if provided

- [x] T026 [US3] Enable schema export to Mermaid in `src/cli/commands/schema.py`:
  - After displaying schema graph, check if export path provided
  - Generate Mermaid diagram from schema_data and relationships
  - Call mermaid_formatter to write .mmd file
  - Integrate with REPL `\export` after `\schema graph` command

**Checkpoint**: User Story 3 complete - users can export to JSON, SQL, Mermaid, and TXT formats. Test independently per quickstart.md examples 3.1-3.5.

---

## Phase 6: User Story 4 - Auto-Export Mode (Priority: P4)

**Goal**: Allow users to configure automatic export of all query results to a default directory with timestamp-based filenames, enabling scheduled data extraction workflows.

**Independent Test**: Enable auto-export in config, run multiple queries, verify all results automatically saved to `~/.querynl/exports/YYYY-MM-DD/` with timestamp filenames. Use `--no-export` flag to skip one query.

### Implementation for User Story 4

- [ ] T027 [P] [US4] [SKIPPED] Add auto-export configuration to config schema in `src/cli/config.py`:
  - Add `auto_export` section to config YAML schema
  - Fields: `enabled` (bool, default False), `output_directory` (str), `filename_template` (str with `{timestamp}` placeholder), `default_format` (str), `create_subdirectories_by_date` (bool)
  - Validation: ensure `filename_template` contains `{timestamp}`, `default_format` is valid ExportFormat

- [ ] T028 [US4] [SKIPPED] Implement auto-export logic in `src/cli/commands/query.py`:
  - After query execution, check if auto-export enabled in config
  - Generate filename from template with timestamp (YYYYMMDD_HHMMSS)
  - Create date subdirectory if `create_subdirectories_by_date` enabled (YYYY-MM-DD)
  - Call `export_to_file()` with generated path and default format
  - Skip if `--no-export` flag provided

- [ ] T029 [US4] [SKIPPED] Add `--no-export` flag to query command in `src/cli/commands/query.py`:
  - Add `@click.option("--no-export", is_flag=True)`
  - Skip auto-export if flag present (explicit export still works)

- [ ] T030 [US4] [SKIPPED] Add auto-export enable/disable commands to `src/cli/commands/config.py`:
  - Add `config auto-export enable` command
  - Add `config auto-export disable` command
  - Add `config auto-export show` to display current settings
  - Prompt for output directory, format, and other settings when enabling

**Checkpoint**: User Story 4 complete - users can configure automatic exports. Test independently with quickstart examples (to be added for US4).

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and ensure Constitution compliance

### Constitution Compliance Tasks

- [x] T031 [P] [POLISH] Security audit: Verify path validation prevents traversal attacks (Principle I - Security-First)
  - Test with `../../../etc/passwd` paths
  - Test with Windows UNC paths `\\server\share`
  - Test with symbolic link exploitation attempts

- [x] T032 [P] [POLISH] Security audit: Verify no database credentials in export files (Principle I - Security-First)
  - Review all formatters to ensure connection strings never written
  - Verify error messages don't leak credentials

- [x] T033 [P] [POLISH] UX validation: Export completes in under 3 seconds for 10,000 rows (Principle II - UX Over Technical Purity)
  - Benchmark CSV export with 10k rows
  - Benchmark JSON export with 10k rows
  - Verify progress indicators don't slow down export

- [x] T034 [P] [POLISH] Transparency: Verify success messages show file path and row count (Principle III - Transparency)
  - Verify FR-016 compliance
  - Check both CLI and REPL modes
  - Verify renamed filename messages display correctly

- [x] T035 [POLISH] Multi-DB parity: Test export across PostgreSQL, MySQL, SQLite, MongoDB (Principle IV - Multi-Database Parity)
  - Export from PostgreSQL → verify CSV, JSON, SQL formats
  - Export from MySQL → verify all formats
  - Export from SQLite → verify all formats
  - Export from MongoDB → verify JSON format (SQL should error gracefully)
  - Verify identical behavior across databases per FR-018

- [x] T036 [P] [POLISH] Fail-safe: Verify auto-rename never overwrites files (Principle V - Fail-Safe Defaults)
  - Test file conflict scenarios
  - Verify timestamp suffixes are unique (down to second precision)
  - Verify original files remain intact

- [x] T037 [P] [POLISH] Fail-safe: Verify auto-export disabled by default (Principle V - Fail-Safe Defaults)
  - Check fresh config file has `auto_export.enabled: false`
  - Verify explicit user action required to enable

### Documentation & Quality Tasks

- [x] T038 [P] [POLISH] Update main README with export feature examples
  - Add "Export Results" section
  - Link to quickstart.md
  - Show basic CSV export example

- [ ] T039 [P] [POLISH] [SKIPPED] Create export troubleshooting guide in `docs/troubleshooting.md`:
  - Permission errors → check directory permissions
  - Disk full → free up space or change export directory
  - Invalid path → path requirements per OS
  - Format errors → supported formats list

- [x] T040 [POLISH] Run all quickstart.md examples for validation:
  - Examples 1.1-1.5 (User Story 1 - CSV Export CLI)
  - Examples 2.1-2.4 (User Story 2 - REPL Export)
  - Examples 3.1-3.5 (User Story 3 - Multiple Formats)
  - Cross-database examples (PostgreSQL, MySQL, SQLite, MongoDB)
  - Large dataset example (100,000 rows with progress)
  - Error scenarios (permission denied, invalid path, disk full)

- [x] T041 [P] [POLISH] Performance optimization for large exports:
  - Profile memory usage during 1M row export
  - Verify streaming prevents OOM
  - Optimize progress callback frequency if needed

- [x] T042 [P] [POLISH] Code cleanup and refactoring:
  - Remove debug logging
  - Ensure consistent error message formatting
  - Add docstrings to all public functions
  - Run linter (ruff) and fix issues

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup (Phase 1) - BLOCKS all user stories
- **User Stories (Phases 3-6)**: All depend on Foundational (Phase 2) completion
  - US1 (P1): Can start after Foundational - No dependencies on other stories
  - US2 (P2): Can start after Foundational - Depends on core exporter from US1 (T011)
  - US3 (P3): Can start after Foundational - Extends US1 exporters (T010)
  - US4 (P4): Can start after US1 complete - Depends on core export functionality
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Foundation only → Delivers CSV export in CLI
- **User Story 2 (P2)**: Foundation + US1 core (T011) → Delivers REPL export
- **User Story 3 (P3)**: Foundation + US1 core (T011) → Delivers JSON/SQL/Mermaid formats
- **User Story 4 (P4)**: Foundation + US1 complete → Delivers auto-export mode

**Note**: US2, US3, US4 all depend on US1's core exporter (T011), so US1 should complete first. However, US2 and US3 can proceed in parallel after US1's core tasks complete.

### Within Each User Story

**US1 (CSV Export - MVP)**:
1. T010 (CSV formatter) [P] parallel with T011 start
2. T011 (core exporter) - central dependency
3. T012 (streaming) depends on T011
4. T013 (CLI integration) depends on T011, T012
5. T014 (error handling) depends on T013

**US2 (REPL Export)**:
1. T015, T016, T017, T018 can proceed in sequence (all same file `repl.py`)

**US3 (Multiple Formats)**:
1. T019, T020, T021, T022 [P] - all format writers in parallel
2. T023, T024 (exporter updates) after format writers complete
3. T025, T026 (CLI/schema integration) after T024

**US4 (Auto-Export)**:
1. T027, T028, T029, T030 proceed in sequence (config and CLI changes)

### Parallel Opportunities

**Setup (Phase 1)**: T001, T002, T003, T004 all [P] - 4 parallel tasks

**Foundational (Phase 2)**: T005, T006, T007 can be parallel (different functions in same file), T008, T009 sequential after

**User Story 1**: T010 and T011 start can overlap, then T012-T014 sequential

**User Story 3**: T019, T020, T021, T022 [P] - 4 format writers in parallel

**Polish**: T031, T032, T033, T034, T036, T037, T038, T039, T041, T042 all [P] - 10 parallel tasks

---

## Parallel Example: User Story 3 (Multiple Formats)

```bash
# Launch all format writers together:
Task T019: "Extend JSON formatter in src/cli/formatting/json_formatter.py"
Task T020: "Create SQL formatter in src/cli/formatting/sql_formatter.py"
Task T021: "Create Mermaid formatter in src/cli/formatting/mermaid_formatter.py"
Task T022: "Create plain text formatter in src/cli/formatting/__init__.py"

# After all writers complete, update exporter routing:
Task T023: "Update format detection in src/cli/export/exporter.py"
Task T024: "Update main exporter to route to format writers"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational (T005-T009) - **CRITICAL CHECKPOINT**
3. Complete Phase 3: User Story 1 (T010-T014)
4. **STOP and VALIDATE**: Test CSV export per quickstart.md examples 1.1-1.5
5. Run on real database with various data types
6. Deploy MVP if ready - users can now export to CSV from CLI!

### Incremental Delivery

1. **Foundation** (Phases 1-2) → Core infrastructure ready
2. **MVP** (Phase 3 - US1) → CSV export in CLI mode → Deploy/Demo
3. **REPL Support** (Phase 4 - US2) → Add REPL export → Deploy/Demo
4. **Format Expansion** (Phase 5 - US3) → JSON, SQL, Mermaid → Deploy/Demo
5. **Automation** (Phase 6 - US4) → Auto-export mode → Deploy/Demo
6. **Polish** (Phase 7) → Constitution compliance, optimization → Final release

Each phase adds value without breaking previous functionality.

### Parallel Team Strategy

With multiple developers:

**Week 1:**
- All: Setup + Foundational (Phases 1-2) - must complete together

**Week 2:**
- Developer A: User Story 1 (T010-T014) - MVP priority
- Developer B: Research/spike User Story 3 format writers

**Week 3:**
- Developer A: User Story 2 (T015-T018) - REPL support
- Developer B: User Story 3 (T019-T026) - Multiple formats

**Week 4:**
- Developer A: User Story 4 (T027-T030) - Auto-export
- Developer B: Polish (T031-T042) - Quality assurance

---

## Task Summary

- **Total Tasks**: 42 tasks
- **Setup (Phase 1)**: 4 tasks (T001-T004)
- **Foundational (Phase 2)**: 5 tasks (T005-T009)
- **User Story 1 (P1 - MVP)**: 5 tasks (T010-T014)
- **User Story 2 (P2)**: 4 tasks (T015-T018)
- **User Story 3 (P3)**: 8 tasks (T019-T026)
- **User Story 4 (P4)**: 4 tasks (T027-T030)
- **Polish (Phase 7)**: 12 tasks (T031-T042)

**Parallel Opportunities**: 18 tasks marked [P] can run in parallel within their phase

**MVP Scope**: Phases 1-3 (T001-T014) = 14 tasks for basic CSV export in CLI

**Full Feature**: All 42 tasks for complete export functionality with all formats and modes

---

## Notes

- [P] tasks = different files, can run in parallel
- [Story] label (US1, US2, US3, US4) maps task to specific user story
- Each user story is independently testable per quickstart.md
- No automated tests generated (not requested in spec) - use manual testing via quickstart.md examples
- Constitution compliance validated in Polish phase (T031-T037)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Follow quickstart.md examples for acceptance testing
