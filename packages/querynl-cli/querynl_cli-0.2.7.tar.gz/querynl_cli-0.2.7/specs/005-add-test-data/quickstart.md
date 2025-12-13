# Quickstart: Test Data Generation

**Feature**: Test Data Generation for Schema Design Mode
**Target Users**: QueryNL CLI users who have created database schemas and want to populate them with test data

## Overview

This feature allows users to generate realistic test data for database schemas using natural language commands. The system uses an LLM to understand the schema and create a data generation plan, then executes that plan using the Faker library to produce realistic sample data.

## Installation

### Prerequisites
- Python 3.10 or higher
- QueryNL CLI installed
- Active database connection (MySQL, PostgreSQL, or SQLite)

### New Dependencies

Add to `requirements.txt`:
```bash
Faker>=38.2.0
toposort>=1.10
```

Install:
```bash
pip install -r requirements.txt
```

## Basic Usage

### Step 1: Create a Schema

First, create a database schema using the existing `\schema` feature:

```sql
querynl> \schema design

Schema Designer> I need a blog with users, posts, and comments

[System generates schema proposal]

Schema Designer> finalize

[Schema created in database]
```

### Step 2: Generate Test Data

Request test data using natural language:

```sql
querynl (blog-db)> add some sample data to these tables

[INFO] Analyzing schema...
[INFO] Generating test data plan...

Generated Plan:
- customers: 15 records
- posts: 45 records
- comments: 120 records

Total: 180 records across 3 tables

[INFO] Generating test data...
[████████████████████████] 100% 180/180 records (1,234 rec/sec)

✓ Successfully inserted 180 records
```

### Step 3: Verify Data

Query the generated data:

```sql
querynl (blog-db)> show me some users and their posts

┌────┬─────────────────┬─────────────────────────┬──────┐
│ id │ name            │ email                   │ posts│
├────┼─────────────────┼─────────────────────────┼──────┤
│  1 │ John Doe        │ john.doe@example.com    │    3 │
│  2 │ Jane Smith      │ jane.smith@example.com  │    5 │
│  3 │ Bob Johnson     │ bob.johnson@example.com │    2 │
└────┴─────────────────┴─────────────────────────┴──────┘
```

## Advanced Usage

### Specify Record Counts

Control how much data is generated:

```sql
querynl> add 100 customers and 500 orders
```

```sql
querynl> generate 1000 sample users
```

### Specify Domain Context

Get more realistic data for specific domains:

```sql
querynl> add sample e-commerce products and orders
```

```sql
querynl> populate with sample medical records data
```

### Clear and Regenerate

Clear existing test data:

```sql
querynl> delete all data from these tables

⚠ Warning: This will delete all data from 3 tables
Continue? (y/N): y

✓ Deleted 180 records
```

Then regenerate:

```sql
querynl> add 50 records per table
```

## Natural Language Examples

The system understands various phrasings:

```sql
# Simple requests
querynl> add test data
querynl> populate with sample data
querynl> generate some fake data

# With quantities
querynl> add 100 sample users
querynl> create 50 customers and 200 orders
querynl> populate each table with 25 records

# With context
querynl> add realistic e-commerce product data
querynl> generate sample social media posts
querynl> create fake customer records

# Specific tables
querynl> add sample data to customers table
querynl> populate products and orders tables
```

## Features

### Automatic Foreign Key Handling

The system automatically:
- Detects foreign key relationships
- Generates parent records before child records
- Assigns valid foreign key references

Example:
```
orders.customer_id → references existing customer.id
order_items.order_id → references existing order.id
```

### Realistic Data Generation

Generated data includes:
- **Names**: John Doe, Jane Smith (using Faker)
- **Emails**: john.doe@example.com (unique)
- **Addresses**: 123 Main St, Springfield
- **Dates**: Recent realistic dates
- **Phone numbers**: (555) 123-4567
- **Product names**: Contextually appropriate names
- **Prices**: Realistic price ranges

### Constraint Compliance

The system respects:
- **NOT NULL**: Always provides values for required columns
- **UNIQUE**: Generates distinct values (no duplicates)
- **FOREIGN KEYS**: References existing parent records
- **CHECK**: Satisfies check constraints (e.g., age >= 18)
- **ENUM**: Selects from valid enum values

### Progress Indication

For large datasets, shows real-time progress:

```
Inserting test data...
[███████████░░░░░] 65% 6,500/10,000 records (1,234 rec/sec) • 0:00:08 • 0:00:04 remaining
```

### Error Handling

If errors occur, you get detailed information:

```
✓ Successfully inserted 95 records
✗ Failed to insert 5 records

Failed Records:
  • UNIQUE constraint violation in column 'email'
    Record: {name: 'John Doe', email: 'duplicate@example.com'}

Options:
  1. Keep successful inserts and continue
  2. Rollback all changes
  3. Export failed records to fix manually
  4. Retry failed records
```

## Performance

Expected performance on typical hardware:

| Dataset Size | Database | Time | Speed |
|--------------|----------|------|-------|
| 1,000 records | PostgreSQL | ~2-3 seconds | ~400 rec/sec |
| 10,000 records | PostgreSQL | ~10-15 seconds | ~800 rec/sec |
| 100,000 records | PostgreSQL | ~90-120 seconds | ~1,000 rec/sec |
| 1,000 records | MySQL | ~2-4 seconds | ~300 rec/sec |
| 10,000 records | MySQL | ~15-20 seconds | ~600 rec/sec |
| 1,000 records | SQLite | ~1-2 seconds | ~600 rec/sec |
| 10,000 records | SQLite | ~8-12 seconds | ~1,000 rec/sec |

Performance tips:
- SQLite with WAL mode is fastest for local testing
- PostgreSQL handles large batches efficiently
- MySQL performance depends on `innodb_log_file_size` setting

## Troubleshooting

### "No schema found"

**Problem**: Tried to generate data without a schema

**Solution**: Create a schema first using `\schema design` or connect to a database with existing tables

### "Foreign key constraint violation"

**Problem**: Circular foreign key dependencies detected

**Solution**: The system will automatically handle this by temporarily disabling FK checks. If you see this error, report it as a bug.

### "Unique constraint violation"

**Problem**: Generated duplicate values for unique columns

**Solution**: The system should prevent this. If it occurs:
1. Check if you're generating > 100K records with unique constraints
2. Clear test data and regenerate with smaller counts
3. Report as a bug if < 100K records

### "Cannot generate valid value for column"

**Problem**: Column has complex constraints the system doesn't understand

**Solution**:
1. Check the constraint definition (e.g., CHECK constraints)
2. Temporarily remove the constraint for testing
3. Request manual INSERT for specific values

### "Operation cancelled by user"

**Problem**: Pressed Ctrl+C during generation

**Solution**: This is normal. The system rolled back incomplete changes. You can retry with:
- Smaller batch sizes
- Fewer tables
- Continue from where it stopped (if prompted)

## Configuration

### Default Record Counts

By default, the system generates:
- **10-20 records** per table when no count specified
- **Proportional counts** for related tables (e.g., 10 users → 30 posts → 90 comments)

### Batch Sizes

The system uses optimal batch sizes per database:
- **PostgreSQL**: 10,000 records per batch
- **MySQL**: 1,000 records per batch
- **SQLite**: 10,000 records per batch

These are automatic and don't require configuration.

### Transaction Behavior

- **< 10K records**: Single transaction (all-or-nothing)
- **> 10K records**: Batched transactions (commit every 10K)

## Integration with Schema Design

Test data generation integrates seamlessly with schema design:

```sql
# Design schema
querynl> \schema design
Schema Designer> blog with users and posts
Schema Designer> finalize

# Immediately populate
querynl> add test data

# Iterate on schema
querynl> \schema modify
Schema Designer> add likes table for posts
Schema Designer> finalize

# Regenerate with new table
querynl> add likes data for existing posts
```

## Best Practices

### 1. Start Small

Generate small datasets first to verify schema:
```sql
querynl> add 10 records per table
```

Then scale up once confirmed:
```sql
querynl> add 1000 records per table
```

### 2. Use Domain Context

Get more realistic data by specifying domain:
```sql
querynl> add e-commerce sample data
```

vs generic:
```sql
querynl> add sample data
```

### 3. Verify Foreign Keys

After generation, check relationships:
```sql
querynl> show me orders without customers
```

Should return no results if FKs are correct.

### 4. Clear Between Iterations

When iterating on schema design:
```sql
querynl> delete all test data
querynl> \schema modify
[make changes]
querynl> add fresh test data
```

### 5. Use Large Datasets for Performance Testing

Test query performance with realistic data volumes:
```sql
querynl> add 100000 products and 1000000 orders
```

Then test queries:
```sql
querynl> find top 10 customers by order count
```

## Next Steps

- [Full API Documentation](./contracts/test_data_generator_api.py)
- [Data Model Details](./data-model.md)
- [Implementation Plan](./plan.md)
- [Research Notes](./research.md)

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review generated SQL (displayed before execution)
3. Report bugs with schema details and error messages
4. Ask in natural language: `querynl> help with test data generation`
