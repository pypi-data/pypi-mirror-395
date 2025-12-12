# InMemoryBackend

The `InMemoryBackend` class provides an in-memory storage backend for agent memory. It supports TTL-based expiration, metadata filtering, LRU eviction, and full-text search capabilities.

## Class Signature

```python
class InMemoryBackend(PyInMemoryBackend):
    def __init__(self) -> None:
        ...

    @classmethod
    def with_max_entries(cls, max_entries: int) -> InMemoryBackend:
        ...

    @classmethod
    def with_ttl_seconds(cls, ttl_seconds: int) -> InMemoryBackend:
        ...
```

## Description

`InMemoryBackend` is a Python wrapper around `PyInMemoryBackend` that implements the Memory interface for storing and querying agent memory entries. It stores entries in memory with optional maximum size limit and automatic cleanup of expired entries.

## Constructor

### `__init__()`

Creates a new in-memory backend instance with default settings.

**Parameters:** None

**Returns:** InMemoryBackend instance

**Notes:**
- No maximum entry limit by default
- Entries are stored indefinitely unless TTL is set

**Example:**
```python
from ceylonai_next import InMemoryBackend

# Create basic backend
backend = InMemoryBackend()

# Store and retrieve
from ceylonai_next import MemoryEntry
entry = MemoryEntry("Hello")
entry_id = backend.store(entry)
retrieved = backend.get(entry_id)
```

---

## Class Methods

### `with_max_entries(max_entries: int) -> InMemoryBackend`

Create a backend with a maximum entry limit using LRU eviction.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `max_entries` | `int` | Maximum number of entries to store |

**Returns:** `InMemoryBackend` - Configured instance

**Notes:**
- When limit is reached, oldest entries are evicted (LRU)
- Useful for memory-constrained environments
- Balances memory usage with data retention

**Example:**
```python
from ceylonai_next import InMemoryBackend

# Backend with max 100 entries
backend = InMemoryBackend.with_max_entries(100)

# Useful for conversation history
chat_memory = InMemoryBackend.with_max_entries(1000)

# Tight limit for resource-constrained environments
limited_memory = InMemoryBackend.with_max_entries(10)
```

---

### `with_ttl_seconds(ttl_seconds: int) -> InMemoryBackend`

Create a backend with default TTL for all entries.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `ttl_seconds` | `int` | Time-to-live in seconds for all stored entries |

**Returns:** `InMemoryBackend` - Configured instance

**Notes:**
- Applies to all entries unless overridden per-entry
- Entries expire automatically after TTL
- Useful for temporary/session-based data

**Example:**
```python
from ceylonai_next import InMemoryBackend

# All entries expire after 1 hour
backend = InMemoryBackend.with_ttl_seconds(3600)

# Session-based memory (5 minute expiration)
session_memory = InMemoryBackend.with_ttl_seconds(300)

# Short-lived cache (30 seconds)
cache_memory = InMemoryBackend.with_ttl_seconds(30)
```

---

## Instance Methods

### `store(entry: MemoryEntry) -> str`

Store a memory entry and return its unique ID.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `entry` | `MemoryEntry` | Entry to store |

**Returns:** `str` - Unique identifier for the stored entry

**Raises:**
- `RuntimeError` - If storage fails

**Example:**
```python
from ceylonai_next import InMemoryBackend, MemoryEntry

backend = InMemoryBackend()

entry = MemoryEntry("Important data")
entry.with_metadata("category", "important")

entry_id = backend.store(entry)
print(f"Stored with ID: {entry_id}")

# Store multiple entries
ids = []
for i in range(5):
    e = MemoryEntry(f"Entry {i}")
    ids.append(backend.store(e))
```

---

### `get(id: str) -> MemoryEntry | None`

Retrieve a memory entry by its ID.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | `str` | Entry ID from store() |

**Returns:** `MemoryEntry | None` - Entry if found and not expired, None otherwise

**Notes:**
- Returns None if entry doesn't exist
- Returns None if entry has expired
- Non-blocking operation

**Example:**
```python
from ceylonai_next import InMemoryBackend, MemoryEntry

backend = InMemoryBackend()

# Store entry
entry = MemoryEntry("Data to retrieve")
entry_id = backend.store(entry)

# Retrieve immediately
retrieved = backend.get(entry_id)
if retrieved:
    print(f"Found: {retrieved.content}")

# Non-existent entry
missing = backend.get("invalid-id")
print(missing is None)  # True
```

---

### `search(query: MemoryQuery) -> List[MemoryEntry]`

Search for entries matching the query criteria.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | `MemoryQuery` | Query with filters and options |

**Returns:** `List[MemoryEntry]` - Matching entries (newest first)

**Notes:**
- Results ordered by creation time (newest first)
- Filters use AND logic (all must match)
- Expired entries excluded automatically
- Respects limit from query

**Example:**
```python
from ceylonai_next import InMemoryBackend, MemoryEntry, MemoryQuery

backend = InMemoryBackend()

# Store entries with metadata
for i in range(5):
    entry = MemoryEntry(f"Message {i}")
    entry.with_metadata("type", "message")
    entry.with_metadata("user", "alice" if i % 2 == 0 else "bob")
    backend.store(entry)

# Search: Get all messages
query = MemoryQuery()
query.with_filter("type", "message")
results = backend.search(query)
print(f"Found {len(results)} messages")

# Search: Get Alice's messages only
alice_query = MemoryQuery()
alice_query.with_filter("type", "message")
alice_query.with_filter("user", "alice")
alice_messages = backend.search(alice_query)
print(f"Alice's messages: {len(alice_messages)}")

# Search with limit
limited_query = MemoryQuery()
limited_query.with_filter("type", "message")
limited_query.with_limit(2)
limited_results = backend.search(limited_query)
print(f"First 2 messages: {len(limited_results)}")
```

---

### `delete(id: str) -> bool`

Delete a memory entry by its ID.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | `str` | Entry ID to delete |

**Returns:** `bool` - True if deleted, False if not found

**Example:**
```python
from ceylonai_next import InMemoryBackend, MemoryEntry

backend = InMemoryBackend()

# Store and delete
entry = MemoryEntry("To delete")
entry_id = backend.store(entry)

print(backend.count())  # 1
deleted = backend.delete(entry_id)
print(f"Deleted: {deleted}")  # True
print(backend.count())  # 0

# Delete non-existent
result = backend.delete("invalid-id")
print(f"Deleted: {result}")  # False
```

---

### `clear()`

Delete all entries from the backend.

**Parameters:** None

**Returns:** `None`

**Example:**
```python
from ceylonai_next import InMemoryBackend, MemoryEntry

backend = InMemoryBackend()

# Store multiple entries
for i in range(10):
    backend.store(MemoryEntry(f"Entry {i}"))

print(f"Count before: {backend.count()}")  # 10

# Clear all
backend.clear()

print(f"Count after: {backend.count()}")   # 0
```

---

### `count() -> int`

Get the total number of entries in the backend.

**Parameters:** None

**Returns:** `int` - Number of non-expired entries

**Notes:**
- Does not count expired entries
- Fast O(1) operation

**Example:**
```python
from ceylonai_next import InMemoryBackend, MemoryEntry
import time

backend = InMemoryBackend()

print(f"Empty: {backend.count()}")  # 0

# Add entries
backend.store(MemoryEntry("Entry 1"))
backend.store(MemoryEntry("Entry 2"))
print(f"After adding: {backend.count()}")  # 2

# Add entry with TTL
temp = MemoryEntry("Temporary")
temp.with_ttl_seconds(1)
backend.store(temp)
print(f"Before expiration: {backend.count()}")  # 3

# Wait for expiration
time.sleep(2)
print(f"After expiration: {backend.count()}")   # 2
```

## Complete Examples

### Example 1: Basic Storage and Retrieval

```python
from ceylonai_next import InMemoryBackend, MemoryEntry

def main():
    # Create backend
    backend = InMemoryBackend()

    # Create and store entry
    entry = MemoryEntry("Important information")
    entry.with_metadata("source", "user_input")
    entry.with_metadata("importance", 5)

    entry_id = backend.store(entry)
    print(f"Stored entry: {entry_id}")

    # Retrieve entry
    retrieved = backend.get(entry_id)
    if retrieved:
        print(f"Content: {retrieved.content}")
        print(f"Metadata: {retrieved.metadata}")
        print(f"Created: {retrieved.created_at}")

if __name__ == "__main__":
    main()
```

### Example 2: Conversation Memory

```python
from ceylonai_next import InMemoryBackend, MemoryEntry, MemoryQuery

def create_conversation_memory():
    """Create memory for multi-user conversation"""
    return InMemoryBackend.with_max_entries(500)

def add_message(backend, speaker, user_id, content, session_id):
    """Add a conversation message"""
    entry = MemoryEntry(content)
    entry.with_metadata("speaker", speaker)
    entry.with_metadata("user_id", user_id)
    entry.with_metadata("session_id", session_id)
    entry.with_metadata("type", "message")
    return backend.store(entry)

def get_user_messages(backend, user_id, session_id):
    """Get all messages from a user"""
    query = MemoryQuery()
    query.with_filter("user_id", user_id)
    query.with_filter("session_id", session_id)
    query.with_filter("speaker", "user")
    return backend.search(query)

def get_conversation_history(backend, session_id, limit=50):
    """Get full conversation history"""
    query = MemoryQuery()
    query.with_filter("session_id", session_id)
    query.with_limit(limit)
    return backend.search(query)

def main():
    # Create backend
    memory = create_conversation_memory()
    session = "chat_001"

    # Simulate conversation
    conversation = [
        ("user", "alice", "Hello!"),
        ("assistant", "bot", "Hi Alice! How can I help?"),
        ("user", "alice", "What's Python?"),
        ("assistant", "bot", "Python is a programming language..."),
        ("user", "bob", "Hey there!"),
        ("assistant", "bot", "Hello Bob!"),
    ]

    print("=== Storing Conversation ===")
    for speaker, user_id, content in conversation:
        add_message(memory, speaker, user_id, content, session)

    print(f"Total messages: {memory.count()}\n")

    # Query: Get Alice's messages
    print("=== Alice's Messages ===")
    alice_msgs = get_user_messages(memory, "alice", session)
    for entry in alice_msgs:
        print(f"- {entry.content}")

    print(f"\n=== Full History ===")
    history = get_conversation_history(memory, session)
    for entry in history:
        speaker = entry.metadata.get("speaker", "?")
        print(f"[{speaker}] {entry.content}")

if __name__ == "__main__":
    main()
```

### Example 3: TTL and Expiration

```python
import time
from ceylonai_next import InMemoryBackend, MemoryEntry, MemoryQuery

def main():
    # Create backend with default 2-second TTL
    backend = InMemoryBackend.with_ttl_seconds(2)

    # Store entry with default TTL
    entry1 = MemoryEntry("Expires with default TTL")
    id1 = backend.store(entry1)

    # Store entry with longer TTL
    entry2 = MemoryEntry("Longer lifetime")
    entry2.with_ttl_seconds(10)
    id2 = backend.store(entry2)

    print(f"Initial count: {backend.count()}")  # 2

    # Check after 3 seconds
    time.sleep(3)
    print(f"After 3 seconds: {backend.count()}")
    print(f"Entry 1 exists: {backend.get(id1) is not None}")  # False
    print(f"Entry 2 exists: {backend.get(id2) is not None}")  # True

    # Wait for entry 2 to expire
    time.sleep(8)
    print(f"\nAfter 11 seconds total: {backend.count()}")  # 0

if __name__ == "__main__":
    main()
```

### Example 4: LRU Eviction

```python
from ceylonai_next import InMemoryBackend, MemoryEntry
import time

def main():
    # Create backend with max 3 entries
    backend = InMemoryBackend.with_max_entries(3)

    # Store entries
    ids = []
    for i in range(5):
        entry = MemoryEntry(f"Entry {i}")
        entry_id = backend.store(entry)
        ids.append(entry_id)
        time.sleep(0.01)  # Ensure different timestamps

    print(f"Stored 5 entries, but max is 3")
    print(f"Current count: {backend.count()}")  # 3

    # Check which entries remain (newest ones)
    print("\nRemaining entries (by ID):")
    print(f"Entry 0 (oldest): {backend.get(ids[0]) is not None}")   # False (evicted)
    print(f"Entry 1: {backend.get(ids[1]) is not None}")            # False (evicted)
    print(f"Entry 2: {backend.get(ids[2]) is not None}")            # True (kept)
    print(f"Entry 3: {backend.get(ids[3]) is not None}")            # True (kept)
    print(f"Entry 4 (newest): {backend.get(ids[4]) is not None}")   # True (kept)

if __name__ == "__main__":
    main()
```

### Example 5: Search with Complex Filters

```python
from ceylonai_next import InMemoryBackend, MemoryEntry, MemoryQuery

def main():
    backend = InMemoryBackend()

    # Create knowledge base
    documents = [
        ("Python for beginners", "python", "tutorial", 1),
        ("Advanced Python", "python", "advanced", 2),
        ("JavaScript basics", "javascript", "tutorial", 1),
        ("React framework", "javascript", "library", 2),
        ("Web development guide", "mixed", "guide", 2),
    ]

    for title, language, category, level in documents:
        entry = MemoryEntry(title)
        entry.with_metadata("language", language)
        entry.with_metadata("category", category)
        entry.with_metadata("level", level)
        backend.store(entry)

    print(f"Stored {backend.count()} documents\n")

    # Search: Python tutorials
    q1 = MemoryQuery()
    q1.with_filter("language", "python")
    q1.with_filter("category", "tutorial")
    python_tutorials = backend.search(q1)
    print("Python tutorials:")
    for doc in python_tutorials:
        print(f"  - {doc.content}")

    # Search: Advanced materials
    q2 = MemoryQuery()
    q2.with_filter("level", 2)
    advanced = backend.search(q2)
    print(f"\nAdvanced materials ({len(advanced)}):")
    for doc in advanced:
        print(f"  - {doc.content} ({doc.metadata['language']})")

    # Search: All JavaScript content
    q3 = MemoryQuery()
    q3.with_filter("language", "javascript")
    js_content = backend.search(q3)
    print(f"\nJavaScript content ({len(js_content)}):")
    for doc in js_content:
        print(f"  - {doc.content}")

if __name__ == "__main__":
    main()
```

## Related APIs

- **[MemoryEntry](./entry.md)** - Individual memory entry
- **[MemoryQuery](./memory-query.md)** - Query interface for searches
- **[Memory](./memory-interface.md)** - Custom memory interface
- **[LlmAgent](../core/llm-agent.md)** - Agent that uses memory

## See Also

- [Memory System Architecture](../../concept/memory.md)
- [Memory Integration Guide](../../guide/memory.md)
- [Custom Memory Backends](../../guide/custom-memory.md)
- [Memory Patterns and Best Practices](../../guide/memory-patterns.md)
