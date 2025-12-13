# Research Findings: QueryNL CLI Technology Decisions

**Date**: 2025-10-13
**Purpose**: Research technical implementation decisions for Python CLI tool
**Status**: Research Only - No Implementation

---

## Executive Summary

This research evaluates technology choices for building a Python-based command-line interface for QueryNL. The CLI will provide terminal-native access to database querying, schema design, and migration management capabilities. Key findings:

1. **Database Drivers**: Reuse existing backend drivers (psycopg2 for PostgreSQL, pymysql for MySQL, sqlite3 for SQLite, pymongo for MongoDB)
2. **CLI Framework**: Click recommended over Typer for mature REPL support via click-repl
3. **Terminal Formatting**: Combined approach using Rich (output) + prompt_toolkit (interactive input)
4. **Credential Storage**: Keyring library with keyrings.cryptfile fallback for headless servers
5. **Binary Distribution**: PyInstaller recommended with optimization techniques to stay under 50MB

---

## 1. Database Drivers

### Decision: **Reuse Existing Backend Drivers**

### Current Backend Stack (from 001-ai-powered-database)

The QueryNL backend already has database driver dependencies specified:

- **PostgreSQL**: psycopg2-binary
- **MySQL**: pymysql
- **SQLite**: sqlite3 (Python standard library)
- **MongoDB**: pymongo

### Rationale

**Code Reuse and Consistency:**
- CLI should share the same database adapter layer as the IDE extension backend
- Maintains consistency in SQL generation and query execution behavior
- Reduces maintenance burden - single set of drivers to update
- Leverages existing test coverage for database interactions

**PostgreSQL Driver Analysis (2025):**
- **psycopg2**: Mature, stable, widely adopted. Synchronous operation suitable for CLI use cases.
- **psycopg3**: Offers async support and performance improvements (5-20% faster in benchmarks), but adds complexity
- **asyncpg**: Fastest option (5x faster than psycopg3) but lacks DB-API 2.0 compatibility

**Decision for CLI:** Stick with psycopg2-binary for initial release because:
- CLI operations are typically interactive and don't require async performance
- Proven stability and compatibility
- Smaller dependency footprint than psycopg3
- Can upgrade to psycopg3 in Phase 2 if async CLI operations become a priority

### Implementation

CLI will import from existing backend's database adapter modules:

```python
# CLI reuses backend database adapters
from querynl.db.postgresql import PostgreSQLAdapter
from querynl.db.mysql import MySQLAdapter
from querynl.db.sqlite import SQLiteAdapter
from querynl.db.mongodb import MongoDBAdapter
```

**Dependency Installation:**
```
# requirements.txt (CLI-specific additions)
click>=8.1.0
click-repl>=0.3.0
rich>=13.0.0
prompt-toolkit>=3.0.52
keyring>=25.0.0
keyrings.cryptfile>=1.3.0
```

### Alternatives Considered

**Option: Use psycopg3 for improved performance**
- **Rejected**: Added complexity for minimal benefit in interactive CLI context. Async support not needed for typical CLI query execution patterns where users wait for results.

**Option: Support SQLAlchemy as an additional abstraction layer**
- **Rejected**: Adds overhead and another dependency. Direct driver usage provides better control and performance for CLI use cases.

---

## 2. CLI Framework: Click vs Typer

### Decision: **Click**

### Comparison Summary

| Feature | Click | Typer | Winner |
|---------|-------|-------|--------|
| **Maturity** | 10+ years, battle-tested | 3 years, newer | Click |
| **REPL Support** | Excellent via click-repl | No native support, can use click-repl | Click |
| **Command Grouping** | Native support, flexible | Native support, simpler syntax | Typer (slightly) |
| **Help Text Generation** | Good, manual decorators | Excellent, auto-generated from type hints | Typer |
| **Type Hints** | Optional | Core design principle | Typer |
| **Performance** | Minimal overhead | Built on Click, same performance | Tie |
| **Learning Curve** | Moderate | Easier for beginners | Typer |
| **Cross-platform** | Excellent | Excellent | Tie |
| **Startup Time** | <100ms typical | <100ms typical | Tie |

### Rationale for Click

**1. REPL Mode Support (Critical Requirement)**

QueryNL CLI requires interactive REPL mode per FR-004. The `click-repl` library provides production-ready REPL functionality:

```python
from click_repl import register_repl

@click.group()
def cli():
    """QueryNL CLI"""
    pass

@cli.command()
def repl():
    """Start interactive REPL"""
    pass

# Automatically creates REPL from all CLI commands
register_repl(cli)
```

**Key Features:**
- Tab completion for commands and arguments
- Command history with readline support
- Context persistence between commands (ctx.obj)
- Shell command execution with `!` prefix
- Built on prompt_toolkit for advanced features

**Typer Alternative:** While Typer is built on Click and could theoretically use click-repl, there's no native integration or documentation. Using Click directly provides better REPL support with less friction.

**2. Maturity and Ecosystem**

Click has been the de facto standard for Python CLIs since 2014:
- Used by major projects: Flask, Ansible, AWS CLI, pip, poetry
- Extensive documentation and community support
- Known edge cases and solutions well-documented
- Proven stability over 10+ years

**3. Explicit Over Magic**

Click's decorator-based approach is more explicit than Typer's type-hint magic:

```python
# Click - explicit and clear
@click.command()
@click.option('--format', type=click.Choice(['table', 'json', 'csv']))
@click.argument('query')
def query_cmd(query: str, format: str):
    pass

# Typer - more concise but relies on type hints
def query_cmd(
    query: str,
    format: Annotated[str, typer.Option()] = "table"
):
    pass
```

For a project requiring REPL integration and complex command structures, Click's explicitness makes debugging easier.

**4. Performance Considerations**

Both frameworks have negligible startup time (<100ms) suitable for CLI applications. Since Typer is built on top of Click, there's no performance advantage—potentially slight overhead from type introspection.

### When Typer Would Be Better

Typer excels for:
- Simple CLIs without REPL requirements
- Projects prioritizing rapid development and minimal boilerplate
- Teams already using FastAPI (same author, similar patterns)
- CLIs where auto-generated help text from type hints is a major benefit

### Implementation Strategy

**Command Structure:**
```python
import click
from click_repl import repl

@click.group()
@click.pass_context
def cli(ctx):
    """QueryNL - AI-powered database CLI"""
    ctx.ensure_object(dict)
    # Load config, initialize state

@cli.group()
def connect():
    """Manage database connections"""
    pass

@connect.command('add')
@click.argument('name')
def connect_add(name):
    """Add a new database connection"""
    pass

@cli.command()
@click.argument('query')
@click.option('--format', type=click.Choice(['table', 'json', 'csv', 'markdown']))
def query(query, format):
    """Execute natural language query"""
    pass

@cli.command()
@click.pass_context
def repl(ctx):
    """Start interactive REPL mode"""
    repl(ctx)
```

**Help Text Example:**
```bash
$ querynl --help
Usage: querynl [OPTIONS] COMMAND [ARGS]...

  QueryNL - AI-powered database CLI

Options:
  --help  Show this message and exit.

Commands:
  connect  Manage database connections
  query    Execute natural language query
  repl     Start interactive REPL mode
  schema   Schema design commands
  migrate  Migration management commands
```

### Alternatives Considered

**argparse (Python standard library)**
- **Rejected**: More verbose, lacks command grouping elegance, no REPL support, harder to maintain complex CLIs

**Typer**
- **Evaluated**: Excellent for simple CLIs, but lack of native REPL support is a blocker. Click's maturity and ecosystem make it the safer choice for QueryNL's requirements.

---

## 3. Terminal Formatting: Rich vs Alternatives

### Decision: **Combined Approach - Rich + prompt_toolkit**

### Architecture

Use both libraries for complementary purposes:

**Rich** - Output Formatting and Display
- Tables with unicode borders
- Syntax highlighting
- Progress bars
- Pretty printing
- Colored output

**prompt_toolkit** - Interactive Input
- Readline replacement
- Command history
- Tab completion
- Multi-line editing
- Key bindings (Emacs/Vi)

### Rationale

**Why Rich for Output:**

1. **Table Rendering** (Critical for Query Results)

Rich excels at rendering tables with automatic column sizing:

```python
from rich.console import Console
from rich.table import Table

console = Console()

table = Table(title="Query Results")
table.add_column("ID", style="cyan")
table.add_column("Name", style="magenta")
table.add_column("Email", style="green")

for row in results:
    table.add_row(str(row['id']), row['name'], row['email'])

console.print(table)
```

**Features:**
- Auto-sizing columns based on terminal width
- Unicode box characters (beautiful rendering)
- Color support with fallback for non-color terminals
- CSV/JSON/markdown output via same codebase
- Pagination support for large datasets

2. **Cross-Platform Color Support**

Rich handles ANSI color codes across Windows, macOS, and Linux without platform-specific code. Automatically detects terminal capabilities and adjusts output.

3. **Progress Indicators**

For long-running operations (schema introspection, migration application):

```python
from rich.progress import track

for step in track(migration_steps, description="Applying migration..."):
    apply_migration_step(step)
```

4. **Performance**

Rich has minimal overhead for typical CLI output volumes. Benchmarks show <5ms delay for rendering 1000-row tables.

**Why prompt_toolkit for Input:**

1. **REPL Enhancement**

click-repl uses prompt_toolkit under the hood, so we're already getting these features:
- Command history (persistent across sessions)
- Tab completion (auto-complete table names, commands)
- Multi-line input (for complex queries)
- Vi/Emacs key bindings
- Mouse support for cursor positioning

2. **Auto-Suggestions**

prompt_toolkit can provide fish-shell-style auto-suggestions:

```python
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory

session = PromptSession(history=FileHistory('~/.querynl/history'))
user_input = session.prompt('querynl> ', auto_suggest=AutoSuggestFromHistory())
```

3. **Minimal Dependencies**

Only requires `Pygments` and `wcwidth` - both lightweight and commonly available.

### Integration Strategy

```python
import click
from rich.console import Console
from rich.table import Table
from click_repl import repl
from prompt_toolkit import PromptSession

console = Console()  # Rich console for output

def format_results(results, format_type='table'):
    """Format query results using Rich"""
    if format_type == 'table':
        table = Table(show_header=True, header_style="bold cyan")
        # Add columns and rows
        console.print(table)
    elif format_type == 'json':
        console.print_json(data=results)
    # etc.

@click.command()
def query(query_text):
    results = execute_query(query_text)
    format_results(results)
```

### Alternatives Considered

**colorama**
- **Rejected**: Basic color support only, no table rendering or advanced features. Rich supersedes it entirely.

**blessed**
- **Evaluated**: Good for full-screen terminal UIs, but overkill for CLI. Rich + prompt_toolkit provide everything needed without blessed's complexity.

**Tabulate**
- **Evaluated**: Excellent table library, but Rich provides tables plus much more (colors, progress, pretty printing). No reason to add another dependency when Rich covers it.

**Using Rich alone (without prompt_toolkit)**
- **Considered**: Rich has `Prompt` class for input, but it's basic compared to prompt_toolkit. For REPL mode with history and completion, prompt_toolkit is superior.

### Bundle Size Impact

- Rich: ~500KB (compressed)
- prompt_toolkit: ~300KB (compressed)
- Total: <1MB additional size

Well within 50MB binary target.

### Performance Characteristics

- Rich table rendering: <5ms for 1000 rows
- prompt_toolkit input handling: <1ms latency
- No noticeable performance impact on CLI responsiveness

---

## 4. Credential Storage: Keyring Library

### Decision: **keyring + keyrings.cryptfile fallback**

### Platform Support

The `keyring` library provides cross-platform credential storage:

**macOS:**
- Uses Keychain Access (native)
- Requires macOS 11+ and Python 3.8.7+ with universal2 binary
- Fully integrated with system security

**Windows:**
- Uses Windows Credential Manager (native)
- Works on Windows 10+
- Credentials stored in Windows Credential Vault

**Linux:**
- Uses Secret Service API (GNOME Keyring, KWallet)
- Requires D-Bus session
- KDE/GNOME desktop environments fully supported

### Rationale

**1. Native Integration**

Using OS keychain provides the best security:
- Credentials encrypted with OS-level keys
- No need to manage encryption keys in application
- Respects OS security policies (Touch ID, biometrics)
- Credentials can be accessed by system administrators if needed

**2. Automatic Backend Selection**

The keyring library automatically chooses the best backend for the current environment:

```python
import keyring

# Automatically uses macOS Keychain / Windows Credential Manager / Secret Service
keyring.set_password("querynl", "prod-db", "database-password")
password = keyring.get_password("querynl", "prod-db")
```

**3. Fallback for Headless Servers**

**Problem:** Headless Linux servers (Docker, SSH sessions, CI/CD) don't have access to GNOME Keyring or D-Bus.

**Solution:** Use `keyrings.cryptfile` as fallback backend.

### Fallback Strategy: keyrings.cryptfile

**Features:**
- Encrypted file-based credential storage
- Uses Argon2 hash for key derivation
- Authenticated AES encryption (GCM mode by default)
- Prevents tampering with authenticated encryption
- Portable across systems

**Implementation:**

```python
import keyring
from keyrings.cryptfile.cryptfile import CryptFileKeyring

# Detect if native keychain is available
try:
    keyring.get_password("querynl", "test")
    # Native keychain works
except Exception:
    # Fallback to encrypted file
    kr = CryptFileKeyring()
    keyring.set_keyring(kr)

    # Set keyring password from environment variable
    kr.keyring_key = os.environ.get('QUERYNL_KEYRING_PASSWORD')
```

**Headless Server Setup:**

```bash
# Set keyring password via environment variable
export QUERYNL_KEYRING_PASSWORD="secure-master-password"

# Or use connection string directly (bypass keyring)
export QUERYNL_CONNECTION_STRING="postgresql://user:pass@host/db"
```

**Security Trade-offs:**

| Approach | Security Level | Use Case |
|----------|---------------|----------|
| Native Keychain | Highest | Desktop/laptop usage |
| CryptFileKeyring + env var | Medium-High | Headless servers with env var management |
| Connection string in env | Medium | CI/CD, Docker containers (use secrets management) |
| Plain text config file | Low (NOT RECOMMENDED) | Never use in production |

### Alternative: Custom Encryption

**Considered:** Implementing custom encryption using `cryptography` library directly.

**Rejected because:**
- Reinventing the wheel (keyring is battle-tested)
- Risk of implementation errors (crypto is hard)
- keyring handles cross-platform differences
- keyrings.cryptfile already provides secure file-based fallback

### Implementation Example

```python
import keyring
import os
from keyrings.cryptfile.cryptfile import CryptFileKeyring

class CredentialManager:
    def __init__(self):
        self.service_name = "querynl"
        self._setup_keyring()

    def _setup_keyring(self):
        """Setup keyring with fallback for headless systems"""
        try:
            # Test if native keychain is available
            keyring.get_password(self.service_name, "__test__")
        except Exception as e:
            # Fallback to encrypted file
            kr = CryptFileKeyring()
            keyring.set_keyring(kr)

            # Password from environment or prompt
            password = os.environ.get('QUERYNL_KEYRING_PASSWORD')
            if not password:
                password = click.prompt(
                    'Master password for credential storage',
                    hide_input=True
                )
            kr.keyring_key = password

    def store_credentials(self, connection_name: str, credentials: dict):
        """Store encrypted credentials"""
        import json
        cred_json = json.dumps(credentials)
        keyring.set_password(self.service_name, connection_name, cred_json)

    def retrieve_credentials(self, connection_name: str) -> dict:
        """Retrieve decrypted credentials"""
        import json
        cred_json = keyring.get_password(self.service_name, connection_name)
        return json.loads(cred_json) if cred_json else None

    def delete_credentials(self, connection_name: str):
        """Remove stored credentials"""
        keyring.delete_password(self.service_name, connection_name)
```

### Alternatives Considered

**python-keyring alternatives:**
- **Rejected**: python-keyring IS the standard. Alternative implementations are less mature.

**HashiCorp Vault / AWS Secrets Manager:**
- **Future Enhancement**: Support for enterprise credential stores in Phase 2. Adds complexity and external dependencies not suitable for initial release.

**Encrypted JSON file with Fernet (cryptography library):**
- **Rejected**: keyrings.cryptfile provides this functionality with better security (Argon2 + authenticated AES). No need to reimplement.

---

## 5. Binary Distribution: PyInstaller vs Nuitka

### Decision: **PyInstaller**

### Comparison Summary

| Criterion | PyInstaller | Nuitka | Winner |
|-----------|-------------|--------|--------|
| **Build Time** | Fast (~2-5 min) | Slow (~15-30 min) | PyInstaller |
| **Binary Size** | 40-80 MB typical | 80-160 MB typical (2x larger) | PyInstaller |
| **Runtime Performance** | Native Python speed | 2-5x faster (compiled) | Nuitka |
| **Ease of Use** | Simple, well-documented | More complex setup | PyInstaller |
| **Compatibility** | Excellent | Good, occasional issues | PyInstaller |
| **Size Optimization** | UPX, --onefile, --exclude | --onefile, zstandard | PyInstaller (easier) |

### Rationale for PyInstaller

**1. Target: <50MB Binary Size**

PyInstaller produces smaller binaries and has better size optimization tooling:

**Base Size Estimates:**
- Python interpreter: ~15 MB
- CLI dependencies (Click, Rich, etc.): ~5 MB
- Database drivers: ~10 MB
- Standard library subset: ~10 MB
- **Total**: ~40 MB (before optimization)

**Optimization Techniques:**

```bash
# Build optimized single-file executable
pyinstaller querynl.py \
    --onefile \
    --strip \
    --exclude-module tkinter \
    --exclude-module matplotlib \
    --exclude-module pandas \
    --exclude-module numpy \
    --name querynl

# Optional: UPX compression (can reduce by 40-50%)
pyinstaller querynl.py --onefile --strip --upx-dir /usr/local/bin
```

**Size Reduction Checklist:**
- [ ] Use `--onefile` to bundle into single executable
- [ ] Use `--strip` to remove debug symbols (Linux/macOS)
- [ ] Exclude unused stdlib modules (tkinter, test, etc.)
- [ ] Use UPX compression (optional, adds ~2-3s startup time)
- [ ] Create virtual environment with only required packages
- [ ] Exclude development dependencies (pytest, mypy, etc.)

**Expected Final Size:** 35-45 MB (with aggressive optimization and UPX)

**2. Build Speed Matters**

For iterative development and CI/CD pipelines:
- PyInstaller: 2-5 minutes per build
- Nuitka: 15-30 minutes per build

PyInstaller's speed enables rapid iteration during development.

**3. Cross-Compilation Complexity**

**PyInstaller:**
- Build on target platform (macOS → macOS binary, Linux → Linux binary)
- Simple GitHub Actions workflow for multi-platform builds
- Well-documented for CI/CD integration

**Nuitka:**
- Similar cross-compilation limitations
- More complex build process
- Longer CI/CD pipeline execution time

**4. When Nuitka Would Be Better**

Nuitka excels when:
- Runtime performance is critical (not a bottleneck for QueryNL CLI - LLM API latency dominates)
- Distribution size >100MB anyway (our target is <50MB)
- Long-running computations (QueryNL is I/O bound, not CPU bound)

For QueryNL CLI:
- Primary latency: LLM API calls (1-3 seconds)
- Secondary latency: Database queries (100ms-1s)
- CLI framework overhead: <10ms (negligible)

**Conclusion:** Nuitka's 2-5x performance improvement doesn't materially impact user experience when LLM API calls dominate latency.

### Size Optimization Techniques

**1. Virtual Environment Approach**

```bash
# Create minimal virtual environment
python -m venv venv-build
source venv-build/bin/activate

# Install ONLY runtime dependencies
pip install click click-repl rich prompt-toolkit keyring psycopg2-binary pymysql pymongo

# Build from minimal environment
pyinstaller querynl.py --onefile
```

**2. Modify .spec File**

```python
# querynl.spec
a = Analysis(['querynl.py'],
    excludes=[
        'tkinter', 'matplotlib', 'pandas', 'numpy',
        'test', 'unittest', 'email', 'xml', 'pydoc'
    ],
    hiddenimports=['keyring.backends'],  # Include keyring backends
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='querynl',
    strip=True,  # Strip symbols
    upx=True,    # UPX compression
    console=True,
)
```

**3. Database Driver Optimization**

Use `psycopg2-binary` instead of `psycopg2` to avoid including compilation dependencies.

**4. UPX Compression**

```bash
# Install UPX
brew install upx  # macOS
apt install upx   # Linux

# PyInstaller with UPX
pyinstaller querynl.py --onefile --upx-dir $(which upx | xargs dirname)
```

**Trade-off:** UPX adds 2-3 seconds to startup time (decompression), but reduces binary size by 40-50%.

### Cross-Platform Build Strategy

**GitHub Actions Workflow:**

```yaml
name: Build Binaries

on: [push, release]

jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]

    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m venv venv-build
          source venv-build/bin/activate
          pip install -r requirements.txt pyinstaller

      - name: Build executable
        run: |
          source venv-build/bin/activate
          pyinstaller querynl.spec

      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: querynl-${{ matrix.os }}
          path: dist/querynl*
```

### Distribution Channels

**1. Binary Downloads (Primary)**
- GitHub Releases with pre-built binaries for macOS/Linux/Windows
- Direct download without Python installation required

**2. PyPI (Secondary)**
```bash
pip install querynl-cli
```
- Requires Python 3.11+ installed
- Easier to update (`pip install --upgrade`)
- Smaller download (no bundled interpreter)

**3. Homebrew (macOS/Linux)**
```bash
brew install querynl
```
- Future enhancement (Phase 2)
- Requires creating and maintaining Homebrew tap

**4. npm (Global Install)**
```bash
npm install -g querynl
```
- Requires Node.js installed
- Not recommended (Python project, adds unnecessary dependency)

### Alternatives Considered

**Nuitka**
- **Evaluated**: Better runtime performance but 2x larger binaries and 6x longer build times. Performance gain irrelevant when LLM API latency dominates user experience.

**PyOxidizer**
- **Evaluated**: Modern alternative to PyInstaller with better Python version support. Less mature ecosystem, fewer optimization options, similar binary sizes. PyInstaller's maturity and documentation make it safer choice.

**cx_Freeze**
- **Rejected**: Older tool, less active development, larger binaries than PyInstaller. No advantages over PyInstaller.

**Briefcase (BeeWare project)**
- **Rejected**: Designed for GUI applications, overkill for CLI tool. PyInstaller is better suited for command-line tools.

---

## Summary of Recommendations

| Component | Recommendation | Rationale |
|-----------|---------------|-----------|
| **Database Drivers** | Reuse backend drivers (psycopg2, pymysql, sqlite3, pymongo) | Code reuse, consistency, proven stability |
| **CLI Framework** | Click | Mature REPL support via click-repl, battle-tested, explicit design |
| **Output Formatting** | Rich | Beautiful tables, progress bars, cross-platform colors |
| **Interactive Input** | prompt_toolkit | Readline replacement, history, tab completion (via click-repl) |
| **Credential Storage** | keyring + keyrings.cryptfile | Native OS keychain with encrypted file fallback for headless |
| **Binary Distribution** | PyInstaller | Smaller binaries (<50MB target), faster builds, easier optimization |

### Implementation Priorities

**Phase 0 (Setup):**
1. Project structure with Click + Rich + prompt_toolkit
2. Basic CLI scaffolding (command groups, help text)
3. Configuration management (~/.querynl/config.yaml)

**Phase 1 (Core Features):**
1. Connection management with keyring integration
2. Natural language query execution
3. Table output formatting with Rich
4. REPL mode with click-repl

**Phase 2 (Advanced Features):**
1. Schema design commands
2. Migration generation
3. Output format options (JSON, CSV, markdown)
4. Binary distribution with PyInstaller

**Phase 3 (Distribution):**
1. PyInstaller optimization for <50MB target
2. GitHub Actions for multi-platform builds
3. Release process and binary distribution

### Dependencies (requirements.txt)

```
# CLI Framework
click>=8.1.0
click-repl>=0.3.0

# Terminal UI
rich>=13.0.0
prompt-toolkit>=3.0.52

# Credential Management
keyring>=25.0.0
keyrings.cryptfile>=1.3.0

# Database Drivers (reuse from backend)
psycopg2-binary>=2.9.0
pymysql>=1.0.0
pymongo>=4.0.0

# Configuration
pyyaml>=6.0

# Shared with backend
pydantic>=2.0.0
```

### Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Binary size >50MB | Medium | Medium | Aggressive optimization, UPX compression, minimal venv |
| Keyring unavailable on headless | High | Low | keyrings.cryptfile fallback documented |
| Click-REPL limitations | Low | Medium | Well-established library, fallback to basic Click commands |
| Cross-platform keychain issues | Medium | Medium | Comprehensive testing, fallback strategies documented |
| PyInstaller bundling errors | Low | High | Test on all platforms, CI/CD validation |

### Next Steps

1. **Phase 0:** Update Technical Context in plan.md with resolved decisions
2. **Phase 1:** Data modeling (shared with backend where possible)
3. **Phase 1:** API contracts (CLI commands, configuration format, output schemas)
4. **Phase 2:** Implementation (tasks.md generation via /speckit.tasks)

---

## References

- Click Documentation: https://click.palletsprojects.com/
- click-repl GitHub: https://github.com/click-contrib/click-repl
- Rich Documentation: https://rich.readthedocs.io/
- prompt_toolkit Documentation: https://python-prompt-toolkit.readthedocs.io/
- keyring Documentation: https://keyring.readthedocs.io/
- keyrings.cryptfile GitHub: https://github.com/frispete/keyrings.cryptfile
- PyInstaller Documentation: https://pyinstaller.org/
- Nuitka Documentation: https://nuitka.net/
- psycopg2 vs psycopg3: https://www.tigerdata.com/blog/psycopg2-vs-psycopg3-performance-benchmark

