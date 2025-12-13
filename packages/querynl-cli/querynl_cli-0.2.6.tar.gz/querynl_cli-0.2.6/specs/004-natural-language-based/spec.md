# Feature Specification: Natural Language Schema Design

**Feature Branch**: `004-natural-language-based`
**Created**: 2025-11-03
**Status**: Draft
**Input**: User description: "natural language based and conversational schema design capability. 1. The user explains the requirement in natural language 2. User uploads a data file(s) (csv, etc) and discuss with the agent to come up with a Db schema 3. Design phase and finalization and then implement."

**Mode**: REPL-Only for MVP (interactive conversation is the core value proposition)

**Constitution**: This specification must comply with [QueryNL Constitution v1.0.0](../../.specify/memory/constitution.md). All requirements must align with Security-First Design, User Experience Over Technical Purity, Transparency, Multi-Database Parity, and Fail-Safe Defaults principles.

## User Scenarios & Testing

### User Story 1 - Conversational Schema Design from Description (Priority: P1)

Users enter REPL mode, start a schema design session with `\schema design`, describe their data needs in natural language, and the system guides them through an interactive conversation to design a complete database schema without requiring knowledge of SQL or database concepts.

**Why this priority**: This is the foundational capability that enables users to get started with schema design immediately. It delivers value even without file uploads, allowing users to design schemas from scratch through conversation alone. REPL mode provides the natural environment for multi-turn conversation. This is the MVP that proves the conversational AI approach works.

**Independent Test**: User can enter REPL, type `\schema design`, describe their requirements in plain English (e.g., "I need to track customers and their orders"), engage in a conversation about relationships and constraints, view the schema with `\schema show`, and save the design for implementation.

**Acceptance Scenarios**:

1. **Given** a user is in REPL mode, **When** they type `\schema design` and describe "I need to track customers and their orders", **Then** the system asks clarifying questions about entities, relationships, and constraints
2. **Given** the system has asked clarifying questions, **When** the user answers questions about customer attributes (name, email, address) and order details, **Then** the system proposes a normalized schema with customers and orders tables including primary/foreign keys
3. **Given** a proposed schema is displayed, **When** the user requests changes ("actually, customers should have multiple addresses"), **Then** the system revises the schema and shows the updated design with a customer_addresses junction table
4. **Given** a finalized schema design, **When** the user types `\schema save`, **Then** the system saves the schema specification for later implementation

---

### User Story 2 - Schema Design from Data Files (Priority: P2)

Users in REPL mode use `\schema upload <file>` to upload sample data files (CSV, Excel, JSON) and the system analyzes the data structure to suggest an optimal database schema, engaging in conversation to clarify relationships and constraints that can't be inferred from the data alone.

**Why this priority**: Many users have existing data in spreadsheets or flat files and want to migrate to a proper database. This provides immediate value by analyzing their actual data and suggesting a schema that fits their existing information. Builds on P1's conversation capability. REPL mode allows seamless file upload mid-conversation.

**Independent Test**: User in REPL types `\schema upload customers.csv`, system analyzes the columns and data types, asks clarifying questions about relationships to other entities, and produces a schema that accurately represents the uploaded data structure.

**Acceptance Scenarios**:

1. **Given** a user is in REPL with a CSV file at customers.csv, **When** they type `\schema upload customers.csv` (file has columns: customer_id, name, email, phone, order_date, product, quantity, price), **Then** the system analyzes the structure and identifies that this appears to contain multiple entities (customers, orders, products) combined
2. **Given** the system has identified multiple entities in one file, **When** it asks "Should orders and customers be separate tables?", **Then** the user can confirm and the system proposes a normalized schema with three tables: customers, orders, and products with appropriate relationships
3. **Given** the user has uploaded multiple CSV files via `\schema upload customers.csv` then `\schema upload orders.csv`, **When** the system detects common columns (customer_id), **Then** it automatically suggests foreign key relationships and asks for confirmation
4. **Given** a schema has been designed from uploaded files, **When** the user types `\schema show mapping`, **Then** they can see how their original CSV columns map to the new database tables and fields

---

### User Story 3 - Iterative Schema Refinement (Priority: P3)

Users in REPL iteratively refine their schema design through multiple conversation rounds, asking "what if" questions, using `\schema history` to compare alternatives, and making changes before finalizing the design.

**Why this priority**: Schema design is rarely perfect on the first attempt. This allows users to explore different design approaches and understand the trade-offs between different schema structures before committing to implementation. REPL's conversational nature makes iteration seamless. Enhances the core P1/P2 capabilities with iteration support.

**Independent Test**: User can take an existing schema proposal in REPL, ask questions like "what if I denormalize this for performance?" or "how would I add multi-tenancy?", use `\schema history` to view previous versions, receive alternative schema designs with explanations of trade-offs, and iterate until satisfied.

**Acceptance Scenarios**:

1. **Given** a normalized schema with separate customer_addresses table in REPL, **When** the user asks "what would happen if I put addresses directly in the customers table?", **Then** the system shows the denormalized alternative and explains trade-offs (simpler queries vs. inability to store multiple addresses)
2. **Given** a proposed schema in REPL, **When** the user asks "how do I add support for multiple currencies?", **Then** the system suggests schema modifications (add currency field, add exchange_rates table) with explanations
3. **Given** a conversation history with multiple schema iterations, **When** the user types `\schema history` and selects "version 2", **Then** the system retrieves and displays the previous schema version for comparison
4. **Given** multiple alternative designs have been explored, **When** the user types `\schema finalize`, **Then** the system marks the selected design as final and prepares it for implementation

---

### User Story 4 - Schema Implementation and Validation (Priority: P4)

Users in REPL implement their finalized schema using `\schema implement <database>` to generate and execute database migration scripts, with the system validating the schema against best practices and warning about potential issues.

**Why this priority**: This is the final step that transforms the conversational design into actual database tables. While important, it depends on having a finalized schema from the earlier stories, making it lower priority for initial MVP. REPL provides natural environment for reviewing and confirming DDL before execution. Can be implemented after P1-P3 are validated.

**Independent Test**: User can take a finalized schema design in REPL, type `\schema implement postgresql`, review the generated DDL statements, confirm execution, and have the schema applied to their connected database with validation and rollback capability.

**Acceptance Scenarios**:

1. **Given** a finalized schema design in REPL, **When** the user types `\schema implement postgresql`, **Then** the system generates PostgreSQL-specific DDL statements with appropriate data types, constraints, and indexes
2. **Given** generated DDL statements are displayed, **When** the user reviews the SQL using `\schema show ddl`, **Then** they can see explanations of each statement and warnings about potential issues (e.g., "Adding this index may take time on large tables")
3. **Given** DDL statements are ready and user types `\schema execute`, **When** the user confirms execution, **Then** the system applies the schema changes in a transaction with the ability to rollback if errors occur
4. **Given** a schema has been implemented, **When** the user types `\schema validate`, **Then** the system checks that all tables, relationships, and constraints exist as designed and reports any discrepancies

---

### REPL Commands

The feature introduces the following new REPL commands for schema design:

| Command | Description | Example |
|---------|-------------|---------|
| `\schema design` | Start a new schema design conversation | `\schema design` |
| `\schema upload <file>` | Upload and analyze data file(s) | `\schema upload customers.csv` |
| `\schema show [view]` | Display current schema (views: erd, ddl, mapping, text) | `\schema show erd` |
| `\schema history` | View previous schema versions | `\schema history` |
| `\schema finalize` | Mark current design as final | `\schema finalize` |
| `\schema save <name>` | Save schema design for later | `\schema save ecommerce_v1` |
| `\schema load <name>` | Load a saved schema design | `\schema load ecommerce_v1` |
| `\schema implement <db>` | Generate DDL for database type | `\schema implement postgresql` |
| `\schema execute` | Execute generated DDL statements | `\schema execute` |
| `\schema validate` | Validate implemented schema | `\schema validate` |
| `\schema export <file>` | Export schema definition | `\schema export schema.json` |
| `\schema reset` | Start over with new design | `\schema reset` |
| `\schema help` | Show schema command help | `\schema help` |

**Usage Flow Example:**
```
querynl> \schema design
System: Let's design your database schema! What would you like to track?

querynl> I need to track customers and their orders

System: Great! A few questions:
1. Should customers be able to have multiple addresses?
2. Can an order contain multiple products?

querynl> yes to both

System: Here's my proposed schema... [displays tables]

querynl> \schema show erd
[Displays ER diagram]

querynl> \schema finalize

querynl> \schema implement postgresql
[Shows DDL statements]

querynl> \schema execute
Ready to create 5 tables. Continue? (yes/no): yes
✓ Schema implemented successfully!
```

---

### Edge Cases

- What happens when a user uploads a very large CSV file (>100MB) for schema analysis in REPL?
- How does the system handle CSV files with inconsistent data types in the same column?
- What if the user uploads files with circular foreign key relationships?
- How does the system handle ambiguous file uploads where relationships aren't clear (e.g., two files with similar column names but no obvious foreign keys)?
- What happens if the user describes a schema that violates database normalization principles? Should the system warn them?
- How does the system handle schema designs that conflict with existing tables in the connected database?
- What if the user wants to design a schema for a database type (MongoDB) that doesn't use traditional tables and foreign keys?
- How does the system handle very complex schemas with 20+ tables and multiple junction tables?
- What happens when the user changes their mind mid-conversation and wants to start over? (Use `\schema reset`)
- How does the system handle incomplete data files (missing headers, empty columns)?
- What happens if the user exits REPL mid-conversation? Should the session be recoverable?

## Requirements

### Functional Requirements

#### REPL Mode Interface

- **FR-001**: System MUST provide schema design functionality exclusively through REPL mode via `\schema` commands
- **FR-002**: System MUST accept natural language descriptions of data requirements via `\schema design` and engage in multi-turn conversations to clarify schema design
- **FR-003**: System MUST ask intelligent follow-up questions to clarify ambiguous requirements (e.g., "Should customers be able to have multiple addresses?" when address is mentioned)
- **FR-004**: System MUST remember the context of the entire REPL session conversation and reference previous design decisions
- **FR-005**: System MUST explain schema design decisions in plain language, avoiding database jargon
- **FR-006**: System MUST allow users to request explanations of database concepts (e.g., "what is a foreign key?" or "why do I need an index?")

#### File Upload and Analysis

- **FR-007**: System MUST support uploading data files in CSV, Excel (.xlsx), and JSON formats via `\schema upload <file>` in REPL
- **FR-008**: System MUST analyze uploaded file structure to infer column names, data types, and relationships
- **FR-009**: System MUST detect potential entity relationships across multiple uploaded files by analyzing common columns
- **FR-010**: System MUST handle files with missing or inconsistent data gracefully, reporting data quality issues to the user
- **FR-011**: System MUST support uploading multiple files in a single REPL session to analyze cross-file relationships
- **FR-012**: System MUST show users how their original file columns map to proposed database tables and fields via `\schema show mapping`

#### Schema Design and Proposal

- **FR-013**: System MUST generate normalized database schemas following industry best practices (3NF by default)
- **FR-014**: System MUST identify and propose primary keys, foreign keys, and indexes based on usage patterns
- **FR-015**: System MUST support designing schemas for multiple database types (PostgreSQL, MySQL, SQLite, MongoDB)
- **FR-016**: System MUST generate schema proposals that include table names, column names, data types, constraints, and relationships
- **FR-017**: System MUST display schema designs in multiple formats via `\schema show [view]`: visual ER diagrams, textual descriptions, and DDL statements
- **FR-018**: System MUST allow users to view and compare different schema design iterations via `\schema history`
- **FR-019**: System MUST support schema versioning with `\schema save <name>` and `\schema load <name>`, allowing users to go back to previous designs

#### Schema Refinement

- **FR-020**: Users MUST be able to request changes to proposed schemas through natural language in REPL ("add a column for", "change this to", "remove that table")
- **FR-021**: System MUST explain trade-offs when users request denormalization or other design alternatives
- **FR-022**: System MUST validate schema changes against best practices and warn about potential issues
- **FR-023**: Users MUST be able to ask "what if" questions and receive alternative schema designs with explanations

#### Schema Implementation

- **FR-024**: System MUST generate database-specific DDL statements (CREATE TABLE, ALTER TABLE, CREATE INDEX) for finalized schemas via `\schema implement <database>`
- **FR-025**: System MUST show users the exact SQL via `\schema show ddl` that will be executed before implementation
- **FR-026**: System MUST validate that the connected database doesn't already have conflicting tables or constraints before executing via `\schema validate`
- **FR-027**: System MUST execute schema changes in a transaction with rollback capability when user runs `\schema execute`
- **FR-028**: System MUST verify that the implemented schema matches the design specification
- **FR-029**: System MUST support incremental schema changes (adding tables to existing schema) as well as creating new schemas from scratch

#### Data Migration Assistance

- **FR-030**: System MUST generate data migration scripts to populate the new schema from uploaded files
- **FR-031**: System MUST validate that sample data from uploaded files can be successfully inserted into the new schema
- **FR-032**: System MUST report data type mismatches or constraint violations before attempting migration

### Key Entities

- **Schema Design Session**: Represents an active or historical conversation about designing a database schema, including all conversation turns, uploaded files, proposed schemas, and user decisions
- **Schema Proposal**: A specific version of a database schema design, including tables, columns, data types, constraints, relationships, and metadata about why design decisions were made
- **Uploaded Data File**: A user-provided data file (CSV, Excel, JSON) with metadata about structure analysis, inferred data types, and detected relationships
- **Schema Entity**: Represents a table in the proposed schema with its columns, data types, constraints, and relationships to other entities
- **Schema Relationship**: Represents foreign key relationships, junction tables, and other connections between schema entities
- **Conversation Turn**: A single exchange in the schema design conversation, including user input, system analysis, clarifying questions, and schema proposals

### Non-Functional Requirements

- **NFR-001**: System MUST respond to schema design questions within 5 seconds for typical conversations
- **NFR-002**: System MUST process and analyze data files up to 100MB in size within 30 seconds
- **NFR-003**: System MUST support concurrent schema design sessions for multiple users
- **NFR-004**: Schema designs MUST be persisted and retrievable for at least 90 days
- **NFR-005**: System MUST handle unexpected conversation interruptions gracefully, allowing users to resume from their last interaction

## Success Criteria

### Measurable Outcomes

- **SC-001**: Users can design a complete database schema (3-5 tables with relationships) through conversation alone in under 10 minutes
- **SC-002**: Users uploading data files receive initial schema proposals within 30 seconds of file analysis completion
- **SC-003**: 85% of users successfully create and implement a working schema without requiring external documentation or support
- **SC-004**: Users can iterate through at least 3 different schema design alternatives in a single session
- **SC-005**: System generates syntactically correct DDL statements for all supported database types 100% of the time
- **SC-006**: 90% of users report understanding the schema design decisions made by the system (measured through post-feature survey)
- **SC-007**: Users can complete the entire workflow (describe → design → implement) for a simple schema (2-3 tables) in under 15 minutes from start to finish

## Scope

### In Scope

- **REPL-only interface** for all schema design functionality via `\schema` commands
- Natural language conversation for schema design in interactive REPL mode
- CSV, Excel, and JSON file upload and analysis via `\schema upload` in REPL
- Schema normalization and best practice recommendations
- Visual ER diagram generation via `\schema show erd`
- DDL generation for PostgreSQL, MySQL, SQLite via `\schema implement <database>`
- Basic data migration from uploaded files
- Schema versioning and comparison via `\schema save/load/history`
- Interactive schema refinement through conversation in REPL

### Out of Scope (for MVP)

- **CLI batch mode** for non-interactive automation (planned for post-MVP as future enhancement)
- Advanced database optimization (query performance tuning, index optimization beyond basics)
- Schema migration for existing production databases with live data
- Complex data transformations during migration (ETL logic)
- Support for extremely complex schemas (>50 tables)
- Real-time collaborative schema design with multiple users
- Automated schema evolution based on application usage patterns
- Support for NoSQL schema design patterns beyond basic MongoDB collections
- Integration with ORM frameworks (Prisma, TypeORM, SQLAlchemy)
- Automatic data profiling and cleansing

## Assumptions

- Users have a connected database instance available for schema implementation
- Users provide sample data files that are representative of their actual data structure
- Users have basic familiarity with database concepts (tables, columns) but not necessarily SQL
- The system has access to an LLM service for natural language understanding and generation
- Database connections use the existing QueryNL connection management system
- Schema design sessions are single-user (no real-time collaboration)
- Default normalization level is 3NF unless user explicitly requests denormalization
- File uploads are limited to 100MB to ensure reasonable processing times
- The system can access existing database metadata (INFORMATION_SCHEMA) to detect conflicts
- MongoDB schema design will follow document-oriented patterns (nested documents, arrays) rather than forcing relational structure

## Dependencies

- Existing QueryNL database connection infrastructure
- LLM service (OpenAI or Anthropic) for natural language processing
- File upload handling via REPL commands (file paths provided by user, processed locally)
- Schema visualization library for ER diagram generation (Mermaid or similar for text-based ER diagrams)
- Database introspection capability (already exists in QueryNL via [schema_introspection.py](../../src/cli/schema_introspection.py))
- CSV/Excel/JSON parsing libraries (pandas or similar)
- REPL infrastructure (already exists in QueryNL via [repl.py](../../src/cli/repl.py))

## Open Questions

None - all critical decisions have reasonable defaults documented in Assumptions section.

## Risk Assessment

### High Risk

- **Schema design quality**: AI-generated schemas may not always follow best practices or may miss important constraints. **Mitigation**: Always show schemas to users before implementation, provide explanations, and validate against database-specific rules.
- **Data loss during migration**: Incorrect migration scripts could lose or corrupt user data. **Mitigation**: Always work with user-provided sample data first, show SQL before execution, use transactions with rollback, and recommend testing on non-production databases.

### Medium Risk

- **Large file processing**: Very large CSV files could cause performance issues or timeouts. **Mitigation**: Implement streaming file processing, set reasonable file size limits (100MB), and provide progress indicators.
- **Ambiguous user requirements**: Natural language descriptions may be unclear or inconsistent. **Mitigation**: Ask clarifying questions, show schema proposals early and often, and support iterative refinement.

### Low Risk

- **Database compatibility**: Different databases have different DDL syntax and features. **Mitigation**: Use well-tested DDL generation libraries, clearly indicate which database type the schema is for, and test generated SQL before execution.

## Future Enhancements (Post-MVP)

- **CLI batch mode** for non-conversational automation workflows (e.g., `querynl schema from-file customers.csv orders.csv --output schema.sql --database postgresql`)
  - Support piping file analysis output to schema generation
  - Enable scripted/automated schema generation without interactive conversation
  - Provide flags for normalization level, database type, and output format
  - Allow pre-configured schema templates for common patterns
- Schema optimization recommendations based on query patterns
- Automatic index suggestions based on query performance analysis
- Support for complex data types (arrays, JSON columns, geometric types)
- Schema comparison and diff tools for existing vs. proposed schemas
- Data quality profiling and cleaning suggestions during file analysis
- Support for time-series and specialized database schema patterns
- Integration with database migration tools (Alembic, Flyway, Liquibase)
- Export schema designs to various formats (Prisma schema, TypeORM entities, SQLAlchemy models)
- AI-powered data modeling best practice suggestions based on domain (e-commerce, SaaS, etc.)
