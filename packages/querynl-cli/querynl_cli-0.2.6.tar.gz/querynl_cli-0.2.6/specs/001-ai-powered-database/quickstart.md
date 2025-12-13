# QueryNL Quickstart Guide

**Version**: 1.0.0
**Date**: 2025-10-11
**Purpose**: Developer guide for getting QueryNL running locally

---

## Prerequisites

### Required Software

- **Python**: 3.11 or higher
- **Node.js**: 18.x or higher
- **npm**: 9.x or higher
- **VS Code**: 1.80 or higher (last 12 months)
- **Git**: For version control

### Optional (for testing)

- **Docker**: For running test databases
- **PostgreSQL**: For database testing
- **MySQL**: For database testing

---

## Project Setup

### 1. Clone Repository

```bash
git clone https://github.com/your-org/QueryNL.git
cd QueryNL
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# OR using Poetry (recommended)
poetry install

# Set up environment variables
cp .env.example .env
# Edit .env with your LLM API keys:
# OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...

# Initialize local database
alembic upgrade head

# Run backend server
python src/main.py
# OR with Poetry
poetry run python src/main.py

# Backend now running at http://localhost:8765
```

**Expected Output:**
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://localhost:8765 (Press CTRL+C to quit)
```

### 3. Extension Setup

```bash
cd ../extension

# Install dependencies
npm install

# Build extension
npm run compile

# Run tests (optional)
npm test

# Package extension
npm run package
# This creates querynl-1.0.0.vsix
```

### 4. Install Extension in VS Code

**Option A: Development Mode**

1. Open VS Code
2. Press `F5` (or Run → Start Debugging)
3. This opens a new "Extension Development Host" VS Code window
4. The extension is active in this window

**Option B: Install VSIX**

1. In VS Code, go to Extensions view (`Cmd+Shift+X` / `Ctrl+Shift+X`)
2. Click "..." menu → Install from VSIX
3. Select `extension/querynl-1.0.0.vsix`
4. Reload VS Code

---

## First Run Validation

### 1. Verify Backend is Running

```bash
curl http://localhost:8765/api/v1/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-10-11T10:00:00Z",
  "dependencies": {
    "llm_api": "available"
  }
}
```

### 2. Verify Extension is Loaded

1. Open VS Code Command Palette (`Cmd+Shift+P` / `Ctrl+Shift+P`)
2. Type "QueryNL"
3. You should see commands:
   - `QueryNL: Connect to Database`
   - `QueryNL: Natural Language Query`
   - `QueryNL: Design Schema`

### 3. Create Test Database Connection

1. Run Docker container with test PostgreSQL:
   ```bash
   docker run -d \
     --name querynl-test-db \
     -e POSTGRES_PASSWORD=testpassword \
     -e POSTGRES_USER=testuser \
     -e POSTGRES_DB=testdb \
     -p 5432:5432 \
     postgres:15-alpine
   ```

2. In VS Code, run `QueryNL: Connect to Database`
3. Fill in connection details:
   - **Name**: Test PostgreSQL
   - **Type**: PostgreSQL
   - **Host**: localhost
   - **Port**: 5432
   - **Database**: testdb
   - **Username**: testuser
   - **Password**: testpassword

4. Click "Test Connection"
   - Should show: ✅ "Connected successfully"

### 4. Execute First Natural Language Query

1. Run `QueryNL: Natural Language Query`
2. Enter: `create a users table with id, email, and name`
3. Extension generates SQL:
   ```sql
   CREATE TABLE users (
     id SERIAL PRIMARY KEY,
     email VARCHAR(255) UNIQUE NOT NULL,
     name VARCHAR(255) NOT NULL
   );
   ```
4. Review SQL and click "Execute"
5. Table created successfully

### 5. Query the Database

1. Run `QueryNL: Natural Language Query` again
2. Enter: `show all tables`
3. Extension generates and executes:
   ```sql
   SELECT table_name
   FROM information_schema.tables
   WHERE table_schema = 'public';
   ```
4. Results display showing "users" table

**✅ Success Criteria**:
- Backend responds to health check
- Extension commands visible in Command Palette
- Database connection established
- SQL generation and execution work

---

## Development Workflow

### Backend Development

**Run with Auto-Reload:**
```bash
cd backend
poetry run uvicorn src.main:app --reload --host 0.0.0.0 --port 8765
```

**Run Tests:**
```bash
# Unit tests
poetry run pytest tests/unit -v

# Integration tests (requires test database)
poetry run pytest tests/integration -v

# All tests
poetry run pytest -v

# With coverage
poetry run pytest --cov=src --cov-report=html
```

**Linting and Formatting:**
```bash
# Run linter
poetry run ruff check src/

# Format code
poetry run black src/

# Type checking
poetry run mypy src/
```

### Extension Development

**Watch Mode (Auto-Compile):**
```bash
cd extension
npm run watch
```

In VS Code:
1. Press `F5` to start debugging
2. Make code changes
3. Press `Cmd+R` / `Ctrl+R` in Extension Development Host to reload

**Run Tests:**
```bash
# Unit tests
npm test

# Extension integration tests
npm run test:integration
```

**Linting:**
```bash
# Run ESLint
npm run lint

# Fix auto-fixable issues
npm run lint:fix
```

### Database Migrations

**Create New Migration (Backend):**
```bash
cd backend

# Auto-generate migration from model changes
poetry run alembic revision --autogenerate -m "Add query_templates table"

# Review generated migration in storage/migrations/versions/

# Apply migration
poetry run alembic upgrade head

# Rollback migration
poetry run alembic downgrade -1
```

---

## Testing Multi-Database Support

### PostgreSQL (Already Running)

```bash
# Test data insertion
docker exec -it querynl-test-db psql -U testuser -d testdb -c \
  "INSERT INTO users (email, name) VALUES ('test@example.com', 'Test User');"
```

### MySQL

```bash
# Start MySQL container
docker run -d \
  --name querynl-mysql \
  -e MYSQL_ROOT_PASSWORD=rootpassword \
  -e MYSQL_DATABASE=testdb \
  -e MYSQL_USER=testuser \
  -e MYSQL_PASSWORD=testpassword \
  -p 3306:3306 \
  mysql:8.0

# Wait for startup (30 seconds)

# Connect via QueryNL extension
# Type: MySQL, Host: localhost, Port: 3306
```

### SQLite

```bash
# Create SQLite database
cd backend
sqlite3 test.db "CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT, name TEXT);"

# Connect via QueryNL extension
# Type: SQLite, File path: /path/to/backend/test.db
```

### MongoDB

```bash
# Start MongoDB container
docker run -d \
  --name querynl-mongo \
  -e MONGO_INITDB_ROOT_USERNAME=testuser \
  -e MONGO_INITDB_ROOT_PASSWORD=testpassword \
  -p 27017:27017 \
  mongo:7.0

# Connect via QueryNL extension
# Type: MongoDB, Host: localhost, Port: 27017
```

**Test Query (MongoDB):**
- Natural language: `show all collections`
- Generated: `db.getCollectionNames()`

---

## Debugging

### Backend Debugging

**VS Code Launch Configuration** (`.vscode/launch.json`):

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "src.main:app",
        "--reload",
        "--host", "0.0.0.0",
        "--port", "8765"
      ],
      "jinja": true,
      "justMyCode": false,
      "cwd": "${workspaceFolder}/backend"
    }
  ]
}
```

**Set Breakpoints:**
1. Open `backend/src/querynl/api/query.py`
2. Click left of line number to set breakpoint
3. Press `F5` to start debugging
4. Execute query from extension → breakpoint hits

**Log Levels:**
```python
# In backend/.env
LOG_LEVEL=DEBUG  # DEBUG, INFO, WARNING, ERROR
```

### Extension Debugging

**VS Code is the Debugger:**

1. Press `F5` → opens Extension Development Host
2. Set breakpoints in `extension/src/*.ts` files
3. Execute commands in Extension Development Host
4. Breakpoints hit in main VS Code window

**Debug Console Output:**
```typescript
// In extension code
import * as vscode from 'vscode';

const outputChannel = vscode.window.createOutputChannel('QueryNL');
outputChannel.appendLine(`Debug: Generated SQL: ${sql}`);
outputChannel.show();
```

**WebSocket Debugging:**

In browser DevTools (if testing webview):
```javascript
// Check WebSocket messages
const ws = new WebSocket('ws://localhost:8765/ws');
ws.onmessage = (event) => console.log('Received:', JSON.parse(event.data));
```

---

## Common Issues

### Issue 1: Backend Won't Start

**Symptoms:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution:**
```bash
cd backend
pip install -r requirements.txt
# OR
poetry install
```

---

### Issue 2: Extension Commands Not Visible

**Symptoms:**
- Command Palette doesn't show QueryNL commands

**Solution:**
1. Check extension is activated: `Developer: Show Running Extensions`
2. Check for errors: `Developer: Toggle Developer Tools` → Console tab
3. Reload window: `Developer: Reload Window`

---

### Issue 3: Database Connection Fails

**Symptoms:**
```
Error: Connection refused (localhost:5432)
```

**Solution:**
```bash
# Check Docker container is running
docker ps | grep querynl-test-db

# Check logs
docker logs querynl-test-db

# Restart container
docker restart querynl-test-db
```

---

### Issue 4: LLM API Rate Limit

**Symptoms:**
```
Error: Rate limit exceeded (429)
```

**Solution:**
1. Check API key is valid in `backend/.env`
2. Wait for rate limit reset (shown in error message)
3. Upgrade API tier if needed
4. Use caching to reduce API calls (set `ENABLE_QUERY_CACHE=true` in `.env`)

---

### Issue 5: WebSocket Connection Drops

**Symptoms:**
- Extension shows "Connecting..." but never connects

**Solution:**
```bash
# Check backend WebSocket endpoint
curl -i -N \
  -H "Connection: Upgrade" \
  -H "Upgrade: websocket" \
  http://localhost:8765/ws

# Should return HTTP 101 Switching Protocols
```

**Check Firewall:**
```bash
# macOS
sudo lsof -i :8765

# Linux
sudo netstat -tulpn | grep 8765
```

---

## Performance Benchmarks

### Expected Performance (Development)

| Operation | Target | Acceptable | Needs Investigation |
|-----------|--------|------------|---------------------|
| Backend startup | <3s | <5s | >5s |
| Extension activation | <2s | <3s | >3s |
| Database connection | <5s | <10s | >10s |
| Simple query generation | <3s | <5s | >5s |
| Complex query generation | <5s | <10s | >10s |
| Schema introspection (100 tables) | <10s | <20s | >20s |
| Query execution (100 rows) | <1s | <2s | >2s |

### Measure Performance

**Backend API:**
```bash
# Install Apache Bench
brew install httpd  # macOS
sudo apt-get install apache2-utils  # Ubuntu

# Benchmark health endpoint
ab -n 1000 -c 10 http://localhost:8765/api/v1/health

# Expected: >100 requests/second
```

**Query Generation:**
```bash
# Use time command
time curl -X POST http://localhost:8765/api/v1/query/generate \
  -H "Content-Type: application/json" \
  -d '{"natural_language_query":"show all users","connection_id":"<uuid>"}'

# Expected: <3 seconds
```

---

## Next Steps

### For Developers

1. **Read Architecture Docs**: See [plan.md](plan.md) for system architecture
2. **Review Data Model**: See [data-model.md](data-model.md) for entity relationships
3. **API Contracts**: See [contracts/](contracts/) for API specifications
4. **Run Full Test Suite**: `poetry run pytest && npm test`
5. **Check Constitution Compliance**: Review [.specify/memory/constitution.md](../.specify/memory/constitution.md)

### For Contributing

1. **Create Feature Branch**: `git checkout -b feature/your-feature`
2. **Make Changes**: Follow coding standards (ruff, black, ESLint)
3. **Write Tests**: Maintain 80%+ coverage
4. **Test Locally**: Run all tests and manual validation
5. **Submit PR**: Include description and test results

### For Production Deployment

1. **Environment Variables**: Set production API keys and secrets
2. **Database Setup**: Use production PostgreSQL (not SQLite)
3. **SSL/TLS**: Configure HTTPS/WSS for API and WebSocket
4. **Monitoring**: Set up logging, metrics, and alerting
5. **Backup**: Configure credential backup strategy

---

## Constitution Compliance Checklist

Before considering development environment "ready", verify:

### ✅ Principle I: Security-First Design
- [ ] Credentials stored in OS keychain (test by viewing DB connection in extension)
- [ ] No credentials visible in logs (`tail -f backend/logs/app.log`)
- [ ] SQL injection prevention (try `'; DROP TABLE users; --` in NL query)

### ✅ Principle II: User Experience Over Technical Purity
- [ ] First query within 5 minutes of installation (timed test)
- [ ] Error messages are actionable (trigger error, check message quality)
- [ ] Extension doesn't block IDE (generate long-running query, continue editing)

### ✅ Principle III: Transparency and Explainability
- [ ] Generated SQL shown before execution (verify in extension UI)
- [ ] Destructive operation confirmation required (test DELETE query)
- [ ] Token usage visible (check after query generation)

### ✅ Principle IV: Multi-Database Parity
- [ ] PostgreSQL connection works
- [ ] MySQL connection works
- [ ] SQLite connection works
- [ ] MongoDB connection works (all above tests passed)

### ✅ Principle V: Fail-Safe Defaults
- [ ] Destructive operation requires confirmation (test DELETE without flag)
- [ ] Migration rollback generated (check generated migration files)
- [ ] Rate limiting active (make 1001 requests rapidly)

---

## Contact & Support

- **Documentation**: `docs/` directory
- **Issues**: GitHub Issues
- **Discussion**: GitHub Discussions
- **Email**: dev@querynl.example.com

---

**Happy Coding! 🚀**
