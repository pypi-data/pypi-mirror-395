# Implementation Plan: Export and Save Query Results

**Branch**: `003-export-and-save` | **Date**: 2025-10-25 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/003-export-and-save/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Add export functionality to QueryNL CLI allowing users to save query results and command outputs to files in multiple formats (CSV, JSON, SQL INSERT, Mermaid diagrams, plain text). Support both CLI (--export flag) and REPL (\export command) modes with automatic format detection, streaming for large datasets, and fail-safe file handling (automatic timestamped renaming on conflicts).

**Primary Goal**: Enable users to save query results from both CLI and REPL modes in standard formats (CSV for spreadsheets, JSON for APIs, SQL for migrations, Mermaid for documentation).

**Technical Approach**: Extend existing formatting infrastructure (csv_formatter.py, json_formatter.py) with file I/O capabilities, add new formatters for SQL INSERT and Mermaid ER diagrams, implement streaming export for large result sets, integrate with CLI commands and REPL session state.

## Technical Context

**Language/Version**: Python 3.10+ (existing codebase uses 3.10-3.12)
**Primary Dependencies**:
- click>=8.1.0 (CLI framework with existing --format support)
- rich>=13.0.0 (terminal UI, already used for formatting)
- Python stdlib: csv, json, pathlib, datetime

**Storage**: File system (local paths, no database storage for exports)
**Testing**: pytest>=8.0.0 with pytest-cov (existing test infrastructure)
**Target Platform**: Cross-platform CLI (Linux, macOS, Windows)
**Project Type**: Single project (src/cli/ structure)
**Performance Goals**:
- Export <10,000 rows in under 3 seconds
- Stream exports for >10,000 rows with progress every 10,000 rows
- Memory-efficient streaming to handle 1M+ rows without OOM

**Constraints**:
- Must work identically across PostgreSQL, MySQL, SQLite, MongoDB
- No external file storage services (S3, etc.) - local filesystem only
- Must preserve existing CLI/REPL user experience (non-breaking)
- Export must not block query execution or display results

**Scale/Scope**:
- 5 export formats (CSV, JSON, SQL, Mermaid, TXT)
- 2 modes (CLI, REPL)
- 21 functional requirements
- Streaming support for datasets up to 1M+ rows

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Reference: [QueryNL Constitution v1.0.0](../../.specify/memory/constitution.md)

### I. Security-First Design ✓
- [x] Credential storage uses AES-256 encryption - **N/A** (export doesn't handle credentials)
- [x] No credentials in logs, errors, or telemetry - **PASS** (export writes query results only, never connection strings)
- [x] Input validation prevents SQL injection - **PASS** (export doesn't execute SQL, only reads results)
- [x] OWASP Top 10 vulnerabilities addressed - **PASS** (path traversal prevention, no code execution)
- [x] Security audit plan defined for major release - **PASS** (include in next security audit)

**Analysis**: Export feature has minimal security surface - it writes user data to local filesystem with user-specified paths. Key risks: path traversal attacks (prevented by pathlib validation), disk full errors (handled gracefully with clear errors), permission errors (checked before export). No credential exposure risk.

### II. User Experience Over Technical Purity ✓
- [x] First query completable within 5 minutes of installation - **PASS** (export is optional, doesn't affect core workflow)
- [x] Error messages are actionable (not stack traces) - **PASS** (FR-010 requires clear error messages for permissions, disk space, invalid paths)
- [x] IDE integration does not block UI - **N/A** (feature is CLI-only)
- [x] Query generation latency < 5 seconds (95th percentile) - **PASS** (export doesn't affect query generation, happens after results returned)

**Analysis**: Export enhances UX by saving interesting results without interrupting workflow. Auto-rename on conflicts (vs. prompting) prevents blocking automation. Progress indicators every 10,000 rows provide transparency without overwhelming users.

### III. Transparency and Explainability ✓
- [x] Generated SQL displayed before execution - **N/A** (export doesn't generate SQL)
- [x] Destructive operations require confirmation - **PASS** (export never overwrites, auto-renames instead - fail-safe)
- [x] Schema/optimization rationale provided - **N/A** (export doesn't modify schemas)
- [x] LLM token usage visible to users - **N/A** (export doesn't use LLM)

**Analysis**: Export provides transparency through success messages showing file path and row count (FR-016), progress indicators for large exports (FR-015), and clear format detection (FR-006 auto-detects from extension).

### IV. Multi-Database Parity ✓
- [x] PostgreSQL, MySQL, SQLite, MongoDB equally supported - **PASS** (FR-018 requires identical export behavior across all databases)
- [x] Test coverage equivalent across all databases - **PASS** (test plan includes all 4 databases)
- [x] Documentation includes database-specific examples - **PASS** (quickstart.md will show examples for each database)

**Analysis**: Export works on query results (database-agnostic data), not database-specific features. SQL INSERT format (FR-013) generates syntax compatible with source database type. All formats work identically regardless of source database.

### V. Fail-Safe Defaults ✓
- [x] Destructive operations require explicit confirmation - **PASS** (auto-rename prevents accidental overwrites, never prompts that could hang automation)
- [x] Migration rollback scripts generated by default - **N/A** (export doesn't generate migrations)
- [x] Rate limiting enabled by default - **N/A** (export is local file I/O, no API calls)
- [x] Telemetry is opt-in (not opt-out) - **N/A** (export doesn't collect telemetry)

**Analysis**: Fail-safe defaults embodied in auto-rename behavior (never overwrites), automatic directory creation (mkdir -p), and streaming for large datasets (prevents OOM). Export defaults to conservative behavior: explicit user action required (--export flag or \export command), no auto-export unless explicitly enabled in config (P4 user story).

**GATE STATUS**: ✅ **PASSED** - All applicable constitutional requirements met. No violations requiring justification.

## Project Structure

### Documentation (this feature)

```
specs/003-export-and-save/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
│   └── export_api.md    # Internal API contract for export service
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```
src/cli/
├── formatting/                    # Existing formatters (extend these)
│   ├── csv_formatter.py          # Extend with streaming CSV export
│   ├── json_formatter.py         # Extend with streaming JSON export
│   ├── sql_formatter.py          # NEW: SQL INSERT statement generator
│   └── mermaid_formatter.py      # NEW: Mermaid ER diagram generator
│
├── export/                        # NEW: Export functionality
│   ├── __init__.py
│   ├── exporter.py               # Main export service (format detection, file handling)
│   ├── streaming.py              # Streaming export for large result sets
│   └── file_utils.py             # File handling (mkdir -p, auto-rename, validation)
│
├── commands/
│   ├── query.py                  # Modify: add --export flag
│   └── schema.py                 # Modify: add Mermaid export support
│
└── repl.py                        # Modify: add \export command

tests/
├── unit/
│   └── export/                    # NEW: Unit tests for export module
│       ├── test_exporter.py
│       ├── test_streaming.py
│       ├── test_formatters.py
│       └── test_file_utils.py
│
└── integration/
    └── export/                    # NEW: Integration tests
        ├── test_cli_export.py     # Test --export flag in query command
        ├── test_repl_export.py    # Test \export in REPL
        └── test_all_databases.py  # Test across PostgreSQL/MySQL/SQLite/MongoDB
```

**Structure Decision**: Single project structure (Option 1) - QueryNL is a unified CLI tool with no separate frontend/backend. New export functionality lives in `src/cli/export/` module, extending existing `formatting/` infrastructure. This maintains consistency with existing codebase structure and allows code reuse between console output formatters and file export formatters.

## Complexity Tracking

*No violations requiring justification - all Constitution Check items passed.*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
