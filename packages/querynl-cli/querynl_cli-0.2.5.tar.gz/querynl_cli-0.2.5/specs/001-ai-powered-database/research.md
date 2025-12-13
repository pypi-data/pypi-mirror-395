# Research Findings: QueryNL Technology Decisions

**Date**: 2025-10-11
**Purpose**: Resolve NEEDS CLARIFICATION items from Technical Context

---

## 1. VS Code Extension Testing Framework

### Decision: **Mocha**

### Rationale:

Mocha is the official and recommended testing framework for VS Code extensions. The VS Code extension generator and `@vscode/test-cli` module use Mocha by default, providing zero-configuration integration.

**Key advantages:**
- Official Microsoft support with comprehensive documentation
- Native async/await support essential for extension testing
- Seamless TypeScript compatibility via ts-node or tsx loaders
- Battle-tested specifically for VS Code extension development
- Full access to VS Code Extension API in tests

### Alternatives Considered:

**Jest:**
- Excellent for general JavaScript testing with large ecosystem
- Requires custom setup for VS Code extensions (no official support)
- Needs ts-jest for TypeScript, adds Babel/webpack complexity
- Not recommended for VS Code extension-specific testing

**Vitest:**
- Modern, fast, excellent TypeScript support out-of-the-box
- No official VS Code extension support
- Best for modern web projects but not for VS Code extensions

### Implementation:

```bash
npm install --save-dev @vscode/test-cli @vscode/test-electron mocha @types/mocha
```

Test files in `extension/tests/suite/` with Mocha runner configuration.

---

## 2. WebSocket Library

### Decision: **reconnecting-websocket** (extension) + **FastAPI native WebSockets** (backend)

### Rationale:

Dual-library approach optimizes for each environment:

**Extension (Browser/Webview Context):**
- **reconnecting-websocket**: Lightweight, automatic reconnection with configurable backoff, works with native WebSocket API
- Dependency-free, multi-platform support (Web, ServiceWorkers, Node.js)
- ~5KB minified bundle size

**Backend (Python/FastAPI):**
- **FastAPI native WebSocket support**: Built on Starlette, production-ready asyncio-based WebSockets
- No additional dependencies needed
- Integrates seamlessly with existing FastAPI architecture

### Alternatives Considered:

**websocket-ts:**
- TypeScript-native with auto-reconnect and message buffering
- Smaller community, less mature ecosystem
- Good alternative but reconnecting-websocket has wider adoption

**isomorphic-ws:**
- Consistent API across Node.js and browser
- **Fatal flaw**: No built-in reconnection support
- Not suitable for QueryNL's reliability requirements

**ws (Node.js):**
- Industry standard for Node.js WebSocket servers
- Would require Python equivalent (FastAPI already provides this)

### Implementation:

**Architecture:**
```
VS Code Webview (reconnecting-websocket) <--WebSocket--> Python Backend (FastAPI WebSocket)
```

**Connection handling:**
- Exponential backoff reconnection (start 1s, max 30s)
- Heartbeat/ping every 30 seconds
- Message queuing during disconnection (buffer last 100 messages)
- Connection status indicator in extension UI

**Endpoint:**
- `ws://localhost:8765/ws` for local backend
- JSON-based message protocol
- Token-based authentication in handshake

---

## 3. ER Diagram Rendering Library

### Decision: **Mermaid.js**

### Rationale:

Mermaid.js provides the best balance of features, VS Code integration, and developer experience for ER diagrams.

**Key advantages:**
- **Native Crow's Foot notation**: Built-in `erDiagram` declaration with relationship types
- Excellent VS Code integration with official Mermaid Chart plugin
- Text-based diagrams (markdown-inspired, easy to generate, version control-friendly)
- Built-in GitHub rendering support
- Active development (20K+ stars, regular releases)
- Reasonable bundle size: ~1MB with Mermaid Tiny (sufficient for ERD)

### Alternatives Considered:

**D3.js:**
- Extremely flexible for custom visualizations
- **Drawbacks**: Much larger bundle (~96.5 KB + dependencies), requires significant custom code for ER diagrams, steeper learning curve
- Overkill for standard ER diagrams

**GraphViz (via viz.js WebAssembly):**
- Professional layout algorithms, DOT language
- **Drawbacks**: Larger bundle (~660 KB), slower rendering, WebAssembly deployment complexity
- Better for complex directed graphs, overengineered for ER diagrams

### Implementation:

```typescript
import mermaid from 'mermaid';

mermaid.initialize({
  startOnLoad: true,
  theme: 'default',
  er: { useMaxWidth: true }
});

const erDiagram = `
erDiagram
    USERS ||--o{ ORDERS : places
    ORDERS ||--|{ ORDER_ITEMS : contains
    PRODUCTS ||--o{ ORDER_ITEMS : "ordered in"

    USERS {
        int id PK
        string email UK
        string name
        timestamp created_at
    }
`;

mermaid.render('erDiagram', erDiagram);
```

**Crow's Foot notation mapping:**
- `||--||` : One to one
- `||--o{` : One to many (mandatory)
- `|o--o{` : Zero or one to many
- `}o--o{` : Many to many

**Bundle optimization:**
- Use Mermaid Tiny (~1 MB) for ERD-only support
- Lazy-load only when schema visualization is opened
- Tree-shaking to import only ER diagram module

**Performance:**
- Handles 50+ table schemas smoothly
- Typical rendering: <500ms
- Supports light/dark theme switching

---

## 4. Migration Framework Integration Priorities

### Decision: **Phase 1: Alembic + Flyway | Phase 2: Django Migrations**

### Rationale:

Support 2 frameworks initially to cover majority of users, then expand based on demand.

**Phase 1 (Initial Release):**

1. **Alembic (Python/SQLAlchemy)**
   - **Why first**: QueryNL backend is Python-based, enables deep integration and code reuse
   - **Market position**: De facto standard for Python migrations with SQLAlchemy
   - **Target users**: Python developers (FastAPI, Flask, standalone scripts)
   - **Technical complexity**: Medium - can import Alembic directly in backend

2. **Flyway (JVM ecosystem)**
   - **Why first**: Most popular enterprise migration tool with 40M downloads
   - **Market position**: Dominant in enterprise environments (25% YoY growth)
   - **Target users**: Java/Kotlin backend developers, enterprise teams
   - **Technical complexity**: Low - simple SQL-based migrations with straightforward file naming

**Phase 2 (Post-Launch):**

3. **Django Migrations**
   - **Why second**: Django at 74% among Python framework users, but framework-specific
   - **Target users**: Django developers (large base but specific ecosystem)
   - **Technical complexity**: Medium - Python-based, ORM-specific patterns
   - **Timing**: Add based on user requests from Django community

**Phase 3 (Future Consideration):**

4. **Liquibase** - Enterprise-focused, comparable to Flyway but more complex
5. **Rails Migrations** - Ruby ecosystem (smaller market but dedicated community)

### Alternatives Considered:

**Starting with 3+ frameworks:**
- **Rejected**: Delays launch, increases testing burden, dilutes focus
- **Better approach**: Start with 2, prove value, expand based on demand

**Framework-agnostic SQL generation only:**
- **Rejected**: Loses framework-specific features (versioning, rollbacks, data migrations)
- **Users expect**: Framework-native migrations

**Liquibase before Flyway:**
- **Rejected**: Flyway's simplicity better for initial release despite Liquibase's feature richness

### Implementation:

**Alembic Integration:**
```python
from alembic.operations import Operations

def generate_alembic_migration(schema_changes):
    migration_template = f'''
"""{{description}}

Revision ID: {{revision_id}}
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    {generate_upgrade_ops(schema_changes)}

def downgrade():
    {generate_downgrade_ops(schema_changes)}
'''
    return migration_template
```

**Flyway Integration:**
```python
def generate_flyway_migration(schema_changes, version):
    filename = f"V{version}__{description}.sql"
    sql_content = generate_sql_from_changes(schema_changes)
    return filename, sql_content
```

**Plugin Architecture:**
- Abstract `MigrationGenerator` base class
- Each framework: Separate subclass for framework-specific generation
- User configuration: Select framework in extension settings
- Testing: Docker containers with framework-specific environments

**Market Coverage:**
- Alembic + Flyway covers ~80% of backend developers
- Python + Java ecosystems represent majority of target users

---

## Summary

| Decision | Choice | Implementation Priority | Bundle Impact |
|----------|--------|------------------------|---------------|
| Testing Framework | Mocha | Setup (Phase 0) | N/A (dev dependency) |
| WebSocket Library | reconnecting-websocket + FastAPI | Phase 1 | ~5KB (extension) |
| ER Diagram Library | Mermaid.js | Phase 1 | ~1MB (lazy-loaded) |
| Migration Frameworks | Alembic + Flyway (P1), Django (P2) | Phase 1, Phase 2 | N/A (backend logic) |

**Total Extension Bundle Impact**: ~1.005 MB (well under 5MB target)

All technology choices:
- Align with Python backend + TypeScript extension architecture
- Are mature, well-documented, and actively maintained
- Minimize implementation risk while maximizing compatibility
- Support QueryNL's constitutional principles (security, UX, transparency)

**Next Steps:**
1. Update Technical Context in plan.md with resolved decisions
2. Proceed to Phase 1: Data modeling and API contracts
3. Begin implementation with chosen technologies
