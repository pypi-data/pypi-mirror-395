# WebSocket Protocol Specification

**Version**: 1.0.0
**Date**: 2025-10-11
**Endpoint**: `ws://localhost:8765/ws`

---

## Overview

The QueryNL WebSocket connection enables real-time bidirectional communication between the VS Code extension and the backend service. It supports:

- Real-time query generation progress updates
- Schema introspection progress
- Connection status changes
- LLM streaming responses
- Heartbeat/keepalive

---

## Connection

### Handshake

**Client → Server (Initial Connection)**

```json
{
  "type": "authenticate",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "client_version": "1.0.0"
}
```

**Server → Client (Authentication Response)**

```json
{
  "type": "authenticated",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "session_id": "660e8400-e29b-41d4-a716-446655440001",
  "server_version": "1.0.0"
}
```

**Server → Client (Authentication Failure)**

```json
{
  "type": "error",
  "error_code": "authentication_failed",
  "message": "Invalid or expired token",
  "close_connection": true
}
```

### Reconnection

The client uses `reconnecting-websocket` library with exponential backoff:

- Initial reconnection delay: 1 second
- Maximum reconnection delay: 30 seconds
- Backoff multiplier: 1.5
- Maximum reconnection attempts: Unlimited

Upon reconnection, client re-authenticates with the same token. Server restores session state if session_id is provided.

---

## Message Format

All messages follow this structure:

```typescript
interface WebSocketMessage {
  type: string;                    // Message type identifier
  request_id?: string;              // UUID for request-response correlation
  timestamp: string;                // ISO 8601 timestamp
  payload: object | null;           // Message-specific data
}
```

---

## Message Types

### 1. Heartbeat

**Purpose**: Keep connection alive and detect disconnections

**Client → Server (Ping)**

```json
{
  "type": "ping",
  "timestamp": "2025-10-11T10:30:00Z"
}
```

**Server → Client (Pong)**

```json
{
  "type": "pong",
  "timestamp": "2025-10-11T10:30:00Z"
}
```

**Timing:**
- Client sends ping every 30 seconds
- Server responds with pong within 5 seconds
- If no pong received within 10 seconds, client considers connection dead and reconnects

---

### 2. Query Generation (Streaming)

**Client → Server (Request)**

```json
{
  "type": "query.generate",
  "request_id": "req_123",
  "timestamp": "2025-10-11T10:30:00Z",
  "payload": {
    "natural_language_query": "show me all users created today",
    "connection_id": "conn_456",
    "session_id": "session_789",
    "stream": true
  }
}
```

**Server → Client (Streaming Progress)**

```json
{
  "type": "query.generate.progress",
  "request_id": "req_123",
  "timestamp": "2025-10-11T10:30:01Z",
  "payload": {
    "stage": "analyzing_schema",
    "progress": 0.2,
    "message": "Introspecting database schema..."
  }
}
```

**Server → Client (Partial Result - Token Streaming)**

```json
{
  "type": "query.generate.chunk",
  "request_id": "req_123",
  "timestamp": "2025-10-11T10:30:02Z",
  "payload": {
    "chunk": "SELECT * FROM users ",
    "accumulated": "SELECT * FROM users "
  }
}
```

**Server → Client (Completion)**

```json
{
  "type": "query.generate.complete",
  "request_id": "req_123",
  "timestamp": "2025-10-11T10:30:03Z",
  "payload": {
    "sql_query": "SELECT * FROM users WHERE created_at >= CURRENT_DATE",
    "explanation": "This query retrieves all user records created today.",
    "confidence": 0.95,
    "is_destructive": false,
    "token_count": 85
  }
}
```

**Server → Client (Error)**

```json
{
  "type": "query.generate.error",
  "request_id": "req_123",
  "timestamp": "2025-10-11T10:30:03Z",
  "payload": {
    "error_code": "ambiguous_query",
    "message": "Multiple interpretations possible. Please clarify...",
    "suggestions": ["Option A: ...", "Option B: ..."]
  }
}
```

**Progress Stages:**
- `validating_input` (0.0-0.1): Validating request
- `analyzing_schema` (0.1-0.3): Introspecting database schema
- `generating_query` (0.3-0.8): LLM processing
- `validating_sql` (0.8-0.9): Syntax validation
- `complete` (1.0): Done

---

### 3. Schema Introspection (Long-Running)

**Client → Server (Request)**

```json
{
  "type": "schema.introspect",
  "request_id": "req_200",
  "timestamp": "2025-10-11T10:31:00Z",
  "payload": {
    "connection_id": "conn_456",
    "refresh_cache": true
  }
}
```

**Server → Client (Progress)**

```json
{
  "type": "schema.introspect.progress",
  "request_id": "req_200",
  "timestamp": "2025-10-11T10:31:05Z",
  "payload": {
    "stage": "fetching_tables",
    "progress": 0.4,
    "message": "Fetching 150 tables...",
    "tables_processed": 60,
    "tables_total": 150
  }
}
```

**Server → Client (Completion)**

```json
{
  "type": "schema.introspect.complete",
  "request_id": "req_200",
  "timestamp": "2025-10-11T10:31:15Z",
  "payload": {
    "tables": [...],
    "relationships": [...],
    "total_tables": 150,
    "introspection_time_ms": 15000
  }
}
```

---

### 4. Connection Status Updates

**Server → Client (Status Change)**

```json
{
  "type": "connection.status_changed",
  "timestamp": "2025-10-11T10:32:00Z",
  "payload": {
    "connection_id": "conn_456",
    "old_status": "connected",
    "new_status": "disconnected",
    "reason": "connection_timeout",
    "message": "Database connection lost. Please reconnect."
  }
}
```

**Possible Status Values:**
- `connecting`: Connection attempt in progress
- `connected`: Successfully connected
- `disconnected`: Not connected
- `error`: Connection error

**Reason Codes:**
- `user_initiated`: User disconnected
- `connection_timeout`: Database connection timeout
- `authentication_failed`: Invalid credentials
- `network_error`: Network connectivity issue

---

### 5. Query Execution (Async)

**Client → Server (Request)**

```json
{
  "type": "query.execute",
  "request_id": "req_300",
  "timestamp": "2025-10-11T10:33:00Z",
  "payload": {
    "sql_query": "SELECT * FROM users WHERE status = 'active'",
    "connection_id": "conn_456",
    "session_id": "session_789",
    "confirm_destructive": false
  }
}
```

**Server → Client (Progress)**

```json
{
  "type": "query.execute.progress",
  "request_id": "req_300",
  "timestamp": "2025-10-11T10:33:01Z",
  "payload": {
    "stage": "executing",
    "progress": 0.5,
    "message": "Executing query..."
  }
}
```

**Server → Client (Completion)**

```json
{
  "type": "query.execute.complete",
  "request_id": "req_300",
  "timestamp": "2025-10-11T10:33:03Z",
  "payload": {
    "success": true,
    "rows": [...],
    "row_count": 42,
    "execution_time_ms": 123,
    "columns": [...]
  }
}
```

---

### 6. LLM Token Usage Updates

**Server → Client (Usage Update)**

```json
{
  "type": "usage.update",
  "timestamp": "2025-10-11T10:34:00Z",
  "payload": {
    "session_id": "session_789",
    "tokens_used_this_request": 85,
    "tokens_used_session": 450,
    "tokens_used_billing_cycle": 8250,
    "quota_remaining": 1750,
    "quota_limit": 10000
  }
}
```

**Constitution Compliance**: Principle III (Transparency) - Users always see token usage

---

### 7. Schema Design Progress

**Client → Server (Request)**

```json
{
  "type": "schema.design",
  "request_id": "req_400",
  "timestamp": "2025-10-11T10:35:00Z",
  "payload": {
    "description": "I need users, products, orders, and reviews",
    "database_type": "postgresql"
  }
}
```

**Server → Client (Progress)**

```json
{
  "type": "schema.design.progress",
  "request_id": "req_400",
  "timestamp": "2025-10-11T10:35:05Z",
  "payload": {
    "stage": "generating_tables",
    "progress": 0.6,
    "message": "Designing table structures...",
    "tables_generated": ["users", "products", "orders"]
  }
}
```

**Server → Client (Completion)**

```json
{
  "type": "schema.design.complete",
  "request_id": "req_400",
  "timestamp": "2025-10-11T10:35:10Z",
  "payload": {
    "schema_id": "schema_500",
    "tables": [...],
    "relationships": [...],
    "rationale": {...},
    "mermaid_diagram": "erDiagram\n  USERS ||--o{ ORDERS : places\n  ..."
  }
}
```

---

### 8. Error Handling

**Server → Client (General Error)**

```json
{
  "type": "error",
  "request_id": "req_123",
  "timestamp": "2025-10-11T10:36:00Z",
  "payload": {
    "error_code": "database_error",
    "message": "Failed to connect to database",
    "details": {
      "reason": "Connection refused",
      "host": "localhost",
      "port": 5432
    },
    "recoverable": true,
    "retry_after_seconds": 30
  }
}
```

**Common Error Codes:**
- `authentication_failed`: Invalid auth token
- `database_error`: Database connection or query error
- `validation_error`: Invalid request payload
- `rate_limit_exceeded`: Quota exceeded
- `internal_error`: Server error
- `ambiguous_query`: Query needs clarification
- `destructive_operation`: Requires confirmation

---

### 9. Clarification Requests

**Server → Client (Clarification Needed)**

```json
{
  "type": "query.clarification_needed",
  "request_id": "req_123",
  "timestamp": "2025-10-11T10:37:00Z",
  "payload": {
    "question": "Did you mean 'users' table or 'user_accounts' table?",
    "options": [
      {"id": "opt_1", "text": "users table", "sql_preview": "SELECT * FROM users..."},
      {"id": "opt_2", "text": "user_accounts table", "sql_preview": "SELECT * FROM user_accounts..."}
    ]
  }
}
```

**Client → Server (Clarification Response)**

```json
{
  "type": "query.clarification_response",
  "request_id": "req_123",
  "timestamp": "2025-10-11T10:37:05Z",
  "payload": {
    "selected_option_id": "opt_1"
  }
}
```

---

### 10. Cancel Request

**Client → Server (Cancel)**

```json
{
  "type": "cancel",
  "request_id": "req_123",
  "timestamp": "2025-10-11T10:38:00Z"
}
```

**Server → Client (Cancelled)**

```json
{
  "type": "cancelled",
  "request_id": "req_123",
  "timestamp": "2025-10-11T10:38:01Z",
  "payload": {
    "message": "Query generation cancelled by user"
  }
}
```

---

## Connection Lifecycle

```
1. Client connects to ws://localhost:8765/ws
2. Client sends "authenticate" message
3. Server validates token
4. Server responds with "authenticated" or closes connection
5. Client and server exchange heartbeats every 30 seconds
6. Client sends requests (query.generate, schema.design, etc.)
7. Server sends progress updates and final responses
8. On disconnect, client auto-reconnects with exponential backoff
9. On reconnect, client re-authenticates
10. Client can gracefully close connection or server can close on error
```

---

## Error Recovery

### Client-Side

1. **Connection Lost**: Auto-reconnect with exponential backoff
2. **Timeout (no pong)**: Close connection and reconnect
3. **Message Parsing Error**: Log error, continue processing other messages
4. **Authentication Failed**: Prompt user to re-authenticate
5. **Rate Limit Exceeded**: Queue messages until quota resets

### Server-Side

1. **Client Disconnected**: Clean up session resources after 5 minutes
2. **Invalid Message Format**: Send error message, maintain connection
3. **LLM API Error**: Send error to client with retry suggestion
4. **Database Error**: Send error to client, maintain WebSocket connection

---

## Performance Characteristics

**Target Latency:**
- Heartbeat round-trip: <100ms
- Message acknowledgement: <50ms
- Query generation start (first progress): <500ms
- Query generation streaming: <100ms per chunk

**Throughput:**
- Maximum concurrent requests per connection: 5
- Maximum message size: 1 MB
- Maximum connections per user: 10

**Resource Limits:**
- Server buffers up to 100 messages per connection if client is slow
- If buffer full, server drops oldest messages and sends warning
- Client buffers up to 50 messages during reconnection

---

## Security

### Authentication
- JWT token required in initial handshake
- Token expires after 24 hours (renewable)
- Invalid/expired token → immediate connection close

### Message Validation
- All messages validated against JSON schema
- SQL queries sanitized before execution (principle I: Security-First)
- Rate limiting applied per user (principle V: Fail-Safe Defaults)

### Transport Security
- Local development: `ws://` (unencrypted)
- Production: `wss://` (TLS encrypted)
- Certificate validation required in production

---

## Testing

### Integration Tests

**Test Cases:**
1. Connection establishment and authentication
2. Heartbeat mechanism
3. Query generation streaming
4. Reconnection after disconnect
5. Error handling for each message type
6. Concurrent request handling
7. Message buffering during slow client
8. Graceful shutdown

### Load Testing

**Targets:**
- 1,000 concurrent connections
- 100 messages/second per connection
- Reconnection storm (1,000 clients reconnect simultaneously)

---

## Example Client Implementation (TypeScript)

```typescript
import ReconnectingWebSocket from 'reconnecting-websocket';

class QueryNLWebSocketClient {
  private ws: ReconnectingWebSocket;
  private pendingRequests: Map<string, (data: any) => void> = new Map();

  constructor(token: string) {
    this.ws = new ReconnectingWebSocket('ws://localhost:8765/ws', [], {
      connectionTimeout: 5000,
      maxRetries: Infinity,
      maxReconnectionDelay: 30000,
      minReconnectionDelay: 1000,
    });

    this.ws.addEventListener('open', () => {
      this.authenticate(token);
      this.startHeartbeat();
    });

    this.ws.addEventListener('message', (event) => {
      const message = JSON.parse(event.data);
      this.handleMessage(message);
    });
  }

  private authenticate(token: string) {
    this.send({
      type: 'authenticate',
      token,
      client_version: '1.0.0',
      timestamp: new Date().toISOString(),
    });
  }

  private startHeartbeat() {
    setInterval(() => {
      this.send({ type: 'ping', timestamp: new Date().toISOString() });
    }, 30000);
  }

  async generateQuery(naturalLanguageQuery: string, connectionId: string): Promise<any> {
    const requestId = crypto.randomUUID();

    return new Promise((resolve) => {
      this.pendingRequests.set(requestId, resolve);

      this.send({
        type: 'query.generate',
        request_id: requestId,
        timestamp: new Date().toISOString(),
        payload: {
          natural_language_query: naturalLanguageQuery,
          connection_id: connectionId,
          stream: true,
        },
      });
    });
  }

  private handleMessage(message: any) {
    if (message.type === 'query.generate.complete' && message.request_id) {
      const resolver = this.pendingRequests.get(message.request_id);
      if (resolver) {
        resolver(message.payload);
        this.pendingRequests.delete(message.request_id);
      }
    }
    // Handle other message types...
  }

  private send(data: any) {
    this.ws.send(JSON.stringify(data));
  }
}
```

---

## Compliance with Constitution

### Principle I (Security-First Design)
- JWT authentication required
- TLS encryption in production
- SQL injection prevention via validation

### Principle III (Transparency)
- Token usage sent after each LLM operation
- Progress updates for all long-running operations
- Error messages are detailed and actionable

### Principle V (Fail-Safe Defaults)
- Destructive operations flagged
- Automatic reconnection with exponential backoff
- Rate limiting prevents quota exhaustion

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-10-11 | Initial specification |
