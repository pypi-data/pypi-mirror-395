# Memory Backends

The Ceylon AI Framework provides a flexible memory abstraction that allows agents to store and retrieve information. This document describes the available memory backends.

## Overview

All memory backends implement the `Memory` trait defined in `runtime/src/core/memory.rs`:

```rust
#[async_trait]
pub trait Memory: Send + Sync {
    async fn store(&self, entry: MemoryEntry) -> Result<String>;
    async fn get(&self, id: &str) -> Result<Option<MemoryEntry>>;
    async fn search(&self, query: MemoryQuery) -> Result<Vec<MemoryEntry>>;
    async fn delete(&self, id: &str) -> Result<bool>;
    async fn clear(&self) -> Result<()>;
    async fn count(&self) -> Result<usize>;
}
```

## Available Backends

### 1. InMemoryBackend (Default)

**Location:** `runtime/src/memory/backends/in_memory.rs`

A fast, thread-safe in-memory storage backend using `DashMap`.

**Features:**
- ✅ Thread-safe concurrent access
- ✅ TTL (Time-To-Live) support with automatic expiration
- ✅ LRU eviction with configurable max entries
- ✅ Metadata filtering
- ✅ Keyword search
- ❌ No persistence (data lost on restart)
- ❌ Limited by available RAM

**Usage:**

```rust
use runtime::memory::InMemoryBackend;
use std::sync::Arc;

// Basic usage
let memory = InMemoryBackend::new();

// With configuration
let memory = InMemoryBackend::new()
    .with_max_entries(1000)    // Limit to 1000 entries
    .with_ttl_seconds(3600);   // Default 1 hour TTL

// Use with agent
let agent = LlmAgent::builder("agent", "ollama::llama3.2")
    .with_memory(Arc::new(memory))
    .build()?;
```

**When to use:**
- Development and testing
- Single-process applications
- Short-lived sessions
- Limited data requirements

---

### 2. RedisBackend (Production)

**Location:** `runtime/src/memory/backends/redis.rs`
**Feature Flag:** `redis`

A production-ready persistent storage backend using Redis.

**Features:**
- ✅ Persistent storage across restarts
- ✅ Distributed/multi-process shared memory
- ✅ Native TTL support via Redis EXPIRE
- ✅ Connection pooling for high performance
- ✅ Namespace isolation (multi-tenant support)
- ✅ Atomic operations
- ✅ Scalable to millions of entries
- ✅ Production-tested reliability

**Prerequisites:**

1. Install Redis:
   ```bash
   # macOS
   brew install redis && redis-server

   # Linux (Debian/Ubuntu)
   sudo apt-get install redis-server && redis-server

   # Docker
   docker run -d -p 6379:6379 redis:latest
   ```

2. Enable the feature flag:
   ```toml
   # Cargo.toml
   [dependencies]
   runtime = { path = "runtime", features = ["redis"] }
   ```

**Usage:**

```rust
use runtime::memory::RedisBackend;
use std::sync::Arc;

// Basic connection
let memory = RedisBackend::new("redis://localhost:6379").await?;

// With configuration
let memory = RedisBackend::new("redis://localhost:6379").await?
    .with_prefix("my_app")        // Namespace isolation
    .with_ttl_seconds(7200);      // Default 2 hour TTL

// Redis Cluster
let memory = RedisBackend::new("redis://node1:6379,node2:6379").await?;

// With authentication
let memory = RedisBackend::new("redis://:password@localhost:6379").await?;

// Redis Sentinel
let memory = RedisBackend::new("redis-sentinel://localhost:26379/mymaster").await?;

// Use with agent
let agent = LlmAgent::builder("agent", "ollama::llama3.2")
    .with_memory(Arc::new(memory))
    .build()?;
```

**Storage Format:**

Redis stores each memory entry as a Hash with the following structure:

- **Key:** `{prefix}:memory:{entry_id}`
- **Index Set:** `{prefix}:memory:index` (contains all entry IDs)

**Hash Fields:**
- `content`: The actual content string
- `metadata`: JSON-encoded metadata HashMap
- `embedding`: JSON-encoded embedding vector (optional)
- `created_at`: ISO 8601 timestamp
- `expires_at`: ISO 8601 timestamp (if TTL set)

**Configuration Options:**

| Method | Description | Default |
|--------|-------------|---------|
| `with_prefix(prefix)` | Set key namespace prefix | `"ceylon"` |
| `with_ttl_seconds(seconds)` | Default TTL for entries | None (no expiration) |

**When to use:**
- Production applications
- Multi-process/distributed systems
- Long-term memory persistence
- Shared memory across services
- High-throughput applications
- Multi-tenant applications (with namespaces)

**Performance:**

- **Write:** ~10,000-50,000 ops/sec (single Redis instance)
- **Read:** ~20,000-100,000 ops/sec (single Redis instance)
- **Scalability:** Linear with Redis Cluster
- **Latency:** <1ms for local Redis, ~1-5ms for network

**Production Deployment:**

```rust
use runtime::memory::RedisBackend;
use std::env;

// Read from environment
let redis_url = env::var("REDIS_URL")
    .unwrap_or_else(|_| "redis://localhost:6379".to_string());

let memory = RedisBackend::new(&redis_url).await?
    .with_prefix(env::var("APP_NAME").unwrap_or_else(|_| "app".into()))
    .with_ttl_seconds(86400); // 24 hour default TTL

// Connection pooling is built-in via ConnectionManager
// No additional configuration needed
```

**Error Handling:**

```rust
use runtime::memory::RedisBackend;

match RedisBackend::new("redis://localhost:6379").await {
    Ok(backend) => {
        println!("Connected to Redis successfully");
        // Use backend
    }
    Err(e) => {
        eprintln!("Failed to connect to Redis: {}", e);
        // Fall back to InMemoryBackend or handle error
    }
}
```

**Testing:**

```bash
# Run Redis backend tests (requires Redis server)
cargo test --features redis redis

# Run specific test
cargo test --features redis test_basic_storage -- --nocapture
```

Tests are marked with `#[ignore]` by default since they require a Redis server. Run with:

```bash
# Start Redis
redis-server

# Run tests
cargo test --features redis -- --ignored --nocapture
```

---

### 3. SqliteBackend

**Location:** `runtime/src/memory/backends/sqlite.rs`
**Feature Flag:** `sqlite`

A file-based persistent storage backend using SQLite.

**Features:**
- ✅ Persistent storage in a single file
- ✅ Good for moderate data sizes
- ✅ Embedded (no separate server needed)
- ✅ ACID transactions
- ⚠️ Single-writer limitation
- ⚠️ Not ideal for distributed systems

**Usage:**

```rust
use runtime::memory::SqliteBackend;

// File-based
let memory = SqliteBackend::new("memory.db").await?;

// In-memory SQLite (testing)
let memory = SqliteBackend::in_memory().await?;
```

**When to use:**
- Single-process applications
- Moderate data sizes (<100GB)
- File-based persistence preferred
- Embedded scenarios (desktop apps)

---

## Comparison Matrix

| Feature | InMemory | Redis | SQLite |
|---------|----------|-------|--------|
| **Persistence** | ❌ | ✅ | ✅ |
| **Multi-process** | ❌ | ✅ | ❌ |
| **Distributed** | ❌ | ✅ | ❌ |
| **Performance** | Fastest | Very Fast | Fast |
| **Scalability** | Limited by RAM | Excellent | Moderate |
| **TTL Support** | ✅ | ✅ (native) | ✅ |
| **Setup** | None | Redis server | None |
| **Production Ready** | ⚠️ | ✅ | ⚠️ |

## Python Bindings

All backends are available in Python:

```python
from ceylon import InMemoryBackend, RedisBackend, LlmAgent

# In-memory
memory = InMemoryBackend()

# Redis (requires redis feature)
memory = RedisBackend("redis://localhost:6379")
memory = memory.with_prefix("my_app")
memory = memory.with_ttl_seconds(3600)

# Use with agent
agent = LlmAgent("agent", "ollama::llama3.2:latest")
agent.with_memory(memory)
agent.build()
```

## Examples

### Rust Examples

- **In-Memory:** See tests in `runtime/src/memory/backends/in_memory.rs`
- **Redis:** `cargo run --example redis_memory --features redis`
- **SQLite:** See tests in `runtime/src/memory/backends/sqlite.rs`

### Python Examples

- **In-Memory:** `bindings/python/examples/demo_agent_memory.py`
- **Redis:** `bindings/python/examples/demo_redis_memory.py`

## Creating Custom Backends

To create a custom memory backend:

1. Implement the `Memory` trait:

```rust
use runtime::core::memory::{Memory, MemoryEntry, MemoryQuery};
use async_trait::async_trait;

pub struct MyCustomBackend {
    // Your fields
}

#[async_trait]
impl Memory for MyCustomBackend {
    async fn store(&self, entry: MemoryEntry) -> Result<String> {
        // Your implementation
    }

    async fn get(&self, id: &str) -> Result<Option<MemoryEntry>> {
        // Your implementation
    }

    // ... implement other methods
}
```

2. Add Python bindings if needed (see `bindings/python/src/lib.rs`)

3. Add feature flag in `runtime/Cargo.toml`

4. Export from `runtime/src/memory/backends/mod.rs`

## Best Practices

### Development
- Use `InMemoryBackend` for quick iterations
- Clear memory between test runs
- Use moderate TTLs to prevent unbounded growth

### Production
- Use `RedisBackend` for persistence and scalability
- Set appropriate TTLs based on data lifetime requirements
- Use namespace prefixes for multi-tenant applications
- Monitor Redis memory usage with `INFO memory`
- Enable Redis persistence (RDB/AOF) for durability
- Consider Redis Cluster for horizontal scaling

### Memory Management
- Always set TTLs for time-sensitive data
- Use metadata filters to organize entries
- Implement cleanup routines for old data
- Monitor memory usage and set limits

## Troubleshooting

### Redis Connection Issues

```rust
// Test connection
use redis::Client;

let client = Client::open("redis://localhost:6379")?;
let mut con = client.get_connection()?;
let _: () = redis::cmd("PING").query(&mut con)?;
println!("Redis connection OK");
```

### Performance Issues

- **Slow queries:** Add indexes or use metadata filters
- **High memory:** Set TTLs or implement cleanup
- **Connection errors:** Use connection pooling (built-in)

## Support

For issues or questions:
- GitHub: https://github.com/ceylonai/ceylon
- Documentation: See inline code documentation
- Examples: `runtime/examples/` and `bindings/python/examples/`
