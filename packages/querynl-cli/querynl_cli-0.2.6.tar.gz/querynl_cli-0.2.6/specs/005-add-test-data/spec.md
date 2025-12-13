# Feature Specification: Test Data Generation for Schema Design Mode

**Feature Branch**: `005-add-test-data`
**Created**: 2025-11-22
**Status**: Draft
**Input**: User description: "I need a feature where user can ask a newly created schema using \schema feature to add some tests data to the tables to test."

**Constitution**: This specification must comply with [QueryNL Constitution v1.0.0](../.specify/memory/constitution.md). All requirements must align with Security-First Design, User Experience Over Technical Purity, Transparency, Multi-Database Parity, and Fail-Safe Defaults principles.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Generate Sample Data for New Schema (Priority: P1)

A user has just created a database schema using the `\schema` feature and wants to immediately populate it with realistic test data so they can practice writing queries and verify the schema design works as intended.

**Why this priority**: This is the core value proposition - enabling users to quickly move from schema design to query testing without manual data entry. This is the MVP that delivers immediate value.

**Independent Test**: Can be fully tested by creating a schema with the `\schema` command, then requesting test data generation, and verifying that tables are populated with valid sample data that respects the schema constraints.

**Acceptance Scenarios**:

1. **Given** a user has created a schema with tables (users, posts, comments), **When** they type "add some sample data to these tables", **Then** the system generates and inserts realistic test data into all tables respecting foreign key relationships and constraints
2. **Given** a user has a schema with foreign key relationships, **When** test data is generated, **Then** the data maintains referential integrity (e.g., post.author_id references valid user.id)
3. **Given** a user requests test data, **When** the data is inserted, **Then** the user receives confirmation showing how many records were added to each table
4. **Given** a user has tables with various data types (integers, strings, dates, booleans), **When** test data is generated, **Then** each column receives appropriate sample values for its data type

---

### User Story 2 - Control Test Data Volume (Priority: P2)

A user wants to specify how much test data to generate, either because they need a larger dataset to test performance or a smaller one for quick verification.

**Why this priority**: Adds flexibility but isn't required for basic functionality. Users can work with default amounts initially.

**Independent Test**: Can be tested by requesting test data with specific quantities (e.g., "add 100 users") and verifying the correct number of records are inserted.

**Acceptance Scenarios**:

1. **Given** a user wants more data, **When** they type "add 50 sample users and 200 posts", **Then** the system generates exactly 50 user records and 200 post records
2. **Given** a user doesn't specify quantity, **When** they request sample data, **Then** the system uses reasonable defaults (10-20 records per table)
3. **Given** a user requests an unreasonably large amount (e.g., 1 million records), **When** the request is processed, **Then** the system warns about performance impact and confirms before proceeding

---

### User Story 3 - Customize Test Data Content (Priority: P3)

A user wants the test data to reflect a specific domain or scenario (e.g., "add sample data for an e-commerce store" vs. generic data).

**Why this priority**: Nice-to-have enhancement that improves realism but isn't essential for basic testing purposes.

**Independent Test**: Can be tested by requesting domain-specific data and verifying the generated content matches the requested context.

**Acceptance Scenarios**:

1. **Given** a user specifies a domain context, **When** they type "add sample e-commerce product data", **Then** the generated data uses appropriate names, categories, and values for products
2. **Given** a user wants realistic names, **When** test data is generated for a users table, **Then** the system generates plausible names rather than random strings

---

### Edge Cases

- What happens when a table has required columns that are difficult to auto-generate (e.g., complex calculated fields, external references)?
- How does the system handle circular foreign key dependencies between tables?
- What happens when the user requests test data for an empty database (no schema created yet)?
- How does the system handle tables with unique constraints when generating multiple records?
- What happens if the database already contains data - should new test data be added or should the system warn about duplicates?
- How does the system handle database-specific data types (e.g., MySQL ENUM, PostgreSQL JSON)?
- What happens if insertion fails partway through (e.g., constraint violation on record 15 of 100)?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST recognize natural language requests to add test/sample data to database tables
- **FR-002**: System MUST generate appropriate sample values for common data types (integers, strings, dates, timestamps, booleans, decimals)
- **FR-003**: System MUST respect foreign key relationships when generating test data, ensuring parent records exist before creating child records
- **FR-004**: System MUST respect unique constraints by generating distinct values for unique columns
- **FR-005**: System MUST respect NOT NULL constraints by always providing values for required columns
- **FR-006**: System MUST execute INSERT statements with actual values (not parameterized placeholders) to avoid the syntax error shown in the user's example
- **FR-007**: System MUST provide clear feedback showing how many records were successfully inserted into each table
- **FR-008**: System MUST handle insertion failures gracefully, reporting which records succeeded and which failed
- **FR-009**: Users MUST be able to specify the quantity of test data to generate (e.g., "add 50 users")
- **FR-010**: System MUST use reasonable default quantities when users don't specify amounts (default: 10-20 records per table)
- **FR-011**: System MUST generate test data that works across all supported database types (MySQL, PostgreSQL, SQLite)
- **FR-012**: System MUST validate that the schema exists and has tables before attempting to generate test data
- **FR-013**: System MUST handle tables in dependency order (insert parent table data before child tables that reference them)
- **FR-014**: System MUST provide a way for users to clear/reset test data if needed
- **FR-015**: System MUST warn users before generating large datasets that might impact performance (threshold: [NEEDS CLARIFICATION: what constitutes "large" - 1000, 10000, or 100000 records?])

### Key Entities

- **Test Data Request**: User's natural language instruction specifying which tables to populate, desired quantity, and optional domain context
- **Schema Metadata**: Information about tables, columns, data types, constraints, and relationships needed to generate valid test data
- **Generated Records**: Sample data rows conforming to schema constraints, with realistic values appropriate for each column type
- **Insertion Result**: Outcome of the data generation operation including success/failure status, record counts, and any error messages

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can request and receive test data for a newly created schema in under 10 seconds for schemas with up to 10 tables
- **SC-002**: Generated test data maintains 100% referential integrity (no orphaned foreign key references)
- **SC-003**: Generated test data violates zero constraints (all NOT NULL, UNIQUE, CHECK constraints are satisfied)
- **SC-004**: 95% of test data generation requests complete successfully without user intervention
- **SC-005**: Users can successfully execute SELECT queries against generated test data to verify their schema design
- **SC-006**: Test data generation works consistently across MySQL, PostgreSQL, and SQLite databases
- **SC-007**: Error messages for failed insertions clearly identify which table and constraint caused the failure, enabling users to fix schema issues

## Assumptions

- Users primarily need test data immediately after creating a schema via `\schema` mode
- Default test data quantities (10-20 records) are sufficient for most schema validation and query practice scenarios
- Users prefer realistic-looking data (names, emails, dates) over completely random strings
- The existing schema introspection capability can provide all necessary metadata for test data generation
- Users working with test data understand it's sample/fake data and shouldn't be used in production
- The LLM can generate contextually appropriate INSERT statements when instructed to use actual values instead of parameterized queries
- Transaction support is available to rollback failed batch insertions
