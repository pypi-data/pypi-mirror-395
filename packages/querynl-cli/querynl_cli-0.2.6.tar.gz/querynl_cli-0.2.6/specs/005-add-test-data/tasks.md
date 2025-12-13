# Tasks: Test Data Generation for Schema Design Mode

**Input**: Design documents from `/specs/005-add-test-data/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/test_data_generator_api.py

**Tests**: Not explicitly requested in feature specification - tests omitted per template guidelines

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

**Constitution Compliance**: All tasks must align with [QueryNL Constitution v1.0.0](../.specify/memory/constitution.md). Security-first design, transparency, and fail-safe defaults are non-negotiable.

## Format: `[ID] [P?] [Story] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Include exact file paths in descriptions

## User Stories Summary

- **User Story 1 (P1)**: Generate Sample Data for New Schema - Core MVP functionality
- **User Story 2 (P2)**: Control Test Data Volume - Quantity specification
- **User Story 3 (P3)**: Customize Test Data Content - Domain context customization

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Add new dependencies and update project configuration

- [X] T001 Add Faker dependency (>=38.2.0) to `requirements.txt`
- [X] T002 Add toposort dependency (>=1.10) to `requirements.txt`
- [X] T003 [P] Run `pip install -r requirements.txt` to install new dependencies
- [X] T004 [P] Create new directory `src/cli/schema_design/` if it doesn't exist (likely already exists per plan.md)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core models and utilities that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 [P] Create `TestDataRequest` model in `src/cli/models.py` with validation (user_query, target_tables, record_counts, domain_context, database_type)
- [X] T006 [P] Create `DataGenerationPlan` model in `src/cli/models.py` with sub-entities (TableGenerationConfig, ColumnGenerationConfig, ForeignKeyConfig)
- [X] T007 [P] Create `InsertionResult` model in `src/cli/models.py` with sub-entities (TableInsertionResult, InsertionError with ErrorType enum)
- [X] T008 [P] Create `ProgressUpdate` and `CancellationToken` utility classes in `src/cli/models.py`
- [X] T009 Create base `IDataSynthesizer` interface in `src/cli/schema_design/data_synthesizer.py` (abstract base class defining generate_value, generate_table_data, clear_unique_cache methods)
- [X] T010 Create base `IInsertionExecutor` interface in `src/cli/schema_design/insertion_executor.py` (abstract base class defining execute_insertion, build_insert_statement, escape_value methods)
- [X] T011 Create base `ITestDataGenerator` interface in `src/cli/schema_design/test_data_generator.py` (abstract base class defining generate_test_data, generate_plan, validate_plan methods)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Generate Sample Data for New Schema (Priority: P1) 🎯 MVP

**Goal**: Enable users to type "add sample data" and get realistic test data with default quantities (10-20 records per table) that respects all constraints and foreign keys

**Independent Test**: Create schema with `\schema design`, request "add sample data", verify tables populated with valid data respecting FKs

**Why MVP**: This is the core value proposition - immediate test data generation without manual specification

### Implementation for User Story 1

**Step 1: Data Synthesis (Faker Integration)**

- [X] T012 [P] [US1] Implement `FakerDataSynthesizer` class in `src/cli/schema_design/data_synthesizer.py`:
  - Initialize Faker instance
  - Implement `generate_value()` for single column based on ColumnGenerationConfig
  - Handle common Faker providers: name, email, phone_number, address, city, country, company, date, random_int, boolean, text
  - Implement unique constraint handling via `fake.unique` property
  - Implement `clear_unique_cache()` method

- [X] T013 [US1] Extend `FakerDataSynthesizer` in `src/cli/schema_design/data_synthesizer.py`:
  - Implement `generate_table_data()` for multiple records
  - Handle foreign key value selection from `foreign_key_refs` dict
  - Track generated primary key values for FK references
  - Respect nullable columns with null_probability

**Step 2: INSERT Statement Generation (Database-Specific)**

- [X] T014 [P] [US1] Implement MySQL INSERT builder in `src/cli/schema_design/insertion_executor.py`:
  - Create `MySQLInsertionExecutor` class implementing `IInsertionExecutor`
  - Implement `escape_value()` for MySQL: backslash escaping for strings, `0`/`1` for booleans, ISO dates
  - Implement `build_insert_statement()` with literal values (NOT parameterized `?`)
  - Handle auto_increment columns (skip in column list)

- [X] T015 [P] [US1] Implement PostgreSQL INSERT builder in `src/cli/schema_design/insertion_executor.py`:
  - Create `PostgreSQLInsertionExecutor` class implementing `IInsertionExecutor`
  - Implement `escape_value()` for PostgreSQL: double quote escaping `''`, `TRUE`/`FALSE` for booleans
  - Implement `build_insert_statement()` with literal values
  - Handle SERIAL/BIGSERIAL columns (skip in column list)

- [X] T016 [P] [US1] Implement SQLite INSERT builder in `src/cli/schema_design/insertion_executor.py`:
  - Create `SQLiteInsertionExecutor` class implementing `IInsertionExecutor`
  - Implement `escape_value()` for SQLite: double quote escaping `''`, `0`/`1` for booleans
  - Implement `build_insert_statement()` with literal values
  - Handle AUTOINCREMENT columns (skip in column list)

**Step 3: Batch Execution with Transaction Management**

- [X] T017 [US1] Implement batch execution in `src/cli/schema_design/insertion_executor.py`:
  - Extend all executor classes with `execute_insertion()` method
  - Implement batching strategy: 1000 rows/batch for MySQL/PostgreSQL, 10000 for SQLite
  - Use savepoint-based error recovery (create savepoint per batch, rollback on error)
  - Handle IntegrityError by retrying failed batch record-by-record
  - Track successful/failed insertions and collect error details
  - Return `TableInsertionResult` with statistics

- [X] T018 [US1] Add transaction management to `src/cli/schema_design/insertion_executor.py`:
  - Implement single transaction for < 10K records (flush periodically)
  - Implement batched transactions for > 10K records (commit every 10K)
  - Implement graceful cancellation support (check CancellationToken between batches)
  - Rollback on cancellation with user notification

**Step 4: LLM Plan Generation**

- [X] T019 [US1] Implement LLM plan generator in `src/cli/schema_design/test_data_generator.py`:
  - Create `TestDataGenerator` class implementing `ITestDataGenerator`
  - Implement `generate_plan()` method that calls LLM with schema metadata
  - Design LLM prompt that returns JSON plan (NOT INSERT statements)
  - Prompt specifies: tables, record_count (default 10-20), columns with faker_provider, insertion_order
  - Parse LLM response and construct `DataGenerationPlan` Pydantic model
  - Include rationale for transparency

- [X] T020 [US1] Add plan validation in `src/cli/schema_design/test_data_generator.py`:
  - Implement `validate_plan()` method
  - Check all faker_provider values are valid Faker methods
  - Verify insertion_order is topologically sorted (parents before children)
  - Ensure all FK references point to earlier tables in insertion_order
  - Check record_counts are positive integers
  - Return list of validation errors (empty if valid)

**Step 5: Foreign Key Dependency Handling**

- [X] T021 [US1] Implement topological sort in `src/cli/schema_design/test_data_generator.py`:
  - Add helper method `_extract_table_dependencies()` from SchemaMetadata
  - Integrate `toposort` library to sort tables by FK dependencies
  - Detect circular dependencies and raise clear error
  - Return insertion order as list of table names

**Step 6: Orchestration and Integration**

- [X] T022 [US1] Implement main orchestration in `src/cli/schema_design/test_data_generator.py`:
  - Implement `generate_test_data()` method coordinating all components
  - Flow: validate request → introspect schema → generate plan → validate plan → execute plan
  - Initialize appropriate InsertionExecutor based on database_type
  - Process tables in insertion_order from plan
  - Track foreign key refs (ForeignKeyTracker) during generation
  - Aggregate results into `InsertionResult`
  - Handle errors and return detailed statistics

- [X] T023 [US1] Add progress indication in `src/cli/schema_design/test_data_generator.py`:
  - Integrate Rich Progress bar showing current table, records completed/total
  - Calculate and display speed (records/sec) using smoothed moving average
  - Calculate ETA based on recent speed
  - Update progress after each batch insertion
  - Show spinner during LLM plan generation phase

**Step 7: REPL Command Integration**

- [X] T024 [US1] Add test data intent detection in `src/cli/repl.py`:
  - Create `_detect_test_data_intent()` method checking for keywords: "add sample data", "add test data", "populate", "generate data"
  - Return True if test data generation intent detected

- [X] T025 [US1] Implement test data command handler in `src/cli/repl.py`:
  - Create `_handle_test_data_generation()` method in REPLManager class
  - Parse user input into `TestDataRequest` (for US1: no explicit counts, use defaults)
  - Call schema introspection to get current schema
  - Validate schema exists and has tables (error if empty database)
  - Instantiate `TestDataGenerator` with LLM service and database connection
  - Call `generate_test_data()` with CancellationToken for Ctrl+C support
  - Display generated plan and prompt for confirmation before execution
  - Show progress during execution
  - Display final results with success/failure statistics

- [X] T026 [US1] Integrate command handler in REPL loop in `src/cli/repl.py`:
  - In main REPL input processing, check `_detect_test_data_intent()` before sending to LLM
  - If detected, route to `_handle_test_data_generation()` instead of normal query flow
  - Ensure proper error handling and user-friendly messages

**Step 8: Error Handling and User Feedback**

- [X] T027 [US1] Implement error reporting in `src/cli/repl.py`:
  - Format `InsertionResult.errors` into user-friendly messages
  - For constraint violations: show constraint name, column, and failed record
  - For < 20 failures: display detailed list with Rich formatting
  - For >= 20 failures: offer to export to file, show summary only
  - Provide clear success summary: "✓ Successfully inserted X records across Y tables"

- [X] T028 [US1] Add schema validation error handling in `src/cli/repl.py`:
  - Check for empty database (no tables) and show helpful message: "No schema found. Create one with `\schema design`"
  - Handle LLM plan generation failures with retry option
  - Handle database connection errors gracefully

**Checkpoint**: At this point, User Story 1 is fully functional. Users can type "add sample data" and get realistic test data with defaults.

**Deliverable**: MVP is complete! Users can test their schemas immediately after creation.

---

## Phase 4: User Story 2 - Control Test Data Volume (Priority: P2)

**Goal**: Allow users to specify exact quantities like "add 100 users" or "add 50 customers and 200 orders"

**Independent Test**: Request "add 100 users" and verify exactly 100 records inserted

**Why P2**: Adds flexibility but basic functionality works without it (US1 uses defaults)

### Implementation for User Story 2

- [X] T029 [US2] Extend NLP parsing in `src/cli/repl.py`:
  - Enhance `_handle_test_data_generation()` to parse quantity specifications from user input
  - Extract patterns like "N records", "N users", "N customers and M orders"
  - Parse table names and their corresponding counts
  - Populate `TestDataRequest.record_counts` dict with parsed values
  - Handle edge case: no quantities specified (US1 behavior - use defaults)

- [X] T030 [US2] Update LLM prompt in `src/cli/schema_design/test_data_generator.py`:
  - Modify `generate_plan()` to incorporate explicit record counts from request
  - If `record_counts` specified in request, override defaults with user values
  - If only some tables specified, use defaults for others
  - Include user's quantity intent in prompt for context

- [X] T031 [US2] Add large dataset warning in `src/cli/repl.py`:
  - In `_handle_test_data_generation()`, check total estimated records
  - If total > 10,000 records (threshold from research), display warning
  - Show estimated time based on database type and record count
  - Prompt for explicit confirmation: "This will generate X records (estimated Ym Zs). Continue? (y/N)"
  - Allow user to cancel or proceed

- [X] T032 [US2] Update progress display in `src/cli/schema_design/test_data_generator.py`:
  - Modify progress bar to show larger totals properly
  - For > 10K records, show progress per table (nested progress bars)
  - Ensure ETA calculation works accurately for large datasets
  - Show current table being processed

**Checkpoint**: User Story 2 complete. Users can now control data volume precisely.

**Deliverable**: "add 1000 users and 5000 orders" works correctly with warnings for large volumes.

---

## Phase 5: User Story 3 - Customize Test Data Content (Priority: P3)

**Goal**: Enable domain-specific data generation like "add e-commerce sample data" for more realistic test data

**Independent Test**: Request "add e-commerce product data" and verify product-appropriate names/categories

**Why P3**: Nice-to-have feature that improves realism but not essential for testing

### Implementation for User Story 3

- [X] T033 [US3] Extend request parsing in `src/cli/repl.py`:
  - Enhance `_handle_test_data_generation()` to extract domain context keywords
  - Detect patterns: "e-commerce", "social media", "blog", "medical", "financial", "inventory"
  - Populate `TestDataRequest.domain_context` with detected domain
  - Pass domain context to plan generation

- [X] T034 [US3] Update LLM prompt for domain awareness in `src/cli/schema_design/test_data_generator.py`:
  - Modify `generate_plan()` to include domain_context in prompt
  - Instruct LLM to select contextually appropriate Faker providers
  - For e-commerce: use company names for product names, currency for prices
  - For blog: use sentence/text for post content, name for authors
  - For medical: use appropriate terminology for fields
  - Include domain reasoning in plan rationale

- [X] T035 [US3] Extend Faker provider selection in `src/cli/schema_design/data_synthesizer.py`:
  - Add domain-specific provider mapping in `FakerDataSynthesizer`
  - Map generic column names to domain providers: "product_name" + e-commerce → company name
  - Handle cases where domain context suggests different value types
  - Fall back to generic providers if domain mapping not available

- [X] T036 [US3] Add domain examples to user feedback in `src/cli/repl.py`:
  - When displaying plan rationale, highlight domain-specific choices
  - Example: "Using company names for product data (e-commerce context)"
  - Help users understand how domain context influenced generation

**Checkpoint**: User Story 3 complete. Domain-customized test data generation works.

**Deliverable**: "add e-commerce sample data" generates realistic product/order/customer data for e-commerce context.

---

## Phase 6: Polish & Integration

**Purpose**: Cross-cutting concerns, error recovery, and final integration

- [X] T037 [P] Add comprehensive error messages in `src/cli/schema_design/test_data_generator.py`:
  - Create `_format_error_message()` helper for constraint violations
  - Parse database error messages and extract constraint/column info
  - Provide actionable suggestions: "UNIQUE constraint on 'email' - generating more unique values than available patterns"

- [X] T038 [P] Implement logging in `src/cli/schema_design/test_data_generator.py`:
  - Add debug logging for plan generation (log full LLM prompt/response)
  - Log batch execution statistics (batch size, time, success/failure)
  - Log FK tracking state (generated IDs per table)
  - Use existing logging configuration from QueryNL

- [X] T039 Add Ctrl+C cancellation handling in `src/cli/repl.py`:
  - Implement signal handler for SIGINT in `_handle_test_data_generation()`
  - Set cancellation token on first Ctrl+C (finish current batch, then rollback)
  - Force exit on second Ctrl+C with warning
  - Display cancellation message: "Operation cancelled by user. Rolling back changes..."

- [X] T040 Add help documentation in `src/cli/repl.py`:
  - Update `\help` command to include test data generation examples
  - Add inline help when test data intent detected but syntax unclear
  - Show examples: "add sample data", "add 100 users", "add e-commerce product data"

- [X] T041 [P] Update constitution compliance documentation:
  - Document security considerations: no SQL injection via Faker-generated values
  - Document transparency: plan shown before execution, INSERT statements logged
  - Document fail-safe: defaults to small batches, warns on large datasets
  - Document multi-database parity: equal functionality across MySQL/PostgreSQL/SQLite
  - Add to project README or CLAUDE.md

**Checkpoint**: All polish tasks complete. Feature is production-ready.

---

## Task Dependencies

### Dependency Graph (by User Story)

```
Setup (T001-T004) → Foundational (T005-T011)
                    ↓
                    User Story 1 (T012-T028) ← MVP Complete
                    ↓
                    User Story 2 (T029-T032) ← Volume Control
                    ↓
                    User Story 3 (T033-T036) ← Domain Context
                    ↓
                    Polish (T037-T041) ← Production Ready
```

### Critical Path (US1 - MVP)
1. **Setup & Foundation** (T001-T011): ~2-3 hours
2. **Data Synthesis** (T012-T013): ~3-4 hours
3. **INSERT Builders** (T014-T016): ~4-5 hours (parallel)
4. **Batch Execution** (T017-T018): ~3-4 hours
5. **LLM Integration** (T019-T021): ~4-5 hours
6. **Orchestration** (T022-T023): ~3-4 hours
7. **REPL Integration** (T024-T026): ~2-3 hours
8. **Error Handling** (T027-T028): ~2-3 hours

**Total MVP Effort**: ~24-32 hours

### Parallelization Opportunities

**Within Foundational Phase** (after T004):
- T005, T006, T007, T008 can run in parallel (different models)
- T009, T010, T011 depend on models but can be parallel

**Within US1 Data Synthesis**:
- T012 and T013 are sequential (T013 extends T012)

**Within US1 INSERT Builders**:
- T014, T015, T016 can run in parallel (different database executors)

**Within US1 Orchestration**:
- T022 and T023 are sequential (progress is part of orchestration)
- T024, T025 are sequential (detection before handling)

**Within Polish**:
- T037, T038, T041 can run in parallel (different concerns)

### Parallel Execution Example (US1)

```bash
# After Foundational complete, parallelize INSERT builders
Terminal 1: Work on T014 (MySQL executor)
Terminal 2: Work on T015 (PostgreSQL executor)
Terminal 3: Work on T016 (SQLite executor)

# Later, parallelize polish tasks
Terminal 1: Work on T037 (error messages)
Terminal 2: Work on T038 (logging)
Terminal 3: Work on T041 (documentation)
```

---

## Implementation Strategy

### Phase Completion Criteria

**Phase 1 (Setup)**:
- ✅ Faker and toposort installed
- ✅ Dependencies verified with `pip list`

**Phase 2 (Foundational)**:
- ✅ All Pydantic models defined and importable
- ✅ All interfaces (IDataSynthesizer, IInsertionExecutor, ITestDataGenerator) defined
- ✅ No syntax errors, code passes `ruff check`

**Phase 3 (US1 - MVP)**:
- ✅ User can type "add sample data" in REPL
- ✅ System generates realistic data with defaults (10-20 records)
- ✅ Foreign keys maintain referential integrity
- ✅ Works across MySQL, PostgreSQL, SQLite
- ✅ Progress bar shows during generation
- ✅ Error messages are actionable

**Phase 4 (US2 - Volume)**:
- ✅ User can specify "add 100 users"
- ✅ System generates exact quantity requested
- ✅ Large dataset warning appears for > 10K records
- ✅ Progress accurate for large datasets

**Phase 5 (US3 - Domain)**:
- ✅ User can specify "add e-commerce data"
- ✅ Generated data reflects domain context
- ✅ Plan rationale explains domain choices

**Phase 6 (Polish)**:
- ✅ Ctrl+C cancellation works gracefully
- ✅ Help documentation updated
- ✅ Error messages comprehensive
- ✅ Logging enabled for debugging
- ✅ Constitution compliance documented

### Testing Strategy (Manual - No Automated Tests)

Since tests were not explicitly requested in the specification, manual testing is recommended:

**After US1 (MVP)**:
1. Create test schema: `\schema design` → "blog with users and posts"
2. Request data: "add sample data"
3. Verify: Query tables, check FK integrity
4. Test each database: MySQL, PostgreSQL, SQLite

**After US2 (Volume)**:
1. Request specific quantity: "add 100 users"
2. Verify: `SELECT COUNT(*) FROM users` returns 100
3. Test large volume: "add 50000 records" → verify warning

**After US3 (Domain)**:
1. Request domain-specific: "add e-commerce product data"
2. Verify: Product names look realistic for e-commerce
3. Compare with generic: "add sample data" → verify difference

**Edge Cases to Test**:
- Empty database (no schema) → error message
- Circular FK dependencies → auto-handled or clear error
- Unique constraints → no duplicates generated
- Ctrl+C during generation → graceful rollback
- Very large dataset (100K records) → performance acceptable

---

## Task Summary

**Total Tasks**: 41
- **Setup**: 4 tasks (T001-T004)
- **Foundational**: 7 tasks (T005-T011)
- **User Story 1 (P1 - MVP)**: 17 tasks (T012-T028)
- **User Story 2 (P2)**: 4 tasks (T029-T032)
- **User Story 3 (P3)**: 4 tasks (T033-T036)
- **Polish**: 5 tasks (T037-T041)

**Parallelizable Tasks**: 15 tasks marked with [P]

**MVP Scope** (recommended first delivery): Setup + Foundational + US1 = 28 tasks

**Independent Testing**:
- **US1**: Create schema, request "add sample data", verify tables populated correctly
- **US2**: Request "add 100 users", verify count = 100
- **US3**: Request "add e-commerce data", verify domain-appropriate content

**Estimated Effort**:
- **MVP (US1)**: 24-32 hours
- **US2**: 4-6 hours
- **US3**: 4-6 hours
- **Polish**: 4-6 hours
- **Total**: 36-50 hours

**Key Success Metrics** (from spec.md Success Criteria):
- SC-001: Test data generation < 10 seconds for 10-table schemas
- SC-002: 100% referential integrity maintained
- SC-003: Zero constraint violations
- SC-004: 95% success rate without user intervention
- SC-006: Works consistently across MySQL, PostgreSQL, SQLite
