# Research: Test Data Generation for Database Schemas

**Date**: 2025-11-22
**Feature**: Test Data Generation for Schema Design Mode

## Executive Summary

Research identified the root cause of the user's problem: the LLM was generating INSERT statements with parameterized placeholders (`?`) which caused SQL syntax errors. The recommended solution is a **hybrid architecture** where the LLM generates a data generation *plan* (not SQL), and Python code executes that plan using the Faker library to generate realistic test data with proper database-specific escaping.

## Key Decisions

### 1. Data Generation Library

**Decision**: Use **Faker 38.2.0+** as primary library with optional Mimesis for performance-critical scenarios

**Rationale**:
- Industry standard with extensive provider ecosystem (names, emails, addresses, phone numbers, dates, etc.)
- Supports 50+ locales for realistic international data
- Built-in `.unique` property for handling unique constraints
- Good performance for typical test data volumes (10K-100K records)
- Extensive documentation and active community support
- No hard dependencies, easy to integrate

**Performance Characteristics**:
- 10K records: < 5 seconds
- 100K records: ~30-60 seconds with batching
- Can use Mimesis (12-15x faster) for 1M+ record scenarios

**Alternatives Considered**:
- **Mimesis**: Faster but fewer community resources and less feature-rich
- **Custom generators**: Too much development overhead for standard data types
- **Pure LLM generation**: Causes parameterized query errors, slow, expensive

### 2. LLM Integration Pattern

**Decision**: **Hybrid Model** - LLM generates plan, Python executes with actual values

**Rationale**:
- Avoids parameterized query errors that plagued the user's original attempt
- Keeps LLM focused on its strength: understanding schema semantics
- Python code handles database-specific escaping and syntax
- Faster execution (no LLM latency per INSERT statement)
- More reliable (deterministic value generation vs. LLM hallucination)

**LLM Responsibilities**:
1. Analyze schema and understand table relationships
2. Determine semantic meaning of columns (e.g., `email` → email address, `city` → city name)
3. Create data generation plan specifying Faker providers for each column
4. Define record quantities and insertion order (respecting foreign keys)
5. Explain strategy to user in natural language

**Python Code Responsibilities**:
1. Execute the LLM-generated plan
2. Generate actual values using Faker/Mimesis
3. Build INSERT statements with proper escaping
4. Handle database-specific syntax (MySQL vs PostgreSQL vs SQLite)
5. Manage foreign key references and track generated IDs
6. Execute SQL against the database

**Example Plan Format**:
```json
{
  "tables": [
    {
      "name": "customers",
      "record_count": 100,
      "columns": [
        {"name": "name", "faker_provider": "name", "params": {}},
        {"name": "email", "faker_provider": "email", "params": {}},
        {"name": "age", "faker_provider": "random_int", "params": {"min": 18, "max": 80}}
      ]
    }
  ],
  "insertion_order": ["customers", "orders", "order_items"],
  "rationale": "Generate customers first, then orders, then order items to satisfy FK constraints"
}
```

### 3. INSERT Statement Generation Strategy

**Decision**: Generate INSERT statements with **literal values** (not parameterized), using database-specific escaping

**Rationale**:
- Parameterized queries (`INSERT INTO users VALUES (?, ?, ?)`) cause SQL syntax errors
- Literal values work directly without parameter binding
- Can use database-specific escaping for correctness and security
- SQLAlchemy's `literal_binds` provides cross-database compatibility

**Database-Specific Escaping**:

| Database | Boolean | String Escaping | Auto-increment | Date Format |
|----------|---------|----------------|----------------|-------------|
| MySQL | `0` or `1` | Backslash escape: `\'` | Skip column | ISO 8601 `'2025-11-23'` |
| PostgreSQL | `TRUE` or `FALSE` | Double quotes: `''` | Skip column | ISO 8601 `'2025-11-23'` |
| SQLite | `0` or `1` | Double quotes: `''` | Skip column | ISO 8601 text `'2025-11-23'` |

**Performance Optimization**: Use multi-row INSERT statements (batch 500-1000 rows per statement) for optimal performance:
```sql
INSERT INTO customers (name, email) VALUES
    ('John Doe', 'john@example.com'),
    ('Jane Smith', 'jane@example.com'),
    ... (500-1000 rows)
```

### 4. Foreign Key Dependency Handling

**Decision**: Use **topological sort** (Kahn's algorithm) to determine table insertion order

**Rationale**:
- Ensures parent records exist before child records (satisfies FK constraints)
- Standard algorithm with proven correctness
- Handles complex multi-level dependencies automatically
- Detects circular dependencies

**Implementation Approach**:
```python
from toposort import toposort_flatten

# Build dependency graph: table -> set of tables it references
dependencies = {
    'orders': {'customers', 'products'},
    'customers': set(),
    'products': set(),
    'order_items': {'orders', 'products'}
}

# Get insertion order
sorted_tables = list(toposort_flatten(dependencies))
# Result: ['customers', 'products', 'orders', 'order_items']
```

**Circular Dependency Handling**:
- **Detection**: Topological sort fails if cycle exists
- **Solution**: Temporarily disable foreign key checks, insert all data, re-enable checks
- **Alternative**: Two-pass insertion (insert with NULL FKs, then UPDATE to set FKs)

**Database-Specific FK Disabling**:
```sql
-- MySQL
SET FOREIGN_KEY_CHECKS = 0;
-- inserts here
SET FOREIGN_KEY_CHECKS = 1;

-- PostgreSQL
SET CONSTRAINTS ALL DEFERRED;
-- inserts here
COMMIT;

-- SQLite
PRAGMA foreign_keys = OFF;
-- inserts here
PRAGMA foreign_keys = ON;
```

### 5. Unique Constraint Handling

**Decision**: Use Faker's `.unique` property with sequential suffixes for large datasets

**Rationale**:
- Faker's built-in uniqueness tracking prevents duplicates
- Sequential suffixes scale beyond Faker's built-in limits
- Simple and reliable for test data purposes

**Implementation**:
```python
from faker import Faker

fake = Faker()

# For small datasets (< 10K unique values)
emails = [fake.unique.email() for _ in range(1000)]
fake.unique.clear()  # Clear cache when done

# For large datasets (> 10K unique values)
def generate_unique_with_suffix(faker_method, count):
    for i in range(count):
        base_value = faker_method()
        yield f"{base_value}_{i}"

emails = list(generate_unique_with_suffix(fake.email, 100000))
```

**Limits to Know**:
- Faker English names: ~750K combinations (1000 last names × 750 first names)
- Emails: Unlimited with numeric suffixes
- UUIDs: Use `uuid.uuid4()` for guaranteed uniqueness

### 6. Transaction Management Strategy

**Decision**: Use **batched transactions** with commits every 10,000-50,000 records

**Rationale**:
- Balances performance with manageable rollback scope
- Allows progress reporting without blocking for entire operation
- Reduces memory consumption via periodic flushes
- Enables partial recovery if errors occur late in the process

**Commit Patterns**:

| Dataset Size | Strategy | Commit Frequency | Rationale |
|--------------|----------|------------------|-----------|
| < 10K records | Single transaction | At end | ACID guarantees, fast enough |
| 10K-100K records | Batched transactions | Every 10K records | Manageable rollback scope |
| > 100K records | Batched transactions | Every 50K records | Performance optimization |

**Implementation**:
```python
# Single transaction with periodic flushes (< 10K records)
with session.begin():
    for batch in chunk_data(records, 10000):
        session.bulk_insert_mappings(Model, batch, return_defaults=False)
        session.flush()  # Releases memory, stays in transaction

# Batched transactions (> 10K records)
for batch in chunk_data(records, 10000):
    with session.begin():
        session.bulk_insert_mappings(Model, batch, return_defaults=False)
```

**Database-Specific Considerations**:
- **PostgreSQL**: No hard transaction size limits, use larger batches (10K-50K)
- **MySQL**: Limited by `innodb_log_file_size` (recommend 256MB+), use 10K batches
- **SQLite**: Use `PRAGMA journal_mode = WAL` for 2x INSERT speed improvement

### 7. Error Handling and Recovery

**Decision**: **Savepoint-based recovery** with individual record fallback

**Rationale**:
- Allows batch operations to fail gracefully without losing all progress
- Provides detailed error reporting at record level
- Gives users options to continue, rollback, or export failed records
- Maintains transaction integrity while maximizing successful insertions

**Error Handling Flow**:
1. **Batch-level**: Try inserting entire batch (1000 records)
2. **Constraint violation**: Rollback to savepoint, retry records individually
3. **Individual failures**: Collect detailed error information (constraint, column, value)
4. **User decision**: Present options (continue, rollback all, export errors, retry)

**Implementation Pattern**:
```python
def insert_with_error_recovery(session, table, records, batch_size=1000):
    stats = {'successful': 0, 'failed': 0, 'errors': []}

    for batch_num, batch in enumerate(chunk_data(records, batch_size)):
        savepoint = f"batch_{batch_num}"
        try:
            session.execute(f"SAVEPOINT {savepoint}")
            session.bulk_insert_mappings(table, batch, return_defaults=False)
            session.execute(f"RELEASE SAVEPOINT {savepoint}")
            stats['successful'] += len(batch)
        except IntegrityError as e:
            session.execute(f"ROLLBACK TO SAVEPOINT {savepoint}")
            # Retry individual records and collect failures
            stats.update(handle_individual_records(session, table, batch, e))

    return stats
```

### 8. Performance Optimization

**Decision**: Use **`bulk_insert_mappings()` with `return_defaults=False`** for optimal performance

**Rationale**:
- 7x faster than standard ORM `add_all()` method
- Minimal memory overhead compared to full ORM objects
- Returns no defaults (auto-increment IDs), which is acceptable for test data
- Cross-database compatible via SQLAlchemy

**Performance Benchmarks (100,000 records)**:
- Raw psycopg2: ~0.166s (baseline)
- SQLAlchemy Core: ~0.207s (1.25x)
- `bulk_insert_mappings()`: ~0.321s (1.93x)
- Standard ORM `add_all()`: ~2.394s (14.4x)

**Batch Size Recommendations**:
- **PostgreSQL**: 1,000-10,000 rows per INSERT statement
- **MySQL**: 1,000 rows per INSERT statement
- **SQLite**: 10,000 rows per INSERT statement

### 9. Progress UX Pattern

**Decision**: Use **Rich library's Progress component** with real-time updates and cancellation support

**Rationale**:
- QueryNL already uses Rich for terminal UI (consistency)
- Provides professional progress bars with speed, ETA, elapsed time
- Supports nested progress for multi-table operations
- Handles Ctrl+C gracefully for user cancellation

**Progress Display Components**:
- Spinner: Visual indication of activity
- Progress bar: Visual representation of completion
- Task progress: Percentage complete
- M of N complete: "5,000 / 10,000 records"
- Speed: "1,234 records/sec"
- Time elapsed: "0:00:15"
- Time remaining: "0:00:45 remaining"

**Cancellation Handling**:
- First Ctrl+C: Finish current batch, rollback transaction, report partial results
- Second Ctrl+C: Force exit (warn user of potential data inconsistency)

## Dependencies to Add

Update `requirements.txt`:
```
Faker>=38.2.0
toposort>=1.10
# Optional: mimesis>=18.0.0  # For performance-critical scenarios (1M+ records)
```

## Implementation Roadmap

### Phase 1: MVP (Core Functionality)
1. Implement test data generator with Faker integration
2. Support MySQL, PostgreSQL, SQLite
3. Handle simple schemas (no circular FKs)
4. LLM generates plan, Python executes with literal values
5. Basic error reporting

### Phase 2: Enhancements
1. Add topological sort for complex FK relationships
2. Handle circular dependencies with FK checks disable
3. Support ENUM and CHECK constraints
4. Add batch INSERT optimization
5. Implement Rich progress bars

### Phase 3: Advanced Features
1. Support very large datasets (1M+ records) with Mimesis
2. Add savepoint-based error recovery
3. Support custom data distributions (e.g., 80% active, 20% inactive)
4. Add data correlation (related records have similar timestamps)
5. Implement user recovery options (continue/rollback/export)

## Open Questions Resolved

**Q: Should we use LLM to generate INSERT statements directly?**
A: No. LLM generates a plan (JSON), Python code executes it with Faker. This avoids parameterized query errors.

**Q: How to handle foreign key dependencies?**
A: Use topological sort (Kahn's algorithm) to determine insertion order. Use `toposort` library for implementation.

**Q: What batch size for optimal performance?**
A: PostgreSQL: 1K-10K, MySQL: 1K, SQLite: 10K. Start conservative and scale based on testing.

**Q: How to handle constraint violations?**
A: Use savepoint-based recovery with fallback to individual record insertion. Report detailed errors to user.

**Q: How to show progress for long operations?**
A: Use Rich Progress component with speed, ETA, and cancellation support (Ctrl+C).

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| LLM generates invalid Faker providers | Validate plan before execution, fallback to sensible defaults |
| Large datasets cause memory issues | Use batched transactions with periodic flushes every 10K records |
| Circular FK dependencies block insertion | Detect cycles, temporarily disable FK checks during insertion |
| User cancels operation mid-insert | Implement graceful cancellation with rollback, report partial results |
| Database-specific syntax differences | Abstract via database dialect layer, test against all supported DBs |
| Unique constraint violations | Use Faker.unique + sequential suffixes, track generated values |

## References

- Faker Documentation: https://faker.readthedocs.io/
- toposort library: https://pypi.org/project/toposort/
- Rich Progress Bars: https://rich.readthedocs.io/en/stable/progress.html
- SQLAlchemy Bulk Operations: https://docs.sqlalchemy.org/en/14/orm/persistence_techniques.html#bulk-operations
- MySQL InnoDB Transaction Size: https://dev.mysql.com/doc/refman/8.0/en/innodb-redo-log.html
- PostgreSQL COPY Performance: https://www.postgresql.org/docs/current/sql-copy.html
